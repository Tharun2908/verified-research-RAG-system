# Serving Benchmark — Mistral-7B on NVIDIA H200 (vLLM)

Performance characterization of the generation backend served with **vLLM 0.23** on a single
**NVIDIA H200** (`cl-worker37`). Measures request throughput, output-token throughput, and
end-to-end latency across concurrency levels, and ablates **fp8 quantization** and **prefix
caching** on a realistic RAG workload.

Model: `mistralai/Mistral-7B-Instruct-v0.3` · `--max-model-len 4096` · `--gpu-memory-utilization 0.85` · greedy decoding · benchmark client `cluster/bench_vllm.py` (async httpx, semaphore-bounded concurrency).

---

## Workload: long-context, prefill-dominated RAG prompts

The primary benchmark uses `--prompt-mode vary_context`: a fixed instruction template plus
**globally unique** retrieved evidence and question per request (the full request id is embedded
in the evidence text, so no two prompts are identical). This matters — an earlier version varied
content only modularly, which let prompts repeat and inflated prefix-cache reuse. The numbers
below use genuinely unique prompts.

Each request carries **~2,247 prompt tokens** (5 evidence chunks + instruction + question) and
generates **~135 output tokens**. The workload is therefore **prefill-dominated**: most compute
is spent processing the long input context, not generating output. This shape drives every result
below.

> A separate "repeated full prompt" mode (`--prompt-mode repeat_full`) exists purely as a
> prefix-cache **upper-bound stress test**; its numbers are not representative of RAG serving and
> are not used as primary results here.

---

## 1. fp8 vs bf16 (both with prefix caching)

| Concurrency | bf16 req/s | fp8 req/s | bf16 tok/s | fp8 tok/s | **fp8 tok/s gain** | bf16 p99 | fp8 p99 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1  | 1.39  | 1.95  | 189.8  | 264.0  | **+39%** | 1.021 | 0.729 |
| 8  | 7.19  | 9.59  | 963.6  | 1299.9 | **+35%** | 1.679 | 1.258 |
| 32 | 12.02 | 16.12 | 1696.4 | 2257.1 | **+33%** | 4.031 | 3.021 |
| 64 | 13.50 | 18.76 | 1906.6 | 2599.3 | **+36%** | 7.933 | 5.816 |

**fp8 delivered a consistent +33–39% output-token throughput gain at every concurrency level**, plus
~25–28% lower p99 latency. Unlike a short-output benchmark (where the fp8 advantage shrinks as the
workload becomes batching-bound), here the gain holds across concurrency because the workload is
**prefill-dominated** — fp8 accelerates the large prefill matmuls that dominate, and that bottleneck
is present at every concurrency. This is the headline serving result. Output quality remained
coherent (spot-checked). The fp8 speedup is specific to the H200's **native fp8 tensor cores** and
would not appear on pre-fp8 hardware.

---

## 2. Prefix caching on vs off (both fp8)

| Concurrency | no-prefix tok/s | prefix tok/s | difference | no-prefix p99 | prefix p99 |
|---:|---:|---:|---:|---:|---:|
| 1  | 264.5  | 264.0  | −0.2% | 0.727 | 0.729 |
| 8  | 1307.6 | 1299.9 | −0.6% | 1.253 | 1.258 |
| 32 | 2242.3 | 2257.1 | +0.7% | 3.054 | 3.021 |
| 64 | 2574.6 | 2599.3 | +1.0% | 5.893 | 5.816 |

**Prefix caching made essentially no difference (±1%, within run-to-run noise) on unique-evidence
RAG prompts.** This is the expected, honest result: prefix caching reuses the KV cache for *shared*
prompt prefixes, and here only the ~80-token instruction is shared — about **3.5% of the ~2,247-token
prompt**. With unique retrieved evidence per query, there is almost nothing to reuse.

**Key lesson:** prefix caching's benefit is proportional to the **shared-prefix fraction** of the
prompt. A RAG system with per-query retrieval shares only the instruction, so prefix caching barely
helps in this configuration. It pays off when the shared prefix is large relative to the variable
part — e.g. a long fixed system prompt, few-shot exemplars reused across requests, or document-level
caching where many questions hit the same document. (A repeated-prompt stress test showed up to +46%,
but that reflects artificial full-prompt reuse, not realistic RAG serving.)

---

## 3. Takeaways

For this **prefill-dominated, unique-evidence** RAG serving workload:

- **fp8 is the decisive optimization: a steady ~33–39% throughput gain and ~25% lower p99** vs bf16,
  because it accelerates the prefill compute that dominates long-context RAG. Best measured config
  (fp8 + prefix caching) reached **18.8 req/s, 2.6k output tok/s, p99 ~5.8 s at concurrency 64.**
- **Prefix caching is ~neutral here (±1%)** — its value scales with the shared-prefix fraction, which
  is small (~3.5%) when each query retrieves unique evidence. It is not a free win for all RAG; it
  must be matched to prompt structure.
- **Benchmark realism matters:** repeated-prompt benchmarks overstate prefix-cache benefit (a +46%
  artifact here). Unique-prompt benchmarks reflect real per-query RAG and are used for all primary
  numbers above.
- **The workload is prefill-bound** (~2,247 prompt vs ~135 output tokens): latency rises steeply with
  concurrency (p99 ~0.7 s → ~5.8 s from conc 1 → 64 under fp8) because concurrent prefill of long
  contexts competes for compute. Reducing retrieved-context size or output length would shift this.

### Method notes
- vLLM 0.23, single H200, Mistral-7B-Instruct-v0.3, `--max-model-len 4096`, `--gpu-memory-utilization 0.85`.
- fp8: `--quantization fp8 --dtype auto`. Prefix-cache ablation: explicit `--enable-prefix-caching` vs `--no-enable-prefix-caching`.
- `--prompt-mode vary_context` with globally unique prompts (full request id embedded in evidence text); warmup and each concurrency level use disjoint prompt-id ranges to prevent cross-level cache reuse.
- 1024 requests/level, warmup excluded. Latency percentiles over per-request end-to-end time from the client.
- `max_tokens=200` is a cap; measured average output was ~135 tokens/request. `tok/s` counts completion tokens only (`usage.completion_tokens`).
- Raw results: `backend/data/bench_bf16_prefix_unique.json`, `bench_fp8_prefix_unique.json`, `bench_fp8_noprefix_unique.json` (gitignored).
