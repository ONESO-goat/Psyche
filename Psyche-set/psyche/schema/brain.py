# The flow here will be that C++ sends the id to python, the python gets the data. Better than sending 
# data over.

from helpers.python_.helpers import BrainCreationError
from base import SchemaLogic
import copy

class BrainLogic(SchemaLogic):

    def __init__(self, brain_id:str[37])->None:
        """
                @brain_id: str[37] = Id of brain, Sent by C++ or achieved by sql.
        """

       
        if not brain_id:
            raise BrainCreationError("Brain id was not provided.")
        super().__init__(schema_id=brain_id, schema_type="brain")

        self.memories = self.schema.memories or []


    
    def obtain_memories(self):
        return copy.deepcopy(self.memories)
