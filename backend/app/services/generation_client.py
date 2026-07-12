"""
backend/app/services/generation_client.py

Generation backend, swappable behind one interface:

    generate(prompt: str) -> str          raises GenerationError on total failure

Selection (real-by-default, same policy as the verifier):

    OpenRouterClient   DEFAULT when OPENROUTER_API_KEY is set.
    StubGenerator      Only when no key is present, or DEV_STUB_GENERATOR=true — and it
                       SAYS SO, loudly, at startup.

FAILURE IS AN EXCEPTION, NOT A STRING. An earlier version returned an error *sentence* when
every upstream model failed. The pipeline then extracted "claims" from that sentence, scored
them with the verifier, and reported verification_status="verified" — a fabricated
verification result, in a system whose entire purpose is not to fabricate. A generation
outage must be a typed failure that skips verification entirely.

The call is I/O-bound (an HTTPS request), so it is genuinely async and belongs ON the event
loop — unlike the verifier, whose CPU-bound forward pass is pushed to a worker thread.

Model fallback chain: the first model that responds wins. One rate-limit or a delisted model
should not take the endpoint down. (Mistral-7B, used for the offline evaluation, is no longer
served by any OpenRouter provider — hence the chain.)
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

GEN_MODELS = [
    "mistralai/ministral-8b-2512",               # primary: cheap, reliable, Mistral family
    "mistralai/mistral-small-3.2-24b-instruct",  # fallback: stronger, still cheap
    "meta-llama/llama-3.3-70b-instruct:free",    # last resort: free (may rate-limit)
]

TIMEOUT_S = 90.0
TEMPERATURE = 0.2


class GenerationError(RuntimeError):
    """
    Generation failed for every configured model.

    Raised, not returned — so no downstream stage can mistake an outage for an answer and
    "verify" it.
    """


class GenerationClient:
    """Base interface."""

    async def generate(self, prompt: str) -> str:
        raise NotImplementedError

    def describe(self) -> dict:
        """Component metadata, surfaced in every API response."""
        return {"implementation": type(self).__name__}


class OpenRouterClient(GenerationClient):
    """Hosted-LLM generation via OpenRouter, with a model fallback chain."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.last_model: str | None = None

    def describe(self) -> dict:
        return {
            "implementation": "OpenRouterClient",
            "model": self.last_model,      # the model that actually answered
            "candidates": GEN_MODELS,
        }

    async def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        errors: list[str] = []

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
                        self.last_model = model
                        return r.json()["choices"][0]["message"]["content"].strip()
                    errors.append(f"{model}: HTTP {r.status_code}")
                except Exception as e:
                    errors.append(f"{model}: {type(e).__name__}")

        raise GenerationError(
            "all generation models failed — " + "; ".join(errors)
        )


class StubGenerator(GenerationClient):
    """
    DEV ONLY. Placeholder text — NOT a real answer. Selected when no OPENROUTER_API_KEY is
    set, or DEV_STUB_GENERATOR=true. Grounding scores over this text are meaningless.
    """

    def __init__(self) -> None:
        self.last_model = None

    def describe(self) -> dict:
        return {
            "implementation": "StubGenerator",
            "model": None,
            "warning": "placeholder text; any grounding computed over it is meaningless",
        }

    async def generate(self, prompt: str) -> str:
        return (
            "[STUB ANSWER] Based on the retrieved evidence, the topic in question is "
            "addressed by the provided sources [1] [2] [3]. The first source establishes "
            "the core finding [1], and additional sources provide supporting context. "
            "(Placeholder text from the stub generator; set OPENROUTER_API_KEY for real "
            "generation.)"
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
            "!! Answers are placeholder text; grounding scores over them are MEANINGLESS.\n"
            "!! Set OPENROUTER_API_KEY in .env for real generation.\n"
            + "!" * 78 + "\n"
        )
        return StubGenerator()
    return OpenRouterClient(os.environ["OPENROUTER_API_KEY"])


generation_client: GenerationClient = _build_client()


def describe_generator() -> str:
    """For the startup banner."""
    return type(generation_client).__name__


async def _demo():
    print(f"generator: {describe_generator()}")
    try:
        out = await generation_client.generate(
            "Answer using ONLY the numbered sources, citing with [n].\n\n"
            "Sources:\n[1] Retrieval-augmented generation combines a parametric generator "
            "with a non-parametric retriever.\n\nQuestion: What is RAG?\n\nAnswer:"
        )
        print("\n" + out)
    except GenerationError as e:
        print(f"\nGENERATION FAILED: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(_demo())
