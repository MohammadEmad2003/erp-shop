import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth import require_api_key
from app.db import get_db

router = APIRouter(prefix="/products", tags=["products"])


class ProductIn(BaseModel):
    sku: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=120)
    price_cents: int = Field(ge=0)
    stock: int = Field(default=0, ge=0)


class Product(ProductIn):
    id: int


@router.get("", response_model=list[Product])
def list_products(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM products ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_key)])
def create_product(product: ProductIn, db: sqlite3.Connection = Depends(get_db)):
    try:
        cur = db.execute(
            "INSERT INTO products (sku, name, price_cents, stock) VALUES (?, ?, ?, ?)",
            (product.sku, product.name, product.price_cents, product.stock),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail=f"SKU {product.sku} already exists")
    return {"id": cur.lastrowid, **product.model_dump()}


class PriceIn(BaseModel):
    price_cents: int = Field(ge=0)


@router.put("/{product_id}/price", response_model=Product, dependencies=[Depends(require_api_key)])
def change_price(product_id: int, body: PriceIn, db: sqlite3.Connection = Depends(get_db)):
    """Change the price and log the change atomically."""
    with db:
        row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        db.execute("UPDATE products SET price_cents = ? WHERE id = ?", (body.price_cents, product_id))
        db.execute(
            "INSERT INTO price_changes (product_id, old_cents, new_cents) VALUES (?, ?, ?)",
            (product_id, row["price_cents"], body.price_cents),
        )
    return {**dict(row), "price_cents": body.price_cents}


@router.get("/{product_id}/price-history")
def price_history(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute(
        "SELECT old_cents, new_cents, changed_at FROM price_changes WHERE product_id = ? ORDER BY id DESC",
        (product_id,),
    ).fetchall()
    return [dict(r) for r in rows]
