from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routers import products, quotes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="ERP Shop", lifespan=lifespan)
app.include_router(products.router)
app.include_router(quotes.router)


@app.get("/health")
def health():
    return {"status": "ok"}
