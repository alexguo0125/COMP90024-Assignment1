from mpi4py import MPI
import json
import sys
from collections import Counter

def extract_languages(line, platform):
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None

    if platform == "mastodon":
        lang = data.get("doc", {}).get("language")
        if isinstance(lang, str) and lang.strip():
            return [lang.strip().lower()]
        return []

    elif platform == "bluesky":
        langs = data.get("record", {}).get("langs", [])
        if isinstance(langs, list):
            clean_langs = []
            for lang in langs:
                if isinstance(lang, str) and lang.strip():
                    clean_langs.append(lang.strip().lower())
            return list(set(clean_langs))
        return []

    return []

def count_languages_parallel(filename, platform, comm):
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_counts = Counter()
    local_bad_json = 0
    local_missing_lang = 0

    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i % size != rank:
                continue

            langs = extract_languages(line, platform)

            if langs is None:
                local_bad_json += 1
                continue

            if not langs:
                local_missing_lang += 1
                continue

            for lang in langs:
                local_counts[lang] += 1

    all_counts = comm.gather(local_counts, root=0)
    all_bad_json = comm.gather(local_bad_json, root=0)
    all_missing_lang = comm.gather(local_missing_lang, root=0)

    if rank == 0:
        total_counts = Counter()
        for c in all_counts:
            total_counts.update(c)

        total_bad_json = sum(all_bad_json)
        total_missing_lang = sum(all_missing_lang)

        return total_counts, total_bad_json, total_missing_lang

    return None, None, None

def print_results(title, counts, bad_json, missing_lang):
    print(f"\n===== {title} =====")
    print(f"Bad JSON lines: {bad_json}")
    print(f"Missing/empty language entries: {missing_lang}")
    print("Language counts:")

    for lang, count in counts.most_common():
        print(f"{lang}: {count}")

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if len(sys.argv) != 3:
        if rank == 0:
            print("Usage: python lang_count_mpi.py <mastodon_file> <bluesky_file>")
        sys.exit(1)

    mastodon_file = sys.argv[1]
    bluesky_file = sys.argv[2]

    start = MPI.Wtime()

    mastodon_counts, mastodon_bad_json, mastodon_missing = count_languages_parallel(mastodon_file, "mastodon", comm)
    comm.Barrier()
    bluesky_counts, bluesky_bad_json, bluesky_missing = count_languages_parallel(bluesky_file, "bluesky", comm)

    end = MPI.Wtime()

    if rank == 0:
        print_results("Mastodon", mastodon_counts, mastodon_bad_json, mastodon_missing)
        print_results("BlueSky", bluesky_counts, bluesky_bad_json, bluesky_missing)
        print(f"\nTotal runtime: {end - start:.6f} seconds")

if __name__ == "__main__":
    main()