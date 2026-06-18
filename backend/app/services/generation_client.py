"""
backend/app/services/generation_client.py

A single generation client with a swappable backend, selected by config:

    settings.llm_base_url == "stub"   -> return canned text locally (no GPU, no network)
    settings.llm_base_url == <a URL>  -> POST to an OpenAI-compatible /v1/chat/completions
                                         (this is what the H200 vLLM server exposes, and also
                                          what hosted APIs like OpenAI/Together expose)

The interface mirrors OpenAI chat completions so the same calling code works for every backend.
At M1 we only need the stub path to work end-to-end. The real-HTTP path is written now so M4 is
a config change (point LLM_BASE_URL at the vLLM server), not a code change.
"""

from __future__ import annotations

import httpx

from app.config import settings


class GenerationClient:
    def __init__(self) -> None:
        # Read the backend choice once at construction.
        self.base_url = settings.llm_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        # True when we should fake responses locally instead of calling a server.
        self.stub_mode = self.base_url == "stub"

    async def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """
        Take a prompt, return the generated text as a plain string.
        Callers (the future generator service) only see a string in / string out —
        they never need to know which backend produced it.
        """
        if self.stub_mode:
            return self._stub_response(prompt)
        return await self._http_response(prompt, max_tokens)

    # --- stub backend ------------------------------------------------------
    def _stub_response(self, prompt: str) -> str:
        """
        Deterministic fake answer for local/no-GPU dev. It detects how many numbered
        sources the prompt contains and produces a citation-shaped answer that
        references them, so the retrieve->prompt->generate->cite flow is testable
        end-to-end without a real model. NOT a real answer — just structurally valid.
        """
        import re
        # count how many "[n]" source markers the prompt contains
        source_nums = sorted(set(int(n) for n in re.findall(r"\[(\d+)\]", prompt)))

        if source_nums:
            cites = " ".join(f"[{n}]" for n in source_nums[:3])
            return (
                "[STUB ANSWER] Based on the retrieved evidence, the topic in question "
                f"is addressed by the provided sources {cites}. The first source "
                f"establishes the core finding [{source_nums[0]}], and additional "
                "sources provide supporting context. (This is placeholder text from the "
                "no-GPU stub; a real vLLM/Mistral backend would generate a substantive "
                "cited answer here.)"
            )
        # fallback if no sources were formatted into the prompt
        preview = prompt.strip().replace("\n", " ")[:120]
        return (
            "[STUB ANSWER] Placeholder generation (no sources detected in prompt). "
            f"Prompt began with: \"{preview}...\"."
        )

    # --- real OpenAI-compatible HTTP backend -------------------------------
    async def _http_response(self, prompt: str, max_tokens: int) -> str:
        """
        POST to an OpenAI-compatible chat-completions endpoint and pull the text
        out of the standard response shape. Used at M4 onward with the H200 vLLM
        server or a hosted API.
        """
        url = f"{self.base_url.rstrip('/')}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        # Standard OpenAI shape: choices[0].message.content
        return data["choices"][0]["message"]["content"]


# A module-level singleton so the rest of the app shares one client.
generation_client = GenerationClient()
