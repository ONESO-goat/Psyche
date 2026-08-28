# ASO/aso_core.py

import json
import copy
from typing import Dict, List, Any, Optional
from datetime import datetime

class Association:
    """
    Single association between two concepts.
    """
    def __init__(self, 
                 source: str,
                 target: str, 
                 strength: float,
                 association_type: str,
                 reason: str = '',
                 memory_id: str | None = None):
        
        self.source = source.lower().strip()
        self.target = target.lower().strip()
        self.strength = max(0.0, min(1.0, strength))  # Clamp 0-1
        self.type = association_type  # 'semantic', 'temporal', 'emotional', 'causal', 'functional'
        self.reason = reason
        self.memory_id = memory_id  # Track which memory created this
        self.created = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source,
            'target': self.target,
            'strength': self.strength,
            'type': self.type,
            'reason': self.reason,
            'memory_id': self.memory_id,
            'created': self.created
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Association':
        assoc = Association(
            source=data['source'],
            target=data['target'],
            strength=data['strength'],
            association_type=data['type'],
            reason=data.get('reason', ''),
            memory_id=data.get('memory_id')
        )
        assoc.created = data.get('created', datetime.now().isoformat())
        return assoc


class AssociationGraph:
    """
    Core association network stored in Brain structure.
    """
    def __init__(self, brain_storage: Dict):
        """
        brain_storage should be the 'brain' dict from your structure.
        We'll store associations inside it.
        """
        self.brain = brain_storage
        
        # Initialize associations storage if it doesn't exist
        if 'associations' not in self.brain:
            self.brain['associations'] = {
                'graph': {},  # {concept: [Association, ...]}
                'metadata': {
                    'total_concepts': 0,
                    'total_associations': 0,
                    'last_updated': datetime.now().isoformat()
                }
            }
    
    @property
    def graph(self) -> Dict[str, List[Dict]]:
        """Access the graph from brain storage."""
        return self.brain['associations']['graph']
    
    def add(self, association: Association):
        """Add bidirectional association."""
        # Forward link
        if association.source not in self.graph:
            self.graph[association.source] = []
        
        # Check for duplicates
        exists = any(
            a['target'] == association.target and a['type'] == association.type
            for a in self.graph[association.source]
        )
        
        if not exists:
            self.graph[association.source].append(association.to_dict())
        
        # Backward link (reverse direction)
        if association.target not in self.graph:
            self.graph[association.target] = []
        
        exists_reverse = any(
            a['target'] == association.source and a['type'] == association.type
            for a in self.graph[association.target]
        )
        
        if not exists_reverse:
            reverse = Association(
                source=association.target,
                target=association.source,
                strength=association.strength,
                association_type=association.type,
                reason=association.reason,
                memory_id=association.memory_id
            )
            self.graph[association.target].append(reverse.to_dict())
        
        # Update metadata
        self._update_metadata()
    
    def get_associations(self, concept: str) -> List[Association]:
        """Get all associations for a concept."""
        concept = concept.lower().strip()
        assoc_dicts = self.graph.get(concept, [])
        return [Association.from_dict(a) for a in assoc_dicts]
    
    def find_path(self, 
                  start: str, 
                  end: str, 
                  max_depth: int = 5) -> Optional[List[str]]:
        """
        Find association path from start to end concept.
        BFS (breadth-first search).
        """
        start = start.lower().strip()
        end = end.lower().strip()
        
        if start == end:
            return [start]
        
        if start not in self.graph:
            return None
        
        # BFS
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            # Get all associations from current concept
            associations = self.get_associations(current)
            
            for assoc in associations:
                next_concept = assoc.target.lower()
                
                if next_concept == end:
                    return path + [next_concept]
                
                if next_concept not in visited:
                    visited.add(next_concept)
                    queue.append((next_concept, path + [next_concept]))
        
        return None
    
    def spread_activation(self, 
                         start: str, 
                         threshold: float = 0.2,
                         max_hops: int = 3) -> Dict[str, float]:
        """
        Spreading activation from start concept.
        Returns {concept: activation_strength}
        """
        start = start.lower().strip()
        
        if start not in self.graph:
            return {start: 1.0}
        
        # Track activation levels
        activation = {start: 1.0}
        current_wave = {start: 1.0}
        
        for hop in range(max_hops):
            next_wave = {}
            
            for concept, strength in current_wave.items():
                associations = self.get_associations(concept)
                
                for assoc in associations:
                    target = assoc.target.lower()
                    
                    # Activation decays with distance
                    new_activation = strength * assoc.strength * 0.7  # 30% decay
                    
                    if new_activation > threshold:
                        # Take max if multiple paths
                        if target in activation:
                            activation[target] = max(activation[target], new_activation)
                        else:
                            activation[target] = new_activation
                        
                        if target not in next_wave or next_wave[target] < new_activation:
                            next_wave[target] = new_activation
            
            current_wave = next_wave
            
            if not current_wave:
                break
        
        return activation
    
    def _update_metadata(self):
        """Update graph statistics."""
        self.brain['associations']['metadata'] = {
            'total_concepts': len(self.graph),
            'total_associations': sum(len(assocs) for assocs in self.graph.values()),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics."""
        total_concepts = len(self.graph)
        total_associations = sum(len(assocs) for assocs in self.graph.values())
        
        avg_associations = total_associations / total_concepts if total_concepts > 0 else 0
        
        # Most connected concepts
        sorted_concepts = sorted(
            self.graph.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        top_connected = [
            {'concept': concept, 'count': len(assocs)}
            for concept, assocs in sorted_concepts[:10]
        ]
        
        return {
            'total_concepts': total_concepts,
            'total_associations': total_associations,
            'avg_associations_per_concept': round(avg_associations, 2),
            'most_connected': top_connected
        }
        
    def save(self, filepath: str = 'associations.json'):
        """Save association graph to file."""
        with open(filepath, 'w') as f:
            json.dump(self.brain['associations'], f, indent=2)
            
    def load(self, filepath: str = 'associations.json'):
        """Load association graph from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.brain['associations'] = data