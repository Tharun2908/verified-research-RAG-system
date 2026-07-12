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

Recompute these from committed artifacts: python verifier_study/3_gold_and_eval/reproduce_bootstrap.py

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

### 3.5 The result

On the human-reviewed grounded-hard tranche (101 binary claims, 15 unsupported, 11 question clusters):

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

---

## 4. What was deployed, and why

```
Deploy:      base SciFact/HealthVer S4  (S4-only, no fusion)

Do not deploy:
  · relevance signal (S2) standalone      — F1 0.254; detects topic mismatch, not support
  · original thesis S4                    — out of domain, over-flags (219/270 gold as unsupported)
  · arXiv-fine-tuned S4                   — no reliable improvement
  · validation-fitted fusion              — advantage was an artifact
  · OOF fusion                            — reliably worse (95% CI excludes zero)
```

S4-only is also the *simplest* deployable thing: one model, no fusion coefficients, no out-of-fold caveat. `support_score = 1 − P(unsupported)`, mapped to three bands (≥0.70 Supported · 0.45–0.69 Weak · <0.45 Unsupported).

---

## 5. A separate finding: claim extraction is its own failure mode

Human review of 150 grounded-hard rows found **10 invalid claim extractions — a 6.7% raw failure rate**, independent of verifier accuracy. Sentence-splitting on `.` breaks on `vs.`, `e.g.`, `et al.`; the verifier then dutifully scores a sentence *fragment* and flags it unsupported. The verifier was right; the input was garbage.

This is visible in the live demo and was fixed there (abbreviation-masked splitting, markdown stripping, citation-debris cleanup). The general lesson: **in a claim-level verification pipeline, extraction quality must be monitored separately from verifier quality**, or extraction failures will be misattributed to the model.

---

## 6. Abstention is not hallucination

A claim asserting the *absence* of information — *"the provided sources do not discuss quantum computing"* — is the model **correctly refusing**, not hallucinating. A binary support verifier has no way to express this: it sees a claim unsupported by the evidence and flags it red.

Left uncorrected, the demo's most dramatic case (a question the corpus can't answer) reported *"100% of claims unsupported"* when the model had in fact done exactly the right thing. Abstentions are now detected, labelled separately, and **excluded from the unsupported rate** — a rule pre-registered during gold-set construction, not invented after seeing the output.

---

## 7. Honest limitations

- **Not calibrated.** ECE ≈ 0.19. Scores rank and label; they are not probabilities.
- **Enriched evaluation.** The grounded-hard tranche is a deliberately hard stress test, not an estimate of production prevalence. 101 binary claims / 15 unsupported → wide absolute uncertainty; paired comparisons are more stable than absolute numbers.
- **Custom splits.** Reported SciFact/HealthVer numbers come from a custom leakage-safe grouped split and are **not** comparable to published benchmark results.
- **Domain gap remains.** The deployed verifier is biomedical-trained, serving a CS/ML corpus. The attempt to close that gap is documented above — it failed.
- **The negative result is bounded.** It applies to *this* teacher-labeled pipeline, not to in-domain adaptation in principle. A cleanly curated in-domain training set might well succeed; the one that could be built with an LLM teacher at this budget did not.

---

## 8. What this study is actually evidence of

The verifier did not get better. What the three weeks produced instead:

- a leakage audit that caught a **96% contaminated** dataset that had passed a naive split check;
- an independent audit finding **46% false positives** in a teacher's positive class, human-validated at 94.3%;
- a **pre-registered decision rule that was allowed to fail**, blocking a retrain that would have looked good and been wrong;
- an evaluation set rebuilt after discovering the first one measured the easy problem (bait) rather than the hard one (subtle overclaim);
- **question-grouped OOF stacking + clustered bootstrap CIs** that turned an apparent fusion improvement into a measured regression;
- and the decision **not to ship** a model that three weeks of work had produced, because it was worse.

That is the result. The verifier that ships is the honest one.

---

### Artifacts

| | |
|---|---|
| Deployed verifier | [`Primeinvincible/scifact-healthver-verifier`](https://huggingface.co/Primeinvincible/scifact-healthver-verifier) |
| Live demo | [Verified Research RAG](https://huggingface.co/spaces/Primeinvincible/verified-research-rag) |
| Adaptation pipeline | `verifier_study/1_scifact_healthver/` |
| Distillation pipeline | `verifier_study/2_arxiv_distillation/` |
| Gold set + evaluation | `verifier_study/3_gold_and_eval/` |
| Teacher audit | `verifier_study/4_teacher_audit/` |
