import json

# Load catalog
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

def retrieve(query, k=5):

    query = query.lower()

    scored = []

    for item in catalog:

        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            item.get("test_type", "")
        ).lower()

        score = 0

        for word in query.split():
            if word in text:
                score += 1

        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = [item for score, item in scored if score > 0]

    return results[:k]