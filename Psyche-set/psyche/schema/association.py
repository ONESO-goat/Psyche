from base import SchemaLogic
import sqlite3

class AssociationLogic(SchemaLogic):
    """
    Single association between two concepts.
    This is a baseModel for the table 'association' 
    """
    def __init__(self, 
                assoc_id: str
                ):
        if not assoc_id:
            return RuntimeError("Association id can not be empty.")

        super().__init__(schema_id=assoc_id, schema_type="association")


def test_add_association(id_:str, 
                         context:str,
                         topic_1_id:str, 
                         topic_2_id:str, 
                         association_type: str,
                         get:bool = False
                        ):
    if not get:
        SQL = """
        INSERT INTO topic 
        (association_id, topic_one_id, topic_two_id, context, association_type) 
        VALUES (?, ?, ?, ?, ?);"""
    else:
        SQL = f"""
            SELECT * 
            from association
            where association_id = ?;
        """
    with sqlite3.connect("app_data.db") as conn:
        cursor = conn.cursor()

        if not get:
            cursor.execute(SQL, (id_, topic_1_id, topic_2_id, context, association_type))
            conn.commit()
        else:
            cursor.execute(SQL, id_)
            data = cursor.fetchall()
            
            return data