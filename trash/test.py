


from typing import List, Dict, Any, Optional
import copy


# inside ASO.py
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
            'test':'test_value',
            'associations_added': associations_added,
            'memory_connections': len(memory_connections)
        }
    