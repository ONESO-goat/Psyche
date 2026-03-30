# memory_systems.py

from typing import List, Dict, Any
from datetime import datetime
import uuid
import numpy as np


class CyberMemory():
    def __init__(self, storage, Brain, emotions, enthusiasm):
        # TODO 
        """
        Docstring for __init__
        
        CyberMemory is a python package where you can create and access
        advanced memory systems. Though the complexity of this can get confusing,
        the primary goal is a system that varies per brain.


        """

        self.Brain = Brain
        self.memory = [{}]
        self.storage = storage
        self.IS = emotions
        self.was = emotions
        self.enthusiasm = enthusiasm

    def __repr__(self) -> str:
        return f"""CyberMemory(storage='{self.storage}', Brain={self.Brain}, 
        emotions={self.IS})"""
    
class EmotionalCalling:
    """
        Like Riley's memory system in Inside Out.
        
        - Memories have emotional colors
        - Strong emotions create stronger memories
        - Emotions can influence how memories are recalled
        - Mood affects which memories surface
        """
    def __init__(self, storage, brain, emotions):
        self.brain = brain
        self.storage = storage
        self.emotions = emotions  # RileyAnderson instance
        
    def encode_memory(self, content: str, emotion_data: Dict, add_timestamp: bool = False):
        """
        Store memory with emotional tagging.
        
        Like in Inside Out - Joy creates happy memories,
        Sadness creates sad memories, etc.
        """

        # Detect which emotion this is
        dominant_emotion = self._detect_dominant_emotion(emotion_data)
        emotion = emotion_data['emotion']
        # Emotional memories are stronger
        importance = self._calculate_importance(emotion_data, dominant_emotion)
        
        # Store with emotion tag
        memory = {
            'id': str(uuid.uuid4()),
            'content': content,
            'dominant_emotion': dominant_emotion,
            'emotion': emotion,
            'importance': importance, 
            'Enthusiasm': {
                'motivation': np.zeros((3, 4)),
                'inspiration': np.zeros((3,4))
            }, # placeholder for now
            'association': {}

        }


        memory = self.emotions.emotion_query(memory)

        if add_timestamp:
            print(memory['timestamp'])
            memory['timestamp'] = datetime.utcnow().isoformat()

        self.storage.add(memory)

        
        # Update emotion levels
    
    def _detect_dominant_emotion(self, emotion_data: Dict) -> str:
        """Figure out which emotion is strongest."""
        emotion_type = emotion_data.get('emotion', '').lower()
        
        # Check each emotion type
        if self.emotions.Joy._feeling_happy({'emotion': emotion_type}):
            return 'happy'
        elif self.emotions.Sadness._feeling_upset({'emotion': emotion_type}):
            return 'sad'
        elif self.emotions.Anger._feeling_angry({'emotion': emotion_type}):
            return 'angry'
        elif self.emotions.Fear._feeling_fear({'emotion': emotion_type}):
            return 'fearful'
        elif self.emotions.Disgust._feeling_disgust({'emotion': emotion_type}):
            return 'disgusted'
        elif self.emotions.Surprise._feeling_surprised({'emotion': emotion_type}):
            return 'surprised'
        else:
            return 'neutral'
    
    def _calculate_importance(self, emotion_data: Dict, emotion_type: str) -> float:
        """Emotional memories are more important (Inside Out concept)."""
        base_importance = 0.5
        
        # Strong emotions → higher importance
        intensity = emotion_data.get('intensity', 0.5)
        
        if emotion_type != 'neutral':
            base_importance += intensity * 0.5
        
        return min(1.0, base_importance)
    
    def recall_by_emotion(self, emotion_type: str) -> List[Dict]:
        """Get all memories of a specific emotion."""
        all_memories = self.storage.get_all()
        return [m for m in all_memories if m.get('emotion') == emotion_type]
    
    def get_current_mood(self) -> Dict[str, float]:
        """Current emotional state (like the console in Inside Out)."""
        return {
            'joy': self.emotions.Joy.level,
            'sadness': self.emotions.Sadness.level,
            'anger': self.emotions.Anger.level,
            'fear': self.emotions.Fear.level,
            'disgust': self.emotions.Disgust.level,
            'surprise': self.emotions.Surprise.level
        }
    
    def color_memory(self, memory_id: int, new_emotion: str):
        """
        Change emotion tag of existing memory.
        
        Like when Sadness touches Joy's memories in the movie.
        """
        memory = self.storage.find(memory_id)
        if memory:
            old_emotion = memory['emotion']
            memory['emotion'] = new_emotion
            
            # Log the change (memory reconstruction)
            memory['recolored'] = True
            memory['original_emotion'] = old_emotion
            
            self.storage.commit()
    
    def create_core_memory(self, content: str, emotion: str):
        """
        Core memories (extra important, never fade).
        
        Like the personality islands in Inside Out.
        """
        memory = {
            'content': content,
            'emotion': emotion,
            'importance': 1.0,  # Maximum
            'core': True,  # Special flag
            'permanent': True  # Never decays
        }
        
        self.storage.add(memory)
    
    def emotional_recall(self, current_mood: str):
        """
        Mood affects which memories come up.
        
        When Riley is sad, sad memories surface more easily.
        """
        all_memories = self.storage.get_all()
        
        # Memories matching current mood get priority
        mood_matched = [m for m in all_memories if m['emotion'] == current_mood]
        others = [m for m in all_memories if m['emotion'] != current_mood]
        
        # Return mood-congruent memories first
        return mood_matched + others
    def get_memory_id(self, memory: Dict[str, Any]):
        id = memory.get('id', '')
        if id.strip() == '':
            raise ValueError(f"Data doesn't have vald id structure: {memory}")
        return id

