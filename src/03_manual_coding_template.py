"""
03_manual_coding_template.py
Creates or updates the manual coding template and instructions.

This script prints a summary of the current manual review groupings and
displays the structure expected in data/review_groups_manual.json. It is
intended to guide the manual coding step where a human reads through
reviews_clean.jsonl and groups similar reviews by theme.

Usage:
    python src/03_manual_coding_template.py

Output: prints the coding table structure and current group stats.
"""

import json
import os


INSTRUCTIONS = """
MANUAL CODING INSTRUCTIONS
===========================
1. Open data/reviews_clean.jsonl in a text editor or spreadsheet tool.
2. Read through each review and assign it to one of the 5 thematic groups.
3. Each group must contain at least 10 reviews.
4. Update data/review_groups_manual.json using the structure below.
5. For each group, provide:
   - group_id   : unique identifier (G1 ... G5)
   - theme      : a short description of the shared user concern
   - review_ids : list of review IDs from reviews_clean.jsonl
   - example_reviews : 2-3 representative raw text excerpts

SUGGESTED THEMES FOR Headspace APP
------------------------------
G1 — Sleep content quality and sleep-aid experience
G2 — Guided meditation sessions and daily practice
G3 — Subscription pricing, paywalls, and billing
G4 — App crashes, bugs, and technical reliability
G5 — Content variety, personalization, and recommendations

JSON TEMPLATE
-------------
{
  "groups": [
    {
      "group_id": "G1",
      "theme": "...",
      "review_ids": ["rev_001", "rev_002", ...],
      "example_reviews": ["...", "..."]
    }
  ]
}
"""


def print_current_groups():
    path = os.path.join("data", "review_groups_manual.json")
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        print("data/review_groups_manual.json not found or empty.")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\nCURRENT MANUAL REVIEW GROUPS")
    print("=" * 40)
    for g in data.get("groups", []):
        n = len(g.get("review_ids", []))
        print(f"  {g['group_id']} | {n:3d} reviews | {g['theme']}")
    total = sum(len(g.get("review_ids", [])) for g in data.get("groups", []))
    print(f"\n  Total reviews coded: {total}")


if __name__ == "__main__":
    print(INSTRUCTIONS)
    print_current_groups()