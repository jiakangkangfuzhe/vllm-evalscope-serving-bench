#!/usr/bin/env bash
set -euo pipefail

# EvalScope CLI changes across versions. This command uses the common perf-style
# OpenAI-compatible API pattern; adjust flags according to your installed version.
MODEL_NAME=${MODEL_NAME:-posttrain-model}
URL=${URL:-http://127.0.0.1:8000/v1/chat/completions}
PARALLEL=${PARALLEL:-16}
NUMBER=${NUMBER:-128}
OUTPUT_DIR=${OUTPUT_DIR:-results/evalscope_perf}

mkdir -p "${OUTPUT_DIR}" logs

evalscope perf \
  --url "${URL}" \
  --model "${MODEL_NAME}" \
  --api openai \
  --parallel "${PARALLEL}" \
  --number "${NUMBER}" \
  --dataset random \
  --stream \
  --output_dir "${OUTPUT_DIR}" \
  2>&1 | tee logs/evalscope_perf.log
