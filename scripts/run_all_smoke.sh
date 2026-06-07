#!/usr/bin/env bash
set -euo pipefail
bash scripts/eval_gsm8k_vllm.sh
bash scripts/sweep_concurrency.sh
