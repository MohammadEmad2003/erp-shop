import logging


def test_requests_are_logged(client, caplog):
    with caplog.at_level(logging.INFO, logger="erp.requests"):
        client.get("/health")
    assert any("GET /health -> 200" in r.getMessage() for r in caplog.records)
