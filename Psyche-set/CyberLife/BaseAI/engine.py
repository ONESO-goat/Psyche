# engine.py - chatgpt gave me this file but I believe i should go with the Rosa class, not sure

from typing import Protocol
from BrainAnomaly.BrainAnomaly import Brain
from Memory.Emotions.Headquarters import Headquarters
from Memory.Emotions.Inside_out import RileyAnderson
from love.friends import Amigo
from Memory.memory_systems import EmotionalCalling
import json
from typing import Any
from BaseAI.states import Rationlized, Operator, System, Agent
from debugging_utils import debug, reset_debug, hashtag




class BaseAI:
    def __init__(self, Brain, model="ollama"):
        self.Brain = Brain
        self.riley = RileyAnderson()
        self.management = EmotionalCalling(self.Brain.mind, self.Brain, RileyAnderson())
        self.HQ = Headquarters(memories=self.Brain.mind.get_all(), Brain=self.Brain)
        self.friends = Amigo(name='friends', Brain=self.Brain)

        self.backend = model
        self.initialized = False

        # Shared states
        self.RATIONAILZED = Rationlized()
        self.OPERATOR = Operator()
        self.SYSTEM = System()
        self.AGENT = Agent()

        self.rdota = 'normal'
        
     def _generate(self, prompt: str, name:str='') -> str:
        """Generate response from AI backend with persistent ROSA persona."""
    
    # Construct the message history with the system prompt at the top
        messages = [
        {'role': 'system', 'content': self.the_prompt},
        {'role': 'user', 'content': prompt}
    ]
        
        if self.backend == 'gemini':
            try:
                from google.genai import types
                
                # For Gemini, we convert the messages to their content format
                # Note: Gemini 2.0+ handles system_instruction separately
                
                response = self.client.models.generate_content(
                    model=self.model_id, 
                    contents=prompt, # Or pass the whole history
                    config=types.GenerateContentConfig(
                        system_instruction=self.the_prompt, # Best way for Gemini
                        #response_mime_type="application/json"
                    )
                )
                
                return response.text or '[]'
            except Exception as e:
                print(f"⚠️ Gemini error: {e}")
                return '[]'
        
        else:  # Ollama
            try:
                import ollama
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=messages, # Now includes ROSA system prompt
                    #format='json',
                    options={'temperature': 0.2}
                )
                return response['message']['content']
                
            except Exception as e:
                print(f"⚠️ Ollama error: {e}")
                return '[]'
            
    def what_you_learn(self, limit: int = 5) -> dict[str, str | list[str]]:
        """Return structured memory context with prioritization."""

        memories = self.Brain.recall_all()

        # Sort by importance (and optionally timestamp later)
        memories = sorted(memories, key=lambda x: x.get("importance", 0), reverse=True)

        # Limit number of memories
        selected_memories = memories[:limit]

        memory_context = ''
        memory_context_list = []

        for index, memory in enumerate(selected_memories, start=1):
            context = memory.get('content', '')
            learn = memory.get('what_was_learned_from_this', '')
            dominant_emotion = memory.get('dominant_emotion', '')
            importance = memory.get('importance', 0)
            timestamp = memory.get('timestamp', '')

            text = f"""
    ====================================

    Memory {index}:

    Context:
    {context}

    What you learned:
    {learn}

    Dominant emotion:
    {dominant_emotion}

    Importance score:
    {importance}

    Timestamp:
    {timestamp}

    ====================================
    """

            memory_context += text
            memory_context_list.append(text.strip())

        return {
            'context': memory_context.strip(),
            'list': memory_context_list
        }     
        
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
        
            
    
    def _generate_quick_summary(self, user: str, ai: str):
        """Generate response from AI backend with persistent ROSA persona."""
    
    # Construct the message history with the system prompt at the top
        messages = f"""
        role = system: content: {ai}
        
        role = user: content: {user}
        """.strip()
        
        instructions = self._summary_instructions()
        
        if self.backend == 'gemini':
            try:
                from google.genai import types
                
                
                # For Gemini, we convert the messages to their content format
                # Note: Gemini 2.0+ handles system_instruction separately
                response = self.client.models.generate_content(
                    model=self.model_id, 
                    contents=messages, # Or pass the whole history
                    config=types.GenerateContentConfig(
                        system_instruction=instructions, # Best way for Gemini
                        response_mime_type="application/json"
                    )
                )
                
                import json
                return json.loads(response.text) if response.text else {}
            
            except Exception as e:
                print(f"⚠️ Gemini error: {e}")
                return {'summary': '', 'emotion': '', 'what_was_learned': '', 'importance': ''}
        
        else:  # Ollama
            try:
                import ollama
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[{'role': 'system', 'content':instructions},
                            {'role': 'user', 'content': user},
                            {'role': 'ai', 'content': ai}], # Now includes ROSA system prompt
                    #format='json',
                    options={'temperature': 0.2}
                )
                import json
                try:
                    return json.loads(response['message']['content'])
                except Exception:
                    return {"summary": response['message']['content'], "emotion": "", "what_was_learned": ""}
            except Exception as e:
                print(f"⚠️ Ollama error: {e}")
                return {'summary': '', 'emotion': '', 'what_was_learned': '', 'importance': ''}

    def define_memory(self, user_input: str, repsonse: str):
        
        summary = self._generate_quick_summary(user=user_input, ai=repsonse)
        
        content = summary['summary']
        
        emotion = summary['emotion']
        
        learnt = summary['what_was_learned']
        
        importance = summary['importance']
        
        dic = { 'emotion': emotion, 'rosa_lesson': learnt, 'importance': importance}
        
        self.add(content=content, emotion_data=dic)
        
        return dic
    
    def update_states(self) -> None:
        self.rational_state = self.RATIONAILZED.get_scale_factor()
        self.operator_state = self.OPERATOR.get_scale_factor()
        self.agent_state = self.AGENT.get_scale_factor()
        self.system_state = self.SYSTEM.get_scale_factor()
        
    
    def add(self, content:str, emotion_data: dict) -> None:
        self.management.encode_memory(content, emotion_data)
        self.commit()

    def commit(self):
        self.Brain.mind.commit()
        
    def get_whole_brain(self) -> Brain:
        return self.Brain.mind.achieve()
    
    def get_memories(self) -> dict:
        return self.Brain.mind.get_all()
    
    # ============== GO ==============
    def go_normal(self) -> None:
        self.rdota = 'normal'
        
    def go_rationalized(self) -> None:
        self.rdota = 'rationalized'
    
    def go_operator(self) -> None:
        self.rdota = 'operator'
    
    def go_system(self) -> None:
        self.rdota = 'system'
    
    def go_agent(self) -> None:
        self.rdota = 'agent'