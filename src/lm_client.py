"""
LM Studio API client.
LM Studio exposes an OpenAI-compatible REST API at http://localhost:1234/v1
"""

import json
import requests
from typing import Optional


class LMStudioClient:
    """Client for LM Studio's local OpenAI-compatible API."""

    def __init__(self, base_url: str = "http://localhost:1234/v1", model: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._connect()

    def _connect(self):
        """Verify LM Studio is running and auto-detect the loaded model."""
        try:
            resp = requests.get(f"{self.base_url}/models", timeout=5)
            resp.raise_for_status()
            models = resp.json().get("data", [])
            if not models:
                raise RuntimeError(
                    "LM Studio is running but no model is loaded.\n"
                    "Load a model in LM Studio and start the local server first."
                )
            if not self.model:
                self.model = models[0]["id"]
            print(f"[+] Connected to LM Studio  |  model: {self.model}")
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Cannot connect to LM Studio at http://localhost:1234\n\n"
                "To fix this:\n"
                "  1. Open LM Studio\n"
                "  2. Load a model (e.g. Mistral 7B, Llama 3, Phi-3)\n"
                "  3. Go to the 'Local Server' tab and click 'Start Server'\n"
            )

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.15) -> str:
        """Send a chat completion request and return the response text."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": 2048,
            "stream": False,
        }
        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=180,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
