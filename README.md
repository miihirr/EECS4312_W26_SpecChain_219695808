# EECS4312_W26_SpecChain

**Author:** Mihirkumar Patel
**Student ID:** 219695808
**Course:** EECS 4312 — Software Requirements Engineering (Winter 2026)

## Application
**Headspace** (com.getsomeheadspace.android) — meditation, sleep, and mindfulness mobile app (Google Play Store)

## Data Collection
Reviews were sampled from Google Play Store listings for the Headspace app.
Collection method: manual export / import (API rate limits restricted live scraping).
Date range: 2024-01-03 to 2024-03-25.

## Dataset
- `data/reviews_raw.jsonl` — 200 raw collected reviews
- `data/reviews_clean.jsonl` — 200 cleaned reviews (NLP-preprocessed)
- Cleaning steps: lowercase, punctuation removal, stopword filtering,
  rule-based lemmatisation, deduplication

## Repository Structure
```
data/        datasets and review groups (raw, clean, manual, auto, hybrid)
personas/    persona files for each pipeline
spec/        requirements specifications (manual, auto, hybrid)
tests/       acceptance test scenarios (JSON)
metrics/     computed metrics per pipeline + summary
prompts/     Groq LLM prompt templates
src/         executable Python scripts
reflection/  final written reflection
```

## Pipelines
| Pipeline  | Groups      | Personas    | Requirements        | Tests |
|-----------|-------------|-------------|---------------------|-------|
| Manual    | 5 (G1-G5)  | 5 (P1-P5)  | 14 (FR1-FR14)       | 28    |
| Automated | 5 (A1-A5)  | 5 (PA1-PA5)| 12 (FR_auto_1-12)   | 24    |
| Hybrid    | 5 (H1-H5)  | 5 (PH1-PH5)| 14 (FR_hybrid_1-14) | 28    |

## How to Run

### Prerequisites
```bash
python -m venv .venv && source .venv/bin/activate
pip install groq
export GROQ_API_KEY="your-key-here"
```

### Validate the repository
```bash
python src/00_validate_repo.py
```

### Re-run the cleaning pipeline
```bash
python src/02_clean.py
```

### Inspect manual pipeline artefacts
```bash
python src/03_manual_coding_template.py   # coding instructions + group stats
python src/04_personas_manual.py          # validate manual personas
```

### Run the full automated pipeline end-to-end
```bash
python src/run_all.py          # skips steps whose outputs already exist
python src/run_all.py --force  # force regeneration via Groq API
```

### Run automated pipeline steps individually
```bash
python src/05_personas_auto.py          # Groq: group reviews + generate personas
python src/06_spec_generate.py          # Groq: generate spec from personas
python src/07_tests_generate.py         # Groq: generate tests from spec
python src/08_metrics.py                # compute + write all metrics
```

### View results
```bash
cat metrics/metrics_summary.json
```

## Metrics Summary
| Metric             | Manual | Automated | Hybrid |
|--------------------|--------|-----------|--------|
| Requirements       | 14     | 12        | 14     |
| Tests              | 28     | 24        | 28     |
| Traceability ratio | 1.00   | 1.00      | 1.00   |
| Testability rate   | 1.00   | 1.00      | 1.00   |
| Ambiguity ratio    | 0.071  | 0.000     | 0.071  |
| Review coverage    | 0.375  | 0.375     | 0.375  |

## Notes
- The automated pipeline requires a valid `GROQ_API_KEY` (Groq cloud API).
- Pre-committed artefacts in `data/`, `personas/`, `spec/`, and `tests/`
  allow grading without re-running the API.
- Use `--force` flags on scripts 05-07 to regenerate from the API.
- LLM model used: `meta-llama/llama-4-scout-17b-16e-instruct` via Groq.
