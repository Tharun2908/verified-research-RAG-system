"""
inspect_grounded_hard_resources.py

Small resource/schema audit before building the grounded-hard tranche.

Run from /workspace/project3:
  python -u inspect_grounded_hard_resources.py > grounded_hard_resource_audit.txt 2>&1

Then paste grounded_hard_resource_audit.txt output.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(".")
TARGETS = [
    Path("data/distill_arxiv_v2/protected_gold_evidence_papers.json"),
    Path("data/distill_arxiv/gold_eval_claims.json"),
    Path("data/distill_arxiv/gold_final_human_reviewed.json"),
    Path("data/distill_arxiv_v2/train_eval_inputs.json"),
    Path("data/distill_arxiv_v2/train_questions.json"),
    Path("v2_train_eval_inputs.json"),
    Path("data_grouped"),
]


def load_json_sample(path: Path) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
        if isinstance(obj, list):
            return {
                "type": "list",
                "len": len(obj),
                "first_keys": list(obj[0].keys()) if obj and isinstance(obj[0], dict) else None,
                "first": obj[0] if obj else None,
            }
        if isinstance(obj, dict):
            return {
                "type": "dict",
                "keys": list(obj.keys())[:50],
                "sample": {k: obj[k] for k in list(obj.keys())[:3]},
            }
        return {"type": type(obj).__name__, "repr": repr(obj)[:1000]}
    except Exception as e:
        return {"error": repr(e)}


def load_jsonl_sample(path: Path, n: int = 2) -> Any:
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
                if len(rows) >= n:
                    break
        return {
            "type": "jsonl",
            "sample_count": len(rows),
            "first_keys": list(rows[0].keys()) if rows and isinstance(rows[0], dict) else None,
            "first": rows[0] if rows else None,
        }
    except Exception as e:
        return {"error": repr(e)}


def short(obj: Any, max_chars: int = 3500) -> str:
    s = json.dumps(obj, ensure_ascii=False, indent=2, default=str)
    if len(s) > max_chars:
        return s[:max_chars] + "\n... [truncated]"
    return s


def print_file_info(path: Path) -> None:
    print("\n" + "=" * 88)
    print(f"PATH: {path}")
    print(f"EXISTS: {path.exists()}")

    if not path.exists():
        return

    if path.is_dir():
        print("TYPE: dir")
        children = sorted(path.rglob("*"))
        files = [p for p in children if p.is_file()]
        print(f"FILES_TOTAL_RECURSIVE: {len(files)}")
        print("TOP FILES:")
        for p in files[:40]:
            try:
                size = p.stat().st_size
            except Exception:
                size = -1
            print(f"  {size:>12}  {p}")
        json_files = [p for p in files if p.suffix.lower() in {".json", ".jsonl"}]
        print("\nJSON/JSONL SAMPLE FILES:")
        for p in json_files[:10]:
            print(f"  {p}")
        for p in json_files[:3]:
            print(f"\nSAMPLE {p}:")
            if p.suffix.lower() == ".jsonl":
                print(short(load_jsonl_sample(p)))
            else:
                print(short(load_json_sample(p)))
        return

    print("TYPE: file")
    print(f"SIZE: {path.stat().st_size} bytes")

    if path.suffix.lower() == ".json":
        print(short(load_json_sample(path)))
    elif path.suffix.lower() == ".jsonl":
        print(short(load_jsonl_sample(path)))
    else:
        try:
            txt = path.read_text(encoding="utf-8", errors="replace")
            print(txt[:2500])
        except Exception as e:
            print(f"Could not read text: {e}")


def grep_python_for_retrieval() -> None:
    print("\n" + "=" * 88)
    print("PYTHON RETRIEVAL/SEARCH CANDIDATES")
    pats = ["retrieve", "retriever", "similarity_search", "vectorstore", "chroma", "faiss", "top_k", "topk"]
    py_files = list(Path(".").rglob("*.py"))
    hits = []
    for p in py_files:
        # skip huge envs if present
        ps = str(p)
        if any(x in ps for x in ["/site-packages/", "/env", "__pycache__"]):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        score = sum(txt.lower().count(pat) for pat in pats)
        if score > 0:
            hits.append((score, p))
    hits.sort(reverse=True)
    for score, p in hits[:40]:
        print(f"{score:>4}  {p}")


def main() -> None:
    print("Grounded-hard tranche resource audit")
    print("=" * 88)
    print(f"CWD: {Path.cwd()}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
    print(f"OPENROUTER_API_KEY present: {bool(os.environ.get('OPENROUTER_API_KEY'))}")
    print(f"ANTHROPIC_API_KEY present: {bool(os.environ.get('ANTHROPIC_API_KEY'))}")
    print(f"HF_HOME: {os.environ.get('HF_HOME')}")
    print(f"TRANSFORMERS_CACHE: {os.environ.get('TRANSFORMERS_CACHE')}")

    print("\nROOT TOP LEVEL:")
    for p in sorted(Path(".").iterdir()):
        try:
            size = p.stat().st_size if p.is_file() else ""
        except Exception:
            size = ""
        print(f"  {size!s:>12}  {p}")

    for t in TARGETS:
        print_file_info(t)

    grep_python_for_retrieval()


if __name__ == "__main__":
    main()
