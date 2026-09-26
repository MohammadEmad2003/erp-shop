import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.db import init_db
from app.routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="ERP Shop", lifespan=lifespan)
app.include_router(products.router)

log = logging.getLogger("erp.requests")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log.info("%s %s -> %s headers=%s", request.method, request.url.path, response.status_code, dict(request.headers))
    return response


@app.get("/health")
def health():
    return {"status": "ok"}
