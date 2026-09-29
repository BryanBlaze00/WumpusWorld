class KnowledgeBase:

    def __init__(self):
        self.visited = set()
        self.safe_cells = set()
        self.breeze_cells = set()
        self.stench_cells = set()
        self.possible_pits = set()
        self.possible_wumpus = set()

    def tell(self, pos, percepts):
        """Ingest new percepts at pos and run logical deductions."""
        self.visited.add(pos)
        self.safe_cells.add(pos)

        # Logical deduction rules go here...

    def ask_is_safe(self, pos):
        """Query if a cell is guaranteed safe."""
        return pos in self.safe_cells

    def ask_next_unvisited_safe(self):
        """Find adjacent or reachable safe unvisited cells."""
        unvisited = self.safe_cells - self.visited
        return unvisited.pop() if unvisited else None