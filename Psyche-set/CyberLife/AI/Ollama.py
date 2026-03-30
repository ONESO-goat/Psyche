

import ollama
import json
from typing import Dict, List, Any

class AssociationAI:
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize with a local model. 
        'llama3.2' is great for speed, 'mistral' or 'phi3' are good alternatives.
        """
        self.model_id = model_name
        # Check if model exists, if not, pull it
        try:
            ollama.show(self.model_id)
        except ollama.ResponseError:
            print(f"Model {self.model_id} not found. Pulling now...")
            ollama.pull(self.model_id)

    def find_associations(self, 
                         content: str, 
                         all_memories: List[Dict],
                         max_associations: int = 10) -> Dict[str, Any]:
        
        memory_context = self._build_memory_context(all_memories)
        
        prompt = f"""Analyze this text and find associations:
TEXT: "{content}"
CONTEXT: This person has these memories:
{memory_context}

Return as JSON:
{{
  "direct_associations": {{ "concept": {{ "strength": 10, "related": [] }} }},
  "personal_associations": [ {{ "memory_id": "uuid", "chain": [], "strength": 8 }} ],
  "emotional_associations": {{ "emotion": "happy", "intensity": 0.7, "reason": "why" }}
}}"""

        # Using Ollama's chat with format='json' (forces valid JSON output)
        response = ollama.chat(
            model=self.model_id,
            messages=[
                {'role': 'system', 'content': 'You are a memory analysis engine. Always output valid JSON.'},
                {'role': 'user', 'content': prompt}
            ],
            format='json', # This is the magic "JSON Mode" in Ollama
            options={'temperature': 0.2} # Keep it stable
        )
        
        try:
            return json.loads(response['message']['content'])
        except (json.JSONDecodeError, KeyError):
            return self._fallback_associations(content)

    def find_memory_connections(self, target_memory: Dict, all_memories: List[Dict], threshold: float = 0.5) -> List[Dict]:
        target_content = target_memory.get('content', '')
        other_memories = [m for m in all_memories if m.get('id') != target_memory.get('id')]
        
        if not other_memories: return []

        memory_list = "\n".join([f"- {m['content']} (ID: {m['id']})" for m in other_memories])
        
        prompt = f"Find connections between this memory: '{target_content}' and these: \n{memory_list}\n" \
                 f"Return a JSON array of connections with strength > {threshold}."

        response = ollama.chat(
            model=self.model_id,
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )

        try:
            return json.loads(response['message']['content'])
        except:
            return []

    def _build_memory_context(self, memories: List[Dict], max_memories: int = 5) -> str:
        if not memories: return "No previous memories."
        recent = sorted(memories, key=lambda m: m.get('importance', 0), reverse=True)[:max_memories]
        return "\n".join([f"- {m.get('content')} ({m.get('dominant_emotion')})" for m in recent])

    def _fallback_associations(self, content: str) -> Dict[str, Any]:
        return {
            "direct_associations": {},
            "personal_associations": [],
            "emotional_associations": {"emotion": "neutral", "intensity": 0.5, "reason": "Local model failed"},
            "error": "Failed to parse Ollama response"
        }