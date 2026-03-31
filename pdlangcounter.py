import pandas as pd
import time
import os

# File paths
bluesky_path = 'datasets/bluesky-small.ndjson'
mastodon_path = 'datasets/mastodon-small.ndjson'

start_time = time.time()

df_bs = pd.read_json(bluesky_path, lines=True)

all_bs_langs = df_bs['record'].apply(lambda x: [l.strip().lower() 
    for l in x.get('langs', [])] if isinstance(x, dict) else []).explode()
bs_counts = all_bs_langs.value_counts()

df_ms = pd.read_json(mastodon_path, lines=True)

all_ms_langs = df_ms['doc'].apply(lambda x: x.get('language').strip().lower() 
    if isinstance(x, dict) and isinstance(x.get('language'), str) else None).dropna()
ms_counts = all_ms_langs.value_counts()

end_time = time.time()

print("=== Top 10 BlueSky Languages (Pandas) ===")
print(bs_counts.head(10))
print("\n=== Top 10 Mastodon Languages (Pandas) ===")
print(ms_counts.head(10))

print(f"\nTotal Time (Pandas): {end_time - start_time:.4f} seconds")