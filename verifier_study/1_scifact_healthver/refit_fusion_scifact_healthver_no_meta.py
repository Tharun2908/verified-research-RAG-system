from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path

import numpy as np
import torch
from tqdm import tqdm

from sentence_transformers import CrossEncoder
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
TRAIN_PATH = "/workspace/project3/data_grouped/verifier_train_grouped.json"
VAL_PATH = "/workspace/project3/data_grouped/verifier_val_grouped.json"
TEST_PATH = "/workspace/project3/data_grouped/verifier_test_grouped.json"

S4_MODEL_DIR = "/workspace/project3/signal4_model_scifact_healthver"
S2_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

OUT_DIR = "/workspace/project3/fusion_scifact_healthver_results"
os.makedirs(OUT_DIR, exist_ok=True)

COEFFS_PATH = "/workspace/project3/fusion_scifact_healthver_coeffs_no_meta.json"

MAX_LENGTH = 512
S2_BATCH_SIZE = 64
S4_BATCH_SIZE = 32
SEED = 42

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------
def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def split_into_sentences(text: str) -> list[str]:
    """
    Simple deployment-matching sentence splitter.

    This mirrors the RealVerifier-side idea:
      - split on sentence-ending punctuation
      - keep non-trivial sentences only

    For single-claim inputs, this usually returns one claim sentence.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip()) >= 10]


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def compute_ece(probs, labels, n_bins: int = 10) -> float:
    probs = np.asarray(probs, dtype=float)
    labels = np.asarray(labels, dtype=float)

    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        if i == n_bins - 1:
            mask = (probs >= bins[i]) & (probs <= bins[i + 1])
        else:
            mask = (probs >= bins[i]) & (probs < bins[i + 1])

        if mask.sum() == 0:
            continue

        bin_acc = labels[mask].mean()
        bin_conf = probs[mask].mean()
        ece += (mask.sum() / len(probs)) * abs(bin_acc - bin_conf)

    return round(float(ece), 4)


def best_threshold_by_f1(probs, labels):
    best_t = 0.5
    best_f1 = -1.0

    for t in np.arange(0.05, 0.96, 0.01):
        preds = (probs >= t).astype(int)
        f1 = f1_score(labels, preds, zero_division=0)

        if f1 > best_f1:
            best_f1 = f1
            best_t = float(t)

    return round(best_t, 2), float(best_f1)


def metrics_at_threshold(probs, labels, threshold: float):
    preds = (probs >= threshold).astype(int)

    return {
        "threshold": float(threshold),
        "f1": float(f1_score(labels, preds, zero_division=0)),
        "precision": float(precision_score(labels, preds, zero_division=0)),
        "recall": float(recall_score(labels, preds, zero_division=0)),
        "auroc": float(roc_auc_score(labels, probs)),
        "auprc": float(average_precision_score(labels, probs)),
        "ece": float(compute_ece(probs, labels)),
        "confusion_matrix": confusion_matrix(labels, preds).tolist(),
    }


# ---------------------------------------------------------------------
# S2 scoring
# ---------------------------------------------------------------------
def score_s2_raw_min_relevance(records, s2_model: CrossEncoder, split_name: str) -> list[float]:
    """
    Thesis-style S2 raw_min_relevance, matched to live verifier:

    For each claim sentence:
      - score (claim_sentence, evidence_sentence) against all evidence sentences
      - keep the best evidence score
    Then:
      - return the minimum best score across claim sentences

    This returns higher = more relevant / more supported.
    """
    raw_scores = []

    for ex in tqdm(records, desc=f"S2 {split_name}"):
        claim = ex["answer"]
        evidence = ex["context"]

        claim_sentences = split_into_sentences(claim)
        evidence_sentences = split_into_sentences(evidence)

        if not claim_sentences or not evidence_sentences:
            raw_scores.append(0.0)
            continue

        best_scores = []

        for claim_sent in claim_sentences:
            pairs = [(claim_sent, evidence_sent) for evidence_sent in evidence_sentences]
            scores = s2_model.predict(
                pairs,
                batch_size=S2_BATCH_SIZE,
                show_progress_bar=False,
            )
            best_scores.append(float(np.max(scores)))

        raw_scores.append(float(np.min(best_scores)))

    return raw_scores


# ---------------------------------------------------------------------
# S4 scoring
# ---------------------------------------------------------------------
@torch.no_grad()
def score_s4(records, tokenizer, model, split_name: str) -> list[float]:
    """
    New fine-tuned S4 score.

    Input order matches thesis S4:
      tokenizer(answer, context)

    Here:
      answer = claim
      context = abstract/evidence

    Returns:
      P(unsupported) = softmax(logits)[1]
    """
    model.eval()
    probs = []

    for start in tqdm(range(0, len(records), S4_BATCH_SIZE), desc=f"S4 {split_name}"):
        batch = records[start:start + S4_BATCH_SIZE]

        answers = [ex["answer"] for ex in batch]
        contexts = [ex["context"] for ex in batch]

        enc = tokenizer(
            answers,
            contexts,
            max_length=MAX_LENGTH,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        input_ids = enc["input_ids"].to(DEVICE)
        attention_mask = enc["attention_mask"].to(DEVICE)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        batch_probs = torch.softmax(outputs.logits, dim=1)[:, 1].detach().cpu().numpy()

        probs.extend(batch_probs.tolist())

    return [float(p) for p in probs]


# ---------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------
def build_features(records, s2_raw, s4_probs, s2_min: float, s2_max: float):
    X = []
    y = []

    denom = s2_max - s2_min
    if denom <= 0:
        raise ValueError(f"Bad S2 range: min={s2_min}, max={s2_max}")

    for ex, raw_s2, s4 in zip(records, s2_raw, s4_probs):
        norm_s2 = clamp01((raw_s2 - s2_min) / denom)
        X.append([norm_s2, float(s4)])
        y.append(int(ex["label"]))

    return np.asarray(X, dtype=float), np.asarray(y, dtype=int)


def save_feature_dump(path, records, s2_raw, s4_probs, s2_min, s2_max):
    rows = []
    denom = s2_max - s2_min

    for ex, raw_s2, s4 in zip(records, s2_raw, s4_probs):
        norm_s2 = clamp01((raw_s2 - s2_min) / denom)

        rows.append({
            "id": ex["id"],
            "source": ex["source"],
            "orig_split": ex["orig_split"],
            "claim_id": ex["claim_id"],
            "abstract_id": ex["abstract_id"],
            "verdict": ex["verdict"],
            "label": int(ex["label"]),
            "raw_s2_min_relevance": round(float(raw_s2), 6),
            "norm_s2_min_relevance": round(float(norm_s2), 6),
            "new_s4_score": round(float(s4), 6),
            "answer": ex["answer"],
            "context_preview": ex["context"][:300],
        })

    save_json(path, rows)


def load_or_compute_features(split_name, records, s2_model, tokenizer, s4_model):
    """
    Cache raw S2 + new S4 scores because S2 can take time.
    """
    cache_path = os.path.join(OUT_DIR, f"{split_name}_raw_features.json")

    if os.path.exists(cache_path):
        print(f"Loading cached raw features: {cache_path}")
        rows = load_json(cache_path)
        s2_raw = [float(r["raw_s2_min_relevance"]) for r in rows]
        s4_probs = [float(r["new_s4_score"]) for r in rows]
        return s2_raw, s4_probs

    print(f"\nComputing raw features for {split_name}...")
    s2_raw = score_s2_raw_min_relevance(records, s2_model, split_name)
    s4_probs = score_s4(records, tokenizer, s4_model, split_name)

    rows = []
    for ex, raw_s2, s4 in zip(records, s2_raw, s4_probs):
        rows.append({
            "id": ex["id"],
            "label": int(ex["label"]),
            "source": ex["source"],
            "verdict": ex["verdict"],
            "raw_s2_min_relevance": float(raw_s2),
            "new_s4_score": float(s4),
        })

    save_json(cache_path, rows)
    print(f"Saved raw feature cache: {cache_path}")

    return s2_raw, s4_probs


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    np.random.seed(SEED)

    print("Device:", DEVICE)
    print("S2 model:", S2_MODEL_NAME)
    print("S4 model:", S4_MODEL_DIR)
    print("Output dir:", OUT_DIR)

    train_records = load_json(TRAIN_PATH)
    val_records = load_json(VAL_PATH)
    test_records = load_json(TEST_PATH)

    print(f"\nLoaded records:")
    print(f"  train={len(train_records)}")
    print(f"  val={len(val_records)}")
    print(f"  test={len(test_records)}")

    print("\nLoading S2 CrossEncoder...")
    s2_model = CrossEncoder(S2_MODEL_NAME, max_length=MAX_LENGTH, device=DEVICE)

    print("Loading new fine-tuned S4...")
    tokenizer = AutoTokenizer.from_pretrained(S4_MODEL_DIR)
    s4_model = AutoModelForSequenceClassification.from_pretrained(S4_MODEL_DIR)
    s4_model.to(DEVICE)
    s4_model.eval()

    # Raw feature computation
    train_s2_raw, train_s4 = load_or_compute_features(
        "train", train_records, s2_model, tokenizer, s4_model
    )
    val_s2_raw, val_s4 = load_or_compute_features(
        "val", val_records, s2_model, tokenizer, s4_model
    )
    test_s2_raw, test_s4 = load_or_compute_features(
        "test", test_records, s2_model, tokenizer, s4_model
    )

    # Normalize S2 using TRAIN distribution only.
    s2_min = float(np.min(train_s2_raw))
    s2_max = float(np.max(train_s2_raw))

    print("\nS2 normalization from TRAIN only:")
    print(f"  s2_min={s2_min:.6f}")
    print(f"  s2_max={s2_max:.6f}")

    X_train, y_train = build_features(train_records, train_s2_raw, train_s4, s2_min, s2_max)
    X_val, y_val = build_features(val_records, val_s2_raw, val_s4, s2_min, s2_max)
    X_test, y_test = build_features(test_records, test_s2_raw, test_s4, s2_min, s2_max)

    # Save normalized feature dumps for inspection.
    save_feature_dump(
        os.path.join(OUT_DIR, "train_features_normalized.json"),
        train_records,
        train_s2_raw,
        train_s4,
        s2_min,
        s2_max,
    )
    save_feature_dump(
        os.path.join(OUT_DIR, "val_features_normalized.json"),
        val_records,
        val_s2_raw,
        val_s4,
        s2_min,
        s2_max,
    )
    save_feature_dump(
        os.path.join(OUT_DIR, "test_features_normalized.json"),
        test_records,
        test_s2_raw,
        test_s4,
        s2_min,
        s2_max,
    )

    print("\nFeature sanity:")
    print(f"  X_train shape: {X_train.shape}")
    print(f"  X_val shape:   {X_val.shape}")
    print(f"  X_test shape:  {X_test.shape}")
    print(f"  train labels: supported={(y_train==0).sum()} unsupported={(y_train==1).sum()}")
    print(f"  val labels:   supported={(y_val==0).sum()} unsupported={(y_val==1).sum()}")
    print(f"  test labels:  supported={(y_test==0).sum()} unsupported={(y_test==1).sum()}")

    # Fit fusion.
    print("\nFitting LogisticRegression fusion on TRAIN...")
    clf = LogisticRegression(max_iter=1000, random_state=SEED)
    clf.fit(X_train, y_train)

    train_prob = clf.predict_proba(X_train)[:, 1]
    val_prob = clf.predict_proba(X_val)[:, 1]
    test_prob = clf.predict_proba(X_test)[:, 1]

    threshold, val_best_f1 = best_threshold_by_f1(val_prob, y_val)

    train_metrics = metrics_at_threshold(train_prob, y_train, threshold)
    val_metrics = metrics_at_threshold(val_prob, y_val, threshold)
    test_metrics = metrics_at_threshold(test_prob, y_test, threshold)

    print("\n=== Fusion metrics ===")
    print("Threshold tuned on VAL F1:", threshold)

    print("\nTRAIN:")
    print(json.dumps(train_metrics, indent=2))

    print("\nVAL:")
    print(json.dumps(val_metrics, indent=2))

    print("\nTEST:")
    print(json.dumps(test_metrics, indent=2))

    # Save predictions.
    def pred_rows(records, X, y, prob, threshold):
        rows = []
        for ex, feats, label, p in zip(records, X, y, prob):
            pred = int(p >= threshold)
            rows.append({
                "id": ex["id"],
                "source": ex["source"],
                "orig_split": ex["orig_split"],
                "claim_id": ex["claim_id"],
                "abstract_id": ex["abstract_id"],
                "verdict": ex["verdict"],
                "label": int(label),
                "norm_s2_min_relevance": round(float(feats[0]), 6),
                "new_s4_score": round(float(feats[1]), 6),
                "fusion_p_unsupported": round(float(p), 6),
                "pred_unsupported": pred,
                "correct": bool(pred == int(label)),
                "answer": ex["answer"],
                "context_preview": ex["context"][:300],
            })
        return rows

    save_json(
        os.path.join(OUT_DIR, "train_fusion_predictions.json"),
        pred_rows(train_records, X_train, y_train, train_prob, threshold),
    )
    save_json(
        os.path.join(OUT_DIR, "val_fusion_predictions.json"),
        pred_rows(val_records, X_val, y_val, val_prob, threshold),
    )
    save_json(
        os.path.join(OUT_DIR, "test_fusion_predictions.json"),
        pred_rows(test_records, X_test, y_test, test_prob, threshold),
    )

    # Save coefficient file for deployment.
    coeffs = {
        "protocol": (
            "SciFact+HealthVer side-project verifier; custom source-stratified grouped split; "
            "no claim_id or abstract_id overlap across train/val/test; "
            "fusion fit on grouped train; threshold tuned on grouped val; test evaluated once"
        ),
        "s2_model": S2_MODEL_NAME,
        "s2_feature": (
            "raw_min_relevance: split claim/evidence into sentences; for each claim sentence, "
            "score against all evidence sentences; keep best evidence score; take min across claim sentences"
        ),
        "s2_norm": {
            "min": s2_min,
            "max": s2_max,
            "source": "computed from grouped train split only",
        },
        "s4_model_dir": S4_MODEL_DIR,
        "feature_order": [
            "norm_s2_min_relevance",
            "new_s4_score",
        ],
        "coef": clf.coef_.flatten().tolist(),
        "intercept": float(clf.intercept_[0]),
        "threshold": float(threshold),
        "score_convention": "output is P(unsupported); support_score = 1 - P(unsupported)",
        "label_mapping": {
            "SUPPORTED": 0,
            "CONTRADICT": 1,
            "NEI": 1,
        },
        "n_train": int(len(y_train)),
        "n_val": int(len(y_val)),
        "n_test": int(len(y_test)),
        "train_metrics": train_metrics,
        "val_metrics": val_metrics,
        "test_metrics": test_metrics,
        "sklearn_version": __import__("sklearn").__version__,
    }

    save_json(COEFFS_PATH, coeffs)

    all_results = {
        "coeffs_path": COEFFS_PATH,
        "coefficients": coeffs,
    }
    save_json(os.path.join(OUT_DIR, "fusion_refit_results.json"), all_results)

    print(f"\nSaved frozen coefficients to: {COEFFS_PATH}")
    print(f"Saved detailed results to: {OUT_DIR}/fusion_refit_results.json")

    print("\nDeployment artifacts for Project 3:")
    print(f"  S4 model: {S4_MODEL_DIR}")
    print(f"  Fusion coefficients: {COEFFS_PATH}")


if __name__ == "__main__":
    main()
