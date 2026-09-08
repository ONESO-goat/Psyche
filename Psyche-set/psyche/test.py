from associations.brain import BrainLogic
import json

fake_brain = None
try:
    with open("brain_test_json/gemini_example.json", 'r') as f:
        fake_brain = json.load(f) 
except json.JSONDecodeError as ex:
    print(f"Failed to open fake brain data: \n\t\u2022 {ex}")
    exit()

if fake_brain is None:
    print("Couldn't connect to brain")
    exit(1)

def main(id_:str):
    brainLogic = BrainLogic(id_)

    if not brainLogic.ok(): # Does nothing, implement sooner than later
        return 
    brainLogic.

if __name__ == "__main__":
    main()