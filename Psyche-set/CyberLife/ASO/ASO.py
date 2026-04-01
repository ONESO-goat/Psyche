# ASO/ASO.py

from typing import List, Dict, Any, Optional
from ASO.aso_core import Association, AssociationGraph
from ASO.aso_ai import AssociationAI
import copy

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
        self.ai = AssociationAI(api_key=api_key, model=model) if api_key or model == 'ollama' else None
    
    def process_memory(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a memory to extract and store associations.
        
        Args:
            memory: Memory dict with 'content', 'id', 'dominant_emotion'
        
        Returns:
            Stats about processing
        """
        if not self.ai:
            return {'error': 'No AI configured'}
        
        content = memory.get('content', '')
        memory_id = memory.get('id', '')
        emotion = memory.get('dominant_emotion', 'neutral')
        
        # Step 1: Extract concepts
        concepts = self.ai.extract_concepts(content)
        
        if not concepts:
            return {'concepts': [], 'associations_added': 0}
        
        # Step 2: For each concept, find associations
        associations_added = 0
        
        for concept_data in concepts:
            concept = concept_data['concept'].lower()
            
            # Find associations
            associations = self.ai.find_associations(
                concept=concept,
                context=content
            )
            
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
        
        memory_connections = self.ai.find_memory_connections(
            memory_content=content,
            memory_emotion=emotion,
            existing_memories=other_memories
        )
        
        # Store in memory
        memory_copy = copy.deepcopy(memory)
        memory_copy['aso_data'] = {
            'concepts': concepts,
            'associations_count': associations_added,
            'memory_connections': memory_connections,
            'processed': True
        }
        
        # Update memory in brain
        self.Brain.mind.replace(old=memory, new=memory_copy)
        self.Brain.mind.commit()
        
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
        
        for i, memory in enumerate(memories, 1):
            # Skip if already processed (unless reprocessing)
            if not reprocess and memory.get('aso_data', {}).get('processed'):
                print(f"  [{i}/{len(memories)}] Skipping (already processed)")
                continue
            
            print(f"  [{i}/{len(memories)}] Processing: {memory.get('content', '')[:50]}...")
            
            try:
                result = self.process_memory(memory)
                print(f"      ✓ {result['associations_added']} associations, {result['memory_connections']} connections")
            except Exception as e:
                print(f"      ✗ Error: {e}")
        
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