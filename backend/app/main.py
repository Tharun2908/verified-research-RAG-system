from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.api.routes_health import router as health_router

# create the app
app = FastAPI(title="Verified Research Agent")

# plug in the health router
app.include_router(health_router)

# mount the Prometheus /metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    return {"service": "verified-research-agent", "status": "running"}