from enum import Enum


class Direction(Enum):
    """Represent the four cardinal orientations used by the agent."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_left(self):
        """Return the orientation one quarter-turn counterclockwise."""
        return Direction((self.value - 1) % 4)

    def turn_right(self):
        """Return the orientation one quarter-turn clockwise."""
        return Direction((self.value + 1) % 4)