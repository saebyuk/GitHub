# 폐쇄망 On-Device LLM 도우미 PoC

PDF 매뉴얼 기반 QA(RAG/LLM-Only 선택) + MariaDB 자연어 조회 + 질의 이력/메트릭 API + **통합 웹 UI(사용자/관리자)**를 포함한 PoC 프로젝트입니다.

## 구현 상태 (현재 코드 기준)
- FastAPI 서버 및 핵심 API 구현
- 브라우저 UI(`/`)에서 사용자 기능(QA/DB조회/이력/메트릭) + 관리자 기능(문서업로드/검수/재학습) 실행 가능
- DB 자연어 질의 시 생성된 SQL을 미리 확인하고 실행 여부를 선택 가능
- QA 모드 선택(`rag`, `llm_only`) 구현
- MariaDB NL2SQL(안전 SELECT 템플릿) 구현
- 최근 질의 이력 조회 API 구현(메모리 저장소)
- 메트릭 요약 API 구현
- 관리자 업로드/재인덱싱 PoC 스텁 API 구현
- DB 초기화/시드 SQL 제공
- Colab 실행 가이드 제공

## 빠른 시작

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

- UI: `http://127.0.0.1:8000/`
- 헬스체크: `http://127.0.0.1:8000/health`

## 주요 API

### 1) QA
- `POST /api/v1/qa/query`
```json
{
  "question": "인증서 갱신 절차 알려줘",
  "mode": "rag",
  "user_id": "u001"
}
```

### 2) MariaDB 자연어 조회
- `POST /api/v1/db/translate-sql` (SQL 미리보기)
- `POST /api/v1/db/nl-query` (조회 실행)
```json
{
  "question": "최근 7일 CRL 오류 이력 보여줘",
  "user_id": "u001"
}
```

### 3) 최근 질의 이력
- `GET /api/v1/history/recent?user_id=u001&limit=20`

### 4) 메트릭 요약
- `GET /api/v1/metrics/summary?mode=all&period=24h&device=all`

### 5) 관리자 PoC API
- `POST /api/v1/admin/documents/upload`
- `GET /api/v1/admin/documents`
- `POST /api/v1/admin/knowledge/review`
- `GET /api/v1/admin/knowledge/reviews`
- `POST /api/v1/admin/reindex`

## 디렉토리 구조

```text
app/
  main.py
  templates/
    index.html
  api/
    admin.py
    db_query.py
    history.py
    metrics.py
    qa.py
    ui.py
  core/
    config.py
    logging.py
  models/
    schemas.py
  repositories/
    history_repo.py
    mariadb_repo.py
  services/
    metrics_service.py
    nl2sql_service.py
    qa_service.py
scripts/
  init_db.sql
  seed_pki_history.sql
docs/
  colab_run_guide.md
  dependency_manifest.md
```

## MariaDB 설정
기본은 Mock 모드(`ENABLE_MARIADB=false`)로 동작합니다.
실DB 연결 시 `.env`에서 다음 설정:

```env
ENABLE_MARIADB=true
MARIADB_HOST=...
MARIADB_PORT=3306
MARIADB_USER=...
MARIADB_PASSWORD=...
MARIADB_DATABASE=...
```

그리고 아래 SQL 실행:
- `scripts/init_db.sql`
- `scripts/seed_pki_history.sql`

## Colab 실행
`docs/colab_run_guide.md` 순서대로 실행하면 Colab에서 바로 API 확인 가능합니다.

## GitHub URL 준비 (Colab clone 전 필수)
현재 저장소를 Colab에서 clone하려면 GitHub 원격 URL이 필요합니다.

```bash
git remote add origin https://github.com/<ORG_OR_USER>/<REPO>.git
git push -u origin work
git remote -v
```


## 자연어 약화 방지(반영)
- Query Rewrite 및 도메인 키워드 처리
- RAG/LLM-Only 모드 분리
- 모호한 질문에 대한 구조화 응답 기반(qa_service)
- 모드별 로그/메트릭 분리 수집

## 다음 단계
- PDF 실제 파싱/정제 파이프라인 고도화
- 벡터 인덱스 및 로컬 LLM 실연동
- 성능 대시보드 시각화 UI 고도화
- 폐쇄망 배포용 아티팩트/체크섬 관리 강화
