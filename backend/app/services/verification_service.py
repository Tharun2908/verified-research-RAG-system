"""
backend/app/services/verification_service.py

The pipeline: question -> retrieve -> generate -> extract claims -> verify each claim
against the evidence IT CITES -> persist -> report the unsupported-claim rate.

Flow:
  1. generate_answer          -> cited answer + numbered evidence  (raises GenerationError)
  2. extract_claims           -> atomic claims, each with its citation numbers
  3. verify each claim        -> support_score, then a label band
  4. unsupported_claim_rate   -> the headline metric
  5. persist across four tables, atomically

Claim<->evidence mapping: generation returns evidence numbered [1..N]; extraction keeps each
claim's citation numbers; we join them here. A claim citing [2] is checked against source 2
ONLY (so a claim that cites a source not supporting it is caught). An UNCITED claim is checked
against ALL retrieved evidence — the fair-chance policy: if nothing supports it, it is
genuinely unsupported rather than merely mis-cited.

Two failure modes are handled explicitly, because both once produced plausible-looking but
false output:

  - GENERATION FAILURE. An earlier version returned the upstream error as an "answer". The
    pipeline then extracted claims from the error message, scored them, and reported
    verification_status="verified" — a fabricated verification result.
  - STUB COMPONENTS. A console warning is invisible to an API client. Every response now
    carries a `components` block, and if either component is a stub the status is
    "development_stub", never "verified".
"""

from __future__ import annotations

import asyncio
import time
from datetime import datetime

from app.db.session import AsyncSessionLocal
from app.db import models
from app.monitoring import metrics
from app.services.claim_extractor import extract_claims
from app.services.evidence_mapping import evidence_text_for_claim as _evidence_text_for_claim
from app.services.generation_client import GenerationError, generation_client
from app.services.generator import generate_answer
from app.services.verifier import get_verifier, label_for_score


def _components() -> dict:
    """Which verifier and generator actually produced this result."""
    return {
        "verifier": get_verifier().describe(),
        "generator": generation_client.describe(),
    }


def _is_degraded(components: dict) -> bool:
    """True if either component is a stub — the result is not a real verification."""
    return (
        components["verifier"]["implementation"] == "StubVerifier"
        or components["generator"]["implementation"] == "StubGenerator"
    )


async def verify_question(question: str, top_k: int = 5) -> dict:
    """
    Full verified-research flow with persistence.

    Returns a dict with: job_id, answer, verification_status, components, per-claim labels
    and scores, and the unsupported_claim_rate.

    verification_status is one of:
        "verified"           real components, claims extracted and scored
        "development_stub"   a stub verifier and/or generator was used — scores are NOT real
        "unverifiable"       no claims could be extracted, so nothing was verified
        "generation_failed"  generation was unavailable; nothing was generated or verified
    """
    metrics.RESEARCH_REQUESTS.inc()
    request_start = time.perf_counter()

    # --- 1: generate (retrieval happens inside generate_answer) ---------------
    gen_start = time.perf_counter()
    try:
        gen = await generate_answer(question, top_k=top_k)
    except GenerationError as e:
        # A generation outage is a FAILURE, not an answer. Do not extract claims from an
        # error string and do not report anything as "verified".
        metrics.STAGE_LATENCY.labels(stage="generate").observe(time.perf_counter() - gen_start)
        metrics.REQUEST_LATENCY.observe(time.perf_counter() - request_start)
        return {
            "job_id": None,
            "question": question,
            "answer": None,
            "verification_status": "generation_failed",
            "error": str(e),
            "components": _components(),
            "n_claims": 0,
            "n_unsupported": 0,
            "unsupported_claim_rate": None,
            "grounding_score": None,
            "claims": [],
        }

    metrics.STAGE_LATENCY.labels(stage="generate").observe(time.perf_counter() - gen_start)
    answer = gen["answer"]
    evidence = gen["evidence"]          # [{number, title, text, chunk_id}]

    # --- 2: extract claims ----------------------------------------------------
    extract_start = time.perf_counter()
    claims = extract_claims(answer)     # [{claim_text, citations}]
    metrics.STAGE_LATENCY.labels(stage="extract").observe(time.perf_counter() - extract_start)

    # --- 3: score + label every claim ----------------------------------------
    # The real verifier is a DeBERTa forward pass per claim: synchronous, ~100s of ms each.
    # Running that inline would block the event loop for the whole request. All claims are
    # scored in ONE worker thread — one hop, not N.
    verify_start = time.perf_counter()
    verifier = get_verifier()

    def _score_all() -> list[float]:
        """Runs in a worker thread. No event loop, no awaits, no DB."""
        return [
            verifier.verify(
                c["claim_text"],
                _evidence_text_for_claim(c["citations"], evidence),
            )
            for c in claims
        ]

    scores = await asyncio.to_thread(_score_all) if claims else []

    scored_claims = []
    for c, score in zip(claims, scores):
        label = label_for_score(score)
        scored_claims.append({
            "claim_text": c["claim_text"],
            "citations": c["citations"],
            "support_score": score,
            "label": label,
        })
        metrics.CLAIMS_VERIFIED.inc()
        metrics.CLAIMS_BY_LABEL.labels(label=label).inc()

    metrics.STAGE_LATENCY.labels(stage="verify").observe(time.perf_counter() - verify_start)

    # --- 4: the headline metric ----------------------------------------------
    n_claims = len(scored_claims)
    if n_claims == 0:
        # Nothing was extracted -> NOTHING was verified. Reporting a 0% unsupported rate here
        # would masquerade as a perfectly-grounded answer.
        verification_status = "unverifiable"
        n_unsupported = 0
        unsupported_rate = None
        grounding_score = None
    else:
        verification_status = "verified"
        n_unsupported = sum(1 for c in scored_claims if c["label"] == "Unsupported")
        unsupported_rate = n_unsupported / n_claims
        grounding_score = sum(c["support_score"] for c in scored_claims) / n_claims

    # If a stub produced any of this, it is not a real verification and must not say it is.
    components = _components()
    if _is_degraded(components) and verification_status == "verified":
        verification_status = "development_stub"

    if unsupported_rate is not None:
        metrics.UNSUPPORTED_CLAIM_RATE.set(unsupported_rate)
    if grounding_score is not None:
        metrics.GROUNDING_SCORE.set(grounding_score)

    # --- 5: persist, atomically ----------------------------------------------
    async with AsyncSessionLocal() as session:
        job = models.ResearchJob(
            question=question,
            status="completed",
            completed_at=datetime.utcnow(),
        )
        session.add(job)
        await session.flush()           # assigns job.job_id

        result = models.ResearchResult(
            job_id=job.job_id,
            answer=answer,
            grounding_score=grounding_score,
            unsupported_rate=unsupported_rate,
        )
        session.add(result)

        by_number = {e["number"]: e for e in evidence}

        for sc in scored_claims:
            claim_row = models.Claim(
                job_id=job.job_id,
                claim_text=sc["claim_text"],
                support_score=sc["support_score"],
                label=sc["label"],
            )
            session.add(claim_row)
            await session.flush()       # assigns claim_row.claim_id

            # Link the claim to the chunk(s) it was actually verified against — the same
            # scoping rule used for scoring, so the stored provenance matches the score.
            cited = sc["citations"] if sc["citations"] else [e["number"] for e in evidence]
            for num in cited:
                ev = by_number.get(num)
                if ev is None:
                    continue            # a citation to a source that doesn't exist
                session.add(models.Evidence(
                    claim_id=claim_row.claim_id,
                    chunk_id=ev.get("chunk_id"),
                    evidence_text=ev["text"],
                    source_title=ev["title"],
                ))

        await session.commit()
        job_id = job.job_id

    metrics.REQUEST_LATENCY.observe(time.perf_counter() - request_start)

    return {
        "job_id": job_id,
        "question": question,
        "answer": answer,
        "verification_status": verification_status,
        "components": components,
        "n_claims": n_claims,
        "n_unsupported": n_unsupported,
        "unsupported_claim_rate": (
            round(unsupported_rate, 4) if unsupported_rate is not None else None
        ),
        "grounding_score": (
            round(grounding_score, 4) if grounding_score is not None else None
        ),
        "claims": scored_claims,
    }


async def _demo():
    result = await verify_question(
        "How can we detect when generated text is unfaithful to its source?",
        top_k=3,
    )
    print(f"status={result['verification_status']}  job_id={result['job_id']}")
    print(f"components: {result['components']}")
    print(f"claims={result['n_claims']}  unsupported={result['n_unsupported']}  "
          f"rate={result['unsupported_claim_rate']}\n")
    for i, c in enumerate(result["claims"], 1):
        print(f"  {i}. [{c['label']:<11} {c['support_score']:.3f}] {c['claim_text']}")


if __name__ == "__main__":
    asyncio.run(_demo())
