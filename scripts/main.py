import argparse
import os
import time
from environment import WumpusEnvironment
from renderer import BoardRenderer


def clear_screen():
    # ANSI escape sequence clears PyCharm terminal & console screen reliably
    print("\033[H\033[2J", end="")
    os.system("cls" if os.name == "nt" else "clear")


def run_simulation(env, renderer, delay=1.0):
    step = 0

    while env.agent.is_alive and not env.is_won():
        clear_screen()
        step += 1

        print(f"=== Step {step} ===")
        renderer.render()

        percepts = env.get_percepts()
        print(f"Percepts at ({env.agent.x}, {env.agent.y}): {percepts}")

        time.sleep(delay)

        # Simulation step logic
        moved = env.move_forward()
        if not moved:
            env.turn_right()
            print("Action: Hit wall -> Turned Right")
        else:
            print("Action: Moved Forward\n")

        if env.get_percepts()["glitter"]:
            env.grab()

    # Render final state
    clear_screen()
    print("=== Final State ===")
    renderer.render()

    if not env.agent.is_alive:
        print("\n💀 The Agent died!")
    elif env.is_won():
        print("\n🎉 Gold Found and Returned Home!")
    elif env.agent.has_gold:
        print("\n🪙 Gold Found! Return to the Starting Cell.")


def positive_float(value):
    delay = float(value)
    if delay < 0:
        raise argparse.ArgumentTypeError("delay must be non-negative")
    return delay


def valid_grid_size(value):
    grid_size = int(value)
    if grid_size < 3:
        raise argparse.ArgumentTypeError("grid size must be at least 3")
    return grid_size


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Run the Wumpus World simulation.")
    parser.add_argument(
        "--delay",
        type=positive_float,
        default=1.0,
        help="seconds to wait between simulation steps (default: 1.0)",
    )
    parser.add_argument(
        "--grid-size",
        type=valid_grid_size,
        default=4,
        help="board width and height (default: 4)",
    )
    return parser.parse_args(args)


def main(args=None):
    options = parse_args(args)
    simulation_env = WumpusEnvironment(grid_size=options.grid_size)
    board_renderer = BoardRenderer(simulation_env)
    run_simulation(simulation_env, board_renderer, delay=options.delay)


if __name__ == "__main__":
    main()