# Excepts_and_hints.py

from typing import Protocol


class InvalidRow(Exception):
    pass

class ValidEmotion(Protocol):
    ...

class InvalidEmotion(Exception):
    pass

class NoArgumentCalled_or_AllNone(Exception):
    pass
