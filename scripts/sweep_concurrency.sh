#!/usr/bin/env bash
set -euo pipefail
mkdir -p data results/sweep
python src/build_toy_gsm8k.py --out data/toy_gsm8k.jsonl
python src/sweep_concurrency.py \
  --input data/toy_gsm8k.jsonl \
  --output_dir results/sweep \
  --model "${MODEL_NAME:-posttrain-model}" \
  --base_url "${BASE_URL:-http://127.0.0.1:8000/v1}" \
  --concurrency 1 2 4 8 16 32
