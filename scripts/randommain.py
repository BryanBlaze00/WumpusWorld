import argparse
import random

from environment import WumpusEnvironment
from renderer import BoardRenderer


def parse_args(args=None):
    """Parse the optional seed used to reproduce a randomized board."""
    parser = argparse.ArgumentParser(
        description="Render a randomized Wumpus World board."
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="seed used to reproduce the randomized board",
    )
    return parser.parse_args(args)


def main(args=None):
    """Create and render a seeded or freshly randomized board."""
    options = parse_args(args)
    seed = options.seed if options.seed is not None else random.SystemRandom().randrange(
        0, 2**32
    )
    print(f"Randomized board seed: {seed}")

    environment = WumpusEnvironment(
        randomize=True,
        grid_size_range=(4, 10),
        randomize_start=True,
        seed=seed,
    )
    BoardRenderer(environment).render()


if __name__ == "__main__":
    main()
