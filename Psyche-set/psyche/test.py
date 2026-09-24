from schema.topic import TopicLogic, test_add_topic
from schema.brain import BrainLogic, test_add_brain_schema
from schema.association import AssociationLogic, test_add_association
import asyncio

from associations import ASO
from typing import Final

# TEST IDS
TEST_TOPIC1_ID: Final[str] = "1"*37 # apples

TEST_TOPIC2_ID: Final[str] = "2"*37 # grapes

TEST_BRAIN_ID: Final[str] = "1"*37

TEST_ASSOCIATION_ID: Final[str] = "1"*37





async def schemaLogicTest(whats_being_tested: str, provided_id:str, create:bool=False):
    try:
        schemas = {
            "brain": BrainLogic,
            "topic": TopicLogic,
            "association": AssociationLogic
        }
        print(f"TESTING '{whats_being_tested}'")

        
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
            Topic
        )
        pass
    except Exception as ex:
        raise ex

def main(brain):
    pass

if __name__ == "__main__":

    asyncio.run(schemaLogicTest(whats_being_tested="brain"))