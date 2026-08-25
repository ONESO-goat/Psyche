from typing import List, Optional, Tuple
from BrainAnomaly.BrainAnomaly import Brain
from BaseAI.Rosalina.meta_rosa import MetaROSA
# from BaseAI.Rosalina.Rosa import rosalina
from BaseAI.LinaXLino.MODEL_LINX import LinaXLino
from Memory.Emotions.Headquarters import Headquarters
from Memory.Emotions.Inside_out import RileyAnderson
from love.friends import Amigo
from Memory.memory_systems import EmotionalCalling
from Drive.Enthusiasm import Enthusiasm
from ASO.ASO import ASO



class Psyche:
    def __init__(self, 
                 gender: str,
                 owner_name: Tuple[str, str, str],
                 name: Tuple[str, str, str], 
                 ai_model: str,
                 ai_api_key: str = '', 
                 pounds: float = 3.0,
                 watts: float = 20.0):
        
        
        """Welcome To Psyche, the heart of CyberLife. 
        This class combines all the core systems into one unified interface to be used in a package. 
        It initializes the Brain, Emotion Systems, Headquarters, and Motivation Systems.

        Args:
            gender (str): The gender of your LINX (Brain)
            owner_name (Tuple[str, str, str]): The name of the owner of the LINX
            name (Tuple[str, str, str]): The name of the LINX
            ai_api_key (str, optional): The API key for the AI model. Defaults to ''.
            ai_model (str, optional): The AI model to use. Defaults to 'qwen'.
            pounds (float, optional): The weight of the brain in pounds. Defaults to 3.0.
            watts (float, optional): The power consumption of the brain in watts. Defaults to 20.0.
        """
        if ai_model not in ['qwen', 'gemini']:
            raise ValueError("Invalid AI model. Supported models are 'qwen' and 'gemini'. More models coming soon!")
        
        # ============ CORE BRAIN ================ #
        self.Brain = Brain(name=name, pounds=pounds, watts=watts)
        self.storage = self.Brain.mind
        self.memories = self.storage.get_current_memories()
        self.watts = watts
        self.pounds = pounds
        
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
        
        # LINX instance (for connecting to ROSA and using AI capabilities)
        self.linx = LinaXLino(
            Brain=self.Brain,
            owners_name=owner_name,
            gender=gender,
            passcode_between_me_and_owner='secret123',
            api_key=ai_api_key,
            model=ai_model
        )
        
        # ============ ASSOCIATION SYSTEM ======== #
        self.aso = ASO(Brain=self.Brain)
        
        # ============ ROSA CONNECTION =========== #
        self.rosa = None  # Will be set when connected to ROSA
        
        # ============ IDENTITY ================== #
        self.name = self.Brain.get_fullname()
        self.first_name = self.Brain.first_name
        self.last_name = self.Brain.last_name
        self.middle_name = '' # Default to empty string, will be set if middle name exists
        if self.Brain.middle_name:
            self.middle_name = self.Brain.middle_name
        
        self.nicknames: List[str] = []
        self.set_up_first_password()  # Prompt user to set up first password for owner access
        
    def connect_to_rosa(self, rosa: MetaROSA):
        """Connect the LINX to ROSA for enhanced AI capabilities."""
        self.rosa = rosa
        self.linx.rosa = rosa  # Connect LINX to ROSA
        
    def add_nickname(self, nickname: str):
        """Add a nickname for the LINX."""
        self.nicknames.append(nickname)
    
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
        
    def replace_brain(self, new_brain: Brain):
        """Replace the current brain with a new one."""
        self.Brain = new_brain
        self.storage = self.Brain.mind
        self.memories = self.storage.get_current_memories()
        self.HQ.Brain = new_brain
        self.management.brain = new_brain
        self.enthusiasm.Brain = new_brain
        self._amigo.new_brain(new_brain=new_brain)
        self.linx.Brain = new_brain
        self.friends.Brain = new_brain
        if self.rosa:
            self.linx.Brain = new_brain  # Update LINX brain if connected to ROSA
        
    def set_up_first_password(self):
        print("Setting up first password for owner access...")
   
        
        while True:
            user = input("Passcode | secret phrase: ")
            if not user:
                print("Passcode cannot be empty. Please try again.")
                continue
            
            if len(user) < 6:
                print("Passcode must be at least 6 characters long. Please try again.")
                continue
            
            self.linx._set_passcode_(user)
            break
    
    def visualize(self, mode: str = '2D'):
        """Show brain visualization."""
        self.Brain.showcase(mode=mode)

