# Rho API v1 sandbox: empirical map of query parameters and error behavior

Target: `https://rhoapi-sandbox.rho.co/api/v1`, bearer `sandbox`.
Probe date: 2026-09-11 23:42 UTC to 2026-09-12 00:08 UTC. All facts below are observed responses unless tagged `[Rho claim]` (asserted only in Rho's own docs).
Raw evidence: `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-filters/` (1,477 files: `<label>.url`, `<label>.hdr`, `<label>.body` per probe, plus two burst logs). Probe driver: `../sandbox/probe.sh`.
Documented contract read from `/private/tmp/claude-501/.../scratchpad/rho/api/*.md` (14 operation pages) and `/private/tmp/claude-501/.../scratchpad/rho/docs/*.md` (14 guide pages).

---

## 0. Headline findings for an integrator

1. **Every unknown query parameter is accepted and silently ignored.** No endpoint ever returns 400 for an unrecognized parameter name. `limit`, `offset`, `per_page`, `size`, `pageSize`, `PAGE_SIZE`, `q`, `query`, `filter`, `expand`, `fields`, `include`, `id`, `currency`, `money_movement_id`, `timezone`, `account_id[]`, and 300 junk params in one URL all return a full unfiltered 200.
2. **An empty value on any `*_before` date parameter silently returns zero rows.** `?date_before=`, `?posted_before=`, `?period_end_before=`, `?due_date_before=`, `?initiated_before=` all return `200` with an empty array. The matching `*_after=` parameters are ignored instead. This is the single most dangerous behavior found: a templated URL with an undefined variable produces an empty result set, not an error.
3. **Enum filter validation is inconsistent across endpoints.** `/cards` rejects a bad `type` or `status` with `400`. `/transactions`, `/statements` and `/invoicing/invoices` accept any garbage string and return `200` with zero rows.
4. **`sort_by` validation is inconsistent across endpoints.** `/accounts` and `/invoicing/customers` return `400` on an unknown value. `/transactions` and `/statements` silently ignore it. `/cards` and `/invoicing/invoices` do not parse it at all.
5. **`/statements` documents `sort_by` but no value changes the result.** Only the default ordering is ever produced.
6. **`/invoicing/customers` documents `sort_by` but `created_at` is the only legal value.** Every other value returns `400`. The parameter can only fail, never do anything.
7. **Page cursors are not opaque and are trivially forgeable.** They are unsigned base64url JSON. An `offset:N` cursor lets you seek to any offset in the result set.
8. **Cursors bind to the raw spelling of filters, not their meaning.** `order=asc` and `order=ASC` return identical rows but their cursors are not interchangeable (`400`). `status=settled` and `status=settled&status=settled` likewise.
9. **The documented rate limits are not enforced in sandbox.** 300 requests at ~3,600 req/min produced 300x `200` and zero `429`.
10. **The documented error body shape is wrong.** Docs show `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"..."}`. The server actually returns `{"type":"2","title":"Unauthenticated","status":401}` with no `detail`.

---

## 1. Sandbox dataset universe (basis for all count arithmetic)

| Endpoint | Total rows | Default page size (no `page_size`) | Default ordering (observed) |
| --- | --- | --- | --- |
| `/accounts` | 14 | 14 returned (dataset smaller than default; default not determinable, >= 14) | `account_name` ascending |
| `/cards` | 8 | 8 returned (>= 8) `[Rho claim]` docs say 20 | ascending by card id / creation |
| `/transactions` | 72 | **20** | `initiated_at` descending |
| `/statements` | 33 | **20** | `period_end` descending |
| `/invoicing/customers` | 7 (8 with `include_deleted=true`) | 7 (>= 7) `[Rho claim]` docs say 20 | `created_at` descending |
| `/invoicing/invoices` | 12 | 12 (>= 12) `[Rho claim]` docs say 20 | `created_at` descending |

Field distributions used to verify filters:

- transactions `account_type`: checking 42, credit 17, rewards 7, savings 6
- transactions `status`: settled 61, failed 8, pending 2, awaiting_approval 1
- transactions `transaction_type`: 22 distinct values, e.g. card_debit 8, credit_repayment 6, ach_debit 6, ach_credit 5
- transactions `card_id` non-null on 12/72, `user_id` non-null on 38/72, `memo`/`note` present on 39/72, `posted_at` null on 1/72
- transactions amount range: `-5900000` to `130000000` minor units
- transactions `initiated_at` range: `2023-05-31T07:29:00Z` to `2026-06-26T19:07:02Z`
- cards: 4 virtual / 4 physical; statuses active 4, locked 1, suspended 1, canceled 1, expired 1
- statements `statement_type`: credit 22, treasury 7, account 4; `period_end` range `2024-07-31` to `2026-05-31`
- invoices `status`: paid 4, pending_payout 2, unpaid 2, overdue 2, confirm_payment 1, cancelled 1
- invoices `date` range `2026-01-15` to `2026-07-10`; `due_date` range `2026-02-01` to `2026-08-20`

---

## 2. Error body taxonomy (exact bytes)

Five distinct shapes exist. All problem responses are `content-type: application/problem+json`, compact JSON, no trailing newline.

| Class | Exact body | Trigger |
| --- | --- | --- |
| Auth | `{"type":"2","title":"Unauthenticated","status":401}` | missing / empty / non-`Bearer` Authorization header |
| Parse failure | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: <name>"}` | value fails type coercion, or a scalar parameter is repeated |
| Semantic validation | `{"type":"1317","title":"<specific message>","status":400}` | value parses but fails a rule |
| Not found | `{"type":"1303","title":"<resource> not found","status":404}` | unknown id on a detail route |
| Framework 404 | `404 page not found` (`text/plain; charset=utf-8`) | unknown path under `/api/v1` |

### 2.1 Every `1317` title string observed

| Title | Produced by |
| --- | --- |
| `page_size must be between 1 and 100` | `page_size` = `0`, `-1`, `101`, `999999` on all six list endpoints |
| `page_token must be a valid cursor` | garbage token, cross-endpoint token, token + changed filter, forged token with bad fingerprint, `v:2`, `offset:-5`, `offset:>total` |
| `invalid sort_by parameter: "<value>"` | `/accounts`, `/invoicing/customers` only |
| `invalid order parameter: "<value>"` | `/accounts`, `/invoicing/customers` only |
| `invalid type parameter: "<value>"` | `/cards` only |
| `invalid status parameter: "<value>"` | `/cards` only |
| `min_amount must be less than or equal to max_amount` | `/transactions` only |

Note the two dialects: `1317` errors echo the offending value in `title` and carry **no `detail` field**; `about:blank` errors name the parameter in `detail` and never echo the value. The documented schema (`type`, `title`, `status`, optional `detail`, example `type: about:blank`) is satisfied structurally but `type` carries an opaque numeric string code, not a URI.

### 2.2 `1303` not-found titles

`transaction not found`, `card not found`, `account not found`, `statement not found`, `customer not found`, `invoice not found`, `invoice file not found`, `transaction file not found`.

### 2.3 Status codes reachable and unreachable

| Code | Reachable in sandbox | How |
| --- | --- | --- |
| 200 | yes | normal |
| 301 | yes | `GET https://rhoapi-sandbox.rho.co/api/v1` (no trailing path) returns nginx `301 Moved Permanently` |
| 400 | yes | two dialects above |
| 401 | yes | omit or malform `Authorization` |
| 403 | **no** | sandbox accepts any non-empty bearer; no scope or IP enforcement exists to trip. `[Rho claim]` production returns 403 for missing scope or IP outside allowlist |
| 404 | yes | unknown id (problem+json) or unknown path (text/plain) |
| 405 | yes | any method other than GET. Body is **empty, zero bytes**, with `allow: GET`. Applies to DELETE, PATCH, OPTIONS and **HEAD** |
| 411 | yes | POST or PUT with no `Content-Length`; HTML error page from the Google frontend, not from Rho |
| 422 | **no** | never observed. Every validation failure is 400 |
| 429 | **no** | see section 9 |

---

## 3. Authentication behavior

| Authorization header | Result |
| --- | --- |
| absent | 401 |
| `Bearer ` (empty token) | 401 |
| `Bearer` (no token at all) | 401 |
| `bearer sandbox` (lowercase scheme) | **401** |
| `Basic c2FuZGJveDpz` | 401 |
| `sandbox` (no scheme) | 401 |
| `Bearer !!!!` | **200** |
| `Bearer rhobat_totallyfake` | **200** |

The bearer scheme keyword is matched **case-sensitively**, which deviates from RFC 7235 (auth-scheme is case-insensitive). Any non-empty token after `Bearer ` is accepted, matching `[Rho claim]` in `docs/v1/auth`.

Response headers on 200 carry **no** `x-ratelimit-*`, no `retry-after`, no `x-request-id`, no `etag`, no `cache-control`. The full set is: `date`, `content-type`, `content-length` (or `content-encoding: gzip` when `--compressed`), `via: 1.1 google`, `cf-cache-status: DYNAMIC`, `referrer-policy`, `strict-transport-security`, `x-content-type-options: nosniff`, `x-frame-options: DENY`, `server: cloudflare`, `cf-ray`. HTTP/1.1 and HTTP/2 both serve identically.

---

## 4. Pagination

### 4.1 `page_size`

Identical behavior on all six list endpoints.

| Value | Result |
| --- | --- |
| `1` .. `100` | 200 |
| `0`, `-1`, `101`, `999999`, `99999999999999999999` | 400 `1317 page_size must be between 1 and 100` |
| `abc`, `1.5`, `10.0`, `1e2`, `0x10`, `true`, `null`, `%20 5`, `3#` | 400 `about:blank ... invalid parameter: page_size` |
| `` (empty) | 400 `about:blank` |
| `+5` (as `%2B5`) | **200, returns 5 rows.** Leading `+` accepted by the integer parser |
| repeated (`page_size=5&page_size=100`) | 400 `about:blank ... invalid parameter: page_size` |

The documented max of 100 is enforced on every endpoint including `/cards` and the invoicing endpoints, whose reference pages state only "Defaults to 20" without naming a maximum.

### 4.2 `page_token` internals

A cursor is base64url (unpadded) of `{"v":1,"f":"<22-char fingerprint>","t":"<base64url of inner state>"}`.

Two inner-state families exist:

| Endpoint | Inner state | Cursor style |
| --- | --- | --- |
| `/accounts` | `{"last_id":"30000000-...-0003","sort_by":"account_name","order":"asc"}` | keyset |
| `/cards`, `/transactions`, `/statements`, `/invoicing/customers`, `/invoicing/invoices` | `offset:20` | **offset** |

Neither layer is signed or encrypted. `f` is a deterministic 22-char hash of the canonicalized filter set; it was byte-identical for the same query across a 5-hour gap and across separate TCP connections, so it is not salted per process or per session.

`[Rho claim]` docs/v1/pagination: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." For five of the six endpoints the cursor is a bare **offset**, which cannot provide that guarantee against inserts. The claim is only structurally true for `/accounts`.

### 4.3 Cursor forging (verified)

| Forged token | Result |
| --- | --- |
| `{"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":b64("offset:70")}` on `/transactions` | **200, returns rows 71-72**. Arbitrary seek works |
| `offset:0` | 200, returns page 1 |
| `offset:71` | 200, 1 row |
| `offset:72` (== total) | 200, **empty array**, `next_page_token: null` |
| `offset:73` (total + 1) | 400 `page_token must be a valid cursor` |
| `offset:100000` | 400 |
| `offset:-5` | 400 |
| `{"v":2,...}` | 400 |
| fingerprint replaced with `AAAA...` | 400 |
| accounts keyset with a real `last_id` from mid-list | **200, seeks to that position** |
| accounts keyset with a nonexistent `last_id` | 400 |
| accounts keyset whose inner `sort_by`/`order` disagrees with the request | 400 |

So: the fingerprint binds the cursor to the endpoint plus the filter spelling; the offset itself is unvalidated except for a `0 <= offset <= total` range check; and the accounts keyset additionally validates that the referenced row exists and that the inner sort state matches.

### 4.4 What breaks a cursor and what does not

| Change between page N and page N+1 | Cursor still valid? |
| --- | --- |
| change `page_size` (e.g. 1 then 100) | **yes** (`page_size` is not in the fingerprint) |
| add an unknown parameter (`&zzz=1`) | **yes** |
| add the explicit default (`order=desc` on transactions, `sort_by=initiated_at`) | **yes**, values are canonicalized before hashing |
| add `include_deleted=false` or `include_deleted=0` on customers | **yes**, canonicalized to the default |
| `initiated_after=2026-01-01` vs `initiated_after=2026-01-01T00:00:00Z` | **yes**, dates are normalized before hashing |
| `order=asc` then `order=ASC` | **NO, 400.** Identical rows, incompatible cursors |
| `status=settled` then `status=settled&status=settled` | **NO, 400.** Identical rows, incompatible cursors |
| drop a filter, add a filter, change a filter | no, 400 (as documented) |
| use a token from a different endpoint | no, 400 |
| `page_token=` (empty string) | treated as absent, 200 page 1 |
| `page_token` repeated | 400 `about:blank ... invalid parameter: page_token` |

Cursor lifetime: tokens minted at 2026-09-11T19:22Z still resolved correctly at 2026-09-12T00:03Z, about 4h 41m later. No expiry observed. `[Rho claim]` "Cursors are designed for live iteration, not for bookmarks."

### 4.5 Last-page behavior

When the row count divides evenly into `page_size` there is **no** trailing empty page. `/transactions?page_size=36` page 2 returns 36 rows and `next_page_token: null`. `/cards?page_size=8` returns 8 rows and a null token on the first request. A forged `offset:72` cursor is the only way to see an empty page.

---

## 5. Per-endpoint parameter matrices

Legend: **honored** = changes the result set; **accepted/no-op** = parsed (it alters the cursor fingerprint) but never changes the result; **ignored** = not parsed at all (fingerprint unchanged); **rejected** = 400.

### 5.1 `GET /accounts`

Documented: `sort_by`, `order`, `page_size`, `page_token`.

| Parameter | Value | Status | Rows | Verdict |
| --- | --- | --- | --- | --- |
| `sort_by` | `account_name` | 200 | 14 | honored (is the default) |
| `sort_by` | `balance` | 200 | 14 | honored, reorders (0-balance rows first) |
| `sort_by` | `account_type`, `id`, `account_number_last_4`, `routing_number_last_4`, `created_at`, `name`, `type`, `bogus_field`, `` | 400 | - | rejected, `invalid sort_by parameter: "<value>"` |
| `order` | `asc` | 200 | 14 | honored (is the default) |
| `order` | `desc` | 200 | 14 | honored, exact reversal |
| `order` | `DESC`, `random`, `` | 400 | - | rejected, `invalid order parameter: "<value>"` |
| `account_type` | `checking` | 200 | **14** | **ignored.** No server-side type filter exists `[Rho claim]` docs say so explicitly |
| `type`, `status`, `search`, `account_id`, `currency`, `zzz` | any | 200 | 14 | ignored |

`sort_by=balance` defaults to ascending; `order` default is `asc` on this endpoint, the opposite of `/transactions` and `/statements`.

### 5.2 `GET /cards`

Documented: `user_id[]`, `type[]`, `status[]`, `page_size`, `page_token`.

| Parameter | Value | Status | Rows | Verdict |
| --- | --- | --- | --- | --- |
| `type` | `virtual` | 200 | 4 | honored |
| `type` | `physical` | 200 | 4 | honored |
| `type` | `virtual&type=physical` | 200 | 8 | honored, OR within the parameter |
| `type` | `plastic`, `Virtual`, ``, `virtual,physical` | 400 | - | **rejected**, `invalid type parameter: "<value>"` |
| `status` | `active` | 200 | 4 | honored |
| `status` | `active&status=locked` | 200 | 5 | honored, OR |
| `status` | all 11 enum values at once | 200 | 8 | honored, matches full set |
| `status` | `frozen` | 400 | - | **rejected**, `invalid status parameter: "frozen"` |
| `user_id` | valid UUID | 200 | 1 | honored |
| `user_id` | two UUIDs | 200 | 2 | honored, OR |
| `user_id` | `nope`, `` | 400 | - | rejected, `invalid parameter: user_id` |
| `user_id` | well-formed but unknown UUID | 200 | 0 | honored, empty |
| `type=virtual&status=active` | | 200 | 2 | AND across different parameters |
| `type=virtual&type=physical&status=expired` | | 200 | 1 | AND of (OR type) and (OR status) |
| `sort_by`, `order`, `search`, `last_4`, `id`, `card_id`, `zzz` | any | 200 | 8 | **ignored**, fingerprint unchanged |

`/cards` is the only endpoint that strictly validates its enum filters.

### 5.3 `GET /transactions`

Documented: `account_id[]`, `account_type[]`, `transaction_type[]`, `status[]`, `user_id[]`, `card_id[]`, `search`, `initiated_after`, `initiated_before`, `posted_after`, `posted_before`, `min_amount`, `max_amount`, `sort_by`, `order`, `page_size`, `page_token`.

**UUID array filters** (`account_id`, `user_id`, `card_id`): honored; repeats OR together (`account_id=A&account_id=B` gives 20 + 12 = 32); malformed value gives 400 `invalid parameter: <name>`; empty value gives 400; unknown but well-formed UUID gives 200 with 0 rows; comma-joined values (`A,B`, raw or `%2C`) give **400**; `account_id[]=A` bracket syntax is **silently ignored** and returns all 72 rows.

**Enum array filters** (`account_type`, `transaction_type`, `status`): honored for correct values, but **never validated**.

| Probe | Status | Rows |
| --- | --- | --- |
| `account_type=checking` | 200 | 42 |
| `account_type=checking&account_type=credit` | 200 | 59 |
| `account_type=bogus` | **200** | **0** |
| `account_type=CHECKING` | **200** | **0** (case-sensitive) |
| `account_type=treasury` | **200** | **0** (valid for statements, not for transactions) |
| `account_type=` | **200** | **0** |
| `transaction_type=card_debit` | 200 | 8 |
| `transaction_type=card_debit&transaction_type=card_refund` | 200 | 12 |
| `transaction_type=nope` | 200 | 0 |
| `status=settled` | 200 | 61 |
| `status=settled&status=failed` | 200 | 69 |
| `status=posted` / `status=Settled` | 200 | 0 |
| `account_type=checking&account_type=checking` (dup value) | 200 | 42 (deduplicated in results, **not** in the cursor fingerprint) |

**Amount filters**:

| Probe | Status | Rows |
| --- | --- | --- |
| `min_amount=0` | 200 | 32 |
| `min_amount=100000` | 200 | 18 |
| `min_amount=-100000` | 200 | 55 |
| `max_amount=0` | 200 | 40 |
| `max_amount=-100000` | 200 | 17 |
| `min_amount=-10000&max_amount=10000` | 200 | 17 |
| `min_amount=10000&max_amount=-10000` | **400** | `1317 min_amount must be less than or equal to max_amount` |
| `min_amount=999999999999999999` | 200 | 0 |
| `min_amount=1.5` / `abc` / `` / repeated | 400 | `about:blank ... invalid parameter: min_amount` |

Amount bounds are **inclusive on both ends** and operate on the **signed** value, so `min_amount=0` selects credits only and `max_amount=0` selects debits only. This is the only cross-field validation anywhere in the API: inverted **date** ranges produce an empty 200, inverted **amount** ranges produce a 400.

**Sort**:

| `sort_by` value | Rows reordered? | Verdict |
| --- | --- | --- |
| `initiated_at` | default order | honored, canonical default |
| `posted_at` | yes | honored; null `posted_at` sorts last under `desc`, first under `asc` |
| `amount` | yes | honored, signed numeric |
| `id`, `counterparty_name`, `status`, `transaction_type`, `account_id`, `account_type`, `card_id`, `user_id`, `memo`, `note`, `created_at`, `updated_at`, `date`, `money_movement_id`, `account_name`, `bogus_field`, `` | **no**, identical to default | **accepted/no-op, HTTP 200, no error** |

| `order` value | Effect |
| --- | --- |
| `desc` | default |
| `asc` | honored, exact reversal (ties flip, no stable secondary key) |
| `ASC` | honored (case-insensitive in effect) but hashed case-sensitively into the cursor |
| `sideways` | **accepted/no-op, falls back to desc, HTTP 200** |

**Undocumented parameters tested, all ignored with 200 and 72 rows**: `q`, `query`, `filter`, `expand`, `fields`, `include`, `id`, `currency`, `money_movement_id`, `timezone`, `limit`, `offset`, `per_page`, `size`, `pageSize`, `PAGE_SIZE`, `account_id[]`, `zzz_not_a_param`, 300 numbered junk params.

### 5.4 `GET /statements`

Documented: `account_id[]`, `statement_type[]`, `period_end_after`, `period_end_before`, `period_start_after`, `period_start_before`, `sort_by`, `order`, `page_size`, `page_token`.

| Probe | Status | Rows | Note |
| --- | --- | --- | --- |
| `statement_type=account` | 200 | 4 | honored |
| `statement_type=credit` | 200 | 22 | honored |
| `statement_type=treasury` | 200 | 7 | honored |
| `statement_type=account&statement_type=treasury` | 200 | 11 | OR |
| `statement_type=monthly` / `checking` / `Credit` / `` | **200** | **0** | not validated |
| `account_id=...0004` | 200 | 7 | honored; document-level OR match |
| `account_id=...0004&account_id=...0013` | 200 | 8 | OR |
| `account_id=zzz` or `account_id=` | 400 | - | `invalid parameter: account_id` |
| `account_id=<unknown uuid>` | 200 | 0 | |
| `account_id=...0004&statement_type=credit` | 200 | 0 | AND across filters |
| `period_end_after=2026-01-01` | 200 | 9 | inclusive |
| `period_end_before=2026-01-01` | 200 | 24 | 9 + 24 = 33, partition is exact |
| `period_end_after=2026-05-31&period_end_before=2026-05-31` | 200 | **0** | `before` is exclusive |
| `period_start_after=2026-01-01` | 200 | 8 | |
| `period_start_before=2026-01-01` | 200 | 25 | |
| `period_end_after=2026-01-01T00:00:00Z` | **400** | - | **date-only format required here**, unlike `/transactions` |
| `period_end_after=2026-99-99` | 400 | - | |
| `sort_by=period_end` / `period_start` / `available_at` / `id` / `bogus` | 200 | 33 | **no value ever changes the order** |
| `order=asc` | 200 | 33 | honored, exact reversal |
| `order=bogus` | **200** | 33 | accepted/no-op, falls back to desc |
| `account_type`, `type`, `search`, `zzz` | 200 | 33 | ignored |

### 5.5 `GET /invoicing/customers`

Documented: `search`, `include_deleted`, `sort_by`, `order`, `page_size`, `page_token`.

| Probe | Status | Rows |
| --- | --- | --- |
| `search=acme` / `ACME` | 200 | 1 (case-insensitive) |
| `search=northwind.example` | 200 | 1 (matches `email`) |
| `search=co` | 200 | 5 (substring, anywhere) |
| `search=Boston` | 200 | **0** (address is NOT searched, matching the docs) |
| `search=` | 200 | 7 (ignored) |
| `search=%` | 200 | 0 (LIKE wildcard escaped) |
| `search` repeated | 400 | `invalid parameter: search` |
| `include_deleted=true` / `True` / `TRUE` / `t` / `1` | 200 | 8 |
| `include_deleted=false` / `0` | 200 | 7 |
| `include_deleted=yes` / `on` / `` / bare `include_deleted` | **400** | `invalid parameter: include_deleted` |
| `include_deleted` repeated | 400 | `invalid parameter: include_deleted` |
| `sort_by=created_at` | 200 | 7 (the only legal value) |
| `sort_by=legal_name` / `email` / `updated_at` / `total_revenue` / `id` / `bogus` | **400** | `invalid sort_by parameter: "<value>"` |
| `order=asc` | 200 | 7, reversed |
| `order=ASC` / `bogus` | **400** | `invalid order parameter: "<value>"` |
| `status`, `customer_id`, `zzz` | 200 | 7 (ignored) |

The boolean parser is Go's `strconv.ParseBool` (accepts `1,t,T,TRUE,true,True,0,f,F,FALSE,false,False`).

### 5.6 `GET /invoicing/invoices`

Documented: `status[]`, `due_date_after`, `due_date_before`, `date_after`, `date_before`, `page_size`, `page_token`. No `sort_by`/`order` documented.

| Probe | Status | Rows |
| --- | --- | --- |
| `status=paid` | 200 | 4 |
| `status=paid&status=unpaid` | 200 | 6 |
| `status=draft` / `Paid` / `paid,unpaid` / `` | **200** | **0** (not validated) |
| `status=canceled` (US spelling) | **200** | **0**. The enum value is `cancelled` |
| `date_after=2026-06-01` | 200 | 6 |
| `date_before=2026-06-01` | 200 | 7 |
| `date_after=2026-05-01&date_before=2026-05-01` | 200 | **2** |
| `due_date_after=2026-07-01&due_date_before=2026-07-01` | 200 | **1** |
| `date_after=2026-07-01&date_before=2026-01-01` | 200 | 0 |
| `date_after=2026-06-01T00:00:00Z` | 400 | date-only format required |
| `date_after=06/01/2026` | 400 | |
| `sort_by=date` / `bogus`, `order=asc` / `bogus` | 200 | 12, **ignored entirely** (fingerprint unchanged) |
| `customer_id`, `search`, `include_deleted`, `zzz` | 200 | 12 (ignored) |

6 + 7 = 13 > 12 and the same-day probes return non-zero, so **both bounds are inclusive** on this endpoint. This differs from `/transactions` and `/statements`, whose `*_before` bounds are exclusive.

---

## 6. Date parameter semantics, side by side

| Endpoint | Parameters | Accepted formats | Rejected formats | `after` | `before` |
| --- | --- | --- | --- | --- | --- |
| `/transactions` | `initiated_after/before`, `posted_after/before` | `2026-01-01`, `2026-01-01T00:00:00Z`, `2026-01-01T00:00:00+00:00`, `2026-01-01T00:00:00.000Z` | `2026-01-01T00:00:00` (no zone), `2026-01-01 00:00:00`, epoch `1767225600`, `01/01/2026`, `2026-13-01`, `2026-02-30`, `not-a-date` | inclusive | **exclusive** |
| `/statements` | `period_end_after/before`, `period_start_after/before` | `2026-01-01` only | **any timestamp form**, `2026-99-99` | inclusive | **exclusive** |
| `/invoicing/invoices` | `date_after/before`, `due_date_after/before` | `2026-01-01` only | any timestamp form, `06/01/2026` | inclusive | **inclusive** |

Out-of-range values behave sanely: `initiated_after=1900-01-01` and `=0001-01-01` both return all 72; `=2999-01-01` returns 0. No lower or upper year bound is enforced.

Null handling: any `posted_after` or `posted_before` bound excludes the row whose `posted_at` is null (`posted_after=` returns 71 of 72).

### 6.1 The empty-value trap, tabulated

| Parameter | Empty value result |
| --- | --- |
| `initiated_after=`, `posted_after=`, `period_end_after=`, `period_start_after=`, `date_after=`, `due_date_after=` | **ignored**, full result set |
| `initiated_before=`, `posted_before=`, `period_end_before=`, `period_start_before=`, `date_before=`, `due_date_before=` | **200 with 0 rows** |
| `account_type=`, `transaction_type=`, `status=`, `statement_type=` | **200 with 0 rows** |
| `account_id=`, `user_id=`, `card_id=` | 400 |
| `page_size=`, `min_amount=`, `max_amount=` | 400 |
| `include_deleted=` | 400 |
| `search=`, `search=%20` | ignored, full result set |
| `page_token=` | ignored, page 1 |
| `sort_by=` | `/accounts` and `/customers`: 400. `/transactions` and `/statements`: accepted/no-op |
| `order=` | `/accounts` and `/customers`: 400. `/transactions` and `/statements`: not tested separately, `order=sideways` is a no-op |

Mechanism: an empty date string is coerced to the zero time `0001-01-01T00:00:00Z`. `field >= zero` is universally true, so `*_after=` is a no-op; `field < zero` is universally false, so `*_before=` empties the set. An empty enum string becomes a literal filter value that matches nothing.

---

## 7. `search` semantics (transactions and customers only)

- Case-insensitive substring, unanchored. `Parking`, `parking`, `park`, `PARKING` all return the same 1 row.
- Leading and trailing whitespace is trimmed: `search=%20Parking%20` returns the same 1 row. `search=%20` alone is a no-op.
- Transactions `search` covers **counterparty_name, memo and note**, verified independently: `GOODS_AND_SERVICES` (memo only) returns 1 row; `Invalid receiving routing number` (note only) returns 2 rows; `Daily credit repayment` (memo and note) returns 6.
- Customers `search` covers **legal_name and email** only. `Boston` (an address city in the fixture) returns 0.
- SQL LIKE metacharacters are escaped, not interpreted. `%` returns 0, `Midtown%Services` returns 0, `Midtown_Parking` returns 0, and `_` returns exactly the 3 rows containing a literal underscore (`GOODS_AND_SERVICES`, `INVALID_RECEIVING_ROUTING_NUMBER`).
- `' OR 1=1--` returns 0 rows, no error. Null byte, CRLF and control characters in the value return 0 rows with no header injection and no 500.
- A 2,000-character value returns 0 rows, no error.
- Repeating `search` is a 400.
- `search` ANDs with every other filter.
- `/invoicing/invoices` has **no** `search`; passing one is silently ignored.

---

## 8. Query-string parsing quirks

| Input | Behavior |
| --- | --- |
| `?page%5Fsize=3` | percent-encoded parameter names are decoded and honored (3 rows) |
| `?page_size=3&x=1;y=2` | a literal `;` makes that whole key/value pair vanish; other parameters survive. Go's `url.ParseQuery` semicolon rejection |
| `?status=settled;x=1&page_size=3` | the entire `status` filter is **silently dropped** (default fingerprint returned) |
| `?&&page_size=3&&` | empty pairs tolerated |
| `?page_size=3%23` (`3#`) | 400, `#` is part of the value once encoded |
| parameter name case | **case-sensitive**. `PAGE_SIZE`, `pageSize` are ignored |
| parameter order in the URL | irrelevant, fingerprint identical |
| 300 unknown parameters | fine, 200 |
| `Accept: application/xml` or `text/plain` | ignored, always `application/json` |

The semicolon behavior is a second silent-filter-loss vector: any filter value containing a raw `;` disappears without an error.

---

## 9. Rate limits

`[Rho claim]` docs/v1/rate-limits: "Per API Access Token: Approximately 60 requests per minute. Per source IP: Approximately 600 requests per minute", with `429` and a `Retry-After` header.

Observed in sandbox:

| Burst | Concurrency | Elapsed | Effective rate | Result |
| --- | --- | --- | --- | --- |
| 90 requests to `/accounts` | 6 | 4 s | ~1,350 req/min | 90x `200`, zero `429` |
| 300 requests to `/transactions` | 20 | 4 s | ~3,600 req/min | 300x `200`, zero `429` |

No `x-ratelimit-*` headers on any response and no `retry-after` on any 200. `429` was not reachable, so its body shape could not be captured. An integrator cannot use the sandbox to exercise retry/backoff paths.

---

## 10. Detail (non-list) endpoints

| Path pattern | Bad-format id | Unknown id | Query parameters |
| --- | --- | --- | --- |
| `/accounts/{account_id}` | 400 `invalid parameter: id` | 404 `account not found` | all ignored |
| `/cards/{id}` | 400 `invalid parameter: id` | 404 `card not found` | all ignored, including `sort_by=bogus` which 400s on `/accounts` |
| `/transactions/{id}` | 400 `invalid parameter: id` | 404 `transaction not found` | ignored |
| `/transactions/{tx}/files/{file_id}` | 400 `invalid parameter: file_id` | 404 `transaction file not found` (also when the file exists but belongs to another transaction) | ignored |
| `/statements/{id}` | **no format validation**: `abcdef`, `-1`, `1.5` all return 404 `statement not found` | 404 | ignored |
| `/invoicing/customers/{id}` | 400 | 404 `customer not found`; a deleted customer still returns 200 with `deleted_at` set | ignored |
| `/invoicing/invoices/{id}` | 400 | 404 `invoice not found` | ignored |
| `/invoicing/invoices/{id}/files/{file_id}` | 400 | 404 `invoice file not found` | ignored |

Statement ids are opaque numeric-looking strings (`572981`, `439951`, `200527`), not UUIDs, and are not validated at all, so a client bug that sends a garbage statement id gets 404 rather than 400. `GET /transactions/{id}/files/{file_id}` returns a signed Google Cloud Storage URL on `rho-api-sandbox.files.rho.co`; statement `pdf_url` values point at `sandbox-statements.files.rho.co`.

---

## 11. Contradictions between the corpus and the live sandbox

1. **Error body `type`.** `docs/v1/auth` shows `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}` and every operation page documents `type` with "Example: about:blank". The server returns `{"type":"2","title":"Unauthenticated","status":401}`: title differs, `detail` is absent, and `type` is an opaque numeric code. Same for 404 (`"1303"`) and semantic 400 (`"1317"`).
2. **RFC citation.** `api/v1/openapi` says errors follow "RFC 9457 problem details"; `docs/v1/auth` cites RFC 7807. Both are cited for the same objects.
3. **`page_size` maximum.** `/cards` and both invoicing list pages document only "Defaults to 20" and name no maximum; the server enforces 1..100 and says so in the error.
4. **Cursor stability.** `docs/v1/pagination` promises insert-stable cursors. Five of six endpoints use a plain `offset:N`, which cannot be insert-stable.
5. **Cursor opacity.** "Cursors are opaque, pass back exactly the string you received." They are unsigned base64url JSON and arbitrary offsets can be forged.
6. **Cursor binding.** "A token returned by one endpoint is only valid for that same endpoint with the same filters and sort order." In fact `page_size` may change freely, explicit defaults may be added freely, and unknown parameters may be added freely, while semantically identical respellings (`ASC` vs `asc`, a duplicated identical enum value) break the token.
7. **`posted_at` nullability.** `api/transactions_listtransactions.md` says `posted_at` is "Null while status is pending". In the sandbox both `pending` rows carry a non-null `posted_at`, and the only null `posted_at` belongs to an `awaiting_approval` row. `docs/v1/transactions` hedges in the opposite direction ("not coupled to status"), so the two Rho pages disagree with each other and the reference page disagrees with the data.
8. **Rate limits.** Documented limits are simply absent in sandbox.
9. **`/statements` `sort_by`.** Documented as "Sort field"; no value has any effect.
10. **`/invoicing/customers` `sort_by`.** Documented as "Sort field. Defaults to created_at when omitted." `created_at` is the only accepted value; everything else is a 400.
11. **`/accounts` sort fields.** Documented only as "Sort field" with no enum. Only `account_name` and `balance` exist; `id` and `created_at` are rejected.
12. **Scopes.** `api/v1/openapi` lists five scopes (`accounts:read`, `cards:read`, `invoicing:read`, `statements:read`, `transactions:read`) but `docs/v1/auth` lists only three ("The scopes available today are" accounts, transactions, statements), omitting cards and invoicing.

---

## 12. Conspicuously absent

- **No count or total.** No `total`, `total_count`, `has_more`, `page.count` or `Link` header anywhere. The only way to size a result set is to walk it. Forging an `offset:N` cursor and binary-searching the 400 boundary is the sole way to learn a total in one or two calls, and that relies on undocumented behavior.
- **No `previous_page_token`.** Iteration is forward only through the public contract.
- **No `422`.** Every validation failure is a 400, so clients cannot distinguish malformed syntax from semantically invalid content by status alone; they must parse `type` (`about:blank` vs `1317`).
- **No machine-readable error codes for field-level problems.** The `1317` bucket covers page size, cursor, sort, order, type, status and amount ordering alike. The offending field name appears only inside the human-readable `title` or `detail` string.
- **No request id / correlation header.** Only Cloudflare's `cf-ray`. Nothing to quote to support.
- **No `Retry-After`, no `x-ratelimit-*`** on any response.
- **No `ETag`, `Last-Modified`, or `Cache-Control`.** Conditional requests are impossible.
- **`HEAD` is not supported** on GET routes (405 with `allow: GET`), which breaks a common cheap-existence-check pattern.
- **No filtering on `/accounts` at all**, and no `search` on `/invoicing/invoices` or `/cards`, so name lookups on those resources must be done client-side after a full walk.
- **No `money_movement_id` filter** on `/transactions`, even though the docs tell you to "group on it to treat the entries of one movement as a unit". You must fetch and group client-side.
- **No `min_amount`/`max_amount` on `/invoicing/invoices`**, and no `customer_id` filter there either, although the invoice object carries `customer.id`.
- **No `created_at`/`updated_at` range filters** on invoices or customers, despite those being the documented sort keys.
- **No dispute, decline or authorization surface** on transactions; `[Rho claim]` docs/v1/transactions: "A refund or credit is not by itself a dispute, v1 exposes no dispute indicator."

---

## 13. Practical guidance distilled

1. Never interpolate a possibly-empty value into a `*_before` parameter. Build the query string conditionally. An empty string silently yields an empty page and your reconciliation job will report "no activity".
2. Validate enum filter values client-side before sending. `/transactions`, `/statements` and `/invoicing/invoices` will not tell you that `status=Settled`, `status=canceled` or `account_type=treasury` is wrong; they return `200 []`.
3. Spell the invoice cancelled status with two Ls: `cancelled`.
4. Do not trust `sort_by` outside `/accounts` (`account_name`, `balance`) and `/transactions` (`initiated_at`, `posted_at`, `amount`). Everywhere else it is decoration or a 400.
5. When paginating, replay the **byte-identical** filter query string on every page. Changing only `page_size` is safe; changing the case of `order` or duplicating an identical enum value is not.
6. Treat `200 []` as ambiguous between "no matching data" and "your filter was silently dropped". Assert against an unfiltered control query when a filtered result comes back empty.
7. Parse errors by `type`: `"about:blank"` means you sent an unparseable value and `detail` names the field; `"1317"` means a rule was violated and `title` carries the message; `"1303"` means not found; `"2"` means unauthenticated.
8. Do not build retry/backoff tests against sandbox. 429 does not occur there.
9. Use `Bearer` with a capital B.
10. Do not use `HEAD` for liveness checks.

---

## 14. Evidence index

All probe artifacts live in `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-filters/`.

| Prefix | Covers |
| --- | --- |
| `base_*` | unfiltered baselines for all six endpoints, with and without `page_size=100` |
| `auth_*` | eight Authorization header variants |
| `ps_*` | `page_size` boundaries, type coercion, aliases |
| `tok_*`, `cur_*`, `ak_*`, `off_*`, `ttl_*`, `pg_*` | cursor validity, forging, binding, TTL, last-page behavior |
| `tx_*`, `txd_*`, `txa_*`, `txs_*`, `txsort_*`, `txq_*`, `txu_*` | transactions filters, dates, amounts, sorting, search, undocumented params |
| `ac*` , `acct_*` | accounts sorting and ignored filters |
| `cd_*` | cards filters |
| `st_*` | statements filters |
| `cu_*` | invoicing customers filters |
| `inv_*` | invoicing invoices filters |
| `fp_*`, `fps_*`, `fpt_*` | cursor-fingerprint sensitivity used to separate "ignored" from "accepted/no-op" |
| `e_*`, `z_*` | empty values, query-string parsing edge cases, control characters |
| `s_*` | search field coverage and LIKE escaping |
| `m_*`, `p_*`, `id_*`, `f_*` | HTTP methods, paths, detail-endpoint 400/404 shapes |
| `ratelimit_burst.txt`, `ratelimit_burst2.txt` | 90 and 300 request bursts |
