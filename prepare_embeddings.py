from sentence_transformers import SentenceTransformer
import pandas as pd

# Load your restaurant review CSV file
df = pd.read_csv("realistic_restaurant_reviews.csv")
texts = df["Review"].dropna().tolist()  # Make sure 'Review' is the correct column

# Chunking logic
def chunk_texts(texts, size=500, overlap=50):
    chunks = []
    for text in texts:
        for i in range(0, len(text), size - overlap):
            chunks.append(text[i:i + size])
    return chunks

chunks = chunk_texts(texts)

# Load sentence transformer and create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

# Create and save dataframe
df_embed = pd.DataFrame({
    "chunk": chunks,
    "embedding": [",".join(map(str, e)) for e in embeddings]
})

df_embed.to_csv("restaurant_chunks.csv", index=False)
print("✅ restaurant_chunks.csv created.")
