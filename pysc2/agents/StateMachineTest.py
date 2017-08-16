
# StateMachine/mousetrap1/MouseTrapTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
import string, sys
sys.path += ['../stateMachine', '../mouse']
from State import State
from StateMachine import StateMachine
from pysc2.agents import base_agent

# A different subclass for each state:

class Waiting(State):
    def run(self):
        print("Waiting: Broadcasting cheese smell")
        return MouseTrap.luring

    def next(self):
        return MouseTrap.luring

class Luring(State):
    def run(self):
        print("Luring: Presenting Cheese, door open")
        return MouseTrap.waiting

    def next(self):
        return MouseTrap.waiting


class MouseTrap(StateMachine, base_agent.BaseAgent):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, MouseTrap.waiting)

# Static variable initialization:
MouseTrap.waiting = Waiting()
MouseTrap.luring = Luring()
