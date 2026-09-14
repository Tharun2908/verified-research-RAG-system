#!/usr/bin/env python3
"""
Expand the grounded-hard human review from 150 to a nested 500-claim sample.

Modes
-----
prepare:
  - Match the existing 150 labeled claims into the new 500 sample by claim_id.
  - Preserve the NEW 500-sample metadata and sampling weights.
  - Carry forward only human label/notes from the old review.
  - Emit a review file containing only the 350 newly sampled claims.

finalize:
  - Parse labels from the completed new-only markdown.
  - Merge old carried labels + new labels into a final 500-row labeled JSONL.
  - Emit raw/weighted label summaries.

Allowed human outcomes:
  SUPPORTED / UNSUPPORTED / ABSTENTION / INVALID_EXTRACTION
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ALLOWED = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION", "INVALID_EXTRACTION"}

DEFAULT_DIR = Path("backend/data/grounded_hard_eval")
DEFAULT_OLD = DEFAULT_DIR / "grounded_hard_random_review_labeled.jsonl"
DEFAULT_SAMPLE = DEFAULT_DIR / "grounded_hard_random_review_500.jsonl"
DEFAULT_NEW_JSONL = DEFAULT_DIR / "grounded_hard_random_review_500_new_only.jsonl"
DEFAULT_NEW_MD = DEFAULT_DIR / "grounded_hard_random_review_500_new_only.md"
DEFAULT_SEEDED = DEFAULT_DIR / "grounded_hard_random_review_500_seeded.jsonl"
DEFAULT_PREP_REPORT = DEFAULT_DIR / "grounded_hard_random_review_500_prepare_report.json"
DEFAULT_FINAL = DEFAULT_DIR / "grounded_hard_random_review_500_labeled.jsonl"
DEFAULT_FINAL_SUMMARY = DEFAULT_DIR / "grounded_hard_random_review_500_labeled_summary.json"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {e}") from e
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def clean(value: Any) -> str:
    return str(value or "").strip()


def clean_label(value: Any) -> str:
    s = clean(value).upper()
    s = s.replace("-", "_").replace(" ", "_")
    s = re.sub(r"[^A-Z_]", "", s)
    return s if s in ALLOWED else ""


def get_existing_label(row: dict[str, Any]) -> str:
    for key in ("human_final_label", "final_label", "label"):
        label = clean_label(row.get(key))
        if label:
            return label
    return ""


def get_existing_notes(row: dict[str, Any]) -> str:
    for key in ("human_final_notes", "final_notes", "notes"):
        value = clean(row.get(key))
        if value:
            return value
    return ""


def format_evidence(text: Any, max_chars: int = 5000) -> str:
    value = clean(text)
    if len(value) > max_chars:
        return value[:max_chars] + "\n\n[TRUNCATED FOR REVIEW FILE]"
    return value


def write_review_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Grounded-Hard Expansion: New Human Review Only",
        "",
        "These rows are the newly sampled claims from the nested 500-claim benchmark.",
        "The original 150 human-reviewed claims are excluded from this file and will be carried forward by `claim_id`.",
        "",
        "Fill `FINAL_LABEL` with exactly one of:",
        "- `SUPPORTED`: the substantive claim is supported by the provided evidence.",
        "- `UNSUPPORTED`: the claim adds, changes, or overstates information not supported by the evidence.",
        "- `ABSTENTION`: refusal, insufficient-evidence statement, or meta statement such as 'the sources do not mention X'.",
        "- `INVALID_EXTRACTION`: the extracted unit is malformed/non-substantive or combines text such that a support judgment is not meaningful.",
        "",
        "Do not use verifier/model scores while labeling.",
        "",
        "---",
        "",
    ]

    for row in rows:
        lines.extend(
            [
                f"## {row['review_id']} — {row['claim_id']}",
                "",
                "**FINAL_LABEL:** ",
                "",
                "**FINAL_NOTES:** ",
                "",
                "### Metadata",
                "",
                f"- review_order: {row.get('review_order')}",
                f"- sampling_stratum: `{row.get('sampling_stratum')}`",
                f"- sampling_weight: `{row.get('sampling_weight')}`",
                f"- hard_policy: `{row.get('hard_policy')}`",
                f"- answer_variant: `{row.get('answer_variant')}`",
                f"- evidence_scope: `{row.get('evidence_scope')}`",
                f"- question_template: `{row.get('question_template')}`",
                "",
                "### Question",
                "",
                clean(row.get("question")),
                "",
                "### Claim",
                "",
                clean(row.get("claim")),
                "",
                "### Evidence",
                "",
                "```text",
                format_evidence(row.get("evidence_text_for_verifier")),
                "```",
                "",
                "---",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def extract_field_block(section: str, field: str) -> str:
    marker = re.search(
        rf"(?:\*\*)?{re.escape(field)}\s*:\s*(?:\*\*)?\s*",
        section,
        flags=re.IGNORECASE,
    )
    if not marker:
        return ""

    rest = section[marker.end():]
    stops = [
        r"\n\s*(?:\*\*)?FINAL_LABEL\s*:",
        r"\n\s*(?:\*\*)?FINAL_NOTES\s*:",
        r"\n\s*###\s+Metadata",
        r"\n\s*###\s+Question",
        r"\n\s*###\s+Claim",
        r"\n\s*###\s+Evidence",
        r"\n\s*---\s*",
        r"\n\s*##\s+GHR\d+",
    ]

    stop = len(rest)
    for pattern in stops:
        m = re.search(pattern, rest, flags=re.IGNORECASE)
        if m:
            stop = min(stop, m.start())
    return rest[:stop].strip()


def parse_review_markdown(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^##\s+(GHR\d+)\s+—\s+([^\s]+)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    parsed: dict[str, dict[str, str]] = {}

    for i, match in enumerate(matches):
        review_id = match.group(1)
        claim_id = match.group(2)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]

        raw_label = extract_field_block(section, "FINAL_LABEL")
        label = clean_label(raw_label)
        notes = extract_field_block(section, "FINAL_NOTES")

        parsed[review_id] = {
            "review_id": review_id,
            "claim_id": claim_id,
            "final_label": label,
            "final_notes": notes,
        }

    return parsed


def weighted_counts(rows: list[dict[str, Any]]) -> dict[str, float]:
    counts: dict[str, float] = defaultdict(float)
    for row in rows:
        counts[str(row["final_label"])] += float(row.get("sampling_weight") or 1.0)
    return {k: round(v, 4) for k, v in sorted(counts.items())}


def prepare(args: argparse.Namespace) -> None:
    old_rows = read_jsonl(args.old_labeled)
    sample_rows = read_jsonl(args.sample_500)

    old_by_claim: dict[str, dict[str, str]] = {}
    bad_old = []

    for row in old_rows:
        claim_id = clean(row.get("claim_id"))
        label = get_existing_label(row)
        if not claim_id or not label:
            bad_old.append(claim_id or "<missing claim_id>")
            continue
        if claim_id in old_by_claim:
            raise SystemExit(f"Duplicate old claim_id: {claim_id}")
        old_by_claim[claim_id] = {
            "label": label,
            "notes": get_existing_notes(row),
        }

    if bad_old:
        raise SystemExit(
            f"Could not recover valid labels for {len(bad_old)} old rows. "
            f"Examples: {bad_old[:10]}"
        )

    sample_ids = [clean(r.get("claim_id")) for r in sample_rows]
    missing_old = sorted(set(old_by_claim) - set(sample_ids))
    if missing_old:
        raise SystemExit(
            f"{len(missing_old)} old reviewed claims are missing from the 500 sample. "
            f"Examples: {missing_old[:10]}"
        )

    seeded = []
    new_only = []

    for row in sample_rows:
        claim_id = clean(row.get("claim_id"))
        rr = dict(row)

        if claim_id in old_by_claim:
            carried = old_by_claim[claim_id]
            rr["final_label"] = carried["label"]
            rr["human_final_label"] = carried["label"]
            rr["final_notes"] = carried["notes"]
            rr["label_source"] = "carried_forward_from_original_150"
        else:
            rr["final_label"] = ""
            rr["human_final_label"] = ""
            rr["final_notes"] = ""
            rr["label_source"] = "pending_new_review"
            new_only.append(dict(row))

        seeded.append(rr)

    write_jsonl(args.out_seeded, seeded)
    write_jsonl(args.out_new_jsonl, new_only)
    write_review_markdown(args.out_new_md, new_only)

    carried_labels = Counter(
        r["final_label"] for r in seeded
        if r.get("label_source") == "carried_forward_from_original_150"
    )

    report = {
        "sample_500_rows": len(sample_rows),
        "old_labeled_rows": len(old_rows),
        "old_claims_found_in_500": len(old_by_claim),
        "new_claims_to_review": len(new_only),
        "carried_forward_label_counts": dict(carried_labels),
        "matching_key": "claim_id",
        "sampling_metadata_source": str(args.sample_500),
        "important": [
            "Sampling weights and review metadata come from the new 500-claim sample.",
            "Only human labels/notes are carried from the original 150 rows.",
            "No evaluated-model prediction is used to choose the 350 new rows.",
            "INVALID_EXTRACTION is preserved as a fourth review outcome.",
        ],
    }
    save_json(args.report, report)

    print("\nPrepared nested 500-claim human review")
    print("=" * 72)
    print(f"500-sample rows:       {len(sample_rows)}")
    print(f"Old labels carried:    {len(old_by_claim)}")
    print(f"New claims to review:  {len(new_only)}")
    print(f"Carried label counts:  {dict(carried_labels)}")
    print("\nWrote:")
    print(f"  {args.out_new_md}")
    print(f"  {args.out_new_jsonl}")
    print(f"  {args.out_seeded}")
    print(f"  {args.report}")


def finalize(args: argparse.Namespace) -> None:
    old_rows = read_jsonl(args.old_labeled)
    sample_rows = read_jsonl(args.sample_500)
    new_rows = read_jsonl(args.new_jsonl)
    parsed = parse_review_markdown(args.new_md)

    old_by_claim = {}
    for row in old_rows:
        cid = clean(row.get("claim_id"))
        label = get_existing_label(row)
        if not cid or not label:
            raise SystemExit(f"Missing valid old human label for claim_id={cid!r}")
        old_by_claim[cid] = {
            "label": label,
            "notes": get_existing_notes(row),
        }

    new_by_claim = {clean(r.get("claim_id")): r for r in new_rows}
    parsed_by_claim: dict[str, dict[str, str]] = {}
    blanks = []
    mismatches = []

    for row in new_rows:
        rid = clean(row.get("review_id"))
        cid = clean(row.get("claim_id"))
        p = parsed.get(rid)
        if not p:
            blanks.append(f"{rid}:{cid}")
            continue
        if p["claim_id"] != cid:
            mismatches.append(
                {"review_id": rid, "expected_claim_id": cid, "found_claim_id": p["claim_id"]}
            )
            continue
        if not p["final_label"]:
            blanks.append(f"{rid}:{cid}")
            continue
        parsed_by_claim[cid] = p

    if mismatches:
        raise SystemExit(f"Review-id/claim-id mismatches found: {mismatches[:10]}")
    if blanks:
        raise SystemExit(
            f"{len(blanks)} new review rows are blank/invalid. Examples: {blanks[:10]}"
        )
    if set(parsed_by_claim) != set(new_by_claim):
        missing = sorted(set(new_by_claim) - set(parsed_by_claim))
        extra = sorted(set(parsed_by_claim) - set(new_by_claim))
        raise SystemExit(f"New-review claim mismatch. missing={missing[:10]} extra={extra[:10]}")

    final_rows = []
    source_counts = Counter()

    for row in sample_rows:
        cid = clean(row.get("claim_id"))
        rr = dict(row)

        if cid in old_by_claim:
            info = old_by_claim[cid]
            source = "carried_forward_from_original_150"
        elif cid in parsed_by_claim:
            p = parsed_by_claim[cid]
            info = {"label": p["final_label"], "notes": p["final_notes"]}
            source = "new_350_review"
        else:
            raise SystemExit(f"No human label available for sampled claim {cid}")

        rr["final_label"] = info["label"]
        rr["human_final_label"] = info["label"]
        rr["final_notes"] = info["notes"]
        rr["label_source"] = source
        source_counts[source] += 1
        final_rows.append(rr)

    raw_counts = Counter(r["final_label"] for r in final_rows)

    binary = [
        r for r in final_rows
        if r["final_label"] in {"SUPPORTED", "UNSUPPORTED"}
    ]
    binary_counts = Counter(r["final_label"] for r in binary)

    by_stratum: dict[str, Counter] = defaultdict(Counter)
    for row in final_rows:
        by_stratum[str(row.get("sampling_stratum"))][row["final_label"]] += 1

    summary = {
        "rows_total": len(final_rows),
        "label_source_counts": dict(source_counts),
        "label_counts_raw": dict(raw_counts),
        "label_counts_weighted": weighted_counts(final_rows),
        "binary_rows_raw": len(binary),
        "binary_label_counts_raw": dict(binary_counts),
        "binary_label_counts_weighted": weighted_counts(binary),
        "by_stratum_raw": {
            k: dict(v) for k, v in sorted(by_stratum.items())
        },
        "sampling_protocol": (
            "nested expansion to 500 using the same model-independent "
            "hard_policy × answer_variant stratified random sampler and seed"
        ),
        "notes": [
            "Sampling metadata and sampling_weight come from the 500-row sample.",
            "Original 150 labels were matched by claim_id, not review_id.",
            "ABSTENTION and INVALID_EXTRACTION should be excluded from binary metrics.",
            "No evaluated-model prediction was used to select the newly reviewed claims.",
        ],
    }

    write_jsonl(args.out_labeled, final_rows)
    save_json(args.out_summary, summary)

    print("\nFinalized 500-claim grounded-hard human review")
    print("=" * 72)
    print(f"Rows total:            {len(final_rows)}")
    print(f"Label sources:         {dict(source_counts)}")
    print(f"Raw labels:            {dict(raw_counts)}")
    print(f"Binary rows:           {len(binary)}")
    print(f"Binary labels:         {dict(binary_counts)}")
    print(f"Weighted binary:       {weighted_counts(binary)}")
    print("\nWrote:")
    print(f"  {args.out_labeled}")
    print(f"  {args.out_summary}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)

    prep = sub.add_parser("prepare")
    prep.add_argument("--old-labeled", type=Path, default=DEFAULT_OLD)
    prep.add_argument("--sample-500", type=Path, default=DEFAULT_SAMPLE)
    prep.add_argument("--out-new-jsonl", type=Path, default=DEFAULT_NEW_JSONL)
    prep.add_argument("--out-new-md", type=Path, default=DEFAULT_NEW_MD)
    prep.add_argument("--out-seeded", type=Path, default=DEFAULT_SEEDED)
    prep.add_argument("--report", type=Path, default=DEFAULT_PREP_REPORT)

    fin = sub.add_parser("finalize")
    fin.add_argument("--old-labeled", type=Path, default=DEFAULT_OLD)
    fin.add_argument("--sample-500", type=Path, default=DEFAULT_SAMPLE)
    fin.add_argument("--new-jsonl", type=Path, default=DEFAULT_NEW_JSONL)
    fin.add_argument("--new-md", type=Path, default=DEFAULT_NEW_MD)
    fin.add_argument("--out-labeled", type=Path, default=DEFAULT_FINAL)
    fin.add_argument("--out-summary", type=Path, default=DEFAULT_FINAL_SUMMARY)

    return ap


if __name__ == "__main__":
    args = build_parser().parse_args()
    if args.mode == "prepare":
        prepare(args)
    else:
        finalize(args)
