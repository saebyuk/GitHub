# Colab 실행 가이드

아래 절차대로 진행하면 **현재 Git 저장소를 Colab에서 clone → 실행 → 시험**할 수 있습니다.

## 0) 먼저 GitHub URL 준비 (필수)
현재 로컬 저장소에 원격(remote)이 없으면 Colab에서 clone할 URL이 없습니다.

### 0-1. GitHub 저장소 생성
GitHub에서 새 저장소를 만든 뒤 URL을 확보합니다.
- HTTPS 예: `https://github.com/<ORG_OR_USER>/<REPO>.git`

### 0-2. 현재 코드 push
로컬에서 아래 명령 실행:
```bash
git remote add origin https://github.com/<ORG_OR_USER>/<REPO>.git
git push -u origin work
```

원격 URL 확인:
```bash
git remote -v
```

---

## 1) Colab에서 코드 clone
```python
!git clone https://github.com/<ORG_OR_USER>/<REPO>.git
%cd <REPO>
!git checkout work
```

---

## 2) 의존성 설치
```python
!python -m pip install --upgrade pip
!pip install -r requirements.txt
```

---

## 3) 서버 실행
```python
import threading, uvicorn

def run_api():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

thread = threading.Thread(target=run_api, daemon=True)
thread.start()
```

---

## 4) 기능 시험 (API)
```python
import requests

print("health:", requests.get("http://127.0.0.1:8000/health").json())

qa_payload = {"question": "인증서 갱신 절차 알려줘", "mode": "rag", "user_id": "u001"}
print("qa:", requests.post("http://127.0.0.1:8000/api/v1/qa/query", json=qa_payload).json())

nl_payload = {"question": "최근 7일 crl 오류 이력 보여줘", "user_id": "u001"}
print("db:", requests.post("http://127.0.0.1:8000/api/v1/db/nl-query", json=nl_payload).json())

print("history:", requests.get("http://127.0.0.1:8000/api/v1/history/recent", params={"user_id":"u001","limit":10}).json())
print("metrics:", requests.get("http://127.0.0.1:8000/api/v1/metrics/summary").json())
```

---

## 5) 기능 시험 (UI)
Colab에서 직접 브라우저 접근 테스트가 필요하면 터널링 도구(예: cloudflared/ngrok) 사용이 필요합니다.
API 시험만으로도 동작 검증은 가능합니다.

---

## 6) MariaDB 실연결 (선택)
1. Colab에서 MariaDB 접근 가능한 네트워크가 있어야 합니다.
2. `.env`에 `ENABLE_MARIADB=true` 및 접속정보를 설정하세요.
3. `scripts/init_db.sql`, `scripts/seed_pki_history.sql` 실행 후 재시험하세요.

---

## 7) 자동 테스트 실행 (선택)
```python
!pytest -q tests/test_api_smoke.py
```
