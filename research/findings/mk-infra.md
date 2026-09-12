# API-First Banking and Embedded Finance Infrastructure, 2026
## Independent research to position the Rho API by contrast

Researched 2026-09-11. Local Rho corpus + independent web sources. Every material claim carries a source URL and a date.
Rho's own assertions are marked **[Rho claim]**, especially anything Rho says about a competitor.

---

## 0. Executive answer up front

Rho's v1 API is **read-only over its own customers' own data**. Five resources, fourteen operations, all `GET`.

That puts Rho in a category that is **not** bank-as-a-service, **not** embedded finance, **not** payment-ops software, and **not** data aggregation. It is the **first-party account-data API** category: the incumbent-bank "treasury reporting API" pattern, rebuilt for a fintech's own customer base, with an MCP server bolted to the front.

- **Who Rho actually competes with there:** Mercury's read-only MCP tier, Brex's Transactions API, Ramp's read endpoints, Slash, and, at the enterprise end, Wells Fargo Gateway / Capital One DevExchange / JPMorgan-style commercial reporting APIs. Rho's real differentiator in that set is not the REST API (everyone has one) but that the MCP server shipped in production at launch and is listed in Anthropic's connector directory.
- **Who Rho does NOT compete with:** Increase, Column, Unit, Treasury Prime, Synctera, Stripe Treasury/Issuing, Modern Treasury, Brex Embedded. Those sell the ability to *originate* money movement or to *manufacture* bank accounts for someone else's end users. Rho's API cannot do either, by design.
- **The exposed flank:** Plaid, Teller, and Stripe Financial Connections can already read a Rho account without Rho's permission or participation, on the customer's authorization. Rho's read-only API competes with *aggregators reading Rho* more directly than it competes with anything Rho names in its own comparison table.
- **The build to become write-capable:** roughly 9 workstreams, of which the hard ones are not engineering. They are Webster Bank sponsor-bank approval for programmatic origination, NACHA/Reg E/OFAC controls on an API-originated payment, dual-control and approval semantics, idempotency, webhooks, and liability allocation for an agent-initiated payment. Detail in §9.

---

## 1. The Rho baseline (verified from the corpus, not inferred)

### 1.1 Surface area, exact

Source: `docs.rho.co/api/v1/openapi` (local: `rho/docs/api_v1_openapi.md`), and 14 operation reference pages in `rho/api/`.

| Resource | Operations | Verb |
| --- | --- | --- |
| Accounts | `GET /accounts`, `GET /accounts/{account_id}` | GET |
| Cards | `GET /cards`, `GET /cards/{id}` | GET |
| Transactions | `GET /transactions`, `GET /transactions/{id}`, `GET /transactions/{transaction_id}/files/{file_id}` | GET |
| Statements | `GET /statements`, `GET /statements/{id}` | GET |
| Invoicing | `GET /invoicing/customers`, `GET /invoicing/customers/{customer_id}`, `GET /invoicing/invoices`, `GET /invoicing/invoices/{invoice_id}`, `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | GET |

**14 operations. Zero POST, PUT, PATCH, DELETE.** API version 1.0.0. Production `https://rhoapi.rho.co/api/v1`, sandbox `https://rhoapi-sandbox.rho.co/api/v1`.

### 1.2 Auth, limits, contract

| Fact | Value | Source |
| --- | --- | --- |
| Token prefix | `rhobat_` | `docs/v1/auth` |
| Max active tokens per business | **20** | `docs/v1/auth` |
| Token inactivity expiry | **45 days** (creation starts the clock if never used) | `docs/v1/auth` |
| Max token lifetime | **1 year**, expiration required | `docs/v1/auth` |
| IP allowlist entries | up to **100** per token | `docs/v1/auth` |
| Who can create | Account Owners and Admins only, 2FA challenge at creation | `docs/v1/auth` |
| Scopes (openapi) | `accounts:read`, `cards:read`, `invoicing:read`, `statements:read`, `transactions:read` | `api/v1/openapi` |
| Scopes (auth guide) | only `accounts:read`, `transactions:read`, `statements:read` | `docs/v1/auth` — **contradiction, see §11** |
| Rate limit, per token | ~**60 requests/minute** | `docs/v1/rate-limits` |
| Rate limit, per source IP | ~**600 requests/minute** | `docs/v1/rate-limits` |
| Error format | RFC 9457 / RFC 7807 `application/problem+json` | `api/v1/openapi`, `docs/v1/auth` |
| Money format | integer minor units + ISO 4217 currency, `amount` is an object not a scalar | `docs/v1/transactions` |
| Pagination | cursor, `page_size` + `page_token`, `next_page_token` null at end | `docs/v1/pagination` |
| Deprecation notice | at least **15 days** | `docs/v1/versioning` |
| Sandbox auth | any non-empty bearer token accepted | `docs/v1/getting-started` |
| Webhooks | **none** | absent from all 13 doc pages; Rho's own blog lists them as "coming next" |
| SDKs | **none published** | absent from corpus; OpenAPI spec only |
| Idempotency keys | **n/a** (no writes); `docs/v1/transactions` uses the word only for *ingestion* idempotency on the reader's side | `docs/v1/transactions` |

### 1.3 Partner OAuth (the one genuinely platform-shaped piece)

Source: `docs.rho.co/docs/v1/partner-auth` (local `rho/docs/docs_v1_partner-auth.md`).

- OAuth 2.0 Authorization Code **with PKCE (S256 required)**, authorization server `https://auth.rho.co`, `audience=https://rhoapi.rho.co`.
- Clients are **registered manually by Rho** via email to `api-partner-request@rho.co`. No self-serve client registration.
- Access token TTL **900 seconds (15 minutes)**. Refresh tokens **single-use, rotating**, **30 days rolling**. The grant itself **1 year**, after which the customer re-approves.
- One active grant per app per business. Only Account Owners and Admins can approve.
- Discovery published at `https://auth.rho.co/.well-known/openid-configuration`.

This is the piece that makes Rho *readable by third-party software* rather than only by the customer's own scripts. It is the seed of a platform. It is also the piece with no self-serve onboarding.

### 1.4 MCP

Source: `docs.rho.co/docs/v1/mcp`, `docs/v1/versioning`.

- Streamable HTTP at `/mcp/v1`, **1:1 with the REST API**. Same auth, same scopes, same error behavior.
- Protocol versions advertised: **`2026-07-28`, `2025-11-25`, `2025-06-18`**. Older versions and JSON-RPC batches rejected.
- Tool names derive from frozen v1 `operationId`s, so **"tool names will never change"** — an explicit contract aimed at agent skills and saved automations.
- Two auth paths: direct API Access Token, or "linked apps" via the MCP client's OAuth connection.
- Rho is listed in **Anthropic's MCP connector directory**; Claude is "the natively supported client today" [Rho claim, `rho.co/product/api`, page current as of August 2026].

### 1.5 Rho's own roadmap statement, on the record

From `rho.co/blog/introducing-rho-api`, published **2026-07-29**, last updated **2026-09-01**:

> "Read access is live today. Acting on Rho programmatically is where the platform is headed."
> "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval, the finance tasks you'd rather delegate. Read ships first because everything else stands on it."
> FAQ, "What's coming next?": "Acting on Rho, not just reading it: **write access, webhooks, more endpoints**."

And from Rho's own ranking post, `rho.co/blog/best-banking-apis-for-business`, published and last updated **2026-08-25**:

> "Write endpoints and webhooks are planned but are not currently available."

So the read-only posture is explicitly framed by Rho as **stage one**, not a permanent product philosophy — even while the product page argues read-only is a security *feature* ("Read-only by design", "No, by design").

### 1.6 Sandbox reality check

Live sandbox capture (`rho/sandbox/transactions.json`, fetched 2026-09-11, HTTP 200 via Cloudflare):

- 20 fixture transactions, `transaction_type` values observed: `card_debit` (8), `credit_repayment` (6), `card_refund` (3), `rewards_cashback_redemption` (1), `ach_credit` (1), `check_payment` (1).
- `status` values observed: `settled` (17), `pending` (2), `failed` (1). Docs additionally name `awaiting_approval`.
- `account_type` values: `checking`, `savings`, `credit`, `investment`, `rewards`.
- Records carry `money_movement_id` to group legs of one movement, `tracking_number` for ACH NACHA trace / wire IMAD-OMAD (MT103 explicitly **not** returned), `user_id`/`card_id` attribution, and `attachments` with `file_id`/`file_name` but **never a signed URL inline** (a separate call mints a short-lived one).

The data model is genuinely good — better than most aggregator-flattened feeds. That is the substantive case for the product. It is still a reader.

---

## 2. Taxonomy: six different businesses that all say "banking API"

The single most common analytical error in this space is treating these as one market. They are six.

| Layer | What is actually sold | Who buys | Money movement | Charter position | Examples |
| --- | --- | --- | --- | --- | --- |
| **A. Chartered API bank** | A bank charter with an API as the only UI | Fintechs, platforms, other banks | Originates on own rails | Owns the charter | Column, Increase (post-2025), Lead Bank, Cross River |
| **B. BaaS middleware** | Program management + ledger + compliance on top of someone else's charter | Fintechs and vertical SaaS | Originates via sponsor bank | Rents a charter | Unit, Synctera, Treasury Prime (historically) |
| **C. Payment ops / ledger software** | Orchestration, ledgering, reconciliation across the banks you already have | Fintechs, marketplaces, lenders, payroll | Instructs money movement at your banks | None | Modern Treasury |
| **D. Embedded finance by a card issuer** | Your software issues *their* cards to *your* customers | B2B software vendors, procurement/travel/ERP | Issues and authorizes card spend | Rents issuer's program | Brex Embedded, Stripe Issuing |
| **E. Data aggregation / connectivity** | Read access to accounts the vendor does not hold | Any app needing another bank's data | Some (Plaid Transfer, Teller/Zelle) | None | Plaid, Teller, Stripe Financial Connections, MX, Finicity |
| **F. First-party account API** | Programmatic access to the customer's own account at *this* provider | The provider's own existing customers | Depends: write-capable or not | Provider's own (or sponsor's) | **Rho**, Mercury, Brex, Ramp, Slash, Wells Fargo Gateway, Capital One DevExchange |

**Rho is exclusively in F, on the read-only side of F.** Nothing in Rho's API touches A, B, C, D, or E.

---

## 3. Vendor profiles

### 3.1 Increase — Layer A (now literally a bank)

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | "Modern bank infrastructure that enables technology companies to programmatically store, move, and reconcile money." 8 capabilities: ACH, bank accounts, cards, checks, wires, real-time payments, FedNow, push-to-card | https://increase.com/ (2026-09-11) |
| Customer | Technology companies building financial products | https://increase.com/ |
| Charter | Founder Darragh Buckley acquired **Twin City Bancorp** (single-branch, Longview, Washington). Fed Reserve Bank of San Francisco approved 100% of voting shares **June 2025**. Rebranded **Increase Bank**, public launch **2026-07-30**. Bank had **$114.6M** assets as of **2026-03-31**. Price undisclosed | https://www.bankingdive.com/news/fintech-increase-buys-washington-bank-stripe/826586/ (2026-07-30) |
| Remaining partner banks | Grasshopper Bank, First Internet Bank of Indiana, Core Bank — multi-bank customers keep them | https://increase.com/ legal footer; Banking Dive (2026-07-30) |
| Scale claims | "Gusto, Ramp, and Stripe rely on Increase technology to process more than $500B annually"; Wikipedia: "hundreds of billions in payments volume per year" | increase.com (2026); https://en.wikipedia.org/wiki/Increase_(company) |
| Recognition | Forbes Fintech 50 in 2025 and 2026; ACH offering = American Banker Innovation of the Year 2025 | Wikipedia (2026) |

**Pricing — Increase is the outlier that publishes a real rate card** (https://increase.com/pricing, read 2026-09-11):

| Item | Price |
| --- | --- |
| Same-day ACH origination | **$2.00** / transaction |
| Next-day ACH origination | **$0.50** / transaction |
| ACH return | **$5.00** / transaction |
| Unauthorized ACH return | **$15.00** / transaction |
| Late return processing | **$25.00** / transaction |
| Wire origination / drawdown origination | **$15.00** each / transaction |
| RTP origination | **$2.50** / transaction |
| FedNow origination | **$2.50** / transaction |
| Check issuance (Increase fulfillment) | **$3.00** / check, **$1.00** / additional page |
| Check return | **$10.00** / check |
| Lockbox | **$20.00** / address / month + **$5.00** / check deposited |
| Virtual card creation | **$0.25** / card |
| Physical cards | first **5 free**, then contact sales |
| Card dispute | **$15.00** / dispute |
| Account numbers | first **10 free**, then contact sales |
| Monthly subscription | none listed |

Note the direct contradiction with a third-party audit (§8) that asserts no BaaS provider publishes a rate card. Increase does.

**Relevance to Rho: none as a competitor.** Increase is what a company would buy if it wanted to *become* Rho. It is a useful benchmark for what "write-capable" costs at the unit level: a programmatic ACH is worth $0.50–$2.00 and a wire $15.00 at the infrastructure layer.

### 3.2 Column — Layer A (nationally chartered developer bank)

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | Banking infrastructure by API on its own national charter: ACH, domestic wires, international wires (multi-currency + FX quotes), real-time payments + request-for-payment, book transfers with hold/clear, checks + lockbox, FDIC-insured accounts (checking, savings, trust, subledger, clearing, sweep), account numbers, entities with KYC/KYB, loans (origination, disbursement, servicing, sale), counterparties + IBAN validation, webhooks, settlement reports, simulation endpoints | https://docs.column.com/ (2026-09-11) |
| Charter | **Nationally chartered bank, Member FDIC**, "Column NA". Described as "the only nationally chartered developer infrastructure bank in the US" | https://column.com/ (2026-09-11); https://www.fintechfutures.com/core-banking-technology/developer-infrastructure-bank-column-launches-to-cut-middleware-bloat |
| Leadership | William Hockey (Plaid co-founder) and Annie Hockey | fintechfutures.com |
| Named customers | Brex, Mercury, Ramp, Best Egg; "seed-stage fintech to global financial institution" | https://column.com/ (2026-09-11) |
| 2026 events | Developer documentation rebuilt from scratch **June 2026**; **Bilt Card 2.0** launched **2026-02-07**, issued by Column N.A. | search result citing Column changelog (2026) |
| Money movement | **Yes, fully**. Explicitly "defined by an OpenAPI spec" | https://docs.column.com/ |
| Pricing | **Not public.** No pricing page content retrievable; no rate card found | https://column.com/pricing returned empty (2026-09-11) |

**Relevance to Rho:** Column is the supply side of the market Rho is not in. Notable that **Mercury and Brex are Column customers** — meaning Rho's two nearest neighbours in Layer F have, underneath them, a chartered API bank that already exposes full write primitives. That is part of why Mercury and Brex can offer write APIs and Rho (on Webster/Santander) has a harder path.

### 3.3 Unit — Layer B (BaaS middleware, multi-bank)

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | "Build financial products on real infrastructure. Store, move, spend, and lend money inside your product." Deposit accounts, FBO wallets, credit accounts; ACH, wire, check, real-time payments, cross-border; brandable debit / charge / revolving credit cards; merchant cash advances, lines of credit, credit cards | https://www.unit.co/ (2026-09-11) |
| Customer | Vertical SaaS, small-business software, real estate / property management, benefits admin, freelancer/creator platforms, nonprofits and membership orgs — i.e. **software companies serving SMBs**, not the SMB itself | https://www.unit.co/ |
| Charter | None. Multiple FDIC-member partner banks, unnamed on homepage. Claims "direct, bare-metal access to the Federal Reserve, the card networks, and bank partners" | https://www.unit.co/ |
| Compliance posture | 99.999% uptime claim; SOC 2 Type 2 + PCI DSS | https://www.unit.co/ |
| Regulatory history | Partner **Thread Bank** received an **FDIC consent order dated 2024-05-21, made public 2024-06-28**, requiring documented risk assessment of fintech partners; Thread supported ~35 fintech programs and was Unit's fourth bank partner | https://www.bankingdive.com/news/fdic-thread-bank-baas-oversight-fintech-partner-aml/720313/ |
| Pricing | **Not a public rate card.** Unit's docs describe a configurable fee framework where "all fees default to $0, and can be updated by reaching out to your Unit contact"; sample end-customer fees cited: $1 same-day ACH, $10 wire, $4 physical card, $1.50 check payment; platform fees invoiced monthly | https://www.unit.co/docs/api/fees/overview/ (accessed 2026-09-11) |

### 3.4 Treasury Prime — Layer B, mid-pivot

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells (2026) | "Bank OS" embedded banking platform, sold to **both** banks/credit unions and fintechs. Modules: digital experiences, accounts/sub-ledger, payment rails, compliance. Partner Marketplace with "20+ leading partners" for KYC, monitoring, instant funding | https://www.treasuryprime.com/ (2026-09-11) |
| Claimed scale | "$10B+ in new deposits", "2.5M+ new active accounts", "$90B+ in Transactions". **No partner-bank count given** despite claiming "the industry's largest network of banks" | https://www.treasuryprime.com/ |
| Strategic pivot | **February 2024**: reoriented to sell embedded banking tech **directly to banks** rather than to fintechs. CEO Chris Dean: "the future of embedded banking is through bank-direct, fintech partnerships." Layoffs reported at roughly **half of ~100 employees** | https://www.bankingdive.com/news/treasury-prime-lay-off-40-50-employees-marketing-liaison-direct-fintech-partner-chris-dean/708770/ ; https://www.fintechfutures.com/partnerships/treasury-prime-trims-workforce-amid-strategic-pivot-to-focus-on-direct-to-bank-partnerships |
| Funding context | $40M Series C led by BAM Elevate, roughly a year before the pivot | Banking Dive (2024) |
| Acquisition status | **No acquisition found** as of 2026-09-11. Company appears independent | search, 2026-09-11 |
| Pricing | Not public; described by third-party audit as "revenue share with partner banks" | https://boldrails.com/resources/baas-pricing-transparency (audit dated **2026-08-02**) |

Treasury Prime is the cautionary example for the middleware layer: squeezed between chartered API banks below and direct bank software above.

### 3.5 Synctera — Layer B

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | End-to-end banking platform: bank accounts + digital wallets, card programs (debit/credit), money movement (account funding and payments), core banking, card processing, end-user onboarding. "Everything you need to build financial products and effectively manage ongoing operations" | https://synctera.com/ (2026-09-11) |
| Customer | FinTechs, embedded-banking providers, **and banks** (tools to "build and scale a compliant sponsor banking program"); dedicated Canada offering | https://synctera.com/ |
| Model | Matchmaker: "Synctera connects you with the banks in our network that best align with your product vision and timeline"; partner banks get "complete control and visibility into program data, reconciliation, operations, and risk management" | https://synctera.com/ |
| Funding | **$15M raised March 2025**, co-led by Fin Capital and Diagram Ventures; total raised **$94M**. **Bolt** signed as largest customer to date; Unified Signal also named | https://techcrunch.com/2025/03/11/baas-startup-synctera-raises-15m-signs-bolt-as-a-customer ; https://www.synctera.com/news/banking-as-a-service-leader-synctera-raises-15m-and-signs-bolt-its-largest-customer-to-date |
| Earlier distress | Laid off staff in March 2024 | https://techcrunch.com/2024/03/26/baas-startup-synctera-layoffs-fintech/ |
| Pricing | Not public. Sales-led; pricing page routes to a contact form as of **2026-05-06**. Third-party characterisation: implementation fee + platform fee + monthly minimum, plus revenue share with partner banks | https://www.xpay.sh/saas-pricing/synctera/ ; https://boldrails.com/resources/baas-pricing-transparency (2026-08-02) |

### 3.6 Stripe — three distinct products, three distinct layers

Stripe is the only vendor here occupying **three** taxonomy slots at once, and conflating them is the second-most-common analytical error.

**(a) Stripe Treasury — 2026 repositioning matters a great deal to Rho.**

Historically Treasury was Layer B/D: BaaS for platforms (Shopify Balance was the flagship). As of the 2026 site it reads as a **direct business banking product** competing with Rho, Mercury, and Brex:

> "store funds, convert currencies, use spend cards, send payouts, and access stablecoins — right from the Stripe Dashboard."
> "2% cashback on eligible purchases wherever Mastercard is accepted." "No monthly fees or minimum balance required."
> "Global payouts to 160 countries"; US businesses can send money to each other "instantly and for free" via Stripe financial accounts.
> — https://stripe.com/treasury (2026-09-11)

Both framings still coexist: https://stripe.com/treasury/platforms remains live for the embedded use case. Analysts describe Treasury as "looking far less like a banking-as-a-service add-on and far more like a full operating account for internet-native businesses," with **balances in 15 currencies by the end of 2026** for US and UK businesses (https://neobanque.ch/blog/stripe-sessions-2026-treasury-stablecoins-ai/, 2026).

Bank partners: **Fifth Third Bank, N.A.** (via Newline) and Goldman Sachs Bank USA (https://stripe.com/treasury, 2026-09-11; https://www.fintechfutures.com/baas/stripe-selects-newline-by-fifth-third-bank-to-expand-its-embedded-financial-services-offering). FDIC pass-through to $250,000.

Published pricing (https://stripe.com/pricing, 2026-09-11):

| Item | Price |
| --- | --- |
| Account management | Included, no storage fee, no minimum balance |
| ACH funding | Included |
| Wire | **$2.00** per wire |
| Instant currency conversion | from **0.5%** of converted amount |
| Cards with Treasury | Included, no cross-border or FX fees |

**(b) Stripe Issuing — Layer D.** Published pricing (https://stripe.com/pricing, 2026-09-11):

| Item | Price |
| --- | --- |
| Virtual card creation | **$0.10** per card |
| Physical card | **$3.50** per standard physical card |
| Dispute | **$15.00** per dispute |
| Cross-border transaction | **1% + 30¢** |
| FX conversion | additional **1%** |

**(c) Stripe Financial Connections — Layer E, and a direct substitute for Rho's read API.** Published pricing (https://stripe.com/pricing, 2026-09-11):

| Item | Price |
| --- | --- |
| Instant bank account verification | **$1.50** per successful instant verification |
| Micro-deposit verification | free |
| Balances | **$0.10** per successful API call |
| Account owners | **$1.50** per successful API call |
| Transactions | **$0.30** per institution per account holder per month |

That last line is the number to hold onto. **$0.30 per account per month buys a third party a transaction feed from a bank account** — including, in principle, a Rho account. That is the price ceiling on read-only bank data as a standalone product. It is effectively zero.

### 3.7 Modern Treasury — Layer C

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | **Software, not a bank.** "One API for multi-rail payments, programmable accounts, real-time reporting, and built-in compliance." Products: Payments (ACH, wires, RTP, FedNow, checks, push-to-card, stablecoins), Ledgers, Stablecoins, expected payments, reconciliation, compliance | https://www.moderntreasury.com/ (2026-09-11) |
| Customer | Fintechs, marketplaces, lenders, payroll products, multi-bank finance teams | moderntreasury.com; corroborated by Rho's own review |
| Bank model | Starts with an integrated PSP, "add direct bank partners as you grow, without changing your integration" | https://www.moderntreasury.com/ |
| Scale | "$600 billion in payments", 99.99% uptime. Elsewhere: "more than $400 billion for companies like Anchorage Digital, Float, Gusto, Navan, Procore, and Sling Money" | moderntreasury.com (2026); https://www.moderntreasury.com/newsroom/press-releases |
| 2026 move | **February 2026**: launched **Payments**, an integrated PSP for fiat and stablecoins | https://www.moderntreasury.com/newsroom/press-releases/modern-treasury-launches-payments |
| Funding | ~$183M raised; ~$2B valuation | https://pitchbook.com/profiles/company/232149-34 ; https://tracxn.com/d/companies/modern-treasury (2026) |
| MCP | First-party MCP server built on its TypeScript SDK, for Claude Desktop, VS Code, Cursor — **read/write, permission-dependent** [Rho's own characterisation] | https://www.rho.co/blog/best-banking-apis-for-business (2026-08-25) |
| Pricing | Three components: platform access, payment usage (per rail), accounts + compliance (KYB/KYC, transaction monitoring). "Exact pricing depends on volume, rails used, and account structure." **"All platform and usage fees apply toward a single minimum commitment."** Annual terms. Per-unit costs fall with volume. **No published figures** | https://www.moderntreasury.com/pricing (2026-09-11) |

Modern Treasury is the clearest "ledger/ops software, not a bank" case in the set, and it is the one whose MCP server most directly makes the counter-argument to Rho's read-only positioning: an MCP server *can* be write-capable and still be safe, if it inherits key scopes.

### 3.8 Brex — two products, two layers

**Brex's own first-party API (Layer F, write-capable).** 10 published REST APIs at https://developer.brex.com/ (2026-09-11), verbatim descriptions:

| API | Description |
| --- | --- |
| Accounting | "View and manage accounting data" |
| Budgets | "Manage budgets and budget programs" |
| Expenses | "View and manage card expenses data, receipt match and receipt uploads" |
| Fields | "View and manage fields and their options" |
| Onboarding | "Refer your customers and personal contacts to Brex and prefill signup information" |
| **Payments** | **"Manage vendors and send ACH, domestic wires, and checks"** |
| Team | "Manage users, locations, departments, and cards" |
| Transactions | "View your transactions, accounts, and statements" |
| Travel | "View trips made in Brex Travel" |
| Webhooks | "Send real-time notifications based on events" |

Rho's competitive table says Brex has "10 REST APIs" and that "the Payments API sends ACH, domestic wires, and checks" — **both verified accurate** against Brex's own docs on 2026-09-11. Rho's competitor research here is, on these points, honest.

**Brex Embedded (Layer D).** Announced **2024-09-18** (https://www.brex.com/journal/press/brex-announces-brex-embedded).

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | "Embed Brex virtual cards in your B2B software to unlock global payments with automated reconciliation" | https://www.brex.com/product/embedded-finance (2026-09-11) |
| Customer | B2B software vendors in ERP, travel, procurement, procure-to-pay | brex.com/product/embedded-finance |
| Capabilities | Virtual card issuance via API; "local-currency payments in 60+ countries with no FX markups"; L2/L3 data synced to customer ERPs; no-code embedding via Conferma and Mastercard ICCP; real-time spend controls. Launch material cited "up to 40x higher limits" and "50+ countries" in 2024 | brex.com (2026-09-11); brex.com/journal/press (2024-09-18) |
| Named partners | Coupa, Zip, Navan, Tekion. Anthropic cited as a Brex-for-Zip customer | brex.com/product/embedded-finance (2026-09-11) |
| Pricing | **Not disclosed.** Revenue is interchange, not a published fee | brex.com (2026-09-11) |

Note the country count moved **50+ (2024) → 60+ (2026)**.

### 3.9 Mercury — Layer F, write-capable, the single closest comparable to Rho

Mercury's API is the exact thing Rho's API is not, from the exact same starting position (a US business banking fintech on sponsor banks, serving startups).

Endpoint inventory from https://docs.mercury.com/llms.txt (2026-09-11):

| Area | Write operations present |
| --- | --- |
| Transactions | `POST createtransaction` — **send money to a recipient** (immediate or approval-required); `PUT updatetransaction`; `POST uploadtransactionattachment` |
| Recipients | `POST createrecipient`, `PUT updaterecipient`, `DELETE deleterecipient`, `POST createrecipientinvite`, `DELETE deleterecipientinvite`, `POST uploadrecipientattachment` |
| Payment approvals | `POST requestsendmoney`, `POST requesttransfermoney` |
| Internal transfers | `POST createinternaltransfer` |
| Cards | `POST createcard` (issue virtual card), `PUT updatecard` (nickname/limits), `PUT freezecard`, `PUT unfreezecard`, `DELETE cancelcard` |
| Vault | `POST revealcardpan` — full PAN/exp/CVC, **agentic cards only** |
| Invoicing | `POST createinvoice`, `PUT updateinvoice`, `DELETE cancelinvoice` |
| Customers | `POST createcustomer`, `PUT updatecustomer`, `DELETE deletecustomer` |
| Categories | `POST createcategory`, `PUT editcategory`, `DELETE deletecategory` |
| Webhooks | `POST createwebhook`, `PUT updatewebhook`, `POST verifywebhook`, `DELETE deletewebhook` |
| Read-only areas | Accounts, statements, organization, treasury, credit, merchants, events, users, SAFEs |
| OAuth2 | `POST startoauth2flow`, `POST obtainaccesstoken` |

Token model (https://docs.mercury.com/docs/getting-started, 2026-09-11), three tiers:

| Tier | Capability | IP allowlist |
| --- | --- | --- |
| Read Only | "Can fetch all available data on your Mercury account" | not required |
| Read and Write | "Can initiate transactions without admin approval, and manage recipients" | **required** |
| Custom | "Can only perform requests on the specific scopes granted" — e.g. `RequestSendMoney` routes through admin approval | per scope |

Base URL `https://api.mercury.com/api/v1/`. Basic auth (token as username) or bearer. Sandbox documented. Mercury's MCP server is **hosted, OAuth, and deliberately read-only**, working with Claude, ChatGPT, Claude Code, Codex CLI. Webhooks: transaction and balance events, **HMAC-SHA256** signatures, filters, retries, at-least-once delivery. Payment creation supports idempotency keys. [The MCP/webhook details are Rho's characterisation of Mercury, https://www.rho.co/blog/best-banking-apis-for-business, 2026-08-25; the endpoint list and token tiers are verified against Mercury's own docs.]

**This is the reference architecture Rho will end up building.** Mercury has solved exactly the problem Rho says it is worried about — agentic payment risk — by splitting the surfaces: write-capable REST API with IP-allowlisted tokens and an approval-scoped middle tier, plus a *separate* read-only MCP server for AI. Rho's "read-only by design" is not a different safety philosophy from Mercury's; it is Mercury's philosophy with the write half not yet shipped.

### 3.10 Ramp — Layer F, write-capable

From https://docs.ramp.com/llms-api.txt (2026-09-11):

- Bearer-token auth.
- **Bills and payments**: create bills with line items and accounting fields; payment methods include **ACH, card, check, wire, crypto**.
- **Cards and funds**: issue virtual and physical cards, manage spend limits and fund allocations, reissue, terminate.
- **Transactions**: create reimbursements and expense submissions; mark transactions ready-to-sync.
- **Vendors**: batch upload/manage up to **500** records; vendor credits; vendor network.
- **Accounting**: upload GL accounts, entities, custom fields (**500 items per batch**), tax codes; sync status to NetSuite, QuickBooks, Xero, Sage Intacct.
- **Treasury and banking**: manage bank and investment accounts, **create transfers**, wallet operations, balance history.
- Batch ops are all-or-nothing; **idempotency keys required** for sync reporting.
- MCP: not found in the API doc index on 2026-09-11. [Rho claims "Three documented MCP servers" for Ramp — https://www.rho.co/product/api, competitive data collected **2026-08-20**. **Unverified** in this research.]

### 3.11 Slash — Layer F, broadest read/write MCP, unsettled status

- API is **explicitly labeled Beta**: "Our API is currently in Beta and is not yet available to the wider public" (https://docs.slash.com/, 2026-09-11).
- Read/write. Endpoints seen: `GET /legal-entity`, `POST /transfers/book-transfer`, `POST /transfer/virtual-account`; cards and transactions referenced. Idempotency keys required on financial transactions.
- Rho's review describes the Slash MCP as three meta-tools — `list_endpoints`, `get_endpoint_schema`, `call_api_endpoint` — giving an agent discoverable passthrough to the whole API, with optional RSA encryption of PAN/CVV, and warns "plaintext may otherwise be returned." [Rho claim, 2026-08-25.] The MCP tools were **not visible** in the docs index fetched 2026-09-11.
- Rho itself flags the contradiction: "Slash's developer documentation still labels the API 'Beta' as of this review, though a company blog post describes it as generally available; treat the current access status as unsettled until Slash's own sources agree." [Rho, 2026-08-25.] This is unusually fair competitor treatment.

### 3.12 Plaid — Layer E, plus a real payments business now

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | Customer-permissioned connectivity to institutions it does not hold: Auth, Balance, Identity, Transactions, Investments, Liabilities, Income, Transfer, Signal, Identity Verification, Monitor, Beacon, Layer | https://plaid.com/docs/account/billing/ (2026-09-11) |
| Customer | Any app that needs *another* institution's data or an ACH pull |  |
| Can it move money | **Yes, selectively.** Plaid Transfer originates ACH; `/transfer/authorization/create` bundles Signal and Balance per-request fees | https://plaid.com/docs/account/billing/ |
| Billing models | **One-time fee per Item**: Auth, Identity, Income (most), Layer. **Monthly subscription per Item**: Transactions, Investments, Liabilities ("an Item will incur a monthly subscription fee as long as a valid `access_token` exists"). **Per-request flat fee**: Balance (`/accounts/balance/get`), Signal (`/signal/evaluate`). **Per-request flexible**: Document Income. Identity Verification charges per anti-fraud engine / data source / document check / selfie check. Monitor = base fee + rescanning | https://plaid.com/docs/account/billing/ (2026-09-11) |
| Plans | Pay-as-you-go (month-to-month, no commitment), Growth (12-month commitment, discounted rates), Custom (volume-based). Free Limited Production: **up to 200 API calls per product** with live data | https://plaid.com/pricing/ (2026-09-11) |
| Published unit prices | **None on plaid.com.** Third-party estimates: Auth **$0.30–$1.00** per successful connection; most products **$0.10–$0.60** per call by tier. Treat as unverified | https://www.getmonetizely.com/articles/plaid-vs-yodlee-how-much-will-financial-data-apis-cost-your-fintech ; https://www.fintegrationfs.com/post/how-much-does-plaid-integration-cost-in-the-us |
| Financials | ARR ~**$575M in 2025**, up from ~**$400M in 2024** (~40% YoY). Series E **$575M on 2025-04-03**, led by Franklin Templeton at a reset **$6.1B**. **$8B** valuation in a **February 2026** employee tender. Peak was $13.4B in 2021 | https://sacra.com/c/plaid/valuation/ ; https://www.connectingthedotsinfin.tech/plaids-valuation-soars-to-8b-as-momentum-returns/ |
| Payments growth | Payments grew **250%** in 2025; new products >20% of ARR at 93% growth as of April 2025 | Sacra (2026) |
| MCP | Rho's assessment: Plaid's MCP products cover "production diagnostics, documentation, mock data, sandbox-token creation, and webhook simulation. They do not provide general AI-agent access to linked users' balances and transactions" [Rho claim, 2026-08-25] |

**The JPMorgan fee fight is the structural story here.** In mid-2025 JPMorgan Chase said it would charge data aggregators for access to customer data; by **September 2025** Plaid had agreed to pay, terms undisclosed, and said it would not pass the fees to clients (https://www.openbankingtracker.com/guides/open-banking-data-access-fees). The CFPB's Section 1033 rule (finalized October 2024) had banned charging for access; **in May 2025 the CFPB announced plans to repeal the no-fee provision**, a federal court has enjoined enforcement, the **2026-04-01 first compliance deadline passed without becoming a binding trigger**, and the rule is being rewritten (https://openbankingtracker.com/guides/section-1033-status, 2026; https://www.congress.gov/crs-product/IF13117).

**Why that matters to Rho:** if data providers can charge aggregators, a first-party API becomes a *revenue* surface, not just a customer-service surface. Rho is currently giving away, free, the exact asset JPMorgan is monetizing. That is a defensible strategic choice for an $X-hundred-million-deposit fintech competing on developer goodwill — but it should be a choice, and Rho's pages never acknowledge the trade.

### 3.13 Teller — Layer E, the technically opinionated aggregator

| Dimension | Fact | Source / date |
| --- | --- | --- |
| What it sells | "The easiest way users connect their bank accounts to your app." Accounts, Balances ("guaranteed live"), Transactions, Identity, **Payments** | https://teller.io/ (2026-09-11) |
| Technical model | **Reverse-engineers each bank's mobile app to find its private API and calls that directly.** Not screen scraping in the classic sense, and not a partner-API aggregator | https://blog.teller.io/ ; https://www.fintegrationfs.com/fintechapisusa/teller-api |
| Security | **Mutual TLS (mTLS) required for all API requests involving end-user data**, in development and production; per-account access tokens from Teller Connect; app never sees raw credentials | https://teller.io/docs/api/authentication (2026) |
| Money movement | **Yes, narrowly: instant transfers via Zelle** | https://teller.io/ (2026-09-11) |
| Coverage | "more than 7,000 financial institutions", ACH micro-deposit fallback for unsupported banks | https://teller.io/ (2026-09-11) |
| Pricing — actually published | Developer tier **free, up to 100 live connections**. Production: account verification **$1.50** per account; balance **$0.10** per call; transactions **$0.30** per enrollment per month; identity **$1.75** per call. Enterprise custom | https://teller.io/ (2026-09-11) |

Teller's transactions price, **$0.30 per enrollment per month**, is identical to Stripe Financial Connections' **$0.30 per institution per account holder per month**. Two independent vendors converging on the same number is a strong signal that this is the market-clearing price of a bank transaction feed.

---

## 4. Consolidated comparison

### 4.1 What each one actually sells

| Vendor | Layer | Core product | Customer | Moves money programmatically | Owns a charter |
| --- | --- | --- | --- | --- | --- |
| **Rho API** | F | Read-only access to the customer's own Rho accounts + MCP | Rho's own existing customers (finance/FP&A/data teams) | **No** | No (Webster Bank, a division of Santander Bank, N.A.) |
| Increase | A | Bank infrastructure by API | Tech companies building financial products | Yes: ACH, wire, RTP, FedNow, checks, cards, push-to-card | **Yes** (Increase Bank, ex-Twin City, since 2025/2026) + 3 partner banks |
| Column | A | Chartered developer bank by API | Fintechs and FIs | Yes: ACH, wires, intl wires, RTP, book, checks, loans | **Yes** (Column N.A., national charter) |
| Unit | B | BaaS middleware, multi-bank | Vertical SaaS and platforms | Yes, via partner banks | No |
| Treasury Prime | B→ bank-direct | Bank OS embedded banking platform | Banks first, fintechs second (post-2024 pivot) | Yes, via partner banks | No |
| Synctera | B | End-to-end BaaS + sponsor-bank tooling | Fintechs, embedded providers, banks; US + Canada | Yes, via partner banks | No |
| Stripe Treasury | D→F hybrid | Stored-value accounts + payouts + cards; also for platforms | Businesses directly, and platforms embedding | Yes: payouts to 160 countries, wires, FX, stablecoins | No (Fifth Third / Newline, Goldman Sachs Bank USA) |
| Stripe Issuing | D | Card issuing API | Platforms and businesses | Card authorization and spend | No |
| Stripe Financial Connections | E | Permissioned external account data | Any app | No (data only) | No |
| Modern Treasury | C | Payment ops + ledger software across your banks | Fintechs, marketplaces, lenders, payroll | Yes, instructs at your banks/PSP | No |
| Brex Embedded | D | Your software issues Brex virtual cards | B2B software vendors (ERP, travel, procurement) | Yes, card rails, 60+ countries | No |
| Brex API (first-party) | F | Full spend + payments API over Brex accounts | Brex's own customers | **Yes**: ACH, domestic wires, checks | No |
| Mercury API | F | Full banking API over Mercury accounts | Mercury's own customers | **Yes**: ACH, recipients, transfers, card issuing | No |
| Ramp API | F | Spend + bill pay + treasury API over Ramp | Ramp's own customers | **Yes**: bills, ACH/card/check/wire/crypto payments, card issuing, transfers | No |
| Slash API | F | Programmable banking + cards, Beta | Slash's own customers | Yes (beta) | No |
| Plaid | E | Aggregation + selected payments | Any app | Yes, narrowly (Transfer = ACH) | No |
| Teller | E | Aggregation via bank mobile APIs | Any app | Yes, narrowly (Zelle) | No |

### 4.2 Pricing transparency, scored

| Vendor | Public rate card | What is actually published |
| --- | --- | --- |
| **Increase** | **Yes, full** | Every rail priced: ACH $0.50–$2.00, wire $15.00, RTP/FedNow $2.50, check $3.00, virtual card $0.25, dispute $15.00 |
| **Stripe** | **Yes, full** | Issuing $0.10 virtual / $3.50 physical / $15 dispute / 1%+30¢ cross-border; Treasury $2.00 wire, 0.5% FX; Financial Connections $1.50 / $0.10 / $1.50 / $0.30 |
| **Teller** | **Yes, full** | 100 free connections; $1.50 verify, $0.10 balance, $0.30/enrollment/mo, $1.75 identity |
| **Rho** | **Yes, trivially** | **$0.** "Available to every Rho customer", no waitlist, no approval, no separate API fee |
| Unit | Partial, model only | Fee framework in docs, "all fees default to $0", configured per contract |
| Plaid | Model only | Plan names + billing model per product; no unit prices; 200 free calls per product |
| Modern Treasury | Model only | Three fee components + "a single minimum commitment", annual terms, no figures |
| Column | No | Nothing retrievable |
| Synctera | No | Sales-led contact form as of 2026-05-06 |
| Treasury Prime | No | Revenue share with partner banks |
| Brex Embedded | No | Interchange-based, undisclosed |

Note the **contradiction**: a third-party audit dated **2026-08-02** claims "no banking-as-a-service provider publishes a public rate card" and that "seven of seven give you nothing to put in a spreadsheet" (https://boldrails.com/resources/baas-pricing-transparency). That audit sampled only the 7 domains ranking for "banking as a service pricing" and **missed Increase entirely**, which publishes the most complete rate card in the category. Do not cite the audit as an absolute.

### 4.3 Money-movement capability, ranked by what an API credential can actually do

| Can an API credential… | Rho | Mercury | Brex | Ramp | Slash | Stripe Treasury | Modern Treasury | Column/Increase | Plaid | Teller |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Read balances | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Read transactions | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Read statements | Yes | Yes | Yes | Yes | ? | Yes | Yes | Yes | No | No |
| Create a recipient/counterparty | **No** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | n/a | n/a |
| Originate ACH | **No** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes (Transfer) | No |
| Originate a wire | **No** | Yes | Yes | Yes | ? | Yes | Yes | Yes | No | No |
| Send a check | **No** | Yes | Yes | Yes | ? | No | Yes | Yes | No | No |
| Instant P2P / RTP / Zelle | **No** | No | No | No | ? | Yes (instant Stripe-to-Stripe) | Yes (RTP/FedNow) | Yes | No | Yes (Zelle) |
| Issue a card | **No** | Yes | Yes | Yes | Yes | Yes | n/a | Yes | No | No |
| Freeze/cancel a card | **No** | Yes | Yes | Yes | Yes | Yes | n/a | Yes | No | No |
| Open an account | **No** | No | No | No | Yes (virtual acct) | Yes | Yes | Yes | No | No |
| Create/cancel an invoice | **No** (read only) | Yes | n/a | n/a | ? | Yes | n/a | n/a | n/a | n/a |
| Receive webhooks | **No** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Publish SDKs | **No** | Yes | Yes | Yes | ? | Yes | Yes | Yes | Yes | Yes |

Rho is the only row in that table with a "No" in every action column.

---

## 5. So what category is Rho actually in?

**Name it precisely: a first-party, single-tenant, read-only account-data API with an MCP front end.**

Decomposed:

1. **First-party.** Rho serves data about accounts Rho itself holds (on Webster Bank). No aggregation layer, no OAuth into other banks. Rho's own framing is correct and is its best line: "Direct connection to the ledger. No aggregator in the chain, no refresh windows, no re-auth loops, no schema flattening your data into someone else's model" (blog, 2026-07-29).
2. **Single-tenant.** A token is "scoped to a single business" (`docs/v1/auth`). There is no concept of an end user of the customer's own product. Nothing in the API lets a Rho customer create accounts or cards for *their* customers. This is what definitively excludes Rho from embedded finance.
3. **Read-only.** 14 GETs.
4. **MCP-front-ended.** This is the only genuinely differentiated part, and it is real: MCP shipped in production at launch, 1:1 with REST, with a frozen tool-name contract and an Anthropic directory listing.

The closest historical analogue is **a commercial bank's treasury reporting API** — Wells Fargo Gateway's cash-reporting endpoints, BAI2/prior-day-balance feeds — repackaged for a self-serve startup audience and given an agent interface. Rho's own review post lands in the same place: it puts Wells Fargo and Capital One in a separate "Traditional Banking APIs" bucket, but the capability Rho ships is reporting, not initiation, which is the Wells Fargo reporting half without the Wells Fargo payment half.

### 5.1 Who Rho competes with in that category

**Direct, same-shape competitors (Layer F, US business banking / spend, self-serve):**

| Competitor | What they have that Rho does not | What Rho has that they do not |
| --- | --- | --- |
| **Mercury** | Write API (payments, recipients, transfers, card issuing), webhooks with HMAC-SHA256, three token tiers incl. approval-scoped, idempotency keys, sandbox | Nothing structural. Mercury also ships a read-only MCP server. **Rho is strictly a subset of Mercury's API surface today.** |
| **Brex** | 10 APIs, Payments API (ACH/wire/check), webhooks, OpenAPI + Postman, partner OAuth, scoped tokens, first-party MCP (early access) | Rho's MCP is GA and in Anthropic's directory; Brex MCP "requires early-access enablement" [Rho claim, 2026-08-25] |
| **Ramp** | Bills, payments across 5 rails incl. crypto, card issuing, transfers, batch accounting sync, idempotency | Rho's MCP posture; Ramp's MCP situation is unverified |
| **Slash** | Read/write MCP passthrough with 3 meta-tools; virtual accounts | Rho is GA; Slash API is docs-labeled Beta |
| **Wells Fargo / Capital One** | Enterprise treasury depth, payment initiation, FX, ERP/TMS connectors | **Self-serve.** Rho: "no waitlist and no approval step." Incumbents require commercial approval, compliance review, signed contract |

**The competitor Rho does not name: Stripe Financial Connections and Plaid, reading Rho.**

This is the real category risk and it appears nowhere in Rho's positioning. A Rho customer who wants their Rho transactions in a third-party tool does not need the Rho API. They can authorize Plaid, Teller, or Stripe Financial Connections and get the same transaction feed for **$0.30 per account per month**, paid by the tool vendor, with zero cooperation from Rho. Rho's "no aggregator in the chain" pitch is a *quality* argument (full detail vs. flattened schema, no refresh windows, no re-auth loops) — and it is a good one — but it is an argument against a free substitute, not against an absent one.

The corollary is that Rho's read-only API mostly **defends** rather than **wins**: it keeps Rho data out of aggregator schemas and keeps the integration surface first-party. That is worth doing. It is not a moat.

### 5.2 Who Rho does not compete with, and should stop implying it does

Rho's product page frames the API against "Open banking APIs and aggregators (Plaid, for example)" and "Banking-as-a-service APIs," then correctly says "The Rho API is neither." That paragraph is the single most accurate thing on the page. The rest of the page then undercuts it with a nav label ("Rho API — **Banking and payments via API**") and an OpenAPI description ("accounts, cards, **payments**, and the transaction ledger") that both promise money movement the API does not have. See §11.

---

## 6. The MCP argument, examined

Rho's strongest genuine claim is architectural: **"Most financial APIs predate agents; MCP got bolted on. This one shipped with its MCP server in production. Not a roadmap item, the architecture"** (blog, 2026-07-29). The evidence supports it in a narrow, checkable way:

- REST and MCP share one contract, one auth model, one scope set, one error shape (`docs/v1/mcp`).
- Tool names are pinned to frozen v1 operationIds and are contractually immutable (`docs/v1/versioning`). Almost nobody else makes that promise.
- Rho supports MCP protocol `2026-07-28`, the newest listed, alongside `2025-11-25` and `2025-06-18`, and rejects anything older plus JSON-RPC batches.

But the *safety* argument that read-only is the right agent posture is weaker than Rho presents, because:

- **Mercury reached the same safety outcome without giving up writes**, by shipping a read/write REST API and a separately read-only MCP server. Rho's own review post says so explicitly (2026-08-25).
- **Modern Treasury and Brex** ship write-capable MCP servers that inherit the credential's scopes, with audit trails. Rho's own review concedes these are legitimate designs: "Write-capable agents may be justified for controlled card, invoice, payment, or spend workflows."
- Rho's own MCP safety checklist prescribes exactly the controls a write-capable Rho would need: least-privilege scopes, separate credentials for analytics vs. money, expiry + rotation, IP allowlisting, **human approval before money moves**, **idempotency keys on every financial write**, audit logs, webhook signatures, revocation testing. Rho has 6 of those 9 today and is missing the 3 that only matter once writes exist.

So: read-only is a defensible *launch* posture and an honest *current* state. It is not a durable differentiator, and Rho itself does not claim it is — the blog says the opposite.

---

## 7. Market context, 2026

| Fact | Value | Source / date |
| --- | --- | --- |
| Embedded finance market, 2026 | ~**$150B+**, projected toward **$450B** by early 2030s, low-to-mid 20% CAGR | https://sumsub.com/blog/banking-as-a-service/ (2026) |
| BaaS platform market | **$19.56B in 2024** → **$75B by 2032**, 18.6% CAGR | https://www.futuremarketinsights.com/reports/banking-as-a-service-baas-platform-market |
| Direction of travel | "In 2026, a handful of scaled fintechs will obtain bank charters and compete directly with sponsor banks and infrastructure-focused financial institutions, increasing competition and pricing pressure" | https://www.moderntreasury.com/journal/2026-fintech-predictions-key-trends-in-payments-banking-and-financial-infrastructure |
| Consolidation | "In 2026, enterprises will aggressively consolidate fintech vendors, prioritizing platforms that combine payments, ledgering, and compliance" | Modern Treasury 2026 predictions |
| Sponsor-bank economics | "In 2026, more banks will charge fintechs directly for data & compliance, passing costs to startups" | https://www.fintechtris.com/blog/the-embedded-finance-playbook |
| Synapse fallout | Chapter 11 April 2024; **~$300M** customer deposits inaccessible for months; **>$95M still unaccounted for** | https://www.yalejournal.org/publications/the-synapse-collapse ; https://natlawreview.com/article/who-owns-compliance-failure-bank-fintech-liability-allocation-banking-service-baas |
| FDIC "Synapse rule" | Proposed **October 2024**: banks holding custodial accounts with transactional features must keep standardized beneficial-owner records and **reconcile daily**; recordkeeping may be delegated but the bank remains accountable and must have continuous direct access. **Still proposed, not finalized, as of mid-2026** | https://www.bclplaw.com/en-US/events-insights-news/synapse-failure-spurs-fdic-to-specify-record-keeping-for-bank-sponsored-fintechs.html |
| Grasshopper (an Increase partner bank) | Enova agreed **2025-12-11** to acquire for ~**$369M**, closing H2 2026; Enova becomes a Fed-regulated BHC, Grasshopper keeps its national charter | https://ir.enova.com/2025-12-11-Enova-Announces-Definitive-Agreement-to-Acquire-Grasshopper-Bank |
| Section 1033 | Finalized Oct 2024; enforcement enjoined; **2026-04-01 first compliance deadline passed non-binding**; CFPB rewriting, including repeal of the no-fee provision announced May 2025 | https://openbankingtracker.com/guides/section-1033-status (2026) |

**The through-line:** the middle of the stack is being squeezed out. Chartered API banks (Column, Increase) are absorbing the middleware layer from below; sponsor banks and direct-bank software (Treasury Prime's pivot) are absorbing it from above. Meanwhile the read-data layer is being commoditized to $0.30/account/month and simultaneously re-priced upward by data providers charging aggregators. A first-party read API is on the *right* side of the second trend and irrelevant to the first.

---

## 8. What Rho would have to build to compete with write-capable platforms

Two very different ambitions. Be clear which one is being asked.

### 8.1 Ambition A: match Mercury / Brex / Ramp (write API over Rho's own customers)

This keeps Rho in Layer F. It is the stated roadmap ("write access, webhooks, more endpoints"). Nine workstreams:

| # | Workstream | What specifically | Hard part |
| --- | --- | --- | --- |
| 1 | **Write scopes** | `payments:write`, `cards:write`, `transfers:write`, `invoicing:write`, `users:write`. Today all 5 scopes end in `:read` | Scope design is the permission model for agents; getting it wrong is unrecoverable under an additive-only v1 contract (removing an enum value requires v2) |
| 2 | **Idempotency** | `Idempotency-Key` header, 24h+ replay window, stored request-hash comparison, conflict semantics. Mercury and Ramp both require it; Rho's own safety checklist says "use them on every financial write" | Must be designed before the first write endpoint ships, not after |
| 3 | **Counterparty / recipient model** | Create, update, delete recipients; bank-detail validation; ACH vs wire routing; international. Mercury has `createrecipient`, `createrecipientinvite`, tax-form attachments | This is where OFAC screening and fraud controls attach |
| 4 | **Approval semantics** | The transaction `status` enum **already has `awaiting_approval`**, so the ledger models it. Needs an API-side equivalent of Mercury's `RequestSendMoney` scope: a credential that can only *propose* a payment for human approval | Rho's checklist: "Require a person to approve before money moves." This is the single feature that makes agentic payments defensible |
| 5 | **Webhooks** | Event catalogue, HMAC signatures, retries with backoff, at-least-once delivery, delivery logs, replay, filters. Rho has **none**; every competitor has them | Without webhooks a write API is unusable: you cannot poll at 60 req/min for payment status |
| 6 | **Rate limits for writes** | 60 req/min/token is a read limit. Writes need separate, likely lower, per-rail limits and velocity caps | Also needs per-token dollar limits, not just request limits |
| 7 | **SDKs** | Rho publishes an OpenAPI spec and nothing else. Mercury, Brex, Ramp, Modern Treasury, Stripe all ship maintained SDKs | Generated SDKs are cheap; maintained ones are not |
| 8 | **Sponsor-bank authorization** | Webster Bank, a division of Santander Bank, N.A. must approve API-originated payment initiation: NACHA origination agreements, ODFI risk limits, Reg E / UCC 4A allocation, OFAC/sanctions screening on API-created counterparties, BSA/AML transaction monitoring on a new origination channel, exposure limits | **This is the real gate, and it is not an engineering problem.** Post-Synapse, post-consent-order, sponsor banks are far more conservative about a new programmatic origination channel than they were in 2021 |
| 9 | **Liability for agent-initiated payments** | Terms of service, who eats a mistaken agent payment, insurance, audit-log retention, forensic replay of an MCP tool call | Nobody in the market has solved this cleanly. It is also the biggest opportunity |

Items 1–7 are months of engineering. Item 8 is the schedule driver. Item 9 is the one that would actually differentiate Rho if solved first, because it is the natural extension of the "read-only by design" brand: not "agents can't touch money" but "**agents can propose, humans dispose, and every step is signed and replayable**."

**Note what this does NOT require:** a charter, a ledger rebuild, or a new bank partner. Rho already moves ACH, wires, checks and issues cards through its dashboard. The rails exist. The API is a second front door onto rails Rho already operates.

### 8.2 Ambition B: compete with Increase / Column / Unit / Stripe Treasury (embedded finance)

This is a different company. Requirements:

| Requirement | Rho's current position | Gap |
| --- | --- | --- |
| Multi-tenant end-user model (Rho's customer creates accounts for *their* customers) | Token is "scoped to a single business" | Total. No end-user, sub-account, FBO, or program concept exists anywhere in v1 |
| Programmatic account opening + KYC/KYB | None in the API | Total. Column and Unit both expose `entities` with KYC/KYB |
| FBO / sub-ledger accounts with daily beneficial-owner reconciliation | Not exposed | Total. And the FDIC's proposed Synapse rule would make this the regulatory centerpiece |
| Card program issuing for third parties | Read-only `GET /cards` over Rho's own cards | Total |
| A charter, or a sponsor bank willing to run a BaaS program | Webster Bank, a division of Santander Bank, N.A., for Rho's own product | Santander is a large regulated institution, not a BaaS sponsor. Running third-party fintech programs is a different regulatory undertaking |
| Program compliance, oversight, reconciliation tooling for the sponsor | None | Total. This is most of what Unit and Synctera actually sell |

**Verdict on Ambition B: Rho should not do this, and nothing on Rho's site suggests it intends to.** The market is consolidating toward chartered players (Column, Increase), the middleware layer is where the casualties are (Synapse, Treasury Prime's halving, Synctera's 2024 layoffs, Thread Bank's consent order), and Rho's asset is a direct SMB/startup customer relationship, which is the opposite of the BaaS business.

### 8.3 The asymmetry worth naming

Rho's current API is **defensive** (keeps Rho data first-party and out of aggregator schemas) and **top-of-funnel** (an MCP listing in Anthropic's directory is distribution to exactly Rho's target customer). Neither of those requires writes.

Writes change the business: a write API turns Rho from a bank account into a **programmable finance backend for a startup's own internal tooling**, which raises switching costs sharply. Every hour a customer spends wiring Rho's write endpoints into their reconciliation, AP, or agent workflow is an hour of lock-in that a read-only integration does not create — because a read integration can be replaced by Plaid in an afternoon, and a write integration cannot be replaced at all.

---

## 9. Contradictions inside Rho's own corpus

| # | Contradiction | Evidence |
| --- | --- | --- |
| 1 | **Scope list disagrees with itself.** Auth guide lists 3 scopes; OpenAPI lists 5 | `docs/v1/auth` ("The scopes available today are:" `accounts:read`, `transactions:read`, `statements:read`) vs `api/v1/openapi` (adds `cards:read`, `invoicing:read`) |
| 2 | **Coverage statement is stale.** Getting Started: "Current release is read-only and **covers accounts and transactions**" — but v1 also covers cards, statements, and invoicing | `docs/v1/getting-started` vs `api/v1/openapi` |
| 3 | **OpenAPI description promises payments that do not exist.** "Programmatic access to Rho's banking, spend, and treasury primitives — accounts, cards, **payments**, and the transaction ledger." There is no payments endpoint | `api/v1/openapi` |
| 4 | **Site nav promises payments.** Products menu: "Rho API — New. **Banking and payments via API**" | `rho.co/product/api` nav, captured 2026 |
| 5 | **Rho's two machine-readable files disagree.** `site-llms.txt`: "Read-only API for Rho account and transaction data… no aggregator (as of 08/01/2026)". `site-llms-full.txt`: "Programmatic access to accounts, **payments**, and card data for engineering and finance teams" | `rho/site-llms.txt` line 33 vs `rho/site-llms-full.txt` line 35 |
| 6 | **"Read-only by design" vs. "read ships first."** Product page: "Read-only by design: tokens cannot initiate payments or modify accounts", "Can API tokens move money? **No, by design.**" Launch blog: "Read access is live today. **Acting on Rho programmatically is where the platform is headed.**" | `rho.co/product/api` vs `rho.co/blog/introducing-rho-api` (2026-07-29, updated 2026-09-01) |
| 7 | **Token-creation location differs from OpenAPI security URL.** Product page and blog: "Settings, then Configurations, then Access Tokens." OpenAPI security block: token URL `https://app.rho.co/settings/access-tokens` | `rho.co/product/api` vs `api/v1/openapi` |
| 8 | **OAuth is declared as `oauth2` in the security scheme but the primary flow is a static bearer token** with a settings-page "token URL", which is not an OAuth token endpoint | `api/v1/openapi` Security → AccessToken → "Type: oauth2, Token URL: https://app.rho.co/settings/access-tokens" |

Independent contradiction worth flagging: **the boldrails BaaS pricing audit (2026-08-02) asserts no provider publishes a rate card; Increase does**, comprehensively. The audit's sample was 7 domains ranking for one query string.

---

## 10. What is conspicuously NOT stated

| Silence | Why it matters |
| --- | --- |
| **No webhooks anywhere.** Not in 13 doc pages, not in the OpenAPI, not in the help center. Rho's own comparison table for its own product says "Webhooks: Not yet" | Every single competitor in Layer F has them. A read API without webhooks forces polling against a 60 req/min ceiling |
| **No SDKs.** OpenAPI spec only | Competitors ship maintained clients in 4–6 languages |
| **No API uptime/SLA figure.** Unit claims 99.999%, Modern Treasury 99.99%. Rho claims nothing | Read-only removes most of the risk, but a data pipeline still needs an availability commitment |
| **No API customer count, call volume, or adoption number.** Three named builders in the launch post (Wayve Payments, Joinergo, Arbor Management), no aggregate | Launched 2026-07-29; six weeks old at time of research. Silence is expected but should not be read as traction |
| **No stated position on aggregators reading Rho.** Rho markets "no aggregator in the chain" as a benefit of *its* API but never says whether Plaid/Teller/Stripe FC can connect to a Rho account, or whether Rho intends to charge them | This is the most important omission. It determines whether the API is a moat or a courtesy |
| **No pricing surface at all.** "$0, available to every Rho customer" | Fine as a launch decision. But JPMorgan is now charging for exactly this data (Plaid agreed to pay, Sept 2025) and the CFPB is rewriting the no-fee rule. Rho has an unpriced asset |
| **No mention of ChatGPT / other MCP clients being supported.** "Claude is the natively supported client today"; "Other MCP clients can connect using the MCP guide" | Mercury's hosted MCP explicitly supports Claude, ChatGPT, Claude Code, and Codex CLI [Rho claim about Mercury, 2026-08-25]. Rho is narrower than the competitor it ranks second |
| **No dispute indicator in v1.** Docs state plainly: "A refund or credit is not by itself a dispute — v1 exposes no dispute indicator" | Honest, and a real gap for reconciliation use cases |
| **No MT103 reference numbers** on international wires | Stated explicitly in `docs/v1/transactions`. Limits international reconciliation |
| **`id` is not unique per row.** "the entries of one money movement can share an `id`" | An unusual and hazardous contract choice that Rho documents carefully but that will break naive warehouse ingestion. Group on `money_movement_id` |

---

## 11. Source index

| Source | URL | Date accessed / dated |
| --- | --- | --- |
| Rho product page, API | https://www.rho.co/product/api | corpus; "current as of August 2026"; competitor data "collected 2026-08-20" |
| Rho API launch blog | https://www.rho.co/blog/introducing-rho-api | published 2026-07-29, last updated 2026-09-01 |
| Rho banking-API ranking | https://www.rho.co/blog/best-banking-apis-for-business | published + last updated 2026-08-25 |
| Rho docs: getting started, auth, rate limits, versioning, MCP, partner auth, pagination, transactions, accounts, cards, statements, invoicing | https://docs.rho.co/docs/v1/* | corpus, fetched 2026-09-11 |
| Rho OpenAPI overview + 14 operation pages | https://docs.rho.co/api/v1/openapi | corpus, fetched 2026-09-11 |
| Rho sandbox live capture | https://rhoapi-sandbox.rho.co/api/v1/* | HTTP 200, 2026-09-11 |
| Rho help center, AI tool access | https://www.rho.co/help-center/the-rho-api/what-connected-ai-tools-have-access-to-in-your-rho-account | corpus |
| Rho machine-readable summaries | site-llms.txt (API entry "as of 08/01/2026"), site-llms-full.txt | corpus |
| Increase pricing | https://increase.com/pricing | 2026-09-11 |
| Increase home / bank | https://increase.com/ , https://increase.com/bank | 2026-09-11 |
| Increase bank acquisition | https://www.bankingdive.com/news/fintech-increase-buys-washington-bank-stripe/826586/ | 2026-07-30 |
| Increase company facts | https://en.wikipedia.org/wiki/Increase_(company) | 2026-09-11 |
| Column home + docs | https://column.com/ , https://docs.column.com/ | 2026-09-11 |
| Column launch coverage | https://www.fintechfutures.com/core-banking-technology/developer-infrastructure-bank-column-launches-to-cut-middleware-bloat | n.d. |
| Unit home | https://www.unit.co/ | 2026-09-11 |
| Unit fee framework | https://www.unit.co/docs/api/fees/overview/ | 2026-09-11 |
| Thread Bank consent order | https://www.bankingdive.com/news/fdic-thread-bank-baas-oversight-fintech-partner-aml/720313/ | order dated 2024-05-21, public 2024-06-28 |
| Treasury Prime home | https://www.treasuryprime.com/ | 2026-09-11 |
| Treasury Prime pivot + layoffs | https://www.bankingdive.com/news/treasury-prime-lay-off-40-50-employees-marketing-liaison-direct-fintech-partner-chris-dean/708770/ ; https://www.fintechfutures.com/partnerships/treasury-prime-trims-workforce-amid-strategic-pivot-to-focus-on-direct-to-bank-partnerships | Feb 2024 |
| Synctera home | https://synctera.com/ | 2026-09-11 |
| Synctera $15M + Bolt | https://techcrunch.com/2025/03/11/baas-startup-synctera-raises-15m-signs-bolt-as-a-customer | 2025-03-11 |
| Synctera 2024 layoffs | https://techcrunch.com/2024/03/26/baas-startup-synctera-layoffs-fintech/ | 2024-03-26 |
| Synctera pricing model | https://www.xpay.sh/saas-pricing/synctera/ | as of 2026-05-06 |
| Stripe Treasury | https://stripe.com/treasury ; https://stripe.com/treasury/platforms | 2026-09-11 |
| Stripe pricing (Issuing, Treasury, Financial Connections) | https://stripe.com/pricing | 2026-09-11 |
| Stripe + Fifth Third Newline | https://www.fintechfutures.com/baas/stripe-selects-newline-by-fifth-third-bank-to-expand-its-embedded-financial-services-offering | n.d. |
| Stripe Sessions 2026 analysis (15 currencies by end-2026) | https://neobanque.ch/blog/stripe-sessions-2026-treasury-stablecoins-ai/ | 2026 |
| Modern Treasury home + pricing | https://www.moderntreasury.com/ , https://www.moderntreasury.com/pricing | 2026-09-11 |
| Modern Treasury Payments launch | https://www.moderntreasury.com/newsroom/press-releases/modern-treasury-launches-payments | Feb 2026 |
| Modern Treasury 2026 predictions | https://www.moderntreasury.com/journal/2026-fintech-predictions-key-trends-in-payments-banking-and-financial-infrastructure | 2026 |
| Brex developer docs | https://developer.brex.com/ | 2026-09-11 |
| Brex Embedded | https://www.brex.com/product/embedded-finance ; https://www.brex.com/journal/press/brex-announces-brex-embedded | 2026-09-11 ; announced 2024-09-18 |
| Mercury docs index | https://docs.mercury.com/llms.txt | 2026-09-11 |
| Mercury getting started / tokens | https://docs.mercury.com/docs/getting-started | 2026-09-11 |
| Ramp API docs | https://docs.ramp.com/llms-api.txt | 2026-09-11 |
| Slash docs | https://docs.slash.com/ | 2026-09-11 |
| Plaid billing models | https://plaid.com/docs/account/billing/ | 2026-09-11 |
| Plaid pricing plans | https://plaid.com/pricing/ | 2026-09-11 |
| Plaid valuation / ARR | https://sacra.com/c/plaid/valuation/ ; https://www.connectingthedotsinfin.tech/plaids-valuation-soars-to-8b-as-momentum-returns/ | Feb 2026 tender at $8B |
| Teller home | https://teller.io/ | 2026-09-11 |
| Teller mTLS / bank-app model | https://teller.io/docs/api/authentication ; https://blog.teller.io/ ; https://www.fintegrationfs.com/fintechapisusa/teller-api | 2026 |
| JPMorgan aggregator fees / 1033 | https://www.openbankingtracker.com/guides/open-banking-data-access-fees ; https://openbankingtracker.com/guides/section-1033-status ; https://www.congress.gov/crs-product/IF13117 | mid-2025 through 2026 |
| Synapse fallout + FDIC rule | https://www.yalejournal.org/publications/the-synapse-collapse ; https://www.bclplaw.com/en-US/events-insights-news/synapse-failure-spurs-fdic-to-specify-record-keeping-for-bank-sponsored-fintechs.html | rule proposed Oct 2024, still proposed mid-2026 |
| BaaS pricing disclosure audit | https://boldrails.com/resources/baas-pricing-transparency | audit dated 2026-08-02 |
| Embedded finance / BaaS market size | https://sumsub.com/blog/banking-as-a-service/ ; https://www.futuremarketinsights.com/reports/banking-as-a-service-baas-platform-market | 2026 |
| Enova / Grasshopper | https://ir.enova.com/2025-12-11-Enova-Announces-Definitive-Agreement-to-Acquire-Grasshopper-Bank | 2025-12-11 |

---

## 12. Four lines to carry into the dossier

1. **Category:** Rho v1 is a first-party, single-tenant, read-only account-data API with an MCP front end. It is the Wells Fargo reporting API for startups, not a banking API in the Increase/Column sense, and not embedded finance in any sense.
2. **Competitive set:** Mercury, Brex, Ramp, Slash on capability (where Rho is strictly a subset of all four), and Plaid / Teller / Stripe Financial Connections on substitution (where they sell the same read for ~$0.30/account/month with no Rho cooperation required). Rho's only real edge is that its MCP server is GA, 1:1 with REST, tool-name-frozen, and in Anthropic's directory.
3. **The read-only story is a launch posture, not a philosophy.** Rho says so itself on 2026-07-29 and again on 2026-08-25. The product page's "No, by design" and the blog's "acting on Rho is where the platform is headed" cannot both be the positioning.
4. **The gating factor for writes is Webster Bank, not Rho's engineers.** Scopes, idempotency, recipients, approvals, webhooks, rate limits, SDKs are months of work. Sponsor-bank authorization for a new programmatic origination channel, in a post-Synapse, post-consent-order supervisory climate, is the schedule. The differentiating feature nobody has shipped is agent-proposes / human-disposes with signed, replayable audit, and it is the natural extension of the brand Rho has already built.
