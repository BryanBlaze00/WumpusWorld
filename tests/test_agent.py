import sys
import unittest
from pathlib import Path


SCRIPTS_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

from agent import KBAgent
from direction import Direction


EMPTY_PERCEPTS = {"breeze": False, "stench": False, "glitter": False}


class TestKBAgentActions(unittest.TestCase):
    def test_glitter_takes_priority_over_navigation(self):
        agent = KBAgent()

        self.assertEqual(
            agent.choose_action(
                (1, 1),
                {"breeze": False, "stench": False, "glitter": True},
            ),
            "GRAB",
        )

    def test_agent_moves_toward_deterministically_selected_safe_target(self):
        agent = KBAgent()

        self.assertEqual(
            agent.choose_action((2, 2), EMPTY_PERCEPTS, Direction.NORTH),
            "TURN_LEFT",
        )

    def test_agent_turns_right_when_target_is_to_the_right(self):
        agent = KBAgent()
        agent.kb.tell((2, 2), EMPTY_PERCEPTS)

        self.assertEqual(
            agent.choose_action((2, 2), EMPTY_PERCEPTS, Direction.SOUTH),
            "TURN_RIGHT",
        )

    def test_agent_moves_forward_when_already_facing_target(self):
        agent = KBAgent()

        self.assertEqual(
            agent.choose_action((2, 2), EMPTY_PERCEPTS, Direction.WEST),
            "FORWARD",
        )

    def test_agent_does_not_target_possible_hazards(self):
        agent = KBAgent()

        self.assertEqual(
            agent.choose_action(
                (2, 2),
                {"breeze": True, "stench": True, "glitter": False},
                Direction.NORTH,
            ),
            agent.NO_ACTION,
        )

    def test_no_action_is_returned_when_no_safe_unvisited_route_exists(self):
        agent = KBAgent()
        agent.kb.tell((2, 2), EMPTY_PERCEPTS)
        agent.kb.visited.update(agent.kb.safe_cells)

        self.assertEqual(
            agent.choose_action((2, 2), EMPTY_PERCEPTS),
            agent.NO_ACTION,
        )

    def test_known_safe_route_can_reach_a_target_beyond_current_cell(self):
        agent = KBAgent()
        agent.kb.tell((1, 1), EMPTY_PERCEPTS)
        agent.kb.tell((2, 1), EMPTY_PERCEPTS)

        self.assertEqual(
            agent.choose_action((1, 1), EMPTY_PERCEPTS, Direction.EAST),
            "TURN_RIGHT",
        )


if __name__ == "__main__":
    unittest.main()
