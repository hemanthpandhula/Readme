from __future__ import annotations

from dataclasses import dataclass

from ai.providers.deterministic import DeterministicProvider
from ai.query_engine.registry import approved_functions
from app.core.config import get_settings
from app.repositories.analytics_repository import AnalyticsRepository


@dataclass
class AIResult:
    intent: str
    answer: str
    evidence: list[dict]
    deterministic_fallback: bool


class AIService:
    def __init__(self, repo: AnalyticsRepository):
        self.repo = repo
        self.settings = get_settings()
        self.provider = DeterministicProvider()
        self.registry = approved_functions()

    def classify(self, question: str) -> str:
        q = question.lower()
        if "profit" in q and "decrease" in q:
            return "profit_drop_reason"
        if "top" in q and "customer" in q:
            return "top_customers"
        if "region" in q and "highest" in q:
            return "highest_revenue_region"
        if "forecast" in q or "next month" in q:
            return "forecast"
        if "unusual" in q or "anomal" in q:
            return "anomalies"
        return "summary"

    def handle(self, question: str) -> AIResult:
        intent = self.classify(question)
        if intent == "top_customers":
            evidence = self.repo.fetch_all(self.registry["top_customers"])
            answer = "Top customers are ranked by realized revenue in the latest warehouse snapshot."
        elif intent == "highest_revenue_region":
            evidence = self.repo.fetch_all(self.registry["highest_revenue_region"])
            answer = "The highest-revenue region is based on aggregated fact sales revenue."
        elif intent == "profit_drop_reason":
            evidence = self.repo.fetch_all(self.registry["profit_drop_reason"])
            answer = "Recent profit movement is tied to month-over-month revenue/profit deltas and should be reviewed with expense trends."
        elif intent == "anomalies":
            evidence = self.repo.fetch_all(self.registry["anomalies"])
            answer = "These are unusual transactions flagged by the anomaly pipeline and require investigation."
        elif intent == "forecast":
            evidence = self.repo.fetch_all(self.registry["forecast"])
            answer = "Forecast is generated from historical monthly revenue with baseline comparison."
        else:
            evidence = [self.repo.fetch_one(self.registry["summary"])]
            answer = "Overall KPI summary is based on warehouse aggregates."

        explained = self.provider.explain(question, answer, evidence)
        return AIResult(intent=intent, answer=explained, evidence=evidence, deterministic_fallback=True)
