import sys
import unittest
from pathlib import Path


SCRIPTS_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

from direction import Direction
from environment import WumpusEnvironment


class TestTurningActions(unittest.TestCase):
    def test_turn_left_changes_direction(self):
        environment = WumpusEnvironment()
        environment.agent.direction = Direction.NORTH

        result = environment.turn_left()

        self.assertTrue(result)
        self.assertEqual(environment.agent.direction, Direction.WEST)

    def test_turn_right_changes_direction(self):
        environment = WumpusEnvironment()
        environment.agent.direction = Direction.NORTH

        result = environment.turn_right()

        self.assertTrue(result)
        self.assertEqual(environment.agent.direction, Direction.EAST)

    def test_four_turns_return_to_original_direction(self):
        environment = WumpusEnvironment()
        original_direction = environment.agent.direction

        for _ in range(4):
            environment.turn_right()

        self.assertEqual(environment.agent.direction, original_direction)

    def test_dead_agent_cannot_turn(self):
        environment = WumpusEnvironment()
        environment.agent.is_alive = False
        original_direction = environment.agent.direction

        result = environment.turn_right()

        self.assertFalse(result)
        self.assertEqual(environment.agent.direction, original_direction)


if __name__ == "__main__":
    unittest.main()
