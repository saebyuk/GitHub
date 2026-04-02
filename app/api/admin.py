from datetime import datetime

from fastapi import APIRouter, File, UploadFile

from app.models.schemas import KnowledgeReviewRequest
from app.repositories.admin_repo import admin_repo

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.post("/documents/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    saved = admin_repo.add_document(filename=file.filename or "unknown", size=len(content))
    return {"message": "업로드 완료", "document": saved}


@router.get("/documents")
def documents() -> list[dict]:
    return admin_repo.list_documents()


@router.post("/knowledge/review")
def review(payload: KnowledgeReviewRequest) -> dict:
    saved = admin_repo.add_review(
        source=payload.source,
        original_text=payload.original_text,
        revised_text=payload.revised_text,
        reviewer=payload.reviewer,
    )
    return {"message": "검수 반영 완료", "review": saved}


@router.get("/knowledge/reviews")
def reviews() -> list[dict]:
    return admin_repo.list_reviews()


@router.post("/reindex")
def reindex() -> dict:
    return {
        "status": "started",
        "message": "재인덱싱 시작",
        "requested_at": datetime.utcnow().isoformat(),
    }
