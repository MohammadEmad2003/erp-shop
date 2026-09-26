import csv
import io
import sqlite3

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.auth import require_api_key
from app.db import get_db

router = APIRouter(prefix="/exports", tags=["exports"], dependencies=[Depends(require_api_key)])


@router.get("/products.csv")
def export_products(db: sqlite3.Connection = Depends(get_db)):
    """The catalogue as CSV, one row per product."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["sku", "name", "price", "stock"])
    for row in db.execute("SELECT sku, name, price_cents, stock FROM products ORDER BY sku"):
        writer.writerow([row["sku"], row["name"], f"{row['price_cents'] / 100:.2f}", row["stock"]])
    return Response(
        content=out.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"},
    )
