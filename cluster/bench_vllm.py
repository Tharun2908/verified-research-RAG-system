"""
bench_vllm.py  --  RUNS ON THE CLUSTER (terminal 2, against the vLLM server in terminal 1)

Benchmarks the local vLLM server: throughput (tokens/sec, req/sec) and latency
percentiles (p50/p95/p99) across several concurrency levels, using realistic
grounded-RAG-shaped prompts.

Run AFTER `vllm serve ...` is up on localhost:8000.

USAGE:
    pip install httpx
    python bench_vllm.py
    # options: --url http://localhost:8000  --model mistralai/Mistral-7B-Instruct-v0.3
    #          --concurrencies 1,8,32,64  --requests-per-level 64  --max-tokens 200
    #          --tag bf16   (label for the run, e.g. bf16 vs fp8)
"""

import time
import json
import asyncio
import argparse
import statistics

import httpx

# A realistic grounded-RAG prompt shape: instruction + several evidence chunks + question.
# (Representative length so KV-cache / prefill costs are realistic, not toy.)
EVIDENCE_BLOCK = "\n".join(
    f"[{i}] " + ("Retrieval-augmented generation grounds language model outputs in retrieved "
                 "documents to reduce hallucination; this passage discusses method " + str(i) +
                 " and its empirical results across several benchmarks in detail. ") * 3
    for i in range(1, 6)
)
PROMPT = (
    "You are a research assistant. Answer the question using ONLY the numbered sources "
    "below. Cite the sources you use with their bracketed number, e.g. [1].\n\n"
    f"Sources:\n{EVIDENCE_BLOCK}\n\n"
    "Question: How does retrieval-augmented generation reduce hallucination?\n\n"
    "Answer (with citations):"
)


async def one_request(client, url, model, max_tokens):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
    }
    t0 = time.perf_counter()
    r = await client.post(f"{url}/v1/chat/completions", json=body, timeout=120)
    dt = time.perf_counter() - t0
    r.raise_for_status()
    data = r.json()
    out_tokens = data["usage"]["completion_tokens"]
    return dt, out_tokens


async def run_level(url, model, concurrency, n_requests, max_tokens):
    """Fire n_requests with the given concurrency; return aggregate stats."""
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency)
    async with httpx.AsyncClient(limits=limits) as client:
        sem = asyncio.Semaphore(concurrency)

        async def guarded():
            async with sem:
                return await one_request(client, url, model, max_tokens)

        wall_start = time.perf_counter()
        results = await asyncio.gather(*[guarded() for _ in range(n_requests)])
        wall = time.perf_counter() - wall_start

    latencies = [dt for dt, _ in results]
    total_out = sum(tok for _, tok in results)
    latencies.sort()

    def pct(p):
        k = max(0, min(len(latencies) - 1, int(round(p / 100 * (len(latencies) - 1)))))
        return latencies[k]

    return {
        "concurrency": concurrency,
        "requests": n_requests,
        "wall_s": round(wall, 2),
        "req_per_s": round(n_requests / wall, 2),
        "out_tokens": total_out,
        "tokens_per_s": round(total_out / wall, 1),
        "latency_p50_s": round(pct(50), 3),
        "latency_p95_s": round(pct(95), 3),
        "latency_p99_s": round(pct(99), 3),
        "latency_mean_s": round(statistics.mean(latencies), 3),
    }


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8000")
    ap.add_argument("--model", default="mistralai/Mistral-7B-Instruct-v0.3")
    ap.add_argument("--concurrencies", default="1,8,32,64")
    ap.add_argument("--requests-per-level", type=int, default=64)
    ap.add_argument("--max-tokens", type=int, default=200)
    ap.add_argument("--tag", default="bf16")
    ap.add_argument("--out", default="bench_results.json")
    args = ap.parse_args()

    levels = [int(x) for x in args.concurrencies.split(",")]
    print(f"Benchmarking {args.model} [{args.tag}] at concurrencies {levels}\n")

    # warmup (not measured) so the first real level isn't penalized by cold start
    print("Warmup...")
    await run_level(args.url, args.model, concurrency=4, n_requests=8, max_tokens=args.max_tokens)

    all_stats = []
    for c in levels:
        n = max(args.requests_per_level, c)  # ensure at least one full wave
        print(f"  concurrency={c}, requests={n} ...", flush=True)
        stats = await run_level(args.url, args.model, c, n, args.max_tokens)
        all_stats.append(stats)
        print(f"    {stats['req_per_s']} req/s | {stats['tokens_per_s']} tok/s | "
              f"p50={stats['latency_p50_s']}s p95={stats['latency_p95_s']}s p99={stats['latency_p99_s']}s")

    out = {"tag": args.tag, "model": args.model, "max_tokens": args.max_tokens, "levels": all_stats}
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"\n=== SUMMARY [{args.tag}] ===")
    print(f"{'conc':>5} {'req/s':>8} {'tok/s':>9} {'p50':>7} {'p95':>7} {'p99':>7}")
    for s in all_stats:
        print(f"{s['concurrency']:>5} {s['req_per_s']:>8} {s['tokens_per_s']:>9} "
              f"{s['latency_p50_s']:>7} {s['latency_p95_s']:>7} {s['latency_p99_s']:>7}")
    print(f"\nSaved to {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
