from Psyche_database.Database import Database

class MemoryService:
    def __init__(self, db: Database | None = None):
        if db is None:
            self.db = Database(name="DefaultMemoryDB")
        elif not isinstance(db, Database):
            raise TypeError("db must be an instance of Database")
        else:
            self.db = db
                    
        

    def create_memory(self, content, emotion):
        # business logic here
        self.db.add_memory(content, emotion)
        
    def get_all_memories(self):
        return self.db.get_all_memories()
    
    def get_memories_by_emotion(self, emotion):
        return self.db.get_memories_by_emotion(emotion)
    
    def delete_memory(self, memory_id):
        self.db.delete_memory(memory_id)
        
    def get_memories_by_timeframe(self, start_time, end_time):
        return self.db.get_memories_by_timeframe(start_time, end_time)
    
    def get_memories_by_friend(self, friend_name):
        return self.db.get_memories_by_friend(friend_name)