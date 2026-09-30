from schema.topic import TopicLogic, test_add_topic
from schema.brain import BrainLogic, test_add_brain_schema
from schema.association import AssociationLogic, test_add_association
import asyncio
from helpers.python_.helpers import (
            Brain, 
            Association,
            Memory,
            Topic,
            BrainTypes,
            EMOTIONS
        )
from associations import ASO
from typing import Final
from datetime import datetime, timezone

# TEST IDS and Variables

TIME = datetime.now(tz=timezone.utc)

TEST_TOPIC1_ID: Final[str] = "1"*48 # apples
TEST_TOPIC2_ID: Final[str] = "2"*48 # grapes

TEST_BRAIN_ID: Final[str] = "1"*37

TEST_ASSOCIATION_ID: Final[str] = "1"*48

TEST_MEMORY1_ID: Final[str] = "1"*37
TEST_MEMORY2_ID: Final[str] = "2"*37

TEST_MEMORY_1 = Memory(
    memory_id=TEST_MEMORY1_ID,
    brain_id=TEST_BRAIN_ID,
    context="I just ate an apple!",
    dominant_emotion=EMOTIONS.JOY, # YELLOW, paints this memory yellow. 
    importance=0.4,
    formed_at=TIME
)

TEST_MEMORY_2 = Memory(
    memory_id=TEST_MEMORY2_ID,
    brain_id=TEST_BRAIN_ID,
    context="Apples and grapes fall in the same family of fruit. Theyre both sold at the local store, market basket.",
    dominant_emotion=EMOTIONS.SURPRISE, # YELLOW, paints this memory yellow. 
    importance=1,
    formed_at=TIME
)

# ============================ TEST functions =================================
async def schemaLogicTest(whats_being_tested: str, provided_id:str, create:bool=False):
    try:
        schemas = {
            "brain": BrainLogic,
            "topic": TopicLogic,
            "association": AssociationLogic
        }
        print(f"TESTING '{whats_being_tested}'")

        if whats_being_tested not in schemas:
            raise RuntimeError(f"'{whats_being_tested}' is invalid.")
        
        if create:

            create_options = {
                        "brain": test_add_brain_schema,
                        "topic": test_add_topic,
                        "association": test_add_association
                    }
            if whats_being_tested == "association":
                create_options["association"](
                    id_=provided_id, 
                    topic_1_id=TEST_TOPIC1_ID,
                    topic_2_id=TEST_TOPIC2_ID,
                    context="Discovered more about fruits",
                    association_type="fruit"
                )

            else:
                create_options[whats_being_tested](id_=provided_id)

        s = await schemas[whats_being_tested].create(schema_id=provided_id, schema_type=whats_being_tested)
        print(s.schema)
        print("\nSUCCESSFUL\n")
        return s
    except Exception as ex:
        print(f"FAILURE OCCURED WITH '{whats_being_tested}': {ex}")
        return None


def database_intergation_test():
    t1 = schemaLogicTest(whats_being_tested="topic", provided_id=TEST_TOPIC1_ID)
    t2 = schemaLogicTest(whats_being_tested="topic", provided_id=TEST_TOPIC2_ID, create=True)

    if not t1 or not t2:
        print(f"""
        T1 or T2 were not created or found:
        T1 == {t1.schema or None}
        \n
        T2 == {t2.schema or None}
    """)
        return
    association_ = schemaLogicTest(
        whats_being_tested="assocation", 
        provided_id=TEST_ASSOCIATION_ID, 
        create=True
    )
    if not association_ or not association_.schema:
        print(f"Association was not created: {association_}")
        return
    print(f"ASSOCIATION was created: {association_.schema}")

def test_schemas():
    try:
        from helpers.python_.helpers import (
            Brain, 
            Association,
            Memory,
            Topic,
            BrainTypes
        )
        from datetime import datetime, timezone

        brain = Brain(
            brain_id=TEST_BRAIN_ID,
            brain_memories={},
            created_at=datetime.now(tz=timezone.utc),
            brain_type=BrainTypes.LINX
        )
        print(brain)
    except Exception as ex:
        raise ex




def huge_assoacition_test():
    
    brain = Brain(
        brain_id=TEST_BRAIN_ID,
        created_at=TIME,
        brain_type=BrainTypes.GENERAL
    )

    APPLE_FACTS = {
            "Central Asia": [
                "Wild ancestors (Malus sieversii) first grew in the forests of Kazakhstan and the Tian Shan mountains over 8,000 years ago."
            ],
            "history": [
                "Travelers and merchants spread the fruit toward Europe and the Middle East."
            ],
            "roman": [
                "The Romans advanced selective breeding and grafting techniques, spreading orchards across Europe and Britain."
            ]
    }
    topic1 = Topic(
        topic_id=TEST_TOPIC1_ID,
        title="apples",
        context="""
        An apple is the round, edible pome fruit of the domesticated tree Malus domestica in the rose family
        """,
        facts=APPLE_FACTS,
        created_at=TIME
    )

    GRAPE_FACTS = {
        "shape": [
            "Botanically classified as a true berry, a grape consists of a protective outer skin, a fleshy pulp, and typically seeds (though many table varieties are bred to be seedless)."
        ],
        "Anatomy": [
            "The pulp is mostly water and natural sugars (glucose and fructose), while the skin provides tannins, color pigments, and wild yeasts"
        ],
        "origins": [
            "test_schemasOrigins: Grape cultivation dates back roughly 8,000 years, with early domestication spanning areas near the Black Sea, Iran, and the Caucasus region."
        ]
    }
    topic2 = Topic( #also known as concept
        topic_id=TEST_TOPIC2_ID,
        title="grapes",
        context="A grape is a small, juicy fruit that grows in clusters on woody climbing vines of the genus Vitis.",
        facts=GRAPE_FACTS,
        created_at=TIME
    )

    association = Association(
        association_id=TEST_ASSOCIATION_ID,
        topic_one_id=topic1.topic_id,
        topic_two_id=topic2.topic_id,

        context="both are fruits",
        strength=0.76,
        source_id="",
        association_type="fruit"
    )
    print(association.to_dict())

def replace_memory_test():
    pass
def main(brain):
    pass

if __name__ == "__main__":

    #asyncio.run(test_schemas())
    huge_assoacition_test()