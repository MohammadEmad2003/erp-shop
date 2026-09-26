from tests.conftest import AUTH


def test_health(client):
    assert client.get("/health").json() == {"status": "ok", "database": "ok"}


def test_create_and_get_product(client, product):
    assert product["sku"] == "MUG-01"
    assert client.get(f"/products/{product['id']}").json() == product


def test_list_products(client, product):
    assert client.get("/products").json() == [product]


def test_create_requires_api_key(client):
    resp = client.post("/products", json={"sku": "X", "name": "X", "price_cents": 1})
    assert resp.status_code == 401


def test_duplicate_sku_conflicts(client, product):
    resp = client.post("/products", json={"sku": "MUG-01", "name": "Other", "price_cents": 1}, headers=AUTH)
    assert resp.status_code == 409


def test_negative_price_rejected(client):
    resp = client.post("/products", json={"sku": "BAD", "name": "Bad", "price_cents": -1}, headers=AUTH)
    assert resp.status_code == 422


def test_unknown_product_404(client):
    assert client.get("/products/999").status_code == 404
