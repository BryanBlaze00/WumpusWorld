import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPTS_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

from environment import WumpusEnvironment
from renderer import BoardRenderer


class TestBoardRenderer(unittest.TestCase):
    def test_custom_layout_is_visible_in_rendered_board(self):
        environment = WumpusEnvironment(
            grid_size=3,
            wumpus_pos=(3, 3),
            pits={(2, 1)},
            gold_pos=(1, 3),
        )
        output = io.StringIO()

        with redirect_stdout(output):
            BoardRenderer(environment).render()

        rendered_board = output.getvalue()
        self.assertIn("👹", rendered_board)
        self.assertIn("🕳️", rendered_board)
        self.assertIn("🪙", rendered_board)
        self.assertEqual(rendered_board.count("┌"), 1)
        self.assertEqual(rendered_board.count("└"), 1)

    def test_ascii_fallback_is_readable(self):
        environment = WumpusEnvironment(
            grid_size=3,
            wumpus_pos=(3, 3),
            pits={(2, 1)},
            gold_pos=(1, 3),
        )
        output = io.StringIO()

        with redirect_stdout(output):
            BoardRenderer(environment).render(use_unicode=False)

        rendered_board = output.getvalue()
        self.assertIn(" W  ", rendered_board)
        self.assertIn(" P  ", rendered_board)
        self.assertIn(" G  ", rendered_board)
        self.assertEqual(rendered_board.count("+"), 16)
        self.assertNotIn("👹", rendered_board)


if __name__ == "__main__":
    unittest.main()
