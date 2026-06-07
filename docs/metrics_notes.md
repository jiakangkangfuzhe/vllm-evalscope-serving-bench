# Serving metrics notes

- **Latency**: end-to-end request time.
- **TTFT**: time to first token; heavily affected by prefill and queueing.
- **TPOT**: time per output token; reflects decode efficiency.
- **Throughput**: requests/sec or tokens/sec.
- **P50/P95/P99**: percentile latency metrics; P95/P99 are important for tail latency.
- **Output tokens/sec**: often more useful than request/sec for LLM serving because output length varies.

When comparing runs, keep model, prompt length, output length, sampling parameters, and hardware fixed.
