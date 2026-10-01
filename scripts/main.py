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

    while env.agent.is_alive and not env.agent.has_gold:
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
    elif env.agent.has_gold:
        print("\n🎉 Gold Found and Grabbed!")


if __name__ == "__main__":
    simulation_env = WumpusEnvironment()
    board_renderer = BoardRenderer(simulation_env)
    run_simulation(simulation_env, board_renderer, delay=1.0)