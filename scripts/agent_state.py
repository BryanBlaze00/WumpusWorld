from direction import Direction

class AgentState:

    def __init__(self, x=1, y=1, direction=Direction.EAST):
        self.x = x  # 1 to 4 (Grid X)
        self.y = y  # 1 to 4 (Grid Y)
        self.direction = direction
        self.has_gold = False
        self.has_arrow = True
        self.is_alive = True