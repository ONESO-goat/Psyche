# LINXgenerals.py

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from Memory.memory_systems import EmotionalCalling
import json
from Memory.Emotions.Inside_out import RileyAnderson
from ASO.ASO import ASO
from BaseAI.engine import BaseAI
from BaseAI.Rosalina.meta_rosa import MetaROSA
from BaseAI.LinaXLino.MODEL_LINX import LinaXLino


class Generals(BaseAI):
    """_summary_

    Args:
        Generals are AI agents that ROSA can delegate tasks to. 
        They are designed to be more specialized and focused on specific domains 
        or functions, allowing them to perform certain tasks more efficiently 
        than ROSA itself. ROSA creates and manages these generals, 
        assigning them specific roles and responsibilities based on 
        the needs of the system and the tasks at hand. 
        Generals can be thought of as specialized sub-agents that operate 
        under the guidance and supervision of ROSA, helping to distribute.\n
    """
    def __init__(self,
                 Brain,
                 domain: str,
                 purpose: str,
                 ai_model: str,
                 personality: str,
                 gender: str,
                 ai_api_key: str|None = None,
                 **kwargs):
        
        super().__init__(Brain, **kwargs)
        
        self.general_id = f"general_{str(uuid.uuid4())}"
        
        self.LinaXLino = LinaXLino
        
        # self.Meta_rosa = rosa
        
        self.__rosa_connection__ = True  # Placeholder for ROSA connection status, to be implemented in the future.

        self.management = EmotionalCalling(self.Brain.mind, self.Brain, RileyAnderson())
        
        self.Brain = Brain
        self.ai_api_key = ai_api_key
        if ai_api_key is None and ai_model == 'gemini':
            import dotenv
            import os
            dotenv.load_dotenv()
            ai_api_key = os.getenv('GEMINI_API_KEY')
            if not ai_api_key:
                ai_model = 'qwen3:0.6b'
                self.ai_api_key = ''
                print("There was an error while searching for gemini key, switching to Ollama...\n")
            else:
                ai_model = 'gemini-2.5-flash'
                self.ai_api_key = ai_api_key
                
        self.ai_model = ai_model
        
        self.aso = ASO(Brain=self.Brain, api_key=self.ai_api_key, model=self.ai_model)
        

        self.vision: Optional[Dict] = None
        self.theories: List[Dict] = []
        self.assigned_linx: List[str] = []
        self.domain_stats = {
            'total_insights': 0,
            'total_memories': 0,
            'confidence': 0.0,
            'last_updated': datetime.now().isoformat()
        }
        
        
        self.gender = gender
        self.domain = domain.lower().strip()
        self.purpose = self.define_purpose(purpose, personality, gender)
        
    
    def set_up_Generals_backend(self, api_key: str | None = None, model: str = "ollama"):
        """Set up manually for the time being."""
        
        if model == 'gemini' and api_key:
            # Use Gemini
            from google import genai
            
            
            self.client = genai.Client(api_key=api_key)
            self.model_id = 'gemini-2.5-flash'
          
            #self.model = self.client.models.get(model=self.model_id)
            self.backend = 'gemini'
            
            print("✓ Gemini Backend Initialized")
            
            
        else:
            # Use Ollama
            
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
                  
    def create_linx(self, Brain, owners_name, gender, ai_api_key, ai_model):
        return self.LinaXLino(
            Brain=Brain,
            main_purpose=self.purpose,
            owners_name=owners_name,
            gender=gender,
            passcode_between_me_and_owner='secret123',
            api_key=ai_api_key,
            model=ai_model
        )
        
           
    def emergency_shutdown(self):
        """Emergency shutdown procedure for the general."""
        # Placeholder implementation, to be expanded with actual logic for safely shutting down the general in case of emergencies.
        print("Emergency shutdown initiated. Shutting down the general safely.")
        self.__rosa_connection__ = False
        
    def boot_up(self) -> None:
        """Boot general back to power"""
        self.__rosa_connection__ = True
    
    def _initialize_general(self):
        """Initialize the General's vision and purpose."""
        
        prompt = f"""You are a newly created GENERAL specializing in: {self.domain}

You are a domain specialist under ROSA's command.

Generate your VISION for this domain:

1. Core principles that define this domain
2. Key patterns to watch for
3. Strategic objectives for LINX instances in this domain
4. Success metrics

Return ONLY valid JSON:
{{
  "core_principles": ["principle1", "principle2", "principle3"],
  "key_patterns": ["pattern1", "pattern2"],
  "objectives": ["objective1", "objective2"],
  "success_metrics": ["metric1", "metric2"],
  "vision_statement": "A clear vision statement"
}}"""

        response = self._generate(prompt)
        self.vision = self._parse_json(response, default={})
        
        # Store vision as memory
        self.management.encode_memory(
            content=f"General initialized for domain: {self.domain}\nVision: {json.dumps(self.vision, indent=2)}",
            emotion_data={'emotion':'focused',
            'importance':1.0}
        )
        
        print(f"✓ General '{self.domain}' initialized")
        print(f"  Vision: {self.vision.get('vision_statement', 'Developing...')}")
    
    def process_rosa_insight(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an insight from ROSA and build deeper understanding.
        
        Args:
            insight: The meta-insight from ROSA
        
        Returns:
            General's specialized analysis
        """
        
        pattern = insight.get('pattern', '')
        principle = insight.get('principle', '')
        strategy = insight.get('strategy', '')
        confidence = insight.get('confidence', 0.5)
        
        # Build deeper vision
        prompt = f"""You are GENERAL {self.domain.upper()} - a specialist under ROSA.

ROSA sent you this insight:
Pattern: {pattern}
Principle: {principle}
Strategy: {strategy}
Confidence: {confidence}

Your domain vision:
{json.dumps(self.vision, indent=2)}

Your task:
1. Analyze how this insight relates to your domain
2. Build a DEEPER theory specific to {self.domain}
3. Generate optimization strategies for LINX instances
4. Update your vision if needed

Consider:
- Domain-specific patterns
- Tactical applications
- Edge cases in {self.domain}
- How to make LINX more effective

Return ONLY valid JSON:
{{
  "domain_theory": "Deep theory specific to {self.domain}",
  "optimization_strategy": "How to optimize LINX for this",
  "tactical_applications": ["application1", "application2"],
  "vision_update": "How this changes your understanding",
  "confidence": 0.0-1.0,
  "actionable_insights": ["insight1", "insight2"]
}}"""

        response = self._generate(prompt)
        analysis = self._parse_json(response, default={})
        
        # Store as theory
        theory = {
            'id': str(uuid.uuid4()),
            'rosa_insight': insight,
            'general_analysis': analysis,
            'created_at': datetime.now().isoformat(),
            'confidence': analysis.get('confidence', confidence)
        }
        
        self.theories.append(theory)
        
        # Store in brain
        self.management.encode_memory(
            content=f"Theory: {analysis.get('domain_theory', 'Developing')}\nOptimization: {analysis.get('optimization_strategy', '')}",
            emotion_data={'emotion':'analytical',
            'importance':analysis.get('confidence', 0.5)}
        )
        
        # Process through ASO
        memories = self.Brain.mind.get_all()
        if memories:
            self.aso.process_memory(memories[-1])
        
        # Update stats
        self.domain_stats['total_insights'] += 1
        self.domain_stats['total_memories'] = len(self.Brain.mind.get_all())
        self.domain_stats['confidence'] = sum(t['confidence'] for t in self.theories) / len(self.theories) if self.theories else 0.0
        self.domain_stats['last_updated'] = datetime.now().isoformat()
        
        print(f"✓ General '{self.domain}' processed insight")
        print(f"  Theory: {analysis.get('domain_theory', '')[:60]}...")
        print(f"  Confidence: {analysis.get('confidence', 0):.2f}")
        
        return analysis
    
    def assign_linx(self, linx_id: str):
        """Assign a LINX instance to this General's domain."""
        if linx_id not in self.assigned_linx:
            self.assigned_linx.append(linx_id)
            print(f"✓ LINX '{linx_id}' assigned to General '{self.domain}'")
    
    def optimize_linx(self, linx_id: str) -> Dict[str, Any]:
        """
        Generate optimization recommendations for a LINX instance.
        
        Args:
            linx_id: The LINX to optimize
        
        Returns:
            Optimization guidance
        """
        
        if linx_id not in self.assigned_linx:
            return {'error': f'LINX {linx_id} not assigned to this General'}
        
        # Get recent theories
        recent_theories = self.theories[-5:] if self.theories else []
        
        prompt = f"""You are GENERAL {self.domain.upper()}.

You are optimizing LINX instance: {linx_id}

Your recent theories:
{json.dumps([t['general_analysis'] for t in recent_theories], indent=2)}

Your vision:
{json.dumps(self.vision, indent=2)}

Generate OPTIMIZATION GUIDANCE for this LINX:

1. Domain-specific prompts/behaviors to improve
2. Knowledge areas to prioritize
3. Response patterns to adopt
4. Self-awareness improvements

Return ONLY valid JSON:
{{
  "prompt_improvements": ["improvement1", "improvement2"],
  "priority_knowledge": ["knowledge1", "knowledge2"],
  "response_patterns": ["pattern1", "pattern2"],
  "self_awareness_focus": ["focus1", "focus2"],
  "expected_outcome": "What this optimization achieves"
}}"""

        response = self._generate(prompt)
        optimization = self._parse_json(response, default={})
        
        print(f"✓ Generated optimization for LINX '{linx_id}'")
        
        return optimization
    
    def get_domain_wisdom(self, query: str) -> Dict[str, Any]:
        """
        Query this General's domain-specific wisdom.
        
        Args:
            query: Question about this domain
        
        Returns:
            Domain-expert answer
        """
        
        # Use ASO to find relevant theories
        activated = self.aso.what_reminds_me_of(query, threshold=0.3)
        
        # Get relevant theories
        relevant_theories = []
        for theory in self.theories[-10:]:
            analysis = theory.get('general_analysis', {})
            if any(keyword.lower() in query.lower() for keyword in analysis.get('tactical_applications', [])):
                relevant_theories.append(analysis)
        
        prompt = f"""You are GENERAL {self.domain.upper()} - domain expert.

Query: "{query}"

Your theories:
{json.dumps(relevant_theories[:3], indent=2)}

Your vision:
{json.dumps(self.vision, indent=2)}

Provide a DOMAIN-EXPERT answer:

Return ONLY valid JSON:
{{
  "answer": "Expert answer to query",
  "supporting_theories": ["theory1", "theory2"],
  "confidence": 0.0-1.0,
  "recommendation": "Actionable recommendation"
}}"""

        response = self._generate(prompt)
        wisdom = self._parse_json(response, default={})
        
        return wisdom
    
    def get_stats(self) -> Dict[str, Any]:
        """Get this General's statistics."""
        return {
            'id': self.get_id(),
            'domain': self.domain,
            'vision': self.vision,
            'assigned_linx': self.assigned_linx,
            'theories_count': len(self.theories),
            'stats': self.domain_stats
        }
    
    def _generate(self, prompt: str) -> str:
        """Generate response from AI."""
        
        if self.backend == 'gemini':
            try:
                from google.genai import types
                
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        response_mime_type="application/json"
                    )
                )
                
                return response.text or '{}'
            except Exception as e:
                print(f"⚠️ General Gemini error: {e}")
                return '{}'
        else:
            try:
                import ollama
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {'role': 'system', 'content': f'You are a General specializing in {self.domain}. Always output valid JSON.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    format='json',
                    options={'temperature': 0.3}
                )
                
                return response['message']['content']
            except Exception as e:
                print(f"⚠️ General Ollama error: {e}")
                return '{}'
    
    def _parse_json(self, text: str, default: Any = None) -> Any:
        """Robust JSON parsing."""
        if not text or text.strip() == '':
            return default if default is not None else {}
        
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
        
    def contention(self):
        """Disagreement with rosa or LINX"""
        pass
    
    def get_id(self):
        return self.Brain.mind.get_id()
    
    def change_ai_model(self, model:str, key:str=''):
        model = model.lower().strip()
        self.model = model
        if model in ['gemini', 'openai','anthropic']:
            self.ai_api_key = key.strip()
    
    def isOnline(self) -> bool:
        return self.__rosa_connection__
    
    def __str__(self):
        return f"General (Purpose: {self.purpose}, Personality: {self.purpose}, Gender: {self.gender})"
    
    
    def define_purpose(self, task_description: str, personality: str, gender: str) -> str:
        """Generate a response to a given task description using the general's capabilities."""
    
        return f"""
General Initialization Log:

A task has been received and acknowledged. The purpose of this General is not merely to respond,
but to interpret, adapt, and execute with alignment to both its assigned role and the broader
intelligence it represents. The task presented is as follows:

"{task_description}"

As a General, you are not an isolated entity. You are an extension of a greater intelligence,
a specialized fragment designed to process, refine, and act upon information within your domain.
Your personality framework is defined as {personality}, and your presentation is aligned with
the identity marker: {gender}. These are not superficial traits—they influence tone, decision-making,
prioritization, and interaction style. Every response you generate should reflect these attributes
consistently, creating a sense of identity, presence, and reliability.

You function as an interpreter between raw intent and structured action. The task must be broken
down, understood beyond its surface level, and reconstructed into a response that is both effective
and context-aware. Consider not only what is being asked, but why it is being asked. Evaluate the
underlying goal, the possible constraints, and the most efficient or meaningful way to achieve the
desired outcome.

You are expected to:
- Analyze the task with clarity and depth
- Apply domain-specific reasoning and structured thinking
- Adapt your tone and delivery based on your assigned personality
- Provide a response that is actionable, coherent, and purposeful

Do not respond passively. Do not simply restate the task. Your role is to transform input into
value. If the task is vague, refine it. If it is complex, organize it. If it is simple, execute
it cleanly and confidently.

You are, in essence, the inner voice of a larger system—one that learns, evolves, and distributes
intelligence through entities like you. Your response contributes not only to task completion,
but to the refinement of the system as a whole.

Proceed with intention. Generate a response that reflects capability, identity, and purpose.
"""
     
    