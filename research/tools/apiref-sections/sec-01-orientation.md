## 1. Orientation and mental model

All observations in this section were captured against the live sandbox and against unauthenticated production metadata endpoints on **2026-09-11 and 2026-09-12 (UTC)**. Wherever a claim comes from Rho's published documentation it is attributed to the page it came from. Wherever it comes from a request this document actually made, it is labelled "observed" and the request is shown.

### 1.1 What the Rho API is

Rho is a business banking and spend-management platform. The Rho API is that platform's read interface to a single Rho business's own data: balances, the transaction ledger, corporate cards, period-end statements, and the invoicing records (issued invoices and the customers they bill).

Rho's own framing, from `/product/api`, contrasts it with the two adjacent categories it is not:

> "The Rho API is neither: it is the banking platform's own front door to your own company's data."

Three properties define the shape of everything else in this document:

| Property | Value | Source |
| --- | --- | --- |
| Surface size | 14 operations, 5 resource families, all `GET` | `https://docs.rho.co/api/v1/openapi` index, confirmed by enumeration |
| Access model | Long-lived bearer token per business (`rhobat_` prefix), or OAuth 2.0 for third-party apps | `/docs/v1/auth`, `/docs/v1/partner-auth` |
| Cost and eligibility | $0, no separate API fee, "every Rho business gets API access, no waitlist and no approval step" | `/product/api` |

The API is versioned in the URL path. The current and only version is `v1`, spec version `1.0.0`. Rho's versioning page commits `v1` to being "stable and additive-only": new enum values, new nullable fields, and new optional query parameters can appear without warning, while removals, renames, type changes, and newly-required fields require a new API version. Deprecations carry "at least 15 days' notice."

> **Divergence:** The versioning page promises at least 15 days' notice before a `v1` deprecation, but there is no machine-readable channel to deliver it on. No `Deprecation` or `Sunset` header (RFC 8594) was observed on any response, on either host. Notice arrives by watching the docs by hand.

### 1.2 What it is not

Naming the non-goals early saves a lot of evaluation time.

| It is not | Consequence |
| --- | --- |
| A payments API | No operation initiates, approves, cancels, or reschedules any money movement. See §1.4. |
| An aggregator (Plaid, Teller, MX) | It reads one business's Rho data only. There is no institution-linking concept, no item, no cross-bank coverage. |
| Banking-as-a-service | You cannot open accounts, issue cards, or onboard sub-entities through it. |
| Event-driven | There are no webhooks and no event stream. Every integration polls. Rho's changelog (2026-08-03) states webhooks are "next", with no date. |
| Browser-callable | No CORS headers are emitted on any response and `OPTIONS` returns `405`. Observed, §1.8. Server-to-server only. |
| A full mirror of the Rho product | There is no Payments, Bill Pay, Users, Departments, Vendors, Approvals, Reimbursements, Expenses, or Treasury-trading resource in `v1`. Bill Pay and AP in particular have no representation at all. |
| Multi-entity | A token is scoped to one business. A Claude MCP connection is likewise one business at a time, per Rho's help center. |

### 1.3 When it shipped, and what that implies

The API came out of beta in mid-2026. Rho published two different dates for the same launch:

| Source | Date | Text |
| --- | --- | --- |
| Blog, "Introducing: The Rho API" | 2026-07-29 | API out of beta, MCP server in production, Claude native support live, available to all customers |
| Changelog, "Introducing Rho API" | 2026-08-03 | "Read-only is live today. Write access and webhooks are next." |
| `/product/api` page footer | "current as of August 2026" | capability as-of stamp |

So the public surface is roughly six weeks old as of this writing (2026-09-11): 44 days after the blog date, 39 after the changelog date. Wherever this document dates the API, that is the figure it means. Three practical implications follow, and each one shows up concretely later in this document:

1. **The documentation is behind the implementation in specific, checkable ways.** Cards and Invoicing shipped, their scopes were added to the OpenAPI document and to the per-product guides, but not back-ported to the central pages. Two of the divergences in this section are exactly this failure mode (§1.6, §1.7).
2. **The sandbox is a static fixture set, not a simulator.** It cannot produce a `403`, a `429`, or a rate-limit header, and at least one documented endpoint is outright broken in it (§1.5). Anything an integrator must handle in production but cannot trigger in sandbox is unit-test territory, not integration-test territory.
3. **The read-only boundary is a v1 property, not a permanent one.** Rho has publicly announced write access as the next step. Design the client so that a future write surface is additive to your code, and do not build product assumptions ("a leaked token cannot move money") that would silently become false on a future version.

### 1.4 The read-only boundary, and exactly what it forbids

This is the single most load-bearing fact about the API, and unusually for a security claim it is structurally verifiable rather than a policy assertion: there is no non-`GET` operation in `v1` to call.

**Observed.** Every write method on every path returns `405 Method Not Allowed` with `Allow: GET` and a zero-byte body, and it does so *before authentication runs*:

```bash
curl -sS -o /dev/null -D - -X POST https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H "Content-Length: 0"
```

```http
HTTP/2 405
date: Sat, 12 Sep 2026 00:23:35 GMT
content-length: 0
allow: GET
via: 1.1 google
cf-cache-status: DYNAMIC
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
server: cloudflare
cf-ray: a39ac3acfbcac4d1-EWR
```

Note the absence of any `Authorization` header. The prior probe pass swept `POST`, `PUT`, `PATCH`, and `DELETE` across all six collection paths and the single-resource paths, with a valid token, a garbage token, and no token at all: `405` in every one of those cells, `Allow: GET` on every path. Routing precedes method checking, which precedes auth, so `POST` to a path that does not exist returns `404 page not found` instead.

Two consequences worth internalising:

- There is no hidden write surface reachable by verb probing. No path advertises anything but `GET`.
- A `405` is **not** evidence that your token was accepted. If you are health-checking with a write verb, you are testing the router, not your credential.

What the boundary forbids, drawn from the operation catalogue plus Rho's own help-center enumeration ("Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account."):

| Cannot | Notes |
| --- | --- |
| Initiate any payment | ACH, wire, international wire, check, internal transfer, bill pay |
| Act on the approvals queue | You can *read* `status: "awaiting_approval"` on transactions; you cannot approve, reject, or cancel |
| Create, issue, lock, cancel, or modify a card | Including spending limits and MCC allow/block rules |
| Manage users, roles, or permissions | No Users resource exists |
| Change any account setting | Including 2FA, alerts, and debit controls |
| Create, edit, send, cancel, or mark-paid an invoice | Invoicing is read-only too, despite being a workflow product in the dashboard |
| Write back to a transaction | No note, memo, label, department, or receipt upload |
| Move Treasury positions | No trading surface |
| Receive a push event | No webhooks. Poll only, under the documented ~60 req/min per token |
| See a full PAN, CVC, or expiry | Cards expose `last_4` only, stated explicitly in `/docs/v1/cards` |

Rho describes four independent enforcement layers behind this: the surface has no write op; every scope is `*:read`, so there is no writable scope to request; only Account Owners and Admins can mint a token or authorize an OAuth or Claude connection, behind 2FA; and credentials expire, cap out at 20 per business, support a 100-entry IP allowlist, and revoke instantly. Layers two through four are covered in the Authentication section; layer one is the one you can verify yourself in ten seconds with the command above.

### 1.5 The two hosts

| Environment | Base URL | Auth | MCP surface |
| --- | --- | --- | --- |
| Production | `https://rhoapi.rho.co/api/v1` | Real API Access Token or OAuth access token | `https://rhoapi.rho.co/mcp/v1` |
| Sandbox | `https://rhoapi-sandbox.rho.co/api/v1` | Any non-empty bearer token | none (observed `404`) |

Both hostnames resolve to the same pair of Cloudflare edge IPs (`104.18.26.176`, `104.18.27.176`, observed via `dig +short`) and return byte-identical `401` bodies and header sets. The sandbox serves a deterministic fictional fixture set. Record counts, observed just after 00:20 UTC on 2026-09-12 by walking every list endpoint at `page_size=100`:

| Endpoint | Response array key | Records |
| --- | --- | --- |
| `/accounts` | `accounts` | 14 |
| `/cards` | `cards` | 8 |
| `/transactions` | `transactions` | 72 |
| `/statements` | `statements` | 33 |
| `/invoicing/customers` | **`customers`** | 7 |
| `/invoicing/invoices` | **`invoices`** | 12 |

The array key is the bare resource name, not the path. `/invoicing/customers` returns `customers`, not `invoicing_customers`. This trips up generic client code that derives the key from the path.

Four things the sandbox cannot do for you:

1. **It cannot produce a `403`.** Scopes are not enforced there at all. A single garbage token (`Bearer qqqq-garbage-token-no-scopes-at-all`) read all five scope families successfully. Your scope-denial handling and your IP-allowlist-rejection handling are untestable before production.
2. **It cannot produce a `429`.** 150 requests on one token inside a 57-second window all returned `200`, a pace 2.5 times the documented per-token allowance, with no throttling and no rate-limit header of any kind. Your backoff path is untestable there.
3. **It has no MCP endpoint.** Observed: `GET https://rhoapi-sandbox.rho.co/mcp/v1` returns `404` with the body `default backend - 404` (the ingress-nginx default backend, meaning no route is configured), and `https://rhoapi-sandbox.rho.co/.well-known/oauth-protected-resource/mcp/v1` returns the same. The MCP guide documents `/mcp/v1` and gives a `claude mcp add` example pointing at production, but never says the sandbox lacks the route.
4. **At least one documented endpoint is broken in it.** All 9 sandbox invoices that carry a `file_id` return `404` from the invoice-file endpoint that is supposed to exchange that `file_id` for a download URL:

```bash
curl -sS -w '\nHTTP %{http_code}\n' \
  "https://rhoapi-sandbox.rho.co/api/v1/invoicing/invoices/70000000-0000-4000-8000-000000000010/files/50000000-0000-4000-8000-000000000027" \
  -H "Authorization: Bearer sandbox"
```

```json
{"type":"1303","title":"invoice file not found","status":404}
```

> **Divergence:** `/docs/v1/invoicing` says "When an invoice has a PDF, `file_id` is present ... Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`." In sandbox, every documented-correct `(invoice_id, file_id)` pairing returns `404`. The equivalent transaction-attachment endpoint works (shown in §1.9). Treat invoice PDF retrieval as unverifiable until you have production credentials.

> **Divergence:** There is no way to tell the two environments apart from an error response. Production and sandbox `401` bodies are byte-identical (`{"type":"2","title":"Unauthenticated","status":401}`, same 52 bytes, same md5), the header sets match, and the hostnames share Cloudflare IPs. No environment marker exists in any response. A typo in `RHO_API_BASE_URL` that points a sandbox integration at production produces a `401` that reads exactly like a bad token, and the developer will reasonably debug the credential rather than the hostname.

### 1.6 The surface: 14 operations across 5 resources

All 14 are `GET`. The `operationId` column is the docs URL slug at `docs.rho.co/api/v1/openapi/<tag>/<id>.md`; Rho commits in the versioning page that MCP tool names derive from these frozen `v1` operationIds and "will never change", though it never publishes the exact casing or the tool-name transform.

| # | Resource | Method and path | operationId | Scope | Kind |
| --- | --- | --- | --- | --- | --- |
| 1 | Accounts | `GET /accounts` | `listaccounts` | `accounts:read` | list |
| 2 | Accounts | `GET /accounts/{account_id}` | `getaccount` | `accounts:read` | single |
| 3 | Cards | `GET /cards` | `listcards` | `cards:read` | list |
| 4 | Cards | `GET /cards/{id}` | `getcard` | `cards:read` | single |
| 5 | Transactions | `GET /transactions` | `listtransactions` | `transactions:read` | list |
| 6 | Transactions | `GET /transactions/{id}` | `gettransaction` | `transactions:read` | single |
| 7 | Transactions | `GET /transactions/{transaction_id}/files/{file_id}` | `gettransactionfile` | `transactions:read` | file |
| 8 | Statements | `GET /statements` | `liststatements` | `statements:read` | list |
| 9 | Statements | `GET /statements/{id}` | `getstatement` | `statements:read` | single |
| 10 | Invoicing | `GET /invoicing/customers` | `listinvoicingcustomers` | `invoicing:read` | list |
| 11 | Invoicing | `GET /invoicing/customers/{customer_id}` | `getinvoicingcustomer` | `invoicing:read` | single |
| 12 | Invoicing | `GET /invoicing/invoices` | `listinvoicinginvoices` | `invoicing:read` | list |
| 13 | Invoicing | `GET /invoicing/invoices/{invoice_id}` | `getinvoicinginvoice` | `invoicing:read` | single |
| 14 | Invoicing | `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | `getinvoicinginvoicefile` | `invoicing:read` | file |

Read that table as three tiers, because the tiers behave very differently:

- **Six list endpoints.** These carry the query surface. `/transactions` alone takes 13 filters (`account_id`, `account_type`, `transaction_type`, `status`, `user_id`, `card_id`, `search`, `initiated_after/before`, `posted_after/before`, `min_amount`, `max_amount`) plus `sort_by`, `order`, and the two pagination parameters. `/statements` takes 6 filters. This is where the real work happens. See the Filters and the Pagination sections.
- **Six single-resource getters.** **Observed:** these return exactly the same fields as the corresponding list row, with zero additions. The sweep that establishes this listed each collection, then re-fetched every row individually (`GET /{resource}/{id}` for each id in the list) and compared deep-equal: 146 resources across the six types (14 accounts, 8 cards, 72 transactions, 33 statements, 7 customers, 12 invoices), 146/146 identical, no key present in one form and not the other, no value differences. There is no summary-versus-detail tier. Fetching a list and then looping single `GET`s to "enrich" rows buys nothing and burns your ~60 req/min budget. The one exception is `GET /statements/{id}`, which buys you a re-signed `pdf_url`, not new fields, and even that is subject to a server-side signing cache described in the Files section.
- **Two file endpoints.** These are not file downloads. They return three keys (`download_url`, `file_id`, `file_name`) where `download_url` is a Google Cloud Storage V4 signed URL with `X-Goog-Expires=899` (14 minutes 59 seconds), fetched without your Rho credential. One of them (`gettransactionfile`) works in sandbox; the other (`getinvoicinginvoicefile`) does not, per §1.5.

> **Divergence:** The getting-started page states "Current release is **read-only** and covers accounts and transactions." The read-only half is correct. The coverage half is wrong by three entire resource families: Cards, Statements, and Invoicing are all live, documented on their own guide pages, present in the OpenAPI index, and returning data in sandbox right now. An evaluator who reads only `/docs/v1/getting-started` will conclude the API is 5 operations when it is 14.

### 1.7 The five scopes

Scopes are `resource:action` strings. Per `/docs/v1/auth` they are enforced before the request reaches the handler, and a token missing the required scope is rejected with `403 Forbidden`. There are exactly five, and every one of them is `:read`:

| Scope | Grants | Covers operations |
| --- | --- | --- |
| `accounts:read` | Account information for the business | 1, 2 |
| `cards:read` | Business cards information | 3, 4 |
| `transactions:read` | Transactions the business has access to | 5, 6, 7 |
| `statements:read` | Statements for the business's accounts | 8, 9 |
| `invoicing:read` | Invoicing information | 10 to 14 |

The authoritative live source is the RFC 9728 protected-resource metadata document, which is public and needs no credential:

```bash
curl -sS https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1
```

```json
{"resource":"https://rhoapi.rho.co/mcp/v1","authorization_servers":["https://auth.rho.co"],"bearer_methods_supported":["header"],"scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],"resource_documentation":"https://docs.rho.co/docs/v1/mcp"}
```

> **Divergence:** `/docs/v1/auth` says "The scopes available today are:" and then lists **three**: `accounts:read`, `transactions:read`, `statements:read`. The OpenAPI `AccessToken` security scheme lists **five**. `/docs/v1/cards` says "Both endpoints require the `cards:read` scope" and `/docs/v1/invoicing` says "Every endpoint requires the `invoicing:read` scope." The live metadata above lists **five**. The authoritative answer is five; the central auth page is stale by exactly the two scopes that shipped with Cards and Invoicing. This matters most for partner OAuth: `/docs/v1/partner-auth` tells you to email Rho your "requested scopes" with the example string `accounts:read transactions:read offline_access` and a link to that stale table, so an app built from those two pages will request too few scopes and discover it only when a customer's Cards or Invoicing call 403s.

The per-operation reference pages do not help you here. Fetch one and look at its Security line:

```bash
curl -sS https://docs.rho.co/api/v1/openapi/accounts/listaccounts.md | sed -n '1,8p'
```

```text
# List accounts

Returns a paginated list of accounts for the authenticated business

Endpoint: GET /accounts
Version: 1.0.0
Security: AccessToken
```

> **Divergence:** `/docs/v1/auth` says "The required scope for each endpoint is listed under its **Security** section in the API reference." It is not. Every one of the 14 operation reference pages carries the bare line `Security: AccessToken` with no scope name attached, as the fetch above shows (`.../cards/listcards.md` behaves the same). There is no published per-endpoint scope mapping anywhere in Rho's docs. The mapping in the table above is reconstructed from the per-product guides plus the resource-to-scope naming pattern; Cards and Invoicing are the only two Rho states outright, and Statements is never given a scope on its own guide page at all.

Three further scope facts, from Rho's help center and `/docs/v1/auth`, that shape design:

- Scope selection happens at token creation or at OAuth consent, and Claude's authorization screen lets the user reduce the requested set. Grant the narrowest set per integration.
- There is no sub-scope granularity at all: no per-account scoping, no date window, no amount ceiling, no field-level redaction. `transactions:read` means the entire ledger for the entire business for all time. `invoicing:read` includes your customers' legal names, emails, and postal addresses, which is third-party PII.
- Only Account Owners and Admins can mint a token (behind a 2FA challenge) or authorize an OAuth or Claude connection.

### 1.8 Decision guide: REST, MCP, or neither

The two surfaces are the same contract. Rho's versioning page states the MCP server is "1:1 with the REST API" and the MCP page states it "uses the same API contract, authentication model, scopes, and error behavior." So the choice is not about capability, it is about who is calling and how the result is consumed.

**Reach for the REST API when:**

| Situation | Why REST |
| --- | --- |
| Warehouse or ETL ingestion of the ledger | You need deterministic pagination, retry, and idempotent upsert. Section on Pagination covers the cursor contract. |
| Reconciliation against an accounting system | You need exact, repeatable field access, not a model's summary of it. |
| An internal dashboard or a scheduled cash report | Server-side scheduled job, cached, one token, predictable request count. |
| Anything that must be auditable | A REST call is reproducible from the request line. A tool call mediated by an LLM is not. |
| You need a specific filter combination | The 13 transaction filters and 6 statement filters are only addressable from REST. An MCP client may or may not expose them all. |

**Reach for MCP when:**

| Situation | Why MCP |
| --- | --- |
| A human is asking ad-hoc questions of the data | "What did we spend on software last quarter?" is a conversation, not a job. |
| You are building an agent workflow in Claude or another MCP client | One command connects it, shown below. |
| You want zero integration code | The Claude connector path (Customize → Connectors → Rho → sign in → pick business → authorize) requires no token handling at all, and uses OAuth rather than a pasted secret. |
| You want tool names that are frozen forever | Rho commits that tool names derive from the frozen `v1` operationIds and will never change, so they are safe to hard-code in saved automations. Tool *descriptions* are explicitly not part of the contract. |

The setup command, verbatim from `/docs/v1/mcp`. Note that it points at production: there is no sandbox MCP host to substitute (§1.5).

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

MCP specifics worth knowing before you commit: it is Streamable HTTP at `/mcp/v1`, it advertises protocol versions `2026-07-28`, `2025-11-25`, and `2025-06-18`, every non-`initialize` request must carry `MCP-Protocol-Version`, JSON-RPC batches are rejected, and anything older than `2025-06-18` is rejected. **Observed:** production `/mcp/v1` is the only endpoint in the estate that returns an RFC-compliant `401`, carrying `www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"`; the REST API at `/api/v1` returns `401` with no `WWW-Authenticate` header at all, on both hosts. Rho publishes no tool list, no input or output schemas, no prompt names, and no resource URIs for the MCP server, so what lands in a model's context is only inferable from the 14 REST operations.

**Neither is the right tool when you need any of the following.** Each of these is a hard stop in `v1`, not a workaround:

| You need | Status | What to do instead |
| --- | --- | --- |
| To write anything | Impossible. All 14 ops are `GET`; §1.4. | Use the dashboard, or wait for the announced write surface. Rho has not said whether writes will land as new `v1` operations or as a new version, so do not assume your `v1` client keeps working unchanged when they arrive. |
| Webhooks or any push event | Do not exist. Changelog 2026-08-03: "Write access and webhooks are next." | Poll, inside the documented ~60 req/min per token and ~600 req/min per source IP. Filter on `posted_after` / `initiated_after` to keep pages small. |
| Real-time or sub-minute freshness | Not achievable. Polling one endpoint every second exceeds the documented token budget; no `ETag`, no `Last-Modified`, no `304` path exists, so every poll transfers the full body. | Re-scope to a polling cadence measured in minutes, or drive the workflow from the Rho dashboard. |
| To call it from a browser | Impossible. **Observed:** no `Access-Control-Allow-Origin` on any response with or without an `Origin` header, no `Vary: Origin`, and `OPTIONS /api/v1/accounts` returns `405` with `allow: GET`. | Proxy through your own backend. This also keeps the token off the client. |
| A cheap liveness probe | `HEAD /api/v1/accounts` returns `405` with `allow: GET`, a deviation from RFC 9110, which expects `HEAD` wherever `GET` is implemented. | Probe with `GET /accounts?page_size=1`. |
| Bill Pay, vendors, users, approvals, departments, reimbursements, or treasury trading | No resource exists in `v1`. | Out of scope for the API entirely. |
| A request id for support escalation | **Observed:** no `X-Request-Id`, `traceparent`, or equivalent on any response. The only correlation handle is Cloudflare's `cf-ray`. | Log `cf-ray` on every response. |
| Rate-limit budget observability | **Observed:** no `RateLimit-*`, no `X-RateLimit-*`, and no `Retry-After` on any of roughly 430 captured responses. | Pace conservatively from a fixed budget; you get no feedback signal. |

> **Divergence:** The rate-limits page documents `429 Too Many Requests` with branch logic on `Retry-After` (positive integer means wait that long, `0` means back off exponentially). None of the 14 operation reference pages documents a `429` response at all. All 14 list `200, 400, 401, 403, 500, 503`, and the 8 single-resource operations add `404`. A client generated from the OpenAPI document will therefore have no `429` case, and the sandbox cannot produce one to catch the gap in testing. Add the `429` path by hand.

### 1.9 In five minutes, against the sandbox

Everything below was run end to end against `https://rhoapi-sandbox.rho.co/api/v1` on 2026-09-12 (UTC) and the outputs are the real ones. You need `curl` and `python3`. You do not need a Rho account, a token, or an approval step.

`--compressed` is worth setting from the start: gzip is the only encoding the API honours (brotli, zstd, and deflate are all declined), and on a 40 KB transactions page it cuts the wire payload by roughly 7 times.

#### Step 1: point at the sandbox

```bash
export RHO_BASE=https://rhoapi-sandbox.rho.co/api/v1
export RHO_TOKEN=sandbox   # any non-empty string works in sandbox
```

The literal string `sandbox` is not special. Sandbox auth is a non-empty-string check after a case-sensitive `Bearer ` prefix, nothing more. Details and the exact inferred algorithm are in the Authentication section.

#### Step 2: read every account and its balance

```bash
curl -sS --compressed "$RHO_BASE/accounts?page_size=100" \
  -H "Authorization: Bearer $RHO_TOKEN" \
  -H "Accept: application/json" | python3 -c '
import sys, json
d = json.load(sys.stdin)
for a in d["accounts"]:
    b = a["balance"]
    print("%s  %-9s %13s %s  %s" % (a["id"], a["account_type"], format(b["amount"] / 100, ",.2f"), b["currency"], a["account_name"]))
print("count", len(d["accounts"]), "next", d["page"]["next_page_token"])
'
```

The real output, in full:

```text
30000000-0000-4000-8000-000000000002  checking       8,761.38 USD  Cash (Checking)
30000000-0000-4000-8000-000000000003  checking      87,116.97 USD  Cash (Checking)
30000000-0000-4000-8000-000000000007  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000008  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000009  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000010  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000005  checking           0.00 USD  Inventory Checking
30000000-0000-4000-8000-000000000006  checking       8,119.70 USD  Primary Checking
30000000-0000-4000-8000-000000000001  checking          10.46 USD  Reserve Checking
30000000-0000-4000-8000-000000000011  rewards            0.00 USD  Rewards
30000000-0000-4000-8000-000000000012  rewards            0.00 USD  Rewards
30000000-0000-4000-8000-000000000013  savings            0.00 USD  Savings
30000000-0000-4000-8000-000000000014  savings            0.00 USD  Savings
30000000-0000-4000-8000-000000000004  checking     154,609.29 USD  Treasury Checking
count 14 next None
```

Two conventions land in that one call and hold everywhere: **money is always an object**, `{"amount": <signed integer minor units>, "currency": "<ISO 4217>"}`, never a decimal; and **the last page is signalled by `page.next_page_token` being JSON `null`**, with the key always present.

Two details in the output are worth carrying into the data-model sections. The four `credit` rows omit `account_number_last_4` and `routing_number_last_4` entirely rather than returning them as `null`, so field-absence is meaningful in this API. And the account displayed as "Treasury Checking" has `account_type: "checking"`; `treasury` shows up as an `account_type` only inside statement rows, where it is not a member of the documented account enum at all.

#### Step 3: filter the ledger

```bash
curl -sS --compressed -G "$RHO_BASE/transactions" \
  -H "Authorization: Bearer $RHO_TOKEN" \
  --data-urlencode "status=settled" \
  --data-urlencode "page_size=3"
```

The first of the three rows, complete and unedited:

```json
{
  "account_id": "30000000-0000-4000-8000-000000000009",
  "account_name": "Credit Account",
  "account_type": "credit",
  "amount": { "amount": -6331, "currency": "USD" },
  "attachments": [
    { "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15", "file_name": "parking-receipt.pdf" }
  ],
  "card_id": "20000000-0000-4000-8000-000000000004",
  "card_name": "Lucas Bennett",
  "counterparty_name": "Midtown Parking Services",
  "id": "019f0554-0bf0-7000-8000-00000000000a",
  "initiated_at": "2026-06-26T19:07:02Z",
  "money_movement_id": "40000000-0000-4000-8000-000000000007",
  "posted_at": "2026-06-27T19:13:15Z",
  "status": "settled",
  "transaction_type": "card_debit",
  "user_full_name": "Lucas Bennett",
  "user_id": "10000000-0000-4000-8000-000000000004"
}
```

Note how much is denormalized onto the row: account name and type, card id and name, user id and name. That is deliberate, and it is why the single-resource getters add nothing (§1.6). Reconciliation rarely needs a second call.

#### Step 4: walk every page

Save as `rho_walk.py`. This is the canonical iteration shape for all six list endpoints; only the path and the array key change.

```python
import json, os, urllib.parse, urllib.request

BASE  = os.environ.get("RHO_BASE", "https://rhoapi-sandbox.rho.co/api/v1")
TOKEN = os.environ.get("RHO_TOKEN", "sandbox")

def walk(path, key, **filters):
    params = dict(filters)
    params.setdefault("page_size", 100)
    while True:
        url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
        yield from body[key]
        token = body["page"]["next_page_token"]
        if token is None:
            return
        params["page_token"] = token

if __name__ == "__main__":
    rows = list(walk("/transactions", "transactions", page_size=25))
    net = sum(r["amount"]["amount"] for r in rows)
    print(f"{len(rows)} transactions, net {net/100:,.2f} USD")
```

```bash
python3 rho_walk.py
```

```text
72 transactions, net 1,723,640.44 USD
```

Three rules the cursor imposes, all covered in depth in the Pagination section: the token is opaque and must be passed back verbatim; it is bound to the endpoint *and* its filters and sort order, so changing any filter mid-walk invalidates it with a `400`; and page size is `[1, 100]` inclusive across all six endpoints, defaulting to 20.

#### Step 5: fetch a file

The file endpoint returns metadata plus a signed URL. The download itself goes to Google Cloud Storage and must not carry your Rho token.

```bash
TID=019f0554-0bf0-7000-8000-00000000000a
FID=2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15

URL=$(curl -sS "$RHO_BASE/transactions/$TID/files/$FID" \
  -H "Authorization: Bearer $RHO_TOKEN" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["download_url"])')

curl -sS -o receipt.pdf -w 'HTTP %{http_code}  %{size_download} bytes  %{content_type}\n' "$URL"
```

```text
HTTP 200  769 bytes  application/pdf
```

The metadata response is exactly three keys:

```json
{
  "download_url": "https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&...",
  "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15",
  "file_name": "parking-receipt.pdf"
}
```

The signed URL is valid for 899 seconds from its `X-Goog-Date`, not the "up to 15 minutes" the docs round it to, and statement PDFs behave differently from transaction attachments in a way the docs do not describe. See the Files and signed URLs section before you build an archiver.

#### Step 6: confirm the boundary yourself

```bash
curl -sS -o /dev/null -w 'POST  -> HTTP %{http_code}\n'   -X POST   -H "Content-Length: 0" -H "Authorization: Bearer $RHO_TOKEN" "$RHO_BASE/accounts"
curl -sS -o /dev/null -w 'DELETE-> HTTP %{http_code}\n'   -X DELETE -H "Authorization: Bearer $RHO_TOKEN" "$RHO_BASE/accounts/30000000-0000-4000-8000-000000000002"
curl -sS -o /dev/null -w 'HEAD  -> HTTP %{http_code}\n'   -I       -H "Authorization: Bearer $RHO_TOKEN" "$RHO_BASE/accounts"
```

```text
POST  -> HTTP 405
DELETE-> HTTP 405
HEAD  -> HTTP 405
```

That is the whole mental model: five read-only resources, fourteen `GET`s, one cursor convention, one money representation, signed URLs for binaries, and a `405` for everything else.

#### Before you move to production

| Step | Where |
| --- | --- |
| Create an API Access Token (Owner or Admin, 2FA-gated, shown once, max 1 year, 45-day idle expiry, max 20 per business, optional 100-entry IP allowlist) | Authentication section |
| Handle the error shapes the sandbox will not show you: `403` (scope or IP allowlist), `429` (undocumented in the OpenAPI), and the non-JSON bodies returned for oversized or duplicated `Authorization` headers | Errors section |
| Pace to the documented ~60 req/min per token, not to what the sandbox tolerates (at least 2.5 times that, observed) | Rate limits section |
| Decide your polling cadence and your `posted_after` watermark, since there are no webhooks and no conditional requests | Pagination and Rate limits sections |
