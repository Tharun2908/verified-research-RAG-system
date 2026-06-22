import os

try:
    import torch
    torch_threads = int(os.getenv("TORCH_NUM_THREADS", "4"))
    torch.set_num_threads(torch_threads)
    try:
        torch.set_num_interop_threads(1)
    except Exception:
        pass  # can't change interop threads after init; intra-op is the one that matters here
    print(f"[startup] torch intra-op threads = {torch.get_num_threads()}")
except Exception as e:
    print(f"[startup] torch thread config skipped: {e}")


from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api.routes_health import router as health_router
from app.api.routes_search import router as search_router
from app.api.routes_retrieve import router as retrieve_router
from app.api.routes_research import router as research_router
from app.api.routes_verify import router as verify_router
from app.services.bm25_retriever import warm_bm25


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Build the BM25 index once at startup so no request pays the rebuild cost.
    n = await warm_bm25()
    print(f"[startup] BM25 index built over {n} chunks.")
    yield
    # (no teardown needed)


app = FastAPI(title="Verified Research Agent", lifespan=lifespan)

# plug in the health router and search router
app.include_router(health_router)

app.include_router(search_router) 

app.include_router(retrieve_router) 

app.include_router(research_router) 

app.include_router(verify_router) 

# mount the Prometheus /metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    return {"service": "verified-research-agent", "status": "running"}