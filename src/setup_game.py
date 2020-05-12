# holds all the initialization for launching the game. Constants for the console, then world start stuff.
# probably split up later into a world creation system.

import tcod

def get_constants():
    constants = {
        'window_title': 'Andromeda Starbase',
        'screen_width': 90,
        'screen_height': 55,
        'renderer': tcod.RENDERER_SDL2
    }

    return constants