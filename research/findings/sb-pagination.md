# Rho sandbox pagination contract, empirically probed

Probed live: `https://rhoapi-sandbox.rho.co/api/v1`, bearer `sandbox` (any non-empty token accepted). All calls via curl on 2026-09-11 (server clock returned `Fri, 11 Sep 2026 23:xx GMT`). Raw evidence saved under `scratchpad/rho/sandbox/probe-pagination/` (161 files: `p.sh`, `walk.py`, per-probe `.json`/`.headers`, `walk_*.json` page logs, `ref_tx_order.txt`, `list_headers.txt`).

Compared against the local doc `scratchpad/rho/docs/docs_v1_pagination.md` and the API reference markdown in `scratchpad/rho/api/*_list*.md`. Every divergence is called out in the last section.

---

## 1. Headline results

| Property | Observed value |
| --- | --- |
| Style | Opaque cursor. Two internal implementations behind the same wrapper: **offset-based** for 5 endpoints, **keyset (last_id)** for `/accounts`. |
| Default `page_size` | **20** (observed directly on `/transactions` and `/statements`; see caveat below) |
| Minimum `page_size` | **1** (`0` -> 400) |
| Maximum `page_size` | **100** (`100` -> 200, `101` -> 400), uniform across all 6 endpoints |
| Page object | `{"page":{"next_page_token": <string|null>}}` and nothing else. No `total`, `has_more`, `count`, `prev`. |
| Last-page signal | `next_page_token: null` (JSON null, key always present; never an empty string, never omitted) |
| Token encoding | base64url, no padding; decodes to JSON `{"v":1,"f":"...","t":"..."}` |
| Token opaque? | Yes in intent, but fully decodable and partially forgeable (see section 6) |
| Ordering stable across page sizes | Yes for all 6 endpoints: identical id sequence at `page_size` 1, 3, 7, 100; no dupes, no skips |
| Token survives changed filters/sort | No -> `400`. Token survives a changed **page_size** -> yes (page_size is not bound) |
| Pagination response headers | None. No `X-Total-Count`, no `Link`, no rate-limit headers on 200s |

---

## 2. Total record counts (each endpoint walked to completion)

Walked with `walk.py` at `page_size` = 1, 3, 7, 100 and cross-checked. Every walk terminated on `next_page_token: null`. Counts identical at every page size.

| Endpoint | Resource key | Total records | Pages @ ps=1 | Pages @ ps=20 (default) |
| --- | --- | --- | --- | --- |
| `/accounts` | `accounts` | **14** | 14 | 1 |
| `/cards` | `cards` | **8** | 8 | 1 |
| `/transactions` | `transactions` | **72** | 72 | 4 |
| `/statements` | `statements` | **33** | 33 | 2 |
| `/invoicing/customers` | `customers` | **7** | 7 | 1 |
| `/invoicing/invoices` | `invoices` | **12** | 12 | 1 |

Note the resource key for invoicing customers is `customers` (not `invoicing_customers`), and for invoices is `invoices`.

---

## 3. Default page size

No `page_size` supplied:

| Endpoint | Records returned with no page_size | Token issued? |
| --- | --- | --- |
| `/transactions` | **20** | yes (72 > 20) |
| `/statements` | **20** | yes (33 > 20) |
| `/accounts` | 14 (all) | null (14 < 20, cannot observe cap) |
| `/cards` | 8 (all) | null |
| `/invoicing/customers` | 7 (all) | null |
| `/invoicing/invoices` | 12 (all) | null |

**Default = 20, proven** on the only two endpoints whose corpus exceeds 20 rows. For the other four the default is unobservable because the full set is smaller than 20; the API reference asserts "Defaults to 20" for cards, invoicing/customers, invoicing/invoices, and this is consistent with (but not independently provable from) the sandbox data.

---

## 4. page_size boundary and value handling

Binary-searched the boundary on `/transactions`, then confirmed the same boundary on all 6 endpoints (`bnd_*` files).

### 4a. Numeric boundary (all endpoints identical)

| page_size | HTTP | Result |
| --- | --- | --- |
| `0` | 400 | error type `1317`, "page_size must be between 1 and 100" |
| `1` | 200 | 1 item (minimum accepted) |
| `2` | 200 | 2 items |
| `99` | 200 | 72 items on /transactions (capped by data, not by cap) |
| `100` | 200 | max accepted |
| `101` | 400 | error type `1317` |
| `150`, `200`, `1000`, `10000` | 400 | error type `1317` |

Boundary is inclusive `[1, 100]`. No endpoint had a different cap; docs/API-ref phrase "max 100" and the sandbox honors exactly 100.

### 4b. Two distinct 400 bodies

There are **two different error shapes**, depending on whether the value parses as an integer at all:

Range error (parses as int but out of `[1,100]`), `type` is `1317`:
```json
{"type":"1317","title":"page_size must be between 1 and 100","status":400}
```
Triggered by: `0`, `-1`, `-5`, `-0`, `1000`, `10000`.

Parse error (does not parse as a plain integer), `type` is `about:blank`:
```json
{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}
```
Triggered by: `2.5`, `2.0`, `abc`, empty (`page_size=`), a space (`%20`), `0x10`, `1e2`, `true`, a duplicate param (`page_size=5&page_size=7`), and a 20-digit overflow (`99999999999999999999`).

### 4c. Values that are silently coerced or ignored

| Input | HTTP | Effect |
| --- | --- | --- |
| `page_size=%2B3` (leading `+`) | 200 | parsed as **3** |
| `page_size=03` (leading zero) | 200 | parsed as **3** |
| `page_size=-0` | 400 | treated as range error `1317` (parses to 0) |
| `page_size[]=5` (array syntax) | 200 | key `page_size[]` ignored; falls back to **default 20** |
| duplicate `page_size=5&page_size=7` | 400 | parse error `about:blank` (rejects, does not pick first/last) |

So: `+N` and leading-zero forms are accepted; float forms including `2.0` are rejected; a bracketed array key is silently dropped rather than erroring.

---

## 5. Page object shape and token anatomy

Top-level keys are exactly the resource array plus `page`:
```json
{"page":{"next_page_token":"eyJ2Ijox..."},"transactions":[ ... ]}
```
`page` has exactly one field, `next_page_token`. No `total`, `total_count`, `has_more`, `has_next`, `count`, `prev_page_token`, `offset`, or `limit` echoed back. Content-type `application/json`. No pagination or rate-limit headers on 200 responses (`list_headers.txt`: only date, content-type, cloudflare/`via`, HSTS, `x-content-type-options`, `x-frame-options`).

### Token decode

The token is **not** opaque in practice. It is base64url without padding and decodes to a small JSON envelope:
```
eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qSXcifQ
  -> {"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":"b2Zmc2V0OjIw"}
```

| Field | Meaning (inferred from behavior) |
| --- | --- |
| `v` | Envelope version. Always `1`. Setting `v:2` -> 400. |
| `f` | Query fingerprint. 22 base64 chars = **16 raw bytes** (looks like a 128-bit digest). Binds the token to endpoint + filters + sort order. Deterministic and stable over time (identical `f` returned across many calls minutes apart). **Does not include page_size.** |
| `t` | The actual cursor, itself base64. Decodes to one of two forms depending on the endpoint. |

### Two cursor implementations under one envelope

**Offset-based** (5 of 6 endpoints: cards, transactions, statements, invoicing/customers, invoicing/invoices). `t` decodes to an ASCII string `offset:N`:
```
"t":"b2Zmc2V0OjIw"  ->  "offset:20"
"t":"b2Zmc2V0OjE"   ->  "offset:1"
```
The offset is the absolute count of rows already consumed. Requesting `page_size=1` yields `offset:1`, `page_size=2` yields `offset:2`, `page_size=50` yields `offset:50`; the `f` is identical in all three, confirming page_size is not part of the fingerprint.

**Keyset-based** (only `/accounts`). `t` decodes to JSON carrying the last row's id plus the sort keys:
```json
{"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}
```
Walking `/accounts` shows `last_id` advancing to the last id of each page, and the rows are genuinely ordered by `account_name` asc with id as tiebreaker (Cash, Cash, Credit x5, Inventory, Primary, Reserve, ...).

This split matters: the doc's stability promise (section 8) only actually holds for the keyset endpoint.

`f` values observed (per query variant, `/transactions` unless noted):

| Query | `f` |
| --- | --- |
| default (no params) | `t0HwRhJ0BSGWYAjAT5bQKg` |
| `order=desc` (= default) | `t0HwRhJ0BSGWYAjAT5bQKg` (same as default) |
| `sort_by=initiated_at` (= default) | `t0HwRhJ0BSGWYAjAT5bQKg` (same) |
| `sort_by=initiated_at&order=desc` | `t0HwRhJ0BSGWYAjAT5bQKg` (same) |
| `order=asc` | `nNrTztCXSL1jz6bsXonMOQ` |
| `sort_by=amount` | `dymXB9iIZmmYk86TS9T-8g` |
| `account_type=checking` | `yzKYfkiECLABzFUrraXw_g` |
| `account_type=credit` | `9AVB5zyC7e55f_PU_MSjPg` |
| `/accounts` default | `SigraTvwZG8Dd7QLdKJzPA` |
| `/accounts sort_by=balance` | `IphmnZ3WlDTdl-uzbroyvQ` |
| `/accounts sort_by=account_name&order=desc` | `teke1sN4JxXz7go2Z3EThA` |

Because specifying the implicit defaults explicitly reproduces the default `f`, a token from a bare request is interchangeable with one from `?sort_by=initiated_at&order=desc` (confirmed 200 on continuation). Default sort/order per endpoint: `/accounts` = account_name asc; `/transactions` = initiated_at desc; `/statements` = period_end (close date) desc, newest first.

---

## 6. Token portability, validation, and tampering

### Portability matrix (token minted from `/transactions?page_size=5`, replayed elsewhere)

| Replay context | HTTP | Meaning |
| --- | --- | --- |
| same endpoint, same (no) filters, `page_size=5` | 200 | normal continuation |
| same endpoint, **`page_size=50`** | 200 | **page_size may change mid-walk** (not bound) |
| same endpoint, `page_size` omitted (default 20) | 200 | works |
| same endpoint, explicit default sort `sort_by=initiated_at&order=desc` | 200 | works (same fingerprint) |
| same endpoint, **added `account_type=checking`** | 400 | "page_token must be a valid cursor" |
| same endpoint, **added `sort_by=amount`** | 400 | same error |
| **statements token used on /transactions** | 400 | cross-endpoint rejected |
| **transactions token used on /statements** | 400 | rejected |
| **accounts token used on /transactions** | 400 | rejected |
| **filtered token (`account_type=checking`) on unfiltered request** | 400 | rejected |
| filtered token on the **same filtered** request | 200 | works |

The gate is purely `f`: the server recomputes the fingerprint from the current request's endpoint+filters+sort and compares it to the `f` embedded in the token. Mismatch -> `400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`. Because page_size is excluded from `f`, a client can legitimately switch page sizes between pages.

### Changing page_size mid-walk is truly safe (no skip/dupe)

Reference order at `page_size=100` (last-6 of ids): `...00000a 000007 000003 000002 000004 000005 00000f 00000c ...`. Took a `page_size=5` token (`offset:5`) and continued it with `page_size=3`: returned records `000005 00000f 00000c` = reference positions 6,7,8 exactly. No overlap, no gap. Offset cursors compose cleanly with a changed page size.

### Tampering / malformed token results (replayed on `/transactions?page_size=3`)

| Token | HTTP | Result |
| --- | --- | --- |
| empty (`page_token=`) | 200 | treated as **first page** |
| `not-a-token` | 400 | invalid cursor |
| `!!!!` (bad base64) | 400 | invalid cursor |
| valid base64 of `hello world` (not JSON) | 400 | invalid cursor |
| `{}` (JSON, no fields) | 400 | invalid cursor |
| `{"v":2,...}` (wrong version) | 400 | invalid cursor |
| valid envelope, `f` zeroed out | 400 | invalid cursor (fingerprint mismatch) |
| `t` = literal `offset:3` (not base64) | 400 | invalid cursor (`t` must itself be base64) |
| `t` = base64 of `offset:-5` | 400 | invalid cursor (negative offset rejected) |
| `t` = base64 of `offset:abc` | 400 | invalid cursor (non-integer offset rejected) |
| `t` = base64 of `offset:100000` | 400 | invalid cursor (offset beyond total rejected) |
| `t` = base64 of `offset:73` (total is 72) | 400 | invalid cursor (offset > total rejected) |
| `t` = base64 of `offset:72` (== total) | 200 | **empty array, `next_page_token: null`** |
| extra field `{"v":1,"f":...,"t":...,"x":"junk"}` | 200 | extra keys ignored, honored normally |
| envelope re-encoded with **standard** base64 + `=` padding | 200 | accepted (decoder takes both urlsafe and standard alphabets, padded or not) |
| `/accounts` keyset with a fabricated nonexistent `last_id` (valid `f`) | 400 | invalid cursor (anchor row must exist) |

Key inferences:
- `f` is a **fingerprint of the query, not an HMAC over the cursor payload**: the offset inside `t` can be freely rewritten (any value in `[0, total]`) while keeping the original `f`, and the server honors it. Only the offset range and the fingerprint are validated, not a signature over `t`.
- The decoder is lenient about base64 alphabet and padding, but strict about the envelope schema (`v` must be 1, `f` must match, `t` must be base64 of a well-formed cursor).
- Offset exactly equal to total yields a valid empty terminal page; offset one past total is a 400. So the only clean terminator via the API's own tokens is the `null` on the natural last page.

---

## 7. Last page and ordering stability

- **Last page always carries `"next_page_token": null`.** The key is always present; it is never an empty string and never omitted. There is no API path that produces an empty-string token (offset==total gives `null`, not `""`).
- **Ordering is stable across page sizes.** For all 6 endpoints, the concatenated id sequence at `page_size` 1, 3, 7, and 100 is byte-for-byte identical (`walk.py` "IDENTICAL" for every endpoint x every size). Unique-id count equals total count at every size -> no duplication and no skipping within a static dataset.
- Full-last-page behavior: when total is an exact multiple of page_size, the last full page still returns a token, and the following request returns an empty array with a null token. Examples: `/cards?page_size=4` (total 8) -> page 1 returns 4 items **with** a token; `/transactions?page_size=36` (total 72) -> `offset:36` token present. `/invoicing/customers?page_size=7` (total exactly 7) -> token is already `null` on the first page because the page filled the entire set.

---

## 8. Divergences from `docs/docs_v1_pagination.md` (and the API reference)

Ranked by materiality.

1. **Stability guarantee is only half-true.** The doc states, unqualified: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." Observed: 5 of 6 endpoints use a plain **absolute offset** (`offset:N`) cursor. An absolute offset cannot deliver that guarantee: an insert or delete positioned before the current offset will shift every subsequent row, causing a skip or a duplicate. Only `/accounts` uses a keyset (`last_id`) cursor that actually provides the promised stability. (The sandbox dataset is static so a live shift cannot be forced here, but the offset mechanism is dispositive: the promise is structurally unattainable for the offset endpoints.) This is the most important divergence.

2. **Documented token format is fictional.** The doc's example token `eyJvIjoxMDAsImQiOiIyMDI2LTA1LTE0In0` decodes to `{"o":100,"d":"2026-05-14"}`. Real tokens are `{"v":1,"f":"...","t":"..."}` with either an `offset:N` or a `last_id` cursor inside `t`. No real token uses the `{"o":...,"d":...}` shape. The doc does disclaim that "format and lifetime are not part of the API contract and may change," so this is illustrative rather than contractual, but it matches nothing the API actually emits.

3. **API reference marks `page.next_page_token` as a required string; it is nullable.** Every `*_list*.md` reference says `page.next_page_token (string, required)` while also noting "null on the last page." Reality: the field is present but `null` on the last page. A strict "required string" schema would reject the real terminal response. It should be typed nullable/`string | null`.

4. **Two undocumented distinct error bodies for page_size.** The doc only says "Values outside the allowed range return `400 Bad Request`." It does not distinguish the range error (`type:"1317"`, "page_size must be between 1 and 100") from the parse error (`type:"about:blank"`, "invalid parameter: page_size"), nor does it document the numeric range in prose (the API ref states only "max 100" for accounts/transactions/statements and never states a minimum or the cap for cards/invoicing endpoints). The min is 1 and the max is 100 uniformly, discoverable only by probing.

5. **page_size is silently excluded from the cursor binding, undocumented as such.** The doc's "Common mistakes" lists `account_id`, `status`, `sort_by` as binding and says changing them forces a restart (confirmed: 400). It never states the useful converse: **page_size can be changed between pages without invalidating the token.** This is a real, safe capability that the docs omit.

6. **Coercion quirks undocumented.** `page_size=+3` and `page_size=03` are accepted as 3; `page_size=2.0` is rejected; `page_size[]=5` is silently ignored and falls back to the default; duplicate `page_size` params 400 rather than resolving to one. None of this is documented.

7. **Confirmations (doc is correct).** Opaque cursor-based pagination: yes. Same two params `page_size` / `page_token`: yes. Omit `page_token` for the first page: yes, and an empty-string `page_token=` also yields the first page. `next_page_token` is a string or `null`: yes. Token bound to same endpoint + same filters + same sort: yes (400 on any change). Cross-endpoint tokens rejected: yes. The canonical "loop until null" walk pattern works verbatim on all 6 endpoints.

---

## 9. Evidence index (probe-pagination/)

- `p.sh`, `walk.py` - probe harness and the completion-walker.
- `def_*.json` - default (no page_size) response per endpoint.
- `ps_*.json`, `bnd_*_*.json` - page_size boundary sweep (global and per-endpoint).
- `nv_*.json` - non-integer / malformed page_size values (hashed filenames).
- `fp_*.json` - fingerprint mapping across filters/sort.
- `tp_*.json` - token portability (cross-endpoint, changed filters, changed page_size).
- `tam_*.json` - token tampering/malformed-cursor tests.
- `mult_*_*.json` - full-last-page (exact multiple) token behavior.
- `walk_*_ps{1,3,7,100}.json` - per-page logs of every completion walk, with decoded cursors.
- `walk_all_ids.json` - concatenated id sequences used for the ordering-stability check.
- `ref_tx_order.txt` - transactions reference order at page_size=100.
- `list_headers.txt` - full response headers on a 200 list call.
