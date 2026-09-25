import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth import require_api_key
from app.db import get_db

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(require_api_key)])


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderIn(BaseModel):
    customer_email: str = Field(min_length=3, max_length=254)
    items: list[OrderItemIn] = Field(min_length=1)


class OrderItem(OrderItemIn):
    unit_price_cents: int


class Order(BaseModel):
    id: int
    customer_email: str
    total_cents: int
    items: list[OrderItem]


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderIn, db: sqlite3.Connection = Depends(get_db)):
    """Place an order and take the ordered quantities out of stock."""
    total = 0
    lines = []
    for item in order.items:
        product = db.execute(
            "SELECT price_cents, stock FROM products WHERE id = ?", (item.product_id,)
        ).fetchone()
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product["stock"] < item.quantity:
            raise HTTPException(status_code=409, detail=f"Not enough stock for product {item.product_id}")

        db.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (product["stock"] - item.quantity, item.product_id),
        )
        total += product["price_cents"] * item.quantity
        lines.append({**item.model_dump(), "unit_price_cents": product["price_cents"]})

    cur = db.execute(
        "INSERT INTO orders (customer_email, total_cents) VALUES (?, ?)", (order.customer_email, total)
    )
    order_id = cur.lastrowid
    for line in lines:
        db.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents) VALUES (?, ?, ?, ?)",
            (order_id, line["product_id"], line["quantity"], line["unit_price_cents"]),
        )
    db.commit()
    return {"id": order_id, "customer_email": order.customer_email, "total_cents": total, "items": lines}


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: sqlite3.Connection = Depends(get_db)):
    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    items = db.execute(
        "SELECT product_id, quantity, unit_price_cents FROM order_items WHERE order_id = ?", (order_id,)
    ).fetchall()
    return {**dict(order), "items": [dict(i) for i in items]}
