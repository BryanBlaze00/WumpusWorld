# Wumpus World AI

A Python implementation of the classic Wumpus World environment from
*Artificial Intelligence: A Modern Approach* by Russell and Norvig.

The project is currently an environment prototype. It provides a fixed 4x4
board, an agent state model, percept generation, and terminal rendering. The
knowledge-based agent and several environment actions are still being built.

## Current Features

- A 4x4 grid with a fixed starting position at `(1, 1)`.
- A Wumpus, pits, and gold placed by the default environment layout.
- Agent movement in the direction it is facing.
- Breeze, stench, and glitter percepts.
- Percept history for cells visited by the environment.
- An emoji-based board renderer.
- Initial `KnowledgeBase` and `KBAgent` classes for future reasoning work.

## Environment Layout

Coordinates begin at `(1, 1)` in the bottom-left corner.

| Object | Position |
| --- | --- |
| Agent start | `(1, 1)` |
| Wumpus | `(1, 3)` |
| Gold | `(2, 3)` |
| Pits | `(3, 1)` and `(3, 3)` |

Pits produce a breeze in adjacent orthogonal cells. The living Wumpus
produces a stench in adjacent orthogonal cells. The gold produces glitter
when the agent is standing on its cell.

## Getting Started

### Prerequisites

- Python 3.8 or newer

The current prototype uses only Python standard-library modules, so no package
installation is required.

### Running the Simulation

From the repository root, run:

```bash
python main.py
```

The simulation renders the board, prints the current percepts, and advances
the agent through the current demonstration loop. The delay is currently
configured in `main.py`.

The renderer uses box-drawing characters and emojis. If a terminal cannot
display them, configure the terminal for UTF-8 or use a UTF-8-capable
integrated terminal.

## Project Structure

| File | Responsibility |
| --- | --- |
| `main.py` | Starts and runs the current demonstration simulation. |
| `environment.py` | Defines the board, hazards, percepts, and movement. |
| `agent_state.py` | Stores the agent's position, direction, and status. |
| `direction.py` | Defines the four directions and turn calculations. |
| `renderer.py` | Draws the board and discovered percepts in the terminal. |
| `kb.py` | Stores the initial knowledge-base facts and query helpers. |
| `agent.py` | Defines the early `KBAgent` decision-making scaffold. |

## Actions and Game State

The environment currently supports forward movement through
`WumpusEnvironment.move_forward()`. The direction enum already provides
left-turn and right-turn calculations, but the environment action methods and
complete agent action loop are still under development.

The agent can be alive or dead, can carry an arrow, and can be marked as
carrying the gold. The current demonstration stops after the agent reaches
the gold or dies. A complete return-home win condition has not yet been
implemented.

## Testing

Automated tests are planned but are not yet part of the repository. Until
they are added, the supported manual smoke test is:

```bash
python main.py
```

Future tests will use Python's standard `unittest` runner and will cover
movement, hazards, percepts, and knowledge-base behavior.

## Planned Work

The project backlog tracks the next development steps, including:

- Completing turning, grabbing, and shooting actions.
- Adding automated tests.
- Implementing percept history and hazard inference.
- Connecting `KBAgent` to the simulation loop.
- Adding a return-home win condition.
- Supporting randomized and configurable board layouts.
- Adding command-line options and continuous integration.

Features listed here as planned are not currently available.
