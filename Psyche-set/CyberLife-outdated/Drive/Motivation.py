# Motivation.py

from typing import Dict, Any
import numpy as np



class Motivation:
    def __init__(self, 
                 Brain, 
                 thought_system,
                 inspiration, 
                 level: float | int = 0):
        """
        Docstring for __init__
        
        Motivation is it's own league when it comes to emotions.
        Though with sadness, happiness, etc you feel that emotion at that current moment,
        with motivation, it scales how you feel.
        Example, you can be angry, but depending on your motivation it can really change things up.
        High motivation would probaly urge you to proceed with violence,
        but lower motivation likely means a simpler mood.

        If level is float, it determines the first row, but if it is an int, it will 
        auto increase all floats in the motivation (mainly 1st and 2nd row).
        example:

        level = 0.2
        [0.2 0.2 0.2 0.2]
        [0.  0.  0.  0. ]
        [0.  0.  0.  0. ]

        level = 10
        [1.0 1.0 1.0 1.0]
        [1.0 1.0 1.0 1.0]
        [0.  0.  0.  0. ]

        The last row focuses on how unmotivated the brain is, representing negative floats
        """

        self.Thoughts = thought_system
        self.level = level
        self.Brain = Brain
        self.inspiration = inspiration
        self.inspire = self._set_up_motivation(level=level)

    def enhanced_inspiration(self,
                            scale: float,  
                            current_motivation: Dict[str, Any],
                            boost: bool = False,):
        
        current = current_motivation['motivation']
        if boost:
            current += scale * 2
        else:
            current += scale
        current_motivation['motivation'] = current
        return current_motivation

    def feeling_motivated(self, data: Dict[str, Any]):
        
        
        if data.get('enthusiasm', False):
            dataset = data['enthusiasm']['motivation']
            total = np.sum(dataset)
            if total == None:
                raise ValueError("Unexplained error occured when processing motivation scale.")
            
            if total == 4:
                print(' -- getting motivated -- ')
                return False
            
            return total > 4
            
        elif all(isinstance(v, np.ndarray) for v in data.values()):
            total = np.sum(list(data.values()))

            if total == 4:
                return 'balanced'
            return total > 4

        else:
            raise KeyError("motivation key for data couldn't be found.")


    def _set_up_motivation(self, level: int | float):
        """
        level:
        if level is a float, it makes every num in the top row to that float
        if level is an int, it adds 1 number to arries, e.q: level = 10

        array = [1 1 1 1]
                [1 1 1 1] 
        """

        data = np.zeros((3,3))

        if isinstance(level, float):
            first_row = data[0]
            first_row *= level
            data[0] = first_row
            return data
        
        elif isinstance(level, int):
            first_row = data[0]
            second_row = data[1]
            index = 0
            index2 = 0

            for i in range(level):
                if index < len(first_row):
                    first_row[index] += level
                    index+=1
                elif index2 < len(second_row):
                    second_row[index2] += level
                    index2+=1
                else:
                    break
            data[0] = first_row
            data[1] = second_row
            return data
        else:
            return data 

    def why(self, 
            memory: Dict[str, Any], 
            why: str = '', 
            auto: bool = True) :
        
        """Explain why the motivation.

        auto means an AI creates the 'why' for you.
        """

        if auto:
            new = memory.copy()
            context = new['context']
            # TODO, create file for AI, call 
            # AI_context = self.AI_.create_inspiration(context)
            # new['inspiation']['reason_for_this'] = AI_context
            # self.Brain.mind.replace(old=memory, new=new)
            # self.Brain.mind.commit()
            # return new
        elif why.strip() != '' and auto is False:
            new = memory.copy()
            new['motivation']['reason_for_this'] = self.why
            self.Brain.mind.replace(old=memory, new=new)
            self.Brain.mind.commit()
            return new
        return
    

    def main_goal_motivation_reasoning(
            self, 
            memory: Dict[str, Any], 
            why: str = '', 
            auto: bool = True) :
        
        """The reasoning behind the main goals inspiration level.

        auto means an AI creates the 'why' for you.
        """

        if auto:
            new = memory.copy()
            context = new['main_goal']
            # TODO, create file for AI, call 
            # AI_context = self.AI_.create_inspiration(context)
            # new['inspiation']['reason_for_this'] = AI_context
            # self.Brain.mind.replace(old=memory, new=new)
            # self.Brain.mind.commit()
            # return new
        elif why.strip() != '' and auto is False:
            new = memory.copy()
            new['motivation']['reason_for_this'] = self.why
            self.Brain.mind.replace(old=memory, new=new)
            self.Brain.mind.commit()
            return new
        
    def _overall(self):
        """
        
        Grab the mean for the overall inspiration for the brain. Instead of the usal
        -1 to 1 3x4 scale, this will be a -20 to 20 sclar scale, represent how motivated, inspired, etc 
        the brain is.
        """
        level = 0.000000000
        memories = self.Brain.mind.get_all()
        for memory in memories:
            for flt in memory['enthusiasm']['motivation']:
                flt = flt / 100
                level += flt
        brain = self.Brain.mind.achieve().copy()
        old = brain
        brain['enthusiasm']['motivation']['scale'] = level
        brain['enthusiasm']['motivation']['details'] = self.understand(level=level)
        self.Brain.mind._revert_warning(new_brain=brain, old_brain=old)
        

    def understand(self, level):
        """TODO: Have an AI to create a reasoning on this inspiration, 
        maybe paragrapth long grabbing common troupes and enjoyments from the user."""

        
    
    def is_database(self, system) -> NotImplementedError:
        """Check if system is a database."""
        return NotImplementedError("Not yet implemented")

        
        