## 5. Endpoint reference: Statements, Invoicing and the file endpoints

This section covers the remaining seven operations of the `v1` surface. Accounts, Cards and Transactions are in the section "Endpoint reference: Accounts, Cards and Transactions"; cursor mechanics are in "Pagination"; token format, scopes and the 401 body are in "Authentication and scopes"; the full error-code catalogue is in "Errors and failure modes". Everything below assumes the shared contract described there: integer minor units paired with an ISO 4217 `currency`, ISO 8601 UTC timestamps, RFC 9457 `application/problem+json` errors, and read-only `GET` access (every write verb on every path in this section returns `405` with `Allow: GET` and an empty body).

All observed behavior in this section was reproduced live against `https://rhoapi-sandbox.rho.co/api/v1` on 2026-09-12 between 00:24Z and 00:31Z UTC, with `Authorization: Bearer sandbox`. Sandbox accepts any non-empty bearer token. Every command below is runnable as written after:

```bash
export RHO=https://rhoapi-sandbox.rho.co/api/v1
export RHO_API_TOKEN=sandbox
```

For production substitute `https://rhoapi.rho.co/api/v1` and a real `rhobat_`-prefixed token.

### 5.1 The seven operations

| Operation id | Method and path | Scope | Returns |
| --- | --- | --- | --- |
| `liststatements` | `GET /statements` | `statements:read` | `{ statements: [...], page: {...} }` |
| `getstatement` | `GET /statements/{id}` | `statements:read` | bare `Statement` |
| `listinvoicinginvoices` | `GET /invoicing/invoices` | `invoicing:read` | `{ invoices: [...], page: {...} }` |
| `getinvoicinginvoice` | `GET /invoicing/invoices/{invoice_id}` | `invoicing:read` | bare `Invoice` |
| `getinvoicinginvoicefile` | `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | `invoicing:read` | `{ file_id, file_name, download_url }` |
| `listinvoicingcustomers` | `GET /invoicing/customers` | `invoicing:read` | `{ customers: [...], page: {...} }` |
| `getinvoicingcustomer` | `GET /invoicing/customers/{customer_id}` | `invoicing:read` | bare `Customer` |

The scope column is inferred, not stated per operation. The official per-operation reference pages carry only `Security: AccessToken`; the scope list appears once, on the OpenAPI index page (`docs.rho.co/api/v1/openapi`), which enumerates `accounts:read`, `cards:read`, `invoicing:read`, `statements:read`, `transactions:read`. The Invoicing guide adds that "Every endpoint requires the `invoicing:read` scope."

> **Divergence:** the Authentication guide lists only three scopes (`accounts:read`, `transactions:read`, `statements:read`). It omits both `cards:read` and `invoicing:read`, which the OpenAPI index does list. An integrator who provisions a token from the Authentication page alone will not know `invoicing:read` exists. Related: the Getting Started page still says "Current release is read-only and covers accounts and transactions", which was true of an earlier release and is not true of `v1` as shipped.

A structural point that saves work across all seven: **the single-resource GET returns exactly the same fields as the list element.** A prior exhaustive sweep compared all 146 sandbox resources across six resource types (14 accounts, 8 cards, 72 transactions, 33 statements, 7 customers, 12 invoices) and found 146 of 146 deep-equal, zero keys present only in the single GET, zero value differences. There is no summary-versus-detail tier anywhere in `v1`. Looping single GETs to enrich list rows buys nothing and burns the documented ~60 requests per minute per token. The single exception is `GET /statements/{id}`, which buys a possibly re-signed `pdf_url` and nothing else (see 5.6).

---

### 5.2 Read this first: the invoice file endpoint returns 404 on every documented-correct pairing

> **Divergence:** `GET /invoicing/invoices/{invoice_id}/files/{file_id}` is documented as the way to exchange an invoice's `file_id` for a signed PDF link. In sandbox it returns `404 {"type":"1303","title":"invoice file not found","status":404}` for **every one of the 9 invoices that advertise a `file_id`**, using exactly the `invoice_id` and `file_id` values those invoices return. Invoice PDF retrieval cannot be integration-tested against the Rho sandbox at all.

The Invoicing guide is explicit about the flow that fails:

> "When an invoice has a PDF, `file_id` is present. When no PDF exists, the field is omitted. Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`; do not persist that URL."

Observed, 2026-09-12 00:25Z. Reproduce the whole sweep:

```bash
curl -s "$RHO/invoicing/invoices?page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json
for i in json.load(sys.stdin)["invoices"]:
    if "file_id" in i:
        print(i["invoice_number"], i["id"], i["file_id"])
' \
| while read num iid fid; do
    code=$(curl -s -o /dev/null -w "%{http_code}" \
      "$RHO/invoicing/invoices/$iid/files/$fid" \
      -H "Authorization: Bearer $RHO_API_TOKEN")
    echo "$num $fid -> $code"
  done
```

Result, all nine:

| Invoice | `invoice_id` | `file_id` | HTTP |
| --- | --- | --- | --- |
| INV-2026-0070 | `70000000-0000-4000-8000-000000000010` | `50000000-0000-4000-8000-000000000027` | 404 |
| INV-2026-0066 | `70000000-0000-4000-8000-000000000002` | `50000000-0000-4000-8000-000000000021` | 404 |
| INV-2026-0060 | `70000000-0000-4000-8000-000000000003` | `50000000-0000-4000-8000-000000000022` | 404 |
| INV-2026-0052 | `70000000-0000-4000-8000-000000000011` | `50000000-0000-4000-8000-000000000028` | 404 |
| INV-2026-0050 | `70000000-0000-4000-8000-000000000008` | `50000000-0000-4000-8000-000000000026` | 404 |
| INV-2026-0045 | `70000000-0000-4000-8000-000000000005` | `50000000-0000-4000-8000-000000000024` | 404 |
| INV-2026-0043 | `70000000-0000-4000-8000-000000000007` | `50000000-0000-4000-8000-000000000025` | 404 |
| INV-2026-0040 | `70000000-0000-4000-8000-000000000004` | `50000000-0000-4000-8000-000000000023` | 404 |
| INV-2026-0002 | `70000000-0000-4000-8000-000000000001` | `50000000-0000-4000-8000-000000000020` | 404 |

The remaining 3 invoices (INV-2026-0065, INV-2026-0041, INV-2026-0001) omit `file_id` entirely, so per the documented contract they have no PDF and are not expected to work.

#### Why this is a fixture gap and not a missing route

Four probes localize the failure precisely. Run them and you can stop suspecting your own code.

```bash
INV=70000000-0000-4000-8000-000000000010
FID=50000000-0000-4000-8000-000000000027

# 1. Documented-correct pairing: 404, the handler ran and the invoice resolved.
curl -s "$RHO/invoicing/invoices/$INV/files/$FID" -H "Authorization: Bearer $RHO_API_TOKEN"

# 2. Malformed file_id: 400 from the validation layer, so the route exists and parses.
curl -s "$RHO/invoicing/invoices/$INV/files/abc" -H "Authorization: Bearer $RHO_API_TOKEN"

# 3. Unknown invoice, known file_id: the error names the INVOICE, not the file.
curl -s "$RHO/invoicing/invoices/70000000-0000-4000-8000-999999999999/files/$FID" \
  -H "Authorization: Bearer $RHO_API_TOKEN"

# 4. Control: the equivalent transactions endpoint works in the same sandbox.
curl -s "$RHO/transactions/019f0554-0bf0-7000-8000-00000000000a/files/2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

| Probe | HTTP | Body |
| --- | --- | --- |
| 1. correct pairing | 404 | `{"type":"1303","title":"invoice file not found","status":404}` |
| 2. malformed `file_id` | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: file_id"}` |
| 3. unknown `invoice_id` | 404 | `{"type":"1303","title":"invoice not found","status":404}` |
| 4. transaction file control | 200 | `{"download_url":"https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?...","file_id":"2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15","file_name":"parking-receipt.pdf"}` |

Reading: probe 2 proves the route is mounted and its parameter validation runs. Probe 3 proves the handler resolves the invoice first and reports `invoice not found` when it cannot, so the `invoice file not found` in probe 1 means the invoice resolved and the **file** did not. Probe 4 proves the signed-URL machinery is alive in this sandbox. The conclusion is that the invoice objects advertise `file_id` values with no blob behind them. It is a fixture-data gap in the invoicing domain, not a sandbox-wide gap and not a routing bug.

Two further observations that matter when you write error handling:

- A real `file_id` under the wrong invoice returns the identical `404 invoice file not found`. Observed: `file_id` `...0027` (belonging to INV-2026-0070) requested under invoice `70000000-0000-4000-8000-000000000002` returns 404, not 403. This is correct IDOR-resistant behavior, but it means a genuine "wrong parent", a genuine "file absent", and this fixture gap are **indistinguishable from the response alone**.
- Requesting any `file_id` on an invoice that omits `file_id` also returns `404 invoice file not found`. Observed against `70000000-0000-4000-8000-000000000006`.

#### What to do about it

1. Build and unit-test invoice PDF retrieval against the **transaction** file endpoint (`GET /transactions/{transaction_id}/files/{file_id}`). The response schema is byte-identical: three fields, `file_id`, `file_name`, `download_url`. The signed-URL semantics in 5.6 apply to both.
2. Do not treat `404` from this endpoint as "this invoice has no PDF". Use the presence of `file_id` on the invoice object for that, and treat the 404 as retryable-or-unavailable.
3. Note that the Transactions guide explicitly promises "Sandbox downloads contain non-empty representative fictional documents". **No equivalent promise or disclaimer appears anywhere for invoicing**, so there is no documented statement that invoice PDFs are or are not present in sandbox.
4. Verify against production before you ship. Nothing in this section establishes that the production endpoint is broken; the finding is specific to the sandbox fixture set, and production could not be probed beyond unauthenticated metadata.

---

### 5.3 Statements

#### 5.3.1 What a statement is

A `statement` record covers **one statement period for one statement type**. Period-level fields sit at the top level; the money lives in an `accounts` array. Per the Statements guide, statements are "the finalized, period-end documents Rho issues for the accounts your business holds", and `GET /statements` "Spans all statement types and all accounts in one aggregated surface."

Full payload, observed via `GET /statements/439950` (signature elided for width):

```json
{
  "id": "439950",
  "statement_type": "account",
  "period_start": "2025-05-01",
  "period_end": "2025-05-31",
  "available_at": "2025-06-02T00:31:23Z",
  "pdf_url": "https://sandbox-statements.files.rho.co/4f7150d8341cae23c6ffa33a.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=file-service%40pledge-218909.iam.gserviceaccount.com%2F20260912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260912T002403Z&X-Goog-Expires=899&X-Goog-Signature=<512 hex chars>&X-Goog-SignedHeaders=host",
  "accounts": [
    {
      "account_id": "30000000-0000-4000-8000-000000000006",
      "account_type": "checking",
      "opening_balance": { "amount": 946209, "currency": "USD" },
      "closing_balance": { "amount": 972409, "currency": "USD" },
      "total_credits":   { "amount": 26200,  "currency": "USD" },
      "total_debits":    { "amount": 0,      "currency": "USD" },
      "total_fees":      { "amount": 0,      "currency": "USD" }
    }
  ]
}
```

Top-level fields:

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `id` | string | yes | "Global statement identifier". Observed: a **numeric string**, not a UUID. Two disjoint ranges in the sandbox: credit `152980` to `200527`, deposit and treasury `428772` to `572981`. Treat as opaque. |
| `period_start` | string (date) | yes | First day of the period, inclusive. |
| `period_end` | string (date) | yes | Close date of the period, inclusive. |
| `available_at` | string (date-time) | yes | When the finalized statement became retrievable. |
| `pdf_url` | string | **no** | Signed download URL, documented "valid for up to 15 minutes", or `null` "when the document cannot be linked". See 5.6. |
| `statement_type` | string | **no** | Enum `account`, `credit`, `treasury`. Not marked required even though all 33 sandbox records carry it. |
| `accounts` | array | yes | Per-account figures. See below. |

#### 5.3.2 The per-account breakdown

Each entry in `accounts` carries one account's figures for the period. Every monetary value is a `Money` object `{ "amount": <integer minor units>, "currency": "<ISO 4217>" }`. There is no scalar amount anywhere in the statement object.

| Field | Type | Marked required | Applies to | Notes |
| --- | --- | --- | --- | --- |
| `account_id` | string | **no** | all | Documented "Null for credit statements, which are not tied to a deposit account". See the divergence below. |
| `account_type` | string | yes | all | Enum `checking`, `savings`, `credit`, `treasury`. |
| `opening_balance` | Money | yes | all | Balance as of the start of `period_start`. |
| `closing_balance` | Money | yes | all | Balance at the close date. The guide calls this "the reconciliation anchor". |
| `total_credits` | Money | yes | all | Sum of credits posted in the period. |
| `total_debits` | Money | yes | all | Sum of debits posted in the period. |
| `total_fees` | Money | yes | all | Fees charged in the period. |
| `repayment_date` | string (date) | no | credit only | Date repayment is or was due. **Never emitted**, see below. |
| `spending` | Money | no | credit only | Total card spend in the period. |
| `repayments` | Money | no | credit only | Repayments applied in the period. |
| `cashback` | Money | no | credit only | Cashback earned in the period. |

The credit-only fields are **omitted keys** on non-credit entries, not nulls. Observed across all 33 sandbox statements: the key set `{spending, repayments, cashback}` is present on exactly the 22 credit entries and absent on the other 11. `repayment_date` is present on 0 of 33.

```bash
curl -s "$RHO/statements?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json
from collections import Counter
st = json.load(sys.stdin)["statements"]
print("statements:", len(st))
print("types:", Counter(s["statement_type"] for s in st))
print("accounts[] lengths:", Counter(len(s["accounts"]) for s in st))
print("credit entries with null account_id:",
      sum(1 for s in st for a in s["accounts"]
          if a["account_type"] == "credit" and a.get("account_id") is None))
print("entries carrying repayment_date:",
      sum(1 for s in st for a in s["accounts"] if "repayment_date" in a))
print("null pdf_url:", sum(1 for s in st if s.get("pdf_url") is None))
'
```

Observed output:

```
statements: 33
types: Counter({'credit': 22, 'treasury': 7, 'account': 4})
accounts[] lengths: Counter({1: 33})
credit entries with null account_id: 0
entries carrying repayment_date: 0
null pdf_url: 0
```

That single command demonstrates four separate divergences at once.

> **Divergence:** `account_id` is documented as null on credit statements. It is non-null on all 22 sandbox credit statements, which carry `30000000-0000-4000-8000-000000000007` or `...0008`. Both IDs resolve in `GET /accounts` as real `account_type: "credit"` accounts named "Credit Account". Worse, filtering by a credit account works: `GET /statements?account_id=30000000-0000-4000-8000-000000000008&page_size=100` returns 11 credit statements, which the documented model says should be impossible. Code that detects credit statements with `account_id is None` will be wrong on every record. Use `statement_type == "credit"` or `accounts[].account_type == "credit"` instead.

> **Divergence:** `repayment_date` is documented on both statement reference pages and in the guide's per-account table as the credit repayment due date. It is absent from all 33 sandbox statements, via both `GET /statements` and `GET /statements/{id}`. There is no way to learn a credit statement's repayment due date from this API. This matters because it is the only credit-terms field in the entire surface: there is no minimum payment, no amount due, no APR and no credit limit anywhere in `v1`.

> **Divergence:** consolidated multi-account statements do not occur. The guide devotes a section, "Filtering by account", to the fact that account and treasury statements "may span multiple checking/savings accounts" and that "a matched statement's `accounts` array and PDF may include additional accounts belonging to your business". All 33 sandbox statements have exactly one `accounts` entry. The stronger evidence is a matched pair: statements `439950` (checking `...0006`) and `439951` (savings `...0013`) cover the same period 2025-05-01 to 2025-05-31, share the same `available_at` of `2025-06-02T00:31:23Z`, and have consecutive IDs. That is one statement per account, not one consolidated statement. The consolidation caveat is unverifiable here, so write the `accounts` loop defensively but do not design around consolidation you cannot observe.

> **Divergence:** `accounts[].account_type` in a statement disagrees with the same account's type in `GET /accounts`, and the two enums are disjoint in both directions. Statement `572981` reports `account_type: "treasury"` for account `30000000-0000-4000-8000-000000000004`; `GET /accounts` reports that same account as `account_type: "checking"`, `account_name: "Treasury Checking"`. The statements enum is `checking, savings, credit, treasury`; the accounts enum is `checking, credit, investment, savings, rewards`. `treasury` exists only in statements, `investment` and `rewards` only in accounts. Do not join on `account_type` across the two APIs. Join on `account_id`, which is consistent.

Observed cross-check:

```bash
curl -s "$RHO/statements/572981" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); a=d["accounts"][0]; print(d["statement_type"], a["account_id"], a["account_type"])'
# treasury 30000000-0000-4000-8000-000000000004 treasury

curl -s "$RHO/accounts?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; print([(a["account_type"], a["account_name"]) for a in json.load(sys.stdin)["accounts"] if a["id"].endswith("0004")])'
# [('checking', 'Treasury Checking')]
```

Two further statement-data facts that are not divergences but will break naive reconciliation:

- **Credit statements report `total_credits`, `total_debits` and `total_fees` as zero on all 22 records**, even where `spending` is 6,931,038 minor units. The three "required" totals are useless for credit reconciliation. The guide's advice, to anchor on `closing_balance` and use the credit trio for the card line, is the only workable path, and it does not say why the totals are empty.
- **Sign conventions are undocumented and inconsistent.** Statement `200527` has `spending: 6931038`, `repayments: -69221`, `cashback: 103965`. Statement `161396` has `spending: -26200`, `repayments: 26200`, `cashback: -327`. No reference states whether these are signed or absolute, or what a negative means. Take absolute values at your own risk.

#### 5.3.3 `GET /statements`

```bash
curl -s "$RHO/statements?period_end_after=2026-05-01&period_end_before=2026-06-01&page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

| Parameter | Type | Documented | Observed |
| --- | --- | --- | --- |
| `account_id` | array | "Return complete statements that include at least one requested account. Multiple values use OR semantics." | Confirmed. Repeated-key array style. `account_id=...0006&account_id=...0013` returns 4 statements (3 for 0006, 1 for 0013). An account with no statements returns `200` and an empty array, not 404. A malformed value returns `400 {"type":"about:blank",...,"detail":"invalid parameter: account_id"}`. |
| `statement_type` | array | "Filter by statement type". Enum not restated on the parameter. | Multi-value OR confirmed. **Unvalidated**: `statement_type=bogus` returns `200` with `"statements":[]`, not a 400. |
| `period_end_after` | string (date) | "Earliest statement close date, **inclusive**" | Confirmed inclusive. `period_end_after=2026-05-31` returns statement `572981`, whose `period_end` is 2026-05-31. |
| `period_end_before` | string (date) | "Latest statement close date, **exclusive**" | Confirmed exclusive. `period_end_after=2026-05-31&period_end_before=2026-05-31` returns 0 rows; `...&period_end_before=2026-06-01` returns 1. |
| `period_start_after` | string (date) | "Earliest statement open date, inclusive" | Confirmed. |
| `period_start_before` | string (date) | "Latest statement open date, exclusive" | Confirmed. |
| `sort_by` | string | "Sort field". No enum, no default given. | **Inert.** `sort_by=period_start`, `period_end`, `available_at`, `id`, `created_at` and `bogus` all return identical ordering and no error. It is nonetheless hashed into the pagination cursor, so changing it mid-iteration invalidates your cursor for no benefit. |
| `order` | string | "Sort direction". No enum, no default given. | Anything that lowercases to `asc` yields ascending. Every other value, including `BOGUS` and omission, yields descending. No 400 for invalid input. Observed: default first ID `572981`, `order=asc` first ID `428772`, `order=BOGUS` first ID `572981`. |
| `page_size` | integer | "Number of statements per page; max 100". Default not documented. | Default **20**. Bounds 1 to 100 enforced: `page_size=0` and `page_size=101` both return `400 {"type":"1317","title":"page_size must be between 1 and 100","status":400}`. |
| `page_token` | string | Opaque cursor from `page.next_page_token`. | See "Pagination". |

Dates accept `YYYY-MM-DD`. A non-ISO value such as `05/01/2026` returns `400` with `detail: "invalid parameter: period_end_after"`. Unknown query parameters are silently ignored with a `200`.

> **Divergence:** `*_before` means **exclusive** on statements and **inclusive** on invoicing, in the same API version, with the same idiom. Both pages document their own behavior correctly and both were verified live, so this is a deliberate asymmetry rather than a documentation bug. It is still a footgun for any shared date-range helper. See 5.4.1 for the invoicing verification.

> **Divergence:** parameter validation strictness is inconsistent across endpoints. `/statements` silently ignores an unknown `sort_by` or `order`; `/invoicing/customers` hard-rejects both with `400 {"type":"1317",...}`. Same parameter names, same version, opposite contracts. Do not write one shared "these params are safe" assumption.

**Conspicuously absent from the filter set:** there is no `available_at_after` or `available_at_before`. The guide's headline workflow is "List statements **as they become available**", and the API gives you no way to ask "what has been finalized since T". Incremental polling requires rescanning by period window and diffing IDs yourself. There is also no batch fetch by ID list, no currency filter, and no way to project only your requested account's figures out of a statement, which the guide states outright: filtering "does not remove those entries or alter the PDF".

#### 5.3.4 `GET /statements/{id}`

Path parameter `id`, string, no format stated. Response is the bare `Statement` object, identical field set to a list element, with no wrapper and no `page`.

```bash
curl -s "$RHO/statements/200527" -H "Authorization: Bearer $RHO_API_TOKEN"
```

Its documented purpose beyond simple retrieval is as the refresh mechanism for an expired `pdf_url`: "If the link lapses, re-fetch the statement with `GET /statements/{id}` for a fresh URL." That remedy does not work the way it reads. See 5.6.3.

Error behavior differs from every other resource in `v1`, because the statement ID is an opaque string rather than a UUID and therefore gets no format validation:

| Request | HTTP | Body |
| --- | --- | --- |
| `GET /statements/999999999` | 404 | `{"type":"1303","title":"statement not found","status":404}` |
| `GET /statements/abc` | 404 | same |
| `GET /statements/-1` | 404 | same |
| `GET /statements/200527/files/x` | 404 | `404 page not found` (plain text, from the Go router, not problem+json) |

> **Divergence:** for accounts, cards, transactions, invoices and customers a malformed ID is a `400` with `detail: "invalid parameter: <name>"`. For statements it is a `404`. Do not validate statement IDs as UUIDs client-side, and do not treat 400-versus-404 as a uniform contract across the API.

Note the last row: **there is no `GET /statements/{id}/files/{file_id}` analogue.** Statements are the only resource in `v1` that embeds a signed URL directly in its payload, and the only refresh path is a full single-statement re-fetch.

#### 5.3.5 Statement census and timing

The sandbox fixture, observed 2026-09-12, is 33 statements, all USD, `period_start` from 2024-07-01 to 2026-05-01.

| `statement_type` | Count | Accounts involved | ID range |
| --- | --- | --- | --- |
| `credit` | 22 | `...0007` (calendar-month cycle), `...0008` (13th to 12th cycle) | 152980 to 200527 |
| `treasury` | 7 | `...0004` | 462701 to 572981 |
| `account` | 4 | `...0006` checking, `...0013` savings | 428772 to 439951 |

Two backing ID ranges, consistent with a deposit ledger and a card ledger stitched into "one aggregated surface". The Versioning guide already tells you to "Treat IDs as opaque strings"; this is why.

`available_at` lag varies by type and is documented only on the product side, not in the API:

| Type | Observed lag | Help-center rule |
| --- | --- | --- |
| `account` (checking, savings) | available on the 2nd of the following month, 00:20Z to 00:31Z | "Checking Account Statements are available on the second calendar day of every month"; "Savings Account Statements are available by the end of the fifth business day of each month" |
| `credit` | the day after `period_end`, 04:00Z to 05:02Z | Card accounts with Daily Terms "on the fifth of every month"; with Monthly Terms "one business day following the statement repayment date" |
| `treasury` | between the 5th and the 8th, 21:00Z to 22:06Z | not covered by the help-center page |

> **Divergence:** the savings statement `439951` became available at `2025-06-02T00:31:23Z`, that is the 2nd of the month, not "by the end of the fifth business day" as the help center states for savings. Neither the observed treasury lag nor the observed credit cycle for account `...0008` (13th to 12th) corresponds to any documented rule. Nothing in the API exposes the billing cycle or the terms; you have to infer them from `period_start` and `period_end`.

Also undocumented: whether a statement can ever be reissued or restated after `available_at`, and what condition produces a `null` `pdf_url`. Zero of 33 sandbox records exercise the null case.

---

### 5.4 Invoicing: invoices

Two resources plus one file exchange. Customers are "the businesses you bill" and are soft-deletable. Invoices are "issued documents" and reference exactly one customer by ID. An invoice has at most one PDF, addressed by `file_id`.

IDs in this domain are UUIDs, as the guide states: customers `60000000-0000-4000-8000-00000000000X`, invoices `70000000-0000-4000-8000-0000000000XX`, invoice files `50000000-0000-4000-8000-000000000XXX`, users `40000000-0000-4000-8000-00000000000X`. Note that invoice IDs are UUIDs while **statement IDs are not**, inside the same `v1` surface. Transaction IDs, which appear on invoice payments, are UUIDv7-shaped, a third format again.

#### 5.4.1 `GET /invoicing/invoices`

"Results are ordered by creation time, newest first. Ordering is not user-configurable; keep filters unchanged while paginating."

| Parameter | Type | Documented | Observed |
| --- | --- | --- | --- |
| `status` | array | "Filter by one or more invoice statuses" | Multi-value OR confirmed. **Unvalidated**: `status=draft`, `status=sent` and `status=bogus` all return `200` with zero rows rather than a 400. Since `draft` and `sent` are plausible-sounding non-values (see 5.4.4), this silently returns an empty result for a reasonable-looking query. |
| `date_after` | string (date) | "Earliest invoice issue date to include, inclusive" | Confirmed. |
| `date_before` | string (date) | "Latest invoice issue date to include, **inclusive**" | Confirmed inclusive. |
| `due_date_after` | string (date) | "Earliest invoice due date to include, inclusive" | Confirmed. |
| `due_date_before` | string (date) | "Latest invoice due date to include, **inclusive**" | Confirmed inclusive: `due_date_after=2026-07-31&due_date_before=2026-07-31` returns INV-2026-0066, due exactly 2026-07-31. |
| `page_size` | integer | "Defaults to 20." Max not documented. | Default 20 confirmed. Bounds 1 to 100 enforced with the same `1317` body as statements. |
| `page_token` | string | Cursor; "keep all filters unchanged". | See "Pagination". |

`sort_by` and `order` are **not documented parameters here**. Observed: they are accepted and ignored. `GET /invoicing/invoices?sort_by=date&order=asc` returns INV-2026-0070 first, identical to the unparameterized call. That is consistent with "Ordering is not user-configurable".

**Conspicuously absent: there is no `customer_id` filter.** There is no supported way to list one customer's invoices. `?customer_id=60000000-0000-4000-8000-000000000001` is silently ignored and returns all 12 rows. The only customer-to-invoice link the API offers is `customer.last_invoice_id`, a single most-recent pointer. Per-customer AR ageing therefore requires pulling every invoice and grouping client-side. Also missing: `invoice_number` lookup, free-text search, `created_at` or `updated_at` ranges, and an `accounting_sync_status` filter, so you cannot ask "which invoices failed to sync". There is no `include_deleted` for invoices either; passing it is ignored and returns all 12.

#### 5.4.2 The invoice object

Identical in list and get. Full payload, observed via `GET /invoicing/invoices/70000000-0000-4000-8000-000000000001`:

```json
{
  "id": "70000000-0000-4000-8000-000000000001",
  "invoice_number": "INV-2026-0002",
  "total": { "amount": 108403, "currency": "USD" },
  "tax_rate": 10,
  "discount_rate": 0,
  "status": "paid",
  "note": "Net 30 terms apply.",
  "date": "2026-01-16",
  "due_date": "2026-02-15",
  "customer": { "id": "60000000-0000-4000-8000-000000000001" },
  "line_items": [
    { "name": "Consulting Services - January", "quantity": 1, "discount_rate": 0, "tax_rate": 10,
      "unit_price": { "amount": 90000, "currency": "USD" },
      "total":      { "amount": 90000, "currency": "USD" } },
    { "name": "Travel reimbursement", "quantity": 1, "discount_rate": 0, "tax_rate": 0,
      "unit_price": { "amount": 9403, "currency": "USD" },
      "total":      { "amount": 9403, "currency": "USD" } }
  ],
  "payments": [
    { "type": "received_in_account", "external_method": null,
      "paid_at": "2026-06-21", "transaction_id": "019eebb0-0938-7000-8000-00000000000b" }
  ],
  "activities": [
    { "activity_type": "created",           "created_at": "2026-01-16T14:32:07Z", "user_id": "40000000-0000-4000-8000-000000000001", "emails": [] },
    { "activity_type": "sent",              "created_at": "2026-01-16T15:00:00Z", "user_id": "40000000-0000-4000-8000-000000000001", "emails": ["info@acmesupplies.com", "ap@acmesupplies.com"] },
    { "activity_type": "downloaded",        "created_at": "2026-01-17T09:12:00Z", "user_id": "40000000-0000-4000-8000-000000000003", "emails": [] },
    { "activity_type": "matched",           "created_at": "2026-06-21T19:37:23Z", "user_id": null, "emails": [] },
    { "activity_type": "marked_as_paid",    "created_at": "2026-06-21T19:38:00Z", "user_id": "40000000-0000-4000-8000-000000000003", "emails": [] },
    { "activity_type": "accounting_synced", "created_at": "2026-06-21T20:00:00Z", "user_id": null, "emails": [] }
  ],
  "file_id": "50000000-0000-4000-8000-000000000020",
  "accounting_sync_status": "synced",
  "accounting_synced_at": "2026-06-21T20:00:00Z",
  "created_at": "2026-01-16T14:32:07Z",
  "updated_at": "2026-06-21T20:00:00Z"
}
```

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `id` | string (UUID) | yes | Stable invoice identifier. |
| `invoice_number` | string | yes | Human-readable. Observed `INV-2026-0001` through `INV-2026-0070` with gaps. Not monotonic with `created_at` ordering and not contiguous, so never infer a count from it. |
| `total` | Money | yes | Tax-inclusive, discount-applied. Derivation in 5.4.3. |
| `tax_rate` | number | yes | Invoice-level tax **percentage**, not basis points. Observed `0`, `6.25`, `8.5`, `10`; fractional values occur. |
| `discount_rate` | number | yes | Invoice-level discount percentage. Observed `0` on 11 invoices, `5` on one. |
| `status` | string | yes | Six values. See 5.4.4. |
| `note` | string | yes | Free text shown to the customer. Marked required but **null on 3 of 12**. May contain any Unicode; INV-2026-0043's note contains a literal `U+2014` character, so do not assume ASCII. |
| `date` | string (date) | yes | Issue date. |
| `due_date` | string (date) | yes | "null when not set". Never null in sandbox, but documented nullable. |
| `customer` | object | yes | Contains **only** `customer.id`. No embedded name or email, so rendering an invoice always costs a second call to `/invoicing/customers/{id}`. |
| `line_items` | array | yes | See below. |
| `payments` | array | yes | May be empty; 5 of 12 have none. See 5.4.5. |
| `activities` | array | yes | Never empty; always at least `created`. See 5.4.6. |
| `file_id` | string (UUID) | **no** | Present on 9 of 12. **Key omitted entirely** when absent, never null. |
| `accounting_sync_status` | string | yes | Five values. See 5.4.7. |
| `accounting_synced_at` | string (date-time) | yes | Marked required but **null on 5 of 12**. |
| `created_at` | string (date-time) | yes | The list sort key. No description in the reference. |
| `updated_at` | string (date-time) | yes | Always at or after `created_at`. |

`line_items[]`:

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | The only text field on a line. |
| `unit_price` | Money | yes | Before line-level discount and tax. |
| `quantity` | number | yes | **Fractional allowed**. Observed `2.5` on INV-2026-0066. |
| `discount_rate` | number | yes | Line-level discount percentage. |
| `tax_rate` | number | yes | "When null, the invoice-level `tax_rate` applies." Marked required and **null is the common case**, 10 of 16 sandbox lines. |
| `total` | Money | yes | Line total **after discount, before tax**. |

There is no line ID, no description separate from `name`, no unit of measure, no per-line GL code, and no ordering index.

**Conspicuously absent from the invoice object:** no invoice-level currency (only inside each `Money`), no subtotal, no tax amount, no discount amount, no amount paid, no amount due or balance, no payment-terms string (the UI collects Net 30 and Due on receipt), no recurrence or schedule field (the UI offers "Schedule this invoice to repeat"), no public payment-portal URL, no `sent_at`, and no `deleted_at`.

Because the list and get payloads are identical, **the list endpoint already returns the full activity log and every payment for every invoice**. A 100-invoice page carries 100 embedded activity arrays and there is no `expand` or `fields` parameter to trim it.

#### 5.4.3 How `total` is computed

Neither the guide nor the reference pages state the arithmetic, and the API exposes neither a subtotal nor a tax amount. Any consumer rendering an invoice must reimplement it. Derived and verified against all 12 sandbox invoices:

```
line.total.amount    = round( quantity * unit_price.amount * (1 - line.discount_rate/100) )

effective_tax(line)  = line.tax_rate if line.tax_rate is not None else invoice.tax_rate

invoice.total.amount = round( SUM( line.total.amount * (1 + effective_tax(line)/100) )
                              * (1 - invoice.discount_rate/100) )
```

Re-verified live, 12 of 12 exact, on 2026-09-12:

```bash
curl -s "$RHO/invoicing/invoices?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json
for i in json.load(sys.stdin)["invoices"]:
    sub = sum(l["total"]["amount"] * (1 + (l["tax_rate"] if l["tax_rate"] is not None else i["tax_rate"]) / 100)
              for l in i["line_items"])
    computed = round(sub * (1 - i["discount_rate"] / 100))
    print(i["invoice_number"], computed, i["total"]["amount"],
          "OK" if computed == i["total"]["amount"] else "MISMATCH")
'
```

Three non-obvious rules this establishes:

1. **Discounts compound.** INV-2026-0045 applies a 5 percent line discount (80,000 to 76,000) and then a 5 percent invoice discount (76,000 to 72,200). The invoice discount applies to the post-line-discount, post-tax subtotal, not to the gross.
2. **Tax is per line, using the line rate when set and the invoice rate when null, then summed.** It is not one invoice-level rate on a subtotal. INV-2026-0066 proves it: a flat 10 percent on its 146,000 subtotal would give 160,600, but the actual total is 158,000 because two of its four lines carry an explicit `tax_rate: 0` while the other two carry `null` and inherit the invoice's 10 percent.
3. **Rounding is to the nearest minor unit at the invoice level.** INV-2026-0052 computes to 45000.0625 and states 45000. One sample is not enough to distinguish half-up from half-even from truncation.

#### 5.4.4 Status: the complete enum and the lifecycle

`status` is "Lifecycle status of an invoice in Invoicing". Exactly six values, in reference order:

| Value | Meaning | Sandbox count | Example |
| --- | --- | --- | --- |
| `paid` | Payment complete. For the card rail the help center says "Once the payout is initiated, the invoice status changes to Paid." | 4 | INV-2026-0050, 0040, 0002, 0001 |
| `unpaid` | Issued, not yet paid. | 2 | INV-2026-0065, 0052 |
| `cancelled` | Voided by the business. British spelling. | 1 | INV-2026-0041 |
| `overdue` | Past due and unpaid. | 2 | INV-2026-0060, 0045 |
| `confirm_payment` | Funds arrived in the Rho account and were matched, awaiting confirmation or allocation by the business. | 1 | INV-2026-0043 |
| `pending_payout` | Card payment captured by Stripe, payout to the Rho checking account not yet initiated. Help center: "The invoice is marked Pending payout while Stripe prepares the deposit." | 2 | INV-2026-0070, 0066 |

**The enum has no `draft` and no `sent`.** The "sent" concept exists only as an activity, so an API consumer cannot distinguish an invoice created but never emailed from one that was emailed, except by scanning `activities` for `activity_type == "sent"`. Rho's own help copy for creating an invoice ends at "You'll see a confirmation once your invoice is successfully created and ready to send", which implies a pre-send state the API does not model.

Lifecycle reconstructed from the sandbox activity logs. Every edge below is backed by a specific record.

```text
created ──> unpaid ──> (sent) ──> unpaid ──> overdue                     [due date passes]
                           │
                           ├─> matched ──> confirm_payment ──> marked_as_paid ──> paid    [bank rail]
                           ├─> card_payment_received ──> pending_payout ──> paid          [card rail, Stripe]
                           ├─> marked_as_paid ──> paid                                    [manual, external payment]
                           └─> cancelled ──> cancelled                                    [terminal]

marked_as_paid ──> marked_as_unpaid                                      [reversal, observed]
```

| Edge | Evidence |
| --- | --- |
| Bank rail, mid-state | INV-2026-0043: activity `matched` at `2026-05-18T00:07:03Z`, one `received_in_account` payment with `transaction_id: 019e3868-5858-7000-8000-00000000001a`, status `confirm_payment`. |
| Bank rail, completion | INV-2026-0002: `matched` at `2026-06-21T19:37:23Z`, then `marked_as_paid` at `2026-06-21T19:38:00Z`, 37 seconds later, status `paid`. So `confirm_payment` is the state between match and human confirmation. |
| Card rail | INV-2026-0070: `card_payment_received` at `2026-07-18T08:00:00Z`, status `pending_payout`, payment recorded as `external` / `credit_card`. |
| Reversal | INV-2026-0066: `marked_as_paid` at `2026-07-20T09:00:00Z`, then `marked_as_unpaid` at `2026-07-20T09:05:00Z` with `user_id: null`, then `card_payment_received` at `2026-07-24T10:00:00Z`, status `pending_payout`. |
| Cancellation terminal | INV-2026-0041: activities are only `created` and `cancelled`, with no `sent`. |

> **Divergence:** `status` is stored, not derived. INV-2026-0065 is `unpaid` with `due_date` 2026-08-15 and INV-2026-0052 is `unpaid` with `due_date` 2026-08-20. Both were past due as of the probe date, 2026-09-12, and neither is `overdue`. Do not assume `overdue == (status == "unpaid" AND due_date < today)`. Either the transition is a batch job whose cadence is undocumented, or the fixture is frozen; nothing in the docs says when `unpaid` becomes `overdue`. If your product needs a correct ageing bucket, compute it from `due_date` yourself and treat `status` as advisory for that one question.

Nothing documents whether status can move backwards other than by inference from `marked_as_unpaid`, and there is no refund or chargeback status or activity type anywhere. The Invoicing terms are explicit that Rho "has no obligation to collect, enforce, dispute, or resolve any invoice, chargeback, refund, or customer dispute on your behalf", so the absence is a product boundary, not an oversight.

#### 5.4.5 `payments[]`

| Field | Type | Marked required | Documented | Observed across 7 payments |
| --- | --- | --- | --- | --- |
| `type` | string | yes | Enum `received_in_account`, `external` | 5 `external`, 2 `received_in_account` |
| `external_method` | string | yes | "Set when type is external". Enum `cash`, `check`, `credit_card`, `other` | `credit_card` twice, `check` once, `cash` once, `other` once; `null` on both `received_in_account` rows |
| `paid_at` | string (date) | yes | "User-provided payment date; set for external payments" | **Set on all 7**, including both `received_in_account` rows |
| `transaction_id` | string | yes | "Transaction identifier when type is received_in_account" | Set on the 2 `received_in_account` rows, `null` on all 5 `external` rows |

`transaction_id` values are UUIDv7-shaped and match the ID format of `GET /transactions`, so the join to the ledger is direct. See the Transactions section for that resource.

> **Divergence:** `paid_at` is documented as "set for external payments" but is populated on `received_in_account` payments too. Observed: INV-2026-0043 has `type: "received_in_account"` with `paid_at: "2026-05-18"`, INV-2026-0002 has `paid_at: "2026-06-21"`. Harmless, but a code generator or validator built on the doc text will be surprised.

> **Divergence, and the important one:** a Rho-processed **card** payment is recorded as `type: "external"`, not `received_in_account`. INV-2026-0070 and INV-2026-0066 both show `{"type": "external", "external_method": "credit_card", "transaction_id": null}` while their activity logs contain `card_payment_received` and their status is `pending_payout`, which is the Stripe rail running inside Rho. So `external` does **not** mean "paid outside Rho"; it means "no matched Rho transaction yet". Detect the Rho card rail via the `card_payment_received` activity or `status == "pending_payout"`, never via `payments[].type`. Nothing in the docs warns about this.

**The single largest modelling gap in this surface: there is no per-payment amount field at all.** The API therefore cannot represent a partial payment, an overpayment, or a multi-payment invoice. Every sandbox invoice has at most one payment. The schema neither models nor excludes the multi-payment case, so if your AR workflow allows partial payment you cannot reconcile it from this API.

All four payment fields are marked required and all four are nullable in practice. A strict code generator that emits non-optional types from `required` will fail to deserialise real payloads on `external_method` and `transaction_id`.

Finally, none of the card economics are exposed. The Invoicing terms and the help center state a card processing fee of **2.9 percent plus $0.30 per transaction**, paid by the business, and a **$10,000 per day** card limit across all invoices. There is no fee field, no net-of-fee amount, no payout ID and no Stripe connection status in the API. An integration reconciling a card-paid invoice sees `total: 98000` while the bank receives 98000 minus (2.9 percent plus 30) = 94,858 minor units, with no API-visible link between the two.

#### 5.4.6 `activities[]`: the audit log

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `activity_type` | string | yes | Eleven values, below. |
| `created_at` | string (date-time) | yes | No description in the reference. |
| `user_id` | string (UUID) | yes | "User associated with the activity when available". **Null on 12 of 44** sandbox activities, all system-generated. |
| `emails` | array of string | yes | Always present. Empty array on 32 of 44. |

Complete enum with observed frequency across the 12 sandbox invoices (44 activities total):

| `activity_type` | Count | `user_id` | `emails` | Interpretation |
| --- | --- | --- | --- | --- |
| `created` | 12 | always set | empty | Invoice created. Present on every invoice, and its `created_at` equals the invoice's `created_at` on all 12. |
| `sent` | 10 | always set | 1 or 2 recipients | Invoice emailed. Absent on INV-2026-0041 (cancelled) and INV-2026-0001. |
| `downloaded` | 2 | set | empty | PDF downloaded. |
| `matched` | 2 | **always null** | empty | Incoming bank transaction auto-matched to the invoice. |
| `marked_as_paid` | 5 | set | empty | Manual mark-as-paid. |
| `marked_as_unpaid` | 1 | **null** | empty | Reversal of the above. |
| `cancelled` | 1 | set | empty | Invoice cancelled. |
| `reminder_sent` | 2 | set | 1 or 2 recipients | Dunning email. |
| `card_payment_received` | 2 | **always null** | empty | Stripe card capture. |
| `accounting_synced` | 6 | **always null** | empty | Invoice pushed to the accounting integration. Count matches the 6 invoices at `accounting_sync_status: "synced"`. |
| `payment_accounting_synced` | 1 | **null** | empty | Payment record pushed separately from the invoice. Only INV-2026-0070. |

Ordering: activities are returned **ascending by `created_at`** on all 12 invoices. That is the opposite of the list-level ordering, and it is not documented anywhere.

`emails` reflects the actual send list at the time of the event, primary plus CCs. Observed: INV-2026-0002's `sent` carries `["info@acmesupplies.com","ap@acmesupplies.com"]`, where the second address is one of that customer's `cc_emails`. INV-2026-0060's `reminder_sent` carries `["hello@brightleaf.design","finance@brightleaf.design"]`.

**`user_id` is unresolvable.** There is no user endpoint in `v1`. The three user IDs in the fixture (`...0001` creates and sends, `...0002` cancels, `...0003` marks paid, downloads and sends reminders) cannot be turned into a name or email through any API call. If your UI wants to show who did what, you need a separate directory.

**Conspicuously absent activity types:** nothing for customer-side view or open, nothing for edits or amendments, nothing for accounting-sync **failure** (even though `accounting_sync_status: "error"` exists, and INV-2026-0045 sits in that state with no failure activity), nothing for refunds or chargebacks, nothing for deletion, and nothing for recurring-schedule generation.

> **Divergence, by omission:** the Invoicing guide never mentions `activities` at all. The entire audit log is documented only as an enum list on the two operation reference pages, with no prose describing what any value means or when it is emitted. Everything in the table above beyond the bare value names is derived from observation.

#### 5.4.7 Accounting sync

| Value | Guide definition | Sandbox count |
| --- | --- | --- |
| `not_pushed` | "eligible to be pushed after being unskipped" | 3 |
| `synced` | "successfully synced to the integration" | 6 |
| `error` | "the most recent sync attempt failed. `accounting_synced_at`, when present, remains the timestamp of the last successful sync." | 1 |
| `skip` | "explicitly excluded from syncing" | 1 |
| `object_changed` | "previously synced, but changed since the last successful sync" | 1 |

Observed behavior of `accounting_synced_at` against each state:

| Invoice | `accounting_sync_status` | `accounting_synced_at` | Note |
| --- | --- | --- | --- |
| INV-2026-0070 | synced | `2026-07-18T09:00:00Z` | equals `updated_at` |
| INV-2026-0066 | synced | `2026-07-24T11:00:00Z` | `updated_at` is later (`16:00:00Z`) |
| INV-2026-0065, 0060, 0052 | not_pushed | `null` | never pushed; no `accounting_synced` activity |
| INV-2026-0050, 0040, 0002, 0001 | synced | set | consistent |
| INV-2026-0045 | **error** | **null** | permitted by "when present", but the only `error` sample gives you no last-success timestamp |
| INV-2026-0043 | object_changed | `2026-05-18T00:07:03Z` | equals both `updated_at` and the `matched` activity time, so the payment match is what invalidated the sync |
| INV-2026-0041 | skip | `null` | the cancelled invoice |

> **Divergence:** the `not_pushed` definition, "eligible to be pushed after being unskipped", describes a transition out of `skip`, not the ordinary never-yet-pushed state, and it implies a skip/unskip control that has no representation in the API. All three sandbox `not_pushed` invoices have `accounting_synced_at: null` and no `accounting_synced` activity, that is, they have simply never been pushed. Read `not_pushed` as "not currently synced", nothing more.

Product context that explains the two separate sync activity types: the help center states invoice syncing is **QuickBooks Online only**, requires the "Sync invoices and customers to QuickBooks" toggle plus a configured Default Accounts Receivable Ledger, back-fills existing invoices on enablement, and that "you'll have to manually sync the invoice payment or include invoice transactions in your automated syncs". That is why `accounting_synced` and `payment_accounting_synced` are distinct, and why only 1 of the 6 synced invoices has the payment leg synced.

**Conspicuously absent:** no field naming the integration, no external or QuickBooks object ID, no error message or code for the `error` state, no `accounting_sync_attempted_at`, and no sync state on the customer object even though the product syncs customers too.

#### 5.4.8 `GET /invoicing/invoices/{invoice_id}`

Path parameter `invoice_id`, string, required. Response is the bare `Invoice`, field-for-field identical to a list element.

```bash
curl -s "$RHO/invoicing/invoices/70000000-0000-4000-8000-000000000001" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

| Request | HTTP | Body |
| --- | --- | --- |
| unknown but well-formed UUID | 404 | `{"type":"1303","title":"invoice not found","status":404}` |
| malformed ID (`xyz`) | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: invoice_id"}` |
| a customer UUID at this path | 404 | `{"type":"1303","title":"invoice not found","status":404}` |

There is no payload advantage over the list form. Use this endpoint for refresh-by-ID, not for enrichment.

---

### 5.5 Invoicing: customers

#### 5.5.1 The customer object

Identical in list and get. Observed via `GET /invoicing/customers/60000000-0000-4000-8000-000000000008`, which is the soft-deleted fixture record:

```json
{
  "id": "60000000-0000-4000-8000-000000000008",
  "legal_name": "Deleted Co",
  "email": "gone@deletedco.example",
  "address": {
    "address1": "9 Archive Rd",
    "address2": "",
    "city": "Chicago",
    "state": "IL",
    "zip_code": "60601",
    "country": "USA"
  },
  "note": "Soft-deleted fixture customer",
  "cc_emails": [],
  "total_revenue": { "amount": 5000, "currency": "USD" },
  "last_invoice_id": "70000000-0000-4000-8000-000000000012",
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": "2026-05-01T12:00:00Z",
  "deleted_at": "2026-05-01T12:00:00Z"
}
```

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `id` | string (UUID) | yes | Stable global customer identifier. |
| `legal_name` | string | yes | No description in the reference. Always populated in sandbox. |
| `email` | string | yes | **Null on 1 of 8** ("Cedar & Co"). |
| `address` | object | yes | Always present, always fully keyed. |
| `address.address1` | string | yes | |
| `address.address2` | string | yes | **Empty string, never null**, when absent. Populated on 2 of 8. |
| `address.city` | string | yes | |
| `address.state` | string | yes | Observed: 2-letter US state codes. |
| `address.zip_code` | string | yes | Observed: 5-digit US ZIPs, leading zero preserved as a string (`"02109"`). |
| `address.country` | string | yes | Observed: all `"USA"`, that is **ISO 3166 alpha-3**, not the alpha-2 used elsewhere in fintech APIs. No standard is stated and no validation is documented. |
| `note` | string | yes | **Null on 4 of 8.** Not covered by `search`. |
| `cc_emails` | array of string | yes | Empty array when none (3 of 8), never null. |
| `total_revenue` | Money | yes | "Total amount collected across paid invoices". See 5.5.4. |
| `last_invoice_id` | string (UUID) | yes | "Identifier of the most recent invoice for this customer". **Null on 1 of 8** (a customer with no invoices). |
| `created_at` | string (date-time) | yes | The default sort key. |
| `updated_at` | string (date-time) | yes | Touched by invoice events, see 5.5.4. |
| `deleted_at` | string (date-time) | yes | "Set when the customer is deleted; null otherwise". Null on 7 of 8. |

No phone, no tax ID, no default payment terms, no default currency, no customer-level accounting sync status and no invoice count.

#### 5.5.2 `GET /invoicing/customers`

"Deleted customers are excluded unless `include_deleted` is true."

| Parameter | Type | Documented | Observed |
| --- | --- | --- | --- |
| `search` | string | "Case-insensitive substring match on `legal_name` and `email`" | Confirmed on both fields and case-insensitive: `search=acme` matches "Acme Supplies", `search=ORBITMEDIA.CO` matches the email `accounts@orbitmedia.co`. `search=Preferred`, a substring of a `note`, returns 0, confirming `note` is not searched. |
| `include_deleted` | boolean | "When true, include deleted customers in the results" | Confirmed: 7 customers by default, 8 with `include_deleted=true`. |
| `sort_by` | string | "Sort field. Defaults to `created_at` when omitted." | **`created_at` is the only accepted value.** `legal_name`, `email`, `updated_at`, `total_revenue`, `id` and `bogus` all return `400 {"type":"1317","title":"invalid sort_by parameter: \"<value>\"","status":400}`. The parameter exists but can only be set to its own default. |
| `order` | string | "Sort direction. Defaults to `desc` when omitted." | Only lowercase `asc` and `desc` accepted. `ASC`, `ascending` and `bogus` return `400 {"type":"1317","title":"invalid order parameter: \"<value>\"","status":400}`. Note that `/statements` accepts `ASC` happily. |
| `page_size` | integer | "Defaults to 20." Max not documented. | Default 20 confirmed. Bounds 1 to 100 enforced. |
| `page_token` | string | Cursor. | See "Pagination". |

Observed validation matrix, reproducible:

```bash
for v in created_at legal_name bogus; do
  printf '%s -> ' "$v"
  curl -s -o /dev/null -w '%{http_code}\n' \
    "$RHO/invoicing/customers?sort_by=$v&page_size=1" \
    -H "Authorization: Bearer $RHO_API_TOKEN"
done
# created_at -> 200
# legal_name -> 400
# bogus      -> 400

for v in asc desc ASC bogus; do
  printf '%s -> ' "$v"
  curl -s -o /dev/null -w '%{http_code}\n' \
    "$RHO/invoicing/customers?order=$v&page_size=1" \
    -H "Authorization: Bearer $RHO_API_TOKEN"
done
# asc -> 200, desc -> 200, ASC -> 400, bogus -> 400
```

#### 5.5.3 Soft-delete semantics, complete

| Aspect | Behavior | Source |
| --- | --- | --- |
| Marker | `deleted_at` timestamp on the customer, null when live | both reference pages |
| List default | deleted customers **excluded** | reference; observed 7 versus 8 |
| List opt-in | `include_deleted=true` | reference; observed |
| Get by ID | **always returns** the deleted customer "while the record exists". No flag needed, no 410, no special status | reference; observed |
| `search` plus `include_deleted` | **They compose.** Observed: `search=deleted` alone returns 0 rows; `search=deleted&include_deleted=true` returns 1, "Deleted Co". The deleted row is filtered out before or alongside the search, not instead of it. This was previously unstated in the docs and unverified | observed 2026-09-12 |
| Sort position of deleted rows | not special-cased; the deleted customer appears in its natural `created_at desc` position, oldest in the fixture | observed |
| Data retained after delete | everything: `legal_name`, `email`, `address`, `note`, `cc_emails`, `total_revenue`, `last_invoice_id` | observed |
| `updated_at` on delete | set equal to `deleted_at`, `2026-05-01T12:00:00Z` | observed |
| Effect on that customer's invoices | **none.** INV-2026-0001 is returned by the default invoice list, still `status: "paid"`, still `accounting_sync_status: "synced"`, and its `customer.id` still points at the deleted record | observed |
| Invoice soft-delete | **does not exist.** Invoices have no `deleted_at`, and `/invoicing/invoices` has no `include_deleted`; passing it is ignored | reference and observed |
| Restore or un-delete | **unstated** anywhere |
| Hard delete and retention | **unstated.** The phrase "while the record exists" implies an eventual purge with no retention period given |

Reproduce the whole model in three calls:

```bash
curl -s "$RHO/invoicing/customers?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["customers"]))'
# 7

curl -s "$RHO/invoicing/customers?page_size=100&include_deleted=true" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["customers"]))'
# 8

curl -s "$RHO/invoicing/customers/60000000-0000-4000-8000-000000000008" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["legal_name"], d["deleted_at"])'
# Deleted Co 2026-05-01T12:00:00Z
```

The practical consequence: an integration that walks `/invoicing/invoices` and joins `customer.id` against a cached list from `/invoicing/customers` will get cache misses, because live invoices can reference deleted customers. The correct pattern is `include_deleted=true` on the list, or a per-ID fetch on miss.

#### 5.5.4 `total_revenue` and `last_invoice_id`, derived

Both fields are documented in one line each and both mean something more specific than the line says. Verified exactly against all 8 sandbox customers.

**`total_revenue.amount` equals the sum of `total.amount` over that customer's invoices whose `status == "paid"`**, and nothing else:

| Customer | `total_revenue` | Sum of `paid` invoice totals | Excluded |
| --- | --- | --- | --- |
| Harbor Logistics LLC | 156750 | 156750 | none |
| Acme Supplies | 108403 | 108403 | INV-2026-0066 `pending_payout` 158000 |
| Brightleaf Design | 43400 | 43400 | INV-2026-0060 `overdue` 45000 |
| Deleted Co | 5000 | 5000 | none |
| Summit Analytics | 0 | 0 | INV-2026-0070 `pending_payout` 98000, INV-2026-0041 `cancelled` 22000 |
| Northwind Traders | 0 | 0 | INV-2026-0065 `unpaid`, INV-2026-0045 `overdue`, INV-2026-0043 `confirm_payment` 10000000 |
| Orbit Media Group | 0 | 0 | INV-2026-0052 `unpaid` 45000 |
| Cedar & Co | 0 | 0 | no invoices |

Therefore **`pending_payout` and `confirm_payment` do not count as collected**, despite the money having been captured or having arrived. The doc string "Total amount collected across paid invoices" is accurate only if you read "paid" as the literal status value, not as English. It is also gross of the 2.9 percent plus $0.30 card fee, so it is not cash received. Do not use it in a cash-basis report. Note also that `Money` carries a single `currency`, so the field cannot represent a mixed-currency customer at all, and nothing documents what happens if one exists.

**`last_invoice_id` points to the customer's invoice with the latest `created_at`**, not the latest `date`, not the latest unpaid one, and it is unaffected by status. Verified on all 8: Summit Analytics points at INV-2026-0070 rather than its cancelled INV-2026-0041; Cedar & Co, with no invoices, is `null`.

One consequence worth knowing before you build change detection: **the customer's `updated_at` tracks invoice activity**. Acme's `updated_at` (`2026-07-24T16:00:00Z`) equals INV-2026-0066's `updated_at`; Summit's equals INV-2026-0070's; Northwind's equals INV-2026-0065's `created_at`. So `updated_at` on a customer is not a reliable "customer details changed" signal.

#### 5.5.5 `GET /invoicing/customers/{customer_id}`

"Returns a single customer from Invoicing by ID, including deleted customers when they still exist (`deleted_at` is set)."

| Request | HTTP | Body |
| --- | --- | --- |
| unknown but well-formed UUID | 404 | `{"type":"1303","title":"customer not found","status":404}` |
| malformed ID (`abc`) | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: customer_id"}` |
| an invoice UUID at this path | 404 | `{"type":"1303","title":"customer not found","status":404}` |

---

### 5.6 The file endpoints and signed-URL mechanics

Three resources in `v1` carry files, and they deliver the URL three different ways.

| Resource | How the URL arrives | TTL documented | TTL observed | Sandbox bucket | Works in sandbox |
| --- | --- | --- | --- | --- | --- |
| Statements | **embedded** as `pdf_url` in both list and get | "valid for up to 15 minutes" | `X-Goog-Expires=899` | `sandbox-statements.files.rho.co` | yes |
| Transaction attachments | exchange at `GET /transactions/{transaction_id}/files/{file_id}` | "short-lived" | `X-Goog-Expires=899` | `rho-api-sandbox.files.rho.co` | yes |
| Invoice PDF | exchange at `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | "short-lived", no number given | **not observable** | unknown | **no, 404 on every `file_id`** (see 5.2) |

The two exchange endpoints return a byte-identical three-field schema:

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `file_id` | string | yes | Echoes the requested ID. |
| `file_name` | string | yes | "Original file name". Observed on transactions: `parking-receipt.pdf`, `repayment-details.csv`. Never appears at the invoice or transaction object level, only here. |
| `download_url` | string | yes | "Fresh, short-lived signed download URL". |

> **Divergence:** only statements commit to a number. The invoicing reference says "Fetch again whenever a new signed URL is needed; do not persist the URL" and gives no TTL at all. By analogy with the two observable buckets, 899 seconds is the likely value, but Rho does not commit to it for invoicing and it could not be measured because the endpoint returns 404.

#### 5.6.1 Anatomy of a signed URL

Both working buckets emit Google Cloud Storage **V4 signed URLs**, RSA-signed by the same service account.

| Component | Value |
| --- | --- |
| Host, transaction attachments | `rho-api-sandbox.files.rho.co` |
| Host, statement PDFs | `sandbox-statements.files.rho.co` |
| Path | `/{24 hex chars}.{ext}`, for example `/f0b72b6108f6ebfd9818fb0f.pdf`, `/4f7150d8341cae23c6ffa33a.pdf` |
| `X-Goog-Algorithm` | `GOOG4-RSA-SHA256` |
| `X-Goog-Credential` | `file-service@pledge-218909.iam.gserviceaccount.com/<YYYYMMDD>/auto/storage/goog4_request` |
| `X-Goog-Date` | signing instant, second granularity, for example `20260912T002403Z` |
| `X-Goog-Expires` | **`899`** on every URL observed, in both buckets |
| `X-Goog-Signature` | 512 hex characters (2048-bit RSA) |
| `X-Goog-SignedHeaders` | `host` |

Two facts an integrator can use directly:

- **The exact deadline is readable from the URL with no network call**: `X-Goog-Date + X-Goog-Expires`. Parse it and decide whether a URL is worth attempting, instead of discovering expiry from a failed download.
- **Object names carry no account, business, invoice or transaction identifier** and are not enumerable. They are also deduplicated: the same `file_id` attached to two different transactions resolves to the same object path.

#### 5.6.2 Failure modes, observed

Every row below was reproduced live on 2026-09-12 against a transaction attachment URL.

| Test | Result |
| --- | --- |
| GET the URL as issued, no `Authorization` header | `200`, `content-type: application/pdf`, 769 bytes, body begins `%PDF-1.4` |
| `HEAD` the URL | `200` |
| `Range: bytes=0-9` | `206`, 10 bytes returned |
| Same URL fetched 3 times | `200` each time. **Not single-use** |
| Last hex character of `X-Goog-Signature` altered | `403`, XML `<Code>SignatureDoesNotMatch</Code>` |
| Last character of the whole query string altered (corrupts `X-Goog-SignedHeaders=host`) | `400`, XML `<Code>MalformedSecurityHeader</Code>`, detail "Host header not signed" |
| Query string stripped, bare object path | `403`, XML `<Code>AccessDenied</Code>`. The bucket is private, there is no public read |
| `X-Goog-Expires` rewritten from `899` to `1` | `400`, XML `<Code>ExpiredToken</Code>`, detail "Request signature expired at: 2026-09-12T00:28:09+00:00", exactly `X-Goog-Date` plus 1 second |
| A URL replayed 27 minutes after signing | `400 ExpiredToken`, "Request signature expired at: 2026-09-11T23:37:21+00:00", exactly signing time plus 899 s |

**Every one of these failures is a Google Cloud Storage XML error document, not RFC 9457 problem+json.** A client that parses every non-2xx body as JSON will throw on all of them. Handle the download leg with a completely separate error path from the API leg.

> **Divergence, minor:** the Transactions guide instructs you to follow the link "straight away, **without an Authorization header**". Observed: sending `Authorization: Bearer sandbox` or `Authorization: Bearer NOPE` alongside the signed URL still returns `200` with the full 769-byte body. GCS ignores the header here because only `host` is in `X-Goog-SignedHeaders`. Follow the doc's advice anyway, since the behavior is not contractual, but a stray header in a shared HTTP client is not the cause of a download failure you are debugging.

Confirming the documented sandbox promise, a transaction CSV attachment downloads as real content:

```csv
transaction_id,account_name,counterparty_name,amount,currency
019f0143-3ea0-7000-8000-000000000003,Credit Account,Cash (Checking),1750,USD
```

That matches the Transactions guide: "Sandbox downloads contain non-empty representative fictional documents, but their contents are not guaranteed to reproduce every field of the transaction fixture." No such statement exists for invoicing.

#### 5.6.3 Expiry, and the statement signing cache

The documented TTL is "valid for up to 15 minutes". The observed `X-Goog-Expires` is 899 seconds, one second short of 15 minutes, which is consistent with a signer computing an absolute deadline and converting back to a relative TTL.

The interesting behavior is that **the two working file surfaces behave differently on refresh**.

A 20-second poll of `GET /statements/200527` and `GET /transactions/.../files/...` in lockstep, run 2026-09-12 00:28Z to 00:37Z, recording the `X-Goog-Date` returned by each. Reproduce it with:

```bash
for i in $(seq 1 28); do
  printf '%s ' "$(date -u +%H:%M:%SZ)"
  printf 'stmt=%s ' "$(curl -s "$RHO/statements/200527" -H "Authorization: Bearer $RHO_API_TOKEN" \
    | python3 -c 'import sys,json,urllib.parse as u; d=json.load(sys.stdin); print(u.parse_qs(u.urlparse(d["pdf_url"]).query)["X-Goog-Date"][0])')"
  printf 'txn=%s\n' "$(curl -s "$RHO/transactions/019f0554-0bf0-7000-8000-00000000000a/files/2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15" \
    -H "Authorization: Bearer $RHO_API_TOKEN" \
    | python3 -c 'import sys,json,urllib.parse as u; d=json.load(sys.stdin); print(u.parse_qs(u.urlparse(d["download_url"]).query)["X-Goog-Date"][0])')"
  sleep 20
done
```

Abridged output, with the two re-sign boundaries marked:

```text
00:28:45Z  stmt=00:24:03Z  txn=00:28:46Z
00:29:06Z  stmt=00:29:06Z  txn=00:29:07Z   <- statement re-signed, 303 s after the prior epoch
00:29:27Z  stmt=00:29:06Z  txn=00:29:28Z
00:30:09Z  stmt=00:29:06Z  txn=00:30:10Z
00:31:11Z  stmt=00:29:06Z  txn=00:31:11Z
00:32:33Z  stmt=00:29:06Z  txn=00:32:34Z
00:33:55Z  stmt=00:29:06Z  txn=00:33:56Z
00:34:16Z  stmt=00:34:16Z  txn=00:34:16Z   <- statement re-signed, 310 s after the prior epoch
00:35:17Z  stmt=00:34:16Z  txn=00:35:18Z
00:37:20Z  stmt=00:34:16Z  txn=00:37:20Z
```

Reading:

- **Transaction attachment URLs are minted fresh on every request.** New `X-Goog-Date`, new signature, a full 899-second window every time. The docs are accurate here.
- **Statement `pdf_url` is served from a server-side signing cache of roughly 300 seconds.** Two back-to-back calls to `GET /statements/200527` return a byte-identical URL. Four re-sign intervals have now been measured across two independent polling runs: 302 s, 313 s, 303 s and 310 s. The cache TTL is not the 899-second expiry.
- Crucially, **each URL is replaced roughly 10 minutes before it expires**, not when it dies. Epoch `00:29:06Z` was valid until `00:44:05Z` and was replaced at `00:34:16Z`, almost 10 minutes early.
- Because the cache rotates about 300 seconds into an 899-second lifetime, **a statement URL you receive always has between roughly 599 and 899 seconds of life left**. Observed minimum residual: 606 s in the earlier run, 610 s in the run above. A statement URL never arrives nearly dead, so the documented "up to 15 minutes" is accurate and conservative.

> **Divergence:** the documented remedy for a lapsed statement link, "If the link lapses, re-fetch the statement with `GET /statements/{id}` for a fresh URL", does not work by the mechanism it describes. Re-fetching does not mint a URL on demand; it returns whatever the ~300-second cache holds. A client **cannot force a re-sign**. In practice the remedy usually works, because the cache rotates about 10 minutes before expiry, so a genuinely expired URL will already have been replaced. But a tight retry loop after a `400 ExpiredToken` will keep receiving the same dead URL until the cache turns over. Back off past the cache TTL instead of retrying immediately.

**The cache key is the PDF blob, not the statement.** Observed on a single `GET /statements?page_size=100`: 33 statements resolved to only **3 distinct object paths**, one shared by the 7 treasury statements, one by the 22 credit statements, one by the 4 account statements.

```bash
curl -s "$RHO/statements?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json, urllib.parse as u
from collections import Counter, defaultdict
st = json.load(sys.stdin)["statements"]
paths, dates = Counter(), defaultdict(set)
for s in st:
    p = u.urlparse(s["pdf_url"]); q = u.parse_qs(p.query)
    paths[p.path] += 1
    dates[p.path].add(q["X-Goog-Date"][0])
for path, n in paths.items():
    print(path, n, sorted(dates[path]))
'
# /41addf56a3d9ab46a2bfedc6.pdf 7  ['20260912T003658Z']
# /e9c29858933afd7a8d42e1a7.pdf 22 ['20260912T003416Z']
# /4f7150d8341cae23c6ffa33a.pdf 4  ['20260912T003658Z']
```

Two consequences. First, because signing is per blob and each blob has its own cache epoch, **a single list response can return URLs signed at different instants with different residual lifetimes**. In the run above, one page of 33 statements carried URLs signed 162 seconds apart, so the credit statements' links had 162 fewer seconds of life than the others. All were still inside the 599 to 899 second band, but do not assume a uniform deadline across one page. Second, the sandbox backs all 33 statements with only 3 real PDFs, so per-statement PDF content is not statement-specific fixture data. Testing "does this PDF match this statement" against sandbox is not meaningful.

#### 5.6.4 Budgeting an archive job

The Statements guide's archiving workflow is:

```bash
curl -s "$RHO/statements?period_end_after=2026-05-01&period_end_before=2026-06-01&page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

followed by "download each `pdf_url` promptly" and "For a long-running archive job, download each PDF soon after you read it rather than collecting URLs up front."

The arithmetic behind that advice is never given, so here it is. A 100-item page issues up to 100 signatures that share a single window of at most 899 seconds, and in the worst case as little as ~599 seconds because of the signing cache. At one PDF every 10 seconds a full page takes 1,000 seconds and you will lose the tail. There is no bulk refresh endpoint and no per-statement file endpoint; the only recovery is a full single-statement re-fetch, which is subject to the cache described above and costs one of your ~60 requests per minute.

Practical shape for a correct archiver:

1. Page with `period_end_after` and `period_end_before` windows rather than cursor-walking the live head. The cursor is offset-based (see "Pagination"), so a statement finalized mid-iteration shifts every subsequent page.
2. Parse `X-Goog-Date` plus `X-Goog-Expires` out of each `pdf_url` on arrival and record the absolute deadline.
3. Download concurrently, but pace below the documented one request per second guidance for the API leg. The GCS download leg does not count against the Rho API rate limit, since it is a different host with no Rho authentication.
4. On a deadline you have already passed, re-fetch `GET /statements/{id}`, and if the URL comes back identical, wait out the remainder of the ~300 second cache before trying again.
5. Do not persist signed URLs anywhere. All three reference pages say so, in three different wordings.

---

### 5.7 Errors specific to these seven operations

The declared error sets in the official reference are:

| Operation | Declared responses |
| --- | --- |
| `GET /statements` | 400, 401, 403, 500, 503 |
| `GET /statements/{id}` | 400, 401, 403, 404, 500, 503 |
| `GET /invoicing/invoices` | 400, 401, 403, 500, 503 |
| `GET /invoicing/invoices/{invoice_id}` | 400, 401, 403, 404, 500, 503 |
| `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | 400, 401, 403, 404, 500, 503 |
| `GET /invoicing/customers` | 400, 401, 403, 500, 503 |
| `GET /invoicing/customers/{customer_id}` | 400, 401, 403, 404, 500, 503 |

> **Divergence:** none of the seven declares `429`, even though the Rate limits page states that limits apply "uniformly across all public Rho API endpoints" and that exceeding them returns `429 Too Many Requests` with a `Retry-After` header. Generated clients built strictly from these operation schemas will have no 429 branch.

What these endpoints actually return, all reproduced live:

| HTTP | `type` | `title` | `detail` | Trigger |
| --- | --- | --- | --- | --- |
| 401 | `"2"` | `Unauthenticated` | absent | missing `Authorization` header. Note: sandbox accepts any non-empty bearer value |
| 404 | `"1303"` | `statement not found` | absent | unknown, malformed or negative statement ID |
| 404 | `"1303"` | `invoice not found` | absent | unknown well-formed invoice UUID |
| 404 | `"1303"` | `customer not found` | absent | unknown well-formed customer UUID |
| 404 | `"1303"` | `invoice file not found` | absent | **every** invoice file fetch, including documented-correct pairings (5.2) |
| 400 | `"1317"` | `page_size must be between 1 and 100` | absent | `page_size=0` or `page_size=101` on all three list endpoints |
| 400 | `"1317"` | `page_token must be a valid cursor` | absent | garbage token, changed filters, cross-endpoint token |
| 400 | `"1317"` | `invalid sort_by parameter: "<v>"` | absent | `/invoicing/customers?sort_by=` anything but `created_at` |
| 400 | `"1317"` | `invalid order parameter: "<v>"` | absent | `/invoicing/customers?order=` anything but `asc` or `desc` |
| 400 | `"about:blank"` | `Bad Request` | `invalid parameter: <name>` | malformed path IDs (`invoice_id`, `customer_id`, `file_id`) and malformed query values (`account_id`, `period_end_after`, `date_after`) |

> **Divergence:** the schema describes `type` as "A URI reference that identifies the problem type. Example: `about:blank`". In practice these endpoints return bare numeric strings `"2"`, `"1303"` and `"1317"` for most failures. `"1303"` is shared by every not-found across the whole API, with the resource identified only by the prose `title`, so `type` is useless for programmatic discrimination. Key off HTTP status plus, reluctantly, `title`. The schema also lists `detail` on the 404 responses; **no 404 observed anywhere returns a `detail`**. Only the `about:blank` validation family carries one.

Two distinct error layers are in play: a Rho application layer that emits numeric `type` codes with no `detail`, and a request-validation layer that emits `about:blank` plus a `detail`. The documentation describes only the second.

Non-JSON error surfaces you will also hit on these paths:

| Surface | Example | Body |
| --- | --- | --- |
| Go router, route not matched | `GET /statements/200527/files/x`, `GET /invoicing/invoices/` | `404 page not found`, plain text |
| Load balancer, outside `/api/v1` | `GET /api/v2/statements` | `default backend - 404`, plain text |
| Write verb on any path here | `POST /invoicing/invoices/{id}` | `405`, **empty body**, `Allow: GET` |

Also worth knowing on these endpoints: paths are case-sensitive, a trailing slash is a 404 with no redirect, unknown query parameters are silently ignored, `Accept` is not negotiated (XML requests get JSON), and no response carries `ETag`, `Last-Modified`, `Cache-Control`, `X-Request-Id` or any `X-RateLimit-*` header, so there are no conditional requests and no visible rate-limit headroom.

Finally, the cursor. The cursor internals belong to "Pagination", but two behaviors bite specifically here:

- **The filter fingerprint is enforced, and `sort_by` is part of it on `/statements` even though `sort_by` has no effect on results.** Changing an inert parameter mid-iteration invalidates your cursor with `400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`.
- **`page_size` is not part of the fingerprint.** Observed: a token issued by `GET /statements?page_size=5` used against `GET /statements?page_size=10&page_token=...` returns `200` with 10 rows starting at offset 5. Changing page size mid-iteration is silently allowed, and since the cursor is offset-based, it is a route to skipped or duplicated rows.

---

### 5.8 Checklist for an integrator

Statements:

1. Detect credit statements with `statement_type == "credit"` or `accounts[].account_type == "credit"`, never with `account_id is None`.
2. Do not expect `repayment_date`. It is documented and never returned, and it is the only credit-terms field in the API.
3. Do not join `accounts[].account_type` to the Accounts API's `account_type`. The vocabularies differ and disagree on the same account. Join on `account_id`.
4. Treat credit `total_credits`, `total_debits` and `total_fees` as unusable; anchor on `closing_balance` and the `spending` / `repayments` / `cashback` trio, and do not assume their signs.
5. There is no `available_at` filter, so incremental "finalized since T" polling is impossible. Rescan by period window and diff IDs.
6. Statement IDs are opaque numeric strings, not UUIDs. Junk IDs return 404, not 400.

Invoicing:

7. The invoice file endpoint returns 404 on every advertised `file_id` in sandbox. Prototype the signed-URL flow against the transactions file endpoint, and verify invoice PDFs in production before shipping.
8. Reimplement the total formula in 5.4.3 if you need a subtotal or tax amount. The API exposes neither.
9. `status` has no `draft` and no `sent`. To learn whether an invoice was emailed, scan `activities` for `sent`. `status=draft` and `status=sent` return `200` with zero rows rather than an error.
10. Do not derive `overdue` from `status`; compute it from `due_date` yourself. Observed invoices sit at `unpaid` weeks past due.
11. A Rho card payment appears as `payments[].type == "external"` with `external_method == "credit_card"` and a null `transaction_id`. Detect the card rail via the `card_payment_received` activity or `status == "pending_payout"`.
12. There is no per-payment amount, so partial payments cannot be represented. If your AR flow needs them, this API cannot reconcile it.
13. There is no `customer_id` filter on invoices. Per-customer views require pulling everything and grouping client-side.
14. Fetch customers with `include_deleted=true` when building the invoice-to-customer join, or live invoices will miss their customer.
15. `total_revenue` counts only `status == "paid"` and is gross of the 2.9 percent plus $0.30 card fee. It is not cash received.
16. A customer's `updated_at` moves when its invoices move, so it is not a "customer details changed" signal.

Everything in this section:

17. Generate all response models with every field nullable. `required` in these schemas is a presence guarantee, not a non-null guarantee: `invoice.note`, `invoice.accounting_synced_at`, `payments[].external_method`, `payments[].transaction_id`, `activities[].user_id`, `customer.email`, `customer.note`, `customer.last_invoice_id`, `customer.deleted_at` and `page.next_page_token` are all marked required and all observed null.
18. Handle both absence conventions. Optional fields are **omitted keys** (`invoice.file_id`, the credit-only statement figures); "required but empty" fields are **explicit nulls**.
19. Never loop single GETs to enrich list rows. All 133 sandbox resources are deep-equal between list and single GET, and the only thing `GET /statements/{id}` adds is a possibly re-signed URL.
20. Give every `switch` on these enums a default case. The Versioning policy classifies "a new enum value" as a non-breaking change that can ship into `v1` at any time.
21. Parse `X-Goog-Date` plus `X-Goog-Expires` out of every signed URL to know its exact deadline, and never persist the URL.
22. Use a separate error path for the download leg. Signed-URL failures are GCS XML, API failures are problem+json, route failures are plain text, and 405 has an empty body.

### 5.9 Enum inventory for this section

| Enum | Values |
| --- | --- |
| `statement.statement_type` | `account`, `credit`, `treasury` |
| `statement.accounts[].account_type` | `checking`, `savings`, `credit`, `treasury` |
| `invoice.status` | `paid`, `unpaid`, `cancelled`, `overdue`, `confirm_payment`, `pending_payout` |
| `invoice.payments[].type` | `received_in_account`, `external` |
| `invoice.payments[].external_method` | `cash`, `check`, `credit_card`, `other` |
| `invoice.activities[].activity_type` | `created`, `sent`, `downloaded`, `matched`, `marked_as_paid`, `marked_as_unpaid`, `cancelled`, `reminder_sent`, `card_payment_received`, `accounting_synced`, `payment_accounting_synced` |
| `invoice.accounting_sync_status` | `not_pushed`, `synced`, `error`, `skip`, `object_changed` |
| `customers.sort_by` | `created_at` only. Enforced with a 400, not documented as a restriction |
| `customers.order` | `asc`, `desc`, lowercase only. Enforced with a 400 |
| `statements.order` | not validated. Anything lowercasing to `asc` is ascending, everything else is descending |
| `statements.sort_by` | not validated and inert, but hashed into the pagination cursor |
