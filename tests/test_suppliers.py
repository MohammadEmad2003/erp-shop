from tests.conftest import AUTH

ACME = {"name": "Acme Ceramics", "email": "sales@acme.example", "phone": "+20 2 1234 5678"}


def test_create_and_get_supplier(client):
    created = client.post("/suppliers", json=ACME, headers=AUTH)
    assert created.status_code == 201
    assert client.get(f"/suppliers/{created.json()['id']}", headers=AUTH).json() == created.json()


def test_list_is_sorted_by_name(client):
    client.post("/suppliers", json={"name": "Zeta"}, headers=AUTH)
    client.post("/suppliers", json={"name": "Alpha"}, headers=AUTH)
    assert [s["name"] for s in client.get("/suppliers", headers=AUTH).json()] == ["Alpha", "Zeta"]


def test_invalid_email_rejected(client):
    assert client.post("/suppliers", json={**ACME, "email": "nope"}, headers=AUTH).status_code == 422


def test_requires_api_key(client):
    assert client.get("/suppliers").status_code == 401
    assert client.get("/suppliers/999", headers=AUTH).status_code == 404
