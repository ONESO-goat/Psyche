# aso_ai.py

from AI.Ollama import AssociationAI_32, AssociationAI_qwen


import json
from typing import Dict, List, Any,Optional
import copy
from ASO.aso_core import Association, AssociationGraph

class AssociationAI:
    """
    Uses AI to find associations.
    """
    def __init__(self, 
                 api_key: Optional[str]= None, 
                 model_name: str = "ollama",
                 model_id: str = "qwen-0.5-flash"):
        """Model name can be 'ollama', 'claude', 'chatgpt','gemini', etc. Ollama is default for local."""
        
        if model_name.lower().strip() == "ollama":
            try:
                self.AI = AssociationAI_qwen(model_name=model_id) or AssociationAI_32(model_name='llama3.2')
                
            except Exception as e:
                self.AI = None
                
                raise ValueError(f"Error initializing Ollama: {e}")
                
        else:
            raise ValueError(f"Unsupported model_name: {model_name}, more models coming soon!")
            
    
    def extract_concepts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract key concepts from text.
        Returns: [{'concept': 'dog', 'category': 'animals', 'importance': 0.9}, ...]
        """
        
        prompt = f"""Extract key concepts from this text:

"{text}"

Find 3-7 main concepts (nouns, entities, ideas).

For each concept:
- What is it?
- Category (person/place/object/emotion/activity/abstract/animal/technology)
- Importance to this text (0.0-1.0)

Return ONLY valid JSON (no markdown):
[
  {{
    "concept": "word",
    "category": "category",
    "importance": 0.9
  }}
]"""

        response = self.model.generate_content(prompt)
        return self._parse_json(response.text, default=[])
    
    def find_associations(self, 
                         concept: str,
                         context: str = '') -> List[Dict[str, Any]]:
        """
        Find what associates with this concept.
        Returns: [{'target': 'cat', 'strength': 0.8, 'type': 'semantic', 'reason': '...'}, ...]
        """
        
        context_str = f"\nContext: {context}" if context else ""
        
        prompt = f"""Find associations for the concept: "{concept}"{context_str}

What concepts does "{concept}" strongly associate with?

Find 5-10 associations. For each:
- Target concept (what it associates to)
- Strength (0.0-1.0, be realistic, most are 0.4-0.8)
- Type: semantic/temporal/emotional/causal/functional
- Brief reason (one sentence)

Examples:
- "dog" → "pet" (0.9, semantic, "dogs are common pets")
- "dog" → "loyal" (0.7, emotional, "dogs known for loyalty")
- "rain" → "wet" (0.9, causal, "rain causes wetness")

Return ONLY valid JSON (no markdown):
[
  {{
    "target": "concept",
    "strength": 0.8,
    "type": "semantic",
    "reason": "brief reason"
  }}
]"""

        response = self.model.generate_content(prompt)
        return self._parse_json(response.text, default=[])
    
    def find_memory_associations(self,
                                memory_content: str,
                                existing_concepts: List[str] = []) -> List[Dict[str, Any]]:
        """
        Find which existing concepts this memory associates with.
        """
        
        if not existing_concepts:
            return []
        
        concepts_str = ", ".join(existing_concepts[:20])  # Limit to 20
        
        prompt = f"""Memory: "{memory_content}"

Existing concepts in the brain: {concepts_str}

Which of these existing concepts does this memory connect to?

Only include genuine connections (shared topics, emotions, causes).

Return ONLY valid JSON (no markdown):
[
  {{
    "concept": "existing_concept",
    "strength": 0.7,
    "reason": "why they connect"
  }}
]

If no connections, return: []"""

        response = self.model.generate_content(prompt)
        return self._parse_json(response.text, default=[])
    
    def _parse_json(self, text: str, default: Any = None) -> Any:
        """Robust JSON parsing."""
        text = text.strip()
        
        # Remove markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        try:
            return json.loads(text)
        except:
            return default if default is not None else {}