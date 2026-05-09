import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

for item in catalog:
    texts.append(item["name"])

embeddings = model.encode(texts)

dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "shl.index")

print("FAISS index created")