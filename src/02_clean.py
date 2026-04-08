"""
02_clean.py
Cleans the raw review dataset and writes reviews_clean.jsonl.

Cleaning steps applied:
  1. Lowercase all text
  2. Remove punctuation and special characters
  3. Remove emojis and non-ASCII characters
  4. Normalize whitespace
  5. Remove stop words
  6. Lemmatize remaining tokens
  7. Drop reviews whose cleaned text has fewer than 3 tokens (too short)
  8. Drop duplicate cleaned texts (deduplication)

Input : data/reviews_raw.jsonl
Output: data/reviews_clean.jsonl
"""

import json
import re
import os

# ---------------------------------------------------------------------------
# Lightweight stop-word list (no external dependency required)
# ---------------------------------------------------------------------------
STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as",
    "until", "while", "of", "at", "by", "for", "with", "about",
    "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in",
    "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how",
    "all", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than",
    "too", "very", "s", "t", "can", "will", "just", "don", "should",
    "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "also",
    "would", "could", "shall", "may", "might", "must", "need",
    "get", "got", "let", "even",
}

# ---------------------------------------------------------------------------
# Minimal rule-based lemmatiser (covers the most common inflections)
# ---------------------------------------------------------------------------
LEMMA_RULES = [
    (r"ies$", "y"),       # stories -> story
    (r"ves$", "f"),       # loves -> love
    (r"ness$", ""),       # effectiveness -> effective
    (r"ment$", ""),       # improvement -> improve
    (r"ation$", "ate"),   # relaxation -> relaxate
    (r"ing$", ""),        # breathing -> breath
    (r"ingly$", ""),      # surprisingly -> surpris
    (r"ed$", ""),         # crashed -> crash
    (r"er$", ""),         # louder -> loud
    (r"ly$", ""),         # quickly -> quick
    (r"s$", ""),          # crashes -> crash
]

_KEEP_SHORT = {"app", "bug", "ok", "ui", "ux", "mp", "ad", "kb", "gb"}


def lemmatize(token: str) -> str:
    """Apply rule-based lemmatisation."""
    if len(token) <= 3 or token in _KEEP_SHORT:
        return token
    for pattern, replacement in LEMMA_RULES:
        if re.search(pattern, token):
            candidate = re.sub(pattern + "$", replacement, token)
            if len(candidate) >= 2:
                return candidate
    return token


def clean_text(raw: str) -> str:
    """Return a cleaned, preprocessed version of *raw*."""
    # 1. Lowercase
    text = raw.lower()

    # 2. Remove emojis / non-ASCII
    text = text.encode("ascii", errors="ignore").decode()

    # 3. Expand common contractions
    contractions = {
        "can't": "cannot", "won't": "will not", "don't": "do not",
        "doesn't": "does not", "didn't": "did not", "isn't": "is not",
        "aren't": "are not", "wasn't": "was not", "weren't": "were not",
        "hasn't": "has not", "haven't": "have not", "hadn't": "had not",
        "i'm": "i am", "i've": "i have", "i'll": "i will", "i'd": "i would",
        "it's": "it is", "that's": "that is", "there's": "there is",
        "they're": "they are", "we're": "we are", "you're": "you are",
        "he's": "he is", "she's": "she is", "let's": "let us",
    }
    for k, v in contractions.items():
        text = text.replace(k, v)

    # 4. Remove punctuation and special characters (keep spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 5. Normalise whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # 6. Tokenise, remove stop words, lemmatise
    tokens = [
        lemmatize(tok)
        for tok in text.split()
        if tok not in STOP_WORDS and len(tok) > 1
    ]

    return " ".join(tokens)


def main():
    raw_path = os.path.join("data", "reviews_raw.jsonl")
    clean_path = os.path.join("data", "reviews_clean.jsonl")

    seen_texts: set = set()
    written = 0
    skipped_short = 0
    skipped_dup = 0

    with open(raw_path, "r", encoding="utf-8") as fin, \
         open(clean_path, "w", encoding="utf-8") as fout:

        for line in fin:
            line = line.strip()
            if not line:
                continue

            record = json.loads(line)
            cleaned = clean_text(record["text"])

            # Drop if too short after cleaning
            if len(cleaned.split()) < 3:
                skipped_short += 1
                continue

            # Drop near-duplicates
            if cleaned in seen_texts:
                skipped_dup += 1
                continue

            seen_texts.add(cleaned)

            clean_record = {
                "id":     record["id"],
                "text":   cleaned,
                "rating": record["rating"],
                "date":   record["date"],
            }
            fout.write(json.dumps(clean_record) + "\n")
            written += 1

    print(f"Cleaning complete.")
    print(f"  Reviews written : {written}")
    print(f"  Skipped (short) : {skipped_short}")
    print(f"  Skipped (dup)   : {skipped_dup}")
    print(f"  Output          : {clean_path}")


if __name__ == "__main__":
    main()