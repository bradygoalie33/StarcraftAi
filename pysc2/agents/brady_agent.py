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
_SELECT_UNIT = actions.FUNCTIONS.select_unit.id
_NOT_QUEUED = [0]
_SELECT_NEW = [0]
_SELECT_ALL = [0]

_SINGLE_SELECT = [0]
_TYPE_SELECT = [2]
testBool = True
apmRestrict = 0

      # 1 / move_camera                                      (1 / minimap[64, 64])
      # example of it working: return actions.FunctionCall(_MOVE_CAMERA, [(25,25)])

      # 3/select_rect                                        (7/select_add [2]; 0/screen [84, 84]; 2/screen2 [84, 84])
      # 331/Move_screen                                      (3/queued [2]; 0/screen [84, 84])
class StateMachine(base_agent.BaseAgent):
    def step(self, obs):
        notSelected = testBool
        global apmRestrict
        apmRestrict = apmRestrict
        if apmRestrict != 0:
            apmRestrict -= 1
            return Waiting.step(obs)
        if obs.observation["player"][1] > 150 and notSelected == True:
            global testBool
            testBool = False

            return actions.FunctionCall(_SELECT_RECTANGLE, [_SELECT_NEW, (0, 0), (64, 64)])
        elif testBool == False and len(obs.observation['multi_select']) > 0:
            # apmRestrict = 100
            return actions.FunctionCall(_SELECT_UNIT, [_TYPE_SELECT, [45]])
        else:
            return Waiting().step(obs)

class BuildABuilding(base_agent.BaseAgent):

  def step(self, obs):
    super(BuildABuilding, self).step(obs)
    notSelected = testBool
    global apmRestrict
    apmRestrict = apmRestrict
    if apmRestrict != 0:
        apmRestrict -= 1
        return actions.FunctionCall(_NO_OP, [])
    if obs.observation["player"][1] > 150 and notSelected == True:
      global testBool
      testBool = False
      # apmRestrict = 100
      return actions.FunctionCall(_SELECT_RECTANGLE, [_SELECT_NEW, (0, 0), (64, 64)])
    elif testBool == False and len(obs.observation['multi_select']) > 0:
        # apmRestrict = 100
        return actions.FunctionCall(_SELECT_UNIT, [_TYPE_SELECT, [45]])
    else:
      return Waiting().step(obs)
      # return actions.FunctionCall(_NO_OP, [])


class SelectEconDrone():
    def step(self, obs):
        print("SELECT DRONE")

class Build():
    def step(self, obs):
      print("Build")
      return actions.FunctionCall(_NO_OP, [])


class Waiting():
    def step(self, obs):
        return actions.FunctionCall(_NO_OP, [])
