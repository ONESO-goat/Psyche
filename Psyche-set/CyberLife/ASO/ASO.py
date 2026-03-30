
from numpy_utils.numpy_helpers import serialize_numpy, deserialize_numpy
import copy
from typing import Dict
from AI.Gemini import AssociationAI_Gem
from AI.Ollama import AssociationAI

class ASO:
    def __init__(self, Brain, api_key: str):
        """
        The key part of the brain. ASO is short for association.

        Associtation works on connect 1 memory to another, or 1 known fact or opinion to another,

        example when I think bat, I think fox, I thought of fox because they're both mammals and a bat reminds me of a fox facially, key word 'remind'. 

        When I think mammals, I think programming, because (some) humans which are mammal creatures, code which includes programming.

        When I think ferret, I think of a memory where I pet and feed a goat: 

         ferret - zoo  _ animals
           |       | /  \ 
         mammal - goat - farm - early memory I feed the goat. 
         
        ASO uses machine learning and AI to help assist as associtation can reach hundreds to even millions of chains even 
        just thinking of the letter 2 or a simple onject like a cup, 
        example when I think cup i think concrete because they're both solid objects, or water or tea.

        The difficult part of this will likely be the speed, as this alone can span 1 memory to thousands lines of JSON code,
        stunting thinking power, but this is natural behavior.

        If you are confused I wrote a long page just on associtations, using my mind as an example, you might cringe but you're here to understand |:3
        
        """
        self.Brain = Brain
        self.memories = self.Brain.mind.get_all()

           # Initialize Gemini AI
        self.ai = AssociationAI()
    
    def find_association(self, 
                        memory: dict = {}, 
                        context: str = '',
                        save_to_memory: bool = True) -> Dict:
        """
        Find associations using Gemini AI.
        """
        
        if memory:
            context = memory.get('content', '')
        
        if not context:
            raise ValueError("Need either memory or context")
        
        # Get associations from AI
        associations = self.ai.find_associations(
            content=context,
            all_memories=self.memories
        )
        
        if save_to_memory and memory:
            # Save to memory
            memory_copy = copy.deepcopy(memory)
            memory_copy['associations'] = associations
            
            # Also find connections to other memories
            connections = self.ai.find_memory_connections(
                target_memory=memory,
                all_memories=self.memories
            )
            
            memory_copy['memory_connections'] = connections
            
            # Update in brain
            self.Brain.mind.replace(old=memory, new=memory_copy)
            self.Brain.mind.commit()
            
            return memory_copy
        
        return associations
    
