from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.post("/documents/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    return {
        "filename": file.filename,
        "size": len(content),
        "message": "업로드 완료 (PoC stub)",
    }


@router.post("/reindex")
def reindex() -> dict:
    return {"status": "started", "message": "재인덱싱 시작 (PoC stub)"}
