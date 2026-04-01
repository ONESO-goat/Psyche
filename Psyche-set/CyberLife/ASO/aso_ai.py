# ASO/aso_ai.py - Universal AI interface for both Gemini and Ollama

import json
from typing import Dict, List, Any

class AssociationAI:
    """
    Universal AI interface for finding associations.
    Supports both Gemini and Ollama.
    """
    def __init__(self, api_key: str | None = None, model: str = 'ollama'):
        """
        Initialize AI.
        
        Args:
            api_key: Gemini API key (if using Gemini)
            model: 'gemini' or 'ollama'
        """
        self.model_type = model.lower()
        
        if self.model_type == 'gemini' and api_key:
            # Use Gemini
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.backend = 'gemini'
            print("✓ Using Gemini 1.5 Flash")
            
        else:
            # Use Ollama
            self.backend = 'ollama'
            self.ollama_model = 'qwen2.5:latest'
            
            # Check if Ollama is available
            try:
                import ollama
                ollama.show(self.ollama_model)
                print(f"✓ Using Ollama ({self.ollama_model})")
            except:
                print(f"⚠ Ollama model '{self.ollama_model}' not found")
                print("  Run: ollama pull qwen2.5:latest")
    
    def extract_concepts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract key concepts from text.
        
        Returns:
            [{'concept': 'dog', 'category': 'animals', 'importance': 0.9}, ...]
        """
        prompt = f"""Extract key concepts from this text:

"{text}"

Find 3-7 main concepts (nouns, entities, ideas).

For each concept:
- concept: the word/phrase
- category: animals/people/places/objects/emotions/activities/abstract/technology
- importance: 0.0-1.0 (how central to this text)

Return ONLY valid JSON (no markdown, no explanation):
[
  {{"concept": "dog", "category": "animals", "importance": 0.9}},
  {{"concept": "friend", "category": "people", "importance": 0.8}}
]"""

        response_text = self._generate(prompt)
        concepts = self._parse_json(response_text, default=[])
        
        # Validate structure
        if isinstance(concepts, list):
            valid_concepts = []
            for c in concepts:
                if isinstance(c, dict) and 'concept' in c:
                    valid_concepts.append({
                        'concept': c.get('concept', '').lower().strip(),
                        'category': c.get('category', 'abstract'),
                        'importance': float(c.get('importance', 0.5))
                    })
            return valid_concepts
        
        return []
    
    def find_associations(self, 
                         concept: str,
                         context: str = '') -> List[Dict[str, Any]]:
        """
        Find what associates with this concept.
        
        Returns:
            [{'target': 'pet', 'strength': 0.9, 'type': 'semantic', 'reason': '...'}, ...]
        """
        context_str = f"\nContext: {context}" if context else ""
        
        prompt = f"""Find associations for the concept: "{concept}"{context_str}

What strongly associates with "{concept}"?

Find 5-10 associations:
- target: what it associates to
- strength: 0.0-1.0 (be realistic, most are 0.4-0.8)
- type: semantic/temporal/emotional/causal/functional
- reason: brief explanation (one sentence)

Examples:
- "dog" → "pet" (0.9, semantic, "dogs are common pets")
- "dog" → "loyal" (0.7, emotional, "dogs known for loyalty")

Return ONLY valid JSON (no markdown):
[
  {{"target": "pet", "strength": 0.9, "type": "semantic", "reason": "dogs are common pets"}},
  {{"target": "loyal", "strength": 0.7, "type": "emotional", "reason": "dogs known for loyalty"}}
]"""

        response_text = self._generate(prompt)
        associations = self._parse_json(response_text, default=[])
        
        # Validate structure
        if isinstance(associations, list):
            valid_assocs = []
            for a in associations:
                if isinstance(a, dict) and 'target' in a and 'strength' in a:
                    valid_assocs.append({
                        'target': a.get('target', '').lower().strip(),
                        'strength': max(0.0, min(1.0, float(a.get('strength', 0.5)))),
                        'type': a.get('type', 'semantic'),
                        'reason': a.get('reason', '')
                    })
            return valid_assocs
        
        return []
    
    def find_memory_connections(self,
                               memory_content: str,
                               memory_emotion: str,
                               existing_memories: List[Dict]) -> List[Dict[str, Any]]:
        """
        Find which existing memories connect to this new memory.
        
        Returns:
            [{'memory_id': 'uuid', 'shared_concepts': ['dog'], 'strength': 0.7, 'reason': '...'}, ...]
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

Connection rules:
✅ Connect if: shared people/places/objects/topics/causes/emotions
❌ Don't connect if: completely different topics

For each connection:
- memory_id: the ID from the list
- shared_concepts: specific things they share
- strength: 0.0-1.0 (how strong the connection)
- reason: why they connect (one sentence)

Return ONLY valid JSON (no markdown):
[
  {{"memory_id": "uuid-here", "shared_concepts": ["dog", "pet"], "strength": 0.8, "reason": "both about dogs"}},
  {{"memory_id": "uuid-here", "shared_concepts": ["rejection", "sadness"], "strength": 0.6, "reason": "both involve disappointment"}}
]

If no genuine connections exist, return: []"""

        response_text = self._generate(prompt)
        connections = self._parse_json(response_text, default=[])
        
        # Validate structure
        if isinstance(connections, list):
            valid_conns = []
            for c in connections:
                if isinstance(c, dict) and 'memory_id' in c:
                    valid_conns.append({
                        'memory_id': c.get('memory_id', ''),
                        'shared_concepts': c.get('shared_concepts', []),
                        'strength': max(0.0, min(1.0, float(c.get('strength', 0.5)))),
                        'reason': c.get('reason', '')
                    })
            return valid_conns
        
        return []
    
    def _generate(self, prompt: str) -> str:
        """Generate response from AI backend."""
        
        if self.backend == 'gemini':
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"⚠ Gemini error: {e}")
                return '[]'
        
        else:  # Ollama
            try:
                import ollama
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {'role': 'system', 'content': 'You are a memory analysis engine. Always output valid JSON with no markdown.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    format='json',  # Force JSON mode
                    options={'temperature': 0.2}
                )
                
                return response['message']['content']
                
            except Exception as e:
                print(f"⚠ Ollama error: {e}")
                return '[]'
    
    def _parse_json(self, text: str, default: Any = None) -> Any:
        """Robust JSON parsing."""
        if not text or text.strip() == '':
            return default if default is not None else []
        
        text = text.strip()
        
        # Remove markdown if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Try to parse
        try:
            parsed = json.loads(text)
            return parsed
        except json.JSONDecodeError as e:
            print(f"⚠ JSON parse error: {e}")
            print(f"  Raw text: {text[:200]}...")
            return default if default is not None else []