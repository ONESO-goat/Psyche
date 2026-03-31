


class love:
    """Base class for relationship/friendship systems."""
    def __init__(self, Brain, who: str):
        self.Brain = Brain
        self.who = who
    def remember_(self, who: str):
        """Get memories related to this friend."""
        return self.Brain.mind.get_memories(who)