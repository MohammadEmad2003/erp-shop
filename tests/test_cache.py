def test_repeated_calls_return_the_same_list(client, product):
    first = client.get("/products").json()
    assert client.get("/products").json() == first == [product]
