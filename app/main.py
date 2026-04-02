from fastapi import FastAPI

from app.api import admin, db_query, history, metrics, qa, ui
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()
app = FastAPI(title=settings.app_name)

app.include_router(ui.router)
app.include_router(qa.router)
app.include_router(db_query.router)
app.include_router(admin.router)
app.include_router(history.router)
app.include_router(metrics.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}
