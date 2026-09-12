"""Rho API client.

This one is real and works today: the sandbox at rhoapi-sandbox.rho.co needs
no account and accepts any non-empty bearer token.

Things learned by probing the live API that this client accounts for:
  - Every endpoint is GET. There are no writes in v1 at all.
  - The `Bearer` scheme is matched case-sensitively, so send it exactly.
  - Unknown query parameters are silently ignored rather than rejected.
  - An EMPTY date filter value (`initiated_before=`) returns 200 with zero
    rows, so never send a filter key with an empty value.
  - `page_size` is bounded [1, 100].
  - Transaction `id` is NOT unique per row: legs of one money movement share
    it. Key on (id, account_id) or group on money_movement_id.
"""
from __future__ import annotations

import time
from typing import Any, Iterator

import httpx

from . import config

LIST_KEYS = {
    "/accounts": "accounts",
    "/cards": "cards",
    "/transactions": "transactions",
    "/statements": "statements",
    "/invoicing/customers": "customers",
    "/invoicing/invoices": "invoices",
}


class RhoError(RuntimeError):
    pass


class RhoClient:
    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or config.RHO_BASE_URL).rstrip("/")
        self.token = token or config.RHO_TOKEN
        self._client = httpx.Client(
            timeout=30.0,
            headers={"Authorization": f"Bearer {self.token}",
                     "Accept": "application/json"},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()

    def _get(self, path: str, params: dict | None = None) -> dict:
        # Drop empty values: an empty *_before returns 200 with zero rows.
        clean = {k: v for k, v in (params or {}).items() if v not in (None, "")}
        url = f"{self.base_url}{path}"
        for attempt in range(4):
            resp = self._client.get(url, params=clean)
            if resp.status_code == 429:
                wait = resp.headers.get("Retry-After")
                delay = int(wait) if (wait or "").isdigit() and int(wait) > 0 else 2 ** attempt
                time.sleep(min(delay, 30))
                continue
            if resp.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            if resp.status_code >= 400:
                raise RhoError(f"{resp.status_code} on {path}: {resp.text[:300]}")
            return resp.json()
        raise RhoError(f"gave up on {path} after retries")

    def paginate(self, path: str, params: dict | None = None,
                 page_size: int = 100) -> Iterator[dict]:
        key = LIST_KEYS[path]
        token = None
        while True:
            page = self._get(path, {**(params or {}), "page_size": page_size,
                                    "page_token": token})
            yield from page.get(key, [])
            token = (page.get("page") or {}).get("next_page_token")
            if not token:
                return

    def all(self, path: str, params: dict | None = None) -> list[dict]:
        return list(self.paginate(path, params))

    # Convenience readers ---------------------------------------------------
    def accounts(self) -> list[dict]:
        return self.all("/accounts")

    def cards(self) -> list[dict]:
        return self.all("/cards")

    def transactions(self) -> list[dict]:
        return self.all("/transactions")

    def customers(self) -> list[dict]:
        return self.all("/invoicing/customers")

    def invoices(self) -> list[dict]:
        return self.all("/invoicing/invoices")

    def ping(self) -> dict[str, Any]:
        accounts = self.accounts()
        return {"ok": True, "accounts": len(accounts),
                "base_url": self.base_url,
                "total_balance_cents": sum(
                    (a.get("balance") or {}).get("amount", 0) for a in accounts)}


def client(**kwargs):
    """Return whichever ledger source is configured. Everything else in the
    app calls this rather than RhoClient directly, so flipping RHO_MODE needs
    no other change."""
    if config.RHO_MODE == "fixtures":
        from datetime import date, timedelta

        from .fixtures import FixtureClient
        days = config.FIXTURE_DAYS_AGO
        return FixtureClient(as_of=date.today() - timedelta(days=days) if days else None)
    return RhoClient(**kwargs)
