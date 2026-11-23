from collections import deque

from direction import Direction
from kb import KnowledgeBase


class KBAgent:
    """Choose actions from percepts and facts recorded in a knowledge base."""

    NO_ACTION = "NO_ACTION"

    def __init__(self):
        """Create an agent with an empty knowledge base."""
        self.kb = KnowledgeBase()

    def choose_action(
        self,
        current_pos,
        percepts,
        direction=Direction.EAST,
    ):
        """Choose one safe action from the current position and percepts.

        The agent updates its knowledge before choosing an action. It never
        treats a possible pit or Wumpus cell as a navigation target. When a
        safe, unvisited cell is known, the shortest route through already
        known-safe cells is followed one action at a time. If no such route is
        available, ``NO_ACTION`` makes the unresolved state explicit.
        """
        self.kb.tell(current_pos, percepts)

        if percepts["glitter"]:
            return "GRAB"

        next_position = self._next_route_position(current_pos)
        if next_position is None:
            return self.NO_ACTION

        desired_direction = self._direction_to(current_pos, next_position)
        if direction == desired_direction:
            return "FORWARD"
        if direction.turn_left() == desired_direction:
            return "TURN_LEFT"
        return "TURN_RIGHT"

    def _next_route_position(self, current_pos):
        """Return the first step toward the nearest reachable safe target."""
        safe_cells = self.kb.safe_cells
        targets = safe_cells - self.kb.visited
        if not targets:
            return None

        queue = deque([(current_pos, [])])
        seen = {current_pos}
        while queue:
            position, path = queue.popleft()
            if position in targets:
                return path[0] if path else None

            for neighbor in sorted(self.kb._adjacent_positions(position)):
                if neighbor in seen or neighbor not in safe_cells:
                    continue
                seen.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
        return None

    @staticmethod
    def _direction_to(current_pos, next_position):
        """Return the cardinal direction from one adjacent cell to another."""
        dx = next_position[0] - current_pos[0]
        dy = next_position[1] - current_pos[1]
        directions = {
            (0, 1): Direction.NORTH,
            (1, 0): Direction.EAST,
            (0, -1): Direction.SOUTH,
            (-1, 0): Direction.WEST,
        }
        try:
            return directions[(dx, dy)]
        except KeyError as error:
            raise ValueError("route positions must be adjacent") from error