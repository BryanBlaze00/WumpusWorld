class KnowledgeBase:

    def __init__(self):
        self.visited = set()
        self.safe_cells = set()
        self.percepts = {}
        self.breeze_cells = set()
        self.stench_cells = set()
        self.glitter_cells = set()
        self.possible_pits = set()
        self.possible_wumpus = set()

    def tell(self, pos, percepts):
        """Ingest new percepts at pos and run logical deductions."""
        self.visited.add(pos)
        self.safe_cells.add(pos)
        self.percepts[pos] = dict(percepts)

        self._update_percept_cells(pos)

    def _update_percept_cells(self, pos):
        percepts = self.percepts[pos]

        self.breeze_cells.discard(pos)
        self.stench_cells.discard(pos)
        self.glitter_cells.discard(pos)

        if percepts["breeze"]:
            self.breeze_cells.add(pos)
        if percepts["stench"]:
            self.stench_cells.add(pos)
        if percepts["glitter"]:
            self.glitter_cells.add(pos)

    def ask_is_safe(self, pos):
        """Query if a cell is guaranteed safe."""
        return pos in self.safe_cells

    def ask_next_unvisited_safe(self):
        """Find adjacent or reachable safe unvisited cells."""
        unvisited = self.safe_cells - self.visited
        return unvisited.pop() if unvisited else None