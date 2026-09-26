from tests.conftest import AUTH


def test_price_change_is_recorded(client, product):
    resp = client.put(f"/products/{product['id']}/price", json={"price_cents": 1500}, headers=AUTH)
    assert resp.json()["price_cents"] == 1500
    history = client.get(f"/products/{product['id']}/price-history").json()
    assert [(h["old_cents"], h["new_cents"]) for h in history] == [(1250, 1500)]


def test_negative_price_rejected(client, product):
    assert client.put(f"/products/{product['id']}/price", json={"price_cents": -1}, headers=AUTH).status_code == 422


def test_unknown_product_404(client):
    assert client.put("/products/999/price", json={"price_cents": 1}, headers=AUTH).status_code == 404


def test_requires_api_key(client, product):
    assert client.put(f"/products/{product['id']}/price", json={"price_cents": 1}).status_code == 401
