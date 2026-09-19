"""
backend/tests/test_failure_paths.py

Tests for the paths that were ADDED to fix earlier review findings — and which, until now,
had no coverage. Every one of these guards a bug that shipped once:

  - a generation outage was returned as an "answer", whose claims were then "verified"
  - the verifier loaded a gitignored local path, so a fresh clone crashed on startup
  - a stub-mode response was indistinguishable from a real one to an API client

These are the regressions most worth preventing, because each produced *plausible-looking*
output rather than an error.

No database, no network, no models — the model-loading tests only check SOURCE RESOLUTION,
not the actual download.
"""

from __future__ import annotations

import os

import pytest

from app.services.generation_client import (
    GenerationError,
    GenerationClient,
    StubGenerator,
    OpenRouterClient,
)
from app.services.verifier import StubVerifier, Verifier


# ------------------------------------------------------ generation failure is typed
class TestGenerationFailureIsTyped:
    """
    A generation outage must RAISE, not return a string.

    It once returned an error sentence. verification_service then extracted "claims" from
    that sentence, scored them with the verifier, and reported verification_status="verified"
    — a fabricated verification result, in a system whose entire purpose is to not fabricate.
    """

    def test_generation_error_is_an_exception(self):
        assert issubclass(GenerationError, Exception)

    @pytest.mark.asyncio
    async def test_openrouter_raises_when_every_model_fails(self, monkeypatch):
        import httpx

        class DeadClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def post(self, *a, **kw):
                raise httpx.ConnectError("simulated upstream outage")

        monkeypatch.setattr(httpx, "AsyncClient", lambda **kw: DeadClient())

        client = OpenRouterClient(api_key="dummy")
        with pytest.raises(GenerationError):
            await client.generate("any prompt")

    @pytest.mark.asyncio
    async def test_error_message_names_the_failed_models(self, monkeypatch):
        import httpx
        from app.services.generation_client import GEN_MODELS

        class DeadClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def post(self, *a, **kw):
                raise httpx.ConnectError("boom")

        monkeypatch.setattr(httpx, "AsyncClient", lambda **kw: DeadClient())

        with pytest.raises(GenerationError) as exc:
            await OpenRouterClient(api_key="dummy").generate("prompt")

        # every candidate should be accounted for — a silent partial failure is not useful
        for model in GEN_MODELS:
            assert model in str(exc.value)


# ------------------------------------------------- component metadata is machine-readable
class TestComponentMetadata:
    """
    A console warning is invisible to an API client. The RESPONSE must say whether the
    result came from a real verifier or a lexical-overlap stub — otherwise a consumer
    cannot tell a real grounding score from a meaningless one.
    """

    def test_verifier_base_class_describes_itself(self):
        assert "implementation" in Verifier().describe()

    def test_stub_verifier_declares_itself_a_stub(self):
        d = StubVerifier().describe()
        assert d["implementation"] == "StubVerifier"
        assert "warning" in d, "the stub must announce that its scores are not real"

    def test_stub_generator_declares_itself_a_stub(self):
        d = StubGenerator().describe()
        assert d["implementation"] == "StubGenerator"
        assert "warning" in d

    def test_openrouter_static_description_has_no_answering_model(self):
        c = OpenRouterClient(api_key="dummy")
        d = c.describe()
        assert d["implementation"] == "OpenRouterClient"
        assert d["model"] is None
        assert "candidates" in d


# ----------------------------------------------------------- model source resolution
class TestVerifierModelSource:
    """
    The verifier once loaded a GITIGNORED local directory. A fresh clone had no such path,
    so the default backend crashed at startup. It now defaults to a PINNED HuggingFace
    revision, with an explicit local override.

    These check resolution only — no download.
    """

    def test_defaults_to_pinned_hub_revision(self, monkeypatch):
        from app.services.verifier_real import (
            resolve_model_source, HF_MODEL_ID, HF_REVISION, LOCAL_PATH_ENV,
        )
        monkeypatch.delenv(LOCAL_PATH_ENV, raising=False)

        source, revision = resolve_model_source()
        assert source == HF_MODEL_ID
        assert revision == HF_REVISION
        assert revision and len(revision) == 40, "must be a full pinned commit, not a branch"

    def test_revision_is_not_a_mutable_branch(self):
        """Following `main` would let a model push silently change verification behaviour."""
        from app.services.verifier_real import HF_REVISION
        assert HF_REVISION not in {"main", "master", None, ""}

    def test_local_override_is_used_when_the_directory_exists(self, monkeypatch, tmp_path):
        from app.services.verifier_real import resolve_model_source, LOCAL_PATH_ENV
        monkeypatch.setenv(LOCAL_PATH_ENV, str(tmp_path))

        source, revision = resolve_model_source()
        assert source == str(tmp_path)
        assert revision is None, "a local checkpoint has no Hub revision"

    def test_missing_local_override_fails_loudly(self, monkeypatch, tmp_path):
        """
        Silently falling back to the Hub when VERIFIER_MODEL_PATH is wrong would score with
        a DIFFERENT model than the operator intended — the exact class of silent substitution
        this project exists to avoid. It must raise.
        """
        from app.services.verifier_real import resolve_model_source, LOCAL_PATH_ENV
        monkeypatch.setenv(LOCAL_PATH_ENV, str(tmp_path / "does_not_exist"))

        with pytest.raises(FileNotFoundError):
            resolve_model_source()
