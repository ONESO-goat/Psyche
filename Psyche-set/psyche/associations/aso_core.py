# ASO/aso_core.py

import json
import asyncio
import copy
from typing import (
    Dict, 
    List, 
    Any, 
    Optional,
    Final,
    final
)
from datetime import datetime
from helpers.python_.helpers import Association

class AssociationGraph:
    """
    Core association network stored in Brain structure.

    Linked True structure, topics that have connections, these connections being associations.
    """
    def __init__(self, topic_data: Dict): # Topic 
        """
            brain_storage should be the 'brain' dict from your structure.
            We'll store associations inside it.
        """
        self.graph = {}

        self.topic_data = topic_data
        
        # Initialize associations storage if it doesn't exist
        if 'associations' not in self.topic_data:
            self.topic_data['associations'] = {
                'graph': {},  # {concept: [Association, ...]}
                'metadata': {
                    'total_concepts': 0,
                    'total_associations': 0,
                    'last_updated': datetime.now().isoformat()
                }
            }
            """
            example:
                {

                    "
                }
            """
    
    # @property
    # def graph(self) -> Dict[str, List[Dict]]:
    #     """
    #         Access the graph from brain storage.
    #     """

    #     # NOTE: REDO 

    #     return self.graph
    
    def add(self, association: Association):
        """
        Add bidirectional association.
        Adding new association to the graph.
        """
        if not association:
            raise RuntimeError("Association is required.")
        
        # Forward link
        if association.source_id not in self.graph:
            self.graph[association.source_id] = []
        
        # Check for duplicates
        exists = any(
            [a.get('topic_two_id', ""), a.get('topic_one_id', "")] 
            == # equals
            [association.topic_two_id, association.topic_one_id] 

            for a in self.graph[association.source_id]
        )
        
        if not exists:
            self.graph[association.source_id].append(association.to_dict())
        
        # Backward link (reverse direction)
        if association.topic_one_id not in self.graph:
            self.graph[association.topic_one_id] = []

        if association.topic_two_id not in self.graph:
            self.graph[association.topic_two_id] = []
        
        # exists_reverse = any(
        #     a['target'] == association.source and a['type'] == association.ty
        #     for a in self.graph[association.target]
        # )
        
        # if not exists_reverse:
        #     reverse = Association(
        #         source=association.target,
        #         target=association.source,
        #         strength=association.strength,
        #         association_type=association.type,
        #         reason=association.reason,
        #         memory_id=association.memory_id
        #     )
        #     self.graph[association.target].append(reverse.to_dict())
        
        # Update metadata
        self._update_metadata()
    
    async def get_associations(self, topic_id: str, max_limit:int) -> List[Association]:
        """Get all associations that connect to a topic/concept."""

        # TODO: Loop, max_limit tells how many to get
    
        
        if not topic_id:
            raise RuntimeError("concept can not be null")
        if not 0 < max_limit <= 100: # Goal is 1000, for now for speed and simple formats, stay at the minimal 100.
            raise RuntimeError("Limit falls outside of valid range (1-100)")

        # asyncio.wait_for()
        assoc_dicts = self.graph.get(topic_id, [])
        return [Association.from_dict(a) for a in assoc_dicts]
    
    @final
    async def _obtain_associations(self, topic_id:str[43], concept:str="")->None|list[Association]:
        """
            Get associations to a concept. Since these associations already have associations,
            we just need direct associations.
            @topic_id (str): The topic id. Can be empty, but then the concept will be required for context.
            @concept (str) default = "": If an Id is not provided, we'll use concept and do some regex.

            return List[Associations] || None if noting was found, ot id and concept we're empty.
        """

        """
            The difference between this function and get_associations is that this gets all, 
            with the concept search being available.
        """
        if not topic_id and not concept:
            return None

        if topic_id:
            if topic_id not in self.graph:
                raise KeyError("Topic ID not found in graph")
            
            ASSOCIATIONS_DATA: Final[list[Association]] = self.graph.get(topic_id, [])
            
            return ASSOCIATIONS_DATA
        else:
            raise NotImplementedError(
                "Concept find in AssociationGraph._obtain_associations() not yet implemented. "
            )
            

        
    def find_path(self, 
                  start_id: str, 
                  end_id: str, 
                  max_depth: int = 5) -> Optional[List[str]]:
        """
        Find association path from start to end concept.
        BFS (breadth-first search).
        """
        start = start.lower().strip()
        end = end.lower().strip()
        
        if start_id == end_id:
            return [start_id]
        
        if start_id not in self.graph:
            return None
        
        # BFS
        queue = [(start_id, [start_id])]
        visited = {start_id}
        
        while queue:
            current_id, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            # Get all associations from current concept
            associations: Final[List[Association] | None] = self._obtain_associations(topic_id=current_id)
            if not associations:
                return []
            
            for assoc in associations:
                next_concept = assoc.topic_two_id.lower()
                
                if next_concept == end_id:
                    return path + [next_concept]
                
                if next_concept not in visited:
                    visited.add(next_concept)
                    queue.append((next_concept, path + [next_concept]))
        
        return None
    
    def spread_activation(self, 
                         start_topic_id: str, 
                         threshold: float = 0.2,
                         max_hops: int = 3) -> Dict[str, float]:
        """
        Spreading activation from start concept.
        Returns {concept: activation_strength}
        """
        
        if start_topic_id not in self.graph:
            return {start_topic_id: 1.0}
        
        # Track activation levels
        activation = {start_topic_id: 1.0}
        current_wave = {start_topic_id: 1.0}
        
        for hop in range(max_hops):
            next_wave = {}
            
            for topic_id, strength in current_wave.items():

                # Get associations, max 25 to avoid long loops/searches
                associations: list[Association] = self.get_associations(topic_id, max_limit=25)
                
                for assoc in associations:

                    # Target is just the second topic
                    target = assoc.topic_two_id.lower()
                    
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
        # TODO: fix
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

        # TODO: When saving to json, review the json before saving to the database.
        with open(filepath, 'w') as f:
            json.dump(self.brain['associations'], f, indent=2)
            
    def load(self, filepath: str = 'associations.json'):
        """Load association graph from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.brain['associations'] = data