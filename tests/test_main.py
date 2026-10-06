import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from main import parse_args


class TestCommandLineOptions(unittest.TestCase):
    def test_defaults_are_preserved(self):
        options = parse_args([])

        self.assertEqual(options.delay, 1.0)
        self.assertEqual(options.grid_size, 4)

    def test_custom_delay_and_grid_size_are_parsed(self):
        options = parse_args(["--delay", "0.25", "--grid-size", "6"])

        self.assertEqual(options.delay, 0.25)
        self.assertEqual(options.grid_size, 6)

    def test_negative_delay_is_rejected(self):
        with self.assertRaises(SystemExit):
            parse_args(["--delay", "-1"])

    def test_small_grid_size_is_rejected(self):
        with self.assertRaises(SystemExit):
            parse_args(["--grid-size", "2"])
