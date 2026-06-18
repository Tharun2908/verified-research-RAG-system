"""
backend/app/services/claim_extractor.py

M5 claim extraction (Path B: sentence-based, real and inspectable now).
Takes a generated answer and splits it into atomic claims, each carrying the
citation numbers it referenced. This is the bridge between generation (M4) and
verification (M6): the verifier scores each claim against its cited evidence, and
unsupported_claim_rate = (unsupported claims) / (total claims) is computed over these.

Design notes:
  - Sentence segmentation via regex (no nltk/spacy dependency for the MVP). Good enough
    for common cases; the planned upgrade is LLM-based decomposition (swappable without
    touching M6, since the output shape stays the same).
  - Each claim stores its citation numbers SEPARATELY from the claim text. The [n] markers
    are stripped from the text (so they don't add noise to the verifier's claim-vs-evidence
    comparison) but kept in `citations` (so M6 knows which evidence to check against).
"""

from __future__ import annotations

import re

# Split on sentence-ending punctuation (. ! ?) followed by whitespace and an uppercase
# letter or bracket. This avoids splitting on "et al." / "2020." in the middle of a
# sentence in the common case. Not perfect — the LLM upgrade handles hard cases.
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[])")

# Find citation markers like [1], [2], [10].
_CITATION = re.compile(r"\[(\d+)\]")

# The stub prefixes answers with "[STUB ANSWER]" — drop that token, it's not a claim.
_STUB_PREFIX = re.compile(r"^\[STUB ANSWER\]\s*", re.IGNORECASE)


def extract_claims(answer: str) -> list[dict]:
    """
    Split an answer into atomic claims.
    Returns a list of:
      {"claim_text": str, "citations": [int, ...]}
    Citations are the source numbers the claim referenced (may be empty).
    """
    # remove the stub prefix if present
    answer = _STUB_PREFIX.sub("", answer).strip()

    # also drop a trailing parenthetical the stub adds, e.g. "(This is placeholder...)"
    # (harmless for real answers; only matches the stub's note)
    answer = re.sub(r"\(This is placeholder text.*?\)$", "", answer, flags=re.DOTALL).strip()

    claims: list[dict] = []
    for raw in _SENTENCE_SPLIT.split(answer):
        sentence = raw.strip()
        if not sentence:
            continue

        # citation numbers in this sentence
        citations = [int(n) for n in _CITATION.findall(sentence)]

        # claim text = sentence with the [n] markers removed and whitespace tidied
        claim_text = _CITATION.sub("", sentence)
        claim_text = re.sub(r"\s+", " ", claim_text).strip()
        # tidy spaces left before punctuation, e.g. "outputs  ." -> "outputs."
        claim_text = re.sub(r"\s+([.,;:])", r"\1", claim_text)

        # filter: skip fragments that are too short to be a real claim
        if len(claim_text) < 12:
            continue

        claims.append({
            "claim_text": claim_text,
            "citations": sorted(set(citations)),
        })

    return claims


def _demo():
    sample = (
        "[STUB ANSWER] RAG combines retrieval with generation [1]. "
        "It reduces hallucination by grounding outputs in retrieved documents [2]. "
        "RAG was first introduced by Lewis et al. in 2020 [1]. "
        "The sources do not discuss deployment costs."
    )
    for i, c in enumerate(extract_claims(sample), 1):
        print(f"{i}. claim={c['claim_text']!r}  citations={c['citations']}")


if __name__ == "__main__":
    _demo()
