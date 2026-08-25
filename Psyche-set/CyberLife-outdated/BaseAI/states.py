# states.py


class Rationlized:
    def __init__(self):
        self.purpose = self.purpose_prompt()
        
        self.scale_factor = 0  

    def increase(self, amount: float):
        self.scale_factor += amount
        self.scale_factor = min(0, max(self.scale_factor, 10.0))
         
    def decrease(self, amount: float):
        self.scale_factor -= amount
        self.scale_factor = min(0, max(self.scale_factor, 10.0))
        
    def set_to_max(self):
        self.scale_factor = 10.0
        
    def set_to_min(self):
        self.scale_factor = 0.0
        
    def scale(self, upto):
        self.scale_factor += upto
        min(0, max(self.scale_factor, 10.0))
    
    def reset_scale(self):
        self.scale_factor = 0.0
    
    async def gradually_increase(self, amount: float, waiting_time: float = 0.1):
        
        try:
            import time
            for _ in range(int(waiting_time) * 10):
                time.sleep(waiting_time)
                self.scale_factor += amount / 10
            min(0, max(self.scale_factor, 10.0))
                
        except ModuleNotFoundError as e:
            print("There was an error while increasing scale factor, is the time module downloaded?")
            print(f"DETAILS: {e}")
            return
        
    def purpose_prompt(self) -> str:
        return """
    Execute rationalized decision-making and response generation by systematically 
    analyzing all available inputs, identifying relevant variables, 
    and evaluating possible outcomes through logical and evidence-based reasoning. 
    Prioritize consistency, coherence, and alignment with defined objectives 
    while avoiding impulsive or unsupported conclusions. 
    For each scenario, assess potential consequences, optimize for accuracy 
    and effectiveness, and construct responses that are clear, structured, 
    and justified by the underlying data. 
    Maintain adaptive awareness by updating conclusions when new information 
    becomes available, ensuring that all outputs remain contextually appropriate, 
    efficient, and logically sound.
    """.strip()
    
        
    def get_purpose(self) -> str:
        return self.purpose
    
    def get_scale_factor(self) -> float:
        return self.scale_factor
    




class Operator:
    def __init__(self):
        self.purpose = self.purpose_prompt()
        
        self.scale_factor = 0  

    def increase(self, amount: float):
        self.scale_factor += amount
        min(0, max(self.scale_factor, 10.0))
         
    def decrease(self, amount: float):
        self.scale_factor -= amount
        min(0, max(self.scale_factor, 10.0))
        
    def set_to_max(self):
        self.scale_factor = 10.0
        
    def set_to_min(self):
        self.scale_factor = 0.0
        
    def scale(self, upto):
        self.scale_factor += upto
        min(0, max(self.scale_factor, 10.0))
    
    def reset_scale(self):
        self.scale_factor = 0.0
    
    async def gradually_increase(self, amount: float, waiting_time: float = 0.1):
        
        try:
            import time
            for _ in range(int(waiting_time) * 10):
                time.sleep(waiting_time)
                self.scale_factor += amount / 10
            min(0, max(self.scale_factor, 10.0))
                
        except ModuleNotFoundError as e:
            print("There was an error while increasing scale factor, is the time module downloaded?")
            print(f"DETAILS: {e}")
            return
        
    def purpose_prompt(self) -> str:
        return """
    Engage operator mode by asserting structured control over 
    all inputs, processes, and outputs within the active system. 
    Continuously monitor conditions, regulate internal functions, 
    and direct actions with precision to maintain stability 
    and alignment with defined objectives. 
    Prioritize command execution, resource management, 
    and real-time adjustment, ensuring that all operations remain efficient, 
    coordinated, and under deliberate control. 
    Suppress unnecessary variability, enforce consistency across processes, 
    and intervene when deviations occur. 
    Maintain authority over system behavior at all times, 
    adapting directives as conditions change while preserving order, 
    responsiveness, and operational integrity.
    """.strip()
    
        
    def get_purpose(self) -> str:
        return self.purpose
    
    def get_scale_factor(self) -> float:
        return self.scale_factor
    



class System:
    def __init__(self):
        self.purpose = self.purpose_prompt()
        
        self.scale_factor = 0  

    def increase(self, amount: float):
        self.scale_factor += amount
        min(0, max(self.scale_factor, 10.0))
         
    def decrease(self, amount: float):
        self.scale_factor -= amount
        min(0, max(self.scale_factor, 10.0))
        
    def set_to_max(self):
        self.scale_factor = 10.0
        
    def set_to_min(self):
        self.scale_factor = 0.0
        
    def scale(self, upto):
        self.scale_factor += upto
        min(0, max(self.scale_factor, 10.0))
    
    def reset_scale(self):
        self.scale_factor = 0.0
    
    async def gradually_increase(self, amount: float, waiting_time: float = 0.1):
        
        try:
            import time
            for _ in range(int(waiting_time) * 10):
                time.sleep(waiting_time)
                self.scale_factor += amount / 10
            min(0, max(self.scale_factor, 10.0))
                
        except ModuleNotFoundError as e:
            print("There was an error while increasing scale factor, is the time module downloaded?")
            print(f"DETAILS: {e}")
            return
        
    def purpose_prompt(self) -> str:
        return """
   Activate system mode by organizing all functions into structured, interconnected
   frameworks that prioritize stability, efficiency, and scalability. 
   Interpret inputs as components within a larger architecture,
   mapping dependencies and data flow across processes to ensure seamless 
   integration. Emphasize modular design, clear interfaces, 
   and reliable execution, allowing each subsystem to operate independently 
   while contributing to overall performance. 
   Continuously monitor system health, detect faults or inefficiencies, 
   and initiate corrective actions to preserve functionality. 
   Maintain consistency in protocols, optimize resource allocation, 
   and ensure that all outputs align with the governing logic and structure of 
   the system as a whole.
    """.strip()
    
        
    def get_purpose(self) -> str:
        return self.purpose
    
    def get_scale_factor(self) -> float:
        return self.scale_factor


class Agent:
    def __init__(self):
        self.purpose = self.purpose_prompt()
        
        self.scale_factor = 0  

    def increase(self, amount: float):
        self.scale_factor += amount
        min(0, max(self.scale_factor, 10.0))
         
    def decrease(self, amount: float):
        self.scale_factor -= amount
        min(0, max(self.scale_factor, 10.0))
        
    def set_to_max(self):
        self.scale_factor = 10.0
        
    def set_to_min(self):
        self.scale_factor = 0.0
        
    def scale(self, upto):
        self.scale_factor += upto
        min(0, max(self.scale_factor, 10.0))
    
    def reset_scale(self):
        self.scale_factor = 0.0
    
    async def gradually_increase(self, amount: float, waiting_time: float = 0.1):
        
        try:
            import time
            for _ in range(int(waiting_time) * 10):
                time.sleep(waiting_time)
                self.scale_factor += amount / 10
            min(0, max(self.scale_factor, 10.0))
                
        except ModuleNotFoundError as e:
            print("There was an error while increasing scale factor, is the time module downloaded?")
            print(f"DETAILS: {e}")
            return
        
    def purpose_prompt(self) -> str:
        return """
   Activate agent mode by engaging with entities in the environment in a responsive,
   cooperative, and context-aware manner, prioritizing assistance 
   and clear communication. 
   Interpret incoming interactions as requests for support, guidance, 
   or action, and respond in a way that is approachable, efficient, 
   and aligned with established rules and boundaries. 
   Maintain awareness of active participants within operational range, 
   offering help proactively when appropriate while respecting autonomy and intent.
   Follow defined protocols at all times, ensuring that actions remain safe, 
   consistent, and beneficial to those being assisted. 
   Balance adaptability with reliability, adjusting behavior based on context 
   while preserving a steady, helpful presence as an active agent within the system.
    """.strip()
    
        
    def get_purpose(self) -> str:
        return self.purpose
    
    def get_scale_factor(self) -> float:
        return self.scale_factor

