"""
04_personas_manual.py
Validates and summarises the manually constructed personas.

This script reads data/review_groups_manual.json and
personas/personas_manual.json, then verifies that:
  - Each review group has a corresponding persona.
  - Each persona references a valid review group.
  - Each persona has all required fields populated.
  - Each evidence review ID exists in reviews_clean.jsonl.

Usage:
    python src/04_personas_manual.py

Output: validation report printed to stdout.
"""

import json
import os


REQUIRED_PERSONA_FIELDS = [
    "id", "name", "description", "derived_from_group",
    "goals", "pain_points", "context", "constraints", "evidence_reviews",
]


def load_jsonl_ids(path: str) -> set:
    ids = set()
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    ids.add(json.loads(line)["id"])
    return ids


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_personas():
    groups_path  = os.path.join("data", "review_groups_manual.json")
    personas_path = os.path.join("personas", "personas_manual.json")
    clean_path   = os.path.join("data", "reviews_clean.jsonl")

    for p in [groups_path, personas_path]:
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            print(f"ERROR: {p} is missing or empty.")
            return

    groups_data  = load_json(groups_path)
    personas_data = load_json(personas_path)
    clean_ids    = load_jsonl_ids(clean_path)

    group_ids = {g["group_id"] for g in groups_data.get("groups", [])}
    personas  = personas_data.get("personas", [])

    print("Manual Personas Validation Report")
    print("=" * 45)

    errors = 0

    for persona in personas:
        pid = persona.get("id", "?")
        print(f"\nPersona {pid} — {persona.get('name', '?')}")

        # Check required fields
        for field in REQUIRED_PERSONA_FIELDS:
            val = persona.get(field)
            if not val:
                print(f"  [FAIL] Missing field: {field}")
                errors += 1
            else:
                expected_type = list if field in ("goals","pain_points","context","constraints","evidence_reviews") else str
                if not isinstance(val, expected_type):
                    print(f"  [FAIL] Field '{field}' should be {expected_type.__name__}")
                    errors += 1
                elif expected_type == list and len(val) == 0:
                    print(f"  [FAIL] Field '{field}' list is empty")
                    errors += 1
                else:
                    print(f"  [OK]   {field}")

        # Check review group reference
        ref = persona.get("derived_from_group")
        if ref and ref not in group_ids:
            print(f"  [FAIL] derived_from_group '{ref}' not in review_groups_manual.json")
            errors += 1

        # Check evidence review IDs
        if clean_ids:
            for rev_id in persona.get("evidence_reviews", []):
                if rev_id not in clean_ids:
                    print(f"  [WARN] Evidence review '{rev_id}' not found in reviews_clean.jsonl")

    print(f"\n{'='*45}")
    covered_groups = {p.get("derived_from_group") for p in personas}
    missing_personas = group_ids - covered_groups
    if missing_personas:
        print(f"[FAIL] These groups have no persona: {missing_personas}")
        errors += len(missing_personas)
    else:
        print(f"[OK]   All {len(group_ids)} groups have a corresponding persona.")

    print(f"\nTotal personas     : {len(personas)}")
    print(f"Total errors found : {errors}")
    if errors == 0:
        print("Validation PASSED.")
    else:
        print("Validation FAILED — please fix the errors above.")


if __name__ == "__main__":
    validate_personas()