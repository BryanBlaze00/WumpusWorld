import sys

from environment import Direction


class BoardRenderer:

    def __init__(self, environment):
        self.env = environment

    def render(self, use_unicode=None):
        if use_unicode is None:
            use_unicode = self._supports_unicode()

        symbols = self._symbols(use_unicode)
        size = self.env.grid_size
        dir_symbols = {
            Direction.NORTH: symbols["north"],
            Direction.EAST: symbols["east"],
            Direction.SOUTH: symbols["south"],
            Direction.WEST: symbols["west"],
        }

        border = symbols["top_left"] + (
            symbols["horizontal"] * 8 + symbols["top_join"]
        ) * (size - 1) + symbols["horizontal"] * 8 + symbols["top_right"]
        divider = symbols["left_join"] + (
            symbols["horizontal"] * 8 + symbols["middle_join"]
        ) * (size - 1) + symbols["horizontal"] * 8 + symbols["right_join"]
        bottom = symbols["bottom_left"] + (
            symbols["horizontal"] * 8 + symbols["bottom_join"]
        ) * (size - 1) + symbols["horizontal"] * 8 + symbols["bottom_right"]

        print(border)

        for y in range(size, 0, -1):
            top_line = symbols["vertical"]
            mid_line = symbols["vertical"]
            bot_line = symbols["vertical"]

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
                    top = symbols["wumpus"]
                elif has_stench:
                    top = symbols["stench"]
                else:
                    top = "    "

                # --- Mid Slot (Agent) ---
                if is_agent:
                    mid = f"{symbols['agent']}{dir_symbols[self.env.agent.direction]}"
                else:
                    mid = "    "

                # --- Bot Slot (Pit / Gold / Breeze) ---
                bot_symbols = []
                if is_pit:
                    bot_symbols.append("pit")
                if is_gold:
                    bot_symbols.append("gold")
                if has_breeze:
                    bot_symbols.append("breeze")

                if "pit" in bot_symbols:
                    bot = symbols["pit"]
                elif "gold" in bot_symbols and "breeze" in bot_symbols:
                    bot = symbols["gold_breeze"]
                elif "gold" in bot_symbols:
                    bot = symbols["gold"]
                elif "breeze" in bot_symbols:
                    bot = symbols["breeze"]
                else:
                    bot = "    "

                top_line += f"  {top}  {symbols['vertical']}"
                mid_line += f"  {mid}  {symbols['vertical']}"
                bot_line += f"  {bot}  {symbols['vertical']}"

            print(top_line)
            print(mid_line)
            print(bot_line)

            if y > 1:
                print(divider)

        print(bottom)

    @staticmethod
    def _symbols(use_unicode):
        if use_unicode:
            return {
                "top_left": "┌",
                "top_join": "┬",
                "top_right": "┐",
                "left_join": "├",
                "middle_join": "┼",
                "right_join": "┤",
                "bottom_left": "└",
                "bottom_join": "┴",
                "bottom_right": "┘",
                "horizontal": "─",
                "vertical": "│",
                "agent": "🤖",
                "north": "⬆️",
                "east": "➡️",
                "south": "⬇️",
                "west": "⬅️",
                "wumpus": " 👹 ",
                "stench": " 🤢 ",
                "pit": " 🕳️ ",
                "gold": " 🪙 ",
                "gold_breeze": "🪙💨",
                "breeze": " 💨 ",
            }
        return {
            "top_left": "+",
            "top_join": "+",
            "top_right": "+",
            "left_join": "+",
            "middle_join": "+",
            "right_join": "+",
            "bottom_left": "+",
            "bottom_join": "+",
            "bottom_right": "+",
            "horizontal": "-",
            "vertical": "|",
            "agent": "A",
            "north": "^",
            "east": ">",
            "south": "v",
            "west": "<",
            "wumpus": " W  ",
            "stench": " S  ",
            "pit": " P  ",
            "gold": " G  ",
            "gold_breeze": "GB  ",
            "breeze": " B  ",
        }

    @staticmethod
    def _supports_unicode():
        encoding = getattr(sys.stdout, "encoding", None)
        if not encoding:
            return True
        try:
            "🤖┌".encode(encoding)
        except UnicodeEncodeError:
            return False
        return True