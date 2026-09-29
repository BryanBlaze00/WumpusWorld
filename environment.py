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

class AgentState:
    def __init__(self, x=1, y=1, direction=Direction.EAST):
        self.x = x  # 1 to 4 (Grid X)
        self.y = y  # 1 to 4 (Grid Y)
        self.direction = direction
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True

class WumpusEnvironment:
    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.agent = AgentState(x=1, y=1, direction=Direction.EAST)

        # 1-indexed coordinates matching AI textbook specs
        self.wumpus_pos = (1, 3)
        self.pits = {(3, 1), (3, 3)}
        self.gold_pos = (2, 3)
        self.wumpus_alive = True

    def get_percepts(self):
        x, y = self.agent.x, self.agent.y

        stench = self._is_adjacent((x, y), self.wumpus_pos) if self.wumpus_alive else False
        breeze = any(self._is_adjacent((x, y), pit) for pit in self.pits)
        glitter = (x, y) == self.gold_pos

        return {"stench": stench, "breeze": breeze, "glitter": glitter}

    def _is_adjacent(self, pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return (dx + dy) == 1

    def move_forward(self):
        if not self.agent.is_alive:
            return False

        dx, dy = 0, 0
        if self.agent.direction == Direction.NORTH:
            dy = 1
        elif self.agent.direction == Direction.EAST:
            dx = 1
        elif self.agent.direction == Direction.SOUTH:
            dy = -1
        elif self.agent.direction == Direction.WEST:
            dx = -1

        new_x = self.agent.x + dx
        new_y = self.agent.y + dy

        # Check 1-indexed grid boundaries (1 to 4)
        if 1 <= new_x <= self.grid_size and 1 <= new_y <= self.grid_size:
            self.agent.x = new_x
            self.agent.y = new_y

            if (self.agent.x, self.agent.y) == self.wumpus_pos and self.wumpus_alive:
                self.agent.is_alive = False
            elif (self.agent.x, self.agent.y) in self.pits:
                self.agent.is_alive = False
            return True
        else:
            return False  # Bumped into a wall