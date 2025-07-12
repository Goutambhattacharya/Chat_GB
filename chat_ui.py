import os
import pandas as pd
import faiss
import numpy as np
import gradio as gr
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load and preprocess data
df = pd.read_csv("realistic_restaurant_reviews.csv")
texts = df["Review"].dropna().tolist()

def chunk_texts(texts, size=500, overlap=50):
    chunks = []
    for text in texts:
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i:i+size])
    return chunks

chunks = chunk_texts(texts)

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Retrieve top-k chunks
def get_top_chunks(query, k=3):
    query_vec = model.encode([query])
    _, I = index.search(np.array(query_vec), k)
    return [chunks[i] for i in I[0]]

# OpenRouter API call
def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()['choices'][0]['message']['content']

# Chat function for Gradio
def chat_with_bot(user_input, history=[]):
    context = "\n".join(get_top_chunks(user_input))
    prompt = f"""Answer the question using only the information below.

Context:
{context}

Question: {user_input}
Answer:"""
    try:
        response = ask_openrouter(prompt)
    except Exception as e:
        response = f"❌ Error: {str(e)}"
    history.append((user_input, response))
    return history, history

# Gradio UI
with gr.Blocks(title="🍕 Restaurant Review Chatbot") as demo:
    gr.Markdown("### 🍕 Chat with the Restaurant Review Bot")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask a question about the reviews")
    state = gr.State([])

    msg.submit(chat_with_bot, [msg, state], [chatbot, state])
    
# Run it!
if __name__ == "__main__":
    demo.launch()
