# psyche_test.py - Test script for Psyche class and overall functionality.

from typing import Dict, Tuple, Any, Optional, List

from BrainAnomaly.BrainAnomaly import Brain
from Memory.Emotions.Headquarters import Headquarters
from Memory.Emotions.Inside_out import RileyAnderson
from love.friends import Amigo
from Memory.memory_systems import EmotionalCalling
from Drive.Enthusiasm import Enthusiasm
from ASO.ASO import ASO



class Psyche:
    """
    Main interface for CyberLife cognitive architecture.
    Combines all systems into one unified API.
    """
    
    def __init__(self, 
                 name: Tuple[str, str, str], 
                 ai_api_key: str = '', 
                 model: str = 'qwen',
                 pounds: float = 3.0,
                 watts: float = 20.0):
        
        # ============ CORE BRAIN ================ #

        self.Brain = Brain(name=name, pounds=pounds, watts=watts)
        self.storage = self.Brain.mind
        self.memories = self.storage.get_current_memories()
        
        # ============ EMOTION SYSTEMS =========== #
        self.Emotions = RileyAnderson()
        self.management = EmotionalCalling(
            storage=self.storage, 
            brain=self.Brain, 
            emotions=self.Emotions
        )
        
        # Individual emotions (shortcuts)
        self.Joy = self.Emotions.Joy
        self.Sadness = self.Emotions.Sadness
        self.Anger = self.Emotions.Anger
        self.Fear = self.Emotions.Fear
        self.Disgust = self.Emotions.Disgust
        self.Surprise = self.Emotions.Surprise
        
        self.operator = self.Emotions.get_dominant_emotion()
        
        # ============ HEADQUARTERS ============== #
        self.HQ = Headquarters(Brain=self.Brain, memories=self.memories)
        
        # ============ MOTIVATION SYSTEMS ======== #
        self.enthusiasm = Enthusiasm(Brain=self.Brain)
        
        # ============ SOCIAL SYSTEMS ============ #
        self._amigo = Amigo(Brain=self.Brain, name=self.Brain.first_name)
        self.friends = self._amigo._friends
        
        # Friendship operators
        self.Meg = self._amigo.Meg      # Past friendships
        self.Bree = self._amigo.Bree    # Long-term friendships
        self.Grace = self._amigo.Grace  # Short-term friendships
        self.Val = self._amigo.Val      # Rivalry/jealousy
        
        # ============ ASSOCIATION SYSTEM ======== #
        self.ASO = ASO(
            Brain=self.Brain, 
            api_key=ai_api_key
        )
        
        # ============ IDENTITY ================== #
        self.name = self.Brain.get_fullname()
        self.first_name = self.Brain.first_name
        self.last_name = self.Brain.last_name
        
        self.watts = self.Brain.power
        self.pounds = self.Brain.brain_size
        
        # Nicknames
        self.nicknames: List[str] = []
    
    def new_memory(self, context: str, emotion: Optional[str] = None, importance: float = 0.5):
        """Create a new memory."""
        
        
        try:
            emotiondata = {'emotion': emotion, 'intensity': importance}
            self.management.encode_memory(
                content=context,
                emotion_data=emotiondata,
            )
        except Exception as e:
            print(f"Error encoding memory: {e}")
            return

    def recall_all(self):
        """Get all memories."""
        return self.Brain.recall_all()
    
    def add_friend(self, 
                   who: str, 
                   where: str, 
                   friendship_type: str = 'short',
                   rating: float = 5.0,
                   nicknames: List[str] = []):
        """Add a new friend."""
        self.friends.connect(
            who=who,
            environment=where,
            type_of_friendship=friendship_type,
            how_much_you_like_this_person=rating,
            details={'nickname': nicknames} if nicknames else {}
        )
    
    def focus_on_memory(self, memory_id: str):
        """Focus headquarters on a memory."""
        self.HQ.focus(id=memory_id)
    
    def get_brain_state(self):
        """Get current overall state."""
        return {
            'name': self.name,
            'memory_count': len(self.memories),
            'dominant_emotion': self.operator.name,
            'brain_power': f"{self.watts}W",
            'brain_size': f"{self.pounds}lbs"
        }
    
    def visualize(self, mode: str = '2D'):
        """Show brain visualization."""
        self.Brain.showcase(mode=mode)


 
# Example usage
if __name__ == '__main__':
    # Create psyche
    import dotenv
    import os
    
    dotenv.load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    psyche = Psyche(
        name=('Julius','', 'Smith'),
        ai_api_key=gemini_key
    )
    
    # Add memories
    psyche.new_memory("Met Sarah at the coffee shop", emotion="happy", importance=0.7)
    psyche.new_memory("Got rejected from MIT", emotion="sad", importance=0.9)
    
    # Add friends
    psyche.add_friend(
        who="Sarah",
        where="coffee shop",
        friendship_type="short",
        rating=7.5,
        nicknames=["Sare", "S"]
    )
    
    # Focus on memory
    memories = psyche.recall_all()
    if memories:
        psyche.focus_on_memory(memories[0]['id'])
        
        # Adjust emotion
        psyche.HQ.ROW1.adjust(by=0.3)
    
    # Check state
    print(psyche.get_brain_state())
    
    # Visualize
    psyche.visualize()