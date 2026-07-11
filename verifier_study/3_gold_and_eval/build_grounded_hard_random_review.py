"""
build_grounded_hard_random_review.py

Build and import a model-independent stratified random human-review sample
for the grounded-hard tranche.

This replaces expensive full Opus screening.

Why this is clean:
  - No evaluated model participates in sampling.
  - No drafter model is needed.
  - Sampling is stratified by construction condition, not prediction.
  - Metrics can later be weighted by stratum N/n.

Inputs:
  grounded_hard_claims.json

Outputs from export:
  grounded_hard_random_review.md
  grounded_hard_random_review.jsonl
  grounded_hard_random_review_sampling_report.json

Outputs from import-labels:
  grounded_hard_random_review_labeled.jsonl
  grounded_hard_random_review_labeled_summary.json

Run export:
  python -u build_grounded_hard_random_review.py export \
    --claims grounded_hard_claims.json \
    --out-md grounded_hard_random_review.md \
    --out-jsonl grounded_hard_random_review.jsonl \
    --report grounded_hard_random_review_sampling_report.json \
    --target-n 150 \
    --seed 2908

Fill FINAL_LABEL in the markdown with:
  SUPPORTED / UNSUPPORTED / ABSTENTION

Then import:
  python -u build_grounded_hard_random_review.py import-labels \
    --md grounded_hard_random_review.md \
    --jsonl grounded_hard_random_review.jsonl \
    --out-jsonl grounded_hard_random_review_labeled.jsonl \
    --summary grounded_hard_random_review_labeled_summary.json
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ALLOWED = {"SUPPORTED", "UNSUPPORTED", "ABSTENTION"}


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
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSONL at {path}:{line_no}: {e}") from e
    return rows


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def clean(s: Any) -> str:
    return str(s or "").strip()


def stratum_key(r: dict[str, Any]) -> str:
    # Construction strata only: no model predictions, no labels.
    return f"{r.get('hard_policy') or 'unknown'}::{r.get('answer_variant') or 'unknown'}"


def allocate_stratified_sample(rows: list[dict[str, Any]], target_n: int, seed: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(seed)

    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        buckets[stratum_key(r)].append(r)

    strata = {k: list(v) for k, v in sorted(buckets.items())}
    total_N = len(rows)

    # Proportional allocation, with a small minimum for tiny strata.
    min_per_stratum = 6
    initial = {}
    for k, vals in strata.items():
        N = len(vals)
        proportional = round(target_n * N / total_N)
        n = max(min_per_stratum, proportional)
        n = min(n, N)
        initial[k] = n

    # Adjust total to target_n.
    current = sum(initial.values())

    if current > target_n:
        # Remove from largest over-allocated strata first, but keep at least min or all if smaller.
        keys = sorted(strata, key=lambda k: initial[k], reverse=True)
        while current > target_n:
            changed = False
            for k in keys:
                floor = min(min_per_stratum, len(strata[k]))
                if initial[k] > floor:
                    initial[k] -= 1
                    current -= 1
                    changed = True
                    if current <= target_n:
                        break
            if not changed:
                break

    elif current < target_n:
        # Add to strata with remaining capacity, prioritizing large strata.
        keys = sorted(strata, key=lambda k: len(strata[k]), reverse=True)
        while current < target_n:
            changed = False
            for k in keys:
                if initial[k] < len(strata[k]):
                    initial[k] += 1
                    current += 1
                    changed = True
                    if current >= target_n:
                        break
            if not changed:
                break

    selected = []
    stratum_stats = {}

    for k, vals in strata.items():
        vals = list(vals)
        rng.shuffle(vals)
        n = initial[k]
        chosen = vals[:n]
        N = len(vals)
        weight = N / n if n > 0 else 0.0

        stratum_stats[k] = {
            "N": N,
            "n": n,
            "sampling_weight": weight,
            "hard_policy": k.split("::", 1)[0],
            "answer_variant": k.split("::", 1)[1],
        }

        for r in chosen:
            rr = dict(r)
            rr["review_id"] = f"GHR{len(selected)+1:04d}"
            rr["sampling_stratum"] = k
            rr["sampling_stratum_N"] = N
            rr["sampling_stratum_n"] = n
            rr["sampling_weight"] = weight
            rr["sampling_seed"] = seed
            rr["sampling_protocol"] = "stratified_random_by_hard_policy_and_answer_variant"
            rr["evaluated_models_used_for_sampling"] = False
            selected.append(rr)

    rng.shuffle(selected)
    for i, r in enumerate(selected, start=1):
        r["review_order"] = i

    report = {
        "input_claims": total_N,
        "target_n": target_n,
        "selected_n": len(selected),
        "seed": seed,
        "sampling_protocol": "stratified_random_by_hard_policy_and_answer_variant",
        "stratum_stats": stratum_stats,
        "selected_by_stratum": dict(Counter(r["sampling_stratum"] for r in selected)),
        "selected_by_hard_policy": dict(Counter(r.get("hard_policy") for r in selected)),
        "selected_by_answer_variant": dict(Counter(r.get("answer_variant") for r in selected)),
        "selected_by_evidence_scope": dict(Counter(r.get("evidence_scope") for r in selected)),
        "evaluated_models_used_for_sampling": False,
        "drafter_model_used_for_sampling": False,
        "notes": [
            "This sample is independent of S2/S4/fusion predictions.",
            "Human labels are final.",
            "Weighted metrics should use sampling_weight to estimate the full grounded-hard claim pool.",
            "ABSTENTION rows should be excluded from binary supported-vs-unsupported metrics and reported separately.",
        ],
    }

    return selected, report


def format_evidence(evidence_text: str, max_chars: int = 5000) -> str:
    evidence_text = clean(evidence_text)
    if len(evidence_text) > max_chars:
        evidence_text = evidence_text[:max_chars] + "\n\n[TRUNCATED FOR REVIEW FILE]"
    return evidence_text


def write_markdown(path: Path, rows: list[dict[str, Any]], report: dict[str, Any]) -> None:
    lines = []
    lines.append("# Grounded-Hard Random Human Review")
    lines.append("")
    lines.append("Fill `FINAL_LABEL` with exactly one of: `SUPPORTED`, `UNSUPPORTED`, `ABSTENTION`.")
    lines.append("")
    lines.append("Label rules:")
    lines.append("- `SUPPORTED`: the substantive claim is supported by the provided evidence.")
    lines.append("- `UNSUPPORTED`: the claim adds/changes/overstates information not supported by the evidence.")
    lines.append("- `ABSTENTION`: refusal, insufficient-evidence statement, or meta statement such as 'the sources do not mention X'.")
    lines.append("")
    lines.append("Sampling:")
    lines.append(f"- Input claim pool: {report['input_claims']}")
    lines.append(f"- Selected claims: {report['selected_n']}")
    lines.append("- Sampling is stratified random by `hard_policy × answer_variant`.")
    lines.append("- No evaluated model was used for sampling.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for r in rows:
        lines.append(f"## {r['review_id']} — {r['claim_id']}")
        lines.append("")
        lines.append(f"**FINAL_LABEL:** ")
        lines.append("")
        lines.append(f"**FINAL_NOTES:** ")
        lines.append("")
        lines.append("### Metadata")
        lines.append("")
        lines.append(f"- review_order: {r.get('review_order')}")
        lines.append(f"- sampling_stratum: `{r.get('sampling_stratum')}`")
        lines.append(f"- sampling_weight: `{r.get('sampling_weight')}`")
        lines.append(f"- hard_policy: `{r.get('hard_policy')}`")
        lines.append(f"- answer_variant: `{r.get('answer_variant')}`")
        lines.append(f"- evidence_scope: `{r.get('evidence_scope')}`")
        lines.append(f"- question_template: `{r.get('question_template')}`")
        lines.append("")
        lines.append("### Question")
        lines.append("")
        lines.append(clean(r.get("question")))
        lines.append("")
        lines.append("### Claim")
        lines.append("")
        lines.append(clean(r.get("claim")))
        lines.append("")
        lines.append("### Evidence")
        lines.append("")
        lines.append("```text")
        lines.append(format_evidence(r.get("evidence_text_for_verifier")))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def export_cmd(args: argparse.Namespace) -> None:
    rows = load_json(args.claims)
    if not isinstance(rows, list):
        raise SystemExit(f"{args.claims} must be a JSON list.")

    selected, report = allocate_stratified_sample(rows, target_n=args.target_n, seed=args.seed)
    write_jsonl(args.out_jsonl, selected)
    write_markdown(args.out_md, selected, report)
    save_json(args.report, report)

    print("\nBuilt grounded-hard random review sample")
    print("=" * 72)
    print(f"Input claims:       {len(rows)}")
    print(f"Selected claims:    {len(selected)}")
    print(f"Target n:           {args.target_n}")
    print(f"Selected by policy: {report['selected_by_hard_policy']}")
    print(f"Selected by arm:    {report['selected_by_answer_variant']}")
    print(f"Selected by scope:  {report['selected_by_evidence_scope']}")
    print("\nWrote:")
    print(f"  {args.out_md}")
    print(f"  {args.out_jsonl}")
    print(f"  {args.report}")


def clean_label(s: Any) -> str:
    s = str(s or "").strip()
    s = re.sub(r"^[>*#\-\s]+", "", s).strip()
    s = s.strip("`*_ ").strip()
    s = s.upper()
    s = s.replace("-", "_").replace(" ", "_")
    s = re.sub(r"[^A-Z_]", "", s)
    return s if s in ALLOWED else ""


def extract_field_block(section: str, field: str) -> str:
    marker_re = re.compile(
        rf"(?:\*\*)?{re.escape(field)}\s*:\s*(?:\*\*)?\s*",
        flags=re.IGNORECASE,
    )
    m = marker_re.search(section)
    if not m:
        return ""

    start = m.end()
    rest = section[start:]

    stop_patterns = [
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
    for pat in stop_patterns:
        sm = re.search(pat, rest, flags=re.IGNORECASE)
        if sm:
            stop = min(stop, sm.start())

    return rest[:stop].strip()


def extract_label(section: str) -> str:
    block = extract_field_block(section, "FINAL_LABEL")
    cand = clean_label(block)
    if cand:
        return cand

    for line in block.splitlines():
        cand = clean_label(line)
        if cand:
            return cand

    upper = block.upper()
    for label in ALLOWED:
        if re.search(rf"\b{label}\b", upper):
            return label

    return ""


def extract_notes(section: str) -> str:
    return extract_field_block(section, "FINAL_NOTES").strip()


def parse_markdown(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^##\s+(GHR\d+)\s+—\s+([^\s]+)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    parsed = {}
    for i, m in enumerate(matches):
        rid = m.group(1)
        cid = m.group(2)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]
        parsed[rid] = {
            "review_id": rid,
            "claim_id": cid,
            "final_label": extract_label(section),
            "final_notes": extract_notes(section),
        }
    return parsed


def weighted_label_counts(rows: list[dict[str, Any]]) -> dict[str, float]:
    out = defaultdict(float)
    for r in rows:
        out[str(r.get("final_label"))] += float(r.get("sampling_weight") or 1.0)
    return {k: round(v, 4) for k, v in sorted(out.items())}


def import_cmd(args: argparse.Namespace) -> None:
    base_rows = read_jsonl(args.jsonl)
    parsed = parse_markdown(args.md)

    updated = []
    blanks = []
    mismatches = []

    for r in base_rows:
        rid = str(r.get("review_id") or "")
        cid = str(r.get("claim_id") or "")
        p = parsed.get(rid)
        if not p:
            blanks.append(rid)
            continue
        if p.get("claim_id") != cid:
            mismatches.append({"review_id": rid, "jsonl_claim_id": cid, "md_claim_id": p.get("claim_id")})
            continue

        label = clean_label(p.get("final_label"))
        if not label:
            blanks.append(rid)

        rr = dict(r)
        rr["final_label"] = label
        rr["human_final_label"] = label
        rr["final_notes"] = p.get("final_notes", "")
        rr["label_source"] = "human_random_stratified_review"
        updated.append(rr)

    if mismatches:
        raise SystemExit(f"Claim mismatches: {mismatches[:5]}")
    if blanks and not args.allow_blanks:
        raise SystemExit(f"Blank/missing FINAL_LABEL for {len(blanks)} rows. First blanks: {blanks[:20]}")

    write_jsonl(args.out_jsonl, updated)

    label_counts = Counter(r.get("final_label") for r in updated)
    binary = [r for r in updated if r.get("final_label") in {"SUPPORTED", "UNSUPPORTED"}]
    binary_counts = Counter(r.get("final_label") for r in binary)

    by_stratum = defaultdict(Counter)
    for r in updated:
        by_stratum[str(r.get("sampling_stratum"))][r.get("final_label")] += 1

    summary = {
        "input_md": str(args.md),
        "input_jsonl": str(args.jsonl),
        "output_jsonl": str(args.out_jsonl),
        "rows_total": len(updated),
        "label_counts_raw": dict(label_counts),
        "label_counts_weighted": weighted_label_counts(updated),
        "binary_rows_raw": len(binary),
        "binary_label_counts_raw": dict(binary_counts),
        "binary_label_counts_weighted": weighted_label_counts(binary),
        "by_stratum_raw": {k: dict(v) for k, v in sorted(by_stratum.items())},
        "blank_labels": len(blanks),
        "notes": [
            "ABSTENTION should be excluded from binary metrics and reported separately.",
            "Use sampling_weight for weighted tranche metrics.",
            "No evaluated model was used for sampling.",
        ],
    }

    save_json(args.summary, summary)

    print("\nImported grounded-hard random review labels")
    print("=" * 72)
    print(f"Rows total:             {len(updated)}")
    print(f"Label counts raw:       {dict(label_counts)}")
    print(f"Label counts weighted:  {summary['label_counts_weighted']}")
    print(f"Binary rows raw:        {len(binary)}")
    print(f"Binary counts raw:      {dict(binary_counts)}")
    print(f"Binary counts weighted: {summary['binary_label_counts_weighted']}")
    print("\nWrote:")
    print(f"  {args.out_jsonl}")
    print(f"  {args.summary}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ex = sub.add_parser("export")
    ex.add_argument("--claims", type=Path, default=Path("grounded_hard_claims.json"))
    ex.add_argument("--out-md", type=Path, default=Path("grounded_hard_random_review.md"))
    ex.add_argument("--out-jsonl", type=Path, default=Path("grounded_hard_random_review.jsonl"))
    ex.add_argument("--report", type=Path, default=Path("grounded_hard_random_review_sampling_report.json"))
    ex.add_argument("--target-n", type=int, default=150)
    ex.add_argument("--seed", type=int, default=2908)
    ex.set_defaults(func=export_cmd)

    im = sub.add_parser("import-labels")
    im.add_argument("--md", type=Path, default=Path("grounded_hard_random_review.md"))
    im.add_argument("--jsonl", type=Path, default=Path("grounded_hard_random_review.jsonl"))
    im.add_argument("--out-jsonl", type=Path, default=Path("grounded_hard_random_review_labeled.jsonl"))
    im.add_argument("--summary", type=Path, default=Path("grounded_hard_random_review_labeled_summary.json"))
    im.add_argument("--allow-blanks", action="store_true")
    im.set_defaults(func=import_cmd)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
