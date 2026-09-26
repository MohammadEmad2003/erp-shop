from contextlib import asynccontextmanager

import sqlite3

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.db import connect, init_db
from app.routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="ERP Shop", lifespan=lifespan)
app.include_router(products.router)


@app.get("/health")
def health():
    try:
        conn = connect()
        try:
            conn.execute("SELECT 1")
        finally:
            conn.close()
    except sqlite3.Error:
        return JSONResponse(status_code=503, content={"status": "degraded", "database": "unreachable"})
    return {"status": "ok", "database": "ok"}
