@echo off
REM ============================================================================
REM  reorganize_verifier_study.bat
REM  Moves the verifier research scripts out of app/services (production code)
REM  into a numbered verifier_study/ tree that tells the story in order.
REM  Run from the repo root: C:\Users\mekal\verified-research-agent
REM ============================================================================

echo Creating verifier_study structure...
mkdir verifier_study 2>nul
mkdir verifier_study\1_scifact_healthver 2>nul
mkdir verifier_study\2_arxiv_distillation 2>nul
mkdir verifier_study\3_gold_and_eval 2>nul
mkdir verifier_study\4_teacher_audit 2>nul
mkdir demo 2>nul

echo.
echo === 1. SciFact/HealthVer adaptation (the one that worked) ===
move backend\prepare_scifact_healthver.py            verifier_study\1_scifact_healthver\ 2>nul
move backend\prepare_scifact_healthver_group_split.py verifier_study\1_scifact_healthver\ 2>nul
move backend\finetune_s4_scifact_healthver.py        verifier_study\1_scifact_healthver\ 2>nul
move backend\run_oof_fusion_scifact.py               verifier_study\1_scifact_healthver\ 2>nul
move backend\fit_eval_s2_s4_fusion.py                verifier_study\1_scifact_healthver\ 2>nul

echo.
echo === 2. arXiv distillation (v1 + leakage-safe v2 rebuild) ===
REM -- v1 pipeline (the one that turned out contaminated)
move backend\app\services\generate_fresh_questions.py       verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\validate_fresh_questions.py       verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_distill_split.py            verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_distill_eval_inputs.py      verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_distill_claims.py           verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\label_distill_claims.py           verifier_study\2_arxiv_distillation\ 2>nul
REM -- the leakage audit that killed v1
move backend\app\services\check_distill_evidence_overlap.py verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\filter_train_against_gold_evidence.py verifier_study\2_arxiv_distillation\ 2>nul
REM -- v2 rebuild (protected-paper split)
move backend\app\services\build_arxiv_v2_safe_papers.py     verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\generate_arxiv_v2_train_questions.py verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\generate_arxiv_v2_bait_questions.py  verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\validate_arxiv_v2_train_questions.py verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_arxiv_v2_clean_train_inputs.py verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_arxiv_v2_bait_inputs.py     verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\merge_arxiv_v2_train_answers.py   verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_arxiv_v2_train_claims.py    verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\check_arxiv_v2_train_protected_overlap.py verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\label_arxiv_v2_train_claims_non_opus.py   verifier_study\2_arxiv_distillation\ 2>nul
move backend\app\services\build_arxiv_v2_binary_splits.py   verifier_study\2_arxiv_distillation\ 2>nul
REM -- the fine-tune itself
move backend\finetune_s4_arxiv_binary.py                    verifier_study\2_arxiv_distillation\ 2>nul

echo.
echo === 3. Gold set + evaluation ===
move backend\app\services\build_gold_candidates.py          verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\draft_gold_labels.py              verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\review_gold_labels.py             verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\draft_arxiv_gold_claims_opus.py   verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\build_arxiv_gold_full_assisted_review.py verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\import_arxiv_gold_full_review.py  verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\gold_blind50_markdown_workflow.py verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\gold_blind50_markdown_workflow_v2.py verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\build_arxiv_gold_blind50_review.py verifier_study\3_gold_and_eval\ 2>nul
move backend\app\services\build_gold_blind50_disagreement_review.py verifier_study\3_gold_and_eval\ 2>nul
REM -- grounded-hard stress test
move backend\build_grounded_hard_tranche_inputs.py          verifier_study\3_gold_and_eval\ 2>nul
move backend\build_grounded_hard_claims.py                  verifier_study\3_gold_and_eval\ 2>nul
move backend\build_grounded_hard_random_review.py           verifier_study\3_gold_and_eval\ 2>nul
move backend\draft_grounded_hard_opus.py                    verifier_study\3_gold_and_eval\ 2>nul
move backend\inspect_grounded_hard_resources.py             verifier_study\3_gold_and_eval\ 2>nul
move backend\grounded_hard_random_review.md                 verifier_study\3_gold_and_eval\ 2>nul
REM -- model evaluation
move backend\eval_s4_binary_no_train.py                     verifier_study\3_gold_and_eval\ 2>nul
move backend\eval_signal2_relevance_arxiv.py                verifier_study\3_gold_and_eval\ 2>nul
move backend\eval_grounded_hard_all_models.py               verifier_study\3_gold_and_eval\ 2>nul
move backend\bootstrap_grounded_hard_clustered.py           verifier_study\3_gold_and_eval\ 2>nul

echo.
echo === 4. Teacher-label audit (the contamination finding) ===
move backend\sample_unsupported_477_audit.py                verifier_study\4_teacher_audit\ 2>nul
move backend\build_unsupported_477_human_review.py          verifier_study\4_teacher_audit\ 2>nul
move backend\app\services\build_blind50_teacher_audit.py    verifier_study\4_teacher_audit\ 2>nul
move backend\app\services\audit_arxiv_gold_blind50.py       verifier_study\4_teacher_audit\ 2>nul
move backend\unsupported_477_sample100_human_review.md      verifier_study\4_teacher_audit\ 2>nul
move backend\unsupported_477_disagreement_human_review.md   verifier_study\4_teacher_audit\ 2>nul

echo.
echo === Cleanup: duplicate file ===
del "backend\build_unsupported_477_human_review (1).py" 2>nul

echo.
echo === Done. Review with: git status ===
echo.
echo NOTE: verifier_real.py and verifier.py STAY in backend/app/services/
echo       (they are production code, not research scripts).
