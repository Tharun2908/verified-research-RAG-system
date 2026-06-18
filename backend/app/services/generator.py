"""
backend/app/services/generator.py

The M4 generation step: question -> retrieve evidence -> grounded prompt -> LLM -> cited answer.

Connects M3 (hybrid_search) to M1 (generation_client). Produces a DRAFT cited answer.
Important framing: prompting for citations does NOT guarantee grounding — the model can
cite a source that doesn't actually support the statement. That is exactly the failure M6's
verifier detects. So this step produces a draft; M6 is what measures whether it's grounded.

Returns BOTH the answer text and the numbered evidence list, because the citation number ->
chunk mapping is what M5 (claim extraction) and M6 (verification) need downstream.
"""

from __future__ import annotations

import asyncio

from app.services.hybrid_search import hybrid_search
from app.services.generation_client import generation_client


def build_prompt(question: str, evidence: list[dict]) -> str:
    """
    Assemble the grounded-generation prompt: instruction + numbered sources + question.
    The [n] numbering is the citation handle that ties the answer back to specific chunks.
    """
    sources_block = "\n".join(
        f"[{e['number']}] {e['text']}" for e in evidence
    )
    return (
        "You are a research assistant. Answer the question using ONLY the numbered "
        "sources below. Cite the sources you use with their bracketed number, e.g. [1]. "
        "If the sources do not contain the answer, say so explicitly.\n\n"
        f"Sources:\n{sources_block}\n\n"
        f"Question: {question}\n\n"
        "Answer (with citations):"
    )


async def generate_answer(
    question: str,
    top_k: int = 5,
) -> dict:
    """
    Full M4 flow. Returns:
      {
        "question": str,
        "answer": str,                # the (draft, possibly-ungrounded) cited answer
        "evidence": [                 # numbered evidence the answer was grounded on
            {"number": int, "title": str, "text": str},
            ...
        ],
      }
    """
    # 1. retrieve top evidence chunks (M3 hybrid pipeline)
    hits = await hybrid_search(question, top_k=top_k)

    # 2. number the evidence 1..N — this numbering is the citation contract
    evidence = [
        {"number": i, "title": h["title"], "text": h["text"]}
        for i, h in enumerate(hits, start=1)
    ]

    # 3. build the grounded prompt
    prompt = build_prompt(question, evidence)

    # 4. call the LLM (stub now; vLLM/API later via env var — no code change)
    answer = await generation_client.generate(prompt)

    return {
        "question": question,
        "answer": answer,
        "evidence": evidence,
    }


async def _demo():
    result = await generate_answer(
        "How can we detect when generated text is unfaithful to its source?",
        top_k=3,
    )
    print("QUESTION:", result["question"])
    print("\nANSWER:\n", result["answer"])
    print("\nEVIDENCE:")
    for e in result["evidence"]:
        print(f"  [{e['number']}] {e['title']}")


if __name__ == "__main__":
    asyncio.run(_demo())
