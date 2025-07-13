import requests

hf_token = "88888******************"  # Replace with your new token if needed

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": "What are 3 fun facts about pandas?"
}

response = requests.post(API_URL, headers=headers, json=payload)

print("✅ Status Code:", response.status_code)
print("📦 Response:", response.text)
