import json
from collections import Counter

def extract_languages(line, platform):
    data = json.loads(line)

    if platform == "mastodon":
        lang = data.get("doc", {}).get("language")
        if lang is None:
            return []
        return [lang]

    elif platform == "bluesky":
        langs = data.get("record", {}).get("langs", [])
        if isinstance(langs, list):
            return langs
        return []

    return []

def count_languages(filename, platform):
    counts = Counter()

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                langs = extract_languages(line, platform)
                for lang in langs:
                    counts[lang] += 1
            except:
                continue

    return counts

mastodon_result = count_languages("mastodon-small.ndjson", "mastodon")
bluesky_result = count_languages("bluesky-small.ndjson", "bluesky")

print("Mastodon:")
for lang, count in mastodon_result.items():
    print(lang, count)

print("\nBlueSky:")
for lang, count in bluesky_result.items():
    print(lang, count)