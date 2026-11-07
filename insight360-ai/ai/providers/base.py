from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    def explain(self, question: str, answer: str, evidence: list[dict]) -> str: ...
