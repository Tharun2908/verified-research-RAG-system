"""
backend/app/services/evidence_mapping.py

Maps a claim's citation numbers to the evidence text it should be verified against.

Kept separate from verification_service (which owns generation, persistence, and metrics)
because this is PURE LOGIC — no I/O, no DB, no models. That makes it independently testable
and keeps the DB stack out of the test path.

Policy:
  - claim cites [n]  -> verify against ONLY those cited sources.
      The model asserted "this comes from source n". We test exactly that assertion, so a
      claim that cites [2] but whose content isn't in [2] gets caught.
  - claim cites nothing -> verify against ALL retrieved evidence.
      We can't know which source it meant, so it gets the fair-chance policy: if NOTHING
      retrieved supports it, it is genuinely unsupported (not merely mis-cited).
  - invalid citation number (e.g. [9] when 3 sources exist) -> ignored, not fatal.
"""

from __future__ import annotations


def evidence_text_for_claim(citations: list[int], evidence: list[dict]) -> str:
    """
    Join the text of the evidence items this claim cited.

    evidence: [{"number": int, "title": str, "text": str}, ...]
    citations: the source numbers the claim referenced (possibly empty)
    """
    by_number = {e["number"]: e for e in evidence}
    if citations:
        chosen = [by_number[c]["text"] for c in citations if c in by_number]
    else:
        chosen = [e["text"] for e in evidence]
    return "\n".join(chosen)


# Backwards-compatible alias (verification_service imported it under the old private name)
_evidence_text_for_claim = evidence_text_for_claim