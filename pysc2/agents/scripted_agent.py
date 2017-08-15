# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
from random import randint

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_IDLE_WORKER = actions.FUNCTIONS.select_idle_worker.id
_SELECT_RECTANGLE = actions.FUNCTIONS.select_rect.id
_MOVE_CAMERA = actions.FUNCTIONS.move_camera.id
_NOT_QUEUED = [0]
_SELECT_ADD = [0]
_SELECT_ALL = [0]
testBool = True


class MoveToBeacon(base_agent.BaseAgent):
  """An agent specifically for solving the MoveToBeacon map."""

  def step(self, obs):
    super(MoveToBeacon, self).step(obs)
    if _MOVE_SCREEN in obs.observation["available_actions"]:
      player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
      neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
      if not neutral_y.any():
        return actions.FunctionCall(_NO_OP, [])
      target = [int(neutral_x.mean()), int(neutral_y.mean())]
      return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, target])
    else:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])

      # 1 / move_camera                                      (1 / minimap[64, 64])
      # example of it working: return actions.FunctionCall(_MOVE_CAMERA, [(25,25)])

      # 3/select_rect                                        (7/select_add [2]; 0/screen [84, 84]; 2/screen2 [84, 84])
      # 331/Move_screen                                      (3/queued [2]; 0/screen [84, 84])

class BuildABuilding(base_agent.BaseAgent) :
  notSelected = True
  def step(self, obs):
    super(BuildABuilding, self).step(obs)
    notSelected = testBool
    rand1 = randint(0, 83)
    rand2 = randint(0, 83)
    rand3 = randint(0, 83)
    rand4 = randint(0, 83)

    if obs.observation["player"][1] > 150 and notSelected == True:
      global testBool
      testBool = False
      return actions.FunctionCall(_SELECT_RECTANGLE, [_SELECT_ADD, (0, 0), (64, 64)])

    # if(len(obs.observation["multi_select"]) != 2):
    #     print("reselect")
    #     return actions.FunctionCall(_SELECT_RECTANGLE, [_SELECT_ADD, (rand1,rand2), (rand3,rand4)])
    elif testBool == False:
      return actions.FunctionCall(5, [_SELECT_ADD, 45])
    else:
      # all_selected = obs.observation["multi_select"]
      # selected_drone = None
      # for unit in all_selected:
      #   if(unit[0] == 84 or unit[0] == 104 or unit[0] == 45):
      #     selected_drone = unit
      #     break
      # print(selected_drone)
      return actions.FunctionCall(_NO_OP, [])


class CollectMineralShards(base_agent.BaseAgent):
  """An agent specifically for solving the CollectMineralShards map."""

  def step(self, obs):
    super(CollectMineralShards, self).step(obs)
    if _MOVE_SCREEN in obs.observation["available_actions"]:
      player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
      neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
      player_y, player_x = (player_relative == _PLAYER_FRIENDLY).nonzero()
      if not neutral_y.any() or not player_y.any():
        return actions.FunctionCall(_NO_OP, [])
      player = [int(player_x.mean()), int(player_y.mean())]
      closest, min_dist = None, None
      for p in zip(neutral_x, neutral_y):
        dist = numpy.linalg.norm(numpy.array(player) - numpy.array(p))
        if not min_dist or dist < min_dist:
          closest, min_dist = p, dist
      return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, closest])  # example of var closest: (28, 32)
    else:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


class DefeatRoaches(base_agent.BaseAgent):
  """An agent specifically for solving the DefeatRoaches map."""

  def step(self, obs):
    super(DefeatRoaches, self).step(obs)
    if _ATTACK_SCREEN in obs.observation["available_actions"]:
      player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
      roach_y, roach_x = (player_relative == _PLAYER_HOSTILE).nonzero()
      if not roach_y.any():
        return actions.FunctionCall(_NO_OP, [])
      index = numpy.argmax(roach_y)
      target = [roach_x[index], roach_y[index]]
      return actions.FunctionCall(_ATTACK_SCREEN, [_NOT_QUEUED, target])
    else:
      return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
