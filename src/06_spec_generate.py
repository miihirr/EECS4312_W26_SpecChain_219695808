"""
06_spec_generate.py
Generates structured requirements specifications from personas using Groq LLM.

Reads:
    personas/personas_auto.json   → writes spec/spec_auto.md
    personas/personas_hybrid.json → writes spec/spec_hybrid.md  (if requested)

Usage:
    python src/06_spec_generate.py                  # auto spec only
    python src/06_spec_generate.py --pipeline hybrid
    python src/06_spec_generate.py --pipeline all   # both
    python src/06_spec_generate.py --force          # overwrite existing

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


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_prompts() -> dict:
    return load_json(_path("prompts", "prompt_auto.json"))


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


def generate_spec(client, personas: dict, prompts: dict, pipeline_tag: str) -> str:
    """Call the LLM to produce a Markdown spec from personas."""
    personas_json = json.dumps(personas, indent=2)
    system = prompts["spec_generation_prompt"]["system"]
    user   = prompts["spec_generation_prompt"]["user_template"].format(
        personas=personas_json,
        pipeline_tag=pipeline_tag,
    )
    return call_groq(client, system, user)


SPEC_TEMPLATE = """# Requirements Specification — {label} Pipeline

## Application
Headspace (com.getsomeheadspace.android) — meditation, sleep, and mindfulness app

## Pipeline
{label}

## Generated Requirements

{requirements}
"""


def format_spec(raw_text: str, label: str) -> str:
    """Wrap raw LLM output in the standard spec header if not already formatted."""
    if raw_text.strip().startswith("# Requirements Specification"):
        return raw_text  # already formatted
    return SPEC_TEMPLATE.format(label=label, requirements=raw_text)


def process_pipeline(client, tag: str, prompts: dict, force: bool):
    personas_path = _path("personas", f"personas_{tag}.json")
    spec_path     = _path("spec",     f"spec_{tag}.md")

    if not os.path.isfile(personas_path):
        print(f"  [SKIP] {personas_path} not found — run 05_personas_auto.py first.")
        return

    if os.path.isfile(spec_path) and not force:
        print(f"  [SKIP] {spec_path} already exists. Use --force to overwrite.")
        return

    label = {"auto": "Automated", "hybrid": "Hybrid"}.get(tag, tag.title())
    print(f"  Generating spec for '{tag}' pipeline...")
    personas = load_json(personas_path)
    raw = generate_spec(client, personas, prompts, label)
    spec_text = format_spec(raw, label)

    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(spec_text)
    req_count = len(re.findall(r"^## Requirement ID:", spec_text, re.MULTILINE))
    print(f"  Written: {spec_path}  ({req_count} requirements)")


def main():
    parser = argparse.ArgumentParser(description="Generate specs from personas (Groq)")
    parser.add_argument(
        "--pipeline", choices=["auto", "hybrid", "all"], default="auto",
        help="Which pipeline to generate spec for (default: auto)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing spec files")
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