"""
backend/app/services/build_arxiv_v2_safe_papers.py

Option B repair:
  Protect the current gold set and build a new TRAIN source pool from papers that do not
  appear in gold evidence.

Inputs:
  data/arxiv_papers.json
  data/distill_arxiv/gold_eval_claims.json

Outputs:
  data/distill_arxiv_v2/protected_gold_evidence_papers.json
  data/distill_arxiv_v2/safe_train_source_papers.json
  data/distill_arxiv_v2/safe_train_source_paper_ids.json
  data/distill_arxiv_v2/safe_paper_report.json

Run from backend/:
  python -m app.services.build_arxiv_v2_safe_papers
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DATA = Path("data")
V1_DIR = DATA / "distill_arxiv"
V2_DIR = DATA / "distill_arxiv_v2"

DEFAULT_CORPUS = DATA / "arxiv_papers.json"
DEFAULT_GOLD_CLAIMS = V1_DIR / "gold_eval_claims.json"


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_title(x: Any) -> str:
    return " ".join(str(x or "").lower().strip().split())


def paper_title(p: dict[str, Any]) -> str:
    return str(p.get("title") or p.get("paper_title") or p.get("name") or "").strip()


def paper_abstract(p: dict[str, Any]) -> str:
    return str(p.get("abstract") or p.get("summary") or p.get("text") or p.get("description") or "").strip()


def paper_arxiv_id(p: dict[str, Any]) -> str | None:
    for k in ["arxiv_id", "id", "paper_id", "entry_id"]:
        if p.get(k) is not None:
            return str(p[k])
    return None


def evidence_pids_and_titles(gold_claims: list[dict[str, Any]]) -> tuple[set[int], set[str], Counter[str]]:
    pids: set[int] = set()
    titles: set[str] = set()
    evidence_key_counts: Counter[str] = Counter()

    for r in gold_claims:
        evidence = r.get("evidence", [])
        if not isinstance(evidence, list):
            continue

        for ev in evidence:
            if not isinstance(ev, dict):
                continue

            pid = (
                ev.get("resolved_corpus_paper_id")
                if ev.get("resolved_corpus_paper_id") is not None
                else ev.get("corpus_paper_id")
                if ev.get("corpus_paper_id") is not None
                else ev.get("paper_id")
            )

            if pid is not None and str(pid).strip() != "":
                try:
                    pid_int = int(pid)
                    pids.add(pid_int)
                    evidence_key_counts[f"pid:{pid_int}"] += 1
                    continue
                except ValueError:
                    pass

            title = norm_title(ev.get("title"))
            if title:
                titles.add(title)
                evidence_key_counts[f"title:{title}"] += 1

    return pids, titles, evidence_key_counts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    ap.add_argument("--gold-claims", type=Path, default=DEFAULT_GOLD_CLAIMS)
    ap.add_argument("--out-dir", type=Path, default=V2_DIR)
    args = ap.parse_args()

    papers = load_json(args.corpus)
    gold_claims = load_json(args.gold_claims)

    if isinstance(papers, dict) and "papers" in papers:
        papers = papers["papers"]

    if not isinstance(papers, list):
        raise SystemExit(f"{args.corpus} must be a JSON list or a dict with a 'papers' list.")
    if not isinstance(gold_claims, list):
        raise SystemExit(f"{args.gold_claims} must be a JSON list.")

    title_to_pid: dict[str, int] = {}
    for i, p in enumerate(papers):
        if not isinstance(p, dict):
            continue
        title = norm_title(paper_title(p))
        if title:
            title_to_pid[title] = i

    protected_pids, protected_titles, evidence_key_counts = evidence_pids_and_titles(gold_claims)

    title_resolved = 0
    unresolved_titles = []
    for t in protected_titles:
        if t in title_to_pid:
            protected_pids.add(title_to_pid[t])
            title_resolved += 1
        else:
            unresolved_titles.append(t)

    protected_rows = []
    safe_rows = []

    for i, p in enumerate(papers):
        if not isinstance(p, dict):
            continue

        row = dict(p)
        row["corpus_paper_id"] = i
        row["_v2_title"] = paper_title(p)
        row["_v2_abstract"] = paper_abstract(p)
        row["_v2_arxiv_id"] = paper_arxiv_id(p)

        if i in protected_pids:
            protected_rows.append(row)
        else:
            safe_rows.append(row)

    safe_ids = [r["corpus_paper_id"] for r in safe_rows]

    report = {
        "inputs": {
            "corpus": str(args.corpus),
            "gold_claims": str(args.gold_claims),
        },
        "outputs": {
            "protected_gold_evidence_papers": str(args.out_dir / "protected_gold_evidence_papers.json"),
            "safe_train_source_papers": str(args.out_dir / "safe_train_source_papers.json"),
            "safe_train_source_paper_ids": str(args.out_dir / "safe_train_source_paper_ids.json"),
            "report": str(args.out_dir / "safe_paper_report.json"),
        },
        "summary": {
            "corpus_papers": len(papers),
            "gold_claims": len(gold_claims),
            "protected_gold_evidence_paper_ids": len(protected_pids),
            "protected_rows_written": len(protected_rows),
            "safe_train_source_papers": len(safe_rows),
            "title_only_protected_evidence_keys": len(protected_titles),
            "title_only_keys_resolved_to_ids": title_resolved,
            "unresolved_title_only_keys": len(unresolved_titles),
        },
        "protected_paper_ids": sorted(protected_pids),
        "safe_paper_ids": safe_ids,
        "top_gold_evidence_keys_by_claim_frequency": dict(evidence_key_counts.most_common(30)),
        "unresolved_title_only_keys_preview": unresolved_titles[:30],
    }

    out_protected = args.out_dir / "protected_gold_evidence_papers.json"
    out_safe = args.out_dir / "safe_train_source_papers.json"
    out_safe_ids = args.out_dir / "safe_train_source_paper_ids.json"
    out_report = args.out_dir / "safe_paper_report.json"

    save_json(out_protected, protected_rows)
    save_json(out_safe, safe_rows)
    save_json(out_safe_ids, safe_ids)
    save_json(out_report, report)

    print("\nOption B: protected gold evidence papers")
    print("=" * 64)
    print(f"Corpus papers:                  {len(papers)}")
    print(f"Gold claims:                    {len(gold_claims)}")
    print(f"Protected gold evidence papers: {len(protected_pids)}")
    print(f"Safe train-source papers:       {len(safe_rows)}")
    print(f"Title-only keys unresolved:     {len(unresolved_titles)}")
    print("\nWrote:")
    print(f"  {out_protected}")
    print(f"  {out_safe}")
    print(f"  {out_safe_ids}")
    print(f"  {out_report}")

    if not safe_rows:
        raise SystemExit("No safe train-source papers remain. Need a different gold split.")
    if unresolved_titles:
        print("\nWARNING: some title-only evidence keys were not resolved. Inspect the report.")


if __name__ == "__main__":
    main()
