def test_quote_adds_vat(client, product):
    resp = client.post("/quotes", json={"items": [{"product_id": product["id"], "quantity": 2}]})
    assert resp.status_code == 200
    assert resp.json() == {"subtotal": 25.0, "vat": 3.5, "total": 28.5}


def test_quote_unknown_product_404(client):
    assert client.post("/quotes", json={"items": [{"product_id": 999, "quantity": 1}]}).status_code == 404


def test_quote_rejects_zero_quantity(client, product):
    resp = client.post("/quotes", json={"items": [{"product_id": product["id"], "quantity": 0}]})
    assert resp.status_code == 422
