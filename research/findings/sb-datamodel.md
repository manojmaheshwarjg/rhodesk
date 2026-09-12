# Rho API v1 sandbox: exhaustive data-model census

Source of truth: live calls to `https://rhoapi-sandbox.rho.co/api/v1` with `Authorization: Bearer sandbox`, captured 2026-09-11 between 23:43Z and 23:59Z. Raw captures live in `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/full/`. Doc-side claims are cross-checked against the local corpus of `docs.rho.co` markdown (`rho/docs/`, `rho/api/`).

Scripts written for this census (all re-runnable):

| script | purpose |
|---|---|
| `rho/sandbox/pageall.py` | generic cursor pager with 429 backoff; writes `<name>.json` (flattened items) and `<name>.raw_pages.json` (verbatim page bodies) |
| `rho/sandbox/fetch_details.py` | fetches `GET /{resource}/{id}` for every id returned by every list |
| `rho/sandbox/fetch_files.py` | fetches every `transactions/{id}/files/{file_id}` and `invoicing/invoices/{id}/files/{file_id}` |
| `rho/sandbox/census2.py` | walks the JSON, emits per-field-path presence / null / type / value-set tables (output in `rho/sandbox/census_tables.md`, reproduced in full as §11 below) |
| `rho/sandbox/analyze.py` | ID scheme, sign convention, interlinking, date ranges |
| `rho/sandbox/probe_enums.py`, `probe_sort.py`, `probe_sort2.py`, `probe_filters.py`, `probe_cover.py` | filter, sort, cursor and error-shape probes |

---

## 1. The whole sandbox dataset in one table

Every list endpoint was paged to exhaustion (`page_size=100`, following `page.next_page_token` until null). Every list fits in a single page.

| resource | endpoint | records | pages at `page_size=100` | id space |
|---|---|---|---|---|
| accounts | `GET /accounts` | **14** | 1 | `30000000-0000-4000-8000-0000000000NN`, NN = 01..14 |
| cards | `GET /cards` | **8** | 1 | `20000000-0000-4000-8000-0000000000NN`, NN = 01..08 |
| transactions | `GET /transactions` | **72** | 1 | UUIDv7, sequence suffix 0x01..0x48 |
| statements | `GET /statements` | **33** | 1 | 6-digit decimal strings, **not UUIDs** |
| invoicing customers | `GET /invoicing/customers` | **7** (8 with `include_deleted=true`) | 1 | `60000000-0000-4000-8000-0000000000NN`, NN = 01..08 |
| invoicing invoices | `GET /invoicing/invoices` | **12** | 1 | `70000000-0000-4000-8000-0000000000NN`, NN = 01..12 |
| transaction attachments | `GET /transactions/{id}/files/{file_id}` | **16 rows / 15 distinct file ids** | n/a | random UUIDv4 |
| invoice files | `GET /invoicing/invoices/{id}/files/{file_id}` | **9 referenced, 0 retrievable** | n/a | `50000000-0000-4000-8000-0000000000NN`, NN = 20..28 |

Implied but never listable as their own resource: **12 users** (`10000000-…-0000000000NN`, NN = 01..12), **65 money movements** (`40000000-…`), and one business. There is no `/users`, `/payments`, `/counterparties`, `/webhooks` or `/business` endpoint: all five return a bare `404 page not found` (plain text, not RFC 9457 JSON).

Coverage was verified, not assumed. Refetching `/transactions` filtered by each of the 14 `account_id`s, each of the 4 `status` values and each of the 5 `account_type` values yielded **zero** transaction ids not already in the unfiltered list, and each partition sums exactly to 72 (accounts 20+12+2+0+15+0+0+6+2+5+2+2+4+2; statuses settled 61 + failed 8 + pending 2 + awaiting_approval 1; account types checking 42 + credit 17 + savings 6 + rewards 7 + investment 0). The unfiltered list is complete.

### 1.1 Currency and scale

Every `currency` field in the entire corpus, across 393 occurrences in all six resources, is `USD`. There is not a single non-USD record, and no field anywhere carries an FX rate, a settlement currency, or a second currency. All monetary values are integers in minor units (cents). The only non-integer numerics in the whole dataset are `invoices.tax_rate`, `invoices.discount_rate`, `line_items[].tax_rate`, `line_items[].discount_rate` and `line_items[].quantity`.

### 1.2 Global date span

| series | earliest | latest |
|---|---|---|
| `transactions.initiated_at` | `2023-05-31T07:29:00Z` | `2026-06-26T19:07:02Z` |
| `transactions.posted_at` | `2023-05-31T07:30:00Z` | `2026-06-27T19:13:15Z` |
| `statements.period_start` | `2024-07-01` | `2026-05-01` |
| `statements.period_end` | `2024-07-31` | `2026-05-31` |
| `statements.available_at` | `2024-08-01T04:02:00Z` | `2026-06-05T21:16:51Z` |
| `invoicing_customers.created_at` | `2026-01-10T09:00:00Z` | `2026-04-12T13:20:00Z` |
| `invoicing_customers.updated_at` | `2026-04-01T08:00:00Z` | `2026-07-24T16:00:00Z` |
| `invoices.created_at` | `2026-01-15T10:00:00Z` | `2026-07-10T09:00:00Z` |
| `invoices.date` (issue) | `2026-01-15` | `2026-07-10` |
| `invoices.due_date` | `2026-02-01` | `2026-08-20` |
| `cards.spend_period_start` | `2025-03-01T12:00:00Z` | `2026-09-09T04:00:00Z` |
| `cards.usage_starts_at` | `2025-10-01T09:00:00Z` | (single value) |
| `cards.usage_ends_at` | `2026-06-30T23:59:59Z` | `2026-09-01T00:00:00Z` |

Two clocks are running. The **ledger fixtures are frozen**: nothing in transactions, statements, invoices or customers is dated after 2026-08-20, and the newest transaction is 2026-06-26, roughly 11 weeks before the capture date of 2026-09-11. The **card spend windows are live**: `spend_period_start` = `2026-09-01T04:00:00Z` and `spend_period_end` = `2026-10-01T04:00:00Z` for the six monthly cards, and the one `daily` card shows `2026-09-09T04:00:00Z` to `2026-09-10T04:00:00Z`, i.e. computed against the real wall clock at request time. The `04:00:00Z` offset is midnight in America/New_York during EDT, which matches the documented "reset on Eastern Time (America/New_York) calendar boundaries" rule and is the one place the sandbox visibly recomputes something per request.

### 1.3 Two temporal formats, never mixed within a field

| shape | fields |
|---|---|
| `YYYY-MM-DDTHH:MM:SSZ` (seconds precision, always `Z`, never fractional) | `transactions.initiated_at`, `transactions.posted_at`, `statements.available_at`, `cards.spend_period_start`, `cards.spend_period_end`, `cards.usage_starts_at`, `cards.usage_ends_at`, `customers.created_at`, `customers.updated_at`, `customers.deleted_at`, `invoices.created_at`, `invoices.updated_at`, `invoices.accounting_synced_at`, `invoices.activities[].created_at` |
| `YYYY-MM-DD` (date only, no zone) | `statements.period_start`, `statements.period_end`, `invoices.date`, `invoices.due_date`, `invoices.payments[].paid_at` |

Not one timestamp in the corpus carries a sub-second component or a non-`Z` offset. An integrator can parse with a single strict format per field.

---

## 2. The ID scheme, verified

The docs tell integrators the opposite of what the sandbox shows, and both statements matter. `docs/v1/versioning` says explicitly: "**Treat IDs as opaque strings.** Do not parse structure out of an `id` or assume a fixed format" and "Persist the full string exactly as returned, without assuming a fixed length or layout." The sandbox ids are in fact extremely structured, and one of them is not even a UUID. Do not build on the structure; do use it to reason about the fixtures.

### 2.1 Prefix map (all `NNNNNNNN-0000-4000-8000-0000000000XX` UUIDv4-shaped)

| prefix | entity | count | range of trailing counter |
|---|---|---|---|
| `10000000` | user (cardholder / initiator) | 12 | 01..12 |
| `20000000` | card | 8 | 01..08 |
| `30000000` | account | 14 | 01..14 |
| `40000000` | money movement **and** invoice activity actor (collision, see 2.4) | 65 + 3 | 01..65 |
| `50000000` | invoice file | 9 | 20..28 |
| `60000000` | invoicing customer | 8 | 01..08 |
| `70000000` | invoice | 12 | 01..12 |

All of these parse as **UUID version 4, variant RFC 4122** (`uuid.UUID(x).version == 4`), because the fixture generator hard-codes the version nibble `4` in group 3 and the variant nibble `8` in group 4. They are obviously not random: the entropy is zero and the trailing 12 hex digits are a decimal-looking counter.

Two id families break the prefix scheme entirely:

- **`transactions.attachments[].file_id`**: genuinely random UUIDv4, e.g. `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15`, `104c1de5-dcd3-429d-933e-d61fd076a55c`. 15 distinct, no shared prefix. Note that invoice `file_id`s use the structured `50000000-` prefix while transaction attachment `file_id`s do not: **file ids are not one namespace**.
- **`statements.id`**: a 6-digit **decimal string**, e.g. `"572981"`, `"152980"`. `uuid.UUID()` rejects all 33. Every statement id is exactly 6 characters. This is the single most important trap in the whole surface: a client that types statement ids as UUIDs will fail against both sandbox and, by implication, production.

### 2.2 Statement ids come from two disjoint sequence spaces

| statement_type | n | id range | observed ids |
|---|---|---|---|
| credit | 22 | 152980..200527 | 152980, 153670, 154411, 155137, 155915, 156744, 157603, 158472, 159417, 160431, 161396, 161929, 163022, 164322, 165954, 167766, 169823, 172111, 174810, 179033, 186996, 200527 |
| account | 4 | 428772..439951 | 428772, 433488, 439950, 439951 |
| treasury | 7 | 462701..572981 | 462701, 469372, 475381, 490851, 514051, 539240, 572981 |

Credit statements live in the 15xxxx-20xxxx band; account and treasury statements share the 42xxxx-57xxxx band. Ids increase monotonically with `period_end` within each band, so the id is a global sequence, not a per-account one. Two ids are adjacent (`439950`, `439951`) and belong to two different accounts for the same period, which is a direct counter-example to the aggregation claim in §5.3.

### 2.3 Transaction ids are UUIDv7 with the random bits zeroed out

All 72 transaction ids parse as `uuid.UUID(x).version == 7`. Structure of `019f0554-0bf0-7000-8000-00000000000a`:

| segment | bits | content | observed |
|---|---|---|---|
| `019f0554-0bf0` | 48 | Unix epoch milliseconds, big-endian | full 3-year spread |
| `7000` | 4 + 12 | version nibble `7`, then `rand_a` | `7000` on **all 72**, i.e. `rand_a` is always zero |
| `8000` | 2 + 14 | variant bits `10`, then `rand_b` high | `8000` on **all 72**, i.e. `rand_b` high is always zero |
| `00000000000a` | 48 | `rand_b` low | a **dense sequence counter**: the 72 suffixes are exactly 1..72 with no gaps |

**The embedded millisecond timestamp equals `initiated_at` exactly** on 70 of 72 records (delta 0.000s). Two records disagree, and both are part of the same tiny fixture cluster:

| id | v7-embedded timestamp | `initiated_at` | delta | type |
|---|---|---|---|---|
| `019d3e86-4481-7000-8000-000000000047` | `2026-03-30T11:34:40.001Z` | `2026-03-30T11:35:00Z` | -19.999s | `wire_fee` |
| `019d3e86-4482-7000-8000-000000000048` | `2026-03-30T11:34:40.002Z` | `2026-03-30T11:36:00Z` | -79.998s | `ach_debit` |

These two are also the two highest sequence numbers (71 and 72) and carry the two highest money movement ids (64 and 65), i.e. they were appended to the fixture set last with a shared base timestamp and a +1ms bump each. Everything else was generated by deriving the id from the business timestamp.

The sequence counter runs roughly **newest-first**: suffix 1 is 2026-06-23, suffix 72 is 2026-03-30 (the late addition). Of 71 adjacent pairs, 15 are out of chronological order, and every one of those breaks is either a multi-leg money movement (both legs get consecutive suffixes regardless of the second-level ordering) or the two appended fixtures. So: **sort by `initiated_at` or by the v7 prefix, never by the suffix.**

Practical consequence: transaction ids are lexicographically sortable by time (the v7 prefix dominates), which is why the default list order and the `sort_by=initiated_at` order coincide. UUIDv4-prefixed ids are not.

### 2.4 A real namespace collision: `40000000-` means two different things

`transactions.money_movement_id` uses `40000000-0000-4000-8000-000000000001` through `…000065` (65 distinct, a contiguous 1..65 run). `invoices.activities[].user_id` uses `40000000-0000-4000-8000-000000000001`, `…000002`, `…000003`. Those three ids therefore look like money movements 1, 2 and 3, but semantically they are Rho users who acted on an invoice.

The rest of the corpus consistently uses the `10000000-` prefix for users: `transactions.user_id` (12 distinct) and `cards.cardholder.user_id` (8 distinct, all a subset of the 12). The invoicing subsystem is the odd one out, and the cross-check confirms it is a genuine dangling reference, not a different view of the same people:

```
invoice.activities[].user_id -> txn user ids   refs=3  resolve=0  DANGLING=3
```

Read as: the Invoicing product's actor ids and the banking product's user ids are **not in the same namespace** in this sandbox. An integrator cannot join an invoice activity to a cardholder or a transaction initiator. This is either a fixture bug or a real product seam; nothing in the docs mentions it either way.

---

## 3. Amount sign convention

### 3.1 The transaction ledger: signed, account-relative, no separate direction field

There is **no** `direction`, `debit_credit` or `type: debit|credit` field anywhere on a transaction. The sign of `amount.amount` is the only directional signal, and it is relative to the account named in `account_id`. Debits are negative, credits positive. Zero never occurs: all 72 transactions are strictly non-zero.

| transaction_type | neg | pos | zero | min | max |
|---|---:|---:|---:|---|---|
| `ach_credit` | 0 | 5 | 0 | 12771 | 108403 |
| `ach_debit` | 6 | 0 | 0 | -1250000 | -56250 |
| `ach_return` | 2 | 0 | 0 | -50582 | -18209 |
| `adjustment_credit` | **1** | 0 | 0 | -4500 | -4500 |
| `adjustment_debit` | 0 | **1** | 0 | 3000 | 3000 |
| `card_debit` | 8 | 0 | 0 | -1622132 | -1750 |
| `card_refund` | 0 | 4 | 0 | 1159 | 228073 |
| `check_deposit` | 0 | 3 | 0 | 100000 | 329900 |
| `check_payment` | 2 | 0 | 0 | -339100 | -339100 |
| `credit_repayment` | 3 | 3 | 0 | -1658253 | 1658253 |
| `credit_repayment_refund` | 2 | 2 | 0 | -282512 | 282512 |
| `internal_transfer` | 2 | 2 | 0 | -123987 | 123987 |
| `international_wire_fee` | 2 | 0 | 0 | -1500 | -1500 |
| `international_wire_out` | 2 | 0 | 0 | -279000 | -52142 |
| `rewards_accrual` | 0 | 4 | 0 | 764 | 108403 |
| `rewards_cashback_redemption` | 3 | 0 | 0 | -108403 | -12771 |
| `savings_deposit` | 0 | 2 | 0 | 3000000 | 130000000 |
| `savings_interest` | 0 | 2 | 0 | 225537 | 257025 |
| `savings_withdrawal` | 2 | 0 | 0 | -1000000 | -225537 |
| `wire_fee` | 1 | 0 | 0 | -1000 | -1000 |
| `wire_in` | 0 | 4 | 0 | 9929125 | 15000000 |
| `wire_out` | 4 | 0 | 0 | -5900000 | -50000 |

Totals: 40 negative, 32 positive, 0 zero. Global range `-5900000` (a failed `wire_out`, i.e. -$59,000.00) to `130000000` (a `savings_deposit`, $1,300,000.00).

**`adjustment_credit` is negative and `adjustment_debit` is positive.** This is the one pair where the type name and the sign are inverted relative to every other pair in the table. The two records are single instances:

- `adjustment_credit`, amount `-4500`, on Treasury Checking, memo `Correction of encoding error regarding check number 100245`, counterparty `Rho`.
- `adjustment_debit`, amount `3000`, on Cash (Checking), counterparty `Rho`, no memo.

Whether this is intentional Rho semantics ("a credit adjustment to Rho's books, debiting you") or a fixture sign bug cannot be resolved from the corpus. Nothing in `docs/v1/transactions` or the OpenAPI markdown defines the sign of an adjustment. **Do not infer direction from the type name; read the sign.**

`credit_repayment`, `credit_repayment_refund` and `internal_transfer` appear with both signs because they are the double-entry types (§3.2). Every other type has a single consistent sign in this dataset.

By account type: checking 25 neg / 17 pos, credit 10 neg / 7 pos, rewards 3 neg / 4 pos, savings 2 neg / 4 pos.

### 3.2 Multi-leg money movements are true double entry

65 distinct `money_movement_id`s cover 72 transactions. 58 are single-leg; **7 have exactly 2 legs**, and in every one of them the two legs sum to zero:

| money_movement_id | leg ids | type | accounts | amounts |
|---|---|---|---|---|
| `…000000000002` | `019f0143-3ea0-…000002` / `…000003` | `credit_repayment` | Cash (Checking) / Credit Account | -1750 / +1750 |
| `…000000000003` | `019efe24-c478-…000005` / `019efe24-c860-…000004` | `credit_repayment` | Cash (Checking) / Credit Account | -1658253 / +1658253 |
| `…000000000006` | `019ef6d6-73b0-…000008` / `…000009` | `credit_repayment` | Cash (Checking) / Credit Account | -144827 / +144827 |
| `…000000000021` | `019e9516-3890-…000018` / `…000019` | `internal_transfer` | Cash (Checking) / Reserve Checking | -123987 / +123987 |
| `…000000000027` | `019db616-fc88-…00001f` / `…000020` | `internal_transfer` | Cash (Checking) / Reserve Checking | **+40564 / -40564** |
| `…000000000059` | `018e5b39-07c0-…000041` / `018e5b39-0ba8-…000040` | `credit_repayment_refund` | Cash (Checking) / Credit Account | +282512 / -282512 |
| `…000000000060` | `018e3ffc-6b78-…000042` / `…000043` | `credit_repayment_refund` | Cash (Checking) / Credit Account | +9418 / -9418 |

Note movement `…21` and movement `…27` are both `internal_transfer` between the same two accounts with **opposite polarity**, so the leg order within a movement carries no meaning; only the per-leg `account_id` and sign do. Leg ids within a movement share the same v7 millisecond in 5 of 7 cases and differ by 1ms in the other 2 (`019efe24-c478` vs `c860`, `018e5b39-07c0` vs `0ba8`).

Every 2-leg movement is `settled` on both legs. There is no example in the sandbox of a movement where the legs have different statuses, so nothing here tells you whether Rho can hand you a half-settled transfer.

### 3.3 Statements use the opposite polarity from transactions

This is the sharpest contradiction in the surface. On a credit statement, `spending` is **positive** for money spent and `repayments` is **negative** for money repaid, which is exactly backwards from `card_debit` (negative) and `credit_repayment` (positive on the credit leg) in the transaction ledger.

The credit-statement identity holds on all 22 credit statements with zero exceptions:

```
closing_balance = opening_balance + spending + repayments
```

Worked example, statement `200527` (credit, account `…008`, 2026-03-13 to 2026-04-12): opening `5453868` + spending `6931038` + repayments `-69221` = `12315685` = closing.

Cashback is a deterministic function of spending, at **two different rates depending on the credit account**, truncated toward zero:

| credit account | rate | evidence |
|---|---|---|
| `30000000-…0000007` (11 statements) | **1.25%** | 3000⇒37 (37.5 truncated), 5100⇒63 (63.75), 6000⇒75, 37600⇒470, 2191⇒27 (27.39), -100⇒-1 (-1.25), -26200⇒-327 (-327.5) |
| `30000000-…0000008` (11 statements) | **1.50%** | 1700⇒25 (25.5), 17210⇒258 (258.15), 5500⇒82 (82.5), 15400⇒231, 50712⇒760 (760.68), 18158⇒272 (272.37), 5257167⇒78857, 2165528⇒32482, 69331⇒1039 (1039.96), 6931038⇒103965 |

Truncation is toward zero, not floor: `-26200` at 1.25% is `-327.5` and yields `-327`, not `-328`. Two periods on account `…007` carry **negative** spending and positive repayments (`158472`: spending `-100`, repayments `100`, cashback `-1`; `161396`: spending `-26200`, repayments `26200`, cashback `-327`), i.e. net refund months with cashback clawed back at the same rate. Nothing in the API exposes the cashback rate itself; it can only be derived.

Deposit statements use a different, mutually exclusive identity:

```
closing_balance = opening_balance + total_credits - total_debits - total_fees
```

which holds on all 4 `account` and all 7 `treasury` statements. Worked example `433488` (account, `…006`, 2024-12): `991900` + `0` - `6000` - `0` = `985900`.

The two families do not overlap. On credit statements `total_credits`, `total_debits` and `total_fees` are **always `0`** and carry no information, so applying the deposit identity to a credit statement gives the wrong answer on 11 of 22 (every one where opening != closing). On account and treasury statements the `spending`, `repayments` and `cashback` keys are **omitted entirely**, not null. Branch on `statement_type`, or on key presence.

Across the whole statement set `total_fees.amount` is `0` in all 33 entries, `total_credits.amount` takes only `{0, 26200}` and `total_debits.amount` only `{0, 6000}`. The deposit-statement aggregates are essentially unexercised fixtures.

### 3.4 Balances do not reconcile to the transaction list

`accounts.balance.amount` is a standalone figure; summing settled transactions per account reproduces it on only 4 of 14 accounts, and those 4 are the ones where both sides are `0`.

| account | name | `balance.amount` | sum of settled txns | match |
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

Sum of all 14 balances: `25861780` ($258,617.80). The transaction list is a curated sample, not a complete ledger, and the sandbox does not pretend otherwise. Do not write reconciliation tests against the sandbox.

Also note: all four `credit` accounts and both `rewards` accounts report `balance.amount = 0`, so the sandbox never shows what a carried credit balance looks like on `/accounts`, even though credit statements clearly carry non-zero closing balances up to `12315685`. There is no `available_balance`, `credit_limit`, `posted_balance` or `pending_balance` field on an account at all.

---

## 4. Enums: documented set vs observed set

Rho's versioning policy warns that a new enum value can ship into `v1` at any time and that clients must have a default branch. The gap between documented and observed is therefore the integrator's real test-coverage problem.

### 4.1 `transaction_type` (33 documented, 22 observed, 11 never seen)

Observed: `ach_credit`, `ach_debit`, `ach_return`, `adjustment_credit`, `adjustment_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `credit_repayment`, `credit_repayment_refund`, `internal_transfer`, `international_wire_fee`, `international_wire_out`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`, `wire_out`.

**Never produced by the sandbox:** `card_credit`, `credit_cashback`, `international_wire_in`, `international_wire_fee_refund`, and the **entire treasury family**: `treasury_deposit`, `treasury_withdrawal`, `treasury_fee`, `treasury_interest`, `treasury_maturity`, `treasury_sale`, `treasury_market_value_adjustment`.

The treasury gap is the notable one. The sandbox has a "Treasury Checking" account (`…004`), it has 7 `treasury` statements, but its only transaction is a single `adjustment_credit` of `-4500`. Treasury is the product Rho markets hardest and it is the one whose transaction shapes an integrator cannot see. Likewise `account_type: investment` is documented and filterable (`?account_type=investment` returns HTTP 200 with 0 results) but no investment account exists.

### 4.2 `transaction_type` x `account_type` (observed pairs only)

| account_type | transaction types seen |
|---|---|
| `checking` | ach_credit 5, ach_debit 6, ach_return 2, adjustment_credit 1, adjustment_debit 1, check_deposit 3, check_payment 2, credit_repayment 3, credit_repayment_refund 2, internal_transfer 4, international_wire_fee 2, international_wire_out 2, wire_fee 1, wire_in 4, wire_out 4 |
| `credit` | card_debit 8, card_refund 4, credit_repayment 3, credit_repayment_refund 2 |
| `rewards` | rewards_accrual 4, rewards_cashback_redemption 3 |
| `savings` | savings_deposit 2, savings_interest 2, savings_withdrawal 2 |
| `investment` | none |

Card transactions land on `credit` accounts only. There is no `card_debit` on a checking account anywhere in the sandbox, so a debit-card-on-checking model is untested.

### 4.3 `transaction_type` x `status`

| type | pending | settled | failed | awaiting_approval |
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

All 4 `wire_out` records and all 3 `check_deposit` records are `failed`. There is no settled `wire_out` and no settled `check_deposit` in the sandbox.

### 4.4 Every other enum, documented vs observed

| field | documented values | observed | never observed |
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

`cards.status` spells `canceled` with one L, while `invoices.status` spells `cancelled` with two. Both spellings are correct within their own product and both appear in the same API version. `activities[].activity_type` also uses `cancelled`. This is a live gotcha for anyone writing a shared status mapper.

Note the deliberate asymmetry: `invoices.status` and `activities[].activity_type` are **fully exercised** (11 of 11 activity types across only 12 invoices), while `cards.status` covers only 5 of 11 and `transaction_type` only 22 of 33. Invoicing is the best-covered product in the sandbox; cards fulfilment and treasury are the worst.

---

## 5. Per-resource structure, semantics and traps

### 5.1 Accounts (14)

| id tail | `account_type` | `account_name` | `balance.amount` | `account_number_last_4` | `routing_number_last_4` |
|---|---|---|---:|---|---|
| 01 | checking | Reserve Checking | 1046 | 0106 | 0089 |
| 02 | checking | Cash (Checking) | 876138 | 9508 | 0089 |
| 03 | checking | Cash (Checking) | 8711697 | 4609 | 0089 |
| 04 | checking | Treasury Checking | 15460929 | 7301 | 0089 |
| 05 | checking | Inventory Checking | 0 | 3608 | 0089 |
| 06 | checking | Primary Checking | 811970 | 5702 | 0089 |
| 07 | credit | Credit Account | 0 | *(absent)* | *(absent)* |
| 08 | credit | Credit Account | 0 | *(absent)* | *(absent)* |
| 09 | credit | Credit Account | 0 | *(absent)* | *(absent)* |
| 10 | credit | Credit Account | 0 | *(absent)* | *(absent)* |
| 11 | rewards | Rewards | 0 | *(absent)* | *(absent)* |
| 12 | rewards | Rewards | 0 | *(absent)* | *(absent)* |
| 13 | savings | Savings | 0 | 3214 | 0089 |
| 14 | savings | Savings | 0 | 2513 | 0089 |

Traps:

- **`account_number_last_4` and `routing_number_last_4` are omitted, not null**, on the 6 credit and rewards accounts. The list surface returns a 4-key object for those (`account_name`, `account_type`, `balance`, `id`) and a 6-key object for the 8 deposit accounts. A strict deserializer that expects all six keys breaks on 6 of 14 records. The OpenAPI markdown lists both fields as non-required, so this is consistent with the spec, but presence varies within a single response array.
- `account_name` is **not unique**: "Cash (Checking)" appears twice, "Credit Account" four times, "Rewards" twice, "Savings" twice. Only `id` identifies an account. `account_number_last_4` is unique across the 8 that have it.
- All 8 deposit accounts share `routing_number_last_4 = "0089"`, i.e. one sponsor bank routing number.
- **"Treasury Checking" has `account_type: "checking"`, not `treasury`.** `treasury` exists as an `account_type` value only inside `statements.accounts[].account_type`; it is **not** a member of the `accounts.account_type` enum at all. The two enums are different sets: accounts use `{checking, credit, investment, savings, rewards}` and statement lines use `{checking, savings, credit, treasury}`. Treasury is a statement-level concept mapped onto a checking account.
- Three accounts (`…005` Inventory Checking, `…008`, `…010` Credit Account) have **zero transactions**. Nine of the 14 appear in no statement.
- There is no `created_at`, `status`, `nickname`, `available_balance` or `credit_limit` on an account. An account is 4 to 6 fields and nothing else.

### 5.2 Cards (8)

| id tail | `name` | `type` | `status` | `last_4` | limit type | limit | current_spend | pending_spend | util | `spend_period_start` | `spend_period_end` |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| 01 | Ethan Parker | virtual | active | 7291 | monthly | 500000 | 6797 | 1500 | 1.4% | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z |
| 02 | Maya Thompson | physical | active | 1846 | monthly | 100000 | 45000 | 8000 | 45.0% | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z |
| 03 | Daniel Rivera | virtual | active | 3150 | monthly | 250000 | 1750 | 250 | 0.7% | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z |
| 04 | Lucas Bennett | physical | locked | 6603 | **daily** | 75000 | 6331 | 900 | 8.4% | 2026-09-09T04:00:00Z | 2026-09-10T04:00:00Z |
| 05 | Sofia Martin Physical Card | physical | active | 0042 | monthly | 200000 | 5331 | 400 | 2.7% | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z |
| 06 | Hannah Brooks | virtual | suspended | 9027 | monthly | 2500000 | 1622132 | 50000 | 64.9% | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z |
| 07 | Emma Walsh Virtual Card | virtual | canceled | 1184 | monthly | 150000 | 121827 | 0 | 81.2% | 2026-09-01T04:00:00Z | 2026-10-01T04:00:00Z |
| 08 | Claire Mitchell | physical | expired | 7732 | **fixed** | 500000 | 0 | 0 | 0.0% | 2025-03-01T12:00:00Z | **null** |

Confirmations and traps:

- `last_4` really does carry a leading zero (`"0042"` on card 05), exactly as the docs warn. It is a string and must stay one.
- The documented rule "`spend_period_end` is null when the limit does not reset (fixed, single_use)" holds: the one `fixed` card is the one null. The 4:00Z boundary confirms America/New_York EDT arithmetic.
- **`spending_limit` is never null** and `spending_limit_type` is never null in the sandbox, even though both are documented as "null when the card has no limit". A no-limit card is untested. Likewise `current_spend` is documented as nullable and is a populated object on all 8.
- **Canceled, suspended, locked and expired cards still report live spend windows.** Card 07 is `canceled` and still shows `spend_period_start` = `2026-09-01T04:00:00Z` recomputed at request time. Card status does not freeze the window.
- **Merchant and MCC controls are omitted, not null, on 7 of 8 cards.** Exactly one card carries `allowed_categories` (`[{code: "5812", name: "Eating places and restaurants"}]`) and `allowed_merchants` (`[{name: "Sweetgreen"}]`); a different single card carries `blocked_categories` (`[{code: "0742", name: "Veterinary services"}]`) and `blocked_merchants` (`[{name: "Petco"}]`). No card has both allow and block lists. The three distinct object shapes returned by `/cards` are: 16 keys (6 cards, no controls), 18 keys with allow lists (1 card), 18 keys with block lists (1 card).
- MCC codes are **strings with leading zeros** (`"0742"`), not integers.
- `shipping_address` is **explicitly `null`** on 4 of 8 cards (all 4 virtual ones), while merchant controls are **omitted**. Both null-ness idioms appear on the same object. `billing_address` is always present on all 8.
- `billing_address.second_line` is omitted on 7 of 8 (`"Floor 5"` on the one). `shipping_address.second_line` is present on all 4 that have a shipping address.
- The docs' markdown export flattens only one level of `$ref`, so `current_spend`, `pending_spend`, `shipping_address`, `allowed_categories` and `allowed_merchants` have **no documented sub-fields**. The sandbox is the only place their shapes are visible: `{amount:int, currency:string}` for the two money objects; `{street, second_line?, city, subdivision, postal_code, country_code}` for `shipping_address` (same shape as `billing_address`); `{code, name}` for categories; `{name}` for merchants.
- `current_spend` is documented as "pending plus settled spend in the current limit window". `pending_spend` is a **separate, additional** field that the OpenAPI markdown lists but never describes, and the two are not nested. On card 01, `current_spend` 6797 and `pending_spend` 1500 are different numbers; whether pending is inside current cannot be determined from the sandbox.
- `cardholder` is a flat `{user_id, first_name, last_name}`; there is no email, role or title. Card `name` equals `"{first} {last}"` on 6 of 8 and adds a suffix on 2 (`"Sofia Martin Physical Card"`, `"Emma Walsh Virtual Card"`), confirming it is a free-text user-editable label, not derived.
- 8 cards, 8 distinct cardholders, 1:1. Four of the 12 users (`…005` Olivia Chen, `…010` Priya Shah, `…011` Grace Morgan, `…012` Andrew Collins) initiate transactions but hold no card.
- Every card has at least one transaction. 12 transactions carry a `card_id`, spread over all 8 cards.

### 5.3 Statements (33)

| statement_type | n | account(s) | period cadence | id band |
|---|---:|---|---|---|
| `credit` | 22 | `…007` (11), `…008` (11) | `…007`: calendar months 2024-07 to 2025-05. `…008`: **13th-to-12th cycles**, 2025-05-13/2025-06-12 through 2026-03-13/2026-04-12 | 152980-200527 |
| `account` | 4 | `…006` Primary Checking (3), `…013` Savings (1) | calendar months 2024-07, 2024-12, 2025-05 | 428772-439951 |
| `treasury` | 7 | `…004` Treasury Checking (7) | calendar months 2025-11 through 2026-05 | 462701-572981 |

Three contradictions with the documented contract, all confirmed on every record:

1. **`statements.accounts[].account_id` is documented as "Null for credit statements, which are not tied to a deposit account". It is never null.** All 22 credit statements carry a real account id (`…007` or `…008`), and those ids resolve to real `account_type: "credit"` accounts on `/accounts`. Zero nulls across all 33 statements.
2. **`statements.accounts` is documented as possibly spanning multiple checking/savings accounts. Its length is 1 on all 33 records**, credit and deposit alike. The pair `439950` (account `…006`, checking) and `439951` (account `…013`, savings) covers the identical period `2025-05-01`..`2025-05-31` as **two separate statements**, which is precisely the case the docs say would be one multi-account statement. The `account_id` filter's documented warning that "a matched statement's accounts array and PDF may include additional accounts" is unexercised.
3. **`statements.accounts[].repayment_date` is documented ("Credit statements only; date repayment is/was due for the period") and never appears** on any of the 22 credit statements.

Further observations:

- `period_end` is the **last day of the month** on 22 of 33 records and is the 12th on the 11 account-`…008` credit statements. Both `period_start` and `period_end` are inclusive (the 13th-to-12th cycles are contiguous with no gap).
- `available_at` lags `period_end` by 1 day on 22 records (all credit), 2 days on 4, and 5 to 8 days on the remaining 7 (treasury and account). Max lag 8 days (`469372`, treasury 2025-12).
- **`pdf_url` is never null** across all 33, contradicting nothing but leaving the documented "or `null` when the document cannot be linked" branch untested.
- The 33 statements resolve to only **3 distinct PDF blobs**: `/e9c29858933afd7a8d42e1a7.pdf` (all 22 credit), `/41addf56a3d9ab46a2bfedc6.pdf` (all 7 treasury), `/4f7150d8341cae23c6ffa33a.pdf` (all 4 account). One placeholder PDF per statement type.
- The signed URL is **regenerated on every request**. Fetching the list and then `GET /statements/{id}` minutes apart produced different `X-Goog-Date` and `X-Goog-Signature` for the same blob. Parameters: `X-Goog-Algorithm=GOOG4-RSA-SHA256`, `X-Goog-Credential=file-service@pledge-218909.iam.gserviceaccount.com/YYYYMMDD/auto/storage/goog4_request`, **`X-Goog-Expires=899`** (899 seconds = 14 minutes 59 seconds, matching the documented "valid for up to 15 minutes"), `X-Goog-SignedHeaders=host`. Host: `sandbox-statements.files.rho.co`. The GCP project name `pledge-218909` leaks in the credential parameter on every signed URL Rho issues, sandbox and, presumably, production.
- Statements carry **no** `account_name`, no statement number, no page count, no `created_at`, and no link back to the transactions they cover. Reconciling a statement to the transaction list requires the integrator to do the date-range and account filtering itself.

### 5.4 Transactions (72)

Presence is the whole story here. The list surface returns **six distinct object shapes** depending on which optional keys are omitted:

| keys | count | which transactions |
|---:|---:|---|
| 12 | 14 | no memo/note, no user, no card |
| 13 | 1 | memo+note+user, **no `posted_at`** (the one `awaiting_approval` record) |
| 14 | 20 | memo+note, no user, no card |
| 14 | 7 | user, no memo/note, no card |
| 16 | 18 | memo+note+user |
| 16 | 12 | user+card, no memo/note |

Optional-key presence, out of 72:

| field | present | omitted | never null when present |
|---|---:|---:|---|
| `posted_at` | 71 | **1** | yes |
| `memo` | 39 | 33 | yes |
| `note` | 39 | 33 | yes |
| `user_id` | 38 | 34 | yes |
| `user_full_name` | 38 | 34 | yes |
| `card_id` | 12 | 60 | yes |
| `card_name` | 12 | 60 | yes |
| `counterparty_logo_url` | **0** | 72 | n/a |
| `tracking_number` | **0** | 72 | n/a |

**Not one transaction field is ever JSON `null`.** Optionality is expressed purely by key omission. The docs say `posted_at` is "Null while status is pending" and `user_id` is "Null for system-initiated transactions"; the sandbox omits the key in both cases instead. A client written against the literal doc wording (`if (txn.posted_at === null)`) will see `undefined` and must handle both.

Key correlations, all exact:

- `posted_at` is present on **all 61 settled, all 8 failed and both pending** records and absent only on the single `awaiting_approval` record (`019d3e86-4482-…000048`, ach_debit, initiated `2026-03-30T11:36:00Z`). So the operative rule is **"absent while awaiting approval"**, not "absent while pending": both `pending` card_debits carry a `posted_at`. The documented rule ("Null while status is pending") is contradicted by the data in both directions.
- `posted_at` is always >= `initiated_at`; 0 negative lags. Range 0 seconds to **1,574,873 seconds (18.2 days)**, on `019d1987-7140-…000028`.
- `memo` and `note` are present or absent **together**, never one without the other (39/39, 33/33). They are **byte-identical on 37 of the 39**. The only two that differ are the two failed ACH records, where `note` = memo + `", Error: Invalid receiving routing number."`. Given the docs describe `memo` as bank-supplied and read-only and `note` as user-entered and editable, the sandbox effectively models them as one field. An integrator cannot use the sandbox to test the distinction.
- `user_id` and `user_full_name` are always present or absent together. Present on exactly the types a person initiates (`ach_credit`, `ach_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `internal_transfer`, `international_wire_out`, `wire_out`) and absent on exactly the system types (`ach_return`, `adjustment_credit`, `adjustment_debit`, `credit_repayment`, `credit_repayment_refund`, `international_wire_fee`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`). The split is clean per type with no type appearing on both sides. Note that `wire_in` and `savings_deposit` are treated as system-initiated even though a human presumably triggered them.
- `card_id` and `card_name` are present on exactly the 12 `card_debit` + `card_refund` records and on nothing else. Zero card-typed transactions lack a card id.
- `account_name` on a transaction is a **denormalized copy** of `accounts.account_name` and inherits its non-uniqueness.
- `counterparty_name` doubles as the other side of an internal transfer: the 37 distinct values include `Cash (Checking)`, `Primary Checking`, `Reserve Checking`, `Treasury Checking`, `Rewards`, plus `Rho`, `Rho Rewards` and `Rho Savings` for system entries. The rest are fictional merchants and people: `Aaron Blake`, `Bowline Journeys Amsterdam`, `Brightstone Consulting LLC`, `Canal House Bistro Amsterdam`, `City Photo Tours London`, `Civic Affairs Inc.`, `Cloudbridge Services LLC`, `Crescent Property Group`, `Everline Creative Studio`, `Foundry Works Inc.`, `Graceway Car Service`, `Greenfield Yard Supply`, `Guangzhou Harbor Apparel Co., Ltd.`, `Harborline Logistics`, `Island Resort Maldives`, `Maison Aurelia SAC`, `Marcus Hill`, `Meridian Travel Inc.`, `Midtown Parking Services`, `Night Kitchen Amsterdam`, `Northstar Office Supply`, `Riverside Community College`, `Summit Legal LLP`, `Teamline Software, Inc.`, `Thomas Reed`, `Wellstone Media LLC`, `Westbridge Polytechnic Institute`, `Zurich Airport Services`.
- **`tracking_number` never appears**, on any transaction, of any type. The documented purpose is ACH NACHA trace numbers and wire IMAD/OMAD. The sandbox has 6 settled ACH debits, 5 settled ACH credits, 4 wire_in, 4 failed wire_out and 2 international_wire_out, and none of them carries one. An integrator building payment tracing cannot exercise it.
- **`counterparty_logo_url` never appears** either, on any of the 72.
- `attachments` is **always present, never null**, and is `[]` on 58 of 72. 12 transactions have 1 attachment, 2 have 2, for 16 rows over 15 distinct `file_id`s. One file id, `cdc328c1-c3a3-4670-a371-28e34891ee68` (`credit-repayment-receipt.pdf`), is attached to **two different transactions**, so `file_id` is not unique per transaction and the `{transaction_id, file_id}` pair is the real key. File names are otherwise unique. One is a `.csv` (`repayment-details.csv`); the other 14 are `.pdf`.
- Memo text leaks internal formats: `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00` (a Postgres timestamptz with microseconds and an Eastern offset, rendered into a user-visible string), `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`, `Daily credit repayment for date 2026/06/23`, `Swift OUR fee`, `PAY1001984`, `SC - 2509 - desk mat shipping`. These are plainly lifted from a real production ledger and then anonymized, which is why the formats are inconsistent.

**`GET /transactions/{id}/files/{file_id}` works**: 16 of 16 returned HTTP 200 with exactly three fields, `{download_url, file_id, file_name}`. There is no size, MIME type, upload timestamp or uploader. Host `rho-api-sandbox.files.rho.co`, same GCS V4 signing with `X-Goog-Expires=899`, and **15 distinct blobs** (one per file id, with the shared file id resolving to the same blob from both transactions).

### 5.5 Invoicing customers (8, of which 1 soft-deleted)

| id tail | `legal_name` | `email` | `total_revenue` | `last_invoice_id` | `deleted_at` | `note` | `cc_emails` |
|---|---|---|---:|---|---|---|---|
| 01 | Acme Supplies | info@acmesupplies.com | 108403 | …02 | null | Preferred Net 30 customer | 2 |
| 02 | Brightleaf Design | hello@brightleaf.design | 43400 | …03 | null | null | 0 |
| 03 | Northwind Traders | orders@northwind.example | 0 | …06 | null | Quarterly retainer | 1 |
| 04 | Harbor Logistics LLC | billing@harborlogistics.com | 156750 | …08 | null | Large volume account | 1 |
| 05 | Summit Analytics | contact@summitanalytics.io | 0 | …10 | null | null | 0 |
| 06 | Cedar & Co | **null** | 0 | **null** | null | null | 0 |
| 07 | Orbit Media Group | accounts@orbitmedia.co | 0 | …11 | null | null | 0 |
| 08 | Deleted Co | gone@deletedco.example | 5000 | …12 | **2026-05-01T12:00:00Z** | Soft-deleted fixture customer | 0 |

- `include_deleted` default is **false**: `/invoicing/customers` returns 7, `?include_deleted=true` returns 8, `?include_deleted=false` returns 7, `?include_deleted=1` returns **8** (so `1` is parsed as true). The deleted customer `…008` is still fully retrievable by id via `GET /invoicing/customers/{id}` regardless of the flag, exactly as documented.
- **`email` is documented as `required` and is `null` on customer `…006`.** Same for `last_invoice_id`, documented required, null on the customer with zero invoices. The OpenAPI "required" marker here means "the key is always present", not "the value is non-null". This distinction matters on every field of this resource: **all 19 field paths are present on all 8 records**, with nullity carrying the optionality. Customers are the mirror image of transactions, where optionality is carried by key omission and nothing is ever null.
- `address.address2` is the empty string `""` on the customers that lack one (not null, not omitted). Three distinct values across 8: `""`, `"Floor 2"`, `"Suite 400"`.
- `address.country` is `"USA"` (3-letter, ISO 3166-1 alpha-3 style) on all 8. Compare `cards.billing_address.country_code` = `"US"` (alpha-2). **Two country encodings in the same API.** Likewise the field names differ: customers use `address1/address2/city/state/zip_code/country`; cards use `street/second_line/city/subdivision/postal_code/country_code`. Two address models, no shared type.
- `cc_emails` is an array, present on all 8, length 0 on 5, 1 on 2, 2 on 1.
- `total_revenue` matches the sum of that customer's **`paid`-status invoices** exactly on all 8 (8/8). `pending_payout`, `confirm_payment`, `overdue` and `unpaid` invoices do not count. Note customer `…003` Northwind Traders holds 3 invoices totalling `10168200` minor units (`72200` overdue, `96000` unpaid, `10000000` confirm_payment) and still reports `total_revenue = 0`, because none is `paid`.
- `last_invoice_id` equals the customer's newest invoice by `created_at` on all 8 (including the null for the invoice-less customer). It resolves into `/invoicing/invoices` in all 7 non-null cases.
- The soft-deleted customer still has a live invoice (`…012`, `INV-2026-0001`, status `paid`), so deleting a customer does not cascade.
- There is no `phone`, `tax_id`, `currency`, `payment_terms` or `default_due_days` on a customer.

### 5.6 Invoicing invoices (12)

| id tail | number | status | total | tax_rate | discount_rate | customer | `file_id` tail | `accounting_sync_status` | lines | payments | activities |
|---|---|---|---:|---|---|---|---|---|---:|---:|---:|
| 01 | INV-2026-0002 | paid | 108403 | 10 | 0 | …001 | …0020 | synced | 2 | 1 | 6 |
| 02 | INV-2026-0066 | pending_payout | 158000 | 10 | 0 | …001 | …0021 | synced | 4 | 1 | 7 |
| 03 | INV-2026-0060 | overdue | 45000 | 0 | 0 | …002 | …0022 | not_pushed | 1 | 0 | 3 |
| 04 | INV-2026-0040 | paid | 43400 | 8.5 | 0 | …002 | …0023 | synced | 1 | 1 | 4 |
| 05 | INV-2026-0045 | overdue | 72200 | 0 | 5 | …003 | …0024 | error | 1 | 0 | 3 |
| 06 | INV-2026-0065 | unpaid | 96000 | 0 | 0 | …003 | *(absent)* | not_pushed | 1 | 0 | 2 |
| 07 | INV-2026-0043 | confirm_payment | 10000000 | 0 | 0 | …003 | …0025 | object_changed | 1 | 1 | 3 |
| 08 | INV-2026-0050 | paid | 156750 | 0 | 0 | …004 | …0026 | synced | 1 | 1 | 4 |
| 09 | INV-2026-0041 | cancelled | 22000 | 0 | 0 | …005 | *(absent)* | skip | 1 | 0 | 2 |
| 10 | INV-2026-0070 | pending_payout | 98000 | 0 | 0 | …005 | …0027 | synced | 1 | 1 | 5 |
| 11 | INV-2026-0052 | unpaid | 45000 | 6.25 | 0 | …007 | …0028 | not_pushed | 1 | 0 | 2 |
| 12 | INV-2026-0001 | paid | 5000 | 0 | 0 | …008 | *(absent)* | synced | 1 | 1 | 3 |

Invoices 06, 09 and 12 omit `file_id` entirely. Invoice numbers are **not** in id order (`…001` is `INV-2026-0002`, `…012` is `INV-2026-0001`), and the sequence has gaps: 0001, 0002, then 0040, 0041, 0043, 0045, 0050, 0052, 0060, 0065, 0066, 0070.

**The invoice total formula, verified against all 12 records:**

```
line.total   = round( unit_price.amount * quantity * (1 - line.discount_rate/100) )
invoice.total = round( SUM over lines of
                        line.total
                        * (1 - invoice.discount_rate/100)
                        * (1 + (line.tax_rate ?? invoice.tax_rate)/100) )
```

12 of 12 exact. The two non-obvious parts:

1. **A null `line_items[].tax_rate` falls back to the invoice-level `tax_rate`, it does not mean zero.** `INV-2026-0066` has 4 lines; two have `tax_rate: null` and two have `tax_rate: 0`. Total = 100000x1.10 + 20000x1.10 + 20000x1.00 + 6000x1.00 = 158000. If null meant 0 the total would be 146000. 10 of the 16 line items have a null tax rate.
2. **Discount is applied twice, once per line and once at the invoice level.** `INV-2026-0045`: unit 40000 x qty 2 = 80000, line discount 5% gives `line.total` 76000, then invoice discount 5% gives 72200. There is no line-level discount plus invoice-level discount netting.

Rounding is to nearest: `INV-2026-0052` computes to `45000.0625` and reports `45000`.

Other structure:

- `quantity` is a **number, not an integer**: values `{1, 2, 2.5, 3}`. JSON encodes `2.5` as a float and `1`/`2`/`3` as integers. Same for `tax_rate` (`0` and `10` as ints, `6.25` and `8.5` as floats) and `discount_rate` (`0`, `5`, both ints). **A strict typed client must declare all three as float/decimal**, not int, even though most values serialize without a decimal point.
- Monetary amounts within a line item can be enormous: `INV-2026-0043` has `unit_price.amount = 5000000` x qty 2 = `10000000` ($100,000.00), the largest invoice in the set.
- `file_id` is **omitted** (not null) on invoices 06, 09 and 12. Every other optional invoice field is **null** when unset (`note` null on 3, `accounting_synced_at` null on 5, `payments[].external_method` null on 2, `payments[].transaction_id` null on 5, `line_items[].tax_rate` null on 10). `file_id` is the lone omission-style field on this resource.
- `due_date` is documented as "null when not set" and is **non-null on all 12**.
- `activities[]` is an append-only audit log, 2 to 7 entries (total 44), ordered oldest-first by `created_at`. `created` is always first. `activities[].emails` is an array present on all 44, empty on 32, length 1 on 10, length 2 on 2. `activities[].user_id` is null on 12 of 44 (system events) and otherwise one of the three `40000000-`-prefixed ids (§2.4).
- The activity trail is internally consistent with `status` and `accounting_sync_status` on every invoice: `cancelled` invoices have `created, cancelled` and `accounting_sync_status: skip`; `synced` invoices end with `accounting_synced`; `not_pushed` invoices have no sync activity; `overdue` invoices carry `reminder_sent`; `pending_payout` invoices carry `card_payment_received`. `INV-2026-0066` uniquely shows a reversal: `marked_as_paid` then `marked_as_unpaid` then `card_payment_received`.
- `payments[]` has 0 or 1 entries, never more. Partial payments and multi-payment invoices are untested. **`payments[].transaction_id` is populated only for `type: "received_in_account"`** (2 of 7 payments); all 5 `external` payments have a null transaction id and a non-null `external_method`. The two populated transaction ids, `019e3868-5858-7000-8000-00000000001a` and `019eebb0-0938-7000-8000-00000000000b`, both resolve into the 72-transaction set, so this is a real cross-product join and the **only** link between Invoicing and the banking ledger.
- `payments[].paid_at` is date-only (`2026-01-20`) while everything else invoice-side is a full timestamp.
- Invoice `note` values are customer-facing. One of them, on `INV-2026-0043`, is `Wire received — confirm allocation.` and contains a literal U+2014 em dash, worth knowing if you render invoice notes into a constrained encoding.
- Invoice distribution across customers: `…003` Northwind Traders 3; `…001` Acme Supplies 2; `…002` Brightleaf Design 2; `…005` Summit Analytics 2; `…004` Harbor Logistics 1; `…007` Orbit Media 1; `…008` Deleted Co 1; `…006` Cedar & Co **0**.

**`GET /invoicing/invoices/{invoice_id}/files/{file_id}` is broken in the sandbox.** All 9 invoices that expose a `file_id` were queried with exactly the id the invoice returned, and all 9 returned:

```
HTTP 404  {"type":"1303","title":"invoice file not found","status":404}
```

The documented contract is explicit that "`file_id` must match `invoice.file_id` from list or get when that field is set", which is exactly what was done. Either the fixture never seeded invoice file blobs, or the endpoint is not wired up. Contrast with the transaction file endpoint, which succeeded 16 of 16. **An integrator cannot test invoice PDF download against this sandbox at all.**

---

## 6. Envelope, pagination, sorting, filtering, errors

### 6.1 Response envelopes

- **List** responses are `{"<resource_key>": [...], "page": {"next_page_token": string|null}}`. The key is `accounts`, `cards`, `transactions`, `statements`, `customers`, `invoices`. Note `/invoicing/customers` uses the bare key `customers`, not `invoicing_customers`, and `/invoicing/invoices` uses `invoices`.
- **Detail** responses (`GET /{resource}/{id}`) are the **bare resource object with no envelope and no `page` key**. Confirmed on all 147 detail fetches across all six resources.
- **The detail surface returns exactly the same field set as the list surface** for every one of the six resources. 14/14 accounts, 8/8 cards, 72/72 transactions, 33/33 statements, 8/8 customers, 12/12 invoices: byte-identical field paths, identical presence, identical nullity. There is **no** "expanded" detail representation. The only reason to call `GET /{id}` is to refresh a signed `pdf_url`, which the statements doc tells you to do.
- Content type is `application/json` on success and `application/problem+json` per the OpenAPI spec on errors. Every response carries `via: 1.1 google`, `server: cloudflare`, `cf-cache-status: DYNAMIC`, `strict-transport-security: max-age=63072000; includeSubDomains; preload`, `x-content-type-options: nosniff`, `x-frame-options: DENY`, `referrer-policy: strict-origin-when-cross-origin`. No `x-request-id`, no `x-ratelimit-*` headers, no `etag`, no `cache-control`.

### 6.2 `page_size` bounds

Probed exhaustively on `/transactions`. Accepted: `1`..`100`. Rejected with HTTP 400 `{"type":"1317","title":"page_size must be between 1 and 100","status":400}`: `-5`, `-1`, `0`, `101`, `150`, `200`, `1000`, `10000`. The `1317` type code is Rho's validation-error code and is reused for every query-parameter problem. The documented defaults differ per endpoint (cards, customers and invoices default to 20; accounts, transactions and statements document "max 100" without stating a default), but **the enforced range is 1..100 uniformly**.

### 6.3 The cursor is not opaque, and it is not what the docs claim

`page.next_page_token` is base64url of a small JSON object, and it decodes cleanly:

```
eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qVSJ9
-> {"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":"b2Zmc2V0OjU"}
   where base64url("b2Zmc2V0OjU") = "offset:5"
```

| field | meaning |
|---|---|
| `v` | cursor format version, `1` everywhere |
| `f` | a 22-char base64url (16-byte) **filter fingerprint**, constant for a given endpoint + filter set, different for every endpoint and for every change of filters |
| `t` | base64url of the position payload |

**Two different pagination strategies coexist in one API version:**

| endpoint | `t` payload decodes to | strategy |
|---|---|---|
| `/transactions` | `offset:5` | **offset** |
| `/statements` | `offset:1` | **offset** |
| `/cards` | `offset:1` | **offset** |
| `/invoicing/customers` | `offset:1` | **offset** |
| `/invoicing/invoices` | `offset:1` | **offset** |
| `/accounts` | `{"last_id":"30000000-0000-4000-8000-000000000002","sort_by":"account_name","order":"asc"}` | **keyset** |

This directly contradicts `docs/v1/pagination`, which states: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." An offset cursor cannot provide that guarantee. Only `/accounts` uses a keyset cursor that actually can. Note also that the `/accounts` cursor reveals the endpoint's **default sort is `account_name` ascending**, which the docs never state.

Observed cursor binding rules, probed directly:

| action | result |
|---|---|
| pass a `/transactions` token to `/statements` | **400** `page_token must be a valid cursor` (the `f` fingerprint is endpoint-scoped, as documented) |
| pass a token back with a **different `page_size`** | **200**, works fine, returns 10 items starting at offset 5 |
| pass a token back with an **added filter** (`status=settled`) | **400** `page_token must be a valid cursor` |
| pass a garbage string as `page_token` | **400** `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |

So `page_size` is deliberately excluded from the fingerprint and may be changed mid-iteration; filters may not. That nuance is not in the docs.

### 6.4 Sorting: four different behaviours across six endpoints

| endpoint | validates `sort_by`? | accepted `sort_by` values | does it actually sort? | default |
|---|---|---|---|---|
| `/accounts` | **yes, 400 on unknown** | **only `balance` and `account_name`** (rejected: id, name, created_at, updated_at, amount, account_type, account_number_last_4, routing_number_last_4, type, account_balance) | yes | `account_name` asc (from the cursor payload) |
| `/invoicing/customers` | **yes, 400 on unknown** | **only `created_at`** (rejected: legal_name, email, updated_at, total_revenue, deleted_at, last_invoice_id, company_name, customer_name, revenue, total, id, name) | yes | `created_at` desc (documented) |
| `/transactions` | **no, silently ignores** | any string returns 200 | yes for `amount`, `initiated_at`, `posted_at`; `sort_by=bogus` falls back to the default | `initiated_at` desc |
| `/statements` | **no, silently ignores** | any string returns 200 | **no.** `period_end`, `period_start`, `available_at` and `bogus` all return the identical sequence. Only `order` has any effect. | `period_end` desc |
| `/cards` | **no, silently ignores** | any string returns 200 | not exercised (8 records, one page) | id order |
| `/invoicing/invoices` | **no, silently ignores** | any string returns 200 | not exercised | `created_at` desc (documented) |

`order` is validated everywhere it is accepted: only lowercase `asc` and `desc`. `ASC`, `up` and `1` all return 400 `invalid order parameter`.

The practical consequence: a typo in `sort_by` fails loudly on 2 endpoints and silently on 4. `/statements` advertises a `sort_by` parameter in its OpenAPI definition that has no observable effect at all.

### 6.5 Filter validation: equally inconsistent

| probe | result |
|---|---|
| `/cards?status=bogus` | **400** `{"type":"1317","title":"invalid status parameter: \"bogus\"","status":400}` |
| `/transactions?status=bogus` | **200**, 0 results |
| `/invoicing/invoices?status=bogus` | **200**, 0 results |
| `/transactions?account_id=00000000-0000-4000-8000-000000000000` (well-formed, unknown) | **200**, 0 results |
| `/transactions?account_id=xyz` (malformed UUID) | **400** `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: ..."}` |
| `/transactions?initiated_after=garbage` | **400**, `about:blank` form |
| `/transactions?nonsense=x` (unknown parameter) | **200**, silently ignored |
| `/cards?user_id=<unknown but well-formed>` | **200**, 0 results |

Note two distinct error body shapes for 400: the `{"type":"1317", "title":"..."}` form for enum/range/cursor problems (no `detail` key) and the RFC 9457 `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: ..."}` form for type-parse problems. The OpenAPI markdown documents only the second shape (`type`, `title`, `status`, `detail` with `Example: about:blank`), so the `1317` numeric-type variant is **undocumented**, and it omits the `detail` field the spec marks as optional but implies.

Filter semantics confirmed:

- **`min_amount` / `max_amount` compare the signed amount, not the absolute value.** `min_amount=0` returns 32 (all positives), `max_amount=0` returns 40 (all negatives), `min_amount=-100` returns 32 (there is no negative amount above -1000). The parameter docs say "Minimum amount in minor units" without mentioning sign.
- `search` on `/transactions` is case-insensitive substring: `rent` and `RENT` both return 2; `zzzz` returns 0. It matched `Monthly office rent` (memo) and did **not** match the merchant-control merchant name `Sweetgreen`, which exists only on a card, confirming the documented scope (counterparty name, memo, note).
- `search` on `/invoicing/customers` is case-insensitive and matches both `legal_name` and `email`: `acme` and `ACME` each return 1; `@deletedco` with `include_deleted=true` returns 1.
- Date filters accept both `2026-01-01` and `2026-01-01T00:00:00Z` and return the same count (47). `initiated_after` inclusive / `initiated_before` exclusive as documented.
- Array filters are OR within a parameter: `transaction_type=wire_in&transaction_type=wire_out` returns 8 (4 + 4); `user_id` with two values returns 3; `status=paid&status=unpaid` on invoices returns 6 (4 + 2); `status=active&status=locked` on cards returns 5 (4 + 1).
- `/statements?account_id=30000000-…0000007` returns 11, exactly the credit statements tied to that account, i.e. the filter behaves as a plain per-account filter in this dataset because no statement spans more than one account.

### 6.6 Rate limiting and auth, as observed

No 429 was ever triggered across roughly 300 requests paced at ~1.05 s intervals, consistent with the documented ~60 req/min per token. No `x-ratelimit` headers are returned, so a client cannot pace adaptively; it must self-throttle. The documented per-IP limit is ~600 req/min.

The literal string `sandbox` is the working bearer token for `https://rhoapi-sandbox.rho.co`. The earlier auth probe set (`rho/sandbox/probe-auth/`) covers 16 header variants.

---

## 7. How the records interlink

### 8.1 Join graph (edges actually present in the payloads)

```
users (10000000-…, 12, no endpoint)
  |  cards.cardholder.user_id           8 of 12 users hold a card
  |  transactions.user_id               12 of 12 users initiate transactions
  v
cards (20000000-…, 8)
  |  transactions.card_id               all 8 cards appear on 12 transactions
  v
transactions (UUIDv7, 72)
  |  transactions.account_id  ---------> accounts (30000000-…, 14), 11 of 14 referenced
  |  transactions.money_movement_id ---> money movements (40000000-…, 65, no endpoint)
  |  transactions.attachments[].file_id -> GET /transactions/{id}/files/{file_id}  [works]
  ^
  |  invoices.payments[].transaction_id  2 of 12 invoices reach into the ledger
  |
invoices (70000000-…, 12)
  |  invoices.customer.id -------------> customers (60000000-…, 8)
  |  invoices.file_id -----------------> GET /invoicing/invoices/{id}/files/{fid}  [404, broken]
  |  invoices.activities[].user_id ----> 40000000-… ids that resolve to NOTHING
  ^
  |  customers.last_invoice_id           7 of 8 customers point at their newest invoice
  |
statements (6-digit decimal, 33)
  |  statements.accounts[].account_id --> accounts, 5 of 14 referenced
  (no edge to transactions at all)
```

### 8.2 Referential integrity, measured

| edge | distinct refs | resolve | dangling |
|---|---:|---:|---:|
| `transactions.account_id` → accounts | 11 | 11 | 0 |
| `transactions.card_id` → cards | 8 | 8 | 0 |
| `statements.accounts[].account_id` → accounts | 5 | 5 | 0 |
| `customers.last_invoice_id` → invoices | 7 | 7 | 0 |
| `invoices.customer.id` → customers | 7 | 7 | 0 |
| `invoices.payments[].transaction_id` → transactions | 2 | 2 | 0 |
| `cards.cardholder.user_id` → transaction user ids | 8 | 8 | 0 |
| **`invoices.activities[].user_id` → transaction user ids** | **3** | **0** | **3** |

One broken edge, and it is the `40000000-` namespace collision described in §2.4.

### 8.3 Orphans and coverage gaps

| gap | detail |
|---|---|
| accounts with **no** transaction | `…005` Inventory Checking, `…008` Credit Account, `…010` Credit Account |
| accounts in **no** statement | 9 of 14: `…001`, `…002`, `…003`, `…005`, `…009`, `…010`, `…011`, `…012`, `…014` |
| customers with **no** invoice | `…006` Cedar & Co (and it is the one with null `email` and null `last_invoice_id`) |
| cards with no transaction | none; all 8 are exercised |
| users with no card | 4 of 12: `…005` Olivia Chen, `…010` Priya Shah, `…011` Grace Morgan, `…012` Andrew Collins |
| transactions with no statement covering them | all 72; there is no statement-to-transaction link in either direction |
| invoices reaching the ledger | 2 of 12 |

### 8.4 The 12 users, as reconstructable

Users are never listable. This table is assembled from `transactions.user_id` + `user_full_name` and `cards.cardholder.{user_id, first_name, last_name}`, which agree on every overlapping id.

| user_id | name | holds card | initiates transactions |
|---|---|---|---|
| `10000000-…0000001` | Ethan Parker | card `…001` (virtual, active) | yes |
| `10000000-…0000002` | Maya Thompson | card `…002` (physical, active) | yes |
| `10000000-…0000003` | Daniel Rivera | card `…003` (virtual, active) | yes |
| `10000000-…0000004` | Lucas Bennett | card `…004` (physical, locked) | yes |
| `10000000-…0000005` | Olivia Chen | no | yes |
| `10000000-…0000006` | Sofia Martin | card `…005` (physical, active) | yes |
| `10000000-…0000007` | Hannah Brooks | card `…006` (virtual, suspended) | yes |
| `10000000-…0000008` | Emma Walsh | card `…007` (virtual, canceled) | yes |
| `10000000-…0000009` | Claire Mitchell | card `…008` (physical, expired) | yes |
| `10000000-…0000010` | Priya Shah | no | yes |
| `10000000-…0000011` | Grace Morgan | no | yes |
| `10000000-…0000012` | Andrew Collins | no | yes |

There is **no user id 10000000-…0000005 holding a card**, and card ids are not offset-aligned with user ids: card `…005` belongs to user `…006`, card `…006` to user `…007`, and so on from card 05 onward. Do not infer the mapping from the counters.

---

## 8. Contradictions between the docs and the sandbox

Every row below is a case where the local `docs.rho.co` corpus asserts something the live sandbox does not do. None of these is a Rho marketing claim; they are all developer-documentation claims, so the label is "doc says" rather than "[Rho claim]".

| # | doc source | doc says | sandbox does |
|---|---|---|---|
| 1 | `api/statements_liststatements.md` | `accounts[].account_id` is "Null for credit statements" | **never null**; all 22 credit statements carry a real credit account id |
| 2 | same | `accounts[]` may span multiple checking/savings accounts | length is **1** on all 33; two same-period statements (`439950`, `439951`) exist as separate records instead |
| 3 | same | `accounts[].repayment_date` exists for credit statements | **never present** on any of the 22 |
| 4 | same | `pdf_url` may be null | **never null** on any of the 33 |
| 5 | `api/transactions_listtransactions.md` | `posted_at` is "Null while status is pending" | present on **both** pending records; absent only on the one `awaiting_approval` record. Also absent, never null |
| 6 | same | `user_id` / `user_full_name` "Null for system-initiated transactions" | key is **omitted**, never null |
| 7 | same | `note` is user-editable, `memo` arrives from the bank | **byte-identical on 37 of 39** records that have them; they are also present or absent strictly together |
| 8 | same | `tracking_number` carries ACH trace / wire IMAD/OMAD | **never present** on any of 72, including 11 ACH and 10 wire records |
| 9 | same | `counterparty_logo_url` | **never present** |
| 10 | `api/cards_listcards.md` | `spending_limit`, `spending_limit_type`, `current_spend` are null when the card has no limit | **never null**; no limitless card exists |
| 11 | `api/invoicing_listinvoicinginvoices.md` | `due_date` is "null when not set" | **never null** on any of 12 |
| 12 | `api/invoicing_getinvoicinginvoicefile.md` | `file_id` "must match invoice.file_id from list or get when that field is set" | doing exactly that returns **404 on all 9** |
| 13 | `api/invoicing_listinvoicingcustomers.md` | `email` and `last_invoice_id` marked `required` | both **null** on customer `…006` |
| 14 | `docs/v1/pagination` | "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages" | 5 of 6 endpoints return a plain **`offset:N`** cursor, which cannot satisfy that; only `/accounts` uses keyset |
| 15 | `docs/v1/pagination` | cursor is "opaque"; "their format ... may change without notice" | it is base64url JSON with a `v:1` version marker and a human-readable payload |
| 16 | `docs/v1/versioning` | "Treat IDs as opaque strings. Do not parse structure out of an `id`" | ids are heavily structured; more importantly **`statements.id` is a 6-digit decimal, not a UUID**, which the docs never say anywhere |
| 17 | `api/statements_liststatements.md` (query params) | `sort_by` is a documented query parameter | it has **no observable effect**; only `order` does |
| 18 | `api/v1/openapi` error schema | 400 bodies are `{type, title, status, detail}` with `type` example `about:blank` | most 400s return `{"type":"1317","title":"...","status":400}` with **no `detail`** and a numeric type code |

Additionally, the docs' markdown export **omits the sub-fields** of `cards.current_spend`, `cards.pending_spend`, `cards.shipping_address`, `cards.allowed_categories` and `cards.allowed_merchants`. Their shapes are recoverable only from the live sandbox (§5.2).

---

## 9. What is conspicuously absent from the entire surface

Not "undocumented", but **not present at all**, across docs and sandbox:

- **Any write operation.** Every one of the 14 documented operations is a `GET`. The five OAuth scopes are all `:read` (`accounts:read`, `cards:read`, `invoicing:read`, `statements:read`, `transactions:read`). There is no scope, endpoint or schema for initiating a payment, creating a card, issuing an invoice, or updating a note. The API is read-only.
- **Webhooks or any push mechanism.** `GET /webhooks` is a 404. There is no `events`, `subscriptions` or notification concept anywhere in the corpus. Every integration must poll, inside a ~60 req/min budget, against list endpoints whose cursors are offsets.
- **A users/employees endpoint.** 12 user ids are referenced by two resources and resolvable by neither. You can never turn `10000000-…0000010` into "Priya Shah" unless she happens to have initiated a transaction you can see.
- **A counterparties/vendors endpoint.** `counterparty_name` is a bare string on a transaction with no id, so counterparties cannot be deduplicated or joined.
- **A money-movement endpoint.** `money_movement_id` groups legs but has no `GET /money-movements/{id}`.
- **A business/organization endpoint.** No legal entity, no EIN, no address, no entitlements.
- **Multi-currency.** One currency in the entire dataset, no FX fields, and `international_wire_in` and `international_wire_fee_refund` are never produced.
- **Any balance other than `balance`.** No available balance, no credit limit, no pending balance, no interest rate, no APY, no yield, despite treasury and savings being marketed products.
- **Any link from a statement to the transactions it covers**, in either direction.
- **Any `created_at`/`updated_at` on accounts, cards, transactions or statements.** Only the two Invoicing resources carry audit timestamps. You cannot do incremental sync by `updated_at` on the banking side; the only ordering keys are `initiated_at`/`posted_at` on transactions and `period_end` on statements.
- **Any idempotency, ETag, or `x-request-id` header**, so a support escalation has no request identifier to quote.
- **`x-ratelimit-*` headers**, so throttling has to be open-loop.
- **Pagination metadata other than the cursor.** No `total_count`, no `has_more`, no page number. You cannot show "1-20 of 347" without draining the list.

---

## 10. Practical checklist for an integrator

1. **Type `statements.id` as a string and never as a UUID.** It is a 6-digit decimal in the sandbox and nothing in the docs says otherwise for production.
2. **Handle key omission, not just null, on transactions.** `posted_at`, `memo`, `note`, `user_id`, `user_full_name`, `card_id`, `card_name` are absent, never null. On invoicing customers the opposite convention applies: always present, sometimes null. Cards mix both (`shipping_address` null, merchant controls omitted; `file_id` omitted on invoices while everything else on that resource is nulled).
3. **Read direction from the sign of `amount.amount`, never from the type name.** `adjustment_credit` is negative and `adjustment_debit` is positive in this dataset.
4. **Branch statement math on `statement_type`.** Credit: `closing = opening + spending + repayments` with spending positive. Deposit and treasury: `closing = opening + total_credits - total_debits - total_fees`, with `spending`/`repayments`/`cashback` absent.
5. **Do not reconcile balances to the transaction list.** They do not tie in the sandbox and the sandbox does not claim they should.
6. **Group by `money_movement_id` before presenting transfers**, or you will double-count every internal transfer and credit repayment. 7 of 65 movements have 2 legs that sum to zero.
7. **Declare `quantity`, `tax_rate` and `discount_rate` as decimals**, not integers. `2.5`, `6.25` and `8.5` all occur.
8. **Treat a null `line_items[].tax_rate` as "inherit the invoice `tax_rate`"**, not as zero, or every multi-rate invoice total will be wrong.
9. **Keep `page_size` constant is not required, but keep filters constant is.** Changing a filter mid-iteration returns 400; changing `page_size` does not.
10. **Give every `switch` on an enum a default branch.** The sandbox exercises only 22 of 33 transaction types, 5 of 11 card statuses and 3 of 7 spending-limit types, so a client that passes sandbox tests has never seen a third of the values production can return, including the entire treasury transaction family.
11. **Watch the two "cancelled" spellings.** `cards.status` uses `canceled`; `invoices.status` and `activities[].activity_type` use `cancelled`.
12. **Watch the two country encodings and two address models.** `customers.address.country` is `"USA"` (alpha-3) with `address1/address2/state/zip_code`; `cards.billing_address.country_code` is `"US"` (alpha-2) with `street/second_line/subdivision/postal_code`.
13. **Re-fetch signed URLs, never cache them.** `X-Goog-Expires=899` on every statement PDF and transaction attachment, regenerated per request.
14. **Do not build invoice-PDF download against the sandbox.** It 404s on all 9 invoices that advertise a `file_id`.
15. **Do not join invoice activities to users.** Their `user_id`s sit in the `40000000-` namespace and resolve to nothing.

---

## 11. Appendix: generated field-path census (full tables)

Produced by `rho/sandbox/census2.py`. Reading the table:

- **`present`** is `occurrences of the key / occurrences of its containing object`. A ratio below 1.0 means the key is **omitted** on some records, which is a different failure mode from null and the single most important signal for an integrator writing a deserializer.
- **`null`** counts records where the key is present with a JSON `null` value.
- **`n distinct` / `observed values`** gives the complete value set whenever cardinality is low enough to print. For a low-cardinality string field, that set **is** the real enum as the sandbox exercises it (compare against §4 for the documented enum).
- List and detail columns are reported separately so that any divergence between the two surfaces would show up. None does.

| resource | list records | detail records | distinct field paths |
|---|---|---|---|
| accounts | 14 | 14 | 8 |
| cards | 8 | 8 | 47 |
| transactions | 72 | 72 | 22 |
| statements | 33 | 33 | 33 |
| invoicing_customers | 8 | 8 | 19 |
| invoicing_invoices | 12 | 12 | 39 |


### `accounts` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `account_name` | string | 14/14 | 0 | 14/14 | 0 | 8 | `Cash (Checking)`, `Credit Account`, `Inventory Checking`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_number_last_4` | string | 8/14 | 0 | 8/14 | 0 | 8 | `0106`, `2513`, `3214`, `3608`, `4609`, `5702`, `7301`, `9508` |
| `account_type` | string | 14/14 | 0 | 14/14 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `balance` | object | 14/14 | 0 | 14/14 | 0 | 0 |  |
| `balance.amount` | int | 14/14 | 0 | 14/14 | 0 | 6 | `0`, `1046`, `811970`, `876138`, `8711697`, `15460929` |
| `balance.currency` | string | 14/14 | 0 | 14/14 | 0 | 1 | `USD` |
| `id` | string | 14/14 | 0 | 14/14 | 0 | 14 | `30000000-0000-4000-8000-000000000001`, `30000000-0000-4000-8000-000000000002`, `30000000-0000-4000-8000-000000000003`, `30000000-0000-4000-8000-000000000004`, `30000000-0000-4000-8000-000000000005`, `30000000-0000-4000-8000-000000000006`, `30000000-0000-4000-8000-000000000007`, `30000000-0000-4000-8000-000000000008`, `30000000-0000-4000-8000-000000000009`, `30000000-0000-4000-8000-000000000010`, `30000000-0000-4000-8000-000000000011`, `30000000-0000-4000-8000-000000000012`, `30000000-0000-4000-8000-000000000013`, `30000000-0000-4000-8000-000000000014` |
| `routing_number_last_4` | string | 8/14 | 0 | 8/14 | 0 | 1 | `0089` |

### `cards` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `allowed_categories` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `allowed_categories[].code` | string | 1/1 | 0 | 1/1 | 0 | 1 | `5812` |
| `allowed_categories[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Eating places and restaurants` |
| `allowed_merchants` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `allowed_merchants[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Sweetgreen` |
| `billing_address` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `billing_address.city` | string | 8/8 | 0 | 8/8 | 0 | 4 | `Austin`, `Boston`, `Chicago`, `New York` |
| `billing_address.country_code` | string | 8/8 | 0 | 8/8 | 0 | 1 | `US` |
| `billing_address.postal_code` | string | 8/8 | 0 | 8/8 | 0 | 7 | `02116`, `10001`, `10005`, `10011`, `10118`, `60601`, `78701` |
| `billing_address.second_line` | string | 1/8 | 0 | 1/8 | 0 | 1 | `Floor 5` |
| `billing_address.street` | string | 8/8 | 0 | 8/8 | 0 | 8 | `1 Main St`, `10 Hudson Yards`, `100 Broadway`, `200 State St`, `350 Fifth Ave`, `45 W 18th St`, `500 Boylston St`, `88 Pine St` |
| `billing_address.subdivision` | string | 8/8 | 0 | 8/8 | 0 | 4 | `IL`, `MA`, `NY`, `TX` |
| `blocked_categories` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `blocked_categories[].code` | string | 1/1 | 0 | 1/1 | 0 | 1 | `0742` |
| `blocked_categories[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Veterinary services` |
| `blocked_merchants` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `blocked_merchants[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Petco` |
| `cardholder` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `cardholder.first_name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Claire`, `Daniel`, `Emma`, `Ethan`, `Hannah`, `Lucas`, `Maya`, `Sofia` |
| `cardholder.last_name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Bennett`, `Brooks`, `Martin`, `Mitchell`, `Parker`, `Rivera`, `Thompson`, `Walsh` |
| `cardholder.user_id` | string | 8/8 | 0 | 8/8 | 0 | 8 | `10000000-0000-4000-8000-000000000001`, `10000000-0000-4000-8000-000000000002`, `10000000-0000-4000-8000-000000000003`, `10000000-0000-4000-8000-000000000004`, `10000000-0000-4000-8000-000000000006`, `10000000-0000-4000-8000-000000000007`, `10000000-0000-4000-8000-000000000008`, `10000000-0000-4000-8000-000000000009` |
| `current_spend` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `current_spend.amount` | int | 8/8 | 0 | 8/8 | 0 | 8 | `0`, `1750`, `5331`, `6331`, `6797`, `45000`, `121827`, `1622132` |
| `current_spend.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `id` | string | 8/8 | 0 | 8/8 | 0 | 8 | `20000000-0000-4000-8000-000000000001`, `20000000-0000-4000-8000-000000000002`, `20000000-0000-4000-8000-000000000003`, `20000000-0000-4000-8000-000000000004`, `20000000-0000-4000-8000-000000000005`, `20000000-0000-4000-8000-000000000006`, `20000000-0000-4000-8000-000000000007`, `20000000-0000-4000-8000-000000000008` |
| `last_4` | string | 8/8 | 0 | 8/8 | 0 | 8 | `0042`, `1184`, `1846`, `3150`, `6603`, `7291`, `7732`, `9027` |
| `name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Claire Mitchell`, `Daniel Rivera`, `Emma Walsh Virtual Card`, `Ethan Parker`, `Hannah Brooks`, `Lucas Bennett`, `Maya Thompson`, `Sofia Martin Physical Card` |
| `pending_spend` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `pending_spend.amount` | int | 8/8 | 0 | 8/8 | 0 | 7 | `0`, `250`, `400`, `900`, `1500`, `8000`, `50000` |
| `pending_spend.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `shipping_address` | null+object | 8/8 | 4 | 8/8 | 4 | 0 |  |
| `shipping_address.city` | string | 4/4 | 0 | 4/4 | 0 | 4 | `Austin`, `Chicago`, `New York`, `San Francisco` |
| `shipping_address.country_code` | string | 4/4 | 0 | 4/4 | 0 | 1 | `US` |
| `shipping_address.postal_code` | string | 4/4 | 0 | 4/4 | 0 | 4 | `10118`, `60601`, `78701`, `94102` |
| `shipping_address.second_line` | string | 4/4 | 0 | 4/4 | 0 | 4 | `Apt 4B`, `Floor 20`, `Suite 200`, `Unit 12` |
| `shipping_address.street` | string | 4/4 | 0 | 4/4 | 0 | 4 | `1 Main St`, `200 State St`, `350 Fifth Ave`, `800 Market St` |
| `shipping_address.subdivision` | string | 4/4 | 0 | 4/4 | 0 | 4 | `CA`, `IL`, `NY`, `TX` |
| `spend_period_end` | null+string | 8/8 | 1 | 8/8 | 1 | 2 | `2026-09-10T04:00:00Z`, `2026-10-01T04:00:00Z` |
| `spend_period_start` | string | 8/8 | 0 | 8/8 | 0 | 3 | `2025-03-01T12:00:00Z`, `2026-09-01T04:00:00Z`, `2026-09-09T04:00:00Z` |
| `spending_limit` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `spending_limit.amount` | int | 8/8 | 0 | 8/8 | 0 | 7 | `75000`, `100000`, `150000`, `200000`, `250000`, `500000`, `2500000` |
| `spending_limit.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `spending_limit_type` | string | 8/8 | 0 | 8/8 | 0 | 3 | `daily`, `fixed`, `monthly` |
| `status` | string | 8/8 | 0 | 8/8 | 0 | 5 | `active`, `canceled`, `expired`, `locked`, `suspended` |
| `type` | string | 8/8 | 0 | 8/8 | 0 | 2 | `physical`, `virtual` |
| `usage_ends_at` | null+string | 8/8 | 5 | 8/8 | 5 | 2 | `2026-06-30T23:59:59Z`, `2026-09-01T00:00:00Z` |
| `usage_starts_at` | null+string | 8/8 | 7 | 8/8 | 7 | 1 | `2025-10-01T09:00:00Z` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `allowed_categories` | len 1 x1 |
| `allowed_merchants` | len 1 x1 |
| `blocked_categories` | len 1 x1 |
| `blocked_merchants` | len 1 x1 |

### `transactions` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `account_id` | string | 72/72 | 0 | 72/72 | 0 | 11 | `30000000-0000-4000-8000-000000000001`, `30000000-0000-4000-8000-000000000002`, `30000000-0000-4000-8000-000000000003`, `30000000-0000-4000-8000-000000000004`, `30000000-0000-4000-8000-000000000006`, `30000000-0000-4000-8000-000000000007`, `30000000-0000-4000-8000-000000000009`, `30000000-0000-4000-8000-000000000011`, `30000000-0000-4000-8000-000000000012`, `30000000-0000-4000-8000-000000000013`, `30000000-0000-4000-8000-000000000014` |
| `account_name` | string | 72/72 | 0 | 72/72 | 0 | 7 | `Cash (Checking)`, `Credit Account`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_type` | string | 72/72 | 0 | 72/72 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `amount` | object | 72/72 | 0 | 72/72 | 0 | 0 |  |
| `amount.amount` | int | 72/72 | 0 | 72/72 | 0 | 64 | 64 distinct, min `-5900000` max `130000000` |
| `amount.currency` | string | 72/72 | 0 | 72/72 | 0 | 1 | `USD` |
| `attachments` | array | 72/72 | 0 | 72/72 | 0 | 0 |  |
| `attachments[].file_id` | string | 16/16 | 0 | 16/16 | 0 | 15 | `104c1de5-dcd3-429d-933e-d61fd076a55c`, `11afe478-b02d-4d88-a774-1e85b434eeee`, `1b6d9736-a62c-48ab-972c-804fb4a7210f`, `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15`, `3f33ab1e-8bb7-4d9e-baf3-633da9e49fd9`, `5557f9f5-74ea-4d12-9fb8-e6483f17c08c`, `5abcd54c-9726-412c-a315-500b007a6263`, `602581d9-13e9-4aaa-a227-55645354bdf8`, `6c086ad1-67c5-408e-b2c7-7766178b2211`, `7de7495f-e0d3-4ada-a79d-6074e745dc33`, `8191a1bf-5585-45a4-8950-381e71835547`, `8c284ea9-bbcb-4d71-8074-0f6fb93d224d`, `8d073098-e509-4fe3-940b-ab22de36fe7a`, `af1456af-1428-4845-8b03-9c98e098ec18`, `cdc328c1-c3a3-4670-a371-28e34891ee68` |
| `attachments[].file_name` | string | 16/16 | 0 | 16/16 | 0 | 15 | `car-service-itinerary.pdf`, `car-service-receipt.pdf`, `checking-repayment-confirmation.pdf`, `cloudbridge-invoice.pdf`, `credit-repayment-receipt.pdf`, `credit-repayment-statement.pdf`, `credit-repayment-summary.pdf`, `office-supply-invoice.pdf`, `office-supply-receipt.pdf`, `parking-receipt.pdf`, `repayment-confirmation.pdf`, `repayment-details.csv`, `rewards-cashback-notice.pdf`, `rewards-redemption-confirmation.pdf`, `software-invoice.pdf` |
| `card_id` | string | 12/72 | 0 | 12/72 | 0 | 8 | `20000000-0000-4000-8000-000000000001`, `20000000-0000-4000-8000-000000000002`, `20000000-0000-4000-8000-000000000003`, `20000000-0000-4000-8000-000000000004`, `20000000-0000-4000-8000-000000000005`, `20000000-0000-4000-8000-000000000006`, `20000000-0000-4000-8000-000000000007`, `20000000-0000-4000-8000-000000000008` |
| `card_name` | string | 12/72 | 0 | 12/72 | 0 | 8 | `Claire Mitchell`, `Daniel Rivera`, `Emma Walsh Virtual Card`, `Ethan Parker`, `Hannah Brooks`, `Lucas Bennett`, `Maya Thompson`, `Sofia Martin Physical Card` |
| `counterparty_name` | string | 72/72 | 0 | 72/72 | 0 | 37 | 37 distinct, `Aaron Blake` … `Zurich Airport Services` |
| `id` | string | 72/72 | 0 | 72/72 | 0 | 72 | 72 distinct, `018870b5-c260-7000-8000-000000000045` … `019f0554-0bf0-7000-8000-00000000000a` |
| `initiated_at` | string | 72/72 | 0 | 72/72 | 0 | 67 | 67 distinct, `2023-05-31T07:29:00Z` … `2026-06-26T19:07:02Z` |
| `memo` | string | 39/72 | 0 | 39/72 | 0 | 25 | `Contractor hours`, `Correction of encoding error regarding check number 100245`, `Daily credit repayment for date 2026/06/23`, `Daily credit repayment for date 2026/06/24`, `Inventory restock`, `Invoice 317 - consulting services`, `Invoice 317 - production hours`, `MONEY TRANSFER`, `Monthly office rent`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00`, `One day Credit refund for date: 2024-03-19 00:00:28.648131-04:00`, `PAY1001984`, `PAY1002456`, `Q3 freight invoice`, `Rewards cashback`, `SC - 2509 - desk mat shipping`, `SC-2509 desk mat order`, `Severance payment`, `Swift OUR fee`, `Transfer to external account`, `Wire fee`, `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle`, `[INVALID_RECEIVING_ROUTING_NUMBER] Vendor payment`, `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`, `note: Inventory purchase closing, reason: Inventory purchase closing, ref: Inventory purchase closing` |
| `money_movement_id` | string | 72/72 | 0 | 72/72 | 0 | 65 | 65 distinct, `40000000-0000-4000-8000-000000000001` … `40000000-0000-4000-8000-000000000065` |
| `note` | string | 39/72 | 0 | 39/72 | 0 | 25 | `Contractor hours`, `Correction of encoding error regarding check number 100245`, `Daily credit repayment for date 2026/06/23`, `Daily credit repayment for date 2026/06/24`, `Inventory restock`, `Invoice 317 - consulting services`, `Invoice 317 - production hours`, `MONEY TRANSFER`, `Monthly office rent`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00`, `One day Credit refund for date: 2024-03-19 00:00:28.648131-04:00`, `PAY1001984`, `PAY1002456`, `Q3 freight invoice`, `Rewards cashback`, `SC - 2509 - desk mat shipping`, `SC-2509 desk mat order`, `Severance payment`, `Swift OUR fee`, `Transfer to external account`, `Wire fee`, `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle, Error: Invalid receiving routing number.`, `[INVALID_RECEIVING_ROUTING_NUMBER] Vendor payment, Error: Invalid receiving routing number.`, `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`, `note: Inventory purchase closing, reason: Inventory purchase closing, ref: Inventory purchase closing` |
| `posted_at` | string | 71/72 | 0 | 71/72 | 0 | 65 | 65 distinct, `2023-05-31T07:30:00Z` … `2026-06-27T19:13:15Z` |
| `status` | string | 72/72 | 0 | 72/72 | 0 | 4 | `awaiting_approval`, `failed`, `pending`, `settled` |
| `transaction_type` | string | 72/72 | 0 | 72/72 | 0 | 22 | `ach_credit`, `ach_debit`, `ach_return`, `adjustment_credit`, `adjustment_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `credit_repayment`, `credit_repayment_refund`, `internal_transfer`, `international_wire_fee`, `international_wire_out`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`, `wire_out` |
| `user_full_name` | string | 38/72 | 0 | 38/72 | 0 | 12 | `Andrew Collins`, `Claire Mitchell`, `Daniel Rivera`, `Emma Walsh`, `Ethan Parker`, `Grace Morgan`, `Hannah Brooks`, `Lucas Bennett`, `Maya Thompson`, `Olivia Chen`, `Priya Shah`, `Sofia Martin` |
| `user_id` | string | 38/72 | 0 | 38/72 | 0 | 12 | `10000000-0000-4000-8000-000000000001`, `10000000-0000-4000-8000-000000000002`, `10000000-0000-4000-8000-000000000003`, `10000000-0000-4000-8000-000000000004`, `10000000-0000-4000-8000-000000000005`, `10000000-0000-4000-8000-000000000006`, `10000000-0000-4000-8000-000000000007`, `10000000-0000-4000-8000-000000000008`, `10000000-0000-4000-8000-000000000009`, `10000000-0000-4000-8000-000000000010`, `10000000-0000-4000-8000-000000000011`, `10000000-0000-4000-8000-000000000012` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `attachments` | len 0 x58, len 1 x12, len 2 x2 |

### `statements` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `accounts` | array | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].account_id` | string | 33/33 | 0 | 33/33 | 0 | 5 | `30000000-0000-4000-8000-000000000004`, `30000000-0000-4000-8000-000000000006`, `30000000-0000-4000-8000-000000000007`, `30000000-0000-4000-8000-000000000008`, `30000000-0000-4000-8000-000000000013` |
| `accounts[].account_type` | string | 33/33 | 0 | 33/33 | 0 | 4 | `checking`, `credit`, `savings`, `treasury` |
| `accounts[].cashback` | object | 22/33 | 0 | 22/33 | 0 | 0 |  |
| `accounts[].cashback.amount` | int | 22/22 | 0 | 22/22 | 0 | 19 | `-327`, `-1`, `0`, `25`, `27`, `37`, `63`, `75`, `82`, `231`, `258`, `272`, `282`, `470`, `760`, `1039`, `32482`, `78857`, `103965` |
| `accounts[].cashback.currency` | string | 22/22 | 0 | 22/22 | 0 | 1 | `USD` |
| `accounts[].closing_balance` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].closing_balance.amount` | int | 33/33 | 0 | 33/33 | 0 | 14 | `0`, `1700`, `18910`, `24410`, `39810`, `90522`, `109322`, `127480`, `972409`, `985900`, `5384647`, `5453868`, `7550175`, `12315685` |
| `accounts[].closing_balance.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].opening_balance` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].opening_balance.amount` | int | 33/33 | 0 | 33/33 | 0 | 13 | `0`, `1700`, `18910`, `24410`, `39810`, `90522`, `109322`, `127480`, `946209`, `991900`, `5384647`, `5453868`, `7550175` |
| `accounts[].opening_balance.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].repayments` | object | 22/33 | 0 | 22/33 | 0 | 0 |  |
| `accounts[].repayments.amount` | int | 22/22 | 0 | 22/22 | 0 | 10 | `-2165638`, `-69221`, `-37600`, `-6000`, `-5100`, `-3000`, `-2191`, `0`, `100`, `26200` |
| `accounts[].repayments.currency` | string | 22/22 | 0 | 22/22 | 0 | 1 | `USD` |
| `accounts[].spending` | object | 22/33 | 0 | 22/33 | 0 | 0 |  |
| `accounts[].spending.amount` | int | 22/22 | 0 | 22/22 | 0 | 19 | `-26200`, `-100`, `0`, `1700`, `2191`, `3000`, `5100`, `5500`, `6000`, `15400`, `17210`, `18158`, `18800`, `37600`, `50712`, `69331`, `2165528`, `5257167`, `6931038` |
| `accounts[].spending.currency` | string | 22/22 | 0 | 22/22 | 0 | 1 | `USD` |
| `accounts[].total_credits` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].total_credits.amount` | int | 33/33 | 0 | 33/33 | 0 | 2 | `0`, `26200` |
| `accounts[].total_credits.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].total_debits` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].total_debits.amount` | int | 33/33 | 0 | 33/33 | 0 | 2 | `0`, `6000` |
| `accounts[].total_debits.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].total_fees` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].total_fees.amount` | int | 33/33 | 0 | 33/33 | 0 | 1 | `0` |
| `accounts[].total_fees.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `available_at` | string | 33/33 | 0 | 33/33 | 0 | 32 | 32 distinct, `2024-08-01T04:02:00Z` … `2026-06-05T21:16:51Z` |
| `id` | string | 33/33 | 0 | 33/33 | 0 | 33 | 33 distinct, `152980` … `572981` |
| `pdf_url` | string | 33/33 | 0 | 33/33 | 0 | n/a | signed GCS URL, see §PDF analysis |
| `period_end` | string | 33/33 | 0 | 33/33 | 0 | 29 | `2024-07-31`, `2024-08-31`, `2024-09-30`, `2024-10-31`, `2024-11-30`, `2024-12-31`, `2025-01-31`, `2025-02-28`, `2025-03-31`, `2025-04-30`, `2025-05-31`, `2025-06-12`, `2025-07-12`, `2025-08-12`, `2025-09-12`, `2025-10-12`, `2025-11-12`, `2025-11-30`, `2025-12-12`, `2025-12-31`, `2026-01-12`, `2026-01-31`, `2026-02-12`, `2026-02-28`, `2026-03-12`, `2026-03-31`, `2026-04-12`, `2026-04-30`, `2026-05-31` |
| `period_start` | string | 33/33 | 0 | 33/33 | 0 | 29 | `2024-07-01`, `2024-08-01`, `2024-09-01`, `2024-10-01`, `2024-11-01`, `2024-12-01`, `2025-01-01`, `2025-02-01`, `2025-03-01`, `2025-04-01`, `2025-05-01`, `2025-05-13`, `2025-06-13`, `2025-07-13`, `2025-08-13`, `2025-09-13`, `2025-10-13`, `2025-11-01`, `2025-11-13`, `2025-12-01`, `2025-12-13`, `2026-01-01`, `2026-01-13`, `2026-02-01`, `2026-02-13`, `2026-03-01`, `2026-03-13`, `2026-04-01`, `2026-05-01` |
| `statement_type` | string | 33/33 | 0 | 33/33 | 0 | 3 | `account`, `credit`, `treasury` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `accounts` | len 1 x33 |

### `invoicing_customers` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `address` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `address.address1` | string | 8/8 | 0 | 8/8 | 0 | 8 | `1 Contoso Way`, `100 Crosby St`, `12 Maple Lane`, `200 Market St`, `450 Pier Ave`, `77 Broadway`, `88 Mission St`, `9 Archive Rd` |
| `address.address2` | string | 8/8 | 0 | 8/8 | 0 | 3 | `<empty string>`, `Floor 2`, `Suite 400` |
| `address.city` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Austin`, `Boston`, `Chicago`, `New York`, `Portland`, `Redmond`, `San Francisco`, `Seattle` |
| `address.country` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USA` |
| `address.state` | string | 8/8 | 0 | 8/8 | 0 | 7 | `CA`, `IL`, `MA`, `NY`, `OR`, `TX`, `WA` |
| `address.zip_code` | string | 8/8 | 0 | 8/8 | 0 | 8 | `02109`, `10012`, `60601`, `78701`, `94105`, `97201`, `98052`, `98101` |
| `cc_emails` | array | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `created_at` | string | 8/8 | 0 | 8/8 | 0 | 8 | `2026-01-10T09:00:00Z`, `2026-01-15T10:00:00Z`, `2026-02-01T09:30:00Z`, `2026-02-20T14:00:00Z`, `2026-03-05T16:45:00Z`, `2026-03-18T11:00:00Z`, `2026-04-01T08:00:00Z`, `2026-04-12T13:20:00Z` |
| `deleted_at` | null+string | 8/8 | 7 | 8/8 | 7 | 1 | `2026-05-01T12:00:00Z` |
| `email` | null+string | 8/8 | 1 | 8/8 | 1 | 7 | `accounts@orbitmedia.co`, `billing@harborlogistics.com`, `contact@summitanalytics.io`, `gone@deletedco.example`, `hello@brightleaf.design`, `info@acmesupplies.com`, `orders@northwind.example` |
| `id` | string | 8/8 | 0 | 8/8 | 0 | 8 | `60000000-0000-4000-8000-000000000001`, `60000000-0000-4000-8000-000000000002`, `60000000-0000-4000-8000-000000000003`, `60000000-0000-4000-8000-000000000004`, `60000000-0000-4000-8000-000000000005`, `60000000-0000-4000-8000-000000000006`, `60000000-0000-4000-8000-000000000007`, `60000000-0000-4000-8000-000000000008` |
| `last_invoice_id` | null+string | 8/8 | 1 | 8/8 | 1 | 7 | `70000000-0000-4000-8000-000000000002`, `70000000-0000-4000-8000-000000000003`, `70000000-0000-4000-8000-000000000006`, `70000000-0000-4000-8000-000000000008`, `70000000-0000-4000-8000-000000000010`, `70000000-0000-4000-8000-000000000011`, `70000000-0000-4000-8000-000000000012` |
| `legal_name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Acme Supplies`, `Brightleaf Design`, `Cedar & Co`, `Deleted Co`, `Harbor Logistics LLC`, `Northwind Traders`, `Orbit Media Group`, `Summit Analytics` |
| `note` | null+string | 8/8 | 4 | 8/8 | 4 | 4 | `Large volume account`, `Preferred Net 30 customer`, `Quarterly retainer`, `Soft-deleted fixture customer` |
| `total_revenue` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `total_revenue.amount` | int | 8/8 | 0 | 8/8 | 0 | 5 | `0`, `5000`, `43400`, `108403`, `156750` |
| `total_revenue.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `updated_at` | string | 8/8 | 0 | 8/8 | 0 | 8 | `2026-04-01T08:00:00Z`, `2026-05-01T12:00:00Z`, `2026-06-30T10:00:00Z`, `2026-06-30T17:00:00Z`, `2026-07-01T08:30:00Z`, `2026-07-10T12:30:00Z`, `2026-07-18T09:00:00Z`, `2026-07-24T16:00:00Z` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `cc_emails` | len 0 x4, len 1 x2, len 2 x2 |

### `invoicing_invoices` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `accounting_sync_status` | string | 12/12 | 0 | 12/12 | 0 | 5 | `error`, `not_pushed`, `object_changed`, `skip`, `synced` |
| `accounting_synced_at` | null+string | 12/12 | 5 | 12/12 | 5 | 7 | `2026-01-20T10:00:00Z`, `2026-05-18T00:07:03Z`, `2026-05-20T09:00:00Z`, `2026-06-21T20:00:00Z`, `2026-06-28T16:00:00Z`, `2026-07-18T09:00:00Z`, `2026-07-24T11:00:00Z` |
| `activities` | array | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `activities[].activity_type` | string | 44/44 | 0 | 44/44 | 0 | 11 | `accounting_synced`, `cancelled`, `card_payment_received`, `created`, `downloaded`, `marked_as_paid`, `marked_as_unpaid`, `matched`, `payment_accounting_synced`, `reminder_sent`, `sent` |
| `activities[].created_at` | string | 44/44 | 0 | 44/44 | 0 | 40 | 40 distinct, `2026-01-15T10:00:00Z` … `2026-07-24T11:00:00Z` |
| `activities[].emails` | array | 44/44 | 0 | 44/44 | 0 | 0 |  |
| `activities[].user_id` | null+string | 44/44 | 12 | 44/44 | 12 | 3 | `40000000-0000-4000-8000-000000000001`, `40000000-0000-4000-8000-000000000002`, `40000000-0000-4000-8000-000000000003` |
| `created_at` | string | 12/12 | 0 | 12/12 | 0 | 12 | `2026-01-15T10:00:00Z`, `2026-01-16T14:32:07Z`, `2026-05-01T09:15:00Z`, `2026-05-01T10:00:00Z`, `2026-05-10T12:00:00Z`, `2026-05-15T08:00:00Z`, `2026-06-01T11:00:00Z`, `2026-06-20T15:00:00Z`, `2026-06-30T10:00:00Z`, `2026-07-01T08:30:00Z`, `2026-07-01T14:32:07Z`, `2026-07-10T09:00:00Z` |
| `customer` | object | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `customer.id` | string | 12/12 | 0 | 12/12 | 0 | 7 | `60000000-0000-4000-8000-000000000001`, `60000000-0000-4000-8000-000000000002`, `60000000-0000-4000-8000-000000000003`, `60000000-0000-4000-8000-000000000004`, `60000000-0000-4000-8000-000000000005`, `60000000-0000-4000-8000-000000000007`, `60000000-0000-4000-8000-000000000008` |
| `date` | string | 12/12 | 0 | 12/12 | 0 | 10 | `2026-01-15`, `2026-01-16`, `2026-05-01`, `2026-05-10`, `2026-05-15`, `2026-06-01`, `2026-06-20`, `2026-06-30`, `2026-07-01`, `2026-07-10` |
| `discount_rate` | int | 12/12 | 0 | 12/12 | 0 | 2 | `0`, `5` |
| `due_date` | string | 12/12 | 0 | 12/12 | 0 | 12 | `2026-02-01`, `2026-02-15`, `2026-05-30`, `2026-06-01`, `2026-06-09`, `2026-06-15`, `2026-07-01`, `2026-07-30`, `2026-07-31`, `2026-08-10`, `2026-08-15`, `2026-08-20` |
| `file_id` | string | 9/12 | 0 | 9/12 | 0 | 9 | `50000000-0000-4000-8000-000000000020`, `50000000-0000-4000-8000-000000000021`, `50000000-0000-4000-8000-000000000022`, `50000000-0000-4000-8000-000000000023`, `50000000-0000-4000-8000-000000000024`, `50000000-0000-4000-8000-000000000025`, `50000000-0000-4000-8000-000000000026`, `50000000-0000-4000-8000-000000000027`, `50000000-0000-4000-8000-000000000028` |
| `id` | string | 12/12 | 0 | 12/12 | 0 | 12 | `70000000-0000-4000-8000-000000000001`, `70000000-0000-4000-8000-000000000002`, `70000000-0000-4000-8000-000000000003`, `70000000-0000-4000-8000-000000000004`, `70000000-0000-4000-8000-000000000005`, `70000000-0000-4000-8000-000000000006`, `70000000-0000-4000-8000-000000000007`, `70000000-0000-4000-8000-000000000008`, `70000000-0000-4000-8000-000000000009`, `70000000-0000-4000-8000-000000000010`, `70000000-0000-4000-8000-000000000011`, `70000000-0000-4000-8000-000000000012` |
| `invoice_number` | string | 12/12 | 0 | 12/12 | 0 | 12 | `INV-2026-0001`, `INV-2026-0002`, `INV-2026-0040`, `INV-2026-0041`, `INV-2026-0043`, `INV-2026-0045`, `INV-2026-0050`, `INV-2026-0052`, `INV-2026-0060`, `INV-2026-0065`, `INV-2026-0066`, `INV-2026-0070` |
| `line_items` | array | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `line_items[].discount_rate` | int | 16/16 | 0 | 16/16 | 0 | 2 | `0`, `5` |
| `line_items[].name` | string | 16/16 | 0 | 16/16 | 0 | 16 | `Analytics retainer - Q2`, `Brand workshop`, `Campaign production`, `Close-out fee`, `Consulting Services - January`, `Consulting Services - July`, `Design sprint`, `Discovery workshop`, `ERP connector`, `Freight services`, `Implementation hours`, `Inventory sync module`, `Onboarding fee`, `Platform license`, `Travel reimbursement`, `Warehouse integration` |
| `line_items[].quantity` | float+int | 16/16 | 0 | 16/16 | 0 | 4 | `1`, `2`, `2.5`, `3` |
| `line_items[].tax_rate` | float+int+null | 16/16 | 10 | 16/16 | 10 | 4 | `0`, `6.25`, `8.5`, `10` |
| `line_items[].total` | object | 16/16 | 0 | 16/16 | 0 | 0 |  |
| `line_items[].total.amount` | int | 16/16 | 0 | 16/16 | 0 | 15 | `5000`, `6000`, `9403`, `20000`, `22000`, `40000`, `42353`, `45000`, `76000`, `90000`, `96000`, `98000`, `100000`, `156750`, `10000000` |
| `line_items[].total.currency` | string | 16/16 | 0 | 16/16 | 0 | 1 | `USD` |
| `line_items[].unit_price` | object | 16/16 | 0 | 16/16 | 0 | 0 |  |
| `line_items[].unit_price.amount` | int | 16/16 | 0 | 16/16 | 0 | 15 | `5000`, `6000`, `8000`, `9403`, `20000`, `22000`, `40000`, `42353`, `45000`, `48000`, `50000`, `52250`, `90000`, `98000`, `5000000` |
| `line_items[].unit_price.currency` | string | 16/16 | 0 | 16/16 | 0 | 1 | `USD` |
| `note` | null+string | 12/12 | 3 | 12/12 | 3 | 9 | `Customer cancelled engagement.`, `Design sprint package.`, `Final invoice before deletion.`, `Follow up scheduled.`, `Freight + handling.`, `Net 30 terms apply.`, `Q2 analytics retainer.`, `Thanks for your business! Net 30 terms apply.`, `Wire received — confirm allocation.` |
| `payments` | array | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `payments[].external_method` | null+string | 7/7 | 2 | 7/7 | 2 | 4 | `cash`, `check`, `credit_card`, `other` |
| `payments[].paid_at` | string | 7/7 | 0 | 7/7 | 0 | 6 | `2026-01-20`, `2026-05-18`, `2026-06-21`, `2026-06-28`, `2026-07-18`, `2026-07-24` |
| `payments[].transaction_id` | null+string | 7/7 | 5 | 7/7 | 5 | 2 | `019e3868-5858-7000-8000-00000000001a`, `019eebb0-0938-7000-8000-00000000000b` |
| `payments[].type` | string | 7/7 | 0 | 7/7 | 0 | 2 | `external`, `received_in_account` |
| `status` | string | 12/12 | 0 | 12/12 | 0 | 6 | `cancelled`, `confirm_payment`, `overdue`, `paid`, `pending_payout`, `unpaid` |
| `tax_rate` | float+int | 12/12 | 0 | 12/12 | 0 | 4 | `0`, `6.25`, `8.5`, `10` |
| `total` | object | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `total.amount` | int | 12/12 | 0 | 12/12 | 0 | 11 | `5000`, `22000`, `43400`, `45000`, `72200`, `96000`, `98000`, `108403`, `156750`, `158000`, `10000000` |
| `total.currency` | string | 12/12 | 0 | 12/12 | 0 | 1 | `USD` |
| `updated_at` | string | 12/12 | 0 | 12/12 | 0 | 12 | `2026-01-20T10:00:00Z`, `2026-05-10T10:00:00Z`, `2026-05-18T00:07:03Z`, `2026-05-20T09:00:00Z`, `2026-06-21T20:00:00Z`, `2026-06-28T16:00:00Z`, `2026-06-30T17:00:00Z`, `2026-07-01T08:00:00Z`, `2026-07-01T08:30:00Z`, `2026-07-18T09:00:00Z`, `2026-07-20T09:00:00Z`, `2026-07-24T16:00:00Z` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `activities` | len 2 x3, len 3 x4, len 4 x2, len 5 x1, len 6 x1, len 7 x1 |
| `activities[].emails` | len 0 x32, len 1 x10, len 2 x2 |
| `line_items` | len 1 x10, len 2 x1, len 4 x1 |
| `payments` | len 0 x5, len 1 x7 |
---
