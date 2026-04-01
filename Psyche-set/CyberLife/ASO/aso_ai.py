# ASO/aso_ai.py

import json
from typing import Dict, List, Any

class AssociationAI:
    """
    AI for finding associations.
    Supports both Gemini and Ollama.
    """
    def __init__(self, api_key: str | None = None, model: str = 'gemini'):
        self.model_type = model
        
        if model == 'gemini' and api_key:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.use_gemini = True
        else:
            # Use Ollama
            self.use_gemini = False
            self.ollama_model = 'qwen2.5:latest'
    
    def extract_concepts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract key concepts from text.
        """
        prompt = f"""Extract key concepts from: "{text}"

Find 3-7 main concepts (nouns, entities, ideas).

Return ONLY JSON (no markdown):
[
  {{"concept": "word", "category": "animals/people/places/objects/emotions/activities/abstract", "importance": 0.9}}
]"""

        response_text = self._generate(prompt)
        return self._parse_json(response_text, default=[])
    
    def find_associations(self, 
                         concept: str,
                         context: str = '') -> List[Dict[str, Any]]:
        """
        Find associations for a concept.
        """
        context_str = f"\nContext: {context}" if context else ""
        
        prompt = f"""Concept: "{concept}"{context_str}

What strongly associates with "{concept}"?

Find 5-10 associations:
- Target concept
- Strength (0.0-1.0, realistic, most 0.4-0.8)
- Type: semantic/temporal/emotional/causal/functional
- Reason (one sentence)

Return ONLY JSON (no markdown):
[
  {{"target": "concept", "strength": 0.8, "type": "semantic", "reason": "brief"}}
]"""

        response_text = self._generate(prompt)
        return self._parse_json(response_text, default=[])
    
    def find_memory_connections(self,
                               memory_content: str,
                               memory_emotion: str,
                               existing_memories: List[Dict]) -> List[Dict[str, Any]]:
        """
        Find which existing memories connect to this new memory.
        """
        if not existing_memories:
            return []
        
        # Build memory context (limit to 5 most recent)
        memory_list = ""
        for i, mem in enumerate(existing_memories[-5:], 1):
            content = mem.get('content', 'N/A')
            emotion = mem.get('dominant_emotion', 'neutral')
            mem_id = mem.get('id', 'unknown')
            memory_list += f"{i}. \"{content}\" (emotion: {emotion}, ID: {mem_id})\n"
        
        prompt = f"""NEW MEMORY: "{memory_content}" (emotion: {memory_emotion})

EXISTING MEMORIES:
{memory_list}

Which existing memories genuinely connect to the new one?

Rules:
✅ Connect if: shared people/places/objects/topics/causes
❌ Don't connect if: just same emotion but different topics

Return ONLY JSON (no markdown):
[
  {{"memory_id": "uuid", "shared_concepts": ["specific"], "strength": 0.7, "reason": "why"}}
]

If no connections: []"""

        response_text = self._generate(prompt)
        return self._parse_json(response_text, default=[])
    
    def _generate(self, prompt: str) -> str:
        """Generate response from AI."""
        if self.use_gemini:
            response = self.model.generate_content(prompt)
            return response.text
        else:
            # Use Ollama
            import requests
            
            try:
                response = requests.post(
                    'http://localhost:11434/api/generate',
                    json={
                        'model': self.ollama_model,
                        'prompt': prompt,
                        'stream': False
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json().get('response', '')
                else:
                    return '[]'
            except:
                return '[]'
    
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