# Load Test — Application-Layer Bottleneck Analysis (M10A)

Sustained-concurrency load test of the live FastAPI `/verify` pipeline
(retrieve → generate → extract → verify → persist), run on the laptop against the local app.

**Scope — this is deliberately an application/orchestration benchmark, not a model benchmark.**
Both the generator and the verifier ran as **stubs**: generation used the stub LLM client (canned
output, no real model call) and verification used `StubVerifier` (lexical overlap), *not* the real
S2+S4 fusion verifier. This is intentional — stubbing the two model-heavy stages isolates the
retrieval, async-orchestration, connection-pool, and persistence layers so their bottlenecks are
visible rather than masked by model latency. The real generator was benchmarked separately on the
H200 in M9 (`docs/serving.md`); the real S2+S4 verifier was evaluated in batch in M8 (`docs/`).

**Test setup:** async load client (`backend/load_test/loadtest_verify.py`), 64 requests/level,
concurrency levels 1–32, rotating set of varied questions. Infra (Postgres/Qdrant/Redis) in Docker;
FastAPI on the host (`fastapi-env`). The retrieval models that *do* run live (all-MiniLM embedder +
ms-marco cross-encoder reranker) run on **CPU** (`torch.cuda.is_available() == False`).

---

## Bottleneck progression (each fix exposed the next)

### Stage 0 — Baseline (before any fix)
| conc | req/s | p99 (s) | errors |
| ---: | ---: | ---: | ---: |
| 1  | 0.11 | 9.6   | 0 |
| 4  | 0.34 | 20.5  | 0 |
| 8  | 0.33 | 39.5  | 0 |
| 16 | 0.26 | 87.1  | 12 |
| 32 | 0.02 | —     | **62/64 failed** |

The system **collapsed under load** — throughput went *backwards* with concurrency and 62 of 64
requests failed at concurrency 32. Even a single request took ~9 s. Three stacked causes, found in
order:

### Stage 1 fix — BM25 index rebuilt once at startup (not per request)
`hybrid_search` was calling `BM25Retriever().build()` on **every request** — a synchronous
full-corpus read + tokenize + index construction. Moved it to a FastAPI `lifespan` startup hook
(built once, reused via a shared instance).
**Result:** single-request latency **8.8 s → 2.8 s** (~3×). But under concurrency the DB connection
pool now exhausted (requests reached persistence simultaneously), throwing
`QueuePool limit of size 5 overflow 10 reached` 500s at concurrency ≥16.

> **Freshness tradeoff (documented limitation):** building the index once at startup means it goes
> stale after new documents are ingested — the in-memory sparse index won't include them until it is
> rebuilt. This is handled by a `rebuild_bm25()` invalidation hook (drops and rebuilds the shared
> index from the current corpus); call it after ingestion/reset, or restart the app. The per-request
> rebuild would have kept the index always-fresh but was the bottleneck fixed here — a deliberate
> freshness-for-throughput trade.

### Stage 2 fix — DB connection pool + session scoping
Raised the SQLAlchemy pool (`pool_size=20, max_overflow=30, pool_pre_ping=True`) **and** scoped DB
sessions tightly: the synchronous cross-encoder rerank now runs **between** two short session
blocks instead of holding a connection open across the whole pipeline.
**Result:** the `QueuePool limit reached` failures from Stage 1 were resolved (the pool no longer
exhausts and connections are released before the rerank). But throughput **still didn't scale**
(~0.35 → 0.30 → 0.20 req/s as concurrency rose) and p99 still climbed steeply — the event loop was
still being blocked by the synchronous model calls, which Stage 3 addresses. (The committed
`loadtest_before.json` and `loadtest_after_bm25.json` capture Stages 0–1; the pool/session change
was validated interactively against the live server and folded directly into Stage 3, so its
intermediate run is not separately archived. The Stage 3 scaling artifacts below are the
load-bearing evidence.)

### Stage 3 fix — synchronous model work moved off the event loop
The dense embed (`_embed_model.encode`) and cross-encoder `rerank` are synchronous CPU calls that
ran **directly in the async event loop**, serializing all concurrent requests. Wrapped both in
`asyncio.to_thread(...)` so they run on worker threads (PyTorch releases the GIL during native
compute, so threads genuinely overlap).
**Result:** the event loop is no longer blocked — concurrency now functions (see below).

---

## Demonstrating that concurrency now scales

With the full production rerank pool (`candidate_pool=50`), each request's cross-encoder pass is
heavy enough on CPU that one request nearly saturates the machine, masking the scaling. To isolate
**whether the concurrency machinery works** from **per-request CPU cost**, the rerank pool was
temporarily reduced to 10 (a test configuration, not the production value) so per-request compute
fits within available cores:

| conc | req/s | p99 (s) | errors |
| ---: | ---: | ---: | ---: |
| 1  | 0.92 | 2.6  | 0 |
| 4  | 2.03 | 2.6  | 0 |
| 8  | 2.00 | 5.6  | 0 |
| 16 | 2.03 | 9.8  | 0 |
| 32 | 1.61 | 26.3 | 0 |

**Throughput scaled 2.2× from concurrency 1 → 4 (0.92 → 2.03 req/s), zero errors** — confirming the
three fixes enable real request-level parallelism (vs the original collapse). It then **plateaus at
~2 req/s** beyond concurrency 4, with latency growing linearly (p99 2.6 → 9.8 → 26 s) — the
signature of a compute-bound ceiling.

---

## The remaining ceiling: parallel CPU inference (correctly a hardware/architecture limit)

The plateau at ~4 concurrent requests on a **16-core** machine has a precise cause:
**PyTorch intra-op parallelism.** `torch.get_num_threads() == 12`, so each cross-encoder inference
already spreads across up to 12 threads. A handful of concurrent inferences therefore saturate the
16 physical cores — request-level concurrency tops out at roughly `cores ÷ threads-per-inference`,
i.e. ~4, not ~16. The cores are not idle; they are consumed by intra-op parallelism *within* each
request.

This is a **hardware/architecture ceiling, not a software defect** — every application-layer
bottleneck (index rebuild, pool exhaustion, event-loop blocking) was removed.

### Confirming the mechanism: intra-op thread tuning (pool=10)

If intra-op oversubscription is really the cause, *reducing* `torch.set_num_threads` should raise
concurrent throughput (fewer cores per inference → more inferences in parallel) at the cost of
single-request latency. Tested directly:

| conc | 12 threads (default) | 2 threads | 4 threads |
| ---: | ---: | ---: | ---: |
| 1  | **0.92** | 0.63 | 0.50 |
| 4  | 2.03 | 1.72 | 2.04 |
| 8  | 2.00 | 2.33 | 2.34 |
| 16 | 2.03 | 2.34 | 2.34 |
| 32 | 1.61 | 2.35 | 2.28 |

**Confirmed.** Fewer intra-op threads (2 or 4) gave **higher and more stable throughput under
concurrency** (~2.3 req/s at conc 8–32) and **eliminated the degradation** the 12-thread config
showed at high load (1.61 req/s at conc 32). The tradeoff is single-request latency: 12 threads is
fastest for one request (0.92 req/s at conc 1) but worst under load. The 2- vs 4-thread difference
was within measurement noise — the finding is "fewer threads helps concurrent serving," not a
precise optimum (laptop measurements are too noisy to claim one).

**This is the classic intra-op vs request-level parallelism tradeoff**, demonstrated empirically:
for a concurrent-serving workload, fewer intra-op threads per inference is the better configuration
because it avoids CPU oversubscription. (It is why serving setups often pin `OMP_NUM_THREADS` low
per worker.)

### Scaling beyond the CPU ceiling — options
The thread tuning improves the CPU ceiling but does not remove it. Fully scaling the production
(pool=50) reranker is a provisioning decision:
- **GPU inference** for the embedder + cross-encoder (models drop from seconds to ~tens of ms) —
  the same "serve inference on dedicated hardware" pattern already used for generation via vLLM on
  the H200 in M9.
- **A dedicated reranker microservice** (model inference scales independently of the API).
- **Tuned intra-op threads** (shipped default lowered from 12 to 4 based on the sweep above).

---

## Summary

| Stage | Fix | Effect |
| --- | --- | --- |
| 0 | — (baseline) | collapses under load: 62/64 fail at conc 32, p99 87 s |
| 1 | BM25 built once at startup | single-request 8.8 s → 2.8 s; exposes DB pool exhaustion |
| 2 | DB pool + tight session scoping | errors eliminated; still doesn't scale (event loop blocked) |
| 3 | model work off event loop (`to_thread`) | concurrency works: 2.2× scaling (conc 1→4), 0 errors |
| — | intra-op thread tuning | 12→2/4 threads: +throughput & stability under load (2.0→2.35 req/s at conc 8-32); confirms oversubscription was the mechanism |
| — | remaining ceiling | CPU parallel-inference capacity; fix = GPU/dedicated inference |

**Takeaway:** three real application-layer bottlenecks diagnosed and fixed under load, with the
improvement demonstrated empirically (collapse → scaling). The remaining limit is correctly
identified as parallel CPU-inference capacity — a hardware boundary addressable by serving the
models on GPU, exactly as the generation path already is.

### Artifacts
`backend/load_test/loadtest_verify.py` (load client). Raw results (committed in
`backend/load_test/`): `loadtest_before.json` (Stage 0), `loadtest_after_bm25.json` (Stage 1),
`loadtest_pool10.json` (Stage 3 scaling demo), `loadtest_pool10_torch2.json` and
`loadtest_pool10_torch4.json` (intra-op thread-tuning sweep).
