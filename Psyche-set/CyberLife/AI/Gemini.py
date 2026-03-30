# association_ai.py

from google import genai
from typing import Dict, List, Any
from pydantic import BaseModel
import google.genai.errors as errors
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type
import json

class AssociationAI_Gem:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
        # Use Gemini 1.5 Flash (free, fast)
        self.model_id = "gemini-2.0-flash"
    def find_batch_connections(self, target_memory: dict, memory_chunk: list):
        """Checks 10 memories at once to save quota."""
        memory_list_str = "\n".join([f"ID: {m['id']} - Content: {m['content']}" for m in memory_chunk])
        
        prompt = f"""
        New Memory: {target_memory['content']}
        
        Compare it against these {len(memory_chunk)} existing memories:
        {memory_list_str}
        
        Return a JSON list of objects for only the memories that have a strong connection (>0.7).
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    @retry(
        wait=wait_random_exponential(min=1, max=60), 
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(errors.ClientError)
    )   
    def find_associations(self, 
                         content: str, 
                         all_memories: List[Dict],
                         max_associations: int = 10) -> Dict[str, Any]:
        """
        Find associations for content using Gemini.
        Returns both general and personal associations.
        """
        
        # Build context from memories
        memory_context = self._build_memory_context(all_memories)
        
        prompt = f"""Analyze this text and find associations:

TEXT: "{content}"

CONTEXT: This person has these memories:
{memory_context}

Find associations in this format:

1. DIRECT CONCEPTS (words/phrases in the text):
   - Extract key concepts
   - For each, find strength (0-10) and related concepts

2. PERSONAL ASSOCIATIONS (from their memories):
   - Connect to their existing memories
   - Show chain: concept → memory

3. EMOTIONAL ASSOCIATIONS:
   - What emotions does this trigger?
   - Why?

Return as JSON:
{{
  "direct_associations": {{
    "concept": {{
      "strength": 10,
      "related": ["concept1", "concept2"],
      "category": "animals/tech/etc"
    }}
  }},
  "personal_associations": [
    {{
      "memory_id": "uuid",
      "chain": ["concept", "intermediate", "memory"],
      "strength": 8
    }}
  ],
  "emotional_associations": {{
    "emotion": "happy",
    "intensity": 0.7,
    "reason": "why"
  }}
}}

Only return valid JSON, no markdown."""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={
        "system_instruction": "You are a memory analysis engine. Always return raw JSON. No markdown blocks.",
        "response_mime_type": "application/json"
    }
        )
        
        # Parse response

        if response.text:
            self._safe_json_parse(response=response)
            associations = json.loads(response.text)
            return associations
        else:
    # Handle case where Gemini blocked the prompt or failed
            print(f"Empty response. Candidate: {response.candidates[0].finish_reason}")
            return self._fallback_associations(content)
    
    def _build_memory_context(self, 
                              memories: List[Dict], 
                              max_memories: int = 5) -> str:
        """Build compressed memory context for prompt."""
        
        if not memories or len(memories) == 0:
            return "No previous memories."
        
        # Take most recent/important memories
        recent = sorted(memories, 
                       key=lambda m: m.get('importance', 0), 
                       reverse=True)[:max_memories]
        
        context = ""
        for i, mem in enumerate(recent, 1):
            context += f"{i}. {mem.get('content', 'N/A')} (emotion: {mem.get('dominant_emotion', 'N/A')})\n"
        
        return context
    
    def _fallback_associations(self, content: str) -> Dict[str, Any]:
        """Fallback if API fails."""
        return {
            "direct_associations": {},
            "personal_associations": [],
            "emotional_associations": {
                "emotion": "neutral",
                "intensity": 0.5,
                "reason": "Unable to process"
            },
            "error": "Failed to parse API response"
        }
    
    def find_memory_connections(self, 
                                target_memory: Dict,
                                all_memories: List[Dict],
                                threshold: float = 0.5) -> List[Dict]:
        """
        Find which existing memories connect to target memory.
        """
        
        target_content = target_memory.get('content', '')
        
        # Build list of other memories
        other_memories = [m for m in all_memories 
                         if m.get('id') != target_memory.get('id')]
        
        if not other_memories:
            return []
        
        memory_list = "\n".join([
            f"{i}. {m['content']} (ID: {m['id']})"
            for i, m in enumerate(other_memories, 1)
        ])
        
        prompt = f"""Find connections between this new memory and existing memories:

NEW MEMORY: "{target_content}"

EXISTING MEMORIES:
{memory_list}

For each existing memory that connects, explain:
1. How they connect (shared concepts, emotions, people, places, etc.)
2. Strength of connection (0.0-1.0)
3. The connecting path

Return as JSON array:
[
  {{
    "memory_id": "uuid",
    "connection_path": ["concept1", "concept2"],
    "strength": 0.8,
    "reason": "Both involve..."
  }}
]

Only include connections with strength > {threshold}.
Only return valid JSON, no markdown."""

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={
        "system_instruction": "You are a memory analysis engine. Always return raw JSON. No markdown blocks.",
        "response_mime_type": "application/json"
    }
        )
        
        if response.text:
         
            associations = json.loads(response.text)
            return associations
        else:
            raise SystemError(f"Empty response. Candidate: {response.candidates[0].finish_reason}")
    
    def _safe_json_parse(self, response):
        # Check if we even got text back
        text = response.text
        if not text:
            return None
        
        # Clean tags only if they exist
        if "```" in text:
            # Splits by triple backticks and takes the content between the first two sets
            parts = text.split("```")
            for part in parts:
                # Look for the part that actually looks like JSON
                if part.startswith("json"):
                    text = part[4:]
                    break
                elif "{" in part:
                    text = part
                    break
                    
        return json.loads(text.strip())