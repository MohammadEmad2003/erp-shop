def test_health_reports_database_down(client, tmp_path, monkeypatch):
    # A directory can't be opened as a database file.
    monkeypatch.setenv("ERP_DB_PATH", str(tmp_path))
    resp = client.get("/health")
    assert resp.status_code == 503
    assert resp.json()["database"] == "unreachable"
