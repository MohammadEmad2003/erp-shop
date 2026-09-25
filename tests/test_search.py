from tests.conftest import AUTH


def add(client, sku, name):
    client.post("/products", json={"sku": sku, "name": name, "price_cents": 100}, headers=AUTH)


def test_search_by_name_and_sku(client):
    add(client, "MUG-01", "Coffee mug")
    add(client, "TEA-02", "Tea cup")
    add(client, "PLT-03", "Dinner plate")

    assert [p["sku"] for p in client.get("/products/search", params={"q": "mug"}).json()] == ["MUG-01"]
    assert [p["sku"] for p in client.get("/products/search", params={"q": "TEA"}).json()] == ["TEA-02"]


def test_search_no_match(client):
    add(client, "MUG-01", "Coffee mug")
    assert client.get("/products/search", params={"q": "chair"}).json() == []


def test_search_requires_text(client):
    assert client.get("/products/search", params={"q": ""}).status_code == 422
