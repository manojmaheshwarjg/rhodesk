## 6. Cross-cutting mechanics

Four mechanisms apply to every call you will ever make against Rho v1: how lists are paged, how the service throttles you, how it reports failure, and what it promises not to change. None of them is endpoint-specific, all of them are load-bearing, and each of them diverges from the published documentation in at least one way that will cost you a production incident if you take the docs at face value.

Everything marked **observed** in this section was captured against the sandbox host `https://rhoapi-sandbox.rho.co/api/v1` with the bearer token `sandbox` on 2026-09-11 and 2026-09-12 UTC. The sandbox accepts any non-empty bearer token (see the Authentication section), so every probe below is reproducible by anyone. Production was not probed beyond unauthenticated metadata. Where a behavior is documented but was not reachable in the sandbox, it is labelled as unverified rather than confirmed.

---

### 6.1 Pagination

Every list endpoint (`/accounts`, `/cards`, `/transactions`, `/statements`, `/invoicing/customers`, `/invoicing/invoices`) uses the same two query parameters and the same response wrapper. The detail endpoints take neither.

#### 6.1.1 The wrapper

Official docs (`/docs/v1/pagination`) describe a response with the resource array at the top level plus a `page` object. That is exactly what the service returns, and nothing more.

```bash
curl -s "https://rhoapi-sandbox.rho.co/api/v1/transactions?page_size=2" \
  -H "Authorization: Bearer sandbox"
```

```json
{
  "page": { "next_page_token": "eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qSXcifQ" },
  "transactions": [ { "id": "…" }, { "id": "…" } ]
}
```

| Property | Value (observed) |
| --- | --- |
| Top-level keys | The resource array plus `page`, nothing else |
| Resource key | Matches the resource: `accounts`, `cards`, `transactions`, `statements`, `customers`, `invoices` |
| `page` fields | Exactly one: `next_page_token` |
| Absent | `total`, `total_count`, `count`, `has_more`, `has_next`, `prev_page_token`, `offset`, `limit` |
| Last-page signal | `"next_page_token": null`. The key is always present, never omitted, never an empty string |
| Response headers | No `Link`, no `X-Total-Count`, no pagination headers of any kind |

Note the two invoicing resource keys: `/invoicing/customers` returns `customers`, not `invoicing_customers`, and `/invoicing/invoices` returns `invoices`. A generic client that derives the key from the last path segment works; one that derives it from the full path does not.

> **Divergence:** every operation reference page types the field as `page.next_page_token (string, required)` while the prose on the same page says "null on the last page". Observed, the field is `null` on the last page of all six endpoints. A strictly generated client with a non-nullable `string` will fail to deserialize the terminal response of every walk. Type it `string | null`.

#### 6.1.2 `page_size`: default, bounds, and coercion

The pagination guide says "Each endpoint defines its own minimum, maximum, and default". The operation reference pages publish two different halves of that and never all three:

| Endpoint | Reference wording | Documented max | Documented default | Documented min |
| --- | --- | --- | --- | --- |
| `GET /accounts` | "Number of accounts per page; max 100" | 100 | not stated | not stated |
| `GET /transactions` | "Number of transactions per page; max 100" | 100 | not stated | not stated |
| `GET /statements` | "Number of statements per page; max 100" | 100 | not stated | not stated |
| `GET /cards` | "Number of cards to return. Defaults to 20." | not stated | 20 | not stated |
| `GET /invoicing/customers` | "Number of customers per page. Defaults to 20." | not stated | 20 | not stated |
| `GET /invoicing/invoices` | "Number of invoices per page. Defaults to 20." | not stated | 20 | not stated |

Observed, the behavior is uniform across all six endpoints. The bound is inclusive `[1, 100]` everywhere, and the default is 20.

```bash
# default page size, proven on the two endpoints whose corpus exceeds 20 rows
curl -s "https://rhoapi-sandbox.rho.co/api/v1/transactions" -H "Authorization: Bearer sandbox" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["transactions"]))'
# -> 20   (sandbox holds 72 transactions; /statements holds 33 and also returns 20)
```

| `page_size` | HTTP | Result (observed, identical on all six endpoints) |
| --- | --- | --- |
| omitted | 200 | 20 items |
| `0`, `-1`, `-0` | 400 | `type` `1317`, "page_size must be between 1 and 100" |
| `1` | 200 | 1 item, the minimum |
| `100` | 200 | the maximum |
| `101`, `150`, `1000`, `10000`, `99999999999999999999` | 400 | `type` `1317`, same title |
| `%2B3` (a leading `+`) | 200 | parsed as 3 |
| `03` | 200 | parsed as 3 |
| `2.0`, `2.5`, `1e2`, `0x10`, `abc`, `true`, `null` | 400 | `type` `about:blank`, `detail` "invalid parameter: page_size" |
| `` (empty value) | 400 | `type` `about:blank` |
| `page_size=5&page_size=7` (repeated) | 400 | `type` `about:blank`. It does not take first or last |
| `page_size[]=5` | 200 | the bracketed key is unrecognized and silently ignored; falls back to 20 |
| `PAGE_SIZE=5`, `pageSize=5` | 200 | parameter names are case-sensitive; ignored; falls back to 20 |

> **Divergence:** `/cards`, `/invoicing/customers` and `/invoicing/invoices` publish no maximum, but observed all three enforce the same 1..100 bound and say so in the error. Conversely `/accounts`, `/transactions` and `/statements` publish no default, but observed all use 20. No endpoint documents a minimum even though the guide says each one defines it. Treat `[1, 100]` and default 20 as the real contract on all six.

> **Divergence:** the docs say only that "values outside the allowed range return `400 Bad Request`". There are actually two distinct 400 bodies with different `type` values and different fields, split on whether the value parses as an integer at all. `?page_size=101` gives `{"type":"1317","title":"page_size must be between 1 and 100","status":400}`; `?page_size=abc` gives `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}`. See 6.3.

#### 6.1.3 What the token decodes to

The docs call the cursor opaque and warn that "their format and lifetime are not part of the API contract and may change without notice". Take the warning seriously as an engineering rule and read the rest of this subsection as diagnostics, not as an interface.

Observed, the token is base64url without padding and decodes to a three-field JSON envelope:

```bash
python3 - <<'PY'
import base64, json, urllib.request
req = urllib.request.Request(
    "https://rhoapi-sandbox.rho.co/api/v1/transactions?page_size=36",
    headers={"Authorization": "Bearer sandbox"})
tok = json.load(urllib.request.urlopen(req))["page"]["next_page_token"]

def b64(s: str) -> bytes:
    s = s.replace("-", "+").replace("_", "/")
    return base64.b64decode(s + "=" * (-len(s) % 4))

env = json.loads(b64(tok))
print(env)                 # {'v': 1, 'f': 't0HwRhJ0BSGWYAjAT5bQKg', 't': 'b2Zmc2V0OjM2'}
print(b64(env["t"]))       # b'offset:36'
PY
```

| Field | Meaning (inferred from observed behavior) |
| --- | --- |
| `v` | Envelope version, always `1`. A token rewritten with `"v":2` returns 400. |
| `f` | Query fingerprint. 22 base64url characters, so 16 raw bytes, consistent with a 128-bit digest. It binds the token to the endpoint plus the canonicalized filter and sort set. It is deterministic and stable across process and connection boundaries, and it does not include `page_size`. |
| `t` | The cursor itself, separately base64-encoded. Its decoded form differs by endpoint (6.1.4). |

The decoder is lenient about the base64 alphabet and padding (standard alphabet with `=` padding is accepted) and strict about the envelope: `v` must be 1, `f` must match the fingerprint the server recomputes for the current request, and `t` must itself be base64 of a well-formed cursor. Unknown extra keys in the envelope are ignored and the token still works.

#### 6.1.4 Two implementations behind one envelope

This is the single most important fact in this subsection. The same wrapper hides two different pagination algorithms.

| Endpoint | Decoded `t` | Style |
| --- | --- | --- |
| `/accounts` | `{"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}` | keyset |
| `/cards` | `offset:N` | absolute offset |
| `/transactions` | `offset:N` | absolute offset |
| `/statements` | `offset:N` | absolute offset |
| `/invoicing/customers` | `offset:N` | absolute offset |
| `/invoicing/invoices` | `offset:N` | absolute offset |

Observed on `/accounts`:

```bash
curl -s "https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=3" \
  -H "Authorization: Bearer sandbox" \
  | python3 -c 'import sys,json,base64
d=json.load(sys.stdin)
b=lambda s:base64.b64decode(s.replace("-","+").replace("_","/")+"="*(-len(s)%4))
env=json.loads(b(d["page"]["next_page_token"])); print(b(env["t"]).decode())'
# -> {"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}
```

`N` in the offset form is the absolute count of rows already consumed: request `page_size=1` and the token carries `offset:1`, request `page_size=50` and it carries `offset:50`, with the same `f` in both cases.

#### 6.1.5 What invalidates a cursor and what does not

The gate is purely the fingerprint `f`. The server recomputes it from the current request's endpoint, filters and sort, and compares. A mismatch is `400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`.

| Change between page N and page N+1 | Cursor still valid? (observed) |
| --- | --- |
| Change `page_size` (5 then 3, 1 then 100) | **Yes.** `page_size` is not in the fingerprint |
| Add an unknown parameter (`&zzz=1`) | Yes, unknown parameters are ignored and not fingerprinted |
| Add the explicit default (`sort_by=initiated_at&order=desc` on `/transactions`) | Yes, defaults are canonicalized before hashing |
| `initiated_after=2026-01-01` then `initiated_after=2026-01-01T00:00:00Z` | Yes, dates are normalized before hashing |
| Add `include_deleted=false` on `/invoicing/customers` | Yes, canonicalized to the default |
| `order=asc` then `order=ASC` | **No, 400.** Identical rows, incompatible cursors |
| `status=settled` then `status=settled&status=settled` | **No, 400.** Identical rows, incompatible cursors |
| Add, drop or change any filter | No, 400 (as documented) |
| Change `sort_by` or `order` to a different value | No, 400 (as documented) |
| Token from a different endpoint | No, 400 |
| `page_token=` (empty string) | Treated as absent: returns page 1, HTTP 200 |
| `page_token` repeated | 400 `about:blank`, "invalid parameter: page_token" |

Changing `page_size` mid-walk is not merely tolerated, it is correct. Observed: take the `offset:5` token minted by `page_size=5`, continue it with `page_size=3`, and you get exactly reference positions 6, 7 and 8 with no gap and no overlap.

```bash
B=https://rhoapi-sandbox.rho.co/api/v1; H="Authorization: Bearer sandbox"
T=$(curl -s "$B/transactions?page_size=5" -H "$H" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["page"]["next_page_token"])')
curl -s "$B/transactions?page_size=3&page_token=$T" -H "$H" \
  | python3 -c 'import sys,json;print([t["id"][-6:] for t in json.load(sys.stdin)["transactions"]])'
# -> ['000005', '00000f', '00000c']   == positions 6,7,8 of the page_size=100 reference order
```

> **Divergence:** the docs list what invalidates a cursor ("same endpoint with the same filters and sort order") but never state the useful converse, that `page_size` may change freely between pages. That is a real capability: you can start a walk with a small page for latency and escalate to 100 once you know the result set is large. Conversely the docs give no warning that the binding is to the *raw spelling* of a filter rather than its meaning. `order=ASC` and `order=asc` return byte-identical rows, and their cursors are mutually invalid.

The practical rule that follows: build the query string once per walk, store it, and replay it byte for byte on every page, varying only `page_token` (and, if you want, `page_size`).

#### 6.1.6 The stability caveat

The pagination guide makes an unqualified promise:

> "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated."

> **Divergence:** this holds structurally only for `/accounts`. Five of six list endpoints use an absolute offset cursor, and an absolute offset cannot deliver that guarantee. If a row is inserted at a position before your current offset while you walk, every later row shifts by one and you skip a record. If a row is deleted before your offset, a record repeats. The sandbox dataset is static, so a live shift cannot be forced there, but the mechanism is dispositive: `offset:N` carries no anchor to any row, so there is nothing for the server to be stable against. `/accounts` is the exception; its `last_id` keyset cursor does provide the promised behavior, and observed it additionally validates that the anchor row still exists (a fabricated `last_id` with a correct fingerprint returns 400).

The engineering consequence is not subtle, because the ordering makes it worse. `/transactions` defaults to `initiated_at` descending, newest first. New transactions arrive at the head of that ordering, which is exactly where an insert does maximum damage to an offset walk: one new transaction between page 1 and page 2 pushes the last row of page 1 into page 2, and you process it twice.

Three mitigations, in order of preference:

1. **De-duplicate on `id` in the client.** Cheap, always correct for duplicates, and the only defense that needs no cooperation from the server. Both loops in 6.1.9 and 6.1.10 do this.
2. **Pin the window with a filter.** For `/transactions`, adding `initiated_before=<the moment you started>` makes the result set closed against new arrivals, because anything inserted after you started falls outside the filter. Note from the Filtering and sorting section that `*_before` is exclusive on `/transactions` and `/statements` but inclusive on `/invoicing/invoices`, and that an empty value on any `*_before` parameter silently returns zero rows.
3. **Accept the skip risk, and re-walk.** If a walk that must be complete cannot be window-pinned, run it twice and union on `id`, or run it against a quiet period.

Skips cannot be detected client-side at all. That asymmetry, duplicates are cheap to fix and skips are invisible, is why a window filter matters for any reconciliation job.

#### 6.1.7 Termination and the last page

Termination is by `null` cursor and nothing else. There is no `has_more`, no count, and no way to know in advance how many pages remain.

Observed, when the row count is an exact multiple of `page_size` there is **no** trailing empty page. The last full page carries the `null` token itself:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1; H="Authorization: Bearer sandbox"   # 72 transactions total
T=$(curl -s "$B/transactions?page_size=36" -H "$H" \
    | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["page"]["next_page_token"])')
curl -s "$B/transactions?page_size=36&page_token=$T" -H "$H" \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print(len(d["transactions"]), d["page"]["next_page_token"])'
# -> 36 None
```

Page 1 returns 36 rows plus an `offset:36` token; page 2 returns the remaining 36 rows and `null`. Likewise `/invoicing/customers?page_size=7` against a 7-row corpus returns 7 rows and a `null` token on the very first call. An empty page is reachable only by hand-crafting a cursor whose offset equals the total, which the API itself never mints.

Your loop must therefore handle three cases: a full page with a token, a short page with a token (`page_size=100` against 72 rows returns 72 rows and `null`, so a short page normally means the end, but never rely on that), and a page whose token is `null`. Never treat "fewer items than `page_size`" as the terminator. Only `next_page_token === null` terminates.

#### 6.1.8 Cursor lifetime, forging, and what that implies

| Property | Observed |
| --- | --- |
| Lifetime | No expiry observed. Tokens minted at 2026-09-11T19:22Z still resolved at 2026-09-12T00:03Z, about 4h41m later. No TTL is documented and no expiry error exists |
| Signature | None. The envelope is unsigned and unencrypted. `f` is a fingerprint of the query, not an HMAC over the cursor payload |
| Forgeable | Yes. Keeping a legitimate `f` and rewriting the inner offset to any value in `[0, total]` is honored. `offset:70` on the 72-row transactions corpus returns the last 2 rows; `offset:72` returns an empty array with a `null` token; `offset:73` returns 400 |
| Validation | Offset must be a non-negative integer no greater than the total. The `/accounts` keyset additionally requires the anchor row to exist and the inner `sort_by`/`order` to match the request |

Two things follow. First, an undocumented binary search on the `offset:N` 400 boundary will tell you a total result count in a handful of calls. It works, and you should not ship it: it depends on the exact cursor format that the docs explicitly reserve the right to change without notice, and it will break silently the day Rho migrates the remaining five endpoints to keyset cursors. Second, because the cursor is not authenticated, do not treat it as a capability. It is scoped to a query, not to a tenant, and it tells an attacker who already holds it nothing more than the query it came from, but it is also not something to log to a third party or embed in a URL you share.

The docs' own advice, "cursors are designed for live iteration, not for bookmarks", is the right rule even though no expiry was observed. Persist a timestamp filter as your resume point, never a cursor.

#### 6.1.9 A correct iteration loop in Python

The sample in the official pagination guide is close but omits three things: it never de-duplicates, it calls `raise_for_status()` with no `429` handling (which directly contradicts Rho's own rate-limits page), and it re-sends a fixed `page_size` without saying whether that is required. The version below is the one to copy. It runs as written.

```python
import os
from typing import Any, Dict, Iterator, Optional

import requests

BASE = os.environ.get("RHO_BASE_URL", "https://rhoapi.rho.co/api/v1")


def paginate(
    session: requests.Session,
    path: str,
    resource_key: str,
    params: Optional[Dict[str, Any]] = None,
    page_size: int = 100,
) -> Iterator[Dict[str, Any]]:
    """Yield every item from a Rho list endpoint.

    `params` must stay byte-identical across pages: any change to a filter or
    to sort_by/order invalidates the cursor with 400. page_size is the one
    parameter that may change mid-walk.
    """
    base_params = dict(params or {})
    base_params["page_size"] = page_size
    page_token: Optional[str] = None
    seen: set = set()

    while True:
        query = dict(base_params)
        if page_token is not None:
            query["page_token"] = page_token

        resp = session.get(f"{BASE}{path}", params=query, timeout=30)
        resp.raise_for_status()          # replace with request_with_retry, see 6.2.5
        body = resp.json()

        items = body[resource_key]
        for item in items:
            # Offset cursors can repeat a row if the data shifts under the walk.
            # De-duplicate on the opaque id rather than trusting the cursor.
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            yield item

        page_token = body["page"]["next_page_token"]
        if page_token is None:           # the ONLY terminator
            return
        if not items:
            # Defensive: a non-null token on an empty page would loop forever.
            raise RuntimeError(f"{path}: empty page with a non-null cursor")


def make_session(token: str) -> requests.Session:
    s = requests.Session()               # keep-alive roughly halves per-call latency
    s.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept-Encoding": "gzip",       # must name gzip explicitly, see 6.2.8
    })
    return s
```

Verified against the sandbox, with the module above saved as `rho_paginate.py`:

```bash
export RHO_BASE_URL=https://rhoapi-sandbox.rho.co/api/v1 RHO_API_TOKEN=sandbox
python3 -c '
import os, rho_paginate as r
s = r.make_session(os.environ["RHO_API_TOKEN"])
print(sum(1 for _ in r.paginate(s, "/transactions", "transactions", {"account_type": "checking"}, page_size=7)))
print(sum(1 for _ in r.paginate(s, "/accounts", "accounts", page_size=3)))'
# -> 42
# -> 14
```

42 matches the sandbox corpus (42 of 72 transactions are `account_type=checking`) and 14 matches the full accounts set, at page sizes that force 6 and 5 round trips respectively.

Three details worth naming. The `seen` set is unbounded, so for a multi-million-row walk swap it for a bloom filter or drop de-duplication and pin a window filter instead (6.1.6). `resource_key` is passed explicitly because it is not always derivable (`/invoicing/customers` returns `customers`). And `page_size` lives in `base_params` rather than being re-sent as a literal, so a caller can raise it mid-walk without touching the cursor.

#### 6.1.10 A correct iteration loop in TypeScript

Same contract, using the platform `fetch` (Node 18+, Deno, Bun, or a browser proxied through your own backend, since the API sends no CORS headers at all).

```typescript
const BASE = process.env.RHO_BASE_URL ?? "https://rhoapi.rho.co/api/v1";
const TOKEN = process.env.RHO_API_TOKEN ?? "";

interface Page {
  next_page_token: string | null; // present on every response, null on the last page
}
type ListResponse<K extends string, T> = { page: Page } & { [P in K]: T[] };

/** Walk every page of a Rho list endpoint.
 *  `params` must be byte-identical on every page: changing a filter or the
 *  sort invalidates the cursor with 400. page_size may change mid-walk. */
export async function* paginate<K extends string, T extends { id: string }>(
  path: string,
  resourceKey: K,
  params: Record<string, string> = {},
  pageSize = 100,
): AsyncGenerator<T> {
  let pageToken: string | null = null;
  const seen = new Set<string>();

  for (;;) {
    const query = new URLSearchParams({ ...params, page_size: String(pageSize) });
    if (pageToken !== null) query.set("page_token", pageToken);

    const resp = await rhoFetch(`${BASE}${path}?${query.toString()}`); // see 6.2.6
    if (!resp.ok) {
      const problem = await resp.text();
      throw new Error(`GET ${path} -> ${resp.status}: ${problem}`);
    }
    const body = (await resp.json()) as ListResponse<K, T>;

    const items = body[resourceKey] as T[];
    for (const item of items) {
      // Offset cursors can repeat a row if the data shifts under the walk.
      if (seen.has(item.id)) continue;
      seen.add(item.id);
      yield item;
    }

    pageToken = body.page.next_page_token;
    if (pageToken === null) return;                 // the ONLY terminator
    if (items.length === 0) throw new Error(`${path}: empty page with a non-null cursor`);
  }
}
```

Verified against the sandbox with `node rho.ts` on Node 26 (native type stripping), `RHO_BASE_URL` pointed at sandbox: 42 checking transactions at `pageSize` 7, 14 accounts at `pageSize` 3, identical to the Python walk.

The `next_page_token: string | null` type is the point of the `Page` interface. If you generate types from Rho's OpenAPI document you will get `string` and your terminal page will throw, per the divergence in 6.1.1.

#### 6.1.11 What pagination does not give you

| Missing | Consequence |
| --- | --- |
| Any total or count | Result-set size is knowable only by walking it. Progress bars are impossible; so is "show 1 of 40 pages" |
| Backwards paging | Iteration is forward only. Re-walk from the start to go back |
| A durable resume point | No documented cursor TTL and explicit advice against bookmarking. Resume from a timestamp filter plus client-side `id` de-duplication |
| An incremental-sync primitive | There is no `updated_after` on any endpoint. Delta sync must be built from `initiated_after`/`posted_after` (transactions) or `date_after` (invoices) plus client dedup. See the Filtering and sorting section |
| `ETag` / `Last-Modified` / `304` | Observed, none are emitted and no conditional request works. Every poll pays the full payload, about 5.6 KB gzipped per 100-transaction page |
| Webhooks or an event stream | Nothing in the corpus. Every integration is poll-only, under the rate ceiling in 6.2 |

---

### 6.2 Rate limits

#### 6.2.1 What is documented

From `/docs/v1/rate-limits`, verbatim:

| Limit | Threshold |
| --- | --- |
| Per API Access Token | Approximately 60 requests per minute |
| Per source IP | Approximately 600 requests per minute |

Plus five prose commitments on the same page:

- "These limits apply uniformly across all public Rho API endpoints."
- "The source-IP limit covers the combined traffic from every integration sharing that IP address, including integrations using different API Access Tokens."
- "We enforce rate limits across a distributed edge network, so the limits are approximate rather than an exact concurrency allowance. Clients must not assume that exactly 60 simultaneous requests will succeed."
- "Pace traffic steadily below one request per second instead of sending the full minute's allowance in a burst."
- "When a limit is exceeded, we return `429 Too Many Requests`."

Derived budget arithmetic, which is the number you actually plan against:

| Quantity | Value |
| --- | --- |
| Per-token budget | ~60 req/min, ~1 req/s, ~86,400 req/day |
| Per-IP budget | ~600 req/min, ~10 req/s |
| Tokens needed to saturate one IP | 10, at full per-token rate |
| Max rows/min per token at `page_size=100` | 6,000 |
| Max rows/min per IP at `page_size=100` | 60,000 |
| Time to walk 1,000,000 transactions on one token | ~167 minutes at the ceiling, longer at the documented pacing |

The per-IP pool is shared, and that interacts badly with the auth guide's advice to pin a stable egress IP for the token allowlist: concentrating your traffic on one NAT gateway also concentrates your rate-limit risk there, where an unrelated team's runaway job can throttle you.

#### 6.2.2 What was actually observed

Neither documented limit is enforced on the sandbox host at any load a responsible probe can generate.

| Test (observed) | Documented expectation | Result |
| --- | --- | --- |
| 60 requests to `/accounts` on token `sandbox`, one connection, 10.67 s (337 req/min) | throttle after ~60 in the minute | 60 x 200 |
| 60 more at concurrency 30 in 1.173 s, same token, same minute (~120 cumulative) | throttle | 60 x 200 |
| 30 more at concurrency 30 against `/transactions?page_size=100`, same minute (~150 cumulative) | throttle | 30 x 200 |
| 60 at concurrency 60 in 0.871 s (68.9 req/s, 4,134 req/min instantaneous) | docs explicitly warn 60 simultaneous may not succeed | all 60 succeeded, twice |
| 65 requests on a brand-new, never-used bearer token in 11.30 s | a fresh bucket should exhaust at ~60 | 65 x 200 |
| 300 requests to `/transactions` at concurrency 20 in ~4 s (~3,600 req/min) | throttle | 300 x 200 |
| 30 requests at concurrency 30 in ~1 s, re-run 2026-09-12 | throttle | 30 x 200, zero rate-limit headers |

Roughly 430 requests over 10.5 minutes produced zero `429` responses and zero `5xx`. The unique-token run rules out the possibility that the literal string `sandbox` is allowlisted.

```bash
# reproduce the last row: 30 concurrent calls, all 200, no rate-limit headers anywhere
B=https://rhoapi-sandbox.rho.co/api/v1
for i in $(seq 1 30); do
  curl -s -o /dev/null -D "/tmp/h$i" -w "%{http_code} " "$B/accounts?page_size=1" \
    -H "Authorization: Bearer sandbox" &
done; wait; echo
grep -lihE "retry-after|ratelimit" /tmp/h[0-9]* | wc -l   # -> 0
```

> **Divergence:** the rate-limits page states concrete thresholds with no environment qualifier, and the sandbox enforces neither. An integrator who load-tests against the sandbox will conclude their client is correctly paced and ship something production may reject. Treat the sandbox as a correctness environment only, never a capacity environment, and size your client against the documented 60/min per token and 600/min per IP.

> **Divergence:** `429` is documented in the rate-limits guide but appears in **none** of the 14 operation reference pages, which uniformly list `200, 400, 401, 403, 500, 503` (plus `404` on the eight single-resource operations). A client generated from the OpenAPI document will not have a `429` branch. Add it by hand.

> **Divergence:** because `429` is unreachable in the sandbox, the entire documented `Retry-After` contract, including the unusual `0` case, is untestable against Rho's own test environment. Nobody can confirm from outside that a `429` from Rho carries `Retry-After` at all. Write the retry path blind, unit-test it against synthetic responses (as the implementations below are), and make a missing `Retry-After` a first-class case.

#### 6.2.3 The `Retry-After` contract, including the documented zero

Verbatim from the docs:

- "If it is a positive integer, wait at least that many seconds before retrying."
- "If it is `0`, we have not applied a fixed cooldown. This does not guarantee that an immediate retry will succeed, so use exponential backoff with jitter instead of retrying in a tight loop."

| `Retry-After` value | Required client behavior | Documented? |
| --- | --- | --- |
| Positive integer seconds | Wait at least that many seconds | Yes |
| `0` | No cooldown was computed. Do **not** retry immediately. Fall through to exponential backoff with jitter | Yes |
| Absent | Not documented. Handle it: fall through to backoff | No |
| HTTP-date form (RFC 9110 permits it) | Not documented. Parse it defensively rather than crashing | No |
| Negative or unparseable | Not documented. Fall through to backoff | No |

The `0` case is the trap. RFC 9110 defines `Retry-After` as a delay in seconds or an HTTP-date, so a naive implementation reads `0`, sleeps zero seconds, and hammers the endpoint in a tight loop precisely when the service is asking it to stop. Rho has repurposed `0` to mean "no fixed cooldown", which is the opposite of what the literal value says. Any correct implementation must special-case it.

Both implementations below encode the same rule: `Retry-After` produces a delay only when it parses to a strictly positive value; every other case, including `0`, absent, negative and malformed, falls through to full-jitter exponential backoff.

#### 6.2.4 No budget observability

| Missing header | Consequence |
| --- | --- |
| `RateLimit-Limit` / `RateLimit-Remaining` / `RateLimit-Reset` | You cannot see how much budget you have left, so you cannot self-pace. Fixed conservative pacing is the only strategy available |
| `X-RateLimit-*` | Same. The de-facto convention is absent too |
| `Retry-After` | Never observed on any status code in roughly 430 responses |
| `X-Request-Id` / `Request-Id` / `traceparent` | No correlation handle for support. Cloudflare's `cf-ray` is the only per-request identifier that exists. Log it on every call |

The complete observed header set on a 200 is ten headers and contains none of the above:

```
HTTP/2 200
date: Sat, 12 Sep 2026 00:25:31 GMT
content-type: application/json
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: a39ac685feff0f61-EWR
```

#### 6.2.5 A correct backoff in Python

Retries `429`, `500`, `502`, `503`, `504` and transport failures. Honors a positive `Retry-After`, treats `0`, absent, negative and malformed as "use backoff", caps any single sleep, adds jitter even to an honored header so a fleet does not resynchronize, and drains the body so the connection can be reused.

```python
import datetime
import email.utils
import random
import time
from typing import Any, Dict, Optional

import requests

RETRYABLE = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 6
BASE_DELAY = 0.5      # seconds
MAX_DELAY = 60.0      # cap on any single sleep
MAX_HONORED_RETRY_AFTER = 300.0


def parse_retry_after(value: Optional[str], now: Optional[float] = None) -> Optional[float]:
    """Return a delay in seconds, or None if the header gives no usable delay.

    Rho documents only integer seconds and assigns `0` the special meaning
    "no fixed cooldown applied", so `0` must NOT be treated as "retry now".
    RFC 9110 also permits an HTTP-date, which Rho does not document; parse it
    anyway rather than crashing.
    """
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        seconds = int(value)
    except ValueError:
        try:
            parsed = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        if parsed is None:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=datetime.timezone.utc)
        now = time.time() if now is None else now
        delta = parsed.timestamp() - now
        return delta if delta > 0 else None
    if seconds <= 0:
        return None          # the documented `0` case: fall back to backoff
    return float(seconds)


def backoff_delay(attempt: int) -> float:
    """Full-jitter exponential backoff. attempt is 1-based."""
    ceiling = min(MAX_DELAY, BASE_DELAY * (2 ** (attempt - 1)))
    return random.uniform(0.0, ceiling)


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
    sleep=time.sleep,
) -> requests.Response:
    last_exc: Optional[Exception] = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = session.request(method, url, params=params, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
            if attempt == MAX_ATTEMPTS:
                raise
            sleep(backoff_delay(attempt))
            continue

        if resp.status_code not in RETRYABLE:
            return resp
        if attempt == MAX_ATTEMPTS:
            return resp

        header_delay = parse_retry_after(resp.headers.get("Retry-After"))
        if header_delay is not None:
            delay = min(header_delay, MAX_HONORED_RETRY_AFTER)
            delay += random.uniform(0.0, 1.0)   # de-synchronise a fleet
        else:
            delay = backoff_delay(attempt)
        resp.close()
        sleep(delay)

    assert last_exc is not None
    raise last_exc
```

Because Rho cannot produce a `429`, the only way to test this is against a synthetic server. Assertions that must pass:

```python
assert parse_retry_after(None) is None
assert parse_retry_after("") is None
assert parse_retry_after("0") is None      # the documented zero, must fall through
assert parse_retry_after("-3") is None
assert parse_retry_after("5") == 5.0
assert parse_retry_after("garbage") is None
# a local server returning 429 (Retry-After: 0), then 429 (Retry-After: 1), then 200
# -> 3 attempts, first sleep < 0.5 s (backoff, not the header), second sleep in [1.0, 2.0]
```

Those assertions were run against a `http.server` stub and pass: attempt count 3, sleeps `[0.37, 1.075]`.

#### 6.2.6 The same in TypeScript

```typescript
const RETRYABLE = new Set([429, 500, 502, 503, 504]);
const MAX_ATTEMPTS = 6;
const BASE_DELAY_MS = 500;
const MAX_DELAY_MS = 60_000;
const MAX_HONORED_RETRY_AFTER_MS = 300_000;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** Milliseconds of delay from a Retry-After header, or null when it gives none.
 *  Rho documents `0` as "no fixed cooldown applied", so 0 must fall through
 *  to exponential backoff rather than becoming an immediate retry. */
export function parseRetryAfter(value: string | null, nowMs = Date.now()): number | null {
  if (value === null) return null;
  const trimmed = value.trim();
  if (trimmed === "") return null;
  if (/^-?\d+$/.test(trimmed)) {
    const seconds = Number(trimmed);
    return seconds > 0 ? seconds * 1000 : null;
  }
  const at = Date.parse(trimmed); // RFC 9110 also allows an HTTP-date
  if (Number.isNaN(at)) return null;
  const delta = at - nowMs;
  return delta > 0 ? delta : null;
}

export function backoffDelayMs(attempt: number): number {
  const ceiling = Math.min(MAX_DELAY_MS, BASE_DELAY_MS * 2 ** (attempt - 1));
  return Math.random() * ceiling; // full jitter
}

export async function rhoFetch(url: string, init: RequestInit = {}): Promise<Response> {
  for (let attempt = 1; ; attempt++) {
    let resp: Response;
    try {
      resp = await fetch(url, {
        ...init,
        headers: {
          Authorization: `Bearer ${process.env.RHO_API_TOKEN ?? ""}`,
          "Accept-Encoding": "gzip",
          ...(init.headers ?? {}),
        },
        signal: AbortSignal.timeout(30_000),
      });
    } catch (err) {
      if (attempt >= MAX_ATTEMPTS) throw err;
      await sleep(backoffDelayMs(attempt));
      continue;
    }
    if (!RETRYABLE.has(resp.status) || attempt >= MAX_ATTEMPTS) return resp;

    const header = parseRetryAfter(resp.headers.get("retry-after"));
    const delay =
      header === null
        ? backoffDelayMs(attempt)
        : Math.min(header, MAX_HONORED_RETRY_AFTER_MS) + Math.random() * 1000;
    await resp.arrayBuffer(); // drain so the connection can be reused
    await sleep(delay);
  }
}
```

Verified the same way against a `node:http` stub returning `429 Retry-After: 0`, then `429 Retry-After: 1`, then `200`: three attempts, total elapsed 2.2 s, which is consistent with backoff on the first and an honored 1 second plus jitter on the second. `parseRetryAfter` returns `null` for `null`, `""`, `"0"`, `"-3"` and `"garbage"`, `5000` for `"5"`, and a positive value for a future HTTP-date.

#### 6.2.7 Pacing rules that follow

1. **Budget one request per second per token.** The docs say "below one request per second", which reads as under 60/min, not at 60/min. At `page_size=100` that is still 6,000 rows a minute.
2. **Do not burst.** Queue and cap concurrency rather than firing a minute's allowance at once, because a distributed counter can trip while your other requests are still in flight.
3. **Use one token per integration and count tokens against the IP pool.** Ten tokens at full rate saturate a single egress IP.
4. **Reuse connections, but do not over-multiplex one of them.** Observed, keep-alive roughly halves per-call latency (p50 206 ms cold, 112 ms warm), but pushing 50 concurrent streams onto a single HTTP/2 connection made p50 about 13x worse (1,504 ms) for only 31 req/s aggregate. Prefer a small pool of connections with modest per-connection concurrency.
5. **Budget 90 to 145 ms of server time per call** from a US East client, plus 70 to 100 ms of connect and TLS on a cold connection, with a rare tail near 1 s. Payload size is not a latency driver.
6. **Send `Accept-Encoding: gzip` explicitly.** Observed, gzip is the only encoding served; brotli, zstd, deflate and the `*` wildcard all get an uncompressed body. On a 40,768-byte transactions page gzip cuts the wire cost to about 5.6 KB, roughly 7x.
7. **Log `cf-ray` on every request.** It is the only identifier Rho support can correlate against.

---

### 6.3 Errors

#### 6.3.1 The RFC 9457 claim versus reality

The API reference overview states: "Errors follow [RFC 9457 problem details]". The auth guide cites the obsolete RFC 7807 for the same objects. Every operation page documents the same four-field schema:

| Field | Type | Required | Documented description |
| --- | --- | --- | --- |
| `type` | string | required | "A URI reference that identifies the problem type. Example: `about:blank`" |
| `title` | string | required | "A short, human-readable summary of the problem type." |
| `status` | integer | required | "The HTTP status code." |
| `detail` | string | optional | "A human-readable explanation specific to this occurrence of the problem." |

> **Divergence:** `type` is not a URI in practice. Observed values are the bare strings `"2"`, `"1303"`, `"1317"` and `"about:blank"`. The first three are numeric family codes. RFC 9457 says a `type` that is not a usable URI should be treated as `about:blank`, so a strictly conforming client collapses all three into one generic type and loses the only machine-readable distinction the API offers.

> **Divergence:** `title` is occurrence-specific, not type-specific. RFC 9457 section 3.1.2 says `title` should not change for a given `type`, but `1303` produces "account not found", "card not found", "statement not found", "customer not found", "invoice not found", "transaction not found", "transaction file not found" and "invoice file not found", and `1317` produces at least seven different strings. The stable part of the document is too coarse to branch on, and the precise part is free prose outside the versioning contract.

> **Divergence:** the auth guide's worked example is `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}`. Observed, the real 401 is `{"type":"2","title":"Unauthenticated","status":401}`: a different `type`, a different `title`, and no `detail` at all. Every 401 and every 404 carries zero diagnostic information beyond the title.

#### 6.3.2 The actual body shapes

Five shapes exist. Only the first four are JSON, and only the first three are problem documents.

| Class | Exact body | Content-Type | Trigger |
| --- | --- | --- | --- |
| Auth | `{"type":"2","title":"Unauthenticated","status":401}` | `application/problem+json` | Missing, empty, or non-`Bearer` Authorization header |
| Parse failure | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: <name>"}` | `application/problem+json` | A value fails type coercion, or a scalar parameter is repeated |
| Semantic validation | `{"type":"1317","title":"<specific message>","status":400}` | `application/problem+json` | The value parses but fails a rule |
| Not found | `{"type":"1303","title":"<resource> not found","status":404}` | `application/problem+json` | Unknown id on a detail route |
| Framework 404 | `404 page not found` | `text/plain; charset=utf-8` | Unknown path under `/api/v1` (Go's `http.NotFound`) |

Beyond those, four non-JSON bodies come from infrastructure in front of the application and your parser must survive all of them:

| Status | Body | Producer |
| --- | --- | --- |
| 405 | **empty**, `content-length: 0`, `allow: GET` | The Go service, on any method other than GET including `HEAD` and `OPTIONS` |
| 411 | HTML, "POST requests require a Content-length header" | Google frontend, before Rho's code. Also returned for `PUT` with the same POST wording |
| 414 | HTML, nginx "Request-URI Too Large" | ingress-nginx, at a URI length ceiling between 8 KB and 16 KB |
| 403 | HTML, Cloudflare "Attention Required!" | Cloudflare WAF, triggered by a nonstandard method token |
| 404 | `default backend - 404`, `text/plain` | ingress-nginx, for paths outside `/api/v1` |

Reproduce the whole set:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1; H="Authorization: Bearer sandbox"
curl -s "$B/accounts?page_size=101"  -H "$H"   # {"type":"1317","title":"page_size must be between 1 and 100","status":400}
curl -s "$B/accounts?page_size=abc"  -H "$H"   # {"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}
curl -s "$B/accounts?page_token=xyz" -H "$H"   # {"type":"1317","title":"page_token must be a valid cursor","status":400}
curl -s "$B/accounts?sort_by=bogus"  -H "$H"   # {"type":"1317","title":"invalid sort_by parameter: \"bogus\"","status":400}
curl -s "$B/accounts/00000000-0000-4000-8000-000000000000" -H "$H"  # {"type":"1303","title":"account not found","status":404}
curl -s "$B/accounts/not-a-uuid"     -H "$H"   # {"type":"about:blank",...,"detail":"invalid parameter: account_id"}
curl -s "$B/accounts"                          # {"type":"2","title":"Unauthenticated","status":401}
curl -s "$B/nope-not-real"           -H "$H"   # 404 page not found      (text/plain)
curl -s -X POST "$B/accounts" -H "$H" -H "Content-Length: 0" -D - -o /dev/null | head -4   # 405, allow: GET, empty body
```

#### 6.3.3 The numeric `type` codes

Four values have been observed across every reachable error path. They are families, not precise identifiers.

| `type` | Status | Meaning | Distinguishing field | Known coverage |
| --- | --- | --- | --- | --- |
| `"2"` | 401 | Unauthenticated. Credential absent, empty, or not presented as `Bearer <value>` | none; `title` is always "Unauthenticated" | Every auth failure, on both `/api/v1` and production `/mcp/v1` |
| `"1303"` | 404 | Resource not found on a detail route | `title` names the resource | account, card, transaction, transaction file, statement, customer, invoice, invoice file |
| `"1317"` | 400 | The value parsed but violated a rule | `title` carries the message and echoes the offending value | `page_size` range, invalid cursor, `sort_by`, `order`, card `type`, card `status`, `min_amount` > `max_amount` |
| `"about:blank"` | 400 | The value failed type binding, or a scalar parameter was repeated | `detail` names the parameter, never echoes the value | any parameter |

Two dialects, and they never mix. A `1317` body carries a descriptive `title` and **no** `detail`. An `about:blank` body carries the generic title "Bad Request" plus a `detail` that names the parameter. So the field you read to find out what went wrong depends on which dialect you got.

Every `1317` title observed:

| Title | Produced by |
| --- | --- |
| `page_size must be between 1 and 100` | all six list endpoints |
| `page_token must be a valid cursor` | garbage token, cross-endpoint token, token plus a changed filter, forged fingerprint, `v:2`, negative offset, offset greater than the total |
| `invalid sort_by parameter: "<value>"` | `/accounts`, `/invoicing/customers` only |
| `invalid order parameter: "<value>"` | `/accounts`, `/invoicing/customers` only |
| `invalid type parameter: "<value>"` | `/cards` only |
| `invalid status parameter: "<value>"` | `/cards` only |
| `min_amount must be less than or equal to max_amount` | `/transactions` only |

#### 6.3.4 Status code to cause

| Status | Reachable in sandbox | Cause | Retry? |
| --- | --- | --- | --- |
| 200 | yes | Success. Note that a `200` with an empty array is ambiguous between "no matching rows" and "your filter was silently dropped": see the Filtering and sorting section on the empty-value trap and the semicolon trap | n/a |
| 301 | yes | `GET /api/v1` with no trailing path, from nginx | Follow it |
| 400 | yes | Two dialects. `about:blank` means an unparseable value or a repeated scalar parameter; `1317` means a rule violation | **No.** Fix the request |
| 401 | yes | Missing, empty, malformed, unknown, revoked, or expired token, or a scheme other than a capital-B `Bearer`. Observed, `bearer sandbox` in lowercase returns 401, which deviates from RFC 7235 case-insensitive scheme matching | No, unless you rotate the credential |
| 403 | **no** | Documented: a valid token missing the required scope, or a source IP outside the token's allowlist. Unreachable in the sandbox, which enforces neither scopes nor allowlists | No |
| 404 | yes | Two shapes: `1303` problem+json for an unknown id on a detail route, `text/plain` for an unknown path | No |
| 405 | yes | Any method other than GET, including `HEAD` and `OPTIONS`. Empty body, `allow: GET`. Observed, this check runs **before** authentication | No |
| 411 | yes | `POST` or `PUT` with no `Content-Length`, from the Google frontend | No |
| 414 | yes | URI longer than the nginx ceiling, between 8 KB and 16 KB | No |
| 422 | **no** | Never observed. Every validation failure is a 400, so status alone cannot separate malformed syntax from invalid content | n/a |
| 429 | **no** | Documented as the rate-limit response. Not reachable in the sandbox at any load; body shape unknown | **Yes**, per 6.2 |
| 500 | not observed | Documented on every operation | Yes, with backoff |
| 503 | not observed | Documented on every operation, with no explanation anywhere of what it means or whether it is retryable | Yes, with backoff |

> **Divergence:** the operation reference documents `403`, `500` and `503` on every endpoint and none of them was reachable in the sandbox, while `405`, `411` and `414` are all readily reachable and documented nowhere. Your error handling has to cover the union, not the documented set.

#### 6.3.5 Parameter validation runs before authentication

This ordering is worth knowing before you debug a credential problem. Observed, with no `Authorization` header at all:

| Request | Status with no credential | Status with a credential |
| --- | --- | --- |
| `GET /accounts?page_size=abc` | **400** `about:blank`, "invalid parameter: page_size" | 400, identical |
| `GET /accounts/not-a-uuid` | **400** `about:blank`, "invalid parameter: account_id" | 400, identical |
| `GET /accounts?page_size=101` | 401 | 400 `1317` |
| `GET /accounts?page_token=garbage` | 401 | 400 `1317` |
| `GET /accounts/<valid-uuid, unknown>` | 401 | 404 `1303` |
| `POST /accounts` | **405** | 405 |

So type binding (the `about:blank` family) and the method check both sit in front of authentication, while semantic validation (the `1317` family) and resource lookup sit behind it. The operational rule: **a non-401 response does not prove your token worked.** If you are smoke-testing credentials, use a request that is unambiguously well-formed, such as `GET /accounts`, and check for `200`.

#### 6.3.6 A correct error parser

Branch on HTTP status. Capture `type` and `title` for logs. Never make control flow depend on either, because `type` is too coarse (one code covers eight resources) and `title` is free prose that the versioning policy does not cover.

```python
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class RhoError(Exception):
    status: int
    kind: str          # branch on this, never on `type` or `title`
    type_code: Optional[str]
    message: str
    cf_ray: Optional[str]

    def __str__(self) -> str:
        return f"{self.status} {self.kind}: {self.message} (cf-ray={self.cf_ray})"


_KIND_BY_STATUS = {
    400: "bad_request",       # your query is wrong, do not retry unchanged
    401: "unauthenticated",   # missing / malformed / unknown / revoked / expired token
    403: "forbidden",         # valid token, missing scope or source IP off the allowlist
    404: "not_found",
    405: "method_not_allowed",
    429: "rate_limited",      # retryable
    500: "server_error",      # retryable
    503: "unavailable",       # retryable
}


def raise_for_rho(resp: requests.Response) -> None:
    if resp.ok:
        return
    kind = _KIND_BY_STATUS.get(resp.status_code, "unexpected")
    type_code: Optional[str] = None
    message = resp.text[:500]

    # Only application-level errors are problem+json. 405 has an empty body,
    # unrouted paths are text/plain, and 403/411/414 from the edge are HTML.
    if resp.headers.get("content-type", "").startswith("application/problem+json"):
        try:
            body = resp.json()
        except ValueError:
            body = {}
        if isinstance(body, dict):
            type_code = body.get("type")
            message = body.get("detail") or body.get("title") or message

    raise RhoError(
        status=resp.status_code,
        kind=kind,
        type_code=type_code,
        message=message,
        cf_ray=resp.headers.get("cf-ray"),
    )
```

Run against the live sandbox it produces, in order, for the nine probes in 6.3.2:

```
400 kind=bad_request          type=1317         msg='page_size must be between 1 and 100'
400 kind=bad_request          type=about:blank  msg='invalid parameter: page_size'
400 kind=bad_request          type=1317         msg='page_token must be a valid cursor'
404 kind=not_found            type=1303         msg='account not found'
400 kind=bad_request          type=about:blank  msg='invalid parameter: account_id'
401 kind=unauthenticated      type=2            msg='Unauthenticated'
404 kind=not_found            type=None         msg='404 page not found\n'
405 kind=method_not_allowed   type=None         msg=''
```

The last two rows are the reason for the content-type guard: a parser that assumes JSON on every non-2xx crashes on the plain-text 404 and on the zero-byte 405.

#### 6.3.7 Rules for an error handler

1. **Branch on status, log `type` and `title`.** There is no stable machine-readable error code, and the free-prose `title` is not covered by the versioning contract.
2. **Never assume the body is JSON.** Four reachable statuses return HTML, plain text, or nothing. Guard on `content-type: application/problem+json` before parsing.
3. **Read `detail` for `about:blank` and `title` for `1317`.** The two dialects put the useful string in different fields and never populate both.
4. **Do not retry a 400.** It means your query is wrong, and it will be wrong again.
5. **Handle 429 even though the OpenAPI document omits it,** and handle a missing `Retry-After` on it.
6. **Log `cf-ray` on every response, success or failure.** There is no request id; `cf-ray` is the only handle Rho support can correlate.
7. **Do not infer authentication success from a non-401.** Type-binding 400s and the 405 method check run ahead of auth (6.3.5).
8. **Treat `200` with an empty array as suspicious after a filtered query.** A silently dropped filter and a genuinely empty result are indistinguishable. Assert against an unfiltered control query.

---

### 6.4 Versioning and compatibility

#### 6.4.1 The model

From `/docs/v1/versioning`, which calls itself "the stability contract for the Rho API":

- "The Rho API is versioned per release; today that's the URL path `/api/v1`. The current version is `v1`."
- "**`v1` is stable and additive-only**. A request that works today keeps working. Changes that would break existing code require a **new API version**; we do not ship them into `/api/v1`."
- "Any `v1` deprecation or sunset comes with **at least 15 days' notice** before the change takes effect."

Versioning is by URL path only. There is no version header, no date-pinned version, no `Accept` media-type versioning, and no per-account pinning. The OpenAPI document additionally carries `Version: 1.0.0`, which is a document version and not something you can request. A future `v2` would be a separate path, so `v1` callers are never migrated implicitly. That is a good property: you will never be moved without changing a URL.

#### 6.4.2 The change classification

Published exhaustively, and short enough to quote in full:

| Change | Classification | Ships into `v1`? |
| --- | --- | --- |
| Add an enum value | Non-breaking | Yes, at any time |
| Add a nullable response field | Non-breaking | Yes, at any time |
| Add an optional query parameter | Non-breaking | Yes, at any time |
| Remove or rename an enum value | Breaking | No, new version |
| Remove a response field | Breaking | No, new version |
| Change a field's type | Breaking | No, new version |
| Make an optional field required | Breaking | No, new version |

Read that first column again as a threat model: Rho reserves the right to send you, without notice and without a version bump, an enum value you have never seen, a response field you have never seen, and to accept a query parameter you do not send. Those three are the ones your code must survive.

#### 6.4.3 What the policy does not classify

The list of breaking changes is short, which makes its silences load-bearing. None of the following is classified anywhere on the page:

| Unclassified change | Why it matters to you |
| --- | --- |
| Adding a **non-nullable** response field | Only nullable additions are blessed. A non-nullable addition is neither permitted nor forbidden |
| Adding a **required** query parameter | Only optional additions are blessed |
| Adding a new endpoint | Presumably additive, never stated |
| Removing an endpoint | Presumably needs a version, never stated |
| Changing pagination defaults or maxima | A `page_size` maximum dropping from 100 to 50 would break any client hard-coding 100, and the page does not say whether that requires a new version |
| Tightening rate limits | Not addressed. The published limits already say "approximately" |
| Changing error `detail` or `title` strings | Not addressed, which is why you must not parse them |
| Changing a sort default | Not addressed. `/transactions` defaulting to `initiated_at` desc is behavior your cursors depend on |
| Changing the **meaning** of an existing enum value without renaming it | The worst case, and the policy is silent |
| MCP protocol version support (`2026-07-28`, `2025-11-25`, `2025-06-18`) | Dropping `2025-06-18` later would be breaking under no stated policy |

#### 6.4.4 The deprecation notice has no delivery channel

A 15-day floor is short by industry norms, and it applies to "any `v1` deprecation or sunset".

> **Divergence:** the versioning page promises at least 15 days' notice but never names the channel that notice arrives on. There is no changelog URL anywhere in the documentation corpus, no status page reference, and observed, no `Deprecation` or `Sunset` response header (RFC 8594) on any of roughly 430 captured responses. The complete header set on a 200 is the ten headers listed in 6.2.4. So the machine-readable channel that would normally carry a deprecation notice does not exist, and the human channel is unspecified. In practice you will learn about a deprecation from an email to whoever created the token, or from your own monitoring.

The operational consequence: build the monitoring that the notice channel does not give you. Alert on a schema drift (an unknown enum value, an unknown field) appearing in production traffic, because that is the earliest signal you will get that something changed.

#### 6.4.5 Client obligations as engineering rules

Rho publishes four obligations. Each is restated below as a concrete rule, with the failure it prevents.

**1. Never switch on an unknown enum without a default.**

Rho's wording: "Give any `switch` on it a default case so a new value shows up as unknown rather than an error." The shipped enums are already large, which tells you how often they grow: `cards.status` has 11 values (`printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `active`, `expiring`, `locked`, `canceled`, `suspended`, `expired`), `transactions.transaction_type` has 22 distinct values in the sandbox corpus alone, `accounts.account_type` has 5, and `invoices.status` has 6. Concretely:

- Model every enum as `string` at the wire boundary, and map to your own closed type in one place with an explicit `unknown` arm.
- In TypeScript, do not type a response field as a union of literals. Type it `string`, then narrow. A union literal type is a lie about the wire, and structural typing will not catch it at runtime.
- In Rust, `#[serde(other)]` on a catch-all variant. In Java, `@JsonEnumDefaultValue`. In Go, a plain `string`. In Kotlin and Swift, a case that carries the raw string.
- An unknown value must degrade, never throw. A new `transaction_type` should render as "other" in a ledger view and must not abort a reconciliation run.
- Do not persist the enum as a database `ENUM` column or a constrained `CHECK`. A new value from Rho becomes an insert failure at 3 a.m.

**2. Ignore unknown response fields.**

- Turn off strict deserialization at the Rho boundary specifically: Jackson `FAIL_ON_UNKNOWN_PROPERTIES = false`, serde without `deny_unknown_fields`, Zod `.passthrough()` rather than `.strict()`, Pydantic `model_config = ConfigDict(extra="ignore")`.
- If you use code generation from Rho's OpenAPI document, check what your generator does with additional properties by default. Several generate strict models.
- Do not checksum or hash a response body to detect change. A new field added upstream changes the hash without changing anything you care about.

**3. Treat IDs as opaque strings.**

- Do not parse structure out of an id. Most ids in the sandbox look like UUIDs, but statement ids are short numeric-looking strings (`572981`, `439951`, `200527`) and are not validated as UUIDs at all, so a garbage statement id returns 404 rather than 400. Any code that assumes "Rho ids are UUIDs" is already wrong.
- Do not use an id's format to route. Do not infer a resource type from an id.
- Store them as `TEXT` or `VARCHAR` with generous headroom, never `UUID`, never `VARCHAR(36)`. The documented obligation is explicit: "without assuming a fixed length or layout".
- Compare ids byte for byte. Do not case-normalize.

**4. Two more rules the policy implies but does not state.**

- **Never switch on `type` in an error body, and never parse `title` or `detail`.** Neither is covered by the versioning contract, `type` is a coarse family code shared across eight resources, and the titles are free prose. Branch on HTTP status (6.3.6).
- **Never persist or parse a `page_token`.** Its "format and lifetime are not part of the API contract and may change without notice", and it demonstrably has two different internal formats already (6.1.4). Everything in 6.1.3 is diagnostics, not interface. If you build the offset-forging total-count trick, you have shipped a dependency on the one thing Rho explicitly disclaimed.

#### 6.4.6 MCP parity

The versioning page extends the same policy to the MCP surface: "The MCP server is 1:1 with the REST API, so the `/mcp/v1` tool schemas follow the same policy as the REST contracts above: additive-only, with breaking changes requiring a new version."

It goes further on tool names: "Tool *names* derive from the frozen `v1` operationIds, so **tool names will never change**." The 14 operationIds are `listaccounts`, `getaccount`, `listcards`, `getcard`, `listtransactions`, `gettransaction`, `gettransactionfile`, `liststatements`, `getstatement`, `listinvoicingcustomers`, `getinvoicingcustomer`, `listinvoicinginvoices`, `getinvoicinginvoice`, `getinvoicinginvoicefile`. Tool descriptions are explicitly not part of the contract and may change at any time.

> **Divergence:** the "1:1 with the REST API" claim is not quite true at the byte level. Observed, the same problem document serializes its keys in different orders on the two surfaces: `/api/v1` returns `{"type":"2","title":"Unauthenticated","status":401}` while production `/mcp/v1` returns `{"status":401,"title":"Unauthenticated","type":"2"}`. Same fields, same values, different serializers, which implies two implementations behind one stated contract. Any client comparing error bodies by hash across the two surfaces will see a difference where none is intended.

> **Divergence:** `/mcp/v1` does not exist on the sandbox host. Observed, `https://rhoapi-sandbox.rho.co/mcp/v1` returns `404 default backend - 404` from the ingress default backend, meaning no route is configured, while the same path on production returns a proper `401 application/problem+json`. The MCP guide documents the production URL and never says the sandbox lacks the surface. See the MCP section.

---

### 6.5 The short version

| Mechanism | The rule |
| --- | --- |
| Pagination | Loop until `page.next_page_token === null`, never on a short page. Replay the filter query byte for byte; only `page_size` may change. De-duplicate on `id`, because five of six endpoints use an offset cursor that cannot honor the documented stability promise. Type the token `string \| null`. Never parse or persist it |
| Rate limits | Size against the documented 60/min per token and 600/min per IP, not against the sandbox, which enforces neither. Pace under 1 req/s per token, cap concurrency, reuse connections without over-multiplexing |
| Retries | Retry 429, 500, 502, 503, 504 and transport errors with full-jitter exponential backoff. Honor `Retry-After` only when it parses to a strictly positive value; `0`, absent, negative and malformed all mean "use backoff". Add `429` to any generated client, since the OpenAPI document omits it |
| Errors | Branch on HTTP status only. Guard on `content-type: application/problem+json` before parsing. `about:blank` puts the detail in `detail`; `1317` puts it in `title`. Log `type`, `title` and `cf-ray`. A non-401 does not prove your token worked |
| Versioning | Assume new enum values, new response fields and new optional parameters arrive without notice. Default case on every enum, lenient deserialization at the boundary, ids as opaque variable-length strings. Deprecation notice is at least 15 days (a floor, not a fixed figure) and arrives on no machine-readable channel, so monitor for schema drift yourself |
