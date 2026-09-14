#!/usr/bin/env python3
"""
H200 verifier efficiency benchmark.

Purpose
-------
Measure the steady-state inference cost of the three verifier policies already
evaluated for quality on the expanded grounded-hard benchmark:

1) DeBERTa-only
2) Confirmation cascade:
      DeBERTa on every claim
      MiniCheck only where DeBERTa predicts UNSUPPORTED
3) MiniCheck-7B-only

The benchmark uses exactly the same 339 binary claim/evidence pairs as
eval_grounded_hard_500.py. ABSTENTION and INVALID_EXTRACTION rows are excluded.

Important measurement choices
-----------------------------
- Model download/load time is reported separately and EXCLUDED from inference time.
- Each model receives a warmup call before timed inference.
- Prefix caching is disabled for MiniCheck, matching the quality evaluation.
- GPU memory is sampled from nvidia-smi during each timed section. This pod is
  expected to have one otherwise-idle H200.
- The cascade timing is computed as:
      DeBERTa full-set inference + MiniCheck routed-subset inference
  This is a sequential steady-state compute benchmark, not a production
  concurrency/load-test result.
- Cost assumes one H200 at the supplied hourly rate. It does not include
  retrieval, generation, storage, networking, or idle/autoscaling overhead.

Run from repository root on the H200 cluster:
    export VLLM_USE_FLASHINFER_SAMPLER=0
    export CC=/usr/bin/gcc
    export CXX=/usr/bin/g++
    CUDA_VISIBLE_DEVICES=0 python \
      verifier_study/3_gold_and_eval/benchmark_verifier_efficiency_h200.py

The environment overrides above were required by the MiniCheck/vLLM stack on the measured
cluster image and are recorded here for exact reruns.

Output:
    backend/data/grounded_hard_eval/verifier_efficiency_h200.json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import threading
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from minicheck.minicheck import MiniCheck


DATA = Path("backend/data/grounded_hard_eval")
INPUT = DATA / "grounded_hard_random_review_500_labeled.jsonl"
OUT = DATA / "verifier_efficiency_h200.json"

HF_MODEL_ID = "Primeinvincible/scifact-healthver-verifier"
HF_REVISION = "902d07844e30e59d311f5cc500b9ec13d08d0002"
BASE_THRESHOLD = 0.06
MAX_LENGTH = 512

EXPECTED_REVIEWED = 500
EXPECTED_BINARY = 339
EXPECTED_UNSUPPORTED = 51

DEFAULT_GPU_HOURLY_USD = 4.0
# M8 cited arm: 193 claims across 43 answers.
DEFAULT_CLAIMS_PER_ANSWER = 193.0 / 43.0


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def as_binary(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip().upper()
    if s in {"UNSUPPORTED", "1", "TRUE"}:
        return 1
    if s in {"SUPPORTED", "0", "FALSE"}:
        return 0
    return None


def weighted_metrics(y: np.ndarray, pred: np.ndarray, w: np.ndarray) -> dict[str, float]:
    tp = float(w[(pred == 1) & (y == 1)].sum())
    fp = float(w[(pred == 1) & (y == 0)].sum())
    fn = float(w[(pred == 0) & (y == 1)].sum())
    tn = float(w[(pred == 0) & (y == 0)].sum())
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2.0 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "weighted_tp": tp,
        "weighted_fp": fp,
        "weighted_fn": fn,
        "weighted_tn": tn,
    }


def gpu_used_mib() -> float | None:
    """Total GPU memory used on GPU 0 according to nvidia-smi."""
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=memory.used",
                "--format=csv,noheader,nounits",
                "-i",
                "0",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return float(out.splitlines()[0])
    except Exception:
        return None


class GPUMemorySampler:
    def __init__(self, interval_s: float = 0.10):
        self.interval_s = interval_s
        self.samples: list[float] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def _run(self) -> None:
        while not self._stop.is_set():
            v = gpu_used_mib()
            if v is not None:
                self.samples.append(v)
            self._stop.wait(self.interval_s)

    def __enter__(self):
        v = gpu_used_mib()
        if v is not None:
            self.samples.append(v)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        v = gpu_used_mib()
        if v is not None:
            self.samples.append(v)

    @property
    def peak_mib(self) -> float | None:
        return max(self.samples) if self.samples else None

    @property
    def min_mib(self) -> float | None:
        return min(self.samples) if self.samples else None


def timed_section(fn: Callable[[], Any]) -> tuple[Any, dict[str, float | None]]:
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    with GPUMemorySampler() as mem:
        t0 = time.perf_counter()
        result = fn()
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        elapsed = time.perf_counter() - t0
    return result, {
        "seconds": elapsed,
        "gpu_memory_min_mib": mem.min_mib,
        "gpu_memory_peak_mib": mem.peak_mib,
    }


def prepare_rows(path: Path):
    source = load_jsonl(path)
    rows = []
    excluded = defaultdict(int)

    for r in source:
        label_raw = r.get("human_final_label") or r.get("final_label") or r.get("label")
        y = as_binary(label_raw)
        if y is None:
            excluded[str(label_raw or "MISSING").upper()] += 1
            continue

        claim = str(r.get("claim") or "").strip()
        evidence = str(r.get("evidence_text_for_verifier") or "").strip()
        if not claim or not evidence:
            raise SystemExit(f"Binary row {r.get('claim_id')} missing claim/evidence.")

        rows.append(
            {
                "claim_id": str(r["claim_id"]),
                "qid": str(r["qid"]),
                "claim": claim,
                "evidence": evidence,
                "y": y,
                "weight": float(r.get("sampling_weight", 1.0)),
            }
        )

    n_unsup = sum(r["y"] for r in rows)
    if (
        len(source) != EXPECTED_REVIEWED
        or len(rows) != EXPECTED_BINARY
        or n_unsup != EXPECTED_UNSUPPORTED
    ):
        raise SystemExit(
            "Benchmark guardrail failed: expected "
            f"{EXPECTED_REVIEWED} reviewed / {EXPECTED_BINARY} binary / "
            f"{EXPECTED_UNSUPPORTED} unsupported, observed "
            f"{len(source)} / {len(rows)} / {n_unsup}."
        )

    return source, rows, dict(excluded)


def load_deberta(local_path: str | None):
    if local_path:
        source = local_path
        kwargs = {}
    else:
        source = HF_MODEL_ID
        kwargs = {"revision": HF_REVISION}

    t0 = time.perf_counter()
    tok = AutoTokenizer.from_pretrained(source, **kwargs)
    model = AutoModelForSequenceClassification.from_pretrained(source, **kwargs)
    model.to("cuda")
    model.eval()
    torch.cuda.synchronize()
    load_s = time.perf_counter() - t0
    return tok, model, source, load_s


def score_deberta_loaded(
    tok,
    model,
    claims: list[str],
    evidence: list[str],
    batch_size: int,
) -> np.ndarray:
    scores: list[float] = []
    with torch.inference_mode():
        for start in range(0, len(claims), batch_size):
            end = min(start + batch_size, len(claims))
            enc = tok(
                claims[start:end],
                evidence[start:end],
                max_length=MAX_LENGTH,
                truncation=True,
                padding=True,
                return_tensors="pt",
            )
            enc = {k: v.to("cuda") for k, v in enc.items()}
            logits = model(**enc).logits
            probs = torch.softmax(logits, dim=1)[:, 1]
            scores.extend(probs.detach().cpu().numpy().astype(float).tolist())
    return np.asarray(scores, dtype=float)


def load_minicheck(cache_dir: str):
    t0 = time.perf_counter()
    scorer = MiniCheck(
        model_name="Bespoke-MiniCheck-7B",
        enable_prefix_caching=False,
        cache_dir=cache_dir,
    )
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    load_s = time.perf_counter() - t0
    return scorer, load_s


def score_minicheck_loaded(
    scorer,
    claims: list[str],
    evidence: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    pred_supported, support_prob, _, _ = scorer.score(docs=evidence, claims=claims)
    pred_supported = np.asarray(pred_supported, dtype=int)
    support_prob = np.asarray(support_prob, dtype=float)
    if len(pred_supported) != len(claims):
        raise RuntimeError("MiniCheck returned unexpected prediction count.")
    return 1 - pred_supported, 1.0 - support_prob


def throughput_block(
    n_claims: int,
    seconds: float,
    gpu_hourly_usd: float,
    claims_per_answer: float,
) -> dict[str, float]:
    claims_per_second = n_claims / seconds
    gpu_hours_per_1000_claims = (1000.0 / claims_per_second) / 3600.0
    cost_per_1000_claims = gpu_hours_per_1000_claims * gpu_hourly_usd
    answers_per_second = claims_per_second / claims_per_answer
    cost_per_1000_answers = (
        (1000.0 / answers_per_second) / 3600.0 * gpu_hourly_usd
    )
    return {
        "effective_claims_per_second": claims_per_second,
        "effective_answers_per_second_at_claims_per_answer": answers_per_second,
        "gpu_hours_per_1000_claims": gpu_hours_per_1000_claims,
        "usd_per_1000_claims": cost_per_1000_claims,
        "usd_per_1000_answers": cost_per_1000_answers,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=INPUT)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--deberta-batch-size", type=int, default=16)
    ap.add_argument("--minicheck-cache-dir", default="./ckpts")
    ap.add_argument("--deberta-local-path", default=os.getenv("VERIFIER_MODEL_PATH"))
    ap.add_argument("--gpu-hourly-usd", type=float, default=DEFAULT_GPU_HOURLY_USD)
    ap.add_argument("--claims-per-answer", type=float, default=DEFAULT_CLAIMS_PER_ANSWER)
    ap.add_argument("--warmup-claims", type=int, default=8)
    args = ap.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is required for this H200 benchmark.")

    props = torch.cuda.get_device_properties(0)
    source, rows, excluded = prepare_rows(args.input)
    claims = [r["claim"] for r in rows]
    evidence = [r["evidence"] for r in rows]
    y = np.asarray([r["y"] for r in rows], dtype=int)
    w = np.asarray([r["weight"] for r in rows], dtype=float)
    n = len(rows)

    print("\nH200 verifier efficiency benchmark")
    print("=" * 80)
    print(f"GPU:                 {torch.cuda.get_device_name(0)}")
    print(f"GPU memory:          {props.total_memory / 1024**3:.1f} GiB")
    print(f"Reviewed rows:       {len(source)}")
    print(f"Binary claims:       {n}")
    print(f"Excluded labels:     {excluded}")
    print(f"GPU hourly rate:     ${args.gpu_hourly_usd:.2f}")
    print(f"Claims/answer:       {args.claims_per_answer:.3f}")
    print()

    # ---------------------------------------------------------------- DeBERTa
    print("[1/3] Loading DeBERTa (load time excluded from inference benchmark)...")
    d_tok, d_model, d_source, d_load_s = load_deberta(args.deberta_local_path)
    print(f"      loaded in {d_load_s:.2f}s")

    warm_n = min(args.warmup_claims, n)
    _ = score_deberta_loaded(
        d_tok, d_model, claims[:warm_n], evidence[:warm_n], args.deberta_batch_size
    )
    torch.cuda.synchronize()

    print(f"      timing {n} claims...")
    d_score, d_timing = timed_section(
        lambda: score_deberta_loaded(
            d_tok, d_model, claims, evidence, args.deberta_batch_size
        )
    )
    d_pred = (d_score >= BASE_THRESHOLD).astype(int)
    routed_idx = np.where(d_pred == 1)[0]
    print(
        f"      {d_timing['seconds']:.3f}s, "
        f"{n / d_timing['seconds']:.1f} claims/s, "
        f"routes {len(routed_idx)}/{n} ({100*len(routed_idx)/n:.1f}%)"
    )

    # Free DeBERTa before loading MiniCheck so each measured footprint is clear.
    del d_model
    del d_tok
    torch.cuda.empty_cache()
    time.sleep(1.0)

    # --------------------------------------------------------------- MiniCheck
    print("\n[2/3] Loading MiniCheck-7B (load time excluded from inference benchmark)...")
    mc, mc_load_s = load_minicheck(args.minicheck_cache_dir)
    print(f"      loaded in {mc_load_s:.2f}s")

    _ = score_minicheck_loaded(
        mc, claims[:warm_n], evidence[:warm_n]
    )
    if torch.cuda.is_available():
        torch.cuda.synchronize()

    print(f"      timing MiniCheck-only on {n} claims...")
    (mc_pred, mc_score), mc_full_timing = timed_section(
        lambda: score_minicheck_loaded(mc, claims, evidence)
    )
    print(
        f"      {mc_full_timing['seconds']:.3f}s, "
        f"{n / mc_full_timing['seconds']:.1f} claims/s"
    )

    routed_claims = [claims[i] for i in routed_idx]
    routed_evidence = [evidence[i] for i in routed_idx]
    print(f"\n[3/3] Timing MiniCheck on cascade subset ({len(routed_idx)} claims)...")
    (mc_route_pred, mc_route_score), mc_route_timing = timed_section(
        lambda: score_minicheck_loaded(mc, routed_claims, routed_evidence)
    )
    print(
        f"      {mc_route_timing['seconds']:.3f}s, "
        f"{len(routed_idx) / mc_route_timing['seconds']:.1f} routed claims/s"
    )

    # -------------------------------------------------------------- predictions
    cascade_pred = d_pred.copy()
    cascade_pred[routed_idx] = mc_route_pred

    d_metrics = weighted_metrics(y, d_pred, w)
    d_metrics["auroc"] = float(roc_auc_score(y, d_score, sample_weight=w))

    mc_metrics = weighted_metrics(y, mc_pred, w)
    mc_metrics["auroc"] = float(roc_auc_score(y, mc_score, sample_weight=w))

    cascade_metrics = weighted_metrics(y, cascade_pred, w)

    # --------------------------------------------------------------- efficiency
    d_eff = throughput_block(
        n, d_timing["seconds"], args.gpu_hourly_usd, args.claims_per_answer
    )
    mc_eff = throughput_block(
        n, mc_full_timing["seconds"], args.gpu_hourly_usd, args.claims_per_answer
    )

    cascade_seconds = d_timing["seconds"] + mc_route_timing["seconds"]
    cascade_eff = throughput_block(
        n, cascade_seconds, args.gpu_hourly_usd, args.claims_per_answer
    )

    # Quality guardrails against the committed expanded-evaluation headline values.
    expected = {
        "deberta_f1": 0.4041,
        "minicheck_f1": 0.6664,
        "cascade_f1": 0.6417,
        "routed": 137,
    }
    guardrail = {
        "deberta_f1_close": abs(d_metrics["f1"] - expected["deberta_f1"]) < 0.01,
        "minicheck_f1_close": abs(mc_metrics["f1"] - expected["minicheck_f1"]) < 0.01,
        "cascade_f1_close": abs(cascade_metrics["f1"] - expected["cascade_f1"]) < 0.01,
        "routed_count_matches": len(routed_idx) == expected["routed"],
    }

    result = {
        "benchmark": {
            "name": "H200 verifier efficiency",
            "gpu": torch.cuda.get_device_name(0),
            "gpu_total_memory_gib": props.total_memory / 1024**3,
            "torch_version": torch.__version__,
            "cuda_version": torch.version.cuda,
            "transformers_version": __import__("transformers").__version__,
            "model_load_time_excluded": True,
            "warmup_claims": warm_n,
            "prefix_caching_minicheck": False,
            "gpu_hourly_usd_assumption": args.gpu_hourly_usd,
            "claims_per_answer_assumption": args.claims_per_answer,
            "claims_per_answer_provenance": "M8 cited arm: 193 claims / 43 answers",
            "interpretation": (
                "Sequential steady-state compute benchmark on the expanded grounded-hard "
                "claim/evidence workload; not a production concurrency/load test."
            ),
        },
        "dataset": {
            "reviewed_rows": len(source),
            "binary_claims": n,
            "supported": int(np.sum(y == 0)),
            "unsupported": int(np.sum(y == 1)),
            "excluded_labels": excluded,
        },
        "deberta_only": {
            "model_source": d_source,
            "model_revision": None if args.deberta_local_path else HF_REVISION,
            "load_seconds_excluded": d_load_s,
            "inference": d_timing,
            "quality": d_metrics,
            "efficiency": d_eff,
        },
        "minicheck_only": {
            "model": "Bespoke-MiniCheck-7B",
            "load_seconds_excluded": mc_load_s,
            "inference": mc_full_timing,
            "quality": mc_metrics,
            "efficiency": mc_eff,
        },
        "confirmation_cascade": {
            "routing_rule": (
                "DeBERTa SUPPORTED -> accept; DeBERTa UNSUPPORTED -> MiniCheck"
            ),
            "claims_sent_to_minicheck": int(len(routed_idx)),
            "raw_escalation_fraction": float(len(routed_idx) / n),
            "deberta_full_inference_seconds": d_timing["seconds"],
            "minicheck_routed_inference": mc_route_timing,
            "combined_sequential_inference_seconds": cascade_seconds,
            "quality": cascade_metrics,
            "efficiency": cascade_eff,
            "structural_recall_note": (
                "MiniCheck never sees DeBERTa-supported claims, so it cannot recover "
                "DeBERTa false negatives."
            ),
        },
        "relative": {
            "cascade_vs_deberta_time_multiplier": (
                cascade_seconds / d_timing["seconds"]
            ),
            "minicheck_vs_deberta_time_multiplier": (
                mc_full_timing["seconds"] / d_timing["seconds"]
            ),
            "cascade_cost_fraction_of_minicheck": (
                cascade_eff["usd_per_1000_claims"]
                / mc_eff["usd_per_1000_claims"]
            ),
            "cascade_f1_fraction_of_minicheck": (
                cascade_metrics["f1"] / mc_metrics["f1"]
            ),
        },
        "quality_guardrail": guardrail,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    print(
        f"DeBERTa     F1={d_metrics['f1']:.4f}  "
        f"time={d_timing['seconds']:.3f}s  "
        f"cost/1k claims=${d_eff['usd_per_1000_claims']:.4f}"
    )
    print(
        f"Cascade     F1={cascade_metrics['f1']:.4f}  "
        f"time={cascade_seconds:.3f}s  "
        f"cost/1k claims=${cascade_eff['usd_per_1000_claims']:.4f}  "
        f"MiniCheck={len(routed_idx)}/{n} ({100*len(routed_idx)/n:.1f}%)"
    )
    print(
        f"MiniCheck   F1={mc_metrics['f1']:.4f}  "
        f"time={mc_full_timing['seconds']:.3f}s  "
        f"cost/1k claims=${mc_eff['usd_per_1000_claims']:.4f}"
    )
    print()
    print(
        "Cascade cost as fraction of MiniCheck-only: "
        f"{100*result['relative']['cascade_cost_fraction_of_minicheck']:.1f}%"
    )
    print(
        "Cascade F1 as fraction of MiniCheck-only: "
        f"{100*result['relative']['cascade_f1_fraction_of_minicheck']:.1f}%"
    )
    print(f"Quality guardrail: {guardrail}")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
