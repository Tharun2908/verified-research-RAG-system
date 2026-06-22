"""
loadtest_verify.py  --  M10A application-layer load test (runs on the LAPTOP)

Drives sustained concurrent load at the FastAPI /verify endpoint and reports throughput
and latency percentiles across concurrency levels. Purpose: expose the event-loop-blocking
bottleneck (per-request BM25 index rebuild inside hybrid_search), then re-run after the fix
to show the improvement.

Diagnostic signature to look for:
  - BEFORE fix: throughput (req/s) FLAT or degrading as concurrency rises (requests serialize
    on the synchronous BM25 build that blocks the event loop), latency balloons.
  - AFTER fix: throughput scales with concurrency, latency stays bounded.

Run against the live app (stub generator, so generation latency doesn't mask the retrieval
bottleneck). FastAPI must be running on the given URL, with Docker infra (postgres/qdrant/redis) up.

USAGE:
    pip install httpx
    python loadtest_verify.py --tag before_fix
    # options: --url http://localhost:8000  --endpoint /verify
    #          --concurrencies 1,4,8,16,32  --requests-per-level 64  --top-k 5
    #          --out loadtest_before.json

A small rotating set of varied questions is used so requests aren't trivially identical
(though the bottleneck is corpus-wide BM25 rebuild, which is query-independent).
"""

import time
import json
import asyncio
import argparse
import statistics
from urllib.parse import quote

import httpx

QUESTIONS = [
    "How does retrieval-augmented generation reduce hallucination?",
    "What methods detect unsupported claims in generated text?",
    "How does cross-encoder reranking improve retrieval?",
    "Why do citations make answers more verifiable?",
    "How is hybrid dense-sparse retrieval combined?",
    "What is claim-level verification in RAG?",
    "How does prefix caching speed up LLM serving?",
    "Why does long context increase hallucination risk?",
]


async def one_request(client, base_url, endpoint, question, top_k):
    url = f"{base_url}{endpoint}?q={quote(question)}&top_k={top_k}"
    t0 = time.perf_counter()
    r = await client.get(url, timeout=120)
    dt = time.perf_counter() - t0
    ok = r.status_code == 200
    return dt, ok


async def run_level(base_url, endpoint, concurrency, n_requests, top_k):
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency)
    async with httpx.AsyncClient(limits=limits) as client:
        sem = asyncio.Semaphore(concurrency)

        async def guarded(i):
            async with sem:
                return await one_request(
                    client, base_url, endpoint, QUESTIONS[i % len(QUESTIONS)], top_k
                )

        wall_start = time.perf_counter()
        results = await asyncio.gather(*[guarded(i) for i in range(n_requests)], return_exceptions=True)
        wall = time.perf_counter() - wall_start

    # separate successes from errors
    oks = [r for r in results if isinstance(r, tuple) and r[1]]
    errs = len(results) - len(oks)
    latencies = sorted(dt for dt, _ in oks)

    def pct(p):
        if not latencies:
            return 0.0
        k = max(0, min(len(latencies) - 1, int(round(p / 100 * (len(latencies) - 1)))))
        return latencies[k]

    return {
        "concurrency": concurrency,
        "requests": n_requests,
        "errors": errs,
        "wall_s": round(wall, 2),
        "req_per_s": round(len(oks) / wall, 2) if wall > 0 else 0.0,
        "latency_p50_s": round(pct(50), 3),
        "latency_p95_s": round(pct(95), 3),
        "latency_p99_s": round(pct(99), 3),
        "latency_mean_s": round(statistics.mean(latencies), 3) if latencies else 0.0,
    }


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--endpoint", default="/verify")
    ap.add_argument("--concurrencies", default="1,4,8,16,32")
    ap.add_argument("--requests-per-level", type=int, default=64)
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--tag", default="before_fix")
    ap.add_argument("--out", default="loadtest_results.json")
    args = ap.parse_args()

    levels = [int(x) for x in args.concurrencies.split(",")]
    print(f"M10A load test [{args.tag}]  {args.url}{args.endpoint}")
    print(f"Concurrencies: {levels}, {args.requests_per_level} req/level, top_k={args.top_k}\n")

    # warmup (not measured) - also triggers any first-request lazy init
    print("Warmup (8 requests at concurrency 2)...")
    await run_level(args.url, args.endpoint, 2, 8, args.top_k)

    all_stats = []
    for c in levels:
        n = max(args.requests_per_level, c)
        print(f"  concurrency={c}, requests={n} ...", flush=True)
        stats = await run_level(args.url, args.endpoint, c, n, args.top_k)
        all_stats.append(stats)
        print(f"    {stats['req_per_s']} req/s | "
              f"p50={stats['latency_p50_s']}s p95={stats['latency_p95_s']}s p99={stats['latency_p99_s']}s | "
              f"errors={stats['errors']}")

    out = {"tag": args.tag, "url": args.url, "endpoint": args.endpoint,
           "top_k": args.top_k, "levels": all_stats}
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n=== SUMMARY [{args.tag}] ===")
    print(f"{'conc':>5} {'req/s':>8} {'p50':>8} {'p95':>8} {'p99':>8} {'errors':>7}")
    for s in all_stats:
        print(f"{s['concurrency']:>5} {s['req_per_s']:>8} {s['latency_p50_s']:>8} "
              f"{s['latency_p95_s']:>8} {s['latency_p99_s']:>8} {s['errors']:>7}")
    print(f"\nKEY DIAGNOSTIC: does req/s SCALE with concurrency, or flatline?")
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
