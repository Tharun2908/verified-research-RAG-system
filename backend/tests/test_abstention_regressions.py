"""Abstention detection must not hide factual assertions from verification."""

import pytest

from app.services.claim_extractor import extract_claims, is_abstention


@pytest.mark.parametrize("text", [
    "The model cannot determine whether a claim is supported.",
    "The algorithm is unable to find the optimal solution.",
    "The benchmark contains insufficient information for this task.",
    "There is insufficient information in the dataset to estimate the parameters.",
    "There is insufficient information to determine the optimal model size.",
    "We cannot establish convergence under this learning rate.",
    "There is no evidence that the treatment improves outcomes.",
    "The results were not reported in the paper.",
    "The paper does not discuss the limitations of its method.",
    "The article quotes the assistant saying I cannot answer confidently.",
    "The sources do not discuss this, but RAG was invented in 1995.",
    "The sources do not discuss this but RAG was invented in 1995.",
    "I cannot answer confidently; RAG requires quantum hardware.",
    "I cannot answer confidently, however RAG requires quantum hardware.",
    "I cannot answer confidently and RAG requires quantum hardware.",
    "I cannot answer confidently so RAG requires quantum hardware.",
    "I cannot answer confidently because RAG requires quantum hardware.",
    "The provided sources do not discuss RAG, which requires quantum hardware.",
    "The provided sources do not discuss RAG — it requires quantum hardware.",
    "I cannot answer confidently (RAG requires quantum hardware).",
])
def test_factual_or_mixed_statement_remains_verifiable(text):
    assert is_abstention(text) is False
    claims = extract_claims(text.rstrip(".") + " [2].")
    assert len(claims) == 1
    assert claims[0]["abstention"] is False
    assert claims[0]["citations"] == [2]
    assert claims[0]["claim_text"] == text


def test_colon_separated_assertion_remains_verifiable():
    text = "The sources do not discuss this: RAG was invented in 1995 [2]."
    assert not is_abstention(text)
    claim, = extract_claims(text)
    # Existing label cleanup can remove the text before the colon. The factual
    # assertion and its citation must still reach verification.
    assert claim["claim_text"] == "RAG was invented in 1995."
    assert claim["abstention"] is False
    assert claim["citations"] == [2]


@pytest.mark.parametrize("text", [
    "I cannot answer confidently.",
    "I can't determine the answer from the provided sources.",
    "I can’t determine the answer from the provided sources.",
    "I am unable to answer from the retrieved evidence.",
    "I'm unable to determine the answer.",
    "We cannot establish the answer from the provided context.",
    "The provided sources do not discuss quantum computing.",
    "The sources don't mention quantum computing.",
    "The retrieved evidence does not contain the answer.",
    "These abstracts do not provide the answer.",
    "None of the provided sources mention quantum computing.",
    "There is insufficient information to determine the answer.",
    "There is not enough relevant information to answer the question.",
])
def test_clear_standalone_refusal_is_abstention(text):
    assert is_abstention(text) is True
    claims = extract_claims(text)
    assert len(claims) == 1
    assert claims[0]["abstention"] is True


def test_refusal_does_not_exempt_the_next_sentence():
    claims = extract_claims(
        "I cannot answer confidently. RAG requires quantum hardware [2]."
    )
    assert [c["abstention"] for c in claims] == [True, False]
    assert claims[1]["citations"] == [2]


def test_classifier_does_not_accept_multiple_sentences_as_one_abstention():
    assert not is_abstention("I cannot answer confidently. RAG requires quantum hardware.")


@pytest.mark.parametrize("text", ["", "   ", None])
def test_empty_input_is_not_an_abstention(text):
    assert is_abstention(text) is False
