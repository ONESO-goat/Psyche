from dotenv import load_dotenv
import os

load_dotenv()  # must come BEFORE getenv

print(os.getenv("API_KEY"))