"""
backend/tests/test_api_verify.py

API-boundary tests for /verify.

The failure behaviour was previously tested only BELOW the API: we knew `GenerationError` was
raised and that `verification_service` handled it, but nothing asserted what an actual HTTP
client sees. That gap matters, because the bug being guarded against was precisely one of
*presentation*: a generation outage that looked, to a caller, like a successful verification.

These tests assert the contract at the boundary:

    generation fails  ->  HTTP 503
                      ->  the verifier is NEVER invoked
                      ->  nothing is persisted

Everything below the route is faked. No database, no models, no network — which requires
that the retrieval models are constructed LAZILY (see hybrid_search.get_embed_model and
reranker.get_reranker). Importing a route must not download 100MB of transformers.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes_verify import router
from app.services.generation_client import GenerationError


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestGenerationOutageReturns503:
    """
    A generation outage is an upstream failure, not a verified answer. The endpoint must say
    so with a 5xx — a 200 carrying an apologetic sentence is exactly the bug this guards.
    """

    def test_returns_503_when_generation_fails(self, client, monkeypatch):
        async def boom(question: str, top_k: int = 5):
            raise GenerationError("all generation models failed — simulated outage")

        monkeypatch.setattr("app.services.verification_service.generate_answer", boom)

        r = client.get("/verify", params={"q": "anything", "top_k": 3})
        assert r.status_code == 503, (
            f"expected 503 on generation outage, got {r.status_code}: {r.text[:200]}"
        )

    def test_503_body_explains_the_failure(self, client, monkeypatch):
        async def boom(question: str, top_k: int = 5):
            raise GenerationError("all generation models failed — ministral: HTTP 429")

        monkeypatch.setattr("app.services.verification_service.generate_answer", boom)

        r = client.get("/verify", params={"q": "anything"})
        assert "detail" in r.json()
        assert "generation" in r.json()["detail"].lower()

    def test_verifier_is_never_invoked_on_generation_failure(self, client, monkeypatch):
        """
        If generation produced nothing, there is nothing to verify. Scoring an error string
        and reporting it as a grounding result is the original bug.
        """
        calls: list[tuple[str, str]] = []

        class SpyVerifier:
            def verify(self, claim_text, evidence_text):
                calls.append((claim_text, evidence_text))
                return 0.5

            def describe(self):
                return {"implementation": "SpyVerifier"}

        async def boom(question: str, top_k: int = 5):
            raise GenerationError("simulated outage")

        monkeypatch.setattr("app.services.verification_service.generate_answer", boom)
        monkeypatch.setattr(
            "app.services.verification_service.get_verifier", lambda: SpyVerifier()
        )

        client.get("/verify", params={"q": "anything"})
        assert calls == [], f"verifier was invoked {len(calls)}x despite generation failing"

    def test_nothing_is_persisted_on_generation_failure(self, client, monkeypatch):
        """A failed request must not leave a 'completed' job row behind."""
        opened: list[str] = []

        def spy_session(*a, **kw):
            opened.append("session")
            raise AssertionError("the database must not be touched when generation fails")

        async def boom(question: str, top_k: int = 5):
            raise GenerationError("simulated outage")

        monkeypatch.setattr("app.services.verification_service.generate_answer", boom)
        monkeypatch.setattr(
            "app.services.verification_service.AsyncSessionLocal", spy_session
        )

        r = client.get("/verify", params={"q": "anything"})
        assert r.status_code == 503
        assert opened == [], "a database session was opened on a failed request"


class TestSuccessfulVerifyShape:
    """The success path must carry component metadata, so a client can tell real from stub."""

    def test_response_declares_its_components(self, client, monkeypatch):
        async def fake_generate(question: str, top_k: int = 5):
            return {
                "question": question,
                "answer": "RAG combines retrieval with generation [1].",
                "evidence": [
                    {"number": 1, "title": "T", "text": "RAG combines retrieval and "
                                                       "generation.", "chunk_id": 1},
                ],
            }

        class FakeVerifier:
            def verify(self, claim_text, evidence_text):
                return 0.91

            def describe(self):
                return {"implementation": "RealVerifier", "model": "m", "revision": "r"}

        class FakeGenerator:
            """
            Must be patched too. `generation_client` is a MODULE-LEVEL singleton chosen at
            import time: with no OPENROUTER_API_KEY it is a StubGenerator, so the status
            would be "development_stub" and this test would fail — or pass — depending on
            the developer's .env. A test must not depend on the environment it runs in.
            """
            def describe(self):
                return {"implementation": "OpenRouterClient", "model": "fake-model"}

        class NoopSession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            def add(self, obj):
                pass

            async def flush(self):
                pass

            async def commit(self):
                pass

        monkeypatch.setattr(
            "app.services.verification_service.generate_answer", fake_generate
        )
        monkeypatch.setattr(
            "app.services.verification_service.get_verifier", lambda: FakeVerifier()
        )
        monkeypatch.setattr(
            "app.services.verification_service.generation_client", FakeGenerator()
        )
        monkeypatch.setattr(
            "app.services.verification_service.AsyncSessionLocal", lambda: NoopSession()
        )

        r = client.get("/verify", params={"q": "what is RAG?"})

        # Assert the status FIRST. A conditional `if r.status_code == 200:` would let this
        # test pass silently on a 500 — testing nothing at all.
        assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text[:300]}"

        body = r.json()
        assert body["verification_status"] == "verified"
        assert body["components"]["verifier"]["implementation"] == "RealVerifier"
        assert body["components"]["generator"]["implementation"] == "OpenRouterClient"
        assert body["n_claims"] >= 1

    def test_stub_components_downgrade_the_status(self, client, monkeypatch):
        """
        A stub anywhere in the chain means the result is NOT a real verification, and the
        response must say so — a client cannot see the server's console warning.
        """
        from app.services.verifier import StubVerifier
        from app.services.generation_client import StubGenerator

        async def fake_generate(question: str, top_k: int = 5):
            return {
                "question": question,
                "answer": "RAG combines retrieval with generation [1].",
                "evidence": [{"number": 1, "title": "T", "text": "RAG combines retrieval "
                                                                 "and generation.",
                              "chunk_id": 1}],
            }

        class NoopSession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            def add(self, obj):
                pass

            async def flush(self):
                pass

            async def commit(self):
                pass

        monkeypatch.setattr(
            "app.services.verification_service.generate_answer", fake_generate
        )
        monkeypatch.setattr(
            "app.services.verification_service.get_verifier", lambda: StubVerifier()
        )
        monkeypatch.setattr(
            "app.services.verification_service.generation_client", StubGenerator()
        )
        monkeypatch.setattr(
            "app.services.verification_service.AsyncSessionLocal", lambda: NoopSession()
        )

        r = client.get("/verify", params={"q": "what is RAG?"})
        assert r.status_code == 200
        body = r.json()
        assert body["verification_status"] == "development_stub", (
            "a stub-produced result must NOT claim to be 'verified'"
        )
        assert "warning" in body["components"]["verifier"]


class TestGenerationFailureDoesNotLoadTheVerifier:
    """
    Regression for a bug my own tests could not catch: the GenerationError handler called
    get_verifier() merely to DESCRIBE the verifier — which would construct (and download) a
    ~700MB model to report on a component that was never used, violating the very contract
    the failure path exists to uphold.

    The earlier test faked get_verifier(), so the real construction never happened and the
    violation was invisible. This one asserts the function is NOT CALLED AT ALL.
    """

    def test_get_verifier_is_not_called_on_generation_failure(self, client, monkeypatch):
        called: list[int] = []

        def exploding_get_verifier():
            called.append(1)
            raise AssertionError(
                "get_verifier() was called on a failed generation — this would load a "
                "700MB checkpoint to describe a verifier that never ran."
            )

        async def boom(question: str, top_k: int = 5):
            raise GenerationError("simulated outage")

        monkeypatch.setattr("app.services.verification_service.generate_answer", boom)
        monkeypatch.setattr(
            "app.services.verification_service.get_verifier", exploding_get_verifier
        )

        r = client.get("/verify", params={"q": "anything"})

        assert r.status_code == 503
        assert called == [], "the verifier must not be constructed when generation fails"
        assert r.json()["detail"]

    def test_failure_response_reports_the_verifier_as_not_invoked(self, client, monkeypatch):
        """The failure body should still be honest about which components ran."""
        from app.services.verification_service import _components_generation_failed

        comps = _components_generation_failed()
        assert comps["verifier"]["implementation"] == "not_invoked"
        assert "generator" in comps
