# The flow here will be that C++ sends the id to python, the python gets the data. Better than sending 
# data over.

from helpers.python_.helpers import Brain, Logger, BrainCreationError
from helpers.python_.debugging_utils import debug
from typing import (
    Awaitable,
    Final,
    final
)
import sqlite3 
import copy
import asyncio
from datetime import datetime

class BrainLogic:

    def __init__(self, brain_id:str[37])->None:
        """
                @brain_id: str[37] = Id of brain, Sent by C++ or achieved by sql.
        """

        self._called: bool = True
        if not brain_id:
            raise BrainCreationError("Brain id was not provided.")
        
        self.brain, created = self.get_brain(brain_id=brain_id)
        if not created:
            raise BrainCreationError(f"({datetime.now().date()}) Brain failed to create.") 
            # Add more details later

        self.memories = self.brain.memories or []


    @classmethod
    async def create(
        cls,
        brain_id: str
    ) -> "BrainLogic":

        brain: Final = await cls._achieve_brain_data(brain_id)

        if brain is None:
            raise BrainCreationError(
                f"Brain with id '{brain_id}' failed to load."
            )

        return cls(brain)
    
    @final
    async def _get_brain(self, brain_id:str[37]) -> Awaitable[Brain|None]:
        """Get the brain during init"""

        if self._called:
            print("Brain already initialized.")
            return None
    
        if not brain_id or brain_id.strip() == "":
            return None
        if any(c in ["'", '"',"<", ">"] for c in brain_id):
            return None

        try:
            brain: Final [Brain|None] = await asyncio.wait_for(
                self._achieve_brain_data(brain_id), 
                timeout=5
            )

            if brain is None:

                return None
            
            self._called = True
            return brain
        except asyncio.TimeoutError:
            
            Logger.error(debug(message="Brain timeout reached", tier=3))
            return None
        except Exception as ex:
            Logger.error(debug(message=f"Brain faced an unexpected error: {ex}", tier=4))
            return None

    @final
    async def _achieve_brain_data(self, brain_id:str[37]) -> Brain|None:
       
        brain_data: Final = self.connect_and_get(brain_id=brain_id)
        if not brain_data:
            return None
        try:
            data_dict  = brain_data.to_dict()
            if not data_dict  or data_dict.get("brain_id", None) != brain_id:
                Logger.error(debug(message="Brain was not created or held false data", tier=3))
                return None
            
            # Turn Brain into BaseModel. copying the data rather than sending over the direct data
            B = Brain(**data_dict)

            return B
        except Exception as ex:
            Logger.error(debug(message=f"Brain faced an error when achieving: \n\t\u2022{ex}", tier=5))
            return None
    @final
    def connect_and_get(self, brain_id:str[37]):
        """
            Connect to the database then obtain brain.
            If connection fails or brain data isn't valid, returns None
        """
        SQL_QUERY:str = """
        
                SELECT *
                FROM brains
                WHERE brain_id = ?;
                
        """
        with sqlite3.connect("app_data.db") as conn:
            cursor = conn.cursor()
        
            conn.execute(SQL_QUERY, brain_id)
        
            brain_data = cursor.fetchall()
            if brain_data[0] != brain_id:
                return None
            return brain_data
        return None

    def ok(self)->bool:
        """Check whether brain creation is finalized"""

        # TODO
        pass
    
    def obtain_memories(self):
        return copy.deepcopy(self.memories)

    @property
    def data(self):
        return self.brain.to_dict()