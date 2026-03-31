# aso_system.py

from typing import List, Dict, Any, Optional
from ASO.aso_core import Association, AssociationGraph
from ASO.aso_ai import AssociationAI

class ASO:
    """
    Main Association System.
    Combines graph + AI.
    """
    def __init__(self, Brain, api_key: str = ''):
        self.graph = AssociationGraph()
        self.Brain = Brain
        self.memories = self.Brain.mind.get_all()
        self.ai = AssociationAI(api_key=api_key) if api_key else None
    
    def process_memory(self, memory_content: str) -> Dict[str, Any]:
        """
        Process a memory to extract and store associations.
        Returns: {'concepts': [...], 'associations_added': 10}
        """
        
        if not self.ai:
            return {'error': 'No AI configured'}
        
        # Step 1: Extract concepts from memory
        concepts = self.ai.extract_concepts(memory_content)
        
        # Step 2: For each concept, find associations
        associations_added = 0
        
        for concept_data in concepts:
            concept = concept_data['concept'].lower()
            
            # Find what this concept associates with
            associations = self.ai.find_associations(
                concept=concept,
                context=memory_content
            )
            
            # Add to graph
            for assoc_data in associations:
                association = Association(
                    source=concept,
                    target=assoc_data['target'].lower(),
                    strength=assoc_data['strength'],
                    association_type=assoc_data['type'],
                    reason=assoc_data['reason']
                )
                
                self.graph.add(association)
                associations_added += 1
        
        return {
            'concepts': concepts,
            'associations_added': associations_added
        }
    
    def find_related(self, concept: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Find concepts related to this one.
        Returns sorted by strength.
        """
        concept = concept.lower()
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
    
    def find_path_between(self, start: str, end: str) -> Optional[List[str]]:
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
    
    def save(self, filepath: str = 'associations.json'):
        """Save association graph."""
        self.graph.save(filepath)
    
    def load(self, filepath: str = 'associations.json'):
        """Load association graph."""
        self.graph.load(filepath)
    
    def stats(self) -> Dict[str, Any]:
        """Get statistics about the association network."""
        return self.graph.get_stats()