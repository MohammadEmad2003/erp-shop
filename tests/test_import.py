from tests.conftest import AUTH

ROWS = [
    {"sku": "A-1", "name": "Plate", "price_cents": 800, "stock": 12},
    {"sku": "A-2", "name": "Bowl", "price_cents": 650, "stock": 20},
]


def test_import_creates_all_rows(client):
    resp = client.post("/products/import", json=ROWS, headers=AUTH)
    assert resp.json() == {"created": 2}
    assert len(client.get("/products").json()) == 2


def test_import_requires_api_key(client):
    assert client.post("/products/import", json=ROWS).status_code == 401
