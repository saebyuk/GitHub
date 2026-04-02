from fastapi import APIRouter, Query

from app.models.schemas import MetricsSummary
from app.services.metrics_service import summarize

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])


@router.get("/summary", response_model=MetricsSummary)
def summary(
    mode: str = Query("all"), period: str = Query("24h"), device: str = Query("all")
) -> MetricsSummary:
    data = summarize(mode=mode, period=period, device=device)
    return MetricsSummary(**data)
