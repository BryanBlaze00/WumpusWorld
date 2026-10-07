import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from randommain import parse_args


class TestRandomMainOptions(unittest.TestCase):
    def test_seed_defaults_to_none(self):
        options = parse_args([])

        self.assertIsNone(options.seed)

    def test_seed_is_parsed(self):
        options = parse_args(["--seed", "123"])

        self.assertEqual(options.seed, 123)

    def test_invalid_seed_is_rejected(self):
        with self.assertRaises(SystemExit):
            parse_args(["--seed", "not-a-number"])


if __name__ == "__main__":
    unittest.main()
