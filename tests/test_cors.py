def test_storefront_origin_is_allowed(client):
    resp = client.options(
        "/products",
        headers={"Origin": "https://shop.example.com", "Access-Control-Request-Method": "GET"},
    )
    assert resp.status_code == 200
    assert "access-control-allow-origin" in resp.headers
