from tests.conftest import AUTH


def test_apply_ten_percent(client):
    client.post("/discounts", json={"code": "save10", "percent": 10}, headers=AUTH)
    resp = client.get("/discounts/SAVE10/apply", params={"amount_cents": 5000})
    assert resp.json() == {"amount_cents": 5000, "discount_cents": 500, "total_cents": 4500}


def test_unknown_code_404(client):
    assert client.get("/discounts/NOPE/apply", params={"amount_cents": 100}).status_code == 404


def test_create_requires_api_key(client):
    assert client.post("/discounts", json={"code": "FREE", "percent": 5}).status_code == 401
