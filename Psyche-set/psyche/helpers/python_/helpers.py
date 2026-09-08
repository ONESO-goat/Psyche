
from typing import Any, Annotated
from pydantic import StringConstraints, BaseModel
from datetime import datetime
import logging
from enum import Enum


class BrainTypes(Enum):
    LINX = "linx"
    MANAGER = "manager"
    GENERAL = "general"

Logger = logging.Logger("psyche")

class BrainCreationError(Exception):
    pass

Memories = list[dict[str, Any]]

class Brain(BaseModel):
    brain_id: Annotated[str, StringConstraints(min_length=37, max_length=37)]
    brain_memories: Memories
    created_at: datetime

    brain_type: BrainTypes
"""
    The Brain (which holds memories, data, or previous theories) of an agent. This can be a Linx or General.
"""

class Association(BaseModel):
    association_id: Annotated[str, StringConstraints(min_length=48, max_length=48)]
    """
        looks like this: association-UUIDv4
    """

    association_one_id:Annotated[str, StringConstraints(min_length=48, max_length=48)] 
    association_two_id: Annotated[str, StringConstraints(min_length=48, max_length=48)]

    context:str

    source_id:str                 
    strength: float
    association_type: str 
