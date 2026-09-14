"""
Binary verifier decision policy.

Threshold provenance
--------------------
The deployed DeBERTa predicts P(unsupported). During SciFact+HealthVer training,
the binary decision threshold was selected on the held-out leakage-safe grouped
validation split by unsupported-class F1, then frozen before grouped test and
grounded-hard evaluation.

Frozen operating point:
    P(unsupported) >= 0.06  -> Unsupported
    P(unsupported) <  0.06  -> Supported

The public pipeline exposes support_score = 1 - P(unsupported), so the equivalent
rule is:
    support_score <= 0.94   -> Unsupported
    support_score >  0.94   -> Supported

Important: the verifier is not well calibrated (ECE about 0.19). The score is
useful for ranking and the frozen decision rule; it must not be interpreted as a
literal probability of correctness.

This pure module is mirrored into the standalone Hugging Face demo. CI asserts
that the backend and demo copies remain byte-for-byte identical.
"""

from __future__ import annotations

P_UNSUPPORTED_THRESHOLD = 0.06
SUPPORT_SCORE_CUTOFF = 1.0 - P_UNSUPPORTED_THRESHOLD


def label_for_score(support_score: float) -> str:
    """Apply the frozen validation-selected binary operating point."""
    if support_score <= SUPPORT_SCORE_CUTOFF:
        return "Unsupported"
    return "Supported"
