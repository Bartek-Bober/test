import requests
import os
from dotenv import load_dotenv


load_dotenv()

def chat_with_history(messages_history: list) -> str:
 
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("Brak klucza API! Ustaw OPENROUTER_API_KEY w pliku .env")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openrouter/free",
        "messages": messages_history,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise RuntimeError(f"Błąd API: {response.text}")

    return response.json()["choices"][0]["message"]["content"]