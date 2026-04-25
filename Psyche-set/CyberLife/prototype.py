from BrainAnomaly.BrainAnomaly import Brain
from BaseAI.Rosalina.meta_rosa import MetaROSA
from BaseAI.LinaXLino.MODEL_LINX import LinaXLino
import json


# This file is a prototype for the Psyche class, which will serve as the main interface for the CyberLife cognitive architecture.
# We are testing just 1 LINX instance connected to ROSA for now, but the final Psyche class will be able to manage multiple LINX instances and other systems.


"""
    setting up a simple loop where we can talk to the LINX prototype, which is connected to ROSA.
    We will test the following:
    1. Basic conversation with the LINX prototype
    2. Storing interactions in the Headquarters memory system
    3. Remembering interactions with ROSA's help
    4. Parsing responses as JSON (since we expect structured data back from the model)
    5. Displaying the raw and parsed responses for comparison 
"""
brain = Brain(name=('Psyche', '', 'Prototype'))
storage = brain.mind
memories = storage.get_current_memories()

rosa = MetaROSA(
    brain=brain,
    api_key='',
    model='gemini'
)

prototype = LinaXLino(
    Brain=brain,
    owners_name=("Alice", "", "Developer"),
    gender='female',
    passcode_between_me_and_owner='secret',
    api_key='',
    rosa=rosa
)






# Main loop to talk to the prototype


while True:
    user = input("TALK TO PROTOTYPE: ").strip()
    if user.lower() in ["exit", "quit", "q"]:
        print("Shutting down PROTOTYPE...")
        break
    if not user:
        continue
    
    raw = prototype._generate(user)
    
    parsed = prototype._parse_json(raw, default=[])
    #prototype.HQ.store_interaction(user_input=user, response=raw, parsed_response=parsed)
    
    prototype.remember_with_rosa(
        content=user,
        emotion="neutral",
        importance=0.5,
        context="general conversation"
    )
    
    if not parsed:
        print(f"\nPROTOTYPE: {raw}\n")
    else:
        print(f"\nPROTOTYPE (parsed): {parsed}\n")