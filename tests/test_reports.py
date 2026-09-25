from tests.conftest import AUTH


def add(client, sku, stock):
    client.post("/products", json={"sku": sku, "name": sku, "price_cents": 100, "stock": stock}, headers=AUTH)


def test_low_stock_lists_emptiest_first(client):
    add(client, "A", 12)
    add(client, "B", 0)
    add(client, "C", 5)
    add(client, "D", 3)

    resp = client.get("/reports/low-stock", headers=AUTH)
    assert [p["sku"] for p in resp.json()] == ["B", "D", "C"]


def test_custom_threshold(client):
    add(client, "A", 12)
    add(client, "B", 0)
    assert [p["sku"] for p in client.get("/reports/low-stock", params={"threshold": 0}, headers=AUTH).json()] == ["B"]


def test_threshold_must_be_in_range(client):
    assert client.get("/reports/low-stock", params={"threshold": -1}, headers=AUTH).status_code == 422
    assert client.get("/reports/low-stock", params={"threshold": 10_001}, headers=AUTH).status_code == 422


def test_report_requires_api_key(client):
    assert client.get("/reports/low-stock").status_code == 401
