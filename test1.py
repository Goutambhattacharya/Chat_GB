import os
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise Exception("❌ API key not loaded!")

# ✅ Check key
print("🔑 API Key (partial):", API_KEY[:10] + "...")

# Prepare headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Payload
payload = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [{"role": "user", "content": "Tell me something inspiring!"}]
}

# API call
response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

print("✅ Status Code:", response.status_code)
try:
    print("📦 Response:", response.json())
except Exception as e:
    print("❌ JSON Error:", e)
    print("🔴 Raw Response:", response.text)
