from __future__ import annotations

import ast
import json
import os
from collections import Counter

from datasets import load_dataset

OUT_DIR = "/workspace/project3/data"
os.makedirs(OUT_DIR, exist_ok=True)

VERDICT_TO_LABEL = {"SUPPORT": 0, "CONTRADICT": 1, "NEI": 1}


def normalize_abstract(x) -> str:
    """Abstract may be a real list, or a stringified list like "['s1', 's2']". Join to text."""
    if isinstance(x, list):
        return " ".join(str(s) for s in x)
    if isinstance(x, str):
        try:
            parsed = ast.literal_eval(x)
            if isinstance(parsed, list):
                return " ".join(str(s) for s in parsed)
        except (ValueError, SyntaxError):
            pass
        return x
    return str(x)


def convert(ex, source: str, split: str, i: int) -> dict:
    verdict = ex["verdict"]
    label = VERDICT_TO_LABEL[verdict]
    return {
        "id": f"{source}_{split}_{i}_{ex.get('claim_id','?')}_{ex.get('abstract_id','?')}",
        "answer": ex["claim"].strip(),
        "context": normalize_abstract(ex["abstract"]).strip(),
        "label": label,
        "verdict": verdict,
        "source": source,
        "split": split,
        "claim_id": str(ex.get("claim_id", "")),
        "abstract_id": str(ex.get("abstract_id", "")),
    }


def load_all():
    print("Loading SciFact (allenai/scifact_entailment)...")
    sf = load_dataset("allenai/scifact_entailment")

    print("Loading HealthVer (dwadden/healthver_entailment)...")
    hv = load_dataset("dwadden/healthver_entailment", trust_remote_code=True)

    train, val, test = [], [], []

    for i, ex in enumerate(sf["train"]):
        train.append(convert(ex, "scifact", "train", i))
    for i, ex in enumerate(sf["validation"]):
        val.append(convert(ex, "scifact", "validation", i))

    for i, ex in enumerate(hv["train"]):
        train.append(convert(ex, "healthver", "train", i))
    for i, ex in enumerate(hv["validation"]):
        val.append(convert(ex, "healthver", "validation", i))
    for i, ex in enumerate(hv["test"]):
        test.append(convert(ex, "healthver", "test", i))

    return train, val, test


def keyset(records, field: str):
    return {(r["source"], r[field]) for r in records if r[field]}


def overlap_report(a_name, a, b_name, b):
    rows = []
    for field in ["claim_id", "abstract_id"]:
        inter = keyset(a, field) & keyset(b, field)
        rows.append((field, a_name, b_name, len(inter)))
    return rows


def print_overlap_report(train, val, test, title):
    print(f"\n=== {title} ===")
    rows = []
    rows.extend(overlap_report("train", train, "val", val))
    rows.extend(overlap_report("train", train, "test", test))
    rows.extend(overlap_report("val", val, "test", test))

    any_overlap = False
    for field, a, b, n in rows:
        if n:
            any_overlap = True
            print(f"  WARNING: {field}: {a} <-> {b}: {n} shared IDs")

    if not any_overlap:
        print("  OK — no claim_id or abstract_id overlaps across splits.")


def make_clean_eval_splits(train, val, test):
    """
    Keep native train unchanged.
    Filter val/test so evaluation examples use unseen claims and unseen evidence documents.

    Strict policy:
      - val_clean removes anything sharing claim_id or abstract_id with train
      - test_clean removes anything sharing claim_id or abstract_id with train or val_clean
    """
    train_claims = keyset(train, "claim_id")
    train_abs = keyset(train, "abstract_id")

    val_clean = [
        r for r in val
        if (r["source"], r["claim_id"]) not in train_claims
        and (r["source"], r["abstract_id"]) not in train_abs
    ]

    val_claims = keyset(val_clean, "claim_id")
    val_abs = keyset(val_clean, "abstract_id")

    test_clean = [
        r for r in test
        if (r["source"], r["claim_id"]) not in train_claims
        and (r["source"], r["abstract_id"]) not in train_abs
        and (r["source"], r["claim_id"]) not in val_claims
        and (r["source"], r["abstract_id"]) not in val_abs
    ]

    return val_clean, test_clean


def summarize(name, records):
    n = len(records)
    lab = Counter(r["label"] for r in records)
    src = Counter(r["source"] for r in records)
    ver = Counter(r["verdict"] for r in records)

    print(f"\n{name}: {n} examples")
    if n == 0:
        return

    pos = lab.get(1, 0)
    print(
        f"  label:   supported(0)={lab.get(0,0)}  unsupported(1)={pos}  "
        f"(positive/unsupported rate {100*pos/n:.1f}%)"
    )
    print(f"  source:  {dict(src)}")
    print(f"  verdict: {dict(ver)}")


def write_json(fname, records):
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(records)} -> {path}")


def main():
    train, val_raw, test_raw = load_all()

    print_overlap_report(train, val_raw, test_raw, "RAW SPLIT OVERLAP CHECK")

    val_clean, test_clean = make_clean_eval_splits(train, val_raw, test_raw)

    print_overlap_report(train, val_clean, test_clean, "CLEAN SPLIT OVERLAP CHECK")

    summarize("TRAIN", train)
    summarize("VAL_RAW", val_raw)
    summarize("VAL_CLEAN", val_clean)
    summarize("HEALTHVER_TEST_RAW", test_raw)
    summarize("HEALTHVER_TEST_CLEAN", test_clean)

    print("\n=== WRITING FILES ===")

    # Training file: native train, unchanged.
    write_json("verifier_train.json", train)

    # Raw eval files: saved for transparency/debugging, not for final claims.
    write_json("verifier_val_raw.json", val_raw)
    write_json("verifier_healthver_test_raw.json", test_raw)

    # Clean eval files: use these for model selection / final evaluation.
    write_json("verifier_val_clean.json", val_clean)
    write_json("verifier_healthver_test_clean.json", test_clean)

    print("\nUse for training:")
    print("  train: /workspace/project3/data/verifier_train.json")
    print("  val:   /workspace/project3/data/verifier_val_clean.json")
    print("  test:  /workspace/project3/data/verifier_healthver_test_clean.json")


if __name__ == "__main__":
    main()
