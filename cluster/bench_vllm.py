"""
bench_vllm.py  --  RUNS ON THE CLUSTER (terminal 2, against the vLLM server in terminal 1)

Benchmarks the local vLLM server: throughput (completion tokens/sec, req/sec)
and latency percentiles (p50/p95/p99) across several concurrency levels, using
grounded-RAG-shaped prompts.

Run AFTER `vllm serve ...` is up on localhost:8000.

USAGE:
    pip install httpx

    # More realistic RAG benchmark:
    # Same instruction/template, but varied evidence/question per request.
    python bench_vllm.py --tag fp8_prefix --prompt-mode vary_context

    # Prefix-cache stress test:
    # Same full prompt every request, useful as an upper-bound prefix-cache test.
    python bench_vllm.py --tag fp8_prefix_stress --prompt-mode repeat_full

OPTIONS:
    --url http://localhost:8000
    --model mistralai/Mistral-7B-Instruct-v0.3
    --concurrencies 1,8,32,64
    --requests-per-level 64
    --max-tokens 200
    --tag bf16 / fp8 / fp8_prefix / etc.
    --out bench_results.json
    --prompt-mode repeat_full | vary_context
"""

import time
import json
import asyncio
import argparse
import statistics
from typing import Dict, List, Tuple

import httpx


# ---------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------

RAG_INSTRUCTION = (
    "You are a research assistant. Answer the question using ONLY the numbered sources "
    "below. Cite the sources you use with their bracketed number, e.g. [1]."
)

# The old fixed evidence/question. This is useful for a prefix-cache stress test.
FIXED_EVIDENCE_BLOCK = "\n".join(
    f"[{i}] "
    + (
        "Retrieval-augmented generation grounds language model outputs in retrieved "
        "documents to reduce hallucination; this passage discusses method "
        + str(i)
        + " and its empirical results across several benchmarks in detail. "
    )
    * 3
    for i in range(1, 6)
)

FIXED_QUESTION = "How does retrieval-augmented generation reduce hallucination?"


TOPICS: List[Tuple[str, str]] = [
    (
        "retrieval-augmented generation",
        "How does retrieval-augmented generation reduce hallucination?",
    ),
    (
        "citation-grounded answering",
        "Why do citations help make generated answers more verifiable?",
    ),
    (
        "hybrid retrieval",
        "How can combining dense and sparse retrieval improve answer grounding?",
    ),
    (
        "reranking",
        "Why can reranking retrieved passages improve faithfulness in RAG?",
    ),
    (
        "context precision",
        "Why does irrelevant retrieved context increase hallucination risk?",
    ),
    (
        "answer verification",
        "How can post-generation verification detect unsupported claims?",
    ),
    (
        "query rewriting",
        "How can query rewriting improve retrieval quality?",
    ),
    (
        "chunking strategy",
        "Why does document chunking affect retrieval-augmented generation?",
    ),
    (
        "abstention",
        "Why should a RAG system abstain when evidence is insufficient?",
    ),
    (
        "long-context generation",
        "What problems can arise when too much context is given to a language model?",
    ),
]


def build_varied_evidence_block(prompt_id: int, n_chunks: int = 5) -> str:
    """
    Build deterministic but varied evidence chunks.

    This keeps the same RAG prompt template across requests, but changes the
    retrieved evidence content. That better matches real RAG serving, where
    the instruction is stable but retrieved chunks differ per query.
    """
    topic, _ = TOPICS[prompt_id % len(TOPICS)]

    chunks = []
    for j in range(1, n_chunks + 1):
        variant = (prompt_id + j) % 7

        text = (
            f"{topic.title()} is evaluated in setting {variant}, where retrieved passages "
            f"are used as evidence for generating answers. The method compares grounded "
            f"answers against unsupported generations and measures whether the answer can "
            f"be traced back to the provided source text. Passage {j} discusses retrieval "
            f"quality, evidence coverage, and the effect of source relevance on final answer "
            f"faithfulness. "
        ) * 3

        chunks.append(f"[{j}] {text}")

    return "\n".join(chunks)


def build_prompt(prompt_id: int, prompt_mode: str) -> str:
    """
    Build the prompt for one request.

    prompt_mode:
      - repeat_full:
          Same full prompt every request.
          This is useful for measuring an upper-bound prefix-cache/stress scenario.

      - vary_context:
          Same instruction/template, but varied evidence/question per request.
          This is more realistic for RAG serving.
    """
    if prompt_mode == "repeat_full":
        evidence_block = FIXED_EVIDENCE_BLOCK
        question = FIXED_QUESTION

    elif prompt_mode == "vary_context":
        evidence_block = build_varied_evidence_block(prompt_id)
        _, question = TOPICS[prompt_id % len(TOPICS)]

    else:
        raise ValueError(f"Unknown prompt_mode: {prompt_mode}")

    return (
        f"{RAG_INSTRUCTION}\n\n"
        f"Sources:\n{evidence_block}\n\n"
        f"Question: {question}\n\n"
        "Answer (with citations):"
    )


# ---------------------------------------------------------------------
# Request / benchmark logic
# ---------------------------------------------------------------------

async def one_request(
    client: httpx.AsyncClient,
    url: str,
    model: str,
    max_tokens: int,
    prompt_id: int,
    prompt_mode: str,
) -> Dict[str, float]:
    prompt = build_prompt(prompt_id=prompt_id, prompt_mode=prompt_mode)

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
    }

    t0 = time.perf_counter()
    r = await client.post(f"{url}/v1/chat/completions", json=body, timeout=120)
    dt = time.perf_counter() - t0

    r.raise_for_status()
    data = r.json()

    usage = data.get("usage", {})
    completion_tokens = usage.get("completion_tokens", 0)
    prompt_tokens = usage.get("prompt_tokens", 0)
    total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)

    return {
        "latency_s": dt,
        "completion_tokens": completion_tokens,
        "prompt_tokens": prompt_tokens,
        "total_tokens": total_tokens,
    }


async def run_level(
    url: str,
    model: str,
    concurrency: int,
    n_requests: int,
    max_tokens: int,
    prompt_mode: str,
    prompt_offset: int = 0,
) -> Dict[str, float]:
    """
    Fire n_requests with the given concurrency and return aggregate stats.

    Note:
      tokens_per_s is completion/output tokens per second, not prompt+completion tokens/sec.
    """
    limits = httpx.Limits(
        max_connections=concurrency,
        max_keepalive_connections=concurrency,
    )

    async with httpx.AsyncClient(limits=limits) as client:
        sem = asyncio.Semaphore(concurrency)

        async def guarded(i: int):
            async with sem:
                return await one_request(
                    client=client,
                    url=url,
                    model=model,
                    max_tokens=max_tokens,
                    prompt_id=prompt_offset + i,
                    prompt_mode=prompt_mode,
                )

        wall_start = time.perf_counter()
        results = await asyncio.gather(*[guarded(i) for i in range(n_requests)])
        wall = time.perf_counter() - wall_start

    latencies = [x["latency_s"] for x in results]
    latencies.sort()

    total_completion_tokens = sum(x["completion_tokens"] for x in results)
    total_prompt_tokens = sum(x["prompt_tokens"] for x in results)
    total_tokens = sum(x["total_tokens"] for x in results)

    def pct(p: float) -> float:
        k = max(
            0,
            min(
                len(latencies) - 1,
                int(round(p / 100 * (len(latencies) - 1))),
            ),
        )
        return latencies[k]

    req_per_s = n_requests / wall
    completion_tokens_per_s = total_completion_tokens / wall

    return {
        "concurrency": concurrency,
        "requests": n_requests,
        "wall_s": round(wall, 2),

        "req_per_s": round(req_per_s, 2),

        # Backward-compatible name:
        # This is completion/output tokens/sec, same as completion_tokens_per_s.
        "tokens_per_s": round(completion_tokens_per_s, 1),

        # More explicit names:
        "completion_tokens": total_completion_tokens,
        "completion_tokens_per_s": round(completion_tokens_per_s, 1),
        "prompt_tokens": total_prompt_tokens,
        "total_tokens": total_tokens,
        "avg_completion_tokens_per_request": round(total_completion_tokens / n_requests, 1),
        "avg_prompt_tokens_per_request": round(total_prompt_tokens / n_requests, 1),

        "latency_p50_s": round(pct(50), 3),
        "latency_p95_s": round(pct(95), 3),
        "latency_p99_s": round(pct(99), 3),
        "latency_mean_s": round(statistics.mean(latencies), 3),
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

async def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--model", default="mistralai/Mistral-7B-Instruct-v0.3")
    ap.add_argument("--concurrencies", default="1,8,32,64")
    ap.add_argument("--requests-per-level", type=int, default=64)
    ap.add_argument("--max-tokens", type=int, default=200)
    ap.add_argument("--tag", default="bf16")
    ap.add_argument("--out", default="bench_results.json")

    ap.add_argument(
        "--prompt-mode",
        choices=["repeat_full", "vary_context"],
        default="vary_context",
        help=(
            "repeat_full = same full prompt every request, useful as prefix-cache stress test; "
            "vary_context = same instruction/template but varied evidence/question per request."
        ),
    )

    args = ap.parse_args()

    levels = [int(x.strip()) for x in args.concurrencies.split(",") if x.strip()]

    print(f"Benchmarking {args.model} [{args.tag}]")
    print(f"URL: {args.url}")
    print(f"Concurrencies: {levels}")
    print(f"Prompt mode: {args.prompt_mode}")
    print(f"Max output tokens cap: {args.max_tokens}\n")

    # Warmup is not measured.
    # In vary_context mode, use a large offset so warmup prompts are not the same
    # as measured prompts. In repeat_full mode, the full prompt is intentionally
    # identical by design.
    print("Warmup...")
    await run_level(
        url=args.url,
        model=args.model,
        concurrency=4,
        n_requests=8,
        max_tokens=args.max_tokens,
        prompt_mode=args.prompt_mode,
        prompt_offset=1_000_000,
    )

    all_stats = []

    for level_idx, c in enumerate(levels):
        # Ensure at least one full wave at each concurrency.
        n = max(args.requests_per_level, c)

        # Offset measured prompts per level so vary_context does not reuse the
        # exact same request set across all concurrency levels.
        prompt_offset = level_idx * 100_000

        print(f"  concurrency={c}, requests={n} ...", flush=True)

        stats = await run_level(
            url=args.url,
            model=args.model,
            concurrency=c,
            n_requests=n,
            max_tokens=args.max_tokens,
            prompt_mode=args.prompt_mode,
            prompt_offset=prompt_offset,
        )

        all_stats.append(stats)

        print(
            f"    {stats['req_per_s']} req/s | "
            f"{stats['tokens_per_s']} completion tok/s | "
            f"avg_out={stats['avg_completion_tokens_per_request']} tok/req | "
            f"p50={stats['latency_p50_s']}s "
            f"p95={stats['latency_p95_s']}s "
            f"p99={stats['latency_p99_s']}s"
        )

    out = {
        "tag": args.tag,
        "model": args.model,
        "url": args.url,
        "max_tokens": args.max_tokens,
        "prompt_mode": args.prompt_mode,
        "note": (
            "tokens_per_s is completion/output tokens per second, not prompt+completion tokens/sec. "
            "max_tokens is a cap; actual completion length can be lower."
        ),
        "levels": all_stats,
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n=== SUMMARY [{args.tag}] ===")
    print(f"prompt_mode={args.prompt_mode}")
    print(
        f"{'conc':>5} "
        f"{'req/s':>8} "
        f"{'out tok/s':>10} "
        f"{'avg out':>8} "
        f"{'p50':>7} "
        f"{'p95':>7} "
        f"{'p99':>7}"
    )

    for s in all_stats:
        print(
            f"{s['concurrency']:>5} "
            f"{s['req_per_s']:>8} "
            f"{s['tokens_per_s']:>10} "
            f"{s['avg_completion_tokens_per_request']:>8} "
            f"{s['latency_p50_s']:>7} "
            f"{s['latency_p95_s']:>7} "
            f"{s['latency_p99_s']:>7}"
        )

    print(f"\nSaved to {args.out}")


if __name__ == "__main__":
    asyncio.run(main())