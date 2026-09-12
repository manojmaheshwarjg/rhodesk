# Spend / AP / T&E Incumbents Rho Displaces: 2026 Research Dossier

Research date: 2026-09-11. All web pages fetched or searched 2026-09-11 unless a different date is noted.
Local Rho corpus paths referenced as `pages/...` under `/private/tmp/claude-501/.../scratchpad/rho/`.

Labeling convention used throughout:
- **[Rho claim]** = asserted only by Rho marketing, not independently verified.
- **[Vendor published]** = taken from the vendor's own pricing or IR page on the date noted.
- **[Third-party]** = resale/benchmark/aggregator sites (Vendr, CostBench, Engine, CheckThat, VendorBenchmark). These are directionally useful but are themselves lead-gen content and should be treated as estimates, not contracts.

---

## 0. The structural thesis, stated precisely

The common framing ("they charge software fees and sit on top of a bank, Rho bundles software free and provides the account") is directionally right but is too coarse. The nine incumbents split into four genuinely different monetization structures, and only one of them is actually a bank.

| Structure | Who | How they get paid | Do they hold the money? | Do they issue the card? |
|---|---|---|---|---|
| **Pure software, touches no money** | SAP Concur, Coupa | Per-report / per-user / per-document subscription + implementation + annual escalators | No | No |
| **Software fee + payment rails take-rate + float** | BILL, Tipalti, Corpay, Airbase/Paylocity | Seat or platform subscription **plus** per-transaction fees **plus** FX spread **plus** interest on customer funds in transit | Yes (as money transmitter / in transit), pays customer nothing on it | Via partner banks (Cross River, WebBank, WEX Bank; Fifth Third for Corpay) |
| **Software fee subsidized by own-card interchange** | Expensify, Navan | Per-member subscription, explicitly discounted when the customer routes spend through the vendor's own card; plus booking fees (Navan) | No (partner issuers) | Via partner banks (Bancorp for Expensify; Celtic Bank/Stripe/Adyen for Navan) |
| **Actual bank that now also sells the software** | American Express | Card annual fees + program fees + interchange + net interest income, and since April 2025 an owned expense-management stack (Center) | **Yes** (American Express National Bank, FDIC member) | **Yes**, as issuer and network |

Rho's own structure, for contrast (from `pages/core/pricing.txt`, fetched 2026-09-11, Rho's fee summary): $0 same-day ACH / wires / checks, $0 subscription, $0 checking minimum, $0 for "Connected, in-platform capabilities: AP, Expense & Accounting Automation", $0 per-user fees, 1% foreign currency transfer, $0 domestic wire recall. Disclosed non-zero fees: $30 international wire recall, optional $15 SWIFT fee, 1% FX conversion, and a Rho Treasury advisory fee "which ranges from 0.15% for deposits of $20M or more to 0.6% (the maximum annual fee) for deposits under $2M" (`pages/core/pricing.txt`, as of 09/11/2026). Rho is not a bank; checking and cards are provided by Webster Bank, a division of Santander Bank, N.A.

**The sharpest true version of the structural claim:** the incumbents monetize the *workflow* (seats, reports, invoices, documents) and are indifferent to, or actively benefit from, the customer keeping deposits elsewhere. Rho monetizes the *balance* (interchange, deposit economics, 1% FX, treasury AUM fee) and gives the workflow away. The float number below is the cleanest evidence that the incumbents already earn balance economics too, while still charging seats.

**The float tell:** BILL earned **$148.4M of "float revenue, which consists of interest on funds held for customers"** in fiscal 2026 alone (BILL FY2026 results, 2026-08-19). BILL customers pay $49-$89 per user per month *and* $0.59 per ACH *and* hand BILL the interest on money in transit. That is three revenue lines off one workflow.

**The counter-nuance that weakens the simple "software fee" framing:** BILL is already mostly not a seat business. In FY2026, subscription fees were **$293.5M of $1,653.2M total revenue, 17.8%**; transaction fees were **$1,211.2M, 73.3%**; float was **$148.4M, 9.0%**. Navan is the same shape in reverse proportion: per its S-1, revenue mix was **~90% usage-based, ~10% subscription**. So the displacement argument against BILL and Navan is not primarily "you are paying seats"; it is "you are paying a take-rate on your own payments to a company that does not hold your account."

---

## 1. BILL (BILL Holdings, NYSE: BILL)

### Positioning (2026)
AP/AR automation plus Spend & Expense (the former Divvy). Explicitly repositioning around AI agents and a "do it for me" experience. CEO Rene Lacerte at the Goldman Sachs Communacopia + Technology Conference, **2026-09-10**: "pricing has to be tied to value creation," and BILL is "analyzing the levers we have...to change from just the subscription pricing model we have today to something that actually more closely matches...the value that we're creating." (https://www.investing.com/news/transcripts/bill-at-goldman-sachs-communacopia--technology-conference-2026-ai-push-93CH-4897043)

This is the single most important competitive datapoint in this dossier: **the largest seat-priced AP incumbent is publicly signaling it will move off seat pricing.**

### Pricing [Vendor published, https://www.bill.com/product/pricing, fetched 2026-09-11]

AP & AR, direct customers, per user per month:

| Plan | Price | What it adds |
|---|---|---|
| Essentials | **$49/user/mo** | Manual CSV integration only. Bill entry, approvals, vendor payments (ACH/card/check), centralized inbox, W-9 Agent, Invoice Coding Agent, standard approval policies, 6 standard user roles, AR invoicing |
| Team | **$65/user/mo** | Automatic 2-way sync with QuickBooks Online / Pro / Premier and Xero; custom user roles |
| Corporate | **$89/user/mo** | Custom approval policies, "discounts for approver-only users", procurement (purchase requests, POs, tolerance rules, 2-way matching) |
| Enterprise | **Custom** | QuickBooks Enterprise, NetSuite, Sage Intacct, Microsoft Dynamics, Acumatica, Rillet; 2-way and 3-way matching; SSO; dual control; multi-entity; API access; priority support |

Accountant partner pricing: **BILL AP & AR Partner $49/month**; **BILL Spend & Expense Partner $0**; wholesale client subscription pricing for resale with "10-20% additional discount based on client volume". Page carries an "as of March 2026" note on accountant partner statistics.

**Spend & Expense: $0 per user per month.** Unlimited physical/virtual cards, budgets with spend controls, AI expense management, mobile app, real-time transaction tracking, reimbursements, receipt capture/matching/coding, integrations, flexible rewards, API access, and "Access credit lines from $1000-$5M" (not guaranteed; application and approval required). BILL states Spend & Expense has "no subscription or per-user software fees."

**So BILL already gives the card+expense product away free and charges only for AP/AR.** Any pitch that says "BILL charges per seat for expense management" is factually wrong as of 2026-09-11. The seat fee is on AP/AR.

Payment fees (payor side), same page:

| Method / event | Fee |
|---|---|
| ACH / ePayment | **$0.59** |
| Check | **$1.99** |
| Virtual card | Free |
| International FX wire / local transfer | Free (FX rate applies) |
| International USD wire | **$19.99** |
| Instant Payment | **1.0%**, $9.99 minimum, $100 maximum |
| Pay Faster ACH | **$11.99** |
| Pay Faster Check: overnight / 2-day / 3-day | **$24.99 / $19.99 / $14.99** |
| Pay by credit or debit card (any disbursement) | **2.9%** |
| BILL Divvy Card virtual card disbursement | Free |
| Check void | $25.00 |
| Returned check void | $3.00 |
| Failed ACH after receiver payment | $50.00 |
| Re-debit after failed funding | $25.00 |
| 1099 e-file to IRS / via Accountant Console / state / mail | $2.99 / $1.99 / $1.49 / $1.99 per form |

Receiver-side: ACH $0.59; card 2.9%; international USD wire $19.99; **Instant Transfer 1%-1.49% ($1 minimum)**; mailed invoice $1.99.

### Financials [Vendor IR, press release dated 2026-08-19]
https://investor.bill.com/news/news-details/2026/BILL-Reports-Fourth-Quarter-and-Fiscal-Year-2026-Financial-Results/default.aspx

Q4 FY2026 (quarter ended 2026-06-30):
- Total revenue **$436.2M, +14% YoY**
- Core revenue (subscription + transaction) **$400.5M, +16% YoY**
- Subscription fees **$76.2M, +11% YoY**
- Transaction fees **$324.3M, +17% YoY**
- Float revenue **$35.7M**
- Total Payment Volume **$98.2B**; **37 million transactions**; **479,300 businesses** using BILL solutions
- Net loss **$18.5M, or $0.19 per share**

Full-year FY2026 (ended 2026-06-30):
- Total revenue **$1,653.2M, +13% YoY**
- Core revenue **$1,504.7M, +16% YoY**
- Subscription fees **$293.5M, +8% YoY**
- Transaction fees **$1,211.2M, +18% YoY**
- Float revenue **$148.4M**
- Gross profit **$1,337.9M, 80.9% gross margin** (prior year $1,190.5M, 81.4%)
- Operating loss **$73.4M** (prior year operating loss $80.6M)
- Net loss **$11.2M, or $0.11 per share**

Note the divergence: subscription fees grew only 8% while transaction fees grew 18%. Seats are the slow half of BILL.

### AI agent adoption [Goldman Sachs conference, 2026-09-10]
- W-9 Agent: **40,000 customers**, **240,000+ W-9 forms collected**
- Invoice Coding Agent: **60,000 customers**
- Touchless Transaction Agent: **30,000 customers** (Spend & Expense side)
- Pay-for-You agents: **30,000 customers**
- **20+ internal risk agents handling ~95% of risk decisions**, "prevented close to $90 million in annual fraud losses"
- Automated customer touchpoints rose from **10% a year prior to over 50%**
- Joint (multi-product) customer adoption **+35% YoY**; multi-product customers at **111% net revenue retention**
- BILL manages **close to $400 billion in annual spend, ~$2 trillion cumulatively**

### 2025-2026 trajectory: under siege from activists, possibly for sale
- **Late September 2025:** Starboard Value disclosed an **8.5% stake** and called for board changes. (https://www.paymentsdive.com/news/activist-investor-targets-bill-performance-Starboard-accounting-software/759578/)
- Elliott Investment Management also reported to have built a stake.
- **October 2025:** BILL agreed to add **four new directors, two proposed by Starboard**.
- **December (2025):** **Barington Capital Group** wrote to directors urging cost cuts and to find a buyer. (https://baptistaresearch.com/barington-pushes-bill-holdings-sale/)
- **2026-05-07:** Q3 FY2026 results announced alongside a **$1.0 billion share repurchase authorization**. (https://investor.bill.com/news/news-details/2026/BILL-Reports-Third-Quarter-Fiscal-Year-2026-Financial-Results-and-Announces-1-0-Billion-Share-Repurchase-Authorization/default.aspx)
- BILL reported to be **reviewing strategic alternatives**, roughly four months after the activist agreement; **Hellman & Friedman** reported to have held acquisition talks. (https://www.paymentsdive.com/news/bill-weighs-the-best-path-to-profits/812067/)

### Bank relationship
BILL is **not a bank**. It is a money transmitter that holds customer funds in transit (hence $148.4M float revenue). BILL Divvy Cards are issued by DivvyPay, LLC's bank partners: **Cross River Bank** (NJ state chartered, FDIC), **WebBank**, and **WEX Bank** (UT state chartered, FDIC); the majority are Cross River and WEX. (https://www.bill.com/blog/bill-divvy-card-requirements; https://www.crossriver.com/divvy-case-study)

### What BILL does NOT include
No business checking account. No treasury / yield product for the customer (BILL keeps the float). No FX hedging. Procurement is a Corporate-tier or add-on feature, not standard. The AR side is invoicing only, not a full billing system.

---

## 2. Navan (Nasdaq: NAVN)

### Positioning (2026)
Travel + expense, with the distinguishing feature being **card-agnosticism**: Navan Connect lets a company keep its existing Visa, Mastercard, or American Express corporate card and layer Navan's expense automation on top. This is the exact inverse of Rho's structure. Navan explicitly does **not** want to be your bank; it wants to sit on top of whatever bank you already have.

### Pricing [Vendor published, https://navan.com/pricing, fetched 2026-09-11]

| Plan | Target | Price |
|---|---|---|
| Navan Business | Companies **up to 300 employees** | **Free** for travel (unlimited trips at no cost). Expense: **free for the first 5 users, then $15 per user per month** |
| Navan Enterprise | Large organizations (300+) | **Custom quote** |

Definition on the page: an **"active expense user"** is "anyone who submits a transaction into Navan expense by manual transaction or Navan Connect."

No per-trip fee is published. Navan monetizes the Business tier through "travel providers' commission fees."

**Contradiction with Rho's corpus:** Rho's `blog__sap-concur-alternatives.txt` and `blog__bill-spend-and-expense-alternatives.txt` (both "Last Updated August 20, 2026") say "Navan Business: Free plan for companies up to 200 employees" / "Free for companies up to 200 employees." Navan's own page says **300**. Rho's number is stale or wrong. Rho also omits the **$15/user/month** expense charge entirely in both posts, describing Navan Business simply as "free ... includes travel and expense features."

### Navan Connect mechanics
Navan Connect enrolls **existing Visa, Mastercard, and American Express corporate cards from more than 250 banks**; the company keeps its current card program, rewards, and benefits, and does not apply for a new card. Transactions flow into Navan for categorization, policy checks, and reconciliation. **Visa and Mastercard transactions report in real time; American Express transactions report daily.** (https://navan.com/blog/navan-connect-next-gen-fintech; https://www.businesstravelnews.com/Payment-Expense/Navan-Connects-Expense-Features-to-Visa-Mastercard-Corp-Cards; Navan Connect launched June 2023 per https://skift.com/2023/06/12/navan-moves-beyond-its-own-smart-card-in-link-up-with-visa-and-mastercard/)

The Navan Card itself is issued by **Celtic Bank (Member FDIC)** in the US, and by Stripe Technology Europe Limited / Stripe Payments UK Limited / Adyen N.V. entities in the EU and UK.

### Financials
S-1 (filed 2025-09-19, https://www.sec.gov/Archives/edgar/data/1639723/000162828025042130/navan-sx1.htm; summarized at https://www.mostlymetrics.com/p/navan-ipo-s1-breakdown):
- FY2024 revenue **$402M** -> FY2025 revenue **$537M, +33% YoY**
- FY2024 net loss **$332M** -> FY2025 net loss **$181M, -45% YoY**
- Gross booking volume **$5.0B (FY2024) -> $6.6B (FY2025), +32%**
- Revenue mix **~90% usage-based** (per-booking and supplier/partner transaction fees) and **~10% subscription** (expense)
- **Usage yield ~7%** in both FY2025 and FY2024
- Revenue lines: travel booking fees and commissions, software subscriptions (Expense free for five users then $15/user/mo), and **card interchange from both the Navan Card and BYO-card via Navan Connect**

IPO: **2025-10-30**, Nasdaq **NAVN**, priced at **$25/share**, raised **~$923M**, valuation **~$6.2B**. Closed first day **down 20% at $20**. (https://news.crunchbase.com/public/navan-ipo-debut-down-nasdaq-navn/; https://capital.com/en-int/learn/ipo/navan-ipo)

FY2026 (year ended 2026-01-31), reported **2026-03-25** (https://investors.navan.com/news-releases/news-release-details/navan-announces-fourth-quarter-and-full-fiscal-year-2026-results):
- Revenue **$702.3M, +31% YoY**
- Gross booking volume **$9.1B, +38% YoY**
- Net loss **$(398.0)M**, widened from $(181.1)M, including **$117.98M loss on extinguishment of debt** and **$47.04M fair value losses**
- EPS **$(4.07)**
- **$34M cash flow from operations, $15M free cash flow** - first full year of positive cash flow, "one year ahead of target"

Q1 FY2027 (reported 2026-06-10): GBV **+50% YoY**; GAAP loss from operations **$18M** (vs $16M in Q1 FY2026); GAAP operating margin **(8)%** (vs (10)%).

Q2 FY2027 (reported ~2026-09): revenue **$232.8M, +35% YoY**, beating consensus of $220.5M; net loss **$29.1M**; GBV **$3.0B, +45% YoY**. Shares fell **11%** on guidance. (https://www.stocktitan.net/news/NAVN/navan-announces-strong-second-quarter-fiscal-year-2027-u2pzpx12w2cb.html; https://www.investing.com/news/company-news/navan-q2-fy27-slides-35-revenue-growth-ai-drives-margins-93CH-4894707)

### What Navan does NOT include
No business checking account. No AP/bill pay for vendor invoices (it is T&E, not AP). No treasury. It does not want your deposits; Navan Connect is explicitly designed so "finance keeps its banking relationship."

### Competitive read vs Rho
Navan is the clearest *non*-overlap on this list. A company can run Rho cards and banking and still use Navan for travel: Rho publishes a Navan integration (`site-llms-full.txt` line 130 lists Navan under "HR and T&E" integrations). Navan is a displacement target only for the expense-report half, and only where the customer would otherwise pay $15/user/month.

---

## 3. American Express (Business and Corporate)

### Positioning (2026)
The only incumbent on this list that is itself an FDIC-insured bank, and since 2025 the only one that has bought its way into owning the expense-management software layer rather than partnering for it.

### The acquisition that matters: Center
- **2025-03-06:** Amex announced an agreement to acquire **Center**, "a software company modernizing expense management," founded 2017, headquartered in Bellevue, WA, offering "an integrated corporate card, expense management, and travel solution." (https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2025/American-Express-to-Acquire-Expense-Management-Software-Company-Center/default.aspx; https://www.businesswire.com/news/home/20250306154813/en/American-Express-to-Acquire-Expense-Management-Software-Company-Center)
- **2025-04-16:** Acquisition **completed**. (https://ir.americanexpress.com/news/investor-relations-news/investor-relations-news-details/2025/American-Express-Completes-Acquisition-of-Center/default.aspx)
- Stated rationale: combine Center's software with Amex corporate and small business cards to create "a seamless expense management platform ... from choice in premium card offerings and rewards to automated accounting and reconciliation," with Center customers reportedly freeing up "an average of 90% of the time previously spent" on review/audit/GL posting.
- Terms not disclosed in the announcements found.

Center also appears in Rho's own corpus as a BILL alternative (`pages/blogcomp/blog__bill-spend-and-expense-alternatives.txt`, "Last Updated August 20, 2026"), described with its original independent pricing model ("no upfront investment or licensing fees, with costs covered by merchant fees and flat fees for corporate travel bookings"). **Rho's post does not mention that Center is now owned by American Express.** That is a stale-content gap in Rho's own marketing.

### Pricing: card fees, not software fees

| Product | Fee | Source / date |
|---|---|---|
| Business Platinum Card | **$895/year**, raised from $695 in the **September 2025** refresh (+$200) | https://upgradedpoints.com/credit-cards/reviews/amex-business-platinum/annual-fee-history/; https://secure.businesswire.com/news/home/20250918170606/en/ (2025-09-18) |
| Business Gold Card | **$375/year**, raised February 2024 | https://upgradedpoints.com/credit-cards/reviews/american-express-business-gold-card/annual-fee-history/ |
| Corporate Card | **$90 annual program fee** to enroll | [Third-party] https://wallethub.com/edu/cc/amex-corporate-card-benefits/151409 |
| Corporate Green Card | **$55 annual enrollment fee** | [Third-party] americanexpress.com corporate benefit-terms pages |
| Corporate Gold Card, Corporate Platinum Card | **No program fee applied** | [Third-party], same |

**Amex charges no per-seat software fee.** It charges per-card annual fees. For a 50-person company issuing 50 Corporate Cards at $90, that is $4,500/year; for 10 Business Platinum cards, $8,950/year. Rho's `pages/core/versus__amex.txt` fixes on the $895 Business Platinum fee and compares it to Rho's $0 annual fee, which is a fair like-for-like on the premium consumer-facing business card and an unfair one against the Corporate Card program.

### Amex as a bank
- **American Express National Bank, Member FDIC**, offers **Business Checking**: **1.30% APY on balances up to $500,000**, **no monthly fee**, no minimum balance requirement, 24/7 live support, fee-free ATM network. APY is variable. (https://www.americanexpress.com/en-us/business/checking/; [Third-party] https://www.bestmoney.com/online-banking/compare-business-checking/reviews/american-express-business-checking)
- **American Express Business Line of Credit** (formerly Kabbage, issued by American Express National Bank): limits **$2,000-$250,000**; instead of interest, a **flat monthly fee per draw of 0.25%-3.5%**; total fees over term **3%-9% (6-month), 6%-18% (12-month), 9%-27% (18-month), 12%-18% (24-month)**; minimum credit score **660**. (https://www.forbes.com/advisor/business-loans/american-express-business-blueprint-review/; https://www.finder.com/business-loans/american-express-business-line-of-credit-review) **Note contradiction:** the 24-month range (12%-18%) is lower than the 18-month range (9%-27%) in the same source set, which is internally inconsistent; treat the term-fee ladder as approximate.
- An older CNBC review cites Kabbage Checking at **1.10% APY on balances up to $100,000**, superseded by the 1.30%/$500k figure above.

This makes Amex the **structurally hardest** competitor for Rho's "we provide the account" argument: Amex already provides the account, already is the bank, and as of April 2025 already owns the software. The gap Rho can attack against Amex is not the bank-vs-fintech axis, it is (a) annual card fees, (b) points-vs-cashback, (c) real-time spend controls and direct-to-GL data, all of which `versus__amex.txt` does attack.

### Financials [Amex Q2 2026, reported 2026-07-24]
https://s26.q4cdn.com/747928648/files/doc_earnings/2026/q2/earnings-result/Q2-2026-Earnings-Press-Release.pdf; https://www.sec.gov/Archives/edgar/data/0000004962/000000496226000322/axp-20260630.htm
- **Commercial Services** segment: total revenues net of interest expense after provisions for credit losses **$4,149M in Q2 2026** vs **$3,852M in Q2 2025**; pretax segment income **$970M** vs **$905M**, **+7% YoY**
- **0.8 million** new proprietary Commercial Services cards acquired in Q2 2026
- Company-wide revenue **+10% YoY**, fourth consecutive quarter of double-digit growth
- Amex transferred two small-business portfolios "not very large and not contributing to earnings," creating **~1% headwind to billed business**

Segment description per the 10-Q: "Commercial Services issues a wide range of proprietary corporate and small business cards and provides services to U.S. businesses, including payment and expense management, **banking** and non-card financing products."

### What Amex does NOT include
No AP automation for non-card vendor payments at scale (Amex partners rather than owns here; note **Melio was acquired by Xero, not Amex**, see Section 10). Historically weak real-time programmatic spend controls and GL enrichment versus fintech issuers, which is the gap Center was bought to close. No multi-bank treasury sweep product.

---

## 4. Expensify (Nasdaq: EXFY)

### Positioning (2026)
Down-market expense management, mid-transition from "Classic Expensify" to "New Expensify" (a chat-native superapp bundling expense, corporate card, travel via Spotnana, bill pay, invoicing, and chat). Revenue is shrinking; the company is now cash-generative and buying back stock.

### Pricing

| Plan | Price | Conditions |
|---|---|---|
| Free | **$0** | Individual expense tracking only. "Expensify is completely free to use as an individual." (https://www.expensify.com/, 2026-09-11) |
| **Collect** | **$5 per member per month, flat** | Month-to-month, no annual commitment required. Introduced **April 2025**; the flat rate applies to workspaces created **on or after 2025-04-01**. (https://ir.expensify.com/news-releases/news-release-details/expensify-launches-simplified-5-pricing-plan-smbs; https://use.expensify.com/blog/collect-plan-pricing-update) |
| **Control**, annual + Expensify Card + >=50% US spend on card | **$9 per member per month** | Requires all three simultaneously: 12-month commitment, Expensify Card enabled, and "at least 50% of your total settled US spending for the month must flow through the Expensify Card" |
| **Control**, annual, **no** Expensify Card / threshold missed | **$18 per member per month** | The published rate **doubles** |
| **Control**, pay-per-use (month-to-month) | **$36 per member per month** | |

[Third-party consolidation of the above: https://checkthat.ai/brands/expensify/pricing, fetched 2026-09-11; corroborated by https://www.trustradius.com/products/expensify/pricing and https://www.g2.com/products/expensify/pricing]

**This is the single cleanest example of the structure Rho attacks.** Expensify publishes a software price and then cuts it by 50% if you hand it your card interchange. If you keep your existing bank's card, you pay **$18/member/month**, which is **2x** the headline. The software fee is explicitly a lever to capture the payment flow.

Other Expensify fees:
- Expensify Card cashback: **1% on US purchases; 2% when monthly spend reaches $250,000+**. Cashback applies first as a subscription credit, excess paid by ACH.
- Bill pay by credit/debit card: **2.9%**. Bill pay via Venmo: **3%** (Venmo's fee).
- No annual fee on the Expensify Card itself.
- ACH reimbursements included in the subscription.

### Financials [Q2 2026, released 2026-08-06]
https://investors.expensify.com/news-releases/news-release-details/expensify-announces-q2-2026-results; transcript https://www.fool.com/earnings/call-transcripts/2026/08/13/expensify-exfy-q2-2026-earnings-call-transcript/
- Revenue **$33.9M**; **net revenue decreased 5% YoY**
- **640,000 average paid members**
- **Card interchange revenue $5.9M, +12% YoY**
- Net loss **$3.9M**, improved from **$8.8M** a year prior
- Non-GAAP net income **$3.4M**; adjusted EBITDA **$6.6M**, both up from losses
- Gross margin **48%** (as reported in coverage; unusually low for this business, treat with caution)
- Operating cash flow **$8.4M**; free cash flow **$6.4M, +2% YoY, +162% sequentially, 19% margin**
- **New Expensify ARR from net new customers grew over 250% YoY to $10M**
- **7% share reduction** disclosed in the accompanying 8-K (https://www.stocktitan.net/sec-filings/EXFY/8-k-expensify-inc-reports-material-event-734834352ddc.html)

Prior comparator: Q4 2025 total revenue **$35.2M, down 5% YoY**; paid members **650,000, down 5% YoY**. (https://www.businesstravelnews.com/Payment-Expense/Expensify-Sees-Growth-in-Travel-Payment-Offerings-in-Q4)

**Read:** Expensify is a shrinking seat business ($33.9M revenue, -5%) with a growing interchange business ($5.9M, +12%). Interchange is now **17.4% of revenue**. The company is executing the same pivot Rho already lives on, but from a much weaker starting balance sheet and without a bank account product.

### 2025-2026 product moves
- **2026-07-20:** **Expensify Card launched in Europe**, "available to businesses of all sizes." (https://www.businesswire.com/news/home/20260720653615/en/Expensify-Launches-Corporate-Card-in-Europe)
- **July 2026:** **Consolidated travel billing** launched, letting companies "centrally manage travel spend without issuing corporate cards to every traveler or relying on employee reimbursements" and pay for flights, hotels, cars, and rail in one monthly bill. (https://ir.expensify.com/news-releases/news-release-details/expensify-launches-consolidated-travel-billing-simplify-how)
- Awards: TrustRadius Buyer's Choice 2026; "Expense Management Platform of the Year," 2026 TravelTech Breakthrough Awards.

### Bank relationship
Not a bank. **Expensify Visa Commercial Card is issued by The Bancorp Bank, N.A.** under license from Visa U.S.A. Inc. for US customers; by **Transact Payments Malta Limited** (EEA) and **Transact Payments Limited** (UK). The travel platform is provided by **Spotnana Technology, Inc.** (https://www.expensify.com/commercialcardprogramterms; https://card.expensify.com/travelterms)

### What Expensify does NOT include
No business checking. No treasury/yield. No credit line or working capital. Bill pay exists but priced punitively for card funding (2.9%). Enterprise ERP (NetSuite, Sage Intacct) requires the Control plan.

### Rho's coverage gap
Rho's `blog__bill-spend-and-expense-alternatives.txt` (Last Updated 2026-08-20) states: **"Expensify's pricing is not public. Contact their support for more info."** That is false as of 2026-09-11; Expensify publishes $5 / $9 / $18 / $36. Rho's `blog__sap-concur-alternatives.txt` lists Expensify tiers as "Individual / Group / Corporate," which is the **pre-2023** naming. Both posts are stale.

---

## 5. SAP Concur

### Positioning (2026)
The enterprise T&E default, still the market-share leader by a wide margin, aggressively repositioning around agentic AI and around **partnering with card issuers rather than becoming one**.

**Market share:** SAP ranked **#1 for Worldwide Travel and Expense Management Software with 48.1% 2025 market share** per IDC, cited in SAP's own 2026 communications. (https://news.sap.com/2026/03/sap-concur-fusion-2026-ai-capabilities-integrated-travel-expense-enhancements-global-partnerships/)

### Pricing [Vendor published, https://www.concur.com/about/pricing, fetched 2026-09-11]

Concur publishes **per-report** pricing, not per-user, and advertises **unlimited users** on all three plans:

| Plan | Published price | Notes |
|---|---|---|
| Base | **"Starting at $7 per report"** | Smaller businesses, basic expense reporting |
| Plus | **"Starting at $11 per report"** | Adds AI-powered features |
| Premium | **Custom pricing** | No starting price disclosed |

The page does **not** separately publish pricing for Concur Travel or Concur Invoice; only bundled per-report plans. Buyers must "Request a quote" or contact sales for Premium.

[Third-party] real-world enterprise economics, which diverge sharply from the published SMB rate card:

| Line item | Range | Source |
|---|---|---|
| Concur Expense | **$9-$24 per active user per month**, or **$5-$12 per report** in mid-market deals | https://costbench.com/software/expense-management/sap-concur/; https://atonementlicensing.com/blog/sap-concur-pricing-2026/ |
| Concur Travel | **$3-$8 per active user**; per-transaction **$15-$25 air, $8-$15 hotel, $5-$10 car** | same |
| Concur Invoice | **$3.50 per document with a $30K minimum**; or $2-$8 per invoice by volume tier | same |
| Implementation, Concur Standard | **$15,000-$40,000**, 4-8 weeks | https://vendorbenchmark.com/vendors/concur-sap-pricing |
| Implementation, Concur Professional | **$80,000-$350,000**, 12-24 weeks | same |
| Professional services generally | **$10,000-$100,000+**, typically **20-50% of first-year subscription value** | https://engine.com/blog/sap-concur-pricing |
| Annual transaction minimums | typically set **20-35% above actual volume** (buyers prepay for unused transactions) | same |
| Annual escalators | **5-8%** | https://vendorbenchmark.com/vendors/concur-sap-pricing |
| Median annual contract value | **$9,859** | https://www.vendr.com/marketplace/concur |

**The per-report model is the structural oddity worth emphasizing.** Concur charges for the artifact of the legacy workflow (the expense report). Rho's product thesis is that the expense report should not exist. From Rho's own expense positioning: "Eliminates the need for traditional expense reports by capturing every receipt automatically" (`pages/blogcomp/blog__bill-spend-and-expense-alternatives.txt`). If reports go to zero, Concur's Base/Plus revenue goes to zero. That is a genuinely sharp wedge.

### 2026 trajectory: partnering with card issuers, not replacing them
At SAP Concur Fusion 2026 (announced **2026-03-25**) and at GBTA Convention 2026:
- **AI-Assisted Delegates Dashboard**, consolidating approvals, bookings, and reports; SAP claims "up to 25% reduction in hours spent resolving issues"
- **Microsoft integration**: create/submit expense reports, upload receipts, book travel, get policy guidance without leaving Microsoft apps
- **American Express partnership**: joint customers "can now create and manage American Express Virtual Cards in Concur Expense"
- **Visa partnership**: Concur Expense integrated with Visa through the **Visa Commercial Integrated Partner program**
(https://news.sap.com/2026/03/sap-concur-fusion-2026-ai-capabilities-integrated-travel-expense-enhancements-global-partnerships/; https://itnerd.blog/2026/03/25/sap-showcases-new-ai-integrated-travel-and-expense-enhancements-and-global-partnerships-at-sap-concur-fusion-2026/)

### Bank relationship
**None.** Concur issues no card, holds no funds, has no charter, earns no float and no interchange. It is the purest example of the "software fee on top of someone else's bank" structure. Its money-movement partners are Amex and Visa.

### What Concur does NOT include
No bank account, no card, no credit, no treasury, no float pass-through, no interchange rebate to the customer. Pricing is not transparent above the SMB tier. Implementation is a separate six-figure line item at Professional scale.

### Note: Rho and Concur coexist
Rho publishes a **SAP Concur integration** (`pages/core/integrations__sap-concur.txt`): "Bring your Rho card and experience the magic of automated expense management ... Once you swipe your connected Rho Corporate Card, SAP Concur goes to work." Rho also integrates with **Emburse** (`pages/core/integrations__emburse.txt`) with copy that is a near-verbatim clone of the Concur page, including a copy-paste error: the Concur page reads **"Connect Emburse with Rho Corporate Cards"** in its body. So Rho simultaneously sells against Concur in the blog and supports it in the product. That is a coexistence posture, not a pure displacement posture.

---

## 6. Tipalti

### Positioning (2026)
Global AP automation and mass payouts for mid-market, strongest on cross-border (200+ countries and territories, 120+ currencies, 50+ payment methods per Rho's summary in `pages/blogcomp/blog__tipalti-reviews.txt`) and on supplier tax compliance (W-9, W-8, 1099, e-filing, withholding). Private, Foster City CA, founded 2010, CEO **Chen Amit**.

### Pricing [Vendor published, https://tipalti.com/pricing/, fetched 2026-09-11]

| Product | Published price | What's stated |
|---|---|---|
| Tipalti Accounts Payable | **Starting at $99/month** | "unlimited users," self-service supplier portal, core automation |
| Tipalti Mass Payments | **Starting at $249/month** | "unlimited users," payee portal, core automation |

Both plans additionally charge, per the vendor's own page:
- **Transaction pricing** per invoice and per payment
- **Module expansion fees** for Procurement, Expenses, Treasury
- **Professional services** for complex implementations

The page explicitly declines to give amounts: "For your custom quote, reach out to our sales team," and the FAQ confirms pricing varies by payment volume, number of entities, enabled modules, and global payment methods.

**Tipalti is the one vendor here whose published price is deliberately a floor, not a price.** Unlimited users at $99/month sounds like the anti-seat model; the real bill is the transaction and FX layer underneath.

[Third-party] estimated real cost structure:

| Line item | Range | Source |
|---|---|---|
| Plan tiers (alt naming) | Select **$99/mo**, Advanced **$199/mo**, Elevate custom | https://costbench.com/software/accounts-payable/tipalti/ |
| Implementation / setup | **$4,000-$5,000**; all plans require a setup fee | https://checkthat.ai/brands/tipalti/pricing |
| Per-payment transaction fee | **$0.20-$36 per payment** | https://multientityaccounting.com/tipalti-pricing-multi-entity/ |
| US ACH | **$0.50-$2.00** (high volume near $0.50-$1.00); another source **~$1.00-$1.15** | same; https://www.erp-information.com/tipalti |
| Domestic wire | **$10-$25**, detailed as **$15.00-$17.25** | same |
| International SWIFT wire | **$26**, range **$20.00-$29.90** | same |
| FX markup | **1.9%-3.5%** for Multi-FX subscribers (under $500 ~3%; over $100,000 ~1.9%); **1.5%-3%** without the subscription | https://multientityaccounting.com/tipalti-pricing-multi-entity/ |
| Additional legal entity | **$500-$600/month per additional entity** | same |
| Typical all-in annual cost, smaller deployments | **$20,000-$45,000** | https://checkthat.ai/brands/tipalti/pricing |
| Share of spend that is transaction+FX rather than platform fee | **50-70%** of what mid-market companies actually pay annually | https://multientityaccounting.com/tipalti-pricing-multi-entity/ |

Compare directly: **Tipalti's 1.9%-3.5% FX markup vs Rho's published 1% foreign currency transfer fee** (`pages/core/pricing.txt`). On $5M of annual cross-border payables, that is a spread of **$45,000 to $125,000 per year** in Rho's favor, before any subscription. This is the single most quantifiable displacement argument in the dossier, though it is an apples-to-oranges comparison in coverage: Rho's international payments are provided by **Wise US Inc.** and Rho does not claim 200-country / 120-currency / 50-method coverage or automated global tax withholding.

### Business trajectory
- **ARR: crossed $200M**; **$75B annual payment volume, +30% YoY**; **~5,000 customers globally**. (https://getlatka.com/companies/tipalti; https://geo.sig.ai/brands/tipalti)
- Total funding **$749M across 8 rounds**; most recent a **$200M debt financing in 2025** (https://tipalti.com/press/tipalti-growth-financing-ai-innovation/). Valuation **$8.3B** (PitchBook/Tracxn; this is a 2021-vintage mark and should be treated as stale).
- Headcount **~1,200 in 2026**, down from **~1,300 in 2024**.
- **Three layoff events, 224 employees total**: **123 in early 2023**; a round announced **2025-07-24** affecting "dozens" (https://www.cpapracticeadvisor.com/2025/07/24/tipalti-job-cuts-affect-dozens-of-employees/165531/); and **100 employees on 2026-01-15, ~8% of global workforce** (https://www.interviewpal.com/layoffs/tipalti; https://layoffs.fyi/company/tipalti/).
- President **Rob Israch**, in a **2026-06-16** interview, said Tipalti expects **sustained profitability by early 2027**, which is "one of the gating factors for us to go IPO in the future, of course." (https://www.paymentsdive.com/news/tipalti-counts-on-future-ipo-ai-finance-automation-software/823594/)

**Contradiction to flag:** https://www.techstackipo.com/ipo/tipalti claims "S-1 Filed" and dates it **2026-03-12**. This is directly inconsistent with the president's June 2026 statement that profitability in early 2027 is a gating factor for an IPO "in the future." The techstackipo claim is from a low-quality aggregator and is **not corroborated** by any primary source found. Do not carry the S-1 claim forward without SEC EDGAR verification.

### Bank relationship
Not a bank. Tipalti moves money through partner rails and holds funds in transit. No card issuing of its own beyond the Tipalti Card (an add-on module), no deposit product, no yield.

### What Tipalti does NOT include
Rho's own critique in `blog__tipalti-reviews.txt` ("Last Updated August 20, 2026"): "Businesses that experience rapid growth may outgrow the platform as it needs capabilities like banking, treasury management, and other spend management functionality offered by different solutions." [Rho claim, but structurally accurate.] Also flagged by Rho from third-party reviews: implementations "can take months, regardless of company size"; "limited" reporting; slow support.

---

## 7. Airbase (now Paylocity)

### The acquisition
- **2024-09-04:** Paylocity announced a definitive agreement to acquire **Airbase Inc.** for **~$325 million**, subject to customary adjustments, **funded by borrowings under Paylocity's revolving credit facility**. Expected to close in **Q1 or Q2 of Paylocity's fiscal 2025**. Expected to represent **~1% of total revenue in fiscal 2025** and to **dilute adjusted EBITDA margin by ~100 basis points in fiscal 2025**. (https://investors.paylocity.com/news-releases/news-release-details/paylocity-announces-definitive-agreement-acquire-airbase-inc; https://www.globenewswire.com/news-release/2024/09/04/2940893/0/en/; https://techcrunch.com/2024/09/04/paylocity-acquiring-corporate-spend-startup-airbase-for-325m)
- **October 2024:** deal closed.
- Stated rationale: expand Paylocity's suite "into the Office of the CFO," fusing HCM real-time employee and payroll data with Airbase bill pay, expense management, corporate cards, and procurement into "a single pane of glass for total operational spend."

### Rebrand and product state
- Rebranded first as **"Airbase by Paylocity."**
- **July 2025:** Paylocity launched **"Paylocity for Finance"** as the integrated spend suite inside HCM, with v1 delivering core modules (AP automation, expenses, cards). (https://www.paylocity.com/company/about-us/newsroom/press-releases/; https://work-management.org/accounting/paylocity-for-finance-review/)
- Current scope: AP automation, bill payments, expense management, corporate cards, guided procurement, vendor management, accounting automation.

### Pricing
- **Pre-acquisition Airbase:** three tiers, **Standard / Premium / Enterprise**. [Third-party] typical **$12-$18 per user per month with volume discounts**; enterprise contracts "typically start at 500+ users with multi-year terms"; estimated annual cost **$18,500-$35,700 for up to 200 employees** and **$45,500-$88,100 for 1,000+ employees**. (https://findstack.com/products/airbase/pricing; https://www.capterra.com/p/185823/Airbase/pricing/)
- **Post-acquisition:** "There is no public pricing, and pricing is sold as part of Paylocity quotes." Paylocity for Finance "uses custom pricing that depends on your selected modules, company size, implementation scope, payment workflows, and integration needs."
- For reference, Paylocity's core HCM is quoted [Third-party] at roughly **$20 / $30 / $40 per user per month** (Core / Professional / Enterprise), which is a separate line from the Finance modules. (https://costbench.com/software/hr/paylocity/)

### Why this matters to the displacement story
Airbase was the closest structural analog to Rho among the pure-software players: one platform for cards, AP, expenses, and procurement, priced per seat. It did **not** survive as an independent. It was bought for **$325M** (a fraction of Ramp's or Brex's marks) and folded into a payroll vendor, and its pricing disappeared behind an HCM quote. **The lesson Rho can point to: per-seat spend management without a balance sheet had no standalone endgame.** [Interpretation, not a sourced claim.]

### Bank relationship
None of its own. Airbase cards were issued through partner banks; post-acquisition the card program sits inside Paylocity. No deposit product, no yield.

### Rho's coverage
Rho maintains `blog__airbase-vs-brex.txt`, `blog__airbase-vs-ramp.txt`, and an Airbase Alternatives post (`site-llms-full.txt` line 98). Spot-check of these files shows **no mention of the Paylocity acquisition**, which closed almost two years before the corpus's "Last Updated" dates. Another stale-content gap.

---

## 8. Coupa

### Positioning (2026)
Enterprise Business Spend Management (source-to-pay, procurement, invoicing, payments, supply chain), private equity owned, now pivoting hard to agentic AI. This is the highest-ACV, furthest-upmarket vendor on the list and the **least** overlapping with Rho's SMB/startup/mid-market base.

### Ownership and financials
- **February 2023:** **Thoma Bravo completed** the acquisition of Coupa in an all-cash transaction valued at **~$8.0 billion**. (https://www.coupa.com/newsroom/thoma-bravo-completes-acquisition-coupa-software/)
- **Over $1 billion in billings** disclosed in the 2024 Total Spend Management Benchmark Report. (https://www.prnewswire.com/news-releases/coupa-delivers-over-1-billion-in-billings-unlocks-175-billion-in-bottom-line-impact-for-global-customers-302063501.html)
- Stated goal in 2024: go from **$1B ARR to $2B ARR in three years**.
- **Q2 FY26 (May-July 2025), press release dated 2025-09-03/2025-09-10:** **$421B USD moved through the Coupa platform** in the quarter; **$14B USD in customer savings** in the quarter; **$273B USD cumulative** customer savings; **190+ new organizations** initiated or expanded; **~3,100 total organizations** in the Coupa community; new logos included Nvidia, Marriott, Honeywell, CoreWeave, GAP Inc. **The release titled "Coupa Continues ARR Growth Trajectory" discloses no actual ARR figure, growth rate, or Coupa Pay volume.** (https://www.prnewswire.com/news-releases/coupa-continues-arr-growth-trajectory-in-q2-fy26-302545066.html)
- Dataset claims escalated over time: **"$8 trillion dataset"** in 2025 messaging, **"nearly $10 trillion in global spend across more than 11 million buyers and suppliers"** in 2026 messaging. Also stated as "a network of 10M+ buyers and suppliers."

### Leadership churn
- **Leagh Turner** became CEO in **November 2023**.
- **2026-08-24:** Coupa announced Turner "is stepping away from the business as Chief Executive Officer for personal reasons." **Mike Lipps**, a **Thoma Bravo Operating Partner**, named **interim CEO**. Lipps previously ran insightsoftware and Intelerad Medical Systems, led a LexisNexis division, and spent 14 years at Intuit including running QuickBooks. (https://www.coupa.com/newsroom/coupa-appoints-mike-lipps-as-interim-ceo/; https://procurementmag.com/news/coupa-ceo-leagh-turner-steps-down)

An interim CEO who is a Thoma Bravo operating partner and a noted M&A operator is a standard pre-transaction posture. [Interpretation.]

### 2026 product
- **2026-05-12, Inspire 2026, Las Vegas:** launched **Coupa Compose** ("a comprehensive environment to build, manage, and orchestrate a digital workforce of AI agents") and **Coupa Catalyst** (AI transformation services). (https://www.prnewswire.com/news-releases/coupa-launches-coupa-compose-and-catalyst-to-accelerate-agentic-ai-value-and-delivery-at-inspire-2026-302769893.html)
- **Navi Agent Studio** generally available in May for building custom agents.
- Acquired **Scoutbee** (AI supplier intelligence and discovery). (https://www.thomabravo.com/press-releases/coupa-announces-acquisition-of-ai-powered-scoutbee-to-drive-supplier-intelligence-and-discovery)

### Pricing [Third-party only; Coupa publishes nothing]
- SMB / mid-market basic configurations: **~$50,000-$150,000 annual subscription**
- Enterprise with multiple modules, high volume, global rollout: **$500,000-$2,000,000+ annually**
(https://www.vendr.com/marketplace/coupa; https://www.itqlick.com/coupa/pricing)
- Coupa also runs a **supplier-side** pricing page (https://supplier.coupa.com/pricing/), i.e. it monetizes both sides of the network.

### Bank relationship
None. Coupa Pay is orchestration on top of bank and card partners. No charter, no deposits, no issuing.

### Displacement read
Coupa is **not a Rho displacement target in practice.** Its buyer is a CPO at a multi-billion-dollar enterprise, its ACV is 10x-100x anything in Rho's range, and Rho does not offer source-to-pay, contract lifecycle management, supplier risk, or supply chain design. Coupa belongs in this dossier as the ceiling of the "software fee on someone else's bank" model, not as a head-to-head competitor. Notably, **Rho publishes no Coupa comparison page** anywhere in the 1,042-URL sitemap or the 125-post comparison blog corpus, which is consistent with this read.

---

## 9. Corpay (NYSE: CPAY)

### Positioning (2026)
A $5B+ revenue corporate payments conglomerate, formerly FLEETCOR, that has been consolidating the AP and cross-border FX market aggressively. This is the **acquirer** in the space, not the acquiree.

### History
- **January 2021:** FLEETCOR acquired Corpay, rebranding it Corpay One.
- **March 2024:** FLEETCOR itself rebranded as **Corpay, Inc. (NYSE: CPAY)**.
(Both per Rho's own summary in `pages/blogcomp/blog__corpay-business-credit-card-reviews.txt`, Last Updated 2026-08-20.)

### 2025-2026 consolidation moves

| Deal | Terms | Date |
|---|---|---|
| **Alpha Group International plc** (B2B cross-border FX, global bank accounts) | **£42.50 cash per ordinary share**, aggregate **~£1.8 billion / ~$2.4 billion** | Completed **2025-10-31** (https://investor.corpay.com/news-releases/news-release-details/corpay-completes-24-billion-cross-border-payments-acquisition) |
| **AvidXchange Holdings** (AP automation, **~$450M revenue**) | LP formed with **TPG**; Corpay invested **~$578 million for ~35% of the LP equity**; enterprise valuation **~$1.9 billion** | LP formed **May 2025**, transaction **completed October 2025** (https://investor.corpay.com/news-releases/news-release-details/corpay-and-tpg-close-avidxchange-acquisition) |

Also announced: divestiture of vehicle/mobility units. (https://www.paymentsdive.com/news/corpay-alpha-group-acquisition-investment-manager-payments-vehicle-divesture/753946/)

**AvidXchange is the marquee datapoint for the thesis.** A public, standalone, seat-and-transaction-priced AP automation company with ~$450M of revenue was taken private at an enterprise value of only **~$1.9B, roughly 4.2x revenue**. Compare Ramp's private marks below. The market is repricing pure AP software down and balance-sheet-attached spend platforms up.

### Financials [Q2 2026, reported ~2026-08-12]
https://investor.corpay.com/news-releases/news-release-details/corpay-reports-second-quarter-financial-results-0; 10-Q https://www.sec.gov/Archives/edgar/data/0001175454/000117545426000050/cpay-20260630.htm
- Total revenue **$1.33 billion, +21% YoY**, beating consensus by 2.6%
- Adjusted net income per diluted share **$7.00, +36%**
- **Corporate Payments segment revenue $548.7 million, +42% YoY, 41% of consolidated revenue**
- Corporate Payments **organic growth 16%**, driven by **43% growth in spend volume**; acquisitions contributed **~$72 million**; favorable FX **$22 million**; fuel prices **~$1 million**
- **Sales bookings +30% YoY; retention 93%**
- FY2026 guidance raised to **$5.31 billion revenue (+17%)** and **cash EPS $27.35 (+28%)**
- **Over 80% of Alpha's corporate volume migrated** onto Corpay's global technology platform
- New growth plan targets markets worth **$600B total revenue opportunity, of which cross-border is $160B** (https://www.fxcintel.com/research/reports/ct-corpay-q2-2026-earnings)
- Alpha is stated to contribute **$2 billion to Corpay's corporate payments segment revenue** by the following year, at which point the segment would be **~40% of overall revenue**

### Pricing
Corpay does not publish enterprise pricing. Notable structural detail: **"Corpay One's monthly subscription is per team within Corpay One, and they don't charge per user or seat."** (https://cp.corpayone.com/pricing/) [Third-party] general range cited at **$10-$100** (https://www.selecthub.com/p/accounts-payable-software/corpay/), which is too vague to be useful. **Corpay Complete** (unified POs, invoice and payment processing, commercial cards, expense management in one UI) is custom-quoted.

Corpay's real monetization is the **FX spread and card rebate economics**, not the subscription. Rho's own review notes: "Some reviewers comment that Corpay's exchange rates are slightly less attractive than those of some competitors, but they stick with Corpay for smooth transaction processing." [Rho claim, sourced to third-party reviews.]

### Bank relationship
**Not a bank.** **Corpay Mastercard is issued by Fifth Third Bank, N.A., or another financial institution**, under license from Mastercard International Incorporated. (https://na.corpay.com/virtual-card) No charter application by Corpay was found in the 2025-2026 charter-application surge coverage (https://www.bankingdive.com/news/inside-the-explosion-of-banking-charter-applications/810250/; https://www.industrialbankers.org/fdic), though the surge itself is real: 2025 saw more applications than any year since 2008, and 2026 is on track to exceed it.

### Rho's critique [Rho claim]
From `blog__corpay-business-credit-card-reviews.txt`: "High late card repayment fees, expensive platform fees, email-only customer support, and a clunky UX may lead businesses to consider alternatives like Rho." Also: the Corpay One Mastercard is a **charge card**, not a credit card ("You cannot carry a balance forward"). Rho does not quantify the "high late card repayment fees," which is a gap: Rho's own terms disclose "the late fee shall be three percent (3%) of the delinquent payment balance for each month that the balance remains unpaid for up to six (6) months" (`pages/core/pricing.txt`).

---

## 10. Cross-vendor comparison tables

### 10.1 Published software pricing, normalized

| Vendor | Unit | Published price | Is it really the price? |
|---|---|---|---|
| **Rho** | per user / per month | **$0** | Yes. Also $0 ACH/wire/check, $0 subscription, $0 minimum. Non-zero: 1% FX, $15 SWIFT (optional), $30 intl wire recall, Treasury fee 0.15%-0.60% |
| **BILL** AP/AR | per user / per month | **$49 / $65 / $89 / custom** | No. Add $0.59 ACH, $1.99 check, 2.9% card, $19.99 intl USD wire, and BILL keeps the float |
| **BILL** Spend & Expense | per user / per month | **$0** | Yes for software. Monetized via interchange and credit ($1,000-$5M lines) |
| **Navan** Travel | per user / per month | **$0** up to 300 employees | Yes. Monetized via supplier commissions (~7% usage yield) |
| **Navan** Expense | per active expense user / month | **$0 for first 5, then $15** | Plus interchange on Navan Card; Navan Connect users keep their own card rewards |
| **Expensify** Collect | per member / month | **$5 flat** | Yes, month-to-month |
| **Expensify** Control | per member / month | **$9 / $18 / $36** | $9 only with annual term + Expensify Card + >=50% US spend on it. **$18 if you keep your own card. $36 month-to-month** |
| **SAP Concur** | **per expense report** | **$7 (Base) / $11 (Plus) / custom (Premium)**, unlimited users | No. Real mid-market: $9-$24/active user/mo, $3.50/invoice document with $30K min, travel per-transaction $5-$25, implementation $15K-$350K, escalators 5-8% |
| **Tipalti** AP | per month platform fee | **from $99** ("unlimited users") | No. Add $0.20-$36/payment, 1.9%-3.5% FX, $500-$600/mo per extra entity, $4K-$5K setup. Transaction+FX = 50-70% of total spend |
| **Tipalti** Mass Payments | per month platform fee | **from $249** | same |
| **Airbase / Paylocity for Finance** | per user / month | **not published** (historically $12-$18) | Now quoted inside a Paylocity HCM deal |
| **Coupa** | annual subscription | **not published** | $50K-$150K SMB; $500K-$2M+ enterprise |
| **Corpay** | per team (Corpay One) / custom (Complete) | **not published** | FX spread and card rebates are the real economics |
| **American Express** | **per card, annual** | **$895** Business Platinum, **$375** Business Gold, **$90** Corporate Card program fee, **$55** Corporate Green enrollment, **$0** program fee Corporate Gold/Platinum | Yes for the card fee. No per-seat software fee. Software (Center) now bundled |

### 10.2 What a 50-person company pays, annualized, software only

Assumptions stated explicitly so they can be argued with: 50 employees, 45 of them submitting expenses, 8 AP/finance seats, ~75 expense reports per month, existing card program kept unless noted.

| Stack | Annual software cost | Working |
|---|---|---|
| **Rho** | **$0** | No subscription, no seats, no per-payment fees |
| **BILL Spend & Expense** alone | **$0** | Free, but requires BILL's own card (no BYOC) |
| **BILL AP/AR (Team) + BILL Spend & Expense** | **$6,240** + payment fees | 8 seats x $65 x 12. Add ~$0.59/ACH x volume |
| **BILL AP/AR (Corporate) + S&E** | **$8,544** + payment fees | 8 x $89 x 12 |
| **Navan Business** (travel + expense) | **$7,200** | (45 - 5) x $15 x 12. Travel free under 300 employees |
| **Expensify Control**, keeping your own card | **$10,800** | 50 x $18 x 12 |
| **Expensify Control**, switching to Expensify Card, annual term, >=50% spend | **$5,400** | 50 x $9 x 12 |
| **Expensify Control**, month-to-month | **$21,600** | 50 x $36 x 12 |
| **Expensify Collect** | **$3,000** | 50 x $5 x 12 |
| **SAP Concur Base**, published rate | **$6,300** + implementation | 75 reports/mo x $7 x 12. Add $15K-$40K Standard implementation in year one |
| **SAP Concur Plus**, published rate | **$9,900** + implementation | 75 x $11 x 12 |
| **Tipalti AP**, small deployment | **$20,000-$45,000 all-in** | $99-$199/mo platform + per-payment + FX + $4K-$5K setup |
| **Airbase (historic list)** | **$7,200-$10,800** | 50 x $12-$18 x 12 |
| **Coupa** | **$50,000+** | Below Coupa's realistic floor; would not be sold this deal |
| **Amex Corporate Card program** | **$4,500** | 50 cards x $90 program fee. No software fee post-Center |
| **Typical real-world stack: Concur Plus + BILL Team + Amex cards** | **~$20,640 + $15K-$40K year-one implementation** | $9,900 + $6,240 + $4,500 |

**The headline number for a sales narrative: a 50-person company running the standard incumbent stack pays roughly $20K-$60K in year one for software and card fees that Rho prices at $0.** Caveat honestly: Rho recovers this through interchange on your spend, the spread on your deposits, and 1% on FX. It is a rebundling, not free money.

### 10.3 Bank and money-holding relationship

| Vendor | Is it a bank? | Who issues the card | Does it hold customer funds | Does it pay the customer yield |
|---|---|---|---|---|
| **Rho** | No (fintech) | Webster Bank, a division of Santander Bank, N.A. (Mastercard) | Deposits at Webster; savings via American Deposit Management Co. partner banks (up to **$75M FDIC**); intl via **Wise US Inc.** | Yes: Treasury, "up to 4.66% on idle cash" as of 09/11/2026, net of a 0.15%-0.60% fee |
| **BILL** | No | Cross River Bank, WebBank, WEX Bank (via DivvyPay LLC) | Yes, in transit | **No. BILL keeps it: $148.4M float revenue FY2026** |
| **Navan** | No | Celtic Bank (US); Stripe Technology Europe / Stripe Payments UK / Adyen N.V. (EU/UK) | No material float | N/A |
| **Expensify** | No | The Bancorp Bank, N.A. (Visa); Transact Payments Malta/Limited (EEA/UK) | Minimal | N/A. Returns value as 1%-2% card cashback and a subscription credit |
| **SAP Concur** | No | **None. Issues no card.** | No | N/A |
| **Tipalti** | No | Tipalti Card (add-on module) via partners | Yes, in transit | No |
| **Airbase / Paylocity** | No | Partner banks | Yes, in transit | No |
| **Coupa** | No | None (Coupa Pay orchestrates partners) | No | N/A |
| **Corpay** | No | **Fifth Third Bank, N.A.** (Mastercard) | Yes | No; returns value as card rebates |
| **American Express** | **Yes. American Express National Bank, Member FDIC** | **Itself** (issuer and network) | **Yes, as deposits** | **Yes: Business Checking 1.30% APY up to $500,000, no monthly fee** |

### 10.4 2025-2026 consolidation timeline

| Date | Event | Value |
|---|---|---|
| **2024-09-04** | Paylocity announces agreement to acquire **Airbase** | **~$325M** |
| **October 2024** | Paylocity/Airbase closes | |
| **2025-03-06** | **American Express** announces agreement to acquire **Center** | undisclosed |
| **2025-04-16** | Amex/Center **completes** | |
| **2025-05** | Corpay forms LP with **TPG** to acquire **AvidXchange** | Corpay ~$578M for ~35%; EV **~$1.9B** on ~$450M revenue |
| **2025-06-24** | **Xero** agrees to acquire **Melio** (not Amex) | **$2.5B upfront**, up to **$0.5B** contingent/deferred/rollover over 3 years |
| **July 2025** | Paylocity launches **"Paylocity for Finance"** (Airbase v1 inside HCM) | |
| **2025-07-24** | **Tipalti** layoffs ("dozens") | |
| **Late Sept 2025** | **Starboard Value** discloses **8.5%** of **BILL** | |
| **2025-09-19** | **Navan** files S-1 | |
| **October 2025** | BILL adds **4 directors, 2 from Starboard** | |
| **2025-10-30** | **Navan IPO**, Nasdaq NAVN, **$25/share**, raised **~$923M**, **~$6.2B** valuation, closed day one **-20% at $20** | |
| **2025-10-31** | Corpay **completes Alpha Group** acquisition | **£42.50/share, ~£1.8B / ~$2.4B** |
| **October 2025** | Corpay/TPG **close AvidXchange** | |
| **2025-11-17** | **Ramp** raises **$300M at $32B** post-money, led by Lightspeed | |
| **December 2025** | **Barington Capital** urges BILL directors to cut costs and find a buyer | |
| **2026-01-15** | **Tipalti** lays off **100 employees, ~8% of workforce** | |
| **2026-03-25** | SAP Concur Fusion 2026; Amex virtual cards inside Concur Expense; Visa Commercial Integrated Partner | |
| **2026-05-07** | BILL Q3 FY2026 + **$1.0B buyback authorization** | |
| **2026-05-12** | **Coupa Compose + Coupa Catalyst** launch at Inspire 2026 | |
| **2026-06** | **Ramp Series F, $750M at $44B** valuation | |
| **2026-07-20** | **Expensify Card launches in Europe** | |
| **July 2026** | Expensify launches **consolidated travel billing** | |
| **2026-08-06** | Expensify Q2 2026: revenue **$33.9M, -5% YoY**; interchange **$5.9M, +12%** | |
| **2026-08-19** | BILL FY2026: revenue **$1,653.2M**, subscription only **17.8%** of it | |
| **2026-08-24** | **Coupa CEO Leagh Turner departs**; **Mike Lipps** (Thoma Bravo operating partner) interim CEO | |
| **2026-09-10** | BILL CEO signals move **off per-seat pricing** toward value-based/consumption pricing | |
| (reported) | **Ramp** in talks toward **$40B+** (May 2026), eyeing **$60B** | |

Sources for the Ramp marks: https://techcrunch.com/2025/11/17/ramp-hits-32b-valuation-just-three-months-after-hitting-22-5b/; https://www.prnewswire.com/news-releases/ramp-raises-series-f-at-44-billion-valuation-302791103.html; https://www.cnbc.com/2026/06/04/ramp-valuation-funding-ai-spend.html; https://techcrunch.com/2026/05/07/ramp-in-talks-to-hit-40b-valuation-6-months-after-reaching-32b/; https://www.pymnts.com/spend-management/2026/ramp-eyes-60-billion-valuation-just-months-after-series-f/

**The valuation asymmetry is the loudest signal in the data.** In the same 24-month window: AvidXchange (~$450M revenue, seat+transaction AP software) went private at **~$1.9B EV**; Airbase (per-seat spend management) sold for **$325M**; Navan (usage-yield T&E) IPO'd at **~$6.2B and immediately fell 20%**; BILL ($1.65B revenue) is fielding activists and reported PE interest. Meanwhile Ramp, which gives the software away and monetizes the card, went **$22.5B -> $32B -> $44B in under a year**. The market is paying for balance-sheet-attached spend, not for seats.

---

## 11. Where Rho's own marketing is wrong, stale, or overstated

This matters because these are the claims most likely to get repeated and then contradicted by a prospect who has the vendor's price sheet open.

| Rho page | Rho's claim | Verified reality (2026-09-11) | Severity |
|---|---|---|---|
| `pages/core/versus__bill.txt` | BILL is "**$45-$89 per user per month** for AP/AR" | BILL publishes **$49-$89**. The $45 low end does not exist | Minor, but it is a checkable error |
| `pages/core/versus__bill.txt` | BILL charges a "**10% instant transfer fee**" | BILL's page: **Instant Payment 1.0%** with a **$9.99 min and $100 max**; receiver-side **Instant Transfer 1%-1.49%** ($1 min). **Rho overstates by ~10x** | **Material. This is the most damaging error in the corpus** |
| `pages/core/versus__bill.txt` | BILL: "Cards + expenses only, no banking or treasury" and "Platform & seat fees ... $45-$89 per user per month" presented against BILL/Divvy | Conflates two BILL products. **BILL Spend & Expense is $0/user/month.** The seat fee applies to AP/AR only | Material |
| `pages/core/versus__bill.txt` | BILL requires "$20K+ minimum cash often required" for credit | Not stated on BILL's pricing page; BILL publishes "credit lines from $1,000-$5M," subject to approval. Unsourced | Unverified |
| `blog__sap-concur-alternatives.txt` (Last Updated 2026-08-20) | "BILL Spend & Expense Pricing ... Essentials: **$45**/user/month ... Team: **$55** ... Corporate: **$79**" | BILL's published AP/AR prices are **$49 / $65 / $89**. All three Rho numbers are wrong, and they are labeled as *Spend & Expense* pricing when Spend & Expense is $0 | **Material, three wrong numbers plus a product mislabel** |
| `blog__sap-concur-alternatives.txt`, `blog__bill-spend-and-expense-alternatives.txt` | "Navan Business: Free plan for companies **up to 200 employees**" | Navan publishes **up to 300 employees** | Minor |
| Both posts above | Navan Business "includes travel and expense features" (free) | Navan Expense is **free for 5 users, then $15/user/month** | Material omission |
| `blog__bill-spend-and-expense-alternatives.txt` | "**Expensify's pricing is not public.** Contact their support for more info." | Expensify publishes **$5 / $9 / $18 / $36** and has since April 2025 | **Material and easily falsified** |
| `blog__sap-concur-alternatives.txt` | Expensify tiers are "Individual / Group / Corporate" | Current names are **Free / Collect / Control**. This is pre-2023 naming | Stale |
| `blog__bill-spend-and-expense-alternatives.txt` | Profiles **Center** as an independent alternative with its own merchant-fee pricing model | **Center was acquired by American Express, completed 2025-04-16** | **Material. Recommending a competitor's subsidiary as an alternative** |
| Airbase posts (`blog__airbase-vs-brex`, `blog__airbase-vs-ramp`, Airbase Alternatives) | Treat Airbase as independent | **Airbase was acquired by Paylocity for $325M, closed October 2024**, rebranded, and folded into "Paylocity for Finance" July 2025 | **Material, ~2 years stale** |
| `pages/core/versus__amex.txt` | Frames Amex as "a $895 travel card" with "basic controls" and "bank feed only, limited data" | The $895 figure is correct for Business Platinum (post-Sept 2025). But Amex **acquired Center in April 2025** specifically to fix expense automation, and the **Corporate Card program fee is $90**, not $895 | Directionally fair on the consumer-facing card, **materially incomplete** on Amex Commercial |
| `pages/core/product__bill-pay.txt` | "Pay vendors without friction ... pays vendors directly from your account" | The step-by-step flow on the same page says **"Once approved, pay by check"** and the $0 fee callouts are "$0 On domestic check payments" and "Check payments at no per-payment fee." **The Bill Pay page as captured describes check as the disbursement method.** Rho's pricing page separately says $0 same-day ACH and wires | See Section 12 |

Rho's strongest, fully defensible comparison claims (all verified above): BILL charges **$0.59/ACH, $1.99/check, 2.9% card**; BILL AP/AR is **$49-$89/user/month**; Amex Business Platinum is **$895/year**; Expensify **doubles to $18** if you keep your own card; Tipalti's FX markup is **1.9%-3.5%** against Rho's **1%**; Concur charges **per expense report**.

---

## 12. What is conspicuously NOT stated

**By the incumbents:**
- **SAP Concur, Coupa, Corpay, Tipalti (beyond the floor), and Airbase/Paylocity all refuse to publish real pricing.** Between them that is most of the mid-market and all of the enterprise. Concur publishes an SMB rate card ($7/$11 per report) that bears little relation to what an enterprise actually signs ($9-$24/active user/month plus six-figure implementation).
- **Concur publishes no implementation fee at all**, despite third-party estimates of **$15K-$40K (Standard) to $80K-$350K (Professional)** and professional services running **20-50% of first-year subscription**.
- **Coupa's "ARR growth trajectory" press release contains no ARR number.** It reports platform volume, customer savings, and logo counts instead. Coupa has not disclosed ARR since the 2024 "$1B billings" claim.
- **BILL does not disclose Divvy/Spend & Expense customer counts or card volume separately** in its FY2026 release, only consolidated TPV ($98.2B in Q4) and total businesses (479,300).
- **Tipalti's $8.3B valuation is a stale 2021-vintage mark** and no vendor or investor has publicly reset it despite two layoff rounds.
- **Navan does not publish the Enterprise price** (300+ employees), which is where its real revenue sits, and does not publish a Navan Connect price at all.
- **Expensify does not publish travel booking fees** despite launching consolidated travel billing in July 2026.
- **No incumbent except Amex offers the customer a deposit account or passes through yield.** BILL explicitly books the float as its own revenue line.

**By Rho:**
- Rho's `pages/core/pricing.txt` does **not** disclose interchange economics, deposit-spread economics, or what Webster Bank pays Rho. The "free" is funded, and the funding mechanism is unstated.
- Rho publishes **no Coupa comparison, no Airbase-vs-Rho comparison, and no Paylocity comparison** anywhere in the 1,042-URL sitemap. The Airbase content that exists compares Airbase to Brex and Ramp, not to Rho.
- Rho's Bill Pay product page (`pages/core/product__bill-pay.txt`) describes the payment step as **"pay by check"** and headlines **"$0 On domestic check payments"**. It does not describe ACH or wire disbursement to vendors in the flow, and it explicitly states **"it does not include procurement or supply-chain management."** Against BILL Corporate ($89/user/month, which includes POs, tolerance rules, and 2-way matching) and Tipalti/Coupa, this is a real functional gap that Rho's comparison pages do not acknowledge.
- Rho does not state a **vendor/payee network size**, **international payment country/currency coverage** (beyond "Wise US Inc. provides it"), **global tax compliance** (W-8, local withholding, 1099 e-filing), or **multi-entity** support. Every AP incumbent leads with these. Tipalti's 200+ countries / 120+ currencies / 50+ methods and BILL's vendor network have no published Rho equivalent.
- Rho's card is a **Mastercard issued by Webster Bank**. Rho does not publish credit limits, underwriting criteria, or whether the card is charge or revolving, while criticizing BILL for "rigid underwriting."
- No Rho page discloses **SOC/FedRAMP/SSO/SCIM/dual-control** parity against BILL Enterprise (which lists SSO and dual control) or Concur Premium.

---

## 13. The three arguments that actually survive scrutiny

Everything above compresses to three defensible wedges, plus one that does not.

**1. The double-dip on float.** BILL charges $49-$89/user/month, $0.59/ACH, 2.9% on card payments, **and** keeps $148.4M/year of interest on customer money in transit (FY2026, 9.0% of its revenue). Tipalti, Corpay, and Airbase/Paylocity have the same shape. Rho's structure gives the workflow away and offers the customer the yield (Treasury, up to 4.66% as of 09/11/2026, net of 0.15%-0.60%). This is the cleanest, most quantified version of the structural claim and it is fully sourced to the incumbent's own press release.

**2. The interchange hostage clause.** Expensify publishes **$9/member/month** and then says: only if you enable the Expensify Card and route **at least 50% of settled US spend** through it, on a 12-month commitment. Otherwise **$18**, or **$36** month-to-month. BILL's Spend & Expense is "$0" but requires BILL's own card with no BYOC. Both vendors have already conceded that the software is worth roughly zero and the card flow is the product; they are just charging a penalty to customers who keep their own bank. Rho charges no penalty because it *is* the card and the account.

**3. The unit of pricing is the artifact of the old workflow.** Concur charges **per expense report**. Tipalti charges per invoice and per payment. Coupa charges per module and per supplier. Every one of these prices scales with the manual work, which means the vendor's revenue is structurally opposed to automating it away. BILL's own CEO conceded the point on **2026-09-10**: "pricing has to be tied to value creation," and BILL is moving "from just the subscription pricing model we have today." When the largest seat-priced AP vendor says the seat model is wrong, that is not Rho's marketing claim, it is the incumbent's.

**The argument that does NOT survive:** "they charge software fees, we don't." It fails against **American Express**, which charges no per-seat software fee, is a real FDIC-insured bank with a 1.30% APY business checking account, owns its expense software outright since April 2025, and is the largest commercial card issuer in the US. It also fails against **BILL Spend & Expense**, which is genuinely $0/user/month. And it is weaker than it looks against **BILL overall**, where subscription is only 17.8% of revenue, and **Navan**, where subscription is ~10%. Against those four, the right argument is not "seats vs no seats," it is "who holds the balance and who gets the yield."

---

## 14. Open questions and verification gaps

1. **Tipalti S-1.** techstackipo.com claims an S-1 filed **2026-03-12**; this contradicts the president's **2026-06-16** statement that profitability by early 2027 is a gating factor for a future IPO. Needs SEC EDGAR full-text search to resolve. Do not use the S-1 claim until verified.
2. **Amex/Center purchase price.** Not disclosed in either Amex press release. Check Amex 10-Q/10-K for Q2 2025 goodwill/intangibles commentary.
3. **What Center became inside Amex.** Is it now a named Amex product, bundled free with Corporate Card, or sold separately? This determines whether Amex has neutralized the "$895 card with no software" attack.
4. **BILL's new pricing model.** Lacerte signaled the shift on 2026-09-10 but gave no design. If BILL moves to consumption/platform pricing with a $0 entry, Rho's "no seat fees" wedge against BILL narrows to float and banking only.
5. **BILL strategic outcome.** Hellman & Friedman talks reported; three activists on the register. A take-private would change the competitive posture materially.
6. **Navan Enterprise pricing.** Unpublished. Given ~90% usage-based revenue and ~7% usage yield, the Enterprise contract is likely a booking-fee structure rather than seats; needs a real quote or an S-1/10-K revenue-disaggregation read.
7. **Concur's actual per-active-user list price.** All $9-$24/user figures are third-party. No primary source found.
8. **Coupa ARR and Coupa Pay volume.** Undisclosed since 2024. Thoma Bravo's interim-CEO appointment (2026-08-24) suggests a process; watch for a disclosure event.
9. **Corpay bank charter.** No application found, but the 2025-2026 charter surge is real and Corpay's AvidXchange + Alpha build-out gives it a reason. Check the FDIC industrial bank tracker and OCC licensing decisions quarterly.
10. **Expensify's 48% gross margin** as reported in Q2 2026 coverage looks anomalously low. Verify against the 10-Q before citing.
11. **Rho Bill Pay disbursement methods.** The captured product page describes check payment and "$0 On domestic check payments"; the pricing page says $0 same-day ACH and wires. Whether Bill Pay disburses by ACH/wire to vendors, and at what limits, needs confirmation from the help center corpus or the product itself.
12. **Rho international AP coverage.** Wise US Inc. is the provider, but country, currency, and payment-method counts are unpublished. This is the largest unfilled gap against Tipalti and Corpay.
