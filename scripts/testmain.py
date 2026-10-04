from environment import WumpusEnvironment
from renderer import BoardRenderer


def main():
    environment = WumpusEnvironment(
        grid_size=5,
        wumpus_pos=(5, 5),
        pits={(1, 4), (2, 2), (3, 3), (4, 4), (5, 1)},
        gold_pos=(3, 5),
    )
    BoardRenderer(environment).render()


if __name__ == "__main__":
    main()
