# Rho API: Statements and Invoicing (complete per-endpoint spec)

Research date: 2026-09-11. Corpus: local snapshot of docs.rho.co (`docs/`, `api/`), live sandbox probes captured 2026-09-11 23:22 to 23:40 UTC (`sandbox/*.json` plus fresh probes run during this pass), rho.co marketing and help-center pages.

Sources used in full:
- `/scratchpad/rho/docs/docs_v1_statements.md`
- `/scratchpad/rho/docs/docs_v1_invoicing.md`
- `/scratchpad/rho/api/statements_liststatements.md`, `statements_getstatement.md`
- `/scratchpad/rho/api/invoicing_listinvoicinginvoices.md`, `invoicing_getinvoicinginvoice.md`, `invoicing_listinvoicingcustomers.md`, `invoicing_getinvoicingcustomer.md`, `invoicing_getinvoicinginvoicefile.md`
- `/scratchpad/rho/sandbox/statements.json`, `invoicing_invoices.json`, `invoicing_customers.json`, `accounts.json`, `transactions.json` plus headers
- Supporting: `docs/api_v1_openapi.md`, `docs/docs_v1_pagination.md`, `docs/docs_v1_auth.md`, `docs/docs_v1_accounts.md`, `docs/docs_v1_versioning.md`, `docs/docs_v1_rate-limits.md`, `docs/docs_v1_mcp.md`, `docs/docs_v1_getting-started.md`, `api/transactions_gettransactionfile.md`
- Product/help: `pages/core/product__invoicing.txt`, `pages/core/policies__invoicing-terms-and-conditions.txt`, `pages/help/help-center__invoicing__accept-card-payments-on-invoices.txt`, `pages/help/help-center__invoicing__create-an-invoice.txt`, `pages/help/help-center__accounting__syncing-invoices-to-your-accounting-software.txt`, `pages/help/help-center__banking__how-to-view-account-and-card-statements.txt`, `pages/help/help-center__general-rho-information__invoice-generator-technical-guide.txt`

Label convention: **[Rho claim]** marks an assertion only Rho makes. **[sandbox]** marks a behaviour observed live against `https://rhoapi-sandbox.rho.co/api/v1`. **[contradiction]** marks a conflict between two Rho sources or between docs and observed behaviour.

---

## 0. Environment and shared contract

| Item | Value | Source |
| --- | --- | --- |
| Production base URL | `https://rhoapi.rho.co/api/v1` | `api_v1_openapi.md` |
| Sandbox base URL | `https://rhoapi-sandbox.rho.co/api/v1` | `api_v1_openapi.md` |
| MCP surface | `/mcp/v1` (Streamable HTTP), same contract/auth/scopes/errors | `docs_v1_mcp.md` |
| MCP protocol versions | `2026-07-28`, `2025-11-25`, `2025-06-18`; older versions and JSON-RPC batches rejected | `docs_v1_mcp.md` |
| API version string on every endpoint page | `Version: 1.0.0` | all `api/*.md` |
| Security scheme name | `AccessToken` (declared `type: oauth2`, token URL `https://app.rho.co/settings/access-tokens`) | `api_v1_openapi.md` |
| Statements scope | `statements:read` | `api_v1_openapi.md` |
| Invoicing scope | `invoicing:read`, stated as required by **every** invoicing endpoint | `docs_v1_invoicing.md`, `api_v1_openapi.md` |
| Amounts | integer minor units, paired with ISO 4217 `currency` | all refs |
| Timestamps | ISO 8601 UTC | `api_v1_openapi.md` |
| Errors | RFC 9457 problem details, `application/problem+json` | `api_v1_openapi.md` |
| Rate limit | approx 60 req/min per token, approx 600 req/min per source IP; `429` with `Retry-After` | `docs_v1_rate-limits.md` |
| Token constraints | `rhobat_` prefix, max 20 active tokens per business, expiry required and capped at 1 year, auto-expiry after 45 days of inactivity, up to 100 IP allowlist entries | `docs_v1_auth.md` |
| Sandbox auth | any non-empty bearer token | `docs_v1_auth.md` |

Response headers observed on all three sandbox endpoints (2026-09-11 23:22 GMT): `via: 1.1 google`, `server: cloudflare`, `cf-cache-status: DYNAMIC`, `strict-transport-security: max-age=63072000; includeSubDomains; preload`, `x-frame-options: DENY`, `x-content-type-options: nosniff`, `referrer-policy: strict-origin-when-cross-origin`. No rate-limit headers (`X-RateLimit-*`, `Retry-After`) are emitted on successful responses. No `ETag`, no `Cache-Control` on API responses.

**[contradiction] Scope table is incomplete.** `docs_v1_auth.md` lists only three scopes (`accounts:read`, `transactions:read`, `statements:read`). `api_v1_openapi.md` lists five, adding `cards:read` and `invoicing:read`. An integrator reading the Authentication guide alone would not know `invoicing:read` exists.

**[contradiction] Getting-started is stale.** `docs_v1_getting-started.md` says "Current release is read-only and covers accounts and transactions." Statements, Cards and Invoicing all ship in the same `v1`.

**Conspicuously not stated:** no individual `api/*.md` operation page names the scope it requires. The pages carry only `Security: AccessToken`. Scope-to-endpoint mapping exists only by inference from the openapi index page.

---

# PART A. STATEMENTS

## A1. Object model

A `statement` record covers **one statement period for one statement type**. Period-level fields sit at the top level; per-account figures live in an `accounts` array.

**[Rho claim]** "Account and treasury statements may span multiple checking/savings accounts; credit statements carry a single entry." (`docs_v1_statements.md`). Not reproducible in sandbox, see A7.

## A2. `GET /statements` (List statements)

Operation: `liststatements`. Description in ref: returns statements "for the authenticated business, newest close date first. Spans all statement types and all accounts in one aggregated surface."

### Query parameters

| Parameter | Type | Documented meaning | Observed behaviour [sandbox] |
| --- | --- | --- | --- |
| `account_id` | array | "Return complete statements that include at least one requested account. Multiple values use OR semantics." | Confirmed. `account_id=...0006&account_id=...0013` returned 4 statements (3 for 0006, 1 for 0013). Repeated-key array style. Malformed value returns `400` `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}`. An account with no statements returns an empty array, not 404. |
| `statement_type` | array | "Filter by statement type" (enum values not restated on the parameter) | Multi-value OR confirmed (`statement_type=account&statement_type=treasury`). **Unvalidated**: `statement_type=bogus` returns `200` with `"statements":[]`, not `400`. |
| `period_end_after` | string (date) | "Earliest statement close date, **inclusive**" | Confirmed inclusive: `period_end_after=2026-05-31` returns the 2026-05-31 statement. |
| `period_end_before` | string (date) | "Latest statement close date, **exclusive**" | Confirmed exclusive: `period_end_before=2026-05-31` excludes the 2026-05-31 statement (0 results); `period_end_before=2026-06-01` includes it. |
| `period_start_after` | string (date) | "Earliest statement open date, inclusive" | Confirmed. |
| `period_start_before` | string (date) | "Latest statement open date, exclusive" | Confirmed: `period_start_after=2026-05-01&period_start_before=2026-05-02` returns the 2026-05-01 statement. |
| `sort_by` | string | "Sort field". **No enum, no default documented.** | **Inert.** Every value tried (`period_end`, `period_start`, `available_at`, `id`, `statement_type`, `created_at`, `bogus`) returns identical ordering and no error. It is, however, hashed into the pagination cursor fingerprint, so changing it mid-iteration invalidates the cursor for nothing. |
| `order` | string | "Sort direction". **No enum, no default documented.** | Effective values: anything that lowercases to `asc` yields ascending (`asc`, `ASC` both work); every other value including `bogus` and omission yields descending. No `400` for invalid input. |
| `page_size` | integer | "Number of statements per page; max 100". **Default not documented.** | Default **20** (bare `GET /statements` returned 20 of 33). Bounds enforced 1..100: `page_size=0` and `page_size=101` both return `400` `{"type":"1317","title":"page_size must be between 1 and 100","status":400}`. |
| `page_token` | string | "Opaque cursor returned as next_page_token in the previous response" | See A8. |

Date parameters accept `YYYY-MM-DD`. A non-ISO value (`05/01/2026`) returns `400` `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: period_end_after"}`.

Unknown query parameters (`?foo=bar`) are silently ignored, `200`.

**Conspicuously absent from the filter set:** no `available_at_after`/`available_at_before` (so you cannot poll "statements finalized since T", which is exactly the incremental-archive use case the guide describes), no `statement_id` batch fetch, no `currency` filter, no `created_at`/`updated_at`, and no way to project only the requested account's figures out of a consolidated statement (the guide explicitly says filtering "does not remove those entries or alter the PDF").

### Response 200 body

```
{ "statements": [ Statement ], "page": { "next_page_token": string|null } }
```

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `statements` | array | yes | Array key matches the resource, per `docs_v1_pagination.md`. |
| `statements[].id` | string | yes | "Global statement identifier". [sandbox] a **numeric string** such as `"572981"`, not a UUID. Two disjoint id ranges in the fixture: deposit/treasury statements `428772`-`572981`, credit statements `152980`-`200527`. Treat as opaque per `docs_v1_versioning.md`. |
| `statements[].period_start` | string (date) | yes | "First day of the statement period (inclusive)". |
| `statements[].period_end` | string (date) | yes | "Close date of the statement period (inclusive)". |
| `statements[].available_at` | string (date-time) | yes | "Timestamp the finalized statement became available". |
| `statements[].pdf_url` | string | no | Short-lived signed download URL, "valid for up to 15 minutes", or `null` "when the document cannot be linked". See A6. |
| `statements[].statement_type` | string | **no** (not marked required) | Enum: `account`, `credit`, `treasury`. Note the type is *not* required in the schema even though every sandbox record carries it. |
| `statements[].accounts` | array | yes | Per-account figures. |
| `page.next_page_token` | string | yes | "null on the last page". Marked required with a nullable value. |

### `accounts[]` entry

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `account_id` | string | no | "Account these figures belong to. Null for credit statements, which are not tied to a deposit account." **[contradiction]**, see A7. |
| `account_type` | string | yes | Enum: `checking`, `savings`, `credit`, `treasury`. |
| `opening_balance` | Money | yes | "Balance as of the start of period_start". |
| `closing_balance` | Money | yes | "Balance as of the close date (period_end), the reconciliation anchor". |
| `total_credits` | Money | yes | "Sum of credits posted in the period". |
| `total_debits` | Money | yes | "Sum of debits posted in the period". |
| `total_fees` | Money | yes | "Fees charged in the period". |
| `repayment_date` | string (date) | no | Credit only; "date repayment is/was due for the period". **Never emitted in sandbox**, see A7. |
| `spending` | Money | no | Credit only; "total card spend in the period". |
| `repayments` | Money | no | Credit only; "repayments applied in the period". |
| `cashback` | Money | no | Credit only; "cashback earned in the period". |

`Money` is `{ "amount": integer (minor units), "currency": string (ISO 4217) }`. Every figure in the statements object is a Money object, including the totals; there is no scalar amount anywhere.

Credit-only fields are **omitted entirely** (key absent) on non-credit entries, not set to `null`. Verified: in the 20-record default page, `spending`/`repayments`/`cashback` keys appear on exactly the 12 credit entries.

## A3. `GET /statements/{id}` (Get statement)

Operation: `getstatement`. Path parameter `id` (string, required, no format stated).

Response 200 is the bare `Statement` object with the identical field set as a list element (no wrapper, no `page`). Verified against `GET /statements/572981` and `GET /statements/200527`.

Adds `404` to the error set. [sandbox] `GET /statements/999999999` returns `404` `{"type":"1303","title":"statement not found","status":404}`.

Documented purpose beyond retrieval: it is the **refresh mechanism for an expired `pdf_url`**. `docs_v1_statements.md`: "If the link lapses, re-fetch the statement with `GET /statements/{id}` for a fresh URL."

## A4. Error responses

List declares `400, 401, 403, 500, 503`. Get declares `400, 401, 403, 404, 500, 503`. Neither declares `429`, despite `docs_v1_rate-limits.md` promising `429 Too Many Requests` on "all public Rho API endpoints". **[contradiction]** in coverage.

All problem bodies are documented as:

| Field | Type | Req | Documented |
| --- | --- | --- | --- |
| `type` | string | yes | "A URI reference that identifies the problem type." Example: `about:blank` |
| `title` | string | yes | "A short, human-readable summary of the problem type." |
| `status` | integer | yes | "The HTTP status code." |
| `detail` | string | no | "A human-readable explanation specific to this occurrence." |

**[contradiction] `type` is frequently not a URI.** Observed sandbox values: `"2"`, `"1303"`, `"1317"`, and `"about:blank"`. See section D2 for the full observed code catalogue.

## A5. Documented workflows

Archiving month-end PDFs (`docs_v1_statements.md`), verbatim call:

```
curl 'https://rhoapi.rho.co/api/v1/statements?period_end_after=2026-05-01&period_end_before=2026-06-01&page_size=100' \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

Guidance: follow the cursor until `next_page_token` is `null`, "then download each `pdf_url` promptly"; "For a long-running archive job, download each PDF soon after you read it rather than collecting URLs up front."

Reconciling balances: "read the `closing_balance` of the relevant `accounts` entry as the anchor for that account's period"; credit statements expose `spending`, `repayments`, `cashback` "to reconcile the card line".

## A6. File and signed-URL semantics (statements)

Statements are the **only** resource in the v1 API that embeds a signed URL directly in a list/get payload. Transactions and Invoicing both refuse to: `docs_v1_transactions.md` says "Transaction responses contain stable attachment metadata but never signed URLs", and invoicing exchanges a `file_id` at a separate endpoint.

| Property | Value | Source |
| --- | --- | --- |
| Documented TTL | "valid for up to 15 minutes" | `docs_v1_statements.md`, both statements refs |
| Observed TTL | `X-Goog-Expires=899` seconds (14 min 59 s) on 20/20 sandbox URLs | [sandbox] |
| Storage | Google Cloud Storage V4 signed URL, `X-Goog-Algorithm=GOOG4-RSA-SHA256` | [sandbox] |
| Sandbox host | `sandbox-statements.files.rho.co` (statements) vs `rho-api-sandbox.files.rho.co` (transaction attachments): **separate buckets per resource** | [sandbox] |
| Signing identity | `file-service@pledge-218909.iam.gserviceaccount.com` (GCP project `pledge-218909`; "Pledge" is Rho's legacy internal project name) | [sandbox], infra leak in the URL |
| Signed headers | `X-Goog-SignedHeaders=host` only, so **no Authorization header may be sent**, and any tampering with the query string invalidates the request | [sandbox] |
| Object naming | 24 hex chars + `.pdf`, e.g. `41addf56a3d9ab46a2bfedc6.pdf`; the object name is stable across re-signings, only `X-Goog-Date`/`X-Goog-Signature` rotate | [sandbox] |
| Verified fetch | `HEAD` with no auth header returns `HTTP/2 200`, `content-type: application/pdf`, `content-length: 37465`, `last-modified: Fri, 31 Jul 2026 12:56:42 GMT`, `cache-control: private, max-age=0` | [sandbox] |
| Failure mode on a tampered URL | GCS XML error, **not** problem+json: `<Error><Code>MalformedSecurityHeader</Code>...<Details>Your request has a malformed header. Host header not signed.</Details>` | [sandbox] |

Practical consequence not spelled out in the docs: a 100-item page issues 100 signatures with a shared 899-second budget, so a serial archive job at even 1 PDF per 10 seconds will lose the tail of the page. The doc hints at it ("download each PDF soon after you read it") but never gives the arithmetic or a bulk-refresh endpoint. There is **no** `GET /statements/{id}/files/{file_id}` analogue for statements; the only refresh path is a full single-statement re-fetch.

`pdf_url` is documented as nullable "when the document cannot be linked". **No sandbox record exercises this**: 0 of 33 statements had a null `pdf_url`. The condition that produces `null` is never stated.

## A7. Sandbox cross-check: statements

Total fixture: **33 statements**, `period_start` range 2024-07-01 to 2026-05-01, `period_end` range 2024-07-31 to 2026-05-31. All `currency: "USD"`. Type mix: 22 `credit`, 7 `treasury`, 4 `account`.

| id | type | period | available_at | acct_type | account_id (last 4) | open | close | credits | debits | fees |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 572981 | treasury | 2026-05-01..05-31 | 2026-06-05T21:16:51Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 539240 | treasury | 2026-04-01..04-30 | 2026-05-07T21:01:51Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 200527 | credit | 2026-03-13..04-12 | 2026-04-13T04:01:36Z | credit | 0008 | 5453868 | 12315685 | 0 | 0 | 0 |
| 514051 | treasury | 2026-03-01..03-31 | 2026-04-07T21:04:45Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 186996 | credit | 2026-02-13..03-12 | 2026-03-13T04:00:31Z | credit | 0008 | 7550175 | 5453868 | 0 | 0 | 0 |
| 490851 | treasury | 2026-02-01..02-28 | 2026-03-06T22:05:55Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 179033 | credit | 2026-01-13..02-12 | 2026-02-13T05:00:37Z | credit | 0008 | 5384647 | 7550175 | 0 | 0 | 0 |
| 475381 | treasury | 2026-01-01..01-31 | 2026-02-06T22:00:58Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 174810 | credit | 2025-12-13..2026-01-12 | 2026-01-13T05:00:35Z | credit | 0008 | 127480 | 5384647 | 0 | 0 | 0 |
| 469372 | treasury | 2025-12-01..12-31 | 2026-01-08T22:00:30Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 172111 | credit | 2025-11-13..12-12 | 2025-12-13T05:00:15Z | credit | 0008 | 109322 | 127480 | 0 | 0 | 0 |
| 462701 | treasury | 2025-11-01..11-30 | 2025-12-05T22:00:32Z | treasury | 0004 | 0 | 0 | 0 | 0 | 0 |
| 169823 | credit | 2025-10-13..11-12 | 2025-11-13T05:00:15Z | credit | 0008 | 90522 | 109322 | 0 | 0 | 0 |
| 167766 | credit | 2025-09-13..10-12 | 2025-10-13T04:00:12Z | credit | 0008 | 39810 | 90522 | 0 | 0 | 0 |
| 165954 | credit | 2025-08-13..09-12 | 2025-09-13T04:00:25Z | credit | 0008 | 24410 | 39810 | 0 | 0 | 0 |
| 164322 | credit | 2025-07-13..08-12 | 2025-08-13T04:00:14Z | credit | 0008 | 18910 | 24410 | 0 | 0 | 0 |
| 163022 | credit | 2025-06-13..07-12 | 2025-07-13T04:00:14Z | credit | 0008 | 1700 | 18910 | 0 | 0 | 0 |
| 161929 | credit | 2025-05-13..06-12 | 2025-06-13T04:00:15Z | credit | 0008 | 0 | 1700 | 0 | 0 | 0 |
| 161396 | credit | 2025-05-01..05-31 | 2025-06-01T04:02:10Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 439951 | account | 2025-05-01..05-31 | 2025-06-02T00:31:23Z | savings | 0013 | 0 | 0 | 0 | 0 | 0 |
| 439950 | account | 2025-05-01..05-31 | 2025-06-02T00:31:23Z | checking | 0006 | 946209 | 972409 | 26200 | 0 | 0 |
| 160431 | credit | 2025-04-01..04-30 | 2025-05-01T04:02:24Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 159417 | credit | 2025-03-01..03-31 | 2025-04-01T04:02:14Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 158472 | credit | 2025-02-01..02-28 | 2025-03-01T05:02:13Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 157603 | credit | 2025-01-01..01-31 | 2025-02-01T05:02:14Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 156744 | credit | 2024-12-01..12-31 | 2025-01-01T05:02:13Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 433488 | account | 2024-12-01..12-31 | 2025-01-02T00:25:31Z | checking | 0006 | 991900 | 985900 | 0 | 6000 | 0 |
| 155915 | credit | 2024-11-01..11-30 | 2024-12-01T05:02:04Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 155137 | credit | 2024-10-01..10-31 | 2024-11-01T04:02:07Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 154411 | credit | 2024-09-01..09-30 | 2024-10-01T04:02:06Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 153670 | credit | 2024-08-01..08-31 | 2024-09-01T04:02:11Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 152980 | credit | 2024-07-01..07-31 | 2024-08-01T04:02:00Z | credit | 0007 | 0 | 0 | 0 | 0 | 0 |
| 428772 | account | 2024-07-01..07-31 | 2024-08-02T00:20:53Z | checking | 0006 | 0 | 0 | 0 | 0 | 0 |

Credit-only figures for the 12 records on the default page:

| id | period_end | spending | repayments | cashback | repayment_date |
| --- | --- | --- | --- | --- | --- |
| 200527 | 2026-04-12 | 6931038 | -69221 | 103965 | key absent |
| 186996 | 2026-03-12 | 69331 | -2165638 | 1039 | key absent |
| 179033 | 2026-02-12 | 2165528 | 0 | 32482 | key absent |
| 174810 | 2026-01-12 | 5257167 | 0 | 78857 | key absent |
| 172111 | 2025-12-12 | 18158 | 0 | 272 | key absent |
| 169823 | 2025-11-12 | 18800 | 0 | 282 | key absent |
| 167766 | 2025-10-12 | 50712 | 0 | 760 | key absent |
| 165954 | 2025-09-12 | 15400 | 0 | 231 | key absent |
| 164322 | 2025-08-12 | 5500 | 0 | 82 | key absent |
| 163022 | 2025-07-12 | 17210 | 0 | 258 | key absent |
| 161929 | 2025-06-12 | 1700 | 0 | 25 | key absent |
| 161396 | 2025-05-31 | -26200 | 26200 | -327 | key absent |

### Discrepancies found (statements)

1. **[contradiction] `account_id` is never null on credit statements.** Both refs and the guide state `account_id` is "Null for credit statements, which are not tied to a deposit account." All 22 sandbox credit statements carry a non-null `account_id` (`30000000-0000-4000-8000-000000000007` or `...0008`), and those IDs resolve in `GET /accounts` as `account_type: "credit"` accounts named "Credit Account". Worse, `GET /statements?account_id=<credit account id>` **works** and returns 11 credit statements, which the documented model says should be impossible. An integrator that codes `if account_type == "credit": account_id is None` will be wrong on every record.

2. **[contradiction] `repayment_date` is never emitted.** The field is documented on both statements refs as the credit repayment due date, and the guide lists it as a per-account figure. Across all 33 sandbox statements the key is **absent** from every `accounts[]` entry, including via `GET /statements/{id}`. There is no way to learn a credit statement's repayment due date from the sandbox.

3. **[contradiction] Consolidated multi-account statements do not exist in the fixture.** The guide devotes a whole section to the fact that "a matched statement's `accounts` array and PDF may include additional accounts" and that account/treasury statements "may span multiple checking/savings accounts". Every one of the 33 sandbox statements has exactly **one** entry in `accounts`. Stronger evidence against consolidation: statements `439950` (checking `...0006`) and `439951` (savings `...0013`) cover the **same period** 2025-05-01..2025-05-31, have the **same** `available_at` (`2025-06-02T00:31:23Z`) and consecutive ids. That is one statement per account, not one consolidated statement. The entire "Filtering by account" caveat is unverifiable and possibly obsolete.

4. **[contradiction] `account_type` on a statement disagrees with the same account's type in `GET /accounts`.** Statement `572981` reports `account_type: "treasury"` for account `30000000-0000-4000-8000-000000000004`. `GET /accounts` reports that same account as `account_type: "checking"`, `account_name: "Treasury Checking"`. The two enums are also disjoint in both directions:
   - Statements enum: `checking`, `savings`, `credit`, `treasury`
   - Accounts enum (`accounts_listaccounts.md`): `checking`, `credit`, `investment`, `savings`, `rewards`
   - `treasury` exists only in statements; `investment` and `rewards` exist only in accounts. `docs_v1_accounts.md` describes `investment` as "Treasury sleeves invested in money-market funds", so the statements `treasury` value is a third, statement-only vocabulary. Joining on `account_type` across the two APIs is unsafe.

5. **Credit statements report `total_credits = total_debits = total_fees = 0` on all 22 records**, even where `spending` is 6,931,038 and `repayments` is -69,221. The three "required" totals are therefore useless for credit reconciliation, and the guide's advice to use `closing_balance` plus the credit trio is the only workable path. Not documented.

6. **Sign conventions are undocumented and inconsistent.** `repayments` is negative on two records (`-69221`, `-2165638`) and positive on one (`26200`, statement `161396`). `spending` is negative on `161396` (`-26200`) and `cashback` is negative there too (`-327`). No ref states whether these are signed or absolute, nor what a negative means.

7. **Credit statement cycles differ per credit account, silently.** Account `...0007` bills on calendar months (2024-07-01..07-31 through 2025-05-01..05-31). Account `...0008` bills on a 13th-to-12th cycle (2025-05-13..06-12 onward). Both are `statement_type: "credit"`. Nothing in the API exposes the cycle or the terms; you have to infer it from `period_start`/`period_end`.

8. **`available_at` lag varies by type and is not documented in the API.** [sandbox] observed lags: `account` statements available on the 2nd of the following month at ~00:20-00:31 UTC; `credit` statements the day after `period_end` at ~04:00-05:02 UTC; `treasury` statements between the 5th and the 8th at ~21:00-22:06 UTC. The help-center page `help-center/banking/how-to-view-account-and-card-statements` gives the product-side rules: checking on "the second calendar day of every month"; savings "by the end of the fifth business day of each month (this can be the sixth or seventh of the month, depending on weekends or holidays)"; card accounts with Daily Terms "on the fifth of every month"; card accounts with Monthly Terms "one business day following the statement repayment date". **[contradiction]** the savings statement `439951` was available `2025-06-02T00:31:23Z`, i.e. the 2nd, not the fifth business day.

9. **Statement ids are numeric strings in two separate ranges**, strongly suggesting two backing systems (deposit/treasury ledger vs card ledger) stitched into "one aggregated surface". `docs_v1_versioning.md` already warns "Treat IDs as opaque strings"; this is the reason.

10. **Cross-ledger consistency check that works:** account statement `439950` (checking `...0006`, May 2025) shows `total_credits = 26200`, and credit statement `161396` (credit `...0007`, same month) shows `repayments = 26200` / `spending = -26200`. The fixture models a card repayment, though it lands as a *credit* on the checking account, which is the wrong direction for a repayment leaving the operating account. Fixture artifact, but it means any sample reconciliation built on the sandbox will not balance.

---

# PART B. INVOICING

## B1. Object model

Two resources plus one file exchange:

- **Customer**: "the businesses you bill". IDs are UUIDs. Soft-deletable.
- **Invoice**: "issued documents". IDs are UUIDs. References exactly one customer by id.
- **Invoice file**: at most one PDF per invoice, addressed by `file_id`.

`docs_v1_invoicing.md`: "A customer ID and its `last_invoice_id` are UUIDs." Confirmed [sandbox]: customers `60000000-0000-4000-8000-00000000000X`, invoices `70000000-0000-4000-8000-0000000000XX`, files `50000000-0000-4000-8000-000000000XXX`, users `40000000-0000-4000-8000-00000000000X`. Note that invoice ids are UUIDs while **statement ids are not**, inside the same v1 surface.

"All amounts are integer minor units in the accompanying currency. For USD, `124500` represents $1,245.00." (`docs_v1_invoicing.md`)

## B2. `GET /invoicing/invoices` (List invoices)

Operation: `listinvoicinginvoices`. Ref: "Results are ordered by creation time, newest first. **Ordering is not user-configurable**; keep filters unchanged while paginating."

### Query parameters

| Parameter | Type | Documented | Observed [sandbox] |
| --- | --- | --- | --- |
| `status` | array | "Filter by one or more invoice statuses" | Multi-value OR confirmed (`status=paid&status=overdue` returned 6). **Unvalidated**: `status=draft`, `status=sent`, `status=bogus` all return `200` with `[]`. |
| `due_date_after` | string (date) | "Earliest invoice due date to include, **inclusive**" | Confirmed inclusive. |
| `due_date_before` | string (date) | "Latest invoice due date to include, **inclusive**" | Confirmed inclusive: `due_date_after=2026-07-31&due_date_before=2026-07-31` returns the invoice due exactly 2026-07-31. |
| `date_after` | string (date) | "Earliest invoice issue date to include, inclusive" | Confirmed. |
| `date_before` | string (date) | "Latest invoice issue date to include, **inclusive**" | Confirmed: `date_after=2026-07-01&date_before=2026-07-01` returns both invoices issued 2026-07-01. |
| `page_size` | integer | "Defaults to 20." **Max not documented.** | Default 20 confirmed. Bounds 1..100 enforced with `{"type":"1317","title":"page_size must be between 1 and 100","status":400}`. |
| `page_token` | string | "Omit it for the first page, and keep all filters unchanged" | See D1. |

**Asymmetry worth flagging:** statements use `*_before` = **exclusive**, invoicing uses `*_before` = **inclusive**. Same API version, same date-range idiom, opposite boundary semantics. Both are documented correctly on their own pages and both were verified live, so this is a deliberate inconsistency rather than a doc bug, but it is a footgun for any shared date-range helper.

`sort_by` and `order` are **not documented parameters** on this endpoint. [sandbox] they are accepted and ignored (`sort_by=date`, `order=asc` change nothing), consistent with "Ordering is not user-configurable".

**Conspicuously absent filters:** no `customer_id` filter. There is no supported way to list one customer's invoices; `?customer_id=...` is silently ignored and returns all 12. The only customer-to-invoice link the API gives you is `customer.last_invoice_id` (a single most-recent pointer). Also missing: `invoice_number` lookup, free-text `search`, `created_at`/`updated_at` range, `accounting_sync_status` filter (so you cannot ask "which invoices failed to sync"), and any `include_deleted` for invoices. Invoices belonging to a soft-deleted customer are returned normally (`INV-2026-0001` for the deleted customer is in the default list).

### Response 200 body

```
{ "invoices": [ Invoice ], "page": { "next_page_token": string|null } }
```

### Invoice object (identical in list and get)

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `id` | string (UUID) | yes | "Stable invoice identifier". |
| `invoice_number` | string | yes | "Human-readable invoice number". [sandbox] `INV-2026-0001` .. `INV-2026-0070`. Not monotonic with `id` or `created_at` ordering. |
| `total` | Money | yes | "Invoice total in minor units". Tax-inclusive and discount-applied, see B6. |
| `tax_rate` | number | yes | "Invoice-level tax percentage". [sandbox] `0`, `6.25`, `8.5`, `10`. Percent, not basis points, and fractional values occur. |
| `discount_rate` | number | yes | "Invoice-level discount percentage". [sandbox] `0` on 11, `5` on one. |
| `status` | string | yes | Enum, 6 values, see B5. |
| `note` | string | yes | "Invoice note shown to the customer". Marked required but **nullable**: `null` on 3 of 12. |
| `due_date` | string (date) | yes | "Invoice due date; **null when not set**". Never null in sandbox (12/12 set). |
| `date` | string (date) | yes | "Invoice issue date". |
| `customer` | object | yes | Contains **only** `customer.id` (string, required, "Customer identifier"). No embedded name or email; a second call to `/invoicing/customers/{id}` is mandatory to render an invoice. |
| `line_items` | array | yes | See below. |
| `payments` | array | yes | See B7. May be empty (5 of 12 have none). |
| `activities` | array | yes | See B8. Never empty (always at least `created`). |
| `file_id` | string (UUID) | **no** | "Identifier of the attached invoice PDF when present." Key is **omitted entirely** when absent (3 of 12), never `null`. |
| `accounting_sync_status` | string | yes | Enum, 5 values, see B9. |
| `accounting_synced_at` | string (date-time) | yes | "Last successful accounting sync timestamp when present". Marked required but nullable: `null` on 5 of 12. |
| `created_at` | string (date-time) | yes | No description given in the ref. The list sort key. |
| `updated_at` | string (date-time) | yes | No description given in the ref. |

**Conspicuously absent from the invoice object:** no currency at the invoice level (only inside each Money), no subtotal, no tax amount, no discount amount, no amount-paid / amount-due / balance, no payment terms string (the UI collects "Net 30 / Due on receipt" per `help-center/invoicing/create-an-invoice`), no recurrence/schedule field despite the UI offering "Schedule this invoice to repeat", no public payment-portal URL, no `sent_at`, no customer-facing invoice title, no shipping, no attachments other than the single generated PDF, and no `deleted_at` (invoices appear to be non-deletable or hard-deletable, unstated).

### `line_items[]` entry

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | "Line item name". |
| `unit_price` | Money | yes | "Unit price before line-level discount and tax". |
| `quantity` | number | yes | "Quantity in public units". **Fractional allowed**: [sandbox] `2.5`. |
| `discount_rate` | number | yes | "Line-level discount percentage". |
| `tax_rate` | number | yes | "**When null, the invoice-level `tax_rate` applies.**" Marked required but nullable, and null is the common case ([sandbox] 10 of 16 lines). |
| `total` | Money | yes | "Line total **after discount, before tax**". |

No line `id`, no description/memo separate from `name`, no unit-of-measure, no per-line accounting category or GL code, no ordering index.

## B3. `GET /invoicing/invoices/{invoice_id}` (Get invoice)

Operation: `getinvoicinginvoice`. Path parameter `invoice_id` (string, required, "Stable global invoice identifier").

Response 200 is the bare Invoice object, field-for-field identical to a list element. Errors add `404`. [sandbox]:
- unknown but well-formed UUID: `404` `{"type":"1303","title":"invoice not found","status":404}`
- malformed id (`xyz`): `400` `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: invoice_id"}`

There is no documented difference between list and get payloads, so **the list endpoint already returns everything**, including the full activity log and every payment. A 100-invoice page therefore carries 100 embedded activity arrays. No `expand`/`fields` parameter exists to trim it.

## B4. `GET /invoicing/invoices/{invoice_id}/files/{file_id}` (Get invoice file)

Operation: `getinvoicinginvoicefile`.

| Path parameter | Type | Req | Notes |
| --- | --- | --- | --- |
| `invoice_id` | string | yes | "Stable global invoice identifier." |
| `file_id` | string | yes | "Identifier from `invoice.file_id`" |

Ref language: "Returns file metadata and a fresh, short-lived signed download URL for the file attached to the invoice. `file_id` must match `invoice.file_id` from list or get when that field is set. **Fetch again whenever a new signed URL is needed; do not persist the URL.**"

### Response 200

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `file_id` | string | yes | "Stable attached invoice PDF identifier" |
| `file_name` | string | yes | "Original file name" |
| `download_url` | string | yes | "Fresh, short-lived signed download URL" |

Error set: `400, 401, 403, 404, 500, 503`. Shape is byte-identical to `GET /transactions/{transaction_id}/files/{file_id}` (`transactions_gettransactionfile.md`), which returns the same three fields.

**No TTL is stated anywhere for the invoicing download URL.** Statements commit to "up to 15 minutes"; transactions and invoicing say only "short-lived". By analogy with the observed transaction attachment URL (`X-Goog-Expires=899`), 899 seconds is the likely value, but Rho does not commit to it for invoicing.

### [contradiction] The sandbox invoice file endpoint is broken

Tested every advertised `file_id` on every invoice that has one (9 of 12). **All 9 return `404`**:

```
GET /invoicing/invoices/70000000-0000-4000-8000-000000000010/files/50000000-0000-4000-8000-000000000027
-> 404 {"type":"1303","title":"invoice file not found","status":404}
```

| Invoice | file_id (last 4) | Result |
| --- | --- | --- |
| INV-2026-0070 | 0027 | 404 invoice file not found |
| INV-2026-0066 | 0021 | 404 |
| INV-2026-0060 | 0022 | 404 |
| INV-2026-0052 | 0028 | 404 |
| INV-2026-0050 | 0026 | 404 |
| INV-2026-0045 | 0024 | 404 |
| INV-2026-0043 | 0025 | 404 |
| INV-2026-0040 | 0023 | 404 |
| INV-2026-0002 | 0020 | 404 |
| INV-2026-0065, 0041, 0001 | (key omitted) | n/a |

Control: the equivalent transactions endpoint **does** work in the same sandbox, returning `file_name: "parking-receipt.pdf"` and a live GCS URL on `rho-api-sandbox.files.rho.co` with `X-Goog-Expires=899`. So this is specific to invoicing, not a sandbox-wide gap. The invoicing file fixture is unreachable: the invoice objects advertise `file_id` values that the file endpoint does not recognise. Any integrator following the documented flow against sandbox will conclude the endpoint is unusable. Also note `docs_v1_transactions.md` explicitly promises "Sandbox downloads contain non-empty representative fictional documents"; no equivalent promise or disclaimer appears for invoicing.

Passing a valid file_id belonging to a *different* invoice also returns `404 invoice file not found` (rather than 403), so the endpoint is at least scoped by invoice. Requesting a file on an invoice with no `file_id` likewise returns `404`.

## B5. Invoice lifecycle and the complete status enum

`status`, described as "Lifecycle status of an invoice in Invoicing". Enum, exactly 6 values, in the order the ref lists them:

| Value | Meaning (docs + help center) | [sandbox] count | Example |
| --- | --- | --- | --- |
| `paid` | Payment complete. For card payments, help center: "Once the payout is initiated, the invoice status changes to Paid." | 4 | INV-2026-0050, 0040, 0002, 0001 |
| `unpaid` | Issued, not yet paid. | 2 | INV-2026-0065, 0052 |
| `cancelled` | Voided by the business. | 1 | INV-2026-0041 |
| `overdue` | Past due and unpaid. | 2 | INV-2026-0060, 0045 |
| `confirm_payment` | Funds arrived in the Rho account and were matched, awaiting confirmation/allocation by the business. | 1 | INV-2026-0043 |
| `pending_payout` | Card payment captured by Stripe, payout to the Rho checking account not yet initiated. Help center: "The invoice is marked Pending payout while Stripe prepares the deposit." | 2 | INV-2026-0070, 0066 |

**The enum has no `draft` and no `sent` value.** `status=draft` and `status=sent` are accepted and return zero rows. The `sent` concept exists only as an *activity*, not a status, so an API consumer cannot distinguish an invoice that has been created but never emailed from one that was emailed, except by scanning `activities` for an entry with `activity_type == "sent"`. Rho's own help copy for creating an invoice ends at "Click Create Invoice. You'll see a confirmation once your invoice is successfully created and **ready to send**", which implies a pre-send state that the API does not model.

### Reconstructed lifecycle

```
created  ->  (unpaid)  ->  sent  ->  unpaid  ->  overdue        [due date passes, unpaid]
                                  \
                                   ->  matched  -> confirm_payment  -> marked_as_paid -> paid    [bank rail: ACH / wire / check]
                                   ->  card_payment_received -> pending_payout -> paid           [card rail: Stripe]
                                   ->  marked_as_paid -> paid                                    [manual, external payment]
                                   ->  cancelled -> cancelled
```

Evidence for each edge from sandbox activity logs:
- Bank rail: INV-2026-0043 has activity `matched` at `2026-05-18T00:07:03Z`, a `received_in_account` payment with `transaction_id: 019e3868-5858-7000-8000-00000000001a`, and status `confirm_payment`. INV-2026-0002 has `matched` `2026-06-21T19:37:23Z` then `marked_as_paid` `2026-06-21T19:38:00Z` (37 seconds later) and status `paid`. So `matched` then human confirmation then `paid`; `confirm_payment` is the state between them.
- Card rail: INV-2026-0070 has `card_payment_received` `2026-07-18T08:00:00Z`, status `pending_payout`.
- `marked_as_unpaid` reverses `marked_as_paid`: INV-2026-0066 shows `marked_as_paid` at `2026-07-20T09:00:00Z` then `marked_as_unpaid` at `2026-07-20T09:05:00Z` (5 minutes later, `user_id: null`).
- Cancellation is terminal in the fixture: INV-2026-0041 has only `created` then `cancelled`, no `sent`.

**Status is stored, not derived.** INV-2026-0065 is `unpaid` with `due_date` `2026-08-15` and INV-2026-0052 is `unpaid` with `due_date` `2026-08-20`; both are past due as of 2026-09-11 but neither is `overdue`. Do not assume `overdue == (status unpaid AND due_date < today)`; either the transition is a batch job or the fixture is frozen. Nothing in the docs says when `unpaid` becomes `overdue`.

**Nothing states whether `status` can go backwards** other than by inference from `marked_as_unpaid`, nor what happens to a `paid` invoice that is refunded or charged back. The Invoicing T&C is explicit that Rho "has no obligation to collect, enforce, dispute, or resolve any invoice, chargeback, refund, or customer dispute on your behalf", and no refund/chargeback status or activity type exists in the API.

## B6. Amount arithmetic (derived and verified)

Neither the guide nor the refs state how `total` is computed. Derived from all 12 sandbox invoices and verified exactly:

```
line.total.amount      = round( quantity * unit_price.amount * (1 - line.discount_rate/100) )
effective_tax(line)    = line.tax_rate if line.tax_rate is not null else invoice.tax_rate
invoice.total.amount   = round( SUM( line.total.amount * (1 + effective_tax(line)/100) )
                                * (1 - invoice.discount_rate/100) )
```

Verification (stated vs computed, all 12 match; the single non-integer intermediate rounds to the stated value):

| Invoice | tax_rate | discount_rate | line totals | computed | stated |
| --- | --- | --- | --- | --- | --- |
| INV-2026-0070 | 0 | 0 | 98000 | 98000 | 98000 |
| INV-2026-0066 | 10 | 0 | 100000(null tax), 20000(null), 20000(tax 0), 6000(tax 0) | 110000+22000+20000+6000 = 158000 | 158000 |
| INV-2026-0065 | 0 | 0 | 96000 | 96000 | 96000 |
| INV-2026-0060 | 0 | 0 | 45000 | 45000 | 45000 |
| INV-2026-0052 | 6.25 | 0 | 42353 (tax 6.25) | 45000.0625 -> 45000 | 45000 |
| INV-2026-0050 | 0 | 0 | 156750 | 156750 | 156750 |
| INV-2026-0045 | 0 | **5** | 76000 (line discount 5 on 2x40000) | 76000 * 0.95 = 72200 | 72200 |
| INV-2026-0043 | 0 | 0 | 10000000 | 10000000 | 10000000 |
| INV-2026-0041 | 0 | 0 | 22000 | 22000 | 22000 |
| INV-2026-0040 | 8.5 | 0 | 40000 (tax 8.5) | 43400 | 43400 |
| INV-2026-0002 | 10 | 0 | 90000 (tax 10), 9403 (tax 0) | 99000 + 9403 = 108403 | 108403 |
| INV-2026-0001 | 0 | 0 | 5000 | 5000 | 5000 |

Two non-obvious rules this establishes:

1. **Discounts compound.** INV-2026-0045 applies a 5% line discount (80,000 -> 76,000) and then a 5% invoice discount (76,000 -> 72,200). Invoice-level discount is applied to the post-line-discount, post-tax subtotal, not to the gross.
2. **Tax is applied per line using the line rate when present, otherwise the invoice rate**, then summed. It is not a single invoice-level tax on a subtotal. INV-2026-0066 proves this: with a flat 10% on the 146,000 subtotal the total would be 160,600, but the actual total is 158,000 because two lines carry an explicit `tax_rate: 0`.
3. **Rounding is to the nearest minor unit at the invoice level** (INV-2026-0052: 45000.0625 -> 45000). Whether it is half-up, half-even or truncation cannot be determined from one sample.

The API exposes neither the subtotal nor the tax amount, so any consumer rendering an invoice must reimplement this formula. It is documented nowhere.

## B7. `payments[]` and payment recording

| Field | Type | Req | Documented | Observed |
| --- | --- | --- | --- | --- |
| `type` | string | yes | "How an invoice payment was recorded." Enum: `received_in_account`, `external` | 5 `external`, 2 `received_in_account` |
| `external_method` | string | yes | "Set when type is `external`". Enum: `cash`, `check`, `credit_card`, `other` | `credit_card` x2, `check` x1, `cash` x1, `other` x1; `null` on both `received_in_account` rows |
| `paid_at` | string (date) | yes | "User-provided payment date; **set for external payments**" | **Set on all 7 payments**, including both `received_in_account` rows (`2026-05-18`, `2026-06-21`). **[contradiction]** |
| `transaction_id` | string | yes | "Transaction identifier when type is `received_in_account`" | Set only on the 2 `received_in_account` rows; `null` on all 5 `external` rows |

`transaction_id` values are UUIDv7-shaped (`019e3868-5858-7000-8000-00000000001a`, `019eebb0-0938-7000-8000-00000000000b`) and match the id format of `GET /transactions`, so the join to the ledger is direct. Note again that invoice/customer ids are UUIDv4-shaped while transaction ids are UUIDv7-shaped.

**[contradiction] A card payment is recorded as `external`, not `received_in_account`.** INV-2026-0070 and INV-2026-0066 both show `type: "external"`, `external_method: "credit_card"`, `transaction_id: null`, yet their activity logs contain `card_payment_received` and their status is `pending_payout` (the Stripe card rail). The name `external` therefore does **not** mean "paid outside Rho"; it means "no matched Rho transaction yet". The help center says card funds land in your Primary Checking account, so a Rho-processed card payment is classified `external` while the money is still in flight. Nothing in the docs warns about this.

Every sandbox invoice has at most one payment. Partial payments, over-payments and multi-payment invoices are neither modelled nor excluded by the schema; there is no per-payment `amount` field at all, so the API **cannot represent a partial payment**. That is the single largest modelling gap in the invoicing surface.

All four required-marked payment fields are nullable in practice. A strict code generator that emits non-optional types from `required` will fail to deserialise real payloads on `external_method` and `transaction_id`.

### Payment rails and fees (product side)

From `policies/invoicing-terms-and-conditions` (last amended **August 26, 2026**, page dated August 25, 2026) and `help-center/invoicing/accept-card-payments-on-invoices`:

| Fact | Value |
| --- | --- |
| Supported rails | ACH transfer, domestic wire, international wire, check, credit card, debit card, Google Pay |
| Rho fee on domestic ACH, wire, check into Rho | $0 |
| Card processing fee | **2.9% + $0.30 per transaction**, paid by the business; the customer pays only the invoice amount |
| Card daily limit | **$10,000 USD per day** across all invoices ("default processing limit"); when exhausted the card option disappears from further invoices |
| Card processor | Stripe, Inc. Rho creates and manages a separate Stripe account; you cannot connect an existing one, and payout details / Payment Portal settings cannot be changed in Stripe |
| Card eligibility | USD-denominated invoices only; requires Stripe verification, "subject to third-party underwriting and approval, which is not guaranteed" |
| Stripe integration statuses (UI) | `Pending`, `Action required`, `Connected`, `Failed` |
| First card payment | "deposits may take up to two weeks while Stripe completes its initial review process" |
| Card funds destination | Primary Checking account |
| Who can connect Stripe | Account Owners and Admins only |
| Invoicing subscription / per-invoice fee | $0, included with a Rho account |

**None of this is surfaced in the API.** There is no fee field, no net-of-fee amount, no Stripe account status, no remaining-daily-limit, and no payout id. An integration reconciling a card-paid invoice will see `total: 98000` while the bank receives 98000 - (2.9% + 30) = 94,858 minor units, with no API-visible link between the two.

## B8. `activities[]` and the complete activity-type enum

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `activity_type` | string | yes | "Activity event recorded against an invoice." Enum, 11 values. |
| `created_at` | string (date-time) | yes | No description in the ref. |
| `user_id` | string (UUID) | yes | "User associated with the activity when available". Marked required, **`null` on 12 of 44** sandbox activities (all system-generated events). |
| `emails` | array of string | yes | "Email addresses associated with the activity". Always present; empty array on 32 of 44. |

Complete enum, with observed frequency across the 12 sandbox invoices (44 activities total):

| `activity_type` | Count | `user_id` present? | `emails` populated? | Interpretation |
| --- | --- | --- | --- | --- |
| `created` | 12 | always (`...0001` in every case) | no | Invoice created. Present on 100% of invoices; `created_at` of this activity equals the invoice's `created_at` on every record. |
| `sent` | 10 | always (`...0001`) | **yes**, 1 or 2 recipients | Invoice emailed. 2 invoices have no `sent`: INV-2026-0041 (cancelled) and INV-2026-0001. |
| `downloaded` | 2 | yes (`...0001`, `...0003`) | no | PDF downloaded. |
| `matched` | 2 | **never** (null) | no | Incoming bank transaction auto-matched to the invoice. |
| `marked_as_paid` | 5 | yes (`...0003` in all 5) | no | Manual mark-as-paid. |
| `marked_as_unpaid` | 1 | **null** | no | Reversal of the above. |
| `cancelled` | 1 | yes (`...0002`) | no | Invoice cancelled. |
| `reminder_sent` | 2 | yes (`...0003`) | **yes**, 1 or 2 recipients | Dunning email. |
| `card_payment_received` | 2 | **never** (null) | no | Stripe card capture. |
| `accounting_synced` | 6 | **never** (null) | no | Invoice pushed to the accounting integration. Count matches the 6 invoices with `accounting_sync_status: "synced"`. |
| `payment_accounting_synced` | 1 | **null** (null) | no | Payment record pushed separately from the invoice. Only INV-2026-0070 has it. |

Ordering: activities are returned **ascending by `created_at`** on all 12 invoices (verified: no invoice had an out-of-order timestamp). This is the opposite of the list-level ordering and is not documented.

Observed multi-recipient `emails`: INV-2026-0002 `sent` carries `["info@acmesupplies.com","ap@acmesupplies.com"]` (primary plus one `cc_emails` entry); INV-2026-0060 `reminder_sent` carries `["hello@brightleaf.design","finance@brightleaf.design"]`. So `emails` reflects the actual send list, primary plus CCs, at the time of the event.

User ids appearing in the fixture: `...0001` (creator/sender), `...0002` (canceller), `...0003` (marks paid, downloads, sends reminders). There is **no user endpoint in v1**, so `user_id` cannot be resolved to a name or email through the API at all.

**Conspicuously absent activity types:** nothing for `viewed`/opened by the customer, nothing for edits or amendments, nothing for accounting-sync *failure* (even though `accounting_sync_status: "error"` exists, INV-2026-0045 has no failure activity), nothing for refunds or chargebacks, nothing for `deleted`, and nothing for recurring-schedule generation.

**[note]** `docs_v1_invoicing.md` never mentions `activities` at all. The entire audit log is documented only by the enum list on the two operation reference pages.

## B9. Accounting sync fields

`accounting_sync_status`, enum of 5, defined in both the guide and the refs:

| Value | Guide definition (`docs_v1_invoicing.md`) | [sandbox] count |
| --- | --- | --- |
| `not_pushed` | "eligible to be pushed after being unskipped" | 3 |
| `synced` | "successfully synced to the integration" | 6 |
| `error` | "the most recent sync attempt failed. `accounting_synced_at`, when present, remains the timestamp of the last successful sync." | 1 |
| `skip` | "explicitly excluded from syncing" | 1 |
| `object_changed` | "previously synced, but changed since the last successful sync" | 1 |

The operation refs give a shorter gloss: "Accounting sync state for an invoice. `object_changed` means the invoice was previously synced but has changed since the last successful sync."

**[note] the `not_pushed` definition is circular and probably wrong.** "Eligible to be pushed **after being unskipped**" describes a transition out of `skip`, not the normal never-yet-pushed state. All 3 sandbox `not_pushed` invoices (INV-2026-0065, 0060, 0052) have `accounting_synced_at: null` and no `accounting_synced` activity, i.e. they have simply never been pushed. The wording implies a skip/unskip control that has no API representation.

`accounting_synced_at` behaviour observed:

| Invoice | sync_status | accounting_synced_at | Consistent with docs? |
| --- | --- | --- | --- |
| INV-2026-0070 | synced | 2026-07-18T09:00:00Z | yes; equals `updated_at` |
| INV-2026-0066 | synced | 2026-07-24T11:00:00Z | yes; `updated_at` is later (2026-07-24T16:00:00Z) |
| INV-2026-0065 | not_pushed | null | yes |
| INV-2026-0060 | not_pushed | null | yes |
| INV-2026-0052 | not_pushed | null | yes |
| INV-2026-0050 | synced | 2026-06-28T16:00:00Z | yes |
| INV-2026-0045 | **error** | **null** | permitted ("when present"), but means the `error` case gives you no last-success timestamp in the only sample |
| INV-2026-0043 | object_changed | 2026-05-18T00:07:03Z | yes; equals `updated_at`, and equals the `matched` activity time, so the change that invalidated the sync was the payment match |
| INV-2026-0041 | **skip** | null | cancelled invoice is skipped |
| INV-2026-0040 | synced | 2026-05-20T09:00:00Z | yes |
| INV-2026-0002 | synced | 2026-06-21T20:00:00Z | yes |
| INV-2026-0001 | synced | 2026-01-20T10:00:00Z | yes |

Cross-reference to the product: `help-center/accounting/syncing-invoices-to-your-accounting-software` states invoice syncing is **QuickBooks Online only** ("not yet available for other accounting integrations"), requires the toggle "Sync invoices and customers to QuickBooks" plus a configured "Default Accounts Receivable Ledger", back-fills existing invoices on enablement, and that "you'll have to manually sync the invoice payment or include invoice transactions in your automated syncs". That last point explains why `accounting_synced` and `payment_accounting_synced` are separate activity types and why only 1 of 6 synced invoices has the payment leg synced.

**Conspicuously absent:** no field names the integration (QuickBooks vs anything else), no external/QuickBooks object id, no error message or error code for the `error` state, no `accounting_sync_attempted_at`, and no sync state for the **customer** object even though the product syncs customers too.

## B10. `GET /invoicing/customers` (List customers)

Operation: `listinvoicingcustomers`. Ref: "Deleted customers are excluded unless `include_deleted` is true."

### Query parameters

| Parameter | Type | Documented | Observed [sandbox] |
| --- | --- | --- | --- |
| `search` | string | "Case-insensitive substring match on `legal_name` and `email`" | Confirmed: `search=acme` matched "Acme Supplies"; `search=ORBITMEDIA.CO` (uppercase) matched on the email `accounts@orbitmedia.co`. `search=Preferred` (a substring of a `note`) returned **0**, confirming `note` is not searched. |
| `include_deleted` | boolean | "When true, include deleted customers in the results" | Confirmed: default 7 customers, `include_deleted=true` returns 8. |
| `sort_by` | string | "Sort field. **Defaults to `created_at` when omitted.**" | **`created_at` is the only accepted value.** `legal_name`, `name`, `email`, `updated_at`, `total_revenue`, `last_invoice_id`, `deleted_at`, `id` and `bogus` all return `400` `{"type":"1317","title":"invalid sort_by parameter: \"<value>\"","status":400}`. The parameter exists but can only be set to its own default. |
| `order` | string | "Sort direction. Defaults to `desc` when omitted." | Only lowercase `asc` and `desc` accepted. `ASC`, `ascending`, `bogus` return `400` `{"type":"1317","title":"invalid order parameter: \"<value>\"","status":400}`. |
| `page_size` | integer | "Defaults to 20." Max not documented. | Default 20 confirmed; bounds 1..100 enforced. |
| `page_token` | string | cursor | See D1. |

**[contradiction] Validation strictness is inconsistent across endpoints in the same API.** `/invoicing/customers` hard-rejects an unknown `sort_by` or `order`; `/statements` silently ignores both, including values it cannot honour. Same parameter names, same version, opposite contracts.

### Response 200 / Customer object (identical in list and get)

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `id` | string (UUID) | yes | "Stable global customer identifier" |
| `legal_name` | string | yes | No description. Always populated in sandbox. |
| `email` | string | yes | No description. **`null` on 1 of 8** ("Cedar & Co"). |
| `address` | object | yes | Always present, always fully keyed. |
| `address.address1` | string | yes | |
| `address.address2` | string | yes | **`""` (empty string), never null**, when absent. 2 of 8 have a value ("Suite 400", "Floor 2"). |
| `address.city` | string | yes | |
| `address.country` | string | yes | [sandbox] all `"USA"`, i.e. **ISO 3166 alpha-3, not the alpha-2 used elsewhere**, and not validated/documented as any standard. |
| `address.zip_code` | string | yes | [sandbox] 5-digit US ZIPs, leading zero preserved as a string (`"02109"`). |
| `address.state` | string | yes | [sandbox] 2-letter US state codes. |
| `note` | string | yes | **`null` on 4 of 8.** |
| `cc_emails` | array of string | yes | Empty array when none (3 of 8); 1 or 2 entries otherwise. Never null. |
| `total_revenue` | Money | yes | "Total amount collected across paid invoices". See B12. |
| `last_invoice_id` | string (UUID) | yes | "Identifier of the most recent invoice for this customer". **`null` on 1 of 8** (a customer with no invoices). |
| `created_at` | string (date-time) | yes | The default sort key. |
| `updated_at` | string (date-time) | yes | |
| `deleted_at` | string (date-time) | yes | "Set when the customer is deleted; **null otherwise**". |

Field marked "required" is only a presence guarantee, not a non-null guarantee: `email`, `note`, `last_invoice_id` and `deleted_at` are all nullable while marked required. No `phone`, no tax id, no default payment terms, no default currency, no customer-level accounting sync status, no invoice count.

## B11. `GET /invoicing/customers/{customer_id}` (Get customer)

Operation: `getinvoicingcustomer`. Path parameter `customer_id` (string, required, "Stable global customer identifier").

Ref: "Returns a single customer from Invoicing by ID, **including deleted customers when they still exist** (`deleted_at` is set)." Guide: "fetching a customer by ID still returns it while the record exists."

Response 200 is the bare Customer object, identical field set. Errors add `404`.

[sandbox] verified against the soft-deleted record:

```json
{ "id": "60000000-0000-4000-8000-000000000008",
  "legal_name": "Deleted Co",
  "email": "gone@deletedco.example",
  "address": {"address1":"9 Archive Rd","address2":"","city":"Chicago","country":"USA","state":"IL","zip_code":"60601"},
  "note": "Soft-deleted fixture customer",
  "cc_emails": [],
  "total_revenue": {"amount":5000,"currency":"USD"},
  "last_invoice_id": "70000000-0000-4000-8000-000000000012",
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": "2026-05-01T12:00:00Z",
  "deleted_at": "2026-05-01T12:00:00Z" }
```

Error behaviour:
- unknown well-formed UUID: `404` `{"type":"1303","title":"customer not found","status":404}`
- malformed id (`abc`): `400` `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: customer_id"}`

## B12. Soft-delete semantics (complete)

| Aspect | Behaviour | Source |
| --- | --- | --- |
| Marker | `deleted_at` timestamp on the customer; `null` when live | both customer refs |
| List default | deleted customers **excluded** | ref + [sandbox] 7 vs 8 |
| List opt-in | `include_deleted=true` | ref + [sandbox] |
| Get by id | **always returns** the deleted customer "while the record exists"; no flag needed and no 410 | ref + [sandbox] |
| Sorting of deleted rows | not special-cased; the deleted customer appears in `created_at desc` position (oldest, 2026-01-10) | [sandbox] |
| `search` interaction | not documented whether `search` and `include_deleted` compose | **unstated** |
| Data retained after delete | everything: `legal_name`, `email`, `address`, `note`, `cc_emails`, `total_revenue` (5000), `last_invoice_id` | [sandbox] |
| `updated_at` on delete | set equal to `deleted_at` (`2026-05-01T12:00:00Z`) | [sandbox] |
| Effect on that customer's invoices | **none**. `INV-2026-0001` is returned by the default invoice list, still `status: paid`, still `accounting_sync_status: synced`, and its `customer.id` still points at the deleted record | [sandbox] |
| Invoice soft-delete | **does not exist**. Invoices have no `deleted_at`, and `/invoicing/invoices` has no `include_deleted` (passing it is ignored) | refs + [sandbox] |
| Un-delete / restore | **unstated** anywhere |
| Hard delete | **unstated**. The phrase "while the record exists" implies eventual purge, with no retention period given |

Practical consequence: a naive integration that walks `/invoicing/invoices` and joins `customer.id` against a cached `/invoicing/customers` list will get cache misses for deleted customers. The correct pattern is `include_deleted=true` on the list, or a per-id fetch.

## B13. Sandbox cross-check: invoices

12 invoices, all `USD`, `created_at` range 2026-01-15 to 2026-07-10, `date` (issue) range 2026-01-15 to 2026-07-10, `due_date` range 2026-02-01 to 2026-08-20.

| invoice_number | id (last 4) | status | total | tax | disc | date | due_date | created_at | updated_at | customer (last 4) | file_id | sync | synced_at | payments | activities |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INV-2026-0070 | 0010 | pending_payout | 98000 | 0 | 0 | 2026-07-10 | 2026-08-10 | 2026-07-10T09:00:00Z | 2026-07-18T09:00:00Z | 0005 | 0027 | synced | 2026-07-18T09:00:00Z | 1 external/credit_card | 5 |
| INV-2026-0066 | 0002 | pending_payout | 158000 | 10 | 0 | 2026-07-01 | 2026-07-31 | 2026-07-01T14:32:07Z | 2026-07-24T16:00:00Z | 0001 | 0021 | synced | 2026-07-24T11:00:00Z | 1 external/credit_card | 7 |
| INV-2026-0065 | 0006 | unpaid | 96000 | 0 | 0 | 2026-07-01 | 2026-08-15 | 2026-07-01T08:30:00Z | 2026-07-01T08:30:00Z | 0003 | omitted | not_pushed | null | 0 | 2 |
| INV-2026-0060 | 0003 | overdue | 45000 | 0 | 0 | 2026-06-30 | 2026-07-30 | 2026-06-30T10:00:00Z | 2026-07-20T09:00:00Z | 0002 | 0022 | not_pushed | null | 0 | 3 |
| INV-2026-0052 | 0011 | unpaid | 45000 | 6.25 | 0 | 2026-06-20 | 2026-08-20 | 2026-06-20T15:00:00Z | 2026-06-30T17:00:00Z | 0007 | 0028 | not_pushed | null | 0 | 2 |
| INV-2026-0050 | 0008 | paid | 156750 | 0 | 0 | 2026-06-01 | 2026-07-01 | 2026-06-01T11:00:00Z | 2026-06-28T16:00:00Z | 0004 | 0026 | synced | 2026-06-28T16:00:00Z | 1 external/other | 4 |
| INV-2026-0045 | 0005 | overdue | 72200 | 0 | 5 | 2026-05-15 | 2026-06-15 | 2026-05-15T08:00:00Z | 2026-07-01T08:00:00Z | 0003 | 0024 | error | null | 0 | 3 |
| INV-2026-0043 | 0007 | confirm_payment | 10000000 | 0 | 0 | 2026-05-10 | 2026-06-09 | 2026-05-10T12:00:00Z | 2026-05-18T00:07:03Z | 0003 | 0025 | object_changed | 2026-05-18T00:07:03Z | 1 received_in_account | 3 |
| INV-2026-0041 | 0009 | cancelled | 22000 | 0 | 0 | 2026-05-01 | 2026-05-30 | 2026-05-01T10:00:00Z | 2026-05-10T10:00:00Z | 0005 | omitted | skip | null | 0 | 2 |
| INV-2026-0040 | 0004 | paid | 43400 | 8.5 | 0 | 2026-05-01 | 2026-06-01 | 2026-05-01T09:15:00Z | 2026-05-20T09:00:00Z | 0002 | 0023 | synced | 2026-05-20T09:00:00Z | 1 external/check | 4 |
| INV-2026-0002 | 0001 | paid | 108403 | 10 | 0 | 2026-01-16 | 2026-02-15 | 2026-01-16T14:32:07Z | 2026-06-21T20:00:00Z | 0001 | 0020 | synced | 2026-06-21T20:00:00Z | 1 received_in_account | 6 |
| INV-2026-0001 | 0012 | paid | 5000 | 0 | 0 | 2026-01-15 | 2026-02-01 | 2026-01-15T10:00:00Z | 2026-01-20T10:00:00Z | **0008 (deleted)** | omitted | synced | 2026-01-20T10:00:00Z | 1 external/cash | 3 |

Ordering verification: `created_at` strictly descending across all 12 (2026-07-10T09:00:00 > 2026-07-01T14:32:07 > 2026-07-01T08:30:00 > ... > 2026-01-15T10:00:00). Matches "ordered by creation time, newest first". Note the two 2026-07-01 invoices are separated correctly by time of day, so ties are unlikely but tie-breaking is undocumented.

Other observations:
- `invoice_number` is not ordered with `created_at` in a contiguous way: numbers jump 0001, 0002, 0040, 0041, 0043, 0045, 0050, 0052, 0060, 0065, 0066, 0070. Sequence gaps exist (drafts, deleted invoices, or a shared counter), so never infer count from the number.
- `updated_at` always >= `created_at`, and for synced invoices `accounting_synced_at` <= `updated_at`.
- One `note` contains a U+2014 character: `"Wire received — confirm allocation."` (INV-2026-0043). Notes are free text and may contain any Unicode.
- The fixture's Acme Supplies address, `100 Crosby St, New York, NY 10012`, is Rho's own corporate address as printed in the site footer.
- `INV-2026-0043` at 10,000,000 minor units ($100,000.00) is the fixture's stress case for large amounts; it is well over the $10,000/day card limit, consistent with its `received_in_account` wire payment.

## B14. Sandbox cross-check: customers

8 customers with `include_deleted=true`, 7 without.

| legal_name | id (last 4) | email | cc_emails | created_at | updated_at | deleted_at | total_revenue | last_invoice_id (last 4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Orbit Media Group | 0007 | accounts@orbitmedia.co | 2 | 2026-04-12T13:20:00Z | 2026-06-30T17:00:00Z | null | 0 | 0011 |
| Cedar & Co | 0006 | **null** | 0 | 2026-04-01T08:00:00Z | 2026-04-01T08:00:00Z | null | 0 | **null** |
| Summit Analytics | 0005 | contact@summitanalytics.io | 0 | 2026-03-18T11:00:00Z | 2026-07-18T09:00:00Z | null | 0 | 0010 |
| Harbor Logistics LLC | 0004 | billing@harborlogistics.com | 1 | 2026-03-05T16:45:00Z | 2026-07-10T12:30:00Z | null | 156750 | 0008 |
| Northwind Traders | 0003 | orders@northwind.example | 0 | 2026-02-20T14:00:00Z | 2026-07-01T08:30:00Z | null | 0 | 0006 |
| Brightleaf Design | 0002 | hello@brightleaf.design | 1 | 2026-02-01T09:30:00Z | 2026-06-30T10:00:00Z | null | 43400 | 0003 |
| Acme Supplies | 0001 | info@acmesupplies.com | 2 | 2026-01-15T10:00:00Z | 2026-07-24T16:00:00Z | null | 108403 | 0002 |
| Deleted Co | 0008 | gone@deletedco.example | 0 | 2026-01-10T09:00:00Z | 2026-05-01T12:00:00Z | **2026-05-01T12:00:00Z** | 5000 | 0012 |

### `total_revenue` semantics (derived and verified)

`total_revenue.amount` equals **the sum of `total.amount` over that customer's invoices whose `status == "paid"`**, exactly, for all 8 customers:

| Customer | total_revenue | sum of `paid` invoice totals | Non-paid invoices excluded |
| --- | --- | --- | --- |
| Harbor Logistics LLC | 156750 | 156750 (INV-2026-0050) | none |
| Brightleaf Design | 43400 | 43400 (INV-2026-0040) | INV-2026-0060 overdue 45000 |
| Acme Supplies | 108403 | 108403 (INV-2026-0002) | INV-2026-0066 pending_payout 158000 |
| Deleted Co | 5000 | 5000 (INV-2026-0001) | none |
| Summit Analytics | 0 | 0 | INV-2026-0070 pending_payout 98000, INV-2026-0041 cancelled 22000 |
| Northwind Traders | 0 | 0 | INV-2026-0065 unpaid, INV-2026-0045 overdue, INV-2026-0043 confirm_payment 10000000 |
| Orbit Media Group | 0 | 0 | INV-2026-0052 unpaid 45000 |
| Cedar & Co | 0 | 0 | no invoices |

Therefore: **`pending_payout` and `confirm_payment` do NOT count as collected**, despite the money having arrived or been captured. The doc string "Total amount collected across paid invoices" is accurate only if "paid" is read as the literal status value. `total_revenue` is also gross of the 2.9% + $0.30 card fee.

**Undocumented and unanswerable from the corpus:** what currency `total_revenue` uses for a multi-currency customer (there is one `currency` field, so presumably it cannot represent mixed currencies at all).

### `last_invoice_id` semantics (derived and verified)

`last_invoice_id` points to the customer's invoice with the **latest `created_at`**, not the latest `date`, not the latest unpaid one, and it is not affected by status:

| Customer | Invoices (created_at desc) | last_invoice_id resolves to |
| --- | --- | --- |
| Acme Supplies | INV-2026-0066 (2026-07-01), INV-2026-0002 (2026-01-16) | INV-2026-0066 |
| Northwind Traders | INV-2026-0065 (2026-07-01), INV-2026-0045 (2026-05-15), INV-2026-0043 (2026-05-10) | INV-2026-0065 |
| Brightleaf Design | INV-2026-0060 (2026-06-30), INV-2026-0040 (2026-05-01) | INV-2026-0060 |
| Summit Analytics | INV-2026-0070 (2026-07-10), INV-2026-0041 (2026-05-01, cancelled) | INV-2026-0070 |
| Cedar & Co | none | null |

`updated_at` on the customer tracks invoice activity: Acme's `updated_at` (`2026-07-24T16:00:00Z`) equals INV-2026-0066's `updated_at`; Summit's equals INV-2026-0070's; Northwind's equals INV-2026-0065's `created_at`. So the customer record is touched by invoice events, which means `updated_at` is not a reliable "customer details changed" signal.

---

# PART C. CROSS-CUTTING FINDINGS

## C1. Complete enum inventory (statements + invoicing)

| Enum | Values | Where |
| --- | --- | --- |
| `statement.statement_type` | `account`, `credit`, `treasury` | statements list + get |
| `statement.accounts[].account_type` | `checking`, `savings`, `credit`, `treasury` | statements list + get |
| `invoice.status` | `paid`, `unpaid`, `cancelled`, `overdue`, `confirm_payment`, `pending_payout` | invoices list + get |
| `invoice.payments[].type` | `received_in_account`, `external` | invoices list + get |
| `invoice.payments[].external_method` | `cash`, `check`, `credit_card`, `other` | invoices list + get |
| `invoice.activities[].activity_type` | `created`, `sent`, `downloaded`, `matched`, `marked_as_paid`, `marked_as_unpaid`, `cancelled`, `reminder_sent`, `card_payment_received`, `accounting_synced`, `payment_accounting_synced` | invoices list + get |
| `invoice.accounting_sync_status` | `not_pushed`, `synced`, `error`, `skip`, `object_changed` | invoices list + get |
| `customers.sort_by` | `created_at` only (enforced, undocumented) | [sandbox] |
| `customers.order` | `asc`, `desc` (enforced, lowercase only) | [sandbox] |

Per `docs_v1_versioning.md`, "A new enum value" is a **non-breaking** change that can ship into v1 at any time, and clients must "Handle unknown enum values gracefully... Give any `switch` on it a default case". Every enum above is therefore open-ended by contract.

## C2. Ordering rules, consolidated

| Endpoint | Default order | Configurable? | Tie-break | Verified |
| --- | --- | --- | --- | --- |
| `GET /statements` | `period_end` descending (newest close date first) | `order` only (`asc` vs anything else); `sort_by` is accepted and inert | undocumented. [sandbox] the two 2025-05-31 statements come out credit `161396` then account `439951` in desc, and the reverse in asc, consistent with a stable secondary key | yes |
| `GET /invoicing/invoices` | `created_at` descending | **No.** "Ordering is not user-configurable" | undocumented | yes |
| `GET /invoicing/customers` | `created_at` descending | `order` (`asc`/`desc`) only; `sort_by` accepts only `created_at` | undocumented | yes |
| `invoice.activities[]` | `created_at` **ascending** | n/a, sub-array | n/a | yes, 12/12 |
| `invoice.line_items[]` | insertion order, no index field | n/a | n/a | assumed |
| `statement.accounts[]` | single element everywhere in sandbox, order unverifiable | n/a | n/a | no |

## C3. Filtering rules, consolidated

| Endpoint | Filter | Multi-value | Boundary | Invalid value |
| --- | --- | --- | --- | --- |
| statements | `account_id` | yes, OR | n/a | `400 about:blank` |
| statements | `statement_type` | yes, OR | n/a | `200` empty (silent) |
| statements | `period_end_after` | no | **inclusive** | `400 about:blank` |
| statements | `period_end_before` | no | **exclusive** | `400 about:blank` |
| statements | `period_start_after` | no | inclusive | `400 about:blank` |
| statements | `period_start_before` | no | exclusive | `400 about:blank` |
| invoices | `status` | yes, OR | n/a | `200` empty (silent) |
| invoices | `date_after` | no | inclusive | `400 about:blank` |
| invoices | `date_before` | no | **inclusive** | `400 about:blank` |
| invoices | `due_date_after` | no | inclusive | `400 about:blank` |
| invoices | `due_date_before` | no | **inclusive** | `400 about:blank` |
| customers | `search` | no | substring, case-insensitive, `legal_name` + `email` only | n/a |
| customers | `include_deleted` | no | boolean | untested for non-boolean |

Combining multiple filters is AND across parameters and OR within an array parameter. Not stated in the docs; verified for `period_end_after` + `period_end_before` and for `status` + `date_*`.

## C4. `required` does not mean non-null

Both invoicing refs mark as `required` a set of fields that are demonstrably null in the sandbox. This is the single most likely source of deserialisation crashes for generated clients:

| Field | Marked | Observed nulls |
| --- | --- | --- |
| `invoice.note` | required | 3 of 12 |
| `invoice.due_date` | required (doc text itself says "null when not set") | 0 of 12, but documented nullable |
| `invoice.accounting_synced_at` | required | 5 of 12 |
| `invoice.payments[].external_method` | required | 2 of 7 |
| `invoice.payments[].transaction_id` | required | 5 of 7 |
| `invoice.activities[].user_id` | required | 12 of 44 |
| `customer.email` | required | 1 of 8 |
| `customer.note` | required | 4 of 8 |
| `customer.last_invoice_id` | required | 1 of 8 |
| `customer.deleted_at` | required (doc says "null otherwise") | 7 of 8 |
| `page.next_page_token` | required | null on every last page |

By contrast `invoice.file_id` is marked **optional** and is genuinely **absent** (key omitted) rather than null, and the credit-only statement fields (`spending`, `repayments`, `cashback`, `repayment_date`) are also key-absent rather than null. So the API mixes two absence conventions: omitted keys for genuinely optional fields, explicit nulls for "required but empty" fields.

## C5. Signed-URL architecture across the three file-bearing resources

| Resource | URL delivery | TTL documented | TTL observed | Bucket host (sandbox) | Works in sandbox |
| --- | --- | --- | --- | --- | --- |
| Statements | **embedded** as `pdf_url` in list and get | "up to 15 minutes" | 899 s | `sandbox-statements.files.rho.co` | **yes** |
| Transaction attachments | separate `GET /transactions/{id}/files/{file_id}` | "short-lived" | 899 s | `rho-api-sandbox.files.rho.co` | **yes** |
| Invoice PDF | separate `GET /invoicing/invoices/{id}/files/{file_id}` | "short-lived", no number | not observable | unknown | **no, 404 on every file_id** |

All are GCS V4 signed URLs signed by `file-service@pledge-218909.iam.gserviceaccount.com` with `X-Goog-SignedHeaders=host`, so they must be fetched with no Authorization header and cannot be proxied with added headers.

Refresh guidance differs by resource: statements say re-fetch the whole statement; invoicing says "Fetch again whenever a new signed URL is needed; do not persist the URL"; transactions say "Follow it straight away, without an Authorization header, and request another one whenever a new URL is needed instead of reusing or persisting the last." Consistent intent, three different wordings, one of which (statements) is the only one that commits to a number.

---

# PART D. PAGINATION AND ERRORS (behavioural, mostly undocumented)

## D1. Cursor internals

`docs_v1_pagination.md` describes the cursor as opaque and claims: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." It also says "Their format and lifetime are not part of the API contract and may change without notice."

[sandbox] the cursor decodes cleanly:

```
next_page_token = base64url( {"v":1,"f":"<22-char base64url fingerprint>","t":"<base64url>"} )
inner t          = base64url( "offset:N" )
```

Worked examples:

| Request | Token | Decoded outer | Decoded `t` |
| --- | --- | --- | --- |
| `GET /statements?page_size=5` | `eyJ2IjoxLCJmIjoiNl9aQ1ZWOEFrR3M5TjdxSENhaHZwUSIsInQiOiJiMlptYzJWME9qVSJ9` | `{"v":1,"f":"6_ZCVV8AkGs9N7qHCahvpQ","t":"b2Zmc2V0OjU"}` | `offset:5` |
| `GET /statements?page_size=7` | | `f` unchanged, `t` = `b2Zmc2V0Ojc` | `offset:7` |
| `GET /statements?page_size=5&statement_type=credit` | | `f` = `RF9_5_qn1RhOur0b7-Yaew` (different) | `offset:5` |
| `GET /statements?page_size=5&order=asc` | | `f` = `R181hVuA96yqmECtQrsLsQ` (different) | `offset:5` |
| `GET /invoicing/customers?page_size=3` | | `f` = `w_1GGrw_nNeSMIW_I5t6fQ` | `offset:3` |
| `GET /invoicing/invoices?page_size=2&status=paid` | `eyJ2IjoxLCJmIjoiZFhmcnZXU3JfWnNWdjJnUWNpbjJIdyIsInQiOiJiMlptYzJWME9qSSJ9` | `{"v":1,"f":"dXfrvWSr_ZsVv2gQcin2Hw","t":"b2Zmc2V0OjI"}` | `offset:2` |

**[contradiction] This is offset pagination, so the stability guarantee cannot hold.** With `/statements` ordered newest-close-date-first, a statement finalized mid-iteration is inserted at position 0 and every subsequent offset page shifts by one, duplicating exactly one record at each page boundary. The docs' claim of insert-safety is false for the default ordering of the very endpoint whose primary workflow is "list statements **as they become available**".

Enforcement observed:
- **Filter fingerprint is enforced.** Reusing a `status=paid` token with `status=unpaid` returns `400` `{"type":"1317","title":"page_token must be a valid cursor","status":400}`. Matches the doc's "Using a cursor with changed filters or sorting will result in `400 Bad Request`".
- **`page_size` is NOT part of the fingerprint.** `GET /statements?page_size=10&page_token=<token from page_size=5>` returns `200` with 10 rows starting at offset 5. So you can change page size mid-iteration, silently, which is another route to skipped or duplicated rows if the client believes the doc's guarantee.
- **`sort_by` IS part of the fingerprint on statements**, even though it has no effect on results. Changing an inert parameter invalidates the cursor.
- Cross-endpoint reuse is rejected: an invoices token on `/invoicing/customers` returns the same `1317` cursor error.
- Garbage tokens return the same `1317` cursor error.
- Token `v` is `1`, so a version field exists for future cursor format changes.

## D2. Observed error-code catalogue

The docs describe only the RFC 9457 field set and give one worked example with `"type":"about:blank"`. The live sandbox uses numeric string codes in `type` for most failures. Complete list of what was reproduced:

| HTTP | `type` | `title` | `detail` | Trigger |
| --- | --- | --- | --- | --- |
| 401 | `"2"` | `Unauthenticated` | absent | missing Authorization header; empty bearer; sandbox token against production |
| 404 | `"1303"` | `statement not found` | absent | `GET /statements/999999999` |
| 404 | `"1303"` | `invoice not found` | absent | `GET /invoicing/invoices/<unknown uuid>` |
| 404 | `"1303"` | `customer not found` | absent | `GET /invoicing/customers/<unknown uuid>` |
| 404 | `"1303"` | `invoice file not found` | absent | every invoice file fetch, including valid `file_id` values |
| 400 | `"1317"` | `page_size must be between 1 and 100` | absent | `page_size=0`, `page_size=101` on all three list endpoints |
| 400 | `"1317"` | `page_token must be a valid cursor` | absent | garbage token, changed filters, cross-endpoint token |
| 400 | `"1317"` | `invalid sort_by parameter: "<v>"` | absent | `/invoicing/customers?sort_by=<anything but created_at>` |
| 400 | `"1317"` | `invalid order parameter: "<v>"` | absent | `/invoicing/customers?order=<anything but asc/desc>` |
| 400 | `"about:blank"` | `Bad Request` | `invalid parameter: <name>` | malformed path ids (`invoice_id`, `customer_id`) and malformed query values (`account_id`, `period_end_after`, `date_after`) |

Two distinct error families are in play: a Rho application layer that emits numeric `type` codes and no `detail`, and a request-validation layer that emits `about:blank` plus a `detail`. The docs describe only the second and present the first's field as "A URI reference that identifies the problem type". `"1303"` and `"2"` are not URI references.

**[contradiction]** `docs_v1_auth.md` shows the 401 body as `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}`. The sandbox returns `{"type":"2","title":"Unauthenticated","status":401}`: different `type`, different `title`, no `detail`.

Also note: the `title` values carry machine-relevant content (parameter names, bounds) while `type` carries an opaque code, which is the reverse of RFC 9457's intent, where `type` is the stable machine identifier and `title` the human summary.

---

# PART E. WHAT IS CONSPICUOUSLY NOT STATED

Statements:
1. No condition under which `pdf_url` is `null`, and no sandbox record exercising it.
2. No `available_at` range filter, so incremental "give me statements finalized since T" polling is impossible; you must re-scan by period.
3. No statement-level currency; only per-figure. No multi-currency statement example.
4. No `sort_by` enum, no default; the parameter appears functionless.
5. No statement of how often a statement can change after `available_at`, or whether one is ever reissued/restated.
6. No mapping between `statement_type` and `accounts[].account_type`, no rule for which `account_type` values can appear under which `statement_type`.
7. No link from a statement to the transactions in its period (no `transaction_ids`, no documented `GET /transactions?period=`, though `posted_at` filters presumably exist on transactions).
8. No credit terms, repayment amount due, minimum payment, APR, or credit limit. `repayment_date` is the only credit-terms field and it never appears.

Invoicing:
9. **No write operations at all.** Every invoicing endpoint is a GET. You cannot create, send, void, mark paid, or attach a PDF via the API. The API is a read mirror of the dashboard.
10. **No partial payment model.** `payments[]` entries carry no amount.
11. No `customer_id` filter on invoices, so per-customer AR ageing requires pulling every invoice.
12. No draft state, no `sent_at`, no payment-portal URL, no recurrence/schedule fields despite the product offering "Schedule this invoice to repeat".
13. No fee, net-of-fee, or payout information for card payments, despite a 2.9% + $0.30 fee and a $10,000/day cap existing on the product side.
14. No Stripe connection status, no remaining daily card limit.
15. No accounting-integration identity, external object id, or error message for `accounting_sync_status: "error"`.
16. No customer sync status even though the product syncs customers to QuickBooks.
17. No user directory, so `activities[].user_id` is unresolvable.
18. No webhooks or events anywhere in v1. Every workflow in these docs is polling.
19. No retention period behind "while the record exists" for soft-deleted customers; no restore.
20. No `include_deleted` semantics when combined with `search`.
21. No statement of how the invoice total is computed (section B6 had to be reverse-engineered).
22. The `address.country` field is not tied to a standard; the fixture uses alpha-3 `USA`.

Both:
23. No `429` in any declared error set, contradicting the rate-limits page.
24. No idempotency, ETag, `If-None-Match`, or `Last-Modified` support on any endpoint.
25. No batch/bulk fetch by id list.
26. No documented tie-break for equal sort keys on any list.

---

# PART F. PRODUCT-SIDE CONTEXT (for the dossier, non-API)

| Fact | Value | Source | As-of |
| --- | --- | --- | --- |
| Invoicing pricing | $0 per-invoice and $0 monthly, "included with your Rho account"; unlimited invoices | `product/invoicing` | "Product claims current as of September 2026" |
| Rho fee on inbound domestic ACH, wire, check | $0 | `product/invoicing`, T&C section 6 | Aug 26, 2026 (T&C) |
| Card processing fee | 2.9% + $0.30 per transaction, paid by the business | T&C section 4, help center | Aug 26, 2026 |
| Card daily limit | $10,000 USD/day across all invoices | T&C section 4, help center | Aug 26, 2026 |
| Card processor | Stripe, Inc.; Rho creates and manages a separate connected account; existing Stripe accounts cannot be connected | help center | 2026 |
| Payer requirements | "0 Rho accounts required for the person paying your invoice" | `product/invoicing` | Sept 2026 |
| Payer methods | credit card, debit card, Google Pay, ACH, domestic wire, international wire, check | `product/invoicing`, help center | Sept 2026 |
| Accounting sync coverage | QuickBooks Online **only**; other platforms "on the roadmap" | help center | 2026 |
| Statement availability | checking: 2nd calendar day; savings: by end of 5th business day; card Daily Terms: the 5th; card Monthly Terms: one business day after the statement repayment date | help center | 2026 |
| Bank partner disclosure | "Checking account and card services provided by Webster Bank, a division of Santander Bank, N.A. Member FDIC"; "Rho is a fintech company, not a bank" | `product/invoicing` | Sept 2026 |
| Legal entity | Under Technologies, Inc. DBA Rho Technologies, 100 Crosby Street, New York, NY 10012 | site footer | 2026 |
| Invoicing T&C | Last amended **August 26, 2026** (page dated August 25, 2026) | `policies/invoicing-terms-and-conditions` | Aug 26, 2026 |

**[Rho claim]** competitor comparison on `product/invoicing`, "Competitive data collected from Stripe, Mercury, and QuickBooks websites as of **2026-09-08**, and may change":

| Dimension | Rho [Rho claim] | Stripe [Rho claim] | Mercury [Rho claim] | QuickBooks [Rho claim] |
| --- | --- | --- | --- | --- |
| Invoicing cost | Included at no extra cost | 0.4% per paid invoice (Starter); 0.5% (Plus) | Unlimited invoices free on every tier; recurring requires Plus ($29.90/mo billed annually) | Free plan capped at 2 invoices/month; unlimited from $20/mo (Lite) |
| ACH / bank transfer fee | $0 on domestic ACH, wires, checks | 0.8% ACH Direct Debit, $5.00 cap, plus per-invoice fee | $1/transaction on Plus, $0 on Pro, unavailable on free tier | 1% per ACH bank payment |
| Recurring invoices | "Not shown" in the Rho column | Stripe Billing 0.7% of billing volume (pay-as-you-go) | Plus and Pro only | From Simple Start ($38/mo) |
| Payment matching | "Not shown" in the Rho column | Automatic reconciliation, Smart Retries | Auto-imports to QuickBooks, NetSuite, Xero | Books update automatically |

Note the table's own Rho column literally reads "Not shown" for recurring invoices and payment matching, while the marketing copy directly above it claims both ("Recurring invoices go out on the schedule you set", "Payments that match themselves"). Self-contradiction inside one page.

**Separate product, do not confuse:** `rho.co/tools/free-invoice-generator` is a standalone free web tool, not the in-product Invoicing API. Its technical guide caps invoices at **5 line items**, generates A4 PDFs, allows a logo of max 2MB in JPEG/JPG/PNG, and has a 10MB max file size. None of those limits apply to the API (the sandbox has a 4-line invoice, and no line-count limit is documented).

---

# PART G. ACTIONABLE SUMMARY FOR AN INTEGRATOR

1. Do not trust `account_id is null` to detect credit statements; use `statement_type == "credit"` or `account_type == "credit"`.
2. Do not expect `repayment_date`; it is documented but never returned.
3. Do not expect consolidated multi-account statements; sandbox issues one statement per account.
4. Do not join `statements.accounts[].account_type` to `accounts.account_type`; the vocabularies differ and disagree on the same account.
5. Do not reuse a `pdf_url` beyond ~14 minutes; re-fetch via `GET /statements/{id}`. Budget your archive job accordingly, one page of 100 shares a single 899-second window.
6. Treat `page_token` as offset-based, not insert-stable, despite the doc. For statements, prefer `period_end_after`/`period_end_before` windows over cursor-walking a live head.
7. Never change `page_size` mid-iteration (allowed, and unsafe).
8. Generate all response models with every field nullable; `required` is a presence guarantee only.
9. Handle both absence conventions: omitted keys (`file_id`, credit-only statement figures) and explicit nulls (everything else).
10. Expect `type` in error bodies to be a numeric string, not a URI. Key off `status` plus `title`, and be ready for a missing `detail`.
11. Reimplement the invoice total formula in B6 if you need a subtotal or tax amount; the API exposes neither.
12. Fetch customers with `include_deleted=true` when building an invoice-to-customer join, or you will miss deleted customers whose invoices are still live.
13. `total_revenue` counts only `status == "paid"`, gross of card fees. Do not use it as cash received.
14. To learn whether an invoice was ever emailed, scan `activities` for `sent`; there is no status or timestamp for it.
15. A card payment appears as `payments[].type == "external"` with `external_method == "credit_card"` and a null `transaction_id`. Detect the Rho card rail via the `card_payment_received` activity or `status == "pending_payout"`, not via `type`.
16. The invoicing file endpoint is currently unusable in sandbox (404 on every advertised `file_id`); build against the transactions file endpoint if you need to prototype the signed-URL flow.
