from datetime import datetime

from fastapi import APIRouter

from app.models.schemas import QAQueryRequest, QAQueryResponse, QueryHistoryItem
from app.repositories.history_repo import history_repo
from app.services.qa_service import answer_question

router = APIRouter(prefix="/api/v1/qa", tags=["qa"])


@router.post("/query", response_model=QAQueryResponse)
def query(payload: QAQueryRequest) -> QAQueryResponse:
    result = answer_question(payload)
    history_repo.add(
        QueryHistoryItem(
            user_id=payload.user_id,
            question=payload.question,
            answer_summary=result.answer[:120],
            mode=payload.mode,
            latency_ms=result.latency_ms,
            tokens_in=result.tokens_in,
            tokens_out=result.tokens_out,
            created_at=datetime.utcnow(),
        )
    )
    return result
