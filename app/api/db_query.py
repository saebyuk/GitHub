from datetime import datetime
from time import perf_counter

from fastapi import APIRouter

from app.models.schemas import DBNLQueryRequest, DBNLQueryResponse, QueryHistoryItem
from app.repositories.history_repo import history_repo
from app.repositories.mariadb_repo import mariadb_repo
from app.services.nl2sql_service import to_safe_select

router = APIRouter(prefix="/api/v1/db", tags=["db"])


@router.post("/nl-query", response_model=DBNLQueryResponse)
def nl_query(payload: DBNLQueryRequest) -> DBNLQueryResponse:
    start = perf_counter()
    sql, params = to_safe_select(payload.question)
    rows = mariadb_repo.query(sql, params)
    latency = int((perf_counter() - start) * 1000) + 20
    summary = f"총 {len(rows)}건"

    history_repo.add(
        QueryHistoryItem(
            user_id=payload.user_id,
            question=payload.question,
            answer_summary=summary,
            mode="db_nl",
            latency_ms=latency,
            created_at=datetime.utcnow(),
        )
    )

    return DBNLQueryResponse(rows=rows, summary=summary, latency_ms=latency)
