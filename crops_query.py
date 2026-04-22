
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("crops_query.json")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search(data, query):
    q = query.lower()
    results = []
    for r in data["records"]:
        if any(q in str(v).lower() for v in [
            r.get("id",""),
            r.get("slug",""),
            r.get("common_name",""),
            r.get("scientific_name","") or "",
            r.get("category",""),
            r.get("subcategory","")
        ]):
            results.append(r)
    return results

def main():
    data = load_data()

    if len(sys.argv) < 2:
        print("Usage: python crops_query.py <search_term>")
        return

    query = sys.argv[1]
    results = search(data, query)

    print(f"\nResults for '{query}' ({len(results)} found):\n")
    for r in results[:10]:  # limit output
        print(f"- {r['common_name']} ({r['scientific_name']}) | base:{r['temperature']['base_c']}°C upper:{r['temperature']['upper_c']}°C")

if __name__ == "__main__":
    main()
