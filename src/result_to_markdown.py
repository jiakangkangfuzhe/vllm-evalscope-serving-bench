#!/usr/bin/env python3
"""Convert a JSONL run file to a compact Markdown summary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rows = [json.loads(x) for x in args.input.read_text(encoding="utf-8").splitlines() if x.strip()]
    lat = [float(r["latency_s"]) for r in rows if r.get("latency_s") is not None]
    ok = [r for r in rows if r.get("is_correct") is True]
    lines = [
        "# Run summary",
        "",
        f"- input file: `{args.input}`",
        f"- requests: {len(rows)}",
        f"- avg latency: {mean(lat):.4f}s" if lat else "- avg latency: N/A",
        f"- accuracy: {len(ok) / len(rows):.4f}" if rows and "is_correct" in rows[0] else "- accuracy: N/A",
        "",
        "## Sample responses",
        "",
    ]
    for row in rows[:5]:
        resp = str(row.get("response", "")).replace("\n", " ")[:180]
        lines.append(f"- id={row.get('id')}: {resp}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
