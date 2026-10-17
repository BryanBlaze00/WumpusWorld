from kb import KnowledgeBase


class KBAgent:
    """Choose actions from percepts and facts recorded in a knowledge base."""

    def __init__(self):
        """Create an agent with an empty knowledge base."""
        self.kb = KnowledgeBase()

    def choose_action(self, current_pos, percepts):
        """Record percepts and begin selecting the next knowledge-based action."""
        # 1. Update KB with current percepts
        self.kb.tell(current_pos, percepts)

        # 2. Check winning condition
        if percepts["glitter"]:
            return "GRAB"

        # 3. Ask KB for safe target
        target = self.kb.ask_next_unvisited_safe()

        # 4. Plan action (FORWARD, TURN_LEFT, TURN_RIGHT) to head toward target
        # ...