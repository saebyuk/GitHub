from fastapi import APIRouter, Query

from app.repositories.history_repo import history_repo

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("/recent")
def recent(user_id: str = Query(...), limit: int = Query(20, ge=1, le=100)) -> list[dict]:
    return [item.model_dump() for item in history_repo.recent(user_id=user_id, limit=limit)]
