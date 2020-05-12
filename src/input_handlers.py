import tcod
import tcod.event
from src.command_stream.command import Command, CommandType
from src.geometry import Direction

DIRECTION_KEYS = {  # key_symbol: Direction
    # dictionary of direction keys to the directions, read by handle_keys.
    # numpad keys. Add arrows/VI keys later.
    tcod.event.K_KP_8: Direction.n,
    tcod.event.K_KP_9: Direction.ne,
    tcod.event.K_KP_6: Direction.e,
    tcod.event.K_KP_3: Direction.se,
    tcod.event.K_KP_2: Direction.s,
    tcod.event.K_KP_1: Direction.sw,
    tcod.event.K_KP_4: Direction.w,
    tcod.event.K_KP_7: Direction.nw,
}

def handle_keys():
    # returns a Command object based on state and input.

    # get the first event in the iterator- keymashing between frames won't advance multiple turns.
    first_event = None
    for event in tcod.event.get():
        if first_event is None:
            first_event = event
    event = first_event

    if event is None:
        return

    if event.type == 'WINDOWCLOSE':
        return Command(CommandType.quit, True)

    if event.type == 'KEYDOWN':
        if event.sym == tcod.event.K_ESCAPE:
            return Command(CommandType.quit, True)
        if event.sym in DIRECTION_KEYS.keys():
            return Command(CommandType.move, DIRECTION_KEYS[event.sym])

    return

