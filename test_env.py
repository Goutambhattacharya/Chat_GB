import os
from dotenv import load_dotenv

# ✅ Load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print("📁 Looking for .env at:", dotenv_path)
load_dotenv(dotenv_path)

api_key = os.getenv("OPENROUTER_API_KEY")

print("🔑 API_KEY found?", api_key is not None)
print("📦 Key value (masked):", api_key[:6] + "..." if api_key else "❌ MISSING")
