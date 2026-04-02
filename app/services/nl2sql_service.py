import re
from datetime import datetime, timedelta

ALLOWED_TABLE = "pki_operation_history"
ALLOWED_COLUMNS = {
    "event_time",
    "system_name",
    "module_name",
    "severity",
    "error_code",
    "message",
    "operator_id",
    "host_name",
    "action_result",
}


def to_safe_select(question: str) -> tuple[str, tuple]:
    lowered = question.lower()
    days = 7
    match = re.search(r"(\d+)\s*일", question)
    if match:
        days = int(match.group(1))

    keyword = None
    for candidate in ["crl", "ocsp", "인증서", "서명", "timeout", "권한"]:
        if candidate in lowered or candidate in question:
            keyword = candidate
            break

    start_time = datetime.now() - timedelta(days=days)
    sql = (
        f"SELECT event_time, error_code, message FROM {ALLOWED_TABLE} "
        "WHERE event_time >= ?"
    )
    params: list = [start_time.strftime("%Y-%m-%d %H:%M:%S")]

    if keyword:
        sql += " AND LOWER(message) LIKE ?"
        params.append(f"%{keyword.lower()}%")

    sql += " ORDER BY event_time DESC LIMIT 100"
    return sql, tuple(params)
