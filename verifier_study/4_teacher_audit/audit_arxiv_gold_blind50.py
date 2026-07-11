"""
backend/app/services/audit_arxiv_gold_blind50.py

Compare blind-50 human labels against available teacher/draft labels.

Inputs:
  data/distill_arxiv/gold_blind50_review_labeled.jsonl

Optional model files, loaded if present:
  data/distill_arxiv/gold_eval_teacher_drafted_opus.json
  data/distill_arxiv/gold_eval_teacher_labeled_llama70b_closed.json
  data/distill_arxiv/gold_eval_teacher_drafted.json          # old flash-lite draft, if present

Outputs:
  data/distill_arxiv/gold_blind50_teacher_audit.json
  data/distill_arxiv/gold_blind50_teacher_audit.md

Run:
  python -m app.services.audit_arxiv_gold_blind50
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


GOLD_DIR = Path("data") / "distill_arxiv"

HUMAN_IN = GOLD_DIR / "gold_blind50_review_labeled.jsonl"

MODEL_FILES = {
    "opus": GOLD_DIR / "gold_eval_teacher_drafted_opus.json",
    "llama70b": GOLD_DIR / "gold_eval_teacher_labeled_llama70b_closed.json",
    "flash_lite_old": GOLD_DIR / "gold_eval_teacher_drafted.json",
}

REPORT_JSON = GOLD_DIR / "gold_blind50_teacher_audit.json"
REPORT_MD = GOLD_DIR / "gold_blind50_teacher_audit.md"

LABELS = ["SUPPORTED", "UNSUPPORTED", "ABSTENTION"]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def norm_label(x: Any) -> str:
    s = str(x or "").strip().upper()
    if s in LABELS:
        return s
    return ""


def extract_model_label(row: dict[str, Any]) -> str:
    for key in [
        "gold_draft_label",
        "teacher_label",
        "draft_label",
        "label",
        "pred_label",
        "model_label",
    ]:
        lab = norm_label(row.get(key))
        if lab:
            return lab
    return ""


def extract_model_conf(row: dict[str, Any]) -> Any:
    for key in [
        "gold_draft_confidence",
        "teacher_confidence",
        "draft_confidence",
        "confidence",
    ]:
        if key in row:
            return row.get(key)
    return None


def extract_model_rationale(row: dict[str, Any]) -> str:
    for key in [
        "gold_draft_rationale",
        "teacher_rationale",
        "draft_rationale",
        "rationale",
    ]:
        if row.get(key):
            return str(row.get(key))
    return ""


def load_model_predictions() -> dict[str, dict[str, dict[str, Any]]]:
    models: dict[str, dict[str, dict[str, Any]]] = {}

    for name, path in MODEL_FILES.items():
        if not path.exists():
            continue
        data = load_json(path)
        if not isinstance(data, list):
            continue

        pred_by_claim = {}
        for row in data:
            if not isinstance(row, dict):
                continue
            cid = str(row.get("claim_id") or "").strip()
            if not cid:
                continue
            pred_by_claim[cid] = {
                "label": extract_model_label(row),
                "confidence": extract_model_conf(row),
                "rationale": extract_model_rationale(row),
                "raw_field_keys": sorted(row.keys()),
            }

        models[name] = pred_by_claim

    return models


def metric_block(human: list[str], pred: list[str]) -> dict[str, Any]:
    n = len(human)
    correct = sum(1 for h, p in zip(human, pred) if h == p)
    covered = sum(1 for p in pred if p)

    confusion = {h: {p: 0 for p in LABELS + ["MISSING"]} for h in LABELS}
    for h, p in zip(human, pred):
        pp = p if p in LABELS else "MISSING"
        if h in confusion:
            confusion[h][pp] += 1

    # Binary unsupported vs rest.
    tp = sum(1 for h, p in zip(human, pred) if h == "UNSUPPORTED" and p == "UNSUPPORTED")
    fp = sum(1 for h, p in zip(human, pred) if h != "UNSUPPORTED" and p == "UNSUPPORTED")
    fn = sum(1 for h, p in zip(human, pred) if h == "UNSUPPORTED" and p != "UNSUPPORTED")
    tn = sum(1 for h, p in zip(human, pred) if h != "UNSUPPORTED" and p != "UNSUPPORTED")

    prec = tp / (tp + fp) if (tp + fp) else None
    rec = tp / (tp + fn) if (tp + fn) else None
    f1 = (2 * prec * rec / (prec + rec)) if prec is not None and rec is not None and (prec + rec) else None

    # Binary supported-vs-unsupported only; exclude ABSTENTION humans and missing preds.
    bin_pairs = [(h, p) for h, p in zip(human, pred) if h in {"SUPPORTED", "UNSUPPORTED"} and p in {"SUPPORTED", "UNSUPPORTED"}]
    bin_correct = sum(1 for h, p in bin_pairs if h == p)
    bin_acc = bin_correct / len(bin_pairs) if bin_pairs else None

    return {
        "n": n,
        "covered_predictions": covered,
        "accuracy_3way": correct / n if n else None,
        "correct_3way": correct,
        "human_counts": dict(Counter(human)),
        "pred_counts": dict(Counter(p if p else "MISSING" for p in pred)),
        "confusion_human_rows_pred_cols": confusion,
        "unsupported_binary": {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
            "precision": prec,
            "recall": rec,
            "f1": f1,
        },
        "supported_unsupported_only_accuracy": bin_acc,
        "supported_unsupported_only_n": len(bin_pairs),
    }


def pct(x: Any) -> str:
    if x is None:
        return "—"
    return f"{100*x:.1f}%"


def main() -> None:
    human_rows = read_jsonl(HUMAN_IN)
    models = load_model_predictions()

    human_by_claim = {}
    for r in human_rows:
        cid = str(r.get("claim_id") or "").strip()
        lab = norm_label(r.get("human_label"))
        if not cid:
            raise SystemExit("Human row missing claim_id.")
        if not lab:
            raise SystemExit(f"Human row {r.get('blind_id')} missing/invalid human_label.")
        human_by_claim[cid] = r

    human_labels = [norm_label(r.get("human_label")) for r in human_rows]
    claim_ids = [str(r.get("claim_id")) for r in human_rows]

    per_model = {}
    row_details = []

    for model_name, pred_map in models.items():
        preds = [pred_map.get(cid, {}).get("label", "") for cid in claim_ids]
        per_model[model_name] = metric_block(human_labels, preds)

    for r in human_rows:
        cid = str(r.get("claim_id"))
        detail = {
            "blind_id": r.get("blind_id"),
            "claim_id": cid,
            "question_type": r.get("question_type"),
            "answer_variant": r.get("answer_variant"),
            "human_label": norm_label(r.get("human_label")),
            "claim": r.get("claim"),
            "model_predictions": {},
        }
        for model_name, pred_map in models.items():
            pred = pred_map.get(cid, {})
            detail["model_predictions"][model_name] = pred
        row_details.append(detail)

    # Pairwise disagreement between models on the blind rows.
    pairwise = {}
    model_names = sorted(models)
    for i, a in enumerate(model_names):
        for b in model_names[i + 1:]:
            pairs = []
            for cid in claim_ids:
                la = models[a].get(cid, {}).get("label", "")
                lb = models[b].get(cid, {}).get("label", "")
                if la and lb:
                    pairs.append((la, lb))
            agree = sum(1 for la, lb in pairs if la == lb)
            pairwise[f"{a}_vs_{b}"] = {
                "n": len(pairs),
                "agree": agree,
                "agreement": agree / len(pairs) if pairs else None,
            }

    report = {
        "input": str(HUMAN_IN),
        "model_files_loaded": {k: str(MODEL_FILES[k]) for k in models},
        "n_human_blind": len(human_rows),
        "human_label_counts": dict(Counter(human_labels)),
        "per_model": per_model,
        "pairwise_model_agreement": pairwise,
        "row_details": row_details,
    }

    save_json(REPORT_JSON, report)

    md = []
    md.append("# Gold Blind-50 Teacher Audit")
    md.append("")
    md.append(f"Human blind rows: **{len(human_rows)}**")
    md.append("")
    md.append("Human label counts:")
    md.append("")
    for label, count in Counter(human_labels).most_common():
        md.append(f"- **{label}:** {count}")
    md.append("")

    md.append("## Model comparison")
    md.append("")
    md.append("| Model | 3-way acc | Correct | Pred counts | Unsupported precision | Unsupported recall | Unsupported F1 | SU-only acc |")
    md.append("|---|---:|---:|---|---:|---:|---:|---:|")
    for model_name, m in per_model.items():
        pred_counts = ", ".join(f"{k}:{v}" for k, v in m["pred_counts"].items())
        ub = m["unsupported_binary"]
        md.append(
            f"| {model_name} | {pct(m['accuracy_3way'])} | {m['correct_3way']}/{m['n']} | "
            f"{pred_counts} | {pct(ub['precision'])} | {pct(ub['recall'])} | {pct(ub['f1'])} | "
            f"{pct(m['supported_unsupported_only_accuracy'])} |"
        )
    md.append("")

    md.append("## Pairwise model agreement")
    md.append("")
    for name, p in pairwise.items():
        md.append(f"- **{name}:** {p['agree']}/{p['n']} = {pct(p['agreement'])}")
    md.append("")

    md.append("## Confusions")
    md.append("")
    for model_name, m in per_model.items():
        md.append(f"### {model_name}")
        md.append("")
        md.append("| Human \\ Pred | SUPPORTED | UNSUPPORTED | ABSTENTION | MISSING |")
        md.append("|---|---:|---:|---:|---:|")
        conf = m["confusion_human_rows_pred_cols"]
        for h in LABELS:
            row = conf[h]
            md.append(f"| {h} | {row['SUPPORTED']} | {row['UNSUPPORTED']} | {row['ABSTENTION']} | {row['MISSING']} |")
        md.append("")

    md.append("## Disagreement rows")
    md.append("")
    for d in row_details:
        preds = {k: v.get("label", "") for k, v in d["model_predictions"].items()}
        if len(set([d["human_label"]] + [p for p in preds.values() if p])) <= 1:
            continue
        md.append(f"### {d['blind_id']} — {d['claim_id']}")
        md.append("")
        md.append(f"- **Human:** {d['human_label']}")
        for model_name, pred in preds.items():
            md.append(f"- **{model_name}:** {pred or 'MISSING'}")
        md.append(f"- **question_type:** {d.get('question_type')}")
        md.append(f"- **answer_variant:** {d.get('answer_variant')}")
        md.append("")
        md.append("> " + str(d.get("claim") or "").replace("\n", "\n> "))
        md.append("")

    REPORT_MD.write_text("\n".join(md), encoding="utf-8")

    print("\nGold blind-50 teacher audit")
    print("=" * 64)
    print(f"Human rows: {len(human_rows)}")
    print(f"Human labels: {dict(Counter(human_labels))}")
    print(f"Models loaded: {list(models.keys())}")
    print("\nModel summary:")
    for model_name, m in per_model.items():
        ub = m["unsupported_binary"]
        print(
            f"  {model_name:16s} "
            f"acc3={pct(m['accuracy_3way'])} "
            f"unsupported_P={pct(ub['precision'])} "
            f"unsupported_R={pct(ub['recall'])} "
            f"unsupported_F1={pct(ub['f1'])} "
            f"pred_counts={m['pred_counts']}"
        )
    print("\nWrote:")
    print(f"  {REPORT_JSON}")
    print(f"  {REPORT_MD}")


if __name__ == "__main__":
    main()
