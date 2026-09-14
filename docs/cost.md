# Capacity & Cost Model — Generation + Verification

This project now has two separate H200 measurements:

1. a **generation-serving study** for Mistral-7B/vLLM, and
2. a **verification-efficiency study** for DeBERTa-only, the confirmation cascade, and MiniCheck-7B-only.

They answer different questions and use different serving assumptions, so they are reported
side-by-side rather than collapsed into one misleading "production cost" number. The live demo
currently generates through **OpenRouter**; the Mistral/vLLM result is a separate systems benchmark.

---

## 1. Generation serving study

The generation benchmark uses Mistral-7B-Instruct-v0.3 on one H200 with long, unique-evidence RAG prompts.

Measured inputs:

- fp8 + prefix caching, concurrency 64: **~2,599 output tokens/s**
- average completion length: **~138 tokens**
- saturation throughput: about **18.8 answers/s**
- H200 price assumption: **$4.00/GPU-hour**

Using an illustrative **40% utilisation assumption**:

- 18.8 answers/s × 0.40 ≈ 7.5 answers/s
- ≈27,100 answers/GPU-hour
- **≈$0.15 per 1,000 generated answers**

At 100% utilisation the arithmetic floor is about $0.06 / 1,000 answers, but that is not an
operating target: the load test shows latency grows substantially as the system approaches saturation.

The more important systems result is not the dollar figure. On the realistic unique-evidence
workload, **fp8 improved throughput by 33–39%**, while prefix caching was effectively neutral
(±1%). An earlier apparent +46% prefix-cache win came from accidentally repeated prompts and was
removed after the benchmark workload was audited. See `docs/serving.md`.

---

## 2. Verification efficiency study

After the expanded grounded-hard study established that MiniCheck-7B is much stronger than the
deployed DeBERTa verifier, the missing systems question became: **what does that quality gain cost?**

The final verifier benchmark runs the **same 339 binary claim/evidence pairs** used for the quality
comparison on one NVIDIA H200.

Measurement protocol:

- DeBERTa-only, confirmation cascade, and MiniCheck-only use the same claims/evidence.
- DeBERTa keeps the frozen `P(unsupported) >= 0.06` rule.
- Confirmation routing is fixed: DeBERTa `SUPPORTED` → accept; DeBERTa `UNSUPPORTED` → MiniCheck.
- MiniCheck prefix caching is disabled, matching the quality evaluation.
- Each model receives warmup calls.
- Model download/load time is measured separately and **excluded** from inference timing.
- The cascade time is `DeBERTa(all claims) + MiniCheck(routed subset)`.
- Cost assumes **$4.00/H200-hour** and counts measured inference time only.
- Per-answer figures use the M8 cited-arm average: **193 claims / 43 answers = 4.49 claims/answer**.

| Policy | Binary F1 | Time / 339 claims | Effective claims/s | $ / 1k claims | $ / 1k answers* |
|---|---:|---:|---:|---:|---:|
| DeBERTa-only | 0.4041 | 1.646 s | 205.9 | $0.0054 | $0.024 |
| Confirmation cascade | **0.6417** | 4.356 s | 77.8 | **$0.0143** | **$0.064** |
| MiniCheck-7B-only | **0.6664** | 5.781 s | 58.6 | $0.0189 | $0.085 |

\* Compute equivalent under the measured sequential throughput and 4.49 claims/answer assumption;
not a production billing estimate.

### The result that matters

The confirmation cascade achieves:

- **96.3% of MiniCheck-only F1**
- at **75.3% of MiniCheck-only measured verification compute cost**
- while invoking MiniCheck on **40.4%** of claims.

The last two percentages are intentionally different. A 40.4% escalation rate does **not** mean
40.4% of MiniCheck cost because every claim still pays for the DeBERTa pass first.

Relative to DeBERTa-only, the cascade is about **2.65×** the measured inference time. MiniCheck-only
is about **3.51×**.

### The routing trade-off

The confirmation cascade is designed to correct DeBERTa's false-positive `UNSUPPORTED` calls.
Claims DeBERTa labels `SUPPORTED` are never sent to MiniCheck, so MiniCheck cannot recover those
false negatives. That is why:

- DeBERTa recall = 0.745
- MiniCheck-only recall = 0.569
- cascade recall = 0.510

while cascade precision rises to **0.866**.

This is a deliberate quality–compute/precision trade, not a universally better classifier.

### Observed GPU memory

During this particular H200 run:

- DeBERTa peak observed GPU memory: about **3.1 GiB**
- MiniCheck runtime: roughly **131 GiB**

The MiniCheck number is a **runtime/configuration footprint**, not an intrinsic memory requirement
of the 7B model. The serving stack reserves substantial device memory. It does, however, explain
why the stronger verifier is not a drop-in replacement for the current CPU-hosted public demo.

---

## 3. Why the two cost numbers are not simply added

It would be tempting to write:

`$0.15 generation + $0.064 cascade verification = $0.214 / 1k answers`

and call that the system cost. That would be misleading.

The two measurements use different operational assumptions:

- the generation figure applies a **40% utilisation factor** to a separate Mistral/vLLM benchmark;
- the verification figures are **measured sequential inference compute equivalents** with model-load and idle time excluded;
- the live demo generator is **OpenRouter**, not the benchmarked Mistral server;
- retrieval, databases, networking, autoscaling, model residency, and idle GPU time are not jointly modeled.

The correct conclusion is therefore comparative:

> On the measured H200 verification workload, the cascade retains 96.3% of MiniCheck-only F1
> while using 75.3% of its measured verification compute cost.

That result is strong enough without pretending it is a full production TCO model.

---

## 4. Reproducing the verifier benchmark

On the measured cluster image, the MiniCheck/vLLM stack required these environment overrides:

```bash
cd /workspace/verified-research-RAG-system

export VLLM_USE_FLASHINFER_SAMPLER=0
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++

CUDA_VISIBLE_DEVICES=0 python \
  verifier_study/3_gold_and_eval/benchmark_verifier_efficiency_h200.py
```

Committed result:

`backend/data/grounded_hard_eval/verifier_efficiency_h200.json`

The script contains guardrails that check that the timed run reproduces the committed quality
results and the expected 137/339 cascade routing count.

---

## 5. Caveats

- **Pricing assumption:** $4/H200-hour is an explicit reference rate, not a universal cloud price.
- **Not a load test:** the verifier benchmark is sequential steady-state inference, not a concurrency/queueing/SLO measurement.
- **Model load excluded:** cold-start and model-residency costs are not in the verifier figures.
- **Claims per answer:** 4.49 comes from the M8 cited arm (193 claims / 43 answers); another workload will produce a different per-answer cost.
- **Stress-test quality:** F1 values come from the enriched grounded-hard benchmark, not production prevalence.
- **Policy validation:** the confirmation cascade has not been frozen as a production routing policy; independent validation data is still required.
- **Retrieval and infrastructure:** Postgres, Qdrant, Redis, networking, storage, and autoscaling are outside these compute-only comparisons.

## Takeaway

The generation experiment shows that **utilisation and benchmark realism** dominate inference
economics: fp8 helps, while unrealistic prompt repetition can create fake cache wins.

The verification experiment adds the missing quality–cost result: the confirmation cascade
recovers nearly all of MiniCheck's F1 while reducing measured verification compute cost by about
one quarter. That is the deployment motivation; productionizing it would be a separate serving
and policy-validation step.
