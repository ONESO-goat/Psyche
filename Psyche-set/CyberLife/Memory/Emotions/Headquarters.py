# Headquarters.py

import numpy as np
import uuid
import copy
from Excepts_and_hints import InvalidEmotion, InvalidRow, ValidEmotion, NoArgumentCalled_or_AllNone
from numpy_utils.numpy_helpers import serialize_numpy, deserialize_numpy
from typing import Protocol, Optional, Tuple, Dict, Any

class Orb(Protocol):
    ...


class ValidStructure:
    def __init__(self, row: np.ndarray):
        
        row = row.copy()
        self.validate_row(row)

    def validate_row(self, row: np.ndarray):
        # Check that it’s a NumPy array
       
        if not isinstance(row, np.ndarray):
            raise InvalidRow("Row must be a Numpy array")

       
        # Check shape
        if row.shape != (4,4):
            raise InvalidRow(
                f"""Invalid row shape.
    Please make sure to follow this order:

    [0. 0. 0. 0.]
    [0. 0. 0. 0.]
    [0. 0. 0. 0.]
    [0. 0. 0. 0.]

    current:
    {row.shape}
    """
            )

        # Optional: Check dtype
        if row.dtype != np.float64:
            raise ValueError(f"Invalid dtype {row.dtype}, expected float64")

        # Optional: Ensure it's writable
        if not row.flags.writeable:
            raise ValueError("Array is read-only. Use .copy() to make it writable.")
        
    def _assign(self, row, memory):
        regulation = "regulation"
        fixed = {regulation: {
          "__numpy__": row,
          "dtype": "<f8",
          "shape": [
            4,
            4
          ]
        }}
        emotion = list(memory.get('emotion', 0).keys())[0]
        memory['emotion'][emotion] = fixed


class Prefrontal_Control(ValidStructure):
    """
    Prefrontal control controls emotion intensity, how much it impacts,
    regulations, etc.

    pythonrow_0 = [
    current_intensity,      # 0.0-1.0: How strong is emotion RIGHT NOW
    regulation_strength,    # 0.0-1.0: How much are we suppressing/amplifying it
    reappraisal_capacity,   # 0.0-1.0: Ability to reinterpret situation (high = resilient)
    inhibition_level        # 0.0-1.0: How much we're holding back expression
]
    """
    def __init__(self,focused_memory, row: np.ndarray, Brain):
        super().__init__(row=row)
        self.focused_memory = focused_memory
        self.focused_memory_copy = copy.deepcopy(focused_memory)
        
        self.emotion = list(self.focused_memory.get('emotion', 0).keys())[0]
        self.memory_shortcut = self.focused_memory['emotion'][self.emotion]['regulation'][0]
        self.first_row = np.array(row[0], dtype=np.float64) 
        self.first_row.flags.writeable = True
       
        """The first row inside memory (4x4) array."""

        #self.current_emotion = current_emotion.lower()

        self.Brain = Brain

    
    def adjust(self, by: float, index: int = 0, auto: bool = True,
           accelerate: Tuple[bool, float] = (False, 0), get: bool = True):
        

        by = float(by)

        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        
        target = self.first_row[index]
       

        if accelerate[0] and accelerate[1] > 0:
            by *= accelerate[1]
        elif accelerate[0] and accelerate[1] <= 0:
            raise ValueError("Invaid acclertation amount.")

        target += by

        target = np.round(target, 4)

        target = max(0.0, min(target, 1.0))


        self.first_row[index] = target
        
        current_regulation = self.focused_memory_copy['emotion'][self.emotion]['regulation']
    
        new_regulation = np.array(current_regulation, dtype=np.float64)

        new_regulation[0] = self.first_row
    
        self.focused_memory_copy['emotion'][self.emotion]['regulation'] = new_regulation
    
        self.Brain.mind.replace(old=self.focused_memory, new=self.focused_memory_copy,auto_save=True)
        
        if auto:
            self.Brain.mind.commit()
        if get:
            return self.get_row1()
        return self.first_row
        
    def get_row1(self):
        return self.first_row

    def __repr__(self) -> str:
        return f"Prefrontal_Control(self, row={self.first_row}, Brain={self.Brain})"
    
class  Physiological_Response(ValidStructure):

    def __init__(self,focused_memory, row: np.ndarray, Brain):
        super().__init__(row=row)
        self.focused_memory = focused_memory
        self.focused_memory_copy = focused_memory
        
        self.emotion = list(self.focused_memory.get('emotion', 0).keys())[0]
        self.memory_shortcut = self.focused_memory['emotion'][self.emotion]['regulation'][0]
        self.second_row = np.array(row[1], dtype=np.float64) 
        self.second_row.flags.writeable = True
       
        """The second row inside memory (4x4) array."""

        #self.current_emotion = current_emotion.lower()

        self.Brain = Brain

    
    def adjust(self, by: float, index: int = 0, auto: bool = True,
           accelerate: Tuple[bool, float] = (False, 0), get: bool = True):
        

        by = float(by)

        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        
        target = self.second_row[index]
        

        if accelerate[0] and accelerate[1] > 0:
            by *= accelerate[1]
        elif accelerate[0] and accelerate[1] <= 0:
            raise ValueError("Invaid acclertation amount.")

        target += by

        target = np.round(target, 4)

        target = max(0.0, min(target, 1.0))


        self.second_row[index] = target
        
        current_regulation = self.focused_memory_copy['emotion'][self.emotion]['regulation']
    
        new_regulation = np.array(current_regulation, dtype=np.float64)

        new_regulation[1] = self.second_row
    
        self.focused_memory_copy['emotion'][self.emotion]['regulation'] = new_regulation
    
 

        self.Brain.mind.replace(old=self.focused_memory, new=self.focused_memory_copy,auto_save=True)
        
        if auto:
            self.Brain.mind.commit()
        if get:
            return self.get_row2()
        
    def get_row2(self):
        return self.second_row

    def __repr__(self) -> str:
        return f"Physiological_Response(self, row={self.second_row}, Brain={self.Brain})"

class Expression__Communication(ValidStructure):
    """Controls facial expressions

        Modulates voice tone and volume
        Drives body language (posture, gestures)
        Sends social signals to others

        Columns:
        pythonrow_2 = [
            facial_intensity,   # 0.0-1.0: How much is showing on face (0 = poker face, 1 = very expressive)
            vocal_expression,   # 0.0-1.0: Voice tone/volume modulation (0 = flat, 1 = highly expressive)
            body_language,      # 0.0-1.0: Posture/gesture intensity (0 = still, 1 = animated)
            social_signal       # 0.0-1.0: Overall communicativeness (0 = hidden, 1 = broadcasting)
]

    # Pride (showing off)
    [0.8, 0.7, 0.8, 0.9]  # Big smile, confident voice, open posture, clearly broadcasting

    # Shame (hiding it)
    [0.2, 0.3, 0.2, 0.1]  # Neutral face, quiet voice, closed posture, hiding feeling

    # Anger (trying not to show it)
    [0.4, 0.3, 0.6, 0.3]  # Some tension visible, controlled voice, tense posture, somewhat hiding


"""
    def __init__(self,focused_memory, row: np.ndarray, Brain):
        super().__init__(row=row)
        self.focused_memory = focused_memory
        self.focused_memory_copy = focused_memory
        
        self.emotion = list(self.focused_memory.get('emotion', 0).keys())[0]
        self.memory_shortcut = self.focused_memory['emotion'][self.emotion]['regulation'][0]
        self.third_row = np.array(row[2], dtype=np.float64) 
        self.third_row.flags.writeable = True
       
        """The third row inside memory (4x4) array."""

        #self.current_emotion = current_emotion.lower()

        self.Brain = Brain

    
    def adjust(self, by: float, index: int = 0, auto: bool = True,
           accelerate: Tuple[bool, float] = (False, 0), get: bool = True):
        

        by = float(by)

        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        
        target = self.third_row[index]


        if accelerate[0] and accelerate[1] > 0:
            by *= accelerate[1]
        elif accelerate[0] and accelerate[1] <= 0:
            raise ValueError("Invaid acclertation amount.")

        target += by

        target = np.round(target, 4)

        target = max(0.0, min(target, 1.0))


        self.third_row[index] = target
        
        current_regulation = self.focused_memory_copy['emotion'][self.emotion]['regulation']
    
        new_regulation = np.array(current_regulation, dtype=np.float64)

        new_regulation[2] = self.third_row
    
        self.focused_memory_copy['emotion'][self.emotion]['regulation'] = new_regulation
    
 

        self.Brain.mind.replace(old=self.focused_memory, new=self.focused_memory_copy,auto_save=True)
        if auto:
            self.Brain.mind.commit()
        if get:
            return self.get_row3()
        
    def get_row3(self):
        return self.third_row

    def __repr__(self) -> str:
        return f"Expression__Communication(self, row={self.third_row}, Brain={self.Brain})"


        
        

class Dopamine(ValidStructure):
    """
    Evaluates reward value of situation
    Creates expectations about outcomes
    Detects prediction errors (better/worse than expected)
    Drives approach (move toward) or avoidance (move away)

    Columns:
    pythonrow_3 = [
        reward_value,         # 0.0-1.0: How rewarding is this situation (0 = punishing, 0.5 = neutral, 1 = highly rewarding)
        expectation,          # 0.0-1.0: What we expected to happen (for comparison)
        prediction_error,     # -1.0 to +1.0: Actual - Expected (negative = disappointed, positive = pleasantly surprised)
        approach_tendency     # 0.0-1.0: Drive to approach (1.0) or avoid (0.0)
    ]
    Example values:
    python# Pride (exceeded expectations, want more)
    [0.9, 0.5, 0.4, 0.9]  # High reward, expected medium, positive surprise, strong approach

    # Disappointment (worse than expected)
    [0.2, 0.7, -0.5, 0.3]  # Low reward, expected high, negative surprise, weak approach

    # Fear (potential threat, avoid)
    [0.1, 0.5, -0.4, 0.1]  # Negative outcome, expected neutral, bad surprise, strong avoidance
    
    """
    def __init__(self,focused_memory, row: np.ndarray, Brain):
        super().__init__(row=row)
        self.focused_memory = focused_memory
        self.focused_memory_copy = focused_memory
        
        self.emotion = list(self.focused_memory.get('emotion', 0).keys())[0]
        self.memory_shortcut = self.focused_memory['emotion'][self.emotion]['regulation'][0]
        self.fourth_row = np.array(row[3], dtype=np.float64) 
        self.fourth_row.flags.writeable = True
       
        """The first row inside memory (4x4) array."""

        #self.current_emotion = current_emotion.lower()

        self.Brain = Brain

    
    def adjust(self, by: float, index: int = 0, auto: bool = True,
           accelerate: Tuple[bool, float] = (False, 0), get: bool = True):
        

        by = float(by)

        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        
        target = self.fourth_row[index]


        if accelerate[0] and accelerate[1] > 0:
            by *= accelerate[1]
        elif accelerate[0] and accelerate[1] <= 0:
            raise ValueError("Invaid acclertation amount.")

        target += by

        target = np.round(target, 4)

        target = max(0.0, min(target, 1.0))


        self.fourth_row[index] = target
        
        current_regulation = self.focused_memory_copy['emotion'][self.emotion]['regulation']
    
        new_regulation = np.array(current_regulation, dtype=np.float64)

        new_regulation[3] = self.fourth_row
    
        self.focused_memory_copy['emotion'][self.emotion]['regulation'] = new_regulation
    
 

        self.Brain.mind.replace(old=self.focused_memory, new=self.focused_memory_copy,auto_save=True)
        if auto:
            self.Brain.mind.commit()
        if get:
            return self.get_row4()
        
    def get_row4(self):
        return self.fourth_row

    def __repr__(self) -> str:
        return f"Expression__Communication(self, row={self.fourth_row}, Brain={self.Brain})"












class EmotionRegulation:
    """
    Models emotion as distributed brain system.
    Based on actual neuroscience.
    """
    
    def __init__(self, emotion_type: str,Brain, focused_memory, 
                 amount: float = 0.0, auto_save: bool = True):
        
        self.emotion_type = emotion_type.lower()
        self.focused_memory = focused_memory
        self.focused_memory_copy = focused_memory
        # 4x4 matrix: [prefrontal, physiological, expression, reward]
        self.emotion = list(self.focused_memory.get('emotion', 0).keys())[0]
        self.state = self.focused_memory['emotion'][self.emotion]['regulation']
        self.Brain = Brain
        # Initialize based on emotion type
        self._initialize_baseline(amount=amount, auto_save=auto_save)
    
    def _initialize_baseline(self, amount: float, auto_save: bool = True):
        """Set baseline values for this emotion."""
        
        baselines = {
            'sad': {
                'reward_value': amount,       # Positive outcome
                'approach_tendency': amount,  # Want more
                'arousal': amount,           # Energized
                'energy': amount             # Energizing emotion
            },
            'shame': {
                'reward_value': amount,
                'approach_tendency': amount,  # Avoid
                'arousal': amount,
                'energy': amount             # Draining
            },
            'fear': {
                'reward_value': amount,       # Threat
                'approach_tendency': amount,  # Strong avoid
                'arousal': amount,            # High activation
                'energy': amount             # Draining but mobilizing
            },
            'happy': {
                'reward_value': amount,
                'approach_tendency': amount,
                'arousal': amount,
                'energy': amount
            },'anger': {
                'reward_value': amount,
                'approach_tendency': amount,
                'arousal': amount,
                'energy': amount
            },'surprise': {
                'reward_value': amount,
                'approach_tendency': amount,
                'arousal': amount,
                'energy':  amount
            },'disgust': {
                'reward_value': amount,
                'approach_tendency': amount,
                'arousal': amount,
                'energy': amount
            }
        }


    
        new_regulation = np.array(self.state, dtype=np.float64)
        print(f"NEW REGULATION: {new_regulation}\n")

    

        baseline = baselines.get(self.emotion_type, {})
        print(f"BASELINE: {baseline}\n")
        
        # Set reward row
        new_regulation[3, 0] = baseline.get('reward_value', 0.0)
        new_regulation[3, 3] = baseline.get('approach_tendency', 0.0)
        
        # Set physiological row
        new_regulation[1, 0] = baseline.get('arousal', 0.0)
        new_regulation[1, 3] = baseline.get('energy', 0.0)

        print(f"\nNEW REGULATION: {new_regulation}\n")
        self.focused_memory_copy['emotion'][self.emotion]['regulation'] = new_regulation
        print(f"COPY: {self.focused_memory_copy}, NOW REPLACEING...\n")
        self.Brain.mind.replace(old=self.focused_memory, 
                                new=self.focused_memory_copy, 
                                auto_save=True)
        
        if auto_save:
            self.Brain.mind.commit()
        
    
    def trigger(self, intensity: float, context: dict):
        """
        Trigger emotion with given intensity.
        Context affects how it manifests.
        """
        
        # Update prefrontal (cognitive layer)
        self.state[0, 0] = intensity  # Current intensity
        self.state[0, 2] = context.get('reappraisal', 0.5)  # Can you reframe it?
        
        # Update physiological
        self.state[1, 0] = intensity * 0.8  # Arousal tracks intensity
        self.state[1, 1] = 0.5 + intensity * 0.3  # Heart rate
        
        # Update expression
        social_context = context.get('social', True)
        if social_context:
            self.state[2, 0] = intensity * 0.7  # Show it on face
            self.state[2, 3] = intensity * 0.8  # Social signaling
        else:
            self.state[2, 0] = intensity * 0.3  # Suppress expression
            self.state[2, 3] = intensity * 0.2
    
    def regulate(self, strategy: str):
        """
        Apply emotion regulation strategy.
        """
        
        if strategy == 'reappraisal':
            # Cognitive reframing reduces intensity
            self.state[0, 1] = 0.8  # High regulation
            self.state[0, 0] *= 0.7  # Reduce intensity
        
        elif strategy == 'suppression':
            # Hide expression but intensity remains
            self.state[0, 3] = 0.9  # High inhibition
            self.state[2, :] *= 0.3  # Reduce all expression
        
        elif strategy == 'acceptance':
            # Allow emotion without fighting it
            self.state[0, 1] = 0.3  # Low regulation
            self.state[1, 3] += 0.1  # Less energy drain
    
    def update(self, time_step: float = 0.1):
        """
        Run one time step of emotion dynamics.
        Emotions change over time based on interactions.
        """
        self.state = self.emotion_dynamics(emotion_matrix=self.state, time_step=time_step)
    
    def get_state(self) -> dict:
        """Get human-readable state."""
        return {
            'intensity': self.state[0, 0],
            'regulation': self.state[0, 1],
            'arousal': self.state[1, 0],
            'energy': self.state[1, 3],
            'expression': self.state[2, 3],
            'reward_value': self.state[3, 0],
            'approach': self.state[3, 3]
        }
    
    def to_dict(self) -> dict:
        """For JSON storage."""
        return {
            'regulation': self.state  # numpy array
        }


    def emotion_dynamics(self, emotion_matrix: np.ndarray, time_step: float) -> np.ndarray:
        """
        Emotions are dynamic - each row influences the others.
        This models how they interact over time.
        """
        
        # Unpack current state
        prefrontal = emotion_matrix[0]  # Row 0
        physiological = emotion_matrix[1]  # Row 1
        expression = emotion_matrix[2]  # Row 2
        reward = emotion_matrix[3]  # Row 3
        
        # === INTERACTIONS ===
        
        # 1. Physiological arousal makes regulation harder
        # High arousal → harder to control
        regulation_difficulty = 1.0 - physiological[0] * 0.5
        prefrontal[1] *= regulation_difficulty
        
        # 2. Strong regulation reduces expression
        # If you're holding back, less shows externally
        expression[3] *= (1.0 - prefrontal[3] * 0.3)  # Inhibition reduces social signal
        
        # 3. Reward value influences arousal
        # Positive outcomes energize, negative ones drain
        if reward[0] > 0.5:
            physiological[3] += 0.1  # Gain energy
        else:
            physiological[3] -= 0.1  # Lose energy
        
        # 4. Prediction errors drive arousal
        # Surprises (positive or negative) increase activation
        arousal_boost = abs(reward[2]) * 0.2
        physiological[0] += arousal_boost
        
        # 5. Facial expression provides feedback (facial feedback hypothesis)
        # Smiling makes you happier, frowning makes you sadder
        if expression[0] > 0.7:
            prefrontal[0] += 0.05  # Expressing intensifies feeling
        
        # 6. Energy depletion reduces regulation capacity
        # Tired → less self-control
        if physiological[3] < 0.3:
            prefrontal[1] *= 0.7  # Weakened regulation
        
        # Clamp values
        emotion_matrix = np.clip(emotion_matrix, 0.0, 1.0)
        
        return emotion_matrix
    
class Headquarters(EmotionRegulation):
    def __init__(self, memories, Brain, Operator: ValidEmotion = 'joy'):
        
        self.Operator = Operator
        self.Brain = Brain
        self.Memory_orbs = memories
        self.focused_memory = None
        self.focused_memory_operator: str = ''
    


    def focus(self, memory: Dict[str, Any] = {}, 
              id: Optional[uuid.UUID | str] = None, regulation_amount: float = 0.0):
        """Focus on a certain memory"""
        if id is not None and not memory:
            try:
                there = self.Brain.mind.find(id=id)
                print(f"THERE: {there}\n")
                
                
                dom_emotion_check  = there.get('dominant_emotion', 0)
                if not dom_emotion_check:
                    raise InvalidEmotion(f"While focusing on memory, the dominant emotion is invalid; ({there})")
                emotion = list(there['emotion'].keys())[0]
                dom_emotion = there['dominant_emotion']
                self.focused_memory = there
                self.focused_memory_operator = dom_emotion.lower()
            
            except RuntimeError as x:
                raise x
            
        elif memory is not None and id is None:
            self.focused_memory = memory
            there = memory.get('dominant_emotion', 0)
            if not there:
                raise InvalidEmotion(f"While focusing on memory, the dominant emotion is invalid; ({there})")
            
            emotion = list(memory['emotion'].keys())[0]
            
            self.focused_memory_operator = there.lower()
            
        else:
            raise NoArgumentCalled_or_AllNone("Please choose one out of the two options [memory] or [id]")
        


        self.ROW1 = Prefrontal_Control(focused_memory=self.focused_memory, row=self.focused_memory['emotion'][emotion]['regulation'], Brain=self.Brain)
        print(" ✓ ROW1 COMPLETE")
        self.ROW2 = Physiological_Response(focused_memory=self.focused_memory, row=self.focused_memory['emotion'][emotion]['regulation'],Brain=self.Brain)
        print(" ✓ ROW2 COMPLETE")
        self.ROW3 = Expression__Communication(focused_memory=self.focused_memory, row=self.focused_memory['emotion'][emotion]['regulation'], Brain=self.Brain)
        print(" ✓ ROW3 COMPLETE")
        self.ROW4 = Dopamine(focused_memory=self.focused_memory, row=self.focused_memory['emotion'][emotion]['regulation'], Brain=self.Brain)
        print(" ✓ ROW4 COMPELTE")
        super().__init__(emotion_type=self.focused_memory_operator, 
                         focused_memory=self.focused_memory, 
                         Brain=self.Brain, 
                         amount=regulation_amount)

    def change_mood(self, new_mood: str, reason: str = 'unknown'):
        """
        Change the dominant emotion of focused memory.
        Like when Sadness touches Joy's memories in Inside Out.
        """
        if not self.focused_memory:
            raise ValueError("No memory focused")
        
        old_emotion = self.focused_memory_operator
        
        # Create new emotion regulation for new mood
        new_regulation = EmotionRegulation(emotion_type=new_mood, focused_memory=self.focused_memory, Brain=self.Brain)
        new_regulation.trigger(
            intensity=self.focused_memory['emotional_intensity'],
            context={'social': True}
        )
        
        # Update memory
        self.focused_memory['dominant_emotion'] = new_mood
        self.focused_memory['emotion'] = {
            new_mood: new_regulation.to_dict()
        }
        self.focused_memory['why_this_feeling'] = reason
        
        # Log the change
        self.focused_memory['recolored'] = True
        self.focused_memory['original_emotion'] = old_emotion
        
        # Save
        self.Brain.mind.commit()
        
        print(f"Memory recolored: {old_emotion} → {new_mood}")
        print(f"Reason: {reason}")

    def update_memory(self):
        """Write changes back to memory."""
        if not self.focused_memory:
            return
        
        # Rebuild the full 4x4 matrix
        updated_matrix = np.array([
            self.ROW1.first_row,
            self.ROW2.second_row,
            self.ROW3.third_row,
            self.ROW4.fourth_row
        ])
        
        # Serialize and save
        emotion_key = self.focused_memory_operator
        self.focused_memory['emotion'][emotion_key]['regulation'] = serialize_numpy(updated_matrix)
        
        # Commit to storage
        self.Brain.mind.commit()

    def get_regulation_matrix(self, memory):
        """Get regulation matrix, handling both formats."""
        emotion = list(memory['emotion'].keys())[0]
        reg = memory['emotion'][emotion]['regulation']
        
        # If serialized, deserialize
        if isinstance(reg, dict) and '__numpy__' in reg:
            return deserialize_numpy(reg)
        
        # Already numpy array
        return reg

    def total_Dopamine(self) -> float:
        """Get total dopamine level (0.0 to 4.0)."""
        if not self.ROW4:
            return 0.0
        return float(np.sum(self.ROW4.get_row4()))




