"""
backend/app/services/build_blind50_teacher_audit.py

Build a blind human-audit sample from the gold teacher-drafted claims.

Purpose:
  Check whether the cheap teacher/drafter labels are trustworthy before using them.
  The review file hides teacher labels and rationales. A separate key file keeps them
  for later agreement analysis.

Default input:
  data/distill_arxiv/gold_eval_teacher_drafted.json

Default outputs:
  data/distill_arxiv/gold_blind50_review.json
  data/distill_arxiv/gold_blind50_review.md
  data/distill_arxiv/gold_blind50_teacher_key.json
  data/distill_arxiv/gold_blind50_manifest.json

After manual review:
  Fill human_label in gold_blind50_review.json with:
    SUPPORTED / UNSUPPORTED / ABSTENTION

Then compare:
  python -m app.services.build_blind50_teacher_audit --compare data/distill_arxiv/gold_blind50_review.json

Run from backend/:
  python -m app.services.build_blind50_teacher_audit
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DISTILL_DIR = Path("data") / "distill_arxiv"

DEFAULT_IN = DISTILL_DIR / "gold_eval_teacher_drafted.json"
DEFAULT_REVIEW_JSON = DISTILL_DIR / "gold_blind50_review.json"
DEFAULT_REVIEW_MD = DISTILL_DIR / "gold_blind50_review.md"
DEFAULT_KEY = DISTILL_DIR / "gold_blind50_teacher_key.json"
DEFAULT_MANIFEST = DISTILL_DIR / "gold_blind50_manifest.json"

VALID = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}


GUIDELINES = """# Blind-50 Gold Label Audit

You are labeling claims against evidence. Do not look at `gold_blind50_teacher_key.json` while reviewing.

Use exactly one of:

- `SUPPORTED`: every factual assertion in the claim is directly supported by, or clearly inferable from, the evidence.
- `UNSUPPORTED`: the claim adds details, numbers, method names, comparisons, causal claims, or scope that the evidence does not support.
- `ABSTENTION`: the claim is not a substantive factual answer; it says the sources/evidence do not contain or discuss the answer, or it refuses due to insufficient evidence.

Judge only against the evidence shown here. Do not use outside knowledge.
"""


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def claim_id(r: dict[str, Any]) -> str:
    if r.get("claim_id"):
        return str(r["claim_id"])
    split = r.get("split", "gold_eval")
    qid = r.get("qid", "q")
    variant = r.get("answer_variant", "answer")
    idx = r.get("claim_index", 0)
    return f"{split}_q{qid}_{variant}_c{idx}"


def teacher_label(r: dict[str, Any]) -> str:
    return str(r.get("teacher_label") or r.get("draft_label") or "MISSING").upper().strip()


def question_type(r: dict[str, Any]) -> str:
    return str(r.get("question_type") or r.get("type") or "unknown")


def answer_variant(r: dict[str, Any]) -> str:
    return str(r.get("answer_variant") or "unknown")


def evidence_text(r: dict[str, Any]) -> str:
    txt = str(r.get("evidence_text_for_verifier") or r.get("evidence_text") or "").strip()
    if txt:
        return txt

    parts = []
    for ev in r.get("evidence", []) or []:
        if isinstance(ev, dict):
            n = ev.get("number", "?")
            title = ev.get("title", "")
            text = ev.get("text", "")
            parts.append(f"[{n}] {title}\n{text}".strip())
    return "\n\n".join(p for p in parts if p).strip()


def claim_text(r: dict[str, Any]) -> str:
    return str(r.get("claim") or r.get("claim_text") or "").strip()


def stratified_sample(rows: list[dict[str, Any]], n: int, seed: int) -> list[dict[str, Any]]:
    """
    Stratify primarily by teacher label so the audit actually probes rare unsupported cases,
    then round-robin within each label across question_type x answer_variant buckets.

    The selected review file does NOT expose teacher labels.
    """
    rng = random.Random(seed)

    by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        lab = teacher_label(r)
        if lab in VALID:
            by_label[lab].append(r)

    # Default quota for n=50: enough supported to detect leniency, enough unsupported to
    # test positive-class correctness, enough abstentions to check refusal handling.
    if n == 50:
        quotas = {"SUPPORTED": 25, "UNSUPPORTED": 15, "ABSTENTION": 10}
    else:
        quotas = {
            "SUPPORTED": round(n * 0.50),
            "UNSUPPORTED": round(n * 0.30),
            "ABSTENTION": n - round(n * 0.50) - round(n * 0.30),
        }

    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()

    def pick_from_label(label: str, target: int) -> None:
        candidates = list(by_label.get(label, []))
        rng.shuffle(candidates)

        buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for r in candidates:
            buckets[(question_type(r), answer_variant(r))].append(r)

        bucket_keys = list(buckets.keys())
        rng.shuffle(bucket_keys)

        # Round-robin over buckets to avoid only one question type or answer variant.
        while len([x for x in selected if teacher_label(x) == label]) < target:
            progressed = False
            for bk in bucket_keys:
                if len([x for x in selected if teacher_label(x) == label]) >= target:
                    break
                if buckets[bk]:
                    r = buckets[bk].pop()
                    cid = claim_id(r)
                    if cid not in selected_ids:
                        selected.append(r)
                        selected_ids.add(cid)
                        progressed = True
            if not progressed:
                break

    # First pass with quotas.
    for lab in ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"]:
        pick_from_label(lab, min(quotas.get(lab, 0), len(by_label.get(lab, []))))

    # Fill any remainder from all unsampled valid rows.
    if len(selected) < n:
        rest = [r for r in rows if teacher_label(r) in VALID and claim_id(r) not in selected_ids]
        rng.shuffle(rest)
        for r in rest:
            if len(selected) >= n:
                break
            selected.append(r)
            selected_ids.add(claim_id(r))

    # Stable review order: shuffle so teacher-label quota order is hidden.
    rng.shuffle(selected)
    return selected[:n]


def make_review_record(i: int, r: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": f"B50-{i:03d}",
        "claim_id": claim_id(r),
        "qid": r.get("qid"),
        "question_type": question_type(r),
        "answer_variant": answer_variant(r),
        "evidence_scope": r.get("evidence_scope"),
        "question": r.get("question"),
        "claim": claim_text(r),
        "evidence_text": evidence_text(r),
        "human_label": None,
        "human_notes": "",
    }


def make_key_record(review: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review["review_id"],
        "claim_id": review["claim_id"],
        "teacher_provider": source.get("teacher_provider"),
        "teacher_model": source.get("teacher_model"),
        "teacher_label": teacher_label(source),
        "teacher_rationale": source.get("teacher_rationale") or source.get("draft_rationale") or "",
    }


def write_markdown(path: Path, review_rows: list[dict[str, Any]]) -> None:
    lines = [GUIDELINES.strip(), ""]
    for r in review_rows:
        lines.append("---")
        lines.append("")
        lines.append(f"## {r['review_id']} — {r['claim_id']}")
        lines.append("")
        lines.append(f"**Question type:** {r['question_type']}")
        lines.append(f"**Answer variant:** {r['answer_variant']}")
        lines.append(f"**Evidence scope:** {r.get('evidence_scope')}")
        lines.append("")
        lines.append("**Question**")
        lines.append("")
        lines.append(str(r.get("question") or "").strip())
        lines.append("")
        lines.append("**Claim**")
        lines.append("")
        lines.append(str(r.get("claim") or "").strip())
        lines.append("")
        lines.append("**Evidence**")
        lines.append("")
        lines.append("```text")
        lines.append(str(r.get("evidence_text") or "").strip())
        lines.append("```")
        lines.append("")
        lines.append("**Human label:** ")
        lines.append("")
        lines.append("**Notes:** ")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build(args: argparse.Namespace) -> None:
    rows = load_json(args.input)
    if not isinstance(rows, list):
        raise SystemExit("Input must be a JSON list.")

    selected = stratified_sample(rows, n=args.n, seed=args.seed)

    review_rows = [make_review_record(i, r) for i, r in enumerate(selected, start=1)]
    key_rows = [make_key_record(review, source) for review, source in zip(review_rows, selected)]

    manifest = {
        "input": str(args.input),
        "n_requested": args.n,
        "n_selected": len(review_rows),
        "seed": args.seed,
        "review_json": str(args.review_json),
        "review_md": str(args.review_md),
        "teacher_key": str(args.key),
        "teacher_label_counts_in_hidden_sample": dict(Counter(k["teacher_label"] for k in key_rows)),
        "question_type_counts": dict(Counter(r["question_type"] for r in review_rows)),
        "answer_variant_counts": dict(Counter(r["answer_variant"] for r in review_rows)),
        "note": "Teacher labels are intentionally hidden from the review files. Do not inspect the key before human labeling.",
    }

    save_json(args.review_json, review_rows)
    write_markdown(args.review_md, review_rows)
    save_json(args.key, key_rows)
    save_json(args.manifest, manifest)

    print("\nBlind-50 audit sample created")
    print("=" * 56)
    print(f"Input claims:             {len(rows)}")
    print(f"Selected:                 {len(review_rows)}")
    print(f"Review JSON:              {args.review_json}")
    print(f"Review MD:                {args.review_md}")
    print(f"Hidden teacher key:        {args.key}")
    print(f"Manifest:                 {args.manifest}")
    print("\nVisible strata:")
    print(f"  question_type:           {manifest['question_type_counts']}")
    print(f"  answer_variant:          {manifest['answer_variant_counts']}")
    print("\nHidden teacher-label sample counts:")
    print(f"  {manifest['teacher_label_counts_in_hidden_sample']}")
    print("\nReview only the JSON/MD. Do not open the key until labels are filled.")


def compare(args: argparse.Namespace) -> None:
    review_rows = load_json(args.compare)
    key_rows = load_json(args.key)

    key_by_id = {r["review_id"]: r for r in key_rows}

    compared = []
    missing = []
    invalid = []

    for r in review_rows:
        rid = r.get("review_id")
        human = str(r.get("human_label") or "").upper().strip()
        if not human:
            missing.append(rid)
            continue
        if human not in VALID:
            invalid.append({"review_id": rid, "human_label": r.get("human_label")})
            continue
        k = key_by_id.get(rid)
        if not k:
            missing.append(rid)
            continue
        teacher = str(k.get("teacher_label") or "").upper().strip()
        compared.append({
            "review_id": rid,
            "claim_id": r.get("claim_id"),
            "human_label": human,
            "teacher_label": teacher,
            "agree": human == teacher,
            "question_type": r.get("question_type"),
            "answer_variant": r.get("answer_variant"),
        })

    n = len(compared)
    agree = sum(1 for r in compared if r["agree"])

    labels = ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"]
    matrix = {h: {t: 0 for t in labels} for h in labels}
    for r in compared:
        h = r["human_label"]
        t = r["teacher_label"]
        if h in labels and t in labels:
            matrix[h][t] += 1

    disagreements = [r for r in compared if not r["agree"]]

    out = {
        "review_file": str(args.compare),
        "key_file": str(args.key),
        "n_compared": n,
        "n_agree": agree,
        "agreement": round(agree / n, 4) if n else None,
        "missing_human_labels": missing,
        "invalid_human_labels": invalid,
        "human_label_counts": dict(Counter(r["human_label"] for r in compared)),
        "teacher_label_counts": dict(Counter(r["teacher_label"] for r in compared)),
        "confusion_matrix_rows_human_cols_teacher": matrix,
        "disagreements": disagreements,
    }

    save_json(args.compare_out, out)

    print("\nBlind-50 teacher agreement")
    print("=" * 56)
    print(f"Compared:        {n}")
    print(f"Agreement:       {agree}/{n} = {100 * agree / n:.1f}%" if n else "Agreement:       n/a")
    print(f"Missing labels:  {len(missing)}")
    print(f"Invalid labels:  {len(invalid)}")
    print("\nConfusion matrix: rows=human, cols=teacher")
    print("                teacher:SUP  teacher:UNSUP  teacher:ABST")
    for h in labels:
        print(f"human:{h:<11s} {matrix[h]['SUPPORTED']:>11} {matrix[h]['UNSUPPORTED']:>14} {matrix[h]['ABSTENTION']:>13}")
    print(f"\nDisagreements:   {len(disagreements)}")
    print(f"Wrote:           {args.compare_out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DEFAULT_IN)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--review-json", type=Path, default=DEFAULT_REVIEW_JSON)
    ap.add_argument("--review-md", type=Path, default=DEFAULT_REVIEW_MD)
    ap.add_argument("--key", type=Path, default=DEFAULT_KEY)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--compare", type=Path, default=None, help="Review JSON after human labels are filled.")
    ap.add_argument("--compare-out", type=Path, default=DISTILL_DIR / "gold_blind50_teacher_agreement.json")
    args = ap.parse_args()

    if args.compare:
        compare(args)
    else:
        build(args)


if __name__ == "__main__":
    main()
