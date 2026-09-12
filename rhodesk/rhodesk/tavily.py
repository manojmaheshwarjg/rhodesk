"""Tavily client: search and extract.

Set TAVILY_API_KEY to go live. Without it every call returns a deterministic
stub so the pipeline still completes end to end.

VERIFY BEFORE THE DEMO: the request shapes below follow Tavily's documented
REST API, but they were written without a key to test against. Check
docs.tavily.com and adjust `_payload` if anything has moved.
"""
from __future__ import annotations

import hashlib
from typing import Any

import httpx

from . import config


# Last failure seen by any client, surfaced in /api/status. A key that has
# run out of credits answers 432 and otherwise looks exactly like a working
# one, which is the same trap a wrong model name set earlier.
last_error: str = ""


class TavilyClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else config.TAVILY_API_KEY
        self.base_url = config.TAVILY_BASE_URL.rstrip("/")

    @property
    def live(self) -> bool:
        return bool(self.api_key)

    def _post(self, path: str, payload: dict) -> dict:
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {self.api_key}"}
        with httpx.Client(timeout=45.0) as client:
            resp = client.post(f"{self.base_url}{path}", json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()

    # -- search -------------------------------------------------------------
    def search(self, query: str, *, topic: str = "general", depth: str = "advanced",
               max_results: int = 5, days: int | None = None) -> list[dict]:
        """Returns [{title, url, content, score, published_date}]."""
        if not self.live:
            return _stub_search(query, max_results)
        payload: dict[str, Any] = {
            "query": query,
            "search_depth": depth,
            "topic": topic,
            "max_results": max_results,
        }
        if days:
            payload["days"] = days
        global last_error
        try:
            data = self._post("/search", payload)
            last_error = ""
        except Exception as exc:  # noqa: BLE001 - never break the pipeline
            last_error = _describe(exc)
            return [{"title": "Tavily search failed", "url": "",
                     "content": str(exc)[:300], "score": 0, "published_date": None,
                     "error": True}]
        return data.get("results", [])

    # -- extract ------------------------------------------------------------
    def extract(self, urls: list[str]) -> list[dict]:
        """Returns [{url, raw_content}] for pages worth reading in full,
        such as a vendor's pricing page."""
        if not urls:
            return []
        if not self.live:
            return [{"url": u, "raw_content": _stub_extract(u)} for u in urls]
        global last_error
        try:
            data = self._post("/extract", {"urls": urls})
        except Exception as exc:  # noqa: BLE001
            last_error = _describe(exc)
            return [{"url": u, "raw_content": "", "error": str(exc)[:200]} for u in urls]
        return data.get("results", [])


def _describe(exc: Exception) -> str:
    resp = getattr(exc, "response", None)
    status = getattr(resp, "status_code", None)
    if status == 432:
        return "432: Tavily credits exhausted for this key"
    if resp is not None:
        return f"{status}: {resp.text[:160]}"
    return str(exc)[:160]


# --- stubs -----------------------------------------------------------------
# Deterministic so the demo looks the same every time it is run.

_STUB_SIGNALS = {
    # Northwind Traders is the sandbox's most overdue customer (88 days), so
    # giving it a distress story lets the Cover posture appear without keys.
    "northwind traders": [
        ("Northwind Traders raises down round at reduced valuation",
         "https://example.com/northwind-down-round",
         "Northwind Traders has closed a funding round at roughly half its "
         "prior valuation. Two existing investors did not participate, and the "
         "company has paused hiring."),
        ("Northwind Traders cuts open roles",
         "https://example.com/northwind-hiring",
         "Open positions fell from 11 to 2 over the last quarter."),
    ],
    "brightleaf design": [
        ("Brightleaf Design named in supplier dispute",
         "https://example.com/brightleaf-dispute",
         "A supplier filed a payment dispute against Brightleaf Design. "
         "No judgment has been entered."),
    ],
    "summit analytics": [
        ("Summit Analytics raises Series B extension at reduced valuation",
         "https://example.com/summit-analytics-extension",
         "Summit Analytics has closed a Series B extension at roughly half its prior "
         "valuation. Two existing investors did not participate in the round."),
        ("Summit Analytics careers page shows hiring slowdown",
         "https://example.com/summit-careers",
         "Open roles fell from 14 in July to 2 today, both in sales."),
    ],
    "orbit media group": [
        ("Orbit Media Group closes Series B",
         "https://example.com/orbit-series-b",
         "Orbit Media Group announced a Series B led by an existing investor. "
         "The company says it will expand its measurement product."),
    ],
    "atlassian": [
        ("Atlassian standard plan pricing",
         "https://www.atlassian.com/software/jira/pricing",
         "Standard is listed at $36.50 per user per month, reduced from $47.00."),
    ],
    "asana": [
        ("Asana pricing",
         "https://asana.com/pricing",
         "Starter and Advanced tiers listed. Advanced is billed per seat per month."),
    ],
}


def _stub_search(query: str, max_results: int) -> list[dict]:
    low = query.lower()
    for key, hits in _STUB_SIGNALS.items():
        if key in low:
            return [{"title": t, "url": u, "content": c, "score": 0.9,
                     "published_date": None, "stub": True}
                    for t, u, c in hits][:max_results]
    digest = hashlib.sha1(query.encode()).hexdigest()[:8]
    return [{
        "title": f"No notable public news found",
        "url": f"https://example.com/no-results/{digest}",
        "content": "Stubbed Tavily result. Set TAVILY_API_KEY for live search.",
        "score": 0.1, "published_date": None, "stub": True,
    }]


def _stub_extract(url: str) -> str:
    if "atlassian" in url:
        return ("Jira Standard $36.50 per user per month. Premium $71.00 per user "
                "per month. Prices updated this quarter.")
    return "Stubbed page extract. Set TAVILY_API_KEY for live extraction."
