
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, name: str, db_name: str = "psyche.db"):
        self.name = name

        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

        self.initialize()

    # ------------------------
    # Setup
    # ------------------------
    def create_tables(self):
        with open("db/schema.sql", "r") as f:
            schema = f.read()

        with self.conn:
            self.conn.executescript(schema)
            
    def initialize(self):
        version = self.conn.execute("PRAGMA user_version").fetchone()[0]

        if version == 0:
            self.create_tables()
            self.conn.execute("PRAGMA user_version = 1")

    # ------------------------
    # Helpers
    # ------------------------
    def _rows_to_dicts(self, rows):
        return [dict(row) for row in rows]

    def _validate_non_empty(self, value, field_name):
        if value is None or value == "":
            raise ValueError(f"{field_name} cannot be empty")

    # ------------------------
    # Create
    # ------------------------ 
    def add_memory(self, content: str, emotion: str | None = None, timestamp: str | None = None):
        self._validate_non_empty(content, "Content")

        if timestamp is None:
            timestamp = datetime.now().isoformat()

        with self.conn:
            self.conn.execute("""
                INSERT INTO memories (content, emotion, name, timestamp)
                VALUES (?, ?, ?, ?)
            """, (content, emotion, self.name, timestamp))

    # ------------------------
    # Read
    # ------------------------
    def get_all_memories(self):
        with self.conn:
            rows = self.conn.execute(
                "SELECT * FROM memories ORDER BY timestamp DESC"
            ).fetchall()
            return self._rows_to_dicts(rows)

    
    def get_memories_by_friend(self, friend_name: str):
        self._validate_non_empty(friend_name, "FRIEND NAME")

        with self.conn:
            rows = self.conn.execute(
                "SELECT * FROM memories WHERE name = ? ORDER BY timestamp DESC",
                (friend_name,)
            ).fetchall()
            return self._rows_to_dicts(rows)
        
    def get_memories_by_emotion(self, emotion: str):
        self._validate_non_empty(emotion, "Emotion")

        with self.conn:
            rows = self.conn.execute(
                "SELECT * FROM memories WHERE emotion = ? ORDER BY timestamp DESC",
                (emotion,)
            ).fetchall()
            return self._rows_to_dicts(rows)

    def get_memories_by_name(self, name: str):
        self._validate_non_empty(name, "Name")

        with self.conn:
            rows = self.conn.execute(
                "SELECT * FROM memories WHERE name = ? ORDER BY timestamp DESC",
                (name,)
            ).fetchall()
            return self._rows_to_dicts(rows)

    def get_memories_by_timeframe(self, start_time: str, end_time: str):
        with self.conn:
            rows = self.conn.execute(
                """
                SELECT * FROM memories
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
                """,
                (start_time, end_time)
            ).fetchall()
            return self._rows_to_dicts(rows)
        
    def get_name(self):
        return self.name
    
    def change_name(self, new_name: str):
        self._validate_non_empty(new_name, "New name")

        with self.conn:
            self.conn.execute(
                "UPDATE memories SET name = ? WHERE name = ?",
                (new_name, self.name)
            )
            self.name = new_name

    def get_recent_memories(self, limit: int = 10):
        with self.conn:
            rows = self.conn.execute(
                "SELECT * FROM memories ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return self._rows_to_dicts(rows)

    def search_memories(self, keyword: str):
        self._validate_non_empty(keyword, "Keyword")

        with self.conn:
            rows = self.conn.execute(
                "SELECT * FROM memories WHERE content LIKE ? ORDER BY timestamp DESC",
                (f"%{keyword}%",)
            ).fetchall()
            return self._rows_to_dicts(rows)

    def count_memories(self):
        with self.conn:
            count = self.conn.execute(
                "SELECT COUNT(*) FROM memories"
            ).fetchone()[0]
            return count

    # ------------------------
    # Update
    # ------------------------
    def update_memory(self, memory_id: int, content: str | None = None, emotion: str | None = None):
        if memory_id is None:
            raise ValueError("Memory ID cannot be None")

        if content is None and emotion is None:
            return  # nothing to update

        fields = []
        values = []

        if content is not None:
            fields.append("content = ?")
            values.append(content)

        if emotion is not None:
            fields.append("emotion = ?")
            values.append(emotion)

        values.append(memory_id)

        query = f"UPDATE memories SET {', '.join(fields)} WHERE id = ?"

        with self.conn:
            self.conn.execute(query, values)
            
    # ======================== ADD MEMORY CONNECTIONS & ASSOCIATIONS ========================
    def add_memory_connection(self, memory_id: int, connection_type: str, target_memory_id: int):
        if memory_id is None or target_memory_id is None:
            raise ValueError("Memory IDs cannot be None")

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO memory_connections (memory_id, connection_type, target_memory_id)
                VALUES (?, ?, ?)
                """,
                (memory_id, connection_type, target_memory_id)
            )
            
    def add_memory_of_friend(self, memory_id: int, friend_name: str):
        if memory_id is None:
            raise ValueError("Memory ID cannot be None")
        self._validate_non_empty(friend_name, "Friend name")

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO memory_friends (memory_id, friend_name)
                VALUES (?, ?)
                """,
                (memory_id, friend_name)
            )

    # ------------------------
    # Delete
    # ------------------------
    def delete_memory(self, memory_id: int):
        if memory_id is None:
            raise ValueError("Memory ID cannot be None")

        with self.conn:
            self.conn.execute(
                "DELETE FROM memories WHERE id = ?",
                (memory_id,)
            )

    def wipe_memories(self):
        """Dangerous: deletes everything (no confirmation here)."""
        with self.conn:
            self.conn.execute("DELETE FROM memories")

    
    def remove_memory_of_friend(self, memory_id: int, friend_name: str):
        if memory_id is None:
            raise ValueError("Memory ID cannot be None")
        self._validate_non_empty(friend_name, "Friend name")

        with self.conn:
            self.conn.execute(
                """
                DELETE FROM memory_friends
                WHERE memory_id = ? AND friend_name = ?
                """,
                (memory_id, friend_name)
            )
    # ------------------------
    # Lifecycle
    # ------------------------
    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ------------------------
    # Debug / Representation
    # ------------------------
    def __repr__(self) -> str:
        return f"Database(name='{self.name}', memories={self.count_memories()})"

