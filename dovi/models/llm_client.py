from __future__ import annotations

import importlib.util
import json
import os
from typing import Any

from dovi.datamodel.pipeline_options import ModelOptions, ModelProvider
from dovi.exceptions import BackendNotAvailableError

_DEFAULT_BASE_URLS: dict[ModelProvider, str] = {
    ModelProvider.OPENAI: "https://api.openai.com/v1",
    ModelProvider.ANTHROPIC: "https://api.anthropic.com/v1",
    ModelProvider.OLLAMA: "http://localhost:11434/v1",
    ModelProvider.VLLM: "http://localhost:8000/v1",
}

_API_KEY_ENV: dict[ModelProvider, str] = {
    ModelProvider.OPENAI: "OPENAI_API_KEY",
    ModelProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
}


class LLMClient:
    """Thin chat-completion client shared by the generation and replication models."""

    def __init__(self, options: ModelOptions) -> None:
        self.options = options
        self.base_url = (options.base_url or _DEFAULT_BASE_URLS[options.provider]).rstrip("/")

    def _api_key(self) -> str | None:
        if self.options.api_key is not None:
            return self.options.api_key.get_secret_value()
        env = _API_KEY_ENV.get(self.options.provider)
        return os.environ.get(env) if env else None

    def complete_json(self, system: str, user: str) -> dict[str, Any]:
        """Run a single-turn completion and parse the response as a JSON object."""
        if importlib.util.find_spec("httpx") is None:
            raise BackendNotAvailableError("llm", extra="llm")
        import httpx

        if self.options.provider is ModelProvider.ANTHROPIC:
            raise NotImplementedError(
                "The Anthropic provider is not supported yet; use an OpenAI-compatible endpoint."
            )

        headers = {"Content-Type": "application/json"}
        if key := self._api_key():
            headers["Authorization"] = f"Bearer {key}"

        payload = {
            "model": self.options.model_id,
            "temperature": self.options.temperature,
            "max_tokens": self.options.max_tokens,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.options.timeout,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)  # type: ignore[no-any-return]
