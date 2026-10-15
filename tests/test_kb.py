import sys
import unittest
from pathlib import Path


SCRIPTS_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

from kb import KnowledgeBase


class TestKnowledgeBasePercepts(unittest.TestCase):
    def setUp(self):
        self.knowledge_base = KnowledgeBase()
        self.position = (2, 2)

    def test_tell_records_visited_safe_and_percepts(self):
        percepts = {"breeze": True, "stench": False, "glitter": True}

        self.knowledge_base.tell(self.position, percepts)

        self.assertIn(self.position, self.knowledge_base.visited)
        self.assertIn(self.position, self.knowledge_base.safe_cells)
        self.assertEqual(self.knowledge_base.percepts[self.position], percepts)

    def test_tell_tracks_positive_percepts(self):
        percepts = {"breeze": True, "stench": True, "glitter": True}

        self.knowledge_base.tell(self.position, percepts)

        self.assertIn(self.position, self.knowledge_base.breeze_cells)
        self.assertIn(self.position, self.knowledge_base.stench_cells)
        self.assertIn(self.position, self.knowledge_base.glitter_cells)

    def test_tell_does_not_track_false_percepts(self):
        percepts = {"breeze": False, "stench": False, "glitter": False}

        self.knowledge_base.tell(self.position, percepts)

        self.assertNotIn(self.position, self.knowledge_base.breeze_cells)
        self.assertNotIn(self.position, self.knowledge_base.stench_cells)
        self.assertNotIn(self.position, self.knowledge_base.glitter_cells)

    def test_retelling_position_updates_percepts(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": True, "stench": True, "glitter": True},
        )
        self.knowledge_base.tell(
            self.position,
            {"breeze": False, "stench": False, "glitter": False},
        )

        self.assertEqual(
            self.knowledge_base.percepts[self.position],
            {"breeze": False, "stench": False, "glitter": False},
        )
        self.assertNotIn(self.position, self.knowledge_base.breeze_cells)
        self.assertNotIn(self.position, self.knowledge_base.stench_cells)
        self.assertNotIn(self.position, self.knowledge_base.glitter_cells)
        self.assertEqual(len(self.knowledge_base.visited), 1)

    def test_safe_queries_remain_consistent(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": False, "stench": False, "glitter": False},
        )

        self.assertTrue(self.knowledge_base.ask_is_safe(self.position))
        self.assertEqual(
            self.knowledge_base.ask_next_unvisited_safe(),
            (1, 2),
        )


class TestKnowledgeBaseInference(unittest.TestCase):
    def setUp(self):
        self.knowledge_base = KnowledgeBase()
        self.position = (2, 2)

    def test_empty_percepts_mark_adjacent_cells_safe(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": False, "stench": False, "glitter": False},
        )

        adjacent = {(1, 2), (3, 2), (2, 1), (2, 3)}

        self.assertTrue(adjacent.issubset(self.knowledge_base.safe_cells))
        self.assertFalse(self.knowledge_base.possible_pits)
        self.assertFalse(self.knowledge_base.possible_wumpus)

    def test_breeze_tracks_possible_pits_without_marking_them_safe(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": True, "stench": False, "glitter": False},
        )

        adjacent = {(1, 2), (3, 2), (2, 1), (2, 3)}

        self.assertEqual(self.knowledge_base.possible_pits, adjacent)
        self.assertFalse(adjacent & self.knowledge_base.safe_cells)

    def test_stench_tracks_possible_wumpus_without_marking_them_safe(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": False, "stench": True, "glitter": False},
        )

        adjacent = {(1, 2), (3, 2), (2, 1), (2, 3)}

        self.assertEqual(self.knowledge_base.possible_wumpus, adjacent)
        self.assertFalse(adjacent & self.knowledge_base.safe_cells)

    def test_safe_observation_removes_cells_from_hazard_candidates(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": True, "stench": True, "glitter": False},
        )
        self.knowledge_base.tell(
            (2, 3),
            {"breeze": False, "stench": False, "glitter": False},
        )

        self.assertNotIn((2, 3), self.knowledge_base.possible_pits)
        self.assertNotIn((2, 3), self.knowledge_base.possible_wumpus)
        self.assertIn((2, 3), self.knowledge_base.safe_cells)

    def test_next_safe_cell_selection_is_deterministic(self):
        self.knowledge_base.tell(
            self.position,
            {"breeze": False, "stench": False, "glitter": False},
        )

        self.assertEqual(
            self.knowledge_base.ask_next_unvisited_safe(),
            (1, 2),
        )


if __name__ == "__main__":
    unittest.main()
