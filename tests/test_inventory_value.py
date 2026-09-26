from tests.conftest import AUTH


def test_empty_inventory(client):
    assert client.get("/reports/inventory-value", headers=AUTH).json() == {"total_cents": 0, "products": 0}


def test_value_is_price_times_stock(client):
    client.post("/products", json={"sku": "A", "name": "A", "price_cents": 1250, "stock": 4}, headers=AUTH)
    client.post("/products", json={"sku": "B", "name": "B", "price_cents": 99, "stock": 10}, headers=AUTH)
    assert client.get("/reports/inventory-value", headers=AUTH).json() == {"total_cents": 5990, "products": 2}


def test_requires_api_key(client):
    assert client.get("/reports/inventory-value").status_code == 401
