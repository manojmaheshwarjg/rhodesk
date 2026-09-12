# Rho (rho.co): Product Dossier: Raw Findings

Compiled 2026-09-11 from a local corpus of rho.co marketing pages, help-center articles, policy pages, docs.rho.co, the public API reference, and captured sandbox API responses.

**Labeling convention used throughout**
- `[Rho claim]` = asserted only by Rho, unverified, especially claims about competitors.
- `[HC]` = from the Rho Help Center (operational detail, generally more specific and more honest than marketing pages).
- `[Marketing]` = from a `/product/*` or other marketing page.
- `[Legal]` = policy / terms / footnote text.
- `[API]` = docs.rho.co or the sandbox API.
- Dates are carried verbatim as Rho states them. Rho's "as of" stamps range from **12/10/2025** to **09/11/2026**.

---

## 0. The one-line frame

Rho is **not a bank**. Every page repeats: *"Rho is a fintech company, not a bank or an FDIC-insured depository institution."* The legal entity is **Under Technologies, Inc. DBA Rho Technologies** (© 2019–2026), HQ **100 Crosby Street, New York, NY 10012**, phone **1 (855) 7-GETRHO / 1-855-743-8746**, email **clientservice@rho.co**.

Rho sells a **$0-software-fee bundle**: the money is made on interchange (cards), the Treasury advisory fee (0.15%–0.60% AUM), FX (1%), and deposit economics, not on subscriptions. Every product page repeats the same anchor: `$0 monthly fee, $0 per-user fee, $0 platform fee, $0 domestic ACH/wire/check`.

---

## 1. Who actually provides each financial service

This is the single most important structural fact about Rho: **it is an orchestration layer over at least seven distinct regulated/third-party providers.**

| Product | Underlying provider (verbatim from Rho) | Regulatory wrapper |
|---|---|---|
| Business Checking | "Checking account and card services provided by **Webster Bank, a division of Santander Bank, N.A.** Member FDIC" | FDIC, $250,000 per entity |
| Business Savings | "Savings account services and up to $75,000,000 in FDIC deposit insurance per entity are provided by **American Deposit Management Co.** and its partner banks (a network of **400+** FDIC- and NCUA-insured institutions, as of August 2026)" | FDIC via sweep; program is "American Deposit Management, LLC and its wholly owned subsidiary ADM Consulting, LLC" |
| Corporate Cards | "The Rho Corporate Cards are issued by **Webster Bank, a division of Santander Bank, N.A.**, member FDIC pursuant to a license from **Mastercard**". Tier is **Mastercard World Elite Business** | Mastercard network |
| Treasury | Adviser: "**RBB Treasury LLC dba Rho Treasury**, an SEC-registered investment adviser and **subsidiary of Rho**". Custody: "**Apex Clearing Corp.** ('Apex') and **Interactive Brokers LLC** ('Interactive'), registered broker dealers and members FINRA/SIPC" | SEC RIA + SIPC $500K (incl. $250K cash) |
| Capital (credit line) | Footer disclaimer: "**Slope** is a financial technology company, not a bank. Business-purpose loans made by **Lead Bank** and subject to credit approval." Body text: "Fees vary based on risk assessment and loan term, and are set when **Slope** underwrites your line." | Lead Bank origination |
| International / FX payments | "International and foreign currency payments services are provided by **Wise US Inc.**" | n/a |
| Invoice card acceptance | "Card payments are processed securely through **Stripe**" [HC]. "Rho creates and manages a separate [Stripe] account for your business" | Stripe |
| Incorporation | "Rho Incorporation is **not a law firm or accounting firm**"; formation docs "reviewed and signed off by a licensed attorney" (unnamed) | n/a |
| KYC / data aggregation | "**Plaid**, **Finicity**, and **Codat**" [HC] | n/a |

**Note the asymmetry:** Rho names Webster/Santander, ADM, Apex, Interactive, Mastercard, Wise, and Stripe openly. It names **Slope** and **Lead Bank** only in a footer disclaimer at the very bottom of `/product/capital`, while the FAQ on the same page says the opposite (see §17, Contradictions).

---

## 2. Platform-wide fee schedule (verbatim)

From `/pricing` ("Rho fee summary") and the homepage fee table. The two versions **differ**.

| # | Line item | /pricing | Homepage |
|---|---|---|---|
| 01 | Same-Day ACH, wires, and checks | $0 * | $0 * |
| 02 | Subscription fees | $0 | $0 |
| 03 | Checking account minimum fees | $0 | $0 |
| 04 | Connected in-platform capabilities: AP, Expense & Accounting Automation | $0 | "Built-in Bill Pay + Invoicing $0" |
| 05 | Per-user fees | $0 | $0 |
| 06 | Foreign currency transfer | **1%** | **1%** |
| 07 | Wire recall fee | "**Domestic** wire recall fee $0" | "Wire recall fee $0" (no "domestic" qualifier) |

**/pricing footnote (verbatim):** *"Applicable fees for the checking account include a **$30 international wire recall fee**, an optional **$15 SWIFT fee**, and a **1% foreign currency conversion fee**. International wires in USD can be subject to additional fees set by recipient, correspondent, or intermediary banks, in addition to the SWIFT network. Unless prohibited by law, the late fee shall be **three percent (3%) of the delinquent payment balance for each month that the balance remains unpaid for up to six (6) months**."*

**Homepage footnote (verbatim, differs):** *"Applicable fees for the checking account include an optional $15 SWIFT fee and 1% foreign currency conversion fee."* Note: **the $30 international wire recall fee is dropped from the homepage footnote.**

Fees not in either table, found only in the help center:
- **Domestic wire that fails and is returned: "a fee of around $20 – $45 will be deducted from your Rho account"** [HC, `fees-for-recalls-failed-wires`]. This directly qualifies the "$0 wire recall fee" headline.
- **International wire "Cover all recipient delivery fees" toggle: flat $15** (as of 08/02/2026) [HC].
- **Invoice card acceptance: 2.9% + $0.30 per transaction, paid by the business** [HC + changelog 08/31/2026]. Not stated anywhere on `/product/invoicing`.
- **Treasury management fee: 0.15%–0.60% annually, billed monthly.**
- Help-center summary [HC, `pricing-requirements`]: *"The only standard payment fee is 1% on foreign-currency transfers."* This is contradicted by the $15 SWIFT, $30 intl recall, $20–45 failed-wire, and 2.9%+$0.30 card fees above.

---

## 3. Business Banking (Business Checking): `/product/business-banking`

### What it literally is
A **business checking account** for US-incorporated LLCs and corporations, held at Webster Bank (a division of Santander Bank, N.A.). Rho is the software/front end. Marketed as "a fintech business bank account built for startups, not branch banking."

### Mechanics
Four-step onboarding: (01) gather EIN + formation docs + government photo ID for any owner ≥25% (multi-member LLCs also need the operating agreement); (02) apply online, "**less than 10 minutes**", "No branch visit, no paper forms, no faxing anything"; (03) manual verification review; (04) fund and transact.

Sub-accounts: *"All businesses get access to a primary Rho Checking Account. You can easily create additional sub-accounts to organize cash for purposes like payroll or taxes."* [HC]. But *"Each Rho customer gets up to $250,000 in FDIC deposit insurance coverage **across all** Rho checking accounts"* [HC], i.e. the sub-accounts do not multiply coverage.

Account numbers: Savings gets **no account or routing numbers**; Checking does (sandbox shows masked `account_number_last_4` and `routing_number_last_4`, all checking accounts sharing routing `...0089`).

### Eligibility / minimums
- Must be a **registered LLC or corporation**. **"Sole proprietorships aren't eligible on Rho."**
- EIN required, **or** an SS-4 while the EIN application is pending: *"an uploaded SS-4 lets you start depositing; the EIN itself unlocks outgoing transfers."*
- Pre-EIN window: **"Non-VC-backed founders get a 30-day pre-EIN window before the EIN arrives; VC-backed founders get 60 days. Both require manual review, and neither is guaranteed."**
- Geography [HC]: entity must be **incorporated in the US**, and must either hold a **US Operating Address** or have **one business owner based in the US with a valid SSN**. Ineligible locations: **Cuba, Iran, North Korea, Russian Federation, South Sudan, Sudan, Syria, Venezuela.**
- **"Virtual addresses from Regus or any other provider are not permitted."** [HC]
- Prohibited industries [HC]: betting/casino gaming chips; adult dating/escort; drug stores, pharmacies and cannabis; drugs, proprietaries and sundries; stamp and coin stores; quasi-cash, currency, money orders, travelers checks; pawn shops; bearer shares; bail and bond payments; currency exchange businesses; nested MSBs/money transmitters; firework sales; online dating services.
- **No minimum opening deposit, no minimum balance.**

### Limits (help center only; absent from the marketing page)
| Rail | Limit |
|---|---|
| Domestic wires out | **$90 million per day** (larger "can be accommodated… communicated to us in advance") |
| International wires out | **$2.5mm per day** |
| International wires in | up to **$10 million per day** |
| ACH in (pull) | **$20 million/day**, **$10 million per transaction** |
| ACH out (push) | **$20 million/day** aggregate |
| Linked external account transfers | **$5 million per transaction**; settle up to **5 business days** |
| Remote check deposit | **No limit**, but 6–7 business days to clear; deposits **over $15,000 in one business day** may get extra screening |

### Settlement times [HC, `payment-settlement-times`]
Outbound: **Outgoing ACH** same-day if created **before 2pm ET and under $1mm**, next day after 2pm ET or over $1mm. **Outgoing domestic wire** same-day if before **4:45pm ET**. **Outgoing international wire** 1–3 business days, up to 5. **Outgoing printed check** up to **8 business days** via USPS. **Internal transfer same business** within 1 hour; **between different Rho businesses** 1 business day. **Checking→Savings** 2 business days. **Checking→Treasury** 2 business days if before 5pm ET (T-Bills) / 4pm ET (mutual funds), else 3.
Inbound: linked account up to 5 business days; ACH 1–3; domestic wire 1–2; international wire 1–5; remote check deposit 2–3 (generally up to 6–7); Savings→Checking 2 business days; Treasury→Checking same T-Bill/fund cutoffs.
*"Deposits made after 2PM ET on a business day or on a Saturday, Sunday or bank holiday are considered received on the next business day."* *"payments over $1mm could take an extra day to settle."*

Check mechanics [HC]: funds are **set aside immediately** when a check is sent but do not leave the account until the check is cashed; **unclashed checks are voided automatically after 90 calendar days**; returned checks go back to the business address on file.

### Fees
$0 monthly, $0 minimum-balance, $0 domestic ACH, $0 domestic wire. See §2 for the exceptions.

### Stated benefits
"$0 monthly fees, ACH fees, and wire fees"; "<10 min to apply"; "Up to $75M in FDIC deposit insurance with a Rho Business Savings Account, a separate account"; "Real humans support from a team that knows your account"; 24/7 human support by phone, email, live chat, and (since June 2026) iMessage and WhatsApp; QuickBooks / NetSuite / Sage Intacct native integrations, Xero via bank feed.

### Caveats / footnotes (verbatim)
> "¹ The Rho Business Savings Account is a separate account from Rho checking. Savings account services and up to $75,000,000 in FDIC deposit insurance per entity are provided by American Deposit Management Co. and its partner banks (a network of 400+ FDIC- and NCUA-insured institutions, as of August 2026), subject to FDIC requirements and limitations. **Coverage reflects the partner-bank network's capacity as of August 2026 and is not a contractual guarantee.** Checking deposits are FDIC-insured up to $250,000 per entity through Webster Bank, a division of Santander Bank, N.A., Member FDIC."

> "What's the catch? The only real limit is on cashback: it's earned on up to $1,000,000 in eligible card spend per calendar year and is subject to program terms. Every fee on this page is $0."

> "FDIC deposit insurance coverage is available only to protect you against the failure of an FDIC-insured bank that holds your deposits… **It does not protect you against the failure of Rho or other third party.**"

Bank partner size claim (homepage): *"Rho partners with Webster Bank, a division of Santander Bank, N.A. Member FDIC — a nationally-charted institution with **$76B in assets**."* (typo "charted" is in the source).

### Competitor table [Rho claim], "Competitive data collected from Mercury, Bluevine, and Chase websites as of 09/06/2026"
| | Rho | Mercury | Bluevine | Chase |
|---|---|---|---|---|
| FDIC insurance | $250K checking; up to $75M via separate Savings | Up to $5M via partner-bank sweep | Up to $3M via Coastal Community Bank program banks | "Member FDIC; no dollar figure published" |
| Monthly fee | $0 | $0 free; Plus $29.90/mo; Pro $299/mo | $0 Standard; Plus $30/mo; Premier $95/mo (waivable) | $15–$95/mo, waived at minimum balance |
| Yield on idle cash | "See current rate at the Rho Business Savings Account" | "Up to 3.89%, tiered by balance (as of 08/28/2026)" | 1.3% Standard / 1.75% Plus / 3.0% Premier | "No numeric rate published" |
| Card cashback | Up to 2% with Rho Platinum | 1.5% flat | "Up to 4% in select categories only" | none |
| Live human support | Yes | "No stated hours" | "No stated hours" | "No stated hours" |
Rho's own footnote on Bluevine: *"Bluevine's cashback applies only at participating merchant categories (restaurants, fuel with caps, hotels capped at $20/transaction), not as a flat rate on all spend."*

---

## 4. Business Savings: `/product/business-savings-account`

### What it literally is
A **separate deposit account** from checking, funded only from Rho Checking, running an **administered sweep** through **American Deposit Management (ADM)** across **400+ FDIC- and NCUA-insured institutions**. Underlying structure per [HC]: *"an administered money market deposit account."* Per the ADM Master Services Agreement, the product component is the **"American Money Market Account (the AMMA)"**; a second component, the **"American Term Deposit Account" (CD Accounts)**, exists in the contract but is **not marketed by Rho anywhere**.

### Mechanics
1. Activate from the dashboard: *"There is no separate application and no new login"* [Marketing]. But [HC] says: navigate to Savings → **Request Access** → *"A member of the Rho Client Service team will prepare and send you a **DocuSign** agreement"* → sign → submitted to the partner for review → account opened, possibly with additional due-diligence questions. **These two descriptions do not match.**
2. Fund from Rho Checking only. *"Transfers into your Rho Savings account can only be initiated from a Rho Checking account."*
3. ADM allocates funds across network institutions in increments **below the $250,000 per-bank FDIC limit**. *"$5 million in Rho Savings: the program spreads it across 20+ institutions, each holding less than $250,000."*
4. One balance, one dashboard view. **No account or routing numbers are issued for Savings.**

### Rate and interest mechanics
- **Up to 1.00% APY, variable, set monthly (as of August 2026; terms apply).**
- **$25,000 average monthly balance required to earn interest.** Below that, *"the balance earns 0% with Rho."*
- *"The rate applies against your average monthly balance, not a single day's snapshot."*
- Interest **accrues daily, paid monthly, posted on the 5th business day of each month** (next business day if the 5th is a weekend/holiday).
- **Interest is calculated using a 30/365 day convention.** [HC]
- Rho's own worked example: *"At that threshold, a year at the full rate works out to roughly **$250** before compounding."*

### Limits
- **Unlimited transfers in.**
- **Six (6) transfers out per month.** (ADM contract: *"Withdrawals are limited to six (6) per month."*)
- ADM operational mechanics [Legal, buried in the T&C page]: withdrawals are processed **Tuesdays and Thursdays**, settling **Wednesdays and Fridays**; requests **≤$3,000,000** received by **12:00 P.M. Central** on a processing day settle next settlement day; **>$3,000,000 is "special handling"** settled at a mutually acceptable date. *"The accounts at the Program Institutions do not include check writing privileges, ATM transactions, or debit card transactions."*
- Settlement [HC]: Checking→Savings typically **same business day if created before 1pm ET**; Savings→Checking typically **next business day if before 1pm ET**. (The marketing page says "within 2 business days typical" and the settlement-times table says "2 business days". Three different numbers for the same movement.)

### Fees
$0 monthly fee on Savings.

### Caveats / footnotes (verbatim)
> "¹ Rho Business Savings is a separate account from Rho checking. Savings account services and up to $75,000,000 in FDIC insurance per entity are provided by American Deposit Management Co. and its network of 400+ partner banks (as of August 2026), **reflecting program capacity on a commercially reasonable efforts basis, not a guarantee.**"

> "…designed to keep no single bank's share above $250,000 **under normal operating conditions**, subject to the terms of the program agreement."

The ADM agreement itself is franker than the marketing: *"if funds in excess of $250,000 are deposited into or withdrawn from the Program in a single day, **for a limited amount of time (intraday or overnight), the entire amount of the withdrawal or deposit may be held at one Program Institution**."* And the agreement makes the client **waive extended deposit insurance** by signing Exhibit A: *"By signing Exhibit A, Client expressly waives extended deposit insurance"*. In other words, amounts above FDIC limits are explicitly **not** secured by collateral or surety bond unless separately elected.

Also in the agreement: *"All Clients other than public unit depositors, **represent and warrant that they are an 'accredited investor'**"*. This is an eligibility condition Rho never mentions on the marketing page.

Which banks: *"The current list of network institutions is available from Rho support on request."* It is **not published.**

### Competitor table [Rho claim], "as of 2026-09-06"
| | Rho | Mercury | Brex | Relay |
|---|---|---|---|---|
| FDIC coverage | Up to $75M/entity | Up to $5M | Up to $6M | Up to $3M |
| Savings APY | Up to 1.00% | No standalone savings (Treasury 3.13%–3.89%) | No standalone savings (Brex Treasury variable) | Up to 3.00%, tiered by plan |
| FDIC-insured deposit account | Yes | No (SIPC only) | No (SIPC only) | Yes |
| Minimum for top rate | $25,000 avg monthly balance | $250,000 across all Mercury accounts | No minimum | No balance minimum |
| Cost to access rate | $0 | $0 to open; 0.15%–0.60% asset fee | $0 | $0 Starter; **$120/mo Scale plan** required for top rate |
| Top rate requires paid plan | No | No | No | Yes |

Rho's own honest admission on this page: *"though Mercury and Brex's treasury yields run higher on funds that aren't FDIC-insured at all."*

---

## 5. Treasury: `/product/treasury` + `/treasury-yield-comparison`

### What it literally is
A **securities investment account**, not a bank account. Advised by **RBB Treasury LLC dba Rho Treasury** (SEC-registered investment adviser, Rho subsidiary), custodied at **Apex Clearing Corporation** (accounts opened after **July 2024**) and **Interactive Brokers LLC** (before that). Securities are *"held directly in your business's name and are not pooled with other clients' assets."*

### The asset menu: the marketing page and the help center disagree on how many assets exist

**[Marketing]** says **three**: *"US Treasury Bills, an ultra-short income fund, and a short-term bond fund."*
**[HC]** says **four**: *"You can hold up to 4 assets simultaneously."*

| Ticker | Asset | Description (verbatim, [HC]) | Suitable for | Liquidity |
|---|---|---|---|---|
| **IJTXX** | JPMorgan U.S. Treasury Plus Money Market Fund | "A government money market fund holding U.S. Treasury securities and repurchase agreements backed by them. Offered as a **cash sweep**… fixed $1.00 NAV and no minimum" | "cash you may need on short notice" | **Same business day** if submitted by 3:00 PM ET |
| **T-Bills** | 13-week (90-day) U.S. Treasury Bills | "purchased at a discount and redeemed at face value at maturity… no NAV variability". Purchased in **$1,000 increments** | "cash you won't need for at least 3 months" | Next business day, cutoff **5:00 PM ET** |
| **MULSX** | Morgan Stanley Ultra-Short Income Portfolio | "commercial paper, corporate debt, and asset-backed securities. **It is not a money market fund** - NAV is variable but designed to remain highly stable" | "4 to 6 months" | 1–2 business days, cutoff **4:00 PM ET** |
| **VFSUX / VFSTX** | Vanguard Short-Term Investment-Grade Fund (Admiral / Investor) | "investment-grade corporate bonds… **carries meaningful NAV variability** due to interest rate movements… **Do not allocate near-term operating cash to VFSUX**" | "at least 1 year" | 1–2 business days, cutoff **4:00 PM ET** |

**IJTXX and the Apex Ascend migration [HC]:** *"VFSUX and the IJTXX money market fund sweep are available through **Apex Ascend**, our new custody platform. If you joined Rho Treasury **on or after July 23, 2026**, your account is on Ascend… If you joined before July 23, your account will migrate to Ascend in the coming months."* **IJTXX is not mentioned on the public treasury page or the yield-comparison page at all.**

**VFSTX→VFSUX transition [HC]:** same fund, different share class; VFSUX has lower expense ratio and is *"the only Vanguard fund available for new allocations"*; existing VFSTX is not force-sold; sales are **FIFO**, so VFSTX is sold first; *"VFSTX disappears when its balance reaches $0.00."*

### Allocation mechanics
- Percentage-based, **5% increments, must total 100%.**
- **Vanguard allocations are capped at 50% of the portfolio** (VFSTX + VFSUX combined). Existing >50% allocations grandfathered but must be reduced before any edit "unless we have approved a higher limit for your account."
- Four presets [HC]: **Maximum liquidity** (same day) 100% IJTXX; **Capital preservation** (3 months) 50% IJTXX / 50% T-Bills; **Balanced income** (4–12 months) 40% IJTXX / 60% MULSX; **Optimized yield** (12+ months) 15% IJTXX / 60% MULSX / 25% VFSUX; plus Custom.
- **Funding order:** *"New funds top up IJTXX first, then go to your other assets."* Investments settle 1–2 business days; IJTXX same business day.
- **Rebalancing:** every deposit/maturity/dividend auto-invests to target; editing target triggers an immediate rebalance (**2 to 4 business days**, no changes allowed while in progress); **monthly rebalance on the 6th of each month if any holding has drifted >5% from target.**
- **Withdrawal rule (important and non-obvious):** *"We do **not** split a withdrawal across IJTXX and your other assets, and you cannot select which assets are sold."* If the request ≤ same-day available balance, it comes entirely from IJTXX/cash; if larger, the **entire** amount is sold proportionally from T-Bills/MULSX/Vanguard and IJTXX is left untouched. Shares sold **FIFO**.
- **Auto-transfer rules:** evaluated at **8:00 a.m. ET**; max **5 active rules per organization**; one rule per account pair; circular flows blocked; Treasury→Checking rules are limited to preset cadences (**weekly**, **twice monthly preset to the 11th and 25th**, or **monthly**) because "Treasury → Checking transfers can take up to 3 business days to settle"; **only one Checking account can be funded by Treasury**; legacy sweep rules were auto-migrated to *"a weekly schedule with Thursday settlement."*

### Eligibility / minimums
**[HC] four conditions:** be a U.S.-registered business; operate primarily in the United States; have at least one founder based in the United States; **maintain at least $50,000 in total deposits**. Application "takes less than 10 minutes"; approval "typically up to **2 business days**". KYC: SSN/TIN/Passport/EIN, possibly formation docs, business license, certificate of good standing, beneficial ownership and authorization forms.

### Fees, tiered on AUM, billed monthly
| Total AUM | Annual fee |
|---|---|
| $20M+ | **0.15%** (15 bps) |
| $10M–$20M | **0.25%** |
| $5M–$10M | **0.35%** |
| $2M–$5M | **0.45%** |
| Under $2M | **0.60%** (max) |

**AUM definition [HC]:** *"AUM includes the combined balance of your Rho Checking **and** Treasury accounts."* (The marketing footnote says "total Rho deposits"; the yield-methodology policy says "total Rho deposits". The public `/product/treasury` table labels the bottom tier **"$50K–$2M"**; `/treasury-yield-comparison` labels the same tier **"$100K–$2M"**.)
*"Fees are calculated daily and charged monthly from your portfolio cash balance. If insufficient cash is available, Rho automatically sells a small amount of holdings."*

### The published yield table (verbatim, "Yields as of 09/11/2026 and change daily")
| Balance | Rho annual fee | Vanguard bond fund net (30-day SEC) | Morgan Stanley fund net (7-day SEC) | 13-week T-Bills net (7-day avg) |
|---|---|---|---|---|
| $20M+ | 0.15% | **4.66%** | 3.70% | 3.66% |
| $10–20M | 0.25% | 4.56% | 3.60% | 3.56% |
| $5–10M | 0.35% | 4.46% | 3.50% | 3.46% |
| $2–5M | 0.45% | 4.36% | 3.40% | 3.36% |
| $50K–$2M | 0.60% | 4.21% | 3.25% | 3.21% |

**The headline "up to 4.66%" is the top-left cell.** The footnote defining it (verbatim, appears in the footer of nearly every Rho page):
> "RBB Treasury LLC dba Rho Treasury… seeks to earn net returns up to 4.66% annually on your idle cash. Net yield numbers as of 09/11/2026, and assumes **total Rho deposits of $20M+**, a **100% allocation to the Vanguard Short-Term Investment-Grade Fund (VFSTX)**, and an annual fee which ranges from 0.15%… to 0.6%…"

**This assumed allocation is impossible under the product's own rules**, which cap Vanguard at 50% of the portfolio. See §17, item 2.

To Rho's credit, `/treasury-yield-comparison` says this out loud: *"the 'up to' number at the top of this page… assumes your entire balance sits in the Vanguard short-term investment-grade bond fund, an allocation we recommend only for cash you won't need for a year or more… Any provider quoting you one big number without telling you what allocation — and what liquidity trade — it implies is leaving out the part that matters."*

### Yield methodology (policy page dated **August 3, 2026**)
- T-Bills: *"the trailing 7-day average U.S. T-Bill yield (13-week), source: U.S. Department of the Treasury"*, with an in-page TODO: *"[Pending: Rho plans to quote the yield of its own most recent T-Bill purchases once a product-sourced feed is available; this section will be updated when that ships.]"*
- Money market funds (MULSX): **7-day SEC yield**. (Note: the methodology page calls MULSX a "money market fund"; the help center says it is not one.)
- Bond funds (VFSTX): **30-day SEC yield**.
- *"Where Rho quotes a single 'up to' figure, it is net of the lowest fee (0.15%, the $20M+ tier)."*
- *"If you see an undated yield anywhere on our site, tell us — that's a bug, not a policy."*
- Settlement promise: *"proceeds from Treasury sell orders are available in your Rho checking account within two (2) business days of trade execution (as of 08/03/2026)."*

### Protection
**SIPC up to $500,000 per customer, including up to $250,000 for cash claims.** *"SIPC protects against the failure of the broker dealer, not against market losses."* Explicitly **not FDIC-insured**.

### Tax / reporting [HC]
Apex issues 1099s where thresholds are met: **$10 for dividends and interest, $20 for cash in lieu, $600 for miscellaneous income**; *"C corporations are generally exempt from 1099 reporting under IRS broker reporting rules."* Tax docs emailed from **rho@tax-docs.com**. Statements posted within **7 business days** of month start; months without deposits/withdrawals/trades roll into a quarterly statement. T-Bill interest is *"subject to federal income tax but exempt from state and local income taxes."* On QSBS: *"Rho does not manage accounts for Qualified Small Business Stock (QSBS) eligibility or compliance."*

**ACAT out:** *"once an ACAT transfer is initiated, you will be unable to add or withdraw funds for **up to 90 days**."*
**Closing:** requires liquidating all holdings, *"typically takes 2-3 business days"*, at market prices.

Apex sender domains customers should expect [HC]: trade confirmations and statements from `notifications@investordelivery.com`, tax docs from `rho@tax-docs.com`, prospectuses from `prospectus_mbox@investordelivery.com`, proxy notices from `id@proxyvote.com`.

### Competitor table [Rho claim], "as of 2026-09-06"
| | Rho | Mercury | Brex | Ramp |
|---|---|---|---|---|
| Minimum to access yield | $50,000 | $250,000 across all Mercury accounts | No minimum deposit | $5,000 initial investment |
| Annual fee | 0.15%–0.60% monthly | 0.15%–0.60% tiered | None | "Up to 0.15% advisory fee" |
| Investor protection | SIPC $500K incl. $250K cash | SIPC $500K total | "SIPC-protected, AAA-rated fund, no coverage cap published" | SIPC $500K incl. $250K cash |
| Liquidity | 2–3 business days | Same-day to 1–2 business days | Same-hour to daily | Same-day to ~2 business days |
| Published rate | "updates daily" | "stamped 08/28/2026 on Mercury's own page" | "checked 2026-09-06" | "**Renders as a placeholder on ramp.com, no fixed rate published** (checked 2026-09-06)" |

From `/treasury-yield-comparison` (more granular, "verified 08/02/2026"): Mercury Treasury **3.01%–3.81% net by deposit tier**, top tier requires **$20M–$50M**, funds JTCXX + MCRYX; Brex **4.01%–4.36%** (fund 7-day yield plus a Brex balance bonus, rates effective 07/31/2026), fund DGVXX (BNY Dreyfus government MMF), top tier requires $20M+, plus a separate Brex Vault FDIC sweep up to $6M.
FDIC-APY comparison set on the same page: **SVB Startup Money Market** "does not publish current rates online; its last public sheet (dated 12/10/2025) showed 0.10% ≤$50K · 2.38% to $1M · 3.30% >$1M"; **Bluevine** 1.3%/1.75%/3.0%; **Grasshopper** 1.55% <$25K, 3.00% $25K+; **Relay** 1.11%/1.75%/3.00% gated by $0/$30/$90-per-month plans; **Axos** up to 1.01% on ≤$50K.
Unusually candid concession section titled **"Where the others win"**: *"Mercury publishes its full net-yield tier schedule with unusual clarity — the transparency standard this page copies — and its JTCXX option redeems same-day, faster than a T-Bill sale settles at Rho… if your board mandates FDIC coverage on every yielding dollar, those beat any securities product, Rho's included. And below Rho Treasury's $50,000 minimum, **Rho doesn't have a yield product to sell you**"*. This contradicts Business Savings at a $25,000 threshold.

---

## 6. Corporate Cards: `/product/corporate-cards`

### What it literally is
A **charge card** (not revolving credit) issued to the business by Webster Bank on the **Mastercard World Elite Business** network. *"the full statement balance is paid on time each period, rather than carried at an interest rate."*

### Three card form factors
**Physical**, **virtual**, and **vendor cards**. *"Each carrying the same underwriting and terms: no personal guarantee and no personal credit check."* Unlimited cards, no per-card fee.

### The two repayment programs
| | **Daily Terms** (default) | **Monthly Terms** |
|---|---|---|
| Repayment | *"Payments are automatically debited from your Rho checking account **just after midnight EST** for that day's activity… for the total amount of settled charges from the prior day"* [HC] | *"A **30-day billing cycle with a 1-day repayment period**", automatic repayment at cycle end from Rho Checking **or an external account** [HC] |
| Spending capacity | *"your company receives a **daily credit limit**… determined based on a combination of your **available checking balance** as well as risk factors that vary by client… this limit is not a static limit over time"* | Underwritten credit limit: *"personalized based on the business's financial health"* |
| Standard cashback | **1.25%** | **1%** |
| Platinum cashback | **up to 2%** | **up to 1.75%** |
| Qualification | Every account starts here | **$25,000 held at Rho**, or **$75,000 combined across Rho and linked external accounts** (personal accounts don't count), subject to underwriting. [HC] phrases it as *"maintain a minimum cash balance of $25,000"* |
| Cashback payout timing | *"typically on the **6th business day of the month**, for the previous month's spend"* | *"typically **6 business days after you pay your statement balance in full**"* |

*"You can only be on one program at a time."* Apply for Monthly Terms in-platform: Cards tab → Credit Information tab → start application. *"Rho may request **read-only access to the business's primary bank accounts**."*

### Credit reporting
> "Rho does not pull any personal credit reports and does not report business card activity to personal credit reports. **We report to the credit bureaus on the entity (business) side at our discretion.**" [HC]

### Eligibility
US-incorporated with an EIN. **No personal guarantee, no personal credit check, no consumer credit report pull.** *"approval is based on the business, not the founder's personal credit."* Underwriting reviews business financials; documents requested include bank and accounting statements for all active business accounts [HC].

### Cashback rules (the dense part)
- **Cap: $1,000,000 in eligible spend per calendar year, across all tiers.** The cap applies to **eligible spend**, not to the dollar amount of cashback. *"Spending more than $1M a year? Talk to sales and we'll build your program."*
- **Redemption deadline: "you must redeem Cashback Rewards within twelve months of being earned, or they will be forfeited. Rho will not provide notifications regarding the impending expiration of your Cashback Rewards."**
- **Payment condition: "You may only receive Cashback Rewards when you pay the full amount due on your billing statement on time… If you do not pay the full amount due on time, you will not receive any Cashback Rewards for the billing period."** Also: *"You will not receive Cashback Rewards if you deposit funds in your Rho Account without making an actual payment to Rho."*
- **Excluded categories (verbatim):** "(1) Walmart Inc. and its affiliates and subsidiaries; (2) utilities merchants, per Mastercard Merchant Category Codes (MCCs); (3) money transfer, digital payment, and quasi-cash merchants, per Mastercard MCCs; and (4) transactions made or authorized outside the U.S."
- **Excluded transaction types (Rewards Terms):** "fees, fines, or interest charges paid to Rho, cash advances, balance transfers, cash equivalents, gift cards, prepaid cards or reloadable prepaid cards, purchases made with Cashback Rewards, person-to-person payments or transfers, prohibited or restricted transactions such as online sports betting and internet gambling transactions, and loan payments or account funding made with the Card."
- **Ownership:** *"the Cashback Rewards you may earn and accumulate **are not your property and do not belong to you until the Cashback Rewards are redeemed and issued to you** in the form of a statement credit."* Non-transferable, non-sellable, not assignable in bankruptcy.
- **Clawback on returns:** *"the difference in credit you receive will cause a deduction of the Cashback Rewards… The deduction will apply as a debit to your billing statement and will be an amount owed and due to Rho."*
- **Errors/disputes window: 60 days** from statement issue.
- **Program change notice: at least 45 days' notice; 90 days from notice to redeem** under current terms; unredeemed rewards forfeited if Rho cancels the program.
- Cashback lands in a dedicated **Rho Rewards checking account** (visible as `account_type: "rewards"` in the API); redemption transfers to Primary Checking are **instant**; only Account Owners, Administrators, or custom roles with "Redeem Rewards" permission can redeem. *"Rewards are earned only on settled transactions."*
- **Tax [HC]: "Cashback from Rho is not considered taxable and we do not issue 1099s for cash back."**
- **Mastercard Easy Savings:** *"Rho customers also earn additional Cashback at participating merchants through Mastercard Easy Savings"* (as part of the World Elite Business program).
- **Late fee:** *"A late fee of **3% of the delinquent payment balance per month** may apply for **up to six months**, unless prohibited by law. **Late payment forfeits rewards.**"*

### Rho Platinum: the four conditions (verbatim, [HC] and Rewards Terms agree)
> 1. "Your payroll is run from Rho"
> 2. "Your business revenue is deposited via Rho Checking"
> 3. "**50% or more** of your company's assets are held at Rho"
> 4. "You have an open Rho Corporate Card"

*"It isn't a paid plan, there's no subscription fee."* *"Platinum status reflects your current setup. If your account no longer meets the qualifications, your Cashback rate returns to the standard rate."* This is the load-bearing commercial mechanism of the whole platform: the top cashback rate is the price Rho pays to become the system of record for payroll, revenue, and the majority of company assets.

### Card controls [HC]
- Limit types: **No Limit, Recurring (daily / weekly / monthly / quarterly / annual), Fixed, Single-use.** Monthly limits reset on the 1st. Fixed-limit cards **auto-lock** once transactions fully settle. Single-use limits **cannot be changed after creation**.
- **Merchant-specific controls: up to 20 distinct merchants** allowlisted per card.
- **Merchant category controls** by Mastercard MCC.
- **International spend is ON by default** on all Rho cards; toggleable.
- **Card usage date windows**; *"By default, all Rho cards expire **3 years from issue date**."*
- Per-card billing address override (default is the org billing address).
- Company-wide merchant restrictions available.
- **Monthly user limits are a legacy feature "no longer part of Rho's standard offering."**
- Hard constraint on both programs: *"Changing a user or card limit does not increase your available balance"* (Daily) / *"does not increase your total available credit"* (Monthly).
- Cards can be added to **Apple Wallet and Google Wallet**; **WeChat is not supported.**
- Statements: monthly card statements issued **on the 5th of each month**.

### Fees
**$0 annual fee, $0 subscription fee, $0 per-card fee.**

### Competitor table [Rho claim], "Brex, Ramp, and Mercury as of 2026-09-08"
| | Rho | Brex | Ramp | Mercury |
|---|---|---|---|---|
| Cashback | "Real cash, not points, no category restrictions": up to 2% Platinum, 1.25% standard | "Category multipliers, not cash back: 7x rideshare, 4x Brex travel, 3x restaurants, 2x software, 1x everything else" | "No published cashback rate; a footnoted '5% savings' figure is an illustrative spend-savings estimate, not a cashback rate" | "1.5% cashback on card spend, flat, no higher tier" |
| Repayment terms | Daily or Monthly, your choice | "Daily payments require over $500K in annual revenue, or a funded-startup path" | "Not published on ramp.com as of this writing" | "start on daily repayment; can switch to 30-day terms once balances reach $15,000" |
| Personal guarantee | Not required | Not required | Not required | Not required |
| Annual/card fees | $0 | "$0/user/month Essentials plan… accepted in 210+ countries" | "No annual or per-card fee stated" | "$0 annual fee on IO cards" |

Note the marketing claim **"no category restrictions"** sits on the same page as a footnote excluding Walmart, utilities, money transfer/quasi-cash, and all non-US transactions.

---

## 7. Vendor Cards: `/product/vendor-cards`

### What it literally is
Not a separate financial product: a **card type within the Rho Corporate Card program**, scoped to one vendor, with its own **"Vendor Cards" tab under Cards**. The page is a lead-gen page (email capture, no pricing section, no FAQ block, no footnotes beyond the standard disclaimer).

### Mechanics
1. *"Generate a dedicated card for any vendor in seconds, with **logo and name already matched**."*
2. *"Send card info directly to vendors without extra steps"*, i.e. one-click share. [HC] the secure link to card details **expires in 72 hours**.
3. *"Apply limits and merchant rules to each vendor."*
4. *"See and report spend by vendor from day one, without relabeling later."*
5. **"Subscription Switch"** integration: *"Replace payment details during checkout and migrate subscriptions in minutes."* On the confirmation page there is a **"Switch subscription"** action; *"Rho will automatically match it to a subscription carrying the same name as the Vendor card."*
6. *"Cards default to the creator as cardholder, so they stay working even when team members churn."*

Creation paths [HC]: Cards tab → Create Card → Vendor Card; or Vendors → Add Vendor → Payment Account dropdown → **Single-use vendor card** (that path can *only* create single-use); or **bulk via CSV upload**, which auto-creates missing vendors. **International spend is ON by default.**

### The single-use AP card variant [HC]
Used as a Bill Pay payment method. Card is nicknamed **"[Payee Name] AP Card: [Invoice Number]"**. *"Single-use Cards can be charged one time and are pre-set with the payment amount and a **14-day card usage window**. You can edit the 14-day card usage window in Card Settings. Once the card is successfully charged, it becomes invalid."* After use, status flips **Active → Canceled** but details remain viewable in Team Cards.

### Limits / caveats
- *"Included with every Rho account… **Unlimited vendor cards** with instant setup."*
- **Web-only:** *"Vendor cards are currently a web-only feature, so they won't appear in the mobile app"* [HC]. But the changelog says vendor-card management arrived on mobile in **May 2026** and **March 2026**. Stale help article or stale changelog.
- **Lifecycle gotcha contradicting the "stay working when team members churn" claim:** *"If the user who created a Vendor Card is removed, you will be prompted to delete the card. Similarly, if a Vendor profile is deleted, **all linked Vendor Cards will be canceled**."* [HC]

### Fees
None stated; included with a Rho account. No footnotes on the page beyond the standard bank disclaimer.

---

## 8. Expense Management: `/product/expense-management`

### What it literally is
Software bundled into the card program: *"Rho's expense management combines corporate cards, spend controls, and automated reconciliation in one platform, with no per-user or platform fees."* Two-step "how it works": (01) issue cards instantly with limits set before the first swipe; (02) reconcile in your books.

### Mechanics
**Pre-spend controls:** limits by card, user, budget; **per-transaction, daily, or monthly** spend limits set before a card is issued; off-policy spend *"gets flagged the moment the card is used — not when you're closing the books."*

**Approval workflows:** *"the setup of **direct manager approvals**, allowing automatic routing of employee expenses up the direct manager approval chain. This can be combined with **dollar amount tiers** to create multi-level approval flows."* Rules can require *"submissions of receipts, notes, or attendees for defined transactions."* Company policy documents can be uploaded; suggested rules exist.

**Receipt capture: the Gmail Connector** (shipped **April 30, 2026**):
- Scans the connected Gmail/Google Workspace inbox for receipts matching keyword and merchant-sender criteria, and auto-attaches them to the matching card transaction.
- *"You set the keywords before connecting, can edit them anytime, and can disconnect instantly."*
- **"The Gmail Connector captures receipts from the point of connection forward."** No backfill. Older receipts must be uploaded or bulk-forwarded manually.
- Each team member connects their own inbox; receipts route only to that cardholder's transactions.
- Replaces auto-forwarding rules: *"Auto-forwarding breaks when card setups or email configurations change — the connector doesn't."*
- Requires *"Permission from your Gmail admin if your organization restricts third-party app access."*
- Other upload paths retained: desktop, email forward, SMS, mobile app photo/file.
- Receipt matching was rebuilt April 2026 with *"merchant identity verification… so a receipt from Uber only ever attaches to an Uber transaction"*, plus confidence scoring and date-proximity logic.
- *"When are more connectors coming? In the pipeline. We will share timing when it is confirmed."*

**Reimbursements (out-of-pocket):**
- Enabled by an Admin/Account Owner under Settings → Expense settings → Reimbursements.
- **Paid directly from the Rho checking account** after direct-manager approval.
- **Mileage:** Rho pre-populates the **current year's IRS rate of $0.70/mile**; admins can override with a company rate. An embedded map auto-calculates distance between stops. *"Your mileage reimbursement will be calculated using the rate your business set **when the expense occurred**."*
- **Hard limit: "Can reimbursements be issued to non-US bank accounts? No, that is not something we support right now."** [Marketing FAQ] / *"Rho processes reimbursements via **ACH for domestic bank accounts only**"* [HC].

**Accounting sync:** native direct integrations with **QuickBooks Online, NetSuite, Sage Intacct, Puzzle**; **Xero via bank feed** (*"Xero connects today through a bank feed rather than a native sync"*). For systems without a direct integration: *"extensive CSV reports and bulk receipt file export."* Note the Marketing FAQ inconsistently lists Xero as a direct accounting integration in one answer (*"QuickBooks Online, NetSuite, Sage Intacct, **Xero**, or Puzzle"*) and excludes it in another.

### Eligibility / minimums
An open Rho account. *"Opening a Rho account requires an EIN, or an SS-4 while your EIN application is in progress… your EIN itself is issued separately by the IRS, **typically within 2 to 4 weeks**."*

### Fees
**$0 per user, $0 per platform, on every plan.** *"Rho's expense management platform is free, with no user or platform usage fees."*

### Caveats / footnotes (verbatim)
> "Cashback is up to 2% with Rho Platinum (terms apply), on card spend, on up to $1,000,000 in eligible annual card spend; 1.25% is standard. Cashback rewards are governed by the Rewards Terms and are **forfeited if not redeemed within 12 months of earning**."

> "Cards are issued pursuant to a license from Mastercard, and the card tier is Mastercard World Elite Business."

> "Competitive data collected from Ramp, Brex, and Mercury websites as of 2026-09-08."

Gmail privacy claim: *"Receipts, and only receipts. The connector scans subject lines and attachments that look like purchase confirmations — nothing else is read, stored, or touched."* / *"No inbox data is retained after disconnection."*

---

## 9. Bill Pay: `/product/bill-pay`

### What it literally is
AP automation bundled into the checking account. *"Rho Bill Pay is not sold as standalone software. It ships with a Rho business banking account."* *"Bill Pay activates once your Rho business banking account is open."* Explicit scope limit: *"it does not include procurement or supply-chain management."*

### Mechanics (four steps as marketed)
1. **Forward the invoice** to a dedicated Rho Bill Pay inbox. *"no login required."*
2. **OCR drafts the bill** for review. Confidence score shown as **Green / Yellow / Red** on the bills table; duplicates auto-flagged. Known caveat [HC]: *"If a user replies in a thread to the original email sent to the Bill Pay inbox and image files invoices are in the email body, duplicate invoices can be created."*
3. **Route for approval.** Custom approval settings; approvals reviewable in the **Rho mobile app**.
4. **Pay and sync.** The marketing page's step 4 reads, verbatim and in full: *"Once approved, **pay by check**."*

### Payment methods: the marketing page and the help center flatly disagree
**[Marketing]** names only checks: *"pays vendors by check"*, *"Rho Bill Pay supports check payments"*, *"$0 on domestic check payments"*, *"Check payments at no per-payment fee"*, *"When a vendor needs a paper check, Rho prints and mails it on your behalf; you never order checkbooks or write checks yourself."* The comparison table's "Domestic per-payment fees" row for Rho reads **"$0 on checks"**.
**[HC, `paying-bills-with-vendor-cards-single-use`]**: *"You can make Bill Pay payments using the following methods: **ACH transfers; Wire transfers (domestic and international); Checks; Single-use cards**."*
The **homepage nav** meanwhile says: *"Bill Pay. **Hundreds of vendors, zero fees**."*

### Scheduling mechanics [HC]
- Payments must be scheduled for a **future business day**. *"Payments scheduled for the same day or a weekend will not be released and may appear as overdue."*
- **Scheduled payments are released at approximately 4:00 a.m. ET on the payment date.**
- Approvals must clear before that release time.
- Payments can be **revoked** before release (Bills → filter Payment Scheduled → three dots → Revoke).
- Bulk payment dates can be updated for **checks, ACH, wires, and single-use virtual cards**.

### Bulk payments [HC]
CSV import into a Rho template; one line item = one payment, **no merging**. Supported: **Checks, ACH, Wires (domestic accounts only), Single-use virtual Rho cards** shared via email. Vendors must exist in Rho first. **Bookkeepers can draft but by default cannot execute payments.** Errors surfaced as "Vendor Missing" (yellow) and "Destination Error."

### International bills [HC]
- **Bill Pay supports international wires in USD only.** Non-USD payments must be sent from the Banking tab and then the bill marked **"Paid Externally"** in Bill Pay.
- **Bulk payments support domestic wires only.**
- *"Rho charges **no fee on international wires sent in USD** (as of **08/02/2026**)."* Recipient/correspondent/intermediary/SWIFT fees may apply; the **"Cover all recipient delivery fees" toggle is a flat $15 (as of 08/02/2026)**; **currency conversion carries a 1% FX rate (as of 08/02/2026)**.
- *"Certain currencies — **IDR, PHP, INR, and MYR** — are processed on local payment rails rather than SWIFT, so tracking is limited once funds leave Rho."*

### Fees
**$0/month, no per-user fee, no per-payment fee on checks.** *"No monthly, per-user, or minimum-balance fee across Rho banking, cards, expense management, and Bill Pay."*

### Caveats / footnotes (verbatim)
> "¹ Published application-time claim for new Rho business banking applications; individual application times vary."

> "Is my money safe with Rho Bill Pay? Bill Pay runs on your Rho checking account. Funds are FDIC insured up to $250,000 **per entity, not per account**…"

> "Can AI do accounts payable? …Rho Bill Pay uses automated invoice capture (optical character recognition) to turn a forwarded invoice into a draft bill for your team to review, **not an AI system that approves payments on its own**."

### Competitor table [Rho claim], "BILL, Ramp, and Relay as of 2026-09-08"
| | Rho | BILL | Ramp | Relay |
|---|---|---|---|---|
| Software cost | Included with Rho Banking | **$49 to $89 per user per month**; Enterprise custom | Free plan; **Ramp Plus $15/user/month** | **Plans from $0 to $120 per month** |
| Domestic per-payment fees | $0 on checks | **ACH $0.59; mailed check $1.99** | "'No software or transaction fees' on its free plan, per Ramp" | "'Additional transaction fees apply,' per Relay's pricing page" |
| Accounting sync | Included | "Tiered: CSV import/export on entry tier; two-way QuickBooks and Xero sync on Team and up" | "Syncs with 10 ERPs including NetSuite, Sage Intacct, and QuickBooks" | "QuickBooks Online and Xero" |
Rho's own FAQ generalization: *"Dedicated AP software commonly charges **$15 to $89 per user per month**."*

---

## 10. Invoicing: `/product/invoicing`

### What it literally is
AR/invoicing built into the checking account. Free to Rho customers. Launched **Beta March 25, 2026**; payment portal + recurring invoices **June 30, 2026**; card acceptance and QuickBooks sync **August 31, 2026**.

### Mechanics
1. Create: add customer (existing or new-by-typing), invoice date, due date, **payment terms (e.g. Net 30 or Due on receipt)**, line items (name, quantity, rate), subtotal/taxes/discounts auto-calculated. A personal note can be added to the recipient email. Operating address can be displayed instead of the registered legal address (Aug 2026).
2. Send by email from Rho. Each invoice carries a **branded payment portal** (logo, colors).
3. Get paid: *"Your customer pays by **ACH, domestic wire, international wire, or check** through a secure payment portal. **No Rho account needed on their end.**"* The key-features block widens this to *"credit card, debit card, Google Pay, ACH, domestic wire, or check."*
4. Reconcile: *"When the payment lands in your Rho account, it matches to the right invoice on its own."* Auto-mark-as-paid shipped April 2026.
Optional: *"Activate a **virtual account number** to minimize risk from unauthorized debits"* (changelog, March 2026).
**Recurring:** *"You can automate repeat billing by enabling **Schedule this invoice to repeat**"* [HC]; cadences **weekly, monthly, quarterly, or annual** (changelog June 2026).

### Card acceptance (the part with real fees) [HC]
- Processed through **Stripe**. An Account Owner or Admin connects; **"you can't connect an existing Stripe account. Rho creates and manages a separate account for your business"**. Payout details and portal settings cannot be changed in Stripe directly.
- Stripe verification statuses: **Pending / Action required / Connected / Failed**. *"Approval decisions are made by Stripe."*
- **Fee: 2.9% + $0.30 per transaction, paid by your business.** *"Your customer pays only the invoice amount."* **"Can the fee be passed to the payer? No, surcharging is not currently available."**
- **Daily card payment limit: $10,000 per day across all invoices.** Once hit, the card option disappears from further invoices until reset; bank transfer and international wire still work.
- **Card payments are available for one-time, full-amount USD invoices only.** Partial payments, overpayments, recurring invoices, and non-USD invoices must be paid by bank transfer or international wire.
- *"For your first card payment, deposits may take **up to two weeks** while Stripe completes its initial review process."*
- Invoice status flow on card payment: **Pending payout → Paid**.
- *"Card information is collected and stored securely by Stripe and is **never stored by Rho**."*

### API-visible enums [API sandbox]
Invoice `status`: `unpaid`, `pending_payout`, `confirm_payment`, `paid`, `overdue`, `cancelled`. Payment `external_method`: `cash`, `check`, `credit_card`, `other`, `received_in_account`. `accounting_sync_status`: `not_pushed`, `synced`, `error`, `skip`, `object_changed`. Amounts are **integer minor units** (`124500` = $1,245.00).

### Fees
**$0 per invoice, $0 per month.** *"$0 on domestic ACH, wire, and check payments into Rho."* The 2.9% + $0.30 card fee is **not mentioned on the product page at all**.

### Caveats / footnotes (verbatim)
> "¹ Rho Invoicing carries no per-invoice fee and no monthly fee for Rho customers, included with your Rho account. Domestic ACH, wire, and check payments into Rho Checking are also $0."

> "**Rho does not guarantee that any payment will be initiated, authorized, completed, or settled, or that any payment will be automatically matched to a particular invoice.**"

> "Finally, be honest about what is not included. **Rho Invoicing does not yet sync with accounting software like QuickBooks or Xero, and there is no mobile app.**" This is contradicted by the 08/31/2026 changelog ("Rho invoices now sync to QuickBooks… as accounts receivable invoices, not generic bank deposits") and by the help article "Syncing invoices to your accounting software."

### Competitor table [Rho claim], "Stripe, Mercury, QuickBooks as of 2026-09-08"
| | Rho | Stripe | Mercury | QuickBooks |
|---|---|---|---|---|
| Invoicing cost | Included | **0.4% per paid invoice (Starter); 0.5% (Plus)** | Unlimited invoices free on every tier; recurring requires Plus ($29.90/mo annual) | Free plan capped at **2 invoices/month**; unlimited from $20/mo (Lite) |
| ACH / bank transfer fee | $0 domestic ACH, wires, checks | **0.8% ACH Direct Debit, $5.00 cap** (plus per-invoice fee) | $1/txn on Plus, $0 on Pro, unavailable on free tier | **1% per ACH bank payment** |
| Recurring invoices | **"Not shown"** | Stripe Billing 0.7% of billing volume | Plus and Pro only | From Simple Start ($38/mo) |
| Payment matching | **"Not shown"** | Automatic reconciliation, Smart Retries | Auto-imports to QuickBooks/NetSuite/Xero | Books update automatically |

The two **"Not shown"** cells are notable: Rho leaves its own row blank for the exact two features the body copy of the same page claims it has.

---

## 11. Capital: `/product/capital`

### What it literally is
A **revolving working-capital line of credit**, marketed as living "inside your Rho account." Explicitly framed against alternatives: *"Rho Capital is a revolving credit line against your business cash flow, **not a term loan or a venture debt facility**"* and *"not a merchant cash advance: no daily withdrawals and no cut of your revenue."*

### Who actually lends
**[Legal footer]** *"Rho is a fintech, not a bank. **Financing offered by third parties.** Rho Capital is not a broker-dealer. It does not participate in the negotiation or execution of any transactions between customers and third-party financing sources. **Rho does not guarantee that the connection services will result in financing.**"*
**[Legal footer, page bottom]** *"**Slope** is a financial technology company, not a bank. **Business-purpose loans made by Lead Bank** and subject to credit approval. Application and consent to obtain personal credit report is required. Subject to minimum revenue and business requirements. Personal Guaranty may be required. Fees vary based on risk assessment and loan term."*
**[Marketing body]** *"Fees vary based on risk assessment and loan term, and are set when **Slope** underwrites your line."*
**[Marketing FAQ]** *"Is Rho a direct lender for its working capital line of credit? **Yes.**"* See §17, item 1.

### Mechanics
1. Apply from the Rho account with EIN, formation documents, ownership information, **plus "a look at recent cash flow."**
2. Underwriting: *"We look at the shape of the business today rather than checking it against a fixed, one-size checklist."* [HC] *"Rho evaluates your real business transaction data — built for businesses with lumpy revenue or a thin credit file that traditional credit scoring under-serves."*
3. Approval: no separate login; the line sits alongside the existing Rho account.
4. Draw, repay, redraw. *"Repaying restores your available credit."*

### Limits / terms
| Attribute | Value |
|---|---|
| Facility size | **Up to $5M**, "sized to your business"; "Larger facilities considered case by case"; [HC] says "up to **$5M+**, subject to underwriting" |
| Funding speed | **"24-48 hrs typical time for funds to land in your Rho account after approval"**; [HC] "typically land… within about 48 hours of application" |
| Repayment window | **Up to 180 days per draw** |
| Prepayment penalty | **$0** |
| Origination fee | [HC] **"no origination fees"** |
| Pricing | **"Fees vary, confirmed before you accept a line."** No rate, APR, or fee range is published anywhere in the corpus. |
| Personal credit | [HC] *"Applying doesn't involve a **hard pull** on your personal credit"*; [Legal] *"Application and **consent to obtain personal credit report** is required"* |
| Personal guaranty | *"A personal guaranty **may be required**, depending on underwriting"* |

### Eligibility
No published revenue floor or age-in-business floor. *"Rho doesn't publish a fixed revenue or age threshold; each application is sized by underwriting."* *"Startups that only have an EIN and no trading history yet are a common case, not an edge case."* But the Slope/Lead Bank disclaimer says *"Subject to **minimum revenue** and business requirements"*. That is an unpublished floor that does exist.

### Stated uses [HC]
*"inventory purchases, supplier payments, payroll bridges, or marketing spend."*

### Caveats / footnotes (verbatim)
> "¹ Larger facilities considered case by case."

> "Funds land in your Rho account in as little as 24-48 hours after approval; **actual timing depends on underwriting review and document completeness**."

Positioning on the homepage nav: *"Capital NEW. Funds land in your Rho account."* Homepage product tile: *"Access capital. Working capital for brands. **No dilution.**"*

---

## 12. Rho Close: `/product/close`

### What it literally is
An **AI/ML transaction-coding assistant** inside the accounting view. Launched **May 27, 2026** ("Introducing Rho Close: Intelligent Transaction Coding for Startups", published May 06 2026, updated September 01 2026). It is a **suggestion engine, not an autopilot**.

### Mechanics
- Learns from *"your chart of accounts, your vendor history, and every coding decision you've made on Rho… **not a generic model trained on someone else's books.**"*
- Trigger: **Accounting Dashboard → "Suggest coding"** above the transaction table. *"Rho Close will generate suggestions for **empty** accounting attributes across the card and banking transactions in your current view."*
- Scope [HC]: **card and banking transactions**. *"It does **not** currently create or modify mapping rules. And it does **not** deliver suggestions for accounting attributes where an accounting attribute has already been selected."*
- Accept/dismiss at three levels: **bulk** (all in view), **per transaction row**, **per attribute** (hover the cell, click the checkmark, or override via dropdown).
- Default-on behavior worth noting: *"If you do attempt to sync your transactions in bulk without accepting or dismissing the suggestions, you can decide whether to accept the suggestions or not as part of the sync"*, and *"If you do sync an individual transaction without actively accepting or dismissing the suggestions, **those suggestions will be applied to the sync**."* The marketing claim *"Nothing syncs until you approve it. Every time."* is therefore about the sync action, not about each suggestion.
- Enabled at Accounting → Settings → General; **toggled on by default.**
- Learning loop: *"Every time you accept or override a suggestion, Rho learns from that decision."*

### Eligibility
**"Rho Close requires a native accounting integration. If you're currently exporting CSVs, you'll need to connect a supported integration."**
Supported set, marketing FAQ: *"QuickBooks Online, Oracle NetSuite, and Sage Intacct via native direct integration. **Xero is also supported via bank feed**, with coding handled on the Xero side."*
Supported set, [HC]: *"businesses with a direct accounting integration (**QuickBooks, NetSuite, Puzzle, or Sage Intacct**)."* **Puzzle appears in one list, Xero in the other; neither list matches.**

### Access
*"Anyone with access to the accounting view on Rho… the founder, a first finance hire, or an outsourced accountant… **Permissions follow your existing Rho account settings.**"*

### Fees
*"Rho Close is included with your Rho account."*

### Caveats
No footnotes, no numbers, no accuracy claim, no benchmark. The only quantified claim is soft: *"Close goes from a few hours to a few minutes, and gets faster every month."* No disclaimer about AI error rates anywhere on the page.

---

## 13. Incorporation: `/product/incorporation`

### What it literally is
**Delaware C-corp formation only**, filed by Rho, attorney-reviewed, with the Rho bank account application opening in the same flow. Launched **August 31, 2026**.

### Mechanics
1. **Questionnaire:** company name, share structure, founder details. [HC] *"Most founders finish the flow in about 5 minutes."*
2. **Rho files the certificate of incorporation with Delaware.**
3. **Attorney review:** *"A licensed attorney reviews and signs off on your certificate of incorporation and other Rho Incorporation formation documents."*
4. **Rho account application + SS-4 (EIN application) prepared and submitted for you.** *"Funds move once the IRS issues your EIN."*
Order of operations [HC]: *"Rho files your Delaware certificate **first**, then submits your EIN application."*

### Timing (carefully hedged)
> "² **Filing time measures Delaware state filing only**, starting the next business day after you submit your information; **it does not measure EIN issuance or account approval**. **About 80% of filings complete within 24 hours**; Delaware processing backlogs can extend this window."

EIN issuance is on IRS time: *"typically within 2 to 4 weeks"* per the expense-management FAQ. Pre-EIN banking window: **30 days non-VC-backed, 60 days VC-backed**, both manual review, neither guaranteed. *"International founders without a U.S. SSN or TIN are supported too — expect a longer EIN timeline from the IRS."*

### Price and the credit-back
- **$400 flat fee**, which **includes state filing fees** and **year-1 registered agent service**.
- Credited back on a qualifying deposit. **Marketing/product threshold: deposit $10,000 of new money and keep daily average balance ≥$10,000 above the pre-deposit balance for 60 days after incorporation.**
- **[HC] adds an undisclosed-on-marketing variant: "($1,000 for founders introduced through an accelerator)."**
- Post-year-1 costs (stated only in the "How the fee works" box): *"platform access after year one is **$1,000 annually** and contract services run **$100 or $250 per contract**. **Delaware franchise taxes apply separately and on an ongoing basis.**"* This $1,000/year platform fee is a striking exception to Rho's "$0 fees" positioning and appears nowhere else in the corpus.

### Full offer terms (verbatim, from the incorporation page footer)
> "*Terms and Conditions: To qualify… you must: (1) incorporate your business through Rho's incorporation service ('Rho Incorporation') on the Rho platform and (2) deposit at least ten thousand dollars ($10,000.00) into your Rho checking account and maintain a daily average balance that is at least ten thousand dollars ($10,000.00) greater than the account balance immediately prior to that qualifying deposit for sixty (60) days after the incorporation. **You may earn more than one reward.** Where you pursue more than one reward concurrently, each additional reward requires an additional qualifying deposit of at least ten thousand dollars ($10,000.00), and the daily average balance requirement shall be increased by ten thousand dollars ($10,000.00) for each such additional reward… **Substituting or reallocating pre-existing funds will not satisfy this account balance requirement.**"

> "The offer reward consists of a reimbursement of the $400.00 fee… which will be **credited to your Rho checking account within thirty (30) days following the first sixty (60) days** of the opening of your Rho checking account if we determine that you have met these offer requirements."

> "The Rho checking account must remain **open and in good standing** throughout the 60-day period… This offer may be changed or discontinued at any time without notice. This offer is available to **both new and existing Rho customers**… **Void where prohibited.** You are solely responsible for any federal, state, or local tax payments… Rho reserves the right to **rescind or demand repayment** of any of the offer bonuses, including reclaiming the reimbursed incorporation fee, if it determines, in its sole discretion, that the customer has engaged in fraudulent, deceptive, or suspicious activity."

> "**Rho Incorporation is not a law firm or accounting firm and does not provide legal, tax, or accounting advice. Rho is not responsible or liable for any errors, omissions, or mistakes made by Rho Incorporation or in any materials, filings, or documents prepared or provided through the service. You are solely responsible for reviewing all such materials…**"

### Eligibility
- **At least one owner or officer must be US-based**, with a **physical US operating address**.
- *"founders in certain restricted countries or excluded industries aren't eligible."*
- **Delaware C-corps only.** *"Does Rho support LLC formation? **Not yet.** Rho Incorporation is C-corp only today; LLC formation is coming soon."* (The nav has said "LLC coming soon" since at least the corpus snapshot.)

### Competitor table [Rho claim], "Stripe Atlas, Clerky, LegalZoom as of 2026-09-07"
| | Rho | Stripe Atlas | Clerky | LegalZoom |
|---|---|---|---|---|
| Upfront price | **$400**, credited back | **$500** one-time, includes state filing fees + yr-1 agent | **$427 to $819** one-time, includes DE filing fees + yr-1 agent | **Starts at $149 plus filing fees, billed separately** |
| Filing speed | ~24 hours; 80% within window | Within two business days | 2 to 3 business days | 1–2 days on its **$349** fastest tier; 7–10 days standard |
| Registered agent | Year 1 covered | Year one; **$100 annually after** | Year one; renewal price not published | **$249 per year, auto-renews** |
| EIN handling | SS-4 prepared and submitted | "Gets your company tax ID" | Completes IRS forms and submits | Not published |
| Account at formation | Rho account app in same flow, subject to approval | **Opens a Stripe Treasury account the moment you incorporate** | Pre-filled applications to outside banks, no EIN needed; opens no account of its own | Not published |

---

## 14. Rho for Slack: `/product/slack`

### What it literally is
A **read-only Slack app** for balance/transaction/statement visibility and alerts. *"Included at no extra cost for Rho customers."*

### Mechanics
Two-layer auth [HC]: (a) **the workspace connection**, where a Rho Admin links one Slack workspace to one Rho business, once; and (b) **"Sign in with Rho"**, where each person ties their own Slack identity to their own Rho account via a personal link.
Setup: a Slack workspace admin installs the app from the Integrations page in the Rho dashboard; a Rho Owner/Admin authorizes; *"If those are two different people, the app generates a hand-off link."*

**Slash commands [HC]:**
| Command | Function |
|---|---|
| `/rho-accounts` | Balances across accounts |
| `/rho-transactions` | Recent transactions plus a link into Rho |
| `/rho-help` | Capability list tailored to your setup |
| `/rho-feedback` | Bug report / request to the Rho team |
| `/rho signin`, `/rho-signout` | Personal sign-in management |
*"Command replies are visible only to you, even in a channel."*

**Home tab:** available balance, accounts, alert settings, connection status, signed-in identity, Refresh, Open in Rho.

**Alerts:** daily balance pulse (*"Cash balances, yield earned, and a heads-up before payroll leaves, posted on the schedule you set"*), real-time inflow/outflow/card activity, with a configurable **dollar threshold**, delivered to a **single** configured private channel and/or DMs. *"Rho won't post alerts to multiple channels, and nothing is sent until you turn alerts on."*

**Agent chat (beta, select businesses only) [HC]:** DM the app, `@Rho` mention in a private channel, or `/rho <question>`. *"The agent answers using your live Rho data: balances, transactions, statements, and spend by vendor, category, or person. Every answer names its sources and includes a reminder that your Rho dashboard stays the source of truth. **It is read-only, so it can look things up but never move money.**"* Questions asked in a channel are answered **by DM**. **Statement download links work for about 15 minutes.** If you ask before signing in, sign in within 15 minutes and the app answers the original question automatically.

### Limits / caveats (verbatim)
> "**Private channels only.** Rho posts to the private channels you add it to." [HC adds: *"The app does not operate in public channels. If it is invited to one, it says so and removes itself."*]

> "Can I approve payments from Slack? **Not yet.** Today's release is visibility and answers. Acting on your money from Slack is coming."

> "A Rho admin authorizes the connection, and can revoke it anytime."

Marketing says *"Your Rho permissions carry over"* and *"respect the Rho permissions you already have."* [HC] says: *"The Rho Slack App is available to **Account Owners and Admins today**, with support for more roles on the way."*

### Fees
None. Included.

---

## 15. Rho API: `/product/api` + docs.rho.co

### What it literally is
A **read-only REST API plus an MCP server**, launched **August 3, 2026** (*"Read-only is live today. Write access and webhooks are next."*). Base URLs: production `https://rhoapi.rho.co/api/v1`, sandbox `https://rhoapi-sandbox.rho.co/api/v1`, MCP at `/mcp/v1`.

### Positioning (Rho's own framing)
*"Open banking APIs and aggregators (Plaid, for example) are third parties that connect many banks to many apps on your behalf. Banking-as-a-service APIs let a software company embed banking inside its own product for its own users. The Rho API is neither: it is **the banking platform's own front door to your own company's data**."*

### Access and tokens [API]
- **Only Account Owners and Admins** can create tokens; creation is **2FA-protected**.
- Token prefix **`rhobat_`**; shown **once only**.
- **At most 20 active tokens per business.**
- **Expiration is required, maximum one year.**
- **Auto-expire after 45 days of inactivity** (for never-used tokens, the window starts at creation).
- Optional **IP allowlist, up to 100 entries per token**.
- `401` = invalid/expired token; `403` = valid token lacking scope, **or request from an IP outside the allowlist**.
- Sandbox accepts **any non-empty bearer token**.

### Scopes: the docs disagree with themselves
`docs/v1/auth` lists exactly three: **`accounts:read`, `transactions:read`, `statements:read`**. But `docs/v1/cards` says *"Both endpoints require the **`cards:read`** scope"* and `docs/v1/invoicing` says *"Every endpoint requires the **`invoicing:read`** scope."* Five scopes exist in practice; the canonical scopes table lists three.

### Rate limits [API]
| Limit | Threshold |
|---|---|
| Per API Access Token | **~60 requests per minute** |
| Per source IP | **~600 requests per minute** |
`429 Too Many Requests` with a `Retry-After` header; *"If it is `0`, we have not applied a fixed cooldown… use exponential backoff with jitter."* *"Pace traffic steadily below one request per second."*

### Resources and enums [API + sandbox]
**Accounts**. `account_type` enum per docs: `checking`, `savings`, `credit`, `investment`, `rewards`. `account_type` is immutable. **No server-side type filter** on the list endpoint; filter client-side. Balances are **integer minor units** with ISO 4217 currency. Sandbox account names observed: "Reserve Checking", "Primary Checking", "Inventory Checking", "Treasury Checking", "Cash (Checking)", "Credit Account", "Savings", "Rewards". (Sandbox and statements use `treasury`, not `investment`. See §17, item 27.)

**Transactions**. One record = one ledger event on one account. `id` is *"not guaranteed unique per row"*; **group on `money_movement_id`**. Full `transaction_type` enum (33 values):
`card_credit`, `card_debit`, `card_refund`, `credit_repayment`, `credit_repayment_refund`, `credit_cashback`, `ach_credit`, `ach_debit`, `ach_return`, `wire_in`, `wire_out`, `wire_fee`, `international_wire_in`, `international_wire_out`, `check_deposit`, `check_payment`, `internal_transfer`, `savings_deposit`, `savings_withdrawal`, `savings_interest`, `treasury_deposit`, `treasury_withdrawal`, `treasury_fee`, `treasury_interest`, `treasury_maturity`, `treasury_sale`, `treasury_market_value_adjustment`, `rewards_accrual`, `rewards_cashback_redemption`, `adjustment_credit`, `adjustment_debit`, `international_wire_fee`, `international_wire_fee_refund`.
`status`: `pending`, `settled`, `failed`, `awaiting_approval`. Filters: `account_id`, `account_type`, `card_id`, `user_id`, `transaction_type`, `status`, `search`, `min_amount`, `max_amount`, `initiated_after/before`, `posted_after/before`, `sort_by`, `order`, `page_size`, `page_token`.
`tracking_number` carries an **ACH NACHA trace number or a wire IMAD/OMAD**; *"MT103 reference numbers are not returned."*
`amount.amount` is a **signed integer in minor units; negative values are debits**.

**Cards**. `type`: `physical`, `virtual`. `status` values observed in sandbox: `active`, `canceled`, `expired`, `locked`, `suspended`. `spending_limit_type` observed: `daily`, `fixed`, `monthly`. Records carry `allowed_categories` / `blocked_categories` (MCC code + name), `allowed_merchants` / `blocked_merchants`, `current_spend`, `pending_spend`, `spend_period_start/end`, `usage_starts_at` / `usage_ends_at`, billing and shipping addresses. `page_size` defaults to 20, range 1–100. *"An unfiltered list includes canceled and expired cards so their stable IDs can still be joined to historical transactions."*

**Statements**. `statement_type` observed: `account`, `credit`, `treasury`. Each carries per-account `opening_balance`, `closing_balance`, `total_credits`, `total_debits`, `total_fees`, plus a **short-lived signed `pdf_url`** (sandbox URL shows `X-Goog-Expires=899`, i.e. ~15 minutes).

**Invoicing**. See §10 for enums. Invoice PDFs via `GET /invoicing/invoices/{invoice_id}/files/{file_id}` returning a *"fresh, short-lived `download_url`; do not persist that URL."*

### MCP [API]
- Streamable HTTP at `/mcp/v1`. *"MCP uses the same API contract, authentication model, scopes, and error behavior as the REST API."*
- Protocol versions advertised: **`2026-07-28`, `2025-11-25`, `2025-06-18`**. *"Versions older than `2025-06-18` and JSON-RPC batches are rejected."* `MCP-Protocol-Version` header required on every non-`initialize` request.
- Two auth paths: **direct** (bearer token) and **linked apps** (OAuth provided by the MCP client).
- Claude Code install line, verbatim: `claude mcp add --scope project --transport http rho-api https://rhoapi.rho.co/mcp/v1 --header "Authorization: Bearer <rho_api_access_token>"`
- Rho is listed in **Anthropic's MCP connector directory**; *"Claude is the natively supported client today."*

### What connected AI tools can and cannot do [HC]
Can see: **Accounts** (details, types, balances), **Transactions** (card, ACH and wire transfers, refunds), **Statements**.
Cannot: *"Move money; Issue, lock, or edit cards; Add or manage users; Make changes to your Rho account."*
*"Only Account Owners and Admins can initiate an OAuth connection."*

### Versioning contract
`v1` is **additive-only**; breaking changes reserved for a new API version. Page tokens *"belong to the API version that created them, so restart pagination when migrating from v0 to v1"* (implying a prior v0).

### Fees / eligibility
**Free.** *"API access is available to every Rho customer, with no waitlist and no approval step."*

### Caveats (verbatim)
> "¹ Rho API access tokens are read-only and scoped to account and transaction data. **Tokens cannot initiate payments or modify accounts**, and can be revoked at any time. **The Rho API is read-only today.**"

> "The Rho API is read-only today; every token is read-only, which also means **a leaked token cannot move money**."

### Competitor table [Rho claim], "Mercury, Brex, Ramp as of 2026-08-20"
| | Rho | Mercury | Brex | Ramp |
|---|---|---|---|---|
| Can API tokens move money? | **No, by design** | "**Yes**, the API can initiate ACH transfers" | "**Yes**, the Payments API sends ACH, domestic wires, and checks" | "**Yes**, write operations include bill creation, payment execution, and card issuance" |
| MCP / AI | Native Claude connection + MCP guide | "Native MCP server, read-only for AI tools" | "No MCP or AI-assistant integration documented on developer.brex.com" | "Three documented MCP servers" |
| Token security | Scoped, revocable, optional IP allowlists, Owners/Admins only | "Scoped tokens with fine-grained permissions and IP allow-listing" | "Admin-created tokens, scoped at creation, **expire after 90 days unused**" | "OAuth 2.0 with granular permission scopes" |
Rho frames read-only as a security feature; a buyer could equally read this row as three competitors having a materially more capable API.

---

## 16. How the products interlock

### Feed map (which product feeds which)

| From → To | Direction and mechanism | Constraints |
|---|---|---|
| **Incorporation → Checking** | Account application opens in the same signup flow; SS-4 filed for you | Funds cannot move until IRS issues the EIN; 30/60-day pre-EIN window |
| **Incorporation → the $400 credit-back** | Credit posted to **Rho Checking** | Requires $10,000 new money + 60-day daily-average-balance test ($1,000 for accelerator-introduced founders) |
| **Checking → Savings** | Only source of funds for Savings. Unlimited transfers in | Same business day if before 1pm ET; **6 withdrawals/month back** |
| **Savings → Checking** | Only destination | Next business day (HC) / 2 business days (settlement table) / "within 2 business days typical" (marketing) |
| **Checking → Treasury** | Manual transfer or auto-transfer rule | $50,000 minimum; 2–3 business days |
| **Treasury → Checking** | Withdrawal or maintain-minimum rule | IJTXX same-day by 3pm ET; other assets 1–3 business days; **only one Checking account can be funded by Treasury**; Treasury→Checking auto-rules limited to weekly / 11th+25th / monthly |
| **Checking → Cards (Daily Terms)** | **Auto-debit just after midnight EST** for prior day's settled charges | Daily credit limit is a function of **available checking balance** + risk factors |
| **Checking or external account → Cards (Monthly Terms)** | Auto-repayment at end of 30-day cycle, 1-day repayment period | Requires **$25,000 held at Rho** (or $75,000 combined with linked external accounts) |
| **Cards → Rewards account** | Cashback accrual posts to a dedicated `rewards` account | Daily Terms: 6th business day of month. Monthly Terms: ~6 business days after paying statement in full |
| **Rewards → Checking** | Manual redemption, **instant** | Owners/Admins (or custom role with Redeem Rewards) only; forfeited if unredeemed 12 months |
| **Rewards → Card statement** | "Pay with Cashback" applies rewards as a statement credit | Credit may land on the following cycle; you must still pay the current statement on time |
| **Cards → Expense Management** | Every card transaction is an expense object with receipt, coding, approvals | Same system; no separate product |
| **Gmail → Expense Management** | Gmail Connector auto-attaches receipts to the matching card transaction | Point-of-connection forward only; per-user connection |
| **Bill Pay inbox → Bill Pay → Checking** | Forwarded invoice → OCR draft → approval → payment debited from Rho Checking | Marketing says check only; HC says ACH, domestic + international wire, check, single-use card |
| **Bill Pay → Vendor Cards** | Single-use AP card issued as a Bill Pay payment method | One charge, preset amount, 14-day window, 72-hour secure-link expiry |
| **Vendors module → Vendor Cards** | Creating a vendor can auto-create a linked single-use card | That path can only create single-use cards; deleting the vendor cancels all linked cards |
| **Invoicing → Checking** | Customer payments land directly in Rho Checking and auto-match to the invoice | Card payments route through a Rho-managed **Stripe** account; 2.9% + $0.30; $10,000/day cap |
| **Capital → Checking** | Approved draws land in the Rho account in 24–48 hours | Underwritten by Slope; loans made by Lead Bank |
| **Everything → Rho Close** | Close reads card and banking transactions plus prior coding decisions and suggests attributes | **Requires a native accounting integration**; ignores already-coded attributes; does not touch mapping rules |
| **Everything → Accounting integrations** | QuickBooks Online, NetSuite, Sage Intacct, Puzzle native; Xero via bank feed | QBO bank feed expanded to Treasury and Savings accounts (April 2026) |
| **Everything → Rho API / MCP** | Read-only accounts, transactions, statements (plus cards and invoicing endpoints) | Owners/Admins create tokens; cannot move money |
| **Everything → Slack app** | Balances, transactions, statements, alerts | Private channels and DMs only; Owners/Admins only today; no payment approval |
| **Payroll + revenue + 50% of assets + open card → Rho Platinum** | The consolidation flywheel: meeting all four raises cashback from 1.25% to 2% (Daily) or 1% to 1.75% (Monthly) | Status is continuously re-evaluated; lose a condition, lose the rate |

### The strategic shape
Three concentric rings:
1. **Acquisition ring** (loss leaders): Incorporation ($400, refunded), Invoicing (free), Bill Pay (free), Expense Management (free), Close (free), Slack (free), API (free), Vendor Cards (free). All of these exist to make Rho Checking the system of record.
2. **Monetization ring:** Corporate Cards (interchange, with Platinum as the consolidation lever), Treasury (0.15%–0.60% AUM, with the fee tier computed on **Checking + Treasury combined**, so holding cash in Rho Checking directly lowers the Treasury fee), Savings (deposit spread: Rho pays up to 1.00% APY while T-bills yield ~3.8%), FX (1%), Capital (referral/origination economics with Slope/Lead Bank).
3. **Gating ring:** the thresholds that push balances toward Rho. **$25,000** avg monthly balance for Savings interest, **$25,000/$75,000** for card Monthly Terms, **$50,000** for Treasury, **50% of company assets** for Platinum, **$20M+** for the best Treasury fee tier, **$10,000** for the incorporation credit-back.

Every "free" product is a cash-concentration mechanism. The only products with published prices are the two where Rho takes a spread anyway (Treasury advisory fee, FX) plus the one fully refundable fee (incorporation).

---

## 17. Contradictions inside the corpus

| # | Topic | Claim A | Claim B | Severity |
|---|---|---|---|---|
| 1 | **Who lends on Capital** | `/product/capital` FAQ: *"Is Rho a direct lender for its working capital line of credit? **Yes.**"* | Same page's footer: *"Financing offered by **third parties**… Rho Capital is not a broker-dealer… Rho does not guarantee that the connection services will result in financing"* + *"Business-purpose loans made by **Lead Bank**"* + *"set when **Slope** underwrites your line"* | **High.** A material lender-identity claim contradicted by its own disclaimer on the same page. |
| 2 | **Treasury headline yield's assumed allocation** | Footnote everywhere: 4.66% *"assumes… a **100% allocation** to the Vanguard Short-Term Investment-Grade Fund (VFSTX)"* | [HC]: *"Vanguard allocations are **capped at 50%** of your portfolio"* | **High.** The advertised top rate assumes an allocation the product forbids. A customer cannot achieve 4.66%. |
| 3 | **Bill Pay payment methods** | `/product/bill-pay`: step 4 is *"Once approved, **pay by check**"*; fee row *"$0 on checks"*; *"Rho Bill Pay supports check payments"* | [HC]: *"ACH transfers; Wire transfers (domestic and international); Checks; Single-use cards"* | **High.** Product page understates the product. |
| 4 | **Number of Treasury assets** | `/product/treasury` and `/treasury-yield-comparison`: **three** (T-Bills, MULSX, VFSTX) | [HC]: **four**, per *"You can hold up to 4 assets simultaneously"*, adding **IJTXX** (the only same-day-liquidity asset, live since 07/23/2026) | **High.** The most liquid asset is invisible on the public pages. |
| 5 | **Is MULSX a money market fund?** | `/product/treasury` table column: *"Morgan Stanley **money market fund**, net (7-day SEC yield)"*; `/policies/yield-methodology`: *"Money market funds (Morgan Stanley MULSX)"* | [HC]: *"**It is not a money market fund** - NAV is variable"* | **High.** Material mischaracterization of investment risk. |
| 6 | **Treasury minimum** | `/product/treasury`, `/treasury-yield-comparison` intro, and its FAQ: **$50,000**; fee tier labeled **"$50K–$2M"** | `/treasury-yield-comparison` comparison table row "Minimum": **$100,000**; tier matrix labeled **"$100K–$2M"** | **High.** Same page states both. |
| 7 | **Rho has no yield product below $50K** | `/treasury-yield-comparison`: *"below Rho Treasury's $50,000 minimum, **Rho doesn't have a yield product to sell you**"* | `/product/business-savings-account`: up to 1.00% APY at a **$25,000** average monthly balance | Medium |
| 8 | **Invoicing accounting sync** | `/product/invoicing`: *"Rho Invoicing **does not yet sync** with accounting software like QuickBooks or Xero, and **there is no mobile app**"* | Changelog 08/31/2026: *"Rho invoices now sync to QuickBooks… as accounts receivable invoices"*; [HC] "Syncing invoices to your accounting software"; changelog also ships mobile invoice/card/reimbursement features | **High.** Marketing page is stale against Rho's own release notes. |
| 9 | **Invoicing recurring + matching** | `/product/invoicing` body: *"Recurring invoices: set them up once and they go out on their own"*, *"payments match to the right invoice automatically"* | Same page's comparison table, Rho column: **"Not shown"** for both Recurring invoices and Payment matching | Medium |
| 10 | **Invoicing card fee** | `/product/invoicing`: *"$0 per-invoice and monthly fees"*, *"$0 on domestic ACH, wire, and check payments"*; card acceptance listed as a feature | [HC] + changelog: **2.9% + $0.30 per card transaction, paid by the business**, capped at **$10,000/day**, surcharging not allowed | **High** (omission on the product page). |
| 11 | **Savings activation** | `/product/business-savings-account`: *"Activate Business Savings from your Rho dashboard. **There is no separate application and no new login.**"* | [HC]: click **Request Access** → Client Service sends a **DocuSign** agreement → signed agreement submitted to the partner for review → *"our partner may request additional information before your account is opened"* | Medium |
| 12 | **Savings → Checking timing** | Marketing: *"Within 2 business days typical"* | [HC sweep article]: *"typically settles the **next business day** if created before 1pm ET"*; [HC settlement table]: *"**2 business days**"* | Low-Medium |
| 13 | **Wire recall fee** | Homepage fee table: *"Wire recall fee $0"* with a footnote omitting recall fees | /pricing: *"**Domestic** wire recall fee $0"* with footnote *"a **$30 international wire recall fee**"*; [HC]: failed/returned domestic wires cost *"around **$20 – $45**"* | Medium |
| 14 | **"The only standard payment fee is 1% on FX"** | [HC, `pricing-requirements`] | Contradicted by $15 SWIFT, $30 international recall, $20–45 failed-wire, 2.9%+$0.30 invoice card fee | Medium |
| 15 | **API scopes** | `docs/v1/auth` scopes table: three scopes (`accounts:read`, `transactions:read`, `statements:read`) | `docs/v1/cards`: `cards:read` required; `docs/v1/invoicing`: `invoicing:read` required | Medium (docs defect) |
| 16 | **API surface** | `/product/api`: *"read-only programmatic access to their **balances, transactions, and statements**"*; `docs/v1/getting-started`: *"covers **accounts and transactions**"* | Docs and sandbox also expose **Cards** and **Invoicing** endpoints | Medium |
| 17 | **Homepage: "Rho API New. Banking and payments via API"** | Homepage nav | `/product/api`: *"**Tokens cannot initiate payments** or modify accounts"* | **High.** The nav label advertises a capability the product explicitly does not have. |
| 18 | **Homepage Treasury yield** | Homepage product tile: *"Up to **4.57%** net yield, automatically"*; homepage footnote dated **08/14/2026** | Homepage nav and every other page: *"Earn up to **4.66%**"*, dated 09/11/2026 | Medium (stale tile) |
| 19 | **Rho Close supported integrations** | `/product/close` FAQ: *"QuickBooks Online, Oracle NetSuite, and Sage Intacct via native direct integration. **Xero** is also supported via bank feed"* | [HC]: *"businesses with a direct accounting integration (**QuickBooks, NetSuite, Puzzle, or Sage Intacct**)"*. Puzzle in, Xero out | Medium |
| 20 | **Rho Close "nothing syncs until you approve"** | `/product/close`: *"Nothing syncs until you say so"*, *"Every step requires your sign-off"* | [HC]: *"If you do sync an individual transaction without actively accepting or dismissing the suggestions, **those suggestions will be applied to the sync**"* | Medium |
| 21 | **Slack permissions** | `/product/slack`: *"Your Rho permissions carry over"*, *"respect the Rho permissions you already have"* | [HC]: *"available to **Account Owners and Admins today**"*. Other roles can sign in only to express interest | Medium |
| 22 | **Vendor cards survive churn** | `/product/vendor-cards`: *"Cards default to the creator as cardholder, so they **stay working even when team members churn**"* | [HC]: *"If the user who created a Vendor Card is removed, you will be prompted to delete the card"*; deleting a vendor cancels all its cards | Medium |
| 23 | **Vendor cards on mobile** | [HC]: *"Vendor cards are currently a **web-only** feature, so they won't appear in the mobile app"* | Changelog March + May 2026: vendor cards viewable and creatable in the mobile app | Low |
| 24 | **Cards "no category restrictions"** | `/product/corporate-cards` comparison: *"Real cash, not points, **no category restrictions**"* | Same page's footnote: excludes Walmart + affiliates, utilities MCCs, money-transfer/quasi-cash MCCs, and **all non-US transactions** | Medium |
| 25 | **Expense management accounting integrations** | One FAQ answer: *"QuickBooks Online, NetSuite, Sage Intacct, **Xero**, or Puzzle"* as direct integrations | Another FAQ answer on the same page: *"**Xero connects today through a bank feed rather than a native sync**"* | Low |
| 26 | **Treasury fee base** | [Marketing/policy]: fee tier based on *"total Rho deposits"* / *"assets under management"* | [HC]: *"AUM includes the combined balance of your Rho **Checking and Treasury** accounts"* | Low-Medium (the HC version is materially more favorable to the customer and is the one not marketed) |
| 27 | **Account type enum** | `docs/v1/accounts`: `investment` | Sandbox statements + auto-generated statement records use `treasury` | Low (API defect) |

---

## 18. What is conspicuously NOT stated

1. **Capital pricing.** No APR, no factor rate, no fee range, no example cost of a draw, anywhere in the corpus. Only *"Fees vary, confirmed before you accept a line."* Rho publishes a precise fee schedule for everything else.
2. **Capital's real eligibility floor.** The page insists there is no fixed threshold, but the Slope/Lead Bank disclaimer says *"Subject to **minimum revenue** and business requirements."* The number is never given.
3. **The Savings partner-bank list.** *"available from Rho support on request."* Never published. A customer cannot check concentration risk pre-signing.
4. **The Savings "accredited investor" representation.** Buried in the ADM Master Services Agreement, absent from all marketing.
5. **The extended-deposit-insurance waiver.** *"By signing Exhibit A, Client expressly waives extended deposit insurance"*. This is the one clause that qualifies the "$75M insured" headline, and it appears only in the reproduced contract.
6. **IJTXX.** The only same-day-liquid Treasury asset does not appear on `/product/treasury` or `/treasury-yield-comparison`, both of which sell "2 to 3 business days" as the liquidity story.
7. **The invoice card fee.** 2.9% + $0.30 appears in the changelog and help center but not on the product page whose headline is "$0 per-invoice and monthly fees."
8. **The $1,000/year post-year-1 incorporation platform fee** and the **$100/$250 per-contract charges.** Stated once, in a small "How the fee works" box on the incorporation page. Never surfaced in the fee summary, on /pricing, or anywhere else.
9. **Card credit limits.** Never quantified. Daily Terms capacity is an opaque function of *"your available checking balance as well as risk factors that vary by client."* Monthly Terms limits are *"personalized."* No minimum, maximum, or typical figure.
10. **Any accuracy claim for Rho Close.** No stated suggestion-accuracy rate, no benchmark, no error-handling disclaimer, despite it writing to customers' general ledgers.
11. **Uptime/SLA for the API.** Rate limits and versioning are documented; availability commitments are not.
12. **Whether the Slack agent-chat beta or the Gmail Connector send customer data to a third-party LLM.** Both are AI features; neither page names a model provider or a data-processing arrangement.
13. **International/FX pricing detail beyond "1%".** The Wise relationship is disclosed; the spread mechanics, mid-market-rate reference, and per-corridor pricing are not.
14. **Savings APY history or how the "variable, set monthly" rate is determined.** The Treasury yield methodology page is rigorous; there is no equivalent for the Savings APY.
15. **Multi-entity mechanics.** "Rho for Enterprises. Streamline accounting and expenses across multiple entities" is nav copy; no product page explains how multi-entity works, and the API token is explicitly *"scoped to a single business."*
16. **Anything about deposit concentration at Webster/Santander** beyond "$76B in assets", and no mention of what happens to checking balances above $250,000 (the answer is implicitly "uninsured, move it to Savings").
17. **LLC formation.** "Coming soon" in the nav since at least this snapshot; no date.
18. **Write access and webhooks for the API.** "Next" as of 08/03/2026; no date.
19. **Payment approval from Slack.** "Coming"; no date.
20. **A published SOC 2 / security page detail set** exists (`/security`, `/trust`, a "SOC 2 Type 2 Compliance" help article) but no product page ties a specific control to a specific product.

---

## 19. Date ledger (carry these through)

| Date stamped | What it stamps |
|---|---|
| **12/10/2025** | SVB's last published rate sheet, still the posted sheet as of 08/02/2026 [Rho claim] |
| **April 10, 2025** | Rewards Terms & Conditions version date |
| **07/23/2026** | Apex Ascend cutover: accounts opened on/after this date get IJTXX + VFSUX |
| **07/31/2026** | Brex rates effective date [Rho claim] |
| **08/02/2026** | International wire fees, $15 delivery-fee toggle, 1% FX rate; Mercury/Brex/SVB/Axos competitor verification |
| **08/03/2026** | Yield Methodology policy date; Treasury settlement promise ("within two business days"); Rho API launch |
| **08/05/2026** | Bluevine verification [Rho claim] |
| **08/14/2026** | Homepage footnote yield date (stale relative to the rest of the site) |
| **08/20/2026** | Mercury treasury minimum verification; API competitor data; Slack page competitor data |
| **August 2026** | Savings APY "up to 1.00%" as-of; 400+ partner-bank network count as-of |
| **08/28/2026** | Mercury yield figures [Rho claim] |
| **08/31/2026** | Incorporation launch; invoice card payments launch; invoice→QuickBooks sync |
| **09/06/2026** | Checking, Savings, Treasury competitor data collection |
| **09/07/2026** | Incorporation competitor data collection |
| **09/08/2026** | Cards, Expense Management, Bill Pay, Invoicing competitor data collection |
| **09/11/2026** | Treasury net yields (4.66% top tier); T-Bill benchmark 3.81%; "Product claims current as of September 2026" |

Blog/article publication dates observed: vendor card guide published **October 06, 2025**, updated **August 29, 2026**; Rho Close announcement published **May 06, 2026**, updated **September 01, 2026**.

---

## 20. Verbatim disclaimer stack (appears on almost every page)

> "Rho is a fintech company, not a bank or an FDIC-insured depository institution. Checking account and card services provided by Webster Bank, a division of Santander Bank, N.A., member FDIC. Savings account services provided by American Deposit Management Co. and its partner banks. International and foreign currency payments services are provided by Wise US Inc. FDIC deposit insurance coverage is available only to protect you against the failure of an FDIC-insured bank that holds your deposits and subject to FDIC limitations and requirements. It does not protect you against the failure of Rho or other third party. Products and services offered through the Rho platform are subject to approval."

> "The Rho Corporate Cards are issued by Webster Bank, a division of Santander Bank, N.A., member FDIC pursuant to a license from Mastercard, subject to approval."

> "Investment management and advisory services provided by RBB Treasury LLC dba Rho Treasury, an SEC-registered investment adviser and subsidiary of Rho. RBB Treasury LLC facilitates investments in securities: investments are not deposits and are not FDIC-insured. Investments are not bank guaranteed, and may lose value. Investment products involve risk, including the possible loss of the principal invested, and past performance does not indicate future results. Registration with the SEC does not imply a certain level of skill or training. Treasury and custodial services provided through Apex Clearing Corp. ('Apex') and Interactive Brokers LLC ('Interactive'), registered broker dealers and members FINRA/SIPC. Interactive rates may vary from Apex rate shown above."

> "Rho Treasury is not insured by the FDIC. Rho Treasury are not deposits or other obligations of Webster Bank, a division of Santander Bank, N.A., or American Deposit Management Co.'s partner banks, and are not guaranteed by Webster Bank… Rho Treasury products are subject to investment risks, including possible loss of the principal invested."

> "* This reflects the sought net yield based on 90-day Treasury Bill rates as of 09/11/2026 and an annual fee which ranges from 0.15% for deposits of $20M or more to 0.6% (the maximum annual fee) for deposits under $2M. Individual results may vary depending on the actual investment date and investment products selected. Past performance is not a guarantee of future performance results. The yield is variable and fluctuates without prior notice. The rate shown is net of fees. **The amount of Treasury Bills available at a particular yield will depend upon the sellers' offer size; any remaining cash balance after the purchase may not earn the same yield.**"

> Testimonial disclosure (Treasury page only): "Certain clients providing testimonials may have received, or may receive, compensation or other items of value, which may include sign-up bonuses, discounts, fee reductions, or promotional incentives, in connection with their participation. **Such compensation or incentives may create a potential conflict of interest.**"

> Rewards footnote (cards): "Cashback is earned on card spend, up to $1,000,000 in eligible spend per calendar year across all tiers, **issued as a statement credit**, requires payment of the full statement balance on time, must be redeemed within 12 months of earning, and excludes certain categories including Walmart and affiliates, utilities, money transfers and quasi-cash, and non-US transactions. A late fee of 3% of the delinquent payment balance per month may apply for up to six months, unless prohibited by law. Late payment forfeits rewards."

---

## 21. Source files read for this document

Marketing: `pages/core/homepage.txt`, `faq.txt`, `pricing.txt`, `changelog.txt`, `treasury-yield-comparison.txt`, and all thirteen `pages/core/product__*.txt` (api, bill-pay, business-banking, business-savings-account, capital, close, corporate-cards, expense-management, incorporation, invoicing, slack, treasury, vendor-cards).
Policies: `policies__yield-methodology.txt`, `policies__cashback-rewards.txt`, `policies__rewards-terms-and-conditions.txt`.
Help center: transfer-limits, payment-settlement-times, fees-for-recalls-failed-wires, rho-platinum-what-it-is-and-how-to-qualify, understanding-card-cashback, cashback-rewards-terms-conditions, the-rho-card-with-daily-terms, the-rho-card-with-monthly-terms-2, understanding-rho-savings-accounts, how-the-rho-savings-sweep-works, rho-savings-account-terms-and-conditions, how-does-fdic-insurance-coverage-work, about-rho-treasury, understanding-rho-treasury, setting-up-auto-transfer-rules, managing-your-rho-treasury-account, about-rho-capital, pricing-requirements, incorporating-your-company-with-rho, bill-pay-at-rho-overview, paying-bills-with-vendor-cards-single-use, paying-international-bills-in-bill-pay, how-to-schedule-a-bill-payment-in-rho, understanding-bulk-payments, understanding-ocr-technology-at-rho, create-an-invoice, accept-card-payments-on-invoices, how-to-create-and-manage-vendor-cards-with-rho, how-to-enable-reimbursements, how-to-use-mileage-reimbursements, how-to-set-up-the-gmail-connector, how-to-set-monthly-user-limits, understanding-rho-card-controls, business-and-industry-eligibility-at-rho, can-i-open-a-rho-account-if-i-dont-live-in-the-u-s, applying-to-rho-faqs, rewards-account-overview, how-do-i-redeem-my-cash-rewards, are-cashback-rewards-taxable, understanding-rho-check-mechanics, how-to-set-up-multiple-operating-accounts, what-is-rho-close, how-to-use-the-rho-slack-app, understanding-the-rho-slack-app, what-connected-al-tools-have-access-to-in-your-rho-account.
API: `docs/docs_v1_{getting-started,auth,rate-limits,mcp,accounts,cards,transactions,invoicing}.md`, `api/transactions_listtransactions.md`, and sandbox captures `sandbox/{accounts,cards,transactions,invoicing_invoices,statements}.json`.
