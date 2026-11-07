from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session


class RepositoryError(Exception):
    pass


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def fetch_one(self, query: str, params: dict | None = None) -> dict:
        try:
            result = self.db.execute(text(query), params or {}).mappings().first()
            return dict(result) if result else {}
        except Exception as exc:
            raise RepositoryError(str(exc)) from exc

    def fetch_all(self, query: str, params: dict | None = None) -> list[dict]:
        try:
            rows = self.db.execute(text(query), params or {}).mappings().all()
            return [dict(r) for r in rows]
        except Exception as exc:
            raise RepositoryError(str(exc)) from exc
