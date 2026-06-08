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

def ask(question, k=5):
    embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=k)

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    # filter out weak matches
    filtered = [(doc, meta) for doc, meta, dist in zip(docs, metas, distances) if dist < 0.7]

    if not filtered:
        return {
            "answer": "I don't have enough information in my documents to answer that.",
            "sources": []
        }

    context = ""
    for i, (doc, meta) in enumerate(filtered):
        context += f"[Document {i+1}: {meta['source_file']}]\n{doc}\n\n"

    prompt = f"""You are an assistant that answers questions about UCLA campus dining.

Use ONLY the documents provided below to answer. Do not use any outside knowledge.
If the documents do not contain enough information to answer confidently, say exactly:
"I don't have enough information in my documents to answer that."

For every claim in your answer, say which document it came from using the label like (Document 1) or (Document 3).

Documents:
{context}

Question: {question}

Answer:"""

    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )

    answer = response.choices[0].message.content.strip()
    sources = list({meta["source_url"] for _, meta in filtered})

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Question: ")
    result = ask(q)
    print(result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print(f"  {s}")