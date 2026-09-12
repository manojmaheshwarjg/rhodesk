## 7. The 2026 competitive landscape

### 7.1 "Business banking" is at least four markets, and most comparisons mix them

Almost every published comparison of Rho against "the competition" is wrong before it starts, because it puts a $44B spend-management company, a 130-year-old national bank, and a developer tool on the same axis. They sell different things to different buyers and make money in different ways. Four markets are worth separating, and a fifth category (the chartered digital banks) sits between two of them.

| Market | What is actually sold | Who signs | How the vendor gets paid | Holds your money? |
|---|---|---|---|---|
| **1. Startup banking platforms** | A bundled account, card, payments and finance software stack, sold self-serve | Founder or first finance hire | Interchange (the fee a merchant's bank pays the card issuer on every swipe), the spread between what the partner bank earns on deposits and what it pays you, FX, advisory fees | Yes, through a partner bank |
| **2. Spend and AP software** | Workflow on top of whatever bank you already use: expense reports, accounts payable (paying supplier invoices), travel, procurement | CFO or controller | Per-seat or per-artifact subscriptions, per-payment take rates, FX spread, interest on money in transit ("float"), card interchange | Only in transit, if at all |
| **3. Traditional and chartered banks** | A deposit account at a federally or state-chartered institution, plus credit | CFO, treasurer, or founder via a relationship manager | Net interest margin (lending your deposits out at more than they pay you), monthly fees, per-item fees, wire fees | Yes, directly |
| **4. Banking infrastructure** | The rails themselves, sold as an API to other companies who then build a bank-like product | An engineering or product team at a fintech | Per-transaction pricing, program fees, revenue share with a sponsor bank | Yes, on behalf of their customer's customers |

Rho competes in markets 1 and 2 simultaneously, which is its central structural bet: it gives away the market-2 software in order to win the market-1 balance. It does not compete in market 4 at all, though its own nav label ("Rho API: Banking and payments via API") invites the confusion. See section 6, The API and the agent surface, for why the API is a first-party read feed rather than infrastructure.

The reason the distinction matters for a buyer is that the four markets have different failure modes. In market 1 your risk is that a company you cannot audit sits between you and an insured bank. In market 2 your risk is paying three times for one workflow. In market 3 your risk is earning 0.01% on your operating cash. In market 4 your risk is that you have become a bank without a charter.

**Assessment:** the single most common analytical error in this space, repeated in Rho's own comparison pages and in most press coverage, is treating "Rho vs Ramp vs Mercury vs Brex vs Chase vs BILL" as one ranked list. Ramp and BILL are market-2 companies that have annexed parts of market 1. Mercury is a market-1 company trying to become a market-3 company. Chase is market 3 and has never seriously entered market 2 for small business (it resells a white-labeled BILL product). Rho is the only one of the set whose whole proposition is that markets 1 and 2 should be the same purchase and the software half should cost nothing.

---

### 7.2 Rho vs Ramp

Ramp is the scale competitor, and the comparison is lopsided on almost every dimension of size while being genuinely close on price transparency and support.

**Verified** (from the adversarially checked claim register, as of 2026-09-11): Ramp closed a $750M Series F on June 4, 2026 at a $44B valuation (co-led by ICONIQ, GIC and Ontario Teachers' Pension Plan), and as of June 1, 2026 reported more than 70,000 customers and more than $200B in annualized purchase volume. Those customer and volume figures are Ramp's own and are not audited. PYMNTS reported on September 8, 2026 that Ramp was in early talks to raise about $1B primary at a $60B valuation, so $44B is the last closed mark, not the current one.

**Verified:** Ramp's agent surface is unusually broad for corporate spend. It runs three MCP servers as Ramp itself counts them (MCP, the Model Context Protocol, is the open standard for letting an AI assistant call a vendor's tools): `mcp.ramp.com/mcp` for account data, `mcp.ramp.com/developer/mcp` for unauthenticated documentation, and `mcp.ramp.com/ramp-data/mcp` for the Ramp Rate and AI Index datasets, the last gated behind a partner program. It publishes an MIT-licensed open-source CLI at `github.com/ramp-public/ramp-cli` whose skill catalog includes `agentic-purchase`. It issues Agent Cards as single-use Visa Intelligent Commerce tokens, still in early access rather than generally available. Its Developer API carries 252 operations across 40 top-level resource groups, read and write, verified against `docs.ramp.com/llms-api.txt` on 2026-09-11. And on August 19, 2026 it launched Router, an LLM gateway, at router.com.

Note what is deliberately absent from that paragraph: the claim that Ramp has "the deepest agent surface in business finance" was tested and rejected as an unfalsifiable superlative with a credible rival claimant in Stripe. The defensible version is narrower: within corporate spend management specifically, Ramp ships more agent capability than Brex, Mercury, Navan or Meow.

| Dimension | Ramp | Rho | Who wins |
|---|---|---|---|
| Last closed valuation | $44B, June 4 2026 (reports of $60B talks, Sept 8 2026) | Not published; SEC shows $104.7M raised across five Form D filings, none since Jan 2022 | Ramp |
| Customers | 70,000+ (Ramp's figure, as of June 1 2026) | "8,000+ businesses" (Rho's figure, Aug 2026, and its own pages also say 5,000) | Ramp |
| Software price | Free tier $0; Plus $15/user/mo **plus an undisclosed platform fee "based on team size"**; Enterprise custom | $0 at every size. No tiers, no seats, no platform fee | Rho |
| ACH / domestic wire / check | $0.59 / $15 / $1.99, all waived if funded from a Ramp Checking account | $0 / $0 / $0 | Rho on list price; parity if you bank at Ramp |
| FX | 3% card FX markup (third-party sourced) | 1% foreign-currency transfer, provided by Wise US Inc. | Rho |
| Published cashback | None. Actual rate reportedly 0% to 1.5%, set per customer after you apply | Published matrix: 1.25% standard / up to 2% with Rho Platinum on Daily Terms, capped at $1M eligible annual spend | Rho on disclosure |
| Treasury minimum | $5,000 initial | $50,000 | **Ramp, by 10x** |
| Advisory fee on invested cash | Up to 0.15% flat | 0.60% under $2M, sliding to 0.15% at $20M+ | Ramp below $20M |
| Headline invested yield | Up to 4.44% YTM as of 09/03/2026 | Up to 4.66% net as of 09/11/2026, but that is the $20M+ tier and assumes a 100% allocation the product caps at 50% | See below |
| API | 252 operations, read **and** write, OAuth 2.0, ~50 scopes, webhooks, sandbox | 14 operations, all GET, five read-only scopes, no webhooks, no public sandbox MCP | Ramp |
| Agent authority | Approve/reject transactions and POs via MCP; Agent Cards can complete a scoped purchase | Read-only by design | Ramp |
| Support on the free tier | 24/7 chat and AI assistant, no phone; phone starts at Plus | 24/7 human phone, chat and SMS on every account at no cost | **Rho** |
| Procurement / three-way match | Yes (procurement is a paid add-on above Plus) | Not offered. Rho states plainly it "does not include procurement or supply-chain management" | Ramp |

**Verdict.** Ramp is a materially larger and deeper product, and Rho's own marketing concedes it. Rho's `versus/ramp` FAQ says Ramp's "agent/AI tooling (hosted MCP server with audited write actions, public CLI) is genuinely ahead," which is an unusually honest thing for a comparison page to print and is accurate. Where Rho genuinely wins is a short list, and it is real: no subscription or seat fee at any size, a published cashback matrix with a 2% ceiling against Ramp's undisclosed rate, 1% FX against Ramp's 3% card markup, and a human on the phone at 2am on a $0 account.

One Rho claim in this matchup does not survive contact with the evidence, and one competitive omission is worth naming alongside it. The omission: Rho argues its $50,000 Treasury minimum as a win against Mercury's $250,000 and never mentions, on its `versus/ramp` page or anywhere else, that Ramp's investment account opens at $5,000, ten times lower than Rho's. That is marketing selectivity rather than a false statement, but it is the largest hole in Rho's own competitive framing. The claim: the 4.66% is the top fee tier's rate and, per the claim register, it assumes a 100% allocation to the Vanguard Short-Term Investment-Grade Fund (VFSTX) while Rho's own help center caps Vanguard allocations at 50% of the portfolio. A cap-compliant 50/50 portfolio at the same top tier yields 4.18% net, 48 basis points below the headline. The cap is not absolute (existing allocations above 50% are grandfathered and a higher limit can be approved on request), so the honest framing is that the headline is unreachable under the product's standard published allocation rules rather than mathematically impossible. Meanwhile the research file puts Rho's sub-$2M tier at 4.21% net, below Ramp's published 4.44%.

**Assessment:** for a company under about 50 people that wants one flat, free, phone-supported stack, Rho is a legitimate choice and Ramp's tiering is a real cost. For a company with multiple entities, a NetSuite instance, a procurement process, or an engineering team that wants to automate finance, Ramp is not replaceable by Rho, and the gap is widening on the agent axis specifically.

---

### 7.3 Rho vs Brex

Brex is the competitor whose identity changed most in 2026, and the change is the whole story.

**Verified** (claim register, confidence high, CONFIRMED): Capital One Financial Corporation completed its acquisition of Brex Inc. on April 7, 2026 under an Agreement and Plan of Merger and Reorganization dated January 22, 2026. Capital One's Q2 2026 Form 10-Q records the fair value of purchase consideration at $4,521 million ($2,630M cash plus 10.6 million COF shares with a fair value of $1,891M, including $13M related to restricted stock units, and still subject to customary post-closing adjustments), and states that immediately following completion Capital One paid off Brex's outstanding $1.1 billion of debt. The deal was announced on January 22, 2026 at a headline value of $5.15 billion, which is the announced transaction value and **not** the arithmetic sum of the closing components ($4.521B + $1.1B = $5.62B). Rho's own blog post on the acquisition gets this wrong, describing $5.15B as "including the debt payoff."

**Verified:** as of September 11, 2026, Brex's own live disclosures state that "Brex LLC is a wholly owned subsidiary of Capital One, N.A." and that the Brex business account's checking leg is "a commercial checking account provided by Column N.A., Member FDIC (an unaffiliated institution)" (FDIC #58224, routing 121145349), while Brex Treasury LLC is "a Capital One company." Pedro Franceschi continued as CEO per Capital One's April 7, 2026 completion release, with no reported change since.

| Dimension | Brex | Rho |
|---|---|---|
| Ownership | Wholly owned subsidiary of Capital One, N.A. since 2026-04-07 | Independent. Under Technologies, Inc. dba Rho Technologies |
| Checking deposits | Column N.A., an **unaffiliated** bank, FDIC #58224 | Webster Bank, a division of Santander Bank, N.A. |
| FDIC ceiling | $250K at Column on checking; Vault sweeps to $6M across 24 to 27 program banks (Brex's marketing and legal pages disagree on the count) | $250K on checking; Savings swept by American Deposit Management to a stated $75M across 400+ FDIC- and NCUA-insured institutions |
| Software price | Essentials $0; Premium $12/user/mo; Enterprise custom | $0, no tiers |
| Banking fee schedule | $0 on domestic and international ACH, wires both directions, checks, opening and maintenance | $0 same-day ACH, domestic wires, checks; 1% FX; $30 international wire recall; optional $15 SWIFT fee |
| The fee not on the pricing page | Up to 3% FX markup on card transactions requiring conversion, plus an undisclosed markup on non-USD wires and global reimbursements | The $20 to $45 failed-domestic-wire fee and the 2.9% + $0.30 invoice card fee, both help-center only |
| Yield on idle cash | Treasury in a money-market fund (DGVXX), 3.35% to 3.70% total return tiered by balance, **no minimum**; checking and Vault pay no yield | Savings up to 1.00% variable at a $25,000 average balance; Treasury from $50,000 |
| Rewards | Brex Points, redeemed at 0.6 cents each for cash, 1 cent in Brex Travel; **earned only on USD transactions with US merchants** | Cash back, 1.25% to 2% depending on terms and Platinum status |
| API and agents | 10 REST APIs including Payments (ACH, wire, check), hosted MCP at `api.brex.com/mcp` with ~37 read tools and 4 low-risk write tools, apps in ChatGPT, Claude and Slack. API access included on the free tier | 14 read-only GET operations, one production read-only MCP server |
| Eligibility floor | US EIN, US incorporation, US operations, US physical address; $50,000 minimum cash for funded startups on monthly terms, or >$500K annual revenue | US-incorporated entity, plus a US operating address or a US-based owner with an SSN. No published revenue or balance minimum to open |

**What an acquisition by a large bank actually means for a buyer evaluating Brex today.** Five things, in rough order of practical weight.

1. **The deposit counterparty did not change.** This is the most commonly misunderstood point. Being owned by Capital One, N.A. did not move Brex customers onto Capital One's charter. Checking is still at Column N.A., which Brex's own footer describes as unaffiliated, and card issuing is still with Emigrant Bank, Fifth Third Bank, N.A. and Airwallex (Netherlands) B.V. No migration has been announced as of 2026-09-11. A buyer who thinks "Brex is now a bank account at Capital One" is wrong.
2. **You lose the ability to monitor the vendor.** Brex results fold into Capital One's Domestic Card sub-segment from Q2 2026, and Brex no longer reports standalone financials. Brex never published audited revenue anyway (the $700M annualized figure traces to a CEO statement), but from here there is nothing at all. The offsetting benefit is that the parent is a supervised, publicly reporting institution with $669.0 billion in total assets as of December 31, 2025, so the counterparty-failure question is effectively closed.
3. **Some of the economics are now a parent-company subsidy.** Brex's treasury return is the underlying fund yield (3.35%) plus an "additional return" of 0.00% to 0.35% paid by Brex itself, and Brex reserves the right to change the tier schedule at any time. That subsidy is now funded by a Capital One subsidiary. It is a marketing expense, not a market rate.
4. **The distribution strategy moved from venture networks to bank channels.** The December 2025 Fifth Third partnership makes Brex the default commercial card for Fifth Third's commercial banking clients, which Franceschi described as "roughly 8% of the U.S. commercial banking sector through a single partner," and Capital One disclosed a lead-sharing program on its Q2 2026 earnings call. Franceschi's January 2026 post promises "Our Essentials plan stays free" and a 50% increase in startup-team headcount. Those are company statements, not contractual commitments.
5. **Leadership continuity is partial.** Franceschi remains CEO, but COO Camilla Matias and Chief Business Officer Art Levy have both departed post-close (Levy in August 2026), so any "the team is unchanged" claim, including Rho's, should not be extended past the CEO.

**Verdict.** Brex is now the better-capitalized option with the broader free tier: $0 on every payment rail, a money-market treasury with no minimum, API access on the free plan, and a functioning MCP server. Rho's genuine wins against Brex are the FDIC savings ceiling ($75M stated versus a hard $6M), the treasury minimum only if you are below $50K, the Mastercard World Elite benefits, and the absence of a $12/user Premium tier for multi-entity and advanced approvals. Rho's genuine loss is that Brex's entry-level economics are now underwritten by a top-ten US bank, and Rho's comparison page omits Brex's $0 fee schedule, its 3.35%-with-no-minimum treasury, and its entire API and agent surface.

---

### 7.4 Rho vs Mercury

Mercury is the closest structural comparable to Rho and is the only competitor in this set that is trying to stop being a fintech.

**Verified** (claim register): Mercury received OCC **preliminary conditional** approval on **April 24, 2026** (Corporate Decision #1372, OCC Control No. 2025-Charter-344332) to charter Mercury Bank, National Association in Salt Lake City, Utah. Mercury announced it publicly on **April 27, 2026**, which is the date commonly but incorrectly cited as the approval date. The approval is preliminary only, and **final OCC authorization to open plus FDIC deposit insurance and Federal Reserve approvals remain outstanding.** The OCC's own decision document says so directly: "The OCC has granted preliminary conditional approval only. Final approval and authorization for the Bank to open will not be granted until all preopening requirements are met."

**Verified:** Mercury states it serves more than 300,000 businesses and individuals, generates more than $650 million in annualized revenue (a run rate, not audited annual revenue, and the underlying data point dates to Q3/Q4 2025), and has maintained four years of GAAP profitability. All three are self-reported and reproduced by press outlets from Mercury's own boilerplate.

**Verified:** Mercury offers a write-capable REST API that can initiate ACH, check, and domestic and international wire payments, and a hosted MCP server at `mcp.mercury.com` with exactly 31 documented tools, **all of which are read-only and cannot move money**. The write capability lives in the REST API and in Mercury's open-source CLI, not in the MCP. Mercury advertises **no phone support on any plan, including the $350/month Pro tier ($299 on annual billing)**, offering only email and in-app messaging.

| Dimension | Mercury | Rho |
|---|---|---|
| Charter status | OCC preliminary conditional approval 2026-04-24 for Mercury Bank, N.A.; FDIC and Fed approvals still pending | Fintech, not a bank. No charter application disclosed |
| Deposit banks | Choice Financial Group and Column N.A., each with sweep networks | Webster Bank (a division of Santander Bank, N.A.) for checking; American Deposit Management for savings |
| FDIC coverage | Up to $5M via up to 20 sweep program banks, on the **operating account** | $250K on checking; up to $75M on **Savings** via 400+ institutions |
| Plans | $0 / $35 / $350 month-to-month, or $0 / $29.90 / $299 with annual billing (the pricing page's toggle defaults to annual), as of 2026-09-11 | $0, no tiers |
| Treasury gate | $250,000 balance across Mercury accounts | $50,000 |
| Treasury fee schedule | 0.60% under $2M sliding to 0.15% at $20M+ | **Identical schedule, same breakpoints** |
| Headline net yield | Up to 3.89% (MCRYX, $20M+, as of 09/04/2026) | Up to 4.66% ($20M+, as of 09/11/2026), on a different methodology |
| Card | IO charge card (a card whose balance must be paid in full each cycle rather than revolved), flat 1.5% cash back | Mastercard World Elite for Business, 1.25% standard / up to 2% Platinum |
| Support | 24/7 chat and email. **No phone at any tier.** Relationship manager at Pro only | 24/7 human phone, chat and SMS on every account, free |
| API writes | Yes: ACH, check, domestic wire directly; international wire through an approval queue; card issue/freeze/cancel; webhooks; sandbox | **No, by design** |
| Agent surface | 31-tool read-only MCP, write-capable CLI, agent cards with a Vault endpoint that lets an agent self-retrieve PAN/expiry/CVC, and Command, an in-app operator that stages real actions for human confirmation | Read-only MCP |
| Customers | 300,000+ (Mercury's figure) | 8,000+ (Rho's figure) |
| Free-tier gating | Recurring invoicing needs Plus; NetSuite categorization needs Pro; reimbursements beyond 5 users need a paid plan | Nothing gated behind a price |

**Why a bank charter matters.** A charter is not a badge; it changes six concrete things, and understanding them is the difference between reading Mercury's April announcement as marketing and reading it as a structural event.

1. **Direct depositor relationship.** At a chartered bank you are the depositor of record and FDIC insurance attaches to an account in your name on the bank's own books. At a fintech you are typically a beneficial owner of a pooled custodial account, and coverage is "pass-through," which the FDIC conditions on records that correctly identify who owns what. If the records are wrong, the coverage is contested.
2. **Resolution mechanics.** A failed insured bank goes into FDIC receivership and insured depositors are typically paid within one business day. A failed fintech goes into bankruptcy, where you are a creditor in a queue behind a trustee, an automatic stay, and professional fees.
3. **Balance-sheet lending.** Venture debt, capital-call lines and traditional working capital require regulatory capital. This is why First Citizens/SVB can lend at 20% to 40% of a startup's last equity round and no fintech can match it from its own balance sheet.
4. **Payment access in your own name.** A charter brings a Federal Reserve master account, the bank's own routing number, and direct Fedwire, FedACH and FedNow access. Mercury has said publicly that the charter is what unlocks Zelle and expanded lending.
5. **Prudential supervision.** The entity holding your money is examined for capital, liquidity, asset quality and anti-money-laundering compliance. Rho, Mercury today, Brex, Ramp, Bluevine, Relay and Novo are not supervised as depositories; their partner banks are.
6. **Governance optics.** An acquirer's diligence team, an auditor, and an enterprise customer's vendor-risk questionnaire all treat "our operating account is at a national bank" differently from "our operating account is at a fintech whose partner bank was acquired last month."

The counterweight: preliminary conditional approval is not permission to open, a charter brings Community Reinvestment Act obligations, call reports and capital requirements, and Mercury's own service model would have to change. Its current no-phone-support posture is the single element of the Mercury picture most likely to expire first, precisely because a chartered bank is expected to answer the phone.

**Verdict.** Mercury beats Rho decisively on scale, programmability and agent readiness, and it is the only competitor with a credible path out of the fintech-layer risk category. Rho beats Mercury on four things that are hard numbers and do not depend on Mercury standing still: phone support that a human answers, the $50K-to-$250K treasury band that Mercury will not serve, the $75M savings FDIC ceiling against $5M, and the absence of paid tiers (recurring invoicing, NetSuite automation and reimbursements beyond five users all cost money at Mercury and nothing at Rho).

One caveat cuts against Rho's favorite statistic. The $75M applies to **Rho Savings**, not Rho Checking, which is $250K per entity. Mercury's checking is swept to $5M. So for an operating balance between $250,000 and $5,000,000 sitting in the account you actually pay bills from, **Mercury's checking is better covered than Rho's.** The comparison only becomes lopsided once the money has been moved into Rho Savings, which caps withdrawals at six per month.

---

### 7.5 Rho vs the spend and AP incumbents

This is the group Rho's marketing attacks hardest: BILL, Navan, American Express, Expensify, SAP Concur, Tipalti, and Airbase (now inside Paylocity). The attack line is "they charge software fees and sit on top of someone else's bank; Rho bundles the software free and provides the account."

**That line is only half right, and the half that is wrong is checkable in an afternoon.**

| Vendor | Published software price | What the price really is | Is it a bank? |
|---|---|---|---|
| **Rho** | $0/user/month | Genuinely $0. Non-zero: 1% FX, optional $15 SWIFT, $30 international wire recall, 0.15% to 0.60% Treasury advisory fee | No. Webster Bank, a division of Santander Bank, N.A. |
| **BILL** AP/AR | $49 / $65 / $89 per user/month | Plus $0.59 ACH, $1.99 check, 2.9% card, $19.99 international USD wire, and BILL keeps the interest on money in transit | No. Cards via Cross River, WebBank, WEX Bank |
| **BILL** Spend & Expense | **$0/user/month** | Genuinely $0 for software; monetized through BILL's own card, no bring-your-own-card | No |
| **Navan** | Travel free under 300 employees; Expense free for 5 users then $15/user/month | ~90% of Navan's revenue is usage-based, ~10% subscription, per its S-1 | No. Celtic Bank issues the US card |
| **American Express** | **No per-seat software fee at all** | $895/year Business Platinum, $375 Business Gold, $90 Corporate Card program fee. Expense software (Center, acquired April 16 2025) now owned outright | **Yes. American Express National Bank, Member FDIC.** Business checking at 1.30% APY up to $500,000 |
| **Expensify** | $5 Collect; Control $9 / $18 / $36 | $9 **only** with an annual term, the Expensify Card enabled, and at least 50% of US spend routed through it. $18 if you keep your own card. $36 month-to-month | No. Bancorp Bank issues the card |
| **SAP Concur** | $7 / $11 **per expense report** | Third-party cost-benchmark estimates, not SAP figures: $9 to $24 per active user/month, $3.50 per invoice document with a $30K minimum, implementation $15K to $40K (Standard) or $80K to $350K (Professional), 5% to 8% annual escalators | No. Issues no card, holds no funds |
| **Tipalti** | From $99/month, "unlimited users" | A floor, not a price: Tipalti's own page declines to state transaction, FX, module and implementation amounts. Third-party cost-benchmark sites, not Tipalti and not independently confirmable (the primary source for these ranges was unreachable on 2026-09-11), put the real cost at $0.20 to $36 per payment, a 1.9% to 3.5% FX markup, $500 to $600/month per extra legal entity and $4K to $5K setup, with transaction and FX said to be 50% to 70% of the annual bill | No |
| **Airbase / Paylocity** | Not published since the acquisition | Historically $12 to $18 per user/month; now quoted inside a Paylocity HCM (human capital management, meaning payroll and HR software) deal | No |

**The correction, stated precisely.** BILL's fiscal 2026 results (announced 2026-08-19, year ended 2026-06-30) show total revenue of $1,653.2M, of which subscription fees were only $293.5M, or **17.8%**. Transaction fees were $1,211.2M (73.3%) and float revenue, which BILL describes as "interest on funds held for customers," was $148.4M (9.0%). So the largest seat-priced AP incumbent is already mostly not a seat business. Navan is the same shape: roughly 90% usage-based, 10% subscription. And on 2026-09-10, at the Goldman Sachs Communacopia + Technology Conference, BILL CEO Rene Lacerte said "pricing has to be tied to value creation" and that BILL is "analyzing the levers we have ... to change from just the subscription pricing model we have today to something that actually more closely matches ... the value that we're creating." That is the incumbent conceding the point on the record, and it also narrows Rho's wedge: if BILL moves to consumption pricing with a $0 entry, "no seat fees" stops being a differentiator against BILL.

The seat-fee argument fails outright against two vendors. **American Express** charges no per-seat software fee, is itself an FDIC-insured bank paying 1.30% APY on business checking up to $500,000, and since April 2025 owns its expense-management software (Center) rather than partnering for it. Rho's `versus/amex` page fixes on the $895 Business Platinum annual fee, which is correct for that card and misleading for Amex Commercial, where the Corporate Card program fee is $90. **BILL Spend & Expense** is genuinely $0 per user per month.

**Where the argument does survive, and it survives well, is three narrower claims.**

1. **The double dip on float.** BILL charges $49 to $89 per user per month, $0.59 per ACH, 2.9% on card-funded payments, **and** keeps $148.4M a year of interest on customer money in transit. Tipalti, Corpay and Airbase/Paylocity have the same shape. Rho gives the workflow away and routes the yield back to the customer through Savings and Treasury. This is the cleanest version of the structural claim, and it is sourced entirely to the incumbent's own press release.
2. **The interchange hostage clause.** Expensify publishes $9 per member per month and then conditions it on a 12-month commitment, the Expensify Card being enabled, and at least 50% of settled US spend flowing through it. Keep your own bank's card and the rate doubles to $18; go month-to-month and it is $36. BILL's $0 Spend & Expense requires BILL's own card with no bring-your-own-card option. Both vendors have already conceded that the software is worth roughly nothing and the card flow is the product. They are simply charging a penalty to customers who keep their existing bank. Rho charges no such penalty because it is the card and the account.
3. **The unit of pricing is the artifact of the old workflow.** Concur charges per expense report. Tipalti charges per invoice and per payment. Coupa charges per module and per supplier. Each of those prices scales with the manual work, which structurally opposes the vendor's revenue to automating it away. Rho's stated product thesis is that the expense report should not exist.

**Assessment:** the honest framing against this group is not "seats versus no seats." It is **who holds the balance and who gets the yield.** That version survives against Amex (which holds the balance but pays 1.30% rather than a treasury yield), against BILL (which keeps the float as revenue), and against Concur and Coupa (which never touch the money at all).

Two things a buyer should hold against Rho here. First, Rho's own comparison content about this group is materially stale and in places wrong: it states BILL charges a "10% instant transfer fee" when BILL's published Instant Payment fee is 1.0% with a $9.99 minimum and a $100 maximum; it says "Expensify's pricing is not public" when Expensify has published $5/$9/$18/$36 since April 2025; it profiles Center as an independent alternative eighteen months after American Express completed the acquisition; and it treats Airbase as independent nearly two years after Paylocity bought it for ~$325M. Second, Rho does not offer procurement, three-way matching (reconciling a purchase order, a goods receipt and an invoice before paying), or published international AP coverage figures, and it publishes no vendor-network size, country or currency counts, or global tax-withholding capability. Against Tipalti's 200+ countries and BILL Corporate's purchase orders and tolerance rules, those are real functional gaps that Rho's comparison pages do not acknowledge.

The market itself is repricing this group downward. In the same 24-month window, AvidXchange (~$450M revenue) went private at roughly $1.9B enterprise value, Airbase sold for ~$325M, Navan IPO'd at ~$6.2B and closed its first day down 20%, BILL is fielding three activist investors and reported private-equity interest, and Ramp went from $22.5B to $32B to $44B. The market is paying for balance-sheet-attached spend, not for seats. That trend is the strongest thing Rho has going for it, and Rho did not cause it.

---

### 7.6 Rho vs traditional banks and the chartered digital banks

This is the comparison where Rho is structurally weakest on safety and structurally strongest on economics, and where the honest answer to "which should I use" is often "both."

| Provider | Monthly fee | Interest on business cash | Outgoing domestic wire | Charter |
|---|---|---|---|---|
| **Chase** | $15 / $40 / $95 by tier, waivable at $2K / $35K / $100K balances | **0.01% APY** on Business Total Savings at every tier; 0.02% relationship Premier Savings; checking "does not earn interest" | $25 online, $35 branch; $40 international USD online | National bank |
| **Bank of America** | $16 / $29.95, waivable at $5K / $15K | Checking is explicitly "non-interest-bearing" | $30 domestic out, $45 international USD out | National bank |
| **Wells Fargo** | $15 / $25 / $75 (the $75 Optimize tier has **no waiver available**) | Navigate and above are interest-bearing, rate not published in the schedule | $30 digital, $40 branch | National bank |
| **First Citizens / SVB** | Online Banking **$125/month**, plus $25/month wire module and $40/month ACH module | Startup Money Market, per Rho's `versus/svb` page citing an SVB rate sheet dated 2025-12-10 and not independently verifiable because SVB publishes no current startup money-market rates online: **0.10% APY under $50K**, 2.38% $50K to $1M, 3.30% above $1M (Rho's figures, unconfirmed) | **$12** online domestic, $25 international USD | National bank (SVB is a division) |
| **HSBC Innovation Banking** | Spark: **$0 for 24 months** including unlimited wires and ACH. Innovation Package: waived only at a **$1,800,000** combined average monthly balance | "Competitive rate," not published | Not published | National bank |
| **Grasshopper Bank, N.A.** | $0 | Innovator Savings **1.55% up to $25K, 3.00% above** (rates as of 2026-01-05) | Free ACH and domestic wires on Accelerator Checking | **National bank charter** |
| **Axos Bank** | $0 Basic Business Checking | Business Interest Checking up to 1.01% APY | Two reimbursed outgoing domestic wires monthly | **Federal charter, OCC supervised** |
| **Rho** | $0 | Savings up to 1.00% variable at a $25,000 average balance; Treasury from $50,000 | $0 | **None.** Fintech; deposits at Webster Bank, a division of Santander Bank, N.A. |

**What a real charter provides that Rho cannot.** Beyond the six items listed in 7.4, three are specific to this comparison. Branches, cash and physical instruments: cash and coin deposits, cashier's checks, notarization. Rho concedes this directly on its own Bank of America comparison page, calling BoA's free cash allowance "real, tangible value that a fully digital platform simply can't offer" and stating "Rho doesn't support cash deposits at all." Venture debt: SVB/First Citizens sizes loans at 20% to 40% of the last equity round with a $4M minimum round, and First Citizens' Global Fund Banking pipeline stood at $11.5 billion at year-end 2025. Earnings-credit accounting: Chase, Wells Fargo, SVB and HSBC all offer analyzed checking where balances generate a credit that offsets service fees (Chase's earnings credit rate was 0.20% to 0.30% as of 2026-09-11). None of the three has a fintech equivalent.

**The honest counter-list.** A charter buys none of the software. Chase has no small-business banking API and resells AP through a white-labeled BILL product. SVB charges $125 a month just to log in, plus $25 for wires and $40 for ACH, plus $50 to $250 a month for bill pay. Bank of America and Wells Fargo publish no ACH origination pricing at all at the small-business tier. And all of them pay 0.01% to 0.02% on business savings while Treasury bills yield multiples of that. A startup parking $2M in Chase Business Total Savings earns roughly $200 a year; the same $2M in a Treasury sleeve earns roughly $60,000. That delta, not the $15 monthly fee, is the real cost of a big-four operating account.

Two timing notes for anyone choosing in late 2026. **SVB is being retired as a brand in Q4 2026**: the technology and healthcare business becomes First Citizens Innovation Banking and Global Fund Banking becomes First Citizens Fund Banking. **Grasshopper is changing owners**: Enova International signed a definitive agreement on 2025-12-11 to acquire Grasshopper Bancorp for ~$369 million, expected to close in the second half of 2026 subject to OCC and Federal Reserve approval, and American Banker reported backlash over a high-cost consumer lender acquiring a bank charter.

**The counterparty risk a fintech layer adds.** Deposit insurance protects against the failure of the institution at the end of the chain. Every hop before that is uninsured operational and ledger risk.

| Structure | Providers | Hops between you and the insured deposit |
|---|---|---|
| Direct deposit at a chartered bank | Chase, BoA, Wells Fargo, First Citizens/SVB, HSBC, Grasshopper, Axos | 1 |
| Fintech program, then partner bank | Novo ($250K at Middlesex Federal Savings) | 2 |
| Fintech program, partner bank, then sweep network | Bluevine ($3M), Lili ($3M), **Rho Savings ($75M via ADM)** | 3 |
| Fintech program, BaaS middleware, partner bank, sweep network | Relay ($3M via Unit and Thread Bank) | 4 |

**The Synapse lesson.** Synapse Financial Technologies, the middleware ledger between consumer fintech brands and their partner banks, filed Chapter 11 on 2024-04-22. More than 100,000 people lost access to over $265 million. The shortfall between the ledger and the cash was put at $65M to $96M by the Chapter 11 trustee (former FDIC Chair Jelena McWilliams) and $60M to $90M by the CFPB; nobody knows the exact figure, and McWilliams stated that a full reconciliation to the last dollar may not be possible. The bankruptcy was **dismissed** in late 2025, nineteen months in, without full reconciliation. On 2025-11-28 the CFPB allocated **$46,248,291** from its Civil Penalty Fund to victims, against a shortfall of $60M to $90M. **Zero dollars of FDIC deposit insurance were paid out, because no insured bank failed.** Evolve, Lineage, American Bank and AMG National Trust all survived.

Three lessons generalize. The failure mode was reconciliation, not insolvency: the program's ledger and the banks' records disagreed and nobody held an authoritative source of truth. The partner bank's regulatory state becomes your regulatory state: the Federal Reserve issued a consent cease-and-desist against Evolve Bank & Trust on 2024-06-14, and the FDIC put Thread Bank, which serves Relay through the middleware provider Unit, under a consent order effective 2024-05-21 that specifically required Thread to build procedures to "unwind third-party business lines, including FinTech partners." And recovery is slow, partial and political: nineteen months to a dismissal, with a civil-penalty fund as the actual remedy.

**The state of the FDIC recordkeeping rule, as of 2026-09-11.** The rule that would have directly addressed Synapse, Recordkeeping for Custodial Accounts (RIN 3064-AG07), would require banks holding custodial accounts with transactional features to maintain beneficial-owner records and **reconcile daily**. It was approved by the FDIC Board on 2024-09-17 and published on 2024-10-02, with comments closing 2025-01-16. **It is still a proposal.** It was not among the four Biden-era proposals the FDIC Board rescinded on 2025-03-03, and no final rule and no withdrawal has issued. Separately, the FDIC's signage and misrepresentation rule (12 CFR Part 328) was finalized on 2026-01-29, effective 2026-03-02, but with compliance **pushed to 2027-04-01**. The substantive Subpart B prohibitions (a non-bank may not claim deposit insurance without disclosing that it is not itself insured, and must clearly identify the insured institutions holding the deposits) are already enforceable law; the granular digital-signage mechanics do not bite until April 2027.

**Assessment:** roughly two years after Synapse, the single federal rule that would have prevented it is unfinalized. A buyer evaluating any fintech deposit product in September 2026 cannot rely on a federal daily-reconciliation mandate, because there is not one.

**Where this lands on Rho specifically.** Rho is a three-hop structure on Savings and a two-hop structure on Checking, and three details from the claim register deserve to be in front of a buyer. Rho publishes the American Deposit Management master services agreement on its own help center, and that agreement commits ADM only to "commercially reasonable efforts to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution," with an explicit carve-out that on a single day "for a limited amount of time (intraday or overnight), the entire amount of the withdrawal or deposit may be held at one Program Institution." That effort standard is industry-standard sweep language (Pershing, Altruist and DriveWealth use near-identical wording), but it is weaker than the benchmark: IntraFi's ICS agreement commits flatly that placements "will not exceed $250,000" and adds a reimbursement obligation if its failure to comply leaves funds uninsured. Second, the same agreement limits withdrawals to six per month and processes them "on Tuesdays and Thursdays ... for settlement to your designated account on Wednesdays and Fridays," which conflicts with Rho's own help-center statement that Savings-to-Checking "typically settles the next business day." That is a liquidity limitation, not an insurance limitation, and it is the genuinely non-standard term. Third, Rho's headline "$75,000,000 in FDIC insurance" is described on its own network as "400+ FDIC- **and NCUA**-insured institutions," and NCUA insures credit unions under a different fund with a different resolution process. Rho also does not publish the network bank list, stating only that it is "available from Rho support on request," which sits awkwardly against 12 CFR 328.102's requirement that a non-bank claiming insurance clearly identify the institutions holding the deposits.

One more fact belongs here because it makes the abstract concrete: **Rho's own partner bank changed control during 2026.** Banco Santander agreed on 2026-02-03 to acquire Webster and completed the acquisition on 2026-08-20 by merging Webster Bank into Santander Bank, N.A. Rho updated its corpus promptly, which is good hygiene, but the point stands that a fintech customer's partner bank can be merged out from under them with no action on their part.

---

### 7.7 The positioning map

Two axes decide most of what matters. **How much of the stack the vendor owns** determines your counterparty risk, your yield, and whether anyone can lend you money off a balance sheet. **How much an agent or API credential can actually do** determines whether your finance function can be automated by software you write, which is the axis moving fastest in 2026.

| Player | Market | Stack ownership | What an API or agent credential can do |
|---|---|---|---|
| **Rho** | Startup banking + spend/AP | Software plus sponsor bank (Webster/Santander; ADM for savings) | **Read only.** 14 GET operations, five read-only scopes, one read-only MCP server |
| **Mercury** | Startup banking | Software plus sponsor banks (Choice, Column); **charter preliminarily approved 2026-04-24, not yet open** | **Money movement.** REST API sends ACH, check, domestic and international wires; CLI writes; agent cards; MCP itself read-only (31 tools) |
| **Brex** | Startup banking + spend | Software plus sponsor bank (Column, unaffiliated); owned by Capital One, N.A. | **Money movement** via the Payments API. MCP has ~37 reads and 4 low-risk writes, no payments |
| **Ramp** | Spend/AP, annexing banking | Software plus sponsor banks (First Internet Bank of Indiana, IntraFi sweep) | **Money movement.** 252 read/write operations; MCP approves transactions and POs; Agent Cards complete scoped purchases (early access) |
| **Meow** | Startup banking | Software plus sponsor bank | **Money movement**, behind an initiator-and-approver workflow |
| **Slash** | Startup banking | Software plus sponsor bank | **Money movement** via an MCP passthrough to the full API |
| **BILL** | Spend/AP | Software only; money transmitter holding funds in transit | **Writes** in-product via four named agents; no first-party MCP found |
| **Navan** | Travel and expense (T&E) | Software only (card via Celtic Bank); explicitly bank-agnostic | **Read only.** 11-tool MCP, read-only at launch (2026-07-01) |
| **Expensify** | Expense | Software only (card via Bancorp) | Writes via API; no first-party MCP found |
| **SAP Concur** | T&E | **Software only.** Issues no card, holds no funds, earns no interchange | Writes via API; no first-party MCP found |
| **Tipalti** | AP / mass payouts | Software only; holds funds in transit | Writes including payouts via API |
| **Airbase / Paylocity** | Spend/AP inside HCM (human capital management) | Software only | Writes via API |
| **American Express** | Cards + expense + banking | **Chartered bank** (American Express National Bank) and card network, plus owned software (Center, April 2025) | Enterprise integrations; no consumer-grade self-serve write API for SMB |
| **Chase** | Traditional banking | **Chartered bank** | No published small-business banking API; treasury APIs at the commercial tier |
| **First Citizens / SVB** | Traditional banking + venture debt | **Chartered bank** | Commercial treasury reporting; no self-serve API |
| **HSBC Innovation Banking** | Traditional banking, cross-border | **Chartered bank** | HSBCnet and commercial channels; no self-serve API |
| **Grasshopper Bank, N.A.** | Chartered digital bank | **Chartered bank** (being acquired by Enova, close expected H2 2026) | **Read only.** First US bank MCP server (with Narmi, 2025-08-20); first bank in Anthropic's directory (2026-07-14) |
| **Axos Bank** | Chartered digital bank | **Chartered bank** | Treasury APIs; no self-serve agent surface published |
| **Bluevine** | SMB fintech | Software plus sponsor bank (Coastal Community Bank) plus sweep | Limited API |
| **Relay** | SMB fintech | Software plus **middleware (Unit)** plus sponsor bank (Thread) plus sweep | Limited API |
| **Column** | Infrastructure | **Chartered bank sold as an API** | **Money movement**, including account opening |
| **Increase** | Infrastructure | **Chartered bank since 2026** (acquired Twin City Bancorp, relaunched 2026-07-30) | **Money movement**, including account opening |
| **Stripe** | Infrastructure + commerce | Software plus sponsor banks; Issuing and Treasury | **Money movement**, with an explicit human-confirmation gate on refunds and outbound payments |
| **Modern Treasury** | Payment ops software | Software only, over the banks you already have | **Money movement** instructions at your own banks |
| **Plaid** | Data connectivity | Software only | Read, plus Plaid Transfer; MCP exposes dashboard diagnostics only, not consumer financial data |

**How to read the map.** Rho occupies the only cell in the top-left quadrant that nobody else is defending: a software-plus-sponsor-bank stack with a deliberately read-only credential. Every other player in the startup banking and spend cohort has either moved right on the authority axis (Mercury, Brex, Ramp, Meow, Slash) or up the ownership axis (Mercury's charter application, Amex's existing one, Grasshopper's and Axos's charters), and several have done both.

Rho says read-only is a feature, and the architectural claim behind it is genuinely well-executed: "Most financial APIs predate agents; MCP got bolted on. This one shipped with its MCP server in production. Not a roadmap item, the architecture." **Verified:** Rho's MCP and REST surfaces do share one contract, one auth model and one scope set, and Rho pins tool names to frozen v1 operation IDs, a commitment almost nobody else makes.

**Assessment:** the safety framing is real but it is a narrowing position. The competitors who reached agent-initiated money movement did not get there by loosening a general-purpose credential. They built a second, narrower primitive that is structurally incapable of general money movement: Ramp's merchant- and amount-scoped Agent Cards, Mercury's agent cards with a vault reveal endpoint and hard-coded guardrails, Stripe's human-confirmation token with a 24-hour expiry. Rho has published no equivalent primitive and no dated roadmap beyond the blog line "Next, it acts on Rho: workflows, money movement with your approval." Until it does, "a leaked token cannot move money" reads to a technical buyer less like a security posture and more like an absent feature, and Rho's own read-only feed has a free substitute: a customer who wants Rho data in a third-party tool can authorize Plaid, Teller or Stripe Financial Connections and get the transaction feed for roughly $0.30 per account per month, paid by the tool vendor, with no cooperation from Rho at all.
