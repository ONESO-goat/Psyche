
#include <imports.h>
#include <format>
#include <string_view>

using namespace std;
class Brain{
private:
    /*
        Usally generals should focus on their own fields, weights would be low (< 0.3).
        Linx's will likely be more creative or free on their decisions and new informations.

    */
    float weights;

    /*
    General -> Piece of Rosa
    LINX -> Either user owned or independent
    MANAGER -> LINX's made by geenrals
    */
    Group familyClass;

    // example ("john", "", "doe")
    tuple<string, string, string> first_middle_last_name; 

public:
    Brain(tuple<string, string, string> const& name, float weights, Group familyCategory){
        if (!validate_name(name)){
            return;
        }
        familyClass = familyCategory;
        first_middle_last_name = name;
        weights = weights;
    }

    bool validate_name( tuple<string,string,string> const& name){

        constexpr std::string_view special_chars = "~!@#$%^&*()+`={}[]\\:;<>,.?/";
        
        string first_name = get<0>(name);
        string middle_name = get<1>(name);
        string last_name = get<2>(name);

        if (first_name.empty() || last_name.empty()){
            throw length_error("First and last name are required");
        }

        if (min(last_name.length(), first_name.length()) < 2  || max( last_name.length(), first_name.length()) > 100){
            throw length_error("First or Last name falls outside the valid range (2-100).");
        }
        
        vector<string> const a = {first_name, middle_name, last_name};
        for (char const n : special_chars){
            if (first_name.find(n) != string::npos ||
                middle_name.find(n) != string::npos ||    
                last_name.find(n) != string::npos    
            ){
                throw logic_error("Name cannot include special characters");
            }
            continue;
        //     int left = 0;
        //     int right = n.size() - 1;
        //     while (left < right)
        //    {     if (special_chars.find(n[right]) != string_view::npos || 
        //             special_chars.find(n[left]) != string_view::npos
        //         ){
        //             throw logic_error("Name cannot include special characters");
        //         }
        //         left++; right--;
        //     }
        }
        
        return true;
    }

    /*
    Display brain visualization

    mode (int): 2 = 2D; 3 = 3D
    */
    void showcase(int mode = 2){

        if (mode == 2){
            render_visualize_brain_2D();
        }
        else if (mode == 3){
            // render_visualize_brain_3D()  // Implement this later
            throw system_error("3D visual not yet made.");
        }
        else{
            string msg = format("Invalid mode: {}. Choose '2' (for 2D) or '3' (for 3D)", to_string(mode));
            throw logic_error(msg);
        }
        
    /*
    Show brain with memories represented.
    */
    void render_visualize_brain_2D(
                 tuple<int,int> figsize = tuple(7,7), 
                 string border_color="black", 
                 string _color="lightgray", 
                 string shape = "circle", 
                 float Brain_Size= 1.0)
        
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.patches import Circle

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Brain outline
        brain_circle = Circle((0, 0), 1.5, 
                            color=_color, 
                            ec='darkgray', 
                            linewidth=3, 
                            alpha=0.3)
        ax.add_patch(brain_circle)
        
        # Each memory = dot inside brain
        memories = self.recall_all()
        
        character_color = {
                'happy': 'yellow',
                'sadness': 'blue',
                'anger': 'red',
                'fearful': 'purple',
                'disgusted': 'green',
                'surprised': 'pink',
                'neutral': 'gray',
            }
        
        for memory in memories:
            # Random position inside brain
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, 1.3)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            color = character_color.get(memory['dominant_emotion'], 'gray')
            size = 50 + memory['importance'] * 100  # Size based on importance
            
            ax.scatter(x, y, s=size, c=color, alpha=0.7, edgecolors='black')
        
        plt.title(f"{self.first_name}'s Brain - {len(memories)} memories")
        plt.show()
    }
}


class Brain(BrainAnomaly):
    def __init__(self,
                pounds: float = 0.005, 
                watts: float = 1.0, 
                name: tuple[str, str, str] = ("john",'', "doe"), 
                storage_size: int = 1000000):

        super().__init__(pounds=pounds, watts=watts)

       
        
        self.first_name, self.middle_name, self.last_name = self._validate_name(name)
        
        self.name: str = f"{self.first_name} {self.middle_name} {self.last_name}".strip()

        #self._create_config_()
        
        self.mind = Storage(self.get_brain_data(), size=storage_size)
        """Storage"""

                # Regional activation tracking (simple version)
        self.region_activity = {
            'forebrain': 0.0,
            'midbrain': 0.0,
            'hindbrain': 0.0
        }


        # Future systems (placeholders)
        # Uncomment when ready to implement:
        # self.forebrain = Prosencephalon(self)
        # self.midbrain = Mesencephalon(self)
        # self.hindbrain = Rhombencephalon(self)
        
    def _validate_name(self, name: tuple[str, str, str]):
        """Validate Brain name"""

        special_chars = r"~!@#$%^&*()+`={}|[]\:;<>?,./'"  

        
        for parts in name:
            if '-' in parts or '_' in parts:
                parts = parts.replace('-', ' ').replace('_', ' ')
                print(f"Name part '{parts}' contained special characters, auto reshaping to '{parts}'")
        
        first_name, middle_name, last_name = name[0].capitalize(), name[1].capitalize(), name[2].capitalize()

        if not first_name or first_name.strip() == '':
            raise NameError("First name cannot be empty")
        
        if len(first_name.split()) > 1:
            print("First name contains more than 2 words, auto reshaping...")
            first_name_list = first_name.split()
            for word in first_name_list:
                last_name+=f" {word}"
            first_name = first_name_list[0]
            
            
        if middle_name and len(middle_name.split()) > 1:
            print("Middle name contains more than 2 words, auto reshaping...")
            middle_name_list = middle_name.split()
            for word in middle_name_list:
                last_name+=f" {word}"
            middle_name = middle_name_list[0]
            
        
        if not last_name or last_name.strip() == '':
            raise NameError("Last name cannot be empty")

        for i in range(3):
            if any(char in special_chars for char in name[i]) and i != 1:
                raise NameError(f"Name cannot contain special characters: {[c for c in name[i] if c in special_chars]}")
        
        
        return first_name, middle_name, last_name


    def BrainCreation(self) -> Tuple[float, float, float]:
        """Create the size of the brain. 
        Grab input of pounds and watts to determine brain.
        Returns tuple for self.showcase"""

        size = self.brain_size
        watts_ = self.power

        forebrain = self.brain_size * 0.5
        midbrain = self.brain_size * 0.3
        hindbrain = self.brain_size * 0.2
        return forebrain, midbrain, hindbrain

    

    def get_brain_data(self) -> Dict[str, Any]:
        stuff = {
            "NAME": {"first": self.first_name, "middle": self.middle_name, "last": self.last_name},
            "WATTS": self.power,
            "SIZE": self.brain_size
        }
        return stuff
    

    def stimulate_region(self, region: str, intensity: float):
        """
        Activate a brain region.
        FUTURE: Will trigger actual neural processing.
        CURRENT: Just tracks activation levels.
        """
        if region not in self.region_activity:
            raise ValueError(f"Unknown region: {region}")
        
        self.region_activity[region] += intensity
        self.region_activity[region] = min(1.0, self.region_activity[region])
        
        # Activation decays over time
        for r in self.region_activity:
            if r != region:
                self.region_activity[r] *= 0.95
    
    def get_brain_state(self):
        """Current state of all regions."""
        return self.region_activity.copy()
    
    def showcase(self, mode: str = "2D") -> None:
        """Display brain visualization."""
        mode = mode.upper()
        
        if mode == '2D':
            self.render_visualize_brain_2D()
        elif mode == '3D':
            #self.render_visualize_brain_3D()  # Implement this later
            raise NotImplementedError("3D visual not yet made.")
        else:
            raise ValueError(f"Invalid mode: {mode}. Choose '2D' or '3D'")
        

    def render_visualize_brain_2D(self, 
                 figsize:tuple[int, int]=(7,7), 
                 border_color:str='black', 
                 _color:str='lightgray', 
                 shape: str = 'circle', 
                 Brain_Size:float= 1.0):
        """Show brain with memories represented."""

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.patches import Circle

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Brain outline
        brain_circle = Circle((0, 0), 1.5, 
                            color=_color, 
                            ec='darkgray', 
                            linewidth=3, 
                            alpha=0.3)
        ax.add_patch(brain_circle)
        
        # Each memory = dot inside brain
        memories = self.recall_all()
        
        character_color = {
                'happy': 'yellow',
                'sadness': 'blue',
                'anger': 'red',
                'fearful': 'purple',
                'disgusted': 'green',
                'surprised': 'pink',
                'neutral': 'gray',
            }
        
        for memory in memories:
            # Random position inside brain
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, 1.3)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            color = character_color.get(memory['dominant_emotion'], 'gray')
            size = 50 + memory['importance'] * 100  # Size based on importance
            
            ax.scatter(x, y, s=size, c=color, alpha=0.7, edgecolors='black')
        
        plt.title(f"{self.first_name}'s Brain - {len(memories)} memories")
        plt.show()

    def remember(self, 
                 content: str, 
                 emotion: str = 'neutral', 
                 importance: float = 0.5, 
                 motivation = np.zeros(4)
                    ) -> None:
        """Store a new memory."""
        memory = {
            'content': content,
            'emotion': emotion.lower(),
            'importance': importance,
            'motivation': motivation,
            'timestamp': datetime.now().isoformat()
        }
        self.mind.add(memory)

    
    def forget(self, memory_item: Dict[str, Any]) -> None:
        """Remove a memory."""
        self.mind.remove(memory_item)

    def recall_all(self):
        """Get all memories."""
        return self.mind.get_all()

    
    def get_memory_count(self) -> int:
        """How many memories are stored."""
        return len(self.mind.memories)
    
    def get_memories_by_emotion(self, emotion: str) -> List[Dict[str, Any]]:
        """Get all memories with specific emotion."""
        return [m for m in self.mind.memories if m.get('emotion') == emotion]
    
    def get_memory_row(self, row: int, emotion: Optional[str] = None)-> np.ndarray:
        """Get selection of memories on emotion."""
        if emotion is not None:
           return self.mind.memories[row]['emotion'][emotion.lower()]['regulation'] 
        emotion = list(self.mind.memories[row]['emotion'].keys())[0]
        return self.mind.memories[row]['emotion'][emotion]['regulation']
    
    def get_storage(self):
        """Get the storage system."""
        return self.mind
    
    def __repr__(self) -> str:
        return f"Brain(name='{self.name}', size={self.brain_size}lbs, power={self.power}W, memories={len(self.mind.memories)})"

    def _create_model_(self, auto_Activation: bool = False):
        """
        FUTURE IMPLEMENTATION:
        Creates persistent database for neural state tracking.
        
        Will store:
        - Synaptic weights (connection strengths between regions)
        - Neurotransmitter levels (dopamine, serotonin analogs)
        - Long-term potentiation (learning traces)
        - Regional activation patterns
        
        Currently creates basic SQLite structure.
        TODO: Integrate with actual neural simulation when regions are implemented.
        """
    
    # Current implementation (basic structure)
    
        import uuid
        import importlib as lib
        from pathlib import Path
        import os
        import sys
        
        try:
            
            id = str(uuid.uuid4())
            file = f"{self.first_name}_MODEL.py" 
            path = Path(id) / Path(file)
            with open(file, 'w') as f:
                f.write(self._())
            if auto_Activation:
                lib.invalidate_caches()

                if os.getcwd() not in sys.path:
                    sys.path.append(os.getcwd())

                module = lib.import_module(file[:-3].strip())
                module.run()
                
        except IOError as e:
            raise IOError("There was an error creating brain database: ", e)
        
        # TODO: Add tables for:
        # - synaptic_connections
        # - neurotransmitter_levels  
        # - activation_history
        # - learning_traces
    
    def _(self) -> str:
        
        script = f"""
import sqlite3
import uuid
from datetime import datetime

def run():
    ID = "{self.first_name}"+str(uuid.uuid4())+datetime.utcnow().isoformat().strip()
    env = "{self.first_name}.env"
    script = "{self.first_name.upper()}_ID="+ID

    with open(env, 'w') as f:
        f.write(script)

    # Create database
    conn = sqlite3.connect("{self.first_name}_brain.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute(''')
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            emotion TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            importance FLOAT
        )
    ''')

    # Insert memory
    cursor.execute('''
        INSERT INTO memories (content, emotion, importance)
        VALUES (?, ?, ?)
    ''', ("First memory", "happy", 0.8))

    conn.commit()

    # Query memories
    cursor.execute('SELECT * FROM memories ORDER BY importance DESC')
    memories = cursor.fetchall()

    conn.close()

"""
        return script
    
    def get_fullname(self) -> str:
        """Return full name of the brain."""
        return self.name
    
    def get_motivation(self) -> np.ndarray:
        """Return motivation vector for a memory."""
        return self.mind.memories[0].get('motivation', np.zeros(4))
    
    def get_inspiration(self) -> np.ndarray:
        """Return inspiration vector for a memory."""
        return self.mind.memories[0].get('inspiration', np.zeros(4))
    
    def get_fullname_by_parts(self) -> Tuple[str, str, str]:
        name_parts = self.name.split()
        if len(name_parts) == 3:
            return name_parts[0], name_parts[1], name_parts[2]
        elif len(name_parts) == 2:
            return name_parts[0], "", name_parts[1]
        else:
            return name_parts[0], "", ""
