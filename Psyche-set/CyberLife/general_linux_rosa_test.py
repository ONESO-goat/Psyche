# test_rosa_general_linx.py
import dotenv
import os
from BrainAnomaly.BrainAnomaly import Brain
from BaseAI.Rosalina.meta_rosa import MetaROSA
from BaseAI.LinaXLino.MODEL_LINX import LinaXLino
import json

# Load environment variables
dotenv.load_dotenv()
gem_key = os.getenv('GEMINI_API_KEY')
if not gem_key:
    check = input(" ✕ GEMINI KEY IS NOT FOUND, CONTINUE? (Y/N): ")
    gem_key = ''
    model = 'ollama'
    if check.lower() != 'y':
        exit()
else:
    check = input(" ✓ GEMINI KEY IS FOUND! KEEP GOING? (Y/N): ")
    if check.lower() != 'y':
        exit()
    
# Create ROSA
rosa_brain = Brain(name=('ROSA', '', 'TEST10'))
rosa = MetaROSA(
    brain=rosa_brain,
    api_key='your_gemini_key',
    model='gemini'
)

print("=" * 70)
print("ROSA SUPREME COMMANDER INITIALIZED")
print("=" * 70)

# Create LINX instances
brain_a = Brain(name=('Alice', '', 'Dev'))
linx_a = LinaXLino(
    Brain=brain_a,
    owners_name=("Alice", "", "Developer"),
    gender='female',
    passcode_between_me_and_owner='secret',
    api_key='your_gemini_key',
    rosa=rosa
)

brain_b = Brain(name=('Bob', '', 'Musician'))
linx_b = LinaXLino(
    Brain=brain_b,
    owners_name=("Bob", "", "Musician"),
    gender='male',
    passcode_between_me_and_owner='secret',
    api_key='your_gemini_key',
    rosa=rosa
)

# Test 1: Coding domain
print("\n" + "=" * 70)
print("TEST 1: CODING DOMAIN")
print("=" * 70)
linx_a.remember_with_rosa(
    content="I hate leetcode, it feels useless for real work",
    emotion="frustrated",
    importance=0.8,
    context="coding interviews"
)

# Test 2: Music domain
print("\n" + "=" * 70)
print("TEST 2: MUSIC DOMAIN")
print("=" * 70)
linx_b.remember_with_rosa(
    content="This chord progression makes me feel nostalgic",
    emotion="wistful",
    importance=0.7,
    context="music composition"
)

# Test 3: Another coding memory (should go to same General)
print("\n" + "=" * 70)
print("TEST 3: MORE CODING (should reuse General)")
print("=" * 70)
linx_a.remember_with_rosa(
    content="I learn better from building projects than tutorials",
    emotion="motivated",
    importance=0.9,
    context="learning to code"
)

# Check Generals
print("\n" + "=" * 70)
print("GENERALS REPORT")
print("=" * 70)
generals = rosa.get_all_generals()
for g in generals:
    print(f"\nGeneral: {g['domain']}")
    print(f"  Vision: {g['vision'].get('vision_statement', 'N/A')}")
    print(f"  Theories: {g['theories_count']}")
    print(f"  Assigned LINX: {len(g['assigned_linx'])}")
    print(f"  Confidence: {g['stats']['confidence']:.2f}")

# Get optimization for LINX
print("\n" + "=" * 70)
print("OPTIMIZING LINX")
print("=" * 70)
optimization = linx_a.apply_optimization()
print(json.dumps(optimization, indent=2))

# Query a General
print("\n" + "=" * 70)
print("QUERYING GENERAL")
print("=" * 70)
wisdom = rosa.query_general('coding_interviews', 'How should I approach interview prep?')
print(json.dumps(wisdom, indent=2))

# Final stats
print("\n" + "=" * 70)
print("ROSA META-STATS")
print("=" * 70)
stats = rosa.get_meta_stats()
print(f"Total Generals: {stats['generals_count']}")
print(f"Total Memories: {stats['total_memories']}")
print(f"Association Network: {stats['association_network']['total_concepts']} concepts")