from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class QAQueryRequest(BaseModel):
    question: str = Field(min_length=2)
    mode: Literal["rag", "llm_only"] = "rag"
    user_id: str = Field(default="anonymous", min_length=1)


class QAQueryResponse(BaseModel):
    answer: str
    mode: Literal["rag", "llm_only"]
    sources: list[str]
    latency_ms: int
    tokens_in: int
    tokens_out: int


class DBNLQueryRequest(BaseModel):
    question: str = Field(min_length=2)
    user_id: str = Field(default="anonymous", min_length=1)


class DBSQLPreviewResponse(BaseModel):
    question: str
    generated_sql: str
    parameters: list[str]


class DBNLQueryResponse(BaseModel):
    rows: list[dict]
    summary: str
    latency_ms: int
    generated_sql: str
    parameters: list[str]


class QueryHistoryItem(BaseModel):
    user_id: str
    question: str
    answer_summary: str
    mode: Literal["rag", "llm_only", "db_nl"]
    latency_ms: int
    tokens_in: int = 0
    tokens_out: int = 0
    device_type: str = "unknown"
    npu_enabled: bool = False
    created_at: datetime


class MetricsSummary(BaseModel):
    mode: str
    period: str
    device: str
    total_queries: int
    avg_latency_ms: float
    p95_latency_ms: float


class KnowledgeReviewRequest(BaseModel):
    source: str = Field(default="manual_v1.pdf#p1")
    original_text: str = Field(min_length=2)
    revised_text: str = Field(min_length=2)
    reviewer: str = Field(default="admin")
