import requests
from bs4 import BeautifulSoup
import json

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

html = response.text

with open("debug.html", "w", encoding="utf-8") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")

catalog = []

links = soup.find_all("a", href=True)

for link in links:

    text = link.get_text(strip=True)
    href = link["href"]

    if len(text) > 2 and "product-catalog" in href:

        full_url = href

        if href.startswith("/"):
            full_url = "https://www.shl.com" + href

        catalog.append({
            "name": text,
            "url": full_url,
            "test_type": "A",
            "tags": text.lower().split()
        })

unique = []
seen = set()

for item in catalog:

    if item["url"] not in seen:

        unique.append(item)
        seen.add(item["url"])

with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(unique, f, indent=2)

print(f"Saved {len(unique)} assessments")