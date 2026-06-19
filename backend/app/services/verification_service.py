"""
backend/app/services/verification_service.py

M6 centerpiece: run the full pipeline for a research question and persist a verified
result tree across four tables.

Flow:
  1. generate_answer (M4)         -> draft cited answer + numbered evidence
  2. extract_claims (M5)          -> atomic claims, each with citation numbers
  3. for each claim:
       - gather its cited evidence text (citation number -> evidence item)
       - verifier.verify(claim, evidence) -> support_score
       - label_for_score(score)   -> Supported / Weak / Unsupported
  4. unsupported_claim_rate = #Unsupported / #claims        (the headline metric)
  5. persist: research_jobs -> research_results + claims -> evidence    (one transaction)

Why the claim<->evidence mapping works: M4 returned evidence numbered [1..N]; M5 kept each
claim's citation numbers; here we join them. Uncited claims are verified against ALL retrieved
evidence by default (configurable) so they get a fair score rather than an automatic zero.
"""

from __future__ import annotations

import asyncio
from datetime import datetime

import time
from app.db.session import AsyncSessionLocal
from app.db import models
from app.services.generator import generate_answer
from app.services.claim_extractor import extract_claims
from app.services.verifier import verifier, label_for_score
from app.monitoring import metrics


def _evidence_text_for_claim(citations: list[int], evidence: list[dict]) -> str:
    """
    Join the text of the evidence items this claim cited.
    evidence items are dicts {number, title, text}; citations are their numbers.
    If the claim cited nothing, fall back to ALL evidence (fair-chance policy).
    """
    by_number = {e["number"]: e for e in evidence}
    if citations:
        chosen = [by_number[c]["text"] for c in citations if c in by_number]
    else:
        chosen = [e["text"] for e in evidence]   # uncited -> verify against everything
    return "\n".join(chosen)


async def verify_question(question: str, top_k: int = 5) -> dict:
    """
    Full verified-research flow with persistence. Returns a summary dict including the
    persisted job_id, the answer, per-claim labels, and the unsupported_claim_rate.
    """
    metrics.RESEARCH_REQUESTS.inc()
    request_start = time.perf_counter()

    # 1: generate (retrieve happens inside generate_answer)
    gen_start = time.perf_counter()
    gen = await generate_answer(question, top_k=top_k)
    metrics.STAGE_LATENCY.labels(stage="generate").observe(time.perf_counter() - gen_start)
    answer = gen["answer"]
    evidence = gen["evidence"]   # [{number, title, text}]

    # 2: extract claims
    extract_start = time.perf_counter()
    claims = extract_claims(answer)   # [{claim_text, citations}]
    metrics.STAGE_LATENCY.labels(stage="extract").observe(time.perf_counter() - extract_start)

    # 3: score + label each claim (timed as the "verify" stage)
    verify_start = time.perf_counter()
    scored_claims = []
    for c in claims:
        ev_text = _evidence_text_for_claim(c["citations"], evidence)
        score = verifier.verify(c["claim_text"], ev_text)
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

    # 4: headline metric
    n_claims = len(scored_claims)
    n_unsupported = sum(1 for c in scored_claims if c["label"] == "Unsupported")
    unsupported_rate = (n_unsupported / n_claims) if n_claims else 0.0
    # overall grounding = mean support score (a simple summary number)
    grounding_score = (
        sum(c["support_score"] for c in scored_claims) / n_claims if n_claims else 0.0
    )
    metrics.UNSUPPORTED_CLAIM_RATE.set(unsupported_rate)
    metrics.GROUNDING_SCORE.set(grounding_score)

    # 5: persist the related record across four tables, atomically
    async with AsyncSessionLocal() as session:
        # research_jobs
        job = models.ResearchJob(
            question=question,
            status="completed",
            completed_at=datetime.utcnow(),
        )
        session.add(job)
        await session.flush()   # assigns job.job_id

        # research_results (PK = job_id)
        result = models.ResearchResult(
            job_id=job.job_id,
            answer=answer,
            grounding_score=grounding_score,
            unsupported_rate=unsupported_rate,
        )
        session.add(result)

        # claims (+ evidence per claim)
        for sc in scored_claims:
            claim_row = models.Claim(
                job_id=job.job_id,
                claim_text=sc["claim_text"],
                support_score=sc["support_score"],
                label=sc["label"],
            )
            session.add(claim_row)
            await session.flush()   # assigns claim_row.claim_id

            # evidence rows: link this claim to the chunk(s) it was verified against.
            # We map the claim's citation numbers back to evidence items (which carry the
            # title + text). NOTE: in this MVP the evidence dicts don't carry chunk_id;
            # we store the title + text snapshot. (A later refinement can thread chunk_id
            # through generator -> here for a hard FK to chunks.)
            cited = sc["citations"] if sc["citations"] else [e["number"] for e in evidence]
            by_number = {e["number"]: e for e in evidence}
            for num in cited:
                ev = by_number.get(num)
                if ev is None:
                    continue
                session.add(models.Evidence(
                    claim_id=claim_row.claim_id,
                    chunk_id=ev.get("chunk_id"),        # real FK to chunks (provenance)
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
        "n_claims": n_claims,
        "n_unsupported": n_unsupported,
        "unsupported_claim_rate": round(unsupported_rate, 4),
        "grounding_score": round(grounding_score, 4),
        "claims": scored_claims,
    }
    
    


async def _demo():
    result = await verify_question(
        "How can we detect when generated text is unfaithful to its source?",
        top_k=3,
    )
    print(f"job_id={result['job_id']}  unsupported_rate={result['unsupported_claim_rate']}  "
          f"grounding={result['grounding_score']}")
    print(f"claims: {result['n_claims']}  unsupported: {result['n_unsupported']}\n")
    for i, c in enumerate(result["claims"], 1):
        print(f"  {i}. [{c['label']:<11} {c['support_score']:.3f}] {c['claim_text']}")


if __name__ == "__main__":
    asyncio.run(_demo())
