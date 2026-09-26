import pytest

from tests.conftest import AUTH


@pytest.fixture
def seven_products(client):
    for i in range(7):
        client.post("/products", json={"sku": f"SKU-{i}", "name": f"Item {i}", "price_cents": 100}, headers=AUTH)


def test_pages_through_products(client, seven_products):
    first = client.get("/products", params={"limit": 3})
    assert [p["sku"] for p in first.json()] == ["SKU-0", "SKU-1", "SKU-2"]
    assert first.headers["X-Total-Count"] == "7"

    last = client.get("/products", params={"limit": 3, "offset": 6})
    assert [p["sku"] for p in last.json()] == ["SKU-6"]


def test_default_page_returns_everything_small(client, seven_products):
    assert len(client.get("/products").json()) == 7


@pytest.mark.parametrize("params", [{"limit": 0}, {"limit": 101}, {"offset": -1}])
def test_bounds_are_enforced(client, params):
    assert client.get("/products", params=params).status_code == 422
