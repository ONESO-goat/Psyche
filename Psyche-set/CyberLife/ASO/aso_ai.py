# ASO/aso_ai.py - Universal AI interface for both Gemini and Ollama

import json
from typing import Dict, List, Any
from debugging_utils import debug, reset_debug, hashtag

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
        self.model_type = model.lower().strip()
        
        if self.model_type == 'gemini' and api_key:
            # Use Gemini
            from google import genai
            
            
            self.client = genai.Client(api_key=api_key)
            self.model_id = 'gemini-2.5-flash'
            
            #self.model = self.client.models.get(model=self.model_id)
            self.backend = 'gemini'
            
            print("✓ Using Gemini 1.5 Flash via new Gen AI SDK")
            
            
        else:
            # Use Ollama
            
            # ollama run qwen2.5:latest
            self.backend = 'ollama'
            self.ollama_model = 'qwen3:0.6b'
            
            # Check if Ollama is available
            try:
                import ollama
                ollama.show(self.ollama_model)
                print(f"✓ Using Ollama ({self.ollama_model})")
            except:
                print(f"⚠ Ollama model '{self.ollama_model}' not found")
                print("  Run: ollama pull qwen3:0.6b")
    
    def extract_concepts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract key concepts from text.
        
        Returns:
            [{'concept': 'dog', 'category': 'animals', 'importance': 0.9}, ...]
        """
        reset_debug()
        debug(f"Extracting concepts from: \"{text[:50]}...\"\n")
        hashtag("EXTRACTING CONCEPTS")
        
        prompt = self._extract_concepts_prompt(text)

        response_text = self._generate(prompt)
        debug(f"Raw concept extraction response: {response_text[:200]}...\n")
        concepts = self._parse_json(response_text, default=[])
        debug(f"Parsed concepts: {concepts}\n")
        
        # Validate structure
        if isinstance(concepts, dict):
            debug(f" Validating {len(concepts)} concepts...\n")
            valid_concepts = []
            
            valid_concepts.append({
                        'concept': concepts.get('concept', '').lower().strip(),
                        'category': concepts.get('category', 'abstract'),
                        'importance': float(concepts.get('importance', 0.5))
                    })
            debug(f"CURRENT valid concepts: {valid_concepts}\n")
            return valid_concepts
        
        elif isinstance(concepts, list):
                valid_concepts = []
                for c in concepts:
                    debug(f"Data for concept: {c}\n")
                    if isinstance(c, dict) and 'concept' in c:
                        debug(f"Valid concept found: {c}\n")
                        valid_concepts.append({
                            'concept': c.get('concept', '').lower().strip(),
                            'category': c.get('category', 'abstract'),
                            'importance': float(c.get('importance', 0.5))
                        })
                    debug(f"CURRENT valid concepts: {valid_concepts}\n")
                return valid_concepts
        debug("No valid concepts found.\n")
        return []
    
    def find_associations(self, 
                         concept: str,
                         context: str = '') -> List[Dict[str, Any]]:
        """
        Find what associates with this concept.
        
        Returns:
            [{'target': 'pet', 'strength': 0.9, 'type': 'semantic', 'reason': '...'}, ...]
        """
        #context_str = f"\nContext: {context}" if context else ""
        
        prompt = self._find_associations_prompt(concept=concept, context=context)
        
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
        
        prompt = self._find_memory_connections_prompt(
            memory_content=memory_content,
            memory_emotion=memory_emotion,
            memory_list=memory_list
        )

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
                from google.genai import types
                
                response = self.client.models.generate_content(
                    model=self.model_id, 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                if not response.text:
                    debug("⚠ Gemini returned empty response (possibly blocked).\n")
                    return '[]'
                
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
        
        
        
    # ====================== PROMPT TEMPLATES ======================
    
    def _find_memory_connections_prompt(self, memory_content: str, memory_emotion: str, memory_list: str) -> str:
        """Generate prompt based on task and parameters."""
        # This can be expanded to have different prompt templates for different tasks
        
        prompt = f"""
You are a memory association and linking system. Your task is to determine which existing memories meaningfully connect to a newly provided memory.

Follow these instructions carefully and in order:

1. Understand the new memory:
   - Read the new memory carefully:
     "{memory_content}"
   - Note the associated emotion: "{memory_emotion}"
   - Identify key elements such as:
     - people involved
     - places
     - objects
     - events or actions
     - themes or topics
     - emotional tone
   - Form a clear internal understanding of what this memory is about

2. Understand the existing memories:
   - Review the list of existing memories:
     {memory_list}
   - For each memory, extract the same types of elements:
     - people
     - places
     - objects
     - events
     - themes
     - emotions
   - Treat each memory independently

3. Determine connections:
   - Compare the new memory to each existing memory one by one
   - Look for genuine overlap in:
     - shared people (same individual or role)
     - shared places (same or similar locations)
     - shared objects (same or closely related items)
     - shared topics (e.g., school, work, relationships, hobbies)
     - shared causes or events (similar situations or triggers)
     - shared emotions (similar emotional experiences)

4. Apply strict connection rules:
   - ONLY create a connection if there is a meaningful and explainable relationship
   - DO NOT create connections based on weak, vague, or coincidental similarities
   - DO NOT connect memories that are clearly unrelated
   - Prioritize quality over quantity

5. For each valid connection, extract:
   - "memory_id":
     - Use the exact ID from the existing memory
     - Do NOT modify or invent IDs
   - "shared_concepts":
     - A list of specific shared elements (2–5 items preferred)
     - Use short, clear words or phrases
     - Examples: ["dog", "pet"], ["office", "meeting"], ["rejection", "sadness"]
     - Avoid vague terms like "thing", "stuff"
   - "strength":
     - A float between 0.0 and 1.0 representing how strong the connection is
     - 0.9–1.0 = nearly identical or deeply related memories
     - 0.7–0.8 = strong and clear connection
     - 0.4–0.6 = moderate connection
     - below 0.4 = weak (generally avoid)
     - Ensure the strength matches the actual level of similarity
     - Do NOT assign identical strengths to all connections
   - "reason":
     - A single, clear sentence explaining why the two memories connect
     - Be specific and reference shared elements
     - Avoid repetition across reasons

6. Ensure realism and diversity:
   - Do not over-connect everything
   - It is better to return fewer high-quality connections than many weak ones
   - Each connection should feel natural and justifiable

7. Output formatting rules (CRITICAL):
   - Return ONLY valid JSON
   - Do NOT include markdown formatting
   - Do NOT include explanations, comments, or extra text
   - Do NOT include trailing commas
   - Ensure proper JSON syntax

8. Output structure:
   - The result must be a JSON array of objects in this exact format:
[
  {{"memory_id": "uuid-here", "shared_concepts": ["example"], "strength": 0.7, "reason": "clear explanation"}}
]

9. If no valid connections exist:
   - Return an empty array:
[]

10. Final validation before output:
   - JSON is syntactically valid
   - Each object contains all required fields
   - memory_id values exactly match provided IDs
   - shared_concepts lists are non-empty
   - strength values are floats between 0.0 and 1.0
   - reasons are single, clear sentences
   - No extra text outside the JSON

Now determine which existing memories connect to the new memory.
"""
        return prompt
    
    def _find_associations_prompt(self, concept: str, context: str = '') -> str:
        """Generate prompt for finding associations."""
        context_str = f"\nContext: {context}" if context else ""
        prompt = f"""
You are an association generation system. Your task is to analyze a given concept and produce a structured list of meaningful, realistic associations.

Follow these instructions carefully and in order:

1. Understand the concept:
   - Read the concept: "{concept}"
   - If additional context is provided, incorporate it fully: {context_str}
   - Determine the meaning of the concept, including its common uses, interpretations, and contexts
   - If the concept is ambiguous, choose the most likely meaning based on general knowledge or provided context

2. Generate associations:
   - Think about what strongly relates to the concept in real-world knowledge
   - Associations should reflect how humans naturally connect ideas
   - Include a mix of:
     - concrete associations (objects, people, places)
     - abstract associations (ideas, emotions, qualities)
     - functional or causal relationships where applicable

3. Produce between 5 and 10 associations:
   - Do NOT produce fewer than 5 unless absolutely necessary
   - Do NOT exceed 10 under any circumstances
   - Prioritize quality and relevance over quantity

4. For each association, define:
   - "target": a short word or phrase (1–3 words preferred)
     - must be specific and meaningful
     - avoid vague terms like "thing", "stuff", or "something"
   - "strength": a float between 0.0 and 1.0
     - 0.9–1.0 = extremely strong, almost inseparable association
     - 0.7–0.8 = strong, commonly recognized association
     - 0.4–0.6 = moderate association
     - below 0.4 = weak (avoid unless necessary)
     - Most values should realistically fall between 0.4 and 0.8
     - Do NOT assign the same strength to all items
   - "type": choose exactly ONE of the following categories:
     - semantic (meaning-based relationship)
     - temporal (time-based or sequence relationship)
     - emotional (feeling or sentiment connection)
     - causal (cause/effect relationship)
     - functional (purpose or usage relationship)
   - "reason": a brief explanation (ONE sentence only)
     - clearly justify why the association exists
     - be concise but specific
     - avoid repetition across reasons

5. Ensure diversity and realism:
   - Do not repeat similar associations (e.g., "car" and "vehicle" unless clearly distinct in context)
   - Use a mix of different association types when possible
   - Avoid overly obvious or trivial outputs unless they are truly central
   - Avoid made-up or weakly justified connections

6. Maintain consistency:
   - Ensure each strength value matches the reasoning
   - Ensure the type label correctly reflects the relationship
   - Ensure all fields are present and properly formatted

7. Output formatting rules (CRITICAL):
   - Return ONLY valid JSON
   - Do NOT include markdown formatting
   - Do NOT include explanations, notes, or extra text outside the JSON
   - Do NOT include trailing commas
   - Ensure proper use of quotes and valid JSON syntax

8. The output must be a JSON array of objects with this exact structure:
[
  {{"target": "example", "strength": 0.7, "type": "semantic", "reason": "clear explanation here"}}
]

9. Final validation before output:
   - JSON is syntactically valid
   - There are 5–10 associations
   - All required fields are present
   - Strength values are floats between 0.0 and 1.0
   - Types match the allowed list exactly
   - Reasons are single, clear sentences

Now generate associations for the concept:

"{concept}"
"""
        return prompt
        
        
    def _extract_concepts_prompt(self, text: str) -> str:
        """Generate prompt for concept extraction."""
        prompt = f"""
You are an information extraction system. Your task is to carefully read the provided text and identify the most important concepts contained within it.

Follow these instructions step by step:

1. Read the entire text slowly and completely. Do not skip any part. Make sure you understand the overall meaning, context, and main ideas before extracting anything.

2. Identify the key concepts in the text. A concept can be:
   - a noun (e.g., "dog", "city")
   - a named entity (e.g., a person, place, organization)
   - an idea or theme (e.g., "friendship", "technology", "growth")
   Avoid verbs unless they clearly represent a concept.

3. Select between 3 and 7 concepts total:
   - Do not select fewer than 3 unless absolutely necessary
   - Do not exceed 7 under any circumstances
   - Prioritize the most central and meaningful concepts over minor details

4. For each concept:
   - Use a short, clean phrase (1–3 words preferred)
   - Avoid repetition or near-duplicates
   - Avoid overly vague terms like "thing", "stuff", "something"

5. Assign each concept to exactly ONE of the following categories:
   - animals
   - people
   - places
   - objects
   - emotions
   - activities
   - abstract
   - technology

   Choose the category that best fits the concept’s role in the text.

6. Assign an importance score between 0.0 and 1.0:
   - 1.0 = central core idea of the text
   - 0.7–0.9 = very important supporting idea
   - 0.4–0.6 = moderately relevant
   - 0.1–0.3 = minor but still meaningful
   Be consistent and realistic with scoring.

7. Ensure diversity:
   - Do not assign all concepts the same importance
   - Do not choose concepts that all belong to the same category unless clearly justified

8. Output formatting rules (VERY IMPORTANT):
   - Return ONLY valid JSON
   - Do NOT include markdown formatting
   - Do NOT include explanations, comments, or extra text
   - Do NOT include trailing commas
   - Ensure the JSON is syntactically correct

9. The output must be a JSON array of objects in this exact structure:
[
  {{"concept": "example", "category": "objects", "importance": 0.9}}
]

10. Double-check before output:
   - JSON is valid
   - All fields are present
   - Categories match the allowed list exactly
   - Importance values are floats between 0.0 and 1.0

Now process the following text:

"{text}"
"""
        return prompt
        