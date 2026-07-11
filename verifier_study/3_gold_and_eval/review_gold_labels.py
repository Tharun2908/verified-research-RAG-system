"""
backend/app/services/review_gold_labels.py

STEP 1.4: HUMAN REVIEW pass — turns Opus drafts into the GOLD eval set.

This is the step that makes the set credible. A human (you) confirms or overrides every
draft label. To avoid automation bias (rubber-stamping the model), the tool shows you the
CLAIM + EVIDENCE and asks for YOUR call FIRST, then reveals the draft and flags disagreements.

Reads  data/gold_drafted.json   (draft_label + draft_rationale, final_label=None)
Writes data/gold_drafted.json   (in place: sets final_label + human_confirmed per record)
       data/gold_eval.json       (FROZEN gold set, written at the end — final_label only)

Resumable: saves after every claim. Re-run to continue where you left off.
Skips records already human_confirmed.

Controls per claim:
    s = SUPPORTED, u = UNSUPPORTED, a = ABSTENTION   (your judgment, entered BEFORE seeing draft)
    (after your call, the draft is revealed; press Enter to keep your call, or re-enter to change)
    q = save and quit
    b = go back one (re-review previous)

USAGE (from backend/):
    python -m app.services.review_gold_labels
"""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path("data")
DRAFT = DATA / "gold_drafted.json"
GOLD = DATA / "gold_eval.json"

LABELS = {"s": "SUPPORTED", "u": "UNSUPPORTED", "a": "ABSTENTION"}


def load():
    with open(DRAFT, encoding="utf-8") as f:
        return json.load(f)


def save(records):
    with open(DRAFT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def freeze_gold(records):
    """Write the final frozen gold set — only human-confirmed final labels."""
    gold = []
    for r in records:
        if r.get("human_confirmed") and r.get("final_label"):
            gold.append({
                "key": r.get("key"),
                "qid": r["qid"],
                "arm": r["arm"],
                "claim_index": r["claim_index"],
                "claim_text": r["claim_text"],
                "evidence_text": r["evidence_text"],
                "gold_label": r["final_label"],
            })
    with open(GOLD, "w", encoding="utf-8") as f:
        json.dump(gold, f, ensure_ascii=False, indent=2)
    return len(gold)


def ask_label(prompt):
    while True:
        v = input(prompt).strip().lower()
        if v in LABELS:
            return LABELS[v]
        if v in {"q", "b", ""}:
            return v
        print("    enter s / u / a  (or q=quit, b=back)")


def propagate_to_twins(records, idx, label):
    """Apply `label` to any OTHER record with identical claim_text + evidence_text.
    Returns the number of twins updated. Marks them auto-propagated for transparency."""
    src = records[idx]
    ct, et = src["claim_text"], src["evidence_text"]
    n = 0
    for j, r in enumerate(records):
        if j == idx:
            continue
        if r.get("human_confirmed"):
            continue
        if r["claim_text"] == ct and r["evidence_text"] == et:
            r["final_label"] = label
            r["human_confirmed"] = True
            r["auto_propagated_from"] = src.get("key")
            n += 1
    return n


def main():
    records = load()
    total = len(records)

    # find where to resume
    i = 0
    while i < total and records[i].get("human_confirmed"):
        i += 1

    agree = sum(1 for r in records
                if r.get("human_confirmed") and r.get("final_label") == r.get("draft_label"))
    override = sum(1 for r in records
                   if r.get("human_confirmed") and r.get("final_label") != r.get("draft_label"))

    print(f"Gold review — {total} claims. Resuming at #{i+1}. "
          f"(so far: {agree} agreed, {override} overridden)\n")
    print("For each: read CLAIM + EVIDENCE, enter YOUR label, THEN the draft is revealed.\n")

    while i < total:
        r = records[i]
        if r.get("human_confirmed"):
            i += 1
            continue

        reason = r.get("_meta", {}).get("selection_reasons") if "_meta" in r else None
        print("=" * 70)
        print(f"[{i+1}/{total}]  key={r.get('key')}  arm={r['arm']}")
        print("-" * 70)
        print("EVIDENCE:")
        print("  " + r["evidence_text"][:700].replace("\n", "\n  "))
        print("\nCLAIM:")
        print("  " + r["claim_text"])
        print("-" * 70)

        # YOUR call first (anti-anchoring)
        your = ask_label("YOUR label [s/u/a]  (q=quit, b=back): ")
        if your == "q":
            break
        if your == "b":
            # step back to last confirmed and clear it
            j = i - 1
            while j >= 0 and not records[j].get("human_confirmed"):
                j -= 1
            if j >= 0:
                records[j]["human_confirmed"] = False
                records[j]["final_label"] = None
                i = j
            continue
        if your == "":
            continue

        # reveal the draft
        draft = r.get("draft_label")
        match = "AGREE" if your == draft else ">>> DISAGREE <<<"
        print(f"\n  your call:  {your}")
        print(f"  Opus draft: {draft}   [{match}]")
        print(f"  Opus reason: {r.get('draft_rationale','')}")

        final = your
        if your != draft:
            # on disagreement, force a deliberate confirm
            c = input("  keep YOUR call? [Enter=yes, or s/u/a to change]: ").strip().lower()
            if c in LABELS:
                final = LABELS[c]

        r["final_label"] = final
        r["human_confirmed"] = True
        n_twins = propagate_to_twins(records, i, final)
        save(records)
        if n_twins:
            print(f"  -> recorded: {final}  (+{n_twins} identical twin(s) auto-labeled)\n")
        else:
            print(f"  -> recorded: {final}\n")
        i += 1

    # stats + freeze
    confirmed = [r for r in records if r.get("human_confirmed")]
    agree = sum(1 for r in confirmed if r["final_label"] == r.get("draft_label"))
    override = len(confirmed) - agree
    dist = {}
    for r in confirmed:
        dist[r["final_label"]] = dist.get(r["final_label"], 0) + 1

    n_gold = freeze_gold(records)
    print("=" * 70)
    print(f"Reviewed {len(confirmed)}/{total}. Agreed with Opus: {agree}, overrode: {override}.")
    print("Final gold label distribution:")
    for lab, n in sorted(dist.items()):
        print(f"  {lab:14s} {n}")
    print(f"\nFroze {n_gold} confirmed labels to {GOLD}.")
    if len(confirmed) < total:
        print(f"({total - len(confirmed)} left — re-run to continue.)")


if __name__ == "__main__":
    main()
