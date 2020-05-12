# In-world entities like items and creatures.
# Basically everything except terrain and networks.
from src.entities.components.component import Component
from src.entities.components.turn_taker import TurnTaker
from src.geometry import Direction, direction_coordinate
from src.world.tiles import Tile


class Entity:
    # Fancy entity using ECS. The basics of being a thing existing in the world.

    def __init__(self, name='???', tile:Tile=Tile('?', (255, 0, 255)), x=0, y=0, solid=False):
        self.name = name
        self.tile = tile
        self.x = x
        self.y = y
        self.solid = solid  # does the entity block movement into its square?
        self.components = []

        self.level = None  # the level this entity is in. Filled out when the entity is added to a level in level.py

        # if the component list is only one component, change it to a list. In case I use this wrong later.
        if isinstance(self.components, Component):
            self.components = [self.components]

    def add_component(self, component:Component):
        self.components.append(component)

    def move(self, direction:Direction):
        # move by 1 tile in given direction

        (dx, dy) = direction_coordinate[direction]
        target_x = self.x + dx
        target_y = self.y + dy

        if self.level.is_square_blocked(target_x, target_y):
            return

        self.x = target_x
        self.y = target_y

        # reduce energy.
        # todo - incorporate Creature Stats
        self.change_energy(-1000)

    def change_energy(self, difference):
        # alters TurnTaker's energy if it has one.
        # returns True if a turntaker exists, false otherwise.
        turn_taker = next((component for component in self.components if isinstance(component, TurnTaker)), None)
        if turn_taker:
            turn_taker.change_energy(difference)
            return True
        else:
            return False
