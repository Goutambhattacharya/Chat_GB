import os
from dotenv import load_dotenv

# Get absolute path to .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
print("📁 Checking .env at:", env_path)
print("📄 File exists:", os.path.exists(env_path))

# Load .env
load_dotenv(dotenv_path=env_path)

# Print environment variable
api_key = os.getenv("OPENROUTER_API_KEY")
print("🔍 OPENROUTER_API_KEY =", api_key if api_key else "❌ NOT FOUND")
