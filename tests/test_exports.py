from tests.conftest import AUTH


def test_export_lists_products(client, product):
    resp = client.get("/exports/products.csv", headers=AUTH)
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/csv")
    lines = resp.text.strip().splitlines()
    assert lines[0] == "sku,name,price,stock"
    assert lines[1] == "MUG-01,Coffee mug,12.50,10"


def test_export_requires_api_key(client):
    assert client.get("/exports/products.csv").status_code == 401
