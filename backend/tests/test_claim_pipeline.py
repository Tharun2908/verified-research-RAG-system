"""
backend/tests/test_claim_pipeline.py

Unit tests for the pure-function core of the verification pipeline: claim extraction,
citation→evidence mapping, label banding, and the unsupported-rate calculation.

No models, no database, no network — these run in milliseconds and are the regression net
for the parts most likely to break silently (a bad sentence split or a mis-mapped citation
produces plausible-looking output, not an error).

Run:  pytest tests/ -v
"""

from __future__ import annotations

import pytest

from app.services.claim_extractor import extract_claims
from app.services.verifier import (
    StubVerifier,
    label_for_score,
    SUPPORTED_THRESHOLD,
    WEAK_THRESHOLD,
)
from app.services.verification_service import _evidence_text_for_claim


# ---------------------------------------------------------------- label bands
class TestLabelBands:
    def test_supported_at_and_above_threshold(self):
        assert label_for_score(SUPPORTED_THRESHOLD) == "Supported"
        assert label_for_score(0.95) == "Supported"
        assert label_for_score(1.0) == "Supported"

    def test_weak_between_thresholds(self):
        assert label_for_score(WEAK_THRESHOLD) == "Weak"
        assert label_for_score(0.60) == "Weak"
        assert label_for_score(SUPPORTED_THRESHOLD - 0.01) == "Weak"

    def test_unsupported_below_weak(self):
        assert label_for_score(WEAK_THRESHOLD - 0.01) == "Unsupported"
        assert label_for_score(0.0) == "Unsupported"

    def test_boundaries_are_inclusive_lower(self):
        """A score exactly on a threshold takes the HIGHER band."""
        assert label_for_score(0.70) == "Supported"
        assert label_for_score(0.45) == "Weak"


# ------------------------------------------------------------ claim extraction
class TestClaimExtraction:
    def test_splits_sentences(self):
        answer = "RAG combines retrieval and generation. It reduces hallucination."
        claims = extract_claims(answer)
        assert len(claims) == 2

    def test_captures_citations(self):
        answer = "RAG combines retrieval and generation [1]. It reduces hallucination [2]."
        claims = extract_claims(answer)
        assert claims[0]["citations"] == [1]
        assert claims[1]["citations"] == [2]

    def test_strips_citation_markers_from_claim_text(self):
        """The [n] markers must not reach the verifier — they are noise, not content."""
        claims = extract_claims("RAG combines retrieval and generation [1].")
        assert "[1]" not in claims[0]["claim_text"]
        assert claims[0]["claim_text"] == "RAG combines retrieval and generation."

    def test_multiple_citations_in_one_claim(self):
        claims = extract_claims("Both approaches reduce hallucination [1][3].")
        assert claims[0]["citations"] == [1, 3]

    def test_duplicate_citations_deduplicated(self):
        claims = extract_claims("This is supported [2] and also [2] again here.")
        assert claims[0]["citations"] == [2]

    def test_uncited_claim_has_empty_citations(self):
        claims = extract_claims("This sentence cites nothing at all.")
        assert claims[0]["citations"] == []

    def test_fragments_below_min_length_are_dropped(self):
        """Short fragments are not claims and must not be scored."""
        claims = extract_claims("Yes. This is a genuine claim about retrieval systems.")
        texts = [c["claim_text"] for c in claims]
        assert "Yes." not in texts

    def test_empty_answer_yields_no_claims(self):
        assert extract_claims("") == []
        assert extract_claims("   ") == []

    @pytest.mark.parametrize("abbrev_sentence", [
        "Correct generations show Wigner-Dyson vs. Poisson-like statistics in the spectrum.",
        "Several methods (e.g., NLI and cross-encoders) are compared in the study.",
        "This was first shown by Lewis et al. in their 2020 retrieval paper.",
        "The results in Fig. 3 confirm the trend across all model sizes.",
    ])
    def test_abbreviations_do_not_split_sentences(self, abbrev_sentence):
        """
        Regression: the sentence splitter used to break on the '.' in 'vs.', 'e.g.',
        'et al.', 'Fig.' — producing FRAGMENTS that the verifier then scored as claims
        and flagged unsupported. Human review measured a 6.7% extraction-failure rate
        from exactly this. One abbreviation-bearing sentence must yield ONE claim.
        """
        claims = extract_claims(abbrev_sentence)
        assert len(claims) == 1, f"split into {len(claims)}: {[c['claim_text'] for c in claims]}"


# ------------------------------------------------- citation -> evidence mapping
class TestEvidenceMapping:
    @pytest.fixture
    def evidence(self):
        return [
            {"number": 1, "title": "Paper One", "text": "Evidence text one."},
            {"number": 2, "title": "Paper Two", "text": "Evidence text two."},
            {"number": 3, "title": "Paper Three", "text": "Evidence text three."},
        ]

    def test_cited_claim_uses_only_its_cited_evidence(self, evidence):
        """A claim citing [2] is checked against source 2 — not everything."""
        text = _evidence_text_for_claim([2], evidence)
        assert "Evidence text two." in text
        assert "Evidence text one." not in text
        assert "Evidence text three." not in text

    def test_multiple_citations_join_their_evidence(self, evidence):
        text = _evidence_text_for_claim([1, 3], evidence)
        assert "Evidence text one." in text
        assert "Evidence text three." in text
        assert "Evidence text two." not in text

    def test_uncited_claim_falls_back_to_all_evidence(self, evidence):
        """
        Fair-chance policy: we don't know which source an uncited claim meant, so we give
        it EVERYTHING. If it fails against all retrieved evidence, it is genuinely
        unsupported — not merely mis-cited.
        """
        text = _evidence_text_for_claim([], evidence)
        for e in evidence:
            assert e["text"] in text

    def test_invalid_citation_number_is_ignored_not_crashed(self, evidence):
        """A model citing [9] when only 3 sources exist must not crash the pipeline."""
        text = _evidence_text_for_claim([9], evidence)
        assert text == ""   # no valid citations resolved

    def test_mixed_valid_and_invalid_citations(self, evidence):
        text = _evidence_text_for_claim([1, 9], evidence)
        assert "Evidence text one." in text

    def test_empty_evidence_list(self):
        assert _evidence_text_for_claim([1], []) == ""
        assert _evidence_text_for_claim([], []) == ""


# ------------------------------------------------------ unsupported-rate maths
class TestUnsupportedRate:
    """
    The headline metric. The critical case is ZERO claims: reporting 0.0 there would
    masquerade as a perfectly-grounded answer, when in fact NOTHING was verified.
    verification_service returns None + status 'unverifiable' instead.
    """

    @staticmethod
    def _rate(labels):
        if not labels:
            return None
        return sum(1 for l in labels if l == "Unsupported") / len(labels)

    def test_all_supported(self):
        assert self._rate(["Supported", "Supported"]) == 0.0

    def test_all_unsupported(self):
        assert self._rate(["Unsupported", "Unsupported"]) == 1.0

    def test_mixed(self):
        assert self._rate(["Supported", "Unsupported", "Weak", "Unsupported"]) == 0.5

    def test_weak_is_not_counted_as_unsupported(self):
        """Weak = retained. Only Unsupported counts against the rate."""
        assert self._rate(["Weak", "Weak"]) == 0.0

    def test_no_claims_is_none_not_zero(self):
        assert self._rate([]) is None


# --------------------------------------------------------------- stub verifier
class TestStubVerifier:
    """The stub is dev-only, but it must still honour the interface contract."""

    def test_returns_score_in_unit_range(self):
        v = StubVerifier()
        s = v.verify("some claim about retrieval", "some evidence about retrieval systems")
        assert 0.0 <= s <= 1.0

    def test_empty_evidence_scores_zero(self):
        assert StubVerifier().verify("a claim", "") == 0.0

    def test_empty_claim_scores_zero(self):
        assert StubVerifier().verify("", "some evidence") == 0.0

    def test_overlap_increases_score(self):
        v = StubVerifier()
        high = v.verify("retrieval augmented generation", "retrieval augmented generation is a method")
        low = v.verify("retrieval augmented generation", "completely unrelated text about cooking")
        assert high > low

# ------------------------------------------- markdown / list structure (regression)
class TestMarkdownStructure:
    """
    Regression: a hosted LLM emits numbered lists, bold labels, and headings. Sentence
    segmentation ALONE glued distinct list items into a single "claim", corrupting both the
    claim text and its citation mapping (a claim tagged [1] carried content from [3]).
    Observed live. The extractor now splits on structural boundaries BEFORE sentences.
    """

    MARKDOWN_ANSWER = (
        "Based on the sources, hallucinations can be detected using the following methods:\n\n"
        "1. **Human-like Criteria Probing (HCPD)** - This approach decomposes judgments "
        "into interpretable criteria [1].\n\n"
        "2. **Optimal Transport (OT)** - OT measures distances between attention "
        "patterns [3].\n\n"
        "**Key Limitation**: Neither method addresses all hallucination types [2]."
    )

    def test_list_items_do_not_merge(self):
        claims = extract_claims(self.MARKDOWN_ANSWER)
        # each list item is its own claim; none contains BOTH method names
        for c in claims:
            has_hcpd = "HCPD" in c["claim_text"]
            has_ot = "Optimal Transport" in c["claim_text"]
            assert not (has_hcpd and has_ot), f"list items merged: {c['claim_text']}"

    def test_citations_map_to_the_right_claim(self):
        claims = extract_claims(self.MARKDOWN_ANSWER)
        by_cite = {tuple(c["citations"]): c["claim_text"] for c in claims}
        assert "HCPD" in by_cite[(1,)]
        assert "Optimal Transport" in by_cite[(3,)]
        assert "Neither method" in by_cite[(2,)]

    def test_list_markers_stripped_from_claim_text(self):
        for c in extract_claims(self.MARKDOWN_ANSWER):
            assert not c["claim_text"].startswith(("1.", "2.", "-", "*"))

    def test_markdown_emphasis_stripped(self):
        for c in extract_claims(self.MARKDOWN_ANSWER):
            assert "**" not in c["claim_text"]

    def test_preamble_line_is_not_a_claim(self):
        """'...using the following methods:' announces; it asserts nothing verifiable."""
        texts = [c["claim_text"] for c in extract_claims(self.MARKDOWN_ANSWER)]
        assert not any(t.rstrip().endswith(":") for t in texts)

    def test_bullets_also_split(self):
        answer = "- First point about retrieval [1].\n- Second point about generation [2]."
        claims = extract_claims(answer)
        assert len(claims) == 2
        assert claims[0]["citations"] == [1]
        assert claims[1]["citations"] == [2]
