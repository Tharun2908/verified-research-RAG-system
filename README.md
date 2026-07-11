# Verified Research RAG System

**A research agent that measures and reports the grounding of its own answers.**

Ask a question over a 250-paper arXiv corpus. The system retrieves evidence, generates a cited answer, then **verifies every claim against the evidence that claim cites** — and tells you how much of its own answer is actually supported.

### ▶ [Try it live](https://huggingface.co/spaces/Primeinvincible/verified-research-rag)

The interesting case is the third example: it asks about something the corpus doesn't cover. The system says so, and the grounding report reflects that it *abstained* rather than fabricated.

---

## Why this isn't another RAG demo

Most RAG systems retrieve, generate, and stop. Whether the generated answer is actually supported by the retrieved evidence is left to the reader.

This system closes that loop. Every answer is decomposed into claims, and each claim is scored against its cited evidence by a fine-tuned faithfulness verifier:

```
🟢 Supported     support ≥ 0.70    the evidence backs this
🟡 Weak          0.45 – 0.69       partial / uncertain support
🔴 Unsupported   < 0.45            the evidence does not back this
⚪ Abstention     —                the model correctly said the sources don't cover it
```

**The verifier is the contribution.** Generation is a hosted LLM call; anyone can do that. Building a verifier that actually catches unsupported claims — and knowing precisely how well it does and doesn't work — is the work.

---

## Architecture

```
question
   │
   ├─► BM25 (sparse)  ─┐
   ├─► dense (MiniLM)  ─┤─► RRF fusion ─► cross-encoder rerank ─► top-k evidence
   │                    │
   ▼                    ▼
generation (LLM, with citation instructions)
   │
   ▼
claim extraction  (sentence split; [n] markers → per-claim evidence scope)
   │
   ▼
claim-level verification  (fine-tuned DeBERTa; cited claims → their cited evidence,
   │                       uncited claims → all retrieved evidence)
   ▼
answer + per-claim grounding scores + unsupported-claim rate
```

**Stack:** FastAPI · Postgres · Qdrant · Redis · BM25 · vLLM · Prometheus/Grafana · Docker · Kubernetes (H200)

---

## The verifier: what worked, what didn't

📄 **[Full writeup: `docs/verifier.md`](docs/verifier.md)** · 🔬 **[Scripts: `verifier_study/`](verifier_study/)**

The verifier began as my thesis entailment model (DeBERTa, trained on RAGTruth). On scientific text it **under-flagged** — removal recall of 19.4%. Handed an obvious fabrication ("RAG was invented in 1995 by a secret government laboratory and requires quantum hardware"), it returned `P(unsupported) = 0.03`. It rubber-stamped a hallucination.

**What fixed it.** Continued fine-tuning on SciFact + HealthVer, over a **custom leakage-safe grouped split** (connected-components over the claim↔abstract graph; zero claim_id or abstract_id crosses splits — the native splits leak abstracts across train/eval, which I checked rather than assumed).

```
                          before      after
P(unsupported) on the
obvious fabrication         0.03  →    0.96      ✓

Recall (grouped test)          —  →    0.84
F1                             —  →    0.77
ECE                        0.058  →    0.19      ← calibration traded for recall,
                                                    deliberately and stated
```

**What didn't.** SciFact/HealthVer is biomedical; the deployed corpus is arXiv CS/ML. So I spent three weeks distilling an LLM teacher's judgments on my own corpus to close that gap. **It did not work**, and the reasons are the most useful thing in this repo:

- The first dataset was **96% contaminated** — splitting by top-1 retrieved paper protects a retrieval *summary*, not the evidence universe that claims actually attach to. Caught by a stricter audit, and the dataset was rebuilt from scratch with a protected-paper split (verified: 11,794 evidence attachments, **0** protected overlap).
- An independent audit of **all 477** claims the teacher labelled unsupported found **218 were actually supported** — 46% false-positive contamination — confirmed by blind human review at 94.3% agreement.
- The evaluation set was measuring the wrong thing: 71 of its 75 unsupported claims were *bait* (trivially off-topic), only 4 were subtle grounded overclaims. A **grounded-hard** stress test was built and human-reviewed.
- A fusion that *appeared* to help turned out to be an artifact. Under **question-grouped out-of-fold stacking** with a **clustered bootstrap**, it was reliably **worse**: −0.074 weighted F1, 95% CI [−0.131, −0.018].
- The auto-cleaning procedure was **pre-registered with an acceptance threshold — and failed it**. No cleaned retrain was run.

**The unadapted SciFact/HealthVer verifier won** (weighted F1 0.403, AUROC 0.788 on grounded-hard) and is what ships. The three weeks of adaptation work produced a *better-understood* verifier, not a better one — and the decision was not to deploy the worse model.

---

## Key results

| | |
|---|---|
| **Verifier (grouped test)** | recall 0.84 · precision 0.71 · F1 0.77 · AUROC 0.71 · ECE 0.19 |
| **Serving (vLLM, H200)** | fp8 vs bf16: **+33–39% throughput** at all concurrencies (prefill-bound workload) |
| | best: **18.8 req/s · 2,599 tok/s · p99 5.8s** @ concurrency 64 |
| | prefix caching: **~0%** on unique-prompt RAG traffic (only ~3.5% shared prefix) |
| **Load test (app layer)** | three stacked bottlenecks found and fixed → **2.2× scaling**, zero errors |
| | BM25 rebuilt per request → build once at startup (8.8s → 2.8s single request) |
| | DB pool exhaustion → sized pool + session scoping |
| | sync model work on the event loop → `asyncio.to_thread` |
| **Cost** | ~**$0.15 per 1,000 answers** at $4/hr GPU, 40% utilization (generation-only) |
| | *utilization dominates GPU price* — the headline finding |

Every number above is reproducible from committed artifacts. See [`docs/`](docs/).

---

## Repo layout

```
backend/                  the production system
  app/
    api/                  FastAPI routes
    services/             retrieval, generation, claim extraction, verification
      verifier.py         interface + label bands
      verifier_real.py    the deployed verifier (S4-only)
    db/                   Postgres + Qdrant
    monitoring/           Prometheus metrics
  load_test/              load-test client + raw results
  data/                   corpus, eval artifacts, benchmark JSONs

cluster/                  vLLM serving benchmark, batch generation + verification
verifier_study/           the verifier research arc (see its README)
  1_scifact_healthver/      the adaptation that worked
  2_arxiv_distillation/     the in-domain attempt that didn't
  3_gold_and_eval/          human gold set + grounded-hard stress test
  4_teacher_audit/          the teacher-contamination finding
demo/                     the live HuggingFace Space app
docs/
  verifier.md             ← the verifier story (start here)
  serving.md              vLLM benchmark: fp8, prefix caching, the artifact I caught
  loadtest.md             the three-bottleneck debugging story
  cost.md                 capacity + cost model
```

---

## Honest limitations

- **The verifier is not calibrated.** ECE ≈ 0.19. Scores are useful as labels and rankings, **not** as literal probabilities.
- **It is recall-oriented.** It over-flags partially-grounded claims. For a safety-oriented verifier that is the intended bias, but it means false positives.
- **Domain gap remains.** The deployed verifier is trained on biomedical claim-verification data and serves a CS/ML corpus. The attempt to close that gap is documented — it failed.
- **Custom splits.** SciFact/HealthVer numbers come from a custom leakage-safe grouped split and are **not** comparable to published benchmark results.
- **Claim extraction is its own failure mode.** Human review found a 6.7% extraction-failure rate (sentence splitting breaks on `vs.`, `e.g.`, `et al.`), independent of verifier accuracy. Fixed in the demo; worth monitoring separately in any claim-level pipeline.
- **The live demo's generator is a hosted LLM** (Mistral via OpenRouter), not the self-hosted Mistral-7B used in the offline evaluation — that model is no longer served. The verifier is the same.
- **The grounded-hard evaluation is a deliberately enriched stress test** (101 binary claims, 15 unsupported), not an estimate of production prevalence. Absolute intervals are wide; paired comparisons are more stable.

---

## Running it

```bash
# infrastructure
docker compose up -d           # Postgres, Qdrant, Redis

# ingest the corpus
python -m app.services.ingest_corpus

# serve
uvicorn app.main:app --reload

# ask something
curl -X POST localhost:8000/verify \
  -H 'Content-Type: application/json' \
  -d '{"question": "How can hallucinations be detected without a source document?"}'
```

The verifier checkpoint lives on HuggingFace: [`Primeinvincible/scifact-healthver-verifier`](https://huggingface.co/Primeinvincible/scifact-healthver-verifier).
