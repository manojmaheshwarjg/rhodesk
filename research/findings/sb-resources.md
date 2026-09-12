# Rho sandbox API: single-resource GETs, file endpoints, error semantics, write-method rejection

Empirical probe of `https://rhoapi-sandbox.rho.co/api/v1` with `Authorization: Bearer sandbox`.
All probes executed 2026-09-11 between 23:38Z and 23:56Z. Raw evidence:
`/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-resources/` (238 files, 1.2 MB).

Scope note: this is the **sandbox**. Production is `https://rhoapi.rho.co/api/v1`. Behaviours below are observed on sandbox fixture data and may not hold in production; where docs and sandbox disagree, both are recorded.

---

## 1. Headline findings

| # | Finding | Confidence |
|---|---|---|
| 1 | **Single-resource GET returns exactly zero additional fields versus the list form.** Swept all 133 resources across 6 types; every one is deep-equal. | Proven exhaustively |
| 2 | **`GET /invoicing/invoices/{id}/files/{fid}` is broken in sandbox: 9/9 documented-correct pairings return 404.** | Proven exhaustively |
| 3 | **Statement `pdf_url` is cached server-side per PDF blob for ~300 s**, then re-signed. Re-fetching a statement inside that window returns the identical URL, so the documented "re-fetch for a fresh URL" remedy does not work on demand. Residual life is bounded at ~599-899 s, so the "up to 15 minutes" claim is honest. | Proven by timed polling over 3 cache epochs |
| 4 | Transaction file `download_url` **is** minted fresh per request (full 899 s every time). Asymmetric with statements. | Proven by timed polling |
| 5 | **405 is returned before authentication.** Write methods are rejected with no token at all. | Proven |
| 6 | **Any non-empty bearer token is accepted on sandbox reads.** `Bearer WRONGTOKEN` returns 200 with full data; only a *missing* header gives 401. | Proven |
| 7 | Two incompatible error envelopes coexist: 400 uses `type:"about:blank"` + `detail`; 404 uses `type:"1303"` + no `detail`. Neither matches the other's documented shape. | Proven |
| 8 | UUID parsing is highly lenient (no-dash, braces, `urn:uuid:`, uppercase all accepted). | Proven |

---

## 2. ID inventory harvested from list endpoints

| Resource | Count | ID shape | Example |
|---|---|---|---|
| accounts | 14 | UUID v4, prefix `30000000-0000-4000-8000-` | `...-000000000002` |
| cards | 8 | UUID v4, prefix `20000000-0000-4000-8000-` | `...-000000000001` |
| transactions | 72 | **UUID v7** (time-ordered), varied | `019f0554-0bf0-7000-8000-00000000000a` |
| statements | 20 | **opaque numeric string**, not a UUID | `572981`, `439951`, `161396` |
| invoicing customers | 7 (8 with `include_deleted=true`) | UUID v4, prefix `60000000-0000-4000-8000-` | `...-000000000007` |
| invoicing invoices | 12 | UUID v4, prefix `70000000-0000-4000-8000-` | `...-000000000010` |
| transaction attachments | 15 distinct `file_id` on 14 transactions | random UUID v4 | `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15` |
| invoice files | 9 `file_id` on 9/12 invoices | UUID v4, prefix `50000000-0000-4000-8000-` | `...-000000000027` |

Notes:
- Transaction IDs are **UUID v7** (`019f0554-0bf0-7000-...`, version nibble `7`). The remaining resources use v4-shaped fixtures with sequential decimal-styled suffixes.
- Invoice suffixes are **decimal-styled, not hex**: `...0009` → `...0010` exists, while `...000a`, `...000b`, `...000c` return 404. Transaction suffixes are genuinely hex (`...00000000000a` is valid).
- Sequential ID-space probing found **no resources hidden from the list endpoints**. Every 200 in the invoice sweep was already in the list; every non-listed ID was a 404.
- 72 transactions paginate as 20/20/20/12 pages. `limit=100` is silently capped at 20.

---

## 3. Single-GET vs list: exhaustive field-by-field diff

Method: fetch the list, extract the row for each ID, fetch `GET /{resource}/{id}`, compare deep-equal and key-set. Every resource of every type was swept, not a sample.

| Resource | n | Deep-equal | Keys only in single-GET | Keys only in list | Value diffs |
|---|---|---|---|---|---|
| accounts | 14 | **14/14** | NONE | NONE | 0 |
| cards | 8 | **8/8** | NONE | NONE | 0 |
| transactions | 72 | **72/72** | NONE | NONE | 0 |
| statements | 20 | **20/20** | NONE | NONE | 0 (see caveat) |
| invoicing customers | 7 | **7/7** | NONE | NONE | 0 |
| invoicing invoices | 12 | **12/12** | NONE | NONE | 0 |
| **Total** | **133** | **133/133** | **NONE** | **NONE** | **0** |

Statements caveat: when the list call and the single GET straddle a signed-URL re-signing boundary, `pdf_url` differs. Captured instance:

```
pdf_url LIST: ...&X-Goog-Date=20260911T233808Z&X-Goog-Signature=4dd645...
pdf_url GET : ...&X-Goog-Date=20260911T234315Z&X-Goog-Signature=132322...
```

Same object path (`/41addf56a3d9ab46a2bfedc6.pdf`), same `X-Goog-Expires=899`, different signing timestamp. This is a re-signing artefact, not extra data. In the same-window sweep all 20 matched exactly.

### 3.1 What this means

The single-resource endpoints are **pure convenience lookups with no payload advantage**. There is no "summary vs detail" tier. Concretely:

- Fetching a list then looping single GETs to "enrich" rows is **pure waste** and, at ~60 req/min per token (documented rate limit), actively harmful.
- Rho's own docs already say this for accounts: *"Every `transaction` already carries `account_id`, `account_type`, and the account's display name, so most reconciliation needs no extra calls"* (`docs/docs_v1_accounts.md:42`). The sweep confirms it generalises to every resource type.
- The only endpoint where a single GET buys you something is `GET /statements/{id}`, and what it buys is a re-signed `pdf_url` (subject to the cache in §5.3), not new fields.

### 3.2 Documented fields that never materialise

Full census over all rows, not a sample.

**Transactions (72 rows):**

| Field | Present | Note |
|---|---|---|
| `account_id`, `account_name`, `account_type`, `amount`, `attachments`, `counterparty_name`, `id`, `initiated_at`, `money_movement_id`, `status`, `transaction_type` | 72/72 | always |
| `posted_at` | 71/72 | 1 null, the pending row |
| `memo` | 39/72 | omitted when unset, not null |
| `note` | 39/72 | omitted when unset |
| `user_id`, `user_full_name` | 38/72 | absent for system-initiated |
| `card_id`, `card_name` | 12/72 | card transactions only |
| **`tracking_number`** | **0/72** | **documented, never emitted** |
| **`counterparty_logo_url`** | **0/72** | **documented, never emitted** |

`tracking_number` is documented in detail (`docs/docs_v1_transactions.md:57`: *"an ACH NACHA trace number, or a wire IMAD/OMAD. MT103 reference numbers are not returned"*) yet **no sandbox transaction carries it, including `wire_out`, `wire_in`, `international_wire_out` and `ach_debit` rows that should**. An integrator cannot test trace-number handling against this sandbox. Same for `counterparty_logo_url`.

**Statements (20 rows, 20 `accounts[]` sub-rows):** `accounts[].repayment_date` is documented but present 0/20. `spending`, `repayments`, `cashback` appear 12/20 (exactly the credit statements).

**Cards (8 rows):** `allowed_categories`, `allowed_merchants`, `blocked_categories`, `blocked_merchants` each appear on only 1/8 cards.

**Invoices (12 rows):** `file_id` present on 9/12. `file_name` never appears at invoice level (consistent with the schema, which only defines it on the file endpoint response).

### 3.3 Enum values actually observed

| Field | Observed values | vs documented |
|---|---|---|
| `transaction_type` | 22 of 33 documented values seen: `ach_credit`, `ach_debit`, `ach_return`, `adjustment_credit`, `adjustment_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `credit_repayment`, `credit_repayment_refund`, `internal_transfer`, `international_wire_fee`, `international_wire_out`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`, `wire_out` | 11 unseen incl. `card_credit`, `credit_cashback`, all 6 `treasury_*`, `international_wire_in`, `international_wire_fee_refund` |
| `status` (transaction) | all 4: `pending`, `settled`, `failed`, `awaiting_approval` | complete |
| `account_type` (transaction) | `checking`, `credit`, `rewards`, `savings` | `investment` never seen |
| `account_type` (accounts list) | `checking`, `credit`, `rewards`, `savings` | `investment` never seen |
| `account_type` (statements `accounts[]`) | `credit`, `savings`, **`treasury`** | **`treasury` is NOT in the documented account_type enum** |
| `statement_type` | `account` (1), `credit` (12), `treasury` (7) | complete |
| card `status` | `active`, `canceled`, `expired`, `locked`, `suspended` | 6 unseen: `printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `expiring` |
| card `type` | `physical`, `virtual` | complete |
| `spending_limit_type` | `daily`, `fixed`, `monthly` | n/a |
| invoice `status` | `cancelled`, `confirm_payment`, `overdue`, `paid`, `pending_payout`, `unpaid` | note British spelling `cancelled` |
| `accounting_sync_status` | all 5: `error`, `not_pushed`, `object_changed`, `skip`, `synced` | complete |
| invoice `activities[].activity_type` | `accounting_synced`, `cancelled`, `card_payment_received`, `created`, `downloaded`, `marked_as_paid`, `marked_as_unpaid`, `matched`, `payment_accounting_synced`, `reminder_sent`, `sent` | n/a |
| invoice `payments[].type` | `external`, `received_in_account` | n/a |
| invoice `payments[].external_method` | `cash`, `check`, `credit_card`, `other`, plus null | n/a |

**Contradiction:** statements nest `account_type: "treasury"` inside `accounts[]`, but the documented `account_type` enum on accounts and transactions is `checking, credit, investment, savings, rewards`. `treasury` is not in it. The statements schema evidently reuses the field name with a different value space, or the account enum is incomplete.

---

## 4. Documented-vs-observed contradictions

| # | Doc says | Observed | Source |
|---|---|---|---|
| C1 | *"`accounts.account_id` ... Null for credit statements, which are not tied to a deposit account."* | **All 12 credit statements carry a non-null `account_id`** (e.g. `30000000-0000-4000-8000-000000000008`) | `api/statements_getstatement.md:37` |
| C2 | *"One entry per account for account and treasury statements, which may span multiple checking/savings accounts"* | **0 of 20 statements has more than one `accounts[]` entry** | same |
| C3 | *"each request to this endpoint issues a fresh, short-lived link ... request another one whenever a new URL is needed instead of reusing or persisting the last"* (transaction files); *"If the link lapses, re-fetch the statement with `GET /statements/{id}` to obtain a fresh URL"* (statements) | **True for transaction files. Misleading for statements**: re-fetching returns the identical cached URL for ~300 s; a client cannot force a re-sign on demand. The cache does rotate ~10 min before expiry, so the remedy usually works in practice, but not by the described mechanism (§5.3) | `docs/docs_v1_transactions.md:71`, `api/statements_getstatement.md:28` |
| C4 | *"When an invoice has a PDF, `file_id` is present ... Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`"* | **All 9 invoices with `file_id` return 404 from that endpoint** | `docs/docs_v1_invoicing.md:44` |
| C5 | Error schema: `type` is *"A URI reference that identifies the problem type. Example: about:blank"* | 404s return `"type":"1303"`, a bare numeric string, not a URI reference. 401 returns `"type":"2"` | all `api/*.md` |
| C6 | Error schema lists `detail` as an available field on 404 | **No 404 anywhere returned a `detail` field.** Only 400s carry it | all `api/*.md` |
| C7 | `tracking_number` documented with detailed semantics | absent from all 72 transactions incl. wires | `docs/docs_v1_transactions.md:57` |
| C8 | `accounts[].repayment_date` documented | absent from all 20 statements | `api/statements_getstatement.md` |

**Conspicuously not stated anywhere in the docs:**
- That statement `pdf_url` values are cached and shared across statements (§5.3). The docs' remedy for a lapsed link does not work.
- That multiple statements can point at the same PDF object. In sandbox, **20 statements resolve to just 3 distinct blobs**.
- Any `Retry-After`, `X-RateLimit-*`, `X-Request-Id`, `ETag` or `Cache-Control` header. None observed on any API response (§8).
- The `Allow: GET` response to write methods, or that it precedes auth.
- That signed URLs are Google Cloud Storage V4 and therefore honour `Range` and `HEAD`.

---

## 5. File endpoints

### 5.1 `GET /transactions/{tid}/files/{fid}`: works

Response is exactly 3 keys, matching the schema:

```json
{
  "download_url": "https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?X-Goog-Algorithm=...",
  "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15",
  "file_name": "parking-receipt.pdf"
}
```

`Content-Type: application/json`. No `page` wrapper.

### 5.2 Signed URL structure

Google Cloud Storage **V4 signed URL**, RSA-signed by a service account.

| Component | Value |
|---|---|
| Scheme/host (transaction attachments) | `https://rho-api-sandbox.files.rho.co` |
| Scheme/host (statement PDFs) | `https://sandbox-statements.files.rho.co` |
| Path | `/{24-hex-char}.{ext}` e.g. `/f0b72b6108f6ebfd9818fb0f.pdf`, `/b9074a472541546b1d40769c.csv` |
| `X-Goog-Algorithm` | `GOOG4-RSA-SHA256` |
| `X-Goog-Credential` | `file-service@pledge-218909.iam.gserviceaccount.com/20260911/auto/storage/goog4_request` |
| `X-Goog-Date` | signing instant, e.g. `20260911T234415Z` (second granularity) |
| `X-Goog-Expires` | **`899`** seconds (14 min 59 s) on every URL observed, both buckets |
| `X-Goog-Signature` | 512 hex chars (2048-bit RSA) |
| `X-Goog-SignedHeaders` | `host` |

Observations:
- **Two distinct buckets**, one per file class, both signed by the same service account `file-service@pledge-218909.iam.gserviceaccount.com`. GCP project id `pledge-218909` is leaked in every signed URL. "Pledge" appears to be a legacy internal project name.
- Object names are **content-addressed-looking 24-hex-char blobs**, carrying no account, business or transaction identifier. No enumerable structure.
- The object path is **stable per `file_id` across transactions**. `file_id` `cdc328c1-c3a3-4670-a371-28e34891ee68` is attached to two different transactions (`019f0143-...-0002` and `019ef6d6-...-0009`) and both resolve to `/1a492c9609a8a945c3523775.pdf`. Deduplicated storage.
- `X-Goog-Expires=899` rather than a round 900 suggests the signer computes an absolute deadline and converts back to a relative TTL, losing a second.

### 5.3 Expiry: stated, observed, and the signing cache

**Stated:** *"valid for up to 15 minutes"* (`docs/docs_v1_statements.md:17`), *"short-lived"* (transaction and invoice file docs). No doc states 899 s.

**Observed expiry rule:** exactly `X-Goog-Date + X-Goog-Expires`, enforced by GCS. Proven two ways.

1. Forcing `X-Goog-Expires=899` → `1` on a URL signed at `20260911T234844Z`:
   ```
   HTTP 400
   <Error><Code>ExpiredToken</Code><Message>Invalid argument.</Message>
   <Details>The provided token has expired. Request signature expired at: 2026-09-11T23:48:45+00:00</Details></Error>
   ```
   23:48:44 + 1 s = 23:48:45 exactly.

2. A statement URL captured in an earlier session at `X-Goog-Date=20260911T232222Z`, replayed at 23:49:29Z (27 minutes later):
   ```
   HTTP 400  ExpiredToken  "Request signature expired at: 2026-09-11T23:37:21+00:00"
   ```
   23:22:22 + 899 s = 23:37:21 exactly.

**The server-side signing cache.** A poller at 20 s intervals fetched `GET /statements/572981` and `GET /transactions/{tid}/files/{fid}` in lockstep for 23 samples across 11 minutes, recording the `X-Goog-Date` returned each time.

Three statement signing epochs were observed:

| Epoch | Signed at | Expires (signed + 899 s) | Re-signed after |
|---|---|---|---|
| 1 | 23:49:09Z | 00:04:08Z | **302 s** |
| 2 | 23:54:11Z | 00:09:10Z | **313 s** |
| 3 | 23:59:24Z | 00:14:23Z | (poller stopped) |

The re-sign interval is **~300 s**, not the 899 s expiry. Crucially, **each URL is replaced roughly 10 minutes before it expires**, so a cached URL is never served close to death.

Residual life at each poll:

| Polled (UTC) | statement `X-Goog-Date` | statement residual | txn file `X-Goog-Date` | txn file residual |
|---|---|---|---|---|
| 23:52:26 | 20260911T234909Z | 702 s | 20260911T235228Z | 901 s |
| 23:53:09 | 20260911T234909Z | 659 s | 20260911T235310Z | 900 s |
| 23:53:50 | 20260911T234909Z | 618 s | 20260911T235351Z | 900 s |
| 23:59:04 | 20260911T235411Z | **606 s (minimum observed)** | 20260911T235904Z | 899 s |
| **23:59:24** | **20260911T235924Z** (re-signed) | 899 s | 20260911T235925Z | 900 s |
| 23:59:45 | 20260911T235924Z | 878 s | 20260911T235945Z | 899 s |

Reading:
- **Transaction file URLs are minted fresh on every request.** New `X-Goog-Date` and new signature on every call, always ~899 s of life. The docs are accurate here.
- **Statement `pdf_url` is served from a ~300 s signing cache.** Repeated `GET /statements/{id}` inside that window returns a byte-identical URL.
- **Residual life is therefore bounded between ~599 s and 899 s** (899 minus the ~300 s cache TTL). Observed minimum 606 s (10.1 min), observed maximum 899 s. A statement URL never arrives nearly-dead.

Consequences, stated precisely:
- Rho's claim *"valid for up to 15 minutes"* (`docs/docs_v1_statements.md:17`) is **accurate and conservative**: in practice you always get at least ~10 minutes.
- Rho's remedy *"If the link lapses, re-fetch the statement with `GET /statements/{id}` to obtain a fresh URL"* is **only conditionally true**. Re-fetching does not mint a URL on demand; it returns whatever the cache holds. Because the cache always rotates ~10 minutes before expiry, a genuinely lapsed URL will in practice have been replaced already, so the remedy usually works, but not because of the mechanism the docs describe. A client cannot force a re-sign.
- The earlier hypothesis that the cache holds until expiry is **wrong** and was ruled out: epoch 2 was replaced at 23:59:24 while valid until 00:09:10, nearly 10 minutes early.

**Cache key is the PDF object, not the statement.** In one list response the 20 statements carried only **3 distinct `X-Goog-Date` values**, matching exactly the 3 distinct object paths:

| Object | Statements | Distinct signing dates | Distinct signatures |
|---|---|---|---|
| `/41addf56a3d9ab46a2bfedc6.pdf` | 7 (all `treasury`): 572981, 539240, 514051, 490851, 475381, 469372, 462701 | 1 (`20260911T234909Z`) | 1 |
| `/e9c29858933afd7a8d42e1a7.pdf` | 12 (all `credit`): 200527, 186996, 179033, 174810, 172111, 169823, 167766, 165954, 164322, 163022, 161929, 161396 | 1 (`20260911T235047Z`) | 1 |
| `/4f7150d8341cae23c6ffa33a.pdf` | 1 (`account`): 439951 | 1 (`20260911T235046Z`) | 1 |

So a single list response can return URLs signed at three different instants with three different residual lifetimes, all still within the 599-899 s band. The sandbox backs all 20 statements with only 3 real PDFs, which also means per-statement PDF content is not statement-specific fixture data.

### 5.4 Are the URLs actually fetchable? Yes

| Test | Result |
|---|---|
| GET signed URL, no `Authorization` header | **200**, `Content-Type: application/pdf`, 769 bytes, body starts `%PDF-1.4` |
| CSV attachment (`repayment-details.csv`) | **200**, `text/csv`, 139 bytes, real content (see below) |
| Statement PDF | **200**, `application/pdf`, **37,465 bytes**, `%PDF-1.3` |
| Same URL fetched 3× | 200 / 200 / 200, 769 B each. **Not single-use** |
| `HEAD` on signed URL | **200** |
| `Range: bytes=0-9` | **206**, 10 bytes, `%PDF-1.4\n1` |
| Signature last hex char altered | **403** `SignatureDoesNotMatch`, body echoes the canonical `StringToSign` |
| Query string stripped (bare object path) | **403** `AccessDenied`. Bucket is private, no public read |
| `X-Goog-Expires` tampered 899 → 1 | **400** `ExpiredToken` |

Real CSV content retrieved, confirming sandbox files are non-empty representative documents as documented:

```csv
transaction_id,account_name,counterparty_name,amount,currency
019f0143-3ea0-7000-8000-000000000003,Credit Account,Cash (Checking),1750,USD
```

Notable response headers on the GCS download:

```
content-security-policy: frame-ancestors bank.rho.co app.rho.co signup.rho.co dashboard.rho.co
x-frame-options: SAMEORIGIN
cache-control: private, max-age=0
cf-cache-status: BYPASS
x-goog-storage-class: STANDARD
x-goog-hash: crc32c=gIoj2A==, md5=6/qObCKEUoLQVLAiXEd65Q==
```

The CSP `frame-ancestors` list leaks four Rho first-party app domains: `bank.rho.co`, `app.rho.co`, `signup.rho.co`, `dashboard.rho.co`. The file bucket sits behind Cloudflare with caching bypassed.

### 5.5 `GET /invoicing/invoices/{iid}/files/{fid}`: broken in sandbox

**Every documented-correct pairing returns 404.** Tested all 9 invoices that carry a `file_id`:

| Invoice | `file_id` | Status |
|---|---|---|
| `70000000-...-000000000001` | `50000000-...-000000000020` | 404 |
| `70000000-...-000000000002` | `50000000-...-000000000021` | 404 |
| `70000000-...-000000000003` | `50000000-...-000000000022` | 404 |
| `70000000-...-000000000004` | `50000000-...-000000000023` | 404 |
| `70000000-...-000000000005` | `50000000-...-000000000024` | 404 |
| `70000000-...-000000000007` | `50000000-...-000000000025` | 404 |
| `70000000-...-000000000008` | `50000000-...-000000000026` | 404 |
| `70000000-...-000000000010` | `50000000-...-000000000027` | 404 |
| `70000000-...-000000000011` | `50000000-...-000000000028` | 404 |

Identical body every time:

```json
{"type":"1303","title":"invoice file not found","status":404}
```

`content-type: application/problem+json`, `content-length: 62`.

This is precisely the call the docs instruct you to make: *"When an invoice has a PDF, `file_id` is present ... Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`."* The `file_id` field is populated on 9/12 invoices exactly as documented, but **no invoice PDF blob exists behind any of them**. Invoice PDF retrieval cannot be integration-tested against this sandbox at all. The endpoint routes correctly (a malformed `file_id` yields a 400, proving the handler runs), so this is a fixture-data gap rather than a missing route.

---

## 6. Error behaviour matrix

### 6.1 Valid-format but unknown ID → 404, `type: "1303"`

| Request | Status | Body |
|---|---|---|
| `/accounts/30000000-0000-4000-8000-999999999999` | 404 | `{"type":"1303","title":"account not found","status":404}` |
| `/accounts/00000000-0000-4000-8000-000000000000` | 404 | `{"type":"1303","title":"account not found","status":404}` |
| `/cards/20000000-0000-4000-8000-999999999999` | 404 | `{"type":"1303","title":"card not found","status":404}` |
| `/transactions/019f0554-0bf0-7000-8000-999999999999` | 404 | `{"type":"1303","title":"transaction not found","status":404}` |
| `/statements/999999` | 404 | `{"type":"1303","title":"statement not found","status":404}` |
| `/invoicing/customers/60000000-0000-4000-8000-999999999999` | 404 | `{"type":"1303","title":"customer not found","status":404}` |
| `/invoicing/invoices/70000000-0000-4000-8000-999999999999` | 404 | `{"type":"1303","title":"invoice not found","status":404}` |
| `/transactions/{real}/files/00000000-0000-4000-8000-000000000000` | 404 | `{"type":"1303","title":"transaction file not found","status":404}` |
| `/invoicing/invoices/{real}/files/00000000-0000-4000-8000-000000000000` | 404 | `{"type":"1303","title":"invoice file not found","status":404}` |

All 404s share `type: "1303"`. The resource is identified only by the human-readable `title`. There are **9 distinct titles but one `type` code**, so `type` is useless for programmatic discrimination and `title` (prose, unversioned) is the only signal. No `detail` field is ever present on a 404, despite the schema listing it.

### 6.2 Malformed ID → 400 with a different envelope

| Request | Status | Body |
|---|---|---|
| `/accounts/abc` | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| `/accounts/123` | 400 | `...detail":"invalid parameter: account_id"}` |
| `/accounts/30000000-0000-4000-8000` (truncated) | 400 | same |
| `/accounts/30000000-0000-4000-8000-0000000000021111` (too long) | 400 | same |
| `/accounts/3000000g-...` (non-hex char) | 400 | same |
| `/accounts/30000000%200000` (space) | 400 | same |
| `/accounts/1%20OR%201=1` | 400 | same |
| `/cards/abc` | 400 | `"detail":"invalid parameter: id"` |
| `/transactions/abc` | 400 | `"detail":"invalid parameter: id"` |
| `/invoicing/customers/abc` | 400 | `"detail":"invalid parameter: customer_id"` |
| `/invoicing/invoices/abc` | 400 | `"detail":"invalid parameter: invoice_id"` |
| `/transactions/{real}/files/abc` | 400 | `"detail":"invalid parameter: file_id"` |
| `/transactions/abc/files/{real}` | 400 | `"detail":"invalid parameter: transaction_id"` |
| `/invoicing/invoices/{real}/files/abc` | 400 | `"detail":"invalid parameter: file_id"` |
| **`/statements/abc`** | **404** | `{"type":"1303","title":"statement not found","status":404}` |
| **`/statements/-1`** | **404** | same |
| **`/statements/99999999999999999999`** | **404** | same |

Two observations:

1. **`/statements/{id}` performs no format validation**, because its ID is an opaque string rather than a UUID. Anything malformed falls through to a 404. So the 400-vs-404 contract is **not uniform across resources**: for five of six resources a malformed ID is a 400, for statements it is a 404.
2. **The `detail` string leaks the internal path-parameter names**, and they are inconsistent with each other: `account_id`, `customer_id`, `invoice_id`, `transaction_id`, `file_id`, but plain **`id`** for cards and transactions. That matches the OpenAPI docs, which declare `account_id` for accounts but bare `id` for cards, transactions and statements.

### 6.3 Mismatched pairing (real file under wrong parent)

| Request | Status | Body |
|---|---|---|
| real `file_id` `2c436c0c...` under a different real transaction `019f031b-...-0007` | 404 | `{"type":"1303","title":"transaction file not found","status":404}` |
| swapped: `019f0554-...-000a` + `8d073098...` (belongs to another txn) | 404 | same |
| real `file_id` under a transaction that has **no** attachments | 404 | same |
| invoice `file_id` `50000000-...-0027` under invoice `70000000-...-0002` | 404 | `{"type":"1303","title":"invoice file not found","status":404}` |
| invoice `file_id` under a **transaction** path | 404 | `{"type":"1303","title":"transaction file not found","status":404}` |
| transaction `file_id` under an **invoice** path | 404 | `{"type":"1303","title":"invoice file not found","status":404}` |

**Mismatched pairing is indistinguishable from an unknown file id**: byte-identical response. Positively: the parent-child relationship *is* enforced; a valid `file_id` does not leak across transactions. The handler does not reveal whether the file exists elsewhere. This is correct IDOR-resistant behaviour. It also means the invoice-file 404s in §5.5 cannot be distinguished from an authorisation failure by response alone.

### 6.4 Cross-type ID confusion

| Request | Status | Title |
|---|---|---|
| customer UUID at `/invoicing/invoices/{id}` | 404 | `invoice not found` |
| invoice UUID at `/invoicing/customers/{id}` | 404 | `customer not found` |
| account UUID at `/cards/{id}` | 404 | `card not found` |
| card UUID at `/accounts/{id}` | 404 | `account not found` |
| transaction UUID at `/accounts/{id}` | 404 | `account not found` |

Clean type isolation. No cross-namespace resolution.

### 6.5 UUID parsing is lenient

All of these resolve to the **same real account** and return 200:

| Form | Path | Result |
|---|---|---|
| canonical | `/accounts/30000000-0000-4000-8000-000000000002` | 200 |
| **no dashes (32 hex)** | `/accounts/30000000000040008000000000000002` | **200** |
| **brace-wrapped** | `/accounts/{30000000-0000-4000-8000-000000000002}` | **200** |
| **`urn:uuid:` prefix** | `/accounts/urn:uuid:30000000-0000-4000-8000-000000000002` | **200** |
| **uppercase hex** | `/transactions/019F0554-0BF0-7000-8000-00000000000A` | **200** |
| no dashes, on file endpoint | `/transactions/019f05540bf07000800000000000000a/files/2c436c0c5d8b4114aa2d8d7bd64d9b15` | **200** |
| no dashes + 1 extra char | `.../files/2c436c0c5d8b4114aa2d8d7bd64d9b15x` | 400 |

This is the exact accept-set of Go's `github.com/google/uuid` `Parse()`, which accepts canonical, `urn:uuid:` prefixed, brace-wrapped and raw-hex forms. Strong signal the API is written in Go. Practical consequence: **the same logical resource has at least 5 distinct URL spellings**, all returning 200 with an identical body whose `id` is always normalised to canonical lowercase-dashed form. Anything keying a cache on the request URL will store up to 5 copies.

### 6.6 Router behaviour

| Request | Status | Body | Notes |
|---|---|---|---|
| `/accounts/` (trailing slash) | 404 | `404 page not found` | **plain text**, not problem+json |
| `//accounts/{id}` (double slash) | 404 | `404 page not found` | |
| `/accounts/{id}/` | 404 | `404 page not found` | strict, no redirect |
| `/accounts/{id}/transactions` | 404 | `404 page not found` | no sub-resources |
| `/transactions/{id}/files` (collection index) | 404 | `404 page not found` | **no file-listing endpoint** |
| `/nope` | 404 | `404 page not found` | |
| `/ACCOUNTS/{id}`, `/Accounts/{id}` | 404 | `404 page not found` | **paths are case-sensitive** |
| `/transactions/{id}/FILES/{fid}` | 404 | `404 page not found` | |
| `/accounts/..%2F..%2Faccounts` | **301** | `<a href="/api/accounts">Moved Permanently</a>` | path normalisation; reveals mount point `/api` |
| `https://.../api/v2/accounts` | 404 | `default backend - 404` | **different 404 text**: load balancer, not the app |
| `https://.../api/accounts` | 404 | `default backend - 404` | |
| `https://.../v1/accounts` | 404 | `default backend - 404` | |

Three distinct 404 surfaces, useful for locating where a request died:
1. `default backend - 404` (plain text): Google Cloud load balancer; the path never reached the Rho app. Only `/api/v1/*` is routed.
2. `404 page not found` (plain text): Go HTTP router; the app was reached but no route matched.
3. `{"type":"1303",...}` (problem+json): the handler ran and the resource was absent.

Unknown routes are **not** returned as problem+json, so a client parsing every error as JSON will break on route typos.

### 6.7 Content negotiation

`Accept: application/xml` and `Accept: nonsense/x` both return **200 application/json**. No negotiation; unknown query params (`?foo=bar&limit=1` on a single GET) are silently ignored.

### 6.8 `account_id` query parameter on `GET /transactions/{id}`

Documented as an optional query param with the bare description *"Account ID for the transaction"*. It is not a hint, it is an **assertion filter**:

| Request | Status |
|---|---|
| `?account_id=30000000-...-000000000009` (the transaction's real account) | 200, full body |
| `?account_id=30000000-...-000000000002` (a different real account) | **404** `transaction not found` |
| `?account_id=abc` | 400 `invalid parameter: account_id` |

Passing the wrong `account_id` makes an existing transaction vanish. The docs do not say this. A client that passes a stale or guessed `account_id` will see spurious 404s for transactions that exist.

---

## 7. Write methods: the read-only claim confirmed

### 7.1 Result matrix

Sent with `Content-Type: application/json` and body `{"x":1}`:

| Method | `/accounts` | `/accounts/{id}` | `/transactions/{id}` | `/invoicing/invoices/{id}` | `/transactions/{id}/files/{fid}` | `/invoicing/customers` |
|---|---|---|---|---|---|---|
| POST | 405 | 405 | 405 | 405 | 405 | 405 |
| PUT | 405 | 405 | 405 | 405 | 405 | n/a |
| PATCH | 405 | 405 | 405 | 405 | 405 | n/a |
| DELETE | 405 | 405 | 405 | 405 | 405 | n/a |

**Every write method on every path returns `405 Method Not Allowed`.** The read-only claim holds. Exact response:

```
HTTP/2 405
date: Fri, 11 Sep 2026 23:47:48 GMT
content-length: 0
allow: GET
via: 1.1 google
cf-cache-status: DYNAMIC
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
server: cloudflare
```

- **Body is empty (0 bytes).** Not problem+json. A client that unconditionally parses the error body as JSON will throw on a 405.
- **`Allow: GET`** on every path, including collections. No path advertises any write verb, so there is no hidden write surface reachable by verb probing.

### 7.2 Method rejection precedes authentication

| Method | Token | Status |
|---|---|---|
| POST / PUT / PATCH / DELETE | `Bearer sandbox` (valid) | 405 |
| POST / PUT / PATCH / DELETE | `Bearer WRONGTOKEN` | **405** |
| POST / PUT / PATCH / DELETE | **no header at all** | **405** |
| GET | no header | **401** `{"type":"2","title":"Unauthenticated","status":401}` |

The 405 is emitted by the router before the auth middleware. An unauthenticated caller can therefore enumerate which methods each path supports. Low severity (the answer is always `GET`), but it means 405 is not evidence that a token was accepted.

Also: `POST` to a **nonexistent** route returns `404 page not found`, not 405, so routing precedes method checking, which precedes auth.

### 7.3 Related auth observation

**`GET` with an arbitrary bearer token succeeds.** `Authorization: Bearer WRONGTOKEN` on `/accounts` returned **200** with the complete 14-account payload including balances. Only the *absence* of the header produces 401. The sandbox validates the presence of a bearer token, not its value, so the literal token `sandbox` in the docs is a convention rather than a credential. Any sandbox data is effectively public to anyone who knows the hostname.

### 7.4 Edge cases

- `POST` **without** a `Content-Length` header returns **`411 Length Required`** as an HTML page from the Google front end, before reaching Rho. Only with a body does the Rho 405 surface.
- `HEAD /accounts` → **405**, `Allow: GET`. HEAD is not supported even though GET is, which is unusual and will break clients that probe with HEAD.
- `OPTIONS /accounts` → **405**, `Allow: GET`, empty body. **No CORS preflight support** and no `Access-Control-Allow-*` headers anywhere. The API is not callable from a browser.
- `TRACE /accounts` → **405** with an **nginx-style HTML body from Cloudflare** (`<center><h1>405 Not Allowed</h1></center><hr><center>cloudflare</center>`), blocked at the edge rather than by Rho.

---

## 8. Response headers

Every API response (200, 400, 404, 405) carries exactly:

```
content-type: application/json | application/problem+json   (absent on 405)
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: <id>-EWR
```

Conspicuously **absent**:
- No `X-RateLimit-Limit` / `-Remaining` / `-Reset`, despite documented limits of ~60 req/min per token and ~600 req/min per source IP. Clients cannot see how close they are; they can only react to a 429. The docs promise a `Retry-After` on 429 but nothing advertises headroom beforehand.
- No `X-Request-Id` or correlation header, so there is no identifier to quote to support.
- No `ETag` or `Last-Modified`, so no conditional requests. Combined with `cf-cache-status: DYNAMIC` and no `Cache-Control`, every read is a full transfer.
- No `Access-Control-Allow-Origin`.
- No API version header. Version lives only in the URL path.

`cf-ray` suffix `EWR` (Newark) on every response; Cloudflare in front of a Google Cloud load balancer (`via: 1.1 google`).

---

## 9. Practical guidance for an integrator

1. **Never loop single GETs to enrich list rows.** Proven zero payload gain across all 133 sandbox resources. At ~60 req/min per token this is the fastest way to hit the rate limit for no benefit.
2. **Statement `pdf_url` always has at least ~10 minutes of life, but you cannot force a fresh one.** Re-fetching the statement inside the ~300 s signing cache returns the identical URL. Do not build a retry loop that assumes re-fetching mints a new URL; on `400 ExpiredToken`, back off past the cache TTL rather than retrying tightly.
3. **Parse the signed URL to know its deadline.** `X-Goog-Date + X-Goog-Expires` is the exact expiry; both are readable from the URL without a network call. Use this to decide whether a URL is worth attempting, instead of discovering expiry from a failed download.
4. **Transaction attachments are safe to fetch on demand**: always a full 899 s window.
5. **Do not build against invoice PDFs using this sandbox.** The endpoint 404s universally.
6. **Handle three different error body shapes**: problem+json with `detail` (400), problem+json without `detail` (401/404), empty body (405), plus plain-text `404 page not found` for bad routes and HTML for edge-level 411/405. Never assume the error body is JSON.
7. **Do not discriminate errors on `type`.** All 404s use `"1303"`; 401 uses `"2"`. Use HTTP status plus, reluctantly, the prose `title`.
8. **Normalise resource IDs yourself.** The API accepts 5 UUID spellings and normalises only in the response body, so URL-keyed caches will fragment.
9. **Do not pass `account_id` to `GET /transactions/{id}`** unless certain it is correct; a wrong value converts a 200 into a 404.
10. **Statement IDs are opaque strings, not UUIDs.** Do not validate them as UUIDs client-side, and expect 404 rather than 400 for junk.

---

## 10. Evidence index

All under `.../scratchpad/rho/sandbox/probe-resources/`:

| File(s) | Contents |
|---|---|
| `list_*.body`, `list_*.headers` | fresh baseline list responses (6 resources) |
| `get_*.body` | representative single-resource GETs |
| `sw_{accounts,cards,customers,invoices,statements}_list.json` | sweep list snapshots |
| `sw_*_get.ndjson` | every single-GET response, one JSON per line |
| `all_txns.ndjson`, `pg_1..4.json` | all 72 transactions, paginated |
| `sweep_txn_get.ndjson` | all 72 transaction single-GETs |
| `file_txn_*.body`, `file_inv_*.body` | file endpoint responses incl. the 404s |
| `err_*.body`, `err_*.headers` | unknown-ID and mismatched-pairing matrix |
| `mal_*.body` | malformed-ID matrix |
| `len_*.body` | UUID leniency, router, query-param matrix |
| `w_*.body`, `w405.headers`, `m_{HEAD,OPTIONS,TRACE}.*` | write-method and method-support probes |
| `dl_txn_ok.pdf`, `dl_txn_csv.csv`, `stmt_pdf2.pdf` | actually downloaded files (769 B PDF, 139 B CSV, 37,465 B statement PDF) |
| `sig_bad.body`, `sig_exp1.body`, `sig_bare.body`, `sig_range.bin` | signed-URL tampering, expiry, range results |
| `signed_url_sample.txt` | one complete signed URL verbatim |
| `poll.log` | timed signed-URL cache observations |
| `cust_default.json`, `cust_incl.json` | `include_deleted` comparison |
| `probe.sh`, `p2.sh`, `p3.sh`, `err.sh`, `mal.sh`, `len.sh`, `write*.sh`, `sig.sh`, `sweep*.sh`, `page.sh`, `del.sh`, `hidden.sh`, `misc.sh`, `poll.sh`, `diff1.sh` | reproducible probe scripts |
