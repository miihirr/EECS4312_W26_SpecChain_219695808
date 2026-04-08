"""
run_all.py
Runs the full automated SpecChain pipeline end-to-end.

Steps executed (automated pipeline only):
  1. Validate repository structure         (00_validate_repo.py)
  2. Clean reviews                         (02_clean.py)
  3. Auto review grouping + personas       (05_personas_auto.py)
  4. Auto spec generation                  (06_spec_generate.py)
  5. Auto test generation                  (07_tests_generate.py)
  6. Compute metrics for all pipelines     (08_metrics.py)

Manual and hybrid artifacts are expected to already exist.

Usage:
    python src/run_all.py           # skip steps whose outputs exist
    python src/run_all.py --force   # force regeneration of automated artifacts

Requirements:
    pip install groq
    export GROQ_API_KEY="your-key-here"
"""

import argparse
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, "src")


def run(script: str, extra_args: list = None, fatal: bool = True) -> bool:
    """Run a Python script within the repo src/ directory."""
    cmd = [sys.executable, os.path.join(SRC, script)] + (extra_args or [])
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BASE)
    if result.returncode != 0 and fatal:
        print(f"ERROR: {script} failed (exit code {result.returncode}).", file=sys.stderr)
        sys.exit(result.returncode)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run the full SpecChain automated pipeline")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate automated artifacts even if they already exist")
    args = parser.parse_args()

    force_flag = ["--force"] if args.force else []

    print("=" * 55)
    print("SpecChain — Full Automated Pipeline")
    print("App: Headspace (com.getsomeheadspace.android)")
    print("=" * 55)

    # Step 1: Validate
    run("00_validate_repo.py", fatal=False)

    # Step 2: Clean reviews
    run("02_clean.py")

    # Step 3: Auto grouping + persona generation
    run("05_personas_auto.py", extra_args=force_flag)

    # Step 4: Auto spec generation
    run("06_spec_generate.py", extra_args=["--pipeline", "auto"] + force_flag)

    # Step 5: Auto test generation
    run("07_tests_generate.py", extra_args=["--pipeline", "auto"] + force_flag)

    # Step 6: Metrics for all pipelines
    run("08_metrics.py")

    print("\n" + "=" * 55)
    print("Pipeline complete.")
    print("Review outputs in metrics/metrics_summary.json")
    print("=" * 55)


if __name__ == "__main__":
    main()