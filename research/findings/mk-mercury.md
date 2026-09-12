# MERCURY (Mercury Technologies, Inc.): Independent 2026 Research Dossier

Research date: 2026-09-11. All figures carry their source's own as-of date where published.
Sourcing convention used below:
- **[Mercury]** = asserted only by Mercury's own properties (mercury.com, support.mercury.com, docs.mercury.com, github.com/MercuryTechnologies). Marketing.
- **[Rho claim]** = asserted by Rho about Mercury (from the local Rho corpus). Treat as adversarial.
- **[3P]** = third-party press, regulator, or review site.

---

## 0. One-paragraph orientation

Mercury is no longer meaningfully "a fintech startup bank for startups." As of 2026 it is a ~$650M-annualized-revenue, four-years-GAAP-profitable, 300,000+ customer platform that (a) received **OCC conditional approval on 2026-04-27 to charter Mercury Bank, N.A.**, (b) has shipped the most aggressive agent/AI surface of any US business banking platform (in-app agent "Command", a hosted read-only MCP server, a money-moving CLI, and **agent cards whose PAN/CVC an AI agent can self-retrieve via a Vault API**), and (c) still has **no phone support at any price tier**. Its strategic vector is vertical integration down into the bank charter and outward into payroll (Central acquisition, April 2026). Its exposed flanks versus Rho are: FDIC ceiling ($5M vs Rho's claimed $75M on savings), Treasury minimum ($250K vs $50K), no advertised business savings APY, no cash deposits, and no human on a phone line.

---

## 1. Corporate facts, scale, and segment

| Fact | Value | Date | Source |
|---|---|---|---|
| Founded | 2017, by Immad Akhund, Jason Zhang, Max Tagher | n/a | [Mercury] mercury.com/blog/annual-letter-2025 (2026-02-05) |
| Legal entity | Mercury Technologies, Inc. | n/a | [Mercury] mercury.com/treasury disclosures |
| Customers | **300,000+** businesses and individuals | 2026-02-05 annual letter; repeated 2026-05-20 | [Mercury] mercury.com/blog/annual-letter-2025, /blog/series-d-announcement |
| Customer growth | **50% YoY** in 2025 | EOY 2025 | [Mercury] annual letter |
| Transaction volume | **$248B in 2025**, up **59%** from **$156B in 2024** | EOY 2025 | [Mercury] annual letter |
| Annualized revenue | **~$650M** | as of **Sept 2025 (Q3 2025)** | [Mercury] annual letter; [3P] Banking Dive, CNBC |
| Profitability | **4 consecutive years** GAAP net income **and** EBITDA positive | stated 2026-05-20 (annual letter Feb 2026 said "three consecutive years") | [Mercury] series-d-announcement vs annual-letter-2025 |
| NPS | **73.8** vs stated banking-industry average of **34** | EOY 2025 | [Mercury] annual letter |
| Market penetration | **1 in 3 U.S. startups** use Mercury | EOY 2025 | [Mercury] annual letter |
| Segment mix | **73%** of new customers in 2025 came from **outside** AI/tech-startup category; **ecommerce = 21%** of new customers | EOY 2025 | [Mercury] annual letter |
| AI segment | onboarded **2.4x** more AI companies in 2025 vs 2024 | EOY 2025 | [Mercury] annual letter |
| Application growth | **2.5x** increase in applications Q1 2026 vs Q1 2025 (vs US Census new-business applications +18%) | Q1 2026 | [Mercury] series-d-announcement |
| Named customers | Supabase, ElevenLabs, Lovable, Linear, Phantom, Tempo; ecommerce: Bogey Bros, Cocolab, Pup Labs; services: Ways & Means, neuemotion; individual: Dwarkesh Patel | 2026-05-20 | [Mercury] series-d-announcement |

### Funding
| Round | Amount | Valuation | Lead | Date | Source |
|---|---|---|---|---|---|
| Series B | n/a | $1.6B | n/a | 2021 | [3P] TechCrunch 2025-03-26 |
| Series C | **$300M** | **$3.5B** post | **Sequoia Capital** (new); Spark, Marathon new; Coatue, CRV, a16z existing | **2025-03-26** | [3P] BusinessWire, TechCrunch |
| Series D | **$200M** | **$5.2B** | **TCV** (new); a16z, Coatue, CRV, Sapphire, Sequoia, Spark | **2026-05-20** | [Mercury] /blog/series-d-announcement; [3P] CNBC, BusinessWire |
| Total raised | ~**$700M** primary + secondary | n/a | n/a | 2026 | [3P] search-aggregated; not independently confirmed on a primary page |

Valuation growth: **+49% in 14 months** (3.5B → 5.2B). [3P] CNBC 2026-05-20.

### M&A
- **Central** (AI-native payroll/benefits/HR compliance, founded 2023, First Round + YC backed) acquired, announced **April 2026**. [3P] The Paypers; [Mercury] mercury.com/blog/mercury-acquires-centralhq
- Central pre-acquisition scale: **>$175M payroll processed**, **~500 startup customers**, of which **250+ were already Mercury customers**. [3P] The Paypers.
- Mercury describes this as "AI-native payroll: With our acquisition of Central we'll bring payroll directly to your Mercury account." [Mercury] series-d-announcement.
- **Payroll is not yet a shipped Mercury product.** Mercury's own help doc "How to set up payroll on Mercury" (updated 2026-05-01) still only describes connecting *third-party* payroll providers (Gusto, Rippling, Deel, Justworks, TriNet, ADP, Intuit, Paychex, Oyster, OnPay, Remote) via ACH debit or reverse wire. **Conspicuously not stated: a launch date or price for first-party Mercury payroll.**

---

## 2. The bank partner situation (the most changed fact since 2024)

### 2.1 Current state
[Mercury] Universal footer disclaimer on every mercury.com page:
> "Mercury is a fintech company, not an FDIC-insured bank. Banking services provided through **Choice Financial Group** and **Column N.A.**, Members FDIC."

But Mercury's own partner-banks blog names **three**:
> "We work with banks that are headquartered in the U.S. and FDIC insured, including **Choice Financial Group, Column, N.A., and Patriot Bank, N.A.**"
,  [Mercury] mercury.com/blog/how-mercury-works-with-partner-banks, authored by Immad Akhund, byline date **2025-03-11**, since edited to include April 2026 content.

**Contradiction to note:** Patriot Bank, N.A. appears in the blog and is the **IO card issuer** ("The IO Card is issued by Patriot Bank, N.A., Member FDIC, pursuant to a license from Mastercard International Incorporated": mercury.com/credit-card), but is **omitted from the deposit disclaimer**. Resolution: Patriot is a **card-issuing** partner, not a deposit partner. Deposits = Choice + Column only.

Debit card issuer disclaimers are themselves inconsistent across Mercury's own help center:
- "The Mercury Debit Cards are issued by **Choice Financial Group and Column N.A.**, Members FDIC, pursuant to licenses from Mastercard" (Contacting our Support Team article)
- "The Mercury Debit Cards are issued by **Column N.A.**, Members FDIC" (Agent cards article, updated 2026-08-21)

### 2.2 Evolve history: the facts
| Event | Date | Source |
|---|---|---|
| Evolve Bank & Trust was Mercury's long-time partner bank | pre-2025 | [Mercury] partner-banks blog |
| Synapse Financial Technologies bankruptcy; ~**$96M** in customer funds mismanaged; Evolve exposed | 2024 | [3P] Cobalt Intelligence / American Banker coverage |
| Evolve data breach (names, addresses, transaction detail leaked) | July 2024 | [3P] Cobalt Intelligence |
| **Federal Reserve enforcement action against Evolve** citing AML, risk management, and consumer compliance deficiencies; Fed alleged Evolve "fail[ed] to have in place an effective risk management framework" for fintech partnerships | **June 2024** | [3P] Banking Dive |
| **Mercury announces it is transitioning away from Evolve** | **2025-03-17** (Banking Dive) / "March 2025" (Mercury) | [3P] Banking Dive; [Mercury] partner-banks blog |
| Customers affected | "small percentage"; migrated "in batches over months" | [3P] Banking Dive |
| Destination partners | Choice Financial Group, Column N.A. | [Mercury] + [3P] |
| Mercury's framing | "we outgrew the relationship" / "giving customers the option to migrate their Mercury accounts to another partner on our platform" | [Mercury]; [3P] paraphrase |

Note the asymmetry: **Mercury frames the Evolve exit as elective; the press frames it as a de-risking move after Evolve's Fed enforcement action and the Synapse blowup.** Mercury's own page never mentions Synapse, the data breach, or the Fed action.

The word "Evolve" survives inside Mercury's own CMS as an internal label: the pricing-page FDIC disclaimer record is literally named `"Business / FDIC (sans Evolve)"` (extracted from the mercury.com/pricing RSC payload, 2026-09-11). Small but telling artifact of the migration.

### 2.3 Mercury Bank, N.A.: the charter
| Fact | Value | Source |
|---|---|---|
| Charter application filed with OCC | **2025-12-19** ("December 2025") | [3P] Banking Dive 2026; [Mercury] annual letter |
| **OCC conditional approval** | **2026-04-27** (BusinessWire release ID 20260427…; PYMNTS says Apr 27; Banking Dive says **Apr 28**): **date discrepancy of one day, unresolved** | [3P] BusinessWire, PYMNTS, Banking Dive; OCC Corporate Decision **#1372**, April 2026 |
| Elapsed time | ~4–5 months application → conditional approval | [3P] |
| HQ | **Utah** | [3P] Banking Dive |
| Proposed bank CEO/president | **Jon Auxier** (ex-SoFi, Green Dot, Goldman Sachs) | [3P] Banking Dive |
| Current status | **bank organization phase**; still needs **final OCC authorization + FDIC approval + Federal Reserve approval** | [Mercury] partner-banks blog; [3P] |
| Estimated final approval | "may be ready for final approval in **2027**" | [3P] search-aggregated; treat as soft |
| Customer impact today | **None.** "Nothing changes for customers just yet… Our partner bank structure remains fully in place in the meantime." | [Mercury] partner-banks blog |
| Capabilities unlocked by charter | **Zelle** built directly into accounts, "an expanded suite of lending products", "deeper payments infrastructure" Mercury owns | [Mercury] series-d-announcement; [3P] PYMNTS quoting Akhund: "Our customers have been asking for Zelle, for expanded lending, for payment infrastructure we actually control." |

Mercury also **joined the American Fintech Council (AFC)** to work on bank-fintech partnership regulatory clarity (date not captured precisely; AFC press release). [3P]

**Strategic read:** the charter is the single biggest structural difference forming between Mercury and every other US business-banking fintech (Rho, Brex, Ramp, Relay all remain partner-bank-only). If Mercury Bank N.A. opens, Mercury stops being "a fintech company, not an FDIC-insured bank": and every comparison built on that disclaimer, including Rho's, gets re-based.

---

## 3. Pricing plans: exact figures

Verified directly from the mercury.com/pricing React Server Components payload on 2026-09-11 (`pricePerMonth` / `annualPricePerMonth` fields plus schema.org Product JSON-LD). This resolves a persistent ambiguity: the pricing page **defaults its toggle to "Annual Pricing (15% off)"**, so a casual read of the page shows $29.90/$299, not the monthly rates.

| Plan | Billed monthly | Billed annually (per month) | JSON-LD `price` |
|---|---|---|---|
| **Mercury** (free) | **$0** | $0 | "0.00" |
| **Mercury Plus** | **$35.00/mo** | **$29.90/mo** | "35.00" |
| **Mercury Pro** | **$350.00/mo** | **$299/mo** | "350.00" |
| Custom | "Get in touch with our team for custom pricing and plan options." No published enterprise SKU. | n/a | n/a |

Annual discount is stated as 15% (35 × 0.85 = 29.75 ≈ 29.90; 350 × 0.85 = 297.50 ≈ 299).

### 3.1 What each plan includes: canonical text from Mercury's own schema.org markup
- **Mercury (free):** "Powerful banking and finance essentials included with every account."
- **Mercury Plus:** "Includes ACH debit invoicing for **$1 per transaction**, recurring invoices, **Invoicing API (500/mo)**, multiple GL codes for bill payments, **reimbursements for up to 20 users/month**, unlimited 1099 tax filings, $50 off eligible LegalZoom Compliance Plans, and 6 months free Xero."
- **Mercury Pro:** "Everything in Plus, plus a **dedicated relationship manager**, ACH debit invoicing at **$0/transaction**, **unlimited Invoicing API**, **NetSuite categorizations**, **reimbursements for up to 250 active users**, unlimited 1099 tax filings, $50 off eligible LegalZoom Compliance Plans, and 6 months free Xero."
- Free tier reimbursement cap is stated elsewhere: paid plan needed for "reimbursing out-of-pocket expenses for **more than 5 active users per month**." [Mercury] /pricing FAQ and /bank-accounts FAQ.

### 3.2 Full plan comparison matrix (decoded from the pricing page's collapsed "Compare our plans" table, 2026-09-11)

| Row | Mercury (free) | Plus | Pro |
|---|---|---|---|
| No monthly fees, overdraft penalties, or minimum balances | ✓ | ✓ | ✓ |
| Business checking and savings | ✓ | ✓ | ✓ |
| Up to $5M in FDIC insurance | ✓ | ✓ | ✓ |
| Free ACH, wires, RTP, checks in USD | ✓ | ✓ | ✓ |
| Access to Personal banking | ✓ | ✓ | ✓ |
| ACH (same-day & next-day), 0–1 business days | $0 | $0 | $0 |
| Domestic wires (same-day & next-day), 0–1 bd | $0 | $0 | $0 |
| Real-time payments (instant) | $0 | $0 | $0 |
| Checkbooks | $0 | $0 | $0 |
| Mailed checks (7–10 bd to send, 1–5 bd to receive) | $0 | $0 | $0 |
| USD international wires (1–3 bd) | $0 | $0 | $0 |
| Non-USD international wires | **1% currency exchange fee** | 1% | 1% |
| Invoicing ACH debits (receiving) | ✗ | **$1/txn** | **$0/txn** |
| Treasury: earn up to [rate] yield | ✓ | ✓ | ✓ |
| Treasury: same-day withdrawals | ✓ | ✓ | ✓ |
| Treasury: no limit on transfers | ✓ | ✓ | ✓ |
| Treasury: **no investment minimum** | ✓ | ✓ | ✓ |
| Virtual and physical debit and credit cards | ✓ | ✓ | ✓ |
| Corporate credit cards (**1.5% cashback**) | ✓ | ✓ | ✓ |
| Non-USD card transactions | **3% currency exchange fee** | 3% | 3% |
| Custom spend limits and merchant-locked cards | ✓ | ✓ | ✓ |
| Duplicate subscription detection | ✓ | ✓ | ✓ |
| All 7 expense-management rows (employee cards, receipt matching, reimbursements, multi-currency + mileage, receipt auto-populate, card-only access, custom categories) | ✓ | ✓ | ✓ |
| Create/send unlimited invoices; accept card/Apple Pay/Google Pay/wire/ACH; customers; catalog; schedule; branded | ✓ | ✓ | ✓ |
| **Send recurring invoices** | ✗ | ✓ | ✓ |
| Invoicing API | ✓ (see §7 caveat) | ✓ | ✓ |
| Bill Pay: unlimited payments, inbox, vendor onboarding, approval rules, duplicate detection, split GL codes | ✓ | ✓ | ✓ |
| Accounting: bank feed import | QBO, Xero, NetSuite | same | same |
| Accounting: **incremental enrichment** | QBO + Xero | QBO + Xero | **+ NetSuite** |
| Accounting: **automatic categorizations** | QBO + Xero | QBO + Xero | **+ NetSuite** |
| Accounting: **categorization rules** | QBO + Xero | QBO + Xero | **+ NetSuite** |
| Taxes: centralized docs, manage 1099 recipients, W-9 auto-scan, corrections, e/postal delivery | ✓ | ✓ | ✓ |
| **Federal & state filing for 1099-NEC & MISC** | **$5/filing** | unlimited ✓ | unlimited ✓ |
| Platform: Payments API, mobile app, third-party integrations (HRIS, payroll, Stripe, Slack) | ✓ | ✓ | ✓ |
| Security: roles/permissions, fraud monitoring, SOC 2, encryption, PCI, MFA | ✓ | ✓ | ✓ |
| **Support: email or contact support via your Mercury dashboard** | ✓ | ✓ | ✓ |
| **Implementation services** | ✗ | **✓** | **✗** |
| **Dedicated relationship manager** | ✗ | ✗ | ✓ |
| Partner perks and rewards | ✓ | ✓ | ✓ |
| $50 off LegalZoom Compliance Plans | ✗ | ✓ | ✓ |
| Free Xero access | 3 months | 6 months | 6 months |

**Apparent CMS error to flag:** "Implementation services" is marked ✓ on **Plus** and ✗ on **Pro**, which is almost certainly a data-entry mistake on Mercury's own page (Pro is the higher tier and is the one with the relationship manager). Do not build a claim on this row.

**Second contradiction:** the Treasury row says "**No investment minimum**" while the same page's jump-link footnote says "*Treasury is unlocked with **$250K** Mercury balance" and the FAQ says "Mercury Treasury is currently available to users with account balances over **$250,000** across all Mercury accounts." Reconciliation: there is no minimum *investment size* once you qualify, but there is a **$250K balance eligibility gate**. Mercury's phrasing invites misreading.

### 3.3 Stale pricing copy on Mercury's own site
Mercury's FAQ blocks on **/pricing**, **/bank-accounts**, and **/credit-card** all still say paid plans start at "**$35/month**": which is correct for monthly billing but inconsistent with the page's own default $29.90 display. More importantly, [Rho claim] (blog, verified 08/17/2026) lists "$0, $35/mo (Plus), $350/mo (Pro); $29.90/$299 with annual billing": **Rho's numbers are correct and match the underlying data.**

### 3.4 Mercury Personal (adjacent SKU)
- **$240/year** standalone subscription; **free with any active business plan in good standing**. [Mercury] /pricing, /personal
- **3.25% APY** on personal savings, no minimum balance, no deposit limit, interest calculated daily and paid at start of each month. **APY accurate as of 06/15/2026**, variable. [Mercury] support article 53170222904596 (updated 2026-09-02)
- Includes: 1 joint account (up to 4 owners), 1 trust account, access to "Invest" (diversified ETF portfolio at **0.1% advisory fee**), up to $5M FDIC, unlimited USD wires/ACH/RTP/checks, debit cards with **no foreign transaction fees**, **reimbursed ATM fees worldwide**.
- Break-even framing Mercury itself publishes: "With just a **$7,500** balance in your savings account, you'll earn more than $240 a year at the current APY."

---

## 4. FDIC coverage mechanics and sweep network size

| Element | Detail | Source |
|---|---|---|
| Headline coverage | **Up to $5M** in FDIC insurance | [Mercury] everywhere |
| Mechanism | Deposits held at Choice Financial Group and Column N.A.; both operate **sweep program networks** of additional FDIC-insured program banks | [Mercury] support 28776806677908 |
| **Sweep network size** | "automatically spreading your deposits across **up to 20 different banks**, without requiring you to open and manage separate bank accounts" | [Mercury] mercury.com/bank-accounts FAQ |
| Arithmetic | 20 × $250,000 = $5,000,000. Consistent. | derived |
| Program bank lists | Choice: `https://rnt.com/files/ddm/bank-list/pbl-rtncu.pdf` (Choice Sweep Bank List). Column: `https://column.com/legal/sweep-program-network-banks` | [Mercury] pricing-page disclaimer record |
| Opt-in | Mercury "gives you the choice to **opt in** to our partner bank's sweep program": i.e. sweep is not automatic/universal | [Mercury] support 28776806677908 |
| Allocation latency | "Newly deposited funds may take **up to 24 business hours** to be allocated to a program bank." | [Mercury] support 28776806677908 |
| Transparency artifact | Mercury issues **sweep statements** showing distribution across program banks, downloadable under Documents & Data → Statements → Sweep Statements. Mercury notes "sweep statements like these aren't currently required by law." | [Mercury] partner-banks blog, support 28776806677908 |
| Pass-through caveat | "Certain conditions must be satisfied for **pass-through** FDIC insurance to apply." Repeated on every page. | [Mercury] |
| Coverage above $5M | "**Eligible customers may have more coverage**, check your Mercury Vault for more information.": undefined, unquantified | [Mercury] support 28776140568212 (updated 2026-07-21) |
| Treasury is NOT FDIC | Treasury funds are **SIPC** (Apex Clearing), **$500,000** total securities+cash with a **$250,000 sublimit for cash**. Not FDIC, not bank deposits, may lose value. | [Mercury] support 28776140568212, /treasury FAQ, partner-banks blog |
| Customer↔bank privity | "each Mercury customer has a **direct contractual agreement with our partner banks** through the terms and conditions you review and accept as part of onboarding… no matter what happens to Mercury, you'll always have access to your funds." | [Mercury] partner-banks blog |

### 4.1 Partner-bank feature divergence (operationally material, rarely discussed)
From [Mercury] support 43065703960852 "Using multiple partner banks on Mercury" (updated 2026-08-21):

| Feature | Choice | Column N.A. |
|---|---|---|
| **Receiving RTP** | ❌ | ✅ |
| **Sending RTP** | ❌ | ✅ |
| **Wire drawdowns (reverse wires)** | ✅ | ❌ |
| International wires (USD and non-USD) | ✅ | ✅ (instructions differ) |
| ACH and domestic wires | ✅ | ✅ (same instructions) |
| Checkbooks and mailed checks | ✅ | ✅ |

Consequences Mercury documents:
- "Transfers between accounts at **different partner banks must be done manually**": via transfer flow (1–3 business days) or manual wire (same-day if before 2pm PT).
- "**Auto transfer rules are only supported between accounts at the same partner bank.**"
- New accounts default to whichever partner bank you most recently opened an account with.

This is a real, under-marketed cost of the multi-partner model: a Mercury customer split across Choice and Column cannot run auto-transfer rules across the split, and loses either RTP or wire drawdowns depending on which bank they sit on. **Wire drawdowns matter for payroll funding** (several payroll providers require reverse wires). That path is Choice-only, while RTP is Column-only. A customer cannot have both on one account.

### 4.2 Partner-bank switching mechanics
[Mercury] support 31577686813076 (updated 2026-09-02) documents a formal migration tool:
- Accept new partner bank T&Cs → Mercury verifies company info ("may take **up to a few weeks**") → first new account auto-opens → account transfer tool copies accounts, balances, recurring payments, issues new debit cards.
- Old accounts stay live during a **transition phase of generally 60–90 days**, then are disabled, then permanently closed "a few weeks later."
- During transition you **cannot deposit or send checks** from old accounts.
- **IO credit cards are NOT reissued** and keep working; Treasury accounts unchanged.
- ACH debits (pulls) must be manually updated by the customer with each originator.
- Transfers via the tool clear in 0–1 business days.

---

## 5. Treasury / yield product

Operator: **Mercury Advisory, LLC**, an SEC-registered investment adviser, wholly-owned subsidiary of Mercury Technologies. Brokerage/clearing/custody: **Apex Clearing Corporation** (SEC-registered broker-dealer, FINRA/SIPC member, "in business for over 40 years").

### 5.1 Eligibility
- **$250,000 available in deposits across accounts within a single Mercury org.** [Mercury] support 41673479637908 (updated 2026-09-09) and /pricing FAQ.
- U.S. entity, physically located in one of: **United States, United Kingdom, Canada, India, Singapore, Israel, Netherlands, Spain, Germany, Denmark, Australia, Mexico**.
- **Excluded entity types:** non-profits/501(c)(3), partnerships, LLPs, single-member LLCs, LLCs taxed as sole proprietorships, foreign financial institutions, foreign-law banks, beneficial-owner-exempt legal entity customers, certain registered and exempt investment advisers, securities brokers/dealers, businesses with a beneficial owner resident in restricted countries.
- Applications reviewed in **3–5 business days** typically.
- "We hope to open Mercury Treasury to all users in the future." [Mercury] /pricing FAQ.

### 5.2 Published net-yield table: **as of 09/04/2026** [Mercury] mercury.com/treasury

| Total Mercury deposits | Government MMF (**MRGXX**), same-day liquidity | Ultra-Short Bonds (**MCRYX**), 1–2 day liquidity |
|---|---|---|
| > $50M | Contact us | Contact us |
| $20M–$50M | 3.59% | **3.89%** |
| $10M–$20M | 3.49% | 3.79% |
| $5M–$10M | 3.39% | 3.69% |
| $2M–$5M | 3.29% | 3.59% |
| **$250K–$2M** | **3.14%** | **3.44%** |

Headline "up to **3.89%**" = MCRYX at $20M+ deposits, **net of fees**, "as of 09/04/2026."

### 5.3 Fee schedule: [Mercury] support 28742040300820 (updated 2026-07-15)
Fee is on **Treasury positions only**, tiered by **total Mercury deposits including Treasury**, calculated daily, charged monthly.

| Total Mercury deposits | Annual fee |
|---|---|
| > $20M | **0.15%** (15 bps) |
| $10M–$20M | 0.25% |
| $5M–$10M | 0.35% |
| $2M–$5M | 0.45% |
| $0–$2M | **0.60%** (60 bps) |

Formula published by Mercury: `Positions × fee_bps / (10,000 × 365)` = daily fee. Worked example: $1.5M invested, $2.5M total deposits → 45 bps → $18.49/day.

### 5.4 Funds, and a 2026 fund swap Mercury's marketing has not fully caught up with
[Mercury] support 49523388503828 "Treasury Mutual Fund Update: Summer 2026" (updated 2026-08-21):
- **July 2026:** Morgan Stanley **Ultra-Short Income Portfolio (MULSX) → MCRYX** ("Morgan Stanley Ultra-Short Strategy Portfolio: Mercury Class"), a **Mercury-exclusive share class** co-designed with Morgan Stanley Investment Management. Opt-out deadline was **2026-07-14**.
- **August 2026:** **J.P. Morgan U.S. Treasury Plus Money Market Fund (JTCXX) → MRGXX** ("State Street Institutional U.S. Government Money Market Fund: Mercury Class"), Mercury-exclusive, developed with State Street.
- **Expense ratios:** MRGXX net **0.14%** vs JTCXX net **0.17%**, as of 06/09/2026.
- MRGXX invests **≥99.5%** of total assets in cash, U.S. government securities, and/or repos collateralized solely by U.S. government securities or cash. Liquidity 0–1 business days; **same-day cutoff 3pm ET**.
- MCRYX: commercial paper and CDs; "carries the highest Fitch rating"; liquidity 1–2 business days but "can take up to 4 business days."
- Allocation between the two funds is adjustable in **10% increments**.
- State Street scale cited: **$6.3T AUM** (as of 2026-06-30) and **$643B** in money-market/short-term fixed income (as of 2026-02-27).

**Stale-content contradictions on Mercury's own properties (all observed 2026-09-11):**
1. The **/pricing** comparison table's Treasury footnote still says same-day withdrawals apply to the "**JPMorgan U.S. Treasury Plus Money Market Fund**": a fund Mercury moved customers out of in August 2026.
2. Support article 41674211743380 "Understanding Mercury Treasury" (updated 2026-09-03) still says funds are "managed by trusted partners like Morgan Stanley and **J.P. Morgan Asset Management**" while the same article's body correctly lists MRGXX (State Street) and MCRYX.

### 5.5 Net yield methodology: [Mercury] support 44370115553044 (updated 2026-08-21)
- MRGXX (money market fund) reported using **7-day Effective SEC yield**; MCRYX (bond fund) using **30-day effective yield**. Both are SEC-defined, industry-standard.
- Mercury refreshes each fund's yield **weekly**, weights by the customer's actual portfolio allocation, then subtracts the annualized advisory fee → displayed net yield.
- Mercury's own worked example (yields from 12/9/2025, $20M deposits): 70% MRGXX @ 3.89% + 30% MCRYX @ 4.08% = gross 3.94% − 0.15% fee = **net 3.79%**.
- Marketing footnote: "Yield and fee caps are represented as annualized numbers… seeks to earn net returns up to 3.89% annually on your idle cash for Mercury deposit sizes over $20M. **Net yield numbers as of 09/04/2026**."

### 5.6 Premium tier
**Mercury Treasury Solutions by Morgan Stanley**: personalized portfolio management, qualification at **$25M** balance across Mercury accounts, "dedicated, white-glove service from Morgan Stanley's experienced portfolio management team." **Separate, unpublished fee structure** ("contact us"). [Mercury] /treasury.

### 5.7 What Treasury does NOT cover
- Not FDIC insured; SIPC only ($500K, $250K cash sublimit).
- Withdrawal timing: MRGXX same-day if initiated by 3pm ET; MCRYX 1–2 bd, up to 4 bd.
- "Automatically transfer idle cash between accounts with customizable **twice-monthly** transfer dates" (support 41674211743380): note this is twice-monthly, not daily, for the scheduled rules; auto-transfer rules also exist separately.
- Mercury teases "**Mercury-exclusive funds and fixed income ladders. These aren't live yet.**" (support 28742040300820)

### 5.8 Business savings APY: conspicuously not stated
Mercury advertises **no APY on business checking or business savings** anywhere on mercury.com or in the help center. Searched all 326 help-center articles for "APY"/"annual percentage yield": the only hits are **Mercury Personal** (3.25%). Yield for businesses is routed entirely through Treasury (min $250K).

However Mercury **does** pay some business interest: support 32787686187924 describes 1099-INT issuance "if you earned $10 or more in interest in 2025 from your Mercury account(s)," and Command's suggested prompts include "How much interest have I earned on my savings this year?" **Rate is unpublished.** [Rho claim] states it correctly: "No standalone business savings APY advertised; yield comes through Mercury Treasury (mercury.com, as of 08/17/2026)."

---

## 6. IO credit card mechanics

Issuer: **Patriot Bank, N.A.**, Member FDIC, Mastercard license. Network tier: **standard Mastercard** (not World Elite) [Rho claim]: Mercury does not publish a network tier, so Rho's characterization is unrebutted but unconfirmed by Mercury.

| Mechanic | Detail | Source |
|---|---|---|
| Type | **Charge card**, balance due in full each period, no revolving, no interest | [Mercury] /credit-card FAQ |
| Underwriting | **Cash-underwritten**: "your IO balance **cannot exceed the cash deposits you have held in Mercury**" | [Mercury] support 28768794858772 (updated 2026-08-22) |
| Credit check | **No credit check** at signup; personal credit not considered or affected | [Mercury] /credit-card FAQ |
| Personal guarantee | **None** | [Mercury] /credit-card |
| Annual fee | **$0** | [Mercury] |
| Cashback | **Unlimited 1.5%** on all settled purchases, tallied monthly, auto-deposited. No higher tier published. | [Mercury] /credit-card, support 28768794858772 |
| Partial early payoff | Cashback credited **in proportion to the amount paid** | [Mercury] /credit-card FAQ |
| Intro limit | Daily repayment; "cash-underwritten limit, **typically up to $5,000**", refreshed **once daily around midnight** | [Mercury] support 28768794858772 / 28768861008276 |
| Intro limit mechanic | Each day the system sets your IO limit = available cash balance (cap $5,000); around midnight it deducts that day's total IO spend from checking; remainder becomes next cycle's limit. **First deposit is the exception**: limit recalculated shortly after it posts. | [Mercury] support 28768861008276 |
| **$15,000 threshold** | At **$15K total Mercury balance** (checking + savings + Treasury) you qualify for higher limits and can choose **30-day/monthly** repayment vs daily | [Mercury] support 28768794858772 |
| External balances | Plaid-linked external business accounts **may** increase limits, but "cash held in Mercury carries more weight"; include/exclude is all-or-nothing; 7-day grace to reconnect a dropped link before limit changes | [Mercury] support 28768861008276 |
| **Financial-statement underwriting** | "**Eligible customers can work with our underwriting team to determine a custom limit based on your company's full financial picture**," reevaluated **quarterly**. Apply via help@mercury.com. | [Mercury] support 28768861008276 |
| Limit review cadence | Automatic, **typically monthly**; more frequently "if there's a significant drop in your Mercury balance"; manual "Request a Limit Increase" button | [Mercury] |
| Dynamic autopay | Optional mid-cycle payment trigger at a threshold you set (e.g. 80% of limit) | [Mercury] |
| Bureau reporting | Payment history reported to **Experian, Equifax, and Dun & Bradstreet** | [Mercury] /credit-card FAQ |
| Non-USD card txn | **3% currency exchange fee**, non-refundable even if the underlying transaction is refunded | [Mercury] /pricing comparison table + /credit-card FAQ |
| Refunds | IO refunds credit back to the card as a positive credit balance; **do not auto-sweep to checking**: requires contacting Support for a manual transfer | [Mercury] support 28768794858772 |
| Metal card | Free for **admins with ≥$50,000** deposits; otherwise plastic; **$49 + shipping** to buy the metal upgrade; non-admins always plastic; standard shipping free | [Mercury] support 30066912540180 (updated 2026-09-11) |
| Spend controls | Custom daily/weekly/monthly limits, custom expiration dates, merchant-locked cards from a list of **over 1,000 merchants**, company-wide merchant/category restrictions, receipt policies with thresholds, **auto-lock cards with overdue tasks**, duplicate subscription detection, HRIS/payroll bulk issuance | [Mercury] /credit-card, /spend-management |
| Perks | Mastercard Zero Liability + fraud protection; discounts on Microsoft, Adobe | [Mercury] /credit-card |

**Important correction to the common framing:** Rho's blog says IO's limit "is a reflection of your bank balance" full stop. Mercury's own help center says that is the *default* path, and that eligible customers can move to **financial-statement underwriting with quarterly reviews**: i.e. Mercury does underwrite the business for some customers. [Rho claim] omits this. Whether that path is widely available is undisclosed.

---

## 7. Developer API

Base URLs: production `https://api.mercury.com/api/v1/`; sandbox `https://api-sandbox.mercury.com/api/v1/`; OAuth2 sandbox `https://oauth2-sandbox.mercury.com/`; card vault `https://vault-api.mercury.com/api/v1/`. Docs: `docs.mercury.com` (versions v1-pre / v1 / v2 published). Contact `api@mercury.com`.

### 7.1 Auth and token model: [Mercury] docs/getting-started (updated 2026-06-12), docs/api-token-security-policies (updated 2025-11-03)
- HTTP **Basic auth** (token as username, empty password) or `Authorization: Bearer secret-token:mercury_production_…`.
- Three token tiers:
  - **Read Only**: all data; **no IP whitelist required**.
  - **Read and Write**: can initiate transactions without admin approval, manage recipients; **IP whitelist required**.
  - **Custom**: scoped; scopes with write access require IP whitelist; `RequestSendMoney` scope lets you queue approval-gated payments **without** an IP whitelist. **Scopes cannot be edited after token creation.**
- IP whitelist supports IPv4/IPv6 singles and CIDR ranges, mixed.
- **Automatic downgrade:** tokens with higher permissions than they used in a **45-day window** are auto-downgraded; 7-day email warning to all admins.
- **Automatic deletion:** tokens unused for **45 days** are deleted; 7-day email warning.
- Token creation is permissioned (admin-level users only).
- OAuth2 web flow available for third-party integrations.

### 7.2 Coverage (from `docs.mercury.com/llms.txt`, 2026-09-11): ~70 documented operations
Accounts, statements (+ PDF download), transactions (list/get/update note+category/attachments), internal transfers (incl. depository↔treasury), recipients (CRUD, invites, tax-form attachments), send money (direct + approval-gated), send-money approval requests, treasury (accounts, transactions, statements), categories (CRUD), merchants (for merchant locking), credit accounts, organization (EIN, legal name, DBAs), users, **SAFEs** (list/get/download PDF), Accounts Receivable (customers CRUD, invoices CRUD, invoice attachments, invoice PDF), **Cards (list/create virtual/get/update/cancel/freeze/unfreeze)**, **Vault (reveal card PAN/expiry/CVC: agentic cards only)**, **Events** (auditable change stream with before/after values), **Webhooks** (CRUD + verify + auto-disable on consecutive failures + reactivate).

### 7.3 Money movement: [Mercury] docs/send-money (updated 2026-08-25)
| | `POST /account/{id}/transactions` | `POST /account/{id}/request-send-money` |
|---|---|---|
| Behavior | Submits immediately; **does not run your org's approval rules** | Always queues for dashboard approval regardless of policy |
| Auth | **Requires IP allowlist** | No IP allowlist |
| Methods | `ach`, `check`, `domesticWire` | `ach`, `check`, `domesticWire`, **`internationalWire`** (requires a `purpose`) |
| Response | `Transaction` | `SendMoneyApprovalRequestResponse` |

- **Bulk/mass payments: client-side only.** "To pay multiple recipients, cycle through your recipient list and send one payment per recipient from your own system." No batch endpoint.
- **RTP and FedNow are NOT available as API send methods.** ("Not Available Today")
- Approval requests emit **no webhook**; you must poll `GET /request-send-money/{requestId}`. Only once approved does it become a transaction with `transaction.created` / `transaction.updated` events.
- Transaction statuses referenced: `sent`, `failed`, `reversed`, `blocked`, `pendingApproval`.

### 7.4 API commercial terms
- "**100 free ACH transfers per month** included with every account." [Mercury] mercury.com/api
- "making **mass payments on our API**" is listed among features that "may incur fees" [Mercury] /pricing FAQ: **the mass-payment fee schedule is conspicuously not published anywhere on mercury.com or in the help center.**
- Invoicing API: "**Create up to 500 invoices/month on Mercury Plus, or unlimited invoices with Pro**" [Mercury] /api, but the /pricing comparison table marks "Invoicing API (send unlimited invoices/month programmatically)" ✓ on **all three tiers including free**. **Direct contradiction between mercury.com/api and mercury.com/pricing.** The schema.org data sides with /api (Plus = "Invoicing API (500/mo)", Pro = "unlimited Invoicing API").
- Security posture: "SOC 2 Type II compliant infrastructure", scoped tokens, IP allow-listing, read/write separation.

### 7.5 Ecosystem
- **n8n community node** launched (changelog entry).
- Recipes published for: bulk receipt upload, bulk tax-doc upload, recipient creation/invite, invoicing, payment approval request, account retrieval, ACH send.
- Changelog velocity in the recent window: Vault API (agent card credentials), credit statement endpoint changes, Cards API, Categories CRUD, checks + domestic wires added to Send Money API, n8n node, Treasury statements, SAFE API, account-balance webhook events, attachment uploads.

---

## 8. MCP and the agent surface (Mercury's clearest lead)

Mercury ships **four distinct agent/AI surfaces**. This is the most differentiated part of the product versus every named competitor.

### 8.1 Mercury MCP (hosted, read-only): **Beta**
- Server URL: **`https://mcp.mercury.com/mcp`**, streamable HTTP, **OAuth**. [Mercury] docs/connecting-mercury-mcp (updated 2026-07-27)
- "Mercury then issues that tool a **read-only token**, for the account you signed in to."
- Explicitly supported clients with documented one-liners: **Claude** (claude.ai custom connector), **ChatGPT** (Apps & Connectors), **Claude Code** (`claude mcp add --transport http -s user mercury https://mcp.mercury.com/mcp` then `claude mcp login mercury`), **Codex CLI** (`codex mcp add mercury --url …`), Google AI Studio, plus generic "other MCP clients" via protected-resource metadata.
- Beta warning Mercury itself publishes: "The Mercury MCP is currently in Beta as we understand the limitations of chat models. **Double check any responses from the LLM** with your Mercury account for any important decisions."
- **31 documented tools** (docs/supported-tools-on-mercury-mcp, updated 2026-07-27), all read: `getAccount`, `getAccountCards`, `getAccountStatements`, `getTransaction`, `getAccounts`, `listCategories`, `listCredit`, `getOrganization`, `getRecipient`, `getRecipients`, `listTransactions`, `getTreasury`, `getTreasuryTransactions`, `getCard`, `listCards`, `getUser`, `getUsers`, `getWebhook`, `getWebhooks`, `getTransactionById`, `getTreasuryStatements`, `listSendMoneyApprovalRequests`, `getSafeRequest`, `getSafeRequests`, `listRecipientsAttachments`, `getAttachment`, `getCustomer`, `listCustomers`, `getInvoice`, `listInvoices`, `listInvoiceAttachments`.
- `listTransactions` "automatically handles pagination for complete results": designed for agent ergonomics.
- Positioning: "Read-only access ensures your AI can analyze data without moving money." [Mercury] /api

### 8.2 Mercury CLI (terminal-native, **can move money**)
- Repo: **github.com/MercuryTechnologies/mercury-cli**, **Apache-2.0**, ~172 stars (observed 2026-09-11). [3P] GitHub
- Install: `curl -sSf https://cli.mercury.com/install.sh | sh`, `go install github.com/MercuryTechnologies/mercury-cli/cmd/mercury@latest` (Go 1.22+), or Nix. Mercury's help center also says "Once in Claude code, type `mercury-cli`. Claude code should pick up the package from Homebrew."
- Capabilities per Mercury: "Write actions such as **making payments**, categorizing transactions, creating invoices, and uploading receipts"; "Human-readable output, structured for piping, scripting, and **LLM consumption**"; runs "from your terminal, a script, or a CI pipeline." [Mercury] /api
- Documented agent-card commands: `mercury cards list --user-id`, `mercury cards reveal --card-id <card-uuid>`. [Mercury] support 51299754284948
- **Asymmetry worth naming:** the MCP is read-only, but the CLI is read-write. An agent with shell access effectively has money-movement capability that the MCP deliberately withholds.

### 8.3 Agent cards + Vault API: [Mercury] support 51299754284948 (updated 2026-08-21)
The sharpest product in this space from any US business bank as of 2026-09-11.

- An **agent card** is a Mercury **virtual** card (debit **or** credit) explicitly designated for an AI agent.
- The agent can **self-retrieve PAN, expiration, and CVC** via API or CLI:
  `GET https://vault-api.mercury.com/api/v1/cards/{cardId}/reveal` with `Authorization: Bearer $MERCURY_TOKEN` → `{"cardNumber":"…","expiration":{"month":7,"year":2031},"cvc":"234"}`
- Hard-coded, non-disableable guardrails, stated as a capability matrix:

| Agent via API/CLI | Normal virtual cards | **Agent** virtual cards |
|---|---|---|
| Create cards | ✅ allowed | 🔴 blocked |
| Update cards (spend limits, nickname) | ✅ allowed | 🔴 blocked |
| Retrieve PAN/expiry/CVC | 🔴 blocked | ✅ allowed |
| Retrieve other card info | ✅ | ✅ |

- **Only humans can create agent cards** (web/mobile app). Agents cannot raise their own limits, unfreeze their own cards, or reach cards they weren't handed. Per-card daily/weekly/monthly limits. Card isolation is enforced.
- Credentials are stored "in a **secure third-party vault**. Mercury never stores raw card numbers or codes." IP-restrictable.
- **Liability language is unusually blunt and is a real commercial risk transfer:**
  > "You acknowledge and agree that you bear **sole responsibility for all agent card transactions, which will be deemed authorized by you regardless of whether the agent acted within the scope of authority** you or the company intended."
- Standard dispute rights preserved; genuine third-party theft follows normal fraud process.
- Governed by the Mercury IO Charge Card Agreement, **Column Commercial Debit Card Agreement**, and Terms of Use.
- Mercury explicitly does not build or vet the agent: "much like it doesn't manage the web browser you use."
- Once credentials leave: "those details move from Mercury into wherever your agent runs, **including the AI platform you're using**… After that, how they're stored and used is in the hands of your agent and your AI provider."
- Mercury logs "certain records of the API and CLI requests used to reveal credentials."
- Marketing artifact: mercury.com/spend-management embeds a verbatim Claude-Code-style agent transcript placing a $100 ad purchase with an agent card on 7/21/2026, 11:55 PM.

### 8.4 Mercury Command (in-app AI operator, **can act**)
- [Mercury] support 50304715308948 (updated 2026-09-02), mercury.com/command
- Available to **all Mercury business and personal customers at no additional cost**; no plan gate found.
- Conversational surface in the dashboard (bottom-left on web; the `>_` icon bottom-right/top-right per the support article: **the two Mercury pages disagree on its location**).
- Can: query balances/transactions/statements; **send payments**; freeze cards; categorize transactions (incl. bulk GL code assignment); create/send invoices; create accounts, recipients, customers, catalog items, departments; set approval thresholds; enable dual approval and separation of duties; set spending limits; view card details; approve transactions in bulk; mark transactions ready to sync; **rebalance treasury funds**; generate a bank letter; run a security checkup; create auto-transfer rules; invite users and issue cards.
- **Every action is staged and requires explicit human confirmation**, and is modifiable before approval. "Command can only perform actions that are already available to you in Mercury. It does not have elevated permissions."
- Privacy: "Sensitive personal and account information, including **card numbers, SSNs, dates of birth, and home addresses**, is never sent to the underlying AI model." Less-sensitive items (recipient names, balances, user emails) are passed as **internal reference IDs** and hydrated only in Mercury's UI. "Powered by third-party AI providers… your conversations are **never used to train their models**."
- **Command is also the support entry point**: "Reach support: escalate any conversation and get routed to a real person on our support team without leaving the chat." (See §9.)
- Shipping history: announced as forthcoming "later this year" in the 2026-05-20 Series D post; live by 2026-09.

### 8.5 Mercury Insights
- Interactive financial dashboard with AI-driven trend detection, ad-hoc Q&A, real-time notifications/recaps. **Included in all plans at no additional cost.** Available to "Mercury users who have access to all accounts" and to Personal users. First shipped 2025 as "our first in-product AI tool." [Mercury] /insights

---

## 9. Support model: the single clearest structural weakness

**There is no phone support at Mercury, at any tier, for any customer.** This is confirmed on Mercury's own properties, not merely asserted by Rho.

Evidence:
1. **mercury.com/contact** offers exactly four paths, none of them a phone number: "New to Mercury? → **Email us**"; "Have an account? → **Log in to message our support team**"; "Want to partner? → Reach out"; "Media inquiry? → Email us." No phone number appears anywhere on the page.
2. **support.mercury.com article 31501481890708 "Contacting our Support Team"** (updated 2026-09-11):
   > "The fastest way to get help is by messaging us directly from your dashboard… **Open Mercury Command** by clicking the `>_` icon… We're available **24/7 and typically respond within 5 minutes**, any time of day."
   > "If you don't have an account or can't login: You can email us at **help@mercury.com**."
   No phone option listed.
3. **mercury.com/pricing "Support and services" section** lists exactly three rows: "Email or contact support via your Mercury dashboard" (all tiers), "Implementation services", "Dedicated relationship manager" (Pro). **No phone row exists.**
4. Other addresses in use: `hello@mercury.com` (eligibility/country questions), `personal@mercury.com` (Personal account closure), `api@mercury.com` (API/MCP feedback), `receipts@mercury.com` and `reimbursements@mercury.com` (ingestion).

**Important nuance, now that Command is the front door:** Mercury has routed first-line support *through its AI agent*. A customer in distress now types into Command and relies on it to "escalate directly to our support team." Mercury does not publish an SLA for that escalation, only the 5-minute first-response figure for the chat itself. This is a defensible design at Mercury's cost structure and a genuine risk at the moment a six-figure wire goes wrong.

**Other support facts:**
- **Status page** exists, segmented by account access, money movement, cards, and support, with subscribable updates. Mercury warns "Not every issue will appear on the status page."
- **Dedicated relationship manager** is Mercury Pro only ($350/mo, or $299/mo annually). [Rho claim] adds "or with a **$10M+ balance**": **this $10M threshold does not appear anywhere on Mercury's own pages or in the help center; treat as unverified.**
- Pro also gets 1:1 advisors on Venture Debt ("a capital advisor and relationship manager") and Working Capital ("your ecom specialist").
- Temporary payment-limit increase requests: admin-only, submitted in-dashboard with documentation, reviewed in **1–2 business days**.

**Rho's claim is accurate:** "No phone support option appears on Mercury's pricing page; support is advertised as 24/7 online with a 5-minute typical response (mercury.com, as of 08/17/2026)." Verified independently on 2026-09-11.

---

## 10. Full product lineup (2026-09-11)

**Banking & More:** Business Checking & Savings · Working Capital Loans · Venture Debt · Treasury by Mercury Advisory
**Cards & Spend:** Business Credit Cards (IO) · Spend Management (budgets, agent cards, reimbursements, departments, auto-locking)
**Payments & Invoicing:** Payments (ACH, domestic wire, RTP, check, USD intl wire, non-USD intl wire) · Invoicing · Bill Pay · Accounting Integrations (QBO, Xero, NetSuite)
**Intelligence:** Command · Insights · API (+ CLI + MCP)
**Personal:** Mercury Personal (incl. Invest)
**Adjacent:** SAFEs (create/manage in-product, plus a free SAFE generator), 1099 filing, business formation resources, Startup/Growth/Ecommerce perk bundles, Investor Database, Burn Rate Calculator
**Announced, not shipped:** first-party payroll (Central), Zelle (charter-gated), expanded lending (charter-gated), fixed-income ladders in Treasury

### Payments detail
| Rail | Price | Timing |
|---|---|---|
| ACH out | $0 | 0–1 bd; **same-day if sent before 12pm PT and < $1,000,000**, else next-day |
| ACH in | $0 | 0–2 bd, posts ~9–11am PT; Plaid-linked → 3 bd, posts ~3pm PT |
| Domestic wire out | $0 | **Cutoff 1:30pm PT**; same-day delivery if before cutoff |
| RTP | $0 | seconds, 24/7/365: **Column N.A. accounts only** |
| Checkbooks | $0, **up to 6 complimentary/year** | n/a |
| Mailed checks | $0 | 7–10 bd to send, 1–5 bd to receive |
| USD international wire | **$0** (SHA) or **$15 flat** (OUR, so Mercury absorbs intermediary fees) | 1–3 bd |
| Non-USD international wire | **1% currency exchange fee**; "40+ local currencies"; ">$200K exchanging? reach out to us to chat about fees" | varies |
| Non-USD card transaction | **3%** currency exchange fee | n/a |
| Invoicing ACH debit received | $1/txn (Plus), $0/txn (Pro), unavailable on free | 1–5 bd |
| Invoice card payment | Stripe fee, "typically **2.9% + $0.30**" | n/a |
| Cash deposits | **Not supported** | n/a |
| Wire drawdowns / reverse wires | supported: **Choice accounts only** | n/a |
| Federal & state 1099-NEC/MISC filing | **$5/filing** on free tier; unlimited on Plus/Pro | n/a |
| Domestic/international wire recall | **not published** | n/a |

### Lending
| Product | Terms | Source |
|---|---|---|
| **Venture Debt** | Interest-only period **up to 18 months**; total loan term **up to 48 months**; origination fee + interest + **a small warrant on common stock**; **no prepayment penalty, no back-end fees, no final payment fees**; for U.S.-incorporated companies that raised VC within the past 12 months or plan to soon | [Mercury] /venture-debt |
| **Working Capital** | Ecommerce only; **≥$250K annual sales**, **≥6 months trading history**, U.S.-incorporated; flat-fee pricing, **fixed weekly repayment**; no personal guarantee; no prepayment fees; app ~10 min, underwriting response **2–3 business days**, dashboard access **1–2 business days** post-signature | [Mercury] /working-capital-loans |
| Both | Originated by **Mercury Lending, LLC (NMLS 2606284)**, serviced by **Mercury Servicing, LLC (NMLS 2606285)**, wholly-owned separately-managed subsidiaries. **Not available to businesses operating in California.** | [Mercury] |

### Eligibility and exclusions
- Must be formed/registered in the U.S. or a U.S. territory, have existing or planned U.S. operations, and a U.S. or international principal-place-of-business address: **not** a registered agent, P.O. box, or UPS box.
- Founders/financial controllers resident in listed prohibited countries are excluded.
- **Cannot open accounts for trusts** (business side).
- Will not accept: money services businesses, adult entertainment, cannabis, internet gambling. "Our product might not be the best fit for businesses frequently dealing with physical cash."
- Multiple businesses manageable under one login.
- Non-U.S.-resident founders explicitly supported for U.S. entities.

### Security/compliance
SOC 2 (Type II claimed on /api), PCI compliance, MFA enforced by default, passkeys/security keys, multi-device auth, backup codes, dark-web monitoring, 3D Secure, ACH authorization allow-listing with per-vendor transaction limits and admin review (with **auto-approve on timeout**: a notable default), dual admin approvals, separation of duties, custom roles.

---

## 11. Known negatives, risks, and what Mercury does not say

1. **No phone support, at any price.** (§9)
2. **No cash deposits.** Structural exclusion of cash-handling businesses.
3. **Business savings pays no advertised APY.** Yield requires $250K and an investment product.
4. **$5M FDIC ceiling** via ~20 sweep banks, an order of magnitude below what deposit-network-based competitors advertise.
5. **Treasury is a security, not a deposit**: SIPC $500K/$250K-cash only, and the fee is charged regardless of performance.
6. **Partner-bank fragmentation** breaks auto-transfer rules and forces an RTP-vs-wire-drawdown choice (§4.1).
7. **Charter execution risk.** Conditional approval is not a charter. FDIC and Fed approvals are still outstanding; final OCC authorization pending; press estimates 2027.
8. **Agent-card liability is fully assigned to the customer**, including out-of-scope agent behavior (§8.3).
9. **Account closures / risk-based offboarding.** [3P] There are documented June 2026 cases of permanent account restriction under a generic "Violation of Terms of Service" with no reason given; Mercury's own article 43095394066452 "Understanding account closures and access restrictions" confirms closures can be risk-based. BBB complaints exist. Mercury notes it "may not always be able to share specific reasons due to legal or compliance constraints."
10. **California lending exclusion** for both Venture Debt and Working Capital.
11. **Historical regulatory footnote:** California DFPI enforcement action / settlement agreement with **Mercury Technologies, Inc. executed 2022-01-03** [3P] dfpi.ca.gov. Underlying conduct and penalty not disclosed on the DFPI summary page; **not resolved by this research.**
12. **Mass-payment API fee is unpublished** despite being named as a chargeable feature.
13. **No published API rate limits** anywhere in docs.mercury.com or llms.txt.
14. **Mercury's own site contradicts itself** on: Invoicing API limits (free tier), the Treasury MMF identity (JPMorgan vs State Street), "Implementation services" tiering, Command's UI location, and debit card issuer identity.
15. **Not stated anywhere:** number of employees; churn/retention; deposit balances held; interchange economics; the business savings interest rate; SLA for human escalation from Command; whether Command's AI provider is Anthropic, OpenAI, or both; whether any Mercury plan will change once Mercury Bank N.A. opens.

---

## 12. HEAD TO HEAD: Mercury vs Rho

Rho facts below come from the local Rho corpus (Rho's own pages, so they are **[Rho claim]** unless independently checked). Mercury facts are as cited above.

### 12.1 Master comparison

| Dimension | **Mercury** | **Rho** | Edge |
|---|---|---|---|
| Legal status | Fintech, not a bank. **OCC conditional approval 2026-04-27 for Mercury Bank, N.A.**; FDIC + Fed approvals pending | Fintech, not a bank. No charter application disclosed | **Mercury**, decisively, if the charter lands |
| Deposit bank(s) | Choice Financial Group + Column N.A. (+ Patriot for IO card issuance) | Webster Bank, a division of **Santander Bank, N.A.** (checking + cards); **American Deposit Management Co.** and partner banks (savings) | Rho: fewer moving parts on checking; Mercury: dual-rail redundancy |
| Bank scale claim | not published | "$76B in assets" (Rho /claude-code) and "$327B-asset U.S. banking organization: per Santander, 8/20/2026" (Rho blog): **Rho cites two different asset figures for its own partner on different pages** | neither |
| **FDIC coverage** | **Up to $5M** via ~**20** sweep program banks | Checking **$250K standard**; **Savings up to $75M per depositor** via ADM and **"a network of 400+ insured institutions"** | **Rho** on ceiling; note Rho's checking is only $250K |
| Monthly software fee | **$0 / $35 / $350** (annual: $0 / $29.90 / $299) | **$0. No paid tiers.** | **Rho** |
| Per-user fee | $0 | $0 | tie |
| Business savings APY | **none advertised** | **1.00% APY** (variable, as of 08/17/2026), **requires $25,000 average monthly balance**; withdrawals to checking settle within 2 bd | **Rho** for balances $25K–$250K |
| **Treasury minimum** | **$250,000** across Mercury accounts | **$50,000** | **Rho** (5x lower gate) |
| Treasury fee tiers | 0.60% <$2M · 0.45% $2–5M · 0.35% $5–10M · 0.25% $10–20M · **0.15% >$20M** | 0.60% <$2M · 0.45% $2–5M · 0.35% $5–10M · 0.25% $10–20M · **0.15% ≥$20M** | **identical schedules: full parity** |
| Treasury headline net yield | **up to 3.89%** (MCRYX, $20M+, as of **09/04/2026**); $250K–$2M tier = **3.14%/3.44%** | **up to 4.66%** ($20M+ tier, net of 0.15%, as of **09/11/2026**); "sought net yield based on **90-day Treasury Bill** rates" | **Rho on paper: but see §12.3** |
| Treasury instruments | Two Mercury-exclusive mutual fund share classes: **MRGXX** (State Street govt MMF) and **MCRYX** (Morgan Stanley ultra-short); 10% allocation increments | **T-Bills, Vanguard VFSTX, Morgan Stanley MULSX**, auto-rebalanced | different design: Mercury = share-class exclusivity; Rho = direct bills + off-the-shelf funds |
| Treasury custodian | Apex Clearing (SIPC $500K/$250K cash) | Apex Clearing **and Interactive Brokers** (FINRA/SIPC) | Rho, marginally (dual custodian) |
| Treasury premium tier | **Morgan Stanley white-glove at $25M** | not published | **Mercury** |
| Card type | IO charge card, Mastercard **standard tier** [Rho claim] | Rho Corporate Card, Mastercard **World Elite for Business** | **Rho** on benefits |
| Card cashback | **flat 1.5%**, no higher tier | **1.25%** standard Daily Terms; **2.0% with Rho Platinum**; Monthly Terms 1.0% std / 1.75% Platinum; Platinum capped at **$1M eligible annual spend** | **Rho** if you qualify for Platinum; **Mercury** on the default path (1.5% > 1.25%) |
| Platinum qualification | n/a | payroll run from Rho + revenue deposited via Rho Checking + **50%+ of company assets at Rho** + open Rho Card. No fee, no application. | Rho's 2% is a deposit-concentration bounty, not a rate card |
| Card underwriting | **Cash-underwritten** by default (balance cap), **plus optional financial-statement underwriting with quarterly review for eligible customers** | Underwritten to the business (revenue, cash flow, financial profile) | **Rho**, but Rho's public framing overstates the gap |
| Repayment | Daily by default; **30-day/monthly unlocked at $15K balance** | Choice of **Daily Terms** (higher cashback) or **Monthly Terms** from the start | **Rho** |
| Personal guarantee / annual fee | none / none | none / none | tie |
| Metal card | admins with **$50K** deposits, else **$49 + shipping** | not published | n/a |
| Card perks | Mastercard Zero Liability, Microsoft + Adobe discounts | Priority Pass lounge (**live 2026-09-01**), primary car rental insurance, 24/7 concierge, ID theft protection | **Rho** |
| **Support** | **24/7 chat + email. NO PHONE, any tier.** Relationship manager = Pro ($350/mo) | **24/7 phone + in-app chat on every account, free**; **1 (855) 7-GETRHO**; claimed typical response "under a minute" | **Rho**, unambiguously |
| **API: read** | REST: accounts, transactions, statements, recipients, treasury, cards, invoices, SAFEs, users, events, webhooks (~70 ops) | **Read-only REST: accounts, transactions, statements** | **Mercury**, by a wide margin |
| **API: write** | **Yes.** Send ACH/check/domestic wire directly; international wire via approval queue; internal transfers; create/freeze/cancel cards; CRUD recipients, customers, invoices, categories; upload attachments | **"No, by design. Tokens are read-only and cannot initiate payments or modify accounts. The Rho API is read-only today."** | **Mercury**, decisively |
| Webhooks / events | **Yes**: webhook CRUD + verify, auditable event stream with before/after values | not published | **Mercury** |
| Sandbox | **Yes**: sandbox.mercury.com signup, api-sandbox.mercury.com, pre-loaded dummy data, "swap one URL for production" | not published | **Mercury** |
| **MCP** | Hosted `mcp.mercury.com/mcp`, OAuth, **read-only, 31 tools**, Beta; documented for Claude, ChatGPT, Claude Code, Codex CLI, Google AI Studio | Native Claude connection **listed in Anthropic's MCP connector directory**, read-only, plus an MCP guide in docs.rho.co | **Mercury** on depth (31 tools, multi-client); **Rho** on directory placement |
| **CLI** | **Yes**: Apache-2.0, `cli.mercury.com/install.sh`, Go/Nix, **write-capable incl. payments** | none published | **Mercury** |
| **Agent cards** | **Yes**: virtual debit/credit designated for agents; agent self-retrieves PAN/expiry/CVC via Vault API/CLI; agents cannot create cards or raise limits; per-card limits; full customer liability | none published | **Mercury**, uniquely |
| In-app AI operator | **Command**: free on all plans, staged-and-confirmed write actions across the whole product, escalates to human support | not published as a comparable surface | **Mercury** |
| AI analytics | **Insights**: free on all plans | Rho Close (month-end close), AI invoice scanning in Bill Pay | roughly comparable framing |
| Bill pay / AP | Free, unlimited, all tiers; inbox, vendor onboarding, approval rules, duplicate detection, split GL | Free AP automation with accounting sync | tie |
| Expense management | Free, all tiers; budgets, policies, reimbursements (5 users free / 20 Plus / 250 Pro) | Free, no user or platform fees | **Rho** (no reimbursement user cap published) |
| Accounting integrations | QBO + Xero free; **NetSuite enrichment/categorization/rules gated to Pro ($350/mo)**; NetSuite bank-feed import free on all tiers | **NetSuite, QuickBooks, Sage Intacct included** free | **Rho** |
| Invoicing | Unlimited + branded + scheduled + catalog on free; **recurring invoices gated to Plus**; ACH debit $1 (Plus) / $0 (Pro); Invoicing API 500/mo (Plus) / unlimited (Pro) | Invoicing included | **Rho** on gating |
| Incorporation | none first-party | **Free Delaware C-Corp, filed in ~24 hours**, $400 min deposit to open the account | **Rho** |
| Payroll | acquired Central (Apr 2026), **not shipped**; third-party integrations today | not published as first-party | **Mercury** directionally |
| Lending | Venture Debt (≤18mo IO, ≤48mo total, warrant, no prepay penalty) + ecommerce Working Capital ($250K sales min); **not in California** | **Rho Capital** ("funds land in your Rho account"); terms not in corpus | **Mercury** on published specificity |
| International | Free USD intl wires (SHA) or $15 OUR; **1%** FX on 40+ currencies | 1% foreign currency transfer; **$15 optional SWIFT fee**; **$30 international wire recall fee**; via **Wise US Inc.** | near-tie; Rho discloses recall fees, Mercury does not |
| SAFEs | create/manage in-product + API; free SAFE generator | Free SAFE Note Generator | tie |
| Cash deposits | **No** | **No** | tie (both lose to Bluevine/traditional) |
| Customers | **300,000+** | **8,000+ businesses** | **Mercury**, ~37x |
| Revenue | ~**$650M** annualized (Q3 2025) | not published | **Mercury** |
| Valuation | **$5.2B** (2026-05-20) | not published | **Mercury** |
| Profitability | **4 consecutive years GAAP + EBITDA** | not published | **Mercury** |

### 12.2 Where each genuinely wins

**Mercury wins on:**
1. **Programmability.** Rho's API cannot move money, by its own published design. Mercury's can, with a mature two-path model (IP-allowlisted direct send vs approval-gated queue), webhooks, an event stream with before/after values, and a sandbox. For any customer whose finance stack is code, this is not close.
2. **Agent readiness.** Agent cards with a Vault reveal endpoint, a write-capable CLI, a 31-tool hosted MCP, and an in-app agent that stages real actions. Rho has a read-only Claude connector. In 2026 this is the fastest-moving axis in the category and Mercury owns it.
3. **Scale and durability.** 300K customers, $248B volume, $650M revenue, four profitable years, $5.2B valuation, and a national bank charter in flight. Rho publishes 8,000+ businesses and no financials.
4. **Free-tier depth.** Bill pay, expense management, unlimited invoicing, Treasury access (once you clear $250K), Command, Insights, API, MCP, and CLI are all free at $0/mo. Rho's $0 is genuinely $0 too, but Mercury's free tier is unusually complete for a plan with paid tiers above it.
5. **Treasury premium path.** Morgan Stanley white-glove at $25M has no Rho analogue in the corpus.
6. **Published lending terms.** Mercury discloses venture debt structure (IO period, term, warrant, no prepayment penalty) and working-capital eligibility. Rho's Capital page does not.

**Rho wins on:**
1. **Phone support.** Mercury has none. This is the cleanest, most defensible Rho attack and it survives verification.
2. **FDIC ceiling on savings.** $75M via 400+ institutions vs $5M via ~20. (Caveat: Rho's *checking* is $250K, Mercury's checking is swept to $5M: so for an operating balance between $250K and $5M, **Mercury's checking is better covered than Rho's checking**. The comparison is only lopsided once money is in Rho Savings.)
3. **Treasury minimum.** $50K vs $250K. The $50K–$250K band is a Rho-only market.
4. **Business savings yield.** 1.00% at $25K average balance vs Mercury's nothing.
5. **No paid tiers.** Recurring invoicing, NetSuite automation, and >5-user reimbursements are all free at Rho and cost $35–$350/mo at Mercury.
6. **Card benefits and 2% ceiling.** World Elite on every card; 2% Platinum vs Mercury's flat 1.5% ceiling.
7. **Sage Intacct.** Mercury supports QBO, Xero, NetSuite only.
8. **Free incorporation.**

### 12.3 The treasury-yield discrepancy: handle carefully

Rho advertises **4.66%** net at $20M+ (as of 09/11/2026, "sought net yield based on 90-day Treasury Bill rates"). Mercury advertises **3.89%** net at $20–50M (as of 09/04/2026, MCRYX 30-day effective SEC yield minus fee) and **3.59%** for MRGXX at the same tier.

The fee schedules are **identical** (0.15%–0.60%, same breakpoints). So the ~77–107 bps gap is entirely a **gross-yield and methodology** difference:
- Gross implied: Rho ≈ 4.81% (90-day T-bill); Mercury ≈ 4.04% (MCRYX) and 3.74% (MRGXX).
- A ~80–100 bps spread between a 90-day T-bill and a government MMF / ultra-short bond fund is not normal in a stable rate environment. Either (a) the curve moved sharply between 09/04 and 09/11, (b) Rho's "sought net yield" is a forward-looking target on a specific instrument at a specific purchase moment rather than a realized fund yield, or (c) the two are not measuring comparable things, which Rho's own footnote hints at: "The amount of Treasury Bills available at a particular yield will depend upon the sellers' offer size; any remaining cash balance after the purchase may not earn the same yield."
- **Do not present 4.66% vs 3.89% as an apples-to-apples yield advantage without flagging methodology.** Mercury reports SEC-standard fund yields; Rho reports a sought net yield on directly-purchased bills.

### 12.4 Rho's claims about Mercury: verification scorecard

| Rho claim | Verdict |
|---|---|
| Mercury pricing $0 / $35 / $350 ($29.90 / $299 annual) | **Confirmed** exactly against mercury.com/pricing RSC + JSON-LD |
| Mercury Treasury $250K minimum, 0.15%–0.60% monthly fee | **Confirmed** (fee is calculated daily, charged monthly, on Treasury positions only) |
| "No phone support option appears on Mercury's pricing page; support is 24/7 online with 5-minute typical response" | **Confirmed** on /pricing, /contact, and support article 31501481890708 |
| Up to $5M FDIC via Choice + Column and their sweep networks | **Confirmed**; sweep size is **up to 20 banks** per Mercury |
| IO is a charge card, 1.5% flat, no annual fee, no PG, no credit check | **Confirmed** |
| 30-day repayment requires $15,000+ at Mercury | **Confirmed** |
| Metal IO card requires $50,000 in deposits (per mercury.com as of 08/02/2026) | **Confirmed**: and Rho omits that it can be **bought for $49** |
| "IO's credit limit is a reflection of your bank balance" / "Rho underwrites the business, Mercury doesn't" | **Materially incomplete.** Mercury's help center documents optional **financial-statement underwriting with quarterly reviews** for eligible customers |
| Recurring invoicing requires Plus; NetSuite categorizations require Pro | **Confirmed** |
| Reimbursing >5 active users/month requires a paid plan | **Confirmed** |
| Bill pay included free on all tiers | **Confirmed** |
| "No standalone business savings APY advertised" | **Confirmed** |
| "Dedicated relationship managers start at Mercury Pro… **or with a $10M+ balance**" | **$10M threshold NOT verifiable** on any Mercury property. Unsupported |
| "Mercury does not offer first-party incorporation" | **Confirmed** |
| Mercury = "Best free option for pre-seed founders" | Rho concedes this in its own five-way matrix; consistent with the evidence |
| Rho's matrix omits Mercury's API write capability, CLI, agent cards, Command, MCP tool count, the OCC charter, payroll/Central, Venture Debt, and Working Capital | **Material omissions.** Rho's Mercury profile is a 2024-era picture of the product |

### 12.5 The strategic read for Rho

1. **The phone-support attack is real and will keep working**: until Mercury opens a bank and staffs a call center, which a charter makes both possible and eventually expected.
2. **The "Mercury is just a free checking account with tiers" attack is decaying fast.** Mercury's 2026 additions (Command, MCP, CLI, agent cards, Central payroll, the charter) are not in Rho's published comparison at all. Rho's versus page was last verified 08/17/2026 and is already behind.
3. **Rho's API is its biggest exposed flank.** "Read-only by design" is a security posture Rho markets as a feature. Against a competitor whose agent can issue itself card credentials and initiate wires, "we can't move money" reads less like safety and more like absence. Rho's own comparison table on /product/api is the only place it names Mercury's "Native MCP server, read-only for AI tools": it does not mention Mercury's write API, CLI, or agent cards, which is the actual gap.
4. **The FDIC and Treasury-minimum wins are durable and quantitative.** $75M vs $5M, and $50K vs $250K, are the two hardest numbers Rho owns. They do not depend on Mercury standing still.
5. **The charter is the event to monitor.** If Mercury Bank, N.A. receives final OCC authorization plus FDIC and Fed approvals, Mercury stops needing the "fintech, not a bank" disclaimer, gains Zelle and direct payment rails, and can plausibly restructure deposit insurance and lending. Every Rho-vs-Mercury artifact will need re-basing at that moment.

---

## 13. Source URLs (all accessed 2026-09-11 unless noted)

**Mercury first-party**
- https://mercury.com/pricing (plans, fee matrix, FAQ, JSON-LD)
- https://mercury.com/treasury (yield table as of 09/04/2026, eligibility, fees, funds)
- https://mercury.com/credit-card (IO)
- https://mercury.com/bank-accounts (sweep = "up to 20 different banks")
- https://mercury.com/command
- https://mercury.com/insights
- https://mercury.com/api (100 free ACH/mo, 500 invoices/mo Plus, MCP/CLI positioning)
- https://mercury.com/spend-management (agent cards, budgets)
- https://mercury.com/personal (3.25% APY, $240/yr, 0.1% Invest fee)
- https://mercury.com/venture-debt
- https://mercury.com/working-capital-loans
- https://mercury.com/contact (no phone number)
- https://mercury.com/blog/how-mercury-works-with-partner-banks (Immad Akhund, 2025-03-11, updated with Apr 2026 charter section)
- https://mercury.com/blog/series-d-announcement (2026-05-20)
- https://mercury.com/blog/annual-letter-2025 (2026-02-05)
- https://mercury.com/blog/mercury-acquires-centralhq

**Mercury help center** (support.mercury.com/hc/en-us/articles/…)
- 31501481890708 Contacting our Support Team (upd 2026-09-11)
- 28776140568212 Understanding FDIC insurance (upd 2026-07-21)
- 28776806677908 Understanding sweep programs (upd 2026-09-08)
- 43065703960852 Using multiple partner banks on Mercury (upd 2026-08-21)
- 31577686813076 Switching Mercury partner banks (upd 2026-09-02)
- 28742040300820 How your Treasury fee is calculated (upd 2026-07-15)
- 44370115553044 How net yield is calculated in Mercury Treasury (upd 2026-08-21)
- 41673479637908 Qualifying for a Treasury account (upd 2026-09-09)
- 41674211743380 Understanding Mercury Treasury (upd 2026-09-03)
- 49523388503828 Treasury Mutual Fund Update: Summer 2026 (upd 2026-08-21)
- 28768794858772 Qualifying for IO (upd 2026-08-22)
- 28768861008276 Understanding IO limit changes (upd 2026-08-20)
- 30066912540180 Qualifying for a metal IO card (upd 2026-09-11)
- 51299754284948 Agent cards: Giving AI agents a card of their own (upd 2026-08-21)
- 50304715308948 Mercury Command overview (upd 2026-09-02)
- 53170222904596 High-yield savings with Mercury Personal (upd 2026-09-02)
- 28773186865684 Processing times for payments
- 53435100997908 How ACH transfers and domestic wires work in the US (upd 2026-09-10)
- 28772666820500 International wire limits (upd 2026-09-10)
- 28772859696148 Requesting higher payment limits (upd 2026-09-11)
- 28767894198164 How to set up payroll on Mercury (upd 2026-05-01)
- 32787686187924 Understanding your 1099-INT tax forms
- 43095394066452 Understanding account closures and access restrictions
- (Full index retrievable via https://support.mercury.com/api/v2/help_center/en-us/articles.json: 326 articles)

**Mercury developer docs** (docs.mercury.com, markdown via `.md` suffix; index at /llms.txt)
- /docs/getting-started.md (upd 2026-06-12)
- /docs/api-token-security-policies.md (upd 2025-11-03)
- /docs/using-mercury-sandbox.md (upd 2026-06-04)
- /docs/what-is-mercury-mcp.md (upd 2025-11-18)
- /docs/connecting-mercury-mcp.md (upd 2026-07-27)
- /docs/supported-tools-on-mercury-mcp.md (upd 2026-07-27)
- /docs/send-money.md (upd 2026-08-25)
- /docs/invoicing.md, /docs/products-overview.md (upd 2026-08-26)

**Third party**
- https://www.bankingdive.com/news/mercury-pivot-partner-bank-evolve/742704/ (Evolve split, 2025-03-17)
- https://www.bankingdive.com/news/mercury-nabs-conditional-occ-charter/818674/ (OCC, HQ Utah, Jon Auxier, app filed 2025-12-19)
- https://www.pymnts.com/news/banking/2026/mercury-wins-conditional-occ-approval-for-banking-license/ (approval 2026-04-27, Akhund quote)
- https://www.businesswire.com/news/home/20260427949683/en/ (OCC conditional approval press release)
- https://www.occ.gov/topics/charters-and-licensing/interpretations-and-decisions/2026/cd1372.pdf (Corporate Decision #1372, April 2026)
- https://www.cnbc.com/2026/05/20/fintech-mercury-valuation-fundraise-bank-charter.html ($5.2B, +49% in 14 months)
- https://www.businesswire.com/news/home/20250326427283/en/ (Series C, $300M at $3.5B, Sequoia)
- https://www.businesswire.com/news/home/20260520511817/en/ (Series D, $200M at $5.2B, TCV)
- https://www.nerdwallet.com/business/banking/reviews/mercury-banking (last updated 2026-01-08; "relies primarily on email for customer support")
- https://github.com/MercuryTechnologies/mercury-cli (Apache-2.0, ~172 stars)
- https://dfpi.ca.gov/enforcement_action/mercury-technologies-inc/ (settlement executed 2022-01-03)
- https://www.thepaypers.com/… (Central acquisition: >$175M payroll, ~500 customers, 250+ already Mercury)

**Rho corpus (local)**: `/private/tmp/.../scratchpad/rho/pages/`
- core/versus__mercury.txt · core/pricing.txt · core/product__api.txt · core/product__treasury.txt · core/product__business-savings-account.txt · core/claude-code.txt
- blogcomp/blog__mercury-io-vs-rho-card.txt (pub 2026-08-03, upd 2026-08-26, "verified as of 08/02/2026")
- blogcomp/blog__mercury-vs-brex-vs-rho-startup-banking-comparison.txt (pub 2026-08-17, upd 2026-08-26)
- blogcomp/blog__mercury-alternatives.txt · blogcomp/blog__mercury-bank-reviews.txt · blogcomp/blog__mercury-business-credit-card-reviews.txt · blogcomp/blog__ramp-vs-mercury.txt · blogcomp/blog__brex-vs-mercury.txt · blogcomp/blog__rho-vs-slash-vs-mercury.txt
