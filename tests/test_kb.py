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
        self.assertIsNone(self.knowledge_base.ask_next_unvisited_safe())


if __name__ == "__main__":
    unittest.main()
