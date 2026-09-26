import sqlite3

from fastapi import APIRouter, Depends, Query

from app.auth import require_api_key
from app.db import get_db
from app.routers.products import Product

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(require_api_key)])


@router.get("/low-stock", response_model=list[Product])
def low_stock(
    threshold: int = Query(default=5, ge=0, le=10_000),
    db: sqlite3.Connection = Depends(get_db),
):
    """Products at or below `threshold` units, emptiest first, for reordering."""
    rows = db.execute(
        "SELECT * FROM products WHERE stock <= ? ORDER BY stock, name", (threshold,)
    ).fetchall()
    return [dict(r) for r in rows]
