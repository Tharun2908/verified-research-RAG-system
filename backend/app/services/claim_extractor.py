"""
backend/app/services/claim_extractor.py

Claim extraction: split a generated answer into atomic claims, each carrying the citation
numbers it referenced. This is the bridge between generation and verification — the verifier
scores each claim against its CITED evidence, and unsupported_claim_rate is computed over
these claims.

EXTRACTION IS A FAILURE MODE IN ITS OWN RIGHT, independent of verifier accuracy. Human review
of 150 generated rows measured a 6.7% raw extraction-failure rate. Two distinct causes, both
handled here:

  1. ABBREVIATIONS. A naive splitter breaks on the "." in "vs.", "e.g.", "et al." — the
     verifier then scores a sentence FRAGMENT and flags it unsupported. The verifier is
     right; the input is garbage. Fix: mask abbreviations before splitting.

  2. MARKDOWN STRUCTURE. Generators emit numbered lists, bullets, and headings. Sentence
     segmentation alone glues distinct list items into one "claim" — corrupting both the
     claim text AND its citation mapping (a claim tagged [1] can carry content from [3]).
     Fix: split on line/list boundaries FIRST, then on sentences within each block.

The generator is also prompted for plain prose (see generator.py). Belt and braces: the
extractor must not depend on the generator obeying.

See docs/verifier.md and tests/test_claim_pipeline.py.
"""

from __future__ import annotations

import re

# --- sentence segmentation --------------------------------------------------
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[])")

# Structural boundaries that are NOT sentence-enders but DO separate assertions:
#   - newlines / blank lines
#   - numbered list items:  "1. "  "2) "
#   - bullets:              "- "  "* "  "• "
# Split on these BEFORE sentence segmentation, so list items never merge.
_BLOCK_SPLIT = re.compile(
    r"\n+"                        # any newline run
    r"|(?:^|\n)\s*\d+[.)]\s+"     # 1.  2)  at start of a line
    r"|(?:^|\n)\s*[-*\u2022]\s+"  # -  *  bullet  at start of a line
)

_HEADING = re.compile(r"^\s*#{1,6}\s*")
# Leading list markers that survive the block split: "1. ", "2) ", "- ", "* ", "• "
_LIST_MARKER = re.compile(r"^\s*(?:\d+[.)]|[-*\u2022])\s+")
# A stub/preamble line that only announces what follows ("...using the following methods:")
# carries no verifiable assertion. Dropping it prevents a non-claim from being scored.
_PREAMBLE = re.compile(r":\s*$")
_CITATION = re.compile(r"\[(\d+)\]")
_STUB_PREFIX = re.compile(r"^\[STUB ANSWER\]\s*", re.IGNORECASE)

_ABBREVS = [
    "e.g.", "i.e.", "et al.", "vs.", "cf.", "approx.", "etc.", "resp.",
    "Fig.", "Eq.", "Sec.", "Ref.", "Tab.", "Ch.", "No.", "al.",
    "Dr.", "Prof.", "Inc.", "Ltd.", "St.",
]
_MASK = "\u241F"

MIN_CLAIM_CHARS = 12


def _mask_abbrevs(text: str) -> str:
    for a in _ABBREVS:
        text = text.replace(a, a.replace(".", _MASK))
    return text


def _unmask(text: str) -> str:
    return text.replace(_MASK, ".")


def _strip_markdown(text: str) -> str:
    """Remove emphasis. Generators emit it; the verifier was never trained on asterisks."""
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"(?<!\w)_{1,2}([^_]+)_{1,2}(?!\w)", r"\1", text)
    return text.replace("*", "")


def _clean(text: str) -> str:
    """Tidy a claim after citation-stripping and markdown removal."""
    text = _strip_markdown(text)
    text = _HEADING.sub("", text)
    # parens left empty by citation stripping: "(, , or )" / "(-)" / "( )"
    text = re.sub(r"\(\s*(?:[,;]|\s|and|or|to|[-\u2013\u2014])*\s*\)", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    # drop a dangling label left by a stripped heading: "Key Limitation: Neither method..."
    text = re.sub(r"^\s*[A-Z][A-Za-z ]{0,30}:\s+(?=[A-Z])", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def extract_claims(answer: str) -> list[dict]:
    """
    Split an answer into atomic claims.

    Returns: [{"claim_text": str, "citations": [int, ...]}, ...]

    Two-stage segmentation:
      1. BLOCK split  — newlines, numbered items, bullets (structural boundaries)
      2. SENTENCE split within each block (abbreviation-safe)
    """
    if not answer or not answer.strip():
        return []

    answer = _STUB_PREFIX.sub("", answer).strip()
    answer = re.sub(r"\(This is placeholder text.*?\)$", "", answer, flags=re.DOTALL).strip()

    claims: list[dict] = []

    for block in _BLOCK_SPLIT.split(answer):
        if not block or not block.strip():
            continue

        block = _LIST_MARKER.sub("", block.strip())

        for raw in _SENTENCE_SPLIT.split(_mask_abbrevs(block)):
            sentence = _unmask(raw).strip()
            if not sentence:
                continue

            citations = [int(n) for n in _CITATION.findall(sentence)]
            text = _clean(_CITATION.sub("", sentence))

            if len(text) < MIN_CLAIM_CHARS:
                continue
            # A line that merely announces what follows ("...the following methods:") makes
            # no verifiable assertion. Scoring it would flag a non-claim as unsupported.
            if _PREAMBLE.search(text):
                continue

            claims.append({
                "claim_text": text,
                "citations": sorted(set(citations)),
            })

    return claims


def _demo():
    sample = (
        "Based on the provided sources, hallucinations can be detected without a source "
        "document using the following methods:\n\n"
        "1. **Human-like Criteria Probing (HCPD)** - This approach emulates human evaluators "
        "by decomposing judgments into interpretable criteria (e.g., logical consistency) "
        "and aggregating scores [1].\n\n"
        "2. **Optimal Transport (OT)** - OT measures geometric distances between attention "
        "patterns compared to reference distributions [3]. It struggles when attention is "
        "correct but content misrepresents source meaning [3].\n\n"
        "**Key Limitation**: Neither method addresses all hallucination types [2]."
    )
    for i, c in enumerate(extract_claims(sample), 1):
        print(f"{i}. cites={c['citations']}  {c['claim_text']}")


if __name__ == "__main__":
    _demo()
