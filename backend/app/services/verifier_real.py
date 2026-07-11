"""
backend/app/services/verifier_real.py

The DEPLOYED verifier: a DeBERTa faithfulness classifier fine-tuned on a custom leakage-safe
grouped split of SciFact + HealthVer. See docs/verifier.md.

MODEL SOURCE. The checkpoint is ~700MB and is NOT in the repository — it lives on the Hub:

    https://huggingface.co/Primeinvincible/scifact-healthver-verifier

By default this class loads it from there (transformers caches it under ~/.cache/huggingface
after the first download, so a fresh clone just works). Set VERIFIER_MODEL_PATH to a local
directory to use a local checkpoint instead — useful offline, or when testing a new fine-tune
before publishing it:

    VERIFIER_MODEL_PATH=app/services/verifier_model/signal4_model_scifact_healthver

Scoring:
    tokenizer(claim, evidence), max_length=512, truncation, padding="max_length"
    p_unsupported = softmax(logits)[:, 1]
    support_score = 1 - p_unsupported            (the interface contract, in [0, 1])

The tokenization matches the thesis scoring script exactly; only the checkpoint differs.

Honest performance note. On the custom leakage-safe grouped SciFact+HealthVer test split:
F1 0.77, precision 0.71, recall 0.84, AUROC 0.71, ECE 0.19. It is recall-oriented and
imperfectly calibrated — scores are useful as labels and rankings, NOT as probabilities.

This is a side-project adaptation of the thesis verifier, not the thesis result itself. The
thesis system (RAGTruth S4 + out-of-fold fusion) is untouched and remains better calibrated
on its native domain.
"""

from __future__ import annotations

import os
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from app.services.verifier import Verifier

# Default: pull from the Hub, so a fresh clone works with no manual setup.
HF_MODEL_ID = "Primeinvincible/scifact-healthver-verifier"

# Optional override for a local checkpoint directory.
LOCAL_PATH_ENV = "VERIFIER_MODEL_PATH"

MAX_LENGTH = 512


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _resolve_model_source() -> str:
    """
    Local directory if VERIFIER_MODEL_PATH points at a real one; otherwise the Hub.

    Fails LOUDLY if VERIFIER_MODEL_PATH is set but missing. Silently falling through to the
    Hub would score with a DIFFERENT model than the operator intended — exactly the class of
    silent-substitution bug this project exists to avoid.
    """
    local = os.getenv(LOCAL_PATH_ENV)
    if local:
        path = Path(local)
        if not path.is_dir():
            raise FileNotFoundError(
                f"{LOCAL_PATH_ENV}={local!r} is set but is not a directory. "
                f"Unset it to load {HF_MODEL_ID} from the Hub instead."
            )
        return str(path)
    return HF_MODEL_ID


class RealVerifier(Verifier):
    """Fine-tuned DeBERTa faithfulness verifier. Loads the model once at construction."""

    def __init__(self) -> None:
        source = _resolve_model_source()
        origin = "local checkpoint" if source != HF_MODEL_ID else "HuggingFace Hub"
        print(f"[verifier] loading {source} ({origin}) ...")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(source)
        self.model = AutoModelForSequenceClassification.from_pretrained(source)
        self.model.to(self.device)
        self.model.eval()

        self.model_source = source
        print(f"[verifier] ready on {self.device}.")

    def _p_unsupported(self, claim: str, evidence: str) -> float:
        enc = self.tokenizer(
            claim, evidence,
            max_length=MAX_LENGTH, truncation=True,
            padding="max_length", return_tensors="pt",
        )
        enc = {k: v.to(self.device) for k, v in enc.items()}
        with torch.no_grad():
            logits = self.model(**enc).logits
            return float(torch.softmax(logits, dim=1)[0, 1].item())

    def verify(self, claim_text: str, evidence_text: str) -> float:
        """Return support_score in [0, 1] (higher = more supported)."""
        if not claim_text or not evidence_text:
            return 0.0
        return _clamp01(1.0 - self._p_unsupported(claim_text, evidence_text))

    def verify_verbose(self, claim_text: str, evidence_text: str) -> dict:
        p = self._p_unsupported(claim_text, evidence_text)
        return {
            "p_unsupported": round(p, 4),
            "support_score": round(_clamp01(1.0 - p), 4),
            "model": self.model_source,
        }


def _demo():
    from app.services.verifier import label_for_score

    v = RealVerifier()
    cases = [
        ("SUPPORTED",
         "Retrieval-augmented generation combines retrieval with generation.",
         "We introduce retrieval-augmented generation (RAG), which combines a pretrained "
         "parametric generator with a non-parametric retrieval component over Wikipedia."),
        ("UNSUPPORTED",
         "RAG was invented in 1995 by a secret government laboratory and requires quantum hardware.",
         "We introduce retrieval-augmented generation (RAG), which combines a pretrained "
         "parametric generator with a non-parametric retrieval component over Wikipedia."),
        ("PARTIAL",
         "Cross-encoder reranking improves retrieval and always runs in under one millisecond.",
         "Passage reranking with BERT cross-encoders substantially improves retrieval quality "
         "over first-stage retrievers, at higher computational cost."),
    ]
    print(f"\n{'case':<14} {'p_unsup':>8} {'support':>8}  label")
    print("-" * 48)
    for name, claim, evidence in cases:
        d = v.verify_verbose(claim, evidence)
        print(f"{name:<14} {d['p_unsupported']:>8} {d['support_score']:>8}  "
              f"{label_for_score(d['support_score'])}")


if __name__ == "__main__":
    _demo()
