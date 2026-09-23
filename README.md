# Wumpus World AI

A Python implementation of the classic Wumpus World environment and Knowledge-Based (KB) agent as described in Artificial Intelligence: A Modern Approach (Russell & Norvig).

## Project Overview

Wumpus World is a 4x4 grid-based environment designed to demonstrate logical reasoning and decision-making under uncertainty. The agent must navigate the board, avoid lethal hazards (Pits and the Wumpus), collect the Gold, and safely return to the start cell (0,0).

### Features

- Environment Engine: Manages grid state, hazard placement, agent state, movement actions, and percept generation.

- Dynamic Percepts: Detects Stench, Breeze, and Glitter relative to adjacent or current cells.

- Extensible Architecture: Designed to support ASCII terminal rendering and automated logical inference engines (TELL / ASK).

---

## Environment Layout

- Grid Size: 4x4

- Start Position: (0,0) (Bottom-Left)

- Hazards:

  - Pits: Emit a Breeze in adjacent orthogonal cells.

  - Wumpus: Emits a Stench in adjacent orthogonal cells.

- Objective: Locate the Gold (Glitter), grab it, and return safely to the starting point.

---

## Getting Started

### Prerequisites

- Python 3.8+

### Running the Engine

Execute the main script to run the base environment test:

```bash
python wumpus_world.py
