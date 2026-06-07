#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME=${MODEL_NAME:-posttrain-model}
BASE_URL=${BASE_URL:-http://127.0.0.1:8000/v1}
CONCURRENCY=${CONCURRENCY:-8}
MAX_TOKENS=${MAX_TOKENS:-256}

mkdir -p data results
python src/build_toy_gsm8k.py --out data/toy_gsm8k.jsonl
python src/openai_api_batch_infer.py \
  --input data/toy_gsm8k.jsonl \
  --output results/vllm_responses.jsonl \
  --model "${MODEL_NAME}" \
  --base_url "${BASE_URL}" \
  --concurrency "${CONCURRENCY}" \
  --max_tokens "${MAX_TOKENS}"
python src/evaluate_answers.py \
  --input results/vllm_responses.jsonl \
  --output results/eval_scored.jsonl \
  --summary results/eval_summary.md
python src/latency_analyzer.py --input results/vllm_responses.jsonl --out results/latency_summary.md
