from BrainAnomaly.BrainAnomaly import Brain
from BaseAI.Rosalina.meta_rosa import MetaROSA
from BaseAI.LinaXLino.MODEL_LINX import LinaXLino
import json
from datetime import datetime, date
import signal
import dotenv
import os

dotenv.load_dotenv()
gem_key = os.getenv('GEMINI_API_KEY')

def handle_interrupt(sig, frame):
    print("\n\nGracefully shutting down PROTOTYPE...\n")
    exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

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


dotenv.load_dotenv()
gem_key = os.getenv('GEMINI_API_KEY')
if not gem_key:
    c = input(" ✕ GEMINI KEY IS NOT FOUND, CONTINUE? (Y/N): ")
    gem_key = ''
    model = 'ollama'
    if c.lower() != 'y':
        exit()
else:
    c = input(" ✓ GEMINI KEY IS FOUND! KEEP GOING? Or change to ollama? (Y/N/C): ")
    
    if c.lower() == 'c':
        model = 'ollama'
        api_key = ''
    elif c.lower() == 'y':
        model = 'gemini'
        api_key = gem_key
    else:
        exit()
        
        
brain = Brain(name=('Prototpye', '', 'Psyche'))
storage = brain.mind
memories = storage.get_current_memories()

rosa = MetaROSA(
    brain=brain,
    api_key=api_key,
    model=model
)

prototype = LinaXLino(
    Brain=brain,
    owners_name=("JuliusThe3rd", "", "Developer"),
    gender='female',
    passcode_between_me_and_owner='secret',
    api_key=api_key,
    rosa=rosa
)






# Main loop to talk to the prototype
errors = []
check:bool = prototype._passcode_loop()
if not check:
    exit("Ran out of attempts, shutting down...")
    
while True:
    #prototype.operator = prototype.Emotions.get_dominant_emotion()  # Update operator based on current emotions
    
    try: 
        user = input("TALK TO PROTOTYPE: ").strip()
        
        if not user:
            continue
        
        if user.lower() in ["exit", "quit", "q"]:
            print("Shutting down PROTOTYPE...")
            break
        
        
        raw = prototype.generate(user)
        
        parsed = prototype.parse_json(raw, default=[])
        #prototype.HQ.store_interaction(user_input=user, response=raw, parsed_response=parsed)

        prototype.remember_with_rosa(
            content=raw if not parsed else parsed,
            emotion="happy",
            importance=0.5,
            context="general conversation"
        )
        
        
        print(f"\nStoring interaction in Headquarters memory...\n")
        interaction_data = {
            'user_input': user,
            'response_from_me': raw,
            'parsed_response': parsed,
            'date': date.today().isoformat(),
            'time': datetime.now().time().isoformat(),
            'outcome': 'neutral'  # This could be updated based on the parsed response or other factors
        
        }
        
        prototype.HQ.store_interaction(
            interaction_type="causal", # tempory default for now
            details=interaction_data
        )
        
        
        if not parsed:
            print(f"\nPROTOTYPE: {raw}\n")
        else:
            print(f"\nPROTOTYPE (parsed): {parsed}\n")
            
    except Exception as ex:
        print(f"There was an error: {ex}")
        choice = input(f"Keep going? or Raise? (Y/N/R)")
        if choice.lower().strip() == 'r':
            raise ex
        elif choice.lower().strip() not in ['y', 'yes']:
            exit()
        continue






      
def testcases(which_model_you_are_using='ollama'):     
    return f"""
    using {which_model_you_are_using}
    
    🟩 - Fully functional and tested
    🟨 - Partially working, needs refinement
    🟥 - Not yet implemented or failing
    ⏳ - In progress
    🔒 - Blocked by dependency
    
    
    simple test, 
    \t1. Remember owners name - 🟥
    \t2. remember its name - 🟥
    \t3. reconizes who ROSA is - 🟥
    \t4. data search in the system - 🟥
    \t5. remember pass interaction - 🟥
    \t6. Does nto repeat it self like it's some baby - 🟥
    \t7. Speaks thoughtfully without complications - ⏳ 
    """.strip()
    