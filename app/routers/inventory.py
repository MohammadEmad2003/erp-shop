import sqlite3

from fastapi import APIRouter, Depends

from app.auth import require_api_key
from app.db import get_db

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(require_api_key)])


@router.get("/inventory-value")
def inventory_value(db: sqlite3.Connection = Depends(get_db)):
    """What the stock on hand is worth, in integer cents."""
    row = db.execute(
        "SELECT COALESCE(SUM(price_cents * stock), 0) AS total, COUNT(*) AS n FROM products"
    ).fetchone()
    return {"total_cents": row["total"], "products": row["n"]}
