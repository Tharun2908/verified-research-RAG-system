"""
Claim extraction shared behavior for the backend and standalone Hugging Face demo.

The demo carries a mirrored copy of this pure module because the Space is deployed as a
standalone target. CI asserts the two copies are byte-for-byte identical so behavior cannot
silently diverge.

Extraction handles three independent failure modes:

1. ABBREVIATIONS
   Naive sentence splitting breaks on "vs.", "e.g.", "et al.", etc.
   Fix: mask abbreviation periods before sentence segmentation.

2. MARKDOWN / LIST STRUCTURE
   Numbered lists, bullets, headings, and line breaks are structural claim boundaries.
   Fix: split on structure first, then sentences within each block.

3. ABSTENTIONS
   Statements such as "the provided sources do not discuss X" are correct refusals, not
   factual claims to score with a binary support verifier.
   Fix: tag them with abstention=True so the pipeline can exclude them from unsupported-rate
   and grounding-score calculations.

See docs/verifier.md and backend/tests/.
"""

from __future__ import annotations

import re


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[])")

_BLOCK_SPLIT = re.compile(
    r"\n+"
    r"|(?:^|\n)\s*\d+[.)]\s+"
    r"|(?:^|\n)\s*[-*\u2022]\s+"
)

_HEADING = re.compile(r"^\s*#{1,6}\s*")
_LIST_MARKER = re.compile(r"^\s*(?:\d+[.)]|[-*\u2022])\s+")
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

_ABSTENTION_PAT = re.compile(
    r"(?:"
    r"(?:sources?|evidence|papers?|documents?|abstracts?|context|text|articles?|studies)"
    r"[^.]{0,60}?\b(?:do|does|did)\s+n[o']?t\b"
    r"[^.]{0,20}?\b(?:contain|discuss|mention|address|cover|provide|include|specify|state|"
    r"describe|report|say|indicate)"
    r"|"
    r"\bnone\s+of\s+the\b[^.]{0,60}?"
    r"\b(?:mention|discuss|contain|address|cover|provide|include|specify|state|describe|"
    r"report|say|indicate)"
    r"|"
    r"\b(?:no|not\s+enough|insufficient)\s+(?:relevant\s+)?information\b"
    r"|"
    r"\b(?:cannot|can'?t|could\s+n[o']?t|unable\s+to)\s+(?:be\s+)?"
    r"(?:answer|determin|find|establish)"
    r"|"
    r"\b(?:is|are|was|were)\s+not\s+"
    r"(?:discussed|mentioned|addressed|covered|described|provided|available|present)"
    r"|"
    r"\bthere\s+(?:is|are)\s+no\b[^.]{0,30}?"
    r"\b(?:mention|discussion|information|evidence|reference)"
    r")",
    re.IGNORECASE,
)


def _mask_abbrevs(text: str) -> str:
    for a in _ABBREVS:
        text = text.replace(a, a.replace(".", _MASK))
    return text


def _unmask(text: str) -> str:
    return text.replace(_MASK, ".")


def _strip_markdown(text: str) -> str:
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"(?<!\w)_{1,2}([^_]+)_{1,2}(?!\w)", r"\1", text)
    return text.replace("*", "")


def _clean(text: str) -> str:
    text = _strip_markdown(text)
    text = _HEADING.sub("", text)
    text = re.sub(r"\(\s*(?:[,;]|\s|and|or|to|[-\u2013\u2014])*\s*\)", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    text = re.sub(r"^\s*[A-Z][A-Za-z ]{0,30}:\s+(?=[A-Z])", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def is_abstention(text: str) -> bool:
    return bool(_ABSTENTION_PAT.search(text or ""))


def extract_claims(answer: str) -> list[dict]:
    """
    Split an answer into atomic claims.

    Returns:
        [{"claim_text": str, "citations": [int, ...], "abstention": bool}, ...]
    """
    if not answer or not answer.strip():
        return []

    answer = _STUB_PREFIX.sub("", answer).strip()
    answer = re.sub(
        r"\(This is placeholder text.*?\)$",
        "",
        answer,
        flags=re.DOTALL,
    ).strip()

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
            if _PREAMBLE.search(text):
                continue

            claims.append(
                {
                    "claim_text": text,
                    "citations": sorted(set(citations)),
                    "abstention": is_abstention(text),
                }
            )

    return claims


if __name__ == "__main__":
    sample = (
        "The provided sources do not discuss quantum search. "
        "RAG combines retrieval and generation [1]."
    )
    for i, claim in enumerate(extract_claims(sample), 1):
        print(i, claim)
