import sys
import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("ucla_dining")
groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def query(question, k=5):
    embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=k)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = ""
    for i, (doc, meta) in enumerate(zip(docs, metas)):
        context += f"[Source {i+1}: {meta['source_file']}]\n{doc}\n\n"

    prompt = f"""Answer the question using only the context below. 
If the context doesn't have enough information, say so instead of guessing.
At the end list which sources you used.

Context:
{context}

Question: {question}"""

    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    print(response.choices[0].message.content)
    print("\nSources used:")
    for i, meta in enumerate(metas):
        print(f"  {i+1}. {meta['source_url']}")

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Question: ")
    query(q)
