"""LLM client with a JSON mode.

Two judgement calls in the whole pipeline need a model: resolving a messy
ledger string to a real company, and turning research into a posture plus a
call script. Everything else is arithmetic and rules.

Set ANTHROPIC_API_KEY (or OPENAI_API_KEY with LLM_PROVIDER=openai) to go live.
Without a key, `json_call` returns the caller's `fallback`, so the pipeline
still completes.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any

import httpx

from . import config


# Last failure seen by any client, surfaced in /api/status. Without this a
# wrong model name is indistinguishable from a working stub.
last_error: str = ""

# A rate limit means "not now", not "no". Worth waiting out.
RATE_LIMIT_RETRIES = 3

# Both model calls are classification, not writing, and the desk compares one
# run against the next. Sampling variation would show up in that comparison as
# business change, which is the one thing the history layer must not invent.
TEMPERATURE = 0.0


class LLMClient:
    def __init__(self, provider: str | None = None):
        self.provider = (provider or config.LLM_PROVIDER).lower()
        # Whether the most recent json_call on THIS client got a real answer.
        # Callers that care about the difference between a model result and a
        # fallback read this; without it a rate-limited run looks identical to
        # a healthy one.
        self.last_call_ok = True

    @property
    def api_key(self) -> str:
        return {"anthropic": config.ANTHROPIC_API_KEY,
                "openai": config.OPENAI_API_KEY,
                "groq": config.GROQ_API_KEY}.get(self.provider, "")

    @property
    def model(self) -> str:
        return {"anthropic": config.ANTHROPIC_MODEL,
                "openai": config.OPENAI_MODEL,
                "groq": config.GROQ_MODEL}.get(self.provider, "")

    @property
    def base_url(self) -> str:
        """Groq speaks the OpenAI chat-completions dialect, so it reuses that
        path with a different host."""
        return (config.GROQ_BASE_URL if self.provider == "groq"
                else "https://api.openai.com/v1")

    @property
    def live(self) -> bool:
        return self.provider != "off" and bool(self.api_key)

    # -- raw ----------------------------------------------------------------
    def complete(self, system: str, user: str, max_tokens: int = 1500) -> str:
        if not self.live:
            return ""
        if self.provider == "anthropic":
            return self._anthropic(system, user, max_tokens)
        return self._openai_compatible(system, user, max_tokens)

    def _anthropic(self, system: str, user: str, max_tokens: int) -> str:
        with httpx.Client(timeout=90.0) as client:
            resp = client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": self.api_key,
                         "anthropic-version": "2023-06-01",
                         "content-type": "application/json"},
                json={"model": self.model, "max_tokens": max_tokens,
                      "temperature": TEMPERATURE, "system": system,
                      "messages": [{"role": "user", "content": user}]},
            )
            resp.raise_for_status()
            blocks = resp.json().get("content", [])
            return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")

    def _openai_compatible(self, system: str, user: str, max_tokens: int) -> str:
        with httpx.Client(timeout=90.0) as client:
            resp = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}",
                         "content-type": "application/json"},
                json={"model": self.model, "max_tokens": max_tokens,
                      "temperature": TEMPERATURE,
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user", "content": user}]},
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    # -- json ---------------------------------------------------------------
    def json_call(self, system: str, user: str, fallback: Any,
                  max_tokens: int = 1500) -> Any:
        """Ask for JSON. Returns `fallback` when no key is set or on any error,
        so a missing key degrades the output rather than breaking the run."""
        if not self.live:
            self.last_call_ok = False
            return fallback
        global last_error
        prompt = system + "\n\nReply with JSON only. No prose, no code fence."

        # Rate limits are the common failure on a shared free tier, and they
        # are the one failure worth waiting out: the request was fine, there
        # was just no headroom.
        for attempt in range(RATE_LIMIT_RETRIES + 1):
            try:
                text = self.complete(prompt, user, max_tokens)
                last_error = ""
                self.last_call_ok = True
                return _parse_json(text, fallback)
            except Exception as exc:  # noqa: BLE001
                detail = str(exc)[:200]
                resp = getattr(exc, "response", None)
                status = getattr(resp, "status_code", None)
                if resp is not None:
                    detail = f"{status}: {resp.text[:200]}"
                last_error = f"{self.provider}/{self.model} - {detail}"
                if status in (429, 503) and attempt < RATE_LIMIT_RETRIES:
                    time.sleep(_retry_after(resp, attempt))
                    continue
                self.last_call_ok = False
                return fallback
        self.last_call_ok = False
        return fallback


def _retry_after(resp: Any, attempt: int) -> float:
    """Honour the provider's own advice when it gives any, otherwise back off."""
    header = ""
    try:
        header = (resp.headers or {}).get("retry-after", "")
    except Exception:  # noqa: BLE001
        pass
    try:
        return min(30.0, max(1.0, float(header)))
    except (TypeError, ValueError):
        return min(20.0, 2.0 * (2 ** attempt))


def _parse_json(text: str, fallback: Any) -> Any:
    if not text:
        return fallback
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.+?)\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Last resort: grab the outermost object or array.
    for opener, closer in (("{", "}"), ("[", "]")):
        start, end = text.find(opener), text.rfind(closer)
        if 0 <= start < end:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    return fallback
