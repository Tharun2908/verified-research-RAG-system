"""
backend/app/services/merge_arxiv_v2_train_answers.py

Merge v2 grounded and bait train answers into one training-answer file with collision-safe IDs.

Inputs:
  data/distill_arxiv_v2/train_answers_grounded.json
  data/distill_arxiv_v2/train_answers_bait.json

Outputs:
  data/distill_arxiv_v2/train_answers_merged.json
  data/distill_arxiv_v2/train_answers_merge_report.json

Run from backend/:
  python -m app.services.merge_arxiv_v2_train_answers
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


V2_DIR = Path("data") / "distill_arxiv_v2"

GROUNDED_IN = V2_DIR / "train_answers_grounded.json"
BAIT_IN = V2_DIR / "train_answers_bait.json"

OUT_MERGED = V2_DIR / "train_answers_merged.json"
OUT_REPORT = V2_DIR / "train_answers_merge_report.json"


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def normalize_rows(rows: list[dict[str, Any]], source: str, start_id: int) -> list[dict[str, Any]]:
    out = []

    for offset, row in enumerate(rows, start=0):
        global_id = start_id + offset

        r = dict(row)
        r["train_row_id"] = global_id
        r["global_qid"] = global_id
        r["train_source"] = source
        r["original_id"] = row.get("id")
        r["original_qid"] = row.get("qid")
        r["id"] = global_id
        r["qid"] = global_id

        if source == "grounded":
            r["type"] = "grounded"
        elif source == "bait":
            r["type"] = "bait"

        out.append(r)

    return out


def main() -> None:
    grounded = load_json(GROUNDED_IN)
    bait = load_json(BAIT_IN)

    if not isinstance(grounded, list):
        raise SystemExit(f"{GROUNDED_IN} must be a JSON list.")
    if not isinstance(bait, list):
        raise SystemExit(f"{BAIT_IN} must be a JSON list.")

    merged = []
    merged.extend(normalize_rows(grounded, "grounded", start_id=1))
    merged.extend(normalize_rows(bait, "bait", start_id=len(merged) + 1))

    missing = []
    for r in merged:
        for field in ["question", "evidence", "plain_answer", "cited_answer"]:
            if field not in r:
                missing.append({"train_row_id": r.get("train_row_id"), "missing": field})

    type_counts = Counter(r.get("type", "unknown") for r in merged)
    source_counts = Counter(r.get("train_source", "unknown") for r in merged)

    report = {
        "inputs": {
            "grounded": str(GROUNDED_IN),
            "bait": str(BAIT_IN),
        },
        "outputs": {
            "merged": str(OUT_MERGED),
            "report": str(OUT_REPORT),
        },
        "summary": {
            "grounded_answers": len(grounded),
            "bait_answers": len(bait),
            "merged_answers": len(merged),
            "missing_required_fields": len(missing),
        },
        "type_counts": dict(type_counts),
        "source_counts": dict(source_counts),
        "missing_required_fields_preview": missing[:30],
    }

    save_json(OUT_MERGED, merged)
    save_json(OUT_REPORT, report)

    print("\nMerged v2 train answers")
    print("=" * 56)
    print(f"Grounded answers: {len(grounded)}")
    print(f"Bait answers:     {len(bait)}")
    print(f"Merged answers:   {len(merged)}")
    print(f"Missing fields:   {len(missing)}")
    print(f"Type counts:      {dict(type_counts)}")
    print(f"Wrote:            {OUT_MERGED}")
    print(f"Wrote report:     {OUT_REPORT}")


if __name__ == "__main__":
    main()
