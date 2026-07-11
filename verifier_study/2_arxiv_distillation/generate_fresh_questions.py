"""
backend/app/services/generate_fresh_questions.py

STEP 1 of the arXiv distillation plan:
Generate fresh questions over the existing 250-paper arXiv corpus, disjoint from the old/dev
M8 questions, and provenance-tracked for later leakage-safe grouped splitting.

Outputs:
  data/distill_arxiv/fresh_questions.json

Question types:
  - grounded: generated from one paper's title + abstract, answerable from that abstract
  - bait: plausible out-of-corpus questions, intended to test unsupported-answer behavior

Usage from backend/:
  python -m app.services.generate_fresh_questions --limit 5 --n-bait 0
  python -m app.services.generate_fresh_questions
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


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
DATA = Path("data")
DISTILL_DIR = DATA / "distill_arxiv"

CORPUS = DATA / "arxiv_papers.json"
OLD_QUESTIONS = DATA / "eval_questions.json"

OUT = DISTILL_DIR / "fresh_questions.json"


# ---------------------------------------------------------------------
# OpenRouter config
# ---------------------------------------------------------------------
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Keep this configurable so changing models does not require code edits.
MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-opus-4.8")


# ---------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------
GROUNDED_SYS = (
    "You write precise, claim-eliciting research questions. Given a paper's title and abstract, "
    "produce questions whose answers would contain specific, checkable factual claims about the "
    "paper's findings, methods, comparisons, or results. Avoid vague questions like "
    "'What is this paper about?'. Each question must be answerable using ONLY this abstract."
)

GROUNDED_USER = (
    "TITLE:\n{title}\n\n"
    "ABSTRACT:\n{abstract}\n\n"
    "Generate 2 specific claim-eliciting questions this abstract directly answers.\n\n"
    "Rules:\n"
    "- The questions must be answerable from this abstract alone.\n"
    "- The expected answer should contain factual claims that can later be verified.\n"
    "- Prefer questions about method, result, comparison, limitation, or finding.\n"
    "- Do not ask generic summary questions.\n\n"
    "Respond with ONLY a JSON array, no markdown, no extra text:\n"
    '[{{"question": "...", "rationale": "what claim the answer will contain"}}, '
    '{{"question": "...", "rationale": "what claim the answer will contain"}}]'
)

BAIT_SYS = (
    "You write plausible-sounding research questions on topics outside a given corpus. "
    "The purpose is to test whether a retrieval system correctly finds no strong evidence. "
    "The questions should sound like real research questions but should be deliberately "
    "out-of-distribution for a corpus of recent NLP, IR, LLM, recommendation, and ML-systems papers."
)

BAIT_USER = (
    "The corpus covers recent NLP / information-retrieval / LLM / recommendation / ML-systems "
    "papers from roughly 2025-2026.\n\n"
    "Generate {n} plausible research questions that are almost certainly NOT answerable by such "
    "a corpus. Good bait topics include classical pre-2000 algorithms, chemistry, astronomy, "
    "genomics, chip fabrication, networking minutiae, or unrelated scientific domains.\n\n"
    "Rules:\n"
    "- The questions should sound credible.\n"
    "- They should not be silly or obviously impossible.\n"
    "- They should be out-of-domain for the described corpus.\n\n"
    "Respond with ONLY a JSON array of strings, no markdown, no extra text:\n"
    '["question 1", "question 2", "..."]'
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def norm_text(s: str) -> str:
    """Normalize question text for exact-ish duplicate detection."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_json_block(txt: str) -> Any | None:
    """
    Parse a JSON array from model output.

    Handles:
      - pure JSON array
      - fenced ```json blocks
      - extra accidental text around the array
    """
    txt = txt.strip()

    # Remove fenced code block if present.
    fence_match = re.search(r"```(?:json)?\s*(.*?)```", txt, flags=re.DOTALL | re.IGNORECASE)
    if fence_match:
        txt = fence_match.group(1).strip()

    # Try direct JSON first.
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        pass

    # Fallback: extract first [...] block.
    start = txt.find("[")
    end = txt.rfind("]")
    if start != -1 and end != -1 and end > start:
        candidate = txt[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None

    return None


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_done() -> list[dict[str, Any]]:
    if OUT.exists():
        data = load_json(OUT)
        if isinstance(data, list):
            return data
    return []


def load_old_question_texts() -> set[str]:
    """
    Load old/dev questions so the fresh batch does not exactly duplicate them.

    Handles:
      - list of dicts
      - list of strings
      - dict with nested question lists
      - fields named question/query/text
    """
    if not OLD_QUESTIONS.exists():
        return set()

    data = load_json(OLD_QUESTIONS)
    old: set[str] = set()

    def visit(obj):
        if isinstance(obj, dict):
            for key in ("question", "query", "text"):
                val = obj.get(key)
                if isinstance(val, str) and val.strip():
                    old.add(norm_text(val))
            for v in obj.values():
                visit(v)

        elif isinstance(obj, list):
            for item in obj:
                visit(item)

        elif isinstance(obj, str):
            if obj.strip().endswith("?"):
                old.add(norm_text(obj))

    visit(data)
    return old


def next_qid(existing: list[dict[str, Any]]) -> int:
    max_qid = 0
    for r in existing:
        try:
            max_qid = max(max_qid, int(r.get("qid", 0)))
        except Exception:
            continue
    return max_qid


def call_opus(
    client: httpx.Client,
    api_key: str,
    system: str,
    user: str,
    max_retries: int = 4,
) -> str:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
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
            r = client.post(
                OPENROUTER_URL,
                json=body,
                headers=headers,
                timeout=90,
            )

            if r.status_code == 429:
                print(f"  rate limited; sleeping {delay:.1f}s")
                time.sleep(delay)
                delay *= 2
                continue

            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()

        except Exception:
            if attempt == max_retries - 1:
                raise

            print(f"  request failed; retrying in {delay:.1f}s")
            time.sleep(delay)
            delay *= 2

    raise RuntimeError("retries exhausted")


def extract_question_item(item: Any) -> tuple[str, str]:
    """
    Return (question, rationale) from either:
      {"question": "...", "rationale": "..."}
      or string.
    """
    if isinstance(item, dict):
        q = str(item.get("question", "")).strip()
        rationale = str(item.get("rationale", "")).strip()
        return q, rationale

    q = str(item).strip()
    return q, ""


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="0=all papers; >0=first N papers for smoke test")
    ap.add_argument("--n-bait", type=int, default=50)
    ap.add_argument("--bait-only", action="store_true", help="only generate missing bait questions")
    ap.add_argument("--sleep", type=float, default=0.3)
    args = ap.parse_args()

    DISTILL_DIR.mkdir(parents=True, exist_ok=True)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Add it to .env or environment variables.")

    if not CORPUS.exists():
        raise SystemExit(f"Missing corpus file: {CORPUS}")

    papers = load_json(CORPUS)
    if not isinstance(papers, list):
        raise SystemExit(f"{CORPUS} must be a JSON list.")

    if args.limit > 0:
        papers = papers[: args.limit]

    existing = load_done()
    results = list(existing)

    old_questions = load_old_question_texts()

    done_papers = {
        int(r["home_paper_id"])
        for r in existing
        if r.get("type") == "grounded" and r.get("home_paper_id") is not None
    }

    seen_questions = set(old_questions)
    for r in existing:
        q = str(r.get("question", "")).strip()
        if q:
            seen_questions.add(norm_text(q))

    qid = next_qid(existing)

    print(f"Model: {MODEL}")
    print(f"Corpus papers loaded: {len(papers)}")
    print(f"Old/dev questions loaded for duplicate blocking: {len(old_questions)}")
    print(f"Existing fresh questions loaded: {len(existing)}")
    print(f"Generating grounded questions for {len(papers)} papers ({len(done_papers)} already done).")
    print(f"Output: {OUT}")
    if args.bait_only:
          papers = []
          print("Bait-only mode: skipping grounded question generation.")

    with httpx.Client() as client:
        # -------------------------------------------------------------
        # Grounded questions
        # -------------------------------------------------------------
        for i, p in enumerate(papers):
            if i in done_papers:
                continue

            if not isinstance(p, dict):
                print(f"  [paper {i}] invalid paper record, skipping")
                continue

            title = str(p.get("title", "")).strip()
            abstract = str(p.get("abstract", "")).strip()

            if not title or not abstract:
                print(f"  [paper {i}] missing title/abstract, skipping")
                continue

            try:
                raw = call_opus(
                    client=client,
                    api_key=api_key,
                    system=GROUNDED_SYS,
                    user=GROUNDED_USER.format(title=title, abstract=abstract),
                )

                qs = parse_json_block(raw)
                if not isinstance(qs, list):
                    print(f"  [paper {i}] parse fail, skipping")
                    continue

                added_for_paper = 0

                for item in qs:
                    q, rationale = extract_question_item(item)
                    if not q:
                        continue

                    q_norm = norm_text(q)
                    if not q_norm:
                        continue

                    if q_norm in seen_questions:
                        print(f"  [paper {i}] skipped duplicate/old question: {q[:90]}")
                        continue

                    qid += 1
                    seen_questions.add(q_norm)

                    results.append(
                        {
                            "qid": qid,
                            "question": q,
                            "type": "grounded",
                            "home_paper_id": i,
                            "source_title": title,
                            "gen_rationale": rationale,
                            "source": "generated_from_arxiv_abstract",
                        }
                    )
                    added_for_paper += 1

                if added_for_paper == 0:
                    print(f"  [paper {i}] no usable new questions added")

            except Exception as e:
                print(f"  [paper {i}] FAILED: {e}")
                continue

            save_json(OUT, results)

            if (i + 1) % 20 == 0:
                grounded_now = sum(1 for r in results if r.get("type") == "grounded")
                print(f"  {i + 1}/{len(papers)} papers processed, grounded questions so far: {grounded_now}")

            time.sleep(args.sleep)

        # -------------------------------------------------------------
        # Bait questions
        # -------------------------------------------------------------
        have_bait = sum(1 for r in results if r.get("type") == "bait")
        missing_bait = args.n_bait - have_bait

        # Do not generate bait during paper-limited smoke tests unless explicitly needed.
        if missing_bait > 0 and args.limit == 0:
            print(f"\nGenerating {missing_bait} bait questions...")

            try:
                raw = call_opus(
                    client=client,
                    api_key=api_key,
                    system=BAIT_SYS,
                    user=BAIT_USER.format(n=missing_bait),
                )

                baits = parse_json_block(raw)
                if not isinstance(baits, list):
                    print("  bait generation parse fail")
                else:
                    added_bait = 0

                    for item in baits:
                        q = str(item).strip()
                        if not q:
                            continue

                        q_norm = norm_text(q)
                        if not q_norm:
                            continue

                        if q_norm in seen_questions:
                            print(f"  skipped duplicate bait: {q[:90]}")
                            continue

                        qid += 1
                        seen_questions.add(q_norm)

                        results.append(
                            {
                                "qid": qid,
                                "question": q,
                                "type": "bait",
                                "home_paper_id": None,
                                "source_title": None,
                                "gen_rationale": "out-of-distribution bait",
                                "source": "generated_bait_out_of_corpus",
                            }
                        )
                        added_bait += 1

                    print(f"  added bait questions: {added_bait}")
                    save_json(OUT, results)

            except Exception as e:
                print(f"  bait generation FAILED: {e}")

    grounded = sum(1 for r in results if r.get("type") == "grounded")
    bait = sum(1 for r in results if r.get("type") == "bait")

    print("\nDone.")
    print(f"Total questions: {len(results)}")
    print(f"  grounded: {grounded}")
    print(f"  bait:     {bait}")
    print(f"Wrote: {OUT}")
    print("\nNext step: retrieval-validate these questions and attach retrieved paper/evidence IDs.")


if __name__ == "__main__":
    main()