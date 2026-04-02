from __future__ import annotations

from typing import Any

import mariadb

from app.core.config import settings


class MariaDBRepository:
    def __init__(self) -> None:
        self._enabled = settings.enable_mariadb

    def query(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        if not self._enabled:
            return [
                {
                    "event_time": "2026-04-01 09:12:00",
                    "error_code": "PKI-CRL-001",
                    "message": "[MOCK] CRL fetch timeout",
                }
            ]

        conn = mariadb.connect(
            host=settings.mariadb_host,
            port=settings.mariadb_port,
            user=settings.mariadb_user,
            password=settings.mariadb_password,
            database=settings.mariadb_database,
        )
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, params)
            rows = cur.fetchall()
            return rows
        finally:
            conn.close()


mariadb_repo = MariaDBRepository()
