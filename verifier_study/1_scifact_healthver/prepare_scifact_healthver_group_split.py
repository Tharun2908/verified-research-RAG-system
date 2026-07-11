from __future__ import annotations

import ast
import json
import os
import random
from collections import Counter, defaultdict

from datasets import load_dataset

OUT_DIR = "/workspace/project3/data_grouped"
os.makedirs(OUT_DIR, exist_ok=True)

SEED = 42
TRAIN_FRAC = 0.80
VAL_FRAC = 0.10
TEST_FRAC = 0.10

VERDICT_TO_LABEL = {
    "SUPPORT": 0,
    "CONTRADICT": 1,
    "NEI": 1,
}


def normalize_abstract(x) -> str:
    """
    Abstract may be:
      - a real list of sentences
      - a stringified list like "['s1', 's2']"
      - plain text

    Return one joined text string.
    """
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

    claim_id = str(ex.get("claim_id", ""))
    abstract_id = str(ex.get("abstract_id", ""))

    return {
        "id": f"{source}_{split}_{i}_{claim_id}_{abstract_id}",
        "answer": ex["claim"].strip(),
        "context": normalize_abstract(ex["abstract"]).strip(),
        "label": label,
        "verdict": verdict,
        "source": source,
        "orig_split": split,
        "claim_id": claim_id,
        "abstract_id": abstract_id,
    }


class DSU:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x

        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]

        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra != rb:
            self.parent[rb] = ra


def load_all_records():
    print("Loading SciFact...")
    sf = load_dataset("allenai/scifact_entailment")

    print("Loading HealthVer...")
    hv = load_dataset("dwadden/healthver_entailment", trust_remote_code=True)

    records = []

    # SciFact has train + validation
    for split in ["train", "validation"]:
        for i, ex in enumerate(sf[split]):
            records.append(convert(ex, "scifact", split, i))

    # HealthVer has train + validation + test
    for split in ["train", "validation", "test"]:
        for i, ex in enumerate(hv[split]):
            records.append(convert(ex, "healthver", split, i))

    return records


def build_components(records):
    """
    Build connected components over claim_id and abstract_id, scoped by source.

    This prevents leakage where:
      - the same claim appears in multiple splits
      - the same evidence abstract appears in multiple splits
      - a chain of claim/abstract links indirectly connects examples
    """
    dsu = DSU()

    for r in records:
        claim_key = f"{r['source']}::claim::{r['claim_id']}"
        abs_key = f"{r['source']}::abstract::{r['abstract_id']}"
        dsu.union(claim_key, abs_key)

    comp_to_records = defaultdict(list)

    for r in records:
        claim_key = f"{r['source']}::claim::{r['claim_id']}"
        root = dsu.find(claim_key)
        comp_to_records[root].append(r)

    return list(comp_to_records.values())


def component_source(component):
    sources = {r["source"] for r in component}

    if len(sources) != 1:
        raise ValueError(f"Component contains multiple sources: {sources}")

    return next(iter(sources))


def split_one_source_components(source: str, components: list[list[dict]]):
    """
    Split connected components for one source into train/val/test.

    The split is grouped, so no component can be split across train/val/test.
    Large components can make exact 80/10/10 impossible, so this uses a greedy
    target-size assignment.
    """
    rng = random.Random(SEED)

    comps = components[:]
    rng.shuffle(comps)
    comps.sort(key=len, reverse=True)

    total = sum(len(c) for c in comps)

    targets = {
        "train": TRAIN_FRAC * total,
        "val": VAL_FRAC * total,
        "test": TEST_FRAC * total,
    }

    buckets = {
        "train": [],
        "val": [],
        "test": [],
    }

    sizes = {
        "train": 0,
        "val": 0,
        "test": 0,
    }

    for comp in comps:
        deficits = {
            split: targets[split] - sizes[split]
            for split in ["train", "val", "test"]
        }

        chosen = max(deficits, key=deficits.get)
        buckets[chosen].extend(comp)
        sizes[chosen] += len(comp)

    print(f"\nSource-stratified split for {source}:")
    print(f"  total={total}")
    print(f"  train={sizes['train']} val={sizes['val']} test={sizes['test']}")

    return buckets["train"], buckets["val"], buckets["test"]


def split_components_source_stratified(components):
    """
    Source-stratified grouped split.

    We split SciFact components and HealthVer components separately, then merge.
    This preserves:
      - no claim_id leakage
      - no abstract_id leakage
      - more balanced SciFact/HealthVer proportions across train/val/test
    """
    final_train = []
    final_val = []
    final_test = []

    sources = sorted({component_source(c) for c in components})

    for source in sources:
        source_components = [
            c for c in components
            if component_source(c) == source
        ]

        tr, va, te = split_one_source_components(source, source_components)

        final_train.extend(tr)
        final_val.extend(va)
        final_test.extend(te)

    return final_train, final_val, final_test


def keyset(records, field):
    return {
        (r["source"], r[field])
        for r in records
        if r[field]
    }


def verify_no_overlap(train, val, test):
    ok = True

    for field in ["claim_id", "abstract_id"]:
        comparisons = [
            ("train", train, "val", val),
            ("train", train, "test", test),
            ("val", val, "test", test),
        ]

        for a_name, a_records, b_name, b_records in comparisons:
            inter = keyset(a_records, field) & keyset(b_records, field)

            if inter:
                ok = False
                print(
                    f"WARNING: {field}: {a_name} <-> {b_name}: "
                    f"{len(inter)} overlaps"
                )

    if ok:
        print("OK — no claim_id or abstract_id overlaps across train/val/test.")

    return ok


def summarize(name, records):
    n = len(records)
    lab = Counter(r["label"] for r in records)
    ver = Counter(r["verdict"] for r in records)
    src = Counter(r["source"] for r in records)
    orig = Counter((r["source"], r["orig_split"]) for r in records)

    print(f"\n{name}: {n} examples")

    if n == 0:
        return

    pos = lab.get(1, 0)

    print(
        f"  label: supported(0)={lab.get(0, 0)} "
        f"unsupported(1)={pos} "
        f"pos_rate={100 * pos / n:.1f}%"
    )
    print(f"  verdict: {dict(ver)}")
    print(f"  source: {dict(src)}")
    print(f"  orig_split: {dict(orig)}")


def write_json(fname, records):
    path = os.path.join(OUT_DIR, fname)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(records)} -> {path}")


def main():
    records = load_all_records()

    print(f"\nLoaded total records: {len(records)}")

    components = build_components(records)
    comp_sizes = [len(c) for c in components]

    print(f"Connected components: {len(components)}")
    print(
        f"Component size max={max(comp_sizes)}, "
        f"mean={sum(comp_sizes) / len(comp_sizes):.2f}"
    )

    train, val, test = split_components_source_stratified(components)

    print("\n=== OVERLAP CHECK ===")
    verify_no_overlap(train, val, test)

    summarize("TRAIN_GROUPED_SOURCE_STRAT", train)
    summarize("VAL_GROUPED_SOURCE_STRAT", val)
    summarize("TEST_GROUPED_SOURCE_STRAT", test)

    print("\n=== WRITING FILES ===")
    write_json("verifier_train_grouped.json", train)
    write_json("verifier_val_grouped.json", val)
    write_json("verifier_test_grouped.json", test)

    print("\nUse these for fine-tuning:")
    print(f"  train: {OUT_DIR}/verifier_train_grouped.json")
    print(f"  val:   {OUT_DIR}/verifier_val_grouped.json")
    print(f"  test:  {OUT_DIR}/verifier_test_grouped.json")


if __name__ == "__main__":
    main()
