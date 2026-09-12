# Rho: The AI / API / Agent Surface

Research date: 2026-09-11. Corpus: local crawl of rho.co (128 core pages, 269 help pages, 125 comparison blog posts), docs.rho.co (14 guides), docs.rho.co API reference (14 operation pages), live sandbox JSON captured 2026-09-11 23:22 UTC, site-llms.txt / site-llms-full.txt, 1042-URL sitemap. Two pages fetched during this pass because they were absent locally: `https://www.rho.co/blog/introducing-rho-api` and `https://www.rho.co/blog/introducing-rho-for-slack`.

Labels: **[Rho claim]** = asserted only by Rho, no independent source in corpus. **[Verified in corpus]** = confirmed against a live sandbox response or a machine-readable spec.

---

## 0. Executive summary of the capability boundary

Rho's entire AI surface today is **read-only retrieval of banking data, plus one natural-language chat beta inside Slack**. There is no write path of any kind exposed to an agent, a token, or an MCP client. The proof is structural, not rhetorical: **all 14 published API operations are HTTP GET**. There is no POST, PUT, PATCH or DELETE anywhere in the v1 surface.

| Question | Answer today (2026-09-11) | Source |
| --- | --- | --- |
| Can an agent read balances? | Yes | `docs/docs_v1_accounts.md` |
| Can an agent read transactions (full detail, all rails)? | Yes | `docs/docs_v1_transactions.md` |
| Can an agent read statements + download statement PDFs? | Yes | `docs/docs_v1_statements.md` |
| Can an agent read cards (incl. limits, spend, MCC blocks)? | Yes, `cards:read` | `api/cards_listcards.md` |
| Can an agent read invoices + customers? | Yes, `invoicing:read` | `api/invoicing_*.md` |
| Can an agent move money (ACH/wire/check/transfer)? | **No** | product/api, help center, ToS |
| Can an agent issue / lock / edit a card? | **No** | `help-center/the-rho-api/what-connected-al-tools-have-access-to...` |
| Can an agent add or manage users? | **No** | same |
| Can an agent change any account setting? | **No** | same |
| Can an agent approve a payment from Slack? | **No**, "Not yet" | `product/slack` FAQ |
| Are there webhooks / push events? | **No**, "not yet" / "planned" | changelog 08/03/2026, blog 08/25/2026 |
| Is there a Rho CLI? | Not mentioned anywhere in corpus | (absence) |
| Is there a ChatGPT / Codex / Cursor connector? | Not for Rho. "Claude is the natively supported client today" | `product/api` |

Rho's own stated roadmap, verbatim: *"Read-only is live today. Write access and webhooks are next."* (changelog, August 3, 2026) and *"Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval, the finance tasks you'd rather delegate."* (blog, July 29, 2026).

---

## 1. The Rho API: what it is

### 1.1 Positioning
From `/product/api` (page states *"Product capabilities described on this page are current as of August 2026"*):

> "The Rho API gives Rho customers **read-only** programmatic access to their balances, transactions, and statements, through a REST API and a **native MCP connection to Claude**. It is available to every Rho customer."

Rho explicitly places itself in a category: not an aggregator (Plaid), not banking-as-a-service. *"The Rho API is neither: it is the banking platform's own front door to your own company's data."*

Four stated properties:
1. **Read-only by design** - "tokens cannot initiate payments or modify accounts"
2. **2 ways in** - REST API plus MCP for Claude
3. **All customers** - "every Rho business gets API access, no waitlist and no approval step"
4. **Owners and Admins only** can create tokens

Pricing: **$0**. *"$0 in monthly, per-user, and minimum-balance fees for Rho Banking."* No separate API fee anywhere in corpus.

### 1.2 Hosts and versioning

| Thing | Value |
| --- | --- |
| Production REST | `https://rhoapi.rho.co/api/v1` |
| Sandbox REST | `https://rhoapi-sandbox.rho.co/api/v1` |
| Production MCP | `https://rhoapi.rho.co/mcp/v1` |
| OAuth authorization server | `https://auth.rho.co` |
| OIDC discovery | `https://auth.rho.co/.well-known/openid-configuration` |
| Token management UI | `https://app.rho.co/settings/access-tokens` (also described as Settings → Configurations → Access Tokens, and Settings → API → Access Tokens) |
| Partner onboarding | `api-partner-request@rho.co` |
| Spec version | `1.0.0`; URL path `/api/v1` |
| Errors | RFC 9457 / RFC 7807 `application/problem+json` |
| Timestamps | ISO 8601 UTC |
| Money | integer minor units + ISO 4217 currency, always as an object `{amount, currency}` |

**Stability contract** (`docs/docs_v1_versioning.md`): v1 is "stable and additive-only". Non-breaking (can ship into v1 any time): new enum value, new nullable response field, new optional query parameter. Breaking (requires a new version): removing/renaming an enum value, removing a response field, changing a field type, making an optional field required. **Deprecation notice: at least 15 days.**

Client obligations Rho writes down explicitly: handle unknown enum values (give every `switch` a default), ignore unrecognized response fields, treat IDs as opaque strings, store IDs as-is.

### 1.3 The complete operation catalogue (14 operations, all GET)

| # | Method + path | operationId | Scope |
| --- | --- | --- | --- |
| 1 | GET /accounts | `listaccounts` | `accounts:read` |
| 2 | GET /accounts/{account_id} | `getaccount` | `accounts:read` |
| 3 | GET /cards | `listcards` | `cards:read` |
| 4 | GET /cards/{id} | `getcard` | `cards:read` |
| 5 | GET /transactions | `listtransactions` | `transactions:read` |
| 6 | GET /transactions/{id} | `gettransaction` | `transactions:read` |
| 7 | GET /transactions/{transaction_id}/files/{file_id} | `gettransactionfile` | `transactions:read` |
| 8 | GET /statements | `liststatements` | `statements:read` |
| 9 | GET /statements/{id} | `getstatement` | `statements:read` |
| 10 | GET /invoicing/customers | `listinvoicingcustomers` | `invoicing:read` |
| 11 | GET /invoicing/customers/{customer_id} | `getinvoicingcustomer` | `invoicing:read` |
| 12 | GET /invoicing/invoices | `listinvoicinginvoices` | `invoicing:read` |
| 13 | GET /invoicing/invoices/{invoice_id} | `getinvoicinginvoice` | `invoicing:read` |
| 14 | GET /invoicing/invoices/{invoice_id}/files/{file_id} | `getinvoicinginvoicefile` | `invoicing:read` |

Five resource families: Accounts, Cards, Transactions, Statements, Invoicing. **No Payments, no Bill Pay, no Users, no Departments, no Vendors, no Treasury-trading, no Reimbursements, no Expenses, no Approvals resource exists in v1.**

### 1.4 Authentication and token lifecycle

Two credential types.

**A. API Access Tokens** (internal integrations):

| Property | Value |
| --- | --- |
| Prefix | `rhobat_` (example in docs: `rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f`) |
| Header | `Authorization: Bearer <token>` (no cookie, no API key, no signed request supported) |
| Who can create | Account Owners and Admins only |
| Creation gate | **2FA challenge at the moment of creation** |
| Shown | **Once**, unrecoverable afterward |
| Max active per business | **20** |
| Expiration | **Required. Maximum one year.** |
| Inactivity expiry | **45 days** without a successful authenticated request (for never-used tokens, the 45-day window starts at creation) |
| IP allowlist | Optional, **up to 100 entries per token** |
| Revocation | Immediate, no grace period, no un-revoke |
| Scope model | `resource:action`, enforced before the handler |

Error semantics: `401` = missing/malformed/unknown/revoked/expired token. `403` = valid token lacking the endpoint's scope, **or request from an IP outside the allowlist**.

**Sandbox auth is intentionally permissive**: `Authorization: Bearer sandbox` works; "the sandbox accepts any non-empty bearer token".

**B. Partner OAuth 2.0** (`docs/docs_v1_partner-auth.md`), for apps connecting to *customers'* Rho accounts:

| Property | Value |
| --- | --- |
| Flow | Authorization Code **with PKCE (S256 required)** |
| `audience` param | `https://rhoapi.rho.co` |
| Registration | Manual, by email to `api-partner-request@rho.co` (name, company, logo, redirect URIs, requested scopes, privacy policy URI, ToS URI, support email) |
| Who consents | Account Owners and Admins only |
| Grants per app per business | **At most one active grant**; re-approving updates it |
| Access token lifetime | **900 seconds / 15 minutes** (`expires_in: 900`) |
| Refresh token | **Single-use, rotates on every refresh**; 30-day rolling window |
| Grant lifetime | **1 year**, then customer must re-approve |
| Revocation | `POST /oauth2/revoke`; customer-side revocation is immediate and kills refresh tokens too |
| `offline_access` | Required in scope list to get refresh tokens |

### 1.5 Scopes - and a contradiction

`docs/docs_v1_auth.md` says "The scopes available today are" and lists **three**:
- `accounts:read`
- `transactions:read`
- `statements:read`

The OpenAPI security block (`docs/api_v1_openapi.md`) lists **five**:
- `accounts:read` - Read access to business accounts information
- `cards:read` - Read access to business cards information
- `invoicing:read` - Read access to Invoicing information
- `statements:read` - Read access to business statements information
- `transactions:read` - Read access to business transactions information

**Contradiction #1.** The auth guide is stale relative to the spec. The Cards guide (`docs_v1_cards.md`) and Invoicing guide (`docs_v1_invoicing.md`) both explicitly require `cards:read` and `invoicing:read` respectively, so the spec is the accurate one. The auth page is the page a developer is most likely to read first.

**Contradiction #2.** `docs/docs_v1_getting-started.md` says: *"Current release is read-only and covers **accounts and transactions**."* It does not mention statements, cards or invoicing, all three of which are fully documented and live in sandbox.

**Contradiction #3.** The OpenAPI security scheme declares `Type: oauth2` with `Token URL: https://app.rho.co/settings/access-tokens` - that is a settings page in the web app, not an OAuth token endpoint (the real one is `https://auth.rho.co/oauth2/token`). Cosmetic spec sloppiness, but it will break OAuth client generators.

### 1.6 Rate limits

| Limit | Threshold |
| --- | --- |
| Per API Access Token | **~60 requests / minute** |
| Per source IP | **~600 requests / minute** (shared across every integration on that IP, including different tokens) |

Enforced at a "distributed edge network", so approximate. `429 Too Many Requests` with `Retry-After`; if `Retry-After` is `0` Rho says there is no fixed cooldown and instructs exponential backoff with jitter. Guidance: "pace traffic steadily below one request per second".

For an agent: **60 rpm per token is the hard ceiling on an agentic loop.** A Claude session walking 100-item pages of a busy ledger hits this quickly.

### 1.7 Pagination

Opaque cursor. `page_size` + `page_token` query params; response wraps items under the resource key plus `page.next_page_token` (string, or `null` on the last page). Cursors are bound to the exact endpoint + filters + sort; changing any of them returns `400`. Cursors are explicitly **not** durable bookmarks ("their format and lifetime are not part of the API contract").

Verified in sandbox: `page_size` default is 20 (transactions and statements returned exactly 20 with a non-null cursor; cards returned 8, invoices 12, customers 7, accounts 14, all with `next_page_token: null`). Max is 100 for accounts/transactions/statements; cards documented as 1-100 with default 20.

Real sandbox cursor value (base64 JSON): `eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qSXcifQ` → decodes to a `{v, f, t}` shape. Docs elsewhere show a different shape `eyJvIjoxMDAsImQiOiIyMDI2LTA1LTE0In0` (`{o, d}`), i.e. the documented example does not match the live implementation.

### 1.8 Data model highlights an agent will actually hit

**`account_type` enum:** `checking`, `credit`, `investment`, `savings`, `rewards`. Immutable for the life of the account.

**`transaction_type` enum (33 values)** - this is the richest enum in the API and the best single artifact for understanding Rho's rails:
`card_credit`, `card_debit`, `card_refund`, `credit_repayment`, `credit_repayment_refund`, `credit_cashback`, `ach_credit`, `ach_debit`, `ach_return`, `wire_in`, `wire_out`, `wire_fee`, `international_wire_in`, `international_wire_out`, `check_deposit`, `check_payment`, `internal_transfer`, `savings_deposit`, `savings_withdrawal`, `savings_interest`, `treasury_deposit`, `treasury_withdrawal`, `treasury_fee`, `treasury_interest`, `treasury_maturity`, `treasury_sale`, `treasury_market_value_adjustment`, `rewards_accrual`, `rewards_cashback_redemption`, `adjustment_credit`, `adjustment_debit`, `international_wire_fee`, `international_wire_fee_refund`

**`status` enum:** `pending`, `settled`, `failed`, `awaiting_approval`. Note `awaiting_approval` - *"a payment waiting on an approver, or a debit waiting on your authorization - and no funds have moved while it sits in that state."* An agent can **see** the approval queue but cannot act on it.

**The `id` trap.** Rho documents this explicitly and it is the single most important gotcha for anyone building ingestion: *"`id` ... Stable across re-fetches, but **not guaranteed unique per row** - the entries of one money movement can share an `id`."* The fix Rho prescribes: key on `id` + `account_id`, or group on `money_movement_id`. *"a warehouse keyed on `id` alone silently drops a leg."*

**Other notable fields:** `tracking_number` (ACH NACHA trace number or wire IMAD/OMAD; **MT103 reference numbers are explicitly not returned**), `counterparty_name` (always present but can be empty string), `counterparty_logo_url`, `memo` (bank/provider-supplied, read-only), `note` (user-editable in Rho, read-only via API), `user_id`/`user_full_name` (null for system-initiated activity like interest), `card_id`/`card_name` (null for non-card types).

`search` does free-text across `counterparty_name`, `memo`, and `note` in one query.

**Explicit gap Rho flags:** *"A refund or credit is not by itself a dispute - v1 exposes no dispute indicator."*

**Lifecycle honesty:** `posted_at` is nullable regardless of status; v1 does **not** guarantee a state transition order; v1 does **not** guarantee a failed transaction has an empty `posted_at`.

**Cards object** exposes a lot: `spending_limit`, `spending_limit_type` (`fixed`, `monthly`, `single_use`, `annual`, `daily`, `weekly`, `quarterly`), `current_spend`, `pending_spend`, `spend_period_start/end`, `usage_starts_at/ends_at`, full `billing_address` and `shipping_address`, and MCC controls (`blocked_categories`/`allowed_categories` with ISO 18245 codes, `blocked_merchants`/`allowed_merchants` by name; block and allow lists are mutually exclusive). `status` enum has 11 values: `printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `active`, `expiring`, `locked`, `canceled`, `suspended`, `expired`.

Card reset semantics: `daily`/`weekly`/`monthly`/`quarterly` reset on **Eastern Time (America/New_York)** calendar boundaries; `annual` resets on the anniversary of when the limit took effect; `fixed` is a lifetime ceiling; `single_use` is spent after one use.

**Card PII boundary:** *"Only the last four PAN digits are returned; full card numbers, CVCs, and expiration dates are not available through these endpoints."* (Contrast: Rho's own blog notes Slash's MCP may return plaintext PAN/CVV unless an RSA key is configured.)

**Statements:** `statement_type` is `account`, `credit` or `treasury`; per-account `account_type` enum for statements is a different set (`checking`, `savings`, `credit`, **`treasury`**) than the accounts enum (which uses `investment`, not `treasury`). **Contradiction #4** - two different type vocabularies for the same underlying concept across two endpoints.

**Signed file URLs:** statement `pdf_url` is "valid for up to 15 minutes". Verified in sandbox: the URL carries `X-Goog-Expires=899` (899 seconds), `X-Goog-Algorithm=GOOG4-RSA-SHA256`, host `sandbox-statements.files.rho.co`, signed by `file-service@pledge-218909.iam.gserviceaccount.com`. So statement storage is Google Cloud Storage under a GCP project named `pledge-218909` ("Pledge" appears to be a legacy internal name). Transaction and invoice attachments follow the same pattern: metadata is stable (`file_id`, `file_name`), the signed `download_url` is minted per request and must be followed **without** an Authorization header.

**Invoicing enums:** invoice `status` = `paid`, `unpaid`, `cancelled`, `overdue`, `confirm_payment`, `pending_payout`. `accounting_sync_status` = `not_pushed`, `synced`, `error`, `skip`, `object_changed`. Payment `type` = `received_in_account`, `external`; `external_method` = `cash`, `check`, `credit_card`, `other`. Activity `activity_type` = `created`, `sent`, `downloaded`, `matched`, `marked_as_paid`, `marked_as_unpaid`, `cancelled`, `reminder_sent`, `card_payment_received`, `accounting_synced`, `payment_accounting_synced`.

### 1.9 Sandbox

Open, deterministic, fictional. No approval needed. Verified live on 2026-09-11: 14 accounts (7 checking incl. "Cash (Checking)" x2, "Inventory Checking", "Primary Checking", "Reserve Checking", "Treasury Checking"; 4 credit; 2 rewards; 2 savings), 8 cards, 12 invoices, 7 invoicing customers, 20+ transactions, 20+ statements. UUIDs are patterned by entity class: users `10000000-...`, cards `20000000-...`, accounts `30000000-...`, money movements `40000000-...`, invoicing users `40000000-...`, customers `60000000-...`, invoices `70000000-...`. Transaction IDs are UUIDv7 (`019f0554-0bf0-7000-...`), which leaks a creation timestamp - worth noting against the "treat IDs as opaque" instruction.

Response headers show the stack: Cloudflare in front (`server: cloudflare`, `cf-ray: ...-EWR`, `cf-cache-status: DYNAMIC`), Google infrastructure behind (`via: 1.1 google`). HSTS `max-age=63072000; includeSubDomains; preload`, `x-frame-options: DENY`, `x-content-type-options: nosniff`. **No rate-limit headers are returned** (no `X-RateLimit-*`), so a client cannot see remaining quota before a 429.

Rho warns: *"Sandbox downloads contain non-empty representative fictional documents, but their contents are not guaranteed to reproduce every field of the transaction fixture."*

---

## 2. The MCP connection

### 2.1 Protocol facts (`docs/docs_v1_mcp.md`)

| Property | Value |
| --- | --- |
| Transport | **Streamable HTTP** |
| Endpoint | `/mcp/v1` (production: `https://rhoapi.rho.co/mcp/v1`), separate from `/api/v1` |
| Protocol versions advertised | **`2026-07-28`, `2025-11-25`, `2025-06-18`** |
| Negotiation | `server/discover` for "the current sessionless protocol" |
| Required header | `MCP-Protocol-Version` on every non-`initialize` request |
| Rejected | Anything older than `2025-06-18`; **JSON-RPC batches** |
| Auth (direct) | `Authorization: Bearer <rho_api_access_token>` |
| Auth (linked apps) | OAuth connection provided by the MCP client, no manual token; "availability depends on the client" |
| Contract | "MCP uses the same API contract, authentication model, scopes, and error behavior as the REST API" |

### 2.2 Tool naming guarantee (unusually strong, and strategically notable)

From `docs_v1_versioning.md`:

> "The MCP server is **1:1 with the REST API** ... Tool *names* derive from the frozen `v1` operationIds, so **tool names will never change**. You can reference them explicitly in workflows, agent skills, and saved automations without them breaking. Tool *descriptions* are not part of the contract - they may be improved at any time to help agents use the tools well, and such changes are never treated as breaking."

Because the mapping is 1:1 with operationIds, the MCP tool set is **14 tools**, inferable as: `listaccounts`, `getaccount`, `listcards`, `getcard`, `listtransactions`, `gettransaction`, `gettransactionfile`, `liststatements`, `getstatement`, `listinvoicingcustomers`, `getinvoicingcustomer`, `listinvoicinginvoices`, `getinvoicinginvoice`, `getinvoicinginvoicefile`. (Names inferred from the frozen-operationId rule plus the reference file naming; the live tool list was not enumerated in this pass.) Rho says the server also exposes "prompts and resources" but does **not** document what they are - it tells you to introspect with an MCP client or MCP Inspector. That is a real documentation gap: **prompt and resource inventory is undocumented.**

### 2.3 Claude Code setup (verbatim from docs)

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

Then `/mcp` inside Claude Code to confirm connection. **This is the only MCP client for which Rho publishes a literal install command.**

### 2.4 The Claude connector (no-code path)

From `/help-center/the-rho-api/connect-claude-to-your-rho-account`:
1. In Claude, open **Customize → Connectors** directory, select **Rho**
2. Sign in with Rho credentials
3. **Select the business you want to connect**
4. If prompted, answer an onboarding question about how you plan to use the integration
5. Review requested permissions, adjust if needed
6. Click **Authorize**

Constraints:
- **Only Account Owners and Administrators** can connect Claude natively
- **One Rho business per connection.** "If you have multiple businesses, Claude connects to one at a time: to switch, reconnect the Rho connector and choose a different business at the authorization step." This is a hard limit for multi-entity customers, and Rho markets to multi-entity enterprises elsewhere (`/solutions/enterprise`).
- Disconnect = remove from Claude connector settings; to revoke server-side, revoke the row under **Settings → API → Linked Apps** in Rho.

`/product/api` on client support: *"Other MCP clients can connect using the MCP guide at docs.rho.co; **Claude is the natively supported client today**."*

### 2.5 What Rho says the MCP connection is for

From `/product/api`, in-depth guide 04, the four canonical use cases:
- Burn and runway dashboards fed by the transactions endpoints
- Reconciliation checks comparing Rho data against an internal ledger
- **"Morning cash briefs assembled by a script or an AI agent over MCP"**
- Spend reporting blending Rho data with CRM or billing data in a warehouse

And the security framing: *"The Rho API is read-only today; every token is read-only, which also means **a leaked token cannot move money**."*

---

## 3. `/claude-code` - what the page actually is

**It is a $500 promotional landing page, not a product page.** It contains **zero** technical content about Claude Code, MCP, the API, or agents. Title: "Don't Slow the Build | Rho for Claude Code Builders".

The offer, headline: *"Shipping with Claude Code? Route your first revenue through Rho and get $500 in Claude credits on us."*

Terms and conditions (footnote 1), all three required:
1. Successfully open a new Rho checking account
2. **Deposit at least $20,000.00 USD generated from proceeds from your app created with Claude Code (by Anthropic PBC)** directly into the Rho checking account **within the first 30 days** after opening, **made directly from your app's payment processing service**
3. **Make a purchase of a Claude product or service valued at least $500 using your Rho corporate credit card** (daily or monthly terms)

Payout: *"The cash reward will show as a **statement credit to your Rho checking account within sixty (60) days** of opening your Rho checking account."*

**Contradiction #5.** The hero promises "$500 in Claude credits on us" but the terms deliver a **$500 cash statement credit to a Rho checking account**, conditioned on the customer first spending $500 at Anthropic on a Rho card. It is a rebate on Anthropic spend, not Anthropic credits. Anthropic is named as "Anthropic PBC" in the terms, indicating a real, specific co-marketing arrangement (or at minimum careful legal naming), but the page carries **no Anthropic branding, no logo, and no statement of partnership**.

Other exclusions: new Rho customers only; anyone who applied in the last 120 days is excluded; one reward per business including all subsidiaries/affiliates; Rho may rescind for "fraudulent, deceptive, or suspicious activity".

The rest of the page is generic founder-banking copy ("Accept money without slowing down", "Real humans, when you actually need them", "Don't let admin creep in", "Pay vendors without breaking flow", "Clean books, no cleanup sprint") plus a very long recycled testimonial wall. Bank disclosure: "Webster Bank, a division of Santander Bank, N.A. - a nationally-charted [sic] institution with **$76B in assets**". Note: other Rho pages describe Santander's US banking organization as **$327B** in assets (per Santander, 8/20/2026) - the $76B figure here is Webster-the-division specifically, so the two numbers coexist across pages without reconciliation.

**`/claude-code` is not in the 1042-URL sitemap's AI grep as a product page and is not linked from the main nav.** It is a standalone acquisition LP.

---

## 4. `/orion` - NOT an AI product

**Orion is a mattress.** Despite the name reading like an AI codename, `/orion` is a deposit-incentive landing page for an **"Orion Sleep System"**.

- Headline: "Founders sleep better with Rho. Earn a new Orion Sleep System when you move your banking to Rho."
- Requirement table: **"Deposits in Rho Checking Account for 90 Days (per Orion Sleep unit) - Sleep System - $225,000"**
- Full terms: maintain an **average daily checking deposit balance of at least $225,000.00 USD for the first 90 days**, **use the Rho checking account for company payroll**, **complete a payroll transaction**, and continue using Rho as primary business banking. Rho reserves the right to verify what counts as a payroll transaction.
- New Rho customers only; 120-day lookout for prior applicants; one reward per business including subsidiaries and affiliates; cannot be combined with other offers.
- Form fields: first name, last name, email, phone.

No mention of AI, agents, or software anywhere on the page. It is the same perk-LP template as `/setupclaw` and `/claude-code`, with different hardware and a different deposit threshold. **Anyone scanning Rho's sitemap for "Orion = AI agent" is wrong.**

---

## 5. `/setupclaw` - the OpenClaw perk

Title: "Rho | SetupClaw customer perks".

Offer: *"Get SetupClaw's white-glove **AI assistant installation** (up to $2400 value) when you move $300K+ to Rho. Clear your inbox, automate your calendar, and actually get things done."*

What the customer receives:
- **Free OpenClaw setup with Mac Mini (up to $2,400 value)**
- **30 days of post-setup support included**

Terms (footnote 1):
- **Deposit and maintain an average daily checking deposit balance of at least $300,000.00 USD for the first 30 days** after opening
- Continue using Rho as primary business banking account
- **SetupClaw reaches out to schedule the OpenClaw installation within 14 days following the first 30 days** of account opening, if the balance requirement was met
- **Installation is subject to availability in your area; remote setup may be substituted if in-person installation is not available**
- New customers only, 120-day lookout, one per business, may be combined with other offers only if the other offer's terms allow it

**Contradiction #6.** The page body says *"Deposit $300,000 USD within the **first 90 days** after your Rho Checking account is opened and maintain it for 30 days"* while the binding terms say *"maintain an average daily checking deposit balance of at least $300,000.00 USD for the **first thirty (30) days**"*. The 90-day and 30-day framings are incompatible.

**Reading:** SetupClaw is a third-party white-glove installer for **OpenClaw**, an AI personal-assistant product that runs on a dedicated **Mac Mini** delivered to the customer. This is Rho paying for a *local, hardware-resident AI assistant* as an acquisition incentive. It is entirely separate from the Rho API/MCP surface - there is no evidence in the corpus that OpenClaw connects to Rho data.

The rest of the page is standard Rho copy, plus a competitive table dated **09/11/2026** (the crawl date, so it renders "as of today"):

| | Rho | Mercury | Brex | Ramp | Amex |
| --- | --- | --- | --- | --- | --- |
| Cashback | Up to 2%* | Up to 1.5% | 0.6% | Up to 1.5% | 0.6% |
| Fees | No Fees | $350/mo (Pro) | $12/user/mo (Premium) | $12/user/mo (Premium) | $695 (Business Platinum) |
| Dedicated support | Yes | Only with Pro | Only with Enterprise | Only with Enterprise | Yes |
| G2 rating | 4.8 | 4.5 | 4.7 | 4.8 | N/A |

[Rho claim] on every competitor cell. Note Rho's own blog (`best-banks-for-ai-startups`, 08/03/2026) puts Mercury software at "$29.90-$299/mo" and Ramp Plus at "$15/user/mo", neither of which matches this table. **Contradiction #7.**

---

## 6. The Slack surface - this is where the actual agent lives

Two URLs: `/product/slack` (full marketing page) and `/grow/slack` (stripped variant of the same copy). Four help-center articles under `/help-center/rho-slack-app/`.

### 6.1 Launch and positioning

Blog "Introducing: Rho for Slack" by Esther Nguyen, **published September 2, 2026, last updated September 2, 2026**. Included at **no extra cost** for Rho customers.

Three shipped capabilities plus one beta:
1. **Daily pulse** - cash balances, yield earned, heads-up before payroll leaves, on a schedule, to a chosen channel
2. **Real-time alerts** - inflows, outflows, card activity, with a dollar threshold
3. **Slash commands** - balances, transactions, statements pulled into any conversation; replies private to the asker
4. **"Rho agent coming soon"** → in help center, already **"(Beta): Ask questions in plain language"**

### 6.2 Commands (help center, authoritative)

| Command | What it does |
| --- | --- |
| `/rho-accounts` | Your balances across accounts |
| `/rho-transactions` | Recent transactions, with a link to see everything in Rho |
| `/rho-help` | Everything the app can do, tailored to your setup |
| `/rho-feedback` | Send the Rho team a bug report, request, or note |
| `/rho signin`, `/rho-signout` | Manage your personal sign-in |
| `/rho-connect` | (Owner/Admin) authorize the workspace→business connection |
| `/rho <question>` | (Beta) natural-language question |

**Contradiction #8.** The launch blog lists the commands as `/rho balances`, `/rho transactions`, `/rho accounts`. The help center lists `/rho-accounts` and `/rho-transactions` and has **no balances command at all**. Two different command vocabularies published one week apart.

### 6.3 The agent chat beta - the most consequential AI fact in the corpus

From `/help-center/rho-slack-app/how-to-use-the-rho-slack-app`, section "(Beta) Ask questions in plain language":

> "**Agent chat is in beta for select Rho businesses.** When it is on for yours, ask questions three ways: DM the Rho app directly; Mention **@Rho** in a private channel; Type your question after `/rho`, like `/rho how much did we spend on travel in July`.
>
> The agent answers using your live Rho data: **balances, transactions, statements, and spend by vendor, category, or person**. Every answer **names its sources** and includes a reminder that **your Rho dashboard stays the source of truth**. It is **read-only**, so it can look things up but never move money."

Mechanics documented:
- Questions asked in a channel are **answered by DM**, so business data stays out of shared rooms
- **Statement download links work for about 15 minutes**; ask again if one expires (matches the API's 15-minute signed-URL policy - strong evidence the Slack agent is built on the same `/api/v1` surface)
- If you ask before signing in, **sign in within 15 minutes and the app answers your original question automatically**
- If agent chat is not enabled for your business, commands still work and you can **request beta access from inside the app**

`/product/slack` FAQ, verbatim: *"**Can I approve payments from Slack?** Not yet. Today's release is visibility and answers. Acting on your money from Slack is coming."*

### 6.4 Slack access and privacy model

Two independent connections:
- **Workspace connection** - a Rho Admin links the Slack workspace to one Rho business, once. **One workspace ↔ one Rho business.**
- **Sign in with Rho** - per-person, each user ties their own Slack identity to their own Rho account via a personal link.

*"The Rho Slack App is available to **Account Owners and Admins today**, with support for more roles on the way. Teammates in other roles can sign in and express interest."* So the Slack app is currently **role-gated to the top two roles**, same as API token creation and Claude connector authorization.

Privacy rules:
- **Private channels and DMs only.** *"If it is invited to [a public channel], it says so and removes itself."*
- Read-only workspace connection: *"can view balances, transactions, and statements. It cannot move money or change anything in Rho."*
- Personal links work only for the person they were sent to
- Command replies visible only to the asker; channel questions answered by DM

Setup: Slack workspace admin installs from **Rho → Settings → Integrations → Slack tile → Connect**. If the installer lacks Slack app-install permission, "Ask a Slack admin" generates a copyable install request. Then `/rho-connect` (Owner/Admin) with a short-lived personal authorization link.

Connection management: appears as a **"Rho for Slack" row under Settings → Linked Apps** with who approved and when. Home tab shows connection health. **Connections lapse after 30 days without use** and any Rho Admin can reconnect with `/rho-connect`. Revoking the Linked Apps row disconnects the workspace for all users.

### 6.5 Alerts

| Alert | What it sends | Default |
| --- | --- | --- |
| Daily balance alerts | Daily summary of account balances | **9:00 AM ET, every day** |
| Transaction notifications | Money in and out above a chosen amount | **$1,000** |
| Card activity alerts | Card spend above a chosen amount | **$1,000** |

Two destinations: **personal alerts** (DMs, per person) and **one notification channel** (private, per business). Instant Setup creates a private `#rho-notifications` channel. Explicit warning: *"channel alerts show real balances and transaction amounts to everyone in the channel."* Rho will not post alerts to multiple channels, and nothing sends until alerts are turned on.

---

## 7. The Gmail connector

Two surfaces: `/connectors/gmail` (marketing, still gated as "Sign up for early access" / "Join the beta") and `/help-center/expenses/how-to-set-up-the-gmail-connector` (full instructions, written as if GA).

**Shipped in the April 30, 2026 changelog:** *"Connect your Gmail once. Rho pulls in your receipts automatically and matches them to the right transactions - no forwarding rules, no manual uploads. ... Rho only scans for receipts - nothing else in your inbox is read or stored. Admins can extend the connector across the whole team in one action."*

**Contradiction #9.** The marketing page still says "Sign up for early access" and "Join the beta" and the help center documents it as a live, self-serve Settings → Integrations flow, while the changelog announced it four and a half months ago. Three different maturity signals for the same feature.

What it does:
- Scans Gmail for emails matching receipt criteria (subject lines and attachments that look like purchase confirmations), pulls them in, **matches them to the right card transaction automatically**
- **Capture is forward-only from the moment of connection.** Older receipts require manual upload or bulk forward.
- Each teammate connects their own inbox; receipts route into the shared expense view; **receipts from a cardholder's inbox attach only to that cardholder's transactions**
- Keyword criteria are user-editable before and after connecting (Settings → Integrations → Gmail → Manage; "Add custom keywords for merchants or services Rho hasn't identified by default")
- Disconnect instantly from Rho settings. *"No inbox data is retained after disconnection."* Already-attached receipts remain in Rho.
- Explicitly positioned as a **replacement for auto-forwarding rules**: *"Auto-forwarding breaks when card setups or email configurations change - the connector doesn't."*

Prerequisites: a Rho account with at least one active card; a Gmail or Google Workspace address; Gmail admin permission if the org restricts third-party app access.

Data boundary, stated twice: *"Rho only requests read access to messages that match receipt criteria"* and *"We don't access personal messages, calendar events, contacts, or any other Google service."* **[Rho claim]** - Gmail's OAuth scope model does not actually support "read only messages matching a keyword"; the narrowest practical read scope is `gmail.readonly` or `gmail.metadata`. Rho does not name the OAuth scope it requests anywhere in the corpus. This is the single largest unverifiable privacy claim on the AI surface.

Beta incentive: **25% off Google Workspace for 6 months.**

Roadmap statement: *"**When are more connectors coming?** In the pipeline. We will share timing when it is confirmed. The Gmail Connector is just the start."* Only one connector exists at `/connectors/*` in the sitemap.

### 7.1 Receipt matching (the ML-adjacent piece)

April 30, 2026 changelog, "Receipt matching, rebuilt": *"Added **merchant identity verification** to every match, so a receipt from Uber only ever attaches to an Uber transaction. Better **normalization, confidence scoring, and date proximity logic** mean more receipts match automatically - and correctly. Cardholders can now **flag a bad match** directly in the app."*

Rho never calls this AI or ML. It is described in classical matching terms.

---

## 8. Adjacent AI in the product (not agent-accessible)

### 8.1 Rho Close - "intelligent transaction coding"
- Blog "Introducing Rho Close: Intelligent Transaction Coding for Startups", Esther Nguyen, **published May 06, 2026, updated September 01, 2026**. In changelog **May 27, 2026**.
- What it does: reviews chart of accounts, vendor history, and prior coding decisions, then suggests a category for every transaction. One click to generate a first pass; accept in bulk or one at a time; override anything.
- **Nothing syncs until the user approves.** Stated five separate times on `/product/close`.
- Requires a **native accounting integration** (QuickBooks Online, Oracle NetSuite, Sage Intacct via direct integration; Xero via bank feed with coding on the Xero side). CSV exporters cannot use it.
- Learns from every accept and override.
- **Conspicuous:** `/product/close` never uses the words "AI", "LLM", "model" or "machine learning" - except negatively: *"Not a generic model. Yours."* and *"not a generic model trained on someone else's books."* Meanwhile the **homepage** markets the same feature as *"**AI codes every transaction.** Month-end in minutes."* **Contradiction #10** - the product page deliberately de-AI's what the homepage AI-ifies.

### 8.2 OCR in Bill Pay
- Forward invoices to a per-org Bill Pay inbox address; "OCR vendors" (third parties, unnamed) parse and auto-populate a draft bill.
- **Confidence score** surfaced on the bills table as a Green / Yellow / Red accuracy indicator: Green = high confidence, no action; Yellow = review suggested, double-check flagged fields; Red = low confidence, verify before paying.
- Duplicate detection: replying in-thread with image invoices in the body creates duplicates, which are auto-flagged.
- Rho's own FAQ draws the line hard: *"Rho Bill Pay uses automated invoice capture (optical character recognition) to turn a forwarded invoice into a draft bill for your team to review, **not an AI system that approves payments on its own**."*
- Mobile reimbursements shipped OCR receipt capture in the **March 25, 2026** changelog.

### 8.3 Free Invoice Generator "AI Paste"
- `/tools/free-invoice-generator` has an **"Autofill with AI - Paste an email or describe the invoice - we'll fill every step"** control. An unauthenticated, top-of-funnel LLM feature. No documentation of model, provider, or data handling.

### 8.4 Homepage "AI Demo"
- The homepage CTA row is "Open Account / Request Demo / **AI Demo**". No page in the corpus explains what an "AI Demo" is. Undocumented surface.

### 8.5 Rho AI Stack (a credits program, not a product)
- Changelog **February 26, 2026**: *"**Save on AI tools with the new Rho AI Stack.** Real credits for the infrastructure you're already building on. **Claude, AWS, Lovable, ElevenLabs**, and more, all included with Rho."*
- `/perks` opens with *"The best companies are building with AI. **The Rho AI Stack helps pay for it.**"* but the 147-perk library rendered on that page **does not list Claude, AWS, Lovable or ElevenLabs anywhere in the captured 50 visible rows** (it is paginated, "01 – 50 of 147"). AI-adjacent perks visible: Fin/Intercom ($6,500 in Fin AI Agent credits + helpdesk free 1 year), Zendesk (Resolution Suite incl. AI Agents and Copilot free 6 months), Proxima (AI Audiences free 30 days + 20% off), Fazeshift (50% off, tagged "Artificial Intelligence").
- **Contradiction #11.** The headline AI Stack partners named in the changelog are not findable in the perk library as captured. Either the library is paginated past them, or the AI Stack is a separate program with no page of its own. There is **no `/ai-stack` URL in the 1042-URL sitemap.**

---

## 9. Legal framing of AI (ToS + Privacy Policy)

This is the least-marketed and most load-bearing part of the AI surface.

### Terms of Service, Section 27, "AI-Assisted Features"
- Definition: *"features that use artificial intelligence, **including third-party large language models**, to summarize your Rho Account information and to generate responses to questions you or your Users submit."*
- **Optional.** Rho may modify, suspend or discontinue any AI-Assisted Feature, in whole or in part, at any time.
- *"Responses ... are produced automatically and may be **incomplete, inaccurate or out of date**. Your Rho Account remains the **authoritative record** ... you agree to **verify any response against your Rho Account before relying on it**."*
- *"No output ... is legal, financial, investment, accounting or tax advice."*
- Provided **"AS-IS", "AS AVAILABLE" and "WITH ALL FAULTS"**. *"Rho shall not be liable for any action you or any User takes, or fails to take, in reliance on any output."*
- *"Rho and its Third-Party Service Providers process the questions submitted and the Rho Account information needed to respond to them."*

**Rho confirms in its own ToS that third-party LLMs process customer banking data.** It never names the provider on any page.

### Terms of Service, Section 28, "Connected Platforms"
- Defines integrations that deliver Rho data through a third-party platform, *"such as a workplace messaging or collaboration platform"* - i.e. Slack, written generically.
- By enabling one, the customer authorizes Rho to disclose *"**Bank Account balances, Transaction detail and output of the AI-Assisted Features**"* to that platform and to everyone with access to the designated workspace/channel/conversation, **whether or not those individuals are Users of Rho**.
- Customer is solely responsible for configuring access. Rho *"does not control and is not responsible for the Connected Platform, including its availability, security, access controls, or retention or deletion of Data."*
- *"Rho is not affiliated with, and the Rho Services are not endorsed by, the operator of any Connected Platform."*

### Terms of Service, Section 12, "Prohibited Activities" - the agent carve-out
> *"For the avoidance of doubt, your access to or use of any application, integration or AI-Assisted Feature that Rho makes available to you, in the manner Rho intends and in accordance with this Agreement, is not a Prohibited Activity, **including where that use involves automated access to, or automated delivery of, Data**."*

This is an explicit, deliberate legal safe harbor for agentic and automated access. Most bank ToS documents do the opposite.

### Privacy Policy
- *"Our service providers include **providers that host the artificial intelligence models used to power certain features of the Rho Service**, and providers that help us monitor the quality of those features. Service providers may use your information only to provide services to us, and are **not permitted to use it for their own purposes, including to train their own models**."*
- Integrations you enable: data disclosed at the company's direction becomes subject to the third-party platform's own agreement and privacy policy, *"and not under this Policy."*

**Conspicuously absent:** no named LLM provider, no data residency statement for AI processing, no retention period for submitted questions, no statement about whether Rho itself trains on customer data (only that *providers* may not), no DPA reference, no AI-specific security attestation on `/security` or `/trust` (neither page mentions AI, MCP, tokens, or the API at all).

---

## 10. Timeline of Rho's AI-related shipping

| Date | Event | Source |
| --- | --- | --- |
| **2026-02-26** | Changelog: **Rho AI Stack** launched (credits for Claude, AWS, Lovable, ElevenLabs "and more"). Also: Puzzle direct integration; mobile deposits | changelog |
| **2026-03-25** | Changelog: Mobile reimbursements with **OCR** receipt capture; Invoicing beta launches | changelog |
| **2026-04-30** | Changelog: **Gmail Connector** ships (auto receipt capture + matching). **Receipt matching rebuilt** with merchant identity verification, normalization, confidence scoring, date-proximity logic; bad-match flagging. Open Banking API FDX v6.4 support + Plaid SSO | changelog |
| **2026-05-06** | Blog: "Introducing Rho Close: Intelligent Transaction Coding for Startups" (updated 2026-09-01) | /product/close |
| **2026-05-27** | Changelog: **Rho Close** announced; Receipt Notifications Reimagined [beta] | changelog |
| **2026-06-30** | Changelog: no AI items (Invoicing payment portal, recurring invoices, mobile card management) | changelog |
| **2026-07-29** | Blog: **"Introducing: The Rho API"** - API out of beta, MCP server in production, Claude native support live, available to all customers. Author Esther Nguyen. Last updated 2026-09-01 | /blog/introducing-rho-api |
| **2026-08-01** | site-llms.txt as-of date for the Rho API entry ("production MCP server that connects Rho to Claude and other AI agents") | site-llms.txt |
| **2026-08-02 / 08-03** | Competitive verification date used across versus pages; Rho Treasury top yield cited at 4.55% | versus/*, blog |
| **2026-08-03** | Changelog: **"Introducing Rho API"** - *"Read-only is live today. Write access and webhooks are next."* Also: Treasury on mobile, Rho Debit Controls, ACH trace IDs in transaction drawer | changelog |
| **2026-08-03** | Blog published: "Best Banks for AI Startups" | blogcomp |
| **2026-08-20** | Competitive data collection date stamped on `/product/api` (Mercury, Brex, Ramp) and `/product/slack` (Stripe, Mercury, QuickBooks) | product pages |
| **2026-08-25** | Blog published + last updated: **"The Best Banking APIs for Business in 2026"**, 16 min, by Justin Wolz. Ranks Rho #1 for MCP-native read-only | blogcomp |
| **2026-08-31** | Changelog: Incorporation, card payments on invoices, QBO invoice sync, mobile home redesign. **No AI items** | changelog |
| **2026-09-01** | Mastercard World Elite benefits as-of date; Rho Close and Rho API blogs both updated | /perks, blogs |
| **2026-09-02** | Blog: **"Introducing: Rho for Slack"** - daily pulse, real-time alerts, slash commands; **"Rho agent coming soon"**, "Currently available in Beta" | /blog/introducing-rho-for-slack |
| **2026-09-11** (today) | Slack **agent chat in beta for select Rho businesses**. No September changelog entry has been published yet - the Slack launch (9 days old) is **not in the changelog**. `/connectors/gmail` still says "early access" | corpus state |

**Shape of the shipping curve:** Rho went from zero public AI/agent surface to a production MCP server in roughly 5 months (Feb→Jul 2026), then added a Slack conversational agent beta 5 weeks later. The Feb→Apr work was ML-adjacent back-office automation (OCR, matching, coding). The Jul→Sep work is the agent surface proper. Two blog authors carry the whole AI narrative: **Esther Nguyen** (announcements) and **Justin Wolz** (comparison/SEO).

**Launch-date discrepancy:** the blog says the API came out of beta **July 29, 2026**; the changelog puts "Introducing Rho API" under **August 3, 2026**. Five-day gap. **Contradiction #12.**

---

## 11. What Rho says about competitors' AI surfaces

All of the following are **[Rho claim]** unless noted.

### From `/product/api`, competitive table, "Competitive data collected from Mercury, Brex, and Ramp websites as of 2026-08-20"

| | Rho | Mercury | Brex | Ramp |
| --- | --- | --- | --- | --- |
| Programmatic access | Read-only access to accounts and transactions | Pull balances and list transactions via REST API | Transactions API: view transactions, accounts, and statements | Transactions endpoints for spend visibility and querying |
| AI assistant / MCP | Native Claude connection plus an MCP guide in developer docs | **Native MCP server, read-only for AI tools** | **No MCP or AI-assistant integration documented on developer.brex.com** | **Three documented MCP servers** |
| Can tokens move money? | **No, by design** | **Yes, the API can initiate ACH transfers** | **Yes, the Payments API sends ACH, domestic wires, and checks** | **Yes, write operations include bill creation, payment execution, and card issuance** |
| Token security | Scoped, revocable, optional IP allowlists, Owners/Admins only | Scoped tokens, fine-grained permissions, IP allow-listing | Admin-created, scoped at creation, **expire after 90 days unused** | OAuth 2.0 with granular permission scopes |
| Public dev docs | docs.rho.co | docs.mercury.com | developer.brex.com (10 REST APIs) | docs.ramp.com (OpenAPI published) |

Note the internal inconsistency: this table says Brex has **no** documented MCP, while Rho's own `best-banking-apis-for-business` post (5 days later, 2026-08-25) says **"Brex's first-party MCP is available to accounts with Developer API access and currently requires early-access enablement"** and ranks Brex as "Best for Spend Management APIs and Permission-Scoped Agents". **Contradiction #13.**

### From `/versus/ramp` (verified 2026-08-02) - a remarkably candid admission

> "When is Ramp a better fit than Rho? ... **Its agent/AI tooling (hosted MCP server with audited write actions, public CLI) is genuinely ahead**, its in-platform travel booking with price-drop rebooking is real..."

This is Rho conceding the agent-capability lead to Ramp on its own comparison page. `/versus/brex` and `/versus/mercury` contain **no MCP or AI discussion at all** - conspicuous, given Rho's own blog calls Mercury "the closest hybrid" and "the most mature banking API in this comparison".

### From `/blog/brex-alternatives`
> "Developer surface: A hosted MCP server and public CLI with **write access (cards, bills, vendors, spend limits)**, permission-inherited and audit-logged."

### From `/blog/best-banks-for-ai-startups` (published 2026-08-03)
> "**Only one platform in this comparison has a banking MCP server for AI agents** - Rho's API is read-only by design... **Mercury's API is the most mature overall (read and write); Ramp's agent surface writes to spend management, not banking.**"

And the explicit two-sided framing, which is the cleanest statement of Rho's strategic bet anywhere in the corpus:
> "**For the honest comparison**: Mercury's API is the most mature overall - read and write, including money movement - and Ramp's hosted MCP writes to spend-management workflows. **If you want agents moving money today, those do more; if you want agents reading finances with a safety guarantee you can explain to your board, Rho's model is the differentiated one.**"

Also from that post, a claim not made anywhere else: tokens are *"business-scoped, created only by Account Owners and Admins behind a two-factor challenge, shown once, and **secret-scannable**"*. The `rhobat_` prefix is what makes secret-scanning possible; "secret-scannable" is not claimed in the docs themselves.

### From `/blog/best-banking-apis-for-business` (2026-08-25), the MCP landscape table

| Platform | First-party MCP role | Access model | **Agent action level** |
| --- | --- | --- | --- |
| **Rho** | Business banking data and Claude workflows | Scoped credentials and native connection | **Read-only** |
| Mercury | Hosted account intelligence | OAuth | **Read-only** |
| Plaid | Diagnostics, docs, sandbox tooling | OAuth or local | Developer ops, not linked-account access |
| Stripe | Payments, billing, commerce tools | Hosted or local, configurable | **Read/write** |
| Slash | Broad API discovery and passthrough | Hosted MCP + API creds | **Read/write** |
| Modern Treasury | NL access to payments, ledgers, reconciliation | API key (inherits key scopes) | **Read/write**, permission-dependent |
| Brex | Spend and finance operations | OAuth or scoped token | **Read/write**, permission-dependent |

Additional competitor detail from the same post: Mercury's hosted OAuth MCP works with *"Claude, ChatGPT, Claude Code, Codex CLI, and other compatible clients"*; Stripe runs `mcp.stripe.com` plus agent plugins for Claude Code, Codex and Cursor; Modern Treasury's MCP is built on its TypeScript SDK for Claude Desktop, VS Code and Cursor; Slash's MCP exposes exactly three meta-tools (`list_endpoints`, `get_endpoint_schema`, `call_api_endpoint`) and *"can encrypt PAN and CVV data using a customer-provided RSA public key before sensitive values reach the agent ... the documentation indicates that plaintext may otherwise be returned"*.

Rho's own MCP safety checklist (worth noting because it is a list of things Rho's own surface makes moot or does not offer): least-privilege scopes, separate credentials, token expiration, IP allowlisting, **human approval before money moves**, **idempotency keys on every financial write**, audit logs, **webhook signature verification**, credential revocation testing, PAN/CVV exposure prevention, validating AI outputs against source records. Of these, Rho currently offers: scopes, expiration, IP allowlisting, revocation, and PAN/CVV non-exposure. It offers **no idempotency keys, no webhooks, no published audit-log surface, and no approval gate** - because it has no writes to gate.

---

## 12. Customer proof points for agentic use (from the API launch post)

Three named builders, all from `/blog/introducing-rho-api` **[Rho claim]**, no independent verification:

| Builder | Company | What they built |
| --- | --- | --- |
| **Seve Ortale** | Wayve Payments | AI-powered finance dashboard **in about five hours**: auto-categorization, burn rate/runway tracking, an "AI CFO chat", automated weekly board summaries. Wired his own **Genspark-powered AI agent, "Goose"**, directly into Rho's API |
| **Ishan Sheth** | Joinergo | Spend-tracking system built **entirely through Rho's MCP connection to Claude**; per-person and go-to-market spend breakdowns to calculate **acquisition cost per demo** |
| **Justin Hays** | Arbor Management | End-to-end bookkeeping automation. Connected Rho's API **and QuickBooks to Claude through an MCP server he built**; a weekly "**bookkeeping skill**" pulls every transaction, categorizes it, and surfaces anything unfamiliar. Replaces **3-5 hours/week** of work by his team plus a fractional CFO |

The Hays case is the most informative: the composite workflow (Rho MCP + a self-built QuickBooks MCP + a Claude skill) is Rho's own evidence that the read-only boundary is not a blocker for the highest-value use case (close automation), because the *write* target is the accounting system, not the bank.

---

## 13. What is conspicuously NOT stated

1. **No named LLM provider.** The ToS admits "third-party large language models" power AI-Assisted Features; the privacy policy admits "providers that host the artificial intelligence models". Neither Anthropic, OpenAI, Google, nor anyone else is named anywhere in the corpus in that role.
2. **No webhooks.** Confirmed absent three times ("Webhooks: Not yet" in the blog table; "write access and webhooks are next" in the changelog; "Write endpoints and webhooks are planned but are not currently available" in the blog). Every competitor in Rho's own table has them.
3. **No CLI.** Rho's own `/versus/ramp` cites Ramp's "public CLI" as an advantage. Rho has none.
4. **No ChatGPT / OpenAI connector.** Rho's blog explains how to connect banks to ChatGPT generically but never claims Rho works there. The `/product/api` line is "Claude is the natively supported client today."
5. **No documented MCP prompts or resources.** Docs say they exist; docs tell you to go introspect them yourself.
6. **No rate-limit response headers.** Verified absent in live sandbox headers. An agent cannot pace itself against remaining quota.
7. **No idempotency keys** anywhere (nothing to make idempotent yet).
8. **No audit-log API or surface.** Rho's own MCP safety checklist demands "preserve agent and API logs for every action taken"; nothing in the corpus describes where a customer sees API or agent access logs.
9. **The `/integrations` page lists Slack nowhere, Gmail nowhere, Claude nowhere, and the API nowhere.** It shows only Accounting/ERP (Xero, Campfire, Puzzle, Sage Intacct, NetSuite, QuickBooks), HR (BambooHR, Workday, Gusto), and Travel (Navan, Emburse, SAP Concur). Yet both Slack and Gmail are set up *from* Settings → Integrations in the product. The marketing page and the product disagree about what an integration is.
10. **`/security` and `/trust` never mention** AI, LLM, MCP, API, tokens, or agents. There is no AI-specific security posture published.
11. **No multi-entity story for AI.** Claude connects to exactly one business at a time; the Slack workspace connects to exactly one business. Rho sells to multi-entity enterprises (`/solutions/enterprise`: "Streamline accounting and expenses across multiple entities") with no stated path.
12. **No pricing or quota tier for heavy API/agent use.** 60 rpm for everyone, free, forever, with no documented upgrade path.
13. **No statement of what happens to agent-submitted questions.** Retention period, logging, and human review of prompts are all unaddressed.
14. **No `/ai-stack` page** despite the changelog launching "the Rho AI Stack" as a named program.
15. **No September 2026 changelog entry** as of 2026-09-11, so the Slack launch (Sept 2) is not in the changelog.
16. **The Gmail OAuth scope is never named.**
17. **MT103 reference numbers are explicitly withheld** from the transactions API, limiting international wire tracing for agents.
18. **No dispute indicator** in v1 (Rho flags this itself).

---

## 14. Full contradiction register

| # | Contradiction | Pages |
| --- | --- | --- |
| 1 | Auth guide lists **3 scopes**; OpenAPI lists **5** (adds `cards:read`, `invoicing:read`) | docs_v1_auth.md vs api_v1_openapi.md |
| 2 | Getting Started says v1 "covers accounts and transactions"; statements, cards and invoicing are all live | docs_v1_getting-started.md vs 4 other docs + sandbox |
| 3 | OpenAPI declares `Type: oauth2` with `Token URL: https://app.rho.co/settings/access-tokens` (a settings page, not a token endpoint) | api_v1_openapi.md vs docs_v1_partner-auth.md |
| 4 | Accounts enum uses `investment`; statements enum uses `treasury` for the same concept | accounts_listaccounts.md vs statements_liststatements.md |
| 5 | `/claude-code` hero promises "$500 in Claude credits"; terms deliver a **cash statement credit** contingent on first spending $500 at Anthropic | /claude-code hero vs footnote 1 |
| 6 | `/setupclaw` body: deposit "within the first 90 days ... maintain it for 30 days"; terms: "first thirty (30) days" | /setupclaw body vs footnote 1 |
| 7 | `/setupclaw` competitor table (Mercury $350/mo Pro, Ramp $12/user/mo) vs blog (Mercury $29.90-$299/mo, Ramp Plus $15/user/mo + unpublished platform fee) | /setupclaw vs /blog/best-banks-for-ai-startups |
| 8 | Slack commands: blog says `/rho balances`, `/rho transactions`, `/rho accounts`; help center says `/rho-accounts`, `/rho-transactions`, no balances command | blog 09/02 vs help center |
| 9 | Gmail connector: shipped in Apr 30 changelog, documented as GA in help center, still "early access / join the beta" on `/connectors/gmail` | three surfaces |
| 10 | Homepage: "**AI** codes every transaction"; `/product/close` avoids "AI" entirely and says "Not a generic model" | homepage vs /product/close |
| 11 | Rho AI Stack names Claude, AWS, Lovable, ElevenLabs; none appear in the visible perk library and there is no `/ai-stack` URL | changelog 02/26 vs /perks vs sitemap |
| 12 | API launch date: blog says **July 29, 2026**; changelog says **August 3, 2026** | blog vs changelog |
| 13 | `/product/api` says Brex has "**No MCP or AI-assistant integration documented**"; `/blog/best-banking-apis-for-business` says Brex has a first-party MCP in early access | product page (08/20 data) vs blog (08/25) |
| 14 | Nav label everywhere: "**Rho API New Banking and payments via API**" - contradicts read-only on every single page of the site | global nav vs everything |
| 15 | `site-llms.txt`: "**Read-only API** for Rho account and transaction data ... production MCP server"; `site-llms-full.txt`: "**Programmatic access to accounts, payments, and card data**" with no read-only qualifier and **no mention of MCP at all** | the two machine-readable summaries |
| 16 | Help center says connected AI tools can access **Accounts, Transactions, Statements**; the API exposes **Cards and Invoicing** too | help center vs OpenAPI |
| 17 | Documented pagination cursor example `{o, d}` shape does not match the live sandbox cursor `{v, f, t}` shape | docs_v1_pagination.md vs sandbox |
| 18 | `/product/api` says tokens "auto-expire after inactivity" with no number; docs specify **45 days** | product page vs docs_v1_auth.md |

**#14 and #15 matter most for an LLM reading Rho's own site.** The global navigation label and the "full" machine-readable summary both describe the API as supporting payments. A model crawling rho.co without reading docs.rho.co would conclude the Rho API can move money. It cannot.

---

## 15. Precise capability boundary for an agent connected to Rho today

### An agent CAN:
- Enumerate every account with type, display name, current balance (minor units), masked account and routing last-4
- Enumerate every transaction across every rail, filtered by account, account type, transaction type (33 values), status, user, card, free-text search, initiated/posted date windows, and min/max amount
- See per-employee and per-card attribution on card spend
- See ACH trace numbers and wire IMAD/OMAD for outbound payment tracing (not MT103)
- Read counterparty name and logo, bank-supplied memo, user-entered note
- See which transactions are **`awaiting_approval`** (the approval queue, read-only)
- Enumerate all cards including canceled and expired, with limits, limit type, current and pending spend, spend window, usage windows, billing and shipping addresses, and MCC allow/block lists
- Enumerate finalized statements with opening/closing balances, total credits/debits/fees, and for credit statements repayment date, spending, repayments, cashback
- Fetch short-lived signed URLs for statement PDFs, transaction attachments, and invoice PDFs (each ~15 min)
- Enumerate invoices (with line items, payments, and full activity log) and invoicing customers (with total revenue and last invoice ID)
- Do all of the above through REST or through MCP, with identical semantics, scopes and errors

### An agent CANNOT:
- Initiate any payment: ACH, wire, international wire, check, internal transfer, bill pay
- Approve, reject, reschedule or cancel anything in the approvals queue
- Create, issue, lock, unlock, cancel, or modify any card, or change any spending limit or MCC rule
- Add, remove, or modify users, roles, or permissions
- Change any account setting, including 2FA, alerts, or debit controls
- Create, edit, send, cancel or mark-paid any invoice, or create/edit/delete an invoicing customer
- Buy, sell, or move Treasury positions
- Write a note, memo, label, department, or receipt attachment back to a transaction
- Trigger an accounting sync or accept a Rho Close suggestion
- Receive a push/webhook event (must poll, at ≤60 rpm/token)
- Access more than one Rho business per Claude connection or per Slack workspace
- See a full PAN, CVC, or card expiration date
- Access anything with a token created by a non-Owner/non-Admin (none can exist)
- Act on money from Slack ("Not yet")

### The four independent enforcement layers Rho describes
1. **Surface**: the v1 API has no non-GET operation to call
2. **Scope**: every scope is `*:read`; there is no writable scope to request
3. **Role**: only Account Owners and Admins can mint a token or authorize an OAuth/Claude/Slack connection, behind 2FA
4. **Credential**: tokens expire (max 1 year, 45-day idle), are capped at 20 per business, can be IP-allowlisted (100 entries), and revoke instantly

The result Rho leans on hardest: *"a leaked token cannot move money"* and *"an agent can see everything and move nothing."*

---

## 16. Strategic read

Rho's AI strategy is a **deliberately narrow, aggressively marketed safety position**. The company shipped the smallest possible agent surface (14 GETs) and then spent more words defending the boundary than describing the capability: the read-only claim appears at least 20 times across `/product/api`, the help center, the launch blog, the ToS, and three comparison posts.

Three things make the position coherent rather than merely limited:
1. **The MCP server is not a wrapper afterthought.** *"Most financial APIs predate agents; MCP got bolted on. This one shipped with its MCP server in production. Not a roadmap item, the architecture."* The 1:1 REST↔MCP contract, frozen tool names, and shared scope/error model back that up.
2. **The frozen-tool-name guarantee** is the strongest agent-facing compatibility promise in the corpus and is aimed squarely at saved skills and automations. No competitor is quoted making it.
3. **The ToS carve-out for automated access** is an explicit legal license for agentic use, which most bank agreements withhold.

The strategic risk Rho itself publishes: on `/versus/ramp` it concedes Ramp's agent tooling is "genuinely ahead", and on `/blog/best-banks-for-ai-startups` it concedes "if you want agents moving money today, those do more". The read-only stance is a differentiator only until write-with-approval-gates becomes table stakes, and Rho has already announced that write access and webhooks are next. The Slack agent beta (Sept 2026) is the first Rho-owned inference surface rather than a data pipe to someone else's model, and it is the surface most likely to become the write path first, because it already has a per-person identity, a role gate, and a human in the loop by construction.

---

## 17. Source file index (absolute paths)

Core pages:
- `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/pages/core/product__api.txt`
- `.../pages/core/claude-code.txt`, `.../orion.txt`, `.../setupclaw.txt`, `.../connectors__gmail.txt`, `.../product__slack.txt`, `.../grow__slack.txt`, `.../changelog.txt`, `.../integrations.txt`, `.../product__close.txt`, `.../perks.txt`, `.../faq.txt`, `.../homepage.txt`, `.../versus__ramp.txt`, `.../policies__terms-of-service.txt`, `.../policies__privacy-policy.txt`, `.../tools__free-invoice-generator.txt`

Help center:
- `.../pages/help/help-center__the-rho-api.txt` (contains the full text of all 4 API articles)
- `.../help/help-center__the-rho-api__connect-claude-to-your-rho-account.txt`
- `.../help/help-center__the-rho-api__connecting-al-tools-to-your-rho-account.txt` (note the URL slug typo: "al" not "ai")
- `.../help/help-center__the-rho-api__what-connected-al-tools-have-access-to-in-your-rho-account.txt`
- `.../help/help-center__the-rho-api__build-a-custom-integration-with-rho.txt`
- `.../help/help-center__rho-slack-app__{understanding,how-to-use,how-to-set-up-rho-alerts-in-slack,how-to-install-and-connect}*.txt`
- `.../help/help-center__expenses__how-to-set-up-the-gmail-connector.txt`
- `.../help/help-center__bill-pay__understanding-ocr-technology-at-rho.txt`

Docs and API reference:
- `.../docs/docs_v1_mcp.md`, `docs_v1_auth.md`, `docs_v1_partner-auth.md`, `docs_v1_versioning.md`, `docs_v1_rate-limits.md`, `docs_v1_pagination.md`, `docs_v1_getting-started.md`, `docs_v1_accounts.md`, `docs_v1_transactions.md`, `docs_v1_cards.md`, `docs_v1_statements.md`, `docs_v1_invoicing.md`, `api_v1_openapi.md`
- `.../api/*.md` (14 operation pages)

Sandbox (captured 2026-09-11 23:22 UTC):
- `.../sandbox/{accounts,cards,transactions,statements,invoicing_invoices,invoicing_customers}.{json,headers}`

Blog:
- `.../pages/extra/blog__introducing-rho-api.txt` (fetched this pass)
- `.../pages/extra/blog__introducing-rho-for-slack.txt` (fetched this pass)
- `.../pages/blogcomp/blog__best-banking-apis-for-business.txt`
- `.../pages/blogcomp/blog__best-banks-for-ai-startups.txt`
- `.../pages/blogcomp/blog__brex-alternatives.txt`, `blog__ramp-alternatives.txt`, `blog__mercury-alternatives.txt`

Machine-readable:
- `.../site-llms.txt`, `.../site-llms-full.txt`, `.../all-urls.txt`
