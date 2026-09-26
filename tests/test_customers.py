import pytest

from tests.conftest import AUTH

ALICE = {"name": "Alice Hassan", "email": "Alice@Example.com", "phone": "+20 100 123 4567"}


def test_create_customer_normalizes_email(client):
    resp = client.post("/customers", json=ALICE, headers=AUTH)
    assert resp.status_code == 201
    assert resp.json()["email"] == "alice@example.com"


def test_duplicate_email_conflicts_case_insensitively(client):
    client.post("/customers", json=ALICE, headers=AUTH)
    resp = client.post("/customers", json={**ALICE, "email": "ALICE@example.com"}, headers=AUTH)
    assert resp.status_code == 409


@pytest.mark.parametrize("email", ["not-an-email", "a@b", "a b@c.com"])
def test_invalid_email_rejected(client, email):
    assert client.post("/customers", json={**ALICE, "email": email}, headers=AUTH).status_code == 422


@pytest.mark.parametrize("method,path", [("GET", "/customers"), ("GET", "/customers/1"), ("POST", "/customers")])
def test_every_endpoint_requires_api_key(client, method, path):
    assert client.request(method, path, json=ALICE).status_code == 401


def test_get_customer(client):
    created = client.post("/customers", json=ALICE, headers=AUTH).json()
    assert client.get(f"/customers/{created['id']}", headers=AUTH).json() == created
    assert client.get("/customers/999", headers=AUTH).status_code == 404
