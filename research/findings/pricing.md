# Rho: The Complete Money Picture

Corpus: local snapshot of rho.co (128 core pages, 269 help pages, 125 comparison blog posts, 14 docs pages, 14 API reference pages, live sandbox JSON, site-llms.txt / site-llms-full.txt, 1042-URL sitemap). Research date 2026-09-11. Every figure below is sourced to a specific local file. Rho asserts most of these itself, so treat unattributed product claims as marketing until independently verified; statements about competitors are tagged **[Rho claim]**.

Legal entity: **Under Technologies, Inc., DBA Rho Technologies**, 100 Crosby Street, New York, NY 10012. Copyright line "© 2019 - 2026". Rho is not a bank. Banking and card services: **Webster Bank, a division of Santander Bank, N.A.** Savings: **American Deposit Management Co. (ADM)**. International/FX: **Wise US Inc.** Treasury advisory: **RBB Treasury LLC dba Rho Treasury** (SEC-registered RIA, Rho subsidiary). Treasury custody: **Apex Clearing Corp.** (accounts opened after July 2024) and **Interactive Brokers LLC** (before that). Capital: loans made by **Lead Bank**, serviced/underwritten by **Slope**. Invoice card acceptance: **Stripe, Inc.**

---

## 1. The advertised fee schedule (and the fact that there are two of them)

Rho publishes a seven-row fee summary. The **pricing page** and the **homepage** disagree on two of the seven rows.

| # | `/pricing` (pages/core/pricing.txt) | `/` homepage (pages/core/homepage.txt) |
|---|---|---|
| 01 | Same-Day ACH, wires, and checks **$0 \*** | Same-Day ACH, wires, and checks **$0 \*** |
| 02 | Subscription Fees **$0** | Subscription fees **$0** |
| 03 | Checking account minimum fees **$0** | Checking account minimum fees **$0** |
| 04 | Connected, in-platform capabilities: AP, Expense & Accounting Automation **$0** | **Built-in Bill Pay + Invoicing $0** |
| 05 | Per-user fees **$0** | Per-user fees **$0** |
| 06 | Foreign currency transfer **1%** | Foreign currency transfer **1%** |
| 07 | **Domestic wire recall fee $0** | **Wire recall fee $0** (unqualified) |

The asterisk footnote on both pages: "Applicable fees for the checking account include a **$30 international wire recall fee**, an optional **$15 SWIFT fee**, and a **1% foreign currency conversion fee**. International wires in USD can be subject to additional fees set by recipient, correspondent, or intermediary banks, in addition to the SWIFT network. Unless prohibited by law, the late fee shall be **three percent (3%) of the delinquent payment balance for each month** that the balance remains unpaid for up to **six (6) months**."

The homepage's unqualified "Wire recall fee $0" is contradicted by the same page's own footnote ($30 international wire recall) and by four other sources (section 3 below).

`site-llms.txt` compresses the whole schedule to one sentence: "the only standard payment fee is **1% on foreign-currency transfers (as of 08/02/2026)**." That sentence is repeated verbatim across the help center ("The only standard payment fee is 1% on foreign-currency transfers", help-center/general-rho-information/pricing-requirements) and dozens of blog posts. It omits at least eight other fees Rho does charge.

---

## 2. Exhaustive fee schedule: everything Rho or its partners charge

### 2.1 Payments and banking

| Fee | Amount | Source | Notes |
|---|---|---|---|
| Monthly / maintenance / minimum-balance fee on checking | **$0** | pricing.txt, product__business-banking.txt | "no monthly fee, no minimum balance" |
| Subscription / platform / software fee | **$0** | pricing.txt; all product pages | No paid tiers exist anywhere in the corpus |
| Per-user / per-seat fee | **$0** | pricing.txt, product__expense-management.txt | "unlimited users at no extra cost" |
| Per-card / annual card fee | **$0** | product__corporate-cards.txt | "$0 annual fee, subscription fee, or per-card fee" |
| Domestic ACH (incl. same-day) | **$0** | pricing.txt | Same-day if created before 2 pm ET and under $1mm |
| Domestic wire out | **$0** | pricing.txt, versus__chase.txt | |
| Domestic wire in | **$0** (not stated; implied by "$0 wires") | | Conspicuously never stated explicitly |
| Physical check payment | **$0** | product__bill-pay.txt "Domestic per-payment fees $0 on checks" | |
| Remote check deposit | **$0** (not stated) | | No fee stated anywhere |
| **Foreign currency conversion / FX transfer** | **1%** | pricing.txt; help-center/payments/how-to-send-an-international-wire | "Rho offers a market-leading 1% FX rate for foreign currency conversion and transmission" |
| International wire sent **in USD** | **$0 Rho fee** | help-center/payments/transfer-faqs: "Rho charges no fee on international wires sent in USD (as of 08/02/2026)" | Third-party bank/SWIFT fees still apply |
| **SWIFT / "cover all recipient delivery fees" toggle** | **flat $15** | pricing.txt ("optional"); help-center/payments/how-to-send-an-international-wire | Buys absorption of recipient/correspondent/intermediary + SWIFT charges. Blog `rho-vs-chase` says "in some corridors that fee is **mandatory with no opt-out**" |
| **International wire recall** | **$30** | pricing.txt footnote | |
| **Wire recall (unqualified)** | **$30** | TOS §15: "Applicable fees for the checking account include a **$30 wire recall fee**, optional $15 SWIFT fee and 1% foreign currency conversion fee"; blog `best-banks-*`: "When a wire recall is necessary, Rho charges a $30 wire recall fee" | The word "international" is absent from the TOS and from the blog |
| **Failed / returned domestic wire** | **"around $20 – $45" deducted from your Rho account** | help-center/payments/fees-for-recalls-failed-wires | Never appears on the pricing page. Directly contradicts "Domestic wire recall fee $0" |
| **Late payment fee (card / any delinquent amount owed Rho)** | **3% of the delinquent balance per month, up to 6 months** (max 18% cumulative) | TOS §15 footnote; TOS Addendum A §2.4; Addendum B §2.4 | |
| Foreign card transaction fee | **"up to 1% of the transaction amount on foreign transactions"** | TOS Addendum A §2.4 and Addendum B §2.4 | Distinct from the 1% FX wire fee; never appears on the pricing page |
| Collection costs, attorneys' fees, court costs | Uncapped, charged to client | TOS Addendum A/B §2.3, §2.4 | |
| Fund-recovery assistance after a client-supplied wrong routing/account number | "billed to you at **Rho's current hourly rate** for such work" | TOS §16 | Hourly rate never published |
| Open-ended fee reservation | "we may determine a fee and change such fee... **Fees are not limited to the aforementioned list and we reserve our right to charge additional or other fees**" | TOS Addendum A/B §2.4 | Contradicts the same addendum's "you... will not be charged any fees except as disclosed herein" |

### 2.2 Invoicing (AR)

| Fee | Amount | Source |
|---|---|---|
| Per-invoice fee | **$0** | product__invoicing.txt; invoicing T&C §6 |
| Monthly invoicing fee | **$0** | product__invoicing.txt |
| ACH / wire / check payment received on an invoice | **$0** | invoicing T&C §6 |
| **Card, debit, or Google Pay payment on an invoice** | **2.9% + $0.30 per transaction** | invoicing T&C §4; help-center/invoicing/accept-card-payments-on-invoices; changelog 08/31/2026 |
| Card payment daily cap | **$10,000 USD per day across all invoices** (default) | invoicing T&C §4; help center |
| Surcharging the payer | **Not available.** "No, surcharging is not currently available." | help-center/invoicing/accept-card-payments-on-invoices |

The card processing fee is paid by the business, not the payer: help center says "This fee is paid by your business. Your customer pays only the invoice amount"; the changelog says "we deduct 2.9% + 30¢ from the payment and deposit the rest into your Rho account". **`/product/invoicing` never mentions the 2.9% + $0.30 fee at all**, and its comparison table shows only "ACH / bank transfer fee: $0 on domestic ACH, wires, and checks" while listing Stripe's 0.8% ACH fee and QuickBooks' 1% ACH fee. Card constraints: USD only, one-time full-amount invoices only (no partial payments, overpayments, recurring, or non-USD), first payout can take up to two weeks during Stripe's initial review.

### 2.3 Treasury (the one advertised recurring fee)

| Total AUM tier | Annual management fee |
|---|---|
| $20M+ (help center: **"> $20M"**) | **0.15%** (15 bps) |
| $10M to $20M | **0.25%** (25 bps) |
| $5M to $10M | **0.35%** (35 bps) |
| $2M to $5M | **0.45%** (45 bps) |
| Under $2M (marketing: "$50K–$2M"; treasury-yield-comparison: "$100K–$2M") | **0.60%** (60 bps, the maximum) |

Sources: policies/yield-methodology; product/treasury; treasury-yield-comparison; help-center/treasury/understanding-rho-treasury; help-center/treasury/about-rho-treasury.

Mechanics: "billed monthly on assets under management". "**AUM includes the combined balance of your Rho Checking and Treasury accounts.**" "The fee is deducted from your portfolio cash balance; if insufficient cash is available, **Rho will automatically sell a small amount of holdings to cover it**." (help-center/treasury/about-rho-treasury). Also possible: "rebalancing transactions and initial purchases... may result in fees. For example, there may be **additional transaction fees, redemption fees, loads, capital gains and other fees**" (TOS Addendum D §1). Full fee detail is deferred to the **ADV-2A Wrap Fee Brochure**, which is not in the corpus and is linked but never summarized on any page.

**Non-obvious: the fee schedule is a cliff, not a marginal bracket.** One rate applies to the whole balance. Crossing a tier boundary lowers the absolute annual fee, creating dead zones where a larger balance pays Rho less:

| At the boundary | Fee just below | Fee just above | Balance needed above the boundary to pay the old fee again |
|---|---|---|---|
| $2M | $1.999M × 0.60% = ~$11,994 | $2.0M × 0.45% = $9,000 | ~$2.67M |
| $5M | $5M × 0.45% = $22,500 | $5M × 0.35% = $17,500 | ~$6.43M |
| $10M | $10M × 0.35% = $35,000 | $10M × 0.25% = $25,000 | ~$14.0M |
| $20M | $20M × 0.25% = $50,000 | $20M × 0.15% = $30,000 | ~$33.3M |

Rho's maximum Treasury advisory revenue per client between $2M and $2.67M of AUM is roughly $12,000/year. At $20M it is $30,000/year.

### 2.4 Incorporation

| Item | Amount | Source |
|---|---|---|
| Rho Incorporation fee | **$400**, credited back on conditions | product__incorporation.txt |
| Credit-back condition | Deposit **$10,000 in new money** into Rho checking **and** keep daily average balance **at least $10,000 above where it started** for **60 days** after incorporation | product__incorporation.txt; treasury-yield-comparison.txt footnote; blog footnotes |
| Registered agent | **Included, year one only** | product__incorporation.txt |
| **Platform access after year one** | **$1,000 annually** | product__incorporation.txt ("How the fee works") |
| **Contract services** | **$100 or $250 per contract** | same |
| Delaware franchise tax | "apply separately and on an ongoing basis" | same |

The $1,000/year renewal and the per-contract charges appear in exactly one sentence on one page. They appear nowhere in the pricing page, the help center, `site-llms.txt`, or `site-llms-full.txt`, all of which describe incorporation as "free" or "$400, credited back". `site-llms-full.txt` further softens the condition to "maintain a **$10,000 average checking balance** for 60 days", dropping "new money" and "above where it started", which are materially harder tests.

### 2.5 Rho Capital

| Item | Terms | Source |
|---|---|---|
| Facility type | Revolving working-capital line of credit, not a term loan or venture debt | product__capital.txt |
| Size | **Up to $5M**; "larger facilities considered case by case"; help center says "up to $5M+" | product__capital.txt; help-center/general-rho-information/about-rho-capital |
| Repayment term per draw | **Up to 180 days**, then redraw | product__capital.txt |
| Funding speed | **24 to 48 hours** after approval | product__capital.txt |
| Origination fee | **$0** ("There are no origination fees") | help-center/general-rho-information/about-rho-capital |
| Prepayment penalty | **$0** on every draw, early or on schedule | product__capital.txt |
| **Interest / pricing** | **Never published.** "Fees vary based on risk assessment and loan term, and are set when **Slope** underwrites your line." "Rates are set during underwriting based on your business, see your offer for exact terms." | product__capital.txt; help center |
| Lender of record | **Business-purpose loans made by Lead Bank**; "Rho Capital lines are issued by Lead Bank and **serviced by Slope**" | product__capital.txt disclosure; blog__brex-vs-mercury footnote |
| Personal guaranty | "may be required, depending on underwriting" | product__capital.txt |
| Personal credit | Help center: "Applying doesn't involve a **hard pull** on your personal credit." Disclosure: "**Application and consent to obtain personal credit report is required**." | help center vs product__capital.txt disclosure |
| Revenue floor | "Subject to **minimum revenue** and business requirements" (disclosure), but product page says "Rho doesn't publish a fixed revenue or age threshold" | |
| Early repayment | `site-llms-full.txt`: "**paying early reduces fees**" | implies time-based (interest-like) pricing, not a flat fee |

**Rho Capital is the only Rho product with completely undisclosed pricing.** There is no rate, no APR, no fee range, and no example anywhere in the corpus. The FAQ on the product page says "Is Rho a direct lender for its working capital line of credit? **Yes.** Rho Capital is a single product", which contradicts the disclosure on the same page ("Financing offered by third parties... Rho Capital is not a broker-dealer. It does not participate in the negotiation or execution of any transactions between customers and third-party financing sources") and the Lead Bank / Slope footnotes.

### 2.6 API and support

- Rho API: **no price stated anywhere**. Launched 03 August 2026 (changelog), read-only, "Write access and webhooks are next." Rate limits: ~60 requests/minute per API access token, ~600 requests/minute per source IP (docs/docs_v1_rate-limits.md).
- Support: "you reach a real human, 24/7, on every account, **at no cost**. No phone trees, no paywalled support tiers." Phone 1 (855) 743-8746, clientservice@rho.co, in-app chat, plus iMessage and WhatsApp since June 2026.

---

## 3. What is genuinely free, with the exact exceptions

Free, unconditionally, on every account:
- Business checking: no monthly fee, no minimum balance, no per-user fee.
- Domestic ACH (including same-day), domestic wires, domestic checks.
- Bill Pay / AP automation, expense management, accounting automation, invoicing (AR), Rho Close, vendor cards, the Rho API, Partner Portal, 24/7 human support.
- Corporate cards: no annual fee, no subscription fee, no per-card fee, no personal guarantee, no personal credit pull.

Not free, in order of how likely a real customer is to hit it:
1. **1% on every foreign-currency conversion.** Unavoidable for any non-USD payment.
2. **2.9% + $0.30** on any invoice paid by card, debit, or Google Pay, with no ability to surcharge the payer.
3. **0.15% to 0.60% per year** on Treasury AUM.
4. **$15** to cover recipient/correspondent/SWIFT fees on an international wire (described as optional on the pricing page, "mandatory with no opt-out" in some corridors per Rho's own blog).
5. **$20 to $45** on a failed and returned domestic wire.
6. **$30** wire recall.
7. **3% per month, up to 6 months** on any delinquent amount owed to Rho.
8. **Up to 1%** on foreign card transactions (TOS card addenda).
9. **$400** to incorporate, plus **$1,000/year** platform access after year one and **$100 or $250 per contract**.
10. Whatever Slope prices the Capital line at.

Fees that do **not** exist at Rho and which Rho contrasts with competitors: overdraft fees, stop-payment fees, incoming wire fees, per-invoice fees, per-seat fees, tiered checking, minimum-balance service charges.

---

## 4. The yield story

### 4.1 Rho Treasury: the numbers as of 09/11/2026

Headline: "**Up to 4.66% net of fees**" (as of 09/11/2026; variable). Every Rho page carries the same footnote: "This reflects the sought net yield based on **90-day Treasury Bill rates as of 09/11/2026** and an annual fee which ranges from 0.15% for deposits of $20M or more to 0.6%... The rate shown is net of fees."

Full net-yield matrix (product/treasury and treasury-yield-comparison, "Yields as of 09/11/2026 and change daily"):

| Total deposits (annual fee) | Vanguard VFSTX/VFSUX net (30-day SEC yield) | Morgan Stanley MULSX net (7-day SEC yield) | 13-week T-Bills net (trailing 7-day avg) |
|---|---|---|---|
| $20M+ (0.15%) | **4.66%** | **3.70%** | **3.66%** |
| $10M–$20M (0.25%) | 4.56% | 3.60% | 3.56% |
| $5M–$10M (0.35%) | 4.46% | 3.50% | 3.46% |
| $2M–$5M (0.45%) | 4.36% | 3.40% | 3.36% |
| $50K–$2M (0.60%) | **4.21%** | **3.25%** | **3.21%** |

Implied gross yields (net + fee at the $20M+ tier): VFSTX/VFSUX ≈ **4.81%** 30-day SEC yield; MULSX ≈ **3.85%** 7-day SEC yield; 13-week T-Bill benchmark stated directly as **3.81%** (trailing 7-day average, source U.S. Department of the Treasury, as of 09/11/2026). The arithmetic across all five tiers is internally consistent: each tier step matches the fee delta exactly.

**The headline is the most aggressive number available.** Rho says so plainly: "the 'up to' number at the top of this page... assumes your entire balance sits in the Vanguard short-term investment-grade bond fund, an allocation we recommend only for cash you won't need for a year or more." The conservative all-T-Bill number at the bottom tier is **3.21% net**, 145 bps below the headline.

**But a 100% Vanguard allocation is not actually permitted.** `product/treasury` step 02 and its FAQ: allocations are "in 5% increments up to 100%, **with the short-term bond fund capped at 50% of your total allocation**." Help center: "Vanguard allocations are **capped at 50%** of your portfolio. If you hold both VFSTX and VFSUX, the limit applies to the two combined... unless we have approved a higher limit for your account." So the headline 4.66% describes an allocation Rho's own product blocks. A 50% VFSUX / 50% IJTXX or MULSX mix at the top tier lands materially lower.

### 4.2 Yield methodology (policies/yield-methodology, dated August 3, 2026)

- **T-Bills**: quoted as the **trailing 7-day average U.S. T-Bill yield (13-week)**, source U.S. Department of the Treasury. Not the yield of Rho's own purchases. Explicit admission: "[Pending: Rho plans to quote the yield of **its own most recent T-Bill purchases** once a product-sourced feed is available; this section will be updated when that ships.]"
- **Money market funds (MULSX)**: **7-day SEC yield**, net of fund expenses.
- **Bond funds (VFSTX)**: **30-day SEC yield**, net of fund expenses.
- "Net" = published instrument yield minus the Rho fee at the stated tier. "Where Rho quotes a single 'up to' figure, it is net of the lowest fee (0.15%, the $20M+ tier)."
- Blended portfolio yield = weighted blend, net of fee, "the same calculation your dashboard shows in real time."
- Self-imposed rule: "If you see an **undated yield** anywhere on our site, tell us, that's a bug, not a policy."
- Settlement: "proceeds from Treasury sell orders are available in your Rho checking account within **two (2) business days** of trade execution (as of 08/03/2026)."

The fund yields are net of **fund expense ratios as well**, which Rho never quotes. VFSUX (Admiral) is explicitly described as having "a lower expense ratio" than VFSTX (Investor), but no expense ratio number appears anywhere in the corpus for any of the four instruments.

### 4.3 What the cash is actually invested in

Marketing says **three** instruments. The help center says **four**.

| Instrument | Ticker | Description (help-center/treasury/about-rho-treasury) | Suitable horizon |
|---|---|---|---|
| JPMorgan U.S. Treasury Plus Money Market Fund | **IJTXX** | Government MMF holding U.S. Treasuries and repos backed by them. "Offered as a **cash sweep**: your allocation is held as cash and swept into the fund automatically each business day." Fixed **$1.00 NAV**, **no minimum**. | Same day |
| Treasury Bills (13-week) | n/a | Purchased at a discount, redeemed at face value. Bought in **$1,000 increments**. No NAV variability. | 3+ months |
| Morgan Stanley Ultra-Short Income Portfolio | **MULSX** | Commercial paper, corporate debt, ABS. "**It is not a money market fund**, NAV is variable but designed to remain highly stable." Interest accrues daily, dividends monthly. | 4 to 6 months |
| Vanguard Short-Term Investment-Grade Fund | **VFSUX** (Admiral) / **VFSTX** (Investor) | Short-term corporate bonds and IG fixed income. "Offers the highest yield potential of the four assets, but carries **meaningful NAV variability**." | 12+ months |

Preset strategies (help-center/treasury/about-rho-treasury):

| Strategy | Holding period | Allocation |
|---|---|---|
| Maximum liquidity | Same day | 100% IJTXX |
| Capital preservation | 3 months | 50% IJTXX / 50% T-Bills |
| Balanced income | 4 to 12 months | 40% IJTXX / 60% MULSX |
| Optimized yield | 12+ months | 15% IJTXX / 60% MULSX / 25% VFSUX |
| Custom | your choice | 5% increments, must total 100%, Vanguard capped at 50% |

Note that none of the four presets reaches the 4.66% headline, and the highest-yield preset holds only 25% Vanguard.

**Share-class migration:** VFSUX "is now the only Vanguard fund available for new allocations." Existing VFSTX holders keep their position, new money goes to VFSUX, and "**VFSTX is sold before VFSUX**... on a first-in, first-out basis (FIFO)." Custody platform migration: "VFSUX and the IJTXX money market fund sweep are available through **Apex Ascend**, our new custody platform. If you joined Rho Treasury **on or after July 23, 2026**, your account is on Ascend... If you joined before July 23, your account will migrate to Ascend in the coming months." Two classes of Treasury customer currently exist with different available instruments.

### 4.4 Minimums, eligibility, liquidity, protection

- **Minimum: $50,000.** Stated on product/treasury (seven times), the help center ("Maintain at least $50,000 in **total deposits**"), yield-methodology, and site-llms. **Contradicted on treasury-yield-comparison.txt, which states the Rho minimum as "$100,000" in both renderings of its comparison table and labels its bottom fee tier "$100K–$2M (0.60%)"** while the same page's prose, FAQ, and footnote say $50,000 and the equivalent product-page row says "$50K–$2M".
- Eligibility (help center): U.S.-registered business, operates primarily in the U.S., at least one U.S.-based founder, at least $50,000 in total deposits. Application takes under 10 minutes; approval "typically 2 business days". KYC: SSN/TIN/passport/EIN, formation documents, business license, certificate of good standing, beneficial ownership forms.
- **Liquidity:** T-Bill sales and mutual fund redemptions settle in **2 business days** if submitted before the daily cutoff (**5:00 PM ET for T-Bills, 4:00 PM ET for mutual funds**) and **3 business days** after. Proceeds reach checking within 2 business days. Marketing shorthand is "2 to 3 business days". `treasury-yield-comparison` uses different wording: "Fund redemptions **next business day**; T-Bill sales settle in 2–3 business days." Account closure: "liquidating all holdings... typically takes 2-3 business days."
- **Standing rules:** auto-transfer between checking and Treasury. "weekly is the fastest cadence Rho supports for that direction" (Treasury to checking).
- **Protection:** SIPC up to **$500,000 per customer including $250,000 for cash** via Apex/Interactive Brokers. Not FDIC. Securities held in the company's name, not pooled.
- **Tax:** Apex may issue a 1099. Thresholds cited: **$10 for dividends and interest, $20 for cash in lieu, $600 for miscellaneous income**. "C corporations are generally exempt from 1099 reporting under IRS broker reporting rules." Tax forms emailed from rho@tax-docs.com. ACAT transfers out are possible but "you will be unable to add or withdraw funds for **up to 90 days**."

### 4.5 Rho Business Savings (FDIC, a different product)

| Item | Value | Source |
|---|---|---|
| APY | **Up to 1.00%**, variable, "as of August 2026; terms apply" | product__business-savings-account.txt |
| Threshold to earn the rate | **$25,000 average monthly balance** | same |
| Below the threshold | "below $25,000, the balance earns **0%** with Rho" | same |
| Monthly fee | **$0** | same |
| FDIC coverage | **Up to $75,000,000 per entity**, "reflecting program capacity on a **commercially reasonable efforts basis, not a guarantee**" | same |
| Network | **400+** FDIC- and NCUA-insured partner banks (marketing, as of August 2026). **TOS Addendum C says "more than 300"** | product page vs TOS |
| Interest accrual | Daily, paid monthly, **posted on the 5th business day** of each month | help-center/banking/understanding-rho-savings-accounts |
| Day-count convention | **30/365** | same |
| Basis | "average monthly balance with **daily ending balances** used to determine the monthly average" | same |
| Transfers in | Unlimited, **only from a Rho Checking account** | same |
| Transfers out | **Limited to six (6) per month** | same; ADM MSA |
| Settlement in | Same business day if created before 1 PM ET | help center |
| Settlement out | Help center: "next business day, if created before 1pm ET". Payment-settlement-times page: "**2 business days**". ADM MSA: processed Tuesdays and Thursdays, settled Wednesdays and Fridays; requests over **$3,000,000** are "special handling" settled at a mutually acceptable day | three-way contradiction |

**Non-obvious: the 30/365 convention.** Twelve months of 30 counted days is 360 day-counts against a 365-day denominator, so a full year at a nominal 1.00% accrues roughly 0.9863% of balance. The ~1.4% shortfall relative to actual/365 is never disclosed as a rate adjustment; only the convention is named, in a help article.

**The ADM master agreement (published in full in the help center) contains two clauses Rho never surfaces in marketing:**
- "Client acknowledges that **ADM may, from time to time, place a certain portion of Client's funds in a non-interest bearing transaction account.**"
- "**By signing Exhibit A, Client expressly waives extended deposit insurance**", after which funds above the per-institution FDIC/NCUA limit "are not guaranteed by the FDIC or NCUA... and, as a result, in the event of a financial failure of any such Program Institution, Client funds... **will be at risk**."
- Intraday/overnight exception: "if funds in excess of $250,000 are deposited into or withdrawn from the Program in a single day, for a limited amount of time (intraday or overnight), **the entire amount... may be held at one Program Institution**."

### 4.6 Competitor yields Rho publishes **[Rho claim]**

Securities products (treasury-yield-comparison, verified by hand on the dates shown):

| Provider | Net yield | Instrument | Minimum | Fee | Verified |
|---|---|---|---|---|---|
| Rho Treasury | Up to 4.66% net | 13-wk T-Bills + MULSX + VFSTX | $50K (table says $100K) | 0.15%–0.60% | 09/11/2026, auto |
| Mercury Treasury | **3.01%–3.81% net by deposit tier** | JPMorgan JTCXX and/or Morgan Stanley MCRYX | **$250,000** | 0.15%–0.60% | 08/02/2026, mercury.com/treasury |
| Brex Business Account | **4.01%–4.36%**, fund 7-day yield plus a Brex balance bonus | BNY Dreyfus DGVXX | None published | No separate program fee disclosed | rates effective 07/31/2026 |

Elsewhere in the same corpus Rho gives **different** Mercury numbers: product/business-savings-account says "Mercury Treasury: **3.13% to 3.89%**" (collected 2026-09-06) and product/business-banking says "Up to **3.89%**, tiered by balance (as of 08/28/2026)". Product/treasury says Mercury's page was "stamped 08/28/2026". These are consistent only if Mercury's rate moved; the pages do not reconcile.

FDIC bank APYs **[Rho claim]** (treasury-yield-comparison):

| Provider | APY and conditions | Verified |
|---|---|---|
| SVB Startup Money Market | 0.10% ≤$50K, 2.38% to $1M, 3.30% >$1M, per a rate sheet **dated 12/10/2025** still posted | checked 08/02/2026 |
| Bluevine Business Checking | 1.3% Standard (requires $500/mo debit spend **or** $2,500/mo incoming payments, else 0%; cap $250K), 1.75% Plus ($250K cap), 3.0% Premier ($95/mo, waivable) | 08/05/2026 |
| Grasshopper Business Savings | 1.55% <$25K, 3.00% $25K+, $100 to open; checking pays at most 1.35% | bank-dated 01/05/2026, checked 08/02/2026 |
| Relay Savings | 1.11% Starter ($0/mo), 1.75% Grow ($30/mo), 3.00% Scale ($90/mo), gated by subscription, max 2 savings accounts | Relay-dated 5/1/2026, checked 08/02/2026 |
| Axos business checking | Up to 1.01% on balances ≤$50K | 08/02/2026 |

Note Rho quotes Relay's top plan as **$90/mo** on treasury-yield-comparison and **$120/mo** on product/business-savings-account ("$0 on Starter plan; **$120/mo Scale plan** required for the top rate", collected 2026-09-06).

Rho also volunteers where it loses: "**below Rho Treasury's $50,000 minimum, Rho doesn't have a yield product to sell you**", Mercury's JTCXX "redeems same-day, faster than a T-Bill sale settles at Rho", and "if your board mandates FDIC coverage on every yielding dollar, those beat any securities product, Rho's included."

---

## 5. Cashback mechanics and qualification

### 5.1 The rate card

| Card program | Standard | Rho Platinum |
|---|---|---|
| Rho Corporate Card with **Daily Terms** | **1.25%** | **2%** |
| Rho Corporate Card with **Monthly Terms** | **1%** | **1.75%** |

Source: policies/cashback-rewards; product__corporate-cards.txt; blog footnotes. Cap: "Cashback Rewards may be earned on **up to $1,000,000 in eligible spend per calendar year**. The cap applies to eligible spend, not to the dollar amount of Cashback Rewards." Maximum annual cashback at the top rate is therefore **$20,000**. Help center adds: "Spending more than $1M a year? **Talk to sales and we'll build your program**."

### 5.2 Rho Platinum qualification: all four required

1. "Your **payroll is run from Rho**";
2. "Your **business revenue is deposited via Rho Checking**";
3. "**50% or more of your company's assets are held at Rho**";
4. "You have an **open Rho Corporate Card**."

"It isn't a paid plan, there's no subscription fee." "Platinum status reflects your current setup. If your account no longer meets the qualifications, your Cashback rate returns to the standard rate." Status is not self-serve: "Contact your account team" to check it.

This is the single most important economic fact about Rho's headline rate: **2% is priced in exchange for payroll flow, revenue flow, and a majority of the company's balance sheet sitting at Rho.** It is a deposit-gathering price, not a card reward.

### 5.3 What does not earn cashback

A "Qualifying Purchase" is "any purchase made with your Card minus returns and other credits." Excluded outright:
- **Walmart Inc. and its affiliates and subsidiaries**;
- **Utilities merchants**, by Mastercard MCC;
- **Money transfer, digital payment, and quasi-cash merchants**, by Mastercard MCC;
- **Transactions conducted or authorized in non-U.S. jurisdictions** (help center: "any charges made outside of the United States will not receive cashback");
- fees, fines, or interest charges paid to Rho; cash advances; balance transfers; cash equivalents; gift cards; prepaid and reloadable prepaid cards; purchases made with Cashback Rewards; person-to-person payments or transfers; online sports betting and internet gambling; **loan payments or account funding made with the Card**.

Also: "You may not receive additional Cashback Rewards if we are unable to independently verify certain information about the merchant... for instance, when a merchant uses a third-party to sell a product or service or otherwise uses a third-party to process your transaction."

`site-llms.txt` and `site-llms-full.txt` describe the product as "**up to 2% cashback on all spending**", which the terms contradict.

### 5.4 Payment, timing, expiry, and clawback

- **Full statement balance must be paid on time and in full.** "If you do not pay the full amount due on time, you will not receive any Cashback Rewards for the billing period; and you forfeit your ability to earn any Cashback Rewards for the billing period."
- "You will not receive Cashback Rewards if you **deposit funds in your Rho Account without making an actual payment to Rho**."
- **Daily Terms payout:** "Cashback posts as one payment, typically on the **6th business day of the month**, for the previous month's spend. There's **no minimum spend** to accrue Cashback."
- **Monthly Terms payout:** "Cashback deposits typically **6 business days after you pay your statement balance in full**."
- **Credited to the Rho Rewards checking account**, then redeemed into Primary Checking **instantly**. Only Account Owners, Administrators, or custom roles with "Redeem Rewards" permission can redeem; Budget Owners, Employees, Bookkeepers, and Investors cannot.
- **Expiry: "you must redeem Cashback Rewards within twelve months of being earned, or they will be forfeited. Rho will not provide notifications regarding the impending expiration of your Cashback Rewards."**
- **Ownership:** "the Cashback Rewards you may earn and accumulate **are not your property and do not belong to you until... redeemed and issued to you in the form of a statement credit by Rho**." Non-transferable, non-assignable, not usable in a bankruptcy proceeding.
- **Returns claw back cashback** as "a debit to your billing statement... an amount owed and due to Rho."
- **Card cancellation or account closure:** "you may **immediately lose all the Cashback Rewards** you may have otherwise been eligible to receive."
- **Program changes:** Rho can add, remove, or change terms, "**imposing fees, charging you to participate** in the Cashback Rewards Program". On cancellation or modification, 45 days' notice and 90 days to redeem; unredeemed rewards are forfeited on cancellation or subject to new terms on modification.
- **Disputes:** within **60 days** of the statement that gave rise to the error.
- **Tax:** help center says "Cashback from Rho is **not considered taxable** and we do not issue 1099s for cash back." (Contrast: referral bonuses, affiliate rewards, statement credit promotions, and sweepstakes prizes are all explicitly taxable per their own terms.)

Redemption mechanics are described two different ways: the terms describe cashback as "a statement credit" applied against the billing statement; the help center describes transferring it from the Rewards Account into Primary Checking. Both mechanisms appear to exist ("Pay with Cashback" applies a credit; "Redeem Rewards" moves cash).

### 5.5 Mastercard Easy Savings (a second, non-Rho cashback layer)

Every Rho card is a **World Elite Mastercard for Business**. Through Mastercard Easy Savings, "on top of Rho's cashback rewards":
- "Cash-back rates range from **1% to 25%**."
- "**4% back at more than 20,000 restaurants**" and hotels including Days Inn and Holiday Inn.
- Named merchants: Avis, Budget, Dropbox, Squarespace, Snapchat.
- "There is **no annual limit** on Easy Savings rebates though some limits may apply at individual merchants' discretion."
- Credited by **Mastercard 1-5 business days after the purchase settles**, shown as "Mastercard Load". Monthly Terms accounts see it in the credit account; Daily Terms accounts see it credited to the card balance.
- Other World Elite benefits (perks page, "as of September 1, 2026"): 24/7 Business Assistant concierge; dated offers such as 30% off QuickBooks and $300 Microsoft Advertising credit; ID theft protection, Zero Liability, My Cyber Risk, 24/7 global emergency card services. "Cardholder benefits are provided by Mastercard, not Rho."

### 5.6 Card credit structure (why the cashback is cheap for Rho)

- **Daily Terms:** "your company receives a **daily credit limit**. The limit is determined based on a combination of your **available checking balance** as well as risk factors." Repayments are "automatically debited from your Rho checking account **just after midnight EST** for that day's activity." TOS Addendum A: "**There is no grace period.**" A billing statement is issued daily whenever the credit account has a positive or negative balance of more than **$1.00** or a foreign transaction or other fee was charged that day.
- **Monthly Terms:** "a **30-day billing cycle with a 1-day repayment period**", automatic debit at cycle end. Requires a minimum cash balance of **$25,000** at Rho, or **$75,000 combined across Rho and linked external accounts** (personal accounts do not count), subject to underwriting. "You can only be on one program at a time."
- Spend limits: "**At no time shall we be required to disclose the spending limit to you**... We reserve the right to reduce your spending limit to **zero dollars** at our sole discretion."
- "**You will not be charged interest on your Credit Account**" (Daily Terms).
- Rho has the "**right to set off and apply any and all deposits** against the Company's Obligations... with or without providing notice to you", and may pull funds "on any date and at any time, in our sole discretion, when the total balance in your Rho Account, linked account(s), and/or Budget Account(s) is less than the balance minimum required by our underwriting criteria."
- Unauthorized use liability: if Rho issues **ten or more** cards, "**you will be liable for all unauthorized use of all Cards**." Fewer than ten cards: liability capped at the lesser of **$50.00** or the amount obtained.
- Credit reporting: "Rho does not pull any personal credit reports and does not report business card activity to personal credit reports. **We report to the credit bureaus on the entity (business) side at our discretion.**" Delinquencies may be reported to business credit bureaus without notice.
- **Cross guaranty (TOS §17):** every Rho account holder "absolutely, unconditionally and irrevocably guarantee[s], as primary obligor and not merely as surety" all obligations of any parent or subsidiary entity with a Rho account.

---

## 6. Referral, affiliate, and partner payouts

### 6.1 Customer referral program (the marketing page)

`/referral-program`: "Refer a company. **You both earn up to $1,000.**"

| Referral's checking balance | You each earn |
|---|---|
| **$20,000+** | **$500** |
| **$100,000+** | **$1,000** |

"Both you and your referral earn the same bonus, based on the checking balance they maintain for **30 consecutive days within their first 90 days**." Paid 30 days after the criteria are met.

### 6.2 Customer referral program (the terms page) does not match

`/referral-program-terms-conditions` documents only the **$500 / $20,000** version and describes the $100,000 threshold as the **superseded** scheme:

- "**Previously**: You earn $500 after 30 consecutive days of meeting all of the following criteria within 90 days of approval: use your Rho account for your company's payroll; make one or more deposits into your Rho checking account and maintain an average monthly balance of at least **$100,000**; complete a payroll transaction."
- "**New**: You and your referral each receive **$500 after 90 days** if you meet the following requirements: maintain an average monthly balance of at least **$20,000**."

**The $1,000 / $100,000 tier advertised on the marketing page appears in neither the old nor the new terms.** The terms page also self-contradicts on eligibility: it contains a full "Referring as a Rho Partner (**non-customer**)" walkthrough and then states, two paragraphs later, "This offer is **not available to non-Rho customers who refer as a Rho partner**." It also contradicts itself on timing ("**30 days** after the referred account has met all the specified requirements" vs "each receive $500 **after 90 days**").

Taxability: "The referral incentive for both the referrer and the referred customer will be considered **taxable income**." Not combinable with any other offer, non-transferable, revocable for "abusive, fraudulent, or terms-violating activities".

### 6.3 Affiliate program: 30% of Rho's gross profit on the referred entity's deposits

`policies/affiliate-terms-of-service`, dated **July 28, 2026**. This is the single most revealing document in the corpus about how Rho actually earns.

Qualification: the Referred Entity must (i) apply and be approved for a Rho checking account, (ii) make a deposit, and (iii) hold the account in good standing throughout the Payout Period.

> "you shall be eligible for a cash credit ('Affiliate Reward') into your Rho Account equivalent to **thirty percent (30%) of the Gross Profits** generated from your Referred Entity's **deposits** that were deposited during that month. You shall be eligible for Affiliate Rewards for a period of **twelve (12) months** after the first deposit made by your Referred Entity."

> "'**Gross Profits**' means the total gross revenue recognized by Rho **attributable to the Referred Entity's Rho Account deposits** during the applicable month, less attributable costs including **interest or yield paid to the Referred Entity, funding costs, payment processing fees, reserves, and other expenses**."

Conditions: new Rho customers only; anyone who applied in the last **120 days** is excluded; new products attached to existing accounts do not qualify; **no limit on the number of referrals**; paid within **30 days** of Rho determining the requirements were met; account must be open and in good standing at the moment of payment; cannot exceed 12 months of rewards; recipient is responsible for all taxes.

The page opens with "¹Terms and Conditions: To qualify for **the offer package listed above**" but **there is no offer package above it**. The footnote is orphaned from whatever landing page it was written for.

### 6.4 Referral Partner Program (TOS Addendum E §3)

- Compensation is "a referral fee, the specifics of which will be detailed in a **Statement of Work**". **No rate is published anywhere.**
- Attribution: a Referral qualifies if it signs up through the Landing Page, or if the Partner identifies it in writing and it created an account within the prior **10 days** or creates one within **60 days** of the notice, with Rho's written approval at Rho's sole discretion.
- "New Rho Customer" excludes anyone who has had discussions with Rho's sales team in the past **three (3) months**.
- Payment: quarterly, remitted "within **thirty (30) calendar days** of the end of the preceding quarter subject to a **minimum payment of $5 per quarter**. If the Referral Fee in any quarter does not meet or exceed $5, the amount will carry over."
- "Referral Fees may be **paused or reduced**, in good faith, in Rho's sole discretion, in the event one or more Activated Referrals become **materially delinquent in their credit card payments** to Rho." (Confirms Rho's partner economics are tied to customer credit performance.)
- Rho may update Referral Fees with **30 days' notice**, applying only to referrals made after the change.
- **Exclusivity clause:** "The Referral Partner agrees **not to promote any competitive product**... In the event that any such competitive product is marketed the Rho Service shall be clearly labeled and identified as the **preferred product**." Competitive product = any third-party deposit, treasury, debit, credit card, expense management, AP, or other Rho-offered product.
- Term: 1 year, auto-renewing; either party may terminate for convenience immediately.

---

## 7. Promotional offers, with conditions

| Offer | Reward | Condition | Source |
|---|---|---|---|
| Global nav banner | **$100** | "No ACH fees and get $100 when you deposit (terms apply)" | every page nav; **no terms page found in corpus** |
| Instagram / growth link | **$250 statement credit** | Open via the link, **deposit $5,000, keep it there 30 days** | grow__ig.txt |
| NerdWallet checking | **$350 statement credit** | Deposit **$10,000** and maintain a **$10,000 average daily** checking balance for the **first 90 days** | lp__nerdwallet-checking.txt |
| Affiliate banking LP | **$350 statement credit** | Same as above | lp__affiliate-banking.txt |
| NerdWallet startup cards | **$500 statement credit** | Spend **$1,000** (after returns/credits) on the Rho Corporate Card in the **first 3 months post-activation** | lp__nerdwallet-startup-cards.txt |
| Affiliate card LP | **$500 statement credit** | Spend **$2,500** (after returns/credits) in the **first 3 months post-activation** | lp__affiliate-card.txt |
| **SAFE note deposits** | **$100 statement credit per qualifying deposit**, max **$5,000** total | Each separate deposit of SAFE proceeds of **$10,000 or more**, held **30 consecutive days**. "Multiple statement credits may be earned up to a maximum total deposit amount of **$500,000**." Credit applied within 30 days after the 30-day requirement is met. "Statement credit **may be reported as income to the IRS**." | policies/promo-safe-notes, dated August 12, 2025 |
| Incorporation credit-back | **$400** | Deposit **$10,000 new money**, keep daily average balance **$10,000 above the starting level** for **60 days** | product/incorporation |
| **Clerky partnership** | **$1,600 bonus** | Incorporate with Clerky and open a Rho account; pre-EIN applications supported | clerky.txt |
| **SetupClaw** | Free white-glove AI assistant install **with a Mac Mini, "up to $2,400 value"** | Deposit **$300,000 USD within the first 90 days** after the Rho Checking account opens and **maintain it for 30 days** | setupclaw.txt |
| **Orion Sleep System** | One Orion Sleep System | **$225,000 in Rho Checking for 90 days, per Orion Sleep unit** | orion.txt (footnote marker ¹ present, **footnote text absent from the page**) |
| Times Square billboard | Rho pays for and designs a billboard in Times Square | Terms not stated on the page | lp__times-square-billboard-perk.txt |
| **Billboard photo campaign** | **$100 per verified upload, max $500 per person** | Post a photo of a Rho billboard in the SF Bay area on X showing "Rho" or "LOCK IN" plus an identifiable Bay Area landmark, tag @rhobusiness, submit at rho-location.vercel.app. Campaign period **Nov 5 to Nov 30, 2025**. Paid within 30 days of verification, as cash, electronic payment, or gift card at Rho's discretion. Participant owes all taxes. Grants Rho a perpetual, irrevocable, royalty-free, sublicensable worldwide license to the content, waives moral rights, caps Rho's total liability at **$500.00** | policies/rho-billboard-social-promotion, dated October 24, 2025 |
| **Escape with Rho sweepstakes** | 9 suitcases (ARV up to **$1,000** each) and 1 U.S. vacation (ARV up to **$6,000**) | April 23, 2025 5:00pm ET to December 31, 2025 5:00pm ET. Open to 50 states + DC **excluding Florida and New York residents**, 21+. Max 2 entries. Prize value reported on **Form 1099** | policies/rewards-terms-and-conditions |
| Rewards Marketplace | "**over $1M in partner deals**" (help center and startups page); clerky.txt says "**$600K+**" on one line and "**$1M+**" two lines later | Requires creating a separate **Built First** account with a business email. "Do not use your Rho password credentials when creating your Built First login." | help-center/general-rho-information/rhos-rewards-marketplace; perks.txt lists **147 perks** across "01 – 50 of 147" |

Named marketplace perks with prices: Clerky Company Lifetime Package **$794**; Stripe **50% off Stripe Atlas + $2,500 in Stripe credits**; Airtable **$1,000 in free credits**; Fin/Intercom **$6,500 in Fin AI Agent credits + Intercom helpdesk free for 1 year**; QuickBooks **30% off for 12 months**; Carta **20% first-year discount**; Slack **25% off Pro and Business+**; HubSpot for Startups **up to 30% off**; AWS **up to $5K in credits**; Ellis **$1,000 off your first visa application**; Zendesk Resolution Suite **free for 6 months**; Justworks **1 month free**; Thoropass **10% discount**; Remote **20% off**; Quo/OpenPhone **20% off first 6 months**.

Note the two statement-credit ladders are not coherent: the same **$500** card reward requires **$1,000** of spend on the NerdWallet page and **$2,500** on the affiliate page.

---

## 8. Every place Rho makes money

### Advertised (Rho names a price)

1. **Treasury advisory fee**: 0.15% to 0.60% per year on AUM, billed monthly, deducted from the portfolio cash balance, with automatic liquidation of holdings if cash is insufficient. Tier is set by **checking + Treasury combined**.
2. **FX margin: 1%** on every foreign-currency conversion, applied through Wise US Inc.
3. **Card acceptance on invoices: 2.9% + $0.30** per transaction, via Stripe, netted out of the payout.
4. **Incorporation: $400** up front (creditable), then **$1,000/year** platform access after year one and **$100 or $250 per contract**.
5. **$15** international wire "cover all fees" charge.
6. **$30** wire recall; **$20 to $45** on failed/returned domestic wires.
7. **3%/month late fee** (up to 6 months) on delinquent amounts; plus collection costs, attorneys' fees, and court costs.
8. **Up to 1%** on foreign card transactions (card addenda).
9. **Hourly billing** for assisting with recovery of misrouted funds (rate unpublished).

### Not advertised anywhere on the site

10. **Net interest income on deposits (the interest spread).** This is the core of the business and Rho never states it on any product, pricing, or help page. It is admitted only in the affiliate terms, which define Gross Profits as "total gross revenue recognized by Rho attributable to the Referred Entity's Rho Account **deposits**... less... **interest or yield paid to the Referred Entity, funding costs, payment processing fees, reserves, and other expenses**." Rho pays an affiliate 30% of that spread for 12 months, which means the spread on a single funded account is large enough to fund a 12-month revenue share. Corroborating structural evidence: every promotional offer in section 7 is priced in **deposit balance held for a fixed period** ($5K/30d, $10K/60-90d, $20K/30d, $100K/30d, $225K/90d, $300K/90d+30d), and Rho Platinum requires payroll, revenue, and 50% of company assets at Rho. Checking pays **0% interest** (no checking APY is published anywhere; the Rewards checking account's interest treatment is never stated).
11. **Interchange.** Rho's cards are World Elite Mastercard for Business, a premium commercial interchange tier. Rho never mentions interchange revenue. It does describe Mercury's model in detail in its own blog: "Mercury makes money in six different ways: interest earned on checking deposits... **merchant fees (interchange fees)** paid by merchants... earnings on **foreign exchange processing** on international wires... customer fees paid by Mercury Treasury customers... origination fees and interest earned on Mercury Venture Debt..." The word "interchange" appears in Rho's corpus only about competitors, never about Rho.
12. **Card credit with near-zero funding cost.** On Daily Terms the credit limit is sized off the customer's own available checking balance, there is no grace period, and repayment is auto-debited just after midnight for the same day's settled charges. Rho earns interchange while the customer's cash never leaves the platform for more than about 24 hours, and Rho holds a contractual right of setoff against all deposits.
13. **Float on settlement timing.** Rho's own settlement table shows money sitting on the platform or at a partner while the customer waits: incoming linked-account transfers **up to 5 business days**; incoming ACH 1-3 business days; remote check deposits **2-3 business days, generally up to 6-7**; checking to savings **2 business days**; savings to checking **next business day / 2 business days / Wed-Fri settlement windows** depending on which page you read; Treasury to checking **2-3 business days**; internal transfers between two different Rho businesses **1 business day**; printed checks **up to 8 business days** to arrive.
14. **Day-count and convention leakage on savings.** 30/365 accrual, interest posted only on the 5th business day of the month, rate paid on the **average monthly balance** rather than daily balances, and 0% paid below a $25,000 average monthly balance.
15. **Non-interest-bearing placement in the savings sweep.** "ADM may, from time to time, place a certain portion of Client's funds in a **non-interest bearing transaction account**" (ADM MSA). Rho and ADM, not the client, capture whatever that placement earns.
16. **The gap between "up to" and actual Treasury yield.** The advertised 4.66% requires a 100% Vanguard allocation the product caps at 50%, and the $20M+ tier. The realistic customer at $50K to $2M in a preset allocation earns materially less while paying 0.60%.
17. **Unredeemed and forfeited cashback.** Cashback expires after 12 months with no expiry notification ("Rho will not provide notifications regarding the impending expiration"), is forfeited entirely for any billing period not paid in full and on time, and is forfeited on card cancellation or account closure. All of it is booked as Rho's property until redeemed.
18. **Partner and marketplace economics.** Rho runs a 147-offer marketplace through Built First and a Mastercard World Elite benefits stack. No disclosure of whether Rho receives revenue share, referral fees, or placement fees from any of the 147 partners. The Referral Partner Program exclusivity clause shows Rho treats partner distribution as a contracted channel.
19. **Incorporation credit-back breakage.** The $400 is refunded only if the customer both deposits $10,000 of *new* money and holds the daily average $10,000 *above the starting level* for 60 days. Customers who fail either test pay $400 plus $1,000/year thereafter.
20. **Capital origination and servicing economics.** Rho routes lending to Lead Bank with Slope underwriting and servicing. Rho's share is never disclosed; the product page insists Rho "is not a broker-dealer" and "does not participate in the negotiation or execution of any transactions between customers and third-party financing sources", which sits awkwardly with its FAQ answer that Rho *is* the direct lender.

---

## 9. Settlement and float table (from Rho's own help center)

**Incoming**

| Type | Settlement |
|---|---|
| Linked account transfer (ACH) | Up to **5 business days** |
| ACH | 1-3 business days |
| Domestic wire | 1-2 business days |
| International wire | 1-5 business days |
| Remote check deposit | 2-3 business days, "generally up to **6-7 business days**" |
| Savings to checking | **2 business days** |
| Treasury to checking (T-Bills) | 2 business days if before 5 pm ET, 3 after |
| Treasury to checking (MULSX/VFSTX) | 2 business days if before 4 pm ET, 3 after |

**Outgoing**

| Type | Settlement |
|---|---|
| ACH | Same-day if created **before 2 pm ET and under $1mm**; next day after 2 pm ET or over $1mm |
| Domestic wire | Same-day if created **before 4:45 pm ET** |
| International wire | 1-3 business days, up to 5 |
| Printed check | **Up to 8 business days** to arrive via USPS |
| Internal transfer, same business | Within 1 hour |
| Internal transfer, **different** Rho businesses | **1 business day** |
| Checking to savings | 2 business days |
| Vendor-initiated ACH pull | Next day |

"Deposits made after 2PM ET on a business day or on a Saturday, Sunday or bank holiday are considered received on the next business day."

**Transfer limits** (help-center/payments/transfer-limits): domestic wires out **$90 million/day**; international wires out **$2.5mm/day**, in up to **$10 million/day**; ACH pull in **$20 million/day with a $10 million per-transaction limit**; ACH push out **$20 million/day aggregate**; linked external accounts **$5 million per transaction**, up to 5 business days to settle; remote check deposits no limit, but **over $15,000 in one business day may be subject to additional screening and delays**.

**Card repayment from an external account**: ACH cutoff 2:00 pm ET; "Card repayments can take **up to 4 business days to settle**."

---

## 10. Contradiction register

| # | Subject | Version A | Version B | Files |
|---|---|---|---|---|
| 1 | Domestic wire recall | "Domestic wire recall fee **$0**" | TOS §15: "a **$30 wire recall fee**"; blog: "Rho charges a $30 wire recall fee"; help center: failed returned domestic wires cost **$20 to $45** | pricing.txt / homepage.txt vs TOS + help-center/payments/fees-for-recalls-failed-wires |
| 2 | Homepage vs pricing fee table | Homepage row 07 "**Wire recall fee $0**" unqualified | Pricing row 07 "**Domestic** wire recall fee $0" | homepage.txt vs pricing.txt |
| 3 | Treasury minimum | **$50,000** (product page, help center, yield methodology, site-llms, seven mentions on the comparison page itself) | **$100,000** in the comparison table, and tier bottom row "**$100K–$2M**" | treasury-yield-comparison.txt lines 52, 109, 259, 291 |
| 4 | Number of Treasury instruments | "**three instruments**: 13-week T-Bills, MULSX, VFSTX" | "**four assets**", adding **IJTXX** as a cash sweep, and VFSUX replacing VFSTX for new money | product/treasury + treasury-yield-comparison vs help-center/treasury |
| 5 | Vanguard allocation | Headline 4.66% "assumes a **100% allocation** to the Vanguard fund" | "the short-term bond fund **capped at 50%** of your total allocation" | same page, product/treasury |
| 6 | Savings partner-bank count | "**400+** FDIC- and NCUA-insured institutions" | TOS Addendum C: "a deposit network of **more than 300** FDIC-insured banks and NCUA-insured credit unions" | marketing vs TOS |
| 7 | Savings to checking settlement | "next business day, if created before 1pm ET" | "**2 business days**" | help-center/banking vs help-center/payments/payment-settlement-times |
| 8 | Savings withdrawal processing | Next business day | ADM MSA: processed **Tue/Thu**, settled **Wed/Fri**; over **$3,000,000** is special handling | help center vs ADM MSA |
| 9 | $25,000 savings figure | "**$25,000 average monthly balance** to earn the rate", below which the balance earns 0% | "You deposit funds into Rho Savings (**$25,000 minimum**)" | product page vs help-center/banking/how-the-rho-savings-sweep-works |
| 10 | Referral top tier | "**up to $1,000**", $100,000 balance tier | Terms document **only $500 / $20,000**; the $100,000 test is described as the **superseded** scheme and required payroll | referral-program.txt vs referral-program-terms-conditions.txt |
| 11 | Referral eligibility | Full "Referring as a Rho Partner (non-customer)" instructions | "This offer is **not available to non-Rho customers** who refer as a Rho partner" | same page, referral-program-terms-conditions.txt |
| 12 | Referral timing | "$500 referral bonus **30 days after** the referred account has met all requirements" | "each receive $500 **after 90 days**" | same page |
| 13 | Capital lender | FAQ: "Is Rho a direct lender... **Yes.** Rho Capital is a single product" | Disclosure: "**Financing offered by third parties**... loans made by **Lead Bank**"; "serviced by **Slope**" | product__capital.txt, same page |
| 14 | Capital credit pull | "Applying doesn't involve a **hard pull** on your personal credit" | "**Application and consent to obtain personal credit report is required**" | help center vs product page disclosure |
| 15 | Card fee ceiling | "you... **will not be charged any fees except as disclosed herein**" | "**Fees are not limited to the aforementioned list and we reserve our right to charge additional or other fees**" | TOS Addendum A, same section |
| 16 | Cashback scope | "up to 2% cashback **on all spending**" | Four excluded merchant categories plus a list of excluded transaction types | site-llms.txt / site-llms-full.txt vs policies/cashback-rewards |
| 17 | Cashback redemption form | "issued to you in the form of a **statement credit**" | "transfer a specified dollar amount... into your **Primary Checking Account**", "deposited... **instantly**" | policies/cashback-rewards vs help-center/cards |
| 18 | Headline Treasury yield | Nav and product pages: **4.66%** | Homepage body and grow__ig: "**Up to 4.57% net yield**" | homepage.txt, grow__ig.txt |
| 19 | Webster / Santander size | "$76B in assets" (homepage) | "$75B FDIC insured institution" (lp__grow) | "Santander's **$327 billion**-asset U.S. banking organization" (site-llms) |
| 20 | Supported FX currencies | "a flat 1% fee is charged on FX transfers for **32 different currencies**" | Help center lists **22** currency codes, two of them restricted (GBP: "SWIFT payments currently unsupported"; PKR: "payments to businesses currently unsupported") | blog__airbase-vs-ramp vs help-center/payments |
| 21 | Currencies on local rails | "Certain currencies including **IDR, PHP, INR, and MYR** are processed via local payments rails" | IDR, PHP, and MYR are **not on the supported currency list** | help-center/payments/how-to-send-an-international-wire vs which-countries-and-currencies-are-supported |
| 22 | $15 SWIFT fee | "**optional** $15 SWIFT fee" | "in some corridors that fee is **mandatory with no opt-out**" | pricing.txt vs blog__rho-vs-chase |
| 23 | TOS version dating | Page header "**August 4, 2026**" | "Version 7.0.0, Last updated **August 27, 2026**" | policies/terms-of-service |
| 24 | Invoicing T&C dating | Header "**August 25, 2026**" | "Last amended **August 26, 2026**" | policies/invoicing-terms-and-conditions |
| 25 | Amex annual fee **[Rho claim]** | "$895 annual fee" | "$695 (Business Platinum)" | versus__amex.txt vs lp__affiliate-banking.txt |
| 26 | Relay top plan **[Rho claim]** | "$90/mo Scale" | "$120/mo Scale plan required for the top rate" | treasury-yield-comparison.txt vs product__business-savings-account.txt |
| 27 | Mercury Treasury yield **[Rho claim]** | "3.01%–3.81% net" (08/02/2026) | "3.13% to 3.89%" (2026-09-06); "Up to 3.89%" (08/28/2026) | treasury-yield-comparison vs business-savings-account vs business-banking |
| 28 | Same $500 card promo | Spend **$1,000** in first 3 months | Spend **$2,500** in first 3 months | lp__nerdwallet-startup-cards vs lp__affiliate-card |
| 29 | Rewards Marketplace value | "$600K+ in exclusive startup perks" | "$1M+ perks and rewards" | clerky.txt, two lines apart |
| 30 | Card fee payer framing | "This fee is **paid by your business**. Your customer pays only the invoice amount." | "we **deduct** 2.9% + 30¢ from the payment and deposit the rest into your Rho account" | help center vs changelog |

---

## 11. What is conspicuously NOT stated

1. **How Rho makes money.** No page in the corpus answers this. A search for "how does Rho make money", "Rho makes money", or "revenue from" across 536 pages returns **zero** hits about Rho. The same corpus contains detailed six-way and five-way breakdowns of **Mercury's** revenue model in Rho's own blog posts.
2. **Interchange.** Never mentioned in connection with Rho, only with Navan and Mercury.
3. **Checking APY.** No interest rate is ever quoted for Rho Checking. The comparison tables answer "Yield on idle cash" for Rho with "See current rate at the Rho Business Savings Account" rather than a number.
4. **Whether the Rewards checking account earns interest.** Never stated.
5. **Rho Capital's price.** No rate, APR, factor rate, fee range, or worked example anywhere.
6. **The Treasury ADV-2A Wrap Fee Brochure contents.** Linked from every page footer, never summarized. The FAQ on the pricing page answers "How much does Rho Treasury cost?" by deferring to it entirely.
7. **Fund expense ratios** for IJTXX, MULSX, VFSTX, or VFSUX, even though every quoted yield is net of them and the VFSTX-to-VFSUX migration is justified by "a lower expense ratio".
8. **The FX spread mechanics.** Rho quotes a "1% FX rate" but never says 1% of what, or whether the underlying rate is Wise's mid-market rate. The API transaction-type enum has `international_wire_fee` and `wire_fee` but **no FX or conversion fee type**, which implies the 1% is embedded in the converted amount and never surfaces as a separate posted line item a customer or accountant can audit.
9. **The $100 deposit bonus terms.** Advertised in the global navigation on every page ("get $100 when you deposit (terms apply)"). No terms page for it exists in the corpus or the 1042-URL sitemap.
10. **The Orion promotion's terms.** The page carries a "Terms and conditions apply.¹" marker with no footnote text.
11. **The affiliate offer package.** The affiliate terms begin "To qualify for the offer package listed above" on a page with nothing above it.
12. **Incoming wire fees.** Never stated as $0 explicitly, only implied.
13. **Per-transaction ACH fees for payroll debits.** Rho's own published blog carries an unedited internal editorial marker twice: "**[VERIFY: Rho's per-transaction ACH fee for payroll debits]**" (blog__gusto-alternatives.txt). Rho's own writers could not confirm this.
14. **The /policies index is incomplete.** It lists four policies: Terms of Service, Reward Terms, Privacy Policy, CAN-SPAM. It does **not** list the Cashback Rewards terms, the Yield Methodology, the Invoicing terms, the Affiliate terms, the SAFE promo terms, or the billboard campaign terms, all of which are live pages.
15. **"Rewards Terms" is ambiguous by design or accident.** The footer link labeled "Rewards Terms" points to `/policies/rewards-terms-and-conditions`, which is the **expired Escape with Rho sweepstakes** (April 23 to December 31, **2025**). The terms that actually govern the headline 2% cashback live at `/policies/cashback-rewards`, titled "Reward Terms", dated **April 10, 2025**, and are not linked from the footer or the policies index.
16. **Whether the Treasury advisory fee is charged on checking balances.** The help center says "AUM includes the combined balance of your Rho Checking and Treasury accounts", and the fee is described as charged "on assets under management". If read literally, a Treasury client pays an advisory fee on non-advised, zero-yield checking cash. No page clarifies this.
17. **Cashback rate at the account level.** The Rewards Account help article says clients can "**manage your cashback rate**" in the Rewards Account, a capability described nowhere else.
18. **Rho's revenue share, if any, from the 147 Rewards Marketplace partners** or from Built First.

---

## 12. API evidence: the fee events that actually exist in production

The `transaction_type` enum in `/api/v1/openapi/transactions` (42 values) is the most honest fee disclosure Rho publishes, because it enumerates the events the ledger can emit:

```
ach_credit, ach_debit, ach_return, adjustment_credit, adjustment_debit,
card_credit, card_debit, card_refund, check_deposit, check_payment,
credit_cashback, credit_repayment, credit_repayment_refund, internal_transfer,
international_wire_fee, international_wire_fee_refund, international_wire_in,
international_wire_out, rewards_accrual, rewards_cashback_redemption,
savings_deposit, savings_interest, savings_withdrawal,
treasury_deposit, treasury_fee, treasury_interest,
treasury_market_value_adjustment, treasury_maturity, treasury_sale,
treasury_withdrawal, wire_fee, wire_in, wire_out
```

Account types: `checking`, `savings`, `credit`, `investment`, `rewards`.

Reads:
- **`wire_fee` exists as a first-class, non-international transaction type.** Domestic wire fee events are representable in the ledger despite "$0 domestic wires".
- **`treasury_fee`** is the advisory fee posting.
- **`savings_interest`** and **`treasury_interest`** are the only income postings to customers; there is **no `checking_interest`**.
- **No `fx_fee`, `conversion_fee`, `card_fee`, `subscription_fee`, `late_fee`, or `invoice_fee` type.** The 1% FX margin, the 2.9% + $0.30 card fee, and the 3%/month late fee are not representable as discrete ledger events in the public API, so a customer reconciling through the API cannot see them itemized.
- `treasury_market_value_adjustment` confirms NAV movement flows through the ledger, consistent with "principal can lose value".

Live sandbox data confirms `rewards` accounts exist with a `balance` and that daily card repayment posts as `credit_repayment` with memo "Daily credit repayment for date 2026/06/24", one day after the charge.

---

## 13. As-of date register

| Fact | As-of date | Source |
|---|---|---|
| Treasury headline 4.66% and all tier yields | **09/11/2026** | product/treasury, treasury-yield-comparison, all page footers |
| 13-week T-Bill benchmark 3.81% | **09/11/2026** (comparison table); footnote elsewhere says **08/02/2026** | treasury-yield-comparison |
| Treasury sell-order settlement to checking, 2 business days | **08/03/2026** | policies/yield-methodology |
| Yield Methodology policy | published **August 3, 2026** | policies/yield-methodology |
| Business Savings up to 1.00% APY, 400+ banks, $75M | **August 2026** | product/business-savings-account |
| Cashback rate schedule ("up to 2%") | **08/21/2026** | site-llms-full.txt |
| Cashback Rewards Program terms | **April 10, 2025** | policies/cashback-rewards |
| Rewards Terms and Conditions (sweepstakes) | **September 11, 2025** | policies/rewards-terms-and-conditions |
| Terms of Service | header **August 4, 2026**; "Version 7.0.0, Last updated **August 27, 2026**" | policies/terms-of-service |
| Invoicing Terms | header **August 25, 2026**; "Last amended **August 26, 2026**" | policies/invoicing-terms-and-conditions |
| Affiliate Terms of Service | **July 28, 2026** | policies/affiliate-terms-of-service |
| SAFE Note offer terms | **August 12, 2025** | policies/promo-safe-notes |
| Billboard campaign terms | **October 24, 2025**; campaign ran **Nov 5 to Nov 30, 2025** | policies/rho-billboard-social-promotion |
| Rho pricing "only standard payment fee is 1% FX" | **08/02/2026** | site-llms.txt |
| Rho Capital claims | "Product claims current as of **September 2026**" | product/capital |
| Rho Treasury product claims | "Product claims current as of **August 2026**" | product/treasury |
| Rho Treasury $50K minimum | **08/04/2026** | site-llms-full.txt |
| Incorporation credit-back terms | **08/02/2026** | site-llms-full.txt |
| International wire USD fee $0 and $15 flat toggle | **08/02/2026** | help-center/payments/transfer-faqs |
| Mastercard World Elite benefits | "Benefits available as of **September 1, 2026**" | perks.txt |
| Apex Ascend custody cutover | accounts opened **on or after July 23, 2026** are on Ascend | help-center/treasury/understanding-rho-treasury |
| Apex vs Interactive Brokers custody | Apex "for accounts opened **after July 2024**", Interactive before | product/treasury |
| Webster/Santander asset figure | "at close **08/20/2026**" | site-llms-full.txt |
| Competitor data, treasury comparison | **08/02/2026** (Mercury, Brex, SVB, Axos); Bluevine **08/05/2026** | treasury-yield-comparison |
| Competitor data, savings and treasury product pages | **2026-09-06** and **08/20/2026** | product/business-savings-account, product/treasury |
| Competitor data, corporate cards | **2026-09-08** | product/corporate-cards |
| Competitor data, invoicing | **2026-09-08** | product/invoicing |
| Competitor data, business banking | **09/06/2026** | product/business-banking |
| Competitor data, affiliate LP comparison | **09/11/2026** | lp__affiliate-banking |
| Ramp and Brex pricing claims | **08/02/2026**, **08/03/2026**, **08/11/2026** | versus__ramp, blog posts |
| Mercury pricing / support claims | **08/17/2026** | versus__mercury |
| Invoice card payments shipped | **August 31, 2026** | changelog |
| Rho Incorporation shipped | **August 31, 2026** | changelog |
| Rho API shipped (read-only) | **August 3, 2026** | changelog |
| site-llms-full.txt baseline verification | **08/04/2026**; file "Last updated 08/21/2026" | site-llms-full.txt |

---

## 14. Bottom line

Rho's published price is a near-zero fee schedule with one named exception (1% FX). The actual price is the balance sheet: the product is priced so that the customer's cash, payroll, and revenue all sit at Rho, and the returns to Rho come from the spread on those deposits, interchange on cards collateralized by the same deposits, and a 15 to 60 basis point advisory fee that is tiered on checking-plus-Treasury balances. The one document in the entire corpus that names this model is the affiliate agreement, which promises partners **30% of the gross profits Rho recognizes on a referred company's deposits for twelve months, net of the interest Rho pays that company**. Everything else about Rho's revenue has to be inferred from promotional terms priced in deposit balance, from a Platinum tier that costs 50% of company assets, and from a public API that can post a `wire_fee` but has no line item for a 1% FX margin.
