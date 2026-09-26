from tests.conftest import AUTH


def place(client, product_id, quantity):
    return client.post(
        "/orders",
        json={"customer_email": "alice@example.com", "items": [{"product_id": product_id, "quantity": quantity}]},
        headers=AUTH,
    )


def test_order_takes_stock_and_totals(client, product):
    resp = place(client, product["id"], 3)
    assert resp.status_code == 201
    assert resp.json()["total_cents"] == 3 * 1250
    assert client.get(f"/products/{product['id']}").json()["stock"] == 7


def test_insufficient_stock_conflicts(client, product):
    assert place(client, product["id"], 11).status_code == 409
    assert client.get(f"/products/{product['id']}").json()["stock"] == 10


def test_unknown_product_404(client):
    assert place(client, 999, 1).status_code == 404


def test_get_order(client, product):
    created = place(client, product["id"], 2).json()
    fetched = client.get(f"/orders/{created['id']}", headers=AUTH).json()
    assert fetched["items"] == [{"product_id": product["id"], "quantity": 2, "unit_price_cents": 1250}]


def test_orders_require_api_key(client, product):
    resp = client.post("/orders", json={"customer_email": "a@b.c", "items": [{"product_id": 1, "quantity": 1}]})
    assert resp.status_code == 401
