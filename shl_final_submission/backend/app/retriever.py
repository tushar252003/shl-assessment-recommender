import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("shl.index")

# Load catalog
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

def retrieve(query, k=5):

    # Convert query into embedding
    embedding = model.encode([query])

    # Search similar vectors
    D, I = index.search(np.array(embedding), k)

    results = []

    for idx in I[0]:

        if idx < len(catalog):
            results.append(catalog[idx])

    return results