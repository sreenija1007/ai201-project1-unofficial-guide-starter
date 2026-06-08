import json
import chromadb
from sentence_transformers import SentenceTransformer

with open("chunks.json") as f:
    chunks = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("ucla_dining")
except:
    pass

collection = client.create_collection("ucla_dining")

batch_size = 50
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    texts = [c["text"] for c in batch]
    embeddings = model.encode(texts).tolist()
    ids = [f"chunk_{i+j}" for j in range(len(batch))]
    metadatas = [{
        "source_file": c["source_file"],
        "source_url": c["source_url"],
        "source_type": c["source_type"],
    } for c in batch]
    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)
    print(f"ingested {i+len(batch)}/{len(chunks)}")

print("done")