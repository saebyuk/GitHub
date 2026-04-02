from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ui_index():
    r = client.get("/")
    assert r.status_code == 200
    assert "PoC UI" in r.text


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_qa_and_history():
    payload = {"question": "인증서 갱신 절차 알려줘", "mode": "rag", "user_id": "u001"}
    qa = client.post("/api/v1/qa/query", json=payload)
    assert qa.status_code == 200
    assert qa.json()["mode"] == "rag"

    hist = client.get("/api/v1/history/recent", params={"user_id": "u001", "limit": 10})
    assert hist.status_code == 200
    assert len(hist.json()) >= 1


def test_db_nl_query_mock():
    payload = {"question": "최근 7일 crl 오류", "user_id": "u001"}
    r = client.post("/api/v1/db/nl-query", json=payload)
    assert r.status_code == 200
    assert "rows" in r.json()
