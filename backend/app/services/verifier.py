"""
backend/app/services/verifier.py

Verification interface + verifier selection.

The DEPLOYED verifier is the SciFact/HealthVer-adapted DeBERTa (see verifier_real.py and
docs/verifier.md). It is the DEFAULT. The StubVerifier is a lexical-overlap placeholder for
local development only, and must be opted into EXPLICITLY:

    DEV_STUB_VERIFIER=true

This is deliberate. An earlier version of this repo defaulted to the stub while the README
implied real verification — producing convincing-looking but meaningless grounding labels.
Real-by-default, loud-warning-on-stub prevents that class of mistake.

Contract (unchanged, both implementations satisfy it):
    verify(claim_text, evidence_text) -> support_score in [0, 1]   (higher = more supported)

Label bands (support_score):
    >= 0.70  Supported     (green)
    0.45-0.69 Weak         (amber)
    <  0.45  Unsupported   (red)
"""

from __future__ import annotations

import asyncio
import os
import re

# --- label thresholds -------------------------------------------------------
SUPPORTED_THRESHOLD = 0.70
WEAK_THRESHOLD = 0.45


def label_for_score(score: float) -> str:
    """Map a support score to a label."""
    if score >= SUPPORTED_THRESHOLD:
        return "Supported"
    if score >= WEAK_THRESHOLD:
        return "Weak"
    return "Unsupported"


# --- verifier interface -----------------------------------------------------
class Verifier:
    """Base interface. Real and stub verifiers both implement `verify`."""

    def verify(self, claim_text: str, evidence_text: str) -> float:
        raise NotImplementedError


class StubVerifier(Verifier):
    """
    DEV ONLY. Lexical-overlap placeholder — NOT a real verifier. Produces varied-looking
    scores so the pipeline can be exercised without loading a model, but the scores are
    scientifically meaningless. Requires DEV_STUB_VERIFIER=true to be selected.
    """

    def verify(self, claim_text: str, evidence_text: str) -> float:
        if not evidence_text:
            return 0.0
        claim_tokens = set(re.findall(r"\w+", claim_text.lower()))
        evid_tokens = set(re.findall(r"\w+", evidence_text.lower()))
        if not claim_tokens:
            return 0.0
        overlap = len(claim_tokens & evid_tokens) / len(claim_tokens)
        return max(0.0, min(1.0, 0.15 + 0.80 * overlap))


# --- selection --------------------------------------------------------------
_verifier: Verifier | None = None


def _use_stub() -> bool:
    return os.getenv("DEV_STUB_VERIFIER", "").strip().lower() in {"1", "true", "yes"}


def get_verifier() -> Verifier:
    """
    Return the process-wide verifier singleton, constructing it on first use.

    Default: RealVerifier (fine-tuned DeBERTa; loads a ~700MB checkpoint once).
    Stub: only when DEV_STUB_VERIFIER is explicitly set — and it says so, loudly.
    """
    global _verifier
    if _verifier is None:
        if _use_stub():
            print(
                "\n" + "!" * 78 + "\n"
                "!! DEV_STUB_VERIFIER=true -> using StubVerifier (lexical overlap).\n"
                "!! Grounding scores are NOT real. Unset DEV_STUB_VERIFIER for the\n"
                "!! fine-tuned verifier.\n"
                + "!" * 78 + "\n"
            )
            _verifier = StubVerifier()
        else:
            # imported lazily so the stub path never pays the torch/transformers import
            from app.services.verifier_real import RealVerifier
            _verifier = RealVerifier()
    return _verifier


async def warm_verifier() -> str:
    """
    Load the verifier at STARTUP (lifespan), not on the first request — model loading is
    seconds of blocking work and must not land on a user's request. Returns the class name.
    """
    v = await asyncio.to_thread(get_verifier)
    return type(v).__name__


def reset_verifier_for_tests() -> None:
    """Clear the singleton (tests only)."""
    global _verifier
    _verifier = None
