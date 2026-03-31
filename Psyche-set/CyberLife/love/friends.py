# friends.py - manage friendships and social connections.

from love.love import love
import copy
from datetime import date
from typing import List, Dict, Any, Optional

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
                details: Dict = {},
                type_of_friendship: str = 'short',
                length: int | None = 7,
                how_much_you_like_this_person: float = 5.0):
        """Connect with an individual."""
        
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
        
        # Pass Brain to all subclasses
        self.Meg = Meg(Brain=Brain)
        self.Val = Val(Brain=Brain)
        self.Grace = Grace(Brain=Brain)
        self.Bree = Bree(Brain=Brain)