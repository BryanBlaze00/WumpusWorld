from environment import WumpusEnvironment
from renderer import BoardRenderer


def main():
    environment = WumpusEnvironment(
        grid_size=5,
        randomize=True,
        seed=7,
        pit_count=5,
    )
    BoardRenderer(environment).render()


if __name__ == "__main__":
    main()
