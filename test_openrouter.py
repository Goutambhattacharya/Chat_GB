import requests
import os
from dotenv import load_dotenv

load_dotenv()

def ask_bot(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "⚠️ Missing API key."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Referer": "http://localhost",
        "User-Agent": "my-flask-chatbot/1.0"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Error:", e)
        return f"⚠️ {str(e)}"
