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


class TestBoardLayouts(unittest.TestCase):
    def test_custom_layout_is_used(self):
        environment = WumpusEnvironment(
            grid_size=5,
            wumpus_pos=(5, 5),
            pits={(2, 2), (4, 4)},
            gold_pos=(3, 5),
        )

        self.assertEqual(environment.grid_size, 5)
        self.assertEqual(environment.wumpus_pos, (5, 5))
        self.assertEqual(environment.pits, {(2, 2), (4, 4)})
        self.assertEqual(environment.gold_pos, (3, 5))

    def test_default_layout_is_unchanged(self):
        environment = WumpusEnvironment()

        self.assertEqual(environment.grid_size, 4)
        self.assertEqual(environment.wumpus_pos, (1, 3))
        self.assertEqual(environment.pits, {(3, 1), (3, 3)})
        self.assertEqual(environment.gold_pos, (2, 3))

    def test_rejects_invalid_layout_positions(self):
        invalid_layouts = (
            {"wumpus_pos": (5, 5)},
            {"pits": {(0, 2)}},
            {"gold_pos": (1, 1)},
            {"wumpus_pos": (2, 2), "gold_pos": (2, 2)},
        )

        for layout in invalid_layouts:
            with self.subTest(layout=layout):
                with self.assertRaises(ValueError):
                    WumpusEnvironment(**layout)


class TestRandomizedLayouts(unittest.TestCase):
    def test_seeded_layouts_are_repeatable(self):
        first = WumpusEnvironment(randomize=True, seed=7)
        second = WumpusEnvironment(randomize=True, seed=7)

        self.assertEqual(first.wumpus_pos, second.wumpus_pos)
        self.assertEqual(first.pits, second.pits)
        self.assertEqual(first.gold_pos, second.gold_pos)

    def test_different_seeds_can_produce_different_layouts(self):
        first = WumpusEnvironment(randomize=True, seed=7)
        second = WumpusEnvironment(randomize=True, seed=8)

        self.assertNotEqual(
            (first.wumpus_pos, first.pits, first.gold_pos),
            (second.wumpus_pos, second.pits, second.gold_pos),
        )

    def test_randomized_layout_respects_constraints(self):
        environment = WumpusEnvironment(
            grid_size=5,
            randomize=True,
            seed=7,
            pit_count=5,
        )
        objects = {environment.wumpus_pos, environment.gold_pos}
        objects.update(environment.pits)

        self.assertEqual(len(environment.pits), 5)
        self.assertNotIn((1, 1), objects)
        self.assertEqual(len(objects), 7)

    def test_randomized_layout_rejects_too_many_pits(self):
        with self.assertRaises(ValueError):
            WumpusEnvironment(grid_size=2, randomize=True, pit_count=3)

    def test_randomized_grid_size_stays_within_range(self):
        environment = WumpusEnvironment(
            grid_size_range=(4, 6),
            randomize=True,
            seed=7,
        )

        self.assertIn(environment.grid_size, (4, 5, 6))

    def test_randomized_pit_count_matches_grid_size(self):
        for grid_size in (4, 5, 6):
            with self.subTest(grid_size=grid_size):
                environment = WumpusEnvironment(
                    grid_size=grid_size,
                    randomize=True,
                    seed=7,
                    randomize_start=True,
                )

                self.assertEqual(len(environment.pits), grid_size - 1)

    def test_randomized_start_area_is_protected(self):
        environment = WumpusEnvironment(
            grid_size=6,
            randomize=True,
            seed=7,
            randomize_start=True,
        )
        protected = environment._protected_start_positions(environment.start_pos)
        objects = {environment.wumpus_pos, environment.gold_pos}
        objects.update(environment.pits)

        self.assertTrue(protected.isdisjoint(objects))

    def test_randomized_layout_is_repeatable(self):
        options = {
            "grid_size_range": (4, 10),
            "randomize": True,
            "seed": 7,
            "randomize_start": True,
        }
        first = WumpusEnvironment(**options)
        second = WumpusEnvironment(**options)

        self.assertEqual(first.grid_size, second.grid_size)
        self.assertEqual(first.start_pos, second.start_pos)
        self.assertEqual(first.wumpus_pos, second.wumpus_pos)
        self.assertEqual(first.pits, second.pits)
        self.assertEqual(first.gold_pos, second.gold_pos)


class TestWinCondition(unittest.TestCase):
    def test_gold_cell_does_not_win_until_agent_returns_home(self):
        environment = WumpusEnvironment()
        environment.agent.x, environment.agent.y = environment.gold_pos

        self.assertTrue(environment.grab())
        self.assertFalse(environment.is_won())

    def test_agent_with_gold_wins_at_start(self):
        environment = WumpusEnvironment()
        environment.agent.has_gold = True

        self.assertTrue(environment.is_won())

    def test_agent_without_gold_does_not_win_at_start(self):
        environment = WumpusEnvironment()

        self.assertFalse(environment.is_won())

    def test_dead_agent_does_not_win_at_start(self):
        environment = WumpusEnvironment()
        environment.agent.has_gold = True
        environment.agent.is_alive = False

        self.assertFalse(environment.is_won())


if __name__ == "__main__":
    unittest.main()
