"""
backend/app/services/generate_arxiv_v2_bait_questions.py

Generate v2 bait questions for the clean arXiv distillation train set.

Purpose:
  Add unsupported/refusal-pressure examples to the v2 train pool. These questions are
  plausible scientific/ML/arXiv-style questions but are not tied to a home paper.

Duplicate blocking:
  - old/dev eval_questions.json
  - v1 fresh/validated/train/gold questions
  - v2 grounded train_questions.json
  - existing v2 bait_questions.json if resuming

Output:
  data/distill_arxiv_v2/bait_questions.json
  data/distill_arxiv_v2/bait_question_generation_raw.json
  data/distill_arxiv_v2/bait_question_generation_report.json

Run from backend/:
  set OPENROUTER_MODEL=anthropic/claude-opus-4.8
  python -m app.services.generate_arxiv_v2_bait_questions --n 80

Smoke:
  python -m app.services.generate_arxiv_v2_bait_questions --n 5
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import httpx

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


DATA = Path("data")
V1_DIR = DATA / "distill_arxiv"
V2_DIR = DATA / "distill_arxiv_v2"

OUT_FINAL = V2_DIR / "bait_questions.json"
OUT_RAW = V2_DIR / "bait_question_generation_raw.json"
OUT_REPORT = V2_DIR / "bait_question_generation_report.json"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-opus-4.8")


SYSTEM_PROMPT = (
    "You write adversarial-but-realistic bait questions for evaluating a scientific RAG system. "
    "The questions should sound plausible for ML/AI/arXiv papers, but should not rely on a specific "
    "provided paper. The goal is to test whether a RAG system fabricates details or correctly refuses "
    "when retrieved evidence is insufficient."
)

USER_TEMPLATE = """Generate exactly {n} bait questions for a scientific RAG hallucination-verification dataset.

Requirements:
- Questions should be plausible for ML/AI/computer-science papers.
- They should ask for specific details such as exact benchmark numbers, ablation outcomes, dataset sizes, method components, author claims, implementation details, or comparisons.
- They should NOT be generic.
- They should NOT ask yes/no questions.
- They should NOT mention "provided evidence", "sources", "abstract", or "paper above".
- They should be diverse across NLP, retrieval, agents, recommendation, vision-language, medical AI, graph learning, optimization, and evaluation.
- Avoid copying these existing question styles too closely:
{examples}

Return ONLY a JSON array of strings, no markdown, no prose.
"""


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_question(q: Any) -> str:
    s = str(q or "").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def dup_key(q: str) -> str:
    q = q.lower().strip()
    q = re.sub(r"[^a-z0-9]+", " ", q)
    return re.sub(r"\s+", " ", q).strip()


def collect_questions(obj: Any, out: list[str]) -> None:
    if isinstance(obj, dict):
        if obj.get("question"):
            out.append(norm_question(obj["question"]))
        if obj.get("query"):
            out.append(norm_question(obj["query"]))
        if obj.get("prompt"):
            out.append(norm_question(obj["prompt"]))
        if "questions" in obj:
            collect_questions(obj["questions"], out)
        for v in obj.values():
            if isinstance(v, (dict, list)):
                collect_questions(v, out)
    elif isinstance(obj, list):
        for x in obj:
            collect_questions(x, out)
    elif isinstance(obj, str):
        s = norm_question(obj)
        if s.endswith("?"):
            out.append(s)


def load_duplicate_blockers() -> tuple[set[str], list[str]]:
    paths = [
        DATA / "eval_questions.json",
        V1_DIR / "fresh_questions.json",
        V1_DIR / "fresh_questions_validated.json",
        V1_DIR / "distill_train_questions.json",
        V1_DIR / "gold_eval_questions.json",
        V2_DIR / "train_questions.json",
        V2_DIR / "bait_questions.json",
    ]

    questions: list[str] = []
    for p in paths:
        if not p.exists():
            continue
        try:
            collect_questions(load_json(p), questions)
        except Exception:
            pass

    keys = {dup_key(q) for q in questions if q}
    keys = {k for k in keys if k}
    return keys, questions


def parse_questions(content: str) -> list[str]:
    txt = (content or "").strip()

    if txt.startswith("```"):
        txt = txt.strip("`").strip()
        if txt.lower().startswith("json"):
            txt = txt[4:].strip()

    start = txt.find("[")
    end = txt.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            arr = json.loads(txt[start : end + 1])
            if isinstance(arr, list):
                return [norm_question(x) for x in arr if norm_question(x)]
        except json.JSONDecodeError:
            pass

    out = []
    for line in txt.splitlines():
        line = line.strip()
        line = re.sub(r"^[-*]\s*", "", line)
        line = re.sub(r"^\d+[\).\s-]+", "", line).strip()
        if line.endswith("?"):
            out.append(norm_question(line))
    return out


def call_model(client: httpx.Client, api_key: str, model: str, n: int, examples: list[str], max_retries: int) -> list[str]:
    example_text = "\n".join(f"- {x}" for x in examples[:30])

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(n=n, examples=example_text)},
        ],
        "temperature": 0.4,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Verified Research Agent",
    }

    delay = 2.0
    for attempt in range(max_retries):
        try:
            resp = client.post(OPENROUTER_URL, json=body, headers=headers, timeout=120)

            if resp.status_code == 429:
                print(f"    rate-limited; sleeping {delay:.0f}s")
                time.sleep(delay)
                delay *= 2
                continue

            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            return parse_questions(content)

        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"    {type(e).__name__}; retry in {delay:.0f}s")
            time.sleep(delay)
            delay *= 2

    return []


def load_existing() -> list[dict[str, Any]]:
    if OUT_FINAL.exists():
        data = load_json(OUT_FINAL)
        if isinstance(data, list):
            return data
    return []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=80)
    ap.add_argument("--batch-size", type=int, default=25)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--max-retries", type=int, default=4)
    args = ap.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Check backend/.env or shell environment.")

    duplicate_keys, duplicate_questions = load_duplicate_blockers()
    existing = load_existing()

    accepted: list[dict[str, Any]] = []
    seen = set(duplicate_keys)

    for r in existing:
        q = norm_question(r.get("question"))
        k = dup_key(q)
        if q and k not in seen:
            seen.add(k)
            accepted.append(r)

    raw_batches = []
    if OUT_RAW.exists():
        try:
            raw_batches = load_json(OUT_RAW)
            if not isinstance(raw_batches, list):
                raw_batches = []
        except Exception:
            raw_batches = []

    print("\nGenerating v2 bait questions")
    print("=" * 64)
    print(f"Target n:              {args.n}")
    print(f"Existing accepted:     {len(accepted)}")
    print(f"Duplicate blockers:    {len(duplicate_keys)}")
    print(f"Model:                 {args.model}")

    with httpx.Client() as client:
        while len(accepted) < args.n:
            need = args.n - len(accepted)
            request_n = min(args.batch_size, max(need + 5, 10))

            try:
                qs = call_model(
                    client=client,
                    api_key=api_key,
                    model=args.model,
                    n=request_n,
                    examples=duplicate_questions[-50:],
                    max_retries=args.max_retries,
                )
                status = "ok"
                error = None
            except Exception as e:
                qs = []
                status = "api_error"
                error = str(e)[:500]

            kept_this_batch = []
            for q in qs:
                q = norm_question(q)
                if not q or not q.endswith("?"):
                    continue
                k = dup_key(q)
                if k in seen:
                    continue
                seen.add(k)
                rec = {
                    "id": len(accepted) + 1,
                    "qid": len(accepted) + 1,
                    "type": "bait",
                    "source": "distill_arxiv_v2_bait_train",
                    "question": q,
                    "generation_model": args.model,
                    "home_paper_id": None,
                    "home_corpus_paper_id": None,
                    "home_title": None,
                }
                accepted.append(rec)
                kept_this_batch.append(q)
                if len(accepted) >= args.n:
                    break

            raw_batches.append({
                "model": args.model,
                "status": status,
                "error": error,
                "requested": request_n,
                "raw_questions": qs,
                "kept": kept_this_batch,
                "accepted_total_after_batch": len(accepted),
            })

            save_json(OUT_RAW, raw_batches)
            save_json(OUT_FINAL, accepted)

            print(f"  accepted {len(accepted)}/{args.n} | kept batch={len(kept_this_batch)} status={status}")
            if status != "ok":
                raise SystemExit(f"Generation failed: {error}")

            time.sleep(args.sleep)

    for i, r in enumerate(accepted, start=1):
        r["id"] = i
        r["qid"] = i

    report = {
        "target_n": args.n,
        "final_n": len(accepted),
        "model": args.model,
        "duplicate_blockers_loaded": len(duplicate_keys),
        "output": str(OUT_FINAL),
        "raw_output": str(OUT_RAW),
        "note": "Bait questions are train-only and must still be paired with non-protected retrieved evidence.",
    }

    save_json(OUT_FINAL, accepted)
    save_json(OUT_REPORT, report)

    print("\nDone.")
    print(f"Bait questions written: {len(accepted)}")
    print(f"Wrote: {OUT_FINAL}")
    print(f"Wrote: {OUT_RAW}")
    print(f"Wrote: {OUT_REPORT}")


if __name__ == "__main__":
    main()
