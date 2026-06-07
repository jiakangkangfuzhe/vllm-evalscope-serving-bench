#!/usr/bin/env python3
"""Concurrent batch inference against an OpenAI-compatible vLLM server.

Input JSONL fields:
- question or prompt
- gold_answer optional

Output JSONL includes raw response, latency, prompt/completion token usage if
returned by the server, and request metadata.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any

import aiohttp
from tqdm import tqdm


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_prompt(row: dict[str, Any]) -> str:
    q = row.get("question") or row.get("prompt") or row.get("input") or ""
    return (
        "Solve the problem step by step. At the end, write the final answer in the format '#### <answer>'.\n\n"
        f"Problem: {q}\n"
    )


async def request_one(
    session: aiohttp.ClientSession,
    url: str,
    model: str,
    row: dict[str, Any],
    max_tokens: int,
    temperature: float,
    timeout_s: float,
) -> dict[str, Any]:
    prompt = build_prompt(row)
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    t0 = time.perf_counter()
    try:
        async with session.post(url, json=payload, timeout=timeout_s) as resp:
            text = await resp.text()
            latency = time.perf_counter() - t0
            if resp.status >= 400:
                return {**row, "prompt": prompt, "error": text, "status": resp.status, "latency_s": latency}
            data = json.loads(text)
            content = data["choices"][0]["message"].get("content", "")
            usage = data.get("usage", {}) or {}
            return {
                **row,
                "prompt": prompt,
                "response": content,
                "status": resp.status,
                "latency_s": latency,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
            }
    except Exception as e:  # keep batch jobs from crashing on one request
        return {**row, "prompt": prompt, "error": repr(e), "latency_s": time.perf_counter() - t0}


async def run(args: argparse.Namespace) -> None:
    rows = read_jsonl(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    url = args.base_url.rstrip("/") + "/chat/completions" if args.base_url.endswith("/v1") else args.base_url.rstrip("/") + "/v1/chat/completions"
    sem = asyncio.Semaphore(args.concurrency)

    async with aiohttp.ClientSession() as session:
        async def bounded(row: dict[str, Any]) -> dict[str, Any]:
            async with sem:
                return await request_one(session, url, args.model, row, args.max_tokens, args.temperature, args.timeout)

        tasks = [bounded(row) for row in rows]
        with args.output.open("w", encoding="utf-8") as fout:
            for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="infer"):
                result = await coro
                fout.write(json.dumps(result, ensure_ascii=False) + "\n")
                fout.flush()
    print(f"Wrote results -> {args.output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base_url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model", default="posttrain-model")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--max_tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
