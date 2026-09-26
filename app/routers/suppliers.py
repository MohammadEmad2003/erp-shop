import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth import require_api_key
from app.db import get_db

router = APIRouter(prefix="/suppliers", tags=["suppliers"], dependencies=[Depends(require_api_key)])


class SupplierIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str | None = Field(default=None, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=254)
    phone: str | None = Field(default=None, pattern=r"^\+?[0-9 ]{7,20}$")


class Supplier(SupplierIn):
    id: int


@router.post("", response_model=Supplier, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierIn, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        "INSERT INTO suppliers (name, email, phone) VALUES (?, ?, ?)",
        (supplier.name, supplier.email, supplier.phone),
    )
    db.commit()
    return {"id": cur.lastrowid, **supplier.model_dump()}


@router.get("", response_model=list[Supplier])
def list_suppliers(db: sqlite3.Connection = Depends(get_db)):
    return [dict(r) for r in db.execute("SELECT * FROM suppliers ORDER BY name").fetchall()]


@router.get("/{supplier_id}", response_model=Supplier)
def get_supplier(supplier_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return dict(row)
