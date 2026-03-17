import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter(payload):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
  