import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth import require_api_key
from app.db import get_db

router = APIRouter(prefix="/discounts", tags=["discounts"])


class DiscountIn(BaseModel):
    code: str = Field(min_length=3, max_length=20)
    percent: int = Field(ge=0)


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_key)])
def create_discount(discount: DiscountIn, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute("INSERT INTO discount_codes (code, percent) VALUES (?, ?)", (discount.code.upper(), discount.percent))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Code already exists")
    return {"code": discount.code.upper(), "percent": discount.percent}


@router.get("/{code}/apply")
def apply_discount(code: str, amount_cents: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT percent FROM discount_codes WHERE code = ?", (code.upper(),)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Unknown discount code")
    discount = amount_cents * row["percent"] // 100
    return {"amount_cents": amount_cents, "discount_cents": discount, "total_cents": amount_cents - discount}
