## 3. The sandbox

The sandbox is where you will spend your first week with this API, and it is the part of the estate most likely to teach you something false. It is a single, shared, read-only fixture set behind an authentication check that validates presence and nothing else. It does not enforce scopes, it does not enforce rate limits, it has no MCP endpoint, and its failure responses are byte-identical to production's. Everything you can learn from it about *shapes* is trustworthy. Almost everything you might infer from it about *policy* is not.

Everything in this section is either quoted from the official `docs.rho.co` corpus (labelled as such) or observed against the live host. Observed facts carry the request that produced them. The probe runs behind this section were executed on 2026-09-11 between 23:38Z and 2026-09-12 00:30Z, and the spot checks in the worked examples were re-run at the end of that window. Raw captures live under `rho/sandbox/` (`probe-auth/`, `probe-pagination/`, `probe-resources/`, `probe-filters/`, `probe-limits/`, and the full dataset walk in `full/`).

---

### 3.1 Base URL and authentication

#### 3.1.1 The two hosts

| | Sandbox | Production |
|---|---|---|
| Base URL | `https://rhoapi-sandbox.rho.co/api/v1` | `https://rhoapi.rho.co/api/v1` |
| Credential | any non-empty bearer token | a real `rhobat_`-prefixed API Access Token |
| MCP endpoint | **none** (404) | `https://rhoapi.rho.co/mcp/v1` |
| DNS A records | `104.18.26.176`, `104.18.27.176` | **the same pair** |
| TLS leaf | `CN=rhoapi-sandbox.rho.co`, Google Trust Services WE1, ECDSA P-256 | `CN=rhoapi.rho.co`, same issuer |

Official docs (`docs/v1/getting-started`) give exactly one sandbox instruction:

```bash
curl https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H "Authorization: Bearer sandbox"
```

and state that "the sandbox accepts any non-empty bearer token, so you do not need to create a real API Access Token before testing requests there." `docs/v1/auth` repeats it: "Sandbox authentication is intentionally permissive so you can test API shapes against fictional data without creating a production API Access Token."

That claim is accurate, and understated. It is also the only thing the docs say about the sandbox anywhere in the corpus, aside from one line in `docs/v1/transactions` noting that sandbox file downloads contain "non-empty representative fictional documents."

#### 3.1.2 What "permissive" means exactly

The sandbox checks that the `Authorization` header value begins with the literal, case-sensitive string `Bearer ` (with one U+0020) and that what follows, after trimming surrounding whitespace, is non-empty. There is no format check, no length check below the nginx header ceiling, no charset check, and no token registry.

Observed, `GET https://rhoapi-sandbox.rho.co/api/v1/accounts` in every case:

| `Authorization` header sent | Status | Body |
|---|---|---|
| `Bearer sandbox` | `200` | full 2,558-byte account fixture |
| `Bearer rhobat_0000…0000` (production-shaped) | `200` | identical bytes |
| `Bearer zzzzz-not-a-real-token-!!!` | `200` | identical bytes |
| `Bearer x` (one character) | `200` | identical bytes |
| `Bearer two words` | `200` | identical bytes |
| `Bearer tökén-ünïcode` | `200` | identical bytes |
| `Bearer AAAA…` (1,024 chars) | `200` | identical bytes |
| `Bearer  sandbox` (two spaces) | `200` | identical bytes |
| `authorization: Bearer sandbox` (lowercase header name) | `200` | identical bytes |
| *(header absent entirely)* | `401` | `{"type":"2","title":"Unauthenticated","status":401}` |
| `Bearer ` (trailing space, empty token) | `401` | same 52 bytes |
| `Bearer  ` (token is one space) | `401` | same 52 bytes |
| `Bearer` (scheme only, no space) | `401` | same 52 bytes |
| `Authorization:` (header present, value empty) | `401` | same 52 bytes |
| `bearer sandbox` (lowercase scheme) | `401` | same 52 bytes |
| `BEARER sandbox` (uppercase scheme) | `401` | same 52 bytes |
| `Bearer\tsandbox` (tab separator) | `401` | same 52 bytes |
| `rhobat_abcdef0123456789` (no scheme) | `401` | same 52 bytes |
| `Basic c2FuZGJveDpzYW5kYm94` | `401` | same 52 bytes |
| `Token sandbox` | `401` | same 52 bytes |
| two `Authorization` headers | `400` | Cloudflare HTML, `cf-ray: -` (killed at the edge) |
| `Bearer AAAA…` (8,169 chars or more) | `400` | nginx HTML, `400 Request Header Or Cookie Too Large` |

Reproduce the two ends of that table:

```bash
# 200 with a token that is obviously not a credential
curl -s -o /dev/null -w '%{http_code}\n' \
  https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H 'Authorization: Bearer zzzzz-not-a-real-token-!!!'
# -> 200

# 401 with an empty bearer value
curl -s -w '\n%{http_code}\n' \
  https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H 'Authorization: Bearer '
# -> {"type":"2","title":"Unauthenticated","status":401}
#    401
```

Three consequences worth internalising before you write a line of client code.

**The scheme match is case-sensitive and space-sensitive.** `bearer`, `BEARER` and `Bearer<tab>` all fail. RFC 9110 §11.1 makes the auth scheme case-insensitive, so this is a deviation, and it is the single most likely cause of a mysterious 401 from a hand-rolled HTTP client. Send exactly `Authorization: Bearer <token>` with one ASCII space.

**Two error paths return HTML, not JSON.** A duplicated `Authorization` header is rejected by Cloudflare with an HTML body, and an oversized one by nginx with an HTML body. The exact ceiling is 8,190 bytes of header line (`"Authorization: Bearer "` is 22 bytes, so 8,168 token characters pass and 8,169 fail), which is the nginx default `large_client_header_buffers` of 8 KB. A client that unconditionally calls `JSON.parse` on an error body will throw on both.

**The 401 carries no `WWW-Authenticate` header.** RFC 9110 §11.6.1 makes it mandatory. It is absent from every REST 401 on both hosts. Production's `/mcp/v1` is the only endpoint in the estate that sends one.

> **Divergence:** `docs/v1/auth` prints this 401 body:
> ```json
> {"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}
> ```
> The live body, on sandbox and production alike, is:
> ```json
> {"type":"2","title":"Unauthenticated","status":401}
> ```
> `type` differs, `title` differs, and `detail` is absent. Three of four fields in the documented example are wrong. Do not key any logic on `title == "Unauthorized"`.

> **Divergence:** the OpenAPI schema describes the problem `type` member as "A URI reference that identifies the problem type. Example: `about:blank`." Live values on the auth, not-found and validation paths are `"2"`, `"1303"` and `"1317"`, bare numeric strings. A strictly conforming RFC 9457 client treats a non-URI `type` as `about:blank` and collapses all three into one generic type, losing the distinction entirely. Branch on the HTTP status code, not on `type`. See the Errors and Problem Details section for the full catalogue.

#### 3.1.3 Alternate credential channels

All rejected with the standard 401, confirming the docs' claim that "no other authentication header (cookie, API key, signed request) is supported":

| Channel | Result |
|---|---|
| `?access_token=sandbox` | `401` |
| `?token=sandbox` | `401` |
| `X-Api-Key: sandbox` | `401` |
| `Cookie: session=sandbox` | `401` |
| `Authorization: Basic <b64>` | `401` |
| `Authorization: Token sandbox` | `401` |

The query-parameter attempts return 401 rather than "unknown parameter" because unknown query parameters are silently ignored (see §3.6), so the request simply proceeds to the auth check with no credential.

Production's RFC 9728 discovery document independently corroborates this: `bearer_methods_supported: ["header"]`. Fetch it without any credential:

```bash
curl -s https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1
```
```json
{"resource":"https://rhoapi.rho.co/mcp/v1","authorization_servers":["https://auth.rho.co"],"bearer_methods_supported":["header"],"scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],"resource_documentation":"https://docs.rho.co/docs/v1/mcp"}
```

The same path on the sandbox host returns `default backend - 404`. The sandbox has no `.well-known` route at all.

---

### 3.2 One shared tenant, read-only

#### 3.2.1 The dataset is identical regardless of token

The token is not a tenant selector. Four different tokens produce byte-identical responses:

| Token | `/accounts` md5 | bytes |
|---|---|---|
| `sandbox` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |
| `rhobat_0000…0000` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |
| `completely-different-token-xyz` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |
| `1` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |

Verify it yourself in two calls:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
curl -s "$B/transactions?page_size=100" -H 'Authorization: Bearer sandbox' | openssl md5
curl -s "$B/transactions?page_size=100" -H 'Authorization: Bearer x'       | openssl md5
# both -> MD5(stdin)= 0e3829abca0416ff2e2058ec9cd1f6eb
```

This confirms the docs' "fictional, deterministic data" claim and establishes something the docs never say: **there is exactly one sandbox business, and anyone who knows the hostname can read all of it.** There is no mechanism, documented or discoverable, for selecting a second tenant, an empty-state business, or an error-state business. No magic tokens, no `?scenario=` parameter, no seeded failure accounts. What you see is what everyone sees.

#### 3.2.2 The dataset is read-only, and 405 precedes authentication

Every write method on every path returns `405 Method Not Allowed` with `allow: GET` and a zero-byte body:

| Method | `/accounts` | `/accounts/{id}` | `/transactions/{id}` | `/invoicing/invoices/{id}` | `/transactions/{id}/files/{fid}` | `/invoicing/customers` |
|---|---|---|---|---|---|---|
| POST | 405 | 405 | 405 | 405 | 405 | 405 |
| PUT | 405 | 405 | 405 | 405 | 405 | n/a |
| PATCH | 405 | 405 | 405 | 405 | 405 | n/a |
| DELETE | 405 | 405 | 405 | 405 | 405 | n/a |

```bash
curl -s -D- -o /dev/null -X POST https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H 'Authorization: Bearer sandbox' -H 'Content-Type: application/json' -d '{}' \
  | grep -Ei '^(HTTP|allow|content-length)'
```
```
HTTP/2 405
content-length: 0
allow: GET
```

No path advertises any write verb, so there is no hidden write surface reachable by verb probing. This is consistent with the whole v1 surface: all 14 documented operations are `GET`, and all five OAuth scopes end in `:read`.

The method check runs **before** the auth check. `DELETE /accounts/{id}` with no `Authorization` header at all returns `405`, not `401` (verified). Two practical consequences: an unauthenticated caller can enumerate which methods each path supports, and a non-401 status is **not** evidence that your token was accepted. The same holds for parameter type-binding errors, which also precede auth: `GET /accounts?page_size=abc` with no credential returns `400 {"type":"about:blank",…,"detail":"invalid parameter: page_size"}`.

The full ordering, derived from requests designed to fail several checks at once:

```
1. Cloudflare edge         duplicate Authorization -> 400 text/html, cf-ray: -
                           nonstandard method token (FOO) -> 403 WAF block page
                           TRACE -> 405 nginx-style HTML
2. Google frontend         POST/PUT without Content-Length -> 411 HTML (no `via` header)
3. ingress-nginx           path outside /api/v1 -> 404 "default backend - 404"
                           header line > 8190 bytes -> 400 "Request Header Or Cookie Too Large"
                           URI between 8 KB and 16 KB -> 414 HTML
4. Go router               unknown path under /api/v1 -> 404 "404 page not found" (text/plain)
5. Method check            -> 405 + "allow: GET", empty body
6. Parameter TYPE BINDING  -> 400 {"type":"about:blank", …, "detail":"invalid parameter: X"}
7. AUTHENTICATION          -> 401 {"type":"2","title":"Unauthenticated","status":401}
8. Handler + semantics     -> 400 {"type":"1317", …} / 404 {"type":"1303", …}
```

Those three distinct 404 surfaces are a useful debugging tool. `default backend - 404` means the request never reached the Rho application. `404 page not found` means the application was reached but no route matched. `{"type":"1303",…}` means the handler ran and the record does not exist.

#### 3.2.3 The fixtures are static, with one live exception

Repeat calls return byte-identical payloads across hours, tokens and connections. The exception is card spend windows, which are computed against the wall clock at request time: the six `monthly` cards report `spend_period_start` = `2026-09-01T04:00:00Z` and `spend_period_end` = `2026-10-01T04:00:00Z`, and the one `daily` card reported `2026-09-09T04:00:00Z` to `2026-09-10T04:00:00Z` on the probe date. The `04:00:00Z` offset is midnight America/New_York under EDT, matching the documented reset rule. Everything else in the dataset is frozen.

The other per-request computation is signed URL generation (§3.5.5), which changes the `X-Goog-Date` and `X-Goog-Signature` query parameters on `statements[].pdf_url` and on transaction file `download_url` without changing anything else.

---

### 3.3 Complete inventory of the fixture dataset

Every list endpoint below was walked to exhaustion at `page_size=100` following `page.next_page_token` until it returned `null`, then re-verified live. Every list fits in a single page at `page_size=100`.

#### 3.3.1 Record counts

| Resource | Endpoint | Records | Pages at `page_size=100` | ID space |
|---|---|---:|---|---|
| accounts | `GET /accounts` | **14** | 1 | `30000000-0000-4000-8000-0000000000NN`, NN = 01..14 |
| cards | `GET /cards` | **8** | 1 | `20000000-0000-4000-8000-0000000000NN`, NN = 01..08 |
| transactions | `GET /transactions` | **72** | 1 | UUIDv7, sequence suffix 0x01..0x48 |
| statements | `GET /statements` | **33** | 1 | 6-digit decimal strings, **not UUIDs** |
| invoicing customers | `GET /invoicing/customers` | **7** (8 with `include_deleted=true`) | 1 | `60000000-0000-4000-8000-0000000000NN`, NN = 01..08 |
| invoicing invoices | `GET /invoicing/invoices` | **12** | 1 | `70000000-0000-4000-8000-0000000000NN`, NN = 01..12 |
| transaction attachments | `GET /transactions/{id}/files/{file_id}` | **16 rows over 15 distinct file ids, on 14 transactions** | n/a | random UUIDv4 |
| invoice files | `GET /invoicing/invoices/{id}/files/{file_id}` | **9 referenced, 0 retrievable** | n/a | `50000000-0000-4000-8000-0000000000NN`, NN = 20..28 |

Reproduce the whole census in one command:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
H='Authorization: Bearer sandbox'
for p in accounts:accounts cards:cards transactions:transactions statements:statements \
         invoicing/customers:customers invoicing/invoices:invoices; do
  path="${p%%:*}"; key="${p##*:}"
  curl -s "$B/$path?page_size=100" -H "$H" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print('$path', len(d['$key']), 'next=', d['page']['next_page_token'])"
done
```
```
accounts 14 next= None
cards 8 next= None
transactions 72 next= None
statements 33 next= None
invoicing/customers 7 next= None
invoicing/invoices 12 next= None
```

Coverage was verified rather than assumed. Refetching `/transactions` filtered by each of the 14 `account_id` values, each of the 4 `status` values and each of the 5 documented `account_type` values yielded zero transaction ids absent from the unfiltered list, and each partition sums to exactly 72: by account 20+12+2+0+15+0+0+6+2+5+2+2+4+2, by status `settled` 61 + `failed` 8 + `pending` 2 + `awaiting_approval` 1, by account type `checking` 42 + `credit` 17 + `savings` 6 + `rewards` 7 + `investment` 0.

Three entity types are referenced by the payloads but have no endpoint of their own: **12 users** (`10000000-…`), **65 money movements** (`40000000-…`), and one unnamed business. `GET /users`, `/payments`, `/counterparties`, `/webhooks` and `/business` all return the bare text `404 page not found`.

#### 3.3.2 Date range

| Series | Earliest | Latest |
|---|---|---|
| `transactions.initiated_at` | `2023-05-31T07:29:00Z` | `2026-06-26T19:07:02Z` |
| `transactions.posted_at` | `2023-05-31T07:30:00Z` | `2026-06-27T19:13:15Z` |
| `statements.period_start` | `2024-07-01` | `2026-05-01` |
| `statements.period_end` | `2024-07-31` | `2026-05-31` |
| `statements.available_at` | `2024-08-01T04:02:00Z` | `2026-06-05T21:16:51Z` |
| `invoicing_customers.created_at` | `2026-01-10T09:00:00Z` | `2026-04-12T13:20:00Z` |
| `invoicing_customers.updated_at` | `2026-04-01T08:00:00Z` | `2026-07-24T16:00:00Z` |
| `invoices.created_at` | `2026-01-15T10:00:00Z` | `2026-07-10T09:00:00Z` |
| `invoices.date` (issue date) | `2026-01-15` | `2026-07-10` |
| `invoices.due_date` | `2026-02-01` | `2026-08-20` |
| `cards.spend_period_start` | `2025-03-01T12:00:00Z` | recomputed per request |
| `cards.usage_starts_at` | `2025-10-01T09:00:00Z` | (single value, 7 of 8 null) |
| `cards.usage_ends_at` | `2026-06-30T23:59:59Z` | `2026-09-01T00:00:00Z` |

The ledger is frozen: nothing in transactions, statements, invoices or customers is dated after 2026-08-20, and the newest transaction is roughly eleven weeks older than the probe date. If you build a dashboard that defaults to "last 30 days," the sandbox will show you an empty screen.

Two temporal formats appear, and they never mix within a field:

| Shape | Fields |
|---|---|
| `YYYY-MM-DDTHH:MM:SSZ` (seconds precision, always `Z`, never fractional) | `transactions.initiated_at`, `transactions.posted_at`, `statements.available_at`, `cards.spend_period_start`, `cards.spend_period_end`, `cards.usage_starts_at`, `cards.usage_ends_at`, `customers.created_at`, `customers.updated_at`, `customers.deleted_at`, `invoices.created_at`, `invoices.updated_at`, `invoices.accounting_synced_at`, `invoices.activities[].created_at` |
| `YYYY-MM-DD` (date only, no zone) | `statements.period_start`, `statements.period_end`, `invoices.date`, `invoices.due_date`, `invoices.payments[].paid_at` |

Not one timestamp in the corpus carries a sub-second component or a non-`Z` offset. A single strict parse format per field is safe against this dataset, though not necessarily against production.

#### 3.3.3 The ID scheme

`docs/v1/versioning` is explicit: "**Treat IDs as opaque strings.** Do not parse structure out of an `id` or assume a fixed format," and "Persist the full string exactly as returned, without assuming a fixed length or layout." Follow that advice. The structure below is documented here so you can reason about the fixtures, not so you can build on it.

| Prefix | Entity | Count | Trailing counter |
|---|---|---:|---|
| `10000000` | user (cardholder or initiator) | 12 | 01..12 |
| `20000000` | card | 8 | 01..08 |
| `30000000` | account | 14 | 01..14 |
| `40000000` | money movement **and** invoice activity actor (a genuine collision, see below) | 65 + 3 | 01..65 |
| `50000000` | invoice file | 9 | 20..28 |
| `60000000` | invoicing customer | 8 | 01..08 |
| `70000000` | invoice | 12 | 01..12 |

All of these parse as UUID version 4, variant RFC 4122, because the fixture generator hard-codes the version nibble `4` and the variant nibble `8`. The entropy is zero and the trailing twelve hex digits are a decimal-looking counter. Note that invoice suffixes are decimal-styled, so `…0009` is followed by `…0010` and `…000a` is a 404, while transaction suffixes are genuinely hex.

Two id families break the scheme entirely, and both matter:

- **`statements.id` is a 6-digit decimal string**, for example `"572981"` and `"152980"`. `uuid.UUID()` rejects all 33. This is the single most important trap in the surface: type it as a string, never as a UUID, and expect `GET /statements/abcdef` to return `404` rather than `400` because the endpoint performs no format validation at all.
- **`transactions.attachments[].file_id` is a genuinely random UUIDv4**, for example `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15`. Invoice `file_id` values use the structured `50000000-` prefix. File ids are not one namespace.

Statement ids come from two disjoint sequence bands, which is also the clearest evidence that the aggregation behaviour documented for statements is not exercised here:

| `statement_type` | n | ID range | Observed ids |
|---|---:|---|---|
| credit | 22 | 152980..200527 | 152980, 153670, 154411, 155137, 155915, 156744, 157603, 158472, 159417, 160431, 161396, 161929, 163022, 164322, 165954, 167766, 169823, 172111, 174810, 179033, 186996, 200527 |
| account | 4 | 428772..439951 | 428772, 433488, 439950, 439951 |
| treasury | 7 | 462701..572981 | 462701, 469372, 475381, 490851, 514051, 539240, 572981 |

Transaction ids are UUIDv7 with the random bits zeroed:

| Segment of `019f0554-0bf0-7000-8000-00000000000a` | Bits | Content | Observed |
|---|---|---|---|
| `019f0554-0bf0` | 48 | Unix epoch milliseconds, big-endian | full three-year spread |
| `7000` | 4 + 12 | version nibble `7`, then `rand_a` | `7000` on all 72, so `rand_a` is always zero |
| `8000` | 2 + 14 | variant bits, then `rand_b` high | `8000` on all 72 |
| `00000000000a` | 48 | `rand_b` low | a dense counter, exactly 1..72 with no gaps |

The embedded millisecond timestamp equals `initiated_at` exactly on 70 of 72 records. The two exceptions are the two highest sequence numbers, appended to the fixture set last with a shared base timestamp. Because the v7 prefix dominates lexicographic order, transaction ids sort by time, which is why the default list order and `sort_by=initiated_at` order coincide. Do not sort by the suffix: of 71 adjacent pairs, 15 are out of chronological order.

**A namespace collision to know about.** `transactions.money_movement_id` uses `40000000-0000-4000-8000-000000000001` through `…000065`. `invoices.activities[].user_id` uses `40000000-0000-4000-8000-000000000001`, `…000002` and `…000003`. Those three ids look like money movements 1, 2 and 3 but semantically are Rho users who acted on an invoice. Everything else in the corpus uses `10000000-` for users. The cross-check is unambiguous: 3 references, 0 resolve, 3 dangling. The invoicing product's actor ids and the banking product's user ids are not in the same namespace, so you cannot join an invoice activity to a cardholder or a transaction initiator.

#### 3.3.4 Money representation

Every `currency` field in the entire corpus, across 393 occurrences in all six resources, is `USD`. There is no non-USD record, no FX rate field, no settlement currency, and no second currency anywhere. All monetary values are **integers in minor units** (cents) inside a `{amount, currency}` object.

The only non-integer numerics in the whole dataset are `invoices.tax_rate`, `invoices.discount_rate`, `line_items[].tax_rate`, `line_items[].discount_rate` and `line_items[].quantity`. Observed values include `2.5`, `6.25` and `8.5`, so all three must be declared as float or decimal in a typed client even though most values serialize without a decimal point.

**Sign convention.** There is no `direction`, `debit_credit` or `type: debit|credit` field on a transaction. The sign of `amount.amount` is the only directional signal, and it is relative to the account named in `account_id`. Debits are negative, credits positive, and zero never occurs.

| `transaction_type` | neg | pos | min | max |
|---|---:|---:|---|---|
| `ach_credit` | 0 | 5 | 12771 | 108403 |
| `ach_debit` | 6 | 0 | -1250000 | -56250 |
| `ach_return` | 2 | 0 | -50582 | -18209 |
| `adjustment_credit` | **1** | 0 | -4500 | -4500 |
| `adjustment_debit` | 0 | **1** | 3000 | 3000 |
| `card_debit` | 8 | 0 | -1622132 | -1750 |
| `card_refund` | 0 | 4 | 1159 | 228073 |
| `check_deposit` | 0 | 3 | 100000 | 329900 |
| `check_payment` | 2 | 0 | -339100 | -339100 |
| `credit_repayment` | 3 | 3 | -1658253 | 1658253 |
| `credit_repayment_refund` | 2 | 2 | -282512 | 282512 |
| `internal_transfer` | 2 | 2 | -123987 | 123987 |
| `international_wire_fee` | 2 | 0 | -1500 | -1500 |
| `international_wire_out` | 2 | 0 | -279000 | -52142 |
| `rewards_accrual` | 0 | 4 | 764 | 108403 |
| `rewards_cashback_redemption` | 3 | 0 | -108403 | -12771 |
| `savings_deposit` | 0 | 2 | 3000000 | 130000000 |
| `savings_interest` | 0 | 2 | 225537 | 257025 |
| `savings_withdrawal` | 2 | 0 | -1000000 | -225537 |
| `wire_fee` | 1 | 0 | -1000 | -1000 |
| `wire_in` | 0 | 4 | 9929125 | 15000000 |
| `wire_out` | 4 | 0 | -5900000 | -50000 |

Totals: 40 negative, 32 positive, 0 zero. Global range `-5900000` (a failed `wire_out`) to `130000000` (a `savings_deposit`).

**`adjustment_credit` is negative and `adjustment_debit` is positive.** That is the one pair where the type name and the sign are inverted relative to every other pair. Nothing in `docs/v1/transactions` or the OpenAPI markdown defines the sign of an adjustment, so it cannot be resolved from the corpus. Read direction from the sign, never from the type name.

**Multi-leg movements are true double entry.** 65 distinct `money_movement_id` values cover 72 transactions. 58 are single-leg and 7 have exactly two legs that sum to zero:

| `money_movement_id` suffix | Type | Accounts | Amounts |
|---|---|---|---|
| `…02` | `credit_repayment` | Cash (Checking) / Credit Account | -1750 / +1750 |
| `…03` | `credit_repayment` | Cash (Checking) / Credit Account | -1658253 / +1658253 |
| `…06` | `credit_repayment` | Cash (Checking) / Credit Account | -144827 / +144827 |
| `…21` | `internal_transfer` | Cash (Checking) / Reserve Checking | -123987 / +123987 |
| `…27` | `internal_transfer` | Cash (Checking) / Reserve Checking | **+40564 / -40564** |
| `…59` | `credit_repayment_refund` | Cash (Checking) / Credit Account | +282512 / -282512 |
| `…60` | `credit_repayment_refund` | Cash (Checking) / Credit Account | +9418 / -9418 |

Movements `…21` and `…27` are both internal transfers between the same two accounts with opposite polarity, so leg order carries no meaning. Group by `money_movement_id` before presenting transfers or you will double-count every one of them. Note there is no `money_movement_id` filter on `/transactions`, so grouping has to happen client-side after a full walk.

**Statements use the opposite polarity from transactions.** On a credit statement, `spending` is positive for money spent and `repayments` is negative for money repaid, which is backwards from `card_debit` (negative) and the credit leg of `credit_repayment` (positive). The credit-statement identity holds on all 22 credit statements with no exceptions:

```
closing_balance = opening_balance + spending + repayments
```

Worked example, statement `200527` (credit, account `…008`, 2026-03-13 to 2026-04-12): `5453868 + 6931038 + (-69221) = 12315685`.

Deposit statements use a different and mutually exclusive identity, which holds on all 4 `account` and all 7 `treasury` statements:

```
closing_balance = opening_balance + total_credits - total_debits - total_fees
```

On credit statements `total_credits`, `total_debits` and `total_fees` are always `0` and carry no information. On account and treasury statements the `spending`, `repayments` and `cashback` keys are **omitted entirely**, not null. Branch on `statement_type`, or on key presence.

Cashback is a deterministic function of spending at two different rates depending on the credit account, truncated toward zero rather than floored: account `…007` runs at 1.25% (11 statements) and account `…008` at 1.50% (11 statements). `-26200` at 1.25% is `-327.5` and yields `-327`, not `-328`. Nothing in the API exposes the rate itself.

**Balances do not reconcile to the transaction list.** Summing settled transactions per account reproduces `accounts.balance.amount` on only 4 of 14 accounts, and those are the four where both sides are zero.

| Account | Name | `balance.amount` | Sum of settled txns | Match |
|---|---|---:|---:|---|
| `…001` | Reserve Checking | 1046 | 83423 | no |
| `…002` | Cash (Checking) | 876138 | 8730522 | no |
| `…003` | Cash (Checking) | 8711697 | 38721683 | no |
| `…004` | Treasury Checking | 15460929 | -4500 | no |
| `…005` | Inventory Checking | 0 | 0 | yes |
| `…006` | Primary Checking | 811970 | -457906 | no |
| `…007` | Credit Account | 0 | 0 | yes |
| `…008` | Credit Account | 0 | 0 | yes |
| `…009` | Credit Account | 0 | 25495 | no |
| `…010` | Credit Account | 0 | 0 | yes |
| `…011` | Rewards | 0 | 58255 | no |
| `…012` | Rewards | 0 | -12007 | no |
| `…013` | Savings | 0 | 2000000 | no |
| `…014` | Savings | 0 | 130257025 | no |

The transaction list is a curated sample, not a complete ledger. Do not write reconciliation tests against the sandbox. Note also that all four credit accounts and both rewards accounts report a zero balance, so the sandbox never shows what a carried credit balance looks like on `/accounts`, even though credit statements carry closing balances up to `12315685`.

#### 3.3.5 Per-resource inventories

**Accounts (14).**

| id tail | `account_type` | `account_name` | `balance.amount` | `account_number_last_4` | `routing_number_last_4` |
|---|---|---|---:|---|---|
| 01 | checking | Reserve Checking | 1046 | 0106 | 0089 |
| 02 | checking | Cash (Checking) | 876138 | 9508 | 0089 |
| 03 | checking | Cash (Checking) | 8711697 | 4609 | 0089 |
| 04 | checking | Treasury Checking | 15460929 | 7301 | 0089 |
| 05 | checking | Inventory Checking | 0 | 3608 | 0089 |
| 06 | checking | Primary Checking | 811970 | 5702 | 0089 |
| 07 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 08 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 09 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 10 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 11 | rewards | Rewards | 0 | *(omitted)* | *(omitted)* |
| 12 | rewards | Rewards | 0 | *(omitted)* | *(omitted)* |
| 13 | savings | Savings | 0 | 3214 | 0089 |
| 14 | savings | Savings | 0 | 2513 | 0089 |

`account_number_last_4` and `routing_number_last_4` are **omitted, not null**, on the six credit and rewards accounts, so `/accounts` returns a four-key object for those and a six-key object for the eight deposit accounts. `account_name` is not unique. All eight deposit accounts share one routing number. "Treasury Checking" has `account_type: "checking"`, not `treasury`, and `treasury` is not a member of the accounts enum at all. Three accounts have zero transactions, and nine of the 14 appear in no statement. There is no `created_at`, `status`, `available_balance` or `credit_limit` on an account.

**Cards (8).**

| id tail | `name` | `type` | `status` | `last_4` | limit type | limit | `current_spend` | `pending_spend` |
|---|---|---|---|---|---|---:|---:|---:|
| 01 | Ethan Parker | virtual | active | 7291 | monthly | 500000 | 6797 | 1500 |
| 02 | Maya Thompson | physical | active | 1846 | monthly | 100000 | 45000 | 8000 |
| 03 | Daniel Rivera | virtual | active | 3150 | monthly | 250000 | 1750 | 250 |
| 04 | Lucas Bennett | physical | locked | 6603 | **daily** | 75000 | 6331 | 900 |
| 05 | Sofia Martin Physical Card | physical | active | **0042** | monthly | 200000 | 5331 | 400 |
| 06 | Hannah Brooks | virtual | suspended | 9027 | monthly | 2500000 | 1622132 | 50000 |
| 07 | Emma Walsh Virtual Card | virtual | canceled | 1184 | monthly | 150000 | 121827 | 0 |
| 08 | Claire Mitchell | physical | expired | 7732 | **fixed** | 500000 | 0 | 0 |

`last_4` really does carry a leading zero on card 05, and it is a string that must stay one. Merchant and MCC controls are omitted, not null, on 7 of 8 cards: exactly one card carries `allowed_categories` (`[{"code":"5812","name":"Eating places and restaurants"}]`) and `allowed_merchants` (`[{"name":"Sweetgreen"}]`), and a different single card carries `blocked_categories` (`[{"code":"0742","name":"Veterinary services"}]`) and `blocked_merchants` (`[{"name":"Petco"}]`). No card has both. MCC codes are strings with leading zeros. `shipping_address` is explicitly `null` on the four virtual cards while merchant controls are omitted, so both null idioms appear on one object. Canceled, suspended, locked and expired cards still report live, recomputed spend windows.

**Statements (33).**

| `statement_type` | n | Accounts | Period cadence | ID band |
|---|---:|---|---|---|
| `credit` | 22 | `…007` (11), `…008` (11) | `…007`: calendar months 2024-07 to 2025-05. `…008`: 13th-to-12th cycles, 2025-05-13/2025-06-12 through 2026-03-13/2026-04-12 | 152980-200527 |
| `account` | 4 | `…006` Primary Checking (3), `…013` Savings (1) | calendar months 2024-07, 2024-12, 2025-05 | 428772-439951 |
| `treasury` | 7 | `…004` Treasury Checking (7) | calendar months 2025-11 through 2026-05 | 462701-572981 |

The 33 statements resolve to only **three distinct PDF blobs**, one per statement type. Statements carry no `account_name`, no statement number, no `created_at`, and no link back to the transactions they cover.

**Transactions (72).** Presence is the whole story. The list surface returns six distinct object shapes depending on which optional keys are omitted:

| Field | Present | Omitted | Ever null when present |
|---|---:|---:|---|
| `posted_at` | 71 | **1** | no |
| `memo` | 39 | 33 | no |
| `note` | 39 | 33 | no |
| `user_id` | 38 | 34 | no |
| `user_full_name` | 38 | 34 | no |
| `card_id` | 12 | 60 | no |
| `card_name` | 12 | 60 | no |
| `counterparty_logo_url` | **0** | 72 | n/a |
| `tracking_number` | **0** | 72 | n/a |
| everything else | 72 | 0 | no |

**Not one transaction field is ever JSON `null`.** Optionality is expressed purely by key omission. `memo` and `note` are present or absent together and are byte-identical on 37 of the 39 records that have them, so the sandbox effectively models them as one field. `user_id` and `user_full_name` are present on exactly the types a person initiates and absent on exactly the system types, with no type on both sides. `card_id` and `card_name` appear on exactly the 12 `card_debit` and `card_refund` records.

**Invoicing customers (7, or 8 with `include_deleted=true`).**

| id tail | `legal_name` | `email` | `total_revenue` | `last_invoice_id` | `deleted_at` |
|---|---|---|---:|---|---|
| 01 | Acme Supplies | info@acmesupplies.com | 108403 | …02 | null |
| 02 | Brightleaf Design | hello@brightleaf.design | 43400 | …03 | null |
| 03 | Northwind Traders | orders@northwind.example | 0 | …06 | null |
| 04 | Harbor Logistics LLC | billing@harborlogistics.com | 156750 | …08 | null |
| 05 | Summit Analytics | contact@summitanalytics.io | 0 | …10 | null |
| 06 | Cedar & Co | **null** | 0 | **null** | null |
| 07 | Orbit Media Group | accounts@orbitmedia.co | 0 | …11 | null |
| 08 | Deleted Co | gone@deletedco.example | 5000 | …12 | **2026-05-01T12:00:00Z** |

Customers are the mirror image of transactions: **all 19 field paths are present on all 8 records**, and optionality is carried by nullity. `address.address2` is the empty string, not null, on the customers that lack one. `address.country` is `"USA"` (alpha-3) while `cards.billing_address.country_code` is `"US"` (alpha-2), and the two address models share no field names. `total_revenue` sums only that customer's `paid`-status invoices, which is why Northwind Traders holds 10,168,200 minor units of invoices and still reports zero.

**Invoicing invoices (12).**

| id tail | Number | Status | Total | `tax_rate` | `discount_rate` | Customer | `file_id` | `accounting_sync_status` | lines | payments | activities |
|---|---|---|---:|---|---|---|---|---|---:|---:|---:|
| 01 | INV-2026-0002 | paid | 108403 | 10 | 0 | …001 | …0020 | synced | 2 | 1 | 6 |
| 02 | INV-2026-0066 | pending_payout | 158000 | 10 | 0 | …001 | …0021 | synced | 4 | 1 | 7 |
| 03 | INV-2026-0060 | overdue | 45000 | 0 | 0 | …002 | …0022 | not_pushed | 1 | 0 | 3 |
| 04 | INV-2026-0040 | paid | 43400 | 8.5 | 0 | …002 | …0023 | synced | 1 | 1 | 4 |
| 05 | INV-2026-0045 | overdue | 72200 | 0 | 5 | …003 | …0024 | error | 1 | 0 | 3 |
| 06 | INV-2026-0065 | unpaid | 96000 | 0 | 0 | …003 | *(omitted)* | not_pushed | 1 | 0 | 2 |
| 07 | INV-2026-0043 | confirm_payment | 10000000 | 0 | 0 | …003 | …0025 | object_changed | 1 | 1 | 3 |
| 08 | INV-2026-0050 | paid | 156750 | 0 | 0 | …004 | …0026 | synced | 1 | 1 | 4 |
| 09 | INV-2026-0041 | cancelled | 22000 | 0 | 0 | …005 | *(omitted)* | skip | 1 | 0 | 2 |
| 10 | INV-2026-0070 | pending_payout | 98000 | 0 | 0 | …005 | …0027 | synced | 1 | 1 | 5 |
| 11 | INV-2026-0052 | unpaid | 45000 | 6.25 | 0 | …007 | …0028 | not_pushed | 1 | 0 | 2 |
| 12 | INV-2026-0001 | paid | 5000 | 0 | 0 | …008 | *(omitted)* | synced | 1 | 1 | 3 |

The invoice total formula, verified against all 12 records:

```
line.total    = round( unit_price.amount * quantity * (1 - line.discount_rate/100) )
invoice.total = round( SUM over lines of
                         line.total
                         * (1 - invoice.discount_rate/100)
                         * (1 + (line.tax_rate ?? invoice.tax_rate)/100) )
```

Two non-obvious parts. A null `line_items[].tax_rate` **falls back to the invoice-level `tax_rate`**, it does not mean zero: `INV-2026-0066` has four lines, two with `tax_rate: null` and two with `tax_rate: 0`, and the total is 100000×1.10 + 20000×1.10 + 20000×1.00 + 6000×1.00 = 158000. If null meant zero the total would be 146000, and 10 of the 16 line items carry a null rate. Second, discount is applied twice, once per line and once at the invoice level, with no netting. Rounding is to nearest: `INV-2026-0052` computes to 45000.0625 and reports 45000.

`file_id` is the lone omission-style field on this resource; every other optional invoice field is null when unset. `payments[]` has 0 or 1 entries and never more, so partial and multi-payment invoices are untested. `payments[].transaction_id` is populated only for `type: "received_in_account"` (2 of 7 payments), and both ids resolve into the 72-transaction set, which is the only link between Invoicing and the banking ledger.

#### 3.3.6 Relationships between records

Edges actually present in the payloads:

```
users (10000000-…, 12, no endpoint)
  |  cards.cardholder.user_id            8 of 12 users hold a card
  |  transactions.user_id                12 of 12 users initiate transactions
  v
cards (20000000-…, 8)
  |  transactions.card_id                all 8 cards appear on 12 transactions
  v
transactions (UUIDv7, 72)
  |  transactions.account_id  ---------> accounts (30000000-…, 14), 11 of 14 referenced
  |  transactions.money_movement_id ---> money movements (40000000-…, 65, no endpoint)
  |  transactions.attachments[].file_id -> GET /transactions/{id}/files/{file_id}   [works]
  ^
  |  invoices.payments[].transaction_id  2 of 12 invoices reach into the ledger
  |
invoices (70000000-…, 12)
  |  invoices.customer.id -------------> customers (60000000-…, 8)
  |  invoices.file_id -----------------> GET /invoicing/invoices/{id}/files/{fid}   [404, broken]
  |  invoices.activities[].user_id ----> 40000000-… ids that resolve to NOTHING
  ^
  |  customers.last_invoice_id           7 of 8 customers point at their newest invoice
  |
statements (6-digit decimal, 33)
  |  statements.accounts[].account_id --> accounts, 5 of 14 referenced
  (no edge to transactions in either direction)
```

Referential integrity, measured:

| Edge | Distinct refs | Resolve | Dangling |
|---|---:|---:|---:|
| `transactions.account_id` to accounts | 11 | 11 | 0 |
| `transactions.card_id` to cards | 8 | 8 | 0 |
| `statements.accounts[].account_id` to accounts | 5 | 5 | 0 |
| `customers.last_invoice_id` to invoices | 7 | 7 | 0 |
| `invoices.customer.id` to customers | 7 | 7 | 0 |
| `invoices.payments[].transaction_id` to transactions | 2 | 2 | 0 |
| `cards.cardholder.user_id` to transaction user ids | 8 | 8 | 0 |
| **`invoices.activities[].user_id` to transaction user ids** | **3** | **0** | **3** |

One broken edge, and it is the `40000000-` collision described above.

Coverage gaps worth knowing before you write assertions:

| Gap | Detail |
|---|---|
| accounts with no transaction | `…005` Inventory Checking, `…008`, `…010` |
| accounts in no statement | 9 of 14: `…001`, `…002`, `…003`, `…005`, `…009`, `…010`, `…011`, `…012`, `…014` |
| customers with no invoice | `…006` Cedar & Co, which is also the one with a null `email` and a null `last_invoice_id` |
| cards with no transaction | none, all 8 are exercised |
| users with no card | 4 of 12: Olivia Chen, Priya Shah, Grace Morgan, Andrew Collins |
| statement-to-transaction links | none, in either direction |
| invoices reaching the ledger | 2 of 12 |

The 12 users are never listable but are reconstructable from `transactions.user_id` plus `cards.cardholder`, which agree on every overlapping id:

| `user_id` | Name | Holds card |
|---|---|---|
| `10000000-…0000001` | Ethan Parker | card `…001` (virtual, active) |
| `10000000-…0000002` | Maya Thompson | card `…002` (physical, active) |
| `10000000-…0000003` | Daniel Rivera | card `…003` (virtual, active) |
| `10000000-…0000004` | Lucas Bennett | card `…004` (physical, locked) |
| `10000000-…0000005` | Olivia Chen | none |
| `10000000-…0000006` | Sofia Martin | card `…005` (physical, active) |
| `10000000-…0000007` | Hannah Brooks | card `…006` (virtual, suspended) |
| `10000000-…0000008` | Emma Walsh | card `…007` (virtual, canceled) |
| `10000000-…0000009` | Claire Mitchell | card `…008` (physical, expired) |
| `10000000-…0000010` | Priya Shah | none |
| `10000000-…0000011` | Grace Morgan | none |
| `10000000-…0000012` | Andrew Collins | none |

Card ids are not offset-aligned with user ids from card 05 onward. Do not infer the mapping from the counters.

#### 3.3.7 Enums: documented versus observed

The versioning policy warns that a new enum value can ship into `v1` at any time and that clients must have a default branch. The gap between documented and observed is therefore your real test-coverage problem.

`transaction_type`: **33 documented, 22 observed, 11 never produced.**

Observed: `ach_credit`, `ach_debit`, `ach_return`, `adjustment_credit`, `adjustment_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `credit_repayment`, `credit_repayment_refund`, `internal_transfer`, `international_wire_fee`, `international_wire_out`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`, `wire_out`.

Never produced: `card_credit`, `credit_cashback`, `international_wire_in`, `international_wire_fee_refund`, and the entire treasury family (`treasury_deposit`, `treasury_withdrawal`, `treasury_fee`, `treasury_interest`, `treasury_maturity`, `treasury_sale`, `treasury_market_value_adjustment`).

The treasury gap is the notable one. The sandbox has a "Treasury Checking" account and seven `treasury` statements, but that account's only transaction is a single `adjustment_credit` of -4500. Treasury is the product whose transaction shapes an integrator most needs and cannot see.

Every other enum:

| Field | Documented values | Observed (with counts) | Never observed |
|---|---|---|---|
| `transactions.status` | pending, settled, failed, awaiting_approval | **all 4** (2 / 61 / 8 / 1) | none |
| `accounts.account_type` | checking, credit, investment, savings, rewards | checking 6, credit 4, rewards 2, savings 2 | **investment** |
| `cards.type` | physical, virtual | physical 4, virtual 4 | none |
| `cards.status` | printing, shipped, out_for_delivery, activate_card, delivery_canceled, active, expiring, locked, canceled, suspended, expired | active 4, locked 1, canceled 1, suspended 1, expired 1 | **printing, shipped, out_for_delivery, activate_card, delivery_canceled, expiring** (the entire fulfilment pipeline) |
| `cards.spending_limit_type` | fixed, monthly, single_use, annual, daily, weekly, quarterly | monthly 6, daily 1, fixed 1 | **single_use, annual, weekly, quarterly** |
| `statements.statement_type` | account, credit, treasury | credit 22, treasury 7, account 4 | none |
| `statements.accounts[].account_type` | checking, savings, credit, treasury | credit 22, treasury 7, checking 3, savings 1 | none |
| `invoices.status` | paid, unpaid, cancelled, overdue, confirm_payment, pending_payout | paid 4, unpaid 2, overdue 2, pending_payout 2, cancelled 1, confirm_payment 1 | none |
| `invoices.accounting_sync_status` | not_pushed, synced, error, skip, object_changed | synced 6, not_pushed 3, error 1, skip 1, object_changed 1 | none |
| `invoices.activities[].activity_type` | created, sent, downloaded, matched, marked_as_paid, marked_as_unpaid, cancelled, reminder_sent, card_payment_received, accounting_synced, payment_accounting_synced | **all 11** | none |
| `invoices.payments[].type` | received_in_account, external | external 5, received_in_account 2 | none |
| `invoices.payments[].external_method` | cash, check, credit_card, other | credit_card 2, cash 1, check 1, other 1 (plus 2 nulls) | none |

Two cross-cutting traps in that table. **`cards.status` spells `canceled` with one L while `invoices.status` and `activities[].activity_type` spell `cancelled` with two.** Both are correct within their own product and both ship in the same API version, so a shared status mapper will silently miss one. And **the statements `account_type` enum is a different set from the accounts `account_type` enum**: statements use `{checking, savings, credit, treasury}`, accounts use `{checking, credit, investment, savings, rewards}`. `treasury` is a statement-level concept mapped onto a checking account.

Invoicing is by far the best-covered product in the sandbox (11 of 11 activity types across only 12 invoices). Cards fulfilment and treasury are the worst.

`transaction_type` crossed with `status`, which is what you actually need when you are picking a fixture to test a UI state against:

| Type | pending | settled | failed | awaiting_approval |
|---|---:|---:|---:|---:|
| `ach_credit` | | 5 | | |
| `ach_debit` | | 5 | | **1** |
| `ach_return` | | 2 | | |
| `adjustment_credit` | | 1 | | |
| `adjustment_debit` | | 1 | | |
| `card_debit` | **2** | 6 | | |
| `card_refund` | | 4 | | |
| `check_deposit` | | | **3** | |
| `check_payment` | | 1 | **1** | |
| `credit_repayment` | | 6 | | |
| `credit_repayment_refund` | | 4 | | |
| `internal_transfer` | | 4 | | |
| `international_wire_fee` | | 2 | | |
| `international_wire_out` | | 2 | | |
| `rewards_accrual` | | 4 | | |
| `rewards_cashback_redemption` | | 3 | | |
| `savings_deposit` | | 2 | | |
| `savings_interest` | | 2 | | |
| `savings_withdrawal` | | 2 | | |
| `wire_fee` | | 1 | | |
| `wire_in` | | 4 | | |
| `wire_out` | | | **4** | |

All four `wire_out` records and all three `check_deposit` records are `failed`. There is no settled wire out and no settled check deposit anywhere in the sandbox.

And crossed with `account_type`:

| `account_type` | Transaction types seen |
|---|---|
| `checking` | ach_credit 5, ach_debit 6, ach_return 2, adjustment_credit 1, adjustment_debit 1, check_deposit 3, check_payment 2, credit_repayment 3, credit_repayment_refund 2, internal_transfer 4, international_wire_fee 2, international_wire_out 2, wire_fee 1, wire_in 4, wire_out 4 |
| `credit` | card_debit 8, card_refund 4, credit_repayment 3, credit_repayment_refund 2 |
| `rewards` | rewards_accrual 4, rewards_cashback_redemption 3 |
| `savings` | savings_deposit 2, savings_interest 2, savings_withdrawal 2 |
| `investment` | none |

Card transactions land on `credit` accounts only. There is no `card_debit` on a checking account anywhere, so a debit-card-on-checking model is untested.

#### 3.3.8 Field-path census

Produced by walking every record on both the list and detail surfaces. `present` is occurrences of the key divided by occurrences of its containing object, so a ratio below 1.0 means the key is **omitted** on some records, which is a different failure mode from null and the single most important signal when writing a deserializer. The list and detail columns were reported separately so that any divergence would show up. None does.

| Resource | List records | Detail records | Distinct field paths |
|---|---:|---:|---:|
| accounts | 14 | 14 | 8 |
| cards | 8 | 8 | 47 |
| transactions | 72 | 72 | 22 |
| statements | 33 | 33 | 33 |
| invoicing_customers | 8 | 8 | 19 |
| invoicing_invoices | 12 | 12 | 39 |

**`accounts`**

| Field path | JSON types | present | null | n distinct | Observed values |
|---|---|---|---:|---:|---|
| `account_name` | string | 14/14 | 0 | 8 | `Cash (Checking)`, `Credit Account`, `Inventory Checking`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_number_last_4` | string | **8/14** | 0 | 8 | `0106`, `2513`, `3214`, `3608`, `4609`, `5702`, `7301`, `9508` |
| `account_type` | string | 14/14 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `balance` | object | 14/14 | 0 | | |
| `balance.amount` | int | 14/14 | 0 | 6 | `0`, `1046`, `811970`, `876138`, `8711697`, `15460929` |
| `balance.currency` | string | 14/14 | 0 | 1 | `USD` |
| `id` | string | 14/14 | 0 | 14 | `30000000-0000-4000-8000-0000000000NN`, NN = 01..14 |
| `routing_number_last_4` | string | **8/14** | 0 | 1 | `0089` |

**`transactions`**

| Field path | JSON types | present | null | n distinct | Observed values |
|---|---|---|---:|---:|---|
| `account_id` | string | 72/72 | 0 | 11 | account ids 01, 02, 03, 04, 06, 07, 09, 11, 12, 13, 14 |
| `account_name` | string | 72/72 | 0 | 7 | `Cash (Checking)`, `Credit Account`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_type` | string | 72/72 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `amount` | object | 72/72 | 0 | | |
| `amount.amount` | int | 72/72 | 0 | 64 | min `-5900000`, max `130000000` |
| `amount.currency` | string | 72/72 | 0 | 1 | `USD` |
| `attachments` | array | 72/72 | 0 | | lengths: 0 ×58, 1 ×12, 2 ×2 |
| `attachments[].file_id` | string | 16/16 | 0 | 15 | random UUIDv4 |
| `attachments[].file_name` | string | 16/16 | 0 | 15 | 14 `.pdf`, 1 `.csv` (`repayment-details.csv`) |
| `card_id` | string | **12/72** | 0 | 8 | all 8 card ids |
| `card_name` | string | **12/72** | 0 | 8 | all 8 card names |
| `counterparty_name` | string | 72/72 | 0 | 37 | `Aaron Blake` … `Zurich Airport Services`, plus `Rho`, `Rho Rewards`, `Rho Savings` and five internal account names |
| `id` | string | 72/72 | 0 | 72 | `018870b5-c260-7000-8000-000000000045` … `019f0554-0bf0-7000-8000-00000000000a` |
| `initiated_at` | string | 72/72 | 0 | 67 | `2023-05-31T07:29:00Z` … `2026-06-26T19:07:02Z` |
| `memo` | string | **39/72** | 0 | 25 | see below |
| `money_movement_id` | string | 72/72 | 0 | 65 | `40000000-0000-4000-8000-0000000000NN`, NN = 01..65 |
| `note` | string | **39/72** | 0 | 25 | identical to `memo` on 37 of 39 |
| `posted_at` | string | **71/72** | 0 | 65 | `2023-05-31T07:30:00Z` … `2026-06-27T19:13:15Z` |
| `status` | string | 72/72 | 0 | 4 | `awaiting_approval`, `failed`, `pending`, `settled` |
| `transaction_type` | string | 72/72 | 0 | 22 | see §3.3.7 |
| `user_full_name` | string | **38/72** | 0 | 12 | the 12 users |
| `user_id` | string | **38/72** | 0 | 12 | `10000000-0000-4000-8000-0000000000NN`, NN = 01..12 |

The memo corpus is worth reading once, because it tells you what the sandbox was built from: `Contractor hours`, `Correction of encoding error regarding check number 100245`, `Daily credit repayment for date 2026/06/23`, `Inventory restock`, `Invoice 317 - consulting services`, `MONEY TRANSFER`, `Monthly office rent`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00`, `PAY1001984`, `Q3 freight invoice`, `Rewards cashback`, `SC - 2509 - desk mat shipping`, `Severance payment`, `Swift OUR fee`, `Transfer to external account`, `Wire fee`, `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle`, `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`. One of those is a Postgres `timestamptz` with microseconds and an Eastern offset rendered into user-visible prose. These were lifted from a real ledger and anonymized, which is why the formats are inconsistent. Your renderer should assume memo text is arbitrary.

**`statements`**

| Field path | JSON types | present | null | n distinct | Observed values |
|---|---|---|---:|---:|---|
| `accounts` | array | 33/33 | 0 | | length 1 on **all 33** |
| `accounts[].account_id` | string | 33/33 | **0** | 5 | accounts `…004`, `…006`, `…007`, `…008`, `…013` |
| `accounts[].account_type` | string | 33/33 | 0 | 4 | `checking`, `credit`, `savings`, `treasury` |
| `accounts[].cashback` | object | **22/33** | 0 | | credit statements only |
| `accounts[].cashback.amount` | int | 22/22 | 0 | 19 | `-327` … `103965` |
| `accounts[].closing_balance.amount` | int | 33/33 | 0 | 14 | `0` … `12315685` |
| `accounts[].opening_balance.amount` | int | 33/33 | 0 | 13 | `0` … `7550175` |
| `accounts[].repayments` | object | **22/33** | 0 | | credit statements only |
| `accounts[].repayments.amount` | int | 22/22 | 0 | 10 | `-2165638` … `26200` |
| `accounts[].spending` | object | **22/33** | 0 | | credit statements only |
| `accounts[].spending.amount` | int | 22/22 | 0 | 19 | `-26200` … `6931038` |
| `accounts[].total_credits.amount` | int | 33/33 | 0 | 2 | `0`, `26200` |
| `accounts[].total_debits.amount` | int | 33/33 | 0 | 2 | `0`, `6000` |
| `accounts[].total_fees.amount` | int | 33/33 | 0 | 1 | `0` |
| `available_at` | string | 33/33 | 0 | 32 | `2024-08-01T04:02:00Z` … `2026-06-05T21:16:51Z` |
| `id` | string | 33/33 | 0 | 33 | 6-digit decimal, `152980` … `572981` |
| `pdf_url` | string | 33/33 | **0** | 3 blobs | signed GCS URL on `sandbox-statements.files.rho.co` |
| `period_end` | string | 33/33 | 0 | 29 | `2024-07-31` … `2026-05-31` |
| `period_start` | string | 33/33 | 0 | 29 | `2024-07-01` … `2026-05-01` |
| `statement_type` | string | 33/33 | 0 | 3 | `account`, `credit`, `treasury` |

The deposit-statement aggregates are essentially unexercised: `total_fees` is `0` on all 33, `total_credits` takes only `{0, 26200}` and `total_debits` only `{0, 6000}`.

**`cards`** (47 field paths; the presence-sensitive ones)

| Field path | present | null | Observed values |
|---|---|---:|---|
| `allowed_categories` / `allowed_merchants` | **1/8** | 0 | one card only |
| `blocked_categories` / `blocked_merchants` | **1/8** | 0 | a different single card |
| `billing_address` | 8/8 | 0 | always present |
| `billing_address.second_line` | **1/8** | 0 | `Floor 5` |
| `cardholder.{user_id,first_name,last_name}` | 8/8 | 0 | 8 distinct users |
| `current_spend` / `pending_spend` | 8/8 | 0 | `{amount:int, currency:"USD"}` |
| `shipping_address` | 8/8 | **4** | explicitly null on the 4 virtual cards |
| `spend_period_end` | 8/8 | **1** | null on the one `fixed` card |
| `spending_limit` / `spending_limit_type` | 8/8 | **0** | never null, so a no-limit card is untested |
| `usage_starts_at` | 8/8 | **7** | `2025-10-01T09:00:00Z` |
| `usage_ends_at` | 8/8 | **5** | `2026-06-30T23:59:59Z`, `2026-09-01T00:00:00Z` |

**`invoicing_customers`** (all 19 paths present on all 8 records; nullity carries optionality)

| Field path | present | null | Observed values |
|---|---|---:|---|
| `address.address1/city/state/zip_code` | 8/8 | 0 | 8, 8, 7, 8 distinct |
| `address.address2` | 8/8 | 0 | `<empty string>`, `Floor 2`, `Suite 400` |
| `address.country` | 8/8 | 0 | `USA` |
| `cc_emails` | 8/8 | 0 | lengths 0 ×4, 1 ×2, 2 ×2 |
| `deleted_at` | 8/8 | **7** | `2026-05-01T12:00:00Z` |
| `email` | 8/8 | **1** | 7 distinct |
| `last_invoice_id` | 8/8 | **1** | 7 distinct |
| `note` | 8/8 | **4** | 4 distinct |
| `total_revenue.amount` | 8/8 | 0 | `0`, `5000`, `43400`, `108403`, `156750` |

> **Divergence:** `api/invoicing_listinvoicingcustomers.md` marks `email` and `last_invoice_id` as `required`. Both are `null` on customer `…006` (Cedar & Co). The OpenAPI "required" marker here means "the key is always present," not "the value is non-null."

**`invoicing_invoices`** (39 paths; the presence-sensitive ones)

| Field path | present | null | Observed values |
|---|---|---:|---|
| `accounting_synced_at` | 12/12 | **5** | 7 distinct timestamps |
| `activities` | 12/12 | 0 | lengths 2 ×3, 3 ×4, 4 ×2, 5 ×1, 6 ×1, 7 ×1 (44 total) |
| `activities[].user_id` | 44/44 | **12** | `40000000-…0000001/2/3` only |
| `due_date` | 12/12 | **0** | 12 distinct |
| `file_id` | **9/12** | 0 | `50000000-…0000020` … `…0000028` |
| `line_items[].quantity` | 16/16 | 0 | `1`, `2`, `2.5`, `3` (float and int) |
| `line_items[].tax_rate` | 16/16 | **10** | `0`, `6.25`, `8.5`, `10` |
| `note` | 12/12 | **3** | 9 distinct, one containing a literal U+2014 |
| `payments` | 12/12 | 0 | lengths 0 ×5, 1 ×7 |
| `payments[].external_method` | 7/7 | **2** | `cash`, `check`, `credit_card`, `other` |
| `payments[].transaction_id` | 7/7 | **5** | two UUIDv7 ids that resolve into `/transactions` |
| `tax_rate` | 12/12 | 0 | `0`, `6.25`, `8.5`, `10` |

---

### 3.4 Sandbox versus production: the four differences that will bite you

The sandbox is a correctness environment, not a policy environment. Four differences matter more than all the rest combined.

#### 3.4.1 No scope enforcement

`docs/v1/auth` states that scopes "are enforced before your request reaches the handler" and that "a request whose token lacks the required scope is rejected with 403 Forbidden." In sandbox, no scope is ever consulted. One garbage token reads every scope family:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
T='Authorization: Bearer qqqq-garbage-token-no-scopes-at-all'
for p in accounts cards transactions statements invoicing/customers invoicing/invoices; do
  printf '%-22s ' "$p"
  curl -s -o /dev/null -w '%{http_code} %{size_download} bytes\n' "$B/$p" -H "$T"
done
```
```
accounts               200 2558 bytes
cards                  200 6357 bytes
transactions           200 13126 bytes
statements             200 28132 bytes
invoicing/customers    200 3383 bytes
invoicing/invoices     200 15390 bytes
```

**`403` is not reachable in sandbox by any means found.** Not by scope, not by IP allowlist, not by anything. Your 403 handling, your scope-error UX and your IP-rejection path are all untestable before production.

> **Divergence:** the docs describe sandbox authentication as "intentionally permissive" and say nothing at all about scopes. A reader reasonably assumes scope checks still apply. They do not. This is the largest functional gap in the sandbox.

While you are here, note a second scope problem that the sandbox cannot help you with. `docs/v1/auth` lists exactly three scopes (`accounts:read`, `transactions:read`, `statements:read`). The OpenAPI `AccessToken` scheme, the per-product docs, and the live RFC 9728 metadata at `https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` all list **five**, adding `cards:read` and `invoicing:read`. Five is authoritative. Anyone building a partner OAuth integration from `docs/v1/auth` alone will request too few. See the Authentication and Scopes section.

#### 3.4.2 No rate limiting observed

`docs/v1/rate-limits` states: "Per API Access Token: Approximately 60 requests per minute. Per source IP: Approximately 600 requests per minute," returns `429 Too Many Requests` when exceeded, and describes branch logic on a `Retry-After` header including the unusual `Retry-After: 0` case.

Measured against the sandbox, across five independent runs from one source IP:

| Run | Requests | Concurrency | Elapsed | Effective rate | Result |
|---|---:|---:|---|---|---|
| Sequential, one connection | 60 | 1 | 10.67 s | 337 req/min | 60 × `200` |
| Parallel, separate connections | 60 | 30 | 1.173 s | 51.2 req/s | 60 × `200` |
| Parallel, separate connections | 60 | 60 | 0.871 s | **68.9 req/s (4,134 req/min instantaneous)** | 60 × `200` |
| Cumulative on one token in one 57 s window | 150+ | mixed | 57 s | >150 req/min | zero `429`, zero `5xx` |
| Sequential on a **brand-new, never-used token** | 65 | 1 | 11.30 s | 345 req/min | 65 × `200` |
| Burst to `/transactions` | 300 | 20 | 4 s | ~3,600 req/min | 300 × `200` |
| Unauthenticated burst | 75 | 1 | 17 s | ~265 req/min | 75 × `401` |
| Spot check re-run at the end of the probe window | 30 | 1 | 9 s | 200 req/min | 30 × `200` |

**Zero `429` responses across approximately 430 requests in 10.5 minutes**, including a sustained run at 2.5× the documented per-token allowance and an instantaneous burst at roughly 69× it. The fresh-token run rules out the possibility that the literal string `sandbox` is simply allowlisted.

No rate-limit headers exist on any response, on any status. No `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `X-RateLimit-*`, `RateLimit-Policy` or `Retry-After` was observed in any of roughly 430 captured responses. The complete header set on a `200` is ten headers and nothing else:

```
HTTP/2 200
date: Sat, 12 Sep 2026 00:27:36 GMT
content-type: application/json
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: a39ac991ab8caf79-EWR
```

> **Divergence:** `docs/v1/rate-limits` gives concrete thresholds with no environment qualifier, and reads as if it applies to both environments. It does not apply to the sandbox at any load this probe could responsibly generate. This is the single most load-bearing unstated caveat on that page.

> **Divergence:** the rate-limits page asserts that `429` is part of the API's behaviour, but **no OpenAPI operation page documents a `429` response**. All 14 operations list `200, 400, 401, 403, 500, 503`, and the 6 single-resource getters and the 2 file endpoints add `404`. A client generated from the OpenAPI document will treat `429` as an unexpected status. Add the case by hand.

Two things follow. You cannot test your backoff code against Rho at all: `429` is unreachable in sandbox, and probing production for it with a real token is an obviously bad idea. Write the retry path blind, unit-test it against synthetic responses, and handle a `429` that arrives with **no** `Retry-After` header, because nothing guarantees one. And do not size your client against sandbox capacity: build to the documented ~60 req/min per token, treat sandbox as a correctness environment only, and self-throttle open-loop because there is no feedback signal to pace against.

The per-source-IP limit of ~600 req/min was deliberately not probed. Reaching it would require a sustained flood against a shared multi-tenant sandbox. It is neither confirmed nor refuted.

#### 3.4.3 No MCP endpoint on the sandbox host

`docs/v1/mcp` documents `https://rhoapi.rho.co/mcp/v1` as the MCP surface, asserts that MCP "uses the same API contract, authentication model, scopes, and error behavior as the REST API," and gives a `claude mcp add` example pointing at production. It never says the sandbox lacks an MCP surface.

| Request | Sandbox | Production |
|---|---|---|
| `GET /mcp/v1` | `404` `default backend - 404` (ingress default backend, the route does not exist) | `401 application/problem+json` with `WWW-Authenticate` |
| `POST /mcp/v1` (JSON-RPC `initialize`) | `404` `default backend - 404` | `401` same body |
| `GET /mcp` | `404` `default backend - 404` | not probed |
| `GET /api/v1/mcp` | `404 page not found` (Go router reached, no route) | not probed |
| `GET /.well-known/oauth-protected-resource/mcp/v1` | `404` `default backend - 404` | `200` with the five scopes |

```bash
curl -s -w ' [%{http_code}]\n' https://rhoapi-sandbox.rho.co/mcp/v1 \
  -H 'Authorization: Bearer sandbox'
# -> default backend - 404 [404]

curl -s -D- -o /dev/null https://rhoapi.rho.co/mcp/v1 | grep -Ei '^(HTTP|www-authenticate)'
# -> HTTP/2 401
#    www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"
```

> **Divergence:** MCP cannot be exercised without a production token. There is no sandbox MCP host, no alternate path, and no statement anywhere in the docs that MCP is production-only. An integrator following the docs' sandbox-first advice and substituting the sandbox host into the MCP URL by analogy hits a bare `404` with no explanation.

There is a second, subtler divergence visible from the outside. The production MCP 401 body and the REST 401 body carry identical keys and values but in different serialization orders, and only MCP sends `WWW-Authenticate`:

```
REST /api/v1/accounts : {"type":"2","title":"Unauthenticated","status":401}   md5 a9b8c917cbc1e5b43579afaee5ccadd5
MCP  /mcp/v1          : {"status":401,"title":"Unauthenticated","type":"2"}   md5 bd60dba151c99a7227902eb6dd9a3738
```

Two serializers, therefore two implementations, behind a claim of 1:1 parity. Any client comparing error bodies byte-wise or by hash across the two surfaces will see a difference where none is semantically intended. See the MCP section.

#### 3.4.4 Production and sandbox return byte-identical 401 bodies

This is the one that costs people an afternoon.

```bash
curl -s -o /tmp/sb401.json  https://rhoapi-sandbox.rho.co/api/v1/accounts
curl -s -o /tmp/pr401.json  https://rhoapi.rho.co/api/v1/accounts
cmp /tmp/sb401.json /tmp/pr401.json && echo 'BYTE-IDENTICAL'
openssl md5 /tmp/sb401.json /tmp/pr401.json
```
```
BYTE-IDENTICAL
MD5(/tmp/sb401.json)= a9b8c917cbc1e5b43579afaee5ccadd5
MD5(/tmp/pr401.json)= a9b8c917cbc1e5b43579afaee5ccadd5
```

Same 52 bytes, same md5. The response headers are identical too, modulo `date` and `cf-ray`:

```bash
curl -s -D /tmp/hs.txt -o /dev/null https://rhoapi-sandbox.rho.co/api/v1/accounts
curl -s -D /tmp/hp.txt -o /dev/null https://rhoapi.rho.co/api/v1/accounts
diff <(grep -viE '^(date|cf-ray)' /tmp/hs.txt) <(grep -viE '^(date|cf-ray)' /tmp/hp.txt) \
  && echo 'HEADERS IDENTICAL'
# -> HEADERS IDENTICAL
```

Both hosts resolve to the same Cloudflare anycast pair (`104.18.26.176`, `104.18.27.176`), both sit behind the same Google-fronted origin stack, and both carry the same ten-header set. **There is no environment marker anywhere in any response.** No `X-Rho-Environment`, no sandbox flag in the problem document, no distinct `type` code, no difference in the `server` or `via` headers.

> **Divergence:** the documented sandbox posture is "any non-empty bearer token is accepted." A developer who typoes `RHO_API_BASE_URL` and points at production gets exactly the 401 a bad sandbox token would produce, and will reasonably conclude the *token* is wrong rather than the *host*. The docs never warn about this.

The defence is cheap: assert on the host in your client configuration, and log it on every failure.

```python
import os, urllib.parse

BASE = os.environ["RHO_API_BASE_URL"]
EXPECTED_HOST = os.environ.get("RHO_EXPECTED_HOST", "rhoapi-sandbox.rho.co")

host = urllib.parse.urlparse(BASE).netloc
if host != EXPECTED_HOST:
    raise SystemExit(f"refusing to run: base URL host is {host!r}, expected {EXPECTED_HOST!r}")
```

#### 3.4.5 Everything else that differs or is untestable

| Surface | Sandbox | Production | Documented? |
|---|---|---|---|
| Auth | any non-empty bearer | real `rhobat_` token | yes |
| Scopes | not enforced, `403` unreachable | enforced per the docs | **no** |
| Rate limits | not enforced up to 68.9 req/s, `429` unreachable | unprobed | **no** |
| `/mcp/v1` | route does not exist | exists, demands auth | **no** |
| `401` body and headers | identical to production | identical to sandbox | **no** |
| Edge IPs | `104.18.26.176`, `104.18.27.176` | the same pair | no |
| Error body families | identical | identical (on the paths reachable unauthenticated) | partially |
| IP allowlist rejection | no mechanism | documented | untestable |
| `500` / `503` | never observed | documented per operation | untestable |
| Token revocation and expiry | no token registry | documented (45-day inactivity, 1-year max) | untestable |

Of the five error responses the OpenAPI documents per operation, **three (`403`, `500`, `503`) are unreachable in sandbox**, and `401` is reachable only by deliberately breaking your own header.

---

### 3.5 Worked examples

Everything below runs as written against the live sandbox. Set these once:

```bash
export RHO_BASE=https://rhoapi-sandbox.rho.co/api/v1
export RHO_AUTH='Authorization: Bearer sandbox'
```

Send `Accept-Encoding: gzip` explicitly in anything you build. gzip is the only encoding served (brotli, zstd, deflate and `Accept-Encoding: *` all return identity), and it cuts a 40,768-byte transactions page to roughly 5.6 to 6.0 KB, a 7× saving. `curl --compressed` does this for you.

#### 3.5.1 List every resource

```bash
curl -s --compressed "$RHO_BASE/accounts"            -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/cards"               -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/transactions"        -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/statements"          -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/invoicing/customers" -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/invoicing/invoices"  -H "$RHO_AUTH" | python3 -m json.tool | head -20
```

The envelope is always `{"<resource_key>": [...], "page": {"next_page_token": string|null}}`. The resource key is **not** the path: `/invoicing/customers` returns the bare key `customers` and `/invoicing/invoices` returns `invoices`.

| Endpoint | Resource key | Rows | Default page size | Default ordering (observed) |
|---|---|---:|---|---|
| `/accounts` | `accounts` | 14 | 20 (unobservable, dataset is smaller) | `account_name` ascending |
| `/cards` | `cards` | 8 | 20 (unobservable) | card id order |
| `/transactions` | `transactions` | 72 | **20, proven** | `initiated_at` descending |
| `/statements` | `statements` | 33 | **20, proven** | `period_end` descending |
| `/invoicing/customers` | `customers` | 7 | 20 (unobservable) | `created_at` descending |
| `/invoicing/invoices` | `invoices` | 12 | 20 (unobservable) | `created_at` descending |

`/accounts` is the only endpoint whose default sort is discoverable from the API itself, because its cursor payload spells it out (§3.5.3). The docs never state it.

#### 3.5.2 Page a resource explicitly

```bash
# page_size is bounded [1, 100] on every endpoint
curl -s "$RHO_BASE/transactions?page_size=1"   -H "$RHO_AUTH" | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]))'   # 1
curl -s "$RHO_BASE/transactions?page_size=100" -H "$RHO_AUTH" | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]))'   # 72
```

Changing `page_size` mid-walk is safe, because `page_size` is deliberately excluded from the cursor's filter fingerprint. Changing a **filter** mid-walk is not, and returns `400`. Neither fact appears in the docs.

#### 3.5.3 Follow a cursor to exhaustion

The canonical loop, which works verbatim on all six endpoints:

```python
#!/usr/bin/env python3
"""Walk any Rho list endpoint to exhaustion. Usage: walk.py transactions transactions"""
import json, os, sys, time, urllib.request, urllib.parse

BASE  = os.environ.get("RHO_BASE", "https://rhoapi-sandbox.rho.co/api/v1")
TOKEN = os.environ.get("RHO_TOKEN", "sandbox")

def get(path, params):
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept-Encoding": "gzip",
    })
    with urllib.request.urlopen(req) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip
            raw = gzip.decompress(raw)
        return json.loads(raw)

def walk(path, key, page_size=100, **filters):
    """Yield every record. Filters must stay byte-identical across pages."""
    token, seen = None, 0
    while True:
        params = dict(filters, page_size=page_size)
        if token:
            params["page_token"] = token
        body = get(path, params)
        rows = body[key]
        seen += len(rows)
        yield from rows
        token = body["page"]["next_page_token"]   # present always, null on the last page
        if token is None:
            return
        time.sleep(1.0)   # self-throttle: ~60 req/min, the documented production budget

if __name__ == "__main__":
    path, key = sys.argv[1], sys.argv[2]
    rows = list(walk(path, key))
    ids  = [r["id"] for r in rows]
    print(f"{path}: {len(rows)} records, {len(set(ids))} distinct ids")
```

```bash
python3 walk.py transactions transactions        # transactions: 72 records, 72 distinct ids
python3 walk.py statements statements            # statements: 33 records, 33 distinct ids
python3 walk.py invoicing/customers customers    # invoicing/customers: 7 records, 7 distinct ids
```

Three properties of the termination condition, all verified by walking every endpoint at `page_size` 1, 3, 7 and 100:

- `page.next_page_token` is **always present** and is either a string or JSON `null`. It is never an empty string and never omitted. The API reference types it as `string, required`, which a strict schema validator will reject on the terminal page.
- The concatenated id sequence is byte-for-byte identical at every page size, with no duplicates and no skips.
- When the row count divides evenly into `page_size`, the last full page still carries a token and the next request returns an empty array with a null token. `/cards?page_size=4` (total 8) returns 4 rows **with** a token on page 1.

The cursor is not opaque in practice, which is worth seeing once so you know what you are carrying:

```bash
T=$(curl -s "$RHO_BASE/transactions?page_size=5" -H "$RHO_AUTH" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["page"]["next_page_token"])')
echo "$T"
python3 - "$T" <<'PY'
import base64, json, sys
d = lambda s: base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
env = json.loads(d(sys.argv[1]))
print(env)
print("inner:", d(env["t"]))
PY
```
```
eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qVSJ9
{'v': 1, 'f': 't0HwRhJ0BSGWYAjAT5bQKg', 't': 'b2Zmc2V0OjU'}
inner: b'offset:5'
```

The same on `/accounts`:

```
{'v': 1, 'f': 'SigraTvwZG8Dd7QLdKJzPA', 't': 'eyJsYXN0X2lkIjoiMzAwMDAwMDAtMDAwMC00MDAwLTgwMDAtMDAwMDAwMDAwMDAzIiwic29ydF9ieSI6ImFjY291bnRfbmFtZSIsIm9yZGVyIjoiYXNjIn0'}
inner: b'{"last_id":"30000000-0000-4000-8000-000000000003","sort_by":"account_name","order":"asc"}'
```

| Endpoint | Inner cursor | Strategy |
|---|---|---|
| `/transactions`, `/statements`, `/cards`, `/invoicing/customers`, `/invoicing/invoices` | `offset:N` | **offset** |
| `/accounts` | `{"last_id":…,"sort_by":"account_name","order":"asc"}` | **keyset** |

> **Divergence:** `docs/v1/pagination` states without qualification that "cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." Five of six endpoints return a plain absolute offset, which cannot deliver that guarantee: an insert or delete before the current offset shifts every subsequent row. Only `/accounts` uses a keyset cursor that structurally can. The sandbox dataset is static so the shift cannot be forced here, but the mechanism is dispositive.

> **Divergence:** the same page describes cursors as "opaque" whose "format and lifetime are not part of the API contract," and prints an example token that decodes to `{"o":100,"d":"2026-05-14"}`. Real tokens decode to `{"v":1,"f":…,"t":…}`. The documented shape matches nothing the API emits.

Cursor binding, probed directly:

| Action | Result |
|---|---|
| pass a `/transactions` token to `/statements` | `400` `page_token must be a valid cursor` |
| pass a token back with a **different `page_size`** | **`200`**, works fine |
| pass a token back with an **added filter** (`status=settled`) | `400` |
| pass a token back with the **explicit default** (`sort_by=initiated_at&order=desc`) | `200`, values are canonicalized before hashing |
| pass a token back with `order=asc` changed to `order=ASC` | **`400`**, identical rows, incompatible cursors |
| pass a token back with a duplicated identical enum value | **`400`** |
| pass a token back with an added unknown parameter | `200` |
| `page_token=` (empty string) | `200`, treated as page one |
| garbage string | `400` `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |

Tokens minted at 19:22Z still resolved at 00:03Z the next day, about 4 h 41 m later, with no expiry observed.

#### 3.5.4 Fetch a single record

```bash
curl -s "$RHO_BASE/accounts/30000000-0000-4000-8000-000000000002"     -H "$RHO_AUTH"
curl -s "$RHO_BASE/cards/20000000-0000-4000-8000-000000000001"        -H "$RHO_AUTH"
curl -s "$RHO_BASE/transactions/019f0554-0bf0-7000-8000-00000000000a" -H "$RHO_AUTH"
curl -s "$RHO_BASE/statements/572981"                                 -H "$RHO_AUTH"
curl -s "$RHO_BASE/invoicing/customers/60000000-0000-4000-8000-000000000001" -H "$RHO_AUTH"
curl -s "$RHO_BASE/invoicing/invoices/70000000-0000-4000-8000-000000000001"  -H "$RHO_AUTH"
```

Detail responses are the **bare resource object with no envelope and no `page` key**, confirmed on all 147 detail fetches.

**The detail surface returns exactly the same field set as the list surface for every one of the six resources.** 14/14 accounts, 8/8 cards, 72/72 transactions, 33/33 statements, 7/7 customers (8/8 with include_deleted=true), 12/12 invoices: identical field paths, identical presence, identical nullity, zero value differences. There is no expanded detail representation.

```bash
# Prove it for one account
A=30000000-0000-4000-8000-000000000002
diff <(curl -s "$RHO_BASE/accounts" -H "$RHO_AUTH" \
        | python3 -c "import sys,json;d=json.load(sys.stdin)['accounts'];print(json.dumps([a for a in d if a['id']=='$A'][0],sort_keys=True,indent=2))") \
     <(curl -s "$RHO_BASE/accounts/$A" -H "$RHO_AUTH" \
        | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin),sort_keys=True,indent=2))") \
  && echo 'IDENTICAL'
```

Looping single GETs to "enrich" list rows is pure waste, and at ~60 req/min per token in production it is the fastest way to burn your budget for no gain. The only reason to call `GET /{id}` is to refresh a signed `pdf_url` on a statement, and even that is subject to a server-side signing cache (§3.5.5).

One trap on the transaction detail route. `GET /transactions/{id}` accepts an optional `account_id` query parameter that the docs describe only as "Account ID for the transaction." It is not a hint, it is an **assertion filter**:

| Request | Status |
|---|---|
| `?account_id=<the transaction's real account>` | `200`, full body |
| `?account_id=<a different real account>` | **`404` `transaction not found`** |
| `?account_id=abc` | `400 invalid parameter: account_id` |

Passing a stale or guessed `account_id` makes an existing transaction vanish. The docs do not say this. Omit the parameter unless you are certain.

#### 3.5.5 Fetch a file and its signed URL

Find a transaction with an attachment, exchange the `file_id` for a signed URL, then download it:

```bash
read TID FID FN < <(
  curl -s "$RHO_BASE/transactions?page_size=100" -H "$RHO_AUTH" | python3 -c '
import sys, json
for t in json.load(sys.stdin)["transactions"]:
    if t["attachments"]:
        a = t["attachments"][0]
        print(t["id"], a["file_id"], a["file_name"]); break
')
echo "$TID $FID $FN"
# 019f0554-0bf0-7000-8000-00000000000a 2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15 parking-receipt.pdf

curl -s "$RHO_BASE/transactions/$TID/files/$FID" -H "$RHO_AUTH" | python3 -m json.tool
```
```json
{
    "download_url": "https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=file-service%40pledge-218909.iam.gserviceaccount.com%2F20260912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260912T002649Z&X-Goog-Expires=899&X-Goog-Signature=092cde4c…&X-Goog-SignedHeaders=host",
    "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15",
    "file_name": "parking-receipt.pdf"
}
```

The response is exactly three keys. There is no size, MIME type, upload timestamp or uploader. Now download it, with **no** `Authorization` header, because the signature is the credential:

```bash
U=$(curl -s "$RHO_BASE/transactions/$TID/files/$FID" -H "$RHO_AUTH" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["download_url"])')
curl -s -o /tmp/attachment.pdf -w 'status=%{http_code} type=%{content_type} bytes=%{size_download}\n' "$U"
head -c 8 /tmp/attachment.pdf; echo
```
```
status=200 type=application/pdf bytes=769
%PDF-1.4
```

Signed URL anatomy, identical on both file classes:

| Component | Value |
|---|---|
| Host, transaction attachments | `rho-api-sandbox.files.rho.co` |
| Host, statement PDFs | `sandbox-statements.files.rho.co` |
| Path | `/{24 hex chars}.{ext}`, content-addressed, no account or transaction identifier |
| `X-Goog-Algorithm` | `GOOG4-RSA-SHA256` |
| `X-Goog-Credential` | `file-service@pledge-218909.iam.gserviceaccount.com/YYYYMMDD/auto/storage/goog4_request` |
| `X-Goog-Date` | signing instant, second granularity |
| `X-Goog-Expires` | **`899`** seconds (14 min 59 s), on every URL observed |
| `X-Goog-SignedHeaders` | `host` |

The expiry rule is exactly `X-Goog-Date + X-Goog-Expires`, enforced by Google Cloud Storage. Both values are readable from the URL with no network call, so parse them to decide whether a URL is still worth attempting rather than discovering expiry from a failed download. Tampering behaves as you would expect: altering the last hex character of the signature gives `403 SignatureDoesNotMatch`, stripping the query string gives `403 AccessDenied`, and forcing `X-Goog-Expires=1` gives `400 ExpiredToken` with the exact deadline in the message. The URLs are not single-use, they honour `HEAD`, and they honour `Range` (a `Range: bytes=0-9` returns `206` with 10 bytes).

Two asymmetries matter:

- **Transaction attachment URLs are minted fresh on every request**, always with a full 899 s window. The docs are accurate here.
- **Statement `pdf_url` values are served from a roughly 300 s server-side signing cache**, keyed on the PDF blob rather than the statement. Repeated `GET /statements/{id}` inside that window returns a byte-identical URL. Because the cache rotates roughly 10 minutes before expiry, residual life is bounded between about 599 s and 899 s, with an observed minimum of 606 s.

> **Divergence:** `api/statements_getstatement.md` says "if the link lapses, re-fetch the statement with `GET /statements/{id}` to obtain a fresh URL." Re-fetching does not mint a URL on demand; it returns whatever the cache holds. Because the cache always rotates well before expiry the remedy usually works in practice, but not by the mechanism described, and **a client cannot force a re-sign**. On a `400 ExpiredToken`, back off past the ~300 s cache TTL rather than retrying tightly.

Also note that a single `/statements` list response can carry URLs signed at three different instants, because the 33 statements resolve to only three distinct PDF blobs and each blob has its own cache entry. And the GCP project name `pledge-218909` leaks in the credential parameter of every signed URL Rho issues.

**Invoice files are broken in the sandbox.** All nine invoices that expose a `file_id` return `404` from the endpoint the docs instruct you to call:

```bash
curl -s -w ' [%{http_code}]\n' \
  "$RHO_BASE/invoicing/invoices/70000000-0000-4000-8000-000000000010/files/50000000-0000-4000-8000-000000000027" \
  -H "$RHO_AUTH"
# -> {"type":"1303","title":"invoice file not found","status":404} [404]
```

> **Divergence:** `docs/v1/invoicing` says "when an invoice has a PDF, `file_id` is present. Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`," and `api/invoicing_getinvoicinginvoicefile.md` adds that `file_id` "must match `invoice.file_id` from list or get when that field is set." Doing exactly that returns 404 on all 9. The route itself is wired up (a malformed `file_id` returns `400`, proving the handler runs), so this is a fixture-data gap. **Invoice PDF retrieval cannot be integration-tested against this sandbox at all.**

#### 3.5.6 Trigger each error class deliberately

Every error class the sandbox can produce, with the exact request that produces it. Run the whole block to populate your test fixtures.

```bash
# 401  missing credential (problem+json, 52 bytes)
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts"

# 400  type-binding failure, "about:blank" family with a `detail` field. PRE-AUTH.
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts?page_size=abc"  -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts/not-a-uuid"     -H "$RHO_AUTH"

# 400  semantic validation, "1317" family with no `detail` field. POST-AUTH.
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/transactions?page_size=101"    -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/transactions?page_token=garbage" -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts?order=ASC"             -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts?sort_by=bogus"         -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/cards?status=bogus"             -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/transactions?min_amount=10000&max_amount=-10000" -H "$RHO_AUTH"

# 404  unknown id, "1303" family
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts/00000000-0000-4000-8000-000000000000" -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/statements/999999" -H "$RHO_AUTH"

# 404  unknown route, text/plain, NOT problem+json
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/webhooks" -H "$RHO_AUTH"

# 404  outside the mount point, ingress default backend, text/plain
curl -s -w ' [%{http_code}]\n' https://rhoapi-sandbox.rho.co/mcp/v1 -H "$RHO_AUTH"

# 405  write method, EMPTY body, `allow: GET`
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$RHO_BASE/accounts" \
  -H "$RHO_AUTH" -H 'Content-Type: application/json' -d '{}'

# 405  HEAD is not supported even though GET is
curl -s -o /dev/null -w '%{http_code}\n' -I "$RHO_BASE/accounts" -H "$RHO_AUTH"

# 411  POST with no Content-Length, HTML from the Google frontend
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$RHO_BASE/accounts" -H "$RHO_AUTH"
```

Observed output:

```
{"type":"2","title":"Unauthenticated","status":401} [401]
{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"} [400]
{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"} [400]
{"type":"1317","title":"page_size must be between 1 and 100","status":400} [400]
{"type":"1317","title":"page_token must be a valid cursor","status":400} [400]
{"type":"1317","title":"invalid order parameter: \"ASC\"","status":400} [400]
{"type":"1317","title":"invalid sort_by parameter: \"bogus\"","status":400} [400]
{"type":"1317","title":"invalid status parameter: \"bogus\"","status":400} [400]
{"type":"1317","title":"min_amount must be less than or equal to max_amount","status":400} [400]
{"type":"1303","title":"account not found","status":404} [404]
{"type":"1303","title":"statement not found","status":404} [404]
404 page not found [404]
default backend - 404 [404]
405
405
411
```

The complete error taxonomy reachable from the sandbox:

| Class | Status | `Content-Type` | Body | `detail`? |
|---|---|---|---|---|
| Missing or malformed credential | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` | no |
| Unknown id on a detail route | `404` | `application/problem+json` | `{"type":"1303","title":"<resource> not found","status":404}` | no |
| Parameter fails type binding (pre-auth) | `400` | `application/problem+json` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: X"}` | **yes** |
| Parameter fails a rule (post-auth) | `400` | `application/problem+json` | `{"type":"1317","title":"<message>","status":400}` | no |
| Unknown path under `/api/v1` | `404` | `text/plain; charset=utf-8` | `404 page not found` | **not a problem document** |
| Path outside `/api/v1` | `404` | `text/plain; charset=utf-8` | `default backend - 404` | **not a problem document** |
| Wrong method | `405` | *(none)* | *(empty, `content-length: 0`)*, `allow: GET` | **not a problem document** |
| `POST`/`PUT` with no `Content-Length` | `411` | `text/html; charset=UTF-8` | Google frontend page | **not a problem document** |
| URI over ~8 KB | `414` | `text/html` | nginx page | **not a problem document** |
| `Authorization` header over 8,190 bytes | `400` | `text/html` | nginx page | **not a problem document** |
| Duplicate `Authorization` header | `400` | `text/html` | Cloudflare page | **not a problem document** |
| Nonstandard method token (`FOO`) | `403` | `text/html; charset=UTF-8` | Cloudflare WAF block page | **not a problem document** |

**Seven of those twelve are not JSON.** Branch on `Content-Type` before parsing, always.

Two additional points on the `1303` and `1317` codes. `1303` covers at least nine distinct not-found conditions (`account`, `card`, `transaction`, `statement`, `customer`, `invoice`, `transaction file`, `invoice file`), distinguished only by the prose `title`. `1317` covers page size, cursor validity, sort field, order, card type, card status and amount ordering. Neither is precise enough to branch on, and `title` is free prose outside the versioning contract. Branch on the HTTP status code. See the Errors and Problem Details section.

Finally, note what you **cannot** trigger: `403`, `422`, `429`, `500` and `503` are all unreachable in the sandbox.

---

### 3.6 Sandbox gotchas

#### 3.6.1 Unknown query parameters are silently ignored

No endpoint ever returns `400` for an unrecognized parameter name. `limit`, `offset`, `per_page`, `size`, `pageSize`, `PAGE_SIZE`, `q`, `query`, `filter`, `expand`, `fields`, `include`, `id`, `currency`, `money_movement_id`, `timezone`, `account_id[]`, and 300 numbered junk parameters in a single URL all return a full, unfiltered `200`.

```bash
curl -s "$RHO_BASE/transactions?limit=5&offset=10&per_page=2&nonsense=x" -H "$RHO_AUTH" \
  | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]),"rows")'
# -> 20 rows
```

Twenty rows, because `limit` does nothing and the default `page_size` of 20 applied. This is exactly how a careless census concludes that the sandbox holds 20 statements rather than 33: `?limit=100` looks like it worked and quietly returns the first default page. The parameter is `page_size`, and the endpoint will never tell you otherwise.

Parameter names are also **case-sensitive** (`PAGE_SIZE` and `pageSize` are ignored), while percent-encoded names are decoded and honoured (`?page%5Fsize=3` returns 3 rows).

A related and nastier variant: **a raw semicolon makes a whole key/value pair vanish.** `?status=settled;x=1&page_size=3` silently drops the entire `status` filter and returns the default fingerprint. That is Go's `url.ParseQuery` rejecting semicolon-separated pairs, and it is a second silent-filter-loss vector.

#### 3.6.2 An empty date filter value returns 200 with zero rows

This is the most dangerous behaviour in the sandbox, because it fails silently in exactly the direction that looks like real data.

```bash
for q in 'initiated_before=' 'initiated_after=' 'posted_before=' 'status=' 'account_type='; do
  printf '%-20s ' "$q"
  curl -s "$RHO_BASE/transactions?$q" -H "$RHO_AUTH" \
    | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]),"rows")'
done
```
```
initiated_before=    0 rows
initiated_after=     20 rows
posted_before=       0 rows
status=              0 rows
account_type=        0 rows
```

The mechanism: an empty date string is coerced to the zero time `0001-01-01T00:00:00Z`. `field >= zero` is universally true, so every `*_after=` is a no-op. `field < zero` is universally false, so every `*_before=` empties the result set. An empty enum string becomes a literal filter value that matches nothing.

The complete empty-value table, which is worth pinning above your desk:

| Parameter | Empty value result |
|---|---|
| `initiated_after=`, `posted_after=`, `period_end_after=`, `period_start_after=`, `date_after=`, `due_date_after=` | **ignored**, full result set |
| `initiated_before=`, `posted_before=`, `period_end_before=`, `period_start_before=`, `date_before=`, `due_date_before=` | **`200` with 0 rows** |
| `account_type=`, `transaction_type=`, `status=`, `statement_type=` | **`200` with 0 rows** |
| `account_id=`, `user_id=`, `card_id=` | `400` |
| `page_size=`, `min_amount=`, `max_amount=` | `400` |
| `include_deleted=` | `400` |
| `search=`, `search=%20` | ignored, full result set |
| `page_token=` | ignored, page one |
| `sort_by=` | `/accounts` and `/invoicing/customers`: `400`. `/transactions` and `/statements`: accepted, no effect |

A templated URL with an undefined variable produces an empty page, not an error, and your reconciliation job reports "no activity." **Build the query string conditionally.** Never interpolate a possibly-empty value into a `*_before` parameter.

The corollary is that `200 []` is ambiguous between "no matching data" and "your filter was silently dropped or nullified." When a filtered result comes back empty, assert against an unfiltered control query before believing it.

#### 3.6.3 `page_size` is bounded [1, 100] with error type `1317`

Probed exhaustively on `/transactions`, then confirmed identical on all six endpoints.

| `page_size` | Status | Body |
|---|---|---|
| `1` .. `100` | `200` | normal |
| `0`, `-1`, `-5`, `-0`, `101`, `150`, `200`, `1000`, `10000`, `999999`, `99999999999999999999` | `400` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| `abc`, `1.5`, `2.0`, `1e2`, `0x10`, `true`, `null`, `%20`, `3#`, empty, duplicated | `400` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}` |
| `%2B3` (leading `+`) | `200` | parsed as **3** |
| `03` (leading zero) | `200` | parsed as **3** |
| `page_size[]=5` (bracket syntax) | `200` | key ignored, falls back to the default 20 |

Note the split: a value that parses as an integer but falls outside the range gets the `1317` family, and a value that does not parse at all gets the `about:blank` family with a `detail` field. Two different producers, two different shapes, one HTTP status.

> **Divergence:** `docs/v1/pagination` says only that "values outside the allowed range return `400 Bad Request`." It does not distinguish the two error shapes, does not state the minimum, and the API reference pages for `/cards`, `/invoicing/customers` and `/invoicing/invoices` say only "Defaults to 20" without naming a maximum. The enforced range is `[1, 100]` uniformly, discoverable only by probing.

#### 3.6.4 Validation is inconsistent across endpoints

This is the deepest gotcha, because it means you cannot learn one rule and apply it everywhere.

**Enum filter validation.** Three endpoints reject a bad value and three accept it and return zero rows:

| Probe | Result |
|---|---|
| `/cards?status=bogus` | `400` `{"type":"1317","title":"invalid status parameter: \"bogus\"","status":400}` |
| `/cards?type=plastic` | `400` `invalid type parameter: "plastic"` |
| `/transactions?status=bogus` | **`200`, 0 rows** |
| `/transactions?account_type=CHECKING` | **`200`, 0 rows** (case-sensitive) |
| `/transactions?account_type=treasury` | **`200`, 0 rows** (valid for statements, not for transactions) |
| `/statements?statement_type=monthly` | **`200`, 0 rows** |
| `/invoicing/invoices?status=draft` | **`200`, 0 rows** |
| `/invoicing/invoices?status=canceled` | **`200`, 0 rows** (the enum value is `cancelled`) |

`/cards` is the only endpoint that strictly validates its enum filters. Validate enum values client-side before sending, or the API will happily tell you there is no data.

**`sort_by` validation.** Four different behaviours across six endpoints:

| Endpoint | Validates `sort_by`? | Accepted values | Does it actually sort? | Default |
|---|---|---|---|---|
| `/accounts` | **yes, 400 on unknown** | only `balance`, `account_name` | yes | `account_name` asc |
| `/invoicing/customers` | **yes, 400 on unknown** | only `created_at` | yes | `created_at` desc |
| `/transactions` | no, silently ignores | any string returns 200 | yes for `amount`, `initiated_at`, `posted_at`; anything else falls back to the default | `initiated_at` desc |
| `/statements` | no, silently ignores | any string returns 200 | **no, nothing changes the order** | `period_end` desc |
| `/cards` | no, not parsed at all | any string returns 200 | not exercised (8 rows) | id order |
| `/invoicing/invoices` | no, not parsed at all | any string returns 200 | not exercised (12 rows) | `created_at` desc |

A typo in `sort_by` fails loudly on two endpoints and silently on four.

> **Divergence:** `/statements` advertises `sort_by` in its OpenAPI definition and its query-parameter table. No value has any observable effect: `period_end`, `period_start`, `available_at` and `bogus` all return the identical sequence. Only `order` does anything.

> **Divergence:** `/invoicing/customers` documents `sort_by` as "Sort field. Defaults to `created_at` when omitted." `created_at` is the only accepted value, and every other value returns `400`. The parameter can only fail, never do anything useful.

`order` is validated wherever it is parsed, and only lowercase `asc` and `desc` are accepted on `/accounts` and `/invoicing/customers`. On `/transactions` and `/statements`, `order=bogus` is a silent no-op that falls back to `desc`, while `order=ASC` is honoured in effect but hashed case-sensitively into the cursor fingerprint, so it breaks any token you carry across it.

**Date parameter semantics.** Three endpoints, three different contracts:

| Endpoint | Parameters | Accepted formats | `after` | `before` |
|---|---|---|---|---|
| `/transactions` | `initiated_after/before`, `posted_after/before` | `2026-01-01`, `2026-01-01T00:00:00Z`, `2026-01-01T00:00:00+00:00`, `2026-01-01T00:00:00.000Z` | inclusive | **exclusive** |
| `/statements` | `period_end_after/before`, `period_start_after/before` | **`2026-01-01` only**, any timestamp form is a `400` | inclusive | **exclusive** |
| `/invoicing/invoices` | `date_after/before`, `due_date_after/before` | **`2026-01-01` only** | inclusive | **inclusive** |

```bash
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/statements?period_end_after=2026-01-01T00:00:00Z" -H "$RHO_AUTH"
# -> {"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: period_end_after"} [400]

curl -s "$RHO_BASE/transactions?page_size=100&initiated_after=2026-01-01T00:00:00Z" -H "$RHO_AUTH" \
  | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]),"rows")'
# -> 47 rows
```

The same ISO-8601 timestamp that works on `/transactions` is a `400` on `/statements`. And the `before` bound is exclusive on two endpoints and inclusive on the third.

**Amount filters.** `min_amount` and `max_amount` compare the **signed** amount, not the absolute value, so `min_amount=0` selects the 32 credits and `max_amount=0` selects the 40 debits. Bounds are inclusive on both ends. The parameter docs say only "minimum amount in minor units" without mentioning sign. This is also the only cross-field validation in the whole API: an inverted amount range is a `400`, while an inverted **date** range is a `200` with zero rows.

**Detail routes.** Malformed ids are a `400` on five resources and a `404` on the sixth:

| Path | Malformed id | Unknown id |
|---|---|---|
| `/accounts/{account_id}` | `400 invalid parameter: account_id` | `404 account not found` |
| `/cards/{id}` | `400 invalid parameter: id` | `404 card not found` |
| `/transactions/{id}` | `400 invalid parameter: id` | `404 transaction not found` |
| `/invoicing/customers/{id}` | `400 invalid parameter: customer_id` | `404 customer not found` |
| `/invoicing/invoices/{id}` | `400 invalid parameter: invoice_id` | `404 invoice not found` |
| **`/statements/{id}`** | **`404 statement not found`** (no format validation at all) | `404 statement not found` |

Note also that the `detail` string leaks the internal path-parameter names, and they are inconsistent: `account_id`, `customer_id`, `invoice_id`, `transaction_id` and `file_id`, but a bare `id` for cards and transactions.

#### 3.6.5 The rest of the list

**UUID parsing is lenient, so one resource has at least five URL spellings.** All of these return `200` with an identical body whose `id` is normalised to canonical lowercase-dashed form: canonical, no dashes (32 hex), brace-wrapped, `urn:uuid:`-prefixed, and uppercase hex. This is the accept-set of Go's `github.com/google/uuid`. Normalise ids yourself, or a URL-keyed cache will store up to five copies of the same record.

**`HEAD` is not supported.** `HEAD /accounts` returns `405` with `allow: GET`. RFC 9110 treats `HEAD` as expected wherever `GET` is implemented. Health checkers and monitoring tools that default to `HEAD` will report the API as broken.

**There is no CORS, at all.** `OPTIONS` returns `405` with no `Access-Control-*` headers, and a `GET` carrying an `Origin` header gets no `Access-Control-Allow-Origin` either, on any status, from any origin including `https://app.rho.co`. A browser preflight can never succeed. Combined with a long-lived opaque credential this is a correct posture, but it is stated nowhere in the docs. Proxy through your own backend.

**Conditional requests are impossible.** No `ETag`, no `Last-Modified`, no `Cache-Control`, no `Vary` is ever emitted. `If-None-Match: *`, `If-None-Match: "abc123"` and `If-Modified-Since` in both directions all return a full `200`. There is no cheap "has anything changed" primitive and no webhook surface anywhere in the corpus, so change detection means full page pulls plus client-side diffing.

**There is no request id.** Cloudflare's `cf-ray` is the only per-request correlator in any response, and it is a CDN identifier, not a Rho one. Log it on every request anyway, because it is all you will have to quote to support.

**There is no pagination metadata beyond the cursor.** No `total`, `total_count`, `has_more`, `count`, `prev_page_token` or `Link` header. You cannot show "1-20 of 347" without draining the list.

**gzip is the only compression served.** Brotli, zstd, deflate and `Accept-Encoding: *` all return identity. Name `gzip` explicitly. Note also that no `Vary: Accept-Encoding` is emitted, which is a correctness hazard for any shared cache in front of your fleet.

**`search` exists on only two endpoints and covers only some fields.** On `/transactions` it is a case-insensitive, unanchored substring over `counterparty_name`, `memo` and `note`. On `/invoicing/customers` it covers `legal_name` and `email` only, so searching for a city returns zero. SQL `LIKE` metacharacters are escaped rather than interpreted. `/cards` and `/invoicing/invoices` have no `search` at all, and `/accounts` has no filtering of any kind, so name lookups on those resources require a full walk and client-side matching.

**`include_deleted` uses Go's `strconv.ParseBool`.** It accepts `1`, `t`, `T`, `TRUE`, `true`, `True`, `0`, `f`, `F`, `FALSE`, `false`, `False`. It rejects `yes`, `on`, an empty value and a bare flag, each with a `400`. The default is `false`, and a soft-deleted customer remains fully retrievable by id regardless of the flag.

**The two "cancelled" spellings will bite a shared status mapper.** `cards.status` is `canceled`. `invoices.status` and `activities[].activity_type` are `cancelled`.

**Two country encodings and two address models coexist.** `customers.address.country` is `"USA"` (alpha-3) with `address1`/`address2`/`city`/`state`/`zip_code`. `cards.billing_address.country_code` is `"US"` (alpha-2) with `street`/`second_line`/`city`/`subdivision`/`postal_code`.

**Documented fields that never materialise.** `transactions.tracking_number` (documented in detail as an ACH NACHA trace or wire IMAD/OMAD) and `transactions.counterparty_logo_url` appear on **zero** of 72 transactions, including 11 ACH and 10 wire records. `statements.accounts[].repayment_date` appears on zero of 22 credit statements. You cannot exercise payment tracing against this sandbox.

> **Divergence:** `api/transactions_listtransactions.md` says `posted_at` is "Null while status is pending." In the sandbox, `posted_at` is present on **both** pending records and on all 61 settled and all 8 failed records, and is absent only on the single `awaiting_approval` record. It is also *absent*, never null. The operative rule is "absent while awaiting approval," and the documented rule is contradicted in both directions. `docs/v1/transactions` restates the same pending rule and then loosens it only for other statuses ("posted_at is nullable, and the contract describes it as null while the status is pending. Beyond that it is not coupled to `status`"), so the guide does not contradict the reference page. Both are contradicted by the data.

> **Divergence:** `api/statements_liststatements.md` says `accounts[].account_id` is "null for credit statements, which are not tied to a deposit account." It is never null: all 22 credit statements carry a real credit account id that resolves on `/accounts`. The same page says `accounts[]` may span multiple checking or savings accounts. Its length is **1 on all 33 records**, and the two same-period statements `439950` (checking) and `439951` (savings) exist as separate records rather than one multi-account statement, which is precisely the case the docs say would be combined.

> **Divergence:** `api/cards_listcards.md` says `spending_limit`, `spending_limit_type` and `current_spend` are null when the card has no limit. All three are non-null on all 8 cards; no limitless card exists in the fixture set. `api/invoicing_listinvoicinginvoices.md` says `due_date` is "null when not set." It is non-null on all 12.

#### 3.6.6 A checklist to work from

1. Assert on the base URL host in your client. Sandbox and production are indistinguishable on the failure path.
2. Send `Authorization: Bearer <token>` with a capital B and exactly one ASCII space.
3. Branch on `Content-Type` before parsing any error body. Seven of twelve error classes are not JSON.
4. Branch on the HTTP status, not on `type`. `1303` and `1317` are coarse families and `title` is unversioned prose.
5. Never infer authentication success from a non-401 status. Type-binding `400`s and `405`s precede auth.
6. Build the query string conditionally. An empty `*_before` value silently empties your result set.
7. Validate enum filter values client-side. Half the endpoints will not tell you.
8. Treat `200 []` as ambiguous and assert against an unfiltered control query.
9. Replay the byte-identical filter query string on every page. `page_size` may change freely; case and duplication may not.
10. Type `statements.id` as a string, never a UUID.
11. Handle key **omission** on transactions and cards, not just null. Handle null on customers and invoices, not just omission.
12. Give every enum switch a default branch. The sandbox exercises 22 of 33 transaction types, 5 of 11 card statuses and 3 of 7 spending-limit types.
13. Read direction from the sign of `amount.amount`, never from the type name.
14. Group by `money_movement_id` before presenting transfers.
15. Never loop single GETs to enrich list rows. The detail surface returns nothing extra.
16. Re-fetch signed URLs rather than caching them, and parse `X-Goog-Date + X-Goog-Expires` to know the deadline.
17. Do not build invoice PDF download against this sandbox. It 404s universally.
18. Do not test backoff, scope errors or IP rejection here. `429` and `403` are unreachable.
19. Do not size your client against sandbox capacity. Self-throttle to the documented ~60 req/min per token.
20. For MCP, target production only.
