# `backend/data/` — committed result artifacts

This folder holds the evaluation and benchmark artifacts for the Verified Research RAG System.
Most of the folder is gitignored (bulk corpus + large regenerable intermediates); the files
committed here are the **small specs and final results** that let you verify the reported numbers
without re-running the full pipeline.

## Committed files

| File | What it is | Produced by |
| --- | --- | --- |
| `eval_questions.json` | The 43-question evaluation spec (36 grounded + 7 out-of-distribution "bait"), each validated against retrieval. | hand-built + validated (M8 step 1) |
| `scores.json` | Per-claim verifier output for all 409 extracted claims: S2/S4 sub-scores, fused hallucination probability, support score, and label (Supported/Weak/Unsupported). | `cluster/verify_batch.py` (real S2+S4 fusion) |
| `judge_results.json` | Independent LLM-as-judge verdict (SUPPORTED/UNSUPPORTED) for each claim, with the verifier's own label alongside, for agreement analysis. | `app/services/gemini_judge.py` (Llama-3.3-70B via OpenRouter, 2026-06-21) |
| `eval_report.json` | Three-arm comparison results (Basic RAG / RAG+citations / Verified) and the grounded-vs-bait unsupported-rate breakdown. | `app/services/analyze_eval.py` |
| `verifier_quality.json` | Verifier graded against the independent judge: removal precision, recall, F1, supported-claim loss, retained-unsupported-rate. Replaces the circular "~0% after filtering" metric. | `app/services/analyze_verifier_quality.py` |
| `bench_bf16_prefix_unique.json` | M9 serving benchmark — bf16 + prefix caching, unique-prompt RAG workload. | `cluster/bench_vllm.py` |
| `bench_fp8_prefix_unique.json` | M9 serving benchmark — fp8 + prefix caching. | `cluster/bench_vllm.py` |
| `bench_fp8_noprefix_unique.json` | M9 serving benchmark — fp8, prefix caching disabled (for the prefix-caching ablation). | `cluster/bench_vllm.py` |

## How to reproduce the headline numbers from these files

- **Three-arm eval + grounded-vs-bait split:** `python -m app.services.analyze_eval` (reads `scores.json` + `eval_questions.json` → `eval_report.json`).
- **Verifier quality vs judge:** `python -m app.services.analyze_verifier_quality` (reads `judge_results.json` → `verifier_quality.json`).
- **Serving benchmark tables:** see `docs/serving.md`; raw per-level numbers are in the three `bench_*_unique.json` files.

## NOT committed (gitignored — regenerable bulk data)

- `arxiv_papers.json` — the 250-paper corpus (re-fetch from arXiv).
- `eval_inputs.json`, `answers.json`, `claims_to_verify.json` — large intermediate pipeline files, regenerable from the questions + corpus + the `build_*` / `generate_batch` scripts.

A full corpus manifest (arXiv IDs + checksums) and end-to-end reproduction commands are planned for the M12 documentation pass.
