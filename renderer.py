from environment import Direction


class BoardRenderer:

    def __init__(self, environment):
        self.env = environment

    def render(self):
        size = self.env.grid_size
        dir_symbols = {
            Direction.NORTH: "⬆️",
            Direction.EAST: "➡️",
            Direction.SOUTH: "⬇️",
            Direction.WEST: "⬅️",
        }

        border = "┌" + ("────────┬" * (size - 1)) + "────────┐"
        divider = "├" + ("────────┼" * (size - 1)) + "────────┤"
        bottom = "└" + ("────────┴" * (size - 1)) + "────────┘"

        print(border)

        for y in range(size, 0, -1):
            top_line = "│"
            mid_line = "│"
            bot_line = "│"

            for x in range(1, size + 1):
                pos = (x, y)
                is_agent = pos == (self.env.agent.x, self.env.agent.y)
                is_wumpus = pos == self.env.wumpus_pos and self.env.wumpus_alive
                is_pit = pos in self.env.pits
                is_gold = pos == self.env.gold_pos

                # Retrieve saved percepts if cell was ever visited
                cell_percepts = self.env.discovered_percepts.get(pos, {})
                has_stench = cell_percepts.get("stench", False)
                has_breeze = cell_percepts.get("breeze", False)

                # --- Top Slot (Wumpus / Stench) ---
                if is_wumpus:
                    top = " 👹 "
                elif has_stench:
                    top = " 🤢 "
                else:
                    top = "    "

                # --- Mid Slot (Agent) ---
                if is_agent:
                    mid = f"🤖{dir_symbols[self.env.agent.direction]}"
                else:
                    mid = "    "

                # --- Bot Slot (Pit / Gold / Breeze) ---
                bot_symbols = []
                if is_pit:
                    bot_symbols.append("🕳️")
                if is_gold:
                    bot_symbols.append("🪙")
                if has_breeze:
                    bot_symbols.append("💨")

                if "🕳️" in bot_symbols:
                    bot = " 🕳️ "
                elif "🪙" in bot_symbols and "💨" in bot_symbols:
                    bot = "🪙💨"
                elif "🪙" in bot_symbols:
                    bot = " 🪙 "
                elif "💨" in bot_symbols:
                    bot = " 💨 "
                else:
                    bot = "    "

                top_line += f"  {top}  │"
                mid_line += f"  {mid}  │"
                bot_line += f"  {bot}  │"

            print(top_line)
            print(mid_line)
            print(bot_line)

            if y > 1:
                print(divider)

        print(bottom)