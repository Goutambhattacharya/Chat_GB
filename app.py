from flask import Flask, request, jsonify
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("sk-proj-5iZMEE8fLmyOxEU3czDfiq7Syzt_jbcb_UYIEUYVhJuHX8HOvwfRHZW9NAGy5HJg_vkCvU9ronT3BlbkFJnvIJyHVb49cTkYqnqIQHTrpXVweeePenDMgIvtf74jwd-gXxipMVoaxCNyeRqU-yeMcQV-reIAKEY")

app = Flask(__name__)

# Load and chunk your document
with open("your_doc.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(raw_text)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(chunks, embedding=embeddings)

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get("message")
    docs = db.similarity_search(user_query)
    context = "\n".join([doc.page_content for doc in docs])
    
    prompt = f"Use the below context to answer the question.\n\nContext:\n{context}\n\nQuestion: {user_query}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({"response": response['choices'][0]['message']['content']})

if __name__ == "__main__":
    app.run(debug=True)
