from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

test = os.getenv("envtest")
print(test)