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

        # component slots. As much as I wanted to just have a list of components, this makes everything
        #  interact/check nicer.
        # components are added post-instantiation.
        self.ai = None
        self.turn_taker = None
        self.player = None
        self.stats = None

        self.level = None  # the level this entity is in. Filled out when the entity is added to a level in level.py

    def move(self, direction:Direction):
        # move by 1 tile in given direction

        (dx, dy) = direction_coordinate[direction]
        target_x = self.x + dx
        target_y = self.y + dy

        if self.level.is_square_blocked(target_x, target_y):
            return

        self.x = target_x
        self.y = target_y

        if self.stats:
            self.change_energy(-self.stats.move_cost)

        # reduce energy.

    def change_energy(self, difference):
        # alters TurnTaker's energy if it has one.
        # returns True if a turntaker exists, false otherwise.
        if self.turn_taker:
            self.turn_taker.change_energy(difference)
            return True
        else:
            return False
