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
        self.percepts[pos] = dict(percepts)

        self._update_percept_cells(pos)
        self._recompute_inferences()

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

    @staticmethod
    def _adjacent_positions(pos):
        x, y = pos
        return {
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        }

    def _recompute_inferences(self):
        """Derive safe cells and possible hazards from all recorded percepts."""
        possible_pits = set()
        possible_wumpus = set()
        pit_free_cells = set()
        wumpus_free_cells = set()

        for pos, percepts in self.percepts.items():
            adjacent = self._adjacent_positions(pos)
            if percepts["breeze"]:
                possible_pits.update(adjacent)
            else:
                pit_free_cells.update(adjacent)
            if percepts["stench"]:
                possible_wumpus.update(adjacent)
            else:
                wumpus_free_cells.update(adjacent)

        safe_cells = set(self.visited) | (pit_free_cells & wumpus_free_cells)
        self.safe_cells = safe_cells
        self.possible_pits = possible_pits - pit_free_cells - safe_cells
        self.possible_wumpus = possible_wumpus - wumpus_free_cells - safe_cells

    def ask_is_safe(self, pos):
        """Query if a cell is guaranteed safe."""
        return pos in self.safe_cells

    def ask_next_unvisited_safe(self):
        """Find adjacent or reachable safe unvisited cells."""
        unvisited = self.safe_cells - self.visited
        return min(unvisited) if unvisited else None