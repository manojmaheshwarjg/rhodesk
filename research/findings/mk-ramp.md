# Ramp: independent 2026 research dossier

Research date: 2026-09-11. All web sources fetched 2026-09-11 unless noted.
Rho corpus references are to the local crawl at `/private/tmp/.../scratchpad/rho/`.

Labeling convention used throughout:
- **[Ramp claim]** = asserted only by ramp.com, support.ramp.com, docs.ramp.com, or a Ramp press release.
- **[Rho claim]** = asserted only by rho.co (marketing; treat competitor statements as adversarial).
- **[3P]** = third party (NerdWallet, TechCrunch, Bloomberg, PYMNTS, CNBC, Accounting Today, etc.).
- Unlabeled = primary-document fact (OpenAPI export, fee schedule, disclosure footnote).

---

## 0. Executive summary of what changed in 2025-2026

1. Ramp's valuation went **$13B (Mar 2025) → $16B (Jun 2025) → $22.5B (Jul 2025) → $32B (Nov 2025) → $44B (Jun 2026)**, and as of **2026-09-08** was reported in early talks at **~$1B primary at $60B**. [3P]
2. Ramp's **flat 1.5% cashback ended in May 2024**. The current rate is **variable 0%-1.5%, set per customer by Ramp, not published**, with a stated floor of 1% [3P: NerdWallet, updated 2026-06-15]. This is the single largest transparency gap in Ramp's consumer-facing offer.
3. Ramp became a **bank-adjacent platform**: Ramp Checking at **2% APY (as of 09/11/2026)** through First Internet Bank of Indiana with IntraFi sweep, and a separate **Ramp Investment Account at up to 4.44% YTM (as of 09/03/2026)**, **$5,000 minimum**, **up to 0.15% advisory fee**, **not FDIC insured**.
4. Ramp shipped an unusually aggressive AI/agent roadmap: **Agents for Controllers (Jul 2025) → Agents for AP (Oct 2025) → Accounting Agents + Ramp Budgets (Q1 2026) → Agent Cards / Visa Intelligent Commerce (Mar 2026) → Procurement agent fleet (Apr 29, 2026) → Ramp Stack for accounting firms (Jun 3, 2026) → Applied AI Solutions (Jun 10, 2026) → Router.com LLM gateway (Aug 19, 2026)**.
5. Ramp now runs **three separate MCP servers** (account, developer-docs, public-data) plus an **open-source CLI with an `agentic-purchase` skill**. The old self-hosted `ramp_mcp` GitHub repo was **archived 2026-07-17** and superseded by the hosted server.
6. Ramp's Developer API exposes **252 documented operations across 39 resource groups**, OAuth 2.0 with ~50 named scopes, 45+ webhook event types, a sandbox at `demo.ramp.com`, and a published OpenAPI spec. This is an order of magnitude beyond Rho's read-only API.
7. Ramp went international by acquisition: **Billhop (announced 2026-03-13)** for UK/Sweden licenses and EU/UK onboarding "beginning this summer", and **Juno (announced 2026-03-16)** for guest/non-employee travel.

---

## 1. Corporate scale, funding, and milestones

### 1.1 Funding and valuation history

| Date | Event | Amount | Valuation | Lead / notable investors | Source |
|---|---|---|---|---|---|
| Mar 2025 | Secondary/round | n/d | $13B | Founders Fund | [3P] Wikipedia, TechCrunch |
| Jun 2025 | Series E | n/d | $16B | Founders Fund, ICONIQ Growth | [3P] TechCrunch 2025-07-30 |
| Jul 30, 2025 | Round | n/d | $22.5B | "45 days after reaching $16B" | [3P] TechCrunch 2025-07-30 |
| Nov 17, 2025 | Primary + employee tender | **$300M** | **$32B** | Lightspeed Venture Partners (lead); new: Alpha Wave Global, Bessemer, Robinhood Ventures, Epicenter Capital | PR Newswire 2025-11-17 |
| Jun 4, 2026 | **Series F** | **$750M** | **$44B** | Co-led ICONIQ, GIC, Ontario Teachers' Pension Plan; also Goldman Sachs Alternatives, D.E. Shaw, Morgan Stanley IM, Generation IM, Insight Partners, BroadLight Capital, Founders Fund | PR Newswire 2026-06-04; Bloomberg; TechCrunch; CNBC |
| Sep 8, 2026 | **In talks** (not closed) | ~$1B primary | **$60B** | undisclosed | [3P] PYMNTS 2026-09-08 |

Total equity raised: **"over $3 billion"** as of Jun 2026 (up from "$2.3 billion" stated Nov 2025). [Ramp claim, PR]

### 1.2 Scale metrics (carry the as-of dates; they move fast)

| Metric | Nov 1, 2025 | Apr 29, 2026 | Jun 1, 2026 | Source |
|---|---|---|---|---|
| Customers | 50,000+ | 50,000+ | **70,000+** | Ramp PRs |
| Customers at $100K+ annualized revenue | 2,200+ | n/d | **3,200+** | Ramp PRs |
| Annualized purchase volume | $100B+ | $100B | **$200B** | Ramp PRs |
| Annualized revenue | $1B+ | n/d | **"Over $1 billion" + positive FCF** | Ramp PRs |
| Enterprise YoY growth | 133% | n/d | 100%+ | Ramp PRs |
| Cumulative customer savings | $10B | $10B | **$12B** | Ramp PRs |
| Cumulative hours saved | 27.5M | 27.5M | 27.5M | Ramp PRs |

- TPV grew **"~170% year-over-year in March 2026"**. [Ramp claim, Series F PR]
- Median customer: **"5% savings and 16% revenue growth in their first year"**; in May 2026 the median customer **"saved 50% more dollars and 32% more hours per year than a year earlier"**. [Ramp claim]
- Ramp says it released **"70+ products and major features"** in the months before the Series F. [Ramp claim]
- **October 2025 AI operating stats** (Ramp's own instrumentation, quoted in the $32B PR): **26.1 million AI decisions across $10 billion in spend; 511,157 policy violations prevented saving $291 million; $5.5 million moved to investments; a $49,000 fake invoice blocked.**
- Headcount: third-party trackers disagree materially. Revelio Labs: **2,455 (2026)** vs 1,883 (2025). Other trackers: **2,718 as of 2026-07-26**, and **~3.2K in 2026**. Treat headcount as ±30%. [3P]
- Revenue: Sacra estimates **~$1.5B annualized by May 2026 (+89% YoY)**; Latka lists **$1.4B**. Ramp's own PR says only "over $1 billion in annualized revenue". [3P / Ramp claim disagreement]
- HQ: Ramp Business Corporation, 28 West 23rd Street, Floor 2, New York, NY 10010 (pricing page footer).
- Licensing entities: **Ramp Payments Corporation NMLS 2371465**, **Ramp Financing Corporation NMLS 2431387**.

### 1.3 Acquisitions

| Target | Announced | What it bought | Source |
|---|---|---|---|
| **Billhop** | 2026-03-13 | Stockholm- and London-based B2B payments platform, **licensed in the UK and Sweden**; regulatory licenses for EU/UK expansion. Ramp to open first international offices in **London and Stockholm**; onboard UK/EU-headquartered businesses "beginning this summer" | PR Newswire 2026-03-13; Bloomberg 2026-03-13; FinTech Futures |
| **Juno** | 2026-03-16 | Guest / non-employee travel coordination (candidates, traveling doctors, visiting researchers, event partners). Founded Dec 2024, Madrona-backed. Terms undisclosed | PR Newswire 2026-03-16; PhocusWire; GeekWire |
| Venue (2024) and one other | pre-2026 | Tracxn lists 4 total acquisitions as of Aug 2026 | [3P] Tracxn |

International footprint as stated in the Billhop PR: **local-currency cards and payments in Canada, Australia, Japan, Mexico, Singapore**; "nearly half of Ramp customers transact internationally across more than 180 countries every week". [Ramp claim]

---

## 2. Product lineup as of Sep 2026

Navigation taxonomy pulled from ramp.com's own footer (2026-09-11):

**Products:** Corporate cards · Expense management · Spend management · Budgets · Banking · Travel · Reimbursements · Procurement · Accounts payable · Vendor management · Approvals · Security · Trust · Mobile app · **Ramp Sheets**
**Platform:** Platform overview · Accounting automation · **Intelligence** · Reporting · Savings · Integrations · Multi-entity · Global · **AI Token Spend Management** · **Router**
**Other surfaces in footer:** Product releases · **Ramp for Agents** · **Ramp Labs** · API documentation · Versus

Note: `ramp.com/ramp-sheets`, `ramp.com/ramp-for-agents`, and `ramp.com/ramp-labs` all returned **404** to a direct curl on 2026-09-11 (they are linked from the footer but resolve via client-side routing or are gated). Conspicuously, Ramp advertises "Ramp for Agents" and "Ramp Labs" in navigation without a fetchable public page.

### 2.1 Cards

| Attribute | Value | Source |
|---|---|---|
| Product type | **Corporate liability charge card**, "30-day payback" | ramp.com/corporate-cards |
| Networks / issuers (US) | **Ramp Visa Corporate Card: Celtic Bank**; for US corporations operating globally: **Column N.A., Member FDIC**. **Ramp Visa Commercial Card: Sutton Bank**. **Ramp Visa Business Card: Lead Bank** | ramp.com/pricing footer |
| Canada | Peoples Trust Company under Visa license; balance **not** CDIC insured; Ramp registered as Payment Service Provider with Bank of Canada | ramp.com/pricing footer |
| UK | **Stripe Payments UK Limited**, EMI authorized by FCA, FRN 900461 | ramp.com/pricing footer |
| EEA | **Stripe Technology Europe Limited**, EMI authorized by Central Bank of Ireland, FRN C187865 | ramp.com/pricing footer |
| Annual fee | $0 | [3P] NerdWallet |
| **Foreign currency conversion fee** | **3%** | [3P] NerdWallet 2026-06 |
| Personal guarantee | Not required; **no personal credit check** | ramp.com + [3P] |
| Underwriting minimum | **$25,000 minimum balance in a US business bank account** | [3P] NerdWallet |
| Eligible entities | Corporations, LLCs, limited partnerships, nonprofits. **Excluded: sole proprietorships, individuals, unregistered businesses** | [3P] NerdWallet |
| Credit limit claim | "Up to 30x higher credit limits than traditional business credit cards" | [Ramp claim] |
| Card counts | Unlimited physical and virtual cards on **all three tiers** including Free | ramp.com/pricing |
| Local issuing | **Local currency card issuing in 30+ countries** = **Enterprise tier only** | ramp.com/pricing |
| Sign-up offer (Jun 2026) | $1,000 on approval, one per new customer, no minimum spend | [3P] NerdWallet. Note a separate affiliate page advertises "$500 + 1.5% cashback"; offers vary by channel |

**Reserve Account (the documented path to a higher limit):** a **locked Ramp Business Account**. Depositing funds raises the 30-day card limit **1:1 with no credit review**. Example from Ramp's own doc: base limit $50,000 + $100,000 deposit = $150,000 total limit. **Only customers on monthly card terms are eligible**; one Reserve Account per legal entity; funds are locked and cannot be spent; **Reserve balances currently earn 2%**. ACH deposits 0-4 business days; wires and RTP usually same day. (support.ramp.com/ramp-reserve-account-overview)

This confirms the Rho claim that Ramp's documented higher-limit path is collateralizing with your own cash. [Rho claim, verified]

### 2.2 Cashback

**This is Ramp's weakest disclosure surface.**

- Ramp's flat **1.5% ended May 2024**. [3P]
- **As of June 2026 Ramp told NerdWallet the rate ranges from 0% to 1.5%, "varies by customer and is determined by Ramp"**, with a stated floor that "at a minimum, every business earns 1% cash back". [3P NerdWallet, updated 2026-06-15; corroborated by CNBC Select, Forbes Advisor, Nav]
- **ramp.com/corporate-cards does not publish a cashback rate.** It publishes **"up to 5% savings"** with a footnote defining it as **"average savings as a percentage of an illustrative customer's total card spending when using Ramp features"** (i.e. a blended spend-reduction estimate, not a rewards rate).
- `support.ramp.com/cashback-overview`, `/how-does-ramp-cashback-work`, `/ramp-rewards` all return **404** (checked 2026-09-11). There is no public cashback terms page comparable to rho.co/policies/cashback-rewards.
- The Developer API does expose `GET /developer/v1/cashbacks` and `GET /developer/v1/cashbacks/{cashback_id}` with scope `cashbacks:read`, so a customer can read their own earned cashback programmatically. The **rate schedule** is still undisclosed.

**Internal contradiction inside the Rho corpus (flag this):**
- `pages/core/versus__ramp.txt` (verified 08/02/2026): "0%-1.5% variable, set per business, tiers undisclosed (NerdWallet, updated 06/15/2026)". Correct.
- `pages/core/product__corporate-cards.txt` (competitive data "collected... as of 2026-09-08"): "**1.5% cashback on card spend, flat, no higher tier**". **This is stale/wrong** and contradicts Rho's own versus page. Also on that page Rho attributes to Ramp "New or lower-balance customers start on daily repayment; accounts can switch to 30-day terms once balances reach $15,000" (Ramp's own Reserve doc references monthly-terms eligibility but does not publish a $15,000 threshold on any page I could fetch).

### 2.3 Bill Pay / AP

**Per-transaction fee schedule (support.ramp.com/bill-pay-fees, current 2026-09-11):**

| Rail | Fee | Notes |
|---|---|---|
| Standard ACH | **$0.59** | **Effective June 1, 2026**, with a 3-month grace period for active Bill Pay customers with ≥1 bill paid before 2026-05-01 |
| Same-day ACH | **$10** | |
| Domestic wire | **$15** | |
| International wire (SWIFT USD) | **$20** | |
| Standard check | **$1.99** | Same June 1, 2026 effective date and grace period as ACH |
| Overnight check delivery | **$20** | **Not waivable** |
| Check attachments | **$1 per page** | **Not waivable** |
| **Stablecoin payments** | **no fee** | |
| Ramp card / virtual card | available (fee not listed) | |

**Fee waiver:** "When paying out of Ramp Checking Account, transaction fees for standard ACH, standard check, same-day ACH, domestic wires, and SWIFT transfers are waived. Fees for overnight check delivery and check attachments still apply."

This is the exact mechanic behind Ramp's marketing line **"unlimited free same-day ACH and international wires for bill payments"** (ramp.com/business-banking). The qualifier is real: free **only when funded from a Ramp Checking Account**. Pay from an external bank and you are on the fee table above. [Rho claim about the qualifier: **verified correct**]

Billing mechanics: fees are **not** debited per bill. They accrue into a **monthly consolidated billing statement**, are not synced to the accounting provider with the bill, and are debited at end of statement period. Batched payments to the same vendor = **one fee for the batch**. A failed-and-resent ACH or check = **one fee total**. Splitting one invoice across two ACH payments = **two fees**. Plus customers get Bill Pay fees bundled onto their Plus subscription charge.

**AP feature set and tier gating (ramp.com/pricing, 2026-09-11):**

| Capability | Free | Plus | Enterprise |
|---|---|---|---|
| Invoice capture with AI OCR | ✓ | ✓ | ✓ |
| Pay bills by check, ACH, card, wire | ✓ | ✓ | ✓ |
| Configurable approval workflows | ✓ | ✓ | ✓ |
| Automated fraud checks from AP Agents | ✓ | ✓ | ✓ |
| 1099 filing (NEC and MISC) | **$.65 per IRS filing, free state filing** (all tiers) | same | same |
| Mobile bill approvals | ✓ | ✓ | ✓ |
| Create bills via CSV upload / import from ERP | ✓ | ✓ | ✓ |
| **Approval rules and routing** (by vendor, dept, accounting field, payment type) | no | ✓ | ✓ |
| **Line item auto-coding from AP agent** | no | ✓ | ✓ |
| **Approval recommendations from AP agent** | no | ✓ | ✓ |
| **Automated batch payments** | no | ✓ | ✓ |
| **Payment release approvals** | no | ✓ | ✓ |
| **Automated card payments** | no | ✓ | ✓ |
| **Line item splits** | no | ✓ | ✓ |
| **Three-way match with imported POs and item receipts** | no | ✓ | ✓ |
| Tax management / W8 uploads | no | ✓ | ✓ |
| Advanced exports | no | ✓ | ✓ |

Ramp's own AP performance claims: **"99% accurate" OCR**, **"2.4x faster" invoice processing vs legacy software**, **"7x fewer clicks" to process bills compared to Bill.com**, **"95% of customers reported improved visibility"**. [Ramp claim]

### 2.4 Expense management

Free tier includes: spend limits with preset accounting codes, automatic receipt collection and matching, employee repayments, reimbursements, transaction alerts and flags, complete expenses via **SMS or Slack**, auto-receipt collection and matching.

Plus adds: **AI-driven expense reviews and policy insights**, **auto-lock cards when compliance is unmet**, approval workflows routed by GL code/entity, limit reimbursement spending, bulk submit/review, weekly batched reimbursements, **approval recommendations for every transaction**, **proactive policy and compliance insights**, parallel approvers, missing receipt affidavits, Sunshine Act support.

Enterprise adds: locally funded reimbursements, pay card statements in local currency.

**International reimbursements:** Ramp support states reimbursements in **60+ countries in local currency**, elsewhere "more than 70 countries and 40 currencies, with payments made in two days or less". Country-specific statutory per diem rates cover a named list of ~20 European countries (Austria, Bulgaria, Croatia, Czechia, Denmark, Finland, Germany, Hungary, Iceland, Ireland, Latvia, Lithuania, Norway, Poland, Romania, Slovakia, Slovenia, Spain, Sweden, UK). The 60 vs 70 country discrepancy is between two Ramp support pages. [Ramp claim, internally inconsistent]

### 2.5 Travel

- Book flights, hotels, car rentals **in Ramp**, with policy enforced at booking so travelers see compliance status per option.
- **Hotel rate monitoring: Ramp rebooks automatically if the price drops by $50 or more.** [Ramp claim, appears on both ramp.com/travel and ramp.com/intelligence]
- Employees can check policy, view trip details, ask questions **via SMS, Slack, or the Ramp app**.
- **Tier gating:** company-wide travel policies on Free; **custom travel policies by role/department/location on Plus+**; **guest bookings (invite external guests to book in Ramp with set budgets and policy controls) on Plus+**; **24/7 phone support for travel bookings on Plus+**.
- Guest bookings is the productized **Juno** acquisition (announced 2026-03-16).
- No booking fee is stated anywhere on ramp.com/travel or ramp.com/pricing. **Conspicuously not stated:** whether Ramp charges a per-booking or per-trip fee, and who the inventory/GDS partner is.
- Developer API exposes `GET /developer/v1/trips` and `GET /developer/v1/trips/{trip_id}`; CLI exposes `ramp travel list|create|bookings|locations`.

### 2.6 Treasury / banking

Ramp runs **two distinct products** and the distinction matters:

**A. Ramp Checking Account (Ramp Business Account)**
| Attribute | Value | As of |
|---|---|---|
| APY | **2% APY** on eligible funds | **09/11/2026**, variable, no notice |
| Who pays interest | **First Internet Bank of Indiana, Member FDIC** | current |
| FDIC structure | **IntraFi Network LLC** sweep for pass-through insurance; marketed as **"FDIC insurance up to tens of millions of dollars per depositor"** | current |
| Minimum balance | **None** | current |
| Account opening / maintenance fee | **$0** | current |
| Transfer caps | **"No transfer caps or transaction limits"** | current |
| Rails | Same-day ACH, domestic wire, **international wire**, **RTP instant payments** | current |
| Fee posture | "Unlimited free same-day ACH and international wires **for bill payments**" | current |
| API rails | Built on **Increase** (Ramp Treasury launch, Jan 2025) | [3P] increase.com customer page |
| Historical APY | **2.5% at launch (Jan 22, 2025)** → **2% (May 2026 onward)** | [3P] |

**Conspicuously NOT stated:** an exact dollar cap on the IntraFi sweep coverage. Ramp says "tens of millions" with no number. Rho publishes "$75,000,000 per entity" for Business Savings. [Rho claim: **verified correct** that Ramp publishes no cap.]

**B. Ramp Investment Account**
| Attribute | Value | As of |
|---|---|---|
| Yield | **up to 4.44% YTM**, net of advisory fee | **09/03/2026** (treasury page) / rendered on pricing page with same figure |
| Advisory fee | **up to 0.15%** charged by **Ramp Advisory LLC** | current |
| Initial minimum | **$5,000** | current |
| Subsequent deposits / withdrawals | **$50 minimum** | current |
| Manager | Portfolios managed by **Moment Advisors, LLC** (subadviser) | current |
| Custody / brokerage | **Apex Clearing Corporation**, SEC-registered broker-dealer, FINRA/SIPC | current |
| Protection | **SIPC up to $500,000 ($250,000 cash)**. **"Not a deposit product, not insured by the FDIC, and may lose value"** | current |
| Liquidity | short-term funds "same-day"; long-term withdrawals typically **2 business days** | current |
| Yield methodology | "yield to maturity (YTM) as of today based on a **hypothetical $10M investment**... market-value-weighted average of security-level YTMs... **excludes fees, expenses, transaction costs, leverage, defaults, and calls/prepayments**" | current |

Note the methodology asymmetry: Ramp's 4.44% is a **YTM on a hypothetical $10M position, with the disclosure explicitly saying YTM excludes fees**, while the page separately says "net of advisory fees". Rho's 4.66% is a **sought net yield from 90-day T-Bill rates net of a stated tiered fee**. These are not apples-to-apples.

Enterprise tier also unlocks **DACAs and letters of credit** (ramp.com/pricing feature table) which is a genuinely enterprise-treasury capability Rho does not list.

### 2.7 Procurement

Procurement is **an add-on to Plus or Enterprise**, explicitly labeled that way in the pricing table: **"Procurement (Add-on to Plus or Enterprise)"**. It is therefore **not** included in the $15/user/mo Plus price. [Rho claim: **verified correct**]

Procurement capabilities (ramp.com/procurement + pricing table):
- AI-powered intake: parses contracts/screenshots, auto-fills forms; **custom intake** is Plus+
- **Advanced workflow builder** (Plus+); dynamic approval routing by vendor, category, spend amount; **parallel approvals** across finance/IT/legal/security; Slack approvals; Ironclad contract review integration
- **Integrations with CLM, TPRM, and Ticketing tools** (Plus+)
- **Vendor onboarding with custom forms** (Plus+)
- **Purchase order management** (Plus+); auto-generates POs post-approval; syncs to NetSuite and QuickBooks Online; one-time virtual card generation
- **Match card transactions to purchase orders** (Plus+)
- **AI-driven vendor compliance reviews** (Plus+)
- **Three-way matching with Ramp POs and item receipts** (Plus+); validates unit/price/total, auto-blocks payment on mismatch
- Vendor intelligence: benchmarks quotes against anonymized transaction data, detects overlapping services, renewal reminders, **Okta integration** for software usage and inactive seat identification

Metrics: **"Intake to pay is now 3x faster"**, approval cycles from weeks to ~48 hours (Skin Pharm case study); Ramp Procurement customers **"on average reduce vendor costs by 16% annually and cut manual purchasing work by 46 hours per month"**. [Ramp claim]

### 2.8 Newer platform surfaces

**Ramp Budgets** (Q1 2026): track budgets vs actuals in real time across T&E, AP, procurement, POs; approvals show remaining and committed; upload an existing budget rather than rebuild. Gated to Plus+ ("Track budgets vs. actuals in real time" appears under Plus).

**Ramp Sheets**: listed in product nav, page not publicly fetchable (404 on direct curl).

**AI Token Spend Management** (ramp.com/ai-token-spend-management):
- Tracks token spend by provider, model, team, user, API key, department, project
- Providers supported: **Anthropic, OpenAI, Gemini, Cursor** ("more being added based on customer demand")
- Connects via the provider's **admin API**; Ramp states it sees **cost and usage metadata only, never prompt or response content**
- Weekly automated briefing with savings recommendations; real-time spike flagging; **spend limits by key with owner/manager/team notification**; automatic **invoice reconciliation** with gap flagging, custom pricing, and commitment-vs-utilization tracking
- **Usable standalone without being a Ramp card/expense customer**, free tier: dashboard + basic briefings + anomaly detection
- Adoption claim: **"Trusted by 2,000+ businesses"**
- Stats: **"12% of monthly AI spend identified as potential savings for the average business (as of June '26)"**; **"1 in 3 businesses found a lower-cost model alternative for the same work (as of June '26)"**; Ramp analyzed **110T tokens** and found 3 spending profiles
- Named customer quotes: Christy Schwartz (CFO, Opendoor), Greg Cooley (Controller, AngelList, "losing $10,000 a month" on missing prompt caching), Neusha Sayadian (Sansa Services)
- Ramp's own AI bill "hit ~10% of payroll" per its CFO [Ramp claim]

**Router / router.com** (launched **2026-08-19**):
- Single API endpoint that routes each request to the lowest-cost model meeting a quality bar
- Model providers at launch: **OpenAI, Anthropic, SpaceXAI (formerly xAI), DeepSeek, Moonshot, Minimax, Nvidia, Z.ai**; **Google Gemini "coming soon"**
- **"Cut your AI costs by 40% on average"**; PYMNTS reported "40% for early customers (vs. 30% internally)"
- **Free routing through 2026**; **$26 in model credits**; pricing after 2026 not announced
- **US-only developers/teams at launch**; enterprise features and more countries "coming soon"
- Install path is an agent-native one-liner: `curl -fsSL https://agents.ramp.com/install.sh | sh && ~/.local/bin/ramp router configure` (note: **`agents.ramp.com`** is the CLI distribution host)
- Ramp says it built and ran this router internally for three years [Ramp claim]
- Sources: PR Newswire 2026-08-19/20; TechCrunch 2026-08-20; Unite.AI

**Ramp Rate** (public dataset, API + MCP): software adoption benchmarks over a trailing 12-month window anchored to the latest complete month. Metrics: **Adoption Rate, Growth Rate, New Adopter Rate, Switch Rate**. REST base `https://api.ramp.com/v1/public/ramp-rate`. Endpoints: `GET /categories`, `/categories/{category}/summary`, `/categories/{category}/vendors`, `/vendors/resolve`, `/vendors/{slug}/profile`, `/vendors/compare` (2-10 vendors). **Requires provisioned access via the Ramp Data Partner Program.**

**AI Index** (public dataset): measures AI adoption among American businesses, sample **"more than 50,000 American businesses and billions of dollars in corporate spend"**, built on Bonney et al. (2024) methodology. REST base `https://api.ramp.com/v1/public/ai-index`; endpoints `GET /adoption`, `/adoption/sectors`, `/adoption/sizes`, each with a `months` parameter (1-120, default 1). Ramp explicitly discloses the limitation: **"Because AI Index is based on observed paid transactions, it likely undercounts total AI adoption when businesses use free tools or employees use personal accounts."** That is unusually honest self-disclosure for marketing-adjacent data.

---

## 3. Pricing tiers and exactly what each gates

### 3.1 Headline pricing (ramp.com/pricing, 2026-09-11)

| Tier | Price | Billing | Trial |
|---|---|---|---|
| **Free** ("AI-assisted") | **$0/mo/user** | monthly | n/a |
| **Plus** ("AI-powered") | **$15/mo/user** **+ "Platform fee based on team size"** | "Save 20% with annual billing" | **30-day free trial** per Ramp FAQ |
| **Enterprise** ("AI-tailored") | **Custom** | Annual billing | contact sales |
| **Procurement** | **Add-on to Plus or Enterprise** (separate line) | n/d | n/d |

**The platform fee is the pricing story.** Ramp publishes the string "Platform fee based on team size" and **no formula, no calculator, no range**. Third-party aggregators report observed platform fees ranging **$0 (qualifying startups/small businesses) to $15,000+/month** for high-volume enterprise deployments, but cannot separate Plus from Enterprise. [3P: saastruecost, vendr, checkthat.ai] There is no way to compute Ramp's total cost of ownership from public information. [Rho claim "undisclosed platform fee": **verified correct**]

### 3.2 Gating that actually bites (from the full pricing comparison table)

| Capability | Free | Plus | Enterprise |
|---|---|---|---|
| **Accounting integrations** | **QuickBooks Online, Xero only** | **+ NetSuite, Sage Intacct, Acumatica, Microsoft Dynamics 365 Business Central, + more** | **+ Workday, Oracle Fusion Cloud, Microsoft Dynamics F&O, + more** |
| **HRIS integrations** | no | **+ Workday** | + Workday, **continuous HRIS sync** |
| **Multi-entity support** | no | ✓ | ✓ |
| **Custom field support** | no | ✓ | ✓ |
| **Custom user roles / multi-entity visibility restrictions** | no | ✓ | ✓ |
| **Audit log** | no | ✓ | ✓ |
| **SCIM, SSO, SAML** | no | ✓ | ✓ |
| **AI coding for every field** | no | ✓ | ✓ |
| **Automated accruals and reconciliation; amortization** | no | ✓ | ✓ |
| **Advanced accounting rules / advanced NetSuite support** | no | ✓ | ✓ |
| **Automated batch payments** | no | ✓ | ✓ |
| **Guest travel bookings** | no | ✓ | ✓ |
| **Custom travel policies (role/dept/location)** | no | ✓ | ✓ |
| **Auto-lock cards on missing receipts** | no | ✓ | ✓ |
| **Custom report builder / schedule exports / share live reports** | no | ✓ | ✓ |
| **Budgets plan-vs-actuals real time** | no | ✓ | ✓ |
| **Local currency card issuing (30+ countries)** | no | no | ✓ |
| **Locally funded reimbursements; pay card statements in local currency; fund bill payments with local currency** | no | no | ✓ |
| **DACAs and letters of credit** | no | no | ✓ |
| **Dedicated account + customer success manager** | no | no | ✓ |
| **Priority 24/7 global support** | no | no | ✓ |
| **Implementation services, custom development, ERP extensions** | no | no | ✓ |
| **Ramp MCP access management** (Company → Integrations → Ramp MCP → Manage access) | no | **Ramp Plus feature** | ✓ |

**Free tier is genuinely substantial:** corporate cards with unlimited physical/virtual issuance, card issuing controls, travel bookings + company-wide travel policy, expense management with receipt matching, reimbursements, AP with OCR + configurable approvals + **AP Agent fraud checks**, treasury (2% checking and 4.44% investment account), **custom reports and insights via AI reporting**, price intelligence, automated vendor tracking and contract extraction, **24/7 chat support**, **1099 filing at $0.65/IRS filing**.

**What most materially forces an upgrade:** NetSuite/Sage Intacct, multi-entity, audit log, SSO/SCIM, batch payments, custom roles, approval routing rules, guest travel, and procurement (which is an add-on even on top of Plus).

---

## 4. Developer platform and API depth

Source of truth: `https://docs.ramp.com/llms-api.txt` (604 KB, downloaded 2026-09-11) and `https://docs.ramp.com/llms.txt` guide index. Rendered docs pages are JS shells; Ramp explicitly instructs agents to read the `.txt` exports and `/openapi/developer-api.json` instead. That instruction itself is a signal about how agent-oriented Ramp's docs strategy is.

### 4.1 Surface area

**252 documented operations across 39 top-level resource groups** under `/developer/v1/`:

| Group | Ops | Group | Ops | Group | Ops |
|---|---|---|---|---|---|
| accounting | 64 | custom-records | 30 | vendors | 27 |
| bills | 15 | funds | 11 | cards | 11 |
| users | 8 | purchase-orders | 8 | webhooks | 6 |
| spend-programs | 4 | reimbursements | 4 | locations | 4 |
| item-receipts | 4 | departments | 4 | transactions | 3 |
| receipts | 3 | receipt-integrations | 3 | memos | 3 |
| blank-canvas-approvals | 3 | banking | 3 | **ai-spend** | 3 |
| vault | 2 | unified-requests | 2 | trips | 2 |
| transfers | 2 | token | 2 | statements | 2 |
| entities | 2 | comments | 2 | cashbacks | 2 |
| business | 2 | bank-accounts | 2 | applications | 2 |
| spend-requests | 1 | roles | 1 | repayments | 1 |
| merchants | 1 | embedded | 1 | custom-form | 1 |
| audit-logs | 1 | | | | |

**Write operations are first-class**, not read-only: create/terminate/suspend physical cards; create/suspend/terminate funds and fund members; create and pay bills; create POs; create and manage users; create custom tables and columns; upload GL accounts, vendors, tax rates, field options; post accounting codings and sync status; approve/reject via Blank Canvas Approvals; create financing applications.

**Standout capabilities Rho has no analogue for:**
- **Custom Records API (30 ops):** define your own tables in Ramp (`custom-tables`), extend native Ramp tables with custom columns (`native-tables`), and **Matrix Tables** for lookup relationships (e.g. map accounting dimensions to approvers so spend auto-routes).
- **Vault API** (`/cards/vault`, `/vault/cards`): retrieve a card's PAN/CVV server-side. Requires **`cards:read_vault` scope plus production approval via a Developer API support ticket**. All customers can use Vault in Sandbox.
- **Embedded cards** (`POST /developer/v1/embedded/cards/{card_id}/embed`): Ramp-served iframe so a user's browser sees card details without the PAN touching your servers.
- **Blank Canvas Approvals:** externalize an approval step to your own procurement/CLM system, receive the request by webhook, return the decision.
- **AI Spend endpoints:** `GET /ai-spend/api-keys` (provider API keys with estimated spend), `/ai-spend/team` (users with estimated AI spend), `/ai-spend/usage` (daily usage/spend by provider, model, product). Plus an **inbound** endpoint `POST /developer/v1/ai-usage/unified` for AI platforms to broadcast customer usage events into Ramp (customers bring their Ramp API key to their AI vendor).
- **Incorporation API** (private preview): approved partners can form a US LLC or, when separately enabled, a C-Corp through Ramp's incorporation provider.
- **Stablecoin currency identifiers** in monetary schemas: `USDB, USDC, USDSUI, USDT, EURC, OPEN_USD` alongside ISO 4217. Stablecoin Bill Pay payments carry **no fee**.

### 4.2 Auth

- **OAuth 2.0**. Token endpoint `POST /developer/v1/token`, revoke at `/developer/v1/token/revoke`, HTTP Basic Auth with client id/secret.
- Grants: **Client Credentials** (server-to-server, no user consent), **Authorization Code** (required for third-party/multi-tenant apps), **Refresh Token**.
- Authorize URLs: `https://app.ramp.com/v1/authorize` (prod), `https://demo.ramp.com/v1/authorize` (sandbox). `state` is required for new integrations. Authorization codes expire in **10 minutes**.
- **Token lifetimes:** Client Credentials access tokens **10 days (864,000s)**, no refresh token. Authorization Code / Refresh Token access tokens **default 1 hour (3,600s)**, configurable per app.
- Token prefixes: `ramp_business_tok_`, `ramp_user_tok_`, `ramp_business_jwt_`, `ramp_user_jwt_`.
- **Scopes are `resource:permission`**, ~50 documented: `accounting:read/write`, `applications:read/write`, `bank_accounts:read/write`, `bills:read/write`, `budgets:read`, `business:read`, `cards:read/write`, **`cards:read_vault`**, `cashbacks:read`, `custom_records:read/write`, `departments:read/write`, `entities:read`, `incorporation:read/write`, `item_receipts:read/write`, `funds:read/write`, `limits:write`, `locations:read/write`, `memos:read/write`, `merchants:read`, `purchase_orders:read/write`, `receipt_integrations:read/write`, `receipts:read/write`, `reimbursements:read/write`, `spend_programs:read/write`, `statements:read`, `tasks:read`, `transactions:read/write`, `transfers:read`, **`treasury:read`**, `users:read/write`, `vendors:read/write`, plus OIDC `openid`, `offline_access`.
- Only **Admin and Business Owner** users can authorize third-party OAuth apps. Insufficient permission produces "Business not authorized to use this application".
- Scopes are bound at issuance and cannot be changed on an existing token.

### 4.3 Rate limits, environments, reliability

- **200 requests per 10-second rolling window, per source IP.** 429 on exceed; exponential backoff recommended (1s, 2s, 4s).
- Requests over **60 seconds** are terminated with **504**.
- Theoretical maximum throughput at 200 req/10s and 100-item pages: **120,000 records per minute**.
- Higher limits available by submitting a Developer API support ticket with documented usage.
- **Sandbox:** frontend `https://demo.ramp.com`, API `https://demo-api.ramp.com`. No real money movement. A **demo actions panel (⌘J)** simulates events: pay current bill, mark reimbursement as paid, add transactions, each with documented role requirements.
- Sync guidance is candid about limitations: `GET /transactions` `synced_after` **"only finds transactions that have been synced to an accounting system after the specified time; it is not a general updated-at filter"**; `GET /bills` `from_created_at` catches **new records only, no updated-at filter**; `GET /purchase-orders` has no incremental param at all. Recommended polling: **every 1-4 hours on weekdays, every 12 hours on weekends**.
- All responses carry an **`x-trace-id`** header for support correlation.
- Deferred/async endpoints include `/deferred` in the URL (e.g. creating a user).

### 4.4 Webhooks

**45+ business event types** across 11 resources, each gated on the matching read scope:

| Resource | Events |
|---|---|
| Applications | `applications.status_updated` |
| Bills | `bills.approved`, `.archived`, `.created`, `.paid`, `.ready_to_sync`, `.rejected`, `.updated` |
| Entities | `entities.created` |
| Item Receipts | `item_receipts.created` |
| Purchase Orders | `purchase_orders.archived`, `.created`, `.updated` |
| Reimbursements | `reimbursements.batch_payment_reimbursed`, `.ready_for_review`, `.ready_to_sync`, `.sync_requested` |
| Spend Requests | `spend_requests.comment_created`, `.created` |
| Transactions | `transactions.all_requirements_met_and_approved_changed`, `.authorized`, `.body_coding_updated`, `.cleared`, `.declined`, `.ready_for_review`, `.ready_to_sync`, `.receipt_added`, `.sync_requested`, `.synced` |
| Unified Requests | `unified_requests.created`, `.external_approval_request`, `.external_approval_request_reset`, `.modified`, `.node_advanced`, `.override_approved`, `.updated` |
| Users | `users.invite_accepted` |
| Vendor Agreements | `vendor_agreements.archived`, `.created`, `.deleted`, `.document_added`, **`.renewal_milestone`** (fixed 90-day renewal milestone), `.updated` |
| Vendors | `vendors.activated`, `.approved`, `.updated` |
| Testing | `tests.test_event`; plus `webhooks.verification` during setup |

Mechanics: HTTPS endpoint must return 2xx within **10 seconds**. Subscriptions start `pending_verification` and require a challenge round-trip. Up to **5 custom `additional_headers`** (names ≤100 chars, values ≤1,000 chars; `Host`, `User-Agent`, `Content-Length`, `Content-Type`, `Accept`, `Accept-Encoding`, `Connection`, `Upgrade`, and anything starting `X-Forwarded`/`X-Real`/`X-Original` are reserved). Signature: **HMAC-SHA256 of the raw request body in `X-Ramp-Signature`**, verified against a `secret` returned at subscription creation. Retries: **2xx** no retry; **3xx/4xx except 429** instant failure no retry; **429/5xx up to 10 total attempts** with exponential backoff and full jitter (first retry 0-2s, capped at 60s). Same event `id` across retries for idempotency. **Events may arrive out of order.** A `transactions.cleared` event can be a purchase, refund, or reversal and **does not include the amount**; you must fetch the transaction and read the signed `entity_amount.value`. A **developer dashboard for webhook monitoring is "coming soon"** (i.e. does not exist yet).

`POST /developer/v1/webhooks/mock-webhook-event` fires a mock at **all matching active subscriptions in the business**, with a **real payload and signature and no test marker**. Ramp warns explicitly: "In production, live receivers can process these events as real activity."

### 4.5 Documented integration patterns

Ramp's `llms.txt` prescribes a decision tree, which is itself a strategy statement:
1. **Default connectors** first (ramp.com/integrations).
2. **Ramp MCP** for conversational assistant workflows; **Ramp CLI** for terminal/scheduled/agent-loop workflows.
3. **Developer API** for server-to-server, Custom Records, webhooks, partner apps, ETL, anything that "needs to outlive a single user session".
4. **Ramp Agent Cards** for agents that must complete a checkout.

ERP coverage in the guides: two-way sync, chart of accounts mirrored in, transactions/bills/reimbursements/payments exported back; **"30+ ERPs"** reconcilable per the Q1 2026 release page.

---

## 5. Ramp's AI and agent strategy, 2025-2026

### 5.1 Shipped timeline

| Date | Shipped | Detail |
|---|---|---|
| **Jul 2025** | **Agents for Controllers** (first agent release) | Auto-enforce expense policy, eliminate unauthorized spend, prevent fraud. Ramp claim: **automate 85% of expense reviews with 99% accuracy, catch 15x more out-of-policy spend than rule-based flags** |
| **Oct 2025** | **Agents for AP** (second agent release) | Invoice coding (learned logic from historical data, **85% of accounting fields right the first time**), approval streamlining with context, and card-payment application by **finding card payment opportunities directly in the vendor's payment portal** |
| **Nov 17, 2025** | AI operating stats disclosed | 26.1M AI decisions over $10B of spend in Oct 2025; 511,157 policy violations prevented ($291M); $49,000 fake invoice blocked |
| **Q1 2026** | **Accounting Agents** | Code transactions and invoices, **"correct on the first pass 9 out of 10 times"**; **auto-sync in-policy spend to ERP with 98% accuracy**; **book month-end accruals for unsynced card transactions** (create, post, reverse); **reconcile across 30+ ERPs**; headline **"Close your books 3x faster"** |
| **Q1 2026** | **Ramp Budgets** | Real-time budget vs actuals across T&E, AP, procurement, POs; approvals carry budget context; upload existing budget |
| **Q1 2026** | **Ramp Global** | Europe launch announced ("this summer" for UK/EU-HQ businesses); pay bills from a UK or EU bank account via **SEPA (EUR)** and **BACS (GBP)**; **local INR reimbursement funding in India**; **local card issuing in Mexican Pesos and Brazilian Real** |
| **2026-03-11/13** | **Agent Cards** | Purchase-scoped, **merchant- and amount-scoped** card credential issued immediately before a single checkout. Built on **Visa Intelligent Commerce (VIC)**. **No PCI exposure: agents never handle raw card data.** Not for subscriptions or later merchant charges (use a Virtual Card) |
| **2026-03-31** | **Ramp x Visa deepened partnership** | Renewed **multi-year issuing agreement** plus integration with **Visa Intelligent Commerce** and the **Visa Trusted Agent Protocol**; "AI agents that securely automate corporate bill pay" |
| **2026-04-29** | **Fleet of procurement AI agents** | Natural Language Intake, Advanced Workflow Builder, Due Diligence, Renewal and Contract Intelligence, **Zero-Touch Sourcing (Early Access)**, Reporting. Runs sourcing events end to end, detects compliance risk, benchmarks price on "millions of Ramp transactions". Stat cited: **average AI contract grew from $39,000 to $500,000 in two years** |
| **2026-06-03** | **Ramp Stack** | "AI operating system for accounting firms". Autonomous agents for bank reconciliations, journal entries, depreciation schedules, prepaid amortization, deferred revenue roll-forwards, variance analysis, month-end close. Onboard a client "within an hour". **Source-linked outputs with full audit trails; firm workflows "never shared, never used to train AI models"**. Market: ~$150B accounting sector; **4,500+ accounting firm partners; 92 of the top 100 CPA firms already have clients on the platform** |
| **2026-06-10** | **Applied AI Solutions** | Enterprise services offering: dedicated engineering + finops expertise to deploy agents. Components: Context Extraction (policies, approval logic, vendor history, contract terms, GL mappings), Workflow Prioritization, System Integration (ERPs, procurement tools, document stores, approval workflows, banks, spreadsheets), Agent Design and Deployment, Human Review and Controls (approval paths, exception queues, audit trails, guardrails), Continuous Improvement. Workflows: token spend, AP, procurement, close, AR, expense. **"Available for select enterprise customers."** No pricing, no named customers |
| **Q2 2026** | **AI Token Spend Management** | see 2.8 |
| **2026-07-17** | **Open-source `ramp_mcp` repo archived** | Replaced by hosted MCP. Repo was MIT, © 2025 Ramp Business Corporation |
| **2026-08-19** | **Router / router.com** | see 2.8 |

### 5.2 MCP: three servers

Ramp ships **three distinct MCP servers**. This is the most complete MCP posture of any spend/banking platform found in this research.

| Server | URL | Auth | Audience | Scope |
|---|---|---|---|---|
| **Ramp MCP** | `https://mcp.ramp.com/mcp` (demo: `https://demo-mcp.ramp.com/mcp`; also `https://mcp.ramp.com/mcp-apps/demo/mcp`) | **Browser OAuth as the signed-in Ramp user** | Customers / end users | Account data **and write actions** |
| **Developer MCP** | `https://mcp.ramp.com/developer/mcp` | **None (unauthenticated)** | Developers and coding agents | Public docs, API reference, OpenAPI schemas |
| **Ramp Data MCP** | `https://mcp.ramp.com/ramp-data/mcp` | **API key** (`RAMP_DATA_API_KEY`, `Authorization: Bearer`) via Ramp Data Partner Program | Researchers, partners | **Ramp Rate** + **AI Index** datasets |

**Ramp MCP capability surface** (grouped by job, because Ramp says tool names "drift"):
- **Read and analyze spend:** search transactions by merchant/amount/date/user/state, pull full spend exports and run SQL-style analysis (admin), load vendors, accounting and tracking categories, departments, entities, locations, spend limits, spend programs, org chart, **treasury balances** (checking balance, daily balance history, business wallet accounts, **investment and portfolio balances**, wallet transfers)
- **Process approvals:** approve/reject transactions, reimbursements, and **unified requests (POs, fund requests, procurement approvals)**. **Bill approvals are NOT available via MCP** (route through the UI or the Blank Canvas Approvals API; "on the roadmap")
- **Submit and complete expenses:** employees submit/resubmit reimbursements, complete required details
- **Edit and act:** transaction memo, fund assignment, accounting categories, trip assignment, attendees; post comments with @mentions; **lock, unlock, activate cards**; apply GL coding to transactions and reimbursements
- **Answer questions:** policy Q&A ("Is this within policy?"), Help Center search, **decline explanations**
- **Make purchases:** generate **Agent Card** credentials
- **Manage trips:** create trips, view with status filters, connect transactions to trips, retrieve flight and hotel bookings
- **Not supported:** **receipt/file uploads through MCP** (stated as an MCP protocol limitation, not a Ramp one)

**Governance and controls (this is the part competitors will struggle to match):**
- Every MCP action **respects the authenticated user's existing Ramp role**. Employees see only their own data; admins see company-wide.
- **Every write operation lands in the customer's Ramp audit log automatically**, no extra wiring.
- Admins manage which employees can connect AI tools at **Company → Integrations → Ramp MCP → Manage access**, restricting by **role, department, or specific users**. **This access-management control is a Ramp Plus feature.**
- **Session expiry: read-only sessions expire 1 week after last use; read-write sessions expire 24 hours after last use.**
- **Custom MCP clients and third-party gateways (Glean, MintMCP, GoSearch named) must have their exact redirect URI allowlisted by Ramp before OAuth completes.** `https://` or `localhost`/`127.0.0.1` only; **no wildcard subdomains**.
- External MCP clients must authorize **through the shared Ramp MCP OAuth client, not their own Developer API OAuth app**.
- Multi-business pattern: any unused path `https://mcp.ramp.com/<business-identifier>/mcp` is an alias for production, letting each client connection hold its own OAuth session. Reserved identifiers: `developer`, `employee`, `mcp`, `ramp-data`, `ramp-rate`.
- Limits: **query results capped at 100 rows**; ETL concurrent-table limits ("too many tables loaded" resolves by dropping unused tables).
- Supported clients called out by name: **Claude (one-click from the MCP directory), ChatGPT (requires Plus/Pro), Notion, Claude Code, Codex, Cursor, VS Code, Windsurf, Continue**. **Microsoft Copilot for 365 is explicitly not supported natively** (integrate via Copilot Studio or Power Automate + Developer API).

**Developer MCP tools:** `developer_docs_search` (scopeable to `/api` or `/guides`), `developer_docs_schema` (returns the OpenAPI operation object, selectable by operation ID, docs URL, or `METHOD /path`), `developer_docs_resolve`, `developer_docs_read`, `developer_docs_list`, a root-index tool, and `developer_submit_feedback`.

### 5.3 Ramp CLI

- **Open source: `github.com/ramp-public/ramp-cli`**. Install `curl -fsSL ... | sh` (distribution host `agents.ramp.com`), or via `uv`.
- **Defaults to Sandbox**; `--env production` or `ramp env` to switch.
- **OAuth login (`ramp auth login`)**; every action is attributed to the authenticating user and inherits their Ramp role exactly. `ramp users me` confirms identity.
- **Output modes: `--human` (tables, default in a TTY) and `--agent` (JSON, default when piped)**, plus `--wide`, `--quiet`, `--no-input` for CI.
- Per-tool flags include `--json` (raw request body), **`--dry_run`/`-n`** (print request without sending), `--page_size`, `--next_page_cursor`.
- **Commands:** `auth`, `config`, `env`, `applications`, **`skills`**, `feedback`.
- **Resources and tools:** `accounting` (categories, category-options) · `bills` (search, get, draft, pending, **approve**, attachments) · `funds` (list, activate, **creds**, lock) · `general` (comment, explain, help-center, policy) · `purchase_orders` (search, get) · `receipts` (**upload**, attach) · `reimbursements` (list, pending, submit, approve, edit) · `requests` (pending, approve) · `transactions` (list, get, approve, edit, missing, flag-missing, explain-missing, memo-suggestions, trips) · `travel` (list, create, bookings, locations) · `users` (me, search, org-chart)
- Note: **the CLI can approve bills and upload receipts, which MCP cannot.** The two channels are deliberately non-identical.
- **Skills system:** packaged instruction sets for agent frameworks. Named skill: **`agentic-purchase`**, which drives Agent Cards end to end (request credential → checkout → audit). Skill URL: `https://github.com/ramp-public/ramp-cli/blob/main/src/ramp_cli/skills/agentic-purchase/SKILL.md`.
- **CLI is backed by `https://api.ramp.com/agent-tools` endpoints which are explicitly "not accessible to external clients."** Ramp reserves that surface for itself.
- Production/remote-host operation: authenticate locally and copy the session config. Warning in docs: **"Some hosted runtimes rewrite `~/.config/ramp/config.toml` on restart, which removes the refresh token."** Treat `config.toml` as a credential.

### 5.4 Agent Cards and agentic payments

- **Agent Card = a purchase-scoped credential, merchant- and amount-scoped, requested immediately before one checkout.** Explicitly **not** for subscriptions or later merchant charges; use a reusable Virtual Card for those.
- **Requires at least one active fund.** Funds and Spend Programs are the constraint layer ("back agent purchases with recurring-budget templates instead of one-off funds").
- Built on **Visa Intelligent Commerce**; Ramp also integrates the **Visa Trusted Agent Protocol**. [3P: stabledash 2026-03-11; Ramp/Visa PR 2026-03-31]
- Two paths: **user-session assistant or terminal agent** → "Agentic Purchase playbook"; **company-owned standalone agent** → "Agentic Payments guide", and **standalone agents are in limited early access** as of 2026-09-11.
- Ramp's stated design principle (Intelligence FAQ): **"no money ever moves without a human confirmation"**. This is in tension with a standalone company-owned agent holding payment authority; the reconciliation is that the approval/fund/spend-program layer is the human gate, not a per-transaction click.

### 5.5 Ramp Intelligence (the umbrella)

Ramp's own framing: **"Ramp Intelligence isn't a single product, it's a layer of AI technology that sits across all our products,"** surfaced by a blue Ramp Intelligence icon. Named behaviors: auto-approve low-risk/routine, escalate risky or ambiguous; answer "is this in policy?" **by text message**; compliance dashboard showing policy violations, review bottlenecks, and worrisome spending patterns; real-time anomaly and **AI-generated-fake** detection; three-way match; price benchmarking against 70,000 businesses; hotel price-drop rebooking; vendor payment portal automation for card-eligible vendors; line-item invoice transcription.

Customer-proof stats on that page: **75% reduction in credit card reconciliation time; $250K savings identified by Ramp's insight tool; 90% of transactions auto-coded; 5X faster transaction review.** [Ramp claim, no per-stat as-of date] Named reference: **Rama Katkar, CFO, Notion**: "People ask how we're using AI in finance and I have a simple answer for them. We use Ramp."

---

## 6. Support model

| Tier | Support entitlement (ramp.com/pricing feature table, 2026-09-11) |
|---|---|
| **Free** | Help center; **"Instant, 24/7 AI help for any Ramp question or task"**; **24/7 chat support**. **No phone support.** |
| **Plus** | All of Free plus **24/7 phone support**; **24/7 phone support for travel bookings**; "Chat, email, and phone support" |
| **Enterprise** | All of Plus plus **Priority support**, **Custom support**, **dedicated account and customer success manager**, **Priority 24/7 global support**, implementation services (custom scoping and rollout, integration setup and validation testing, employee training and change management) |

A general support phone number is published in the ramp.com footer: **+1-855-206-7283**. The pricing table nonetheless marks **24/7 phone support as a Plus and Enterprise row**, not a Free row.

Developer support is **ticket-based only** ("Submit a Developer API support ticket"), across MCP, CLI, webhooks, rate-limit increases, Vault production approval, redirect-URI allowlisting, and Ramp Data access. There is no published developer SLA.

**Assessment of the Rho claim** ("Ramp funnels most founders into low cost channels and reserves higher touch service for larger accounts"): **directionally correct but overstated.** Free-tier customers do get **24/7 chat plus a 24/7 AI assistant**, which is more than "automated help centers or general support queues". What is genuinely gated is **phone**, **priority**, and **named humans**.

---

## 7. Head-to-head: Ramp vs Rho

Rho figures below are from the local corpus (`pages/core/*.txt`), crawled with rho.co's own as-of dates. Rho's numbers are also marketing; where Rho asserts something about Ramp I verified it independently and say so.

### 7.1 Fees and pricing

| Dimension | **Ramp** | **Rho** | Verdict |
|---|---|---|---|
| Platform / subscription | **Free tier $0**; **Plus $15/user/mo + undisclosed platform fee based on team size** (20% off annual); **Enterprise custom, annual billing**; **Procurement is an add-on on top of Plus or Enterprise** | **$0 subscription, $0 per-user, $0 platform fee, at every size**; AP, expense and accounting automation included | **Rho wins on price transparency and TCO predictability.** Ramp's undisclosed platform fee makes its Plus TCO uncomputable from public information |
| Standard ACH (bill payment) | **$0.59** (effective 2026-06-01), **waived if funded from Ramp Checking** | **$0 same-day ACH** | Rho cheaper at list; parity if you bank at Ramp |
| Same-day ACH | **$10**, waived from Ramp Checking | **$0** | Rho cheaper at list |
| Domestic wire | **$15**, waived from Ramp Checking | **$0** (**$0 domestic wire recall fee**) | Rho cheaper at list |
| International wire (SWIFT USD) | **$20**, waived from Ramp Checking | **optional $15 SWIFT fee**; **$30 international wire recall fee** | Rho slightly cheaper; both add recipient/correspondent bank fees |
| FX / foreign-currency transfer | **3% card FX conversion fee** [3P NerdWallet]; bill-pay FX rate not published | **1% foreign currency conversion**, the only standard payment fee; FX provided by **Wise US Inc.** | **Rho materially cheaper and clearer on FX** |
| Check | **$1.99 standard** (effective 2026-06-01), **$20 overnight (never waived)**, **$1/page attachments (never waived)** | **$0 on domestic checks** | Rho cheaper |
| Stablecoin payment | **no fee**, `USDB/USDC/USDSUI/USDT/EURC/OPEN_USD` supported | not offered | **Ramp only** |
| 1099 filing | **$0.65 per IRS filing, free state filing**, all tiers | not published | Ramp discloses; Rho silent |
| Card annual/per-card fee | $0 | $0 | tie |
| Late fee | not published | **3% of delinquent payment balance per month, up to 6 months** | Rho discloses |

**Net:** Rho's fee sheet is a one-screen list with no tiers. Ramp's is a fee table plus a waiver conditioned on holding a Ramp Checking Account plus an undisclosed subscription platform fee. **On raw payment fees Rho wins on list price; Ramp closes most of the gap only for customers who move their operating account to Ramp**, which is exactly the strategic intent of the waiver.

### 7.2 Cashback

| | **Ramp** | **Rho** |
|---|---|---|
| Published rate | **None.** ramp.com shows "up to 5% savings" (a blended spend-savings estimate, not a rewards rate). Actual rate **0%-1.5%, set per customer, disclosed after you apply**, floor 1% [3P NerdWallet 2026-06-15] | **Published matrix.** Daily Terms: **1.25% standard / up to 2% Rho Platinum**. Monthly Terms: **1% standard / up to 1.75% Platinum** |
| Cap | not published | **$1,000,000 in eligible spend per calendar year, across all tiers**; **earned cashback must be redeemed within 12 months or forfeited** |
| Qualification | Ramp's undisclosed assessment of the business | **Rho Platinum requires: payroll run from Rho, business revenue deposited via Rho Checking, 50%+ of company assets at Rho, and an open Rho Corporate Card** |
| Network / benefits | Visa. Cardholder benefits not enumerated on ramp.com | **Mastercard World Elite for Business**: Priority Pass lounge access, primary car rental insurance, 24/7 concierge, Easy Savings rebates, ID theft protection (as of 08/02/2026) |

**Verdict: Rho wins decisively on disclosure, and its top rate (2%) exceeds Ramp's ceiling (1.5%).** But Rho's 2% carries a heavy qualification bar that amounts to "make Rho your primary bank", and a $1M annual cap plus a 12-month redemption forfeiture. Ramp's 1.5% ceiling has no published cap or forfeiture clause. For a company that will not consolidate onto Rho, the realistic comparison is **Rho 1.25% (published) vs Ramp 0-1.5% (unknown until after application)**.

### 7.3 AP / bill pay

| Dimension | **Ramp** | **Rho** |
|---|---|---|
| Included in base | Yes, on the Free tier | Yes, included with banking, no software fee |
| **Payment rails** | **ACH, same-day ACH, domestic wire, SWIFT USD international wire, check (standard + overnight), Ramp/virtual card, stablecoin** | Rho's Bill Pay page describes **invoice capture, approval routing, duplicate detection, scheduled payments, accounting sync, and payment by check**, with "**Domestic per-payment fees $0 on checks**". **Rho's own product page does not describe ACH/wire/card execution inside Bill Pay**, while its pricing page advertises $0 same-day ACH and $0 domestic wires as account-level payment fees. **This is an unresolved ambiguity in Rho's own corpus** |
| Invoice intake | AI OCR, "99% accurate", CSV upload, ERP import, `POST /spend-requests/draft-via-ocr` | Forward to a Bill Pay inbox with no login required, AI capture drafts the bill |
| Approvals | Configurable workflows on Free; **rules-based routing by vendor/dept/accounting field/payment type on Plus+**; parallel approvers; mobile approvals; **payment release approvals (Plus+)**; **Blank Canvas external approvals via API** | Routes to the right approvers, flags duplicates before payment, mobile approvals |
| **AP agents** | **4 named agents: auto-coding, fraud prevention (unexpected vendor bank changes), approval recommendations with vendor history, automatic card-payment capture for cashback.** Fraud-check agent is on Free; coding/approval/batch agents are **Plus+** | AI invoice capture. No named agent products |
| Three-way match | Yes, with imported POs and item receipts (Plus+), and with Ramp POs and item receipts (Procurement add-on) | Not offered. Rho states plainly: **"It does not include procurement or supply-chain management"** |
| Batch payments | **Plus+** | not gated (no tiers) |
| Procurement | **Separate paid add-on on top of Plus or Enterprise** | **Not offered at all** |
| ERP sync | QuickBooks Online + Xero on Free; NetSuite, Sage Intacct, Acumatica, Dynamics 365 BC on Plus; Workday, Oracle Fusion Cloud, Dynamics F&O on Enterprise; **30+ ERPs reconcilable** | **QuickBooks, NetSuite, Sage Intacct, Xero, Puzzle, Campfire, all included, no tier** |

**Verdict:** **Ramp's AP is a materially deeper product** (more rails, three-way match, PO matching, named agents, ERP breadth, external approval APIs) but it is **tiered**: the automation that makes it deep is Plus+, and procurement is an add-on even then. **Rho's AP is simpler, flat-priced, and complete for a lean finance team**, but it has no procurement, no three-way match, and its own page emphasizes check as the payment method. For a 20-person startup Rho's AP is sufficient and cheaper; for a 300-person multi-entity company Ramp's AP is not replaceable by Rho's.

### 7.4 Treasury: minimums, yield, and protection

| Dimension | **Ramp** | **Rho** |
|---|---|---|
| Operating-cash yield | **Ramp Checking 2% APY (as of 09/11/2026)**, FDIC via First Internet Bank of Indiana + IntraFi sweep | Rho Checking is **FDIC-insured to $250,000 at Webster Bank, a division of Santander Bank, N.A.**; Rho does not publish a checking APY. **Rho Business Savings** is the interest-bearing deposit product |
| Investment yield | **up to 4.44% YTM (as of 09/03/2026)**, net of up to 0.15% advisory fee | **up to 4.66% net (as of 09/11/2026)**, tiered by balance |
| Yield methodology | **YTM on a hypothetical $10M position**; disclosure says YTM "excludes fees, expenses, transaction costs, leverage, defaults, and calls/prepayments" while the headline says "net of advisory fees" | **Sought net yield based on 90-day T-Bill rates**, net of the tier fee; full tier table published (4.66% / 4.56% / 4.46% / 4.36% / 4.21%) |
| **Minimum to access yield** | **$5,000 initial; $50 subsequent** | **$50,000** |
| Fee on invested balances | **up to 0.15%** flat | **0.60% under $2M; 0.45% $2-5M; 0.35% $5-10M; 0.25% $10-20M; 0.15% $20M+**, billed monthly |
| Manager / custodian | Moment Advisors LLC (subadviser); **Apex Clearing Corporation** custody; Ramp Advisory LLC is the RIA | **RBB Treasury LLC dba Rho Treasury**, SEC-registered RIA; custody at **Apex Clearing Corp.** (post-Jul 2024) and **Interactive Brokers LLC** (prior) |
| Protection | SIPC $500,000 incl. $250,000 cash. **"Not a deposit product, not insured by the FDIC, and may lose value"** | SIPC $500,000 incl. $250,000 cash. Same disclosure posture |
| Liquidity | short-term same-day; long-term typically **2 business days** | **2 to 3 business days** (T-Bill sales and mutual fund redemptions settle T+2 before the daily cutoff of 5:00 PM ET T-Bills / 4:00 PM ET mutual funds, T+3 after) |
| Allocation control | portfolios managed by Moment; not user-configurable per public docs | **US T-Bills, ultra-short income fund, short-term bond fund in 5% increments; short-term bond fund capped at 50%** |
| Max FDIC coverage published | **"tens of millions"** with **no numeric cap** | **$75,000,000 per entity** via American Deposit Management Co.'s **400+ FDIC/NCUA institution network** (as of 08/02/2026) |
| Enterprise treasury instruments | **DACAs and letters of credit (Enterprise tier)** | not offered |

**Verdicts:**
- **Minimum: Ramp wins by 10x.** $5,000 vs $50,000. Rho's own versus page frames its $50K minimum as a win against **Mercury's $250K**, which is true, but Ramp's $5K is lower than both and Rho's versus/ramp page does not mention it. **This is the most important gap in Rho's own competitive framing.**
- **Fee at small balances: Ramp wins big.** A $200K position pays **0.15% at Ramp vs 0.60% at Rho**, a 45bp difference that swamps the 22bp headline yield gap. **Rho's 4.66% is only the $20M+ tier; the sub-$2M tier is 4.21%, which is BELOW Ramp's stated 4.44%.**
- **Headline net yield at large balances: Rho wins.** 4.66% at $20M+ vs 4.44%, though the methodologies differ (sought net T-Bill yield vs hypothetical-$10M YTM).
- **Deposit safety ceiling: Rho wins on disclosure.** A published $75M number beats "tens of millions". But note the asymmetry of the comparison Rho makes: Rho's $75M is on **Business Savings via ADM's 400+ bank network**, Rho **Checking** is only **$250K at Webster/Santander**, while Ramp's IntraFi sweep applies to the **operating checking account itself**.
- **Rho's corpus contains a now-false claim about Ramp treasury.** `treasury-yield-comparison` / `product__treasury.txt` says Ramp's net yield "**Renders as a placeholder on ramp.com, no fixed rate published (checked 2026-09-06)**". As of **2026-09-11** ramp.com/treasury, ramp.com/business-banking, and ramp.com/pricing all render **2% APY (as of 09/11/2026)** and **4.44% (as of 09/03/2026)** with full footnotes. That Rho line should be considered stale or a rendering artifact of Rho's crawl.

### 7.5 Support

| | **Ramp** | **Rho** |
|---|---|---|
| Free/base tier | **24/7 chat** + **24/7 AI assistant**; help center. **No phone** | **24/7 live human support on every account and every tier**, at no cost: **phone 1-855-7-GETRHO**, in-app chat, **SMS** |
| Paid tier | **24/7 phone (Plus+)**; travel-booking phone support (Plus+) | same as base |
| Enterprise | Dedicated account + CSM, priority 24/7 global support, implementation services, training, change management | not published as a separate tier |
| Developer support | **Ticket only**, no published SLA | docs.rho.co |
| Published phone | +1-855-206-7283 (footer) | 1-855-7-GETRHO, clientservice@rho.co |

**Verdict: Rho wins on this axis and the win is real.** Phone-to-a-human on a $0 account is a genuine differentiator, and it is the axis Rho's testimonials lean on hardest. Ramp's counter is a 24/7 AI assistant plus chat on Free and a named CSM only at Enterprise. Rho's characterization of Ramp is **overstated but not false**.

### 7.6 API openness

| Dimension | **Ramp** | **Rho** |
|---|---|---|
| Model | **Full read/write REST API** | **Read-only by design.** "Tokens cannot initiate payments or modify accounts... The Rho API is read-only today" |
| Operations | **252 documented operations, 39 resource groups** | **Accounts, transactions, statements** |
| Auth | **OAuth 2.0**, Client Credentials + Authorization Code + Refresh Token, ~50 granular scopes, Admin/Business-Owner consent required | **Access tokens created in Settings → Configurations → Access Tokens by Account Owners/Admins only**, scoped to account and transaction data, **optional IP allowlist**, **expiry you set up to one year**, revocable |
| Can the API move money? | **Yes.** Create and pay bills, issue and terminate cards, create/suspend funds, create POs, create users | **No, by design** |
| Card issuing via API | **Yes** (physical create/terminate/suspend; virtual list/fetch; Vault PAN retrieval with approval; embedded iframe) | No |
| Webhooks | **45+ event types**, HMAC-SHA256 signatures, 10-attempt retry with jitter, verification handshake, mock events | not published in the corpus |
| Custom data model | **Custom Records: custom tables, native-table extension, Matrix Tables for approver routing** | No |
| Rate limits | **200 req / 10s per source IP**; 60s request timeout; increases by ticket | "rate limits" documented at docs.rho.co (figure not in corpus) |
| Sandbox | **`demo.ramp.com` + `demo-api.ramp.com`** with a ⌘J demo-actions simulator | not published |
| OpenAPI | **Published** (`/openapi/developer-api.json`) plus `llms.txt`, `llms-api.txt`, `llms-guides/*.txt` machine-readable exports | **Published OpenAPI specification** at docs.rho.co |
| Availability | Developer Console app registration; partner program for multi-tenant; production gates on Vault and custom MCP redirect URIs | **Every Rho customer, no waitlist, no approval step** |

**Verdict: Ramp wins openness by an order of magnitude on capability; Rho wins on a narrow, defensible safety property.** Rho's pitch is literally "a leaked token cannot move money", and it markets read-only as a feature rather than a limitation. Ramp's API is a platform for building products on top of Ramp (partner apps, ERP connectors, embedded issuing, agent purchasing). Rho's API is a data feed for your own company. These are different products, and **Rho's own comparison table on `product__api.txt` concedes the point**, listing Ramp with "Three documented MCP servers", "write operations include bill creation, payment execution, and card issuance", and "OAuth 2.0 with granular permission scopes".

### 7.7 AI and agent surface

| Dimension | **Ramp** | **Rho** |
|---|---|---|
| MCP servers | **Three**: account (OAuth, read **and write**), developer-docs (unauthenticated), public-data (API key) | **One production MCP server, read-only**, listed in Anthropic's connector directory; "Claude is the natively supported client today" |
| MCP write actions | **Yes**: approve/reject transactions, reimbursements, POs and fund requests; edit coding/memos/trips; lock/unlock/activate cards; submit reimbursements; post comments; create trips; **generate Agent Card purchase credentials** | **No**, by design |
| Agent payment authority | **Agent Cards**: merchant- and amount-scoped credential, one checkout, Visa Intelligent Commerce, no PCI exposure to the agent | **None** |
| CLI | **Open-source `ramp-cli`** with `--agent` JSON mode, `--dry_run`, and an installable **`agentic-purchase` skill** | **None** |
| Named agent products | Agents for Controllers, Agents for AP, Accounting Agents, Purchasing/Procurement agents (6 named), Ramp Stack, Applied AI Solutions, AI Token Spend Management, Router | AI invoice capture on Bill Pay; automatic expense coding; no named agent products |
| AI governance | Role-respecting, **every write in the audit log**, admin access management per employee (Plus feature), read-only sessions expire 1 week / read-write 24 hours, redirect-URI allowlisting for custom clients | Read-only tokens, Owner/Admin creation with 2FA, IP allowlist, auto-expiry on inactivity |
| Public AI datasets | **AI Index** (50,000+ businesses) and **Ramp Rate**, via REST + MCP, partner-gated | None |
| AI spend management | **AI Token Spend Management** (Anthropic/OpenAI/Gemini/Cursor) + **Router.com** LLM gateway, 40% cost reduction claim, free through 2026 | None |

**Verdict: Ramp is decisively ahead on AI surface, and Rho says so itself.** Rho's own `versus/ramp` FAQ concedes: **"Its agent/AI tooling (hosted MCP server with audited write actions, public CLI) is genuinely ahead, its in-platform travel booking with price-drop rebooking is real, and international reimbursements cover 60+ countries in local currency (all verified on ramp.com/support, 2026-08-02)."** That concession is accurate and I independently verified every element of it.

Rho's only structural counter-argument is the safety framing: a read-only MCP cannot be prompt-injected into moving money. Ramp's answer is layered controls (funds, spend programs, approval workflows, role inheritance, audit log, scoped one-shot credentials) rather than a capability ceiling. **Which is better depends entirely on the buyer's risk appetite, and there is no factual dispute about the capability gap.**

### 7.8 Where each wins, compressed

**Ramp wins on:** treasury minimum ($5K vs $50K) and advisory fee at sub-$20M balances; AP rail breadth and three-way matching; procurement (which Rho does not offer at all); ERP breadth (Workday, Oracle Fusion, Dynamics F&O, Acumatica, 30+ ERPs); global (local card issuing in 30+ countries, reimbursements in 60-70 countries and 40 currencies, SEPA/BACS, INR, MXN/BRL); developer API depth and write capability; webhooks; sandbox; agent/AI surface across the board; a genuinely usable $0 tier; stablecoin payments; DACAs and letters of credit; enterprise implementation services; scale (70,000 customers, $200B annualized volume, $44B valuation).

**Rho wins on:** published cashback matrix with a higher ceiling (2% vs 1.5%); zero platform/per-user/subscription fees at any size; lower list payment fees including 1% FX vs 3% card FX; 24/7 human phone support on every tier at no cost; a named partner bank inside Santander's US organization plus a published $75M FDIC savings ceiling; card-token safety by construction (read-only API); tiered net-yield transparency with a full published fee/tier table; Mastercard World Elite for Business benefits; no-personal-guarantee cards with a published Monthly Terms threshold ($25,000 at Rho or $75,000 combined); free Delaware C-corp incorporation and pre-EIN account opening; simplicity of one flat product with no upgrade path.

---

## 8. Contradictions, gaps, and things conspicuously not stated

### On Ramp's side
1. **No published cashback rate anywhere on ramp.com.** The only public number is a third-party-sourced 0%-1.5% range. `support.ramp.com/cashback-overview`, `/how-does-ramp-cashback-work`, `/ramp-rewards` all 404.
2. **No platform fee formula, range, or calculator** for Ramp Plus. "Platform fee based on team size" is the entire disclosure.
3. **No numeric FDIC sweep cap.** "Tens of millions of dollars per depositor" with no figure, while competitors publish exact ceilings.
4. **No travel booking fee disclosure** and no named travel inventory partner on ramp.com/travel.
5. **60+ vs 70+ countries** inconsistency between two Ramp support pages on international reimbursements.
6. **Investment Account yield methodology is internally tense**: the headline says "net of advisory fees" while the footnote says YTM "excludes fees, expenses, transaction costs".
7. **"No money ever moves without a human confirmation"** (Intelligence FAQ) sits uneasily beside Agent Cards and "company-owned standalone agents" in limited early access.
8. **Footer-linked pages that do not resolve:** `ramp.com/ramp-sheets`, `ramp.com/ramp-for-agents`, `ramp.com/ramp-labs` all returned 404 to direct fetch on 2026-09-11.
9. **Ramp MCP cannot approve bills or upload receipts**, but the CLI can do both. The capability surfaces are asymmetric and Ramp documents this openly.
10. **Webhook monitoring dashboard "coming soon"** and `synced_after` is explicitly not an updated-at filter. Both are honest admissions of platform immaturity in a product this large.
11. **`api.ramp.com/agent-tools` is reserved**: the CLI's own backing endpoints are "not accessible to external clients". Ramp's agent story is open at the MCP/CLI layer but closed at the primitive layer.
12. **Router.com pricing after 2026 is unannounced**, and it is US-only at launch.
13. **Headcount and revenue figures diverge wildly across third parties** (2,455 / 2,718 / 3.2K employees; $1B / $1.4B / $1.5B revenue). Ramp's own PR says only "over $1 billion".

### On Rho's side (relevant to a Ramp comparison)
1. **Internal contradiction on Ramp cashback:** `versus__ramp.txt` (08/02/2026) says 0%-1.5% variable; `product__corporate-cards.txt` (competitive data as of 2026-09-08) says "**1.5% cashback on card spend, flat, no higher tier**". The second is wrong and newer.
2. **Stale claim on Ramp treasury:** Rho says Ramp's yield "renders as a placeholder on ramp.com, no fixed rate published (checked 2026-09-06)". On 2026-09-11 Ramp publishes 2% APY (as of 09/11/2026) and 4.44% (as of 09/03/2026) on three separate pages with full footnotes.
3. **Rho never mentions Ramp's $5,000 investment-account minimum** in its versus/ramp treasury row, even while making the $50K-vs-$250K minimum argument against Mercury. Ramp's minimum is 10x lower than Rho's.
4. **Rho's 4.66% headline is the $20M+ tier.** The under-$2M tier is **4.21% net**, which is below Ramp's published 4.44%. Rho's own table discloses this; its versus/ramp row does not.
5. **Rho's Bill Pay product page describes payment by check** and states "$0 on checks" as the domestic per-payment fee, without describing ACH/wire/card execution inside Bill Pay, while the pricing page advertises $0 same-day ACH and $0 domestic wires at the account level. The scope of Bill Pay's rails is ambiguous in Rho's own corpus.
6. **Rho concedes Ramp's AI lead explicitly** in its own FAQ, which is unusually honest for a versus page and should be treated as a reliable signal.
7. Rho's claim that Ramp "funnels most founders into low cost channels" understates Ramp Free's 24/7 chat plus 24/7 AI assistant, though the phone-support gating is real.

---

## 9. Source index

**Ramp primary (fetched 2026-09-11 unless noted)**
- https://ramp.com/pricing (full tier + feature comparison table + disclosure footnotes; local copy `ramp/pricing.txt`)
- https://ramp.com/treasury
- https://ramp.com/business-banking
- https://ramp.com/corporate-cards
- https://ramp.com/bill-pay
- https://ramp.com/procurement
- https://ramp.com/travel
- https://ramp.com/intelligence (local copy `ramp/intelligence.txt`)
- https://ramp.com/ai-token-spend-management (local copy `ramp/aitoken.txt`)
- https://ramp.com/router (local copy `ramp/router.txt`)
- https://ramp.com/developer-tools
- https://ramp.com/new-on-ramp-q1-2026 (local copy `ramp/q1-2026.txt`)
- https://ramp.com/new-on-ramp-q2-2026 (local copy `ramp/q2.txt`)
- https://support.ramp.com/bill-pay-fees (local copy `ramp/bill-pay-fees.txt`)
- https://support.ramp.com/ramp-mcp and https://support.ramp.com/hc/en-us/articles/45516494479891-Ramp-MCP
- https://support.ramp.com/ramp-reserve-account-overview
- https://support.ramp.com/international-reimbursements
- https://docs.ramp.com/llms.txt (local copy `ramp/llms.txt`)
- https://docs.ramp.com/llms-api.txt (604 KB, 252 operations; local copy `ramp/llms-api.txt`)
- https://docs.ramp.com/llms-guides/{mcp,ramp-mcp,developer-mcp,ramp-data-mcp,build-for-ai-agents,cli,rate-limiting,sandbox,authorization,webhooks,cards-and-funds,virtual-cards,bill-payments,procurement,ai-index,ramp-rate,ai-usage,introduction}.txt (local copies in `ramp/guides/`)
- https://github.com/ramp-public/ramp_mcp (archived 2026-07-17)
- https://github.com/ramp-public/ramp-cli

**Ramp press releases**
- 2025-11-17 $32B: https://www.prnewswire.com/news-releases/ramp-reaches-32-billion-valuation-doubling-revenue-and-customers-in-past-year-302616510.html
- 2025-10 Agents for AP: https://www.prnewswire.com/news-releases/ramp-launches-agents-for-ap-to-automate-accounts-payable-302576975.html
- 2025-07 Agents for Controllers: https://www.prnewswire.com/news-releases/ramp-introduces-ai-agents-to-automate-finance-operations-302502154.html
- 2026-03-13 Billhop: https://www.prnewswire.com/news-releases/ramp-acquires-billhop-to-expand-access-for-uk-and-european-customers-302712928.html
- 2026-03-16 Juno: https://www.prnewswire.com/news-releases/ramp-acquires-juno-to-expand-guest-travel-and-build-the-complete-travel-solution-for-every-business-302714356.html
- 2026-03-31 Visa: https://www.prnewswire.com/news-releases/ramp-and-visa-deepen-partnership-to-power-the-next-era-of-autonomous-finance-302728894.html
- 2026-04-29 Procurement agents: https://www.prnewswire.com/news-releases/ramp-launches-fleet-of-ai-agents-across-its-procurement-platform-302756657.html
- 2026-06-03 Ramp Stack: https://www.prnewswire.com/news-releases/ramp-launches-stack-an-ai-operating-system-for-accounting-firms-302789630.html
- 2026-06-04 Series F $44B: https://www.prnewswire.com/news-releases/ramp-raises-series-f-at-44-billion-valuation-302791103.html
- 2026-06-10 Applied AI Solutions: https://www.prnewswire.com/news-releases/ramp-launches-applied-ai-solutions-helping-enterprises-deploy-ai-agents-across-finance-operations-302796179.html
- 2026-08-19 Router.com: https://www.prnewswire.com/news-releases/ramp-launches-routercom-to-cut-companies-rising-ai-bills-302855572.html

**Third party**
- NerdWallet, "Ramp Card: 2026 Review" (rate range confirmed to NerdWallet June 2026; updated 2026-06-15): https://www.nerdwallet.com/business/credit-cards/reviews/ramp-card
- TechCrunch 2026-06-04: https://techcrunch.com/2026/06/04/ramp-raises-750m-at-44b-valuation-as-investors-hunger-for-fintechs-with-an-ai-story/
- TechCrunch 2026-08-20 (Router): https://techcrunch.com/2026/08/20/ramp-launches-its-own-ai-model-router-called-router/
- TechCrunch 2025-11-17 ($32B): https://techcrunch.com/2025/11/17/ramp-hits-32b-valuation-just-three-months-after-hitting-22-5b/
- TechCrunch 2025-07-30 ($22.5B): https://techcrunch.com/2025/07/30/ramp-hits-22-5b-valuation-just-45-days-after-reaching-16b/
- Bloomberg 2026-06-04 ($44B) and 2026-03-13 (Billhop)
- CNBC 2026-06-04: https://www.cnbc.com/2026/06/04/ramp-valuation-funding-ai-spend.html
- PYMNTS 2026-09-08 ($60B talks): https://www.pymnts.com/spend-management/2026/ramp-eyes-60-billion-valuation-just-months-after-series-f/
- PYMNTS 2026-06 (Ramp Stack / $150B accounting): https://www.pymnts.com/artificial-intelligence-2/2026/ramp-courts-150-billion-accounting-sector-with-new-ai-system/
- Accounting Today (Ramp Stack; Ramp agents)
- CPA Practice Advisor 2026-05-02 and 2026-06-03
- Increase (Ramp Treasury rails): https://increase.com/customers/ramp-treasury
- Finovate (Ramp Treasury launch 2025-01-22; Juno acquisition)
- Sacra, Latka, Revelio Labs, Tracxn (revenue/headcount/acquisition counts, mutually inconsistent)
- stabledash 2026-03-11 (Agent Cards / Visa Intelligent Commerce)

**Rho corpus (local)**
- `pages/core/versus__ramp.txt`, `pricing.txt`, `product__api.txt`, `product__treasury.txt`, `product__corporate-cards.txt`, `product__bill-pay.txt`, `site-llms.txt`
