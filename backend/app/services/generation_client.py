"""
backend/app/services/generation_client.py

Generation backend, swappable behind one interface:

    generate(prompt: str) -> str

Selection (same real-by-default policy as the verifier):

    OpenRouterClient   DEFAULT when OPENROUTER_API_KEY is set. Calls a hosted LLM.
    StubGenerator      Fallback when no key is present, or when DEV_STUB_GENERATOR=true.
                       Returns placeholder text and SAYS SO, loudly, at startup.

An earlier version of this repo defaulted silently to the stub while the README described a
real pipeline. Real-by-default with a loud warning on degradation prevents that.

The call is I/O-bound (an HTTPS request), so it is genuinely async and belongs ON the event
loop — unlike the verifier, whose CPU-bound torch forward pass is pushed to a worker thread.

Model fallback chain: the first model that responds wins. A single upstream rate-limit or a
delisted model should not take the endpoint down. (Mistral-7B, used for the offline
evaluation, is no longer served by any OpenRouter provider — hence the chain.)
"""

from __future__ import annotations

import os

import httpx

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Tried in order; first success wins.
GEN_MODELS = [
    "mistralai/ministral-8b-2512",               # primary: cheap, reliable, Mistral family
    "mistralai/mistral-small-3.2-24b-instruct",  # fallback: stronger, still cheap
    "meta-llama/llama-3.3-70b-instruct:free",    # last resort: free (may rate-limit)
]

TIMEOUT_S = 90.0
TEMPERATURE = 0.2


class GenerationClient:
    """Base interface."""

    async def generate(self, prompt: str) -> str:
        raise NotImplementedError


class OpenRouterClient(GenerationClient):
    """Hosted-LLM generation via OpenRouter, with a model fallback chain."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_err = None

        async with httpx.AsyncClient(timeout=TIMEOUT_S) as client:
            for model in GEN_MODELS:
                try:
                    r = await client.post(
                        OPENROUTER_URL,
                        headers=headers,
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": TEMPERATURE,
                        },
                    )
                    if r.status_code == 200:
                        return r.json()["choices"][0]["message"]["content"].strip()
                    last_err = f"HTTP {r.status_code} from {model}"
                except Exception as e:  # network error, timeout, malformed response
                    last_err = f"{type(e).__name__} from {model}"

        # Every model failed. Return a clear message rather than raising — the caller still
        # has real retrieval results to show, and the verifier must NOT be handed an error
        # string to score (verification_service treats this as an ordinary answer, so keep
        # it short and honest).
        return f"The generation service is currently unavailable ({last_err})."


class StubGenerator(GenerationClient):
    """
    DEV ONLY. Placeholder text — NOT a real answer. Used when no OPENROUTER_API_KEY is set,
    or when DEV_STUB_GENERATOR=true. Any grounding scores computed over this text are
    meaningless.
    """

    async def generate(self, prompt: str) -> str:
        return (
            "[STUB ANSWER] Based on the retrieved evidence, the topic in question is "
            "addressed by the provided sources [1] [2] [3]. The first source establishes "
            "the core finding [1], and additional sources provide supporting context. "
            "(This is placeholder text from the stub generator; set OPENROUTER_API_KEY "
            "for real generation.)"
        )


# --- selection --------------------------------------------------------------
def _use_stub() -> bool:
    if os.getenv("DEV_STUB_GENERATOR", "").strip().lower() in {"1", "true", "yes"}:
        return True
    return not os.getenv("OPENROUTER_API_KEY")


def _build_client() -> GenerationClient:
    if _use_stub():
        reason = (
            "DEV_STUB_GENERATOR=true"
            if os.getenv("DEV_STUB_GENERATOR")
            else "OPENROUTER_API_KEY is not set"
        )
        print(
            "\n" + "!" * 78 + "\n"
            f"!! Generation is STUBBED ({reason}).\n"
            "!! Answers are placeholder text and grounding scores over them are meaningless.\n"
            "!! Set OPENROUTER_API_KEY in .env for real generation.\n"
            + "!" * 78 + "\n"
        )
        return StubGenerator()
    return OpenRouterClient(os.environ["OPENROUTER_API_KEY"])


# The active client. `generator.py` imports this and calls `.generate(prompt)`.
generation_client: GenerationClient = _build_client()


def describe_generator() -> str:
    """For the startup banner."""
    return type(generation_client).__name__


async def _demo():
    print(f"generator: {describe_generator()}")
    out = await generation_client.generate(
        "You are a research assistant. Answer using ONLY the numbered sources, citing "
        "with [n].\n\nSources:\n[1] Retrieval-augmented generation combines a parametric "
        "generator with a non-parametric retriever.\n\nQuestion: What is RAG?\n\n"
        "Answer (with citations):"
    )
    print("\n" + out)


if __name__ == "__main__":
    import asyncio
    asyncio.run(_demo())
