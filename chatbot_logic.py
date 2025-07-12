import os
import pandas as pd
import faiss
import numpy as np
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load data
df = pd.read_csv("realistic_restaurant_reviews.csv")
texts = df["Review"].dropna().tolist()  # use the correct column name

# Chunking
def chunk_texts(texts, size=500, overlap=50):
    chunks = []
    for text in texts:
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i:i + size])
    return chunks

chunks = chunk_texts(texts)

# Embedding
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

# Vector store
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(np.array(embeddings))

def get_top_chunks(query, k=3):
    query_vec = model.encode([query])
    _, I = index.search(np.array(query_vec), k)
    return [chunks[i] for i in I[0]]

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()['choices'][0]['message']['content']

def ask_bot(user_input):
    context = "\n".join(get_top_chunks(user_input))
    prompt = f"""Answer the following question using only the information provided below.

Context:
{context}

Question: {user_input}
Answer:"""
    return ask_openrouter(prompt)
