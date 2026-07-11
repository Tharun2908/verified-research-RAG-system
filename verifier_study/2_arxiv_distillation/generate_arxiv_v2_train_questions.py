"""
backend/app/services/generate_arxiv_v2_train_questions.py

Generate Option-B train questions only from safe non-gold-evidence papers.

Requires first:
  python -m app.services.build_arxiv_v2_safe_papers

Input:
  data/distill_arxiv_v2/safe_train_source_papers.json

Output:
  data/distill_arxiv_v2/train_questions_raw.json
  data/distill_arxiv_v2/train_questions.json
  data/distill_arxiv_v2/train_question_generation_report.json

Run from backend/:
  set OPENROUTER_MODEL=anthropic/claude-opus-4.8
  python -m app.services.generate_arxiv_v2_train_questions --n-per-paper 3

Smoke:
  python -m app.services.generate_arxiv_v2_train_questions --limit-papers 3 --n-per-paper 3
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

SAFE_PAPERS = V2_DIR / "safe_train_source_papers.json"
OUT_RAW = V2_DIR / "train_questions_raw.json"
OUT_FINAL = V2_DIR / "train_questions.json"
OUT_REPORT = V2_DIR / "train_question_generation_report.json"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-opus-4.8")


SYSTEM_PROMPT = (
    "You write high-quality scientific evaluation questions for a RAG system. "
    "Each question must be answerable from the provided paper title and abstract, "
    "but should require a factual, specific answer rather than a vague summary."
)

USER_TEMPLATE = """Paper title:
{title}

Paper abstract:
{abstract}

Write exactly {n} grounded questions about this paper.

Requirements:
- Each question must be answerable from the title/abstract.
- Questions should ask about concrete methods, limitations, results, datasets, comparisons, metrics, or contributions.
- Avoid yes/no questions.
- Avoid generic questions like "What is the main idea?"
- Do not mention "the abstract" or "the provided text".
- Make each question useful for later claim-level fact checking.
- Return ONLY a JSON array of strings, no markdown, no prose.

Example:
["What limitation of prior graph-based recommendation methods does the paper identify?", "What benchmark improvement does the proposed method report?"]
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


def paper_title(p: dict[str, Any]) -> str:
    return str(p.get("_v2_title") or p.get("title") or p.get("paper_title") or "").strip()


def paper_abstract(p: dict[str, Any]) -> str:
    return str(p.get("_v2_abstract") or p.get("abstract") or p.get("summary") or p.get("text") or "").strip()


def corpus_id(p: dict[str, Any]) -> Any:
    return p.get("corpus_paper_id")


def arxiv_id(p: dict[str, Any]) -> Any:
    return p.get("_v2_arxiv_id") or p.get("arxiv_id") or p.get("id") or p.get("paper_id")


def load_duplicate_blockers() -> set[str]:
    """
    Block old/dev/current questions so v2 adds new training coverage.
    Handles several schemas.
    """
    paths = [
        DATA / "eval_questions.json",
        V1_DIR / "fresh_questions.json",
        V1_DIR / "fresh_questions_validated.json",
        V1_DIR / "distill_train_questions.json",
        V1_DIR / "gold_eval_questions.json",
        V2_DIR / "train_questions.json",
    ]

    seen: set[str] = set()

    def visit(obj: Any) -> None:
        if isinstance(obj, dict):
            if "questions" in obj:
                visit(obj["questions"])
            for key in ["question", "query", "prompt"]:
                if obj.get(key):
                    seen.add(dup_key(norm_question(obj[key])))
            # Some files may be dicts of records.
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    visit(v)
        elif isinstance(obj, list):
            for x in obj:
                visit(x)
        elif isinstance(obj, str) and obj.strip().endswith("?"):
            seen.add(dup_key(norm_question(obj)))

    for p in paths:
        if not p.exists():
            continue
        try:
            visit(load_json(p))
        except Exception:
            continue

    return {x for x in seen if x}


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

    # fallback: split numbered/bulleted lines
    out = []
    for line in txt.splitlines():
        line = line.strip()
        line = re.sub(r"^[-*]\s*", "", line)
        line = re.sub(r"^\d+[\).\s-]+", "", line).strip()
        if line.endswith("?"):
            out.append(norm_question(line))
    return out


def call_model(
    client: httpx.Client,
    api_key: str,
    model: str,
    title: str,
    abstract: str,
    n: int,
    max_retries: int,
) -> list[str]:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(title=title, abstract=abstract[:5000], n=n)},
        ],
        "temperature": 0.2,
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


def load_existing_raw() -> list[dict[str, Any]]:
    if OUT_RAW.exists():
        data = load_json(OUT_RAW)
        if isinstance(data, list):
            return data
    return []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--safe-papers", type=Path, default=SAFE_PAPERS)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--n-per-paper", type=int, default=3)
    ap.add_argument("--limit-papers", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--max-retries", type=int, default=4)
    args = ap.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Check backend/.env or shell environment.")

    papers = load_json(args.safe_papers)
    if not isinstance(papers, list):
        raise SystemExit(f"{args.safe_papers} must be a JSON list.")

    if args.limit_papers > 0:
        papers = papers[: args.limit_papers]

    existing_raw = load_existing_raw()
    done_pids = {r.get("corpus_paper_id") for r in existing_raw if r.get("status") == "ok"}

    duplicate_blockers = load_duplicate_blockers()
    accepted_questions: list[dict[str, Any]] = []
    raw_results: list[dict[str, Any]] = list(existing_raw)
    seen_questions = set(duplicate_blockers)

    # Keep existing accepted questions if resuming.
    for r in existing_raw:
        if r.get("status") != "ok":
            continue
        for q in r.get("questions", []) or []:
            k = dup_key(q)
            if k and k not in seen_questions:
                seen_questions.add(k)
                accepted_questions.append({
                    "qid": None,  # assigned after full pass
                    "type": "grounded",
                    "source": "distill_arxiv_v2_safe_train",
                    "question": q,
                    "home_paper_id": r.get("corpus_paper_id"),
                    "home_corpus_paper_id": r.get("corpus_paper_id"),
                    "home_arxiv_id": r.get("arxiv_id"),
                    "home_title": r.get("title"),
                    "generation_model": r.get("model"),
                })

    print("\nGenerating v2 train questions")
    print("=" * 64)
    print(f"Safe papers requested:       {len(papers)}")
    print(f"Already completed papers:    {len(done_pids)}")
    print(f"Duplicate blockers loaded:   {len(duplicate_blockers)}")
    print(f"Model:                       {args.model}")
    print(f"Questions per paper:         {args.n_per_paper}")

    with httpx.Client() as client:
        for i, p in enumerate(papers, start=1):
            pid = corpus_id(p)
            if pid in done_pids:
                continue

            title = paper_title(p)
            abstract = paper_abstract(p)

            if not title or not abstract:
                rec = {
                    "corpus_paper_id": pid,
                    "arxiv_id": arxiv_id(p),
                    "title": title,
                    "model": args.model,
                    "status": "skipped_missing_title_or_abstract",
                    "questions": [],
                }
                raw_results.append(rec)
                save_json(OUT_RAW, raw_results)
                continue

            try:
                qs = call_model(
                    client=client,
                    api_key=api_key,
                    model=args.model,
                    title=title,
                    abstract=abstract,
                    n=args.n_per_paper,
                    max_retries=args.max_retries,
                )
                status = "ok"
                error = None
            except Exception as e:
                qs = []
                status = "api_error"
                error = str(e)[:500]

            clean_qs = []
            for q in qs:
                q = norm_question(q)
                if not q or not q.endswith("?"):
                    continue
                k = dup_key(q)
                if k in seen_questions:
                    continue
                seen_questions.add(k)
                clean_qs.append(q)
                accepted_questions.append({
                    "qid": None,
                    "type": "grounded",
                    "source": "distill_arxiv_v2_safe_train",
                    "question": q,
                    "home_paper_id": pid,
                    "home_corpus_paper_id": pid,
                    "home_arxiv_id": arxiv_id(p),
                    "home_title": title,
                    "generation_model": args.model,
                })

            rec = {
                "corpus_paper_id": pid,
                "arxiv_id": arxiv_id(p),
                "title": title,
                "model": args.model,
                "status": status,
                "error": error,
                "questions_raw": qs,
                "questions": clean_qs,
            }
            raw_results.append(rec)
            save_json(OUT_RAW, raw_results)

            print(f"  [{i}/{len(papers)}] pid={pid} kept={len(clean_qs)} status={status}")
            time.sleep(args.sleep)

    # Assign stable qids for v2.
    for idx, q in enumerate(accepted_questions, start=1):
        q["qid"] = idx
        q["id"] = idx

    report = {
        "input_safe_papers": str(args.safe_papers),
        "model": args.model,
        "n_per_paper": args.n_per_paper,
        "safe_papers_requested": len(papers),
        "raw_records": len(raw_results),
        "questions_total": len(accepted_questions),
        "raw_output": str(OUT_RAW),
        "final_output": str(OUT_FINAL),
        "duplicate_blockers_loaded": len(duplicate_blockers),
        "status_counts": {},
    }

    status_counts = {}
    for r in raw_results:
        status_counts[r.get("status", "unknown")] = status_counts.get(r.get("status", "unknown"), 0) + 1
    report["status_counts"] = status_counts

    save_json(OUT_FINAL, accepted_questions)
    save_json(OUT_REPORT, report)

    print("\nDone.")
    print(f"Questions written: {len(accepted_questions)}")
    print(f"Wrote raw:          {OUT_RAW}")
    print(f"Wrote final:        {OUT_FINAL}")
    print(f"Wrote report:       {OUT_REPORT}")


if __name__ == "__main__":
    main()
