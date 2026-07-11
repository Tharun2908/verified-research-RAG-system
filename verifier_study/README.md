# Verifier Study

The research behind the deployed verifier. **Read [`docs/verifier.md`](../docs/verifier.md) first** — it is the writeup; these are the scripts that produced it.

Headline: the SciFact/HealthVer adaptation **fixed** the verifier's recall failure on scientific text. A subsequent three-week in-domain arXiv distillation study **did not** improve it, and the negative result is reported rather than buried.

These are research scripts, run against a cluster (`/workspace/project3`) and a local corpus. They are recorded for provenance and reproducibility, not packaged as a library.

---

## 1. `1_scifact_healthver/` — the adaptation that worked

Continue fine-tuning the thesis S4 (RAGTruth DeBERTa) on scientific claim-verification data, to fix a measured 19.4% removal recall on arXiv text.

| Script | Does |
|---|---|
| `prepare_scifact_healthver.py` | Load SciFact + HealthVer, map to binary, **audit native splits for leakage** |
| `prepare_scifact_healthver_group_split.py` | Rebuild as a **connected-components grouped split** (no claim_id or abstract_id crosses splits) |
| `finetune_s4_scifact_healthver.py` | Continued fine-tune from the thesis S4 checkpoint |
| `run_oof_fusion_scifact.py` | Question-grouped **out-of-fold** fusion stacking |
| `fit_eval_s2_s4_fusion.py` | Fit/evaluate the S2+S4 logistic fusion head |

**Outcome:** deployed. Recall 0.84 on the grouped test split; the obvious-hallucination failure case goes from `P(unsupported)=0.03` to `0.96`. Traded calibration (ECE 0.058 → 0.19) for recall — deliberately.

---

## 2. `2_arxiv_distillation/` — the in-domain attempt

Distil a teacher's judgments on the actual deployment corpus (arXiv CS/ML), to close the biomedical→CS domain gap.

**v1 — abandoned (96% contaminated).** Split questions by top-1 retrieved paper. Insufficient: claims attach evidence from *many* papers after generation.

| Script | Does |
|---|---|
| `generate_fresh_questions.py` | Generate 300 questions (grounded + bait) over the corpus |
| `validate_fresh_questions.py` | Retrieval-validate; drop unanswerable grounded / answerable bait |
| `build_distill_split.py` | Question-wise train/gold split (top-1 paper grouping) |
| `build_distill_eval_inputs.py` · `build_distill_claims.py` | Generate answers, extract claims |
| `label_distill_claims.py` | Teacher labels the training pool |
| **`check_distill_evidence_overlap.py`** | **The audit that killed v1** — strict evidence-overlap check → 341/355 gold claims contaminated |
| `filter_train_against_gold_evidence.py` | Attempted salvage (left 366 rows / 21 positives — too small) |

**v2 — leakage-safe rebuild (protected-paper split).**

| Script | Does |
|---|---|
| `build_arxiv_v2_safe_papers.py` | Protect all 99 gold-evidence papers; 151 safe training papers |
| `generate_arxiv_v2_train_questions.py` · `generate_arxiv_v2_bait_questions.py` | Regenerate over the safe pool only |
| `validate_arxiv_v2_train_questions.py` | Retrieve top-10 → **drop protected papers** → keep top-3 safe |
| `build_arxiv_v2_clean_train_inputs.py` · `build_arxiv_v2_bait_inputs.py` | Build generation inputs |
| `merge_arxiv_v2_train_answers.py` · `build_arxiv_v2_train_claims.py` | Mistral generation + claim extraction (2227 claims) |
| **`check_arxiv_v2_train_protected_overlap.py`** | **The decisive check** — 11,794 evidence attachments, **0 protected overlap** |
| `label_arxiv_v2_train_claims_non_opus.py` | Llama-3.3-70B teacher labels (Opus reserved as independent auditor) |
| `build_arxiv_v2_binary_splits.py` | Question-grouped binary train/val (0 qid overlap) |
| `finetune_s4_arxiv_binary.py` | Fine-tune S4 from two initial checkpoints |

**Outcome:** not deployed. No reliable improvement over the unadapted verifier.

---

## 3. `3_gold_and_eval/` — human gold + the evaluation that mattered

**Gold set construction** (model-drafted, human-confirmed — the human label is the gold label):

| Script | Does |
|---|---|
| `build_gold_candidates.py` | Enriched selection (bait + disagreements + judge-flagged), emits a **blind** file |
| `draft_gold_labels.py` | Independent model drafts labels **blind** (three-way: supported / unsupported / abstention) |
| `review_gold_labels.py` | **Anti-anchoring human review** — you judge *first*, the draft is revealed *after* |
| `draft_arxiv_gold_claims_opus.py` · `build_arxiv_gold_full_assisted_review.py` · `import_arxiv_gold_full_review.py` | Assisted-review workflow |
| `gold_blind50_markdown_workflow*.py` · `build_arxiv_gold_blind50_review.py` | Blind 50-claim human audit of draft quality |

**Grounded-hard stress test** — because the first gold set was measuring the wrong thing (71 of 75 unsupported claims were *bait*, only 4 were subtle grounded overclaims):

| Script | Does |
|---|---|
| `build_grounded_hard_tranche_inputs.py` | Generate under **weakened/censored evidence** (weak home chunk, distractors, remove-strongest) |
| `build_grounded_hard_claims.py` | Mistral generation + claim extraction (1245 claims) |
| `build_grounded_hard_random_review.py` | Stratified random sampling for human review |
| `draft_grounded_hard_opus.py` | (Opus screening — abandoned on cost; replaced by model-independent random sampling) |

Anti-circularity rule enforced: **no evaluated verifier generated, sampled, or labelled its own evaluation set.**

**Evaluation:**

| Script | Does |
|---|---|
| `eval_s4_binary_no_train.py` | Evaluate S4 variants on gold |
| `eval_signal2_relevance_arxiv.py` | Relevance signal (S2) standalone |
| `eval_grounded_hard_all_models.py` | All models on the human-reviewed grounded-hard tranche |
| **`bootstrap_grounded_hard_clustered.py`** | **Paired question-clustered bootstrap CIs** — this is what turned an apparent fusion win into a measured regression |

**Outcome:** the unadapted SciFact/HealthVer verifier ranked first (weighted F1 0.403, AUROC 0.788). OOF fusion was **reliably worse**: −0.074 weighted F1, 95% CI [−0.131, −0.018].

---

## 4. `4_teacher_audit/` — the contamination finding

If you distil a teacher, your student inherits the teacher's errors. So the teacher was audited.

| Script | Does |
|---|---|
| `sample_unsupported_477_audit.py` | Audit **all 477** claims the Llama teacher labelled unsupported, using Opus as an independent judge |
| `build_unsupported_477_human_review.py` | Build a **blind** 100-row human validation of the proposed corrections |
| `build_blind50_teacher_audit.py` · `audit_arxiv_gold_blind50.py` | Blind draft-quality audits |
| `unsupported_477_sample100_human_review.md` | The human review artifact |
| `unsupported_477_disagreement_human_review.md` | Disagreement adjudication |

**Outcome:**

```
Of 477 teacher "unsupported" labels, Opus relabelled:
  218 → SUPPORTED     (46% false-positive contamination)
  181 → UNSUPPORTED
   78 → ABSTENTION

Blind human audit of the supported-corrections: 94.3% agreement  → confirmed
Abstention corrections: 30.0% exact / 73.3% action agreement     → BELOW the
                                                                    pre-registered
                                                                    threshold
```

The pre-registered rule was **allowed to fail**. No auto-cleaned retrain was run.

---

## Reproducing

These scripts assume:
- a cluster workspace at `/workspace/project3` (fine-tuning, batch scoring)
- the 250-paper arXiv corpus at `backend/data/arxiv_papers.json`
- `OPENROUTER_API_KEY` in `.env` for teacher/auditor calls

Most are resumable (they write incrementally and skip completed work on re-run) — a habit learned the hard way when a quota wall killed a long unsaved labelling run.
