#!/usr/bin/env python3
"""Build a tiny GSM8K-style JSONL for serving/eval smoke tests."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROWS = [
    {"id": "toy-001", "question": "Tom has 2 apples and buys 3 more. How many apples does he have?", "gold_answer": "5"},
    {"id": "toy-002", "question": "A box has 4 bags with 6 candies each. How many candies are there?", "gold_answer": "24"},
    {"id": "toy-003", "question": "If a train travels 60 miles per hour for 2 hours, how many miles does it travel?", "gold_answer": "120"},
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/toy_gsm8k.jsonl"))
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for row in ROWS:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(ROWS)} rows -> {args.out}")


if __name__ == "__main__":
    main()
