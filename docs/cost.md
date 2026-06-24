# Capacity & Cost Model — Generation-Dominated (M11)

Translates the measured M9 serving throughput into an operating cost for the system's
generation step: **what does it cost to produce a verified answer at scale?** Expressed as
cost per 1,000 answers and answers per GPU-hour.

This model is **generation-dominated by design** — it uses the LLM generation step (the
heaviest component) as the cost basis and **excludes retrieval and verification compute**.
That makes it a clean lower bound on total system cost, with explicit, tunable assumptions
rather than a single opaque figure. (An interactive version of this calculator was built
alongside this doc; all inputs below are adjustable there.)

---

## Headline

At a **market H200 rate (~$4.00/GPU-hr)** and a **realistic 40% utilization**, generating a
verified answer costs roughly:

> **~$0.15 per 1,000 answers** (≈ 0.015¢ each) — generation step only.

This is cheap because a 7B model on an H200 generates fast. But the single figure is less
useful than the two levers that move it:

| Lever | Range tested | Effect |
| --- | --- | --- |
| **GPU price** | $2.60 (neocloud) → $4.00 (market) → $10.60 (hyperscaler) | spans cost ~**4×** |
| **Utilization** | 100% (saturation floor) → 40% (realistic) → 10% (idle-heavy) | spans cost ~**10×** |

**Utilization is the dominant lever** — bigger than the choice of GPU provider. A cheap GPU
run at 10% utilization can cost more per answer than an expensive GPU run at 80%. This is the
core economics lesson: production inference cost is mostly about **keeping the accelerator
fed** (batching, request consolidation), not about finding the lowest hourly rate.

---

## The model (how the numbers compose)

All inputs are measured or explicitly assumed:

1. **Generation throughput** *(measured, M9)*: fp8 + prefix caching, H200, concurrency 64,
   unique-prompt RAG workload → **~2,599 output tokens/sec**.
2. **Tokens per answer** *(measured, M9)*: ~**138** completion tokens average.
3. **Answers/sec at saturation** = 2,599 ÷ 138 ≈ **18.8 answers/sec** (100% utilization).
4. **Utilization factor** *(assumed)*: real serving never runs at 100% (queuing blows up
   latency — demonstrated in the M10A load test). A realistic steady-state is ~30–50%; this
   model defaults to **40%** → ~7.5 answers/sec.
5. **Answers/GPU-hour** = answers/sec × 3,600.
6. **Cost/answer** = GPU $/hr ÷ answers/GPU-hour. **Cost/1,000** = ×1,000.

Worked example (market rate, 40% util):
- 18.8 answers/s × 0.40 = 7.5 answers/s → ~27,100 answers/GPU-hour
- $4.00 ÷ 27,100 ≈ $0.000148/answer → **~$0.15 / 1,000 answers**

At 100% utilization the floor is ~$0.06/1,000 — included for reference, but **a fantasy floor**,
not an operating number.

---

## What this model deliberately excludes (and why it matters)

- **Retrieval cost** (dense embed + Qdrant + BM25): small per query, but non-zero; runs on
  CPU/separate hardware in the current design.
- **Verification cost** (real S2 + S4 fusion): the thesis verifier ran in **batch** (M8), so it
  has per-claim timing but no live-serving throughput. On GPU it would add a second model-inference
  cost per answer — potentially comparable to generation for multi-claim answers. **This is the
  largest excluded term** and would be the next thing to measure for a full-system cost.
- **Idle / overhead**: model load time, autoscaling lag, non-inference CPU. Folded loosely into
  the utilization factor rather than modeled separately.
- **Networking / storage / egress**: provider-dependent; can dominate for data-heavy workloads
  (egress alone is $0.08–0.12/GB on hyperscalers).

So the headline figure is a **generation-only lower bound**. Total cost-per-answer is higher,
dominated by whatever the verification step costs once served live.

---

## Caveats

- **Pricing is a mid-2026 snapshot.** H200 on-demand spans ~$2.30–$13.78/GPU-hr across providers
  (working median ~$3.95–4.00); expected to soften through 2026 as Blackwell B200/B300 ship.
- **Throughput is config-specific.** The 2,599 tok/s figure is fp8 + prefix caching at concurrency
  64 on a *single* H200 with this prompt shape (~2,247 prompt tokens). Different model, hardware,
  context length, or batch settings change it (see `docs/serving.md`).
- **Single-GPU basis.** Multi-GPU scaling is roughly linear for throughput but adds coordination
  and availability cost not modeled here.

## Takeaway

The generation step is cheap (~$0.15/1k answers at realistic utilization), and **utilization, not
GPU price, is the dominant cost driver** — which is why production inference economics centers on
keeping the GPU saturated. The honest total-system cost is higher and gated by the verification
step's live-serving cost, which is the clear next measurement.
