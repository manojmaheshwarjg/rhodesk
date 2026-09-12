## 4. How Rho makes money

Rho's pricing page is a list of zeros. Seven rows, six of them `$0`, under the headline "Finance automation - without annoying subscription fees." The machine-readable summary Rho publishes for language models compresses the whole schedule into one sentence: "No monthly fees, no per-user fees, no platform software fees; $0 same-day ACH and $0 domestic wires, the only standard payment fee is 1% on foreign-currency transfers (as of 08/02/2026)." A product page goes further: "Every fee on this page is $0."

So where does the money come from? Six places, only four of which Rho names. This section walks each one, prices it where a price is published, and then sets out what the research could and could not substantiate.

### 4.1 The revenue map

| Line | What it is | Does Rho disclose it? |
|---|---|---|
| Interchange | A cut of every card purchase, paid by the merchant | No. Never mentioned on any Rho page |
| Deposit spread | Rho earns more on customer balances than it pays out | No. Named only in the affiliate contract |
| Treasury advisory fee | 0.15% to 0.60% per year on assets | Yes, with a full tier table |
| FX margin | 1% on foreign-currency conversion | Yes, it is the headline fee |
| Invoice card acceptance | 2.9% + $0.30 per card-paid invoice | Only in the invoicing terms and one help article |
| Capital, incorporation, transaction fees | Lending referral plus a long tail of charges | Partially, in footnotes and the Terms of Service |

Two lines carry the business. The other four are rounding by comparison.

### 4.2 Interchange: the fee the merchant pays

**The mechanic.** When a company buys something with a Rho card, the merchant does not receive the full purchase price. The card networks route a percentage of it back to the institution that issued the card. That percentage is **interchange**. A $10,000 software invoice paid on a premium US commercial card sends roughly $230 to $260 back up the chain, and the merchant absorbs it as a cost of accepting cards. This is why interchange is the natural revenue base for any company that gives finance software away: the payer never sees a line item, and the fee scales with the customer's spending rather than with their headcount.

Two structural facts make commercial cards the rich end of this market. First, the Durbin Amendment's interchange cap (a 2010 US law limiting what banks can charge on debit transactions) applies to debit, not to credit and charge cards, so business charge cards are uncapped. Second, premium commercial tiers price above consumer cards.

**What Rho issues.** Every Rho card is a Mastercard World Elite Business charge card, issued by Webster Bank, a division of Santander Bank, N.A. A **charge card** is one where the full balance is repaid each cycle rather than carried at an interest rate, so the issuer earns interchange but no lending interest. On Rho's Daily Terms the balance is auto-debited from the customer's own checking balance roughly a day after the charge settles.

**Verified:** Mastercard's published 2026 to 2027 US interchange schedule, effective 2026-04-17, prices World Elite at 2.60% + $0.10 on Merit I, the baseline program covering card-not-present purchases (online and keyed transactions). Commercial rates vary materially by the type of merchant, by how much purchase detail the merchant transmits with the transaction, and by the size of the individual purchase, so 2.60% is a ceiling reference rather than a blended average. The issuer does not keep all of it: the network takes its own cut (called assessments), and in a sponsor-bank arrangement the bank (Webster, now inside Santander) takes a share before anything reaches the program manager, which is the role Rho itself plays.

**What Rho gives back.**

| Program | Daily Terms | Monthly Terms |
|---|---|---|
| Standard | 1.25% | 1.00% |
| Rho Platinum | up to 2.00% | up to 1.75% |

Cashback is capped at $1,000,000 of eligible spend per calendar year across all tiers, must be redeemed within 12 months or it is forfeited, and is forfeited entirely for any billing period not paid in full and on time. Rho's own rewards terms state that "Rho will not provide notifications regarding the impending expiration."

**Assessment:** on the card line alone, the arithmetic is thin. If gross commercial interchange blends somewhere in the low 2% range and the sponsor bank and network take their share first, a 2% giveback leaves very little. Rho Platinum is therefore best read not as a card product at all but as a **deposit-acquisition instrument**: it is the only tier that pays 2%, and qualifying for it requires payroll, revenue and 50% or more of company assets at Rho (see 4.10). Rho is buying balances with interchange it may barely be earning. The $1M annual cap, the 12-month expiry with no warning, and the total forfeiture on a single late payment are all breakage mechanisms that recover some of that giveback.

**Verified (with an important caveat):** the adversarial check on this dossier's fee claims found that **interchange as a Rho revenue line is unsourced inside the rho.co corpus**. The word never appears in connection with Rho anywhere on the site, only in Rho's descriptions of Mercury. The support is external and dated: Banking Dive, 2022-08-23, quoting Rho's own characterization that the company "generates a significant proportion of its revenue from interchange fees" and "doesn't charge subscription fees." Treat interchange as a well-supported inference with one four-year-old first-party corroboration, not as a disclosed fact.

The contrast is sharp, and Rho drew it itself. On its own comparison blog Rho writes out a competitor's model in full: "Mercury makes money in six different ways: Interest earned on checking deposits... Merchant fees (interchange fees) are paid by merchants when customers use an IO card or a Mercury debit card... Earnings on foreign exchange processing on international wires..." Rho publishes no equivalent paragraph about itself.

### 4.3 Deposit spread: the largest line, and the one Rho never names

**The mechanic.** A company's cash sitting in an account is a liability to the institution holding it and an asset it can deploy. The institution pays the depositor one rate and earns another, and the gap is **net interest margin**, or the deposit spread. It is the oldest business in banking. When a fintech says its software is free, the deposit spread is usually the reason it can.

**What Rho pays.**

| Account | Rate paid to the customer | Condition |
|---|---|---|
| Rho Checking | No interest rate published anywhere on rho.co | n/a |
| Rho Business Savings | up to 1.00% APY, variable, as of August 2026 | requires a $25,000 average monthly balance; 0% below it |

The absence on checking is not an oversight of this research. The public API's transaction-type enumeration includes `savings_interest` and `treasury_interest` but has **no `checking_interest` type at all**, which is consistent with checking never paying interest as a matter of product design rather than of current rate levels.

The savings mechanics narrow it further. Interest is "calculated using your average monthly balance with daily ending balances used to determine the monthly average," on "a 30/365 day convention," posted "on the 5th business day of each month." A 30/365 convention counts 360 interest days in a 365-day year, so a nominal 1.00% pays closer to 0.986% over a full year. Averaging rather than accruing daily means a balance that spikes and drains earns on the average, not on the peak.

**What the same money could earn.** Rho's own treasury comparison page, on 2026-09-11, cites the US Department of the Treasury for a **3.81% trailing 7-day average yield on 13-week US Treasury Bills**. That is the risk-free short-term rate against which any deposit rate should be read.

**Assessment:** as of 2026-09-11, the gross gap between the short-term risk-free rate and what Rho pays is roughly **2.8 percentage points on savings** and roughly **3.8 percentage points on checking**. That gap is not Rho's profit. Out of it come the sponsor bank's share (Webster, a division of Santander, holds the checking deposits), American Deposit Management's share (ADM administers the savings sweep, the arrangement that spreads deposits across 400-plus partner banks to stretch FDIC insurance, covered in the banking-mechanics section), funding costs, reserves and operations. Rho has never published its share of it. But the order of magnitude is clear: on a company holding $2,000,000 at Rho, the gross spread available is in the tens of thousands of dollars per year, against a software bill of $0 and card cashback on a fraction of that.

One more line sits inside the sweep. The ADM master services agreement Rho publishes states that "ADM may, from time to time, place a certain portion of Client's funds in a non-interest bearing transaction account." Whatever those placements earn accrues to ADM and Rho, not to the customer.

**The one document that admits the model.** Rho's Affiliate Terms of Service, dated 2026-07-28, is the only page in the entire 522-page corpus that describes Rho's deposit economics. It is worth quoting at length because the definition is unusually precise:

> "Once your Referred Entity has satisfied the offer's conditions, you shall be eligible for a cash credit ("Affiliate Reward") into your Rho Account equivalent to thirty percent (30%) of the Gross Profits (as defined hereinafter) generated from your Referred Entity's deposits that were deposited during that month. You shall be eligible for Affiliate Rewards for a period of twelve (12) months after the first deposit made by your Referred Entity ("Payout Period"). "Gross Profits" means the total gross revenue recognized by Rho attributable to the Referred Entity's Rho Account deposits during the applicable month, less attributable costs including interest or yield paid to the Referred Entity, funding costs, payment processing fees, reserves, and other expenses."

Read it carefully. Rho recognizes **revenue attributable to a customer's deposits**. It nets off **the interest it pays that customer**. What remains is large enough that Rho will hand a third party 30% of it for twelve months as a customer-acquisition cost. Note the qualifiers the verifier insisted on: the share is capped at a twelve-month payout period, it is paid as a credit into the affiliate's own Rho account rather than cash, and "Gross Profits" is net of five cost categories. Quoting "30% of gross profit" without those caveats overstates the economics.

**Assessment:** this clause is the single clearest public evidence of how Rho thinks about its own business. It is also, revealingly, filed under affiliate marketing rather than under pricing.

### 4.4 The Rho Treasury advisory fee

Rho Treasury is a separate investment product (covered in the products section) run by RBB Treasury LLC, an SEC-registered investment adviser and a Rho subsidiary. It charges a straightforward asset-based fee.

| Total AUM | Annual fee |
|---|---|
| $20M+ | 0.15% (15 bps) |
| $10M to $20M | 0.25% |
| $5M to $10M | 0.35% |
| $2M to $5M | 0.45% |
| Under $2M | 0.60% |

"bps" is basis points, hundredths of a percentage point. Fees are "calculated daily and charged monthly from your portfolio cash balance. If insufficient cash is available, Rho automatically sells a small amount of holdings." Minimum to open: "at least $50,000 in total deposits."

The design detail that matters is how the tier is computed. Rho's help center states it plainly: **"AUM includes the combined balance of your Rho Checking and Treasury accounts."** So moving operating cash into Rho Checking, which pays nothing, lowers the percentage fee charged on the invested cash. The fee schedule is engineered to reward exactly the behavior the deposit spread depends on.

**Verified:** RBB Treasury's Form ADV annual amendment, filed 2026-03-25, reports **$1,892,904,589 in regulatory assets under management across 1,078 discretionary accounts** (1,071 corporations or other businesses, 7 charitable organizations). At the published schedule that implies roughly $3M to $9M of annual advisory revenue depending on how the book distributes across tiers, though the ADV does not publish that distribution and the estimate is mine, not Rho's. Note that $1.89B is the advisory subsidiary's regulatory AUM and is a different quantity from Rho's marketed "$4B+ in deposits."

Rho also quotes yields net of this fee, which is the honest convention. The complication is what the headline yield assumes: the 4.66% figure on /treasury-yield-comparison (as of 2026-09-11) assumes a 100% allocation to the Vanguard Short-Term Investment-Grade Fund at the $20M+ fee tier, while the product caps that fund at 50% of a portfolio. A cap-compliant portfolio at the best fee tier reaches 4.18%. That is treated fully in the products section; it belongs here only as a reminder that the fee tier and the headline rate are quoted at the same unreachable corner of the matrix.

### 4.5 The 1% foreign exchange fee

Rho charges 1% when converting US dollars into another currency to send abroad. International payments are provided by Wise US Inc. Rho's own copy calls it "a market-leading 1% FX rate for foreign currency conversion and transmission," and it is genuinely competitive against legacy business banking, where 2% to 3% is common.

Two things are not disclosed. Rho never says 1% of what, or whether the underlying rate is the mid-market rate Wise itself quotes, so the total take (Rho's margin plus whatever spread sits underneath) is not computable from public information. And the fee never surfaces as an auditable line: the public API's transaction types include `wire_fee` and `international_wire_fee` but **no `fx_fee` or `conversion_fee`**, which means the 1% is embedded in the converted amount and cannot be reconciled as a discrete ledger event.

Separately, and distinct from the wire fee, the card Terms of Service reserve "up to 1% of the transaction amount on foreign transactions." That one appears nowhere on the pricing page.

### 4.6 Card acceptance on invoices: 2.9% + $0.30

If a Rho customer lets their own customers pay an invoice by card, Rho deducts **2.9% + $0.30 per transaction** from the payment before depositing the rest. The invoicing terms state it, a help article states it ("This fee is paid by your business. Your customer pays only the invoice amount"), and the changelog states it. The product page /product/invoicing does not.

**Assessment:** 2.9% + $0.30 is Stripe's standard published card rate, and Rho's own terms confirm the feature is "powered by Stripe, Inc." with a "default processing limit of $10,000 USD per day." This looks like a pass-through with little or no margin. The commercial logic is not the fee: it is that the customer's receivables land in a Rho checking account, where the deposit spread applies.

### 4.7 Rho Capital: referral economics, undisclosed

Rho Capital is a revolving credit line against business cash flow, sized at up to $5M on /product/capital and in its FAQ, though the /blog/rho-capital announcement says "up to $2M" in its own highlights. Rho publishes exactly two prices for it: **$0 origination fee** and **$0 prepayment penalty**. No interest rate, APR, factor rate or price range appears on any Rho page, including four Capital-related URLs that were fetched live on 2026-09-11 specifically to close that gap.

Who actually lends is genuinely unclear from Rho's own copy, and the two statements sit on the same page:

| Where | What it says |
|---|---|
| FAQ on /product/capital | "Is Rho a direct lender for its working capital line of credit? **Yes.**" |
| Body pricing copy, same page | Fees "are set when **Slope underwrites your line**." |
| Hero and end-of-content disclosure | "Rho is a fintech, not a bank. **Financing offered by third parties.** Rho Capital is not a broker-dealer. It does not participate in the negotiation or execution of any transactions between customers and third-party financing sources." |
| Site footer | "Slope is a financial technology company, not a bank. **Business-purpose loans made by Lead Bank** and subject to credit approval." |

**Verified:** all four quotes are live on the page as of 2026-09-11. Note that the Slope sentence is in ordinary mid-page sales copy, not fine print, so "buried in the footer" is not a fair characterization of it. Only the Lead Bank sentence is footer text.

**Assessment:** the disclosure language ("not a broker-dealer," "does not participate in the negotiation or execution") is standard lead-generator drafting, which is what a company writes when it is introducing customers to a third-party lender rather than lending its own balance sheet. Rho's share of a Capital line is nowhere disclosed: not a referral fee, not an origination split, not a servicing share. The FAQ "Yes" is defensible as a statement about product experience (the line lives inside the Rho account end to end) and indefensible as a statement about who holds the credit risk. A reader should treat Capital's contribution to Rho revenue as unknown and probably small relative to interchange and deposits.

### 4.8 Incorporation: a fee that is mostly a deposit test

Rho will file a Delaware C-corp for **$400**, "credited back once you deposit $10,000 in new money into your Rho checking account and keep your daily average balance at least $10,000 above where it started for the 60 days after incorporation." Then, in one sentence on one page: "Registered agent service is included for your first year with Rho Incorporation; **platform access after year one is $1,000 annually and contract services run $100 or $250 per contract**."

**Assessment:** the $400 is a conditional charge. It is credited back only if the customer deposits $10,000 of genuinely new money and keeps the daily average balance at least $10,000 above the starting balance for the 60 days after incorporation, so anyone who misses either half pays it. Nothing is escrowed or restricted in the meantime: the rebate condition is a deposit test, not a price. The verifier flagged that "$1,000 annual incorporation platform fee" is a gloss: the corpus never defines what "platform access" covers or whether it is a registered-agent renewal, so quote the sentence rather than the label.

### 4.9 The fee reality

Rho repeats one sentence in four of its own documents (its help center pricing article, its Chase comparison page, and both machine-readable site summaries), with reworded variants on three more pages: **"The only standard payment fee is 1% on foreign-currency transfers."** Rho never claims "no fees except," so the sentence is technically scoped by the word *standard*. Against that, the corpus documents at least eleven other priced charges.

#### Fees that were substantiated, with source

| Fee | Amount | Source |
|---|---|---|
| Foreign currency transfer | 1% | /pricing fee summary row 06 |
| International wire recall | $30 | /pricing asterisk footnote |
| Wire recall (no "international" qualifier) | $30 | Terms of Service line 191 |
| SWIFT "cover all recipient delivery fees" | flat $15, optional | /pricing footnote; help center |
| Failed and returned domestic wires | "around $20 - $45" | help center, Fees for Recalls and Failed Wires |
| Late payment | "three percent (3%) of the delinquent payment balance for each month," up to six months | /pricing footnote; card addenda |
| Card foreign transaction | "up to 1% of the transaction amount on foreign transactions" | Terms of Service only |
| Card payment on invoices | 2.9% + $0.30 per transaction | Invoicing T&Cs Sec. 4; help center; changelog |
| Incorporation | $400, creditable | /product/incorporation |
| Incorporation, after year one | "$1,000 annually" platform access; "$100 or $250 per contract" | /product/incorporation, one sentence |
| Rho Treasury management | 0.15% to 0.60% per year | /pricing FAQ footnote; help center tier table |
| Wire-recovery assistance | "Rho's current hourly rate for such work" | Terms of Service line 194 |

And above all of them sits an open-ended reservation, in the card addenda: **"Fees are not limited to the aforementioned list and we reserve our right to charge additional or other fees."** The same addendum also promises the customer "will not be charged any fees except as disclosed herein."

#### Which of these are actually hidden

Honesty about the limits of the research is part of the deliverable, so: the word *hidden* does not survive contact with the evidence for several of these.

- **Printed in the pricing page's own asterisk footnote, therefore fine print rather than undisclosed:** the $30 international wire recall, the $15 SWIFT fee, and the 3% monthly late fee. The Treasury fee range is disclosed in the same footnote ("0.15% for deposits of $20M or more to 0.6%... for deposits under $2M"), and the 1% FX fee is the headline.
- **Genuinely buried:** the $20 to $45 failed-wire fee (one help-center article; note that it prices a different event from the pricing page's "07 Domestic wire recall fee $0", which covers a customer-requested recall rather than a wire returned by the receiving bank, so the two are unreconciled rather than contradictory, see section 10), the 2.9% + $0.30 invoice card fee (absent from /product/invoicing), the up-to-1% card foreign-transaction fee (Terms of Service only), and the $1,000-a-year plus $100/$250-per-contract incorporation charges (one sentence on one page, absent from /pricing, the help center and both site summaries).

#### Claims the verifier could NOT substantiate

Four assertions that appear in the underlying research did not survive adversarial checking, and this dossier drops or corrects them:

1. **"Plus interchange, disclosed nowhere except the affiliate agreement."** Factually wrong. The affiliate agreement discloses only deposit-attributable gross profit and never uses the word interchange. Interchange as a Rho revenue line is unsourced inside the corpus; the support is external (Banking Dive, 2022) and it is an inference.
2. **"Rho's revenue is disclosed nowhere."** Too absolute. The 1% FX charge and the 0.15% to 0.60% Treasury AUM fee are both published on the pricing and product pages, with exact numbers.
3. **"The pricing page denies ten fees the help center charges."** Not supported under either reading of "the pricing page." The help center names six nonzero fees; /pricing affirmatively discloses three of them plus the incorporation fee elsewhere. Only two help-center fees are absent from /pricing, and only one (the $20 to $45 failed-wire fee) sits anywhere near an affirmative `$0` line, and even that one prices a returned wire rather than the customer-requested recall the `$0` row covers. The pricing page meanwhile discloses two fees the help center never mentions, so the gap runs in both directions.
4. **"A $1,000 annual incorporation platform fee."** A gloss. The verbatim text is "platform access after year one is $1,000 annually," and Rho never defines what platform access covers.

One genuine internal contradiction is worth keeping: **Rho's published schedule contradicts itself on wire recall.** /pricing says "Domestic wire recall fee $0" and footnotes a "$30 international wire recall fee"; the homepage says "Wire recall fee $0" with no qualifier; the Terms of Service say "$30 wire recall fee" with no qualifier. Cite the specific document, never a blended figure.

### 4.10 The gating structure

Once the revenue model is clear, the thresholds stop looking like product tiers and start looking like a single coherent instrument for pulling cash onto the platform.

| Threshold | What it unlocks | Source |
|---|---|---|
| $10,000 of new money, held 60 days | $400 incorporation fee credited back | /product/incorporation |
| $25,000 average monthly balance | Savings earns interest at all; below it, 0% | help center, Understanding Rho Savings |
| $25,000 held at Rho (or $75,000 across Rho plus linked external accounts) | Card Monthly Terms, subject to underwriting | /product/corporate-cards |
| $50,000 in total deposits | Eligibility to open Rho Treasury | help center, Treasury |
| Payroll + revenue + **50% or more of company assets** at Rho + an open card | Rho Platinum, the up-to-2% cashback tier | help center, Rho Platinum |
| $20,000,000+ combined checking and Treasury | The best Treasury fee tier, 0.15% | help center, Managing your Rho Treasury account |

And every partner-microsite promotion is priced the same way. The 77 `/partner/*` pages gate their sign-up bonuses on an average daily checking balance held for a fixed period: 22 of them at $20,000, a middle band at $100,000 to $300,000, and 25 of them at $400,000 or $500,000. Fifty-six of the 77 also require that "you use your Rho account for your company's payroll."

**This is a legitimate and common model, and it should be said plainly.** Free software funded by balances is how Mercury, Brex, Ramp and most of the sector work, and how consumer brokerages and many banks have worked for decades. Nobody is being deceived by the existence of a spread. The customer receives real value: banking, cards, expense management, bill pay, invoicing and accounting sync, at $0 of software cost, against incumbents that charge $12 to $15 per user per month for a subset of the same thing. Rho's version of the bargain is unusually consistent, because unlike Ramp (free tier plus a $15/user Plus tier plus an undisclosed platform fee) and Brex ($12/user Premium plus Enterprise contracts), Rho does not also sell seats. It took one side of the trade and stayed there.

**What it means for a customer deciding how much cash to concentrate.** The thresholds resolve to a single ask: put most of your money here, run payroll here, land revenue here. Three consequences follow, and they are the actual decision.

1. **The best economics require the largest concentration.** Platinum's 50%-of-company-assets test and the Treasury fee ladder both pay you for concentrating. A company that keeps a second bank relationship for redundancy is choosing to be worse off on rate and cashback. That is a real cost of prudence, and Rho has priced it deliberately.
2. **The rate you are paid is not the rate your cash could earn.** Below $25,000 of average savings balance, idle cash at Rho earns zero. Above it, up to 1.00% as of August 2026 against a 3.81% 13-week T-bill (2026-09-11). The gap is the price of the free software, and it is substantially larger than the software would cost to buy. Concentration only pays if the treasury product is actually used, which requires $50,000 and a willingness to hold securities rather than insured deposits.
3. **Concentration compounds non-price risks.** Rho is not a bank; deposits sit at Webster, a division of Santander, and at ADM's partner network. The counterparty, FDIC-aggregation and account-freeze questions belong to the trust and risk section, but they are the reason a 50%-of-assets test is a governance decision rather than a rate decision.

The honest summary for a finance lead: Rho's software is worth more than $0 and you are paying for it, in basis points, on the balance you agree to keep there. Whether that is a good trade is arithmetic, and it is computable. Multiply your average balance by the spread between Rho's paid rate and the short-term rate, and compare the result to what the incumbent stack would bill you in seats. For a 50-person company running the standard legacy toolset, that incumbent bill is roughly $20,000 to $60,000 in year one. For a company sitting on $5,000,000 of idle cash in checking, the spread is larger than that. For a ten-person company with $300,000 in the bank, it is not.

### 4.11 How this compares

| Company | Interchange | Deposit spread | Software seats | Other named lines |
|---|---|---|---|---|
| Rho | Yes (undisclosed) | Yes (undisclosed) | **None, at any size** | 1% FX; 0.15%-0.60% Treasury; 2.9%+$0.30 invoices |
| Mercury | Yes, self-disclosed | Yes, self-disclosed | Yes (Financial Workflows, Mercury Personal) | FX on international wires; Treasury fees; venture-debt origination and interest |
| Brex | Yes | Yes | $12/user/month Premium; Enterprise custom | FX markup; net interest on charge-card receivables |
| Ramp | Yes | Yes | $15/user/month Plus (plus an undisclosed platform fee); Enterprise custom | Bill pay, FX, procurement add-on |

Mercury's row is quoted from Mercury's own disclosure, which Rho reproduced approvingly on its blog. Brex's and Ramp's seat prices are verbatim from their pricing pages as captured in this research.

**Assessment:** Rho is the most committed to the balance-funded model and the least forthcoming about it. Mercury publishes a six-item list of how it makes money; Rho publishes a list of zeros. Both companies run essentially the same engine. The difference is disclosure, and on that specific axis Rho is behind the competitor it most often writes about.
