from agent_state import AgentState
from direction import Direction

class WumpusEnvironment:

    def __init__(
        self,
        grid_size=4,
        wumpus_pos=(1, 3),
        pits=None,
        gold_pos=(2, 3),
    ):
        self.grid_size = grid_size
        self.start_pos = (1, 1)
        self.agent = AgentState(
            x=self.start_pos[0],
            y=self.start_pos[1],
            direction=Direction.EAST,
        )

        self.wumpus_pos = wumpus_pos
        self.pits = set(pits) if pits is not None else {(3, 1), (3, 3)}
        self.gold_pos = gold_pos
        self._validate_layout()
        self.wumpus_alive = True

        # Stores percept history: {(x, y): {"stench": bool, "breeze": bool, "glitter": bool}}
        self.discovered_percepts = {}

        # Log initial tile percepts at (1,1)
        self.record_current_percepts()

    def _validate_layout(self):
        if not isinstance(self.grid_size, int) or self.grid_size < 1:
            raise ValueError("grid_size must be a positive integer")

        positions = {
            "wumpus": self.wumpus_pos,
            "gold": self.gold_pos,
        }
        for name, position in positions.items():
            if not self._is_valid_position(position):
                raise ValueError(f"{name} position is outside the board")

        for pit in self.pits:
            if not self._is_valid_position(pit):
                raise ValueError("pit position is outside the board")

        start = (self.agent.x, self.agent.y)
        if self.wumpus_pos == start or self.gold_pos == start or start in self.pits:
            raise ValueError("the agent start position cannot contain an object")

        if self.wumpus_pos == self.gold_pos or self.wumpus_pos in self.pits:
            raise ValueError("hazard and gold positions cannot overlap")
        if self.gold_pos in self.pits:
            raise ValueError("hazard and gold positions cannot overlap")

    def _is_valid_position(self, position):
        return (
            isinstance(position, tuple)
            and len(position) == 2
            and all(isinstance(coordinate, int) for coordinate in position)
            and 1 <= position[0] <= self.grid_size
            and 1 <= position[1] <= self.grid_size
        )

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

    def is_won(self):
        return (
            self.agent.is_alive
            and self.agent.has_gold
            and (self.agent.x, self.agent.y) == self.start_pos
        )

    def shoot(self):
        if not self.agent.is_alive or not self.agent.has_arrow:
            return False

        self.agent.has_arrow = False

        dx, dy = 0, 0
        if self.agent.direction == Direction.NORTH:
            dy = 1
        elif self.agent.direction == Direction.EAST:
            dx = 1
        elif self.agent.direction == Direction.SOUTH:
            dy = -1
        elif self.agent.direction == Direction.WEST:
            dx = -1

        x, y = self.agent.x + dx, self.agent.y + dy
        while 1 <= x <= self.grid_size and 1 <= y <= self.grid_size:
            if (x, y) == self.wumpus_pos and self.wumpus_alive:
                self.wumpus_alive = False
                self.record_current_percepts()
                break
            x += dx
            y += dy

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