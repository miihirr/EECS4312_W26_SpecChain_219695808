"""
08_metrics.py
Computes and writes metrics for all three pipelines.

Metrics computed per pipeline:
  - dataset_size         : total lines in reviews_clean.jsonl
  - persona_count        : number of personas
  - requirements_count   : number of ## Requirement ID: headers in spec
  - tests_count          : number of test objects in tests JSON
  - traceability_links   : group→persona + persona→req + test→req references
  - review_coverage      : unique review IDs across groups / dataset_size
  - traceability_ratio   : reqs with a Source Persona citation / total reqs
  - testability_rate     : reqs that have ≥1 test / total reqs
  - ambiguity_ratio      : reqs containing vague terms / total reqs

Usage:
    python src/08_metrics.py

Writes:
    metrics/metrics_manual.json
    metrics/metrics_auto.json
    metrics/metrics_hybrid.json
    metrics/metrics_summary.json
"""

import json
import os
import re

VAGUE_TERMS = re.compile(
    r"\b(fast|quickly|easy|easily|intuitive|user.friendly|better|good|"
    r"nice|seamless|smooth|simple|convenient|efficient|effectively|"
    r"reasonable|appropriate|sufficient)\b",
    re.IGNORECASE,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(*parts):
    return os.path.join(BASE, *parts)


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------

def count_clean_reviews() -> int:
    p = _path("data", "reviews_clean.jsonl")
    if not os.path.isfile(p):
        return 0
    with open(p, encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def load_json(path: str):
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def count_personas(path: str) -> int:
    data = load_json(path)
    if data is None:
        return 0
    return len(data.get("personas", []))


def unique_reviews_in_groups(path: str) -> set:
    data = load_json(path)
    if data is None:
        return set()
    ids = set()
    for g in data.get("groups", []):
        ids.update(g.get("review_ids", []))
    return ids


def count_traceability_links(groups_path: str, personas_path: str, tests_path: str) -> int:
    """
    Count explicit traceability links:
      - group → persona  (1 link per persona that references a group)
      - persona → req    (1 per persona, since each req has a Source Persona)
      - test → req       (1 link per test object)
    """
    links = 0
    personas_data = load_json(personas_path)
    if personas_data:
        for p in personas_data.get("personas", []):
            if p.get("derived_from_group"):
                links += 1
        # persona → req (proxy: 1 per persona)
        links += len(personas_data.get("personas", []))
    # test → req
    tests_data = load_json(tests_path)
    if tests_data:
        tests = tests_data if isinstance(tests_data, list) else tests_data.get("tests", [])
        if isinstance(tests, list):
            links += len(tests)
    return links


def parse_spec(path: str):
    """Return (requirements_count, ambiguity_count, reqs_with_persona_count)."""
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        return 0, 0, 0
    with open(path, encoding="utf-8") as f:
        text = f.read()
    req_blocks = re.split(r"(?=^## Requirement ID:)", text, flags=re.MULTILINE)
    req_blocks = [b for b in req_blocks if b.strip().startswith("## Requirement ID:")]
    total = len(req_blocks)
    ambiguous = sum(1 for b in req_blocks if VAGUE_TERMS.search(b))
    with_persona = sum(1 for b in req_blocks if re.search(r"Source Persona\s*:", b))
    return total, ambiguous, with_persona


def count_tests(path: str) -> int:
    data = load_json(path)
    if data is None:
        return 0
    if isinstance(data, list):
        return len(data)
    return len(data.get("tests", []))


def reqs_with_tests(spec_path: str, tests_path: str) -> tuple:
    """Return (reqs_covered_by_tests, total_reqs)."""
    if not os.path.isfile(spec_path):
        return 0, 0
    with open(spec_path, encoding="utf-8") as f:
        text = f.read()
    req_ids = re.findall(r"^## Requirement ID:\s*(\S+)", text, re.MULTILINE)
    total = len(req_ids)
    if total == 0:
        return 0, 0
    tests_data = load_json(tests_path)
    if tests_data is None:
        return 0, total
    tests = tests_data if isinstance(tests_data, list) else tests_data.get("tests", [])
    referenced = {t.get("requirement_id") for t in tests if t.get("requirement_id")}
    covered = sum(1 for r in req_ids if r in referenced)
    return covered, total


# ---------------------------------------------------------------------------
# Per-pipeline computation
# ---------------------------------------------------------------------------

def compute_metrics(pipeline: str) -> dict:
    suffix = "auto" if pipeline == "automated" else pipeline
    groups_path   = _path("data",     f"review_groups_{suffix}.json")
    personas_path = _path("personas", f"personas_{suffix}.json")
    spec_path     = _path("spec",     f"spec_{suffix}.md")
    tests_path    = _path("tests",    f"tests_{suffix}.json")

    dataset_size    = count_clean_reviews()
    persona_count   = count_personas(personas_path)
    unique_reviews  = unique_reviews_in_groups(groups_path)
    review_coverage = round(len(unique_reviews) / dataset_size, 4) if dataset_size else 0.0

    req_count, ambiguous_count, with_persona = parse_spec(spec_path)
    tests_count        = count_tests(tests_path)
    traceability_links = count_traceability_links(groups_path, personas_path, tests_path)
    traceability_ratio = round(with_persona / req_count, 4) if req_count else 0.0
    covered, total_r   = reqs_with_tests(spec_path, tests_path)
    testability_rate   = round(covered / total_r, 4) if total_r else 0.0
    ambiguity_ratio    = round(ambiguous_count / req_count, 4) if req_count else 0.0

    return {
        "pipeline":           pipeline,
        "dataset_size":       dataset_size,
        "persona_count":      persona_count,
        "requirements_count": req_count,
        "tests_count":        tests_count,
        "traceability_links": traceability_links,
        "review_coverage":    review_coverage,
        "traceability_ratio": traceability_ratio,
        "testability_rate":   testability_rate,
        "ambiguity_ratio":    ambiguity_ratio,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pipelines = ["manual", "automated", "hybrid"]
    results = {}

    for pipeline in pipelines:
        print(f"Computing metrics for: {pipeline}")
        m = compute_metrics(pipeline)
        results[pipeline] = m

        suffix = "auto" if pipeline == "automated" else pipeline
        out_path = _path("metrics", f"metrics_{suffix}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=2)
        print(f"  Written: {out_path}")

    summary = {
        "app":          "Headspace",
        "dataset_size": results["manual"]["dataset_size"],
        "manual":       results["manual"],
        "automated":    results["automated"],
        "hybrid":       results["hybrid"],
    }
    summary_path = _path("metrics", "metrics_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written: {summary_path}")

    print("\n--- Metrics Summary ---")
    header = f"{'Metric':<25} {'Manual':>10} {'Auto':>10} {'Hybrid':>10}"
    print(header)
    print("-" * len(header))
    keys = [
        "requirements_count", "tests_count", "traceability_links",
        "review_coverage", "traceability_ratio", "testability_rate", "ambiguity_ratio",
    ]
    for k in keys:
        row = (
            f"{k:<25} {results['manual'][k]:>10} "
            f"{results['automated'][k]:>10} {results['hybrid'][k]:>10}"
        )
        print(row)


if __name__ == "__main__":
    main()