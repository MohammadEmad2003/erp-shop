import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth import require_api_key
from app.db import get_db

# Customer records are personal data: every endpoint is staff-only.
router = APIRouter(prefix="/customers", tags=["customers"], dependencies=[Depends(require_api_key)])


class CustomerIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=254)
    phone: str | None = Field(default=None, pattern=r"^\+?[0-9 ]{7,20}$")


class Customer(CustomerIn):
    id: int


@router.post("", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerIn, db: sqlite3.Connection = Depends(get_db)):
    try:
        cur = db.execute(
            "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
            (customer.name, customer.email.lower(), customer.phone),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A customer with this email already exists")
    return {"id": cur.lastrowid, **customer.model_dump(), "email": customer.email.lower()}


@router.get("", response_model=list[Customer])
def list_customers(db: sqlite3.Connection = Depends(get_db)):
    return [dict(r) for r in db.execute("SELECT * FROM customers ORDER BY name").fetchall()]


@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(row)
