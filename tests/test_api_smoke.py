from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ui_index():
    r = client.get("/")
    assert r.status_code == 200
    assert "사용자 화면" in r.text
    assert "관리자 화면" in r.text


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
    body = r.json()
    assert "rows" in body
    assert "generated_sql" in body



def test_db_translate_sql_preview():
    payload = {"question": "최근 3일 ocsp 오류", "user_id": "u001"}
    r = client.post("/api/v1/db/translate-sql", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "generated_sql" in body
    assert "SELECT" in body["generated_sql"]


def test_admin_review_and_docs():
    review_payload = {
        "source": "manual.pdf#p1",
        "original_text": "기존 문장",
        "revised_text": "수정된 문장",
        "reviewer": "admin01",
    }
    rv = client.post("/api/v1/admin/knowledge/review", json=review_payload)
    assert rv.status_code == 200
    reviews = client.get("/api/v1/admin/knowledge/reviews")
    assert reviews.status_code == 200
    assert len(reviews.json()) >= 1

    docs = client.get("/api/v1/admin/documents")
    assert docs.status_code == 200
