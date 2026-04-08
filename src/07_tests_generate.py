"""
07_tests_generate.py
Generates acceptance test scenarios from a requirements specification using Groq LLM.

Reads:
    spec/spec_auto.md   → writes tests/tests_auto.json
    spec/spec_hybrid.md → writes tests/tests_hybrid.json  (if requested)

Usage:
    python src/07_tests_generate.py                  # auto tests only
    python src/07_tests_generate.py --pipeline hybrid
    python src/07_tests_generate.py --pipeline all
    python src/07_tests_generate.py --force          # overwrite existing

Requirements:
    pip install groq
    export GROQ_API_KEY="your-key-here"

Model: meta-llama/llama-4-scout-17b-16e-instruct
"""

import argparse
import json
import os
import re
import sys

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
BASE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(*parts):
    return os.path.join(BASE, *parts)


def load_prompts() -> dict:
    with open(_path("prompts", "prompt_auto.json"), encoding="utf-8") as f:
        return json.load(f)


def call_groq(client, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.2,
        max_tokens=4096,
    )
    return response.choices[0].message.content.strip()


def extract_json(text: str):
    """Extract first JSON array or object from potentially prose-wrapped text."""
    m = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if m:
        return json.loads(m.group(1).strip())
    m = re.search(r"(\[[\s\S]*\]|\{[\s\S]*\})", text)
    if m:
        return json.loads(m.group(1))
    raise ValueError(f"No JSON found in response:\n{text[:500]}")


def generate_tests(client, spec_text: str, prompts: dict) -> list:
    """Call Groq to produce test objects from a spec."""
    system = prompts["test_generation_prompt"]["system"]
    user   = prompts["test_generation_prompt"]["user_template"].format(
        spec=spec_text[:6000]  # stay within context window
    )
    raw  = call_groq(client, system, user)
    data = extract_json(raw)
    if isinstance(data, list):
        return data
    return data.get("tests", [])


def process_pipeline(client, tag: str, prompts: dict, force: bool):
    spec_path  = _path("spec",  f"spec_{tag}.md")
    tests_path = _path("tests", f"tests_{tag}.json")

    if not os.path.isfile(spec_path) or os.path.getsize(spec_path) == 0:
        print(f"  [SKIP] {spec_path} missing or empty — run 06_spec_generate.py first.")
        return

    if os.path.isfile(tests_path) and not force:
        print(f"  [SKIP] {tests_path} already exists. Use --force to overwrite.")
        return

    print(f"  Generating tests for '{tag}' pipeline...")
    with open(spec_path, encoding="utf-8") as f:
        spec_text = f.read()

    tests = generate_tests(client, spec_text, prompts)

    with open(tests_path, "w", encoding="utf-8") as f:
        json.dump({"tests": tests}, f, indent=2)
    print(f"  Written: {tests_path}  ({len(tests)} tests)")


def main():
    parser = argparse.ArgumentParser(description="Generate tests from specs (Groq)")
    parser.add_argument(
        "--pipeline", choices=["auto", "hybrid", "all"], default="auto",
        help="Which pipeline to generate tests for (default: auto)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing test files")
    args = parser.parse_args()

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

    tags = ["auto", "hybrid"] if args.pipeline == "all" else [args.pipeline]
    for tag in tags:
        process_pipeline(client, tag, prompts, args.force)

    print("Done.")


if __name__ == "__main__":
    main()