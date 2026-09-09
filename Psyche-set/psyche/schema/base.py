import time
from pydanic import BaseModel
from typing import (
    final,
    Final,
    TypeVar,
    Awaitable

)
import asyncio
from helpers.python_.helpers import (
    SchemaCreationError, 
    Logger, 
    SchemasTypes, 
    VALID_SCHEMAS
)

from helpers.python_.debugging_utils import debug
import aiosqlite # sqlite3 but with async logic

ST = TypeVar('ST') # Assoc, Brain, Topic, and so on
"""Schema Type"""

@final
class SchemaLogic:
    def __init__(self, schema_id: str):

        if not schema_id:
            raise RuntimeError("Schema id is required")

        self.__called = False
        self.schema: ST = self._get_schema(schema_id)
        if schema is None:
            raise SchemaCreationError(f"Schema of type '{ST}' couldn't be created")
        
        self._meta_id = schema_id



    @final
    async def _get_schema(self, schema_id:str[37]) -> Awaitable[ST|None]:
            """Get the Schema during init"""
    
            if self.__called:
                print("schema already initialized.")
                return None
        
            if not schema_id or schema_id.strip() == "":
                return None
            
            if  not {"'", '"',"<", ">"}.isdigjoint(schema_id):
                return None
    
            try:
                schema: Final[ST|None] = await asyncio.wait_for(
                    self._achieve_schema_data(schema_id), 
                    timeout=5
                )
    
                if schema is None:
    
                    return None
                
                self.__called = True
                return schema
            except asyncio.TimeoutError:
                
                Logger.error(debug(message="schema timeout reached", tier=3))
                return None
            except Exception as ex:
                Logger.error(debug(message=f"schema faced an unexpected error: {ex}", tier=4))
                return None
            
    async def _achieve_schema_data(self, schema_id:str, schema_type:SchemasTypes)->ST|None:
        try:
            if (
                not schema_type or 
                schema_type.value not in VALID_SCHEMAS or 
                not SchemasTypes(schema_type)
                ):
                raise SchemaCreationError(f"Schema type '{schema_type}' is invalid.")

            table_name: Final[str] = schema_type.value
            SQL_QUERY: Final[str] = f"""
                select *
                from {table_name}
                where {table_name}_id = ?;
            """
            async with aiosqlite.connect("app_data.db") as conn:
                # Set row_factory to Row to get dictionary-like access for Pydantic/dataclasses
                conn.row_factory = aiosqlite.Row
                
                async with conn.execute(SQL_QUERY, (schema_id,)) as cursor:
                    row = await cursor.fetchone()
                    
                    if not row:
                        return None
                    
                    # Convert SQLite row to a standard dictionary
                    data_dict = dict(row)
                    
                    # Instantiate object mapping dynamically
                    schema_class = VALID_SCHEMAS[schema_type.value]
                    schema_object = schema_class(**data_dict)
                    
                    # Non-blocking sleep if artificial throttling is required
                    await asyncio.sleep(0.1)
                    
                    return schema_object

        except aiosqlite.Error as db_ex:
            
            print(f"Database error occurred: {db_ex}")
            Logger.error(debug(message=f"Database error occurred: {db_ex}", tier=5))
            return None
        except Exception as ex:
          
            print(f"Unexpected error: {ex}")
            Logger.error(debug(message=f"Unexpected error: {ex}", tier=5))
            return None