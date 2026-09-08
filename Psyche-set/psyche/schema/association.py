from typing import (
    Dict, 
    Any,
    final,
    Final, 
    Awaitable
)
import asyncio as ao
from helpers.python_.helpers import Association, Logger
from helpers.python_.debugging_utils import debug
from datetime import datetime
import sqlite3

class AssociationLogic:
    """
    Single association between two concepts.
    This is a baseModel for the table '' 
    """
    def __init__(self, 
                assoc_id: str
                ):

        self.called = False

        association_data: Association = self.get_association(association_id=assoc_id)
        if not association_data:
            return 
        
        self.id = association_data.association_id
        self.source_id = association_data.source_id
        self.strength = max(0.0, min(1.0, association_data.strength))  # Clamp 0-1
        self.type = association_data.association_type  # 'semantic', 'temporal', 'emotional', 'causal', 'functional'

        self.created = datetime.now().isoformat()

    @final
    async def get_association(self, association_id:str)->None|Association:
        try:
            data:Final = await self.connect_and_get(association_id=association_id)
            if not data:
                return None
            return Association(**data)
        except Exception as ex:
            Logger.error(debug(message=f"Brain faced an error when achieving: \n\t\u2022{ex}", tier=5))
            return None

    @final
    def connect_and_get(self, association_id:str[37]):
            """
                Connect to the database then obtain an association.
                If connection fails or association data isn't valid, returns None
            """
            SQL_QUERY:str = """
            
                    SELECT *
                    FROM association
                    WHERE association_id = ?;
                    
            """
            with sqlite3.connect("app_data.db") as conn:
                cursor = conn.cursor()
            
                conn.execute(SQL_QUERY, association_id)
            
                association_data = cursor.fetchall()
                if association_data[0] != association_id:
                    return None
                return association_data
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'source': self.source_id,
            'target': self.target,
            'strength': self.strength,
            'type': self.type,
            'reason': self.reason,
            'memory_id': self.memory_id,
            'created': self.created
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Association':
        assoc = Association(
            source=data['source'],
            target=data['target'],
            strength=data['strength'],
            association_type=data['type'],
            reason=data.get('reason', ''),
            memory_id=data.get('memory_id')
        )
        assoc.created = data.get('created', datetime.now().isoformat())
        return assoc
