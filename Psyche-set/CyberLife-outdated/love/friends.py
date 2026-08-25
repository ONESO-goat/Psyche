# friends.py - manage friendships and social connections.

from love.love import love
import copy
from datetime import date
from typing import List, Dict, Any, Optional

from BrainAnomaly.BrainAnomaly import Brain

class friends(love):
    """
    This class focuses on making friends and structures.
    """
    def __init__(self, operator: str, Brain, ai = ''):
        super().__init__(Brain=Brain, who=operator)  # ← Call parent init
        
        self._Brain = Brain
        self.operator = operator
        self.memories = copy.deepcopy(self._Brain.mind.get_all())
        
   
        brain_data = self._Brain.mind.memories[0]
        
        # Ensure friends dict exists
        if 'friends' not in brain_data['brain']['_personal_data']:
            brain_data['brain']['_personal_data']['friends'] = {}
        
        self.friends = brain_data['brain']['_personal_data']['friends']
        self.ai = ai
        self.auto_accept: bool = False

    def connect(self, 
                who: str,
                environment: str,
                details: Dict[str, Any] = {},
                type_of_friendship: str = 'short',
                length: int | None = 7,
                how_much_you_like_this_person: float = 5.0):
        
        """
    Establishes and records a structured "connection" (i.e., friendship or relationship)
    with an individual inside the system's internal memory model.

    This method normalizes input, validates key fields, optionally extracts metadata
    (such as nicknames), and persists the resulting relationship into the agent's
    internal "brain" data structure. It is designed to be tolerant of imperfect input,
    silently ignoring certain invalid cases while strictly enforcing others.

    -------------------------------------------------------------------------------
    PARAMETERS
    -------------------------------------------------------------------------------
    who : str
        The name of the individual to connect with.

        - Must be a non-empty string after stripping whitespace.
        - If empty or less than 1 character after stripping, the function exits early.
        - The name is normalized by:
            - Stripping leading/trailing whitespace
            - Capitalizing the first letter (e.g., "alice" → "Alice")
        - This normalized value is used as the unique key in memory storage.

    environment : str
        Describes the context or setting where the connection was formed.

        Examples:
            - "school"
            - "work"
            - "gym"
            - "online community"

        Constraints and behavior:
        - Must be at least 3 characters long after stripping whitespace.
        - If invalid, the function exits early without raising an error.
        - The value is normalized to lowercase before storage.

    details : Dict[str, Any], optional (default = {})
        Optional metadata about the person.

        Supported keys:
        - 'nickname':
            - Can be either:
                - A single string
                - A list of strings
            - Each nickname is:
                - Stripped of whitespace
                - Validated via `self._validate_name`
                - Capitalized before storage
            - Invalid nickname formats (non-str/list) are ignored silently.

        Notes:
        - This dictionary is not deeply validated beyond supported keys.
        - Unknown keys are ignored.

    type_of_friendship : str, optional (default = 'short')
        Defines the intended duration or nature of the relationship.

        Allowed values (case-insensitive):
            - 'short'    → Temporary or casual connection
            - 'long'     → Ongoing but not permanent
            - 'forever'  → Intended permanent relationship
            - 'auto'     → System-determined duration (interpretation external)

        Behavior:
        - Input is normalized to lowercase before validation.
        - If the value is not in the allowed set, a TypeError is raised.

    length : int | None, optional (default = 7)
        The number of days before the connection is considered for removal.

        - Stored as-is under the key:
            'time_till_removal_(days)'
        - If None, no explicit expiration is implied (interpretation handled elsewhere).
        - No validation is performed on this value.

    how_much_you_like_this_person : float, optional (default = 5.0)
        A numeric affinity score representing how much the user likes the person.

        Behavior:
        - Automatically clamped to the range [0.0, 10.0]
        - Values below 0.0 become 0.0
        - Values above 10.0 become 10.0

        Interpretation:
        - 0.0 → Strong dislike
        - 5.0 → Neutral
        - 10.0 → Maximum affinity

    -------------------------------------------------------------------------------
    INTERNAL PROCESSING STEPS
    -------------------------------------------------------------------------------
    1. Normalize and validate `type_of_friendship`
       - Convert to lowercase
       - Ensure it is one of the allowed values
       - Raise TypeError if invalid

    2. Validate `who`
       - Strip whitespace
       - Exit early if empty or invalid

    3. Validate `environment`
       - Strip whitespace
       - Exit early if fewer than 3 characters

    4. Clamp affinity score
       - Ensure value lies between 0.0 and 10.0

    5. Normalize key fields
       - PERSON = capitalized version of `who`
       - environment = lowercase version

    6. Process nicknames (if provided)
       - Accepts string or list of strings
       - Each nickname:
            - Stripped
            - Validated via `_validate_name`
            - Capitalized
       - Stored as a list

    7. Access internal memory structure
       - Uses:
            self._Brain.mind.memories[0]
       - Assumes this structure exists and is properly initialized

    8. Insert structured relationship record
       - Stored under:
            brain_data['brain']['_personal_data']['friends'][PERSON]

    -------------------------------------------------------------------------------
    STORED DATA STRUCTURE
    -------------------------------------------------------------------------------
    The following dictionary is created for each connection:

    {
        'type_of_friendship': str,
        'where': str,
        'scale': float,
        'nicknames': List[str],
        'knew_them_at': {
            'date': str (ISO format, YYYY-MM-DD),
            'time_till_removal_(days)': int | None
        },
        'associations': dict (initially empty),
        'connected_memories': list (initially empty)
    }

    Notes:
    - 'associations' is reserved for future relational metadata
    - 'connected_memories' is intended to link experiences/events

    -------------------------------------------------------------------------------
    SIDE EFFECTS
    -------------------------------------------------------------------------------
    - Mutates internal memory state (persistent within the object)
    - Calls `self.confirm()` after successful insertion
    - Prints a confirmation message:
        "✓ Connected with <PERSON>"

    -------------------------------------------------------------------------------
    ERROR HANDLING
    -------------------------------------------------------------------------------
    - Raises:
        TypeError:
            If `type_of_friendship` is invalid

    - Silent early returns (no exception):
        - Invalid or empty `who`
        - Invalid `environment` (too short)

    - Assumes:
        - `_validate_name` raises its own exceptions if needed
        - Internal memory structure exists and is accessible

    -------------------------------------------------------------------------------
    USAGE EXAMPLES
    -------------------------------------------------------------------------------
    Basic:
        connect("alice", "school")

    With nicknames:
        connect("bob", "work", details={"nickname": ["bobby", "rob"]})

    Custom relationship:
        connect("charlie", "gym", type_of_friendship="long", length=30)

    Edge case (clamping):
        connect("dave", "online", how_much_you_like_this_person=15.0)
        # Stored as 10.0

    -------------------------------------------------------------------------------
    DESIGN NOTES
    -------------------------------------------------------------------------------
    - Designed for resilience: avoids raising errors for minor input issues
    - Prioritizes internal consistency via normalization
    - Separates validation strictness:
        - Critical fields → enforced (type_of_friendship)
        - Non-critical → fail silently (who, environment)
    - Acts as a foundational primitive for building a relationship graph
      within the system's cognitive architecture
    """
        
        valid_types = ['short', 'long', 'forever', 'auto']
        type_of_friendship = type_of_friendship.lower()
        
        if type_of_friendship not in valid_types:
            raise TypeError(f"Invalid friendship type. Choose: {', '.join(valid_types)}")
        
        if not who.strip() or len(who) < 1:
            return
        
        if not environment.strip() or len(environment) < 3:
            return
        
        # Clamp rating
        how_much_you_like_this_person = max(0.0, min(how_much_you_like_this_person, 10.0))
        
        PERSON = who.strip().capitalize()
        environment = environment.strip().lower()
        
        # Process nicknames
        nicknames = []
        if details and 'nickname' in details:
            nickname_input = details['nickname']
            
            if isinstance(nickname_input, list):
                for name in nickname_input:
                    name = name.strip()
                    self._validate_name(name)
                    nicknames.append(name.capitalize())
            elif isinstance(nickname_input, str):
                name = nickname_input.strip()
                self._validate_name(name)
                nicknames.append(name.capitalize())
        
        # FIX: Access structure correctly
        brain_data = self._Brain.mind.memories[0]
        
        brain_data['brain']['_personal_data']['friends'][PERSON] = {
            'type_of_friendship': type_of_friendship,
            'where': environment,
            'scale': how_much_you_like_this_person,
            'nicknames': nicknames,
            'knew_them_at': {
                'date': date.today().isoformat(),
                'time_till_removal_(days)': length
            },
            'associations': {},
            'connected_memories': []
        }
        
        self.confirm()
        print(f"✓ Connected with {PERSON}")

    def confirm(self):
        """Commit changes to disk."""
        self._Brain.mind.commit()

    def forget(self, who: str, full: bool = False):
        """Remove a friend."""
        who = who.strip().capitalize()
        
        brain_data = self._Brain.mind.memories[0]
        friends_dict = brain_data['brain']['_personal_data']['friends']
        
        if who in friends_dict:
            if full:
                # Completely remove
                del friends_dict[who]
            else:
                # Move to decayed memories
                if 'decayed_memories' not in brain_data['brain']:
                    brain_data['brain']['decayed_memories'] = []
                
                brain_data['brain']['decayed_memories'].append({
                    'type': 'friend',
                    'name': who,
                    'data': friends_dict[who],
                    'forgotten_date': date.today().isoformat()
                })
                
                del friends_dict[who]
            
            self.confirm()
            print(f"✓ Forgot {who}")
        else:
            print(f"✗ {who} not found in friends")

    def remember_(self, who: str) -> bool:
        """Remember a forgotten friend."""
        who = who.strip().capitalize()
        
        brain_data = self._Brain.mind.memories[0]
        
        # Check if in decayed memories
        if 'decayed_memories' in brain_data['brain']:
            for i, decayed in enumerate(brain_data['brain']['decayed_memories']):
                if decayed.get('type') == 'friend' and decayed.get('name') == who:
                    # Restore friend
                    friends_dict = brain_data['brain']['_personal_data']['friends']
                    friends_dict[who] = decayed['data']
                    
                    # Add note
                    friends_dict[who]['remembered_date'] = date.today().isoformat()
                    
                    # Remove from decayed
                    brain_data['brain']['decayed_memories'].pop(i)
                    
                    self.confirm()
                    print(f"✓ Remembered {who}")
                    return True
        
        print(f"✗ {who} not found in forgotten friends")
        return False

    def _validate_name(self, name: str):
        """Validate name."""
        special_chars = r"~!@#$%^&*()_+`={}|[]\:;<>?,./'"
        
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        
        if any(char in special_chars for char in name):
            invalid = ''.join([c for c in name if c in special_chars])
            raise ValueError(f"Name contains invalid characters: {invalid}")
        
        if len(name) > 160 or len(name) < 1:
            raise NameError(f"Name length invalid: {len(name)} (must be 1-160)")


# Subclasses with proper init

class Meg(friends):
    """Focuses on ended/past friendships."""
    def __init__(self, Brain):
        super().__init__(Brain=Brain, operator='meg')
    
    def who(self, who: str):
        """Get info about past friend."""
        # TODO: Implementation
        pass
    
    def remember(self, who: str):
        return super().remember_(who)


class Bree(friends):
    """Focuses on long-term/childhood friendships."""
    def __init__(self, Brain):
        super().__init__(Brain=Brain, operator='bree')
    
    def who(self, who: str):
        pass
    
    def remember(self, who: str):
        return super().remember_(who)


class Grace(friends):
    """Focuses on short-term/temporary friendships."""
    def __init__(self, Brain):
        super().__init__(Brain=Brain, operator='grace')
    
    def who(self, who: str):
        pass
    
    def remember(self, who: str):
        pass


class Val(friends):
    """Focuses on jealousy/rivalry in friendships."""
    def __init__(self, Brain):
        super().__init__(Brain=Brain, operator='val')
    
    def who(self, who: str):
        pass
    
    def remember(self, who: str):
        pass


class Amigo:
    """Main interface for friendship management."""
    def __init__(self, name: str, Brain):
        self._friends = friends(operator=name, Brain=Brain)
        self.Brain = Brain
        # Pass Brain to all subclasses
        self.Meg = Meg(Brain=self.Brain)
        self.Val = Val(Brain=self.Brain)
        self.Grace = Grace(Brain=self.Brain)
        self.Bree = Bree(Brain=self.Brain)
        
    def new_brain(self, new_brain: Brain):
        """Update brain reference for all components."""
        self.Brain = new_brain
        self._friends._Brain = new_brain
        self.Meg._Brain = new_brain
        self.Val._Brain = new_brain
        self.Grace._Brain = new_brain
        self.Bree._Brain = new_brain
    
    @property
    def friends(self):
        return self._friends