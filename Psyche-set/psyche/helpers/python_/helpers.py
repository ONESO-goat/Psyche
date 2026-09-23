
from typing import Any, Annotated, Final
from pydantic import StringConstraints, BaseModel
from datetime import datetime
import logging
from enum import Enum, StrEnum



class SchemasTypes(StrEnum):
    
    TOPIC= "topic"
    BRAIN = "brain"
    ASSOCIATION = "association"



class BrainTypes(Enum):
    LINX = "linx"
    MANAGER = "manager"
    GENERAL = "general"

Logger = logging.Logger("psyche")

class BrainCreationError(Exception):
    pass

class SchemaCreationError(Exception):
    pass



class Topic(BaseModel):
    topic_id: Annotated[str, StringConstraints(min_length=37, max_length=37)]
    
    created_at: datetime

class Memory(BaseModel):
    memory_id: str

    brain_id: str 

    context: str
    dominant_emotion: str

    importance: float
    
    formed_at: datetime


class Brain(BaseModel):
    brain_id: Annotated[str, StringConstraints(min_length=37, max_length=37)]
    brain_memories: dict[str, Memory]
    created_at: datetime

    brain_type: BrainTypes

    def replace_memory(self,memory_id:str, new_memory:dict):
        """
            Replace an existing memory with new data.
        """
        try:
            if not self.brain_memories.get(memory_id, None):
                raise RuntimeError("Memory does not exist")
            memory_BaseModel = Memory(new_memory)
            self.brain_memories[memory_id] = memory_BaseModel
        except Exception as ex:
            raise ex
    def commit(self) -> bool:
        """Commit to database. Returns true if saved, false otherwise."""
        raise NotImplementedError("Brain.Commit() yet to exist")
"""
    The Brain (which holds memories, data, or previous theories) of an agent. This can be a Linx or General.
"""

class Association(BaseModel):
    association_id: Annotated[str, StringConstraints(min_length=48, max_length=48)]
    """
        looks like this: association-UUIDv4
    """

    topic_one_id:Annotated[str, StringConstraints(min_length=48, max_length=48)] 
    topic_two_id: Annotated[str, StringConstraints(min_length=48, max_length=48)]

    context:str

    source_id:str                 
    strength: float
    association_type: str 


VALID_SCHEMAS: Final[dict[str, Any]] = {
    "topic": Topic,
    "brain": Brain, 
    "association": Association,
}