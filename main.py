from environment import WumpusEnvironment
from renderer import BoardRenderer

if __name__ == "__main__":
    env = WumpusEnvironment()
    renderer = BoardRenderer(env)

    print("Initial Wumpus World State:")
    renderer.render()

    print("\nMoving agent forward...")
    env.move_forward()
    renderer.render()