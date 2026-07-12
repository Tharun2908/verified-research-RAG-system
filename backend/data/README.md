# Evaluation artifacts

Committed so the reported numbers can be independently recomputed.

## Corpus
- `arxiv_papers.json` — the 250-paper corpus (title, authors, year, abstract). Ingested by
  `app.services.ingest_corpus`. One abstract = one chunk.

## M8 evaluation (43 questions / 409 claims)
- `eval_questions.json` — the questions (`type: grounded | bait`)
- `answers.json` — generated answers (plain + cited arms)
- `claims_to_verify.json` — extracted claims with their evidence
- `scores.json` — verifier scores (S2, S4, fusion, label)
- `judge_results.json` — independent LLM-judge verdicts
- `verifier_quality.json`, `eval_report.json` — computed metrics

## Serving benchmarks (vLLM, H200)
- `bench_bf16_prefix_unique.json`, `bench_fp8_prefix_unique.json`,
  `bench_fp8_noprefix_unique.json` — the corrected unique-prompt runs. (The earlier
  `*_varied` files contain the run whose "+46% prefix caching" turned out to be an artifact
  of accidentally repeated prompts; kept for provenance.)

## Grounded-hard evaluation (`grounded_hard_eval/`)
The headline model comparison in `docs/verifier.md`.
- `grounded_hard_random_review_labeled.jsonl` — **the human labels** (the gold standard)
- `grounded_hard_random_review_sampling_report.json` — how the sample was drawn
- `binary_predictions.jsonl` — per-model predictions on the human-reviewed claims
- `abstention_rows.jsonl` — the abstention subset
- `metrics_summary.json` — the computed comparison table
- `bootstrap_summary.json` — question-clustered bootstrap CIs
- `fusion_ft_scifact_oof_hard_predictions.jsonl` — OOF-fusion per-claim predictions
- `fusion_base_scifact_trainfit_hard_predictions.jsonl` — train-fitted fusion predictions
- `fold_assignments.jsonl` — the question-grouped OOF folds
- `oof_fusion_metrics_summary.json` — fusion metrics

**Reproducibility.** The OOF-fusion predictions (fusion_ft_scifact_oof_hard_predictions.jsonl), the train-fitted fusion predictions, the fold assignments, and the human labels are all committed — so the reported −0.074 weighted-F1 difference (95% CI [−0.131, −0.018]) can be recomputed from the repository root with : 
python verifier_study/3_gold_and_eval/reproduce_bootstrap.

## Distillation (`distill_arxiv/`, `distill_arxiv_v2/`)
Selected reports from the arXiv distillation study (see `docs/verifier.md`):
- `distill_arxiv/evidence_overlap_report.json` — the audit that found 96% contamination
- `distill_arxiv/gold_final_human_reviewed.json` — the human-reviewed gold set
- `distill_arxiv_v2/safe_paper_report.json`, `protected_gold_evidence_papers.json` — the
  protected-paper split
- `distill_arxiv_v2/train_protected_evidence_overlap_report.json` — the 0-overlap verification
- `distill_arxiv_v2/.../metrics_summary.json` — fine-tune metrics

## Not committed
- Model checkpoints → [HuggingFace](https://huggingface.co/Primeinvincible/scifact-healthver-verifier)
- The full 1,245-claim generation pool (11MB) and raw bootstrap replicates (11MB) — the
  human-reviewed subset and the summaries are here instead.