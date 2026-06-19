"""
backend/app/services/verifier.py

M6 verification interface + stub implementation.

The real verifier is the thesis S2+S4 logistic-regression fusion (see cluster:
/workspace/fusion_logreg_s2s4.py, signal4_model/). Per the project's environment-isolation
rule, the real verifier runs in its OWN pinned environment (transformers==4.44.0) and is
swapped in later; it must NOT contaminate fastapi-env. So here we:

  - define the clean interface the rest of the system depends on:
        verify(claim_text, evidence_text) -> support_score in [0, 1]   (higher = more supported)
  - provide a STUB implementation for local dev (no model, no GPU, no transformers pin)
  - provide the label mapping (thesis thresholds), used regardless of which verifier is active

When the real verifier is wired in (its own service/env), it satisfies the same `verify`
signature; nothing downstream changes. Same swappable pattern as the generation client.

Thesis facts the REAL implementation will use (NOT needed by the stub):
  S2 = cross-encoder/ms-marco-MiniLM-L-6-v2, min-aggregated, normalized with
       S2_MIN=-11.430, S2_MAX=10.641 ; norm_s2 = clamp01((raw_min - S2_MIN)/(S2_MAX - S2_MIN))
  S4 = fine-tuned nli-deberta-v3-base (signal4_model/), transformers==4.44.0,
       ignore_mismatched_sizes=True, input "answer [SEP] context", higher = more hallucination
  Fusion = logistic regression over [norm_s2_min, s4_score, task_onehot, model_onehot]
  Output = support probability in [0,1]  (this interface's contract)
"""

from __future__ import annotations

import re

# --- label thresholds (thesis) ---------------------------------------------
# support_score in [0,1], higher = more supported.
SUPPORTED_THRESHOLD = 0.70   # >= 0.70 -> Supported (green)
WEAK_THRESHOLD = 0.45        # 0.45-0.69 -> Weak (amber); < 0.45 -> Unsupported (red)


def label_for_score(score: float) -> str:
    """Map a support score to a label using the thesis thresholds."""
    if score >= SUPPORTED_THRESHOLD:
        return "Supported"
    if score >= WEAK_THRESHOLD:
        return "Weak"
    return "Unsupported"


# --- verifier interface -----------------------------------------------------
class Verifier:
    """
    Base interface. Real and stub verifiers both implement `verify`.
    """

    def verify(self, claim_text: str, evidence_text: str) -> float:
        raise NotImplementedError


class StubVerifier(Verifier):
    """
    Placeholder verifier for local dev. Returns a deterministic, VARIED support score
    based on lexical overlap between claim and evidence (a weak proxy for support, so
    test output shows a realistic mix of labels). NOT the real verifier — no S2/S4, no model.
    """

    def verify(self, claim_text: str, evidence_text: str) -> float:
        if not evidence_text:
            return 0.0   # no evidence to support against

        claim_tokens = set(re.findall(r"\w+", claim_text.lower()))
        evid_tokens = set(re.findall(r"\w+", evidence_text.lower()))
        if not claim_tokens:
            return 0.0

        # fraction of claim words that appear in the evidence (Jaccard-ish, claim-weighted)
        overlap = len(claim_tokens & evid_tokens) / len(claim_tokens)

        # squash a bit so pure-overlap=1.0 maps near (but not exactly) 1, and add a small
        # floor so partial overlaps land in the Weak band rather than collapsing to 0.
        score = 0.15 + 0.80 * overlap
        return max(0.0, min(1.0, score))


# Active verifier for the app. Swap this line to the real verifier later (in its own env).
verifier: Verifier = StubVerifier()


def _demo():
    pairs = [
        ("RAG combines retrieval with generation.",
         "We introduce retrieval-augmented generation, combining parametric and non-parametric memory."),
        ("RAG was invented in 1995 by a secret lab.",
         "We introduce retrieval-augmented generation, combining parametric and non-parametric memory."),
        ("Cross-encoders rerank passages.",
         "Passage reranking with BERT cross-encoders improves retrieval quality over first-stage retrievers."),
    ]
    for claim, evidence in pairs:
        s = verifier.verify(claim, evidence)
        print(f"score={s:.3f}  label={label_for_score(s):<11}  claim={claim!r}")


if __name__ == "__main__":
    _demo()
