from environment import WumpusEnvironment
from renderer import BoardRenderer


def main():
    environment = WumpusEnvironment(
        randomize=True,
        grid_size_range=(4, 10),
        randomize_start=True,
    )
    BoardRenderer(environment).render()


if __name__ == "__main__":
    main()
