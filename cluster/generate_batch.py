"""
generate_batch.py  --  RUNS ON THE CLUSTER (not the laptop)

Reads eval_inputs.json (self-contained: questions + evidence) and generates, per question,
TWO answers with Mistral-7B-Instruct:
  - plain_answer : arm 1 (Basic RAG)        -> evidence given, NO citation instruction
  - cited_answer : arms 2 & 3 (RAG+cites / Verified) -> evidence given, cite with [n]

Writes answers.json, which is copied back to the laptop for claim extraction + verification.

This script is STANDALONE: it depends only on transformers + torch (already pip-installed in
the cluster pod) and the input JSON. It does NOT import the laptop project. Prompts are built
inline here, mirroring the laptop's generator.build_prompt.

USAGE (in the cluster pod, after the usual session setup + HF login):
    python generate_batch.py
    # optional: python generate_batch.py --in eval_inputs.json --out answers.json --max-new 400

Make sure eval_inputs.json is in the working directory (copy it onto the PVC first).
"""

import json
import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"


def build_plain_prompt(question, evidence):
    """Arm 1: evidence provided, NO citation instruction."""
    sources = "\n".join(f"[{e['number']}] {e['text']}" for e in evidence)
    return (
        "You are a research assistant. Answer the question using the information in the "
        "sources below. If the sources do not contain the answer, say so explicitly.\n\n"
        f"Sources:\n{sources}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )


def build_cited_prompt(question, evidence):
    """Arms 2 & 3: evidence provided, cite with [n]."""
    sources = "\n".join(f"[{e['number']}] {e['text']}" for e in evidence)
    return (
        "You are a research assistant. Answer the question using ONLY the numbered sources "
        "below. Cite the sources you use with their bracketed number, e.g. [1]. If the "
        "sources do not contain the answer, say so explicitly.\n\n"
        f"Sources:\n{sources}\n\n"
        f"Question: {question}\n\n"
        "Answer (with citations):"
    )


def generate(model, tokenizer, prompt, max_new_tokens):
    """Single-prompt generation using Mistral's chat template, low-temperature for repeatability."""
    messages = [{"role": "user", "content": prompt}]
    # tokenize=True + return_dict=True gives a BatchEncoding with input_ids + attention_mask
    enc = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True,
        return_dict=True,
    ).to(model.device)

    with torch.no_grad():
        out = model.generate(
            **enc,                      # unpack input_ids + attention_mask
            max_new_tokens=max_new_tokens,
            do_sample=False,            # greedy -> deterministic eval
            pad_token_id=tokenizer.eos_token_id,
        )
    # decode only the newly generated tokens (strip the prompt)
    prompt_len = enc["input_ids"].shape[-1]
    gen = out[0][prompt_len:]
    return tokenizer.decode(gen, skip_special_tokens=True).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", default="eval_inputs.json")
    ap.add_argument("--out", dest="out_path", default="answers.json")
    ap.add_argument("--max-new", dest="max_new", type=int, default=400)
    args = ap.parse_args()

    print(f"Loading {MODEL_ID} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    model.eval()
    print("Model loaded.")

    with open(args.in_path, encoding="utf-8") as f:
        inputs = json.load(f)

    results = []
    for item in inputs:
        qid = item["id"]
        question = item["question"]
        evidence = item["evidence"]

        plain = generate(model, tokenizer, build_plain_prompt(question, evidence), args.max_new)
        cited = generate(model, tokenizer, build_cited_prompt(question, evidence), args.max_new)

        results.append({
            "id": qid,
            "type": item["type"],
            "question": question,
            "evidence": evidence,          # carry evidence through for downstream verification
            "plain_answer": plain,
            "cited_answer": cited,
        })
        print(f"  Q{qid:>2} done  (plain {len(plain)} chars, cited {len(cited)} chars)")

    with open(args.out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {len(results)} answers to {args.out_path}")


if __name__ == "__main__":
    main()
