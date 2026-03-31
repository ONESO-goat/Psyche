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
    

    
    def find_associations(self, 
                     content: str, 
                     dominant_emotion: str,  # ← ADD THIS
                     all_memories: List[Dict],  
                     max_associations: int = 10) -> Dict[str, Any]:
        """
        IMPROVED version with better prompting.
        """
        
        # Build memory context (but keep it SHORT)
        memory_context = self._build_memory_context(all_memories, max_memories=3)
        
        prompt = f"""You are analyzing a memory to find associations.

    MEMORY TO ANALYZE:
    Content: "{content}"
    Emotion: {dominant_emotion}

    TASK 1 - Extract Key Concepts:
    Find the main concepts/entities in this memory. For each:
    - What is it?
    - How strongly related to the memory (0-10)?
    - What other concepts does it connect to?
    - What category (people, places, objects, emotions, activities, abstract)?

    TASK 2 - Personal Memory Connections:
    The person has these other memories:
    {memory_context}

    Which of these memories connects to the current one? Only include if:
    - They share concepts (people, places, objects)
    - They share emotions
    - They're causally related
    DON'T connect unrelated memories just because they exist.

    TASK 3 - Emotional Analysis:
    - What emotion does THIS specific memory trigger?
    - How intense (0.0-1.0)?
    - WHY does it trigger this emotion?

    CRITICAL RULES:
    - Use the ACTUAL emotion from the memory ({dominant_emotion})
    - Don't mix up different memories
    - Only connect memories that genuinely relate
    - Be specific, not generic

    OUTPUT FORMAT (JSON only, no markdown):
    {{
    "direct_associations": {{
        "concept_name": {{
        "strength": 10,
        "related": ["word1", "word2"],
        "category": "people/places/objects/emotions/activities/abstract"
        }}
    }},
    "personal_memory_connections": [
        {{
        "memory_id": "actual_uuid_here",
        "reason": "specific reason they connect",
        "strength": 0.8,
        "shared_concepts": ["concept1", "concept2"]
        }}
    ],
    "emotional_analysis": {{
        "emotion": "{dominant_emotion}",
        "intensity": 0.8,
        "triggers": ["trigger1", "trigger2"],
        "why": "specific reason for this emotion"
    }}
    }}"""

        if not memory and not context:
            raise ValueError("Need either memory or context")
        
        if memory:
            content = memory.get('content', '')
            emotion = memory.get('dominant_emotion', 'neutral')
        else:
            content = context
            emotion = 'neutral'
        
        # Get associations (just for THIS memory)
        associations = self.ai.find_associations(
            content=content,
            dominant_emotion=emotion,  # ← Pass emotion!
            all_memories=self.memories
        )
        
        # Get memory connections (which OTHER memories relate)
        memory_connections = self.ai.find_memory_connections(
            target_memory=memory if memory else {'content': content, 'id': 'temp'},
            all_memories=self.memories,
            threshold=0.4  # Be selective
        )
        
        if save_to_memory and memory:
            # Update memory
            memory_copy = copy.deepcopy(memory)
            memory_copy['associations'] = associations
            memory_copy['memory_connections'] = memory_connections
            
            # Replace
            self.Brain.mind.replace(old=memory, new=memory_copy)
            self.Brain.mind.commit()
            
            return memory_copy
        
        return {
            'associations': associations,
            'memory_connections': memory_connections
        }
        
        
    def process_all_memories(self, reprocess: bool = False):
        """
        Process ALL memories to find associations.
        
        reprocess: If True, recompute even if associations exist
        """
        
        memories = self.Brain.mind.get_all()
        
        for i, memory in enumerate(memories):
            print(f"\nProcessing memory {i+1}/{len(memories)}...")
            
            # Skip if already has associations (unless reprocessing)
            if not reprocess and memory.get('associations'):
                print("  → Already has associations, skipping")
                continue
            
            try:
                # Process THIS memory only
                updated = self.find_association(
                    memory=memory,
                    save_to_memory=True
                )
                print(f"  ✓ Found associations")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue
        
        print(f"\n✓ Processed {len(memories)} memories")
    