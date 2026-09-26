from tests.conftest import AUTH


def add(client, sku, category=None):
    body = {"sku": sku, "name": sku, "price_cents": 100}
    if category:
        body["category"] = category
    return client.post("/products", json=body, headers=AUTH).json()


def test_filter_by_category(client):
    add(client, "MUG", "kitchen")
    add(client, "PEN", "office")
    add(client, "CUP", "kitchen")
    assert [p["sku"] for p in client.get("/products", params={"category": "kitchen"}).json()] == ["MUG", "CUP"]


def test_category_is_optional(client):
    assert add(client, "BAG")["category"] is None
    assert len(client.get("/products").json()) == 1


def test_empty_category_rejected(client):
    resp = client.post("/products", json={"sku": "X", "name": "X", "price_cents": 1, "category": ""}, headers=AUTH)
    assert resp.status_code == 422
