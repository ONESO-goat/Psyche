from schema.topic import TopicLogic, test_add_topic
import asyncio
testId = "1"*37
async def main(whats_being_tested: str, create:bool=False):
    try:
        print(f"TESTING '{whats_being_tested}'")
        if create:
            test_add_topic()

        t = await TopicLogic.create(schema_id=testId, schema_type=whats_being_tested)
        t.test()
        print("\nSUCCESSFUL\n")
    except Exception as ex:
        print(f"FAILURE OCCURED WITH '{whats_being_tested}': {ex}")
        
        
if __name__ == "__main__":

    asyncio.run(main(whats_being_tested="topic"))