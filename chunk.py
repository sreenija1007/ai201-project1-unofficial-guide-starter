import os
import json
import random
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs_dir = "documents"
output_file = "chunks.json"

review_sources = {"reviews"}

def get_splitter(source_type):
    if source_type in review_sources:
        return RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    return RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)

chunks = []

for fname in sorted(os.listdir(docs_dir)):
    if not fname.endswith(".txt"):
        continue

    with open(f"{docs_dir}/{fname}") as f:
        content = f.read()

    lines = content.split("\n")
    source_url = lines[0].replace("source_url: ", "").strip()
    source_type = lines[1].replace("source_type: ", "").strip()
    text = "\n".join(lines[3:]).strip()

    if not text:
        print(f"warning: {fname} is empty after cleaning")
        continue

    splitter = get_splitter(source_type)
    splits = splitter.split_text(text)

    for i, chunk in enumerate(splits):
        if len(chunk.strip()) < 50:
            continue
        chunks.append({
            "text": chunk.strip(),
            "source_file": fname,
            "source_url": source_url,
            "source_type": source_type,
            "chunk_index": i
        })

with open(output_file, "w") as f:
    json.dump(chunks, f, indent=2)

print(f"total chunks: {len(chunks)}")
print("\n--- 5 sample chunks ---")
for c in random.sample(chunks, min(5, len(chunks))):
    print(f"\n[{c['source_file']}]")
    print(c['text'][:300])
    print("...")
