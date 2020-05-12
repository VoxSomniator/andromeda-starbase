# A game level. Terrain grids, entities, etc.
from src.world.tiles import Tile
from src.entities.entity import Entity

from src.entities.components import ai_jiggle, turn_taker


class Level():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.terrain = self.initialize_terrain()
        self.entities = []

    def initialize_terrain(self):
        # "terrain" is the bottom-most layer. True for Bulkhead, False for Vacuum.
        grid = [[False for y in range(self.height)] for x in range(self.width)]

        # make a square of bulkhead. temporary function remove later
        for x in range(10, 30):
            for y in range(10, 25):
                grid[x][y] = True

        return grid

    def add_entity(self, entity:Entity):
        entity.level = self
        self.entities.append(entity)

    def display_map(self):
        # returns an array of Tiles, whatever is to be displayed. Generally topmost items.
        # todo - change to display a section of the map, for scrolling viewport
        tiles = [[Tile('X', (255, 0, 0), (255, 255, 255)) for y in range(self.height)] for x in range(self.width)]

        # add terrain
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y]:
                    tiles[x][y] = Tile('▓', (120, 120, 120), (0, 0, 0))
                else:
                    tiles[x][y] = Tile('▓', (30, 10, 30), (0, 0, 0))

        # add entities
        for entity in self.entities:
            # check if entity in in bounds
            if entity.x < self.width and entity.x >=0 and entity.y < self.height and entity.y >= 0:

                # if entity has a tile, add it, or error character
                if isinstance(entity.tile, Tile):
                    tiles[entity.x][entity.y] = entity.tile
                else: tiles[entity.x][entity.y] = Tile('?', (255, 0, 255), (0, 255, 0))

        return tiles

    def is_square_blocked(self, x, y):
        # checks for solid obstructions- terrain or blocking entities.
        # todo - solid map bits
        # entities
        for entity in self.entities:
            if entity.x == x and entity.y == y and entity.solid:
                return True

        return False
