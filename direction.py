from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_left(self):
        return Direction((self.value - 1) % 4)

    def turn_right(self):
        return Direction((self.value + 1) % 4)