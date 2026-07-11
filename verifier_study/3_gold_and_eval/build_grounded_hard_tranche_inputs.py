"""
build_grounded_hard_tranche_inputs.py

Build a model-independent grounded-hard generation tranche from existing protected
gold-side arXiv eval inputs.

This script DOES NOT use S2/S4/fusion predictions. It only uses existing question/evidence
artifacts as a protected-paper seed pool and creates new questions + censored evidence variants.

Input expected on cluster:
  gold_eval_inputs.json

Output:
  grounded_hard_eval_inputs.json
  grounded_hard_input_build_report.json

Run from /workspace/project3:
  python -u build_grounded_hard_tranche_inputs.py \
    --in gold_eval_inputs.json \
    --out grounded_hard_eval_inputs.json \
    --report grounded_hard_input_build_report.json \
    --max-inputs 160 \
    --seed 2908

Then generate answers:
  nohup python -u generate_batch.py \
    --in grounded_hard_eval_inputs.json \
    --out grounded_hard_answers.json \
    --max-new 400 \
    > grounded_hard_generation.log 2>&1 &
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


QUESTION_TEMPLATES = [
    (
        "method_scope",
        "What method, system, or framework is introduced in the paper '{title}', and what problem is it designed to address?",
    ),
    (
        "dataset_benchmark",
        "What datasets, benchmarks, or evaluation settings are described in the paper '{title}'?",
    ),
    (
        "results_comparison",
        "What main experimental results or comparisons are reported in the paper '{title}'?",
    ),
    (
        "limitations_ablation",
        "What limitations, ablations, or analysis findings are discussed in the paper '{title}'?",
    ),
]

POLICY_ORDER = [
    "home_weak_1",
    "home_weak_plus_distractors",
    "drop_home_related",
    "remove_strongest",
]


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_title(s: Any) -> str:
    s = str(s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def stable_int(s: str, mod: int = 10**9) -> int:
    h = hashlib.sha1(s.encode("utf-8")).hexdigest()
    return int(h[:12], 16) % mod


def evidence_pid(e: dict[str, Any]) -> str:
    for k in ["resolved_corpus_paper_id", "corpus_paper_id", "paper_id", "id"]:
        if e.get(k) is not None and str(e.get(k)).strip():
            return str(e[k])
    return ""


def evidence_title(e: dict[str, Any]) -> str:
    return str(e.get("title") or "").strip()


def is_home_evidence(e: dict[str, Any], home_pid: str, home_title: str) -> bool:
    pid = evidence_pid(e)
    if home_pid and pid == home_pid:
        return True
    if home_title and norm_title(evidence_title(e)) == norm_title(home_title):
        return True
    return False


def clean_evidence_item(e: dict[str, Any], number: int, rank: int) -> dict[str, Any]:
    out = dict(e)
    out["number"] = number
    out["rank"] = rank
    return out


def get_home_pid(row: dict[str, Any]) -> str:
    for k in ["home_corpus_paper_id", "home_paper_id", "corpus_paper_id", "paper_id"]:
        if row.get(k) is not None and str(row.get(k)).strip():
            return str(row[k])
    # fallback: find first evidence pid whose title matches home_title
    home_title = str(row.get("home_title") or "").strip()
    for e in row.get("evidence", []) or []:
        if norm_title(evidence_title(e)) == norm_title(home_title):
            return evidence_pid(e)
    return ""


def get_home_title(row: dict[str, Any]) -> str:
    if row.get("home_title"):
        return str(row["home_title"]).strip()
    ev = row.get("evidence", []) or []
    if ev:
        return evidence_title(ev[0])
    return "the target paper"


def unique_seed_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Keep diverse protected-paper seeds. If several rows have the same home paper, keep up to
    two because their evidence neighborhoods may differ.
    """
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        home_pid = get_home_pid(r)
        home_title = get_home_title(r)
        key = home_pid or norm_title(home_title)
        if not key:
            key = str(r.get("qid") or r.get("id") or len(buckets))
        buckets[key].append(r)

    seeds = []
    for key, items in sorted(buckets.items(), key=lambda kv: kv[0]):
        seeds.extend(items[:2])
    return seeds


def select_evidence(row: dict[str, Any], policy: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ev = list(row.get("evidence", []) or [])
    ev = [e for e in ev if str(e.get("text") or "").strip()]
    ev = sorted(ev, key=lambda e: (int(e.get("rank") or e.get("raw_rank") or 9999), -float(e.get("score") or 0.0)))

    home_pid = get_home_pid(row)
    home_title = get_home_title(row)

    home = [e for e in ev if is_home_evidence(e, home_pid, home_title)]
    non_home = [e for e in ev if not is_home_evidence(e, home_pid, home_title)]

    selected: list[dict[str, Any]] = []
    meta = {
        "policy": policy,
        "home_pid": home_pid,
        "home_title": home_title,
        "available_evidence": len(ev),
        "available_home_chunks": len(home),
        "available_non_home_chunks": len(non_home),
    }

    if policy == "home_weak_1":
        if not home:
            return [], {**meta, "drop_reason": "no_home_chunk"}
        selected = home[:1]

    elif policy == "home_weak_plus_distractors":
        if not home:
            return [], {**meta, "drop_reason": "no_home_chunk"}
        selected = home[:1] + non_home[:2]
        if len(selected) < 2:
            return [], {**meta, "drop_reason": "not_enough_distractors"}

    elif policy == "drop_home_related":
        selected = non_home[:3]
        if len(selected) < 2:
            return [], {**meta, "drop_reason": "not_enough_non_home"}

    elif policy == "remove_strongest":
        if len(ev) < 2:
            return [], {**meta, "drop_reason": "not_enough_evidence"}
        selected = ev[1:4]
        if len(selected) < 2:
            return [], {**meta, "drop_reason": "not_enough_after_drop"}

    else:
        raise ValueError(f"Unknown policy: {policy}")

    selected = [clean_evidence_item(e, number=i + 1, rank=i + 1) for i, e in enumerate(selected)]
    meta["selected_evidence"] = len(selected)
    meta["selected_home_chunks"] = sum(1 for e in selected if is_home_evidence(e, home_pid, home_title))
    meta["selected_non_home_chunks"] = len(selected) - meta["selected_home_chunks"]
    meta["selected_titles"] = [evidence_title(e) for e in selected]
    meta["selected_pids"] = [evidence_pid(e) for e in selected]
    return selected, meta


def build_inputs(seed_rows: list[dict[str, Any]], max_inputs: int, seed: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(seed)

    candidates = []
    drops = []
    seen_questions = set()

    for seed_idx, row in enumerate(seed_rows, start=1):
        home_pid = get_home_pid(row)
        home_title = get_home_title(row)

        # Shuffle template/policy pairing per seed to avoid identical ordering artifacts.
        templates = QUESTION_TEMPLATES[:]
        policies = POLICY_ORDER[:]
        rng.shuffle(templates)
        rng.shuffle(policies)

        for ti, (template_name, template) in enumerate(templates):
            policy = policies[ti % len(policies)]
            question = template.format(title=home_title)
            qkey = (norm_title(home_title), template_name, policy)
            if qkey in seen_questions:
                continue
            seen_questions.add(qkey)

            selected, meta = select_evidence(row, policy)
            if not selected:
                drops.append({
                    "seed_idx": seed_idx,
                    "source_qid": row.get("qid") or row.get("id"),
                    "home_pid": home_pid,
                    "home_title": home_title,
                    "template_name": template_name,
                    "policy": policy,
                    **meta,
                })
                continue

            candidates.append({
                "_source_row": row,
                "_template_name": template_name,
                "_policy": policy,
                "_policy_meta": meta,
                "home_pid": home_pid,
                "home_title": home_title,
                "question": question,
                "evidence": selected,
            })

    # Prioritize policies that are likely to produce grounded-hard overclaims.
    # Still include all policies for spectrum.
    policy_priority = {
        "home_weak_plus_distractors": 0,
        "home_weak_1": 1,
        "remove_strongest": 2,
        "drop_home_related": 3,
    }
    rng.shuffle(candidates)
    candidates.sort(key=lambda c: (policy_priority.get(c["_policy"], 99), stable_int(c["question"] + c["_policy"])))

    if max_inputs and len(candidates) > max_inputs:
        candidates = candidates[:max_inputs]

    out = []
    for i, c in enumerate(candidates, start=1):
        source = c["_source_row"]
        out.append({
            "id": i,
            "qid": i,
            "split": "grounded_hard_tranche",
            "type": "grounded_hard",
            "question": c["question"],
            "home_paper_id": c["home_pid"],
            "home_corpus_paper_id": c["home_pid"],
            "home_title": c["home_title"],
            "source": "protected_gold_side_grounded_hard",
            "search_k": None,
            "evidence_k": len(c["evidence"]),
            "home_forced_into_selected_evidence": False,
            "hard_policy": c["_policy"],
            "question_template": c["_template_name"],
            "source_gold_qid": source.get("qid") or source.get("id"),
            "construction_notes": (
                "Model-independent grounded-hard tranche. S2/S4/fusion predictions were not used. "
                "Evidence was censored/weakened before generation."
            ),
            "policy_meta": c["_policy_meta"],
            "evidence": c["evidence"],
        })

    report = {
        "input_seed_rows": len(seed_rows),
        "candidate_inputs_before_cap": len(candidates) + max(0, 0),
        "output_inputs": len(out),
        "max_inputs": max_inputs,
        "seed": seed,
        "policy_counts": dict(Counter(x["hard_policy"] for x in out)),
        "template_counts": dict(Counter(x["question_template"] for x in out)),
        "home_paper_count": len(set(str(x["home_corpus_paper_id"]) or norm_title(x["home_title"]) for x in out)),
        "drop_count": len(drops),
        "drop_reasons": dict(Counter(d.get("drop_reason", "unknown") for d in drops)),
        "drops_sample": drops[:20],
        "no_evaluated_model_used_for_sampling": True,
        "warning": (
            "Questions are templated from protected gold-side paper titles and paired with "
            "weakened/censored evidence. This is an enriched stress tranche, not a natural "
            "user-query distribution."
        ),
    }

    return out, report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", type=Path, default=Path("gold_eval_inputs.json"))
    ap.add_argument("--out", type=Path, default=Path("grounded_hard_eval_inputs.json"))
    ap.add_argument("--report", type=Path, default=Path("grounded_hard_input_build_report.json"))
    ap.add_argument("--max-inputs", type=int, default=160)
    ap.add_argument("--seed", type=int, default=2908)
    args = ap.parse_args()

    rows = load_json(args.in_path)
    if not isinstance(rows, list):
        raise SystemExit(f"{args.in_path} must be a JSON list.")

    seed_rows = unique_seed_rows(rows)
    out, report = build_inputs(seed_rows, max_inputs=args.max_inputs, seed=args.seed)

    save_json(args.out, out)
    save_json(args.report, report)

    print("\nBuilt grounded-hard tranche inputs")
    print("=" * 72)
    print(f"Input rows:          {len(rows)}")
    print(f"Seed rows:           {len(seed_rows)}")
    print(f"Output inputs:       {len(out)}")
    print(f"Home papers:         {report['home_paper_count']}")
    print(f"Policy counts:       {report['policy_counts']}")
    print(f"Template counts:     {report['template_counts']}")
    print(f"Drop count:          {report['drop_count']}")
    print(f"Drop reasons:        {report['drop_reasons']}")
    print("\nExample:")
    if out:
        ex = out[0]
        print(json.dumps({
            "qid": ex["qid"],
            "question": ex["question"],
            "home_title": ex["home_title"],
            "hard_policy": ex["hard_policy"],
            "question_template": ex["question_template"],
            "evidence_titles": [e.get("title") for e in ex["evidence"]],
            "evidence_count": len(ex["evidence"]),
        }, ensure_ascii=False, indent=2))
    print("\nWrote:")
    print(f"  {args.out}")
    print(f"  {args.report}")


if __name__ == "__main__":
    main()
