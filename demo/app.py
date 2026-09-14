"""
Verified Research RAG — live demo (HuggingFace Space, CPU-only)

Full pipeline:
    question
      -> hybrid retrieval (BM25 + dense MiniLM, RRF fusion, cross-encoder rerank)
      -> generation (hosted LLM via OpenRouter, with citation instructions)
      -> claim extraction (sentence split, citation markers -> evidence scope)
      -> claim-level verification (fine-tuned DeBERTa faithfulness verifier)
      -> answer displayed with per-claim grounding scores

Runs entirely on CPU. The models are small (DeBERTa-base verifier + two MiniLM encoders),
so CPU inference is a few seconds per query — and it never fails on GPU quota.

The VERIFIER is the point: every claim is scored against the evidence it cites, and the
system reports how much of its own answer is actually grounded.

Honest notes:
  - Generation is a hosted LLM call (the verifier, not the generator, is the contribution).
  - The verifier is recall-oriented and imperfectly calibrated (see repo for full evaluation,
    including a negative result on in-domain adaptation).
  - Corpus is a fixed 250-paper arXiv snapshot (NLP / IR / LLM / ML-systems, 2025-2026).
"""

import os
import re
import json

import numpy as np
import gradio as gr
import httpx
import spaces      # required: ZeroGPU hardware needs >=1 @spaces.GPU function to exist
import torch

from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from claim_extractor import extract_claims
from decision_policy import P_UNSUPPORTED_THRESHOLD, label_for_score

# ----------------------------------------------------------------------------- config
VERIFIER_REPO = "Primeinvincible/scifact-healthver-verifier"
EMBED_MODEL = "all-MiniLM-L6-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
# Hosted generation via OpenRouter. Tried in order — the first that responds wins.
# (Mistral-7B, used for the offline evaluation, is no longer served on OpenRouter; the
# generator is not the contribution here, the verifier is.)
GEN_MODELS = [
    "mistralai/ministral-8b-2512",              # primary: cheap, reliable, Mistral family
    "mistralai/mistral-small-3.2-24b-instruct", # fallback: stronger, still cheap
    "meta-llama/llama-3.3-70b-instruct:free",   # last resort: free (may rate-limit)
]
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

CANDIDATE_POOL = 30
TOP_K = 4
MAX_LENGTH = 512
DEVICE = "cpu"   # CPU-only: models are small (DeBERTa-base + 2x MiniLM); no GPU needed,
                 # which makes the Space reliable (no ZeroGPU quota/queue failures).


# ZeroGPU requires at least one @spaces.GPU function to exist at startup, but free-tier
# GPU allocation is unreliable (quota/queue -> "No CUDA GPUs are available"). So we declare
# one to satisfy the check and NEVER call it: the whole pipeline runs on CPU, where these
# small models (DeBERTa-base + 2x MiniLM) are perfectly fast enough. Reliability > speed.
@spaces.GPU(duration=1)
def _zerogpu_startup_probe():
    """Exists only to satisfy ZeroGPU's startup requirement. Not used by the pipeline."""
    return "ok"


# ---------------------------------------------------------------- ZeroGPU shim
# The Space is on ZeroGPU hardware, which REFUSES to start unless at least one
# @spaces.GPU function exists ("No @spaces.GPU function detected during startup").
# But free-tier ZeroGPU frequently cannot actually allocate a GPU ("No CUDA GPUs are
# available"), which crashes any real GPU work. Our models are small (DeBERTa-base +
# two MiniLMs) and run fine on CPU in a few seconds — so we declare this no-op to
# satisfy the startup check and run all real inference on CPU. Reliability > speed:
# a demo that always works beats one that 500s when the GPU queue is busy.
@spaces.GPU(duration=1)
def _zerogpu_startup_shim():
    return "ok"



# ------------------------------------------------------------------------ load (startup)
print("Loading corpus...")
with open("arxiv_papers.json", encoding="utf-8") as f:
    PAPERS = json.load(f)                       # one abstract = one chunk
CHUNKS = [p["abstract"] for p in PAPERS]
TITLES = [p["title"] for p in PAPERS]

print("Loading models...")
embedder = SentenceTransformer(EMBED_MODEL, device=DEVICE)
reranker = CrossEncoder(RERANK_MODEL, max_length=MAX_LENGTH, device=DEVICE)
v_tok = AutoTokenizer.from_pretrained(VERIFIER_REPO)
v_model = AutoModelForSequenceClassification.from_pretrained(VERIFIER_REPO).to(DEVICE).eval()

print("Building index...")
if os.path.exists("embeddings.npy"):
    EMB = np.load("embeddings.npy")
else:
    EMB = embedder.encode(CHUNKS, show_progress_bar=True, normalize_embeddings=True)
    np.save("embeddings.npy", EMB)
EMB = EMB / (np.linalg.norm(EMB, axis=1, keepdims=True) + 1e-9)

bm25 = BM25Okapi([re.findall(r"\w+", c.lower()) for c in CHUNKS])
print("Ready.")


# --------------------------------------------------------------------------- helpers
def rrf(rank_lists, k=60, top_k=CANDIDATE_POOL):
    """Reciprocal rank fusion (matches the app's fusion)."""
    scores = {}
    for ranked in rank_lists:
        for rank, doc_id in enumerate(ranked):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])[:top_k]]




# ------------------------------------------------------------- retrieval
def retrieve(query, top_k=TOP_K):
    qv = embedder.encode(query, normalize_embeddings=True)
    dense_ids = np.argsort(-(EMB @ qv))[:CANDIDATE_POOL].tolist()

    bm25_scores = bm25.get_scores(re.findall(r"\w+", query.lower()))
    bm25_ids = np.argsort(-bm25_scores)[:CANDIDATE_POOL].tolist()

    fused = rrf([dense_ids, bm25_ids])
    rr = reranker.predict([(query, CHUNKS[i]) for i in fused])
    order = np.argsort(-rr)[:top_k]
    return [{"title": TITLES[fused[o]], "text": CHUNKS[fused[o]], "score": float(rr[o])}
            for o in order]


# ----------------------------------------------------- hosted generation (HTTP)
def generate(query, evidence):
    """Call OpenRouter, walking the GEN_MODELS fallback chain. Returns (answer, model_used)."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "The generation service is not configured (missing API key).", None

    ctx = "\n\n".join(f"[{i+1}] {e['title']}\n{e['text']}" for i, e in enumerate(evidence))
    system = (
        "You are a research assistant. Answer the question using ONLY the numbered sources. "
        "Cite each factual statement with its source number in brackets, e.g. [1]. "
        "If the sources do not contain the answer, say so plainly. Be concise (3-5 sentences)."
    )
    user = f"SOURCES:\n{ctx}\n\nQUESTION: {query}\n\nAnswer with citations:"

    last_err = None
    for model in GEN_MODELS:
        try:
            r = httpx.post(
                OPENROUTER_URL,
                json={"model": model,
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user", "content": user}],
                      "temperature": 0.2},
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"},
                timeout=90,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip(), model
            last_err = f"{r.status_code}"
        except Exception as e:
            last_err = type(e).__name__
    return (f"The generation service is temporarily unavailable ({last_err}). "
            f"Retrieval and verification still ran — see the sources below."), None


# ---------------------------------------------------------- verification
def verify_claims(claims, evidence):
    """Score each claim against ITS cited evidence (uncited -> all evidence).
    ABSTENTION claims are not scored — they assert absence, not fact."""
    out = []
    for c in claims:
        if c.get("abstention"):
            out.append({**c, "support": None, "label": "Abstention"})
            continue
        if c["citations"]:
            ev = "\n\n".join(evidence[i - 1]["text"] for i in c["citations"]
                             if 1 <= i <= len(evidence))
        else:
            ev = "\n\n".join(e["text"] for e in evidence)

        if not ev or not c["claim_text"]:
            score = 0.0
        else:
            enc = v_tok(c["claim_text"], ev, max_length=MAX_LENGTH, truncation=True,
                        padding="max_length", return_tensors="pt").to(DEVICE)
            with torch.no_grad():
                p_unsup = torch.softmax(v_model(**enc).logits, dim=1)[0, 1].item()
            score = max(0.0, min(1.0, 1.0 - p_unsup))
        out.append({**c, "support": score, "label": label_for_score(score)})
    return out


# ------------------------------------------------------------------------- pipeline
BADGE = {"Supported": "🟢", "Unsupported": "🔴", "Abstention": "⚪"}


def run(query):
    if not query.strip():
        return "Enter a question.", "", ""

    evidence = retrieve(query)
    answer, model_used = generate(query, evidence)

    # If generation failed, don't run the verifier on an error string.
    if model_used is None:
        src_md = "### Retrieved evidence\n" + "\n".join(
            f"**[{i+1}]** {e['title']}  \n<sub>{e['text'][:280]}…</sub>"
            for i, e in enumerate(evidence)
        )
        return answer, "", src_md

    claims = extract_claims(answer)
    scored = verify_claims(claims, evidence) if claims else []

    abstentions = [c for c in scored if c["label"] == "Abstention"]
    substantive = [c for c in scored if c["label"] != "Abstention"]
    unsupported = sum(1 for c in substantive if c["label"] == "Unsupported")

    def _row(c):
        support = "—" if c["support"] is None else f"{c['support']:.2f}"
        cites = ", ".join(f"[{i}]" for i in c["citations"]) or "(uncited)"
        return f"| {BADGE[c['label']]} {c['label']} | {support} | {cites} | {c['claim_text']} |"

    rows = [_row(c) for c in scored]

    if substantive:
        rate = unsupported / len(substantive) * 100
        headline = (f"- Substantive claims: **{len(substantive)}**\n"
                    f"- Flagged unsupported: **{unsupported}** ({rate:.0f}%)")
    else:
        headline = ("- Substantive claims: **0**\n"
                    "- **The model abstained** — it reported that the sources do not cover this "
                    "question, rather than inventing an answer. Nothing to verify.")

    abst_note = ""
    if abstentions:
        abst_note = (f"\n- Abstention statements: **{len(abstentions)}** "
                     f"<sub>(assertions that the sources lack the information — correct refusals, "
                     f"not hallucinations; excluded from the unsupported rate)</sub>")

    grounding = (
        f"### Grounding report\n"
        f"{headline}{abst_note}\n"
        f"- <sub>generator: `{model_used}` · verifier: fine-tuned DeBERTa · "
        f"binary cutoff: P(unsupported) ≥ {P_UNSUPPORTED_THRESHOLD:.2f}</sub>\n"
        f"- <sub>support score is an uncalibrated ranking score, not a probability</sub>\n\n"
        f"| Verdict | Support score | Cites | Claim |\n|---|---|---|---|\n" + "\n".join(rows)
    )
    src = "### Retrieved evidence\n" + "\n".join(
        f"**[{i+1}]** {e['title']}  \n<sub>{e['text'][:280]}…</sub>"
        for i, e in enumerate(evidence)
    )
    return answer, grounding, src


EXAMPLES = [
    "How can hallucinations in large language models be detected without a source document?",
    "What are the limitations of using stronger encoders as SPLADE backbones?",
    "How does quantum computing improve vector database search?",   # bait — not in corpus
]

with gr.Blocks(title="Verified Research RAG") as demo:
    gr.Markdown(
        "# Verified Research RAG\n"
        "Ask a question over a 250-paper arXiv corpus (NLP / IR / LLM / ML-systems). "
        "The system retrieves evidence, generates a cited answer, then **verifies every claim "
        "against the evidence it cites** with a fine-tuned faithfulness verifier — and reports "
        "how much of its own answer is actually grounded.\n\n"
        "🟢 Supported · 🔴 Unsupported · ⚪ Abstention (the model correctly said the "
        "sources don't cover it) — *try the third example: it asks about "
        "something the corpus doesn't cover.*"
    )
    q = gr.Textbox(label="Question", placeholder="Ask about the corpus…", lines=2)
    btn = gr.Button("Ask + Verify", variant="primary")
    gr.Examples(EXAMPLES, inputs=q)
    ans = gr.Markdown()
    grd = gr.Markdown()
    srcs = gr.Markdown()
    btn.click(run, inputs=q, outputs=[ans, grd, srcs])
    q.submit(run, inputs=q, outputs=[ans, grd, srcs])
    gr.Markdown(
        "---\n"
        "**Honest limitations.** Generation is a hosted LLM call — the *verifier* is the "
        "contribution, not the generator. The verifier (DeBERTa, fine-tuned on a leakage-safe "
        "SciFact+HealthVer split) is recall-oriented and imperfectly calibrated. The binary "
        "decision uses the validation-selected P(unsupported) ≥ 0.06 cutoff; the displayed "
        "support score is useful for ranking, not as a literal probability. A rigorous in-domain adaptation "
        "study produced a *negative* result — see the repo write-up."
    )

if __name__ == "__main__":
    demo.launch()
