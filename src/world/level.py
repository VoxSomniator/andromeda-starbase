# A game level. Terrain grids, entities, etc.
from src.world.tiles import Tile
from src.entities.entity import Entity
from src.world.structure import Structure
import tcod


class Level():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.terrain = self.initialize_terrain()
        # todo - floors
        # todo - networks
        self.structures = self.initialize_structures()
        self.entities = []

    def initialize_terrain(self):
        # "terrain" is the bottom-most layer. True for Bulkhead, False for Vacuum.
        grid = [[False for y in range(self.height)] for x in range(self.width)]

        # make a square of bulkhead. temporary function remove later
        for x in range(10, 30):
            for y in range(10, 25):
                grid[x][y] = True

        return grid

    def initialize_structures(self):
        # "structures" go on top of terrain. Objects for walls, windows, doors- only one structure per square.
        #  goes on top of Floors and Terrains.
        # default value of a square with no structure is False.
        grid = [[False for y in range(self.height)] for x in range(self.width)]

        # add one wall.
        for y in range(10, 25):
            grid[13][y] = Structure('wall', True, True, Tile('╬', (200, 200, 200)))

        return grid

    def get_fov_map(self):
        # returns the opacity/solidity map for this level.
        fov_map = tcod.map.Map(self.width, self.height)

        for x in range(self.width):
            for y in range(self.height):
                fov_map.walkable[y][x] = not self.is_square_blocked(x, y)
                fov_map.transparent[y][x] = not self.is_square_opaque(x, y)

        return fov_map

    def add_entity(self, entity:Entity):
        entity.level = self
        self.entities.append(entity)

    def get_tile_at(self, x, y, void_tile:Tile=Tile()):
        # returns the tile for a specific coordinate. Entities on top, then constructions, floors, networks, and terrain.
        # if coordinates are out of level bound, return void tile.

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return void_tile

        location_entities = []
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                location_entities.append(entity)
        # eventually add entity ordering here, like creatures being on top of items. For now just return the first.
        if location_entities:
            return location_entities[0].tile

        if self.structures[x][y]:
            return self.structures[x][y].tile

        # terrain hardcoding. Either make this work more like terrain later, or just make the hardcoded values
        #  constants/level-dependent variables.
        if self.terrain[x][y]:
            return Tile('▓', (120, 120, 120), (0, 0, 0))
        elif not self.terrain[x][y]:
            return Tile('▓', (30, 10, 30), (0, 0, 0))

        # if this appears something has gone terribly wrong or I forgot to implement a new type of thing
        return Tile('!', (255, 0, 0), (0, 0, 0))

    def get_rect_tiles(self, start_x:int, start_y:int, width:int, height:int, void_tile:Tile=Tile()):
        # returns a grid of tiles for a specific subsection of the map, with void_tile for out-of-bounds squares.
        # start_x and start_y CAN be negative! Width and height should be positive.
        tiles= [[Tile('X', (255, 0, 0), (255, 255, 255)) for y in range(height)] for x in range(width)]

        # the tile grid, representing the screen, will be iterated over.
        # for every tile grid coordinate, add the start_x and _y values to get the world coordinate.
        # if it's out of world bounds, add the void_tile.

        # note to self don't mix up width and self.width

        for x in range(width):
            for y in range(height):
                world_x = x + start_x
                world_y = y + start_y
                if world_x < 0 or world_x >= self.width or world_y < 0 or world_y >= self.height:
                    # tile out of bounds
                    tiles[x][y] = void_tile
                else:
                    # tile in bounds hooray
                    tiles[x][y] = self.get_tile_at(world_x, world_y)

        return tiles

    def get_rect_tiles_in_fov(self, start_x:int, start_y:int, width:int, height:int, void_tile:Tile=Tile(),
                              fov_entity:Entity=None, unseen_tile=Tile('X', (0, 0, 255))):
        # works like get_rect_tiles, except tiles outside an entity's FOV are covered with unseen_tile.
        # if there's no entity, just returns the same as get_rect_tiles.
        if not fov_entity:
            return self.get_rect_tiles(start_x, start_y, width, height, void_tile)
        else:
            tiles= [[Tile('X', (255, 0, 0), (255, 255, 255)) for y in range(height)] for x in range(width)]

            for x in range(width):
                for y in range(height):
                    world_x = x + start_x
                    world_y = y + start_y
                    if world_x < 0 or world_x >= self.width or world_y < 0 or world_y >= self.height:
                        tiles[x][y] = void_tile
                    else:
                        if fov_entity.vision and fov_entity.vision.is_square_visible(world_x, world_y):
                            tiles[x][y] = self.get_tile_at(world_x, world_y)
                        else:
                            tiles[x][y] = unseen_tile

            return tiles


    def is_square_blocked(self, x, y):
        # checks for solid obstructions- terrain or blocking entities.
        # bounds
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        # structures
        if self.structures[x][y]:
            if self.structures[x][y].impassible:
                return True
        # entities
        for entity in self.entities:
            if entity.x == x and entity.y == y and entity.solid:
                return True

        return False

    def is_square_opaque(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        # structures
        if self.structures[x][y]:
            if self.structures[x][y].opaque:
                return True

        return False
