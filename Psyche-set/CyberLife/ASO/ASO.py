# ASO/ASO.py

from typing import List, Dict, Any, Optional
from ASO.aso_core import Association, AssociationGraph
from ASO.aso_ai import AssociationAI
from debugging_utils import debug, reset_debug, hashtag
import copy
from ASO._info_ import _explaination

class ASO:
    """
    Association System - integrates with Brain structure.
    
    The key part of the brain. ASO = Association.
    
    Associations connect memories, facts, and concepts.
    Example: "bat" → "fox" (both mammals, similar faces)
    Example: "ferret" → "zoo" → "farm" → "goat memory"
    """
    
    def __init__(self, Brain, api_key: str | None = None, model: str = 'gemini'):
        """
        Initialize ASO with Brain instance.
        
        Args:
            Brain: Your Brain instance
            api_key: Gemini API key (if using Gemini)
            model: 'gemini' or 'ollama'
        """
        self.Brain = Brain
        
        # Get brain structure
        brain_data = self.Brain.mind.memories[0]['brain']
        
        # Initialize graph (stored IN the brain structure)
        self.graph = AssociationGraph(brain_storage=brain_data)
        
        # Initialize AI
        self.ai = AssociationAI(api_key=api_key, model=model)
    
    # ASO/ASO.py - Update the process_memory method

    def process_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a memory to extract and store associations.
        """
        if not self.ai:
            return {
                'error': 'No AI configured',
                'concepts': [],
                'associations_added': 0,
                'memory_connections': 0
            }
        
        content = memory.get('content', '')
        memory_id = memory.get('id', '')
        emotion = memory.get('dominant_emotion', 'neutral')
        
        print(f"    → Extracting concepts from: \"{content[:50]}...\"")
        
        # Step 1: Extract concepts
        concepts = self.ai.extract_concepts(content)
        debug(f"Extracted concepts: {concepts}\n")
        if not concepts:
            print(f"    ⚠ No concepts extracted")
            return {
                'concepts': [],
                'associations_added': 0,
                'memory_connections': 0
            }
        
        print(f"    ✓ Found {len(concepts)} concepts: {[c['concept'] for c in concepts]}")
        
        # Step 2: For each concept, find associations
        associations_added = 0
        
        for concept_data in concepts:
            concept = concept_data['concept'].lower()
            
            # Find associations
            associations = self.ai.find_associations(
                concept=concept,
                context=content
            )
            
            print(f"      → {concept}: {len(associations)} associations")
            
            # Add to graph
            for assoc_data in associations:
                association = Association(
                    source=concept,
                    target=assoc_data['target'],
                    strength=assoc_data['strength'],
                    association_type=assoc_data['type'],
                    reason=assoc_data.get('reason', ''),
                    memory_id=memory_id
                )
                
                self.graph.add(association)
                associations_added += 1
        
        # Step 3: Find connections to other memories
        all_memories = self.Brain.mind.get_all()
        other_memories = [m for m in all_memories if m.get('id') != memory_id]
        
        memory_connections = []
        if other_memories:
            print(f"    → Finding connections to {len(other_memories)} other memories...")
            memory_connections = self.ai.find_memory_connections(
                memory_content=content,
                memory_emotion=emotion,
                existing_memories=other_memories
            )
            print(f"    ✓ Found {len(memory_connections)} memory connections")
        
        # Store in memory
        memory_copy = copy.deepcopy(memory)
        memory_copy['aso_data'] = {
            'concepts': concepts,
            'associations_count': associations_added,
            'memory_connections': memory_connections,
            'processed': True
        }
        
        debug(f"Memory after ASO processing: {memory_copy.get('id','')}\n")
        # Update memory in brain
        self.Brain.mind.replace(old=memory, new=memory_copy)
        self.Brain.mind.commit()
        
        #self.commit()  # Save graph state to brain storage
        return {
            'concepts': concepts,
            'associations_added': associations_added,
            'memory_connections': len(memory_connections)
        }
    
    def process_all_memories(self, reprocess: bool = False):
        """
        Process ALL memories in the brain.
        
        Args:
            reprocess: If True, reprocess even if already processed
        """
        memories = self.Brain.mind.get_all()
        
        print(f"Processing {len(memories)} memories...")
        
        hashtag("LOOPING ASO System - Processing All Memories")
        reset_debug()
        
        for i, memory in enumerate(memories, 1):
            # Skip if already processed (unless reprocessing)
            
            if not reprocess and memory.get('aso_data', {}).get('processed'):
                print(f"  [{i}/{len(memories)}] Skipping (already processed)")
                continue
            
            print(f"  [{i}/{len(memories)}] Processing: {memory.get('content', '')[:50]}...")
            
            debug(f"Processing memory ID: {memory.get('id', '')}\n")
            
            try:
                result = self.process_memory(memory)
                debug(f"CURRENT Result: {result}\n")  
                #debug(f"TESTING: {result.get('test', 'no test value')}\n") 
                print(f"      ✓ {result['associations_added']} associations, {result['memory_connections']} connections")
            
            except Exception as e:
                
                print(f"      ✗ Error: {e}")
        
        self.commit()  # Final commit after processing all
        print(f"\n✓ Complete! {self.get_stats()['total_associations']} total associations")
    
    def find_related(self, concept: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Find concepts related to this one.
        """
        associations = self.graph.get_associations(concept)
        
        # Sort by strength
        sorted_assocs = sorted(associations, key=lambda a: a.strength, reverse=True)
        
        return [
            {
                'concept': a.target,
                'strength': a.strength,
                'type': a.type,
                'reason': a.reason
            }
            for a in sorted_assocs[:max_results]
        ]
    
    def find_path(self, start: str, end: str) -> Optional[List[str]]:
        """
        Find association chain from start to end.
        """
        return self.graph.find_path(start, end)
    
    def what_reminds_me_of(self, concept: str, threshold: float = 0.3) -> Dict[str, float]:
        """
        What does this concept remind me of?
        Uses spreading activation.
        """
        return self.graph.spread_activation(concept, threshold=threshold)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the association network."""
        return self.graph.get_stats()
    
    def get_concept_info(self, concept: str) -> Dict[str, Any]:
        """
        Get all information about a concept.
        """
        concept = concept.lower().strip()
        
        # Get direct associations
        associations = self.graph.get_associations(concept)
        
        # Get memories that mention this concept
        memories = self.Brain.mind.get_all()
        related_memories = []
        
        for memory in memories:
            aso_data = memory.get('aso_data', {})
            concepts = aso_data.get('concepts', [])
            
            if any(c['concept'].lower() == concept for c in concepts):
                related_memories.append({
                    'id': memory['id'],
                    'content': memory['content'],
                    'emotion': memory.get('dominant_emotion')
                })
        
        return {
            'concept': concept,
            'association_count': len(associations),
            'associations': [
                {
                    'target': a.target,
                    'strength': a.strength,
                    'type': a.type
                }
                for a in sorted(associations, key=lambda x: x.strength, reverse=True)[:10]
            ],
            'related_memories': related_memories
        }
        
    def save(self, filepath: str = 'associations.json'):
        """Save association graph."""
        self.graph.save(filepath)
        
    def commit(self):
        """Commit current graph state to brain storage."""
        self.Brain.mind.commit()
        
    def about_ASO(self, more_details: bool = False) -> str:
        """Explain what ASO is in a human-friendly way."""
        
        explaination = r"""
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

        If you are confused I wrote a long page just on associtations, using my mind as an example, you might cringe but you're here to understand |:3\n\n\n\n
        
        """
        if more_details:
            explaination += _explaination()
            
        return explaination.strip()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __str__(self):
        
        return "ASO (Association System): connects ideas and memories."
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - commit changes."""
        self.commit()   
    
    