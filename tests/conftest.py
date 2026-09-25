import pytest
from fastapi.testclient import TestClient

API_KEY = "test-key"
AUTH = {"X-API-Key": API_KEY}


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("ERP_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("ERP_API_KEY", API_KEY)
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def product(client):
    resp = client.post(
        "/products",
        json={"sku": "MUG-01", "name": "Coffee mug", "price_cents": 1250, "stock": 10},
        headers=AUTH,
    )
    return resp.json()
