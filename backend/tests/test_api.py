def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_analyze_dangerous(client):
    response = client.post("/api/analyze", json={"url": "http://paypal.com@evil.tk/login"})
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "dangerous"
    assert body["verdict_label"] == {"ar": "خطر", "en": "Dangerous"}
    assert body["advice"]["ar"] and body["advice"]["en"]
    assert {f["rule_id"] for f in body["findings"]} >= {"at_symbol", "brand_impersonation"}


def test_analyze_safe(client):
    body = client.post("/api/analyze", json={"url": "https://www.google.com"}).json()
    assert body["verdict"] == "safe"
    assert body["findings"] == []


def test_analyze_empty_returns_422(client):
    response = client.post("/api/analyze", json={"url": "  "})
    assert response.status_code == 422
    assert response.json()["detail"]["message"]["ar"]


def test_batch_from_text(client):
    text = "Check https://www.google.com and hxxp://g00gle-verify[.]tk/login and www.bit.ly/x"
    response = client.post("/api/analyze/batch", json={"text": text})
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["total"] == 3
    assert body["summary"]["safe"] >= 1
    assert body["summary"]["dangerous"] >= 1
    assert body["items"][1]["input"] == "http://g00gle-verify.tk/login"


def test_batch_with_invalid_entries(client):
    body = client.post("/api/analyze/batch", json={"urls": ["https://example.com", "not a url"]}).json()
    assert body["summary"]["invalid"] == 1
    assert body["items"][1]["error"]["en"]


def test_batch_without_urls_returns_422(client):
    assert client.post("/api/analyze/batch", json={"text": "no links"}).status_code == 422
    assert client.post("/api/analyze/batch", json={}).status_code == 422


def test_history_and_stats(client):
    client.post("/api/analyze", json={"url": "https://www.google.com"})
    client.post("/api/analyze", json={"url": "http://192.168.0.1/paypal/login"})

    page = client.get("/api/history").json()
    assert page["total"] == 2
    assert page["items"][0]["host"] == "192.168.0.1"

    dangerous = client.get("/api/history", params={"verdict": "dangerous"}).json()
    assert dangerous["total"] == 1

    stats = client.get("/api/stats").json()
    assert stats["total"] == 2
    assert stats["safe"] == 1 and stats["dangerous"] == 1
    assert any(r["rule_id"] == "ip_address" for r in stats["top_rules"])

    scan_id = page["items"][0]["id"]
    assert client.delete(f"/api/history/{scan_id}").status_code == 204
    assert client.delete(f"/api/history/{scan_id}").status_code == 404
    assert client.get("/api/history").json()["total"] == 1

    assert client.delete("/api/history").json() == {"deleted": 1}
    assert client.get("/api/stats").json()["total"] == 0
