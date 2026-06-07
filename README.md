# vllm-evalscope-serving-bench

A practical lab repository for **vLLM serving**, **EvalScope performance testing**, and **post-training model evaluation**.

The repository focuses on an LLM Infra workflow:

1. launch a vLLM OpenAI-compatible API server;
2. send concurrent batch requests for benchmark/evaluation data;
3. run EvalScope performance tests;
4. save raw responses, extracted answers, latency metrics, and failure cases;
5. analyze serving parameters such as `max_model_len`, `max_num_seqs`, `max_num_batched_tokens`, and `gpu_memory_utilization`.

## Layout

```text
.
├── configs/                    # vLLM and EvalScope config examples
├── data/                       # Tiny toy benchmark data
├── docs/                       # Serving / metric notes
├── results/                    # Generated outputs and result templates
├── scripts/                    # Launch, benchmark, sweep, eval scripts
└── src/                        # OpenAI-compatible batch inference utilities
```

## Quick start

```bash
conda create -n vllm-bench python=3.10 -y
conda activate vllm-bench
pip install -r requirements.txt

python src/build_toy_gsm8k.py --out data/toy_gsm8k.jsonl
bash scripts/launch_vllm_server.sh
bash scripts/eval_gsm8k_vllm.sh
bash scripts/bench_evalscope_perf.sh
```

## What this repo is for

- post-training model serving verification;
- benchmark generation and response saving;
- answer extraction and failure-case analysis;
- TTFT / TPOT / latency / throughput tracking;
- basic concurrency and serving-parameter sweeps.

## What this repo is not

This repo does not contain fake production numbers. Result templates under `results/` should be replaced only after real runs.
