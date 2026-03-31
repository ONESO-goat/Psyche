# ASO.py - Association module for the brain


from numpy_utils.numpy_helpers import serialize_numpy, deserialize_numpy
import copy
from typing import Any, Dict, List
from AI.Gemini import AssociationAI_Gem
from AI.Ollama import AssociationAI_32, AssociationAI_qwen

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
        if api_key:
            from aso_ai import AssociationAI
            self.ai = AssociationAI(api_key=api_key)
        else:
            # Use Ollama
            self.ai = AssociationAI_qwen()
            
    def find_association(self, 
                        memory: dict = {}, 
                        context: str = '',
                        save_to_memory: bool = True) -> Dict:
        """
        Find associations using AI.
        """     
        if memory:
            context = memory.get('content', '')
        if not context:
            raise ValueError("Need either memory or context")
        associations = self.ai.find_associations(
            content=context,
            all_memories=self.memories
        )
        if save_to_memory:
            # Save associations to memory (optional)
            for assoc in associations:
                assoc_memory = {
                    'content': f"Association: {assoc['source']} -> {assoc['target']} (strength: {assoc['strength']}, type: {assoc['type']}, reason: {assoc['reason']})",
                    'metadata': {
                        'source': assoc['source'],
                        'target': assoc['target'],
                        'strength': assoc['strength'],
                        'type': assoc['type'],
                        'reason': assoc['reason']
                    }
                }
                self.Brain.mind.add(assoc_memory)