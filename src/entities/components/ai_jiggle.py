# testing AI, makes the entity random-walk around
from src.entities.components.component import Component
from src.geometry import Direction
import random


class AiJiggle(Component):

    def __init__(self, owner):
        Component.__init__(self, owner)

    def turn(self):
        # implement "turn" methods in any ai components
        # todo - ai component superclass?
        self.owner.move(random.choice(list(Direction)))