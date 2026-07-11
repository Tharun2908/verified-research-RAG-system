"""
backend/app/services/build_distill_split.py

STEP 3 of arXiv distillation:
Build a leakage-aware question split from retrieval-validated fresh questions.

Input:
  data/distill_arxiv/fresh_questions_validated.json

Outputs:
  data/distill_arxiv/distill_train_questions.json
  data/distill_arxiv/gold_eval_questions.json
  data/distill_arxiv/dropped_questions.json
  data/distill_arxiv/distill_split_summary.json

Method:
  - Keep only retrieval-valid questions:
      keep_grounded, keep_bait
  - Build connected components over:
      question qid + corpus paper ids used as evidence
  - Split by components, not individual questions, so train/gold do not share evidence paper IDs.
  - Uses retrieved_hits up to --max-rank. Set this to the same top-k evidence depth you plan to use
    for generation. Default is 5.

Usage from backend/:
  python -m app.services.build_distill_split --max-rank 5 --gold-frac 0.22
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

DATA = Path("data")
DISTILL_DIR = DATA / "distill_arxiv"
IN_PATH = DISTILL_DIR / "fresh_questions_validated.json"
TRAIN_OUT = DISTILL_DIR / "distill_train_questions.json"
GOLD_OUT = DISTILL_DIR / "gold_eval_questions.json"
DROP_OUT = DISTILL_DIR / "dropped_questions.json"
SUMMARY_OUT = DISTILL_DIR / "distill_split_summary.json"

KEEP_STATUSES = {"keep_grounded", "keep_bait"}


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def evidence_ids_for_question(q: dict[str, Any], max_rank: int) -> set[int]:
    """
    Use the retrieved hit-level resolved corpus IDs up to max_rank.
    Always include home_paper_id for grounded questions, because it is the intended support paper.
    """
    ids: set[int] = set()

    # Add top-ranked retrieved evidence IDs.
    for h in q.get("retrieved_hits", []) or []:
        try:
            rank = int(h.get("rank", 999999))
        except Exception:
            rank = 999999

        if rank > max_rank:
            continue

        pid = h.get("resolved_corpus_paper_id")
        if isinstance(pid, int):
            ids.add(pid)

    # Fallback if no hit-level IDs exist.
    if not ids:
        for pid in q.get("retrieved_corpus_paper_ids", []) or q.get("retrieved_paper_ids", []) or []:
            if isinstance(pid, int):
                ids.add(pid)

    # Always include home paper for grounded questions.
    if q.get("type") == "grounded" and q.get("home_paper_id") is not None:
        try:
            ids.add(int(q["home_paper_id"]))
        except Exception:
            pass

    return ids


class DSU:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: str, b: str) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def build_components(questions: list[dict[str, Any]], max_rank: int) -> list[dict[str, Any]]:
    dsu = DSU()
    qid_to_question: dict[int, dict[str, Any]] = {}
    qid_to_evidence: dict[int, set[int]] = {}

    for q in questions:
        qid = int(q["qid"])
        qid_to_question[qid] = q
        q_node = f"q:{qid}"
        dsu.find(q_node)

        evidence_ids = evidence_ids_for_question(q, max_rank=max_rank)
        qid_to_evidence[qid] = evidence_ids

        for pid in evidence_ids:
            p_node = f"p:{pid}"
            dsu.union(q_node, p_node)

    root_to_qids: dict[str, list[int]] = defaultdict(list)
    root_to_pids: dict[str, set[int]] = defaultdict(set)

    for qid, q in qid_to_question.items():
        root = dsu.find(f"q:{qid}")
        root_to_qids[root].append(qid)
        root_to_pids[root].update(qid_to_evidence[qid])

    comps: list[dict[str, Any]] = []
    for root, qids in root_to_qids.items():
        comp_questions = [qid_to_question[qid] for qid in sorted(qids)]
        type_counts = Counter(q.get("type") for q in comp_questions)
        comps.append(
            {
                "component_id": len(comps),
                "root": root,
                "qids": sorted(qids),
                "paper_ids": sorted(root_to_pids[root]),
                "n_questions": len(qids),
                "n_papers": len(root_to_pids[root]),
                "type_counts": dict(type_counts),
                "questions": comp_questions,
            }
        )

    comps.sort(key=lambda c: (-c["n_questions"], -c["n_papers"], c["component_id"]))
    for i, c in enumerate(comps):
        c["component_id"] = i
    return comps


def split_components(
    comps: list[dict[str, Any]],
    gold_frac: float,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Greedy component split.

    Objective:
      - target gold question count ~= gold_frac
      - preserve bait ratio reasonably
      - never split a component
    """
    rng = random.Random(seed)

    total_q = sum(c["n_questions"] for c in comps)
    target_gold = round(total_q * gold_frac)

    # Shuffle same-size components for deterministic but non-pathological assignment.
    shuffled = list(comps)
    rng.shuffle(shuffled)
    shuffled.sort(key=lambda c: c["n_questions"], reverse=True)

    gold_comps: list[dict[str, Any]] = []
    train_comps: list[dict[str, Any]] = []
    gold_n = 0

    for c in shuffled:
        # If a component alone would overshoot too much and gold already has some content,
        # put it into train. Otherwise put components into gold until target is reached.
        if gold_n < target_gold:
            gold_comps.append(c)
            gold_n += c["n_questions"]
        else:
            train_comps.append(c)

    # If a giant component caused gold to be huge, swap strategy:
    # largest component to train, then fill gold from smaller components.
    if gold_n > target_gold * 1.8 and len(comps) > 1:
        largest = max(comps, key=lambda c: c["n_questions"])
        remaining = [c for c in comps if c is not largest]
        rng.shuffle(remaining)
        remaining.sort(key=lambda c: c["n_questions"], reverse=True)

        train_comps = [largest]
        gold_comps = []
        gold_n = 0
        for c in remaining:
            if gold_n < target_gold:
                gold_comps.append(c)
                gold_n += c["n_questions"]
            else:
                train_comps.append(c)

    return train_comps, gold_comps


def flatten_components(comps: list[dict[str, Any]], split_name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for c in comps:
        for q in c["questions"]:
            row = dict(q)
            row["distill_split"] = split_name
            row["component_id"] = c["component_id"]
            row["component_paper_ids"] = c["paper_ids"]
            rows.append(row)
    rows.sort(key=lambda r: int(r["qid"]))
    return rows


def summarize_questions(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "n": len(rows),
        "type_counts": dict(Counter(r.get("type") for r in rows)),
        "status_counts": dict(Counter(r.get("validation_status") for r in rows)),
        "unique_retrieved_corpus_paper_ids": len(
            {
                pid
                for r in rows
                for pid in r.get("component_paper_ids", [])
                if isinstance(pid, int)
            }
        ),
    }


def overlap(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> dict[str, Any]:
    a_qids = {int(r["qid"]) for r in a}
    b_qids = {int(r["qid"]) for r in b}
    a_pids = {pid for r in a for pid in r.get("component_paper_ids", []) if isinstance(pid, int)}
    b_pids = {pid for r in b for pid in r.get("component_paper_ids", []) if isinstance(pid, int)}
    return {
        "qid_overlap": sorted(a_qids & b_qids),
        "paper_id_overlap": sorted(a_pids & b_pids),
        "n_qid_overlap": len(a_qids & b_qids),
        "n_paper_id_overlap": len(a_pids & b_pids),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-rank", type=int, default=5, help="Use retrieved hits up to this rank for grouping")
    ap.add_argument("--gold-frac", type=float, default=0.22)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    if not IN_PATH.exists():
        raise SystemExit(f"Missing input: {IN_PATH}")

    all_rows = load_json(IN_PATH)
    if not isinstance(all_rows, list):
        raise SystemExit(f"{IN_PATH} must be a list")

    usable = [r for r in all_rows if r.get("validation_status") in KEEP_STATUSES]
    dropped = [r for r in all_rows if r.get("validation_status") not in KEEP_STATUSES]

    comps = build_components(usable, max_rank=args.max_rank)
    train_comps, gold_comps = split_components(comps, gold_frac=args.gold_frac, seed=args.seed)

    train_rows = flatten_components(train_comps, "distill_train")
    gold_rows = flatten_components(gold_comps, "gold_eval")

    split_overlap = overlap(train_rows, gold_rows)

    summary = {
        "input_path": str(IN_PATH),
        "max_rank_for_grouping": args.max_rank,
        "gold_frac_requested": args.gold_frac,
        "seed": args.seed,
        "total_input": len(all_rows),
        "usable": len(usable),
        "dropped": len(dropped),
        "component_count": len(comps),
        "largest_components": [
            {
                "component_id": c["component_id"],
                "n_questions": c["n_questions"],
                "n_papers": c["n_papers"],
                "type_counts": c["type_counts"],
                "sample_qids": c["qids"][:10],
                "sample_paper_ids": c["paper_ids"][:20],
            }
            for c in comps[:10]
        ],
        "train": summarize_questions(train_rows),
        "gold": summarize_questions(gold_rows),
        "overlap_check": split_overlap,
    }

    save_json(TRAIN_OUT, train_rows)
    save_json(GOLD_OUT, gold_rows)
    save_json(DROP_OUT, dropped)
    save_json(SUMMARY_OUT, summary)

    print("Done.")
    print(json.dumps(summary, indent=2)[:6000])
    print(f"\nWrote train: {TRAIN_OUT}")
    print(f"Wrote gold:  {GOLD_OUT}")
    print(f"Wrote drop:  {DROP_OUT}")
    print(f"Wrote summary: {SUMMARY_OUT}")

    if split_overlap["n_qid_overlap"] != 0 or split_overlap["n_paper_id_overlap"] != 0:
        raise SystemExit("ERROR: split leakage detected. See overlap_check in summary.")


if __name__ == "__main__":
    main()
