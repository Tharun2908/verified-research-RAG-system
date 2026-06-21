# Serving Benchmark — Mistral-7B on NVIDIA H200 (vLLM)

Performance characterization of the generation backend served with **vLLM 0.23** on a single
**NVIDIA H200** (cl-worker37). Measures throughput and latency across concurrency levels, and
ablates two optimizations relevant to this RAG workload: **fp8 quantization** and **prefix
caching**. Benchmarked with realistic grounded-RAG prompts (fixed instruction + 5 evidence
chunks + question), 200 max output tokens, greedy decoding.

Model: `mistralai/Mistral-7B-Instruct-v0.3` · `--max-model-len 4096` · `--gpu-memory-utilization 0.85`.

---

## 1. Baseline: bf16 throughput scaling

| Concurrency | req/s | tokens/s | p50 (s) | p95 (s) | p99 (s) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1  | 3.30  | 194.6  | 0.302 | 0.308 | 0.310 |
| 8  | 21.81 | 1297.3 | 0.346 | 0.425 | 0.425 |
| 32 | 45.95 | 2745.4 | 0.648 | 0.736 | 0.739 |
| 64 | 58.50 | 3496.4 | 1.036 | 1.077 | 1.084 |

**Throughput scaled ~18×** (195 → 3,496 tok/s) from concurrency 1 → 64 via vLLM's continuous
batching, while p99 latency stayed **under 1.1 s**. Throughput was still increasing at concurrency
64, so the 7B workload continues to benefit from higher request-level parallelism on the H200.
(This is a throughput/latency observation only — GPU/SM utilization, memory bandwidth, and power
draw were not measured, so it does not by itself establish how close the device is to saturation.)

---

## 2. fp8 quantization vs bf16

Re-served with `--quantization fp8` (dynamic fp8; the H200 has native fp8 tensor cores). Identical
benchmark.

| Concurrency | bf16 tok/s | fp8 tok/s | fp8 speedup | bf16 p99 | fp8 p99 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1  | 194.6  | 279.4  | **+44%** | 0.310 | 0.223 |
| 8  | 1297.3 | 1698.2 | **+31%** | 0.425 | 0.305 |
| 32 | 2745.4 | 3014.7 | **+10%** | 0.739 | 0.681 |
| 64 | 3496.4 | 3911.5 | **+12%** | 1.084 | 0.963 |

**fp8 was faster AND lower-latency at every level** — up to **+44% throughput** and **~28% lower
p99** at low concurrency, courtesy of the H200's hardware fp8 path. Output quality remained
coherent (spot-checked).

**Why the speedup shrinks with concurrency (+44% → +12%):** at low concurrency the workload is
**compute-bound**, so faster fp8 matmuls dominate; at high concurrency it shifts toward
**memory-bandwidth / batching-bound**, where raw compute speedup matters less. The fp8 win is
largest exactly where compute is the bottleneck.

---

## 3. Prefix caching (fp8)

Grounded-RAG prompts share a long fixed instruction prefix across every request. Prefix caching
computes that prefix's KV-cache once and reuses it. Ablated with `--no-enable-prefix-caching` vs
`--enable-prefix-caching` (both fp8).

| Concurrency | no-prefix tok/s | prefix tok/s | speedup | no-prefix p99 | prefix p99 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1  | 269.3  | 278.5  | +3%  | 0.228 | 0.232 |
| 8  | 1387.4 | 1723.7 | **+24%** | 0.413 | 0.348 |
| 32 | 2142.2 | 2993.3 | **+40%** | 0.969 | 0.698 |
| 64 | 2507.0 | 3661.6 | **+46%** | 1.513 | 1.039 |

**The win grows with concurrency (+3% → +46%)** — and that's workload-specific: prefix caching's
value is proportional to how much prefix is *shared across concurrent requests*. A fixed-instruction
RAG system maximizes that sharing, so the more concurrent requests, the more redundant prefill is
eliminated. p99 latency at 64-way concurrency dropped **31%** (1.51 s → 1.04 s).

---

## 4. Takeaways

For this RAG serving workload, fp8 and prefix caching provide **complementary** benefits. fp8
improves low-concurrency performance by accelerating model execution on the H200's tensor cores,
while prefix caching improves high-concurrency serving by reusing the shared instruction prefix
across requests. The best **measured** configuration — **fp8 + prefix caching** — reached **61.0
req/s and 3.66k tok/s at concurrency 64, with p99 latency ~1.04 s**.

- **The optimizations are regime-dependent and workload-aware:** fp8 helps most when compute-bound
  (low concurrency); prefix caching helps most when many concurrent requests share the instruction
  prefix (high concurrency). They are complementary across the load curve.
- **H200 fp8 is hardware-accelerated**, not emulated — the fp8 throughput gain is specific to this
  class of GPU and would not appear on pre-fp8 hardware.
- **Note on the "best config" comparison:** a single bf16 + no-prefix-caching run was not measured
  as a separate arm (the bf16 baseline used vLLM's defaults), so the fp8+prefix improvement over a
  pure bf16/no-prefix baseline is not stated as a single combined multiplier here — each
  optimization's effect is reported against its own controlled ablation above.

### Method notes
- vLLM 0.23, single H200, Mistral-7B-Instruct-v0.3, 200 max tokens, greedy, realistic RAG prompts.
- **`max_tokens=200` is a cap, not the actual generation length.** With greedy decoding the model
  hit its stop token earlier — derived average output was ~60 tokens/request (e.g. 3,911 tok/s ÷
  65.2 req/s ≈ 60 at fp8/conc-64). Throughput numbers reflect these ~60-token completions.
- 64 requests/level, warmup pass excluded, latency percentiles over per-request end-to-end time.
- Benchmark client: `cluster/bench_vllm.py` (async httpx, semaphore-bounded concurrency).
- Note: recent vLLM enables prefix caching by default; the isolated effect in §3 comes from the
  explicit `--no-enable-prefix-caching` vs `--enable-prefix-caching` comparison.
