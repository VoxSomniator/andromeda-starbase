# Immobile constructions in a level- walls, doors, windows etc.
# can take damage and be destroyed or rebuilt. Goes on top of floors, networks, and terrain.
#  Goes under entities but can be impassible.
from src.world.tiles import Tile

class Structure:

    def __init__(self, name, impassible=False, opaque=False, tile=Tile()):
        self.name = name
        self.impassible = impassible
        self.opaque = opaque
        self.tile = tile
