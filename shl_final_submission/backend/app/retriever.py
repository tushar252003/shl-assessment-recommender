import json

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

def retrieve(query, k=5):

    query = query.lower().strip()

    scored = []

    for item in catalog:

        searchable_text = (
            item.get("name", "") + " " +
            item.get("test_type", "") + " " +
            " ".join(item.get("tags", []))
        ).lower()

        searchable_words = searchable_text.split()

        score = 0

        for word in query.split():

            if word in searchable_words:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    results = [item for score, item in scored[:k]]

    return results