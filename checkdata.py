import json

files = {
    "bluesky": "datasets/bluesky-small.ndjson",
    "mastodon": "datasets/mastodon-small.ndjson"
}

for source, path in files.items():
    print(f"\n=== {source.upper()} ===")
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            rec = json.loads(line)
            print("Top-level keys:", rec.keys())
            if source == "mastodon":
                inner = rec.get("doc", {})
            else:
                inner = rec.get("record", {})
            print("Inner 'record' keys:", inner.keys() if isinstance(inner, dict) else type(inner))
            print("lang value:", inner.get("lang") if isinstance(inner, dict) else "N/A")
            print("langs value:", inner.get("langs") if isinstance(inner, dict) else "N/A")
            print("language value:", inner.get("language") if isinstance(inner, dict) else "N/A")
            
            if inner.get("language") is not None:
                print("language value:", inner.get("language"))
                break
