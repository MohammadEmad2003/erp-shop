import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.db import get_db

router = APIRouter(prefix="/quotes", tags=["quotes"])

VAT_RATE = 0.14  # Egyptian standard VAT


class QuoteLine(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class QuoteIn(BaseModel):
    items: list[QuoteLine] = Field(min_length=1)


class Quote(BaseModel):
    subtotal: float
    vat: float
    total: float


@router.post("", response_model=Quote)
def create_quote(quote: QuoteIn, db: sqlite3.Connection = Depends(get_db)):
    """Price a basket before checkout: subtotal, VAT and the total to pay."""
    subtotal = 0.0
    for line in quote.items:
        row = db.execute("SELECT price_cents FROM products WHERE id = ?", (line.product_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Product {line.product_id} not found")
        price = row["price_cents"] / 100
        subtotal += price * line.quantity

    vat = round(subtotal * VAT_RATE, 2)
    return {"subtotal": subtotal, "vat": vat, "total": subtotal + vat}
