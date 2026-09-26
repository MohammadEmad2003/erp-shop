from tests.conftest import AUTH


def test_sku_is_trimmed_and_uppercased(client):
    resp = client.post("/products", json={"sku": "  mug-01 ", "name": "Mug", "price_cents": 100}, headers=AUTH)
    assert resp.json()["sku"] == "MUG-01"


def test_case_variants_conflict(client):
    client.post("/products", json={"sku": "MUG-01", "name": "Mug", "price_cents": 100}, headers=AUTH)
    resp = client.post("/products", json={"sku": "mug-01", "name": "Mug 2", "price_cents": 100}, headers=AUTH)
    assert resp.status_code == 409


def test_blank_sku_rejected(client):
    assert client.post("/products", json={"sku": "   ", "name": "X", "price_cents": 1}, headers=AUTH).status_code == 422
