# Verified Research RAG System

**A research agent that measures and reports the grounding of its own answers.**

Ask a question over a 250-paper arXiv corpus. The system retrieves evidence, generates a cited answer, then **verifies every claim against the evidence that claim cites** — and reports how much of its own answer is actually supported.

### ▶ [Try it live](https://huggingface.co/spaces/Primeinvincible/verified-research-rag)

The interesting example is the third one: it asks about something the corpus doesn't cover. The system says so, and the grounding report shows it *abstained* rather than fabricated.

---

## Why this isn't another RAG demo

Most RAG systems retrieve, generate, and stop. Whether the answer is actually supported by the retrieved evidence is left to the reader.

This system closes that loop. Every answer is decomposed into claims, and each claim is scored against **the evidence it cites**:

```
🟢 Supported     support ≥ 0.70     the cited evidence backs this
🟡 Weak          0.45 – 0.69        partial / uncertain support
🔴 Unsupported   < 0.45             the evidence does not back this
```

A claim citing `[2]` is checked against source 2 — so a claim that cites a source which doesn't actually support it gets caught. An uncited claim is checked against *all* retrieved evidence (fair-chance policy): if nothing in the retrieved evidence supports it, it is marked unsupported relative to the available context.

**The contribution is the evaluation and audit loop around grounded generation.** The system does not just attach a verifier and report one score; it tests whether the verifier, labels, splits, sampling protocol, fusion logic, and serving measurements are themselves trustworthy. That process caught leakage, noisy teacher labels, a misleading evaluation set, a harmful fusion model, and a benchmark artifact — and the failed variants are kept as part of the evidence rather than hidden.

---

## Architecture

```
question
   │
   ├─► BM25 (sparse)   ─┐
   ├─► dense (MiniLM)  ─┤─► RRF fusion ─► cross-encoder rerank ─► top-k evidence
   │                     │
   ▼                     ▼
generation  (hosted LLM, prompted for cited plain prose)
   │
   ▼
claim extraction  (structural + sentence segmentation; [n] markers → per-claim evidence scope)
   │
   ▼
claim-level verification  (fine-tuned DeBERTa, one forward pass per claim)
   │
   ▼
answer + per-claim grounding scores + unsupported-claim rate
```

**Stack:** FastAPI · Postgres · Qdrant · Redis · BM25 · vLLM (benchmarks) · Prometheus/Grafana · Docker · Kubernetes (H200)

The diagram above is the **current live path**. MiniCheck-7B and the cascade results below are evaluation results; they have not yet replaced the deployed DeBERTa verifier.

---

## Verification study: what worked, what failed, what we learned

📄 **[Full writeup: `docs/verifier.md`](docs/verifier.md)** · 🔬 **[Scripts: `verifier_study/`](verifier_study/)**

The verifier began as my thesis entailment model (DeBERTa, trained on RAGTruth). On scientific text it **under-flagged** — removal recall of 19.4%. Handed an obvious fabrication ("RAG was invented in 1995 by a secret government laboratory and requires quantum hardware"), it returned `P(unsupported) = 0.03`. It rubber-stamped a hallucination.

**What fixed that specific failure.** Continued fine-tuning on SciFact + HealthVer over a **custom leakage-safe grouped split** — connected components over the claim↔abstract graph, so no claim *or abstract* crosses train/eval. (The datasets' native splits leak abstracts across splits; I checked rather than assumed.)

```
                                        before      after
P(unsupported) on the obvious fabrication  0.03  →   0.96     ✓
recall (grouped test)                         —  →   0.84
F1                                            —  →   0.77
ECE                                       0.058  →   0.19     ← calibration traded for
                                                                 recall, deliberately
```

**What didn't.** SciFact/HealthVer is biomedical; the corpus is arXiv CS/ML. So I spent three weeks distilling an LLM teacher's judgments on my own corpus to close that gap. **It did not work**, and the reasons are the most useful thing in this repo:

- The first dataset was **96% contaminated**. Splitting by top-1 retrieved paper protects a retrieval *summary*, not the evidence universe claims actually attach to. Caught by a stricter audit; rebuilt with a protected-paper split (verified: 11,794 evidence attachments, **0** protected overlap).
- An independent audit of **all 477** claims the teacher labelled unsupported found **218 were actually supported** — 46% false-positive contamination — confirmed by blind human review at 94.3% agreement.
- The evaluation set was measuring the wrong thing: 71 of its 75 unsupported claims were *bait* (trivially off-topic); only 4 were subtle grounded overclaims. A **grounded-hard** stress test was built and human-reviewed.
- A fusion that *appeared* to help was an artifact. Under question-grouped **out-of-fold stacking** with a **clustered bootstrap**, it was reliably **worse**: −0.074 Binary F1 (unsupported class, design-weighted), 95% CI [−0.131, −0.018].
- The auto-cleaning procedure was **pre-registered with an acceptance threshold — and failed it**. No cleaned retrain was run.

**Among the lightweight variants, the unadapted SciFact/HealthVer verifier performed best** on the original 101-claim grounded-hard model-selection tranche (Binary F1 0.403, AUROC 0.788), so the worse arXiv-adapted variants were not deployed.

A stronger external baseline changed the picture. I expanded the same model-independent stratified human review from **150 to 500 reviewed claims**. After excluding 122 abstentions and 39 invalid extractions, the expanded grounded-hard binary benchmark contains **339 claims: 288 supported and 51 unsupported**. On this larger set, the deployed DeBERTa reached precision 0.277, recall 0.745, Binary F1 **0.404**, and AUROC **0.773**. **Bespoke-MiniCheck-7B** reached precision **0.805**, recall 0.569, Binary F1 **0.666**, and AUROC **0.878**. MiniCheck therefore remained substantially stronger in F1 and ranking quality, but the larger benchmark also showed that the original 101-claim tranche had overstated its absolute F1.

That led to two routing experiments on the expanded benchmark. A generic **uncertainty cascade still failed**: even escalating 74.9% of claims to MiniCheck reached only F1 **0.479**, suggesting that DeBERTa's errors were not concentrated near its decision threshold. A more targeted **confirmation cascade** worked much better: accept DeBERTa's `SUPPORTED` decisions, but send every DeBERTa `UNSUPPORTED` decision to MiniCheck for confirmation. It escalated **137/339 claims (40.4%)**, reached precision **0.866**, recall 0.510, and F1 **0.642**. The paired F1 gain over DeBERTa was **+0.238**, 95% CI **[+0.090, +0.362]**. Its F1 difference from MiniCheck-only was **−0.025**, 95% CI **[−0.097, +0.039]** — not distinguishable on this stress test, but not evidence of equivalence.

These cascade results are **quality–compute measurements on an enriched stress test, not a validated deployment policy**. The routing rule itself does not use human labels, but selecting a production policy would still require independent validation data.

---

## Key results

| | |
|---|---|
| **Lightweight verifier** (custom leakage-safe grouped SciFact+HealthVer test) | recall 0.84 · precision 0.71 · F1 0.77 · AUROC 0.71 · ECE 0.19 |
| **Expanded grounded-hard: deployed DeBERTa** | 339 binary claims / 51 unsupported · precision 0.277 · recall 0.745 · Binary F1 **0.404** · AUROC 0.773 |
| **Expanded grounded-hard: MiniCheck-7B** | precision **0.805** · recall 0.569 · Binary F1 **0.666** · AUROC **0.878** |
| **Expanded grounded-hard: confirmation cascade** | MiniCheck on **40.4%** of claims · precision **0.866** · recall 0.510 · Binary F1 **0.642** |
| **Serving** (vLLM, H200, Mistral-7B) | fp8 vs bf16: **+33–39% throughput** at all concurrencies (prefill-bound) |
| | best: **18.8 req/s · 2,599 tok/s · p99 5.8 s** @ concurrency 64 |
| | prefix caching: **~0%** on unique-prompt RAG traffic (only ~3.5% shared prefix — an earlier "+46%" was a benchmarking artifact from accidentally repeated prompts) |
| **Load test** (app layer, stubbed model calls) | three stacked bottlenecks found and fixed → **2.2× scaling**, zero errors |
| | BM25 rebuilt per request → built once at startup (8.8 s → 2.8 s single request) |
| | DB pool exhaustion → sized pool + session scoping |
| | sync model work on the event loop → `asyncio.to_thread` |
| **Cost** | ~**$0.15 per 1,000 answers** at $4/hr GPU, 40% utilisation (generation only) |
| | *utilisation dominates GPU price* — the headline finding |

**What is reproducible from this repo:** the M8 evaluation (409 claims), the serving benchmarks, the grounded-hard model comparison, the MiniCheck-7B baseline, and both cascade analyses — the human labels, per-model predictions, metrics, and bootstrap CIs are committed under `backend/data/`. **What is not:** model checkpoints (the deployed DeBERTa checkpoint lives on [HuggingFace](https://huggingface.co/Primeinvincible/scifact-healthver-verifier)), the full 1,245-claim generation pool, and the raw bootstrap replicates. Fine-tuning scripts assume a cluster workspace. This is *documented provenance plus reproducible headline results* — not a one-command rebuild of everything.

---

## Running it

Requires Docker and Python 3.10+. Generation needs an `OPENROUTER_API_KEY`
([get one](https://openrouter.ai/keys) — queries cost fractions of a cent).

```bash
# from the repository root
cp .env.example backend/.env      # then add your OPENROUTER_API_KEY
docker compose up -d              # Postgres, Qdrant, Redis, Prometheus, Grafana

cd backend
pip install -r requirements.txt

python -m app.db.init_db                # create tables + Qdrant collection
python -m app.services.ingest_corpus    # ingest the 250-paper corpus (committed)

uvicorn app.main:app --reload
```

The verifier checkpoint (~700MB) is **not** in the repo — it is pulled from
[HuggingFace](https://huggingface.co/Primeinvincible/scifact-healthver-verifier) on first
startup and cached. No manual download.

Startup prints which components are live. There is **no silent degradation**:

```
[verifier] loading Primeinvincible/scifact-healthver-verifier (HuggingFace Hub) ...
[verifier] ready on cpu.
[startup] BM25 index built over 250 chunks.
[startup] verifier:  RealVerifier
[startup] generator: OpenRouterClient
```

Then:

```bash
curl "http://localhost:8000/verify?q=How+can+hallucinations+be+detected+without+a+source+document&top_k=4"
```

Returns the answer, every extracted claim with its citations, support score and label, and
the unsupported-claim rate. If generation is unavailable, the endpoint returns **503** — it
does not return a fabricated "verified" result.

**Degraded modes are explicit.** Without `OPENROUTER_API_KEY`, generation falls back to a
stub and prints a wall of warnings. `DEV_STUB_VERIFIER=true` swaps in a lexical-overlap stub
for model-free development — and says so. Both defaults are *real*; you have to opt out.

```bash
pytest tests/ -v    # 56 tests. No database or models required.
#   claim extraction, citation mapping, label bands, rate maths
#   generation failure -> typed error -> HTTP 503
#   stub components are machine-detectable
#   model source resolution (pinned Hub revision / local override)
```

---

## Repo layout

```
backend/                  the application (FastAPI service + evaluation harness)
  app/
    api/                  routes
    services/
      hybrid_search.py    BM25 + dense + RRF + rerank
      generator.py        prompt assembly
      generation_client.py  OpenRouter (real) | stub (explicit opt-in)
      claim_extractor.py  structural + sentence segmentation
      verifier.py         interface, label bands, verifier selection
      verifier_real.py    the deployed verifier (fine-tuned DeBERTa)
      verification_service.py  the pipeline + persistence
    db/                   Postgres + Qdrant
    monitoring/           Prometheus metrics
  tests/                  unit tests for the pure-logic core
  load_test/              load-test client + raw results
  data/                   corpus + committed evaluation artifacts

cluster/                  vLLM serving benchmark, batch generation + verification
verifier_study/           the verifier research arc (see its README)
demo/                     the HuggingFace Space app
docs/
  verifier.md             ← the verifier story (start here)
  serving.md              vLLM benchmark
  loadtest.md             the three-bottleneck debugging story
  cost.md                 capacity + cost model
```

**On `demo/`.** The Space re-implements the pipeline with an in-process index (numpy + BM25
over the 250 abstracts) instead of Postgres and Qdrant, because a free CPU Space cannot run
them. It uses the same retrieval design (BM25 + dense → RRF → cross-encoder rerank) and the
same verifier checkpoint.

The two extractors have **partially diverged**: the demo has abstention detection (which the
backend lacks) and the backend has structural list/block segmentation (which the demo lacks).
Both are fixes to real, separately-observed failures; neither has been ported across yet.
This is a known duplication cost of maintaining a second, dependency-free target, and it is
the first thing to consolidate.

---

## Honest limitations

- **The deployed DeBERTa verifier is not calibrated.** ECE ≈ 0.19. Scores are useful as labels and rankings, **not** as probabilities.
- **The deployed verifier is recall-oriented and over-flags.** On the expanded grounded-hard benchmark, its Binary F1 is 0.404 with precision 0.277 despite recall 0.745. MiniCheck-7B is substantially stronger on the same claims, but it is not yet the live verifier.
- **The confirmation cascade is not yet a production routing policy.** It reaches F1 0.642 with 40.4% MiniCheck escalation on the expanded stress test; choosing and freezing a deployment policy still requires independent validation data.
- **Domain gap remains.** The deployed verifier is trained on biomedical claim-verification data and serves a CS/ML corpus. The attempt to close that gap with in-domain distillation is documented — it failed.
- **Custom splits.** SciFact/HealthVer numbers come from a custom leakage-safe grouped split and are **not** comparable to published benchmark results.
- **Claim extraction is its own failure mode.** The expanded 500-row human review marked 39 rows as invalid extractions (7.8% raw), independent of verifier accuracy. Fixed (structural segmentation, abbreviation masking) and now regression-tested — but in any claim-level pipeline, extraction quality must be monitored *separately* from verifier quality, or extraction bugs get misattributed to the model.
- **The grounded-hard evaluation is a deliberately enriched stress test**, not an estimate of production prevalence. The expanded human review contains 500 rows; after excluding 122 abstentions and 39 invalid extractions, binary evaluation uses **339 claims with 51 unsupported**. This materially strengthens the positive-class evidence over the original 101-claim / 15-unsupported tranche, but it still should not be interpreted as production prevalence.
- **The demo's generator is not the evaluated generator.** The offline evaluation used self-hosted Mistral-7B; it is no longer served on OpenRouter, so the live path uses a current hosted model. The deployed verifier is the same DeBERTa checkpoint described above.
- **This is a research and serving prototype, not a production service.** No auth, no rate limiting, no CI, no migrations. `/verify` is an unauthenticated GET that writes to the database. The serving *benchmarks* are real (measured on an H200); the *operational* hardening is not there.

---

## Artifacts

| | |
|---|---|
| Live demo | [huggingface.co/spaces/Primeinvincible/verified-research-rag](https://huggingface.co/spaces/Primeinvincible/verified-research-rag) |
| Verifier checkpoint | [`Primeinvincible/scifact-healthver-verifier`](https://huggingface.co/Primeinvincible/scifact-healthver-verifier) |
| The verifier study | [`docs/verifier.md`](docs/verifier.md) · [`verifier_study/`](verifier_study/) |
