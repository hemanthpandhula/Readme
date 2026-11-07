from datetime import datetime, date
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime


class DashboardSummaryResponse(BaseModel):
    total_revenue: float
    total_cost: float
    total_profit: float
    total_expenses: float
    profit_margin_pct: float
    transaction_count: int


class MonthlyTrendPoint(BaseModel):
    year: int
    month: int
    period_start: date
    revenue: float
    profit: float
    quantity: int


class DataQualityResponse(BaseModel):
    execution_id: int | None = None
    status: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    total_records: int | None = None
    valid_records: int | None = None
    rejected_records: int | None = None
    quality_score: float | None = None
    notes: str | None = None


class AIChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class AIChatResponse(BaseModel):
    intent: str
    answer: str
    evidence: list[dict]
    deterministic_fallback: bool


class RunResponse(BaseModel):
    status: str
    detail: str
