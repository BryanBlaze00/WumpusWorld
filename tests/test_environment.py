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

    def test_grab_collects_gold(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = environment.gold_pos

        result = environment.grab()

        self.assertTrue(result)
        self.assertTrue(environment.agent.has_gold)

    def test_grab_fails_away_from_gold(self):
        environment = WumpusEnvironment()

        result = environment.grab()

        self.assertFalse(result)
        self.assertFalse(environment.agent.has_gold)

    def test_dead_agent_cannot_grab_gold(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = environment.gold_pos
        environment.agent.is_alive = False

        result = environment.grab()

        self.assertFalse(result)
        self.assertFalse(environment.agent.has_gold)


class TestMovement(unittest.TestCase):
    def test_move_forward_in_each_direction(self):
        movements = (
            (Direction.NORTH, (1, 1), (1, 2)),
            (Direction.EAST, (1, 1), (2, 1)),
            (Direction.SOUTH, (2, 2), (2, 1)),
            (Direction.WEST, (2, 1), (1, 1)),
        )

        for direction, start, expected in movements:
            with self.subTest(direction=direction):
                environment = WumpusEnvironment()
                environment.agent.x, environment.agent.y = start
                environment.agent.direction = direction

                result = environment.move_forward()

                self.assertTrue(result)
                self.assertEqual(
                    (environment.agent.x, environment.agent.y),
                    expected,
                )

    def test_move_forward_at_wall_keeps_agent_in_place(self):
        wall_positions = (
            (Direction.NORTH, (1, 4)),
            (Direction.EAST, (4, 1)),
            (Direction.SOUTH, (1, 1)),
            (Direction.WEST, (1, 1)),
        )

        for direction, position in wall_positions:
            with self.subTest(direction=direction):
                environment = WumpusEnvironment()
                environment.agent.x, environment.agent.y = position
                environment.agent.direction = direction

                result = environment.move_forward()

                self.assertFalse(result)
                self.assertEqual(
                    (environment.agent.x, environment.agent.y),
                    position,
                )

    def test_dead_agent_cannot_move(self):
        environment = WumpusEnvironment()
        environment.agent.is_alive = False
        original_position = (environment.agent.x, environment.agent.y)

        result = environment.move_forward()

        self.assertFalse(result)
        self.assertEqual(
            (environment.agent.x, environment.agent.y),
            original_position,
        )


class TestShooting(unittest.TestCase):
    def test_shooting_in_wumpus_direction_kills_wumpus(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = (1, 1)
        environment.agent.direction = Direction.NORTH

        result = environment.shoot()

        self.assertTrue(result)
        self.assertFalse(environment.wumpus_alive)
        self.assertFalse(environment.agent.has_arrow)

    def test_missed_shot_consumes_arrow(self):
        environment = WumpusEnvironment()
        environment.agent.direction = Direction.EAST

        result = environment.shoot()

        self.assertTrue(result)
        self.assertTrue(environment.wumpus_alive)
        self.assertFalse(environment.agent.has_arrow)

    def test_second_shot_is_rejected(self):
        environment = WumpusEnvironment()

        self.assertTrue(environment.shoot())
        self.assertFalse(environment.shoot())
        self.assertFalse(environment.agent.has_arrow)

    def test_dead_agent_cannot_shoot(self):
        environment = WumpusEnvironment()
        environment.agent.is_alive = False

        result = environment.shoot()

        self.assertFalse(result)
        self.assertTrue(environment.agent.has_arrow)
        self.assertTrue(environment.wumpus_alive)


class TestHazardsAndPercepts(unittest.TestCase):
    def test_entering_pit_kills_agent(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = (2, 1)
        environment.agent.direction = Direction.EAST

        result = environment.move_forward()

        self.assertTrue(result)
        self.assertEqual((environment.agent.x, environment.agent.y), (3, 1))
        self.assertFalse(environment.agent.is_alive)

    def test_entering_live_wumpus_kills_agent(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = (1, 2)
        environment.agent.direction = Direction.NORTH

        result = environment.move_forward()

        self.assertTrue(result)
        self.assertEqual((environment.agent.x, environment.agent.y), (1, 3))
        self.assertFalse(environment.agent.is_alive)

    def test_breeze_is_detected_adjacent_to_pit(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = (2, 1)

        percepts = environment.get_percepts()

        self.assertTrue(percepts["breeze"])

    def test_stench_is_detected_adjacent_to_wumpus(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = (1, 2)

        percepts = environment.get_percepts()

        self.assertTrue(percepts["stench"])

    def test_glitter_is_detected_on_gold_cell(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = environment.gold_pos

        percepts = environment.get_percepts()

        self.assertTrue(percepts["glitter"])


if __name__ == "__main__":
    unittest.main()
