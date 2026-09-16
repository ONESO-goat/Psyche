

# The flow here will be that C++ sends the id to python, the python gets the data. Better than sending 
# data over.


from helpers.python_.debugging_utils import debug

from .base import SchemaLogic
import sqlite3

class TopicLogic(SchemaLogic):
    def __init__(self, schema_id):
   
        super().__init__(schema_id, schema_type="topic")
       

    def test(self):
        print(self.schema)

testId = "1"*37
def test_add_topic(id_:str=testId, get:bool = False):
    if not get:
        SQL = "INSERT INTO topic (topic_id, what, context) VALUES (?, ?, ?);"
    else:
         SQL = """SELECT * 
         from topic 
         where topic_id = ?;
         """
    with sqlite3.connect("app_data.db") as conn:
        cursor = conn.cursor()

        if not get:
            cursor.execute(SQL, (id_, "apples", "a food people eat"))
            conn.commit()
        else:
            cursor.execute(SQL, id_)
            data = cursor.fetchall()
           
            return data
if __name__ == "__main__":
    t = TopicLogic()