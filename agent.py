from kb import KnowledgeBase


class KBAgent:

    def __init__(self):
        self.kb = KnowledgeBase()

    def choose_action(self, current_pos, percepts):
        # 1. Update KB with current percepts
        self.kb.tell(current_pos, percepts)

        # 2. Check winning condition
        if percepts["glitter"]:
            return "GRAB"

        # 3. Ask KB for safe target
        target = self.kb.ask_next_unvisited_safe()

        # 4. Plan action (FORWARD, TURN_LEFT, TURN_RIGHT) to head toward target
        # ...