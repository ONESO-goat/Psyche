
from typing import Any, Annotated, Final
from pydantic import StringConstraints, BaseModel, Field, ConfigDict
from datetime import datetime, timezone
import logging
from enum import Enum, StrEnum
import random
import numpy as np

def generate_unique_number_id():
    number = random.randint(1_000_000_000_000_000, 9_999_999_999_999_999)
    return number


class SchemasTypes(StrEnum):
    
    TOPIC= "topic"
    BRAIN = "brain"
    ASSOCIATION = "association"




class BrainTypes(Enum):
    model_config = ConfigDict(frozen=True)

    LINX = "linx"
    MANAGER = "manager"
    GENERAL = "general"

_5x5_grid_template: Final[np.ndarray] = np.zeros(5,5)

Logger = logging.Logger("psyche")

class BrainCreationError(Exception):
    pass

class SchemaCreationError(Exception):
    pass

class EMOTIONS(Enum):
    model_config = ConfigDict(frozen=True)

    NEUTRAL = "gray"       
    JOY = "yellow"         
    ANGER = "red"
    DISGUST = "dark_green"
    SURPRISE = "light_orange"
    SADNESS = "medium_blue"
    FEAR = "purple"
    TRUST = "teal"
    ENVY = "green"
    GUILT = "brown"
    PRIDE = "gold" 
    CONFUSION = "silver"   
    OVERWHELM = "slate"  
"""
    Emotions? Emotions are a unique trait in LINX's. When forming a memory, an emotion is taken 
    out of the event depending the the 5x5 grid, rather than an AI choosing an emotion.
    example;
    [ 0.3  0.5  0.4  0.9  0.5] # joy - Joy is dominate
    [ 0.0  0.0  0.0  0.2  0.0] # anger - Mini anger
    [ 0.0  0.0  0.4  0.3  0.2] # sadness - Everyone feels slight sadness am I right?
    [ 0.0  0.0  0.0  0.0  0.0] # disgust - Disgust is non-existent
    [ 0.2  0.2  0.2  0.2  0.2] # fear - fear is staying consistent 

    final output: Joy, leading to anxiety 

    NOTE: Explain this better later
    
""" 


A_lot_Of_Dictionaries = dict
class Topic(BaseModel):
    topic_id: Annotated[str, StringConstraints(min_length=48, max_length=48)]

    title: str
    context: str

    facts: dict[str, A_lot_Of_Dictionaries|set|list[Any]] = Field(default=list())
    """
        Facts stores facts in certain domains.
        For example, the topic is about Julius (me).
        I go to massbay, and plan to transfer to a 4 year school like northeastern, 
        Amherst, or, if I am lucky, MIT.

        That will be stored in its own domain, for example "interest"
        {   
        
        "education": {"massbay", "burlington high school"},
        "interest": {
                "games": {"overwatch", ...},
                "transfer": {
                    "school": {"MIT", "Umass amherest", ...},
                    "moving": {"california", "passport bro", ...}
                },
                inf_amount_of_dicts...
            }
        }
    """
    
    created_at: Final[datetime] = Field(default=datetime.now(tz=timezone.utc))

class Memory(BaseModel):
    memory_id: str

    brain_id: str 

    context: str
    dominant_emotion: EMOTIONS

    importance: float
    
    formed_at: Final[datetime] = Field(default=datetime.now(tz=timezone.utc))


class Brain(BaseModel):
    brain_id: Annotated[str, StringConstraints(min_length=37, max_length=37)]
    brain_memories: dict[str, Memory] = Field(default=dict())

    created_at: Final[datetime] = Field(default=datetime.now(tz=timezone.utc))

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

    def to_dict(self):
        
        return dict(self)


VALID_SCHEMAS: Final[dict[str, Any]] = {
    "topic": Topic,
    "brain": Brain, 
    "association": Association,
}