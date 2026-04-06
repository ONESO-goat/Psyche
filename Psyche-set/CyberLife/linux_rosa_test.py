# test_rosa_linx.py

from BrainAnomaly.BrainAnomaly import Brain
from BaseAI.Rosalina.meta_rosa import MetaROSA
from BaseAI.Rosalina.Rosa import rosalina
import dotenv
import os
from BaseAI.LinaXLino.MODEL_LINX import LinaXLino
import json

dotenv.load_dotenv()
gem_key = os.getenv("GEMINI_API_KEY")

# Create ROSA (the queen brain)
rosa_brain = Brain(name=('ROSA', '', 'CORE'))
rosa = MetaROSA(
    brain=rosa_brain,
    api_key=gem_key,
    model='gemini'
)

print("=" * 60)
print("ROSA INITIALIZED")
print("=" * 60)

# Create LINX instance A
brain_a = Brain(name=('Alice', '', 'Assistant'))
linx_a = LinaXLino(
    Brain=brain_a,
    owners_name='Alice',
    gender='female',
    passcode_between_me_and_owner='secret123',
    api_key=gem_key,
    rosa=rosa  # Connect to ROSA
)

# Create LINX instance B
brain_b = Brain(name=('Bob', '', 'Operator'))
linx_b = LinaXLino(
    Brain=brain_b,
    owners_name='Bob',
    gender='male',
    passcode_between_me_and_owner='secret456',
    api_key=gem_key,
    rosa=rosa  # Connect to ROSA
)

# LINX A adds memory
print("\n" + "=" * 60)
print("LINX A: Adding memory")
print("=" * 60)
linx_a.remember_with_rosa(
    content="I hate leetcode, it feels useless",
    emotion="frustration",
    importance=0.7,
    context="coding interviews"
)

# LINX B adds similar memory
print("\n" + "=" * 60)
print("LINX B: Adding memory")
print("=" * 60)
linx_b.remember_with_rosa(
    content="Interview prep is so disconnected from real work",
    emotion="frustration",
    importance=0.6,
    context="job searching"
)

# Query ROSA's wisdom
print("\n" + "=" * 60)
print("QUERYING ROSA")
print("=" * 60)
wisdom = rosa.query_wisdom("How do people feel about interview preparation?")
print(json.dumps(wisdom, indent=2))

# Check ROSA's meta-stats
print("\n" + "=" * 60)
print("ROSA META-STATS")
print("=" * 60)
stats = rosa.get_meta_stats()
print(f"Registered LINX: {stats['registered_linx']}")
print(f"Total memories: {stats['total_memories']}")
print(f"Association network: {stats['association_network']['total_concepts']} concepts")
print(f"Instances: {len(stats['instances'])}")