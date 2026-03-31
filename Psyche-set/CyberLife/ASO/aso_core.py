# aso_core.py

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
                 reason: str = ''):
        self.source = source
        self.target = target
        self.strength = max(0.0, min(1.0, strength))  # Clamp 0-1
        self.type = association_type  # 'semantic', 'temporal', 'emotional', 'causal'
        self.reason = reason
        self.created = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source,
            'target': self.target,
            'strength': self.strength,
            'type': self.type,
            'reason': self.reason,
            'created': self.created
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Association':
        assoc = Association(
            source=data['source'],
            target=data['target'],
            strength=data['strength'],
            association_type=data['type'],
            reason=data.get('reason', '')
        )
        assoc.created = data.get('created', datetime.now().isoformat())
        return assoc


class AssociationGraph:
    """
    Core association network.
    Stores all associations as a graph.
    """
    def __init__(self):
        # Graph structure: {concept: [Association, Association, ...]}
        self.graph: Dict[str, List[Association]] = {}
    
    def add(self, association: Association):
        """Add bidirectional association."""
        # Forward link
        if association.source not in self.graph:
            self.graph[association.source] = []
        self.graph[association.source].append(association)
        
        # Backward link (reverse direction)
        reverse = Association(
            source=association.target,
            target=association.source,
            strength=association.strength,
            association_type=association.type,
            reason=association.reason
        )
        
        if association.target not in self.graph:
            self.graph[association.target] = []
        self.graph[association.target].append(reverse)
    
    def get_associations(self, concept: str) -> List[Association]:
        """Get all associations for a concept."""
        return self.graph.get(concept.lower(), [])
    
    def find_path(self, 
                  start: str, 
                  end: str, 
                  max_depth: int = 5) -> Optional[List[str]]:
        """
        Find association path from start to end concept.
        Returns chain like: ["dog", "mammal", "cat"]
        """
        start = start.lower()
        end = end.lower()
        
        if start == end:
            return [start]
        
        # BFS (breadth-first search)
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
        
        return None  # No path found
    
    def spread_activation(self, 
                         start: str, 
                         threshold: float = 0.3,
                         max_hops: int = 3) -> Dict[str, float]:
        """
        Spreading activation from start concept.
        Returns {concept: activation_strength}
        """
        start = start.lower()
        
        # Track activation levels
        activation = {start: 1.0}
        
        # Process in waves
        current_wave = {start: 1.0}
        
        for hop in range(max_hops):
            next_wave = {}
            
            for concept, strength in current_wave.items():
                # Get associations
                associations = self.get_associations(concept)
                
                for assoc in associations:
                    target = assoc.target.lower()
                    
                    # Calculate new activation (decays with distance)
                    new_activation = strength * assoc.strength * 0.7  # 30% decay per hop
                    
                    if new_activation > threshold:
                        # Update activation (take max if multiple paths)
                        if target in activation:
                            activation[target] = max(activation[target], new_activation)
                        else:
                            activation[target] = new_activation
                        
                        # Add to next wave
                        if target not in next_wave or next_wave[target] < new_activation:
                            next_wave[target] = new_activation
            
            current_wave = next_wave
            
            if not current_wave:
                break
        
        return activation
    
    def save(self, filepath: str):
        """Save graph to JSON."""
        data = {}
        for concept, associations in self.graph.items():
            data[concept] = [a.to_dict() for a in associations]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str):
        """Load graph from JSON."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.graph = {}
        for concept, associations in data.items():
            self.graph[concept] = [Association.from_dict(a) for a in associations]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics."""
        total_concepts = len(self.graph)
        total_associations = sum(len(assocs) for assocs in self.graph.values())
        
        # Average associations per concept
        avg_associations = total_associations / total_concepts if total_concepts > 0 else 0
        
        # Most connected concepts
        sorted_concepts = sorted(
            self.graph.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        top_connected = [
            (concept, len(assocs))
            for concept, assocs in sorted_concepts[:10]
        ]
        
        return {
            'total_concepts': total_concepts,
            'total_associations': total_associations,
            'avg_associations_per_concept': avg_associations,
            'most_connected': top_connected
        }