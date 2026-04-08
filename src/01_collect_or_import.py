"""
01_collect_or_import.py
Imports or reads the raw review dataset for the Headspace app.

This script documents how reviews were originally collected from the Google
Play Store using the google-play-scraper library and stored in
data/reviews_raw.jsonl. Because the pre-collected file already exists in
the repository, this script verifies the file and prints summary statistics
rather than re-scraping (which would require network access and a specific
scraper version).

To re-collect from scratch, install the scraper:
    pip install google-play-scraper

Then uncomment and adapt the SCRAPING section below.

Input : (none — reads from data/reviews_raw.jsonl if it exists)
Output: prints dataset summary stats
"""

import json
import os
from collections import Counter


# ---------------------------------------------------------------------------
# SCRAPING  (commented out — the pre-collected file is committed to the repo)
# ---------------------------------------------------------------------------
# from google_play_scraper import reviews, Sort
#
# APP_ID = "com.getsomeheadspace.android"
# MAX_REVIEWS = 5000
# LANG = "en"
# COUNTRY = "us"
#
# def scrape_reviews():
#     result, _ = reviews(
#         APP_ID,
#         lang=LANG,
#         country=COUNTRY,
#         sort=Sort.NEWEST,
#         count=MAX_REVIEWS,
#     )
#     raw_path = os.path.join("data", "reviews_raw.jsonl")
#     with open(raw_path, "w", encoding="utf-8") as f:
#         for i, rev in enumerate(result, start=1):
#             record = {
#                 "id":     f"rev_{i:03d}",
#                 "text":   rev["content"],
#                 "rating": rev["score"],
#                 "date":   rev["at"].strftime("%Y-%m-%d"),
#             }
#             f.write(json.dumps(record) + "\n")
#     print(f"Scraped {len(result)} reviews to {raw_path}")
# ---------------------------------------------------------------------------


def summarise_raw():
    raw_path = os.path.join("data", "reviews_raw.jsonl")
    if not os.path.isfile(raw_path):
        print(f"ERROR: {raw_path} not found. Run the scraper or restore the file.")
        return

    records = []
    with open(raw_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if not records:
        print("reviews_raw.jsonl is empty.")
        return

    rating_counts = Counter(r["rating"] for r in records)
    dates = [r["date"] for r in records]

    print(f"Raw dataset summary — data/reviews_raw.jsonl")
    print(f"  Total reviews : {len(records)}")
    print(f"  Date range    : {min(dates)} to {max(dates)}")
    print(f"  Rating dist.  :", dict(sorted(rating_counts.items())))


if __name__ == "__main__":
    summarise_raw()