# The Verifier

The verifier is what makes this system a *verified* RAG system rather than another RAG demo. It scores every generated claim against the evidence that claim cites, and reports how much of the answer is actually grounded.

This document records how that verifier was built, the one adaptation that worked, and a three-week in-domain adaptation study that **did not** work — and why the negative result is reported rather than buried.

**Deployed verifier:** a DeBERTa faithfulness classifier fine-tuned on a custom leakage-safe grouped split of SciFact + HealthVer. Live demo: [Verified Research RAG](https://huggingface.co/spaces/Primeinvincible/verified-research-rag) · Model: [`Primeinvincible/scifact-healthver-verifier`](https://huggingface.co/Primeinvincible/scifact-healthver-verifier)

---

## 1. The starting point, and the failure that motivated everything

The verifier began as the entailment signal (S4) from my thesis: a DeBERTa classifier trained on **RAGTruth**, predicting `P(hallucination)` for a `(claim, evidence)` pair. On RAGTruth it performs well (AUROC 0.847 standalone; 0.875 fused with a relevance signal, ECE 0.058).

On **scientific text it under-flagged**. The batch evaluation over the arXiv corpus measured removal recall of **19.4%** — it missed four out of five unsupported claims.

That number is abstract until you watch it happen. Wiring the real verifier into the live path and handing it an obvious fabrication:

```
claim:    "RAG was invented in 1995 by a secret government laboratory
           and requires quantum hardware."
evidence: "We introduce retrieval-augmented generation (RAG), which combines
           a pretrained parametric generator with a non-parametric retrieval
           component over Wikipedia."

S4 P(unsupported) = 0.03      →  label: Supported
```

The verifier rubber-stamped it. A live demo whose central claim is "this system catches hallucinations" cannot ship with a verifier that does this. Hosting a bad verifier is worse than hosting no demo.

**Root cause:** RAGTruth is summarization/QA over news and general web text. The verifier had never seen a scientific claim–abstract pair. It was out of domain.

---

## 2. What worked: SciFact + HealthVer adaptation

The fix was to continue fine-tuning S4 on public **scientific claim-verification** data, where the "unsupported" class is densely represented and in-domain.

**Data.** `allenai/scifact_entailment` + `dwadden/healthver_entailment` — both `(claim, abstract) → SUPPORT | CONTRADICT | NEI`. Collapsed to binary, since the deployed verifier answers one question ("does this evidence support this claim?"): `SUPPORT → 0`, `CONTRADICT + NEI → 1`.

**Leakage control.** The datasets' native splits are split *by claim*, but the same **abstract** recurs across splits — one COVID abstract carries many claims. A first pass caught it:

```
abstract_id overlap: train↔val 406,  train↔test 217,  val↔test 186
```

If an abstract appears in training, the model has memorized its wording before it ever appears at evaluation. So the split was rebuilt: **connected components** over the (claim ↔ abstract) graph, split whole components, stratified by source.

```
train 6715 · val 840 · test 839
claim_id overlap: 0      abstract_id overlap: 0
```

This is a **custom leakage-safe grouped split**, not the official SciFact/HealthVer benchmark split — numbers here are not comparable to published leaderboards, by design.

**Result (grouped test, S4-only):**

| | |
|---|---|
| F1 | 0.77 |
| Precision | 0.71 |
| **Recall** | **0.84** |
| AUROC | 0.71 |
| ECE | 0.19 |

Recompute these from committed artifacts: 
```
python verifier_study/3_gold_and_eval/reproduce_bootstrap.py
```
And the failing case:

```
"RAG was invented in 1995 by a secret government laboratory..."
    before:  P(unsupported) = 0.03   →  Supported     ✗
    after:   P(unsupported) = 0.96   →  Unsupported   ✓
```

**The honest tradeoff:** recall is up, calibration is down. The thesis verifier's ECE was 0.058; this one is 0.19. It is a *recall-oriented* verifier whose scores are useful as **labels and rankings, not as literal probabilities**. For a system whose job is to catch unsupported claims, that is the right trade — but it is a trade, and it is stated rather than hidden.

**A note on scope.** This is a *side-project adaptation* of the thesis verifier, not the thesis result. The thesis artifacts (RAGTruth S4 + out-of-fold fusion) are untouched and remain the better-calibrated system on their native domain.

---

## 3. What didn't work: in-domain arXiv distillation

SciFact and HealthVer are **biomedical**. The deployed corpus is **arXiv CS/ML**. Fixing one domain gap left another. The obvious next step: distil a strong teacher's judgments on *my own* corpus and adapt the verifier to the domain it actually serves.

It didn't work — and the reasons are more interesting than a positive result would have been.

### 3.1 The first dataset was 96% contaminated

The v1 pipeline split questions by their **top-1 retrieved paper**, which seemed sufficient. It wasn't. After generation, claims attach evidence from *many* papers, not just the top-1. A stricter audit against the actual attached evidence:

```
Gold claims checked:      355
Contaminated:             341
Clean:                     14
Contamination rate:      96.1%
```

**The lesson, stated as a rule:** *protect every paper that appears in the final gold evidence set, then build the training pool only from papers outside that protected set.* Splitting on a retrieval *summary* protects nothing; you must split on the evidence universe that actually gets used.

The v1 training set was abandoned.

### 3.2 The leakage-safe v2 rebuild

```
Corpus papers:                  250
Protected gold-evidence papers:  99
Safe training papers:           151
```

Questions were regenerated over the safe pool only; retrieval was filtered (retrieve top-10 → drop protected papers → keep top-3 safe). Mistral-7B generated answers (plain + cited arms); claims were extracted with citation-scoped evidence.

```
Claims: 2227      Evidence attachments: 11794
Protected overlap: 0
```

Zero. That check is the load-bearing one.

### 3.3 The teacher was wrong 46% of the time

Training labels came from **Llama-3.3-70B** (deliberately not Opus, which was reserved as an independent auditor):

```
SUPPORTED 1535 · UNSUPPORTED 477 · ABSTENTION 215
```

A post-hoc audit of **all 477** claims the teacher called unsupported, using Opus as an independent judge, found:

```
relabeled SUPPORTED:   218    ← 46% of the "unsupported" class
relabeled UNSUPPORTED: 181
relabeled ABSTENTION:   78
```

A **blind human audit** of 100 of these disagreements confirmed the corrections: **94.3% agreement** on the proposed supported→unsupported reversals. The teacher's positive class was substantially contaminated with false positives.

The obvious move — auto-clean the labels and retrain — was **pre-registered with an acceptance threshold**, and it *failed* that threshold: the abstention corrections reached only 30.0% exact agreement and 73.3% binary action agreement with human review. Below the bar. **No cleaned retrain was performed.** Pre-registering the rule is what made it possible to fail it honestly instead of tuning until the answer looked good.

### 3.4 The evaluation set was measuring the wrong thing

The human-reviewed gold set (355 claims, human-labeled three-way) looked like a triumph for the base verifier — F1 0.75, AUROC 0.977. Then:

```
75 unsupported claims in gold
  71 were bait      ← trivially out-of-topic
   4 were grounded  ← the actual hard case
```

The gold set was measuring *"can you spot a question the corpus doesn't cover"*, not *"can you spot a subtle overclaim from partially-relevant evidence."* The second is the problem that matters. So a **grounded-hard** stress test was built: answers generated under deliberately weakened or censored evidence (keep only a weak home chunk; add distractors; remove the strongest evidence), then **human-reviewed**.

Anti-circularity was enforced explicitly: no evaluated verifier was allowed to generate, sample, or label its own evaluation set.

### 3.5 Original grounded-hard model-selection result

The original human-reviewed grounded-hard model-selection tranche contained **101 binary claims, 15 unsupported, and 62 question clusters**. This is the tranche used to compare the lightweight verifier variants, relevance signal, arXiv fine-tuning, and fusion heads; the bootstrap resamples all 62 clusters:

| Model |  Binary F1(unsupported class, design-weighted) | Precision | Recall | AUROC |
|---|---:|---:|---:|---:|
| **Base SciFact/HealthVer (unadapted)** | **0.403** | **0.285** | 0.689 | **0.788** |
| S2 + base, train-fitted fusion | 0.395 | 0.277 | 0.689 | 0.741 |
| arXiv-fine-tuned SciFact/HealthVer | 0.366 | 0.249 | 0.689 | 0.737 |
| S2 + fine-tuned, **OOF fusion** | 0.329 | 0.216 | 0.689 | 0.735 |
| Relevance signal (S2) alone | 0.254 | 0.145 | 1.000 | 0.734 |

**The unadapted verifier won.** arXiv teacher-label adaptation did not reliably improve anything.

And the fusion result is worth dwelling on. A validation-fitted fusion *appeared* to help. Under **question-grouped out-of-fold stacking** — the leakage-resistant protocol — the advantage vanished and inverted:

```
OOF fusion vs. base verifier,  Binary F1(unsupported class, design-weighted):  -0.074
95% question-clustered bootstrap CI:        [-0.131, -0.018]
```

Reliably **worse**. The earlier "improvement" was the fusion head having seen the same partition used to select its own threshold.

### 3.6 Expanded external baseline and cascade evaluation

The original model-selection tranche had only 15 unsupported positives, which was enough to expose
the lightweight-model ordering but too small for strong claims about an external verifier baseline
or a routing policy. I therefore expanded the **same model-independent stratified human-review
protocol** from 150 to **500 reviewed claims**, preserving the original 150 judgments by `claim_id`
and reviewing 350 newly sampled claims.

The expanded review contains:

```text
500 reviewed rows
288 SUPPORTED
 51 UNSUPPORTED
122 ABSTENTION
 39 INVALID_EXTRACTION
```

Binary evaluation excludes abstentions and invalid extractions, leaving **339 claims: 288
supported and 51 unsupported**. Sampling weights are recomputed from the 500-claim stratified
sample; all paired uncertainty estimates resample whole `qid` clusters.

On exactly those 339 binary claims:

| System | Precision | Recall | Binary F1 | AUROC |
|---|---:|---:|---:|---:|
| Deployed SciFact/HealthVer DeBERTa | 0.277 | **0.745** | 0.404 | 0.773 |
| **Bespoke-MiniCheck-7B** | **0.805** | 0.569 | **0.666** | **0.878** |
| Confirmation cascade | **0.866** | 0.510 | 0.642 | — |

The expanded benchmark preserved the main conclusion while correcting the absolute scale of the
smaller pilot: MiniCheck remained substantially stronger than the deployed DeBERTa, but its Binary
F1 fell from 0.769 on the original 101-claim tranche to **0.666** on the larger 339-claim
benchmark.

The targeted **confirmation cascade** uses a simple label-independent rule:

```text
DeBERTa predicts SUPPORTED   -> accept
DeBERTa predicts UNSUPPORTED -> MiniCheck makes the final decision
```

It sent **137/339 claims (40.4%)** to MiniCheck and reached Binary F1 **0.642**. Relative to
DeBERTa-only, the paired question-clustered improvement was:

```text
Delta F1 = +0.238
95% CI   = [+0.090, +0.362]
```

Relative to MiniCheck-only:

```text
Delta F1 = -0.025
95% CI   = [-0.097, +0.039]
```

That difference is not distinguishable from zero on this stress test, but it is **not evidence of
equivalence**.

The confirmation rule has a structural recall limit: any claim DeBERTa predicts `SUPPORTED` is
accepted immediately, so MiniCheck never gets a chance to recover DeBERTa false negatives. This
explains why cascade recall is **0.510**, below DeBERTa-only at 0.745 and MiniCheck-only at 0.569,
while precision rises sharply to **0.866**. The policy is primarily correcting DeBERTa's false
positive `UNSUPPORTED` calls.

A generic uncertainty-routing policy did not work. Escalating claims closest to DeBERTa's frozen
`P(unsupported)=0.06` decision threshold improved only slowly; even at **74.9% MiniCheck usage**,
Binary F1 reached just **0.479**, far below MiniCheck-only at 0.666. DeBERTa's errors were
therefore not concentrated near its decision boundary in a way that made margin-based routing
useful.

### 3.7 H200 quality–compute measurement

The same 339 binary claim/evidence pairs were then timed on one NVIDIA H200. Model download/load
time was measured separately and **excluded**; each model received a warmup; MiniCheck prefix
caching was disabled to match the quality evaluation. This is a sequential steady-state compute
measurement, not a production concurrency/load test.

| Policy | Binary F1 | Time / 339 claims | Effective claims/s | Cost / 1k claims* | Cost / 1k answers** |
|---|---:|---:|---:|---:|---:|
| DeBERTa-only | 0.4041 | 1.646 s | 205.9 | $0.0054 | $0.024 |
| Confirmation cascade | **0.6417** | 4.356 s | 77.8 | **$0.0143** | **$0.064** |
| MiniCheck-only | **0.6664** | 5.781 s | 58.6 | $0.0189 | $0.085 |

\* Assumes $4/H200-hour and counts only measured inference time.
\** Uses the M8 cited-arm average of 193 claims / 43 answers = 4.49 claims per answer.

The cascade recovers **96.3% of MiniCheck-only F1 at 75.3% of its measured verification compute
cost**. It is 2.65× the DeBERTa-only inference time, versus 3.51× for MiniCheck-only. The 40.4%
escalation rate should therefore **not** be read as 40.4% of MiniCheck cost: every claim still pays
for the DeBERTa pass first.

Observed GPU memory in this configuration was about **3.1 GiB peak for DeBERTa** and roughly
**131 GiB for the MiniCheck runtime**. The latter is a runtime/configuration footprint, not an
intrinsic memory requirement of the model itself.

These are **quality-compute measurements on an enriched stress test**, not a frozen production
routing policy. The routing rule itself never uses human labels, but selecting a deployment policy
would still require independent validation data.


---

## 4. What is deployed, and why

```text
Current live verifier:
  base SciFact/HealthVer S4  (S4-only, no fusion)

Rejected lightweight variants:
  · relevance signal (S2) standalone      — F1 0.254; detects topic mismatch, not support
  · original thesis S4                    — out of domain, over-flags (219/270 gold as unsupported)
  · arXiv-fine-tuned S4                   — no reliable improvement
  · validation-fitted fusion              — advantage was an artifact
  · OOF fusion                            — reliably worse (95% CI excludes zero)

Stronger offline result, not yet the live path:
  · MiniCheck-7B                          — F1 0.666, AUROC 0.878 on expanded grounded-hard
  · confirmation cascade                  — F1 0.642 with 40.4% MiniCheck escalation
```

The deployed S4 remains the current live verifier because it is already integrated, lightweight,
and operationally simple. The expanded evaluation shows that **MiniCheck-7B is the stronger
verifier offline**, so the deployment choice should no longer be read as evidence that DeBERTa is
the best available model.

There are concrete operational reasons it has not simply been swapped in. The public Hugging Face
Space is CPU-constrained, while the tested MiniCheck runtime is a 7B serving stack; on the H200
efficiency run it occupied roughly **131 GiB** in this configuration. The backend could host a GPU
cascade, but doing that responsibly would require batching/serving integration, failure handling,
live latency characterization, and an independently validated routing policy. The new H200
benchmark answers the first cost question; it does not turn the stress-test routing rule into a
production policy.

The live interface now uses the **same frozen binary operating point as the evaluation**:
`P(unsupported) >= 0.06 -> Unsupported`, otherwise `Supported`. The 0.06 threshold was selected on
the held-out leakage-safe grouped SciFact+HealthVer validation split by unsupported-class F1, then
frozen before grouped test and grounded-hard evaluation; the grounded-hard labels were not used to
tune it.

That protocol avoids test-set tuning, but it does **not** solve domain shift: the threshold was
selected on biomedical SciFact/HealthVer, while the live corpus is arXiv CS/ML. There is currently
no independent in-domain validation split for operating-point selection. The grounded-hard
precision of 0.277 is consistent with this remaining domain/operating-point mismatch, and those
labels are deliberately not reused to retune the threshold. Since the public interface exposes
`support_score = 1 - P(unsupported)`, the equivalent rule is
`support_score <= 0.94 -> Unsupported`.

The previous `Supported / Weak / Unsupported` UI bands were removed because only one decision
threshold had actually been validated. With ECE ≈ 0.19, neither `P(unsupported)` nor
`support_score` should be read as a literal probability/confidence value; the score is retained
for ranking and auditability, while the binary label uses the frozen validation-selected operating
point.


---

## 5. A separate finding: claim extraction is its own failure mode

The original 150-row grounded-hard review found **10 invalid claim extractions (6.7%)**. The expanded 500-row review found **39 invalid extractions (7.8%)**, confirming that extraction is a persistent failure mode independent of verifier accuracy. Sentence-splitting on `.` breaks on `vs.`, `e.g.`, `et al.`; the verifier then dutifully scores a sentence *fragment* and flags it unsupported. The verifier may be behaving consistently; the input itself is malformed.

The fix is now aligned across the backend and standalone live demo: abbreviation-masked sentence splitting, structural list/block segmentation, markdown stripping, citation-debris cleanup, and explicit abstention detection. The demo carries a mirrored pure extractor module because it is deployed independently, and CI asserts that mirror stays identical to the backend version. The general lesson: **in a claim-level verification pipeline, extraction quality must be monitored separately from verifier quality**, or extraction failures will be misattributed to the model.

---

## 6. Abstention is not hallucination

A claim asserting the *absence* of information — *"the provided sources do not discuss quantum computing"* — is the model **correctly refusing**, not hallucinating. A binary support verifier has no way to express this: it sees a claim unsupported by the evidence and flags it red.

Left uncorrected, the demo's most dramatic case (a question the corpus can't answer) reported *"100% of claims unsupported"* when the model had in fact done exactly the right thing. Abstentions are now detected, labelled separately, and **excluded from the unsupported rate** — a rule pre-registered during gold-set construction, not invented after seeing the output.

---

## 7. Honest limitations

- **Not calibrated.** ECE ≈ 0.19. Scores rank and label; they are not probabilities.
- **Operating point is out of domain.** The 0.06 threshold is validation-selected without test leakage, but the validation domain is biomedical SciFact/HealthVer rather than arXiv CS/ML. No independent in-domain threshold-validation split currently exists.
- **Enriched evaluation.** Grounded-hard is a deliberately hard stress test, not an estimate of production prevalence. The expanded human review has 500 rows and yields **339 binary claims / 51 unsupported** after excluding abstentions and invalid extractions. This materially strengthens the positive-class evidence over the original 101/15 tranche, but the resulting class balance still should not be interpreted as production prevalence.
- **Cascade is offline.** Its quality and sequential H200 compute cost are measured, but it still lacks an independent policy-validation set and production serving/batching/failure-path validation.
- **Custom splits.** Reported SciFact/HealthVer numbers come from a custom leakage-safe grouped split and are **not** comparable to published benchmark results.
- **Domain gap remains.** The deployed verifier is biomedical-trained, serving a CS/ML corpus. The attempt to close that gap is documented above — it failed.
- **The negative result is bounded.** It applies to *this* teacher-labeled pipeline, not to in-domain adaptation in principle. A cleanly curated in-domain training set might well succeed; the one that could be built with an LLM teacher at this budget did not.


---

## 8. What this study is actually evidence of

The in-domain teacher-distillation experiment did **not** improve the lightweight verifier. What the study produced instead is a stronger evaluation and decision-making process:

- a leakage audit that caught a **96% contaminated** dataset that had passed a naive split check;
- an independent audit finding **46% false positives** in a teacher's positive class, human-validated at 94.3%;
- a **pre-registered decision rule that was allowed to fail**, blocking a retrain that would have looked good and been wrong;
- an evaluation set rebuilt after discovering the first one measured the easy problem (bait) rather than the hard one (subtle overclaim);
- **question-grouped OOF stacking + clustered bootstrap CIs** that turned an apparent fusion improvement into a measured regression;
- an expanded 500-row human review that raised the binary hard-positive count from **15 to 51**;
- an external MiniCheck-7B baseline showing that the deployed lightweight verifier is **not** the strongest available verifier on this domain;
- a confirmation cascade that recovered most of MiniCheck's Binary F1 while invoking it on **40.4%** of claims;
- an H200 efficiency benchmark showing that the cascade reaches **96.3% of MiniCheck-only F1 at 75.3% of its measured verification compute cost**, rather than assuming escalation rate equals cost;
- an H200 efficiency benchmark showing that the cascade reaches **96.3% of MiniCheck-only F1 at 75.3% of its measured verification compute cost**, rather than assuming escalation rate equals cost;
- and a generic uncertainty cascade that failed, preventing a superficially attractive routing story from being overstated.

The useful result is not that every experiment succeeded. It is that the system's claims were repeatedly revised when stronger evaluation contradicted the earlier story.

---

### Artifacts

| | |
|---|---|
| Deployed verifier | [`Primeinvincible/scifact-healthver-verifier`](https://huggingface.co/Primeinvincible/scifact-healthver-verifier) |
| Live demo | [Verified Research RAG](https://huggingface.co/spaces/Primeinvincible/verified-research-rag) |
| Adaptation pipeline | `verifier_study/1_scifact_healthver/` |
| Distillation pipeline | `verifier_study/2_arxiv_distillation/` |
| Gold set + evaluation | `verifier_study/3_gold_and_eval/` |
| Expanded 500-row labels | `backend/data/grounded_hard_eval/grounded_hard_random_review_500_labeled.jsonl` |
| Expanded model predictions | `backend/data/grounded_hard_eval/grounded_hard_500_model_predictions.jsonl` |
| Expanded summary | `backend/data/grounded_hard_eval/grounded_hard_500_eval_summary.json` |
| Uncertainty-cascade curve | `backend/data/grounded_hard_eval/grounded_hard_500_uncertainty_cascade_curve.csv` |
| H200 verifier-efficiency script | `verifier_study/3_gold_and_eval/benchmark_verifier_efficiency_h200.py` |
| H200 verifier-efficiency result | `backend/data/grounded_hard_eval/verifier_efficiency_h200.json` |
| H200 verifier-efficiency script | `verifier_study/3_gold_and_eval/benchmark_verifier_efficiency_h200.py` |
| H200 verifier-efficiency result | `backend/data/grounded_hard_eval/verifier_efficiency_h200.json` |
| Teacher audit | `verifier_study/4_teacher_audit/` |
