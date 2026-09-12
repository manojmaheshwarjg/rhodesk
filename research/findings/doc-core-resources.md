# Rho API v1: Core Resources (Accounts, Transactions, Cards)

Complete endpoint-by-endpoint specification, conceptual guidance from the guide pages, and a field-level
cross-check of the documented shapes against the live sandbox responses captured 2026-09-11 23:22 GMT.

Research date: 2026-09-11. All contract facts below are `Version: 1.0.0` of the Rho API unless noted.

## 0. Sources used

| Source | Path | Nature |
| --- | --- | --- |
| Accounts guide | `rho/docs/docs_v1_accounts.md` | Rho conceptual doc |
| Transactions guide | `rho/docs/docs_v1_transactions.md` | Rho conceptual doc |
| Cards guide | `rho/docs/docs_v1_cards.md` | Rho conceptual doc |
| OpenAPI index | `rho/docs/api_v1_openapi.md` | Rho spec export (markdown) |
| Auth / Pagination / Rate limits / Versioning / Getting started / MCP / Partner auth | `rho/docs/docs_v1_*.md` | Rho conceptual docs |
| Operation refs (markdown export) | `rho/api/accounts_*.md`, `rho/api/transactions_*.md`, `rho/api/cards_*.md` | Rho spec export |
| Operation refs (rendered HTML, fetched 2026-09-11 for this analysis) | `rho/tmpfetch/html_*.txt` | Same spec, **strictly richer** than the `.md` export |
| Live sandbox responses | `rho/sandbox/{accounts,cards,transactions}.json` + `.headers` | Ground truth, fictional data |
| Product marketing | `rho/pages/core/product__api.txt` | Marketing, treat as [Rho claim] |
| Help centre | `rho/pages/help/help-center__cards__*.txt` | Product behaviour, not API contract |

**Important methodological finding.** The `.md` operation exports in `rho/api/` are a **lossy** rendering of the
same OpenAPI document that the HTML reference renders. The `.md` files silently drop, for every operation:

* the **required scope** (HTML shows `AccessToken ( Required scopes : accounts:read )`, the `.md` only says `Security: AccessToken`);
* **defaults** for `sort_by`, `order`, `page_size`;
* **numeric ranges** (`page_size integer, [ 1 .. 100 ]`);
* **string formats** (`uuid`, `date-time`, `uri`) and **patterns** (`last_4` → `^[0-9]{4}$`);
* **enum values on query parameters** (`account_type`, `transaction_type`, `status`, `sort_by`, `order`);
* the **`429 Too Many Requests`** response, which is present on every operation in the HTML and on none in the `.md`;
* the **`or null`** nullability marker on response fields.

Everything below is reconciled against the HTML (authoritative) and flags where the `.md` disagrees.

---

## 1. Global contract

### 1.1 Servers

| Environment | Base URL |
| --- | --- |
| Production | `https://rhoapi.rho.co/api/v1` |
| Sandbox | `https://rhoapi-sandbox.rho.co/api/v1` |
| MCP (production) | `https://rhoapi.rho.co/mcp/v1` |
| OAuth authorization server (partners) | `https://auth.rho.co` |

The REST path prefix is `/api/v1`; the MCP prefix is `/mcp/v1`. Operation paths quoted in the reference
(`GET /accounts`) are **relative to `/api/v1`**.

### 1.2 Authentication and scopes

Single supported credential: a bearer token in `Authorization: Bearer <token>`.
"No other authentication header (cookie, API key, signed request) is supported."

Two token families:

* **API Access Token** (`rhobat_` prefix, example given: `rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f`).
  Long-lived, opaque, scoped to a single business. Created only by Account Owners and Admins, behind a 2FA
  challenge, at `https://app.rho.co/settings/access-tokens`. Max **20 active tokens** per business.
  Expiration is **required, maximum one year**. Auto-expires after **45 days of inactivity** (window starts at
  creation for never-used tokens). Optional IP allowlist, **up to 100 entries**. Raw secret shown once.
  Revocation is immediate, no grace period, no un-revoke.
* **OAuth 2.0 partner tokens** (Authorization Code + PKCE `S256`, `audience=https://rhoapi.rho.co`).
  Access token `expires_in: 900` (15 minutes). Refresh tokens single-use and rotating, 30-day rolling.
  Grant lasts 1 year. Registration by emailing `api-partner-request@rho.co`. One active grant per app per business.

Sandbox accepts **any non-empty bearer token** (`Authorization: Bearer sandbox`), intentionally permissive.

Scopes are `resource:action` and are "enforced before your request reaches the handler". Missing scope → `403`.

| Scope | Meaning (from OpenAPI security block) | Listed in `docs_v1_auth.md` scope table? |
| --- | --- | --- |
| `accounts:read` | Read access to business accounts information | Yes |
| `cards:read` | Read access to business cards information | **No** |
| `invoicing:read` | Read access to Invoicing information | **No** |
| `statements:read` | Read access to business statements information | Yes |
| `transactions:read` | Read access to business transactions information | Yes |
| `offline_access` | Refresh-token grant (OAuth partners only) | Not in the table; only in `docs_v1_partner-auth.md` |

**Contradiction #1.** `docs_v1_auth.md` states "The scopes available today are:" and lists exactly three
(`accounts:read`, `transactions:read`, `statements:read`). The OpenAPI security object lists five, adding
`cards:read` and `invoicing:read`. The Cards guide independently states "Both endpoints require the
`cards:read` scope", and the rendered reference confirms `cards:read` on both card operations. The auth guide
is stale.

### 1.3 Required scope per core operation (from the rendered reference only)

| Operation | Method + path | Required scope |
| --- | --- | --- |
| ListAccounts | `GET /accounts` | `accounts:read` |
| GetAccount | `GET /accounts/{account_id}` | `accounts:read` |
| ListTransactions | `GET /transactions` | `transactions:read` |
| GetTransaction | `GET /transactions/{id}` | `transactions:read` |
| GetTransactionFile | `GET /transactions/{transaction_id}/files/{file_id}` | `transactions:read` |
| ListCards | `GET /cards` | `cards:read` |
| GetCard | `GET /cards/{id}` | `cards:read` |

Note that `GET /transactions/{transaction_id}/files/{file_id}` requires only `transactions:read`; there is no
separate file or document scope.

### 1.4 Pagination

Opaque cursor pagination on every list endpoint. Two query params, identical everywhere:

| Param | Type | Notes |
| --- | --- | --- |
| `page_size` | integer, `[1 .. 100]` | Default **20** on all three core list endpoints. Out-of-range → `400 Bad Request`. |
| `page_token` | string | Opaque; omit for the first page. |

Response envelope: the item array is keyed by resource name (`accounts`, `transactions`, `cards`), plus a
`page` object whose single field `next_page_token` is `string` or `null` (`null` = last page). `page` and
`next_page_token` are both marked **required**, i.e. the key is always present even when the value is null.

Rho's stated rules:

* a token is valid only for "that **same endpoint with the same filters and sort order**"; changing filters or
  sort and reusing the cursor yields `400 Bad Request`;
* "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will
  not shift existing pages or cause items to be skipped or duplicated";
* cursors are "designed for live iteration, not for bookmarks. Their format and lifetime are not part of the
  API contract";
* page tokens "belong to the API version that created them, so restart pagination when migrating from v0 to v1"
  (Cards guide). This is the **only mention of a `v0` anywhere in the corpus**; no v0 documentation exists.

**Contradiction #2 (observed, sandbox).** The sandbox `next_page_token`
`eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qSXcifQ` base64url-decodes to:

```json
{"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":"b2Zmc2V0OjIw"}
```

where `f` is a 16-byte binary value (a filter/sort fingerprint, which is exactly the mechanism that enforces
the "same filters" rule) and `t` base64-decodes to the ASCII string **`offset:20`**. The cursor is therefore an
**offset cursor**, at least in sandbox. Offset pagination is precisely the scheme under which an insert during
iteration *does* shift pages and cause skips or duplicates, contradicting the stability guarantee quoted above.
Caveat: sandbox data is static and the production implementation is not observable here.

### 1.5 Rate limits

| Limit | Threshold |
| --- | --- |
| Per API Access Token | approximately **60 requests per minute** |
| Per source IP | approximately **600 requests per minute** |

Applies "uniformly across all public Rho API endpoints"; the IP limit aggregates across different tokens
sharing an IP. Enforced "across a distributed edge network, so the limits are approximate". Guidance: pace
below 1 req/s, do not burst.

On breach: `429 Too Many Requests`. `Retry-After` handling: positive integer → wait at least that many
seconds; value `0` → "we have not applied a fixed cooldown", use exponential backoff with jitter.

`429` appears in the response list of **every** core operation in the rendered reference. It appears in **none**
of the `.md` exports. No response body schema for `429` is published (the `.md` files that do list statuses
give a problem+json schema for 400/401/403/404/500/503 only).

### 1.6 Error envelope

All errors are RFC 9457 problem details, `Content-Type: application/problem+json`. Identical four-field shape
on every documented error status:

| Field | Type | Required | Meaning | Example |
| --- | --- | --- | --- | --- |
| `type` | string | yes | URI reference identifying the problem type | `about:blank` |
| `title` | string | yes | Short human-readable summary of the problem type | `Unauthorized` |
| `status` | integer | yes | The HTTP status code | `401` |
| `detail` | string | no | Human-readable explanation specific to this occurrence | `Token is revoked or has expired` |

There is **no machine-readable error code**, no `instance`, no `errors[]` array, no field-level validation
detail, and no correlation/request id in the body or in the observed headers. Every published example uses
`type: "about:blank"`, i.e. no typed problem URIs are documented.

**Contradiction #3 (minor).** The OpenAPI index cites RFC 9457; `docs_v1_auth.md` links the problem-details
shape to RFC 7807, which RFC 9457 obsoletes.

Documented status semantics:

| Status | When |
| --- | --- |
| `400` | Malformed request; `page_size` outside range; `page_token` reused with changed filters or sort |
| `401` | Missing `Authorization` header, malformed token, unknown token, revoked token, expired token |
| `403` | Valid token lacking the endpoint's scope, **or** request from an IP outside the token's allowlist |
| `404` | Resource does not exist or belongs to another business (single-resource endpoints only) |
| `429` | Rate limit exceeded (HTML reference only) |
| `500` | Server error |
| `503` | Service unavailable |

Note `403` conflates two very different conditions (scope failure and IP allowlist failure) with no
discriminating field beyond free-text `detail`.

**Not stated:** whether `404` vs `403` is used for a resource belonging to another business. The Cards guide
says `404` ("returns `404` when the card does not exist **or belongs to another business**"). The Accounts and
Transactions guides never say. The `403` description in the auth guide covers only scope and IP.

### 1.7 Status codes declared per operation

| Operation | `.md` export declares | HTML reference declares |
| --- | --- | --- |
| ListAccounts | 200, 400, 401, 403, 500, 503 | 200, 400, 401, 403, **429**, 500, 503 |
| GetAccount | 200, 400, 401, 403, 404, 500, 503 | 200, 400, 401, 403, 404, **429**, 500, 503 |
| ListTransactions | 200, 400, 401, 403, 500, 503 | 200, 400, 401, 403, **429**, 500, 503 |
| GetTransaction | 200, 400, 401, 403, 404, 500, 503 | 200, 400, 401, 403, 404, **429**, 500, 503 |
| GetTransactionFile | 200, 400, 401, 403, 404, 500, 503 | 200, 400, 401, 403, 404, **429**, 500, 503 |
| ListCards | 200, 400, 401, 403, 500, 503 | 200, 400, 401, 403, **429**, 500, 503 |
| GetCard | 200, 400, 401, 403, 404, 500, 503 | 200, 400, 401, 403, 404, **429**, 500, 503 |

List endpoints declare no `404`; single-resource endpoints do.

### 1.8 Versioning contract

Additive-only. Non-breaking (may ship into `v1` at any time): **a new enum value**, **a new nullable response
field**, **a new optional query parameter**. Breaking (requires a new API version): removing or renaming an
enum value, removing a response field, changing a field's type, making an optional field required.
Deprecation or sunset carries **at least 15 days' notice**.

Client obligations stated: handle unknown enum values (give every `switch` a default case, `transaction_type`
named explicitly), ignore unrecognised fields, treat IDs as opaque strings, store IDs as-is with no assumed
length or layout. MCP tool schemas follow the same policy, and **tool names derive from frozen `v1`
operationIds and "will never change"**; tool *descriptions* are explicitly outside the contract.
Implied MCP tool names from the reference slugs: `listaccounts`, `getaccount`, `listtransactions`,
`gettransaction`, `gettransactionfile`, `listcards`, `getcard`.

MCP protocol versions advertised: `2026-07-28`, `2025-11-25`, `2025-06-18`. Anything older than `2025-06-18`
and JSON-RPC batches are rejected. Every non-`initialize` request must carry `MCP-Protocol-Version`.

### 1.9 Observed response headers (sandbox, all six captures identical)

```
HTTP/2 200
content-type: application/json
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: <id>
```

**Conspicuously absent from the response headers:** any `X-RateLimit-*` / `RateLimit-*` budget headers (so a
client cannot see remaining quota against the ~60/min token limit before being `429`'d), any request-id or
trace-id header other than Cloudflare's `cf-ray`, any `ETag`, `Last-Modified`, or `Cache-Control`, and any
API-version header. Stack is fronted by Cloudflare with a Google (GCP/GCLB) origin.

---

## 2. Shared schema objects

These component schemas are referenced by name in the rendered reference and are shared across resources.

### `Money`

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `amount` | integer | yes | Minor units, e.g. cents for USD. Signed on transactions (negative = debit). |
| `currency` | string | yes | ISO 4217 code, e.g. `USD`. |

Used as `Account.balance`, `Transaction.amount`, `Card.spending_limit`, `Card.current_spend`,
`Card.pending_spend`. Guidance repeated in three places: "treat amounts as integers rather than decimals".
There is no separate `amount_decimal`, no `exponent`/`scale` field, and no FX rate or original-currency field
anywhere on a transaction (see §5.4).

### `Page`

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `next_page_token` | string or null | yes | Pass as `page_token` for the next page; `null` on the last page. |

There is **no** total count, no `has_more`, no `previous_page_token`, and no page number.

### `Address` (cards only)

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `street` | string | yes | First address line. |
| `second_line` | string | no | Suite, unit, or second address line. |
| `city` | string | yes | |
| `subdivision` | string | yes | State, province, or region. |
| `postal_code` | string | yes | |
| `country_code` | string | yes | ISO 3166-1 alpha-2. |

### `Cardholder`

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `user_id` | string (uuid) | yes | Stable global identifier for the cardholder. Joins to `Transaction.user_id`. |
| `first_name` | string | yes | |
| `last_name` | string | yes | |

No email, no employee id, no role, no status on the cardholder object.

### `MerchantCategory`

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `code` | string | yes | Fixed-width ISO 18245 merchant category code (MCC). |
| `name` | string | no | Human-readable category name "when available". |

### `Merchant`

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Human-readable merchant name. |

Merchant controls identify merchants **only by display name** - no merchant id, no network acceptor id.

### `TransactionAttachment`

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `file_id` | string (uuid) | yes | Stable attachment identifier. |
| `file_name` | string | yes | Original file name. |

No MIME type, no byte size, no uploaded-at timestamp, no uploader, no document classification
(receipt vs invoice vs memo). See §5.6.

### `AccountType` enum (shared by Account and Transaction)

`checking`, `credit`, `investment`, `savings`, `rewards` (5 values).

Note the Statements resource uses a **different** account-type vocabulary: the Statements guide says
"One of checking, savings, credit, or **treasury**". `treasury` is not a member of `AccountType`; the Accounts
API calls the equivalent thing `investment`. **Contradiction #4**: two type vocabularies for the same concept
across sibling resources in the same API version.

---

## 3. Accounts

### 3.1 Conceptual guidance (`docs_v1_accounts.md`)

* The Accounts API "exposes the bank accounts your business holds on Rho - checking, savings, credit,
  treasury investment vehicles, and rewards accounts".
* `account_type` "determines what it can hold and how it behaves" and is **immutable for the lifetime of an
  account**.

| `account_type` | Rho's definition |
| --- | --- |
| `checking` | Operating cash accounts used for everyday inflows and outflows. |
| `savings` | Higher-yield depository accounts segregated from operating cash. |
| `credit` | Revolving credit lines backing corporate cards. |
| `investment` | Treasury sleeves invested in money-market funds or short-duration securities. |
| `rewards` | Cash-back balances earned on card spend. |

* A list call "returns every account in scope for your API Access Token, each with a **single** `balance`
  object". There is exactly one balance per account: **no available-vs-current split, no pending balance, no
  credit limit, no available credit, no APR** on a `credit` account, and no yield on an `investment` account.
* "The list endpoint has **no server-side type filter**". Rho tells you to fetch a page and filter the
  `accounts` array client-side by `account_type`, with the sample `GET /api/v1/accounts?page_size=100`.
* Join guidance: "Every `transaction` already carries `account_id`, `account_type`, and the account's display
  name, so most reconciliation needs no extra calls. When you need live balance or masked account details,
  fetch the account once via `/api/v1/accounts/{account_id}` and cache the result for the duration of the job."

### 3.2 `GET /accounts` (ListAccounts)

Returns a paginated list of accounts for the authenticated business. Scope: `accounts:read`.

Query parameters:

| Param | Type | Required | Default | Constraints / enum |
| --- | --- | --- | --- | --- |
| `sort_by` | string | no | `"account_name"` | Enum: `account_name`, `balance` |
| `order` | string | no | `"asc"` | Enum: `asc`, `desc` |
| `page_size` | integer | no | `20` | `[1 .. 100]` |
| `page_token` | string | no | n/a | Opaque cursor from `page.next_page_token` |

There is **no** `account_id`, `account_type`, `currency`, or `status` filter, and no `search`.

Response `200` body:

| Field | Type | Required | Nullable | Meaning |
| --- | --- | --- | --- | --- |
| `accounts` | array of `Account` | yes | no | |
| `accounts[].id` | string (uuid) | yes | no | Global account identifier |
| `accounts[].account_type` | string enum | yes | no | `checking` \| `credit` \| `investment` \| `savings` \| `rewards` |
| `accounts[].balance` | `Money` | yes | no | Current balance in account currency |
| `accounts[].balance.amount` | integer | yes | no | Minor units |
| `accounts[].balance.currency` | string | yes | no | ISO 4217 |
| `accounts[].account_number_last_4` | string | **no** | yes | Masked account number, last 4 |
| `accounts[].routing_number_last_4` | string | **no** | yes | Masked routing number, last 4 |
| `accounts[].account_name` | string | **no** | yes | Display name |
| `page` | `Page` | yes | no | |
| `page.next_page_token` | string | yes | yes | `null` on last page |

The `Account` object has **6 properties total** (confirmed by the HTML reference's "Show 6 array properties").
No `created_at`, no `status`, no `currency` at account level (only inside `balance`), no nickname/alias
distinct from `account_name`, no bank/partner name, no full account or routing number, no IBAN/SWIFT.

Errors: `400`, `401`, `403`, `429`, `500`, `503`. **No `404`** (list endpoint).

### 3.3 `GET /accounts/{account_id}` (GetAccount)

Returns a single account by its identifier. Scope: `accounts:read`.

Path parameters:

| Param | Type | Required | Format |
| --- | --- | --- | --- |
| `account_id` | string | yes | `uuid` |

No query parameters at all.

Response `200`: the identical `Account` object, unwrapped (`id`, `account_type`, `balance{amount,currency}`,
`account_number_last_4`, `routing_number_last_4`, `account_name`), with the same nullability.

Errors: `400`, `401`, `403`, `404`, `429`, `500`, `503`.

### 3.4 Accounts: documented vs observed (sandbox `accounts.json`, 14 accounts, `next_page_token: null`)

| Field | Documented | Present in sandbox | Notes |
| --- | --- | --- | --- |
| `id` | required | 14/14 | All of form `30000000-0000-4000-8000-0000000000NN`, NN = 01..14 |
| `account_type` | required | 14/14 | |
| `balance` | required | 14/14 | All `USD` |
| `account_name` | optional, nullable | **14/14 present** | Never null, never absent in practice |
| `account_number_last_4` | optional, nullable | **8/14** | **Key omitted entirely** (not null) on all 4 `credit` and both `rewards` accounts |
| `routing_number_last_4` | optional, nullable | **8/14** | Same 8 accounts; every value is `"0089"` |

Observed `account_type` distribution: `checking` 6, `credit` 4, `rewards` 2, `savings` 2, **`investment` 0**.
The sandbox never exercises the `investment` enum value, so an `investment` account's shape (in particular
whether it carries masked numbers) is unverifiable from the corpus.

Observed balances (minor units, USD): `Reserve Checking` 1 046; `Cash (Checking)` 876 138; `Cash (Checking)`
8 711 697; `Treasury Checking` 15 460 929; `Inventory Checking` 0; `Primary Checking` 811 970; all 4 `Credit
Account` 0; both `Rewards` 0; both `Savings` 0.

Notes and mismatches:

1. **Null vs omitted.** The reference types the three optional account fields as "string or null". The sandbox
   **omits the keys** rather than emitting `null`. A strict deserializer that maps "nullable" to "present but
   null" will not break, but a client that assumes presence will. Rho never documents which of the two
   representations to expect; both must be handled.
2. **Contradiction #5.** The Accounts guide says "Alongside the balance, each account carries its type, a
   display name, and the masked account and routing numbers." Six of fourteen sandbox accounts (every `credit`
   and every `rewards` account) carry **no** masked account or routing number. The guide's blanket statement is
   wrong; the schema (optional + nullable) is right.
3. **Display names are not unique.** `Cash (Checking)` appears twice, `Credit Account` four times, `Rewards`
   twice, `Savings` twice. Any reconciliation keyed on `account_name` collides. Only `id` is unique.
4. **Default sort confirmed empirically.** The sandbox list is in ascending alphabetical order of
   `account_name` (Cash, Cash, Credit ×4, Inventory, Primary, Reserve, Rewards ×2, Savings ×2, Treasury),
   consistent with `sort_by=account_name&order=asc`, a default that is documented **only** in the HTML
   reference, not in the `.md` export.
5. The routing number is identical (`0089`) across all deposit accounts, consistent with a single sponsor bank
   (Webster Bank, a division of Santander Bank, N.A., per Rho's own disclosures). The API never names the bank.

---

## 4. Transactions

### 4.1 What a transaction is (`docs_v1_transactions.md`)

"A single `transaction` record models **one ledger event against one account**." The API "surfaces every
monetary movement that touches the accounts your business holds on Rho - card spend, ACH, wires, internal
transfers, interest, and refunds."

The three identity concepts, exactly as Rho frames them:

| Concept | Rho's wording | Consequence |
| --- | --- | --- |
| `id` | "The transaction's identifier. **Stable across re-fetches, but not guaranteed unique per row** - the entries of one money movement can share an `id`." | `id` alone is **not** a primary key. |
| `money_movement_id` | "Identifier shared by every transaction entry belonging to the same money movement. Group on it to treat the entries of one movement as a unit rather than as unrelated events." | The join key for the two (or more) legs of a transfer. |
| `account_id` | "The account the event posted against." | The disambiguator that makes `(id, account_id)` unique. |

Rho's explicit ingestion rule: "Re-fetching a day's window returns the same `id` values, so ingestion can be
made naturally idempotent. Do not assume `id` is unique per row, though: the entries of a single money
movement can share an `id`, so a warehouse keyed on `id` alone **silently drops a leg**. Either key on `id`
together with the fields that distinguish entries of the same movement, such as `account_id`, or group on
`money_movement_id` and treat the movement as your unit."

This is the reason `GET /transactions/{id}` carries an optional `account_id` query parameter (§4.6).

### 4.2 Lifecycle: pending vs posted

* `status` is one of `pending`, `settled`, `failed`, `awaiting_approval`.
* "Most events are created pending and settle once funds clear, and `initiated_at` is always present."
* "The amount can shift between an initial card authorization and final clearing." (There is **no**
  authorized-amount vs settled-amount pair in the schema; `amount` is described as "Settled amount in account
  currency" even while `status` is `pending`.)
* "Failed transactions - insufficient funds, a returned ACH, a declined card - remain queryable for audit
  purposes."
* `awaiting_approval`: "held pending action on your side - a payment waiting on an approver, or a debit waiting
  on your authorization - and **no funds have moved** while it sits in that state." No approver identity,
  approval deadline, or approval-step field is exposed.
* `posted_at` semantics, quoted in full because they are unusually hedged:
  "`posted_at` is nullable, and the contract describes it as null while the status is pending. Beyond that it
  is not coupled to `status`: `v1` does **not** guarantee that a failed transaction has an empty `posted_at`,
  so read the field as nullable whatever the status. Nor does `v1` guarantee a **transition order**, so
  reconcile on the `status` and timestamps a response actually carries rather than on an assumed progression."

So: no state machine is promised. A client may observe `settled` → something else, or a `failed` row with a
`posted_at`, and neither is a contract violation.

### 4.3 Counterparty, annotations, attribution, tracing

| Field | Rho's description | Nullability |
| --- | --- | --- |
| `counterparty_name` | "The merchant, or the other side of the money movement. **Always present, though it can be an empty string.**" | required, non-null, possibly `""` |
| `counterparty_logo_url` | "A logo for the counterparty when Rho has one on file. Null otherwise." | nullable, `uri` format |
| `memo` | "Original text describing the transaction, supplied by a bank or payment provider or generated by Rho. Unlike `note`, it is **not user-editable**. Omitted when unavailable." | optional / nullable |
| `note` | "A user or system annotation on the transaction. Omitted when unset." Editable in Rho. | optional / nullable |
| `user_id` | "The user the transaction is attributed to. **Null for system-initiated activity such as interest.**" | nullable, uuid |
| `user_full_name` | Denormalized display name; null for the same system-initiated activity. | nullable |
| `card_id` | "The card the spend was made on. **Null for every non-card transaction type.**" | nullable, uuid |
| `card_name` | Card display name. Card transactions only. | nullable |
| `tracking_number` | "The payment network identifier for tracing an outbound transaction: an ACH **NACHA trace number**, or a wire **IMAD/OMAD**. **MT103 reference numbers are not returned.** Null for transaction types that carry no network identifier." | nullable |
| `account_name` | "That account's display name, denormalized onto the record so reconciliation rarely needs a second call to Accounts." | **required** on a transaction |

`search` matches free text "across `counterparty_name`, `memo`, and `note`, so a single query covers all
three". No per-field search, no exact-match counterparty filter, no wildcard/operator syntax documented, and
no statement of whether search is case-insensitive, prefix, substring, or tokenized.

**Note the asymmetry:** `Transaction.account_name` is required and non-null, while `Account.account_name` on
the Accounts resource is optional and nullable. Two representations of the same attribute disagree on
nullability across resources.

### 4.4 `transaction_type`: all 33 enum values

Grouped for readability; the enum order below is the spec's own order.

| # | Value | Family |
| --- | --- | --- |
| 1 | `card_credit` | Card |
| 2 | `card_debit` | Card |
| 3 | `card_refund` | Card |
| 4 | `credit_repayment` | Credit line |
| 5 | `credit_repayment_refund` | Credit line |
| 6 | `credit_cashback` | Credit line |
| 7 | `ach_credit` | ACH |
| 8 | `ach_debit` | ACH |
| 9 | `ach_return` | ACH |
| 10 | `wire_in` | Domestic wire |
| 11 | `wire_out` | Domestic wire |
| 12 | `wire_fee` | Domestic wire |
| 13 | `international_wire_in` | International wire |
| 14 | `international_wire_out` | International wire |
| 15 | `check_deposit` | Check |
| 16 | `check_payment` | Check |
| 17 | `internal_transfer` | Internal |
| 18 | `savings_deposit` | Savings |
| 19 | `savings_withdrawal` | Savings |
| 20 | `savings_interest` | Savings |
| 21 | `treasury_deposit` | Treasury |
| 22 | `treasury_withdrawal` | Treasury |
| 23 | `treasury_fee` | Treasury |
| 24 | `treasury_interest` | Treasury |
| 25 | `treasury_maturity` | Treasury |
| 26 | `treasury_sale` | Treasury |
| 27 | `treasury_market_value_adjustment` | Treasury |
| 28 | `rewards_accrual` | Rewards |
| 29 | `rewards_cashback_redemption` | Rewards |
| 30 | `adjustment_credit` | Adjustment |
| 31 | `adjustment_debit` | Adjustment |
| 32 | `international_wire_fee` | International wire |
| 33 | `international_wire_fee_refund` | International wire |

Structural observations:

* Values 32 and 33 are appended **after** the adjustment pair rather than next to values 13-14, which is the
  fingerprint of an additive enum extension shipped into `v1` after the original list (consistent with the
  stated "a new enum value" non-breaking policy).
* There is **no** `international_wire_return`, no `check_return`, no `wire_return`, and no `card_dispute` /
  `chargeback` value. The guide states this explicitly for disputes: "A refund or credit is not by itself a
  dispute - `v1` exposes **no dispute indicator**."
* There is no `fee` value for the standard 1% foreign-currency transfer fee that Rho's marketing describes;
  the only fee values are `wire_fee`, `treasury_fee`, `international_wire_fee`
  (+`international_wire_fee_refund`).
* There is no `bill_pay_*` family despite Bill Pay being a headline product; bill payments presumably surface
  as `ach_debit` / `check_payment` / `wire_out` without any product attribution field.
* There is no `invoicing_*` / receivable family despite the Invoicing resource existing in the same API.
* `credit_cashback` (credit-line family) and `rewards_accrual` / `rewards_cashback_redemption` (rewards family)
  are distinct; the corpus never explains when cashback lands as which.

`transaction_type` is a **flat enum, not a (rail, direction) pair**. Direction must be inferred from the sign
of `amount.amount` or from the value name.

### 4.5 `GET /transactions` (ListTransactions)

Returns a paginated list of transactions. Scope: `transactions:read`.

Query parameters (16 total). Array parameters are repeatable; "Repeat a parameter to match any of its values"
(OR within a parameter). Different parameters are AND-composed.

| Param | Type | Format | Default | Enum / constraint | Semantics |
| --- | --- | --- | --- | --- | --- |
| `account_id` | array of string | `uuid` | n/a | n/a | Filter by one or more accounts |
| `account_type` | array of string | n/a | n/a | `checking`, `credit`, `investment`, `savings`, `rewards` | Filter by account type |
| `transaction_type` | array of string | n/a | n/a | the 33 values in §4.4 | Filter by transaction type |
| `status` | array of string | n/a | n/a | `pending`, `settled`, `failed`, `awaiting_approval` | Filter by transaction status |
| `user_id` | array of string | `uuid` | n/a | n/a | "Filter by initiating user"; accepts repeats so one call can cover several employees |
| `card_id` | array of string | `uuid` | n/a | n/a | Filter by one or more cards |
| `search` | string | n/a | n/a | n/a | Free-text across `counterparty_name`, `memo`, `note` |
| `initiated_after` | string | `date-time` | n/a | n/a | Earliest `initiated_at`, **inclusive** |
| `initiated_before` | string | `date-time` | n/a | n/a | Latest `initiated_at`, **exclusive** |
| `posted_after` | string | `date-time` | n/a | n/a | Earliest `posted_at`, **inclusive** |
| `posted_before` | string | `date-time` | n/a | n/a | Latest `posted_at`, **exclusive** |
| `min_amount` | integer | n/a | n/a | n/a | Minimum amount in minor units; "currency is implicit from the queried account" |
| `max_amount` | integer | n/a | n/a | n/a | Maximum amount in minor units; same currency note |
| `sort_by` | string | n/a | **`"initiated_at"`** | Enum: `initiated_at`, `posted_at`, `amount` | Sort field |
| `order` | string | n/a | **`"desc"`** | Enum: `asc`, `desc` | Sort direction |
| `page_size` | integer | n/a | **`20`** | `[1 .. 100]` | |
| `page_token` | string | n/a | n/a | n/a | Opaque cursor |

Half-open interval convention (`after` inclusive, `before` exclusive) is consistent across both date pairs,
which makes `posted_after=D&posted_before=D+1` a clean accounting day. Rho's own reconciliation example:

```bash
curl 'https://rhoapi.rho.co/api/v1/transactions?status=settled&posted_after=2026-05-21T00:00:00Z&posted_before=2026-05-22T00:00:00Z&page_size=100' \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

Filters that do **not** exist: `money_movement_id` (you cannot retrieve the other legs of a movement by its
movement id, so you must page the window and group client-side), `counterparty_name` exact match, `currency`,
`has_attachments`, `memo`/`note` presence, `tracking_number`, `updated_after` (there is no change-feed or
delta cursor at all), and any merchant-category filter.

Sign semantics interact badly with `min_amount`/`max_amount`: `amount.amount` is **signed** (negative =
debit), so "transactions over $100" requires two queries or client-side filtering, and Rho never documents
whether the min/max comparison is on the signed value or its magnitude.

Response `200` body. The `Transaction` object has **20 properties** (confirmed by "Show 20 array
properties"):

| # | Field | Type | Format | Required | Nullable | Meaning |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | string | uuid | yes | no | Global transaction identifier. Not guaranteed unique per row. |
| 2 | `money_movement_id` | string | uuid | yes | no | Shared by all entries of one money movement. |
| 3 | `account_id` | string | uuid | yes | no | Account the event posted against. |
| 4 | `account_type` | string enum | n/a | yes | no | `checking`/`credit`/`investment`/`savings`/`rewards` |
| 5 | `initiated_at` | string | date-time | yes | no | When the event was created. Always present. |
| 6 | `posted_at` | string | date-time | **no** | **yes** | When the event cleared the ledger. "Null while status is pending." |
| 7 | `transaction_type` | string enum | n/a | yes | no | 33 values, §4.4 |
| 8 | `status` | string enum | n/a | yes | no | `pending`/`settled`/`failed`/`awaiting_approval` |
| 9 | `amount` | `Money` | n/a | yes | no | "Settled amount in account currency"; signed integer minor units |
| 9a | `amount.amount` | integer | n/a | yes | no | Negative = debit |
| 9b | `amount.currency` | string | n/a | yes | no | ISO 4217 |
| 10 | `account_name` | string | n/a | yes | no | Denormalized account display name |
| 11 | `counterparty_name` | string | n/a | yes | no | Merchant or other side; may be `""` |
| 12 | `counterparty_logo_url` | string | uri | no | yes | Logo when Rho has one on file |
| 13 | `note` | string | n/a | no | yes | User-added text in Rho. **Editable.** Omitted when unset. |
| 14 | `memo` | string | n/a | no | yes | Text that arrived with the transaction (bank / provider / Rho-generated). **Read-only.** Omitted when unset. |
| 15 | `user_id` | string | uuid | no | yes | Null for system-initiated transactions (interest, etc.) |
| 16 | `user_full_name` | string | n/a | no | yes | Same nullability as `user_id` |
| 17 | `card_id` | string | uuid | no | yes | Card transactions only; null for all other transaction types |
| 18 | `card_name` | string | n/a | no | yes | Card transactions only |
| 19 | `tracking_number` | string | n/a | no | yes | ACH NACHA trace number or wire IMAD/OMAD. MT103 not returned. |
| 20 | `attachments` | array of `TransactionAttachment` | n/a | **yes** | no | Empty array when no files. Stable descriptors; signed URLs resolved on demand. |

Plus the envelope `page.next_page_token`.

Errors: `400`, `401`, `403`, `429`, `500`, `503`. No `404`.

### 4.6 `GET /transactions/{id}` (GetTransaction)

Returns a single transaction by its global identifier. Scope: `transactions:read`.

| Param | In | Type | Format | Required | Meaning |
| --- | --- | --- | --- | --- | --- |
| `id` | path | string | uuid | yes | Transaction identifier |
| `account_id` | query | string | uuid | **no** | "Account ID for the transaction" |

Response `200`: the same 20-property `Transaction`, unwrapped.

Errors: `400`, `401`, `403`, `404`, `429`, `500`, `503`.

**The single most under-documented thing in the core API.** Because `id` is explicitly "not guaranteed unique
per row", `GET /transactions/{id}` is an inherently ambiguous lookup, and the optional `account_id` query
parameter is evidently the disambiguator, but the reference describes it only as "Account ID for the
transaction" and neither guide mentions it at all. Never stated:

* what the endpoint returns when an `id` matches multiple entries and `account_id` is omitted (first match?
  arbitrary leg? `400`? a list?);
* whether `account_id` is required in that case;
* whether passing an `account_id` that does not match the transaction gives `404` or `400`;
* whether the `id` collision is a real production condition or only a theoretical one.

### 4.7 `GET /transactions/{transaction_id}/files/{file_id}` (GetTransactionFile)

"Returns file metadata and a fresh, short-lived signed download URL." Scope: `transactions:read`.

| Param | In | Type | Format | Required | Meaning |
| --- | --- | --- | --- | --- | --- |
| `transaction_id` | path | string | uuid | yes | "Transaction identifier returned in the transaction `id` field" |
| `file_id` | path | string | uuid | yes | "Stable identifier from `transaction.attachments[].file_id`" |

Response `200`:

| Field | Type | Format | Required | Meaning |
| --- | --- | --- | --- | --- |
| `file_id` | string | uuid | yes | Stable attachment identifier |
| `file_name` | string | n/a | yes | Original file name |
| `download_url` | string | uri | yes | Fresh, short-lived signed download URL |

Errors: `400`, `401`, `403`, `404`, `429`, `500`, `503`.

Attachment semantics, quoted from the Transactions guide:

* "Transaction responses contain stable attachment metadata but **never signed URLs**. Request a fresh,
  short-lived URL only when the file is needed."
* "each request to this endpoint issues a fresh, short-lived link. **Follow it straight away, without an
  Authorization header**, and request another one whenever a new URL is needed instead of reusing or
  persisting the last."
* "Set `{transaction_id}` to the transaction's `id`, and `{file_id}` to an `attachments[].file_id` value.
  A transaction `id` identifies one transaction."
* "Sandbox downloads contain non-empty representative fictional documents, but their contents are **not
  guaranteed to reproduce every field of the transaction fixture**."

**Contradiction #6.** The file endpoint's own guidance says "A transaction `id` identifies one transaction",
which directly contradicts the same document's `id` definition ("not guaranteed unique per row - the entries
of one money movement can share an `id`") and the whole idempotent-ingestion section. The file endpoint also
has **no `account_id` disambiguator**, unlike `GET /transactions/{id}`, so if ids can collide the file lookup
has no way to say which leg it means.

**Not stated about attachments/files:**

* the actual TTL of `download_url`. The Statements guide commits to a number ("valid for up to **15 minutes**")
  for `pdf_url`; the transaction file endpoint says only "short-lived" and never quantifies it.
* whether the signed URL is single-use or re-fetchable within its TTL.
* the file's MIME type, size, upload time, or uploader.
* whether `file_id` is globally unique or unique only within a transaction (see the observed counter-example in
  §4.8 note 5).
* any limit on attachment count or size per transaction.
* any way to **list** files, or to upload/delete one. The API is read-only.

### 4.8 Transactions: documented vs observed (sandbox `transactions.json`, 20 rows, page 1 of ≥2)

Key presence across the 20 captured rows:

| Field | Schema | Rows present | Rows absent |
| --- | --- | --- | --- |
| `id`, `money_movement_id`, `account_id`, `account_type`, `initiated_at`, `transaction_type`, `status`, `amount`, `account_name`, `counterparty_name`, `attachments` | required | 20 | 0 |
| `posted_at` | optional, nullable | **20** | 0 |
| `user_id`, `user_full_name` | optional, nullable | 13 | 7 |
| `card_id`, `card_name` | optional, nullable | 11 | 9 |
| `memo` | optional, nullable | 8 | 12 |
| `note` | optional, nullable | 8 | 12 |
| `counterparty_logo_url` | optional, nullable | **0** | 20 |
| `tracking_number` | optional, nullable | **0** | 20 |

* **Fields documented but never observed:** `counterparty_logo_url`, `tracking_number`.
  `tracking_number` in particular is unverifiable: the sandbox page contains no ACH-out, wire, or other
  outbound-rail transaction that would carry one.
* **Fields observed but not documented:** none. The sandbox emits no undocumented keys.
* **Null is never used.** Every optional field is either present with a value or **absent from the JSON
  object**. Not a single `null` appears anywhere in `transactions.json`. The schema types these as
  "string or null"; the wire format uses omission. Clients must treat absent and null as equivalent.

Observed distributions:

| Dimension | Counts |
| --- | --- |
| `status` | `settled` 17, `pending` 2, `failed` 1. **`awaiting_approval` never exercised.** |
| `transaction_type` | `card_debit` 8, `credit_repayment` 6, `card_refund` 3, `rewards_cashback_redemption` 1, `ach_credit` 1, `check_payment` 1. **27 of 33 enum values never exercised** (no ACH debit/return, no wire of any kind, no check deposit, no internal transfer, no savings or treasury activity, no adjustments, no `rewards_accrual`, no `credit_cashback`). |
| `account_type` | `credit` 14, `checking` 5, `rewards` 1. No `savings`, no `investment`. |
| `attachments` length | 1 file on 12 rows, 0 files on 6 rows, 2 files on 2 rows. |

**Mismatch A. `posted_at` is populated on `pending` and `failed` rows.** The contract says "Null while status
is pending". Observed:

| `id` | `status` | `transaction_type` | `amount` | `initiated_at` | `posted_at` |
| --- | --- | --- | --- | --- | --- |
| `019ef508-2808-7000-8000-000000000006` | `pending` | `card_debit` | -45 000 | 2026-06-23T15:10:13Z | **2026-06-23T15:10:13Z** |
| `019ef37e-4418-7000-8000-000000000001` | `pending` | `card_debit` | -4 947 | 2026-06-23T07:59:59Z | **2026-06-23T07:59:59Z** |
| `019eda73-2218-7000-8000-000000000012` | `failed` | `check_payment` | -339 100 | 2026-06-18T11:17:19Z | **2026-06-18T11:17:19Z** |

In each case `posted_at == initiated_at` exactly. Either the sandbox fixture is wrong, or (more likely, given
how carefully the guide hedges) the real rule is the hedged one: "read the field as nullable whatever the
status" and do not infer settlement from a non-null `posted_at`. **A client that treats `posted_at != null` as
"posted" will wrongly count a pending authorization and a failed check as cleared.** This is the single most
consequential doc/reality gap in the core API.

**Mismatch B. `money_movement_id` groups legs, but the legs do NOT share an `id`.** The guide's warning is
that "the entries of one money movement can share an `id`". In the sandbox, all three multi-leg movements have
**distinct** ids per leg:

| `money_movement_id` | Legs (`id` tail, `account_id` tail, signed amount, type) |
| --- | --- |
| `40000000-…-000000000002` | `…0003` on acct `…0007` +1 750 `credit_repayment`; `…0002` on acct `…0002` -1 750 `credit_repayment` |
| `40000000-…-000000000003` | `019efe24-c860-…0004` on acct `…0009` +1 658 253; `019efe24-c478-…0005` on acct `…0003` -1 658 253 |
| `40000000-…-000000000006` | `…0009` on acct `…0009` +144 827; `…0008` on acct `…0003` -144 827 |

Both legs of each movement carry identical `memo`/`note` text and identical `posted_at`, and their amounts sum
to zero. The shared-`id` case the documentation warns about is **never demonstrated** anywhere in the corpus,
so the failure mode Rho tells integrators to guard against cannot be reproduced or tested against the sandbox.
Note also that leg ids are not even lexically adjacent in one case (`019efe24-c860-…` vs `019efe24-c478-…`),
and `initiated_at` differs by a second between the legs (09:38:04Z vs 09:38:03Z) while `posted_at` is
identical.

**Mismatch C. `memo` and `note` are identical strings on every row that has them.** All 8 rows carrying
annotations have `memo == note` (`"Daily credit repayment for date 2026/06/24"`, `"Rewards cashback"`,
`"Monthly office rent"`). The documented distinction (`memo` = read-only, arrived with the transaction;
`note` = user-editable annotation in Rho) is therefore **not exercised by the sandbox at all**, and no fixture
shows a user-authored note distinct from the bank memo. The 12 card transactions carry neither field.

**Mismatch D. Id format.** Transaction `id`s are **UUIDv7** (`019f0554-0bf0-7000-…`, `019ef37e-4418-7000-…`);
the leading 48 bits are a millisecond timestamp, and they sort in the same order as `initiated_at`. Every other
id in the sandbox is a **UUIDv4-shaped synthetic constant** (`10000000-0000-4000-8000-…` users,
`20000000-…` cards, `30000000-…` accounts, `40000000-…` money movements). The versioning doc explicitly tells
clients to "**Treat IDs as opaque strings**. Do not parse structure out of an `id`", worth heeding, since the
transaction id genuinely does encode a timestamp today.

**Mismatch E. One `file_id` is attached to two different transactions.**
`file_id cdc328c1-c3a3-4670-a371-28e34891ee68` / `credit-repayment-receipt.pdf` appears on **both**
`019f0143-3ea0-7000-8000-000000000002` (checking account `…0002`) and
`019ef6d6-73b0-7000-8000-000000000009` (credit account `…0009`), two transactions in two different money
movements (`…0002` and `…0006`). So `file_id` is **not** a per-transaction identifier; the same stored file is
referenced from multiple transactions, and `GET /transactions/{transaction_id}/files/{file_id}` is genuinely a
two-part key. The documentation calls `file_id` a "stable attachment identifier" and never says it can be
shared across transactions. All other 11 distinct file ids appear once each.

**Mismatch F. Default sort confirmed.** The 20 rows are strictly descending by `initiated_at`
(2026-06-26T19:07:02Z down to 2026-06-13T00:45:30Z), matching the HTML-only documented defaults
`sort_by=initiated_at`, `order=desc`. The page holds exactly 20 items, matching the HTML-only default
`page_size=20`, and `next_page_token` is non-null so more pages exist.

**Sign convention, observed:** debits negative, credits positive, consistently.
`card_debit` always negative; `card_refund` always **positive** (+228 073, +39 109, +3 475);
`credit_repayment` positive on the `credit` account and negative on the `checking` account (the credit
balance is being paid down while cash leaves);
`rewards_cashback_redemption` -108 403 on the `rewards` account paired with `ach_credit` +108 403 on
`checking`. Note that those two legs carry **different** `money_movement_id`s (`…0010` and `…0008`), so the
rewards-out and cash-in legs of the same economic event are **not** grouped by `money_movement_id` in this
fixture. A client grouping on `money_movement_id` to net out internal movements would not net this one.

Also: the `ach_credit` rewards-cashback row is attributed to a user (`user_id 10000000-…0005`,
`"Olivia Chen"`) even though it is plainly system-generated, while the `rewards_cashback_redemption` leg has
no user attribution at all. That undercuts the guide's framing that `user_id` is "Null for system-initiated
activity such as interest".

### 4.9 Workflow recipes Rho publishes

| Goal | Rho's prescription |
| --- | --- |
| Daily reconciliation | `posted_after`/`posted_before` on the accounting-day boundaries + `status=settled` + `page_size=100`, follow cursor to `next_page_token: null` |
| Card refunds and credits | `transaction_type=card_refund` and `transaction_type=card_credit` against the `account_type=credit` slice. "A refund or credit is not by itself a dispute - `v1` exposes no dispute indicator." |
| Spend per employee | `user_id=<uuid>&transaction_type=card_debit&posted_after=…&page_size=100`; `user_id` accepts repeats; substitute `card_id` to scope by card |
| Idempotent ingestion | Key on `(id, account_id)` **or** group on `money_movement_id`; never on `id` alone |
| Balance snapshot | `GET /accounts?page_size=100`, filter `account_type` client-side |
| Join account details | Use the denormalized `account_id`/`account_type`/`account_name` on the transaction; fetch `/accounts/{id}` once and cache "for the duration of the job" |

---

## 5. Cards

### 5.1 Scope and framing

"The Cards API exposes the physical and virtual cards belonging to the business linked to your API Access
Token. **Both endpoints require the `cards:read` scope**."

"An unfiltered list includes **canceled and expired cards** so their stable IDs can still be joined to
historical transactions." This is the API's answer to the "how do canceled cards behave" question: they are
never removed from the API, their `id` remains valid and joinable to `Transaction.card_id` forever, and
`GET /cards/{id}` continues to resolve them. To exclude them you must pass an explicit `status` filter.

Security posture: "**Only the last four PAN digits are returned; full card numbers, CVCs, and expiration dates
are not available through these endpoints.**" There is no `expires_at` / `exp_month` / `exp_year` field on the
Card object at all; the closest is `usage_ends_at`, which is a usage-window control, not the PAN expiry.

### 5.2 `GET /cards` (ListCards)

Scope: `cards:read`.

| Param | Type | Format | Default | Enum / constraint | Semantics |
| --- | --- | --- | --- | --- | --- |
| `user_id` | array of string | `uuid` | n/a | n/a | Filter by one or more cardholder user IDs |
| `type` | array of string | n/a | n/a | `physical`, `virtual` (`CardType`) | Filter by one or more card types |
| `status` | array of string | n/a | n/a | the 11 `CardStatus` values, §5.4 | Filter by one or more card lifecycle statuses |
| `page_size` | integer | n/a | **`20`** | `[1 .. 100]` | |
| `page_token` | string | n/a | n/a | n/a | Opaque cursor; omit for the first page |

"Repeat a parameter to match any of its values. Different filters are combined, so a request with
`type=virtual&status=active` returns cards that match both." Same OR-within / AND-across semantics as
transactions.

**ListCards has no `sort_by` and no `order`**, unlike ListAccounts and ListTransactions. Card ordering is
therefore neither configurable nor documented. (Observed: the 8 sandbox cards come back in ascending `id`
order, `20000000-…0001` through `…0008`.) There is also no `search`, no date filter, no
`spending_limit_type` filter, and no filter for cards with merchant controls.

Response `200`: `{ "cards": [Card…], "page": { "next_page_token": … } }`. The `Card` object has
**20 properties**.

Errors: `400`, `401`, `403`, `429`, `500`, `503`.

### 5.3 `GET /cards/{id}` (GetCard)

Scope: `cards:read`. Path param `id`, string, `uuid`, required, "Stable global card identifier."
No query parameters. "It uses the same Card object as the list endpoint."
"The endpoint returns `404` when the card does not exist **or belongs to another business**."

Errors: `400`, `401`, `403`, `404`, `429`, `500`, `503`.

### 5.4 The `Card` object: all 20 properties

| # | Field | Type | Format / pattern | Required | Nullable | Meaning |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | string | uuid | yes | no | Stable global card identifier **referenced by transactions** (`Transaction.card_id`) |
| 2 | `name` | string | n/a | yes | no | **User-editable** name assigned to the card |
| 3 | `last_4` | string | `^[0-9]{4}$` | yes | no | Last four PAN digits, **including leading zeroes** (hence string, not integer) |
| 4 | `type` | string enum | `CardType` | yes | no | `physical` \| `virtual` |
| 5 | `status` | string enum | `CardStatus` | yes | no | 11 values, below |
| 6 | `cardholder` | `Cardholder` | n/a | yes | no | `{user_id, first_name, last_name}` |
| 7 | `spending_limit` | `Money` or null | n/a | yes | **yes** | Configured limit; null when the card has no limit |
| 8 | `spending_limit_type` | string enum or null | `CardSpendingLimitType` | yes | **yes** | 7 values, below; null when the card has no limit |
| 9 | `current_spend` | `Money` or null | n/a | yes | **yes** | **Pending plus settled** spend in the current limit window; null when no limit or unavailable |
| 10 | `pending_spend` | `Money` or null | n/a | yes | **yes** | Pending portion of `current_spend`; null when `current_spend` is null or the pending breakdown is unavailable |
| 11 | `spend_period_start` | string or null | date-time | yes | **yes** | Start of the current window, computed in **America/New_York**. Null when unavailable. For `fixed` and `single_use` this is when the lifetime total began. |
| 12 | `spend_period_end` | string or null | date-time | yes | **yes** | **Exclusive** end of the current window, America/New_York. Null when the limit does not reset (`fixed`, `single_use`), when `current_spend` is null, or when the window could not be determined. |
| 13 | `usage_starts_at` | string or null | date-time | yes | **yes** | Earliest time the card may be used; null when unrestricted |
| 14 | `usage_ends_at` | string or null | date-time | yes | **yes** | Latest time the card may be used; null when unrestricted |
| 15 | `billing_address` | `Address` or null | n/a | yes | **yes** | Billing address used for card verification |
| 16 | `shipping_address` | `Address` or null | n/a | yes | **yes** | Physical-card delivery address; **null for virtual cards** or when not recorded |
| 17 | `blocked_categories` | array of `MerchantCategory` | n/a | **no** | no | Categories declined at authorization. **Present only for a block list.** |
| 18 | `allowed_categories` | array of `MerchantCategory` | n/a | **no** | no | Only categories permitted at authorization. **Present only for an allow list.** |
| 19 | `blocked_merchants` | array of `Merchant` | n/a | **no** | no | Merchants declined at authorization. **Present only for a block list.** |
| 20 | `allowed_merchants` | array of `Merchant` | n/a | **no** | no | Only merchants permitted at authorization. **Present only for an allow list.** |

`CardStatus`, 11 values in spec order:
`printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `active`, `expiring`,
`locked`, `canceled`, `suspended`, `expired`.

The first five are physical-fulfilment states (`activate_card` reads as an imperative, i.e. "delivered,
awaiting activation"); `active`/`expiring` are usable states; `locked`/`suspended`/`canceled`/`expired` are
not-usable states. **Rho never documents the difference between `locked` and `suspended`**, nor which
transitions are possible, nor which statuses are reachable for a `virtual` card. From the help centre (product
behaviour, not contract): `locked` is the user-toggled Lock Card / Unlock Card state and is reversible;
`canceled` is terminal ("Once you've canceled your Rho Card, it cannot be reactivated", and the card "will be
deleted and no longer display on the My Cards page" in the UI, while remaining visible in the API);
a fixed-limit card "will automatically lock" once its transactions fully settle, which explains a `locked`
status that no human set. `suspended` has no help-centre counterpart and is presumably issuer- or
risk-initiated.

`CardSpendingLimitType`, 7 values, with Rho's exact reset semantics:

| Value | Reset behaviour | `spend_period_end` |
| --- | --- | --- |
| `daily` | Resets on Eastern Time (America/New_York) calendar boundary | non-null |
| `weekly` | Resets on ET calendar boundary | non-null |
| `monthly` | Resets on ET calendar boundary | non-null |
| `quarterly` | Resets on ET calendar boundary | non-null |
| `annual` | Resets on **the anniversary of when the limit took effect, not on a calendar boundary** | non-null |
| `fixed` | "a lifetime ceiling that does not reset" | **null** |
| `single_use` | "spent after one use" | **null** |

"High utilization means the next charge can decline." Enum order in the spec is
`fixed`, `monthly`, `single_use`, `annual`, `daily`, `weekly`, `quarterly`, again suggesting
`daily`/`weekly`/`quarterly` were added after the original three (`fixed`, `monthly`, `single_use`, `annual`).

Merchant controls: "Merchant controls use **either** the `blocked_*` fields **or** the `allowed_*` fields,
**never both**." Categories are ISO 18245 MCCs with a human-readable name when available; merchants are
identified by human-readable name only. The block/allow choice is expressed purely by **which keys are present
in the payload**. There is no explicit `control_mode: allow|block` discriminator, so a client must infer mode
from key presence, and "no controls at all" is indistinguishable in shape from "an empty allow list" would be
except that all four keys are simply absent.

**No card field exists for:** PAN, CVC, expiry date, issuer/network (Mastercard, per Rho's disclosures),
created_at, last-used-at, the account or credit line the card draws on (there is **no `account_id` on a
Card**, so you can only connect a card to an account via transactions), digital-wallet provisioning state,
replacement/predecessor card id (relevant since expiry auto-reissues a new card with a new number), or
department/label/accounting-code metadata that the Rho UI clearly supports.

### 5.5 Cards: documented vs observed (sandbox `cards.json`, 8 cards, `next_page_token: null`)

All 16 required keys are present on all 8 cards. The 4 optional control arrays appear on exactly one card each.

| Card `id` tail | `name` | `type` | `status` | limit type | `spending_limit` | `current_spend` | `pending_spend` | `spend_period_start` | `spend_period_end` | `usage_starts_at` | `usage_ends_at` | `shipping_address` | control keys |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `…0001` | Ethan Parker | virtual | active | monthly | 500 000 | 6 797 | 1 500 | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z | 2025-10-01T09:00:00Z | **2026-09-01T00:00:00Z** | null | `blocked_categories`, `blocked_merchants` |
| `…0002` | Maya Thompson | physical | active | monthly | 100 000 | 45 000 | 8 000 | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z | null | null | present | `allowed_categories`, `allowed_merchants` |
| `…0003` | Daniel Rivera | virtual | active | monthly | 250 000 | 1 750 | 250 | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z | null | null | null | none |
| `…0004` | Lucas Bennett | physical | **locked** | **daily** | 75 000 | 6 331 | 900 | 2026-09-09T04:00:00Z | 2026-09-10T04:00:00Z | null | null | present | none |
| `…0005` | Sofia Martin Physical Card | physical | active | monthly | 200 000 | 5 331 | 400 | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z | null | null | present | none |
| `…0006` | Hannah Brooks | virtual | **suspended** | monthly | 2 500 000 | 1 622 132 | 50 000 | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z | null | null | null | none |
| `…0007` | Emma Walsh Virtual Card | virtual | **canceled** | monthly | 150 000 | 121 827 | 0 | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z | null | 2026-06-30T23:59:59Z | null | none |
| `…0008` | Claire Mitchell | physical | **expired** | **fixed** | 500 000 | 0 | 0 | 2025-03-01T12:00:00Z | **null** | null | 2026-06-30T23:59:59Z | present | none |

Observations and mismatches:

1. **The documented null-vs-omitted contract holds exactly for cards.** All 16 required keys are always
   present; the nullable ones (`usage_starts_at`, `usage_ends_at`, `shipping_address`, `spend_period_end`) are
   emitted as **explicit `null`**, unlike accounts and transactions, where optional keys are omitted. So the
   API uses **both** conventions, split by whether the field is `required` in the schema: required+nullable →
   explicit `null`; optional → key omitted. That rule is never stated anywhere, but it is consistent across all
   three resources in the capture, and it is the single most useful deserialization rule in this document.
2. **`spend_period_end: null` on the `fixed` card** (`…0008`) matches the documented rule exactly; its
   `spend_period_start` `2025-03-01T12:00:00Z` is "when the lifetime total began". Note the `12:00:00Z` time,
   which is **not** an ET midnight boundary, unlike every other card.
3. **All `monthly` windows are `2026-09-01T04:00:00Z` → `2026-10-01T04:00:00Z`** and the `daily` window is
   `2026-09-09T04:00:00Z` → `2026-09-10T04:00:00Z`. `04:00Z` is midnight EDT, confirming the documented
   America/New_York computation (and confirming these are EDT, not EST, dates; an EST window would be
   `05:00:00Z`, which the corpus never demonstrates and which a naive client hard-coding `-04:00` would break
   on after the November DST change).
4. `spending_limit_type` is **never null** and `spending_limit` is **never null** in the sandbox, so the
   documented "no limit" card (both null, plus `current_spend`/`pending_spend`/`spend_period_*` null) is
   **never exercised**. Nor are `weekly`, `quarterly`, `annual`, or `single_use`: only `monthly` (6), `daily`
   (1), `fixed` (1) appear. 4 of 7 limit types unobserved.
5. **Statuses observed:** `active` 4, `locked` 1, `suspended` 1, `canceled` 1, `expired` 1.
   **6 of 11 never exercised**: `printing`, `shipped`, `out_for_delivery`, `activate_card`,
   `delivery_canceled`, `expiring`.
6. **Contradiction #7. A card with an elapsed usage window is still `active`.** Card `…0001` has
   `usage_ends_at: 2026-09-01T00:00:00Z`, ten days before the capture (2026-09-11), `status: "active"`, and a
   live spend window running to 2026-10-01. The corpus never says whether `status` reflects the usage window;
   evidently it does not, so **`status == "active"` is not sufficient to conclude a card is usable**: a client
   must also check `usage_starts_at`/`usage_ends_at` against now.
7. **Contradiction #8. `current_spend` and `pending_spend` do not reconcile against the transaction
   fixture.** `current_spend` is defined as "pending plus settled spend in the current limit window", and the
   windows above all start 2026-09-01, yet every card transaction in `transactions.json` is dated June 2026.
   Card-by-card:
   * `…0001` Ethan Parker: `current_spend` 6 797 = 4 947 + 1 850, the exact sum of his two June `card_debit`s,
     one `pending` and one `settled`. But `pending_spend` is 1 500, which matches **neither** (the pending one
     is 4 947).
   * `…0002` Maya Thompson: `current_spend` 45 000 = her single **pending** -45 000 `card_debit`, yet
     `pending_spend` is 8 000.
   * `…0003` Daniel Rivera: `current_spend` 1 750 = his single **settled** debit, yet `pending_spend` is 250.
   * `…0004` Lucas Bennett: 6 331 = his single settled debit; `pending_spend` 900.
   * `…0005` Sofia Martin: 5 331 = her single settled debit; `pending_spend` 400.
   * `…0006` Hannah Brooks: 1 622 132 = her single settled debit; `pending_spend` 50 000.
   * `…0007` Emma Walsh: 121 827 = her single settled debit; `pending_spend` 0.
   * `…0008` Claire Mitchell: `current_spend` 0, although three `card_refund` rows (+228 073, +39 109, +3 475)
     are attributed to her card, consistent with refunds not reducing spend below zero, or with refunds being
     excluded from `current_spend` entirely. Rho never says whether refunds net against `current_spend`.

   So: `current_spend` tracks the sum of all that card's transactions **regardless of the stated window**, and
   `pending_spend` is a free-standing fixture value that is **not** the pending subset of `current_spend` on
   any card. Rho's own caveat ("Sandbox downloads … are not guaranteed to reproduce every field of the
   transaction fixture") is about downloaded files, not about these aggregates, so this is an unflagged
   inconsistency. **Do not calibrate a `current_spend`/`pending_spend` implementation against the sandbox.**
8. **Merchant controls, observed shape.** Card `…0001` carries
   `blocked_categories: [{"code":"0742","name":"Veterinary services"}]` and
   `blocked_merchants: [{"name":"Petco"}]`. Card `…0002` carries
   `allowed_categories: [{"code":"5812","name":"Eating places and restaurants"}]` and
   `allowed_merchants: [{"name":"Sweetgreen"}]`. The "never both" rule holds. The other six cards omit all four
   keys. `name` is present on both category entries, so the "when available" caveat is unexercised.
   Note the doc example in `docs_v1_cards.md` uses `"code": "5812", "name": "Eating Places and Restaurants"`
   (title case) while the sandbox returns `"Eating places and restaurants"` (sentence case). The human-readable
   names are not stable casing and should not be used as keys.
9. **Cardholder ids `10000000-…0001` through `…0009` skip nothing but card ids cover only 8**: user
   `…0005` ("Olivia Chen", who appears as the attributed user on the `ach_credit` rewards row) holds **no card**
   in the fixture. Cards and users are therefore not 1:1, and `ListCards(user_id=…)` can legitimately return
   an empty list for a real user.
10. `name` is a free-text, user-editable label: the sandbox uses the cardholder's own name for six cards
    (`"Ethan Parker"`) and a descriptive label for two (`"Sofia Martin Physical Card"`,
    `"Emma Walsh Virtual Card"`). The docs example uses `"Travel card"`. `name` is not a stable identifier and
    is not unique.
11. `last_4` values observed: `0042`, `1846`, `7291`, `6603`, `3150`, `9027`, `1184`, `7732`. The leading-zero
    case (`0042`) is present, justifying the string type and the `^[0-9]{4}$` pattern.

### 5.6 Joining cards to transactions

The only documented join is `Card.id` ↔ `Transaction.card_id` (plus `Cardholder.user_id` ↔
`Transaction.user_id`). Verified in the sandbox: all 11 card-attributed transactions carry a `card_id` that
exists in `cards.json`, and `Transaction.card_name` equals `Card.name` on every one of them, including for the
`canceled` card `…0007` and the `expired` card `…0008`, which is exactly the stated reason canceled and
expired cards stay listed.

There is **no** reverse join: a `Card` has no `account_id`, so "which credit line does this card draw on" is
answerable only by looking at the `account_id` on that card's transactions. In the sandbox all card
transactions post to `credit` accounts (`30000000-…0007`, `…0009`), never to `checking`, consistent with the
Accounts guide's "`credit` = Revolving credit lines backing corporate cards".

---

## 6. Contradictions, gaps, and what is conspicuously not stated

### 6.1 Contradictions found

| # | Contradiction | Where |
| --- | --- | --- |
| 1 | Auth guide lists 3 scopes; OpenAPI security lists 5 (`cards:read`, `invoicing:read` missing from the guide) | `docs_v1_auth.md` vs `api_v1_openapi.md` + Cards guide |
| 2 | Pagination guide promises insert-stable cursors; the sandbox cursor decodes to `offset:20` | `docs_v1_pagination.md` vs `sandbox/transactions.json` |
| 3 | Problem details cited as RFC 9457 in one place, RFC 7807 in another | `api_v1_openapi.md` vs `docs_v1_auth.md` |
| 4 | Account type vocabulary differs between resources: `investment` (Accounts/Transactions) vs `treasury` (Statements) | `docs_v1_accounts.md` vs `docs_v1_statements.md` |
| 5 | Accounts guide says every account carries masked account and routing numbers; 6 of 14 sandbox accounts carry neither | `docs_v1_accounts.md` vs `sandbox/accounts.json` |
| 6 | "A transaction `id` identifies one transaction" vs "`id` … not guaranteed unique per row", in the same document | `docs_v1_transactions.md`, attachments section vs field table |
| 7 | Card `…0001` is `status: active` with `usage_ends_at` ten days in the past | `sandbox/cards.json` |
| 8 | `current_spend` / `pending_spend` do not reconcile with the transaction fixture or with the stated spend window on any of the 8 cards | `sandbox/cards.json` vs `sandbox/transactions.json` |
| 9 | `posted_at` is non-null on both `pending` rows and the `failed` row, against "Null while status is pending" | schema vs `sandbox/transactions.json` |
| 10 | `Transaction.account_name` required and non-null; `Account.account_name` optional and nullable | `transactions_*.md` vs `accounts_*.md` |
| 11 | Getting-started says "Current release is read-only and covers **accounts and transactions**", while the same doc set ships Statements, Cards, and Invoicing | `docs_v1_getting-started.md` vs `api_v1_openapi.md` |
| 12 | The product page describes "a read-only REST API covering accounts, transactions, and statements" and never mentions Cards or Invoicing endpoints | `pages/core/product__api.txt` vs the reference. [Rho claim], as of August 2026 |
| 13 | The OpenAPI summary says the API covers "accounts, cards, **payments**, and the transaction ledger", but there is no payments endpoint in `v1` | `api_v1_openapi.md` |
| 14 | The `.md` operation exports omit `429` on every operation; the rendered reference declares it on every operation | `rho/api/*.md` vs `rho/tmpfetch/html_*.txt` |

### 6.2 Conspicuously not stated

**Write operations.** Nothing. The entire `v1` surface is `GET`. No POST/PATCH/DELETE, no idempotency-key
header, no webhook or event subscription, no push notification. There is no `updated_at` on any object and no
delta/change-feed parameter, so "what changed since my last sync" can only be approximated by re-polling a
date window. And since `posted_at` can be null and `initiated_at` is immutable, a status change from
`pending` to `settled` moves a row into the `posted_*` window only after it posts; a `pending → failed`
transition is invisible to a `posted_*`-windowed poller. Rho's marketing states this positively: "Rho API
access tokens are read-only … Tokens cannot initiate payments or modify accounts" [Rho claim].

**Balances.** No available vs current balance, no pending/held amount, no credit limit or available credit on a
`credit` account, no APR, no minimum payment, no statement balance, no yield/APY on `savings` or `investment`,
no as-of timestamp on `balance` (so you cannot tell how stale a balance is).

**Transaction economics.** No original/foreign currency amount, no FX rate, no FX or cross-border fee field, no
interchange or network data, no MCC on the transaction (MCCs appear only on card controls), no merchant id, no
authorization code, no ARN, no decline reason, no dispute state, no auth-vs-cleared amount pair, no receipt
requirement or compliance status, no department/label/GL-code/accounting-category fields despite Rho's expense
product exposing all of them, and no `is_reversal`/`reverses_transaction_id` link.

**Card fields.** No `account_id`, no PAN/CVC/expiry, no network/issuer, no created/issued date, no
replacement-card linkage, no digital-wallet state, no per-card MCC group names beyond the raw ISO 18245 codes,
no explicit allow/block mode discriminator.

**Operational.** No rate-limit budget headers; no request id; no documented `download_url` TTL for transaction
files (Statements commits to 15 minutes, Transactions says only "short-lived"); no statement of whether the
signed URL is single-use; no maximum for `search` string length; no documented behaviour for `min_amount`/
`max_amount` against signed amounts; no documented behaviour of `GET /transactions/{id}` when `id` is
ambiguous and `account_id` is omitted; no `v0` documentation despite `v0` being referenced; no
`Idempotency-Key`; no sandbox data dictionary or fixture manifest; no published SLA or uptime target.

**Sandbox coverage gaps that matter for implementation.** 27 of 33 `transaction_type` values, 6 of 11
`CardStatus` values, 4 of 7 `CardSpendingLimitType` values, 1 of 5 `AccountType` values (`investment`), the
`awaiting_approval` status, the no-limit card, a non-null `tracking_number`, a non-null
`counterparty_logo_url`, an empty-string `counterparty_name`, a `memo` that differs from its `note`, and the
shared-`id` money-movement case are **all unexercised**. A client cannot verify its handling of any of them
against the sandbox.

### 6.3 Practical implementation rules distilled

1. **Key transactions on `(id, account_id)`**, or group on `money_movement_id`. Never on `id` alone.
2. **Treat absent and `null` as the same thing.** Required+nullable fields come back as explicit `null`
   (cards); optional fields come back **omitted** (accounts, transactions). Handle both everywhere.
3. **Do not infer settlement from `posted_at`.** Read `status`; `posted_at` is populated on `pending` and
   `failed` rows in practice.
4. **Do not infer usability from `status: active`** on a card; check `usage_starts_at`/`usage_ends_at` too.
5. **Give every enum switch a default branch**. Rho ships new enum values into `v1` without a version bump,
   and `transaction_type` shows clear evidence of having been extended already.
6. **Amounts are signed integers in minor units.** Debits negative, credits positive, refunds positive.
7. **Follow the cursor to `next_page_token: null`; never change filters or sort mid-iteration; never persist a
   cursor.**
8. **Fetch file URLs at the moment of download**, follow them **without** an `Authorization` header, and never
   cache them.
9. **Pace below 1 request/second**; there are no budget headers to steer by, and `Retry-After: 0` means
   "back off with jitter", not "retry now".
10. Card spend aggregates (`current_spend`, `pending_spend`) are **not** reproducible from the transaction
    feed in the sandbox; treat them as server-computed opaque values.

---

## 7. As-of dates carried through

| Fact | As-of / date |
| --- | --- |
| API contract version | `1.0.0`, `v1`, stable and additive-only |
| Sandbox responses captured | Fri, 11 Sep 2026 23:22:21-22 GMT |
| Card spend windows in sandbox | current window 2026-09-01T04:00:00Z → 2026-10-01T04:00:00Z (monthly), 2026-09-09 → 2026-09-10 (daily) |
| Sandbox transaction data range | 2026-06-13T00:45:30Z to 2026-06-26T19:07:02Z (page 1 of ≥2) |
| MCP protocol versions supported | `2026-07-28`, `2025-11-25`, `2025-06-18` |
| `product/api` marketing page capability statement | "current as of August 2026" |
| Competitive API comparison on `product/api` | "collected from Mercury, Brex, and Ramp websites as of 2026-08-20" [Rho claim] |
| HTML reference pages re-fetched for this analysis | 2026-09-11 |
