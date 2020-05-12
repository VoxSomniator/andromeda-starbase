# Player control pseudo-AI.
# passed a Game object on game start. When prompted for its turn, tells the game to switch to
#  PLAYER_TURN state and ask for input.

from src.entities.components.component import Component


class Player(Component):

    def __init__(self, owner, game):
        Component.init(self, owner)
        self.game = game

    def turn(self):
        print ("player turn!")
        # call engine function