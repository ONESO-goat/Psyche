from BrainAnomaly.BrainAnomaly import Brain
from Rosalina.Rosa import rosalina




if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    
    
    def test1():
        
        gem_key = os.getenv("GEMINI_API_KEY")
        model = 'gemini'
        
        if not gem_key:
            check = input(" ✕ GEMINI KEY IS NOT FOUND, CONTINUE? (Y/N): ")
            gem_key = ''
            model = 'ollama'
            if check.lower() != 'y':
                return
        else:
            check = input(" ✓ GEMINI KEY IS FOUND! KEEP GOING? (Y/N): ")
            if check.lower() != 'y':
                return
                
        # Initialize Brain + ROSA
        brain = Brain(name=("Rosa", "Lina", "Psyche"))
        rosa = rosalina(brain)
        rosa.set_up(api_key=gem_key, model=model)

        print("\n🧠 ROSA is ready. Type 'exit' to quit.\n")

        while True:
            try:
                user = input("TALK TO ROSA: ").strip()

                if user.lower() in ["exit", "quit", "q"]:
                    print("Shutting down ROSA...")
                    break

                if not user:
                    continue

               
                raw = rosa._generate(user)

                # 🔥 Parse JSON safely (since you expect JSON output)
                parsed = rosa._parse_json(raw, default=[])

                # If model didn't return JSON, fallback
                if not parsed:
                    print(f"\nROSA: {raw}\n")
                else:
                    print(f"\nROSA (parsed): {parsed}\n")

                # 🔥 OPTIONAL: store interaction in Brain
                try:
                    rosa.Brain.mind.add({
                        "user": user,
                        "response": parsed if parsed else raw
                    })
                except Exception as e:
                    print(f"⚠ Memory store error: {e}")

            except KeyboardInterrupt:
                print("\nInterrupted. Shutting down ROSA...")
                break

            except Exception as e:
                print(f"⚠ Runtime error: {e}")
                
    def test2(use_gem: bool=True):
    
        import os

        gem_key = os.getenv("GEMINI_API_KEY2")
        model = 'gemini'
        if use_gem:
            if not gem_key:
                check = input(" ✕ GEMINI KEY IS NOT FOUND, SWITCHING TO OLLAMA.CONTINUE? (Y/N): ")
                gem_key = ''
                model = 'ollama'
                if check.lower() != 'y':
                    return
            else:
                check = input(" ✓ GEMINI KEY IS FOUND! KEEP GOING? (Y/N): ")
                if check.lower() != 'y':
                    return
        else:
                gem_key = ''
                model = 'ollama'
                
        # Initialize Brain + ROSA

        brain = Brain(name=("Rosa", "Lina", "Psyche"))
        rosa = rosalina(brain)
        rosa.set_up(api_key=gem_key, model=model)
        
        rosa_key = os.getenv("ROSA_CODE")
        
        if rosa_key:
            rosa._switch_(rosa_key)
        else:
            print("⚠ ROSA CODE NOT FOUND")
            return
        
        print("\n🧠 ROSA is ready. Type 'exit' to quit.\n")

        while True:
            user = input("TALK TO ROSA: ").strip()

            if user.lower() in ["exit", "quit", 'q']:
                print("Shutting down ROSA...")
                break

            if not user:
                continue

            # 🔥 Generate normal response
            response = rosa._generate(user)

            print(f"\nROSA: {response}\n")

            # 🔥 Store memory (simple version)
            try:
                memory = rosa.define_memory(user_input=user, repsonse=response)
                print("====================================")
                print("====================================")
                print(f"✓ Rosa memory stored: {memory}\n")
                
            except Exception as e:
                print(f"⚠ Memory error: {e}")
                
                
    test2(True)