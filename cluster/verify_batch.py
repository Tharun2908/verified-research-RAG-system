"""
verify_batch.py  --  RUNS ON THE CLUSTER (not the laptop)

Scores eval claims with the REAL thesis verifier: S2 (cross-encoder relevance) + S4
(fine-tuned DeBERTa) fused by the no-metadata logistic regression. Reuses the exact
thesis methodology:
  - S4 loading + scoring  == signal4_score_train.py  (softmax(logits)[:,1] = P(hallucination))
  - S2 normalization      == fusion_logreg_s2s4_no_meta.py  (S2_MIN/S2_MAX constants)
  - fusion                == fusion_logreg_s2s4_no_meta.py  (logreg on [norm_s2, s4], no metadata)

The fusion logreg is FIT on the thesis RAGTruth train scores (already on the cluster),
then APPLIED to the eval claims. This keeps the verifier identical to the thesis system.

Reads:  claims_to_verify.json   [{qid, arm, claim_index, claim_text, evidence_text}, ...]
        /workspace/relevance_results_train_v2.json  (S2 train scores, for fitting fusion)
        /workspace/signal4_results_train.json       (S4 train scores, for fitting fusion)
        /workspace/signal4_model/                    (the fine-tuned S4 checkpoint)
Writes: scores.json            [{qid, arm, claim_index, norm_s2, s4_score,
                                 hallucination_prob, support_score, label}, ...]

USAGE (cluster pod, after session setup):
    pip install sentence-transformers scikit-learn   # plus transformers/torch already there
    python verify_batch.py
    # paths overridable: --claims claims_to_verify.json --out scores.json
"""

import json
import argparse
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import CrossEncoder
from sklearn.linear_model import LogisticRegression

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
S4_MODEL_DIR = "/workspace/signal4_model"
S2_MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"
MAX_LENGTH = 512

# S2 normalization (from the thesis fusion scripts)
S2_MIN, S2_MAX = -11.430, 10.641

# support-score label thresholds (project convention)
SUPPORTED_THRESHOLD = 0.70
WEAK_THRESHOLD = 0.45

# fusion train data (thesis RAGTruth scores already on the cluster)
REL_TRAIN_PATH = "/workspace/relevance_results_train_v2.json"
S4_TRAIN_PATH = "/workspace/signal4_results_train.json"


def norm_s2(val):
    return float(max(0.0, min(1.0, (val - S2_MIN) / (S2_MAX - S2_MIN))))


def label_for_score(score):
    if score >= SUPPORTED_THRESHOLD:
        return "Supported"
    if score >= WEAK_THRESHOLD:
        return "Weak"
    return "Unsupported"


# ---------------------------------------------------------------------------
# 1. fit the no-metadata fusion on thesis RAGTruth train scores
# ---------------------------------------------------------------------------
def fit_fusion():
    with open(REL_TRAIN_PATH) as f:
        rel_train = {ex["idx"]: ex for ex in json.load(f)}
    with open(S4_TRAIN_PATH) as f:
        s4_train = {ex["idx"]: ex for ex in json.load(f)}

    common = sorted(rel_train.keys() & s4_train.keys())
    X, y = [], []
    for idx in common:
        r2, r4 = rel_train[idx], s4_train[idx]
        if r2["raw_min_relevance"] is None or r4["signal4_score"] is None:
            continue
        X.append([norm_s2(r2["raw_min_relevance"]), r4["signal4_score"]])
        y.append(int(r2["ground_truth_hallucination"]))
    X, y = np.array(X), np.array(y)

    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X, y)
    print(f"Fusion fit on {len(y)} RAGTruth train examples (features: norm_s2, s4).")
    return clf


# ---------------------------------------------------------------------------
# 2. score eval claims with S4 + S2
# ---------------------------------------------------------------------------
def score_claims(claims):
    # --- S4: fine-tuned DeBERTa, P(hallucination) = softmax(logits)[:,1] ---
    print("Loading S4 (fine-tuned DeBERTa)...")
    s4_tok = AutoTokenizer.from_pretrained(S4_MODEL_DIR)
    s4_model = AutoModelForSequenceClassification.from_pretrained(S4_MODEL_DIR).to(DEVICE)
    s4_model.eval()

    s4_scores = []
    print(f"Scoring {len(claims)} claims with S4...")
    with torch.no_grad():
        for i in range(0, len(claims), 16):
            batch = claims[i:i + 16]
            enc = s4_tok(
                [c["claim_text"] for c in batch],       # answer position
                [c["evidence_text"] for c in batch],    # context position  -> "answer [SEP] context"
                max_length=MAX_LENGTH,
                truncation=True,
                padding="max_length",
                return_tensors="pt",
            ).to(DEVICE)
            logits = s4_model(**enc).logits
            probs = torch.softmax(logits, dim=1)[:, 1].cpu().numpy()
            s4_scores.extend(probs.tolist())
            if (i // 16 + 1) % 5 == 0:
                print(f"  S4 {i + len(batch)}/{len(claims)}", flush=True)

    # free S4 before loading S2
    del s4_model
    if DEVICE == "cuda":
        torch.cuda.empty_cache()

    # --- S2: cross-encoder relevance, then normalize ---
    print("Loading S2 (cross-encoder)...")
    s2_model = CrossEncoder(S2_MODEL_ID, max_length=512, device=DEVICE)
    print(f"Scoring {len(claims)} claims with S2...")
    raw_s2 = s2_model.predict(
        [(c["claim_text"], c["evidence_text"]) for c in claims],
        batch_size=32,
        show_progress_bar=True,
    )
    norm_s2_scores = [norm_s2(float(v)) for v in raw_s2]

    return s4_scores, norm_s2_scores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", default="claims_to_verify.json")
    ap.add_argument("--out", default="scores.json")
    args = ap.parse_args()

    with open(args.claims, encoding="utf-8") as f:
        claims = json.load(f)
    print(f"Loaded {len(claims)} claims to verify.")

    clf = fit_fusion()
    s4_scores, norm_s2_scores = score_claims(claims)

    # --- fuse: predict P(hallucination), invert to support_score, label ---
    X_eval = np.array([[norm_s2_scores[i], s4_scores[i]] for i in range(len(claims))])
    halluc_probs = clf.predict_proba(X_eval)[:, 1]

    out = []
    for i, c in enumerate(claims):
        support = 1.0 - float(halluc_probs[i])      # SINGLE inversion at the boundary
        out.append({
            "qid": c["qid"],
            "arm": c["arm"],
            "claim_index": c["claim_index"],
            "norm_s2": round(norm_s2_scores[i], 4),
            "s4_score": round(s4_scores[i], 4),
            "hallucination_prob": round(float(halluc_probs[i]), 4),
            "support_score": round(support, 4),
            "label": label_for_score(support),
        })

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # quick summary
    from collections import Counter
    label_counts = Counter(r["label"] for r in out)
    print(f"\nWrote {len(out)} scored claims to {args.out}")
    print(f"Label distribution: {dict(label_counts)}")


if __name__ == "__main__":
    main()
