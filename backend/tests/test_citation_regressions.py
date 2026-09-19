"""Citations must stay with their claim through splitting and evidence lookup."""

import pytest

from app.services.claim_extractor import extract_claims
from app.services.evidence_mapping import evidence_text_for_claim


@pytest.mark.parametrize("answer", [
    "RAG retrieves external knowledge. [1] DeBERTa verifies claims. [2]",
    "RAG retrieves external knowledge.[1] DeBERTa verifies claims.[2]",
    "RAG retrieves external knowledge.[1]DeBERTa verifies claims.[2]",
    "RAG retrieves external knowledge. [1]. DeBERTa verifies claims. [2].",
    "RAG retrieves external knowledge [1]. DeBERTa verifies claims [2].",
])
def test_sentence_suffix_citations_belong_to_the_preceding_claim(answer):
    claims = extract_claims(answer)
    assert [c["claim_text"] for c in claims] == [
        "RAG retrieves external knowledge.", "DeBERTa verifies claims.",
    ]
    assert [c["citations"] for c in claims] == [[1], [2]]


@pytest.mark.parametrize("markers", [
    "[1, 2]", "[1,2]", "[ 1 , 2 ]", "[1][2]", "[1] [2]",
    "[2, 1, 2][1]",
])
@pytest.mark.parametrize("after_period", [False, True])
def test_grouped_citations_are_parsed_cleaned_and_deduplicated(markers, after_period):
    sentence = "Both approaches improve retrieval"
    answer = f"{sentence}. {markers}" if after_period else f"{sentence} {markers}."
    claim, = extract_claims(answer)
    assert claim["claim_text"] == sentence + "."
    assert claim["citations"] == [1, 2]


def test_grouped_citations_limit_the_evidence_scope():
    claims = extract_claims(
        "RAG retrieves external knowledge. [1, 3] DeBERTa verifies claims. [2]"
    )
    evidence = [
        {"number": 1, "text": "Source one."},
        {"number": 2, "text": "Source two."},
        {"number": 3, "text": "Source three."},
        {"number": 4, "text": "Uncited distractor."},
    ]
    assert [evidence_text_for_claim(c["citations"], evidence) for c in claims] == [
        "Source one.\nSource three.", "Source two.",
    ]


def test_unknown_grouped_citations_do_not_become_uncited_claims():
    claim, = extract_claims("RAG requires quantum hardware. [8, 9]")
    assert claim["citations"] == [8, 9]
    assert evidence_text_for_claim(claim["citations"], [{"number": 1, "text": "Other."}]) == ""


def test_leading_citation_in_a_new_block_stays_in_that_block():
    claims = extract_claims(
        "- RAG retrieves external knowledge. [1]\n"
        "- [2, 3] DeBERTa verifies claims."
    )
    assert [c["citations"] for c in claims] == [[1], [2, 3]]


def test_citations_are_not_carried_over_from_a_discarded_fragment():
    claim, = extract_claims("Yes. [1] RAG retrieves external knowledge.")
    assert claim["citations"] == []


def test_abbreviations_and_decimal_numbers_still_work():
    claims = extract_claims(
        "Lewis et al. report a 0.25 gain, e.g. on retrieval. [1, 2] "
        "DeBERTa verifies claims [3]."
    )
    assert len(claims) == 2
    assert "et al." in claims[0]["claim_text"]
    assert "0.25" in claims[0]["claim_text"]
    assert [c["citations"] for c in claims] == [[1, 2], [3]]


@pytest.mark.parametrize("ending", ["?", "!", '."', ".\u201d", ".)"])
def test_citations_follow_sentence_punctuation_and_closing_marks(ending):
    claims = extract_claims(
        f"RAG retrieves external knowledge{ending} [1] DeBERTa verifies claims. [2]"
    )
    assert len(claims) == 2
    assert claims[0]["claim_text"] == "RAG retrieves external knowledge" + ending
    assert [c["citations"] for c in claims] == [[1], [2]]


def test_cited_refusal_does_not_steal_the_next_claims_citations():
    claims = extract_claims(
        "The provided sources do not discuss quantum computing. [1, 2] "
        "RAG requires quantum hardware. [3]"
    )
    assert [c["abstention"] for c in claims] == [True, False]
    assert [c["citations"] for c in claims] == [[1, 2], [3]]
