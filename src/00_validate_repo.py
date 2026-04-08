"""
00_validate_repo.py
Checks whether all required folders and files exist in the repository.
Prints a clear status message for each required item and exits with a
non-zero code if any required file is missing.

Usage:
    python src/00_validate_repo.py
"""

import os
import sys

REQUIRED = [
    # data
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",
    # personas
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",
    # specs
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",
    # tests
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",
    # metrics
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_summary.json",
    # prompts
    "prompts/prompt_auto.json",
    # src scripts
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/03_manual_coding_template.py",
    "src/04_personas_manual.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",
    # docs
    "README.md",
    "reflection/reflection.md",
]


def main():
    print("Checking repository structure...")
    missing = []
    for path in REQUIRED:
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            print(f"  [OK]      {path}")
        elif os.path.isfile(path):
            print(f"  [EMPTY]   {path}  <-- file exists but is empty")
            missing.append(path)
        else:
            print(f"  [MISSING] {path}")
            missing.append(path)

    print()
    if missing:
        print(f"Repository validation FAILED — {len(missing)} file(s) missing or empty:")
        for m in missing:
            print(f"    {m}")
        sys.exit(1)
    else:
        print("Repository validation complete — all required files found.")


if __name__ == "__main__":
    main()