import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ask_bot(user_input):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ API key not found")
        return "⚠️ API key not configured."

    print("🔐 Using API Key:", api_key[:10])

    url = "https://openrouter.ai/api/v1/chat/completions"

    # IMPORTANT: correct header names — no "HTTP-Referer"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Referer": "http://localhost:5000",       # OpenRouter expects this, no "HTTP-" prefix
        "User-Agent": "my-flask-chatbot/1.0"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("📦 Status Code:", response.status_code)
        print("📦 Response:", response.text)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Error:", e)
        return f"⚠️ Error: {str(e)}"
