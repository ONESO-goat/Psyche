


class love:
    """Base class for relationship/friendship systems."""
    """Not finished yet, but will be in the future. This is a placeholder for now."""
    def __init__(self, Brain, who: str):
        self.Brain = Brain
        self.who = who
    def remember_(self, who: str):
        """Get memories related to this friend."""
        return self.Brain.mind.get_memories(who)