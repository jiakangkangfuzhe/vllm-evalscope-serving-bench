#!/usr/bin/env python3
"""Score vLLM responses using simple GSM8K-style numeric extraction."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from answer_extractor import extract_answer, normalize_number
except ImportError:
    from .answer_extractor import extract_answer, normalize_number


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, default=Path("results/eval_summary.md"))
    args = parser.parse_args()

    total = 0
    correct = 0
    failures = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.input.open("r", encoding="utf-8") as fin, args.output.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            row = json.loads(line)
            pred = extract_answer(row.get("response", ""))
            gold = normalize_number(row.get("gold_answer"))
            ok = pred is not None and pred == gold
            row.update({"extracted_answer": pred, "gold_normalized": gold, "is_correct": ok})
            total += 1
            correct += int(ok)
            if not ok:
                failures.append(row)
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

    acc = correct / total if total else 0.0
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Evaluation summary",
        "",
        f"- samples: {total}",
        f"- correct: {correct}",
        f"- accuracy: {acc:.4f}",
        "",
        "## Failure cases",
        "",
    ]
    for row in failures[:20]:
        lines.append(f"- id={row.get('id')}, pred={row.get('extracted_answer')}, gold={row.get('gold_normalized')}")
    args.summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"accuracy={acc:.4f}; wrote {args.output} and {args.summary}")


if __name__ == "__main__":
    main()
