from tests.conftest import AUTH


def test_delete_product(client, product):
    resp = client.delete(f"/products/{product['id']}", headers=AUTH)
    assert resp.status_code == 204
    assert client.get(f"/products/{product['id']}").status_code == 404


def test_delete_unknown_product_404(client):
    assert client.delete("/products/999", headers=AUTH).status_code == 404
