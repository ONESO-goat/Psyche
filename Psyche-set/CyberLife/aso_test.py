# test_aso_integration.py

from BrainAnomaly.BrainAnomaly import Brain
from ASO.ASO import ASO
from Memory.memory_systems import EmotionalCalling
from Memory.Emotions.Inside_out import RileyAnderson
import json
import os

gemini_key = os.environ.get("GEMINI_API_KEY")

# Create brain
brain = Brain(name=('William', '', 'Smith'))
management = EmotionalCalling(storage=brain.mind, brain=brain, emotions=RileyAnderson())

# Add some memories
management.encode_memory("I met my friend who owns a Shih Tzu", {'emotion': "happy", 'importance': 0.7})
management.encode_memory("I own a pitbull and love him!", {'emotion': "happy", 'importance': 0.8})
management.encode_memory("I was rejected from MIT", {'emotion': "sad", 'importance': 0.9}, add_timestamp=True)

# Initialize ASO
aso = ASO(
    Brain=brain,
    api_key='',  # Or None for Ollama
    model='ollama'  # Or 'ollama'
)

# Process all memories
print("=" * 60)
print("PROCESSING MEMORIES")
print("=" * 60)
aso.process_all_memories(reprocess=False)

# Check stats
print("\n" + "=" * 60)
print("ASSOCIATION NETWORK STATS")
print("=" * 60)
stats = aso.get_stats()
print(json.dumps(stats, indent=2))

# Find related concepts
print("\n" + "=" * 60)
print("WHAT'S RELATED TO 'DOG'?")
print("=" * 60)
related = aso.find_related("dog")
for r in related:
    print(f"  {r['concept']}: {r['strength']:.2f} ({r['type']})")

# Find path
print("\n" + "=" * 60)
print("PATH FROM 'DOG' TO 'FRIEND'?")
print("=" * 60)
path = aso.find_path("dog", "friend")
if path:
    print(f"  {' → '.join(path)}")
else:
    print("  No path found")

# Spreading activation
print("\n" + "=" * 60)
print("WHAT DOES 'DOG' REMIND ME OF?")
print("=" * 60)
activated = aso.what_reminds_me_of("dog", threshold=0.2)
for concept, strength in sorted(activated.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {concept}: {strength:.2f}")

# Get concept info
print("\n" + "=" * 60)
print("INFO ABOUT 'DOG'")
print("=" * 60)
info = aso.get_concept_info("dog")
print(json.dumps(info, indent=2))

# Check brain structure (associations are stored IN the brain)
print("\n" + "=" * 60)
print("BRAIN STRUCTURE (associations stored here)")
print("=" * 60)
brain_data = brain.mind.memories[0]['brain']
print(f"Associations in brain: {len(brain_data.get('associations', {}).get('graph', {}))}")
print(f"Metadata: {brain_data.get('associations', {}).get('metadata', {})}")