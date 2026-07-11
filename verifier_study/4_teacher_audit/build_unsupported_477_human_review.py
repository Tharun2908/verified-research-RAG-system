#!/usr/bin/env python
"""
Build a blind human-review file for Opus disagreements among the 477 original
UNSUPPORTED rows, then rebuild cleaned train/validation files without changing
qid membership.

Labels:
SUPPORTED, UNSUPPORTED, ABSTENTION, INVALID_EXTRACTION
"""

from __future__ import annotations
import argparse, json, re
from collections import Counter
from pathlib import Path

ALLOWED = {"SUPPORTED","UNSUPPORTED","ABSTENTION","INVALID_EXTRACTION"}

def load_json(p):
    return json.load(open(p, encoding="utf-8"))

def read_jsonl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]

def write_jsonl(p, rows):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def save_json(p, obj):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(obj, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def cid(r):
    return str(r["claim_id"])

def txt(x):
    return str(x or "").strip()

def ev(r):
    return txt(r.get("evidence_text_for_verifier") or r.get("evidence_text"))

def norm_label(x):
    s = str(x or "").strip().upper().strip("`*_ ")
    s = re.sub(r"[^A-Z_]", "", s.replace("-", "_").replace(" ", "_"))
    return s if s in ALLOWED else ""

def export(args):
    audit = load_json(args.audit)
    disagree = [dict(r) for r in audit if str(r.get("opus_label","")).upper() != "UNSUPPORTED"]
    manifest = []
    lines = [
        "# Blind Human Review — Original UNSUPPORTED Rows Flagged by Independent Audit",
        "",
        "Fill `FINAL_LABEL` with exactly one of:",
        "`SUPPORTED`, `UNSUPPORTED`, `ABSTENTION`, `INVALID_EXTRACTION`.",
        "",
        "The Opus draft label is intentionally hidden.",
        "",
        "---",""
    ]
    for i, r in enumerate(disagree, 1):
        rr = dict(r)
        rr["review_id"] = f"UPR{i:04d}"
        manifest.append(rr)
        lines += [
            f"## {rr['review_id']} — {cid(rr)}","",
            "**FINAL_LABEL:** ","",
            "**FINAL_NOTES:** ","",
            "### Metadata","",
            f"- source_split: `{rr.get('audit_source_split')}`",
            f"- qid: `{rr.get('qid')}`",
            f"- answer_variant: `{rr.get('answer_variant')}`",
            f"- evidence_scope: `{rr.get('evidence_scope')}`","",
            "### Question","",txt(rr.get("question")),"",
            "### Claim","",txt(rr.get("claim") or rr.get("claim_text")),"",
            "### Evidence","","```text",ev(rr),"```","","---",""
        ]
    Path(args.out_md).write_text("\n".join(lines), encoding="utf-8")
    write_jsonl(args.out_jsonl, manifest)
    counts = Counter(str(r.get("opus_label","")).upper() for r in audit)
    save_json(args.summary, {
        "audit_rows_total": len(audit),
        "opus_label_counts": dict(counts),
        "human_review_rows": len(manifest),
        "review_is_blind_to_opus_label": True,
        "retrain_trigger_rows": 96,
        "opus_flagged_rows": len(manifest),
        "trigger_reached_by_opus_draft": len(manifest) >= 96
    })
    print("Audit rows:", len(audit))
    print("Human-review rows:", len(manifest))
    print("Opus counts:", dict(counts))
    print("Wrote:", args.out_md, args.out_jsonl, args.summary)

def field(section, name):
    m = re.search(rf"(?:\*\*)?{re.escape(name)}\s*:\s*(?:\*\*)?\s*", section, re.I)
    if not m:
        return ""
    rest = section[m.end():]
    stops = [
        r"\n\s*(?:\*\*)?FINAL_LABEL\s*:",
        r"\n\s*(?:\*\*)?FINAL_NOTES\s*:",
        r"\n\s*###\s+Metadata", r"\n\s*###\s+Question",
        r"\n\s*###\s+Claim", r"\n\s*###\s+Evidence",
        r"\n\s*---\s*", r"\n\s*##\s+UPR\d+"
    ]
    end = len(rest)
    for pat in stops:
        q = re.search(pat, rest, re.I)
        if q: end = min(end, q.start())
    return rest[:end].strip()

def parse_md(p):
    s = Path(p).read_text(encoding="utf-8")
    pat = re.compile(r"^##\s+(UPR\d+)\s+—\s+([^\s]+)\s*$", re.M)
    ms = list(pat.finditer(s))
    out = {}
    for i,m in enumerate(ms):
        sec = s[m.end() : (ms[i+1].start() if i+1 < len(ms) else len(s))]
        out[m.group(1)] = {
            "claim_id": m.group(2),
            "final_label": norm_label(field(sec,"FINAL_LABEL")),
            "final_notes": field(sec,"FINAL_NOTES")
        }
    return out

def import_clean(args):
    manifest = read_jsonl(args.manifest)
    parsed = parse_md(args.md)
    audit = load_json(args.audit)
    train = read_jsonl(args.train)
    val = read_jsonl(args.val)

    human = {}
    notes = {}
    blanks = []
    for r in manifest:
        rid, c = r["review_id"], cid(r)
        p = parsed.get(rid)
        if not p or p["claim_id"] != c or not p["final_label"]:
            blanks.append(rid); continue
        human[c] = p["final_label"]
        notes[c] = p["final_notes"]
    if blanks:
        raise SystemExit(f"Blank/missing/mismatched labels for {len(blanks)} rows: {blanks[:20]}")

    final_pos = {}
    reviewed_ids = set(human)
    for r in audit:
        c = cid(r)
        if c in human:
            final_pos[c] = human[c]
        elif str(r.get("opus_label","")).upper() == "UNSUPPORTED":
            final_pos[c] = "UNSUPPORTED"
        else:
            raise SystemExit(f"Unreviewed Opus disagreement: {c}")

    def rebuild(rows, split):
        kept, removed = [], []
        for r in rows:
            rr = dict(r)
            if int(rr["label"]) == 0:
                lab = "SUPPORTED"
                src = "original_supported_unchanged"
            else:
                lab = final_pos[cid(rr)]
                src = "human_adjudicated" if cid(rr) in reviewed_ids else "teacher_and_opus_agreed_unsupported"
            rr["cleaning_final_label_name"] = lab
            rr["cleaning_label_source"] = src
            rr["cleaning_source_split"] = split
            if cid(rr) in notes:
                rr["cleaning_human_notes"] = notes[cid(rr)]
            if lab == "SUPPORTED":
                rr["label"] = 0; rr["label_name"] = "SUPPORTED"; kept.append(rr)
            elif lab == "UNSUPPORTED":
                rr["label"] = 1; rr["label_name"] = "UNSUPPORTED"; kept.append(rr)
            else:
                rr["cleaning_removal_reason"] = lab; removed.append(rr)
        return kept, removed

    tr_keep,tr_rm = rebuild(train,"train")
    va_keep,va_rm = rebuild(val,"val")
    if {str(r["qid"]) for r in tr_keep} & {str(r["qid"]) for r in va_keep}:
        raise SystemExit("qid overlap after cleaning")

    write_jsonl(args.out_train,tr_keep)
    write_jsonl(args.out_val,va_keep)
    removed_path = Path(args.summary).parent / "removed_abstention_invalid.jsonl"
    adjud_path = Path(args.summary).parent / "human_adjudicated_disagreements.jsonl"
    write_jsonl(removed_path,tr_rm+va_rm)
    write_jsonl(adjud_path,[
        {**r,"human_final_label":human[cid(r)],"human_final_notes":notes[cid(r)]}
        for r in manifest
    ])

    ac = Counter(final_pos.values())
    contaminated = ac["SUPPORTED"]+ac["ABSTENTION"]+ac["INVALID_EXTRACTION"]
    summary = {
        "audit":{
            "rows_total":len(audit),
            "human_reviewed_disagreements":len(manifest),
            "final_positive_label_counts":dict(ac),
            "final_contaminated_rows":contaminated,
            "final_contamination_rate":contaminated/len(audit),
            "retrain_trigger_reached":contaminated>=96
        },
        "cleaned":{
            "train_rows":len(tr_keep),
            "val_rows":len(va_keep),
            "train_label_counts":dict(Counter(int(r["label"]) for r in tr_keep)),
            "val_label_counts":dict(Counter(int(r["label"]) for r in va_keep)),
            "train_removed":len(tr_rm),
            "val_removed":len(va_rm),
            "removed_reason_counts":dict(Counter(r["cleaning_removal_reason"] for r in tr_rm+va_rm)),
            "train_val_qid_overlap":0
        }
    }
    save_json(args.summary,summary)
    print(json.dumps(summary,indent=2))
    print("Wrote:",args.out_train,args.out_val,args.summary)

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    ex=sub.add_parser("export")
    ex.add_argument("--audit",type=Path,default=Path("unsupported_477_opus_audit.json"))
    ex.add_argument("--out-md",type=Path,default=Path("unsupported_477_disagreement_human_review.md"))
    ex.add_argument("--out-jsonl",type=Path,default=Path("unsupported_477_disagreement_manifest.jsonl"))
    ex.add_argument("--summary",type=Path,default=Path("unsupported_477_disagreement_review_summary.json"))
    ex.set_defaults(func=export)

    im=sub.add_parser("import-clean")
    im.add_argument("--md",type=Path,default=Path("unsupported_477_disagreement_human_review.md"))
    im.add_argument("--manifest",type=Path,default=Path("unsupported_477_disagreement_manifest.jsonl"))
    im.add_argument("--audit",type=Path,default=Path("unsupported_477_opus_audit.json"))
    im.add_argument("--train",type=Path,default=Path("data/distill_arxiv_v2/binary_train.jsonl"))
    im.add_argument("--val",type=Path,default=Path("data/distill_arxiv_v2/binary_val.jsonl"))
    im.add_argument("--out-train",type=Path,default=Path("data/distill_arxiv_v2_cleaned/binary_train_cleaned.jsonl"))
    im.add_argument("--out-val",type=Path,default=Path("data/distill_arxiv_v2_cleaned/binary_val_cleaned.jsonl"))
    im.add_argument("--summary",type=Path,default=Path("data/distill_arxiv_v2_cleaned/cleaning_summary.json"))
    im.set_defaults(func=import_clean)
    a=ap.parse_args(); a.func(a)

if __name__=="__main__":
    main()
