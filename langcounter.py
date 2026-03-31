from mpi4py import MPI
import json
from collections import Counter

bluesky_path = 'datasets/bluesky-small.ndjson'
mastodon_path = 'datasets/mastodon-small.ndjson'

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

bluesky_counter = Counter()
mastodon_counter = Counter()

for source, path in [("bluesky", bluesky_path), ("mastodon", mastodon_path)]:
    with open(path, 'r') as f:
        for line in f:
            rec = json.loads(line)
            if source == "bluesky":
                langs = rec.get("record", {}).get("langs", [])
                for lang in langs:
                    bluesky_counter[lang.split("-")[0]] += 1
            elif source == "mastodon":
                lang = rec.get("doc", {}).get("language")
                if lang:
                    mastodon_counter[lang.split("-")[0]] += 1

print("Bluesky:", bluesky_counter.most_common(20))
print("Mastodon:", mastodon_counter.most_common(20))