.PHONY: data eval analyze templates

data:
	python src/build_toy_gsm8k.py --out data/toy_gsm8k.jsonl

eval:
	python src/openai_api_batch_infer.py --input data/toy_gsm8k.jsonl --output results/vllm_responses.jsonl --model $${MODEL_NAME:-Qwen/Qwen2.5-0.5B-Instruct}
	python src/evaluate_answers.py --input results/vllm_responses.jsonl --output results/eval_scored.jsonl --summary results/eval_summary.md

analyze:
	python src/latency_analyzer.py --input results/vllm_responses.jsonl --out results/latency_summary.md

templates:
	python src/result_to_markdown.py --input results/vllm_responses.jsonl --out results/run_summary.md || true
