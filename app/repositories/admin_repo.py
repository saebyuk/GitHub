from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class DocumentItem:
    document_id: int
    filename: str
    size: int
    uploaded_at: str


@dataclass
class ReviewItem:
    review_id: int
    source: str
    original_text: str
    revised_text: str
    reviewer: str
    created_at: str


class InMemoryAdminRepository:
    def __init__(self) -> None:
        self._docs: list[DocumentItem] = []
        self._reviews: list[ReviewItem] = []
        self._doc_seq = 1
        self._review_seq = 1

    def add_document(self, filename: str, size: int) -> dict:
        item = DocumentItem(
            document_id=self._doc_seq,
            filename=filename,
            size=size,
            uploaded_at=datetime.utcnow().isoformat(),
        )
        self._docs.insert(0, item)
        self._doc_seq += 1
        return asdict(item)

    def list_documents(self) -> list[dict]:
        return [asdict(d) for d in self._docs]

    def add_review(self, source: str, original_text: str, revised_text: str, reviewer: str) -> dict:
        item = ReviewItem(
            review_id=self._review_seq,
            source=source,
            original_text=original_text,
            revised_text=revised_text,
            reviewer=reviewer,
            created_at=datetime.utcnow().isoformat(),
        )
        self._reviews.insert(0, item)
        self._review_seq += 1
        return asdict(item)

    def list_reviews(self) -> list[dict]:
        return [asdict(r) for r in self._reviews]


admin_repo = InMemoryAdminRepository()
