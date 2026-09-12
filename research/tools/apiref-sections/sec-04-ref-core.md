## 4. Endpoint reference: Accounts, Transactions and Cards

Seven operations make up the core of the Rho `v1` REST surface. All seven are `GET`. There are no write
verbs anywhere in `v1`: every non-`GET` method on every path returns `405 Method Not Allowed` with
`Allow: GET` (observed, `POST https://rhoapi-sandbox.rho.co/api/v1/accounts` → `405`, empty body).

This section is the working reference for those seven. For each one: method, path, required scope, every
parameter with its type, default, constraint and whether the constraint is actually enforced, the full
response field table with types, nullability and observed presence rates, every enum value spelled out, a
real sandbox request with its real response, and the error conditions. Where Rho's documentation and the
live API disagree, the disagreement is called out inline.

Cross-references: the credential model and scope grants are covered in section 2, Authentication and
authorization; the cursor mechanics, the offset-versus-keyset split and the empty-value traps are covered
in full in section 6.1, Pagination; the error envelope taxonomy is covered in section 6.3, Errors.
Statements and Invoicing have their own section, section 5.

### 4.0 Conventions and evidence base

**Base URLs** (official docs, `api_v1_openapi.md`):

| Environment | Base URL |
| --- | --- |
| Production | `https://rhoapi.rho.co/api/v1` |
| Sandbox | `https://rhoapi-sandbox.rho.co/api/v1` |

Every operation path below is relative to that prefix. Paths are case sensitive (observed: `GET /ACCOUNTS`
returns a plain-text `404 page not found`, not JSON).

**Authentication.** `Authorization: Bearer <token>`, nothing else. On sandbox any non-empty token is
accepted, and the scheme keyword is matched case sensitively (observed: `Bearer WRONGTOKEN` → `200`;
`bearer sandbox` → `401 {"type":"2","title":"Unauthenticated","status":401}`).

**Evidence base.** Every "observed" claim in this section comes from live calls to
`https://rhoapi-sandbox.rho.co/api/v1` with `Authorization: Bearer sandbox`, captured 2026-09-12 between
00:20Z and 00:40Z UTC. The full sandbox dataset is small and was paged to exhaustion, so presence rates are
census figures, not samples:

| Resource | Records | Pages at `page_size=100` |
| --- | --- | --- |
| accounts | 14 | 1 |
| transactions | 72 | 1 |
| cards | 8 | 1 |

Sandbox data is fictional and frozen (newest transaction `initiated_at` is `2026-06-26T19:07:02Z`), with one
exception: card spend windows are recomputed against the real wall clock on every request. Response bodies
below are the real bytes, reformatted for reading: the API emits compact JSON with keys in alphabetical
order and escapes the ampersand in URL strings as the six-character sequence backslash-u-0-0-2-6, so a
byte-level diff against these examples will show key order and that escape. No values were changed.
Presence rates below describe the sandbox fixture, not a production guarantee. They are useful because
they show which documented fields Rho's own reference implementation never emits.

> **Divergence:** the markdown operation exports under `docs.rho.co/api/v1/openapi/**.md` are a lossy
> rendering of the same OpenAPI document the HTML reference renders. For every one of the seven
> operations the `.md` export silently drops the **required scope**, the **defaults** for `sort_by`,
> `order` and `page_size`, the numeric range on `page_size`, the `uuid`/`date-time`/`uri` formats, the
> `^[0-9]{4}$` pattern on `last_4`, the **enum values on query parameters**, the `or null` nullability
> marker on response fields, and the **`429 Too Many Requests`** response that the HTML declares on every
> operation. If you generate a client from the markdown export you will produce a client with no scope
> documentation, no defaults and no 429 handling. Use the rendered HTML reference, or the tables below.

**The null-versus-omitted rule.** This is the single most useful deserialization fact in the API and it is
documented nowhere. The wire format uses two different idioms, split by whether the field is `required` in
the schema:

| Schema shape | Wire representation | Where you see it |
| --- | --- | --- |
| `required` and nullable | key always present, value may be `null` | every nullable field on `Card` |
| optional (not `required`) | key **omitted entirely**, value is never `null` | every optional field on `Account` and `Transaction`, and the four merchant-control arrays on `Card` |

Observed: across all 72 transactions and all 14 accounts there is **not a single JSON `null`**; across the
8 cards there are 17 explicit `null`s (`shipping_address` 4, `usage_ends_at` 5, `usage_starts_at` 7,
`spend_period_end` 1) and zero omissions among the 16 required keys. The reference types the optional
transaction and account fields as "string or null", so a client that only checks for `null` will read
`undefined` and take the wrong branch. Treat absent and `null` as the same thing everywhere.

**Money.** Shared object used by `Account.balance`, `Transaction.amount`, `Card.spending_limit`,
`Card.current_spend` and `Card.pending_spend`.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `amount` | integer | yes | Minor units, for example cents for USD. Signed on transactions, where negative is a debit. |
| `currency` | string | yes | ISO 4217 code. |

There is no `amount_decimal`, no scale or exponent field, no FX rate and no original-currency field anywhere
in the core surface. Every one of the 393 `currency` occurrences in the sandbox is `USD`.

**Page.** The envelope on all three list operations.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `next_page_token` | string or null | yes | Pass back as `page_token`. `null` means last page. |

No total count, no `has_more`, no previous cursor, no page number. Sizing a result set requires walking it.

### 4.1 The seven operations at a glance

| Operation | Method and path | Scope | Declared statuses (rendered HTML reference) |
| --- | --- | --- | --- |
| ListAccounts | `GET /accounts` | `accounts:read` | 200, 400, 401, 403, 429, 500, 503 |
| GetAccount | `GET /accounts/{account_id}` | `accounts:read` | 200, 400, 401, 403, 404, 429, 500, 503 |
| ListTransactions | `GET /transactions` | `transactions:read` | 200, 400, 401, 403, 429, 500, 503 |
| GetTransaction | `GET /transactions/{id}` | `transactions:read` | 200, 400, 401, 403, 404, 429, 500, 503 |
| GetTransactionFile | `GET /transactions/{transaction_id}/files/{file_id}` | `transactions:read` | 200, 400, 401, 403, 404, 429, 500, 503 |
| ListCards | `GET /cards` | `cards:read` | 200, 400, 401, 403, 429, 500, 503 |
| GetCard | `GET /cards/{id}` | `cards:read` | 200, 400, 401, 403, 404, 429, 500, 503 |

Scopes come from the HTML reference's Security block, for example `AccessToken ( Required scopes :
accounts:read )` on ListAccounts. List operations declare no `404`; single-resource operations do. The
file operation needs only `transactions:read`; there is no separate document or file scope.

> **Divergence:** `docs/v1/auth` states "The scopes available today are:" and lists exactly three:
> `accounts:read`, `transactions:read`, `statements:read`. The OpenAPI security object lists five, adding
> `cards:read` and `invoicing:read`, and the Cards guide independently says "Both endpoints require the
> `cards:read` scope". The auth guide is stale. If you are provisioning a token for a card integration,
> grant `cards:read` even though the scope table does not list it.

> **Divergence:** the status column above is the rendered HTML reference's, and the `429` in it is the
> status the two renderings of the same OpenAPI document disagree about. Verified 2026-09-11 against
> `docs.rho.co/api/v1/openapi/accounts`, `/transactions` and `/cards`: the rendered response list reads
> `200, 400, 401, 403, 429, 500, 503`. None of the fourteen `.md` exports contains the string `429` at
> all, and no `429` body schema is published anywhere, so take the `.md` sets as this table minus `429`
> and add the rate-limit branch to any generated client by hand. `429` is also not reachable in sandbox:
> 300 requests in 4 seconds (roughly 3,600 per minute, against a documented ceiling of about 60 per minute
> per token) returned 300 × `200` and zero `429`. You cannot exercise your backoff path against sandbox.

### 4.2 Parameter semantics shared by the three list operations

These behaviours are identical or near-identical across `/accounts`, `/transactions` and `/cards`, so they
are stated once here and only the deviations are repeated per operation.

**`page_size`** is documented as `integer, [ 1 .. 100 ]`, default `20`, on all three. The range is enforced
uniformly and identically:

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=101' \
  -H 'Authorization: Bearer sandbox'
```

```json
{"type":"1317","title":"page_size must be between 1 and 100","status":400}
```

`0`, `-1`, `101` and `999999` all produce that body. A value that fails integer parsing (`abc`, `1.5`, empty,
or the parameter repeated) produces the other 400 dialect instead:
`{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}`.

The default of `20` is directly observable only on `/transactions`, because the accounts and cards fixtures
are smaller than a default page (observed: `GET /transactions` with no `page_size` returns 20 items and a
non-null cursor; `GET /accounts` returns all 14 and `GET /cards` returns all 8, both with
`next_page_token: null`).

**`page_token`** is an unsigned base64url JSON object, not an opaque blob. Two families exist. `/accounts`
returns a keyset cursor that names its own sort state; `/transactions` and `/cards` return an offset cursor:

```
/accounts  -> {"v":1,"f":"SigraTvwZG8Dd7QLdKJzPA","t":"..."}  where t decodes to
              {"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}
/transactions -> {"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":"b2Zmc2V0OjI"}  where t decodes to "offset:2"
```

`f` is a 16-byte fingerprint of the endpoint plus the canonicalized filter set. Observed binding rules:
replaying the same query with the token works (`200`); changing only `page_size` works (`200`); adding a
filter fails (`400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`); using a
`/transactions` token on `/cards` fails the same way. See section 6.1, Pagination, for the forging
behaviour and the full binding matrix.

> **Divergence:** `docs/v1/pagination` promises "Cursors are stable across changes to the underlying data:
> new items inserted while you are iterating will not shift existing pages or cause items to be skipped or
> duplicated", and separately that cursors are "opaque". Both `/transactions` and `/cards` return a plain
> `offset:N`, which cannot provide insert stability, and no cursor on any endpoint is signed or encrypted.
> Only `/accounts` uses a keyset cursor that structurally can honour the promise.

**Filter and sort validation is inconsistent between the three endpoints**, and the inconsistency is the
main source of silent wrong answers. Summary of observed behaviour:

| Endpoint | Unknown `sort_by` | Unknown `order` | Unknown enum filter value | Unknown parameter name |
| --- | --- | --- | --- | --- |
| `/accounts` | `400 invalid sort_by parameter: "created_at"` | `400 invalid order parameter: "DESC"` | no enum filters exist | `200`, ignored |
| `/transactions` | `200`, silently falls back to the default | `200`, silently falls back to `desc` | `200` with **0 rows** | `200`, ignored |
| `/cards` | `200`, parameter is not parsed at all | `200`, not parsed | `400 invalid status parameter: "bogus"` | `200`, ignored |

The practical rule: `200 []` from `/transactions` is ambiguous between "no matching data" and "you
misspelled a filter value". Validate enum values client-side before sending, and assert a filtered empty
result against an unfiltered control query.

**The empty-value trap.** Interpolating an undefined variable into a `*_before` parameter silently empties
the result set rather than erroring (observed: `GET /transactions?posted_before=` → `200` with
`"transactions": []`). An empty date coerces to the zero time `0001-01-01T00:00:00Z`, so `field < zero` is
never true. The matching `*_after=` parameters are ignored instead, and an empty enum value
(`status=`, `account_type=`) also yields `200` with zero rows. Build query strings conditionally.

---

### 4.3 Accounts

The Accounts API exposes the bank accounts the business holds on Rho. Per the Accounts guide, `account_type`
"determines what it can hold and how it behaves" and is **immutable for the lifetime of an account**.

`AccountType`, all five values, with Rho's own definitions:

| Value | Rho's definition |
| --- | --- |
| `checking` | Operating cash accounts used for everyday inflows and outflows. |
| `savings` | Higher-yield depository accounts segregated from operating cash. |
| `credit` | Revolving credit lines backing corporate cards. |
| `investment` | Treasury sleeves invested in money-market funds or short-duration securities. |
| `rewards` | Cash-back balances earned on card spend. |

Observed distribution over the 14 sandbox accounts: `checking` 6, `credit` 4, `rewards` 2, `savings` 2,
`investment` **0**. The `investment` shape, in particular whether such an account carries masked numbers, is
unverifiable from the sandbox.

> **Divergence:** the Statements resource uses a different account-type vocabulary for the same concept.
> `statements.accounts[].account_type` emits `treasury`, which is not a member of `AccountType` at all,
> while the Accounts API calls the nearest equivalent `investment`. Compounding it, the sandbox account
> named "Treasury Checking" (`30000000-0000-4000-8000-000000000004`) has `account_type: "checking"`. Do
> not build one shared account-type enum across Accounts and Statements.

#### 4.3.1 `GET /accounts` (ListAccounts)

Returns a paginated list of accounts for the authenticated business. Scope: `accounts:read`.

**Query parameters**

| Param | Type | Default | Constraint | Enforced? |
| --- | --- | --- | --- | --- |
| `sort_by` | string | `"account_name"` | Enum: `account_name`, `balance` | **Yes.** Any other value, including `id`, `created_at`, `account_type`, `account_number_last_4` and the empty string, returns `400 {"type":"1317","title":"invalid sort_by parameter: \"<value>\"","status":400}` |
| `order` | string | `"asc"` | Enum: `asc`, `desc` | **Yes**, and case sensitively. `DESC` returns `400 invalid order parameter: "DESC"` |
| `page_size` | integer | `20` | `[1 .. 100]` | **Yes**, see 4.2 |
| `page_token` | string | none | Opaque cursor | **Yes**, keyset cursor bound to endpoint plus sort state |

There is no `account_id`, `account_type`, `currency`, `status` or `search` filter. The Accounts guide says
so explicitly ("The list endpoint has no server-side type filter") and tells you to filter the returned
array client-side. Observed: `GET /accounts?account_type=checking` returns all **14** accounts, silently
ignored, not rejected.

Note that `order` defaults to `asc` here and to `desc` on `/transactions`. `sort_by=balance` with no
explicit `order` sorts ascending (observed: first three rows are the three zero-balance accounts).

**Response `200`**

| Field | Type | Required | Nullable | Observed presence (n=14) | Notes |
| --- | --- | --- | --- | --- | --- |
| `accounts` | array of Account | yes | no | 14 rows | |
| `accounts[].id` | string (uuid) | yes | no | 14/14 | Only unique key on the object |
| `accounts[].account_type` | string enum | yes | no | 14/14 | 4 of 5 values seen |
| `accounts[].balance` | Money | yes | no | 14/14 | |
| `accounts[].balance.amount` | integer | yes | no | 14/14 | All USD; values `0`, `1046`, `811970`, `876138`, `8711697`, `15460929` |
| `accounts[].balance.currency` | string | yes | no | 14/14 | `USD` on all |
| `accounts[].account_name` | string | no | yes | **14/14** | Never omitted, never null in practice |
| `accounts[].account_number_last_4` | string | no | yes | **8/14** | Key omitted, not null, on all 4 `credit` and both `rewards` accounts |
| `accounts[].routing_number_last_4` | string | no | yes | **8/14** | Same 8 rows; every value is `"0089"` |
| `page.next_page_token` | string | yes | yes | 1/1 | |

The Account object has exactly 6 properties. There is no `created_at`, no `status`, no account-level
`currency`, no bank or partner name, no full account or routing number, no IBAN or SWIFT, and no
available-versus-current balance, credit limit, available credit, APR or yield. An account is 4 to 6 keys
and nothing else.

**Real request and response**

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=3' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "accounts": [
    {
      "account_name": "Cash (Checking)",
      "account_number_last_4": "9508",
      "account_type": "checking",
      "balance": { "amount": 876138, "currency": "USD" },
      "id": "30000000-0000-4000-8000-000000000002",
      "routing_number_last_4": "0089"
    },
    {
      "account_name": "Cash (Checking)",
      "account_number_last_4": "4609",
      "account_type": "checking",
      "balance": { "amount": 8711697, "currency": "USD" },
      "id": "30000000-0000-4000-8000-000000000003",
      "routing_number_last_4": "0089"
    },
    {
      "account_name": "Credit Account",
      "account_type": "credit",
      "balance": { "amount": 0, "currency": "USD" },
      "id": "30000000-0000-4000-8000-000000000007"
    }
  ],
  "page": {
    "next_page_token": "eyJ2IjoxLCJmIjoiU2lncmFUdndaRzhEZDdRTGRLSnpQQSIsInQiOiJleUpzWVhOMFgybGtJam9pTXpBd01EQXdNREF0TURBd01DMDBNREF3TFRnd01EQXRNREF3TURBd01EQXdNREEzSWl3aWMyOXlkRjlpZVNJNkltRmpZMjkxYm5SZmJtRnRaU0lzSW05eVpHVnlJam9pWVhOakluMCJ9"
  }
}
```

Three things are visible in that one response. The first two rows share the display name `Cash (Checking)`,
so `account_name` is not unique. The third row has no `account_number_last_4` and no
`routing_number_last_4` key at all. And the rows are in ascending `account_name` order, which is the
default that the `.md` export never states.

> **Divergence:** the Accounts guide states "Alongside the balance, each account carries its type, a display
> name, and the masked account and routing numbers." Six of the fourteen sandbox accounts, every `credit`
> and every `rewards` account, carry neither masked number. The guide's blanket statement is wrong; the
> schema, which marks both fields optional, is right. Any UI that renders "••••{account_number_last_4}"
> unconditionally will print `••••undefined` on credit and rewards accounts.

> **Divergence:** the schema types the three optional account fields as "string **or null**", but the API
> **omits the keys** instead of emitting `null`. This is the general rule from 4.0, and accounts are where
> it bites first.

> **Divergence:** display names are not unique and are not identifiers. `Cash (Checking)` appears twice,
> `Credit Account` four times, `Rewards` twice, `Savings` twice. Nothing in the docs says `account_name`
> can repeat. Key on `id`.

> **Divergence:** the `/accounts` cursor payload literally contains `{"sort_by":"account_name",
> "order":"asc"}`. The defaults are therefore observable from the wire even though the `.md` export omits
> them. This also means the endpoint's own cursor contradicts the "cursors are opaque" claim in the
> pagination guide.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `page_size` outside `[1..100]` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| 400 | `page_size` unparseable or repeated | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}` |
| 400 | `sort_by` not in the enum | `{"type":"1317","title":"invalid sort_by parameter: \"created_at\"","status":400}` |
| 400 | `order` not `asc`/`desc` | `{"type":"1317","title":"invalid order parameter: \"DESC\"","status":400}` |
| 400 | `page_token` garbage, cross-endpoint, or filters changed | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| 401 | Missing, empty, or non-`Bearer` Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403 | Token lacks `accounts:read`, or source IP outside the token allowlist | Documented only. Not reachable in sandbox, which performs no scope or IP checks |
| 429 | Rate limit exceeded, about 60 req/min per token | Documented only (HTML reference). Not reachable in sandbox |
| 500, 503 | Server side | Not reachable in sandbox |

#### 4.3.2 `GET /accounts/{account_id}` (GetAccount)

Returns a single account. Scope: `accounts:read`.

**Path parameters**

| Param | Type | Format | Required |
| --- | --- | --- | --- |
| `account_id` | string | `uuid` | yes |

There are no query parameters, and any that you pass are silently ignored.

**Response `200`**: the identical Account object, unwrapped, with identical nullability and identical
presence rates. Observed exhaustively: all 14 single-resource fetches are byte-for-byte deep-equal to the
corresponding row in the list response. There is no expanded detail representation and no field you can
only get from the single fetch.

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts/30000000-0000-4000-8000-000000000001' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "account_name": "Reserve Checking",
  "account_number_last_4": "0106",
  "account_type": "checking",
  "balance": { "amount": 1046, "currency": "USD" },
  "id": "30000000-0000-4000-8000-000000000001",
  "routing_number_last_4": "0089"
}
```

And the credit-account shape, which is the four-key variant:

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts/30000000-0000-4000-8000-000000000007' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "account_name": "Credit Account",
  "account_type": "credit",
  "balance": { "amount": 0, "currency": "USD" },
  "id": "30000000-0000-4000-8000-000000000007"
}
```

> **Divergence:** looping single GETs to "enrich" list rows buys nothing. This was verified across all 133
> sandbox resources of all six types: zero extra keys, zero value differences. At roughly 60 requests per
> minute per token, an enrichment loop is the fastest way to hit the rate limit for no benefit. Rho says as
> much for transactions ("most reconciliation needs no extra calls") but never states the general rule.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `account_id` not parseable as a UUID | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| 404 | Well-formed UUID that does not exist, or belongs to another business | `{"type":"1303","title":"account not found","status":404}` |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As for ListAccounts | Not reachable in sandbox |

> **Divergence:** UUID parsing is far more lenient than "string, format uuid" implies. All of these return
> `200` with the same body: canonical form, 32 hex digits with no dashes
> (`/accounts/30000000000040008000000000000001`), brace-wrapped, `urn:uuid:`-prefixed, and uppercase hex.
> The response always normalises `id` to canonical lowercase dashed form. Any cache keyed on request URL
> will store up to five copies of the same account. This is the accept-set of Go's `github.com/google/uuid`.

> **Divergence:** the `detail` string leaks the internal path-parameter name, and the names are
> inconsistent across resources: `account_id` here, but bare `id` for `/cards/{id}` and
> `/transactions/{id}`. That matches the OpenAPI declarations, so error-string matching on `detail` is
> resource-specific.

---

### 4.4 Transactions

A transaction record models one ledger event against one account. Three identity concepts matter, and Rho's
own framing is unusual enough to quote:

| Field | Rho's wording | Consequence |
| --- | --- | --- |
| `id` | "The transaction's identifier. Stable across re-fetches, but not guaranteed unique per row. The entries of one money movement can share an `id`." | `id` alone is not a primary key |
| `money_movement_id` | "Identifier shared by every transaction entry belonging to the same money movement." | The join key for the legs of a transfer |
| `account_id` | "The account the event posted against." | The disambiguator that makes `(id, account_id)` unique |

Rho's stated ingestion rule is to key on `(id, account_id)` or to group on `money_movement_id`, never on
`id` alone.

> **Divergence:** the shared-`id` case the documentation tells you to defend against is **never
> demonstrated**. All 72 sandbox transaction ids are distinct, and all 7 multi-leg money movements have
> distinct ids per leg. Observed, movement `40000000-0000-4000-8000-000000000002`: leg
> `019f0143-3ea0-7000-8000-000000000003` on account `…0007` at `+1750`, and leg
> `019f0143-3ea0-7000-8000-000000000002` on account `…0002` at `-1750`. You cannot reproduce the failure
> mode against sandbox, so write the composite key defensively and test it with synthetic data.

> **Divergence:** the attachments section of the same Transactions guide states "A transaction `id`
> identifies one transaction", contradicting the field definition above in the same document. The file
> endpoint also has no `account_id` disambiguator, so if ids really can collide, file lookup has no way to
> express which leg it means.

**Sign convention.** There is no `direction` or `debit_credit` field. The sign of `amount.amount` is the
only directional signal and it is relative to `account_id`. Observed across 72 rows: 40 negative, 32
positive, 0 zero. Refunds are positive. `credit_repayment` is positive on the `credit` leg and negative on
the `checking` leg of the same movement.

> **Divergence:** `adjustment_credit` is **negative** (observed: a single `-4500` on Treasury Checking) and
> `adjustment_debit` is **positive** (observed: a single `+3000` on Cash (Checking)). Every other type pair
> in the dataset has the sign its name implies. Nothing in the docs defines the sign of an adjustment.
> Read the sign, never the type name.

`TransactionStatus`, all four values:

| Value | Meaning per the guide | Observed (n=72) |
| --- | --- | --- |
| `pending` | Created, funds not yet cleared | 2 |
| `settled` | Cleared the ledger | 61 |
| `failed` | Insufficient funds, returned ACH, declined card. Remains queryable for audit | 8 |
| `awaiting_approval` | "held pending action on your side, and no funds have moved while it sits in that state" | 1 |

`TransactionType`, all 33 documented values, in spec order:

| # | Value | Family | Observed (n=72) |
| --- | --- | --- | --- |
| 1 | `card_credit` | Card | 0 |
| 2 | `card_debit` | Card | 8 |
| 3 | `card_refund` | Card | 4 |
| 4 | `credit_repayment` | Credit line | 6 |
| 5 | `credit_repayment_refund` | Credit line | 4 |
| 6 | `credit_cashback` | Credit line | 0 |
| 7 | `ach_credit` | ACH | 5 |
| 8 | `ach_debit` | ACH | 6 |
| 9 | `ach_return` | ACH | 2 |
| 10 | `wire_in` | Domestic wire | 4 |
| 11 | `wire_out` | Domestic wire | 4 |
| 12 | `wire_fee` | Domestic wire | 1 |
| 13 | `international_wire_in` | International wire | 0 |
| 14 | `international_wire_out` | International wire | 2 |
| 15 | `check_deposit` | Check | 3 |
| 16 | `check_payment` | Check | 2 |
| 17 | `internal_transfer` | Internal | 4 |
| 18 | `savings_deposit` | Savings | 2 |
| 19 | `savings_withdrawal` | Savings | 2 |
| 20 | `savings_interest` | Savings | 2 |
| 21 | `treasury_deposit` | Treasury | 0 |
| 22 | `treasury_withdrawal` | Treasury | 0 |
| 23 | `treasury_fee` | Treasury | 0 |
| 24 | `treasury_interest` | Treasury | 0 |
| 25 | `treasury_maturity` | Treasury | 0 |
| 26 | `treasury_sale` | Treasury | 0 |
| 27 | `treasury_market_value_adjustment` | Treasury | 0 |
| 28 | `rewards_accrual` | Rewards | 4 |
| 29 | `rewards_cashback_redemption` | Rewards | 3 |
| 30 | `adjustment_credit` | Adjustment | 1 |
| 31 | `adjustment_debit` | Adjustment | 1 |
| 32 | `international_wire_fee` | International wire | 2 |
| 33 | `international_wire_fee_refund` | International wire | 0 |

Eleven values are never produced by the sandbox, including the entire treasury family. Values 32 and 33
appear after the adjustment pair rather than next to values 13 and 14, which is the fingerprint of an enum
already extended inside `v1`. Rho's versioning policy permits new enum values at any time, so every switch
on `transaction_type` needs a default branch.

Absent from the enum entirely: any dispute or chargeback value (the guide says "`v1` exposes no dispute
indicator"), any return variant for wires or checks, any bill-pay family, and any invoicing or receivable
family.

#### 4.4.1 `GET /transactions` (ListTransactions)

Returns a paginated list of transactions. Scope: `transactions:read`. Sixteen query parameters, more than
the other six operations combined.

**Query parameters**

| Param | Type | Default | Constraint | Enforced? |
| --- | --- | --- | --- | --- |
| `account_id` | array of string (uuid) | none | Repeatable, OR within | Format **yes** (`account_id=xyz` → `400 invalid parameter: account_id`); existence **no** (unknown well-formed UUID → `200` with 0 rows). Comma-joined values are a `400`; `account_id[]=` bracket syntax is silently ignored |
| `account_type` | array of string | none | Enum: `checking`, `credit`, `investment`, `savings`, `rewards` | **No.** `account_type=bogus`, `CHECKING` and `treasury` all return `200` with 0 rows |
| `transaction_type` | array of string | none | Enum: the 33 values above | **No.** Any string returns `200` with 0 rows |
| `status` | array of string | none | Enum: `pending`, `settled`, `failed`, `awaiting_approval` | **No.** `status=bogus` returns `200` with 0 rows |
| `user_id` | array of string (uuid) | none | Repeatable, OR within | Format yes, existence no |
| `card_id` | array of string (uuid) | none | Repeatable, OR within | Format yes, existence no |
| `search` | string | none | Free text over `counterparty_name`, `memo`, `note` | Case-insensitive unanchored substring; whitespace trimmed; SQL LIKE metacharacters escaped, not interpreted. Repeating it is a `400` |
| `initiated_after` | string (date-time) | none | Inclusive | Accepts `2026-01-01` and full RFC 3339 with a zone. A zoneless timestamp is a `400` |
| `initiated_before` | string (date-time) | none | **Exclusive** | Same formats. Empty value returns 0 rows |
| `posted_after` | string (date-time) | none | Inclusive | Same. Excludes rows with no `posted_at` |
| `posted_before` | string (date-time) | none | **Exclusive** | Same. Empty value returns 0 rows |
| `min_amount` | integer | none | Inclusive lower bound | Compares the **signed** value. `min_amount=0` returns only the 32 credits |
| `max_amount` | integer | none | Inclusive upper bound | Compares the signed value. `max_amount=0` returns only the 40 debits |
| `sort_by` | string | `"initiated_at"` | Enum: `initiated_at`, `posted_at`, `amount` | **No.** Only those three reorder; every other value, including the empty string, returns `200` in default order |
| `order` | string | `"desc"` | Enum: `asc`, `desc` | **No.** `order=sideways` returns `200` in `desc` order. `ASC` works but hashes differently into the cursor |
| `page_size` | integer | `20` | `[1 .. 100]` | **Yes** |
| `page_token` | string | none | Cursor | **Yes**, offset cursor |

Repeating an array parameter ORs its values; different parameters are ANDed. Observed:
`transaction_type=wire_in&transaction_type=wire_out` returns 8 rows (4 + 4);
`user_id` with two values returns 3 rows.

The half-open date convention (`after` inclusive, `before` exclusive) makes
`posted_after=D&posted_before=D+1` a clean accounting day. Observed:
`posted_after=2026-06-23T00:00:00Z&posted_before=2026-06-24T00:00:00Z` returns 8 rows.

Filters that do not exist: `money_movement_id` (so you cannot fetch the other legs of a movement by its
movement id), exact-match counterparty, `currency`, `has_attachments`, `tracking_number`, any
merchant-category filter, and any `updated_after` or delta cursor. There is no change feed of any kind.

> **Divergence:** `min_amount` and `max_amount` compare the signed value, which the parameter description
> ("Minimum amount in minor units") does not say. "All transactions over $100" therefore needs two queries
> or client-side filtering. An inverted amount range is the only cross-field validation in the whole API
> (`min_amount=10000&max_amount=-10000` → `400 {"type":"1317","title":"min_amount must be less than or
> equal to max_amount","status":400}`), while an inverted **date** range returns `200` with zero rows.

> **Divergence:** the three enum filters are not validated. `status=Settled`, `status=posted` and
> `account_type=treasury` are all `200` with an empty array. Contrast `/cards`, which rejects the same
> class of mistake with a `400`. Two endpoints in the same API version, opposite behaviour.

**Response `200`**: the Transaction object has 20 properties.

| # | Field | Type | Format | Required | Nullable | Present (n=72) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | string | uuid | yes | no | 72/72 | UUIDv7 in sandbox; 72 distinct |
| 2 | `money_movement_id` | string | uuid | yes | no | 72/72 | 65 distinct, 7 of them with 2 legs |
| 3 | `account_id` | string | uuid | yes | no | 72/72 | 11 distinct of 14 accounts |
| 4 | `account_type` | string enum | | yes | no | 72/72 | `checking` 42, `credit` 17, `rewards` 7, `savings` 6 |
| 5 | `initiated_at` | string | date-time | yes | no | 72/72 | Always present, seconds precision, always `Z` |
| 6 | `posted_at` | string | date-time | **no** | yes | **71/72** | Omitted on the one `awaiting_approval` row. Never `null` |
| 7 | `transaction_type` | string enum | | yes | no | 72/72 | 22 of 33 values |
| 8 | `status` | string enum | | yes | no | 72/72 | All 4 values |
| 9 | `amount` | Money | | yes | no | 72/72 | Signed; range `-5900000` to `130000000` |
| 10 | `account_name` | string | | **yes** | **no** | 72/72 | Denormalized copy of `Account.account_name` |
| 11 | `counterparty_name` | string | | yes | no | 72/72 | 37 distinct. Documented as possibly `""`; no empty string observed |
| 12 | `counterparty_logo_url` | string | uri | no | yes | **0/72** | Documented, never emitted |
| 13 | `note` | string | | no | yes | 39/72 | User-editable in Rho |
| 14 | `memo` | string | | no | yes | 39/72 | Bank or provider supplied, read-only |
| 15 | `user_id` | string | uuid | no | yes | 38/72 | 12 distinct users |
| 16 | `user_full_name` | string | | no | yes | 38/72 | Always present or absent together with `user_id` |
| 17 | `card_id` | string | uuid | no | yes | 12/72 | Exactly the `card_debit` and `card_refund` rows |
| 18 | `card_name` | string | | no | yes | 12/72 | Together with `card_id` |
| 19 | `tracking_number` | string | | no | yes | **0/72** | Documented, never emitted |
| 20 | `attachments` | array of TransactionAttachment | | **yes** | no | 72/72 | `[]` on 58 rows, 1 file on 12, 2 files on 2 |

`TransactionAttachment` is `{file_id: string(uuid), file_name: string}`, both required. There is no MIME
type, byte size, upload timestamp, uploader or document classification.

> **Divergence, the most consequential one in the core API.** The reference says `posted_at` is "Null while
> status is pending". Live behaviour contradicts it in both directions. Both `pending` rows carry a
> `posted_at`, and it equals `initiated_at` exactly. All 8 `failed` rows carry one too. The only row
> without one is the single `awaiting_approval` row, and there the key is **omitted**, not null. The
> operative rule in the fixture is "absent while awaiting approval". A client that treats
> `posted_at != null` as "posted" will count a pending authorization and a failed check as cleared. Read
> `status`. The Transactions guide states the same pending rule (`docs/v1/transactions`: "Null while the
> status is pending") and then adds that, beyond pending, `posted_at` is "not coupled to `status`" and
> should be read "as nullable whatever the status". The two Rho pages agree with each other. Both state a
> pending rule that the data contradicts.

> **Divergence:** `tracking_number` and `counterparty_logo_url` are documented in detail and emitted on
> zero of 72 transactions, including the 11 `ach_credit` and `ach_debit` rows and the 10 domestic and
> international wire transfer rows (counting neither the 2 `ach_return` rows nor the 3 wire-fee rows),
> which per the documented semantics should carry a NACHA trace number or an IMAD/OMAD. Payment-tracing
> code cannot be exercised against sandbox at all.

> **Divergence:** `memo` and `note` are documented as different things (`memo` arrives from the bank and is
> read-only, `note` is user-entered and editable). In the fixture they are present or absent strictly
> together, 39/39 and 33/33, and byte-identical on 37 of the 39. The only two that differ are the failed
> ACH rows, where `note` is the memo plus `", Error: Invalid receiving routing number."`. The distinction
> the docs draw is untestable here.

> **Divergence:** `Transaction.account_name` is `required` and non-null, while `Account.account_name` on
> the Accounts resource is optional and nullable. The same attribute has two different contracts in the
> same API version. Practically, the transaction copy is the safer one to read.

> **Divergence:** `user_id` is documented as "Null for system-initiated activity such as interest". The
> split in the fixture is clean per transaction type, but the type assignment is arguable: `wire_in` and
> `savings_deposit` carry no user, while the `ach_credit` leg of a rewards cashback is attributed to a
> named user even though it is plainly system-generated. Do not infer "a human did this" from the presence
> of `user_id`.

**Real request and response**

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions?transaction_type=card_debit&status=pending&page_size=2' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "transactions": [
    {
      "id": "019ef508-2808-7000-8000-000000000006",
      "money_movement_id": "40000000-0000-4000-8000-000000000004",
      "account_id": "30000000-0000-4000-8000-000000000009",
      "account_name": "Credit Account",
      "account_type": "credit",
      "amount": { "amount": -45000, "currency": "USD" },
      "attachments": [
        { "file_id": "af1456af-1428-4845-8b03-9c98e098ec18", "file_name": "car-service-receipt.pdf" },
        { "file_id": "104c1de5-dcd3-429d-933e-d61fd076a55c", "file_name": "car-service-itinerary.pdf" }
      ],
      "card_id": "20000000-0000-4000-8000-000000000002",
      "card_name": "Maya Thompson",
      "counterparty_name": "Graceway Car Service",
      "initiated_at": "2026-06-23T15:10:13Z",
      "posted_at": "2026-06-23T15:10:13Z",
      "status": "pending",
      "transaction_type": "card_debit",
      "user_full_name": "Maya Thompson",
      "user_id": "10000000-0000-4000-8000-000000000002"
    }
  ],
  "page": { "next_page_token": null }
}
```

The second row is elided above. It is `019ef37e-4418-7000-8000-000000000001`, a `-4947` `card_debit` on
card `…0001` with the same key set. Those two are the only `pending` rows in the fixture, which is why the
cursor is already `null` at `page_size=2`.

Note `posted_at` present and equal to `initiated_at` on a `pending` row, and note the absence of `memo`,
`note`, `counterparty_logo_url` and `tracking_number` keys rather than `null` values.

The `awaiting_approval` row is the one record in the fixture with no `posted_at` key:

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions?status=awaiting_approval' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "transactions": [
    {
      "id": "019d3e86-4482-7000-8000-000000000048",
      "money_movement_id": "40000000-0000-4000-8000-000000000065",
      "account_id": "30000000-0000-4000-8000-000000000002",
      "account_name": "Cash (Checking)",
      "account_type": "checking",
      "amount": { "amount": -1250000, "currency": "USD" },
      "attachments": [],
      "counterparty_name": "Harborline Logistics",
      "initiated_at": "2026-03-30T11:36:00Z",
      "memo": "Q3 freight invoice",
      "note": "Q3 freight invoice",
      "status": "awaiting_approval",
      "transaction_type": "ach_debit",
      "user_full_name": "Daniel Rivera",
      "user_id": "10000000-0000-4000-8000-000000000003"
    }
  ],
  "page": { "next_page_token": null }
}
```

**Sorting, observed.** Default order is `initiated_at` descending, verified against all 72 rows (the
sequence is monotonically non-increasing). `sort_by=amount` sorts on the signed value, so `order=asc` puts
the largest debit first (`-5900000`). Under `sort_by=posted_at&order=asc` the row with no `posted_at` sorts
**first**; under `desc` it sorts last. `sort_by=bogus` and `order=sideways` both return `200` in default
order, with no indication that the parameter was discarded.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | Malformed UUID in `account_id`, `user_id` or `card_id` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| 400 | Unparseable or repeated scalar (`page_size`, `min_amount`, `search`, `page_token`) | `about:blank` form naming the parameter in `detail` |
| 400 | Unparseable date, including a zoneless timestamp like `2026-01-01T00:00:00` | `about:blank` form |
| 400 | `page_size` outside `[1..100]` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| 400 | `min_amount > max_amount` | `{"type":"1317","title":"min_amount must be less than or equal to max_amount","status":400}` |
| 400 | `page_token` invalid, from another endpoint, or filters changed mid-iteration | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| 401 | Missing or malformed Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403 | Missing `transactions:read`, or IP outside the allowlist | Documented only |
| 429 | Rate limited | Documented only (HTML reference) |
| **200 with 0 rows** | Misspelled enum filter value, or an empty `*_before` value | Not an error. This is the failure mode to guard against |

#### 4.4.2 `GET /transactions/{id}` (GetTransaction)

Returns a single transaction. Scope: `transactions:read`.

| Param | In | Type | Format | Required | Documented description |
| --- | --- | --- | --- | --- | --- |
| `id` | path | string | uuid | yes | Global transaction identifier |
| `account_id` | query | string | uuid | **no** | "Account ID for the transaction" |

**Response `200`**: the same 20-property Transaction object, unwrapped. Verified deep-equal to the list row
on all 72 transactions.

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "id": "019ef508-2808-7000-8000-000000000006",
  "money_movement_id": "40000000-0000-4000-8000-000000000004",
  "account_id": "30000000-0000-4000-8000-000000000009",
  "account_name": "Credit Account",
  "account_type": "credit",
  "amount": { "amount": -45000, "currency": "USD" },
  "attachments": [
    { "file_id": "af1456af-1428-4845-8b03-9c98e098ec18", "file_name": "car-service-receipt.pdf" },
    { "file_id": "104c1de5-dcd3-429d-933e-d61fd076a55c", "file_name": "car-service-itinerary.pdf" }
  ],
  "card_id": "20000000-0000-4000-8000-000000000002",
  "card_name": "Maya Thompson",
  "counterparty_name": "Graceway Car Service",
  "initiated_at": "2026-06-23T15:10:13Z",
  "posted_at": "2026-06-23T15:10:13Z",
  "status": "pending",
  "transaction_type": "card_debit",
  "user_full_name": "Maya Thompson",
  "user_id": "10000000-0000-4000-8000-000000000002"
}
```

> **Divergence, and a live footgun.** The optional `account_id` query parameter is documented with the five
> words "Account ID for the transaction" and is mentioned in neither guide. It is not a hint, it is an
> **assertion filter**. Observed on the transaction above, whose real account is
> `30000000-0000-4000-8000-000000000009`:
>
> ```bash
> # correct account: 200
> curl -s -o /dev/null -w '%{http_code}\n' \
>   'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006?account_id=30000000-0000-4000-8000-000000000009' \
>   -H 'Authorization: Bearer sandbox'
>
> # a different real account: 404
> curl -s \
>   'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006?account_id=30000000-0000-4000-8000-000000000002' \
>   -H 'Authorization: Bearer sandbox'
> # {"type":"1303","title":"transaction not found","status":404}
> ```
>
> A stale or guessed `account_id` turns an existing transaction into a `404`. Pass it only when you are
> certain, which in practice means only when you took it from the same transaction record.

Also never stated anywhere: what the endpoint returns when an `id` genuinely matches multiple entries and
`account_id` is omitted (first match, arbitrary leg, `400`, a list?), and whether `account_id` becomes
required in that case. The sandbox cannot answer it because no id collision exists there.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `id` not parseable as a UUID | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: id"}` |
| 400 | `account_id` query value not parseable | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| 404 | Unknown id, or `account_id` that does not match the transaction | `{"type":"1303","title":"transaction not found","status":404}` |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As elsewhere | Not reachable in sandbox |

#### 4.4.3 `GET /transactions/{transaction_id}/files/{file_id}` (GetTransactionFile)

"Returns file metadata and a fresh, short-lived signed download URL." Scope: `transactions:read`. This is
the only way to get bytes: transaction responses carry stable attachment descriptors and never URLs.

**Path parameters**

| Param | Type | Format | Required | Source |
| --- | --- | --- | --- | --- |
| `transaction_id` | string | uuid | yes | The transaction's `id` |
| `file_id` | string | uuid | yes | An `attachments[].file_id` value from that transaction |

No query parameters; any passed are ignored.

**Response `200`**: exactly three keys, all required.

| Field | Type | Format | Required | Notes |
| --- | --- | --- | --- | --- |
| `file_id` | string | uuid | yes | Echoes the request |
| `file_name` | string | | yes | Original file name, for example `car-service-receipt.pdf` |
| `download_url` | string | uri | yes | Google Cloud Storage V4 signed URL |

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006/files/af1456af-1428-4845-8b03-9c98e098ec18' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "download_url": "https://rho-api-sandbox.files.rho.co/8dd93c7776de909c0546477c.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=file-service%40pledge-218909.iam.gserviceaccount.com%2F20260912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260912T002646Z&X-Goog-Expires=899&X-Goog-SignedHeaders=host&X-Goog-Signature=0937465ff53c011a…",
  "file_id": "af1456af-1428-4845-8b03-9c98e098ec18",
  "file_name": "car-service-receipt.pdf"
}
```

Fetch the URL immediately, without an `Authorization` header. Observed: the signed URL returns `200
application/pdf`; it is **not** single-use (three fetches, three `200`s); it honours `HEAD` and `Range`
(`Range: bytes=0-9` → `206`); stripping the query string gives `403 AccessDenied`; altering one signature
character gives `403 SignatureDoesNotMatch`.

> **Divergence:** the TTL is never documented. The Transactions guide says only "short-lived", while the
> Statements guide commits to "up to 15 minutes" for its `pdf_url`. Observed here on every call:
> `X-Goog-Expires=899` seconds, that is 14 minutes 59 seconds, measured from `X-Goog-Date`. Both values are
> readable from the URL itself, so compute the deadline locally instead of discovering expiry from a failed
> download. Unlike statement URLs, transaction file URLs are minted fresh on every request, so there is no
> signing cache to work around.

> **Divergence:** `file_id` is documented as a "stable attachment identifier" and is **not** unique per
> transaction. Observed: `cdc328c1-c3a3-4670-a371-28e34891ee68` (`credit-repayment-receipt.pdf`) is
> attached to two different transactions in two different money movements, and both resolve to the same
> storage blob. 16 attachment rows across 15 distinct file ids. The real key is the
> `(transaction_id, file_id)` pair, exactly as the path implies, but nothing in the docs says a file can be
> shared.

> **Divergence:** there is no way to list a transaction's files independently. `GET
> /transactions/{id}/files` returns the Go router's plain-text `404 page not found`, not problem+json. Your
> only inventory is the `attachments` array on the transaction itself, and a client that parses every error
> body as JSON will throw on this one.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `transaction_id` unparseable | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: transaction_id"}` |
| 400 | `file_id` unparseable | Same form, `"detail":"invalid parameter: file_id"` |
| 404 | Unknown `file_id` | `{"type":"1303","title":"transaction file not found","status":404}` |
| 404 | Real `file_id` under the wrong transaction | Byte-identical to the above |
| 404 | Real `file_id` under a transaction with no attachments | Byte-identical |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As elsewhere | Not reachable in sandbox |

The parent-child relationship is enforced and a mismatched pairing is indistinguishable from an unknown
file. That is correct IDOR-resistant behaviour: the handler never reveals that the file exists elsewhere. It
also means you cannot distinguish "wrong parent" from "no such file" by response alone, so log the pair you
sent.

There is no upload, no delete, and no way to attach a file. The whole surface is read-only.

---

### 4.5 Cards

The Cards API exposes the physical and virtual cards belonging to the business linked to the token. Both
operations require `cards:read`. Security posture, quoted: "Only the last four PAN digits are returned; full
card numbers, CVCs, and expiration dates are not available through these endpoints." There is no
`expires_at` field at all; `usage_ends_at` is a usage-window control, not the PAN expiry.

An unfiltered list includes canceled and expired cards so their stable ids stay joinable to historical
transactions. To exclude them you must pass an explicit `status` filter.

`CardType`: `physical`, `virtual`. Observed 4 and 4.

`CardStatus`, all 11 values in spec order:

| Value | Reading | Observed (n=8) | Accepted as a filter value? |
| --- | --- | --- | --- |
| `printing` | Fulfilment | 0 | Yes, `200` with 0 rows |
| `shipped` | Fulfilment | 0 | Yes |
| `out_for_delivery` | Fulfilment | 0 | Yes |
| `activate_card` | Delivered, awaiting activation | 0 | Yes |
| `delivery_canceled` | Fulfilment | 0 | Yes |
| `active` | Usable | 4 | Yes |
| `expiring` | Usable | 0 | Yes |
| `locked` | Not usable, reversible | 1 | Yes |
| `canceled` | Not usable, terminal | 1 | Yes |
| `suspended` | Not usable | 1 | Yes |
| `expired` | Not usable | 1 | Yes |

All 11 are accepted by the filter (verified one by one), which is the only machine-readable confirmation of
the full enum, since the `.md` export omits query-parameter enums. Rho never documents the difference
between `locked` and `suspended`, which transitions are possible, or which statuses a virtual card can
reach. From the help centre, which is product behaviour rather than API contract: `locked` is the
user-toggled Lock Card state and is reversible; `canceled` is terminal; a fixed-limit card locks itself once
its transactions fully settle.

> **Divergence:** `cards.status` spells it `canceled` with one L, while the Invoicing resource in the same
> API version spells it `cancelled`. The filter enforces the difference: `GET /cards?status=cancelled`
> returns `400 {"type":"1317","title":"invalid status parameter: \"cancelled\"","status":400}`. A shared
> status mapper across products will break on this.

`CardSpendingLimitType`, all 7 values, with Rho's reset semantics:

| Value | Reset behaviour | `spend_period_end` | Observed (n=8) |
| --- | --- | --- | --- |
| `daily` | Eastern Time (America/New_York) calendar boundary | non-null | 1 |
| `weekly` | ET calendar boundary | non-null | 0 |
| `monthly` | ET calendar boundary | non-null | 6 |
| `quarterly` | ET calendar boundary | non-null | 0 |
| `annual` | Anniversary of when the limit took effect, not a calendar boundary | non-null | 0 |
| `fixed` | Lifetime ceiling, does not reset | **null** | 1 |
| `single_use` | Spent after one use | **null** | 0 |

The spec's own enum order is `fixed`, `monthly`, `single_use`, `annual`, `daily`, `weekly`, `quarterly`,
again suggesting the last three were added later.

Merchant controls use either the `blocked_*` fields or the `allowed_*` fields, never both. There is no
explicit `control_mode` discriminator: the mode is expressed purely by which keys are present.

#### 4.5.1 `GET /cards` (ListCards)

Scope: `cards:read`.

**Query parameters**

| Param | Type | Default | Constraint | Enforced? |
| --- | --- | --- | --- | --- |
| `user_id` | array of string (uuid) | none | Cardholder user ids, repeatable, OR within | Format **yes** (`user_id=nope` → `400 invalid parameter: user_id`); existence no (`200` with 0 rows) |
| `type` | array of string | none | Enum: `physical`, `virtual` | **Yes.** `type=plastic`, `type=Virtual` and `type=virtual,physical` all return `400 invalid type parameter: "<value>"` |
| `status` | array of string | none | Enum: the 11 `CardStatus` values | **Yes.** `status=frozen` → `400 invalid status parameter: "frozen"` |
| `page_size` | integer | `20` | `[1 .. 100]` | **Yes** |
| `page_token` | string | none | Cursor | **Yes**, offset cursor |

OR within a parameter, AND across parameters. Observed: `status=active&status=locked` → 5 cards;
`type=virtual&status=active` → 2 cards.

> **Divergence:** ListCards has **no `sort_by` and no `order`**, unlike the other two list operations. The
> parameters are not merely undocumented, they are not parsed: passing `sort_by=bogus` returns `200` with
> all 8 cards and does not even change the cursor fingerprint. Card ordering is undefined by the contract.
> Observed order is ascending by `id`. Do not depend on it.

> **Divergence:** `page_size` is documented on this operation as "Number of cards to return. Defaults to
> 20" with no maximum stated in the `.md` export. The server enforces `[1 .. 100]` here exactly as
> elsewhere, and says so in the error.

**Response `200`**: the Card object has 20 properties, 16 of them `required`.

| # | Field | Type | Required | Nullable | Present (n=8) | Nulls | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | string (uuid) | yes | no | 8/8 | 0 | Joins to `Transaction.card_id` |
| 2 | `name` | string | yes | no | 8/8 | 0 | Free text, user-editable, not unique |
| 3 | `last_4` | string, `^[0-9]{4}$` | yes | no | 8/8 | 0 | String because of leading zeroes; `"0042"` observed |
| 4 | `type` | enum | yes | no | 8/8 | 0 | `physical` \| `virtual` |
| 5 | `status` | enum | yes | no | 8/8 | 0 | 5 of 11 values seen |
| 6 | `cardholder` | Cardholder | yes | no | 8/8 | 0 | `{user_id, first_name, last_name}`, all required |
| 7 | `spending_limit` | Money or null | yes | **yes** | 8/8 | **0** | Documented null when no limit |
| 8 | `spending_limit_type` | enum or null | yes | **yes** | 8/8 | **0** | Documented null when no limit |
| 9 | `current_spend` | Money or null | yes | **yes** | 8/8 | **0** | "Pending plus settled spend in the current limit window" |
| 10 | `pending_spend` | Money or null | yes | **yes** | 8/8 | **0** | "Pending portion of `current_spend`" |
| 11 | `spend_period_start` | string (date-time) or null | yes | **yes** | 8/8 | 0 | Computed in America/New_York |
| 12 | `spend_period_end` | string (date-time) or null | yes | **yes** | 8/8 | **1** | Exclusive end. Null on the `fixed` card |
| 13 | `usage_starts_at` | string (date-time) or null | yes | **yes** | 8/8 | **7** | Null when unrestricted |
| 14 | `usage_ends_at` | string (date-time) or null | yes | **yes** | 8/8 | **5** | Null when unrestricted |
| 15 | `billing_address` | Address or null | yes | **yes** | 8/8 | 0 | |
| 16 | `shipping_address` | Address or null | yes | **yes** | 8/8 | **4** | Null on all 4 virtual cards |
| 17 | `blocked_categories` | array of MerchantCategory | **no** | no | **1/8** | n/a | Key present only for a block list |
| 18 | `allowed_categories` | array of MerchantCategory | **no** | no | **1/8** | n/a | Key present only for an allow list |
| 19 | `blocked_merchants` | array of Merchant | **no** | no | **1/8** | n/a | Block list only |
| 20 | `allowed_merchants` | array of Merchant | **no** | no | **1/8** | n/a | Allow list only |

`Address`: `street` (required), `second_line` (optional, omitted on 7 of 8 billing addresses), `city`,
`subdivision`, `postal_code`, `country_code` (ISO 3166-1 alpha-2), all required except `second_line`.
`MerchantCategory`: `code` (required, fixed-width ISO 18245 MCC, a **string** with leading zeros such as
`"0742"`) and `name` (optional). `Merchant`: `name` only, no id.

**Real request and response**

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/cards?type=virtual&status=active&page_size=1' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "cards": [
    {
      "id": "20000000-0000-4000-8000-000000000001",
      "name": "Ethan Parker",
      "last_4": "0042",
      "type": "virtual",
      "status": "active",
      "cardholder": {
        "user_id": "10000000-0000-4000-8000-000000000001",
        "first_name": "Ethan",
        "last_name": "Parker"
      },
      "spending_limit": { "amount": 500000, "currency": "USD" },
      "spending_limit_type": "monthly",
      "current_spend": { "amount": 6797, "currency": "USD" },
      "pending_spend": { "amount": 1500, "currency": "USD" },
      "spend_period_start": "2026-09-01T04:00:00Z",
      "spend_period_end": "2026-10-01T04:00:00Z",
      "usage_starts_at": "2025-10-01T09:00:00Z",
      "usage_ends_at": "2026-09-01T00:00:00Z",
      "billing_address": {
        "street": "100 Broadway",
        "second_line": "Floor 5",
        "city": "New York",
        "subdivision": "NY",
        "postal_code": "10005",
        "country_code": "US"
      },
      "shipping_address": null,
      "blocked_categories": [ { "code": "0742", "name": "Veterinary services" } ],
      "blocked_merchants": [ { "name": "Petco" } ]
    }
  ],
  "page": { "next_page_token": "eyJ2IjoxLCJmIjoicUJZV2JIU015OWdGNzFVLUE1ck1uUSIsInQiOiJiMlptYzJWME9qRSJ9" }
}
```

That single record shows both null idioms on one object: `shipping_address` is explicitly `null`, while
`allowed_categories` and `allowed_merchants` are absent entirely. It also shows the leading-zero `last_4`
and the `04:00:00Z` window boundary, which is midnight EDT.

> **Divergence:** the `04:00:00Z` boundaries confirm the documented America/New_York computation, but they
> are **EDT** boundaries. An EST window would be `05:00:00Z`, which the sandbox never demonstrates because
> its windows are always recomputed against the current wall clock. A client that hard-codes `-04:00` will
> break after the November DST change. Convert with a real tz database.

> **Divergence:** `spending_limit`, `spending_limit_type`, `current_spend` and `pending_spend` are all
> documented as null when the card has no limit. None of them is ever null in the fixture: 8 of 8 cards
> carry populated objects. The no-limit card is unexercised, so the code path you write for it is untested.

> **Divergence, the largest in the Cards resource.** `current_spend` is defined as "pending plus settled
> spend in the current limit window", and every window in the fixture starts `2026-09-01`. Every card
> transaction in the fixture is dated June 2026, outside every window. Yet `current_spend` reproduces the
> sum of that card's debits exactly. Measured live, per card:
>
> | Card | Status | Limit type | `current_spend` | `pending_spend` | Sum of that card's debits | Card transactions in the fixture |
> | --- | --- | --- | ---: | ---: | ---: | --- |
> | `…0001` | active | monthly | 6797 | 1500 | 6797 | one pending `-4947`, one settled `-1850` |
> | `…0002` | active | monthly | 45000 | 8000 | 45000 | one pending `-45000` |
> | `…0003` | active | monthly | 1750 | 250 | 1750 | one settled `-1750` |
> | `…0004` | locked | daily | 6331 | 900 | 6331 | one settled `-6331` |
> | `…0005` | active | monthly | 5331 | 400 | 5331 | one settled `-5331` |
> | `…0006` | suspended | monthly | 1622132 | 50000 | 1622132 | one settled `-1622132` |
> | `…0007` | canceled | monthly | 121827 | 0 | 121827 | one settled `-121827` |
> | `…0008` | expired | fixed | 0 | 0 | 0 | four settled `card_refund`s totalling `+271816` |
>
> So `current_spend` ignores the stated window, and `pending_spend` is not the pending subset of
> `current_spend` on any card (card `…0002`'s only transaction is pending at 45000, yet `pending_spend` is
> 8000). Card `…0008` shows that refunds do not push `current_spend` negative, but Rho never says whether
> refunds net against it at all. Treat both aggregates as server-computed opaque values and do not
> calibrate an implementation against the sandbox.

> **Divergence:** card `…0001` above is `status: "active"` with `usage_ends_at: "2026-09-01T00:00:00Z"`,
> which was in the past at capture time, and with a spend window running to 2026-10-01. `status` evidently
> does not reflect the usage window. `status == "active"` is therefore **not** sufficient to conclude a
> card is usable: check `usage_starts_at` and `usage_ends_at` against now as well.

> **Divergence:** canceled, suspended, locked and expired cards still report live spend windows recomputed
> per request. Card `…0007` is `canceled` and still returns `spend_period_start: "2026-09-01T04:00:00Z"`.
> Card status does not freeze the window.

> **Divergence:** the `.md` export flattens only one level of `$ref`, so `current_spend`, `pending_spend`,
> `shipping_address`, `allowed_categories` and `allowed_merchants` have **no documented sub-fields** at
> all. Their shapes are recoverable only from the wire: `{amount, currency}` for the two money objects, the
> same six-field Address as `billing_address` for shipping, `{code, name}` for categories, `{name}` for
> merchants.

> **Divergence:** the Cards guide's example prints the MCC name as `"Eating Places and Restaurants"` (title
> case); the API returns `"Eating places and restaurants"` (sentence case). Category and merchant names are
> display strings with unstable casing. Never key on them; key on `code` for categories, and accept that
> merchants have no id at all.

> **Divergence:** a Card carries **no `account_id`**. There is no way to ask which credit line a card draws
> on. The only answer is to look at the `account_id` on that card's transactions. Observed: every card
> transaction in the fixture posts to a `credit` account (`…0007` or `…0009`), never to checking.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `type` not in `{physical, virtual}` | `{"type":"1317","title":"invalid type parameter: \"Virtual\"","status":400}` |
| 400 | `status` not one of the 11 values | `{"type":"1317","title":"invalid status parameter: \"frozen\"","status":400}` |
| 400 | `user_id` not a UUID or empty | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: user_id"}` |
| 400 | `page_size` outside `[1..100]` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| 400 | Invalid or cross-endpoint `page_token` | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403 | Missing `cards:read`, or IP outside the allowlist | Documented only |
| 429, 500, 503 | As elsewhere | Not reachable in sandbox |

#### 4.5.2 `GET /cards/{id}` (GetCard)

Scope: `cards:read`. Path parameter `id`, string, `uuid`, required. No query parameters. Returns the same
20-property Card object, unwrapped. Verified deep-equal to the list row on all 8 cards.

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/cards/20000000-0000-4000-8000-000000000008' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "id": "20000000-0000-4000-8000-000000000008",
  "name": "Claire Mitchell",
  "last_4": "7732",
  "type": "physical",
  "status": "expired",
  "cardholder": {
    "user_id": "10000000-0000-4000-8000-000000000009",
    "first_name": "Claire",
    "last_name": "Mitchell"
  },
  "spending_limit": { "amount": 500000, "currency": "USD" },
  "spending_limit_type": "fixed",
  "current_spend": { "amount": 0, "currency": "USD" },
  "pending_spend": { "amount": 0, "currency": "USD" },
  "spend_period_start": "2025-03-01T12:00:00Z",
  "spend_period_end": null,
  "usage_starts_at": null,
  "usage_ends_at": "2026-06-30T23:59:59Z",
  "billing_address": {
    "street": "350 Fifth Ave",
    "city": "New York",
    "subdivision": "NY",
    "postal_code": "10118",
    "country_code": "US"
  },
  "shipping_address": {
    "street": "350 Fifth Ave",
    "second_line": "Floor 20",
    "city": "New York",
    "subdivision": "NY",
    "postal_code": "10118",
    "country_code": "US"
  }
}
```

This is the `fixed`-limit case, and it matches the documented rule exactly: `spend_period_end` is `null`
because a lifetime ceiling does not reset, and `spend_period_start` is when the lifetime total began. Note
that its `12:00:00Z` start is not an ET midnight boundary, unlike every other card in the fixture, and that
all four merchant-control keys are absent because this card has no controls.

The Cards guide states the `404` semantics explicitly, and they are the only place in the corpus where Rho
commits to `404` rather than `403` for another business's resource: "The endpoint returns `404` when the
card does not exist or belongs to another business."

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `id` not parseable as a UUID | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: id"}` |
| 404 | Unknown card, or a card belonging to another business | `{"type":"1303","title":"card not found","status":404}` |
| 404 | An id of the wrong type, for example an account UUID | Same body. Clean type isolation, no cross-namespace resolution |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As elsewhere | Not reachable in sandbox |

---

### 4.6 Joining the three resources

The edges that actually exist in the payloads:

| From | Field | To | Integrity in the fixture |
| --- | --- | --- | --- |
| Transaction | `account_id` | Account `id` | 11 distinct refs, 11 resolve, 0 dangling |
| Transaction | `card_id` | Card `id` | 8 distinct refs, 8 resolve, 0 dangling |
| Transaction | `user_id` | Cardholder `user_id` | 8 of the 12 transaction users hold a card |
| Transaction | `money_movement_id` | nothing | No `/money-movements` endpoint exists |
| Transaction | `attachments[].file_id` | GetTransactionFile | 16 rows, 15 distinct ids, all resolve |
| Card | `cardholder.user_id` | nothing | No `/users` endpoint exists |

Practical consequences:

1. **A transaction is self-sufficient for reconciliation.** It carries `account_id`, `account_type` and
   `account_name` denormalized, plus `card_id`/`card_name` and `user_id`/`user_full_name` when they apply.
   Fetch `/accounts` once for balances and masked numbers and cache it for the job.
2. **Group on `money_movement_id` before presenting transfers.** 7 of 65 movements have two legs that sum
   to zero. A client that does not group will double count every internal transfer and credit repayment.
   There is no filter on `money_movement_id`, so grouping must happen client-side over a paged window.
3. **Cards to accounts has no direct edge.** Infer it from the `account_id` on that card's transactions.
4. **Users are referenced but never listable.** There is no `/users` endpoint, so a `user_id` can only be
   turned into a name if that user appears as a cardholder or on a transaction you can see. Four of the 12
   fixture users hold no card.
5. **Canceled and expired cards keep resolving.** `Transaction.card_name` still equals `Card.name` for the
   `canceled` and `expired` cards, which is exactly why they stay in unfiltered lists.

### 4.7 Divergence index for this section

| # | Operation | Documentation says | Live behaviour |
| --- | --- | --- | --- |
| 1 | all seven | `.md` export is the reference | `.md` drops scopes, defaults, ranges, formats, query enums, nullability markers and the entire `429` response |
| 2 | all seven | Auth guide lists 3 scopes | OpenAPI lists 5; `cards:read` is required and missing from the guide |
| 3 | all seven | Optional fields are "string or null" | Optional fields are **omitted**; only `required` + nullable fields emit `null` |
| 4 | list ops | Cursors are opaque and insert-stable | Unsigned base64url JSON; `offset:N` on transactions and cards, keyset only on accounts |
| 5 | ListAccounts | Every account carries masked account and routing numbers | 6 of 14 carry neither key |
| 6 | ListAccounts | (silent) | `account_name` is not unique; four accounts share `Credit Account` |
| 7 | ListAccounts | (silent, `.md`) | Defaults are `sort_by=account_name`, `order=asc`, `page_size=20` |
| 8 | ListTransactions | `posted_at` is "Null while status is pending" | Present on both pending and all 8 failed rows; absent on the `awaiting_approval` row |
| 9 | ListTransactions | `tracking_number`, `counterparty_logo_url` documented in detail | Emitted on 0 of 72 rows |
| 10 | ListTransactions | `memo` is bank-supplied, `note` is user-edited | Byte-identical on 37 of 39 rows, present or absent strictly together |
| 11 | ListTransactions | `Transaction.account_name` required non-null | `Account.account_name` optional and nullable for the same attribute |
| 12 | ListTransactions | Enum filters are enums | `status`, `account_type`, `transaction_type` are unvalidated: garbage gives `200 []` |
| 13 | ListTransactions | `sort_by` and `order` are enums | Unvalidated; unknown values silently fall back to the default |
| 14 | ListTransactions | `min_amount`/`max_amount` in minor units | Compare the **signed** value; inverted range is the only cross-field `400` |
| 15 | GetTransaction | `account_id` is "Account ID for the transaction" | An assertion filter: a wrong value turns `200` into `404` |
| 16 | GetTransaction | `id` may be shared across entries | All 72 ids distinct; multi-leg movements have distinct ids per leg |
| 17 | GetTransactionFile | "A transaction `id` identifies one transaction" | Contradicts the `id` definition in the same guide |
| 18 | GetTransactionFile | `download_url` is "short-lived" | `X-Goog-Expires=899` seconds, minted fresh per request, not single-use, honours `Range` |
| 19 | GetTransactionFile | `file_id` is a stable attachment identifier | One `file_id` is attached to two transactions; the real key is the pair |
| 20 | ListCards | `spending_limit`, `spending_limit_type`, `current_spend` null when no limit | Never null across all 8 cards |
| 21 | ListCards | `current_spend` is spend "in the current limit window" | Equals total card debits regardless of the window; `pending_spend` matches nothing |
| 22 | ListCards | (silent) | No `sort_by`/`order`; card order is undefined by contract |
| 23 | ListCards | `status` is a lifecycle field | `active` with an elapsed `usage_ends_at` is possible; status does not imply usability |
| 24 | ListCards | (silent) | `canceled` (cards) versus `cancelled` (invoicing) in one API version; the filter rejects the wrong spelling |
| 25 | GetCard | `id` is "string, format uuid" | Five spellings accepted (no dashes, braces, `urn:uuid:`, uppercase), normalised only in the body |
| 26 | all seven | Errors are RFC 9457 problem details with `type` example `about:blank` | Three dialects in practice: `about:blank` with `detail`, numeric `1317`/`1303`/`2` without `detail`, and a plain-text `404 page not found` for unrouted paths |
