# Serving Benchmark — Mistral-7B on NVIDIA H200 (vLLM)

Performance characterization of a local generation backend served with **vLLM 0.23** on a single
**NVIDIA H200** (`cl-worker37`). The benchmark measures request throughput, output-token throughput,
and end-to-end latency across concurrency levels, and ablates two serving optimizations relevant to
RAG workloads:

- **FP8 quantization** on H200 tensor cores.
- **Prefix caching** for repeated RAG instruction/template prefixes.

Model: `mistralai/Mistral-7B-Instruct-v0.3`  
Server: `vllm serve ... --max-model-len 4096 --gpu-memory-utilization 0.85`  
Decoding: greedy (`temperature=0.0`)  
Benchmark client: async `httpx`, semaphore-bounded concurrency.

---

## Benchmark modes

Two prompt modes were used.

| Mode | What varies? | What it measures |
|---|---|---|
| `repeat_full` | Nothing. The full prompt is repeated: instruction + evidence + question. | Prefix-cache stress test / upper-bound reuse. |
| `vary_context` | Same instruction/template, but evidence chunks and questions vary across requests. | More realistic RAG serving benchmark. |

The **primary results** below use `vary_context`, because this better matches real RAG serving: the instruction template is stable, while retrieved evidence and user questions differ.

---

## 1. Primary benchmark: varied-context RAG prompts

These runs use `--prompt-mode vary_context`, with approximately **120–130 output tokens/request**. Throughput is reported as **completion/output tokens per second**, not prompt+completion tokens/sec.

### 1.1 BF16 + prefix caching baseline

| Concurrency | req/s | output tok/s | avg output tok/req | p50 (s) | p95 (s) | p99 (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 1  | 1.59  | 192.2  | 121.2 | 0.583 | 1.013 | 1.015 |
| 8  | 10.65 | 1302.3 | 122.3 | 0.689 | 1.084 | 1.194 |
| 32 | 23.37 | 2968.1 | 127.0 | 1.027 | 1.606 | 1.683 |
| 64 | 29.45 | 3654.5 | 124.1 | 1.593 | 2.134 | 2.145 |

This is the realistic BF16 baseline for the updated benchmark. Compared with the earlier single-prompt run, request throughput is lower because the generated answers are roughly twice as long, but output-token throughput remains high.

---

### 1.2 FP8 vs BF16 with prefix caching enabled

Both runs use varied-context prompts and prefix caching.

| Concurrency | BF16 req/s | FP8 req/s | req/s gain | BF16 output tok/s | FP8 output tok/s | tok/s gain | BF16 p99 | FP8 p99 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1  | 1.59  | 2.30  | **+44.7%** | 192.2  | 276.8  | **+44.0%** | 1.015 | 0.699 |
| 8  | 10.65 | 13.55 | **+27.2%** | 1302.3 | 1773.6 | **+36.2%** | 1.194 | 0.915 |
| 32 | 23.37 | 26.91 | **+15.1%** | 2968.1 | 3323.0 | **+12.0%** | 1.683 | 1.500 |
| 64 | 29.45 | 33.88 | **+15.0%** | 3654.5 | 4172.5 | **+14.2%** | 2.145 | 1.865 |

**Finding:** FP8 improved throughput and reduced tail latency at every concurrency level. At 64-way concurrency, FP8 increased throughput from **29.45 → 33.88 req/s** and **3.65k → 4.17k output tok/s**, while reducing p99 latency from **2.15s → 1.87s**.

The speedup is largest at low concurrency, where compute is a stronger bottleneck. At higher concurrency, batching and memory movement become more important, so the relative FP8 gain shrinks but remains positive.

---

### 1.3 Prefix caching ablation under FP8

Both runs use FP8 and varied-context prompts.

| Concurrency | no-prefix req/s | prefix req/s | req/s gain | no-prefix output tok/s | prefix output tok/s | tok/s gain | no-prefix p99 | prefix p99 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1  | 2.24 | 2.30  | **+2.7%**  | 276.8  | 276.8  | **+0.0%**  | 0.696 | 0.699 |
| 8  | 11.64 | 13.55 | **+16.4%** | 1473.3 | 1773.6 | **+20.4%** | 1.098 | 0.915 |
| 32 | 19.44 | 26.91 | **+38.4%** | 2383.2 | 3323.0 | **+39.4%** | 2.575 | 1.500 |
| 64 | 22.80 | 33.88 | **+48.6%** | 2839.6 | 4172.5 | **+46.9%** | 2.796 | 1.865 |

**Finding:** Prefix caching still helps substantially even when evidence and questions vary. At 64-way concurrency, prefix caching improved FP8 throughput from **22.8 → 33.9 req/s** and **2.84k → 4.17k output tok/s**, while reducing p99 latency from **2.80s → 1.87s**.

The benefit grows with concurrency because more simultaneous requests share the same instruction template and prompt structure, allowing vLLM to reuse cached prefix states and reduce repeated prefill work.

---

## 2. Prefix-cache stress test: repeated full prompt

The earlier benchmark used a single repeated RAG-shaped prompt: fixed instruction, fixed evidence chunks, and fixed question. This is useful as a **stress test / upper-bound** for prefix caching, but it should not be interpreted as the only realistic RAG setting.

These runs generated shorter completions, roughly **~60 output tokens/request**, so request throughput is not directly comparable with the varied-context benchmark above.

### 2.1 BF16 throughput scaling: repeated full prompt

| Concurrency | req/s | output tok/s | p50 (s) | p95 (s) | p99 (s) |
|---:|---:|---:|---:|---:|---:|
| 1  | 3.30  | 194.6  | 0.302 | 0.308 | 0.310 |
| 8  | 21.81 | 1297.3 | 0.346 | 0.425 | 0.425 |
| 32 | 45.95 | 2745.4 | 0.648 | 0.736 | 0.739 |
| 64 | 58.50 | 3496.4 | 1.036 | 1.077 | 1.084 |

Throughput scaled strongly from concurrency 1 to 64 via vLLM continuous batching, while p99 latency stayed under 1.1s. This is a throughput/latency observation only: GPU/SM utilization, memory bandwidth, and power draw were not measured.

---

### 2.2 FP8 vs BF16: repeated full prompt

| Concurrency | BF16 output tok/s | FP8 output tok/s | FP8 speedup | BF16 p99 | FP8 p99 |
|---:|---:|---:|---:|---:|---:|
| 1  | 194.6  | 279.4  | **+44%** | 0.310 | 0.223 |
| 8  | 1297.3 | 1698.2 | **+31%** | 0.425 | 0.305 |
| 32 | 2745.4 | 3014.7 | **+10%** | 0.739 | 0.681 |
| 64 | 3496.4 | 3911.5 | **+12%** | 1.084 | 0.963 |

FP8 was faster and lower-latency at every level in the repeated-prompt benchmark.

---

### 2.3 Prefix caching under FP8: repeated full prompt

| Concurrency | no-prefix output tok/s | prefix output tok/s | speedup | no-prefix p99 | prefix p99 |
|---:|---:|---:|---:|---:|---:|
| 1  | 269.3  | 278.5  | +3%  | 0.228 | 0.232 |
| 8  | 1387.4 | 1723.7 | **+24%** | 0.413 | 0.348 |
| 32 | 2142.2 | 2993.3 | **+40%** | 0.969 | 0.698 |
| 64 | 2507.0 | 3661.6 | **+46%** | 1.513 | 1.039 |

This confirms the upper-bound behavior: when the entire prompt is repeated, prefix caching can eliminate a large amount of repeated prefill work. At 64-way concurrency, p99 latency dropped from **1.51s → 1.04s**.

---

## 3. Takeaways

- **Best measured realistic configuration:** `fp8 + prefix caching` on varied-context RAG prompts, reaching **33.9 req/s**, **4.17k output tok/s**, and **1.87s p99 latency** at concurrency 64.
- **FP8 helps model execution:** under varied-context prompts with prefix caching, FP8 improved concurrency-64 throughput by roughly **14–15%** and reduced p99 latency by roughly **13%** compared with BF16.
- **Prefix caching helps serving efficiency:** under FP8 with varied-context prompts, prefix caching improved concurrency-64 throughput by roughly **47–49%** and reduced p99 latency by roughly **33%** compared with no prefix caching.
- **Prompt design matters:** repeated full-prompt benchmarks are useful as prefix-cache stress tests, while varied-context benchmarks better represent normal RAG serving where evidence and questions change across requests.
- **H200 FP8 is hardware-accelerated**, not emulated; the FP8 speedup is specific to GPUs with native FP8 support.

---

## Method notes

- vLLM 0.23, single NVIDIA H200, Mistral-7B-Instruct-v0.3.
- Server settings: `--max-model-len 4096`, `--gpu-memory-utilization 0.85`.
- FP8 runs used `--quantization fp8 --dtype auto`.
- Prefix-caching ablation used explicit `--enable-prefix-caching` vs `--no-enable-prefix-caching`.
- Benchmark client: `bench_vllm.py`, using async `httpx` and semaphore-bounded concurrency.
- Each level used 64 requests; warmup pass excluded.
- Latency percentiles are per-request end-to-end latency measured from the benchmark client.
- `max_tokens=200` is a cap, not the actual generation length.
- `output tok/s` / `completion tok/s` counts generated completion tokens only, using `usage.completion_tokens` returned by the vLLM OpenAI-compatible API.
