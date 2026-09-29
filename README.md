# Wumpus World AI

A Python implementation of the classic Wumpus World environment from
*Artificial Intelligence: A Modern Approach* by Russell and Norvig.

The project explores how an agent can use its surroundings and stored
knowledge to navigate a grid, avoid hazards, and find the gold. It is being
developed incrementally, with the current work tracked in GitHub Issues.

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
the agent through the demonstration loop.

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
| `kb.py` | Provides the knowledge-base foundation for agent reasoning. |
| `agent.py` | Provides the knowledge-based agent foundation. |

## Testing

Automated tests are being developed as part of the project. For now, run the
simulation as a manual smoke test:

```bash
python main.py
```

The issue tracker contains the current development tasks and project roadmap.
