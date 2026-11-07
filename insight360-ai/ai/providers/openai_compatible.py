from __future__ import annotations

import httpx


class OpenAICompatibleProvider:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model

    def explain(self, question: str, answer: str, evidence: list[dict]) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an analytics explainer. Never invent values."},
                {"role": "user", "content": f"Question: {question}\nBase answer: {answer}\nEvidence: {evidence}"},
            ],
            "temperature": 0,
        }
        with httpx.Client(timeout=20) as client:
            r = client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Authorization": f"******"},
            )
            r.raise_for_status()
            data = r.json()
        return data["choices"][0]["message"]["content"]
