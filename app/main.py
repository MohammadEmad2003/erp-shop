from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routers import exports, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="ERP Shop", lifespan=lifespan)
app.include_router(products.router)
app.include_router(exports.router)


@app.get("/health")
def health():
    return {"status": "ok"}
