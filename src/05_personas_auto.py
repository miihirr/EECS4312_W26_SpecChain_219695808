"""
05_personas_auto.py
Automated review-grouping and persona-generation pipeline using Groq LLM.

Steps:
  1. Load cleaned reviews from data/reviews_clean.jsonl
  2. Call Groq API to cluster reviews into thematic groups
     → writes data/review_groups_auto.json
  3. Call Groq API to generate a persona for each group
     → writes personas/personas_auto.json

Requirements:
    pip install groq
    export GROQ_API_KEY="your-key-here"

Usage:
    python src/05_personas_auto.py            # skips if outputs already exist
    python src/05_personas_auto.py --force    # overwrites existing outputs

Model: meta-llama/llama-4-scout-17b-16e-instruct
"""

import argparse
import json
import os
import sys

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
BASE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(*parts):
    return os.path.join(BASE, *parts)


def load_clean_reviews(n: int = 75) -> list[dict]:
    """Load the first *n* cleaned reviews (keep prompt within token budget)."""
    path = _path("data", "reviews_clean.jsonl")
    reviews = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reviews.append(json.loads(line))
            if len(reviews) >= n:
                break
    return reviews


def load_prompts() -> dict:
    path = _path("prompts", "prompt_auto.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def call_groq(client, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system",  "content": system},
            {"role": "user",    "content": user},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    return response.choices[0].message.content.strip()


def extract_json_block(text: str):
    """Extract the first JSON object or array from a potentially prose-wrapped response."""
    import re
    # Try fenced code block first
    m = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if m:
        return json.loads(m.group(1).strip())
    # Try raw JSON starting with { or [
    m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if m:
        return json.loads(m.group(1))
    raise ValueError(f"No JSON found in response:\n{text[:500]}")


# ---------------------------------------------------------------------------
# Step 1: Review grouping
# ---------------------------------------------------------------------------

def group_reviews(client, reviews: list[dict], prompts: dict) -> dict:
    """Ask the LLM to cluster reviews, return groups JSON."""
    review_list = "\n".join(
        f"[{r['id']}] (rating={r.get('rating','?')}) {r['text'][:200]}"
        for r in reviews
    )
    system = prompts["review_grouping_prompt"]["system"]
    user   = prompts["review_grouping_prompt"]["user_template"].format(
        reviews=review_list
    )
    raw = call_groq(client, system, user)
    data = extract_json_block(raw)
    if isinstance(data, list):
        return {"groups": data}
    return data


# ---------------------------------------------------------------------------
# Step 2: Persona generation
# ---------------------------------------------------------------------------

def generate_personas(client, groups: dict, prompts: dict) -> dict:
    """Ask the LLM to create a persona per group."""
    groups_json = json.dumps(groups, indent=2)
    system = prompts["persona_generation_prompt"]["system"]
    user   = prompts["persona_generation_prompt"]["user_template"].format(
        groups=groups_json
    )
    raw = call_groq(client, system, user)
    data = extract_json_block(raw)
    if isinstance(data, list):
        return {"personas": data}
    return data


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Automated persona generation (Groq)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()

    groups_out   = _path("data",     "review_groups_auto.json")
    personas_out = _path("personas", "personas_auto.json")

    if not args.force:
        if os.path.isfile(groups_out) and os.path.isfile(personas_out):
            print("Outputs already exist. Use --force to regenerate.")
            print(f"  {groups_out}")
            print(f"  {personas_out}")
            return

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    try:
        from groq import Groq  # type: ignore
    except ImportError:
        print("ERROR: groq package not installed. Run: pip install groq", file=sys.stderr)
        sys.exit(1)

    client  = Groq(api_key=api_key)
    prompts = load_prompts()
    reviews = load_clean_reviews(n=75)
    print(f"Loaded {len(reviews)} reviews for automated pipeline.")

    print("Step 1: Grouping reviews via Groq...")
    groups = group_reviews(client, reviews, prompts)
    with open(groups_out, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)
    print(f"  Written: {groups_out}  ({len(groups.get('groups', []))} groups)")

    print("Step 2: Generating personas via Groq...")
    personas = generate_personas(client, groups, prompts)
    with open(personas_out, "w", encoding="utf-8") as f:
        json.dump(personas, f, indent=2)
    print(f"  Written: {personas_out}  ({len(personas.get('personas', []))} personas)")

    print("Done.")


if __name__ == "__main__":
    main()