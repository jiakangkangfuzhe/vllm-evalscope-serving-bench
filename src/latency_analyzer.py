#!/usr/bin/env python3
"""Summarize latency and token-throughput from JSONL inference outputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def percentile(xs: list[float], p: float) -> float:
    if not xs:
        return 0.0
    return float(np.percentile(np.array(xs, dtype=float), p))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results/latency_summary.md"))
    args = parser.parse_args()

    latencies = []
    total_tokens = 0
    completion_tokens = 0
    n_error = 0
    n = 0
    with args.input.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            n += 1
            if row.get("error"):
                n_error += 1
            if row.get("latency_s") is not None:
                latencies.append(float(row["latency_s"]))
            total_tokens += int(row.get("total_tokens") or 0)
            completion_tokens += int(row.get("completion_tokens") or 0)

    wall_time = max(latencies) if latencies else 0.0
    lines = [
        "# Latency summary",
        "",
        f"- requests: {n}",
        f"- errors: {n_error}",
        f"- avg latency: {np.mean(latencies):.4f}s" if latencies else "- avg latency: 0",
        f"- p50 latency: {percentile(latencies, 50):.4f}s",
        f"- p95 latency: {percentile(latencies, 95):.4f}s",
        f"- p99 latency: {percentile(latencies, 99):.4f}s",
        f"- total tokens/sec estimate: {total_tokens / wall_time:.2f}" if wall_time else "- total tokens/sec estimate: 0",
        f"- output tokens/sec estimate: {completion_tokens / wall_time:.2f}" if wall_time else "- output tokens/sec estimate: 0",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
