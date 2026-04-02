from collections import deque
from datetime import datetime

from app.models.schemas import QueryHistoryItem


class InMemoryHistoryRepository:
    def __init__(self, max_items: int = 500) -> None:
        self._items: deque[QueryHistoryItem] = deque(maxlen=max_items)

    def add(self, item: QueryHistoryItem) -> None:
        self._items.appendleft(item)

    def recent(self, user_id: str, limit: int = 20) -> list[QueryHistoryItem]:
        return [item for item in self._items if item.user_id == user_id][:limit]


history_repo = InMemoryHistoryRepository()
