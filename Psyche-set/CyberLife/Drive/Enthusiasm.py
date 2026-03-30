# Enthusiasm.py

from Drive.Inspiration import Inspiration
from Drive.Motivation import Motivation
import numpy as np



class Enthusiasm:
    def __init__(self, Brain):
        self.Brain = Brain
        self.motivation = self.Brain.get_motivation() # 0
        self.inspiration = self.Brain.get_inspiration() # 0
        self.memories = self.Brain.mind.get_all()
    
    def _find_main_goal(self):
        main_goal = {} 
        sum_inspire = 0
        sum_motivate = 0

        for index, memory in enumerate(self.memories):
            inspiration = memory['enthusiasm']['inspiration']
            motivation = memory['enthusiasm']['motivation']
            inspire_sum = np.sum(inspiration)
            motivate_sum = np.sum(motivation)
            if inspire_sum > sum_inspire:
                sum_inspire = inspire_sum
            if motivate_sum > sum_motivate:
                sum_motivate = motivate_sum
            if index == len(self.memories):
                main_goal = memory
            
        why = 'You just like it for now.' # TODO: AI finds the why for the user
        brain = self.Brain.mind.achieve().copy()
        oldb = brain
        main_goal['backstory'] = why
        brain['main_goal'] = main_goal

        self.Brain.mind._revert_warning(old_brain=oldb, new_brain=brain)
        
        


            
            
