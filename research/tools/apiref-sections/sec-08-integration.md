## 8. Building on it

Everything below assumes the contract established earlier in this document: fourteen `GET` operations, six list endpoints, opaque-in-intent cursors, a documented budget of roughly 60 requests per minute per token, and no push channel of any kind. This section is about the consequences for code you have to run in production.

The shape of the problem, stated once: **you are building a read-only mirror of somebody else's ledger, by polling, with no change feed, no totals, no conditional requests, and no way to be notified that anything happened.** Every design decision here follows from that.

### 8.1 The constraints that actually drive the design

| Constraint | Evidence | What it forces |
| --- | --- | --- |
| No webhooks, no events, no subscriptions | `GET /webhooks`, `/events`, `/subscriptions` all return `404 page not found` (plain text, Go router). No such concept appears anywhere in the docs corpus. | Poll. Your data freshness floor is your poll interval. |
| No `updated_at` on the banking resources | Accounts, cards, transactions and statements carry no `created_at` or `updated_at` at all. Only `invoicing/customers` and `invoicing/invoices` do, and neither is filterable. | You cannot ask "what changed". You must re-read windows and diff client-side. |
| No `updated_after` filter anywhere | Transactions expose `initiated_after/before` and `posted_after/before` only. No guide offers a change-based filter on any resource, and nothing in the docs acknowledges the gap. | Your watermark has to be a business timestamp, which is not monotonic with respect to change. |
| No `ETag`, `Last-Modified`, `Cache-Control` | Observed: `If-None-Match: *` and `If-Modified-Since` in both directions all return a full `200` with the complete body. `cf-cache-status: DYNAMIC` on 249 of 249 API responses. | There is no cheap "has anything changed" probe. Every poll pays full payload cost. |
| `HEAD` returns `405 allow: GET` | Observed: `curl -I https://rhoapi-sandbox.rho.co/api/v1/accounts` returns `405`. | Liveness checks and existence probes must be real `GET`s. |
| No `total_count`, no `has_more`, no `Link` header | The `page` object has exactly one field, `next_page_token`. | You cannot size a result set without draining it, and you cannot show "1-20 of 347". |
| Five of six list endpoints use an offset cursor | Decoded tokens: `{"v":1,"f":"…","t":base64("offset:20")}` on cards, transactions, statements, invoicing customers and invoicing invoices. Only `/accounts` carries a keyset payload (`{"last_id":…,"sort_by":"account_name","order":"asc"}`). | A long walk over live data can skip or duplicate rows. You need a dedupe key and a periodic full sweep. |
| ~60 req/min per token, ~600 req/min per source IP | Documented in `docs/v1/rate-limits`. Not enforced in sandbox (observed: 150 requests on one token in a 57-second window, zero `429`; 68.9 req/s instantaneous, zero `429`). | Build to the documented budget, not the sandbox's tolerance. The per-IP pool is shared across all your tokens. |
| Read-only | All 14 operations are `GET`. Every write method on every path returns `405` with `allow: GET`, and that `405` is emitted **before** authentication (observed: `POST /accounts` with no `Authorization` header returns `405`, not `401`). All five OAuth scopes end in `:read`. | Nothing you build can move money, issue a card, or annotate a record. |

> **Divergence:** The pagination guide states, unqualified: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." Five of the six list endpoints return a bare absolute offset inside the cursor, which cannot deliver that guarantee: an insert positioned before the current offset shifts every subsequent row. Only `/accounts` uses a keyset cursor that structurally can. The sandbox dataset is static so the failure cannot be forced there, but the mechanism is dispositive. Treat the anti-skip and anti-duplicate promise as false for `/transactions`, `/statements`, `/cards`, `/invoicing/customers` and `/invoicing/invoices`. See also the Pagination section.

### 8.2 Incremental sync

#### 8.2.1 Why the obvious design is wrong

The obvious design is: keep a watermark, ask for everything after it, advance the watermark. That design is wrong here for four independent reasons, and each one alone is enough to corrupt your mirror.

**1. Rows mutate in place.** A transaction is created and then changes. `status` moves through `pending`, `settled`, `failed` and `awaiting_approval`. `posted_at` appears later. The docs are explicit that the money can change too: "The amount can shift between an initial card authorization and final clearing." There is no authorized-amount and settled-amount pair in the schema; `amount` is described as "Settled amount in account currency" even while `status` is `pending`. `note` is user-editable in the Rho web app at any time. None of these mutations moves `initiated_at`, so none of them is visible to a watermark on `initiated_at`.

**2. There is no state machine to lean on.** Quoted in full from the Transactions guide, because it is unusually candid: "`v1` does **not** guarantee that a failed transaction has an empty `posted_at`, so read the field as nullable whatever the status. Nor does `v1` guarantee a **transition order**, so reconcile on the `status` and timestamps a response actually carries rather than on an assumed progression." You may not assume `pending → settled` is terminal, and you may not assume `settled` never changes again.

**3. `posted_at` arrives arbitrarily late.** Measured across the 71 sandbox transactions that carry one: median lag is 0 seconds, 47 of 71 are exactly zero, p90 is 1 day, and the maximum is **18.23 days** (a settled `check_payment`). A row initiated on the 1st can post on the 19th. A `posted_after`-based sync window narrower than that silently drops it.

```bash
# The row with the longest observed lag
curl -s -H "Authorization: Bearer sandbox" \
  'https://rhoapi-sandbox.rho.co/api/v1/transactions?transaction_type=check_payment&page_size=100' \
  | python3 -c 'import sys,json,datetime as d
f="%Y-%m-%dT%H:%M:%SZ"
for t in json.load(sys.stdin)["transactions"]:
    if "posted_at" in t:
        lag=(d.datetime.strptime(t["posted_at"],f)-d.datetime.strptime(t["initiated_at"],f))
        print(t["id"], t["status"], t["initiated_at"], t["posted_at"], lag)'
```

**4. You cannot sync on `posted_at` instead.** It is tempting, because `posted_at` is the accounting-relevant timestamp and Rho's own daily-reconciliation recipe uses it. But any `posted_after` or `posted_before` bound excludes every row that has no `posted_at` at all, which is exactly the set of rows you most need to track.

```bash
# 72 transactions exist; a posted_at bound sees 71.
curl -s -H "Authorization: Bearer sandbox" \
  'https://rhoapi-sandbox.rho.co/api/v1/transactions?posted_after=2000-01-01&page_size=100' \
  | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["transactions"]))'
# -> 71
```

> **Divergence:** `api/transactions_listtransactions.md` says `posted_at` is "Null while status is pending". Observed in the sandbox: both `pending` rows carry a non-null `posted_at`, and the only row without one is the single `awaiting_approval` record (`019d3e86-4482-7000-8000-000000000048`). The operative rule is "absent while awaiting approval", not "absent while pending". Worse, the field is **omitted**, never `null`, so a client written to the literal doc wording (`if txn.posted_at is None`) sees a `KeyError` or an `undefined`, not a null. `docs/v1/transactions` hedges in the opposite direction ("not coupled to `status`"), so Rho's two pages disagree with each other and the reference page disagrees with the data. Verify: `GET /transactions?status=pending&page_size=100` returns two rows, both with `posted_at`.

#### 8.2.2 The filters you can actually sync on

Only a subset of the documented query surface is usable as a sync primitive. This is the working set, per endpoint.

| Endpoint | Usable sync filter | Accepted format | Boundary semantics | Notes |
| --- | --- | --- | --- | --- |
| `/transactions` | `initiated_after`, `initiated_before` | `2026-01-01` or `2026-01-01T00:00:00Z` or `…+00:00` or `…000Z` | `after` inclusive, `before` **exclusive** | The only monotonic-ish key. Does not move when a row changes. |
| `/transactions` | `posted_after`, `posted_before` | same | `after` inclusive, `before` **exclusive** | Excludes rows with no `posted_at`. Good for closing a book, useless for change detection. |
| `/statements` | `period_end_after/before`, `period_start_after/before` | **date-only**, `2026-01-01`. A timestamp form returns `400`. | `after` inclusive, `before` **exclusive** | `available_at` lags `period_end` by 1 to 8 days observed, so re-scan a trailing window. |
| `/invoicing/invoices` | `date_after/before`, `due_date_after/before` | **date-only**. Timestamp forms return `400`. | **both inclusive** | These are issue and due dates. Neither moves when an invoice's `status` changes. |
| `/invoicing/customers` | none | n/a | n/a | No date filter at all. `sort_by=created_at` is the only legal sort value; everything else is a `400`. |
| `/accounts` | none | n/a | n/a | No filters of any kind. `account_type=checking` is silently ignored and returns all rows. |
| `/cards` | none | n/a | n/a | `user_id[]`, `type[]`, `status[]` only. No dates. |

Boundary inclusivity is not uniform, and the difference is real:

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
count() { python3 -c 'import sys,json;d=json.load(sys.stdin);print(len(d[sys.argv[1]]))' "$1"; }

# transactions: after is INCLUSIVE, before is EXCLUSIVE.
# The corpus runs from 2023-05-31T07:29:00Z to 2026-06-26T19:07:02Z.
curl -s -H "$H" "$B/transactions?initiated_before=2023-05-31T07:29:00Z&page_size=100" | count transactions  # 0
curl -s -H "$H" "$B/transactions?initiated_after=2026-06-26T19:07:02Z&page_size=100"  | count transactions  # 1

# invoices: BOTH bounds inclusive. Same day on both sides still returns rows.
curl -s -H "$H" "$B/invoicing/invoices?date_after=2026-05-01&date_before=2026-05-01&page_size=100" | count invoices  # 2
```

Two traps will destroy a sync job silently, and neither is documented.

**The empty-value trap.** An empty value on any `*_before` parameter coerces to the zero time `0001-01-01T00:00:00Z`; `field < zero` is universally false, so you get `200` with an empty array. An empty `*_after` is a no-op and returns everything. A templated URL with an undefined variable therefore reports "no activity" rather than failing.

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
curl -s -H "$H" "$B/transactions?posted_before=&page_size=100"
# {"page":{"next_page_token":null},"transactions":[]}
```

Build query strings conditionally and refuse to emit an empty value. The reference client below raises on this rather than sending it.

**The unvalidated-enum trap.** `/cards` validates `type` and `status` and returns `400` on a bad value. `/transactions`, `/statements` and `/invoicing/invoices` do not: they accept any string and return `200` with zero rows. `status=Settled`, `status=posted`, `account_type=treasury` and `status=canceled` (the invoice enum is `cancelled`, two Ls) all look like working queries that found nothing.

> **Divergence:** `docs/v1/pagination` says only that "Values outside the allowed range return `400 Bad Request`", and every filter is documented with an enum. In practice enum validation is present on `/accounts` and `/invoicing/customers` (`sort_by`, `order`), present on `/cards` (`type`, `status`), and entirely absent on `/transactions`, `/statements` and `/invoicing/invoices`. Validate enums client-side; the server will not tell you. See the Filters section for the full per-endpoint matrix.

Corollary for operations: **`200 []` is ambiguous** between "no matching data" and "your filter was silently dropped". Whenever a filtered query returns empty, assert against an unfiltered control query before concluding anything.

#### 8.2.3 The design: three lanes

Because no single query answers "what changed", correct sync is three overlapping passes with different cadences. Each one covers a failure mode the others miss.

| Lane | Query | Catches | Misses | Cost per run |
| --- | --- | --- | --- | --- |
| **A. New rows** | `initiated_after = watermark - skew`, walked to `null` | Anything newly initiated since last poll | Mutations to older rows; backdated inserts | `ceil(new/100)`, normally 1 request |
| **B. Open-row re-read** | `GET /transactions/{id}` for every row you last saw as `pending`, `awaiting_approval`, or missing `posted_at` | `pending → settled`, amount revision, late `posted_at` | Changes to rows you never saw as open | 1 request per open row |
| **C. Trailing window** | `initiated_after = now - 35d`, walked to `null` | Backdated inserts, any mutation inside the window, offset-cursor skips inside the window | Anything older than the window | `ceil(window_rows/100)` |
| **D. Full sweep** | unfiltered walk to `null` | Everything, including a row an offset cursor skipped months ago | Nothing, but it is expensive | `ceil(total/100)` |

Lane C's 35-day width is not arbitrary: it is roughly double the longest `posted_at` lag observed in the corpus (18.23 days), with headroom. Widen it if your own production data shows longer tails, and measure that directly rather than trusting this number.

**Do not pick an `initiated_after` floor for lane D.** The sandbox corpus spans 2023-05-31 to 2026-06-26, three years, and a naive "last 3 years" horizon drops the two oldest rows. Walk `/transactions` with no date filter at all. If that walk is too expensive, partition it by `account_id` (which is a real, honored filter) rather than by date.

**The watermark must be a `initiated_at` value you actually observed, not your wall clock.** There is no server-supplied cursor, no `created_at`, and no guarantee that a row initiated at T becomes visible at T. Advancing to `max(initiated_at)` and re-scanning from `max - skew` on the next run is correct only because lanes B, C and D exist behind it.

**Every page of a walk must send the byte-identical query string.** The cursor is bound to a fingerprint of the literal filter spelling, not its meaning. `order=asc` then `order=ASC` returns the same rows but invalidates the token. `status=settled` then `status=settled&status=settled` likewise. Changing `page_size` mid-walk is safe (`page_size` is deliberately excluded from the fingerprint), but there is no reason to.

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
# The token survives a changed page_size and dies on a changed filter.
T=$(curl -s -H "$H" "$B/transactions?page_size=5" | python3 -c 'import sys,json;print(json.load(sys.stdin)["page"]["next_page_token"])')
curl -s -o /dev/null -w '%{http_code}\n' -H "$H" "$B/transactions?page_size=37&page_token=$T"          # 200
curl -s                              -H "$H" "$B/transactions?page_size=5&page_token=$T&status=settled"
# {"type":"1317","title":"page_token must be a valid cursor","status":400}
```

Handle that `400` mid-walk by restarting the walk from page 1, not by aborting. Your dedupe key makes the repeat harmless.

#### 8.2.4 Cadence against the budget

The documented budget is approximately 60 requests per minute per token and approximately 600 per minute per source IP, with the explicit pacing advice "pace traffic steadily below one request per second". Read literally, your sustained ceiling is under 60/min, so size against **0.9 req/s = 54 req/min = 77,760 req/day**.

Worked example: a business posting 300 transactions per day, with roughly 30 rows open at any moment, and 330,000 rows of history.

| Lane | Cadence | Requests per run | Requests per day | Wall time per run at 0.9 rps |
| --- | --- | --- | --- | --- |
| A | every 5 min | 1 | 288 | 1 s |
| B | every 5 min | 30 | 8,640 | 33 s |
| C | hourly | `ceil(35 x 300/100)` = 105 | 2,520 | 117 s |
| D | weekly | `ceil(330000/100)` = 3,300 | 471 amortised | 61 min |
| **Total** | | | **~11,900** | **15% of budget** |

Backfill arithmetic, at `page_size=100` and 0.9 req/s:

| Rows | Requests | Elapsed |
| --- | --- | --- |
| 10,000 | 100 | 1.9 min |
| 100,000 | 1,000 | 18.5 min |
| 1,000,000 | 10,000 | 3.1 h |

A million-row backfill consumes a token's entire budget for three hours. Run backfills on a **separate API Access Token** so steady-state sync is not starved. Note that separate tokens do not buy you separate IP budgets: the ~600 req/min per-source-IP ceiling is shared across every token behind that egress address, including other teams' integrations.

Two transport facts change these numbers materially, both observed:

- **Always send `Accept-Encoding: gzip` explicitly.** Only gzip is served. Brotli, zstd, deflate and the wildcard `*` are all declined and return the full payload. On a 40,768-byte transactions page, gzip cuts the wire to about 5.6 KB, a 7.2x saving.
- **Reuse connections, but do not over-multiplex one.** Keep-alive halves effective latency (cold total p50 206 ms vs warm server TTFB p50 112 ms). Multiplexing 50 streams onto a single HTTP/2 connection made per-request p50 13x worse (1,504 ms) for only 31 req/s aggregate. A small pool of connections with modest per-connection concurrency beats the usual HTTP/2 advice here.

Budget approximately 90 to 145 ms of server time per call from a US East client, plus 70 to 100 ms of connect and handshake when cold, with a rare ~1 s tail. Payload size is not a latency driver.

#### 8.2.5 Syncing the other resources

| Resource | Strategy | Why |
| --- | --- | --- |
| `/accounts` | Full walk every poll (14 rows in sandbox; small everywhere). No filters exist. | Balances are the only volatile field and there is no way to ask for changed ones. |
| `/cards` | Full walk every poll. | No date filters. Spend windows (`spend_period_start/end`, `current_spend`) are recomputed per request against the real clock, so cards look "changed" constantly. |
| `/statements` | `period_end_after = last_period_end - 60d`, dedupe on `id`. | `available_at` lags `period_end` by 1 to 8 days observed, so a statement appears after its period closes. |
| `/invoicing/invoices` | Full walk every poll. | `date`/`due_date` filters do not move when `status` or `accounting_sync_status` changes, so they are useless for change detection. No `customer_id` filter either. |
| `/invoicing/customers` | Full walk every poll, with `include_deleted=true` if you need soft-deleted records. | No date filter of any kind. |

**Exclude signed URLs from your change fingerprint.** `statements[].pdf_url` is a Google Cloud Storage V4 signed URL that is re-signed roughly every 300 seconds. If `pdf_url` is part of what you diff, every statement will look changed on most polls. The same applies to `download_url` from the file endpoints, although those never appear on a resource record (transaction responses carry only `attachments[].file_id` and `file_name`, never a URL).

> **Divergence:** `api/statements_getstatement.md` says "If the link lapses, re-fetch the statement with `GET /statements/{id}` to obtain a fresh URL." Observed: `pdf_url` is served from a server-side signing cache keyed on the **PDF blob**, not the statement, with a TTL of about 300 s (re-sign intervals of 302 s and 313 s measured across three epochs). Re-fetching inside that window returns a byte-identical URL. You cannot force a re-sign. In practice the cache rotates roughly 10 minutes before the 899-second expiry, so a genuinely dead URL has usually already been replaced, but not by the mechanism the docs describe. The observed residual life band is 599 to 899 seconds. Transaction file `download_url` values, by contrast, are minted fresh on every request with a full 899 s window. Parse `X-Goog-Date + X-Goog-Expires` out of the URL to know its deadline without a network call.

### 8.3 Idempotency and reconciliation

#### 8.3.1 The primary key is `(id, account_id)`, never `id`

This is the single most important storage decision, and Rho states it plainly in the Transactions guide: "Do not assume `id` is unique per row, though: the entries of a single money movement can share an `id`, so a warehouse keyed on `id` alone **silently drops a leg**. Either key on `id` together with the fields that distinguish entries of the same movement, such as `account_id`, or group on `money_movement_id` and treat the movement as your unit."

The existence of an optional `account_id` query parameter on `GET /transactions/{id}` is the corroborating evidence: the endpoint would not need a disambiguator if `id` were unique.

> **Divergence:** The sandbox cannot exercise the collision. All 72 transaction ids are distinct, `(id, account_id)` yields the same 72 distinct keys, and the seven two-leg money movements all carry **different** ids on each leg (for example movement `…000000000002` has legs `019f0143-3ea0-…000002` and `…000003`). So the documented hazard is real per the contract and untestable per the fixtures. Key on `(id, account_id)` anyway. Additionally, the transaction-file reference page states "A transaction `id` identifies one transaction", directly contradicting the same product's `id` definition, and `GET /transactions/{id}/files/{file_id}` has no `account_id` disambiguator at all, so if ids ever do collide the file lookup has no way to say which leg it means.

#### 8.3.2 Money movements, not transactions, are the accounting unit

65 distinct `money_movement_id` values cover the 72 sandbox transactions. Seven movements have exactly two legs, and in every one of them **the two legs sum to zero**: an internal transfer of 123,987 minor units appears as `-123987` on Cash (Checking) and `+123987` on Reserve Checking. A credit repayment of 1,658,253 appears as `-1658253` on checking and `+1658253` on the credit account.

If you post both legs to a general ledger as independent events, you double-count every internal transfer and every credit repayment. Group on `money_movement_id` and decide once, per movement, what the accounting event is.

Leg order within a movement carries no meaning. Movements `…21` and `…27` are both `internal_transfer` between the same two accounts with **opposite polarity** in the leg array. Only the per-leg `account_id` and sign are load-bearing.

There is **no `money_movement_id` filter** on `/transactions`, despite the docs telling you to "group on it to treat the entries of one movement as a unit". You cannot fetch the sibling legs of a movement by its id. You must page a date window wide enough to contain all legs and group client-side. Leg timestamps within a movement were identical to the millisecond in 5 of 7 sandbox cases and differed by 1 ms in the other 2, so a window of seconds is sufficient in practice, but nothing guarantees the legs settle together. There is no sandbox example of a movement whose legs have different statuses, so half-settled transfers are untested surface.

#### 8.3.3 What can change under you, and what cannot

| Field | Changes after first sight? | Handling |
| --- | --- | --- |
| `id`, `money_movement_id`, `account_id`, `account_type`, `initiated_at`, `transaction_type` | No (assumed stable; the docs call `id` "stable across re-fetches") | Safe to key and partition on. |
| `status` | Yes, in any direction; no transition order guaranteed | Store current value plus a history row. Never assume terminality. |
| `posted_at` | Yes, appears late; up to 18.23 days after `initiated_at` observed | Nullable and **omitted, not null**, when unset. |
| `amount.amount` | Yes, documented: "can shift between an initial card authorization and final clearing" | Store the current value plus the prior one. Do not post to a GL until the row is `settled` unless you are prepared to reverse. |
| `note` | Yes, user-editable in the Rho app | Exclude from accounting logic, include in your change fingerprint if you surface it. |
| `memo` | Documented as bank-supplied and read-only | Treat as stable, but see the divergence below. |
| `attachments[]` | Yes, new attachments can appear | `(transaction_id, file_id)` is the key; `file_id` is not unique per transaction. |
| `account_name`, `card_name`, `user_full_name` | Denormalized copies; can drift from the source | Do not join on them. `account_name` is not unique: "Cash (Checking)" appears twice, "Credit Account" four times. |

> **Divergence:** `docs/v1/transactions` distinguishes `memo` ("supplied by a bank or payment provider", not user-editable) from `note` ("a user or system annotation", editable). Observed: `memo` and `note` are present or absent strictly together (39 of 72 have both, 33 have neither) and are **byte-identical on 37 of the 39**. The only two that differ are failed ACH rows, where `note` is `memo` plus `", Error: Invalid receiving routing number."` The sandbox effectively models them as one field, so you cannot use it to test code that depends on the distinction.

**Rows never disappear.** Failed transactions "remain queryable for audit purposes", and canceled and expired cards stay in the unfiltered card list "so their stable IDs can still be joined to historical transactions". So a row vanishing from your sync is a bug in your sync, not a delete, with one exception: an offset cursor can skip a row mid-walk while the underlying data shifts. That is precisely what the periodic full sweep is for. Never implement "row absent from this window, therefore deleted".

#### 8.3.4 Reconciling to an accounting system

The mechanics that make this workable, and the ones that do not.

**What works.** The idempotent-ingestion pattern Rho publishes is sound: "Re-fetching a day's window returns the same `id` values, so ingestion can be made naturally idempotent." A closed accounting day is a clean half-open interval:

```bash
curl -s -H "Authorization: Bearer $RHO_API_TOKEN" \
  'https://rhoapi.rho.co/api/v1/transactions?status=settled&posted_after=2026-05-21T00:00:00Z&posted_before=2026-05-22T00:00:00Z&page_size=100'
```

`posted_after` is inclusive and `posted_before` is exclusive, so consecutive days tile without overlap or gap. Pin the day boundaries in the timezone your books close in, converted to UTC, and record which timezone you used: the API takes and returns `Z` timestamps exclusively, with no sub-second component and no non-`Z` offset anywhere in the corpus.

**What does not work: balance reconciliation.** `accounts[].balance.amount` is a standalone figure that does not reconcile to the transaction list. Summing settled transactions per account reproduces the balance on only 4 of 14 sandbox accounts, and all four are the ones where both sides are zero. The sandbox transaction list is a curated sample, not a complete ledger, and it does not pretend otherwise. **Do not write a balance-equals-sum-of-transactions assertion and test it against the sandbox**; you will either conclude the API is broken or, worse, tune your logic to match a fixture artifact. Test that assertion against production or not at all.

There is also no `available_balance`, `credit_limit`, `posted_balance` or `pending_balance` on an account. An account is four to six fields: `id`, `account_name`, `account_type`, `balance`, plus `account_number_last_4` and `routing_number_last_4` on deposit accounts only. All four sandbox credit accounts and both rewards accounts report `balance.amount = 0`, so you never see what a carried credit balance looks like on `/accounts` even though credit statements clearly carry non-zero closing balances.

**What does not work: statement-to-transaction reconciliation.** There is no link from a statement to the transactions it covers, in either direction. Reconciling a statement means doing the account and date-range filtering yourself, against a `period_start`/`period_end` pair that is inclusive on both ends, and accepting that the arithmetic may not close because the two surfaces use opposite sign conventions (see 8.4.2).

**Invoicing is almost entirely disconnected from the ledger.** The only join between the Invoicing product and the banking ledger is `invoices[].payments[].transaction_id`, and it is populated **only** for payments with `type: "received_in_account"`. In the sandbox that is 2 of 7 payments; the other 5 are `type: "external"` with a null `transaction_id` and a non-null `external_method`. There is no `customer_id` filter on `/invoicing/invoices` and no `accounting_sync_status` filter, so you cannot ask "which invoices failed to sync" and you cannot list one customer's invoices; both require a full walk plus client-side filtering.

> **Divergence:** `invoices[].activities[].user_id` uses the `40000000-` prefix, which everywhere else in the corpus means a **money movement id**. All three such ids fail to resolve against the 12 banking user ids (which use the `10000000-` prefix). Measured: 3 references, 0 resolve, 3 dangling. The Invoicing product's actor identities and the banking product's user identities are not in the same namespace. You cannot join an invoice activity to a cardholder or a transaction initiator. Nothing in the docs mentions this either way.

**Do not enrich list rows with single GETs.** Verified exhaustively across all 133 sandbox resources of all six types: `GET /{resource}/{id}` returns a byte-identical field set to the list row, with zero additional keys and zero value differences. There is no summary-versus-detail tier. Looping single GETs to "enrich" a list is pure waste and, against a ~60 req/min budget, actively harmful. The one exception is `GET /statements/{id}`, and what it buys is a possibly-re-signed `pdf_url`, not new fields.

**Do not pass `account_id` to `GET /transactions/{id}` speculatively.** The reference describes it only as "Account ID for the transaction". It is in fact an assertion filter: a wrong value turns a `200` into a `404`.

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
TX=019ef508-2808-7000-8000-000000000006   # this row lives on account ...0009
curl -s -o /dev/null -w '%{http_code}\n' -H "$H" "$B/transactions/$TX?account_id=30000000-0000-4000-8000-000000000009"  # 200
curl -s -o /dev/null -w '%{http_code}\n' -H "$H" "$B/transactions/$TX?account_id=30000000-0000-4000-8000-000000000002"  # 404
```

### 8.4 Handling money correctly

#### 8.4.1 Integer minor units, always

Every monetary value in the API is a `Money` object: `{"amount": <integer minor units>, "currency": "USD"}`. The docs repeat "treat amounts as integers rather than decimals" in three separate places. There is no `amount_decimal`, no `exponent` or `scale` field, no FX rate, and no original-currency field anywhere.

Store minor units as a 64-bit integer. Never round-trip through a float. The sandbox range is `-5900000` to `130000000` minor units (`-$59,000.00` to `$1,300,000.00`), comfortably inside int64, but a `float64` loses exactness above 2^53 minor units and there is no documented ceiling.

The exceptions are on Invoicing, and they are genuine non-integers:

| Field | Observed values | Required client type |
| --- | --- | --- |
| `invoices[].line_items[].quantity` | `1`, `2`, `2.5`, `3` | decimal / float, **not** int |
| `invoices[].tax_rate`, `line_items[].tax_rate` | `0`, `10` (ints), `6.25`, `8.5` (floats) | decimal / float |
| `invoices[].discount_rate`, `line_items[].discount_rate` | `0`, `5` | decimal / float |

A strict typed client must declare all three as decimal even though most values serialize without a decimal point. A Go or Rust client that types `quantity` as an integer will fail to deserialize the invoice with `quantity: 2.5`.

The invoice total formula, verified exact on all 12 sandbox invoices:

```
line.total    = round( unit_price.amount * quantity * (1 - line.discount_rate/100) )
invoice.total = round( SUM over lines of
                         line.total
                         * (1 - invoice.discount_rate/100)
                         * (1 + (line.tax_rate ?? invoice.tax_rate)/100) )
```

Two non-obvious parts. A **null** `line_items[].tax_rate` falls back to the invoice-level `tax_rate`; it does **not** mean zero (10 of 16 sandbox line items are null, and treating null as 0 gives the wrong total on `INV-2026-0066`: 146,000 instead of 158,000). And discount is applied **twice**, once per line and once at the invoice level; they do not net.

#### 8.4.2 Sign conventions, which are not consistent across the API

**On transactions:** the sign of `amount.amount` is the only directional signal. There is no `direction`, `debit_credit` or `type: debit|credit` field. The sign is **relative to the account named in `account_id`**: debits negative, credits positive. Zero never occurs across all 72 sandbox rows.

Do not infer direction from the type name. The one pair where name and sign disagree:

| `transaction_type` | Sandbox amount | Account | Note |
| --- | --- | --- | --- |
| `adjustment_credit` | **-4500** | Treasury Checking | "Correction of encoding error regarding check number 100245", counterparty `Rho` |
| `adjustment_debit` | **+3000** | Cash (Checking) | counterparty `Rho`, no memo |

Both are single instances, and nothing in `docs/v1/transactions` or the OpenAPI defines the sign of an adjustment, so whether this is intentional Rho semantics or a fixture sign bug cannot be resolved from the corpus. Either way: **read the sign, never the name.**

`credit_repayment`, `credit_repayment_refund` and `internal_transfer` appear with both signs because they are the double-entry types. Every other type has a single consistent sign across the sandbox.

**On statements, the polarity is inverted.** On a credit statement, `spending` is **positive** for money spent and `repayments` is **negative** for money repaid, which is exactly backwards from `card_debit` (negative) and the credit leg of `credit_repayment` (positive) in the transaction ledger. A single sign convention across both surfaces is impossible; branch explicitly.

The two statement families use mutually exclusive identities, verified on every sandbox record:

```
credit statements  (22/22):  closing_balance = opening_balance + spending + repayments
deposit statements (11/11):  closing_balance = opening_balance + total_credits - total_debits - total_fees
```

Applying the deposit identity to a credit statement gives the wrong answer on 11 of 22, because `total_credits`, `total_debits` and `total_fees` are always `0` on credit statements and carry no information. On `account` and `treasury` statements the `spending`, `repayments` and `cashback` keys are **omitted entirely**, not null. Branch on `statement_type`, or on key presence:

```python
from rho_client import RhoClient, SANDBOX


def closing_balance(statement: dict, acct: dict) -> int:
    """Minor units. Branch on statement_type: the two families share no arithmetic."""
    if statement["statement_type"] == "credit":
        # spending is POSITIVE for spend, repayments NEGATIVE for repayment.
        return (acct["opening_balance"]["amount"]
                + acct["spending"]["amount"]
                + acct["repayments"]["amount"])
    # account and treasury statements omit spending/repayments/cashback entirely.
    return (acct["opening_balance"]["amount"]
            + acct["total_credits"]["amount"]
            - acct["total_debits"]["amount"]
            - acct["total_fees"]["amount"])


client = RhoClient("sandbox", SANDBOX, rate_per_sec=4.0)
checked = 0
for statement in client.paginate("/statements"):
    for acct in statement["accounts"]:
        assert closing_balance(statement, acct) == acct["closing_balance"]["amount"], statement["id"]
        checked += 1
print(checked, "account lines reconciled")   # 33
```

**Amount filters compare the signed value, not the magnitude.** `min_amount=0` returns the 32 credits; `max_amount=0` returns the 40 debits. "Transactions over $100" therefore needs two queries or client-side filtering. Both bounds are inclusive. An inverted amount range is the only cross-field validation in the entire API and returns `400 {"type":"1317","title":"min_amount must be less than or equal to max_amount"}`, while an inverted **date** range returns a quiet `200` with zero rows.

#### 8.4.3 Currency

Every `currency` field in the entire sandbox corpus, across 393 occurrences in all six resources, is `USD`. There is no non-USD record, no FX rate, no settlement currency, and no second currency field anywhere. The documented `transaction_type` enum contains `international_wire_in`, `international_wire_out`, `international_wire_fee` and `international_wire_fee_refund`, and the sandbox produces the latter two but never a non-USD amount.

Store `currency` anyway, on every Money column, and enforce that a comparison or sum across two different currency codes is a programming error. The versioning contract explicitly allows new enum values into `v1` at any time, and "currency is implicit from the queried account" is the only guidance the reference gives on `min_amount`/`max_amount`. A single-currency assumption baked into your schema is the kind of thing that costs a migration later.

### 8.5 Storing and joining IDs

#### 8.5.1 The id shapes, and the one that will break you

| Resource | Observed shape | Example | Parses as UUID? |
| --- | --- | --- | --- |
| accounts | UUIDv4-shaped, prefix `30000000-0000-4000-8000-` | `…-000000000002` | yes |
| cards | UUIDv4-shaped, prefix `20000000-` | `…-000000000001` | yes |
| transactions | **UUIDv7**, time-ordered | `019f0554-0bf0-7000-8000-00000000000a` | yes |
| **statements** | **6-digit decimal string** | `"572981"`, `"152980"` | **no** |
| invoicing customers | UUIDv4-shaped, prefix `60000000-` | `…-000000000007` | yes |
| invoicing invoices | UUIDv4-shaped, prefix `70000000-` | `…-000000000010` | yes |
| transaction attachment `file_id` | genuinely random UUIDv4 | `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15` | yes |
| invoice `file_id` | UUIDv4-shaped, prefix `50000000-` | `…-000000000027` | yes |

> **Divergence:** `docs/v1/versioning` says "Treat IDs as opaque strings. Do not parse structure out of an `id` or assume a fixed format" and "Persist the full string exactly as returned, without assuming a fixed length or layout." That advice is correct and you should follow it, but the docs never state the one consequence that actually matters: **`statements.id` is not a UUID.** All 33 sandbox statement ids are exactly six decimal digits and `uuid.UUID()` rejects every one. A client that types statement ids as `uuid` will fail against sandbox and, by implication, production. Worse, `/statements/{id}` performs **no** format validation at all, so a garbage statement id returns `404 {"type":"1303","title":"statement not found"}` rather than the `400 invalid parameter` the other five resources give you. Store every id as `TEXT`/`VARCHAR`, never as a native UUID column.

The other prefix structure is real but you must not build on it, both because the docs forbid it and because it is fixture-generator artifact: all the `NNNNNNNN-0000-4000-8000-` ids have zero entropy and a decimal-looking counter in the last group.

#### 8.5.2 Normalize ids before using them as keys

The path parser accepts at least five distinct spellings of the same UUID, all returning `200` with an identical body whose `id` is normalized to canonical lowercase-dashed form:

| Spelling | Path | Result |
| --- | --- | --- |
| canonical | `/accounts/30000000-0000-4000-8000-000000000002` | 200 |
| no dashes (32 hex) | `/accounts/30000000000040008000000000000002` | 200 |
| brace-wrapped | `/accounts/{30000000-0000-4000-8000-000000000002}` | 200 |
| `urn:uuid:` prefix | `/accounts/urn:uuid:30000000-0000-4000-8000-000000000002` | 200 |
| uppercase hex | `/transactions/019F0554-0BF0-7000-8000-00000000000A` | 200 |

This is the exact accept-set of Go's `github.com/google/uuid` `Parse()`. Anything keying a cache on the request URL will store up to five copies of the same resource. Normalize to the canonical lowercase-dashed form yourself before it reaches a cache key, a log line or a database column.

#### 8.5.3 The joins that exist, and the ones that do not

Measured referential integrity across the whole sandbox corpus:

| Edge | Refs | Resolve | Dangling |
| --- | --- | --- | --- |
| `transactions.account_id` → accounts | 11 | 11 | 0 |
| `transactions.card_id` → cards | 8 | 8 | 0 |
| `statements.accounts[].account_id` → accounts | 5 | 5 | 0 |
| `customers.last_invoice_id` → invoices | 7 | 7 | 0 |
| `invoices.customer.id` → customers | 7 | 7 | 0 |
| `invoices.payments[].transaction_id` → transactions | 2 | 2 | 0 |
| `cards.cardholder.user_id` → transaction `user_id`s | 8 | 8 | 0 |
| **`invoices.activities[].user_id`** → transaction `user_id`s | **3** | **0** | **3** |

Three entity types are referenced by id and have **no endpoint at all**: users (`10000000-…`, 12 distinct), money movements (`40000000-…`, 65 distinct), and the business itself. You can reconstruct a partial user directory only by unioning `transactions.user_id` + `user_full_name` with `cards.cardholder.{user_id, first_name, last_name}`, and it will be missing anyone who neither holds a card nor initiated a visible transaction. `counterparty_name` is a bare string with no id, so counterparties cannot be deduplicated or joined.

`file_id` is **not one namespace**: invoice file ids use the structured `50000000-` prefix while transaction attachment file ids are random UUIDv4. And a single attachment `file_id` can be attached to two different transactions (`cdc328c1-c3a3-4670-a371-28e34891ee68` appears on both `019f0143-…-0002` and `019ef6d6-…-0009`, resolving to the same deduplicated blob), so the real key is the pair `(transaction_id, file_id)`.

#### 8.5.4 A schema that survives all of the above

```sql
CREATE TABLE rho_transaction (
    -- (id, account_id) is the primary key: `id` alone can drop a leg of a money movement.
    id                 TEXT        NOT NULL,
    account_id         TEXT        NOT NULL,
    money_movement_id  TEXT        NOT NULL,
    -- Store enums as text with no CHECK constraint. v1 may add values at any time.
    transaction_type   TEXT        NOT NULL,
    status             TEXT        NOT NULL,
    account_type       TEXT        NOT NULL,
    amount_minor       BIGINT      NOT NULL,   -- signed, account-relative. Never a float.
    currency           CHAR(3)     NOT NULL,
    initiated_at       TIMESTAMPTZ NOT NULL,
    posted_at          TIMESTAMPTZ,            -- omitted (not null) in the payload when unset
    counterparty_name  TEXT        NOT NULL,   -- may be the empty string
    account_name       TEXT        NOT NULL,   -- denormalized, NOT unique, do not join on it
    card_id            TEXT,
    user_id            TEXT,                   -- dangling: there is no /users endpoint
    memo               TEXT,
    note               TEXT,                   -- user-editable, changes after first sight
    raw                JSONB       NOT NULL,   -- keep the whole body: v1 adds fields additively
    first_seen_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, account_id)
);
CREATE INDEX ON rho_transaction (money_movement_id);
CREATE INDEX ON rho_transaction (initiated_at DESC);
CREATE INDEX ON rho_transaction (status) WHERE status IN ('pending', 'awaiting_approval');

CREATE TABLE rho_statement (
    id            TEXT NOT NULL PRIMARY KEY,   -- 6-digit decimal string, NOT a uuid
    statement_type TEXT NOT NULL,
    period_start  DATE NOT NULL,               -- date-only, inclusive
    period_end    DATE NOT NULL,               -- date-only, inclusive
    available_at  TIMESTAMPTZ NOT NULL,
    raw           JSONB NOT NULL               -- pdf_url excluded from change detection
);

CREATE TABLE rho_transaction_file (
    transaction_id TEXT NOT NULL,
    file_id        TEXT NOT NULL,              -- not unique across transactions
    file_name      TEXT NOT NULL,
    PRIMARY KEY (transaction_id, file_id)
);
```

Two schema rules worth stating explicitly, both derived from the versioning contract:

- **No `CHECK` constraint on any enum column, and a `default` branch on every switch.** "A new enum value" is classified as non-breaking and may ship into `v1` at any time. `transaction_type` already has 33 documented values, of which the sandbox produces 22; `cards.status` has 11, of which the sandbox produces 5. Your code will meet values it has never seen.
- **Keep the raw body.** "A new nullable response field" is also non-breaking. A strict deserializer (`serde` with `deny_unknown_fields`, Jackson with `FAIL_ON_UNKNOWN_PROPERTIES`, a non-defaulted generated enum) will break on an additive change that Rho is contractually entitled to ship without notice.

One spelling trap for any shared status mapper: `cards.status` spells it `canceled` with one L, while `invoices.status` and `activities[].activity_type` spell it `cancelled` with two. Both are correct within their own product and both ship in the same API version.

### 8.6 Retry, backoff and throttling

#### 8.6.1 What is retryable

| Status | Retry? | Notes |
| --- | --- | --- |
| `200` | n/a | |
| `400` | **No** | Two distinct dialects: `{"type":"about:blank",…,"detail":"invalid parameter: X"}` for a type-parse failure, `{"type":"1317","title":"<message>"}` for a semantic rule. Both are your bug. The exception: `"page_token must be a valid cursor"` mid-walk, which means restart the walk from page 1. |
| `401` | **No** | Fix the credential. Note that `401` is byte-identical between sandbox and production, so a wrong-host misconfiguration is indistinguishable from a wrong token. |
| `403` | **No** | Missing scope or source IP off the allowlist. Unreachable in sandbox: any non-empty bearer token grants all five scope families. |
| `404` | **No** | Except on `/statements/{id}`, where it also covers malformed ids. |
| `405` | **No** | Zero-byte body, `allow: GET`. You sent a write method. |
| `411`, `414` | **No** | HTML bodies from the Google frontend and nginx respectively, not from Rho. `414` means your URI crossed the ~8 KB to 16 KB nginx ceiling. |
| `429` | **Yes** | Honor `Retry-After` if present, otherwise exponential backoff with jitter. |
| `500`, `503` | **Yes** | Documented in the OpenAPI, never observed in sandbox. No guidance published for either. |
| Connection errors, timeouts | **Yes** | Every operation is a `GET`, so retries are free. There are no idempotency keys because there is nothing to make idempotent. |

Because every operation is a read, you have an unusual luxury: **retries are always safe.** Use it. Set an aggressive-but-bounded retry policy and stop worrying about duplicate side effects.

#### 8.6.2 Your error parser must tolerate non-JSON

At least five error-body shapes exist, and only three of them are JSON:

| Producer | Status | Content-Type | Body |
| --- | --- | --- | --- |
| Rho application (semantic) | 400, 404 | `application/problem+json` | `{"type":"1317"\|"1303",…}`, no `detail` |
| Rho application (parse) | 400 | `application/problem+json` | `{"type":"about:blank",…,"detail":"invalid parameter: X"}` |
| Rho auth middleware | 401 | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| Go router | 404 | `text/plain; charset=utf-8` | `404 page not found` |
| Go method check | 405 | *(none)* | **zero bytes**, `allow: GET` |
| ingress-nginx | 400, 414 | `text/html` | `400 Request Header Or Cookie Too Large`, `414 Request-URI Too Large` |
| Google frontend | 411 | `text/html` | `Error: Length Required` |
| Cloudflare WAF | 403 | `text/html` | "Attention Required!" block page |
| GCLB | 404 | `text/plain` | `default backend - 404` |

Branch on `Content-Type` before parsing. A client that unconditionally calls `.json()` on an error body throws on `405`, on route typos, and on an oversized `Authorization` header.

**Branch on the HTTP status, not on `type`.** The `type` member is not a URI despite the OpenAPI describing it as "A URI reference that identifies the problem type. Example: `about:blank`". Live values are `"2"`, `"1303"`, `"1317"` and `"about:blank"`. `1303` covers at least nine distinct not-found conditions across six resources; `1317` covers page size, cursor validity, sort, order, card type, card status and amount ordering alike. The only field that distinguishes them is `title`, which is free prose outside the versioning contract. There is no published registry for the numeric codes, and the gaps in the numbering imply a larger internal catalogue that is not published.

#### 8.6.3 Throttling is open-loop, and you cannot rehearse it

There are **no rate-limit headers of any kind**. No `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, no `X-RateLimit-*`, no `RateLimit-Policy`, across roughly 430 captured responses. You cannot pace adaptively. The only strategy available is a fixed, conservative, client-side token bucket.

> **Divergence:** `docs/v1/rate-limits` specifies approximately 60 req/min per token and approximately 600 req/min per source IP, returns `429 Too Many Requests`, and defines `Retry-After` handling including the unusual `Retry-After: 0` case. None of it is enforced or observable in the sandbox. Measured: 150 requests on one token inside a 57-second window, zero `429`; 65 requests on a brand-new, never-before-used token in 11.3 seconds, zero `429`; 60 concurrent requests completing in 0.871 s (68.9 req/s), zero `429`. The docs' own warning that "clients must not assume that exactly 60 simultaneous requests will succeed" was contradicted twice. `Retry-After` was never emitted on any status, so the documented branch logic is unexercisable. **You cannot test your backoff code against Rho's own test environment.** Write it blind and unit-test it against synthetic responses.

> **Divergence:** `429` is fully specified in the rate-limits guide and **absent from every one of the 14 OpenAPI operation pages**, all of which document `200, 400, 401, 403, 500, 503` (plus `404` on the 8 single-resource operations). A client generated from the OpenAPI document will treat `429` as an unmodeled status. Add the case by hand.

Practical rules that follow:

- Self-throttle at **0.9 req/s sustained** per token, with burst 1. The docs' advice is "below one request per second"; there is no documented burst allowance and no stated window semantics (fixed or sliding).
- Handle a `429` with an **absent** `Retry-After`. Nothing guarantees it is emitted.
- Treat `Retry-After: 0` as "use exponential backoff with jitter", not "retry now". This is a non-standard use of the header and Rho defines it explicitly.
- Do not size your client against sandbox tolerance. Sandbox absorbed 2.5x the documented per-token rate without complaint; production may not.
- Watch the **shared per-IP pool**. At 54 req/min per token, one egress IP supports about 11 tokens before the ~600 req/min ceiling binds, and that ceiling counts every integration behind the same NAT, including other teams'. Pinning a stable egress IP for the token's IP allowlist is good security and concentrates rate-limit risk on the same address.

### 8.7 Observability

#### 8.7.1 There is no request id

The only per-request correlation handle on any response is Cloudflare's `cf-ray` (for example `a39acb002db9f9a9-EWR`). There is no `X-Request-Id`, `Request-Id`, `X-Correlation-Id`, `traceparent`, or `X-Cloud-Trace-Context` on any status, on sandbox or production. **Log `cf-ray` on every request, success and failure.** It is the only thing you can quote to support.

Log alongside it: the full request URL including the query string (cursors and filters are the thing that goes wrong), the HTTP status, the response `Content-Type`, the elapsed time, and for errors the raw body bytes truncated. The `via: 1.1 google` header is a useful tell: with it, the request reached the Google-fronted origin stack; without it, Cloudflare or the Google frontend terminated it early.

#### 8.7.2 The alarms that matter

This API fails quietly far more often than it fails loudly. These are the signals worth alerting on, because every one of them corresponds to a real silent-failure mode documented above.

| Signal | What it detects |
| --- | --- |
| A filtered query returns `200 []` while an unfiltered control query on the same endpoint returns rows | A silently dropped filter: an unvalidated enum value, an empty `*_before` value, or a raw `;` in a filter value (Go's `url.ParseQuery` makes that whole key/value pair vanish) |
| Sync watermark has not advanced in N intervals | A stuck cursor, a silently empty result set, or genuinely no activity. You cannot distinguish these from the API, so alarm and investigate. |
| Row count from a full sweep drops between runs | An offset cursor skipped rows, or a filter changed. Rows never disappear from this API. |
| `400 page_token must be a valid cursor` rate above zero | Your query string is not byte-stable across pages |
| Count of rows stuck in `pending` or `awaiting_approval` beyond N days | Lane B is not re-reading them, or genuinely stuck money |
| Distinct `money_movement_id` count with an odd number of legs where you expect pairs | A half-ingested transfer |
| Any 5xx, any non-JSON error body, any `429` | Unrehearsable paths. Alarm on the first occurrence. |
| Token age approaching 45 days of inactivity, or approaching its expiry date | Tokens expire after 45 days of inactivity (window starts at creation for unused tokens) and carry a mandatory expiry of at most one year. There is no API to manage them and no warning mechanism. |

That last row deserves emphasis. Token lifecycle is entirely a UI operation: creation requires an Account Owner or Admin plus a 2FA challenge, there is no create/list/revoke API, and the maximum is 20 active tokens per business. Programmatic key rotation is impossible. Put the expiry date in a calendar and in your runbook.

#### 8.7.3 Metrics worth keeping

- Requests per minute per token, plotted against the documented 60, since you have no server-side signal.
- Page count and row count per walk, per endpoint, per run. A sudden change in page count at a fixed `page_size` is the cheapest available proxy for "the dataset moved".
- Wall time per full sweep. This is your backfill and disaster-recovery budget.
- Distribution of `posted_at - initiated_at` in your own production data. The sandbox says 18.23 days is the worst case; your lane C window should be sized against your real tail, not this one.
- Upsert outcome mix (inserted / updated / unchanged). A healthy steady state is mostly `unchanged` with a small `updated` tail. An `updated` rate that climbs means fields are churning, most likely a signed URL or a recomputed spend window leaking into your change fingerprint.

### 8.8 What you cannot build

Everything in this table is a hard "no" in `v1`, not a gap you can work around with a clever query.

| You cannot | Evidence | What it forces instead |
| --- | --- | --- |
| **Initiate a payment.** No ACH, no wire, no check, no transfer, no bill pay, no invoice send. | All 14 operations are `GET`. `POST`, `PUT`, `PATCH` and `DELETE` return `405 allow: GET` on every path, emitted before authentication. All five scopes end in `:read`. Rho's own product page: "Tokens cannot initiate payments or modify accounts... The Rho API is read-only today." | Your product is a read-side mirror plus an out-of-band handoff. Any "approve and pay" flow ends in a deep link to the Rho web app and a human. Design the UX around a handoff, not around an API call that you will add later. |
| **Issue, lock, unlock, or reconfigure a card.** No limit changes, no merchant-control edits, no PAN, CVC or expiry. | No write operation exists. `allowed_categories`, `allowed_merchants`, `blocked_categories` and `blocked_merchants` are read-only fields (and present on only 1 of 8 sandbox cards each). "Only the last four PAN digits are returned; full card numbers, CVCs, and expiration dates are not available through these endpoints." | Card administration stays in Rho's UI. You can build spend monitoring against `spending_limit`, `current_spend` and `pending_spend`, and alerting on utilisation, and a "lock this card" workflow whose last step is a link and a person. |
| **Receive a webhook.** No events, no subscriptions, no push of any kind. | `GET /webhooks` returns `404 page not found`. No such concept appears anywhere in the docs corpus. | Poll on the three-lane design in 8.2.3. Your data-freshness SLA is your poll interval, and your worst case is your lane C period. Tell downstream consumers what that interval is; do not let them assume real time. |
| **Bulk export.** No CSV or NDJSON endpoint, no export job, no `total_count`, no `Link` header, no backwards paging. `page_size` caps at 100. | The `page` object has exactly one field. Documented and enforced range is `[1, 100]` on all six endpoints. | Backfills are full cursor walks: `ceil(N/100)` requests paced at under 1 req/s. Budget 3.1 hours per million rows and run them on a dedicated token. Build resumability into the walk, because there is no bookmark: "Cursors are designed for live iteration, not for bookmarks", with no documented TTL. Resume by re-walking with a narrowed `initiated_after`, not by persisting a cursor. |
| **Serve more than one business from one token.** No entity selector, no `business_id` parameter, no business or organization endpoint. | A token is scoped to "the business linked to your API Access Token". Sandbox has one global fixture tenant and the token is demonstrably not a tenant selector: four different tokens return byte-identical data (md5 `593d7be465d362f7a9ba94fcbebbb927` on `/accounts`). | One credential per legal entity, N credentials for N entities, an explicit entity dimension in your schema and in every query path, and N separate rate-limit budgets that nonetheless share one ~600 req/min per-IP pool. At 54 req/min per token, one egress IP supports about 11 entities. Beyond that, spread egress addresses or accept queueing. For a partner serving many customers, note that the docs never say whether an OAuth-issued access token gets its own 60/min bucket or shares the partner's. |

Also absent, and worth knowing before you scope a feature around it:

- **No user or employee directory.** 12 user ids are referenced by two resources and resolvable by neither. You can only name a user who appears on a card or a transaction you can see.
- **No counterparty or vendor entity.** `counterparty_name` is a bare string with no id. Vendor deduplication is entirely your problem.
- **No money-movement endpoint.** `money_movement_id` groups legs but cannot be fetched or filtered on.
- **No dispute, decline or authorization surface.** Stated outright: "A refund or credit is not by itself a dispute, `v1` exposes no dispute indicator." There is no `card_dispute` or `chargeback` transaction type.
- **No payment tracing in practice.** `tracking_number` is documented in detail ("an ACH NACHA trace number, or a wire IMAD/OMAD") and never appears on any of the 72 sandbox transactions, including 11 ACH rows and 10 wire rows. `counterparty_logo_url` likewise never appears.
- **No invoice PDF retrieval, in sandbox.** All 9 invoices carrying a `file_id` return `404 {"type":"1303","title":"invoice file not found"}` from the exact call the docs prescribe. The handler routes (a malformed `file_id` returns `400`), so this is a fixture gap rather than a missing route, but you cannot integration-test invoice PDFs at all.
- **No browser client.** `OPTIONS` returns `405` with no CORS headers, and a `GET` carrying an `Origin` gets no `Access-Control-Allow-Origin`. Proxy through your own backend. This is the correct posture for a long-lived opaque secret, and it is nowhere stated in the docs.
- **No sandbox scenario control.** No way to elicit a `403`, `429`, `500`, `503`, an empty account list, or a second tenant. Three of the five error responses the OpenAPI documents per operation are unreachable in sandbox, and `401` is reachable only by deliberately breaking the header.

### 8.9 Reference implementation

A complete, runnable client. Tested against `https://rhoapi-sandbox.rho.co/api/v1` on 2026-09-11: it walks all six list endpoints to exhaustion, returns 72 transactions with 72 distinct `(id, account_id)` keys, and produces the expected `1303`/`about:blank` error classifications. Requires `requests`.

#### 8.9.1 `rho_client.py`

```python
"""Minimal Rho API v1 client. Read-only, poll-based."""
from __future__ import annotations

import json
import logging
import random
import threading
import time
from typing import Any, Iterable, Iterator, Sequence

import requests

log = logging.getLogger("rho")

SANDBOX = "https://rhoapi-sandbox.rho.co/api/v1"
PRODUCTION = "https://rhoapi.rho.co/api/v1"

# The array key in a list response is NOT derivable from the path:
# /invoicing/customers returns "customers", /invoicing/invoices returns "invoices".
RESOURCE_KEY = {
    "/accounts": "accounts",
    "/cards": "cards",
    "/transactions": "transactions",
    "/statements": "statements",
    "/invoicing/customers": "customers",
    "/invoicing/invoices": "invoices",
}

RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class RhoError(Exception):
    def __init__(self, status: int, body: Any, cf_ray: str | None, url: str):
        self.status = status
        self.body = body
        self.cf_ray = cf_ray          # the only correlation handle Rho gives you
        self.url = url
        detail = body if isinstance(body, str) else json.dumps(body, sort_keys=True)
        super().__init__(f"HTTP {status} on {url} (cf-ray={cf_ray}): {detail[:400]}")

    @property
    def problem_type(self) -> str | None:
        return self.body.get("type") if isinstance(self.body, dict) else None

    @property
    def title(self) -> str | None:
        return self.body.get("title") if isinstance(self.body, dict) else None


class RhoAuthError(RhoError): pass
class RhoNotFound(RhoError): pass
class RhoBadRequest(RhoError): pass
class RhoCursorInvalid(RhoBadRequest): pass
class RhoRateLimited(RhoError): pass


class TokenBucket:
    """Open-loop self-throttle. Rho emits no rate-limit headers, so pacing cannot be adaptive."""

    def __init__(self, rate_per_sec: float = 0.9, burst: int = 1):
        self._rate = rate_per_sec
        self._capacity = float(burst)
        self._tokens = float(burst)
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def take(self) -> None:
        while True:
            with self._lock:
                now = time.monotonic()
                self._tokens = min(self._capacity, self._tokens + (now - self._last) * self._rate)
                self._last = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                wait = (1.0 - self._tokens) / self._rate
            time.sleep(wait)


def clean_params(pairs: Iterable[tuple[str, Any]]) -> list[tuple[str, str]]:
    """Drop None; refuse empty strings.

    An empty value on any *_before filter returns 200 with zero rows instead of an error,
    so a templated query with an undefined variable silently reports "no activity".
    """
    out: list[tuple[str, str]] = []
    for key, value in pairs:
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            for item in value:                      # repeats OR together within one parameter
                if item is None or str(item) == "":
                    raise ValueError(f"empty value in repeated parameter {key!r}")
                out.append((key, str(item)))
            continue
        text = str(value)
        if text == "":
            raise ValueError(f"empty value for parameter {key!r}; omit it instead")
        out.append((key, text))
    return out


class RhoClient:
    def __init__(
        self,
        token: str,
        base_url: str = PRODUCTION,
        *,
        rate_per_sec: float = 0.9,
        max_attempts: int = 6,
        timeout: tuple[float, float] = (5.0, 30.0),
        session: requests.Session | None = None,
    ):
        if not token:
            raise ValueError("token must be non-empty")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.bucket = TokenBucket(rate_per_sec)
        self.session = session or requests.Session()
        self.session.headers.update({
            # One ASCII space, capital B. 'bearer' and a tab both return 401.
            "Authorization": f"Bearer {token}",
            # Only gzip is served. 'Accept-Encoding: *' gets you the full 7x payload.
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "User-Agent": "rho-client/1.0",
        })
        # Several connections, low per-connection concurrency: 50 streams on one h2
        # connection measured 13x worse p50 than a warm single stream.
        adapter = requests.adapters.HTTPAdapter(pool_connections=4, pool_maxsize=4, max_retries=0)
        self.session.mount("https://", adapter)

    # -- transport ---------------------------------------------------------

    def get(self, path: str, params: Sequence[tuple[str, str]] = ()) -> dict:
        url = f"{self.base_url}{path}"
        for attempt in range(1, self.max_attempts + 1):
            self.bucket.take()
            try:
                resp = self.session.get(url, params=list(params), timeout=self.timeout)
            except requests.RequestException:
                if attempt == self.max_attempts:
                    raise
                self._sleep_backoff(attempt, None)
                continue

            cf_ray = resp.headers.get("cf-ray")
            log.debug("GET %s -> %s cf-ray=%s", resp.url, resp.status_code, cf_ray)

            if resp.status_code == 200:
                return resp.json()

            body = self._parse_error_body(resp)
            if resp.status_code in RETRYABLE_STATUS and attempt < self.max_attempts:
                self._sleep_backoff(attempt, resp.headers.get("Retry-After"))
                continue
            raise self._classify(resp.status_code, body, cf_ray, resp.url)
        raise RuntimeError("unreachable")

    @staticmethod
    def _parse_error_body(resp: requests.Response) -> Any:
        """Error bodies are not always JSON.

        405 is zero bytes, unrouted paths are text/plain, oversized headers and edge blocks
        are HTML, and only 400/401/404 from the application are problem+json.
        """
        if "json" in resp.headers.get("content-type", ""):
            try:
                return resp.json()
            except ValueError:
                pass
        return resp.text[:1000]

    @staticmethod
    def _classify(status: int, body: Any, cf_ray: str | None, url: str) -> RhoError:
        # Branch on status. `type` is an overloaded non-URI code with no published registry:
        # 1303 covers nine not-found conditions, 1317 covers seven validation failures.
        if status == 401:
            return RhoAuthError(status, body, cf_ray, url)
        if status == 404:
            return RhoNotFound(status, body, cf_ray, url)
        if status == 429:
            return RhoRateLimited(status, body, cf_ray, url)
        if status == 400:
            title = body.get("title") if isinstance(body, dict) else ""
            if isinstance(title, str) and "cursor" in title:
                return RhoCursorInvalid(status, body, cf_ray, url)
            return RhoBadRequest(status, body, cf_ray, url)
        return RhoError(status, body, cf_ray, url)

    @staticmethod
    def _sleep_backoff(attempt: int, retry_after: str | None) -> None:
        # Retry-After has never been observed on any Rho response, so treat it as optional.
        # The docs define Retry-After: 0 as "no cooldown computed", not "retry now".
        delay = min(2 ** (attempt - 1), 30.0)
        if retry_after:
            try:
                hinted = float(retry_after)
                if hinted > 0:
                    delay = max(delay, hinted)
            except ValueError:
                pass
        time.sleep(delay + random.uniform(0, delay * 0.25))

    # -- pagination --------------------------------------------------------

    def paginate(
        self,
        path: str,
        params: Sequence[tuple[str, str]] = (),
        *,
        page_size: int = 100,
        max_pages: int = 10_000,
    ) -> Iterator[dict]:
        """Walk a list endpoint to exhaustion.

        Filters are sent byte-identically on every page: the cursor is bound to a fingerprint
        of the literal query, so order=asc then order=ASC invalidates the token even though
        both return the same rows.
        """
        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be between 1 and 100")
        key = RESOURCE_KEY.get(path)
        if key is None:
            raise ValueError(f"unknown list endpoint {path!r}")

        base = list(params) + [("page_size", str(page_size))]
        token: str | None = None
        seen_tokens: set[str] = set()
        for _ in range(max_pages):
            page_params = base if token is None else base + [("page_token", token)]
            try:
                body = self.get(path, page_params)
            except RhoCursorInvalid:
                if token is None:
                    raise
                # The dataset moved under an offset cursor. Restart; the caller dedupes.
                log.warning("cursor invalidated on %s, restarting walk", path)
                token, seen_tokens = None, set()
                continue

            yield from body.get(key, [])

            token = body.get("page", {}).get("next_page_token")
            if token is None:                     # the ONLY end-of-pages signal
                return
            if token in seen_tokens:
                raise RuntimeError(f"cursor loop detected on {path}")
            seen_tokens.add(token)
        raise RuntimeError(f"page limit exceeded on {path}")

    # -- typed helpers -----------------------------------------------------

    def list_accounts(self) -> list[dict]:
        return list(self.paginate("/accounts"))

    def list_transactions(
        self,
        *,
        account_id: Sequence[str] | None = None,
        status: Sequence[str] | None = None,
        transaction_type: Sequence[str] | None = None,
        initiated_after: str | None = None,
        initiated_before: str | None = None,
        posted_after: str | None = None,
        posted_before: str | None = None,
        page_size: int = 100,
    ) -> Iterator[dict]:
        valid_status = {"pending", "settled", "failed", "awaiting_approval"}
        for value in status or ():
            # /transactions does not validate enums: status=Settled returns 200 with zero rows.
            if value not in valid_status:
                raise ValueError(f"unknown transaction status {value!r}")
        params = clean_params([
            ("account_id", account_id),
            ("status", status),
            ("transaction_type", transaction_type),
            ("initiated_after", initiated_after),
            ("initiated_before", initiated_before),
            ("posted_after", posted_after),
            ("posted_before", posted_before),
        ])
        return self.paginate("/transactions", params, page_size=page_size)

    def get_transaction(self, transaction_id: str) -> dict:
        # Never pass account_id here: a wrong value turns a 200 into a 404.
        return self.get(f"/transactions/{transaction_id}")

    def get_transaction_file(self, transaction_id: str, file_id: str) -> dict:
        return self.get(f"/transactions/{transaction_id}/files/{file_id}")


# -- domain helpers --------------------------------------------------------


def row_key(txn: dict) -> tuple[str, str]:
    """The real primary key. `id` alone can silently drop a leg of a money movement."""
    return (txn["id"], txn["account_id"])


def is_open(txn: dict) -> bool:
    """Rows that can still change. v1 promises no transition order, so re-read these."""
    return txn.get("status") in ("pending", "awaiting_approval") or "posted_at" not in txn


def change_fingerprint(txn: dict) -> tuple:
    """Fields observed or documented to mutate in place after first sight.

    Note .get(): optionality on transactions is expressed by key OMISSION, never by null.
    """
    return (
        txn.get("status"),
        txn.get("posted_at"),
        txn["amount"]["amount"],
        txn["amount"]["currency"],
        txn.get("memo"),
        txn.get("note"),
    )
```

#### 8.9.2 `sync.py`

```python
"""Incremental transaction sync. No webhooks, no updated_at, so this is a multi-lane poll."""
from __future__ import annotations

import datetime as dt
import logging
from dataclasses import dataclass, field
from typing import Callable, Iterable

from rho_client import RhoClient, change_fingerprint, is_open, row_key

log = logging.getLogger("rho.sync")

# Longest posted_at - initiated_at lag in the sandbox corpus is 18.23 days (a settled
# check_payment). 47 of 71 rows lag zero; p90 is 1 day. Size this against YOUR tail.
LATE_ARRIVAL_DAYS = 35
CLOCK_SKEW = dt.timedelta(minutes=5)


def rfc3339(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class SyncState:
    """Persist this. `watermark` is an observed initiated_at, never a wall clock."""

    watermark: dt.datetime | None = None
    open_keys: set[tuple[str, str]] = field(default_factory=set)
    last_full_sweep: dt.datetime | None = None


@dataclass
class SyncResult:
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0


def sync_transactions(
    client: RhoClient,
    state: SyncState,
    upsert: Callable[[dict], str],
    *,
    now: dt.datetime | None = None,
    full_sweep_every: dt.timedelta = dt.timedelta(days=7),
) -> tuple[SyncState, SyncResult]:
    """`upsert` returns "inserted", "updated" or "unchanged" and must be idempotent."""
    now = now or dt.datetime.now(dt.timezone.utc)
    result = SyncResult()
    seen: dict[tuple[str, str], dict] = {}

    def collect(rows: Iterable[dict]) -> None:
        for row in rows:
            seen.setdefault(row_key(row), row)

    do_full = (
        state.watermark is None
        or state.last_full_sweep is None
        or now - state.last_full_sweep >= full_sweep_every
    )

    if do_full:
        # Unfiltered. Any initiated_after floor you pick can silently cut off the tail:
        # the sandbox corpus starts 2023-05-31, three years before its newest row.
        log.info("full sweep, unfiltered")
        collect(client.list_transactions(page_size=100))
        state.last_full_sweep = now
    else:
        # Lane A: newly initiated rows.
        lane_a_from = state.watermark - CLOCK_SKEW
        log.info("lane A from %s", rfc3339(lane_a_from))
        collect(client.list_transactions(initiated_after=rfc3339(lane_a_from), page_size=100))

        # Lane C: trailing window, catches backdated inserts and in-place mutations.
        lane_c_from = now - dt.timedelta(days=LATE_ARRIVAL_DAYS)
        if lane_c_from < lane_a_from:
            log.info("lane C from %s", rfc3339(lane_c_from))
            collect(client.list_transactions(initiated_after=rfc3339(lane_c_from), page_size=100))

        # Lane B: rows still open from before the trailing window, one by one.
        # There is no money_movement_id filter and no id-set filter, so this is the
        # only way to re-read a specific old row.
        for txn_id, _account_id in [k for k in state.open_keys if k not in seen]:
            try:
                collect([client.get_transaction(txn_id)])
            except Exception as exc:      # a 404 here is a bug worth seeing, not a no-op
                log.warning("open row %s unreadable: %s", txn_id, exc)

    open_keys: set[tuple[str, str]] = set()
    max_initiated: dt.datetime | None = state.watermark
    for key, row in seen.items():
        outcome = upsert(row)
        setattr(result, outcome, getattr(result, outcome) + 1)
        if is_open(row):
            open_keys.add(key)
        initiated = dt.datetime.strptime(
            row["initiated_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=dt.timezone.utc)
        if max_initiated is None or initiated > max_initiated:
            max_initiated = initiated

    state.open_keys = open_keys
    if max_initiated is not None:
        state.watermark = max_initiated
    return state, result


def make_upsert(store: dict[tuple[str, str], dict]) -> Callable[[dict], str]:
    """Replace the dict with your database. The contract is: keyed on (id, account_id),
    idempotent, and reports whether anything in the change fingerprint moved."""

    def upsert(row: dict) -> str:
        key = row_key(row)
        prior = store.get(key)
        store[key] = row
        if prior is None:
            return "inserted"
        return "unchanged" if change_fingerprint(prior) == change_fingerprint(row) else "updated"

    return upsert
```

#### 8.9.3 Running it

```python
import datetime as dt, logging
from rho_client import RhoClient, SANDBOX
from sync import SyncState, sync_transactions, make_upsert

logging.basicConfig(level=logging.INFO)
client = RhoClient("sandbox", SANDBOX, rate_per_sec=4.0)   # production: 0.9, and a real token

store: dict = {}
upsert = make_upsert(store)
state = SyncState()

state, first = sync_transactions(client, state, upsert)
print(first)          # SyncResult(inserted=72, updated=0, unchanged=0)
print(len(state.open_keys))   # 3  (2 pending card_debits + 1 awaiting_approval)

state, second = sync_transactions(client, state, upsert)
print(second)         # SyncResult(inserted=0, updated=0, unchanged=4)
```

The second run costs four requests: one page for lane A, plus one `GET /transactions/{id}` for each of the three open rows. That is the steady state the three-lane design is built to produce.

One deliberate omission: the client does **not** pin sandbox versus production beyond the `base_url` you pass. It cannot help you there. Sandbox and production rejections are byte-identical (same 52-byte body, same header set, same Cloudflare IPs, md5 `a9b8c917cbc1e5b43579afaee5ccadd5`), so a typo in your base URL surfaces as exactly the `401` a bad token would. Assert on `base_url` in your own configuration tests, and never let the environment be inferred.
