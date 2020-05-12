# geometry helper classes and utilities. Directions, rectangles, lines etc
from enum import Enum


# direction enums. So strings don't get wonky.
class Direction(Enum):
    n = 1
    ne = 2
    e = 3
    se = 4
    s = 5
    sw = 6
    w = 7
    nw = 8

# direction dictionary. Tuple vector offset things you know what it's for
# read when directions need to become coordinates, prefer storing Direction enum.
direction_coordinate = {
    Direction.n: (0, -1),
    Direction.ne: (1, -1),
    Direction.e: (1, 0),
    Direction.se: (1, 1),
    Direction.s: (0, 1),
    Direction.sw: (-1, 1),
    Direction.w: (-1, 0),
    Direction.nw: (-1, -1)
}