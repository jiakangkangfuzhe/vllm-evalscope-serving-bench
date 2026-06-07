# vLLM serving notes

## Important concepts

- **KV Cache**: stores previous key/value states during autoregressive decoding. Memory increases with batch size, sequence length, number of concurrent sequences, model hidden size, and number of layers.
- **PagedAttention**: vLLM's memory-management mechanism for KV cache blocks; it reduces fragmentation and improves serving throughput.
- **Continuous batching**: requests can enter/leave a running batch dynamically, improving GPU utilization under mixed-length online serving.
- **Prefill vs decode**: prefill processes the prompt and is usually compute-heavy; decode generates one token per step and is often memory-bandwidth / scheduling sensitive.
- **max_model_len / max_num_seqs / max_num_batched_tokens**: key knobs that trade off admission capacity, memory pressure, and latency.

## What to record in each run

- model name and precision;
- GPU type/count and tensor parallel size;
- vLLM launch command;
- request concurrency and output length;
- TTFT / TPOT / latency P50/P95/P99;
- input tokens/sec and output tokens/sec;
- GPU memory utilization and OOM/failure cases.
