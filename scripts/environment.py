from agent_state import AgentState
from direction import Direction

class WumpusEnvironment:

    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.agent = AgentState(x=1, y=1, direction=Direction.EAST)

        self.wumpus_pos = (1, 3)
        self.pits = {(3, 1), (3, 3)}
        self.gold_pos = (2, 3)
        self.wumpus_alive = True

        # Stores percept history: {(x, y): {"stench": bool, "breeze": bool, "glitter": bool}}
        self.discovered_percepts = {}

        # Log initial tile percepts at (1,1)
        self.record_current_percepts()

    def record_current_percepts(self):
        pos = (self.agent.x, self.agent.y)
        self.discovered_percepts[pos] = self.get_percepts()

    def get_percepts(self):
        x, y = self.agent.x, self.agent.y
        stench = (
            self._is_adjacent((x, y), self.wumpus_pos)
            if self.wumpus_alive
            else False
        )
        breeze = any(self._is_adjacent((x, y), pit) for pit in self.pits)
        glitter = (x, y) == self.gold_pos
        return {"stench": stench, "breeze": breeze, "glitter": glitter}

    def _is_adjacent(self, pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return (dx + dy) == 1

    def turn_left(self):
        if not self.agent.is_alive:
            return False

        self.agent.direction = self.agent.direction.turn_left()
        return True

    def turn_right(self):
        if not self.agent.is_alive:
            return False

        self.agent.direction = self.agent.direction.turn_right()
        return True

    def grab(self):
        if not self.agent.is_alive:
            return False

        if (self.agent.x, self.agent.y) != self.gold_pos:
            return False

        self.agent.has_gold = True
        return True

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

        if 1 <= new_x <= self.grid_size and 1 <= new_y <= self.grid_size:
            self.agent.x = new_x
            self.agent.y = new_y

            # Save percepts for the new cell
            self.record_current_percepts()

            if (
                self.agent.x,
                self.agent.y,
            ) == self.wumpus_pos and self.wumpus_alive:
                self.agent.is_alive = False
            elif (self.agent.x, self.agent.y) in self.pits:
                self.agent.is_alive = False
            return True
        else:
            return False