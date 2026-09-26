from tests.conftest import AUTH


def test_patch_changes_only_given_fields(client, product):
    resp = client.patch(f"/products/{product['id']}", json={"price_cents": 1400}, headers=AUTH)
    assert resp.json()["price_cents"] == 1400
    assert resp.json()["name"] == "Coffee mug"


def test_patch_unknown_product_404(client):
    assert client.patch("/products/999", json={"name": "X"}, headers=AUTH).status_code == 404


def test_patch_requires_api_key(client, product):
    assert client.patch(f"/products/{product['id']}", json={"name": "X"}).status_code == 401
