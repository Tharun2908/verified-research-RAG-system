# Verified Research RAG System

A retrieval-augmented research assistant that **measures and reports the grounding of its own answers** — treating hallucination rate as a measurable, monitorable property rather than an afterthought. Every answer is decomposed into atomic claims, each claim is checked against its cited evidence by a faithfulness verifier, and unsupported claims are flagged in the live API and removed in the batch verified-evaluation path. The verifier is a fine-tuned S2+S4 fusion model, evaluated in batch against an independent LLM judge (results committed); the live API currently runs a lightweight stub verifier for GPU-free reproducibility, with the real verifier's live integration scoped as future work.

Built as a production-scale system: an async FastAPI pipeline (hybrid retrieval → grounded generation → claim extraction → claim-level verification → persistence + Prometheus/Grafana monitoring), benchmarked on an NVIDIA H200 with vLLM, load-tested to find and fix real concurrency bottlenecks, and costed at serving scale.

> Part of a three-project portfolio on LLM safety & reliability: a prior project *trained* a model to reduce hallucinations (prevention), a thesis *built* a verifier to detect them (detection), and this project *builds the deployment system* around that verifier — a research assistant that decomposes and verifies its own claims, benchmarked and load-tested at serving scale (deployment).

---

## Highlights

- **Self-verifying RAG pipeline** — answers are claim-decomposed and checked against cited evidence by an S2+S4 faithfulness verifier (a cross-encoder relevance signal fused with a fine-tuned NLI entailment model). The verifier was evaluated in batch (committed score/judge artifacts); the live API exposes the unsupported-claim rate as a Prometheus metric and currently runs a stub verifier in that path.
- **Honest, judge-validated evaluation** — a 43-question / 409-claim study over an arXiv corpus with a three-arm comparison and an independent LLM-as-judge, reporting **measured precision/recall** rather than a self-referential "0% after filtering."
- **Real serving engineering on an H200** — vLLM benchmark with an fp8-vs-bf16 quantization ablation (**steady +33–39% throughput**) and a prefix-caching ablation that **corrected a benchmarking artifact** (an apparent +46% that was actually ~0% on realistic prompts).
- **Load-tested and bottleneck-fixed** — drove the live pipeline from collapse under load (62/64 requests failing at 32 concurrent) to clean scaling by diagnosing and fixing three stacked bottlenecks, then correctly identifying the remaining ceiling as a hardware limit.
- **Costed at scale** — a generation-dominated capacity/cost model grounded in the measured H200 throughput.

The recurring theme is *measured honesty*: several headline numbers were corrected mid-project after catching circular metrics or benchmarking artifacts in the project's own results.

---

## Architecture

```
question
   │
   ▼
hybrid retrieval ── BM25 (sparse) + dense (all-MiniLM → Qdrant) ─→ RRF fusion ─→ cross-encoder rerank
   │
   ▼
grounded generation ── numbered evidence + cite-your-sources prompt ─→ Mistral-7B (vLLM on H200)
   │
   ▼
claim extraction ── answer ─→ atomic claims, each with its cited source numbers
   │
   ▼
claim-level verification ── S2 (relevance) + S4 (fine-tuned NLI) fusion ─→ support score + label per claim
   │
   ▼
persistence + monitoring ── Postgres (jobs→results→claims→evidence) + Prometheus/Grafana
```

**Endpoint progression** (each builds on the last): `/search` (dense baseline) → `/retrieve` (hybrid) → `/research` (retrieve + generate) → `/verify` (full verified + persisted flow).

### Stack
Async FastAPI · async SQLAlchemy + Postgres · Qdrant (vectors) · Redis · sentence-transformers (embedder + cross-encoder) · a fine-tuned DeBERTa NLI verifier · vLLM + Mistral-7B (H200) · Prometheus + Grafana · Docker Compose. Generation is an external, swappable vLLM HTTP service (stub mode for GPU-free local development).

---

## Key results

### 1. Evaluation — does verification actually work?

A 43-question (36 grounded + 7 out-of-distribution "bait") / 409-claim study over a 250-paper arXiv corpus, using a real Mistral-7B generator and the real S2+S4 verifier (both run in batch on the cluster), with an independent **Llama-3.3-70B judge** (a different model family, for independence).

| Arm | What changes | Unsupported-claim rate |
| --- | --- | --- |
| Basic RAG | retrieve + generate | 8.3% |
| RAG + citations | prompt requests `[n]` citations | 4.7% |
| Verified | verifier removes flagged claims | 95.3% of claims retained |

- **The verifier discriminates** rather than flagging at random: on plain answers it flags out-of-distribution bait claims at **34.6%** vs grounded claims at **4.7%** (~7× separation) — the core validity evidence.
- **Judge-validated, and honest about it.** Graded against the independent judge, the verifier is conservative: **removal precision 51.8%**, **supported-claim loss only 3.9%**, but **recall 19.4%** — it under-flags, leaving ~15% judge-unsupported claims in the filtered output. Raw judge agreement was 82.6% (Cohen's κ = 0.21).
- **The weakness has a known cause.** The low recall is consistent with the predicted out-of-domain degradation of the RAGTruth-trained verifier on scientific abstracts — a finding that *confirms* a mechanistic hypothesis rather than contradicting it. The fix (in-domain verifier adaptation) is documented future work.

> An earlier version of this evaluation reported "~0% unsupported after filtering." That metric was **circular** — it only restated what the verifier flagged. It was replaced with judge-graded precision/recall, which is the honest measure.

### 2. Serving benchmark — vLLM on an H200

`docs/serving.md`. Mistral-7B, vLLM 0.23, unique-prompt RAG workload (~2,247 prompt vs ~135 output tokens → prefill-dominated).

- **fp8 vs bf16: a steady +33–39% throughput gain at every concurrency level**, plus ~25% lower p99 latency. The gain stays consistent (rather than shrinking under load) because the workload is prefill-bound and fp8 accelerates the prefill compute that dominates. Best config reached **18.8 req/s, 2,599 output tok/s, p99 ~5.8 s at concurrency 64.**
- **Prefix caching: ~0% on unique-evidence prompts** — and that is the *corrected* result. An initial run showed +46%, but the benchmark prompts were accidentally repeating; with genuinely unique evidence, only the ~80-token instruction prefix is shared, so there is almost nothing to cache. **The lesson — prefix caching's benefit equals the shared-prefix fraction of the prompt — is more valuable than the inflated number it replaced.**

### 3. Load test — finding and fixing real bottlenecks

`docs/loadtest.md`. Load-tested the live `/verify` pipeline and worked through three stacked bottlenecks:

| Stage | State | Fix |
| --- | --- | --- |
| Baseline | collapses under load: 62/64 fail at 32 concurrent, p99 87 s | — |
| 1 | per-request BM25 index rebuild (single request ~9 s) | build the index once at startup |
| 2 | DB connection-pool exhaustion under concurrency | larger pool + tight session scoping |
| 3 | synchronous model calls blocking the async event loop | offload to a thread pool (`asyncio.to_thread`) |

After the fixes, throughput **scaled 2.2× (concurrency 1→4) with zero errors**. The remaining plateau was diagnosed precisely as a **hardware ceiling** — PyTorch intra-op threading (12 threads/inference) saturating the 16 cores at ~4 concurrent requests — and confirmed by a thread-tuning sweep (fewer intra-op threads gave higher, more stable throughput under load). The architectural fix (GPU inference for the reranker, the same pattern already used for generation) is documented.

### 4. Capacity & cost

`docs/cost.md`. A generation-dominated cost model grounded in the measured H200 throughput: at a market H200 rate and realistic utilization, the generation step costs on the order of cents per thousand answers — and the model makes explicit that **utilization, not GPU price, is the dominant cost driver**, with retrieval and live verification flagged as the excluded terms.

---

## Repository layout

```
backend/app/
├── main.py                       FastAPI app (lifespan startup, routers, /metrics)
├── config.py                     env-driven settings (swappable LLM backend)
├── api/                          route handlers: /search /retrieve /research /verify /health
├── db/                           async SQLAlchemy session, 7-table schema, Qdrant setup
├── services/
│   ├── ingestion.py              embed papers → Qdrant vectors + Postgres metadata
│   ├── hybrid_search.py          BM25 + dense → RRF → cross-encoder rerank
│   ├── generator.py              retrieve → grounded prompt → LLM → cited answer
│   ├── claim_extractor.py        answer → atomic claims + citations
│   ├── verifier.py               verifier interface, S2+S4 labeling logic, stub (live default)
│   ├── verification_service.py   full verified flow + persistence + metrics
│   └── generation_client.py      swappable stub / vLLM HTTP client
└── monitoring/metrics.py         Prometheus metrics
cluster/                          bench_vllm.py, generate_batch.py, verify_batch.py (H200 jobs)
docs/                             serving.md, loadtest.md, cost.md
backend/load_test/                load-test client + raw results
docker-compose.yml                Postgres, Qdrant, Redis, Prometheus, Grafana
```

---

## Running it locally

The full stack runs locally with **no GPU**. For GPU-free reproducibility the live `/verify` path uses **stub generation and a stub verifier** (lexical overlap) — so the pipeline, persistence, and monitoring all run end-to-end without a model server. The real Mistral generator (M9) and real S2+S4 verifier (M8) were run separately on the cluster; pointing the app at them is described below and in the docs.

```bash
# 1. infra
docker-compose up -d            # Postgres, Qdrant, Redis, Prometheus, Grafana

# 2. app (from backend/)
pip install -r requirements.txt
uvicorn app.main:app --port 8000

# 3. query the verified pipeline
curl "http://localhost:8000/verify?q=How%20does%20RAG%20reduce%20hallucination&top_k=5"
```

The response includes the answer, each extracted claim with its support score and label (Supported / Weak / Unsupported), the overall grounding score, and the unsupported-claim rate — all also exported as Prometheus metrics and visualised in the included Grafana dashboard.

To use real generation, point the app at a vLLM server: set `LLM_BASE_URL` to the server URL and `LLM_MODEL` to the model id (the generation client speaks the OpenAI-compatible API).

---

## Design notes & honest limitations

- **The verifier: real, evaluated in batch; stub in the live path (for now).** The S2+S4 fusion verifier — lightweight enough to run on CPU — was evaluated offline in batch, and those results (the discrimination, precision/recall, and judge agreement above) are from that real verifier, with committed `scores.json` / `judge_results.json` / `verifier_quality.json` artifacts. The **live `/verify` API endpoint currently uses a stub verifier** (lexical overlap) for GPU-free reproducibility; **wiring the real S2+S4 verifier into the live request path is scoped future work.** A higher-accuracy cascade that escalates uncertain claims to a 7B verifier on GPU is a documented benchmark, deliberately *not* in the live path (its tail latency would break the GPU-free demo).
- **The verifier is domain-bound.** It was trained on RAGTruth (news/wiki); on scientific abstracts it under-flags. This is measured, explained, and owned — not hidden.
- **The cost model is generation-only** by design; live verification cost is the largest excluded term and the clear next measurement.
- Several numbers in this README are *corrected* values — the original prefix-caching gain and the original "0% after filtering" were both replaced after catching an artifact and a circular metric in the project's own results.
