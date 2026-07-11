#!/usr/bin/env python
"""
sample_unsupported_477_audit.py

Create a blind 100-row human audit of Opus disagreements among the 477 rows
originally labeled UNSUPPORTED, then assess agreement and optionally build the
single cleaned train/validation dataset.

Pre-registered sample:
  - 70 Opus SUPPORTED disagreements
  - 30 Opus ABSTENTION disagreements
  - preserve train/validation proportions within each Opus stratum
  - fixed seed 2908

Decision rule:
  - overall agreement >= 0.85
  - Opus-SUPPORTED stratum agreement >= 0.80
  - Opus-ABSTENTION stratum agreement >= 0.80

If all three pass:
  - sampled rows use human labels
  - unsampled Opus disagreements use Opus labels
  - Opus/original UNSUPPORTED agreements remain UNSUPPORTED
  - original SUPPORTED rows remain SUPPORTED
  - ABSTENTION and INVALID_EXTRACTION are removed from binary data
  - original qid train/validation membership is preserved

If any rule fails:
  - no cleaned train/validation files are built
  - the adaptation track should stop

Export:
  python -u sample_unsupported_477_audit.py export \
    --audit unsupported_477_opus_audit.json \
    --out-md unsupported_477_sample100_human_review.md \
    --manifest unsupported_477_sample100_manifest.jsonl \
    --summary unsupported_477_sample100_sampling_summary.json \
    --seed 2908

Assess and, only if passed, build cleaned datasets:
  python -u sample_unsupported_477_audit.py assess-build \
    --md unsupported_477_sample100_human_review.md \
    --manifest unsupported_477_sample100_manifest.jsonl \
    --audit unsupported_477_opus_audit.json \
    --train data/distill_arxiv_v2/binary_train.jsonl \
    --val data/distill_arxiv_v2/binary_val.jsonl \
    --out-dir data/distill_arxiv_v2_cleaned_sample100
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ALLOWED = {
    "SUPPORTED",
    "UNSUPPORTED",
    "ABSTENTION",
    "INVALID_EXTRACTION",
}

TARGETS = {
    "SUPPORTED": 70,
    "ABSTENTION": 30,
}


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
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


def claim_id(row: dict[str, Any]) -> str:
    value = row.get("claim_id")
    if value is None or not str(value).strip():
        raise ValueError(f"Missing claim_id in row with keys {sorted(row.keys())}")
    return str(value)


def clean_text(value: Any) -> str:
    return str(value or "").strip()


def evidence_text(row: dict[str, Any]) -> str:
    return clean_text(
        row.get("evidence_text_for_verifier")
        or row.get("evidence_text")
        or ""
    )


def normalize_label(value: Any) -> str:
    text = str(value or "").strip().upper()
    text = text.strip("`*_ ")
    text = text.replace("-", "_").replace(" ", "_")
    text = re.sub(r"[^A-Z_]", "", text)
    return text if text in ALLOWED else ""


def allocate_by_split(
    rows: list[dict[str, Any]],
    target: int,
) -> dict[str, int]:
    counts = Counter(str(row.get("audit_source_split")) for row in rows)
    total = sum(counts.values())
    if total < target:
        raise ValueError(f"Cannot sample {target} from only {total} rows.")

    raw = {
        split: target * count / total
        for split, count in counts.items()
    }
    allocation = {
        split: min(counts[split], int(raw[split]))
        for split in counts
    }

    remaining = target - sum(allocation.values())
    order = sorted(
        counts,
        key=lambda split: (
            raw[split] - int(raw[split]),
            counts[split],
        ),
        reverse=True,
    )

    while remaining > 0:
        changed = False
        for split in order:
            if allocation[split] < counts[split]:
                allocation[split] += 1
                remaining -= 1
                changed = True
                if remaining == 0:
                    break
        if not changed:
            raise RuntimeError("Could not complete split allocation.")

    return allocation


def export_sample(args: argparse.Namespace) -> None:
    audit = load_json(args.audit)
    if not isinstance(audit, list):
        raise SystemExit(f"{args.audit} must contain a JSON list.")
    if len(audit) != 477:
        raise SystemExit(f"Expected 477 audit rows, found {len(audit)}.")

    rng = random.Random(args.seed)
    selected: list[dict[str, Any]] = []
    allocation_report: dict[str, Any] = {}

    for opus_label, target in TARGETS.items():
        pool = [
            dict(row)
            for row in audit
            if str(row.get("opus_label") or "").upper() == opus_label
        ]
        allocation = allocate_by_split(pool, target)
        allocation_report[opus_label] = {
            "pool_total": len(pool),
            "target": target,
            "pool_by_split": dict(
                Counter(str(r.get("audit_source_split")) for r in pool)
            ),
            "sample_by_split": allocation,
        }

        by_split: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in pool:
            by_split[str(row.get("audit_source_split"))].append(row)

        for split, n in allocation.items():
            candidates = by_split[split]
            rng.shuffle(candidates)
            for row in candidates[:n]:
                rr = dict(row)
                rr["hidden_opus_stratum"] = opus_label
                selected.append(rr)

    if len(selected) != 100:
        raise RuntimeError(f"Expected 100 selected rows, got {len(selected)}.")

    rng.shuffle(selected)
    manifest = []

    lines = [
        "# Blind Human Audit — 100 Opus Disagreements",
        "",
        "Fill `FINAL_LABEL` with exactly one of:",
        "",
        "- `SUPPORTED`",
        "- `UNSUPPORTED`",
        "- `ABSTENTION`",
        "- `INVALID_EXTRACTION`",
        "",
        "The Opus draft label is hidden. Do not use verifier scores or grounded-hard results.",
        "",
        "---",
        "",
    ]

    for index, row in enumerate(selected, start=1):
        rr = dict(row)
        rr["review_id"] = f"U100_{index:03d}"
        rr["sample_seed"] = args.seed
        rr["sample_protocol"] = (
            "70 Opus SUPPORTED + 30 Opus ABSTENTION; "
            "train/val proportions preserved within each stratum"
        )
        manifest.append(rr)

        lines.extend([
            f"## {rr['review_id']} — {claim_id(rr)}",
            "",
            "**FINAL_LABEL:** ",
            "",
            "**FINAL_NOTES:** ",
            "",
            "### Metadata",
            "",
            f"- source_split: `{rr.get('audit_source_split')}`",
            f"- qid: `{rr.get('qid')}`",
            f"- answer_variant: `{rr.get('answer_variant')}`",
            f"- evidence_scope: `{rr.get('evidence_scope')}`",
            f"- question_type: `{rr.get('question_type')}`",
            "",
            "### Question",
            "",
            clean_text(rr.get("question")),
            "",
            "### Claim",
            "",
            clean_text(rr.get("claim") or rr.get("claim_text")),
            "",
            "### Evidence",
            "",
            "```text",
            evidence_text(rr),
            "```",
            "",
            "---",
            "",
        ])

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines), encoding="utf-8")
    write_jsonl(args.manifest, manifest)

    summary = {
        "audit_rows_total": len(audit),
        "sample_rows": len(manifest),
        "seed": args.seed,
        "targets": TARGETS,
        "allocation": allocation_report,
        "sample_hidden_stratum_counts": dict(
            Counter(row["hidden_opus_stratum"] for row in manifest)
        ),
        "sample_source_split_counts": dict(
            Counter(str(row.get("audit_source_split")) for row in manifest)
        ),
        "decision_rule": {
            "overall_agreement_min": 0.85,
            "supported_stratum_agreement_min": 0.80,
            "abstention_stratum_agreement_min": 0.80,
        },
        "opus_label_hidden_from_reviewer": True,
    }
    save_json(args.summary, summary)

    print("\nBuilt blind 100-row audit")
    print("=" * 72)
    print(f"Rows: {len(manifest)}")
    print("Hidden strata:", summary["sample_hidden_stratum_counts"])
    print("Source splits:", summary["sample_source_split_counts"])
    print("Allocation:", json.dumps(allocation_report, indent=2))
    print("\nWrote:")
    print(f"  {args.out_md}")
    print(f"  {args.manifest}")
    print(f"  {args.summary}")


def extract_field(section: str, field_name: str) -> str:
    match = re.search(
        rf"(?:\*\*)?{re.escape(field_name)}\s*:\s*(?:\*\*)?\s*",
        section,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""

    rest = section[match.end():]
    stop_patterns = [
        r"\n\s*(?:\*\*)?FINAL_LABEL\s*:",
        r"\n\s*(?:\*\*)?FINAL_NOTES\s*:",
        r"\n\s*###\s+Metadata",
        r"\n\s*###\s+Question",
        r"\n\s*###\s+Claim",
        r"\n\s*###\s+Evidence",
        r"\n\s*---\s*",
        r"\n\s*##\s+U100_\d+",
    ]

    end = len(rest)
    for pattern in stop_patterns:
        stop = re.search(pattern, rest, flags=re.IGNORECASE)
        if stop:
            end = min(end, stop.start())

    return rest[:end].strip()


def parse_review(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    header = re.compile(
        r"^##\s+(U100_\d+)\s+—\s+([^\s]+)\s*$",
        flags=re.MULTILINE,
    )
    matches = list(header.finditer(text))

    parsed = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end]

        parsed[match.group(1)] = {
            "claim_id": match.group(2),
            "final_label": normalize_label(
                extract_field(section, "FINAL_LABEL")
            ),
            "final_notes": extract_field(section, "FINAL_NOTES"),
        }

    return parsed


def assess_build(args: argparse.Namespace) -> None:
    manifest = read_jsonl(args.manifest)
    parsed = parse_review(args.md)
    audit = load_json(args.audit)
    train_rows = read_jsonl(args.train)
    val_rows = read_jsonl(args.val)

    if len(manifest) != 100:
        raise SystemExit(f"Expected 100 manifest rows, found {len(manifest)}.")
    if len(audit) != 477:
        raise SystemExit(f"Expected 477 audit rows, found {len(audit)}.")

    human_labels: dict[str, str] = {}
    human_notes: dict[str, str] = {}
    hidden_strata: dict[str, str] = {}
    blanks = []
    mismatches = []

    for row in manifest:
        review_id = str(row["review_id"])
        cid = claim_id(row)
        review = parsed.get(review_id)

        if not review:
            blanks.append(review_id)
            continue
        if review["claim_id"] != cid:
            mismatches.append({
                "review_id": review_id,
                "manifest_claim_id": cid,
                "markdown_claim_id": review["claim_id"],
            })
            continue
        if not review["final_label"]:
            blanks.append(review_id)
            continue

        human_labels[cid] = review["final_label"]
        human_notes[cid] = review["final_notes"]
        hidden_strata[cid] = str(row["hidden_opus_stratum"]).upper()

    if mismatches:
        raise SystemExit(f"Claim mismatches: {mismatches[:10]}")
    if blanks:
        raise SystemExit(
            f"Blank or missing labels for {len(blanks)} rows. "
            f"First: {blanks[:20]}"
        )

    agreement_rows = []
    for row in manifest:
        cid = claim_id(row)
        opus_label = hidden_strata[cid]
        human_label = human_labels[cid]
        agreement_rows.append({
            "review_id": row["review_id"],
            "claim_id": cid,
            "source_split": row.get("audit_source_split"),
            "opus_label": opus_label,
            "human_label": human_label,
            "agree": opus_label == human_label,
            "human_notes": human_notes[cid],
        })

    overall_agreement = sum(r["agree"] for r in agreement_rows) / len(agreement_rows)

    stratum_results = {}
    for stratum in ("SUPPORTED", "ABSTENTION"):
        subset = [r for r in agreement_rows if r["opus_label"] == stratum]
        agreement = sum(r["agree"] for r in subset) / len(subset)
        stratum_results[stratum] = {
            "n": len(subset),
            "agree_n": sum(r["agree"] for r in subset),
            "agreement": agreement,
            "human_label_counts": dict(
                Counter(r["human_label"] for r in subset)
            ),
        }

    decision_pass = (
        overall_agreement >= 0.85
        and stratum_results["SUPPORTED"]["agreement"] >= 0.80
        and stratum_results["ABSTENTION"]["agreement"] >= 0.80
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "sample100_human_adjudications.jsonl", agreement_rows)

    decision_summary = {
        "decision_rule": {
            "overall_agreement_min": 0.85,
            "supported_stratum_agreement_min": 0.80,
            "abstention_stratum_agreement_min": 0.80,
        },
        "observed": {
            "overall_agreement": overall_agreement,
            "strata": stratum_results,
        },
        "decision_pass": decision_pass,
        "next_step": (
            "build exactly one cleaned train/validation dataset and run one retrain"
            if decision_pass
            else "stop adaptation track; do not use automatic cleaning"
        ),
    }
    save_json(args.out_dir / "sample100_agreement_summary.json", decision_summary)

    print("\n100-row agreement audit")
    print("=" * 72)
    print(f"Overall: {overall_agreement:.2%}")
    print(
        "SUPPORTED stratum:",
        f"{stratum_results['SUPPORTED']['agreement']:.2%}",
    )
    print(
        "ABSTENTION stratum:",
        f"{stratum_results['ABSTENTION']['agreement']:.2%}",
    )
    print("Decision passed:", decision_pass)

    if not decision_pass:
        print("\nNo cleaned datasets were built.")
        print(f"Wrote: {args.out_dir / 'sample100_agreement_summary.json'}")
        return

    audit_by_cid = {claim_id(row): row for row in audit}
    sampled_ids = set(human_labels)

    final_original_positive_labels: dict[str, str] = {}
    label_sources: dict[str, str] = {}

    for cid, row in audit_by_cid.items():
        opus_label = str(row.get("opus_label") or "").upper()

        if cid in sampled_ids:
            final_original_positive_labels[cid] = human_labels[cid]
            label_sources[cid] = "sample100_human_label"
        elif opus_label in ALLOWED:
            final_original_positive_labels[cid] = opus_label
            label_sources[cid] = "accepted_opus_after_sample100_audit"
        else:
            raise SystemExit(f"Invalid Opus label for {cid}: {opus_label!r}")

    def rebuild(
        original_rows: list[dict[str, Any]],
        split_name: str,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        kept = []
        removed = []

        for row in original_rows:
            rr = dict(row)
            original_label = int(rr["label"])

            if original_label == 0:
                final_label = "SUPPORTED"
                label_source = "original_supported_teacher_label_unchanged"
            else:
                cid = claim_id(rr)
                final_label = final_original_positive_labels[cid]
                label_source = label_sources[cid]

            rr["cleaning_original_label"] = original_label
            rr["cleaning_final_label_name"] = final_label
            rr["cleaning_label_source"] = label_source
            rr["cleaning_source_split"] = split_name

            if claim_id(rr) in human_notes:
                rr["cleaning_human_notes"] = human_notes[claim_id(rr)]

            if final_label == "SUPPORTED":
                rr["label"] = 0
                rr["label_name"] = "SUPPORTED"
                kept.append(rr)
            elif final_label == "UNSUPPORTED":
                rr["label"] = 1
                rr["label_name"] = "UNSUPPORTED"
                kept.append(rr)
            elif final_label in {"ABSTENTION", "INVALID_EXTRACTION"}:
                rr["cleaning_removal_reason"] = final_label
                removed.append(rr)
            else:
                raise RuntimeError(f"Unexpected final label: {final_label}")

        return kept, removed

    cleaned_train, removed_train = rebuild(train_rows, "train")
    cleaned_val, removed_val = rebuild(val_rows, "val")

    train_qids = {str(row.get("qid")) for row in cleaned_train}
    val_qids = {str(row.get("qid")) for row in cleaned_val}
    qid_overlap = train_qids & val_qids
    if qid_overlap:
        raise SystemExit(
            f"Train/validation qid overlap after cleaning: {len(qid_overlap)}"
        )

    write_jsonl(args.out_dir / "binary_train_cleaned.jsonl", cleaned_train)
    write_jsonl(args.out_dir / "binary_val_cleaned.jsonl", cleaned_val)
    write_jsonl(
        args.out_dir / "removed_abstention_invalid.jsonl",
        removed_train + removed_val,
    )

    final_positive_counts = Counter(final_original_positive_labels.values())
    contamination_count = (
        final_positive_counts["SUPPORTED"]
        + final_positive_counts["ABSTENTION"]
        + final_positive_counts["INVALID_EXTRACTION"]
    )

    cleaning_summary = {
        "agreement_decision": decision_summary,
        "original_positive_audit": {
            "rows": 477,
            "final_label_counts": dict(final_positive_counts),
            "contaminated_rows": contamination_count,
            "contamination_rate": contamination_count / 477,
            "pre_registered_20_percent_trigger_reached": contamination_count >= 96,
        },
        "cleaned_train": {
            "rows": len(cleaned_train),
            "label_counts": dict(
                Counter(int(row["label"]) for row in cleaned_train)
            ),
            "questions": len(train_qids),
            "removed": len(removed_train),
        },
        "cleaned_val": {
            "rows": len(cleaned_val),
            "label_counts": dict(
                Counter(int(row["label"]) for row in cleaned_val)
            ),
            "questions": len(val_qids),
            "removed": len(removed_val),
        },
        "removed_reason_counts": dict(
            Counter(
                row["cleaning_removal_reason"]
                for row in removed_train + removed_val
            )
        ),
        "train_val_qid_overlap": 0,
        "grounded_hard_used_for_cleaning": False,
        "allowed_follow_up": (
            "one cleaned SciFact/HealthVer-initialized retrain; "
            "one evaluation on existing human gold and grounded-hard; no iteration"
        ),
    }
    save_json(args.out_dir / "cleaning_summary.json", cleaning_summary)

    print("\nDecision passed. Cleaned datasets built.")
    print(
        "Cleaned train:",
        len(cleaned_train),
        dict(Counter(int(r["label"]) for r in cleaned_train)),
    )
    print(
        "Cleaned val:",
        len(cleaned_val),
        dict(Counter(int(r["label"]) for r in cleaned_val)),
    )
    print(
        "Final original-positive contamination:",
        f"{contamination_count}/477 = {contamination_count / 477:.2%}",
    )
    print("\nWrote:")
    print(f"  {args.out_dir / 'binary_train_cleaned.jsonl'}")
    print(f"  {args.out_dir / 'binary_val_cleaned.jsonl'}")
    print(f"  {args.out_dir / 'cleaning_summary.json'}")
    print(f"  {args.out_dir / 'sample100_agreement_summary.json'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument(
        "--audit",
        type=Path,
        default=Path("unsupported_477_opus_audit.json"),
    )
    export_parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("unsupported_477_sample100_human_review.md"),
    )
    export_parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("unsupported_477_sample100_manifest.jsonl"),
    )
    export_parser.add_argument(
        "--summary",
        type=Path,
        default=Path("unsupported_477_sample100_sampling_summary.json"),
    )
    export_parser.add_argument("--seed", type=int, default=2908)
    export_parser.set_defaults(func=export_sample)

    assess_parser = subparsers.add_parser("assess-build")
    assess_parser.add_argument(
        "--md",
        type=Path,
        default=Path("unsupported_477_sample100_human_review.md"),
    )
    assess_parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("unsupported_477_sample100_manifest.jsonl"),
    )
    assess_parser.add_argument(
        "--audit",
        type=Path,
        default=Path("unsupported_477_opus_audit.json"),
    )
    assess_parser.add_argument(
        "--train",
        type=Path,
        default=Path("data/distill_arxiv_v2/binary_train.jsonl"),
    )
    assess_parser.add_argument(
        "--val",
        type=Path,
        default=Path("data/distill_arxiv_v2/binary_val.jsonl"),
    )
    assess_parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/distill_arxiv_v2_cleaned_sample100"),
    )
    assess_parser.set_defaults(func=assess_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
