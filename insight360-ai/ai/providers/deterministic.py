from __future__ import annotations


class DeterministicProvider:
    def explain(self, question: str, answer: str, evidence: list[dict]) -> str:
        return (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Evidence rows are attached from approved analytics functions."
        )
