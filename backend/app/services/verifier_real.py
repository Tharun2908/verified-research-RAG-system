"""
backend/app/services/verifier_real.py

REAL verifier (deployed): the SciFact+HealthVer-adapted S4 model, S4-ONLY.

This is a side-project adaptation of the thesis verifier, NOT the thesis system itself:
  - Thesis verifier      = RAGTruth-trained S4 + out-of-fold S2+S4 fusion (stays untouched).
  - Deployed verifier    = S4 continued-fine-tuned on a custom leakage-safe grouped split of
                           SciFact + HealthVer, used S4-ONLY (no S2, no fusion).

Why S4-only: the fine-tuned S4 alone fixed the recall failure (obvious scientific
hallucinations that the thesis verifier missed), the S2+S4 fusion gain over S4-alone was
negligible, and that fusion was NOT out-of-fold (fit on in-sample S4 scores) — so S4-only is
the cleaner, more defensible deployment. Fusion code is kept separately as a documented,
honestly-labelled non-OOF diagnostic, not in the live path.

Recipe:
  S4 tokenization matches thesis signal4_score_train.py:
    tokenizer(answer=claim, context=evidence), max_length=512, truncation, padding="max_length"
    s4_p_unsupported = softmax(logits)[:,1]   (higher = more unsupported/hallucinated)
  support_score = 1 - s4_p_unsupported
  Label: three-band on support_score (>=0.70 Supported / 0.45-0.69 Weak / <0.45 Unsupported)
         via verifier.label_for_score (unchanged).

Model loads ONCE at construction (expensive). Instantiate at app startup (lifespan),
not per request. Wrap verify() calls in asyncio.to_thread at the call site so the sync torch
work doesn't block the event loop.

Honest performance note:
On the custom leakage-safe grouped SciFact+HealthVer test split, the S4-only verifier reached
approximately F1=0.77, precision=0.71, recall=0.84, AUROC=0.71, AUPRC=0.80, ECE=0.19.
It is recall-oriented and not perfectly calibrated; scores are useful for labels/ranking but
should NOT be treated as literal probabilities. The thesis verifier remains the better-calibrated
system on its native RAGTruth domain.
"""

from __future__ import annotations

from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from app.services.verifier import Verifier   # reuse the interface + label_for_score

_HERE = Path(__file__).parent
# Deployed = SciFact+HealthVer-adapted checkpoint. Thesis signal4_model/ stays untouched.
MODEL_DIR = _HERE / "verifier_model" / "signal4_model_scifact_healthver"
MAX_LENGTH = 512


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


class RealVerifier(Verifier):
    """SciFact+HealthVer-adapted S4-only verifier. Loads the model once at construction."""

    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
        self.model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
        self.model.to(self.device)
        self.model.eval()

    def _s4_p_unsupported(self, claim: str, evidence: str) -> float:
        """S4 P(unsupported) for (claim, evidence). tokenizer(answer=claim, context=evidence)."""
        enc = self.tokenizer(
            claim, evidence,
            max_length=MAX_LENGTH, truncation=True,
            padding="max_length", return_tensors="pt",
        )
        enc = {k: v.to(self.device) for k, v in enc.items()}
        with torch.no_grad():
            logits = self.model(**enc).logits
            p_unsup = torch.softmax(logits, dim=1)[0, 1].item()
        return float(p_unsup)

    def verify(self, claim_text: str, evidence_text: str) -> float:
        """Return support_score in [0,1] (higher = more supported)."""
        if not evidence_text or not claim_text:
            return 0.0
        p_unsup = self._s4_p_unsupported(claim_text, evidence_text)
        return _clamp01(1.0 - p_unsup)

    def verify_verbose(self, claim_text: str, evidence_text: str) -> dict:
        p_unsup = self._s4_p_unsupported(claim_text, evidence_text)
        return {
            "s4_p_unsupported": round(p_unsup, 4),
            "support_score": round(_clamp01(1.0 - p_unsup), 4),
        }


def _demo():
    from app.services.verifier import label_for_score
    v = RealVerifier()

    cases = [
        ("SUPPORTED (claim matches evidence)",
         "Retrieval-augmented generation combines retrieval with generation.",
         "We introduce retrieval-augmented generation (RAG), which combines a pretrained "
         "parametric generator with a non-parametric retrieval component over Wikipedia."),
        ("UNSUPPORTED (claim not in evidence)",
         "RAG was invented in 1995 by a secret government laboratory and requires quantum hardware.",
         "We introduce retrieval-augmented generation (RAG), which combines a pretrained "
         "parametric generator with a non-parametric retrieval component over Wikipedia."),
        ("PARTIAL (some support, some drift)",
         "Cross-encoder reranking improves retrieval and always runs in under one millisecond.",
         "Passage reranking with BERT cross-encoders substantially improves retrieval quality "
         "over first-stage retrievers, at higher computational cost."),
    ]

    print(f"{'case':<40} {'s4_unsup':>9} {'support':>8}  label")
    print("-" * 72)
    for name, claim, evidence in cases:
        d = v.verify_verbose(claim, evidence)
        lab = label_for_score(d["support_score"])
        print(f"{name:<40} {d['s4_p_unsupported']:>9} {d['support_score']:>8}  {lab}")

    print("\nSanity checks:")
    print("  - SUPPORTED  -> high support (Supported)")
    print("  - UNSUPPORTED -> low support (Unsupported)  [the fixed failure]")
    print("  - PARTIAL    -> likely Unsupported (model leans toward flagging overclaims)")


if __name__ == "__main__":
    _demo()
