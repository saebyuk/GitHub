from statistics import mean

from app.repositories.history_repo import history_repo


def summarize(mode: str, period: str, device: str) -> dict:
    all_items = [item for item in history_repo._items if mode in ("all", item.mode)]
    latencies = [item.latency_ms for item in all_items] or [0]
    sorted_lat = sorted(latencies)
    p95_idx = int(len(sorted_lat) * 0.95) - 1
    p95_idx = max(p95_idx, 0)

    return {
        "mode": mode,
        "period": period,
        "device": device,
        "total_queries": len(all_items),
        "avg_latency_ms": float(mean(latencies)),
        "p95_latency_ms": float(sorted_lat[p95_idx]),
    }
