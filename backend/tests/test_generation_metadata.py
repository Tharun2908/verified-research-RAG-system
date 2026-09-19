"""Request-local provenance through the real generation and verification pipeline.

Only external HTTP, retrieval, database, and model scoring are faked.
"""

import asyncio
import threading

import httpx
import pytest

from app.services import generation_client as clients
from app.services import generator, verification_service as service


@pytest.fixture
def pipeline(monkeypatch):
    requests = []

    def respond(request):
        import json
        body = json.loads(request.content)
        prompt, model = body["messages"][0]["content"], body["model"]
        requests.append((prompt, model))
        if "Question: outage" in prompt:
            return httpx.Response(503)
        if "Question: second" in prompt and model == clients.GEN_MODELS[0]:
            return httpx.Response(429)
        name = "Second" if "Question: second" in prompt else "First"
        return httpx.Response(200, json={
            "choices": [{"message": {"content": f"{name} answer cites the evidence [1]."}}],
        })

    async_client = httpx.AsyncClient
    monkeypatch.setattr(clients.httpx, "AsyncClient", lambda **kw: async_client(
        transport=httpx.MockTransport(respond), **kw
    ))
    shared = clients.OpenRouterClient(api_key="test-only")
    monkeypatch.setattr(generator, "generation_client", shared)
    monkeypatch.setattr(service, "generation_client", shared)

    async def retrieve(question, top_k):
        return [{"chunk_id": 1, "title": "Evidence", "text": "Evidence for the answer."}]

    monkeypatch.setattr(generator, "hybrid_search", retrieve)

    class Verifier:
        def verify(self, claim, evidence):
            return 0.9
        def describe(self):
            return {"implementation": "RealVerifier", "model": "test-verifier"}

    monkeypatch.setattr(service, "get_verifier", lambda: Verifier())

    class Session:
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            return False
        def add(self, obj):
            pass
        async def flush(self):
            pass
        async def commit(self):
            pass

    monkeypatch.setattr(service, "AsyncSessionLocal", Session)
    return shared, requests, Verifier


@pytest.mark.asyncio
async def test_overlapping_requests_keep_their_own_models(pipeline, monkeypatch):
    """A pauses during scoring while B completes with the fallback model."""
    _, requests, Verifier = pipeline
    loop = asyncio.get_running_loop()
    first_scoring = asyncio.Event()
    release_first = threading.Event()

    class PausingVerifier(Verifier):
        def verify(self, claim, evidence):
            if claim.startswith("First"):
                loop.call_soon_threadsafe(first_scoring.set)
                assert release_first.wait(timeout=10), "first request was never released"
            return super().verify(claim, evidence)

    monkeypatch.setattr(service, "get_verifier", lambda: PausingVerifier())
    first_task = asyncio.create_task(service.verify_question("first"))
    try:
        await asyncio.wait_for(first_scoring.wait(), timeout=5)
        second = await asyncio.wait_for(service.verify_question("second"), timeout=5)
    finally:
        release_first.set()
        first = await asyncio.wait_for(first_task, timeout=5)

    assert first["answer"].startswith("First")
    assert second["answer"].startswith("Second")
    assert first["components"]["generator"]["model"] == clients.GEN_MODELS[0]
    assert second["components"]["generator"]["model"] == clients.GEN_MODELS[1]
    assert first["verification_status"] == second["verification_status"] == "verified"
    assert [model for _, model in requests] == [
        clients.GEN_MODELS[0], clients.GEN_MODELS[0], clients.GEN_MODELS[1],
    ]


@pytest.mark.asyncio
async def test_failure_after_success_has_no_answering_model(pipeline, monkeypatch):
    await service.verify_question("first")

    def forbidden():
        raise AssertionError("failure must not load the verifier or open the database")

    monkeypatch.setattr(service, "get_verifier", forbidden)
    monkeypatch.setattr(service, "AsyncSessionLocal", forbidden)
    failed = await service.verify_question("outage")
    assert failed["verification_status"] == "generation_failed"
    assert failed["answer"] is None
    assert failed["components"]["generator"]["model"] is None
    assert failed["components"]["verifier"]["implementation"] == "not_invoked"


@pytest.mark.asyncio
async def test_generation_exposes_fallback_metadata(pipeline):
    result = await generator.generate_answer("second")
    assert isinstance(result["answer"], str)
    assert result["generator"]["implementation"] == "OpenRouterClient"
    assert result["generator"]["model"] == clients.GEN_MODELS[1]
    assert result["evidence"][0]["number"] == 1


@pytest.mark.asyncio
async def test_stub_generation_keeps_warning_and_null_model(pipeline, monkeypatch):
    monkeypatch.setattr(generator, "generation_client", clients.StubGenerator())
    result = await service.verify_question("first")
    assert result["verification_status"] == "development_stub"
    assert result["components"]["generator"]["model"] is None
    assert "warning" in result["components"]["generator"]
