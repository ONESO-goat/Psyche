import sqlite3



class Database: 
    def __init__(self, name, brain, db_name='psyche.db'):
        self.name = name
        self.brain = brain
        
        self.force = False
        
        
        if self.force:
            self._warning()
            print("Force mode enabled: All operations will bypass confirmation prompts.")

        
        self.conn = sqlite3.connect(db_name) 
        self.conn.row_factory = sqlite3.Row
        self.create_tables() 
        
    
    def _warning(self) -> None:
        print("WARNING: Force mode is enabled. This will bypass all confirmation prompts and may lead to irreversible actions.\n")
        print("Use with caution!\n")
        print("To disable force mode, set 'self.force = False' in the Database class")
        
    def _message(self, msg):
        print(f"[{self.name}] {msg}")

    def create_tables(self): 
        with self.conn: 
            self.conn.execute(''' CREATE TABLE IF NOT EXISTS memories ( 
                              id INTEGER PRIMARY KEY, 
                              content TEXT, 
                              emotion TEXT, 
                              name TEXT,
                              timestamp TEXT ) ''') 
            
    def add_memory(self, content, emotion, timestamp): 
        with self.conn: 
            self.conn.execute(''' 
                                INSERT INTO memories 
                                (content, 
                                emotion, 
                                name,
                                timestamp) VALUES (?, ?, ?, ?) ''', 
                                (content, emotion, self.name, timestamp)) 
    def get_memories(self): 
        with self.conn: return self.conn.execute(
            'SELECT * FROM memories').fetchall()
        
    def get_memories_by_emotion(self, emotion):
        if not emotion:
            raise ValueError("Emotion cannot be empty")
        
        with self.conn:
            return self.conn.execute(
                'SELECT * FROM memories WHERE emotion = ?',
                (emotion,)
            ).fetchall()
    
    def delete_memory(self, memory_id):
        if memory_id == None or str(memory_id).strip() == '':
            raise ValueError("Memory ID cannot be empty")
        
        with self.conn:
            self.conn.execute(
                'DELETE FROM memories WHERE id = ?',
                (memory_id,)
            )
            
    def get_memories_by_timeframe(self, start_time, end_time):
        with self.conn:
            return self.conn.execute(
                'SELECT * FROM memories WHERE timestamp BETWEEN ? AND ?',
                (start_time, end_time)
            ).fetchall()
            
    def get_memories_by_friend(self, friend_name):
        if not friend_name:
            raise ValueError("Friend name cannot be empty")
        
        with self.conn:
            return self.conn.execute(
                'SELECT * FROM memories WHERE name = ?',
                (friend_name,)
            ).fetchall()
        
    def close(self):
       self.conn.close()
    
    def _wipe_confirmation(self):
        if not self.force:
            print("="*50)
            print("""
                  WARNING: You are about to delete ALL memories from the database. This action is irreversible.
                  Please confirm that you want to proceed.
                  """)
            print("="*50)
            print()
            print("Type 'Y' to confirm, or any other key to cancel.")
            confirm = input("Are you sure you want to delete all memories? (Y/N): ")
            if confirm.lower() != "y":
                print("Operation cancelled.")
                return False
        return True
    
    def wipe(self):
        """Delete all memories."""
        if not self.force:
            check = self._wipe_confirmation()
            if not check:
                return
           

        try:
            self.conn.execute('DELETE FROM memories')
            self.conn.commit()
            print("All memories have been deleted.")
        except Exception as e:
            print(f"Error deleting memories: {e}")
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
       
    def __repr__(self) -> str:
        return f"Database(name='{self.name}', memories={len(self.get_memories())})"
    
    
    
    
    
    
    
    
    
    
    