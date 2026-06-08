import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("ucla_dining")

test_queries = [
    "What dining hall is known for healthy food at UCLA?",
    "What is De Neve Late Night and when does it run?",
    "Is the UCLA meal plan worth it for off campus students?",
]

for query in test_queries:
    print(f"\nQUERY: {query}")
    print("-" * 60)
    embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=5)

    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"\n[Result {i+1}] distance={dist:.3f} source={meta['source_file']}")
        print(doc[:300])
        print("...")