#!/usr/bin/env python3
"""Run multiple concurrency levels against a vLLM OpenAI-compatible server."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/toy_gsm8k.jsonl")
    parser.add_argument("--output_dir", type=Path, default=Path("results/sweep"))
    parser.add_argument("--model", default="posttrain-model")
    parser.add_argument("--base_url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--concurrency", nargs="+", type=int, default=[1, 2, 4, 8, 16])
    parser.add_argument("--max_tokens", type=int, default=256)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for c in args.concurrency:
        out = args.output_dir / f"responses_c{c}.jsonl"
        cmd = [
            "python", "src/openai_api_batch_infer.py",
            "--input", args.input,
            "--output", str(out),
            "--model", args.model,
            "--base_url", args.base_url,
            "--concurrency", str(c),
            "--max_tokens", str(args.max_tokens),
        ]
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)
        subprocess.run([
            "python", "src/latency_analyzer.py",
            "--input", str(out),
            "--out", str(args.output_dir / f"latency_c{c}.md"),
        ], check=True)


if __name__ == "__main__":
    main()
