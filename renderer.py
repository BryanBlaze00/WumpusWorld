from environment import Direction


class BoardRenderer:

    def __init__(self, environment):
        self.env = environment

    def render(self):
        size = self.env.grid_size
        dir_symbols = {
            Direction.NORTH: "▲",
            Direction.EAST: "►",
            Direction.SOUTH: "▼",
            Direction.WEST: "◄",
        }

        # ASCII Box borders
        border = "┌" + ("───────┬" * (size - 1)) + "───────┐"
        divider = "├" + ("───────┼" * (size - 1)) + "───────┤"
        bottom = "└" + ("───────┴" * (size - 1)) + "───────┘"

        print(border)

        # Loop y down from 4 to 1 (Top row to Bottom row)
        for y in range(size, 0, -1):
            top_line = "│"
            mid_line = "│"
            bot_line = "│"

            # Loop x from 1 to 4 (Left column to Right column)
            for x in range(1, size + 1):
                # Entity checks matching 1-indexed coordinates
                is_agent = (x, y) == (self.env.agent.x, self.env.agent.y)
                is_wumpus = (
                    (x, y) == self.env.wumpus_pos and self.env.wumpus_alive
                )
                is_pit = (x, y) in self.env.pits
                is_gold = (x, y) == self.env.gold_pos

                # Slot contents
                top = " W " if is_wumpus else "   "
                mid = (
                    f"A{dir_symbols[self.env.agent.direction]}"
                    if is_agent
                    else "  "
                )
                bot = " G " if is_gold else (" P " if is_pit else "   ")

                top_line += f"  {top}  │"
                mid_line += f"  {mid}   │"
                bot_line += f"  {bot}  │"

            print(top_line)
            print(mid_line)
            print(bot_line)

            # Print section divider for all rows except the bottom-most
            if y > 1:
                print(divider)

        print(bottom)