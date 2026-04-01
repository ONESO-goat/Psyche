from pyparsing import Dict
from typing import List, Dict, Any
from Psyche_database.Database import Database

class MemoryService:
    def __init__(self, db: Database | None = None):
        """ MemoryService manages all memory-related operations.
        If no Database instance is provided, it will create a default one."""
        
        self.force = False  # For wipe confirmation
        
        if db is None:
            self.db = Database(name="DefaultMemoryDB")
        elif not isinstance(db, Database):
            raise TypeError("db must be an instance of Database")
        else:
            self.db = db
                    
        
    # ======================= MEMORY MANAGEMENT =======================
    
    def add_memories_from_list(self, memories: List[Dict]):
        for memory in memories:
            self.create_memory(memory['content'], memory['emotion'])
            
    def create_memory(self, content, emotion):
        # business logic here
        self.db.add_memory(content, emotion)
        
    def delete_memory(self, memory_id):
        """Delete a memory by ID."""
        self.db.delete_memory(memory_id)
    
    
    # ======================= GET FUNCTIONS =======================
    def get_memory_stats(self):
        memories = self.db.get_all_memories()
        emotion_counts = {}
        for memory in memories:
            emotion = memory['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        return emotion_counts
    
    def get_memories_by_timeframe(self, start_time, end_time):
        return self.db.get_memories_by_timeframe(start_time, end_time)
    
    def get_memories_by_friend(self, friend_name):
        return self.db.get_memories_by_friend(friend_name)
    
    def get_memory_by_context(self, content):
        memories = self.db.get_all_memories()
        for memory in memories:
            if content in memory['content']:
                return memory
        return None
    
    def get_memory_by_id(self, memory_id):
        memories = self.db.get_all_memories()
        for memory in memories:
            if memory['id'] == memory_id:
                return memory
        return None
    
    def get_all_memories(self):
        return self.db.get_all_memories()
    
    def get_memories_by_emotion(self, emotion):
        return self.db.get_memories_by_emotion(emotion)
    
    
    # ======================= ANALYTICS & INSIGHTS =======================
    def get_common_themes(self, top_n=5):
        memories = self.db.get_all_memories()
        theme_counts = {}
        for memory in memories:
            content = memory['content']
            # Simple keyword extraction (could be improved with NLP)
            words = content.split()
            for word in words:
                theme_counts[word] = theme_counts.get(word, 0) + 1
        
        # Sort themes by frequency
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_themes[:top_n]
    
    
    def change_memory_emotion(self, memory_id, new_emotion):
        memory = self.get_memory_by_id(memory_id)
        if memory:
            self.db.delete_memory(memory_id)
            self.db.add_memory(memory['content'], new_emotion, memory['timestamp'])
            return True
        return False
    
    def change_memory_content(self, memory_id, new_content):
        memory = self.get_memory_by_id(memory_id)
        if memory:
            self.db.delete_memory(memory_id)
            self.db.add_memory(new_content, memory['emotion'], memory['timestamp'])
            return True
        return False
    
    def change_memory_friend(self, memory_id, new_friend):
        memory = self.get_memory_by_id(memory_id)
        if memory:
            self.db.remove_memory_of_friend(memory_id, memory['name'])
            self.db.add_memory_of_friend(memory_id, new_friend)
            return True
        return False
    
    def change_name(self, new_name):
        self.db.change_name(new_name)
    
    
    def wipe_memories(self, confirmation: bool = False):
        
        if self.force: confirmation = True  # Force bypasses confirmation
        
        if not confirmation:
            raise ValueError("Confirmation required to wipe memories")
        
        check = self._wipe_confirmation()
        if not check:
            return

        self.db.wipe_memories()
        print("All memories have been deleted.")
        
        
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
    
