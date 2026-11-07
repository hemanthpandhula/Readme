from app.services.ai_service import AIService


class StubRepo:
    def fetch_all(self, query: str):
        return [{"ok": True}]

    def fetch_one(self, query: str):
        return {"ok": True}


def test_ai_intent_classification():
    svc = AIService(StubRepo())
    assert svc.classify("show top ten customers") == "top_customers"
    assert svc.classify("forecast next month") == "forecast"


def test_ai_response_contains_evidence():
    svc = AIService(StubRepo())
    out = svc.handle("Which region has the highest revenue?")
    assert out.evidence
    assert out.deterministic_fallback is True
