# The flow here will be that C++ sends the id to python, the python gets the data. Better than sending 
# data over.

from helpers.python_.helpers import BrainCreationError
from base import SchemaLogic
import copy
import sqlite3

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


testId = "1"*37
def test_add_brain_schema(id_:str=testId, get:bool = False):
    if not get:
        SQL = "INSERT INTO topic (brain_id) VALUES (?);"
    else:
         SQL = f"""SELECT * 
         from brain
         where brain_id = ?;
         """
    with sqlite3.connect("app_data.db") as conn:
        cursor = conn.cursor()

        if not get:
            cursor.execute(SQL, (id_))
            conn.commit()
        else:
            cursor.execute(SQL, id_)
            data = cursor.fetchall()
           
            return data
if __name__ == "__main__":
    pass