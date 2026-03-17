
import requests
import json
import os

from dotenv import load_dotenv

# Załaduj zmienne z pliku .env
load_dotenv()


def chat_with_openrouter(
    prompt: str,
    model: str = "",
    api_key: str | None = None,
) -> str:
    """
    Wysyła zapytanie do OpenRouter.ai i zwraca odpowiedź modelu.

    Args:
        prompt:  Treść wiadomości użytkownika.
        model:   Identyfikator modelu.
        api_key: Klucz API OpenRouter. Jeśli None, pobiera z env.

    Returns:
        Odpowiedź modelu jako string.
    """

    # ---------- klucz API ----------
    api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError(
            "Brak klucza API! Ustaw zmienną OPENROUTER_API_KEY "
            "lub przekaż api_key jako argument."
        )

    # ---------- endpoint i nagłówki ----------
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://example.com",   # wymagane przez OpenRouter
        "X-Title": "HelloWorld App",              # opcjonalne – nazwa aplikacji
    }

    # ---------- ciało żądania ----------
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Jesteś pomocnym asystentem. Odpowiadaj zwięźle.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "max_tokens": 512,
        "temperature": 0.7,
    }

    # ---------- wysłanie żądania ----------
    response = requests.post(url, headers=headers, json=payload, timeout=60)

    # ---------- obsługa błędów HTTP ----------
    if response.status_code != 200:
        error_detail = response.text
        raise RuntimeError(
            f"Błąd API ({response.status_code}): {error_detail}"
        )

    # ---------- parsowanie odpowiedzi ----------
    data = response.json()

    # Sprawdzenie, czy odpowiedź zawiera oczekiwane dane
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Nieoczekiwany format odpowiedzi: {json.dumps(data, indent=2)}"
        ) from exc

    return content


# ──────────────────────────────────────────────
#  MAIN – punkt wejścia
# ──────────────────────────────────────────────
if __name__ == "__main__":

    # --- Konfiguracja -----------------------------------------------------------
    # Wstaw swój klucz lub ustaw zmienną środowiskową OPENROUTER_API_KEY
    API_KEY = os.getenv("OPENROUTER_API_KEY", "")  # np. "sk-or-v1-abc123..."
    
    #lista modeli free: https://openrouter.ai/collections/free-models
    MODEL = "openrouter/free" 


    print("=" * 60)
    print("  🚀  Hello World – OpenRouter.ai")
    print("=" * 60)

    # --- 1. Tryb zwykły (non-streaming) ----------------------------------------
    print("\n📨  Tryb zwykły (non-streaming):\n")
    try:
        answer = chat_with_openrouter(
            prompt="Powiedz 'Hello World' i krótko wyjaśnij, czym jest OpenRouter.",
            model=MODEL,
            api_key=API_KEY,
        )
        print(answer)
    except Exception as e:
        print(f"❌ Błąd: {e}")

    print("\n" + "-" * 60)
