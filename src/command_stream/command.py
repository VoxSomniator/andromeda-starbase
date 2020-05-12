# Various control events. Input handler creates these, they're processed by engine.
# Type is an event type enum like Move or Inventory. Data is movement direction or other values or just True.
from enum import Enum


class CommandType(Enum):
    quit = 1  # game is quit. data is True.
    menuclose = 2  # a menu is closed. Not the game- inventory, etc. data is True.
    move = 3  # player moves. data is direction?


class Command:
    def __init__(self, command_type:CommandType, data):
        self.command_type = command_type
        self.data = data
