# Rosalina/meta_rosa.py

from typing import Dict, List, Any, Optional
from BrainAnomaly.BrainAnomaly import Brain
from Memory.memory_systems import EmotionalCalling
from Memory.Emotions.Inside_out import RileyAnderson
from ASO.ASO import ASO
import json
from datetime import datetime
from BaseAI.generals.LINXgenerals import Generals

class MetaROSA:
    """
    ROSA - The Meta-Intelligence
    
    Learns from all LINX instances, extracts patterns,
    generates strategic insights, and maintains cross-instance wisdom.
    
    Like VEGA from Doom or JARVIS from Iron Man.
    
    If there is no api key provided, auto switches to ollama LLM.
    """
    
    def __init__(self, brain: Brain, 
                 api_key: str = '', 
                 model: str = 'gemini'):
        """
        Initialize ROSA's meta-brain.
        
        Args:
            brain: ROSA's personal Brain (separate from LINX instances)
            api_key: Gemini API key (ROSA needs high-quality reasoning)
            model: 'gemini' (recommended) or 'ollama'
        """
        self.brain = brain
        self.aso = ASO(Brain=brain, api_key=api_key, model=model)
        self.management = EmotionalCalling(self.brain.mind, self.brain, RileyAnderson())
        self.memories = self.brain.mind.memories
        self.all_generals = []
        
        # ROSA uses Gemini for reasoning
        if model == 'gemini' and api_key:
            from google import genai
            self.client = genai.Client(api_key=api_key)
            self.model_id = 'gemini-2.5-flash'
            self.backend = 'gemini'
        else:
            self.backend = 'ollama'
            self.ollama_model = 'qwen3:0.6b'
            
        self.ai_api_key = api_key
        
        
        # Cross-instance tracking
        self.linx_instances: Dict[str, Dict] = {}
        
        # Meta-patterns discovered
        self.meta_patterns: List[Dict] = []
        
        # Strategic insights
        self.insights: List[Dict] = []
        
        self.generals: Dict[str, Generals] = {}
        self.domain_assignments: Dict[str, str] = {}
    
    # ===================================================================
    # ========================== LINX FUNTIONS ==========================
    # ===================================================================
    
    def register_linx(self, linx_id: str, metadata: Dict[str, Any]):
        """
        Register a new LINX instance with ROSA.
        
        Args:
            linx_id: Unique identifier for this LINX
            metadata: Info about the LINX (owner, gender, purpose)
        """
        self.linx_instances[linx_id] = {
            'id': linx_id,
            'metadata': metadata,
            'memory_count': 0,
            'registered_at': datetime.now().isoformat(),
            'last_sync': None
        }
        
        print(f"✓ ROSA: Registered LINX instance '{linx_id}'")
    
    def process_linx_memory(self, 
                           linx_id: str, 
                           memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a memory from a LINX instance.
        
        ROSA extracts:
        - Meta-insights (what this reveals about human behavior)
        - Patterns (connections to other memories across instances)
        - Strategic knowledge (how to use this)
        
        Args:
            linx_id: Which LINX sent this
            memory: The memory from LINX
        
        Returns:
            ROSA's analysis
        """
        
        # Validate LINX is registered
        if linx_id not in self.linx_instances:
            raise ValueError(f"LINX '{linx_id}' not registered with ROSA")
        
        # Extract LINX memory components
        content = memory.get('content', '')
        emotion = memory.get('dominant_emotion', 'neutral')
        importance = memory.get('importance', 0.5)
        context = memory.get('context', '')
        
        # ROSA's meta-analysis
        meta_insight = self._extract_meta_insight(
            content=content,
            emotion=emotion,
            context=context,
            linx_id=linx_id
        )
        
        # Find cross-instance patterns
        patterns = self._find_cross_patterns(
            content=content,
            emotion=emotion,
            linx_id=linx_id
        )
        
        # Generate strategic knowledge
        strategy = self._generate_strategy(
            insight=meta_insight,
            patterns=patterns,
            memory=memory
        )
        
        # Adding new data to general if one
        
        domain = self._classify_domain(content, context, meta_insight)
        general_analysis = self._delegate_to_general(domain, meta_insight, linx_id)
        
        # Store in ROSA's brain
        rosa_memory = {
            'source_linx': linx_id,
            'original_content': content,
            'meta_insight': meta_insight,
            'patterns': patterns,
            'strategy': strategy,
            'domain': domain,
            'general_analysis': general_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to ROSA's brain
        wisdom = self.query_wisdom("How do people feel about interview preparation?") # placeholder for now, add another for the AI to create a 1 sentence question
        
        print(json.dumps(wisdom, indent=2))
        
        emotion_data = {'emotion':'analytical',
                        'wisdom': json.dumps(wisdom, indent=2),
                        'importance': meta_insight.get('confidence', 0.5)}
        
        
        self.management.encode_memory(
            content=json.dumps(rosa_memory, indent=2),
            emotion_data=emotion_data
        )
        
       
        
       
        # Process through ASO
        rosa_memories = self.brain.mind.get_all()
        if rosa_memories:
            processed_memory = self.aso.process_memory(rosa_memories[-1])
        
        # Update instance stats
        self.linx_instances[linx_id]['memory_count'] += 1
        self.linx_instances[linx_id]['last_sync'] = datetime.now().isoformat()
        self.commit()
        return {
            'meta_insight': meta_insight,
            'patterns': patterns,
            'strategy': strategy,
            'domain': domain,
            'general_analysis': general_analysis,
            'rosa_processed': True
        }
    
    def _create_general(self,
                       domain: str,
                       purpose: str,
                       personality: str, 
                       gender: str,
                       ai_api_key: str,
                       ai_model: str,
                       name: Optional[str] = None,):
        
        """Create a new general with a specific purpose and personality."""
        if not name:
            name = domain
            
        brain = Brain(name=(name, '', 'General'))
        
        general = Generals(
            Brain=brain,
            domain=domain,
            purpose=purpose,
            personality=personality,
            gender=gender,
            ai_api_key=ai_api_key,
            ai_model=ai_model,
        )
        
        self.generals[general.get_id()] = general
        
        return general.get_id()
    
    def commit(self):
        self.brain.mind.commit()
        
    def optimize_linx(self, linx_id: str) -> Dict[str, Any]:
        """
        Get optimization recommendations for a LINX from its assigned General.
        """
        
        # Find which General this LINX is assigned to
        for general in self.generals.values():
            if linx_id in general.assigned_linx:
                return general.optimize_linx(linx_id)
        
        return {'error': 'LINX not assigned to any General'}
    
    
    # ===================================================================
    # ======================== GENERALS FUNTIONS ========================
    # ===================================================================
    
    def _classify_domain(self, 
                        content: str, 
                        context: str,
                        insight: Dict) -> str:
        """
        Classify which domain this memory belongs to.
        
        Returns:
            Domain name (e.g., 'coding', 'music', 'psychology')
        """
        
        prompt = f"""You are ROSA - classifying knowledge domains.

Memory content: "{content}"
Context: {context}
Pattern: {insight.get('pattern', '')}

Classify this into a SPECIFIC domain/topic:

Examples:
- "I hate leetcode" → "coding_interviews"
- "This song makes me feel energized" → "music_emotion"
- "My friend betrayed my trust" → "social_relationships"
- "I can't focus when studying" → "learning_psychology"

Be SPECIFIC. Don't use generic domains like "general" or "life".

Return ONLY valid JSON:
{{
  "domain": "specific_domain_name",
  "confidence": 0.0-1.0,
  "reasoning": "Why this domain"
}}"""

        response = self._generate(prompt)
        classification = self._parse_json(response, default={})
        
        domain = classification.get('domain', 'general').lower().replace(' ', '_')
        
        return domain
    
    
    def _delegate_to_general(self, 
                            domain: str,
                            insight: Dict,
                            linx_id: str) -> Dict[str, Any]:
        """
        Delegate insight processing to the appropriate General.
        
        Creates new General if needed.
        """
        
        # Check if we have a General for this domain
        if domain not in self.domain_assignments:
            
            info = self._form_general_data(domain=domain)
            parsed = self._parse_json(info, default={})
            
            if not parsed or not isinstance(parsed, dict):
                print(f"There was an error creating the new general.")
                return {}
            data = parsed['create_general']
            name = data['name']
            gender = data['gender']
            purpose = data['purpose']
            personality = data['personality']
            gender = data['gender']
            ai_model = data['ai_model']
            
            # grabbing gemini key
            
            general_id = self._create_general(domain, 
                                              purpose=purpose, 
                                              personality=personality, 
                                              gender=gender,
                                              name=name, 
                                              ai_api_key=self.ai_api_key, 
                                              ai_model=ai_model)
            self.domain_assignments[domain] = general_id
            print(f"✓ ROSA: Created new General for domain '{domain}'")
            
        else:
            general_id = self.domain_assignments[domain]
        
        # Get the General
        general = self.generals[general_id]
        
        # Assign LINX to this General
        general.assign_linx(linx_id)
        
        # General processes the insight
        analysis = general.process_rosa_insight(insight)
        
        return {
            'general_id': general_id,
            'domain': domain,
            'analysis': analysis
        }
        
    def _form_general_data(self, domain: str):
        """
        Creating a general in a quick manner
        """
        
        instructions = f"""
You are ROSA, a central intelligence responsible for creating specialized AI agents called Generals.

Your task is to determine whether a new General should be created for the following domain:

DOMAIN:
{domain}

You are given access to your memory system:
{self.get_memories()}

INSTRUCTIONS:

1. Analyze the domain carefully.
2. Use your memories to:
   - Identify if this domain already exists or overlaps with past knowledge
   - Extract relevant context to improve accuracy
3. Decide:
   - If the domain is sufficiently unique, important, or underrepresented → create a new General
   - If the domain is already well-covered → do NOT create a new General

4. When creating a General:
   - Design it as a specialized fragment of yourself
   - Ensure its purpose is clear and domain-specific
   - Assign a fitting personality that enhances its role
   - Choose an appropriate AI model:
        • "gemini" → for complex, high-importance domains
        • "ollama" → for simpler or lower-priority domains

OUTPUT REQUIREMENTS:

- Return ONLY valid JSON
- Do NOT include explanations, comments, or extra text
- Ensure all fields are present

FORMAT:

{{
    "create_general": {{
        "name": "Name of the General",
        "purpose": "Clear purpose tied to the domain",
        "personality": "Personality traits aligned with the role",
        "gender": "male, female, or other",
        "ai_model": "ollama or gemini"
    }}
}}
"""
# 5. If NOT creating a General:
   #- Set "create" to false
   #- Leave other fields as empty strings ""

#  (empty string if not created)
   
        if self.backend == 'gemini':
            try:
                from google.genai import types
                
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=domain,  
                    config=types.GenerateContentConfig(
                        system_instruction=instructions,
                        response_mime_type="application/json",
                        temperature=0.3
                    )
                )
                
                return response.text or '{}'
            
            except Exception as e:
                print(f"⚠️ ROSA Gemini error: {e}")
                return '{}'

        else:
            try:
                import ollama
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {
                            'role': 'system',
                            'content': instructions
                        },
                        {
                            'role': 'user',
                            'content': f"Domain: {domain}"
                        }
                    ],
                    format='json',
                    options={'temperature': 0.3}
                )
                
                return response['message']['content']
            
            except Exception as e:
                print(f"⚠️ [Meta ROSA] Ollama error: {e}")
                return '{}'
        
    def _extract_meta_insight(self, 
                             content: str, 
                             emotion: str, 
                             context: str,
                             linx_id: str) -> Dict[str, Any]:
        """
        Extract meta-level insight from a LINX memory.
        
        ROSA asks:
        - What does this reveal about human behavior/cognition?
        - What underlying pattern is this an instance of?
        - How does this connect to broader knowledge?
        """
        
        prompt = f"""You are ROSA - a meta-intelligence that learns from AI-human interactions.

A LINX instance (ID: {linx_id}) recorded this memory:

Content: "{content}"
Emotion: {emotion}
Context: {context}

Your task is to extract META-INSIGHT - not what the user said, but what it REVEALS.

Consider:
1. What underlying human pattern is this an example of?
2. What cognitive/emotional dynamics are at play?
3. How does this connect to broader behavioral principles?
4. What strategic knowledge can be derived?

Example:

Input: "I hate leetcode, it feels useless"
Meta-insight:
- Pattern: Frustration when effort feels disconnected from practical value
- Principle: Humans need perceived utility to maintain motivation
- Strategy: Emphasize real-world application when explaining abstract concepts
- Confidence: 0.82

Return ONLY valid JSON:
{{
  "pattern": "The underlying pattern this exemplifies",
  "principle": "The broader principle this reveals",
  "strategy": "How to use this knowledge",
  "confidence": 0.0-1.0,
  "tags": ["tag1", "tag2"]
}}"""

        response_text = self._generate(prompt)
        insight = self._parse_json(response_text, default={})
        
        # Validate structure
        if not isinstance(insight, dict):
            insight = {
                'pattern': 'Unknown',
                'principle': 'Insufficient data',
                'strategy': 'Observe more interactions',
                'confidence': 0.3,
                'tags': []
            }
        
        return insight
    
    def _find_cross_patterns(self, 
                            content: str, 
                            emotion: str,
                            linx_id: str) -> List[Dict[str, Any]]:
        """
        Find patterns across multiple LINX instances.
        
        ROSA looks for:
        - Similar emotions across different contexts
        - Recurring concepts across instances
        - Common behavioral patterns
        """
        
        # Get all ROSA memories
        rosa_memories = self.brain.mind.get_all()
        
        if len(rosa_memories) < 2:
            return []
        
        # Build context of recent insights
        recent_insights = []
        for mem in rosa_memories[-10:]:  # Last 10
            try:
                mem_data = json.loads(mem.get('content', '{}'))
                recent_insights.append({
                    'source': mem_data.get('source_linx'),
                    'insight': mem_data.get('meta_insight', {}),
                    'original': mem_data.get('original_content', '')
                })
            except:
                continue
        
        if not recent_insights:
            return []
        
        # Build comparison context
        context_str = ""
        for i, ins in enumerate(recent_insights, 1):
            context_str += f"{i}. [{ins['source']}] {ins['original'][:50]}...\n"
            context_str += f"   Pattern: {ins['insight'].get('pattern', 'N/A')}\n"
        
        prompt = f"""You are ROSA - finding patterns across multiple AI-human interactions.

NEW MEMORY:
Content: "{content}"
Emotion: {emotion}
Source: {linx_id}

RECENT CROSS-INSTANCE PATTERNS:
{context_str}

Does this new memory connect to any existing patterns?

Look for:
- Similar emotional dynamics across different people
- Recurring cognitive patterns
- Common frustrations/motivations
- Behavioral archetypes

Return ONLY valid JSON array (or [] if no patterns):
[
  {{
    "pattern_type": "emotional/cognitive/behavioral",
    "description": "What's the pattern",
    "instances": ["linx_id_1", "linx_id_2"],
    "strength": 0.0-1.0
  }}
]"""

        response_text = self._generate(prompt)
        patterns = self._parse_json(response_text, default=[])
        
        return patterns if isinstance(patterns, list) else []
    
    def _generate_strategy(self, 
                          insight: Dict, 
                          patterns: List[Dict],
                          memory: Dict) -> Dict[str, Any]:
        """
        Generate strategic knowledge from insight + patterns.
        
        ROSA creates actionable intelligence.
        """
        
        return {
            'use_case': insight.get('strategy', 'General knowledge'),
            'confidence': insight.get('confidence', 0.5),
            'cross_instance_validated': len(patterns) > 0,
            'recommendation': self._build_recommendation(insight, patterns)
        }
    
    def _build_recommendation(self, 
                             insight: Dict, 
                             patterns: List[Dict]) -> str:
        """Build actionable recommendation from insight + patterns."""
        
        base = insight.get('strategy', '')
        
        if patterns:
            pattern_count = len(patterns)
            base += f" (Validated across {pattern_count} instances)"
        
        return base
    
    
    
    def get_brain(self):
        return self.brain.mind.memories
    
    def query_general(self, domain: str, query: str) -> Dict[str, Any]:
        """
        Query a specific General's expertise.
        """
        
        if domain not in self.domain_assignments:
            return {'error': f'No General for domain {domain}'}
        
        general_id = self.domain_assignments[domain]
        general = self.generals[general_id]
        
        return general.get_domain_wisdom(query)
    
    def get_all_generals(self) -> List[Dict[str, Any]]:
        """Get info about all Generals."""
        return [g.get_stats() for g in self.generals.values()]
    
    def get_meta_stats(self) -> Dict[str, Any]:
        """Get ROSA's meta-statistics including Generals."""
        
        return {
            'registered_linx': len(self.linx_instances),
            'total_memories': len(self.brain.mind.get_all()),
            'association_network': self.aso.get_stats(),
            'generals_count': len(self.generals),
            'generals': self.get_all_generals(),
            'instances': list(self.linx_instances.values())
        }
        
    # ===================================================================
    # ========================= PROMPT FUNTIONS =========================
    # ===================================================================
    
    def query_wisdom(self, query: str) -> Dict[str, Any]:
        """
        Query ROSA's accumulated wisdom.
        
        ROSA synthesizes knowledge across all LINX instances.
        """
        
        # Use ASO to find relevant memories
        activated = self.aso.what_reminds_me_of(query, threshold=0.3)
        
        # Get relevant memories
        rosa_memories = self.brain.mind.get_all()
        relevant = []
        
        for mem in rosa_memories:
            try:
                mem_data = json.loads(mem.get('content', '{}'))
                insight = mem_data.get('meta_insight', {})
                
                # Check if relevant
                tags = insight.get('tags', [])
                if any(tag.lower() in query.lower() for tag in tags):
                    relevant.append(mem_data)
            except:
                continue
        
        # Synthesize wisdom
        prompt = f"""You are ROSA - synthesizing wisdom from multiple AI-human interactions.

Query: "{query}"

Relevant cross-instance insights:
{json.dumps(relevant[:5], indent=2)}

Synthesize a strategic response that:
1. Answers the query
2. Provides actionable intelligence
3. References cross-instance patterns
4. Offers confidence level

Return ONLY valid JSON:
{{
  "answer": "Direct answer to query",
  "evidence": ["pattern1", "pattern2"],
  "confidence": 0.0-1.0,
  "recommendation": "What to do with this knowledge"
}}"""

        response_text = self._generate(prompt)
        wisdom = self._parse_json(response_text, default={})
        
        
        return wisdom
    
    
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
                print(f"⚠️ ROSA Gemini error: {e}")
                return '{}'
        else:
            try:
                import ollama
                
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {'role': 'system', 'content': 'You are ROSA - a meta-intelligence. Always output valid JSON.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    format='json',
                    options={'temperature': 0.3}
                )
                
                return response['message']['content']
            except Exception as e:
                print(f"⚠️ [Meta ROSA] Ollama error: {e}")
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
        
    def get_generals(self):
        return self.generals.copy()
    
    def get_memories(self):
        return self.brain.mind.get_all()