# Player control pseudo-AI.
# really just a flag for "this is player!"
from src.entities.components.component import Component


class Player(Component):

    def __init__(self, owner):
        Component.__init__(self, owner)

    def turn(self):
        print ("player turn! this really should not have been called.")