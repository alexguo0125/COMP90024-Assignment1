#Changelog
#Row 65 & 74: count en-us differently (not using '''code = lang.split("-")[0].lower()''')
#adding "Byte-offset parallelism" for file chunking, so each process can read from different part of the file

import time
import os
from mpi4py import MPI
import json
import itertools
from collections import Counter

#list possible top languages
LANG_NAMES = {
    'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish',
    'zh': 'Chinese', 'ja': 'Japanese', 'pt': 'Portuguese', 'it': 'Italian',
    'nl': 'Dutch', 'ru': 'Russian', 'sv': 'Swedish', 'fi': 'Finnish',
    'pl': 'Polish', 'ar': 'Arabic', 'ko': 'Korean', 'tr': 'Turkish',
    'uk': 'Ukrainian', 'th': 'Thai', 'nb': 'Norwegian', 'da': 'Danish',
    'ca': 'Catalan', 'is': 'Icelandic', 'lt': 'Lithuanian', 'eo': 'Esperanto',
    'el': 'Greek', 'hu': 'Hungarian', 'cs': 'Czech', 'ro': 'Romanian',
    'yi': 'Yiddish', 'ak': 'Akan', 'hy': 'Armenian', 'sc': 'Sardinian', 'en-au': 'English', 'zh-cn': 'Chinese'
}

#import
local_bluesky = 'datasets/bluesky-medium.ndjson'
cluster_bluesky = 'bluesky-large.ndjson'
bluesky_path = local_bluesky if os.path.exists(local_bluesky) else cluster_bluesky

local_mastodon = 'datasets/mastodon-medium.ndjson'
cluster_mastodon = 'mastodon-large.ndjson'
mastodon_path = local_mastodon if os.path.exists(local_mastodon) else cluster_mastodon

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#setup time & counter
start_time = time.time()

bluesky_counter = Counter()
mastodon_counter = Counter()

bluesky_no_lang = 0
mastodon_no_lang = 0
bluesky_bad_json = 0
mastodon_bad_json = 0

#Loop counting, data handling using parallelism
for source, path in [("bluesky", bluesky_path), ("mastodon", mastodon_path)]:
    #rank logic
    file_size = os.path.getsize(path)
    chunk_size = file_size // size
    start_offset = rank * chunk_size
    end_offset = (rank + 1) * chunk_size if rank < size - 1 else file_size

    with open(path, 'rb') as f:
        f.seek(start_offset)
        '''if not the first rank, skip the first partial line (it belongs to the previous rank)'''
        if rank > 0:
            f.readline()

        while f.tell() < end_offset:
            line = f.readline()
            if not line:
                break
            
            '''ill formatted json handling'''
            try:
                rec = json.loads(line.decode('utf-8'))
            except json.JSONDecodeError:
                if source == "bluesky":
                   bluesky_bad_json += 1
                else:
                    mastodon_bad_json += 1
                continue

            '''null language'''
            if source == "bluesky":
                langs = rec.get("record", {}).get("langs", [])
                if not langs:
                    bluesky_no_lang += 1
                for lang in langs:
                    code = lang.strip().lower()
                    if code:
                        bluesky_counter[code] += 1

            elif source == "mastodon":
                lang = rec.get("doc", {}).get("language")
                if not lang:
                    mastodon_no_lang += 1
                if lang:
                    code = lang.strip().lower()
                    if code:
                        mastodon_counter[code] += 1

#Gather and final count
all_bluesky = comm.gather(bluesky_counter, root=0)
all_mastodon = comm.gather(mastodon_counter, root=0)
all_bs_nolang = comm.gather(bluesky_no_lang, root=0)
all_ms_nolang = comm.gather(mastodon_no_lang, root=0)
all_bs_badjson = comm.gather(bluesky_bad_json, root=0)
all_ms_badjson = comm.gather(mastodon_bad_json, root=0)

if rank == 0:
    final_bluesky = Counter()
    for c in all_bluesky:
        final_bluesky.update(c)

    final_mastodon = Counter()
    for c in all_mastodon:
        final_mastodon.update(c)

#count bad json & no language
    print(f"\nBluesky  — Bad JSON: {sum(all_bs_badjson):,} | No language: {sum(all_bs_nolang):,}")
    print(f"Mastodon — Bad JSON: {sum(all_ms_badjson):,} | No language: {sum(all_ms_nolang):,}")

#Time end + print time taken
    elapsed = time.time() - start_time
    print(f"\nTime taken: {elapsed:.4f} seconds\n")

#Print Formatting
    print(f"{'':=<90}")
    print(f"{'#':<5}{'Mastodon Languages':<20}{'Frequency of':<25}{'BlueSky Languages':<20}{'Frequency of':<20}")
    print(f"{'':5}{'Used':<20}{'Occurrence (#posts)':<25}{'Used':<20}{'Occurrence (#posts)':<20}")
    print(f"{'':=<90}")
    mas = final_mastodon.most_common(10)
    sky = final_bluesky.most_common(10)
    for i, ((ml, mc), (sl, sc)) in enumerate (itertools.zip_longest(mas, sky, fillvalue=("", 0)), 1):
        mname = f"{ml.title()} ({LANG_NAMES.get(ml, '?')})" if ml else ""
        sname = f"{sl.title()} ({LANG_NAMES.get(sl, '?')})" if sl else ""
        mcount = f"{mc:,}" if mc else ""
        scount = f"{sc:,}" if sc else ""
        print(f"{i:<5}{mname:<20}{mcount:<25}{sname:<20}{scount}")
    print(f"{'':=<90}")