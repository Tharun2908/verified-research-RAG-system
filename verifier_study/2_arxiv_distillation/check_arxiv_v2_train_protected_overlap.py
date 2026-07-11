"""
backend/app/services/check_arxiv_v2_train_protected_overlap.py

Strict leakage check for Option-B arXiv v2 train claims.

Checks:
  - every claim in data/distill_arxiv_v2/train_claims.json
  - every evidence paper attached to the claim:
      * claim["evidence"]
      * claim["all_evidence"]
  - against all protected gold-evidence papers:
      data/distill_arxiv_v2/protected_gold_evidence_papers.json

Expected:
  protected overlap claims = 0

Outputs:
  data/distill_arxiv_v2/train_protected_evidence_overlap_report.json
  data/distill_arxiv_v2/train_claims_no_protected_overlap.json

Run from backend/:
  python -m app.services.check_arxiv_v2_train_protected_overlap
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


V2_DIR = Path("data") / "distill_arxiv_v2"

CLAIMS_IN = V2_DIR / "train_claims.json"
PROTECTED_IN = V2_DIR / "protected_gold_evidence_papers.json"

REPORT_OUT = V2_DIR / "train_protected_evidence_overlap_report.json"
CLEAN_OUT = V2_DIR / "train_claims_no_protected_overlap.json"


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_title(x: Any) -> str:
    return " ".join(str(x or "").lower().strip().split())


def get_pid(obj: dict[str, Any]) -> int | None:
    for k in ["resolved_corpus_paper_id", "corpus_paper_id", "paper_id", "home_corpus_paper_id", "home_paper_id"]:
        if obj.get(k) is not None and str(obj.get(k)).strip() != "":
            try:
                return int(obj[k])
            except Exception:
                pass
    return None


def get_title(obj: dict[str, Any]) -> str:
    for k in ["title", "paper_title", "_v2_title", "home_title"]:
        if obj.get(k):
            return str(obj[k]).strip()
    return ""


def protected_sets(rows: list[dict[str, Any]]) -> tuple[set[int], set[str], dict[int, dict[str, Any]]]:
    pids: set[int] = set()
    titles: set[str] = set()
    pid_to_row: dict[int, dict[str, Any]] = {}

    for r in rows:
        if not isinstance(r, dict):
            continue
        pid = get_pid(r)
        title = norm_title(get_title(r))
        if pid is not None:
            pids.add(pid)
            pid_to_row[pid] = r
        if title:
            titles.add(title)

    return pids, titles, pid_to_row


def iter_evidence_items(claim: dict[str, Any]):
    """
    Yield evidence items from both selected claim evidence and all attached evidence.
    Dedupe by object pid/chunk/title/source_field.
    """
    seen = set()

    for source_field in ["evidence", "all_evidence"]:
        evs = claim.get(source_field)
        if not isinstance(evs, list):
            continue

        for idx, ev in enumerate(evs):
            if not isinstance(ev, dict):
                continue

            pid = get_pid(ev)
            title = get_title(ev)
            chunk_id = ev.get("chunk_id")
            key = (source_field, pid, norm_title(title), str(chunk_id))
            if key in seen:
                continue
            seen.add(key)

            yield source_field, idx, ev, pid, title


def main() -> None:
    claims = load_json(CLAIMS_IN)
    protected = load_json(PROTECTED_IN)

    if not isinstance(claims, list):
        raise SystemExit(f"{CLAIMS_IN} must be a JSON list.")
    if not isinstance(protected, list):
        raise SystemExit(f"{PROTECTED_IN} must be a JSON list.")

    protected_pids, protected_titles, protected_pid_to_row = protected_sets(protected)

    bad_claim_ids = set()
    bad_rows = []
    clean_claims = []
    missing_pid_evidence = []
    evidence_items_checked = 0

    by_train_source = Counter()
    by_answer_variant = Counter()
    by_overlap_source_field = Counter()
    protected_pid_hits = Counter()
    protected_title_hits = Counter()

    for claim in claims:
        claim_id = claim.get("claim_id")
        claim_has_overlap = False
        overlaps_for_claim = []

        for source_field, idx, ev, pid, title in iter_evidence_items(claim):
            evidence_items_checked += 1
            title_key = norm_title(title)

            if pid is None:
                missing_pid_evidence.append({
                    "claim_id": claim_id,
                    "source_field": source_field,
                    "evidence_index": idx,
                    "title": title,
                    "chunk_id": ev.get("chunk_id"),
                })
                continue

            pid_overlap = pid in protected_pids
            title_overlap = bool(title_key and title_key in protected_titles)

            if pid_overlap or title_overlap:
                claim_has_overlap = True
                bad_claim_ids.add(claim_id)
                by_train_source[claim.get("train_source", "unknown")] += 1
                by_answer_variant[claim.get("answer_variant", "unknown")] += 1
                by_overlap_source_field[source_field] += 1
                if pid_overlap:
                    protected_pid_hits[str(pid)] += 1
                if title_overlap:
                    protected_title_hits[title_key] += 1

                overlaps_for_claim.append({
                    "source_field": source_field,
                    "evidence_index": idx,
                    "pid": pid,
                    "title": title,
                    "chunk_id": ev.get("chunk_id"),
                    "pid_overlap": pid_overlap,
                    "title_overlap": title_overlap,
                })

        if claim_has_overlap:
            bad_rows.append({
                "claim_id": claim_id,
                "train_row_id": claim.get("train_row_id"),
                "qid": claim.get("qid"),
                "train_source": claim.get("train_source"),
                "answer_variant": claim.get("answer_variant"),
                "claim": claim.get("claim") or claim.get("claim_text"),
                "overlaps": overlaps_for_claim,
            })
        else:
            clean_claims.append(claim)

    report = {
        "inputs": {
            "claims": str(CLAIMS_IN),
            "protected": str(PROTECTED_IN),
        },
        "outputs": {
            "report": str(REPORT_OUT),
            "clean_claims": str(CLEAN_OUT),
        },
        "summary": {
            "train_claims": len(claims),
            "protected_gold_evidence_papers": len(protected_pids),
            "evidence_items_checked": evidence_items_checked,
            "claims_with_protected_overlap": len(bad_claim_ids),
            "clean_claims": len(clean_claims),
            "missing_pid_evidence_items": len(missing_pid_evidence),
            "strict_pass": len(bad_claim_ids) == 0,
        },
        "by_train_source": dict(by_train_source),
        "by_answer_variant": dict(by_answer_variant),
        "by_overlap_source_field": dict(by_overlap_source_field),
        "protected_pid_hits_top30": dict(protected_pid_hits.most_common(30)),
        "protected_title_hits_top30": dict(protected_title_hits.most_common(30)),
        "bad_claims_preview": bad_rows[:50],
        "missing_pid_evidence_preview": missing_pid_evidence[:50],
    }

    save_json(REPORT_OUT, report)
    save_json(CLEAN_OUT, clean_claims)

    print("\nStrict v2 train protected-evidence overlap check")
    print("=" * 72)
    print(f"Train claims:                       {len(claims)}")
    print(f"Protected gold evidence papers:      {len(protected_pids)}")
    print(f"Evidence items checked:              {evidence_items_checked}")
    print(f"Claims with protected overlap:        {len(bad_claim_ids)}")
    print(f"Clean claims written:                {len(clean_claims)}")
    print(f"Missing PID evidence items:          {len(missing_pid_evidence)}")
    print(f"STRICT PASS:                         {len(bad_claim_ids) == 0}")
    print("\nWrote:")
    print(f"  {REPORT_OUT}")
    print(f"  {CLEAN_OUT}")

    if bad_rows:
        print("\nFirst overlap preview:")
        print(json.dumps(bad_rows[0], ensure_ascii=False, indent=2)[:2000])

    if missing_pid_evidence:
        print("\nFirst missing-PID evidence preview:")
        print(json.dumps(missing_pid_evidence[0], ensure_ascii=False, indent=2)[:1000])


if __name__ == "__main__":
    main()
