## 3. The product surface, one piece at a time

This is the reference section. Every product gets the same treatment: what it is in one sentence, how it actually works, who provides it, what you have to be or have to get it, the limits, the fees, and the one caveat that changes how you should think about it.

Three labels run through this section and the rest of the dossier. **Rho says** marks Rho's own published words, whether from a marketing page, a help-center article, or a contract. **Verified:** marks a claim that was put to an independent checker instructed to refute it, with the checker's corrected wording carried over intact, hedges included. **Assessment:** marks my own conclusion. Unlabeled operational detail (cutoff times, status names, field lists) comes from Rho's help center, which across 269 pages is consistently more precise and more candid than the marketing site.

Everything here was captured from rho.co, its help center, its policy pages, its API docs and its live sandbox on 2026-09-11. Rates, fee schedules and product availability change; dates are attached wherever they matter.

### 3.0 Who actually provides each service

Rho is a software company that sits on top of other people's licenses. It says so on nearly every page: "Rho is a fintech company, not a bank or an FDIC-insured depository institution." That single fact explains most of the structure below, because each product answers to a different provider with a different rulebook.

| Product | Provider, verbatim from Rho | What protects the money |
|---|---|---|
| Business Checking | "Webster Bank, a division of Santander Bank, N.A." Member FDIC | FDIC, $250,000 per entity |
| Business Savings | "American Deposit Management Co. and its partner banks (a network of 400+ FDIC- and NCUA-insured institutions, as of August 2026)" | FDIC via a sweep across many banks |
| Corporate Cards | Issued by Webster Bank "pursuant to a license from Mastercard"; tier is Mastercard World Elite Business | Mastercard network rules |
| Treasury | Adviser: "RBB Treasury LLC dba Rho Treasury, an SEC-registered investment adviser and subsidiary of Rho." Custody: Apex Clearing Corp. and Interactive Brokers LLC | SIPC, $500,000 including $250,000 cash |
| Capital | "Slope is a financial technology company, not a bank. Business-purpose loans made by Lead Bank" | Not applicable, this is borrowing |
| International and FX payments | "International and foreign currency payments services are provided by Wise US Inc." | Not applicable |
| Invoice card acceptance | "Card payments are processed securely through Stripe" | Stripe's terms |
| Incorporation | "Rho Incorporation is not a law firm or accounting firm"; documents "reviewed and signed off by a licensed attorney" (unnamed) | Not applicable |
| Identity and bank-data checks | Plaid, Finicity, Codat | Not applicable |

FDIC insurance, for readers new to US banking, is a federal government guarantee that if a bank fails, depositors get their money back up to $250,000 per depositor per bank. It protects you against the bank failing. It does not protect you against the software company in front of the bank failing, and Rho says this plainly: "It does not protect you against the failure of Rho or other third party."

**Assessment:** note the asymmetry in how openly the providers are named. Webster, ADM, Apex, Interactive Brokers, Mastercard, Wise and Stripe appear in body copy and disclaimers on many pages. Slope and Lead Bank, the two entities that actually underwrite and make the loans, appear once, at the bottom of one page, in a footer that sits below a FAQ answer saying the opposite. See 3.10.

---

### 3.1 Business Checking

**What it is.** A US business checking account held at Webster Bank, with Rho as the entire software experience on top of it.

**How it works.** Onboarding is four steps: gather your EIN (the IRS-issued Employer Identification Number, a company's federal tax ID), formation documents and a government photo ID for every owner holding 25% or more; apply online, which Rho markets as "less than 10 minutes"; wait for manual verification; fund and transact. Every business gets one primary checking account and can create additional sub-accounts ("to organize cash for purposes like payroll or taxes"). The sandbox shows the shape of this: 14 accounts across account types `checking`, `savings`, `credit`, `investment` and `rewards`, with names like "Reserve Checking", "Inventory Checking" and "Treasury Checking". Rho's routing number is 021913655.

Two account features are documented but never marketed. **Virtual Account Numbers** are credit-only receiving numbers: a customer or vendor can push money to them but nothing can be pulled out, which isolates your real account number from anyone you have to hand details to. **Springing DACAs** (Deposit Account Control Agreements, the instrument a lender uses to take control of your operating account if you default) are supported by email request, which matters if you borrow against receivables or inventory.

**Eligibility.** A registered LLC (limited liability company) or corporation. Rho says on /product/business-banking: "Sole proprietorships aren't eligible on Rho." The controlling geographic rule is in the help center: "entities must be incorporated in the United States, and either hold a US Operating Address or have one business owner based in the United States with a valid tax identification number (SSN)." So a non-US founder can bank with Rho if the company is a US entity that meets that address-or-US-owner test. Virtual office addresses "from Regus or any other provider are not permitted." There is a published list of prohibited industries (gambling, adult services, cannabis and pharmacies, quasi-cash and money services, pawn shops, fireworks, online dating and others) prefaced with "such as", so it is illustrative rather than exhaustive. (Quasi-cash is the card industry's term for anything that converts straight back into cash, such as money orders, traveler's cheques or casino chips. It comes back as a cashback exclusion in 3.5.) No minimum opening deposit and no minimum balance.

**Verified:** Rho's own pages contradict each other on entity type and on whether you can open before your EIN arrives. The Terms of Service (v7.0.0, last updated August 27, 2026) are broader than the marketing page, admitting any "business, charitable organization or not-for-profit organization" and barring "individual consumer use", while the Business Savings page says the product is "available to LLCs, corporations, and sole proprietorships that already bank with Rho" and the EIN help article says flatly "You'll need your EIN letter to join Rho." These are not resolvable from published sources and should be flagged rather than silently resolved in Rho's favor.

**Fees.** $0 monthly, $0 minimum balance, $0 domestic ACH, $0 domestic wire, $0 outgoing check. The exceptions are enumerated in 3.4.

**The caveat that matters.** FDIC coverage on checking is $250,000 per entity across *all* your Rho checking accounts, not per sub-account. Opening five sub-accounts gets you five ledgers, not $1.25M of insurance. Rho states this correctly in the help center and states it correctly in the Bill Pay FAQ ("per entity, not per account"), but the headline "up to $75M in FDIC insurance" that appears in the site navigation belongs to a different product, Savings, which you have to open separately.

---

### 3.2 Business Savings

**What it is.** A separate deposit account, funded only from Rho Checking, whose balance is spread across hundreds of partner banks so that no single bank holds more than the $250,000 FDIC limit.

**How it works.** The mechanism is a **sweep network**: an administrator takes one balance from you and places it as many sub-deposits at many different FDIC-insured banks, each under the insurance cap, so the whole balance is covered. Rho's administrator is American Deposit Management (ADM), whose network Rho describes as "400+ FDIC- and NCUA-insured institutions, as of August 2026." Rho's own worked example: "$5 million in Rho Savings: the program spreads it across 20+ institutions, each holding less than $250,000." The underlying instrument, per the published ADM agreement, is the "American Money Market Account (the AMMA)". No account or routing numbers are issued for Savings, and money can only arrive from, and return to, Rho Checking. The benchmark for this mechanism, used throughout this dossier, is IntraFi, the bank-owned network behind the two dominant deposit-placement programs: ICS, or Insured Cash Sweep, for checking-style balances, and CDARS for certificates of deposit. ADM is measured against it below and again in 7.6 and 9.2.

**Getting in.** Marketing says "There is no separate application and no new login." The help center says you click Request Access, after which "A member of the Rho Client Service team will prepare and send you a DocuSign agreement" which goes to the partner for review, possibly with follow-up due-diligence questions. Those two descriptions do not match. The ADM agreement also contains a representation that all clients other than public unit depositors (government bodies: a state, a county, a municipality or similar) "are an 'accredited investor'", a condition Rho never mentions in marketing. Accredited investor is a defined SEC status, not a figure of speech: per the SEC's own capital-raising guidance, a company reaches it by owning investments or holding assets in excess of $5 million, or by being an entity all of whose equity owners are themselves accredited.

**Rate and limits.** Up to 1.00% APY, variable, set monthly (as of August 2026). You need a **$25,000 average monthly balance** to earn anything at all: below that "the balance earns 0% with Rho." Interest accrues daily on a 30/365 convention, meaning every month counts as 30 days, so a year pays 360 days of interest rather than 365 and a nominal 1.00% works out closer to 0.986% (the arithmetic is in 4.3). It posts on the 5th business day of the month. Rho's own example of the return at the threshold: "a year at the full rate works out to roughly $250 before compounding." Transfers in are unlimited. Transfers out are capped at **six per month**.

**Fees.** $0.

**The caveat that matters.**

**Verified:** all four contested provisions appear word for word in the ADM master services agreement that Rho publishes in its own help center. ADM "will use commercially reasonable efforts to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution," subject to the caveat that on a single day "for a limited amount of time (intraday or overnight), the entire amount of the withdrawal or deposit may be held at one Program Institution"; withdrawals are "limited to six (6) per month" and processed "on Tuesdays and Thursdays (Processing Days) for settlement to your designated account on Wednesdays and Fridays"; and "By signing Exhibit A, Client expressly waives extended deposit insurance." Three corrections follow. The published text is not the full agreement: it stops at Section 10, omits the Interest, fee and termination sections it cross-references, does not reproduce Exhibit A, and the $75M figure appears nowhere in the agreement. The effort standard and the intraday transit exposure are standard deposit-sweep language rather than a Rho-specific weakness, matched almost verbatim by Pershing, Altruist, DriveWealth and IntraFi. And the Exhibit A waiver gives up collateralization or a surety bond on excess balances, a feature ADM offers chiefly to public-unit and municipal depositors, which IntraFi's ICS and CDARS do not offer at all, so waiving it leaves a corporate client in the same posture as every mainstream competitor. The one genuinely non-standard term is the twice-weekly withdrawal cadence, since IntraFi's ICS settles every business day with an optional same-day withdrawal. Where ADM is fairly criticized against the industry benchmark is the effort standard itself: IntraFi commits flatly that placements "will not exceed $250,000" and backs that with a reimbursement obligation if its failure leaves funds uninsured, whereas ADM promises only commercially reasonable efforts and offers no equivalent make-whole.

Two further frictions. Rho's own pages give three different settlement times for the same movement (help center: next business day if requested before 1pm ET; the settlement-times table: 2 business days; the marketing page: "within 2 business days typical"), and none of the three matches the Tuesday/Thursday cadence in the published contract. And the list of network banks is not published: "The current list of network institutions is available from Rho support on request."

**Assessment:** the $75M headline is real in the sense that program capacity supports it and Rho footnotes it honestly ("reflecting program capacity on a commercially reasonable efforts basis, not a guarantee"). Treat it as a capacity statement, not a contractual number. The operational cost of the coverage is liquidity: six withdrawals a month, on a cadence the published contract pins to two days a week.

---

### 3.3 Rho Treasury

**What it is.** A brokerage account holding short-term government and corporate debt, managed by Rho's own SEC-registered investment adviser, not a bank account.

**How it works.** You allocate a percentage of a balance across a short menu of assets in 5% increments totaling 100%. Securities are "held directly in your business's name and are not pooled with other clients' assets." Custody is at Apex Clearing for accounts opened after July 2024 and Interactive Brokers before that.

The menu, and the first inconsistency: marketing names three assets ("US Treasury Bills, an ultra-short income fund, and a short-term bond fund"), the help center documents four.

| Ticker | What it is | Suited to | How fast you get out |
|---|---|---|---|
| IJTXX | JPMorgan US Treasury Plus money market fund, offered as a cash sweep, fixed $1.00 NAV | "cash you may need on short notice" | Same business day if by 3:00pm ET |
| T-Bills | 13-week US Treasury Bills, bought in $1,000 increments | "cash you won't need for at least 3 months" | Next business day, cutoff 5:00pm ET |
| MULSX | Morgan Stanley Ultra-Short Income Portfolio (commercial paper, corporate debt, asset-backed) | "4 to 6 months" | 1 to 2 business days, cutoff 4:00pm ET |
| VFSUX / VFSTX | Vanguard Short-Term Investment-Grade Fund, investment-grade corporate bonds | "at least 1 year" | 1 to 2 business days, cutoff 4:00pm ET |

NAV means net asset value, the per-share price of a fund. A fixed $1.00 NAV means the price does not move; a variable NAV means it can. Four other words in that table carry the risk difference. **Commercial paper** is short-term debt issued by large companies, effectively a corporate IOU, and **asset-backed** debt is debt secured on a pool of loans, so both carry a small risk that the borrower does not pay, unlike a Treasury Bill. **Investment-grade** is the ratings agencies' label for the safer band of corporate debt, above the speculative or "junk" band: safer than most corporate borrowing and still not risk-free. And a **cash sweep** here means the fund your uninvested cash sits in by default, which is a different mechanism from the savings sweep network in 3.2. Rho is explicit that VFSUX "carries meaningful NAV variability due to interest rate movements" and warns "Do not allocate near-term operating cash to VFSUX."

Three mechanics are unusual enough to record. **Funding order:** "New funds top up IJTXX first, then go to your other assets." **Rebalancing:** editing a target triggers an immediate rebalance taking 2 to 4 business days during which no changes are allowed, plus an automatic monthly rebalance on the 6th if any holding has drifted more than 5% from target. **Withdrawal:** "We do not split a withdrawal across IJTXX and your other assets, and you cannot select which assets are sold." If your request fits inside the same-day available balance it comes entirely from IJTXX. If it is one dollar larger, the *entire* amount is sold proportionally from T-Bills, MULSX and Vanguard, and IJTXX is left untouched. Shares are sold first-in-first-out.

**Eligibility.** A US-registered business operating primarily in the United States, at least one US-based founder, and at least $50,000 in total deposits. Approval "typically takes up to 2 business days."

**Fees.** An annual management fee billed monthly, calculated daily, tiered on assets under management. AUM here is defined in the help center as "the combined balance of your Rho Checking and Treasury accounts," so your checking balance helps you into a cheaper tier.

| Total AUM | Annual fee |
|---|---|
| $20M+ | 0.15% |
| $10M to $20M | 0.25% |
| $5M to $10M | 0.35% |
| $2M to $5M | 0.45% |
| Under $2M | 0.60% |

If there is not enough cash in the portfolio to pay the fee, "Rho automatically sells a small amount of holdings."

**Protection.** SIPC up to $500,000 per customer including up to $250,000 for cash. SIPC (Securities Investor Protection Corporation) covers the failure of the broker holding your securities, not losses in the market. Rho says this correctly and says this is "not FDIC-insured."

**The caveat that matters: the headline yield.** The published tier matrix on 2026-09-11 showed, at the top ($20M+, 0.15% fee), a net 4.66% on the Vanguard fund, 3.70% on MULSX and 3.66% on T-Bills. "Up to 4.66%" is the top-left cell of that grid, and it appears in the site navigation and in the footer of nearly every Rho page.

**Verified:** on /treasury-yield-comparison, footnote † states that the 4.66% headline "assumes a 100% allocation to the Vanguard Short-Term Investment-Grade Fund (VFSTX)", while /product/treasury says the short-term bond fund is "capped at 50% of your total allocation" and Rho's own help center says "Vanguard allocations are capped at 50% of your portfolio"; under that cap the highest blended net yield available at the top fee tier ($20M+, 0.15%) is 4.18% (50% VFSTX at 4.66% net plus 50% MULSX at 3.70% net), not 4.66%. The cap is not absolute, however: the help center states that pre-existing allocations above 50% remain in place and that a higher limit can be approved on request, so the headline is unreachable under the product's standard allocation rules rather than mathematically impossible. The checker's explicit correction on this point: "'Mathematically unreachable' is too strong... The defensible framing is that the headline is not achievable under the product's standard, self-published allocation rules, and that the cap-compliant ceiling at the top fee tier is 4.18%." Two further exact findings. The minimum discrepancy is real: /treasury-yield-comparison says "$50,000 minimum" in its hero, body and FAQ, while the Minimum row of its own comparison table reads "$100,000" and its bottom tier band reads "$100K-$2M" (the equivalent band on /product/treasury reads "$50K-$2M"). And MULSX is labeled a money market fund on the yield-methodology policy page and on the comparison page, while the help center says "It is not a money market fund - NAV is variable but designed to remain highly stable", which matches the fund's own SEC prospectus. Yields move daily and these pages update automatically; 4.66%, 3.70% and the 4.18% derived ceiling were true on 2026-09-11 and the live page itself showed an internal date mismatch, hero stamped 09/12/2026 and footnote stamped 09/11/2026.

Note also that the asterisk footnote under the same 4.66% figure on /product/treasury says something different again, attributing the yield to "90-day Treasury Bill rates", which is not what that page's own table produces.

**Assessment:** the numbers are all published, the methodology page is dated and specific (T-Bills on a trailing 7-day average, money market funds on 7-day SEC yield, bond funds on 30-day SEC yield, "net of the lowest fee"; the 7-day and 30-day SEC yields are the SEC's standard formulas for stating a fund's recent income as an annual rate after fees, so that two funds can be compared on the same basis), and /treasury-yield-comparison says the uncomfortable part out loud: "the 'up to' number at the top of this page... assumes your entire balance sits in the Vanguard short-term investment-grade bond fund, an allocation we recommend only for cash you won't need for a year or more." Rho even runs a section titled "Where the others win" conceding that Mercury's disclosure is the standard it copied and that Mercury's fund redeems faster. That is unusually honest for a rate page. The problem is that the honest paragraph lives on one page while the unreachable number lives in the navigation bar of every page. The reader should take 4.18% as the realistic ceiling under standard rules at the largest balance tier, and considerably less below $20M.

One more liquidity trap worth knowing: initiating an ACAT transfer (the industry process for moving a brokerage account to another broker) locks the account, and "you will be unable to add or withdraw funds for up to 90 days."

---

### 3.4 The rails: timing, cutoffs, limits and checks

This subsection is the answer to every question a controller asks in the first meeting. All of it is from the help center; almost none of it appears on the marketing site.

**Vocabulary.** **ACH** (Automated Clearing House) is the US batch network that moves payroll, most recurring vendor payments and direct debits; it is cheap, takes a day or more, and can be returned. A **wire** is a same-day, individually processed bank transfer that is effectively irreversible once sent. A **push** is you sending money; a **pull** or **debit** is someone else taking it with your authorization.

**Cutoff times.** Miss these and the money moves a day later.

| Cutoff | Applies to |
|---|---|
| 2:00pm ET | Outgoing ACH (same-day only if also under $1mm) |
| 2:00pm ET | Card repayment ACH pulls; also the general cutoff after which incoming deposits count as next business day |
| 4:45pm ET | Outgoing domestic wires, for same-day arrival |
| 3:00pm ET | Incoming domestic wires, for same-day credit "in most cases" |
| 1:00pm ET | Checking to Savings, and Savings to Checking |
| 3:00pm ET | Treasury withdrawal funded from IJTXX or uninvested cash |
| 5:00pm ET | Treasury T-Bill sale |
| 4:00pm ET | Treasury mutual-fund redemption (MULSX, VFSTX/VFSUX) |
| ~4:00am ET | Release time for all scheduled payments, and therefore the approval deadline |
| 8:00am ET | Daily evaluation of auto-transfer rules |
| just after midnight ET | Daily Terms card auto-repayment debit (Rho's card page writes this one as EST) |
| 12:00pm Central | ADM savings-sweep deposit and withdrawal cutoffs |

**Settlement, outgoing.**

| Payment | Time |
|---|---|
| ACH | Same day if created before 2pm ET and under $1mm; otherwise next day |
| Domestic wire | Same day if created before 4:45pm ET; otherwise next day |
| International wire | 1 to 3 business days, up to 5 |
| Printed check | Up to 8 business days to arrive via USPS |
| Internal transfer, same business | Within 1 hour |
| Internal transfer, different Rho businesses | 1 business day (the internal-transfer page says 2 to 3 hours) |
| Checking to Savings | Same business day if before 1pm ET (settlement table says 2 business days) |
| Checking to Treasury | 2 business days before the asset cutoff, 3 after |
| Card repayment | Up to 4 business days to settle |

**Settlement, incoming.**

| Payment | Time |
|---|---|
| Linked external account transfer | Up to 5 business days |
| ACH | 1 to 3 business days |
| Domestic wire | 1 to 2 business days |
| International wire | 1 to 5 business days |
| Remote check deposit | 2 to 3 business days, "generally up to 6-7 business days" |
| Savings to Checking | 2 business days (savings pages say next business day if before 1pm ET) |
| Treasury to Checking | 2 business days before the asset cutoff, 3 after |

Rho repeats one blanket caveat across these pages: "payments over $1mm could take an extra day to settle."

**Transfer limits.**

| Rail | Limit |
|---|---|
| Outgoing domestic wires | $90 million per day |
| Outgoing international wires | $2.5mm per day |
| Incoming international wires | Up to $10 million per day |
| ACH pulls in | $20 million per day, $10 million per transaction |
| ACH pushes out | $20 million per day aggregate |
| Linked external account transfers | $5 million per transaction |
| Remote check deposit | No limit, but over $15,000 in one business day may trigger extra screening |
| Savings transfers out | 6 per month |
| Card payments on Rho invoices | $10,000 per day across all invoices |

Rho describes the headline limits as raisable: larger wires, ACH transfers and linked-account transfers "can be accommodated, as long as they are communicated to us in advance." The route is always a phone call to your Rho specialist. The Terms of Service reserve the opposite power too: "Rho reserves the right to impose limits on Transactions... at its sole discretion... without prior notice."

**Checks, inbound.** Remote deposit capture only, by phone or web photo. "Rho does not accept check deposits by mail or in person." US checks only, with 9-digit ABA routing numbers (the American Bankers Association number that identifies the bank, printed along the bottom of every US check). Digital-copy checks need an exact endorsement string on the back: "Pay to the order of Webster Bank, a division of Santander Bank, N.A. For Mobile Deposit Only" plus company name, Rho's routing number, the last four of the account, and the date. Five different Rho pages give four different clearing times for the same deposit (3 business days, 2 to 3 business days, 2 to 3 with a 6 to 7 ceiling, and a flat 6 to 7).

**Checks, outbound.** Rho prints and mails them; you never hold check stock. No checkbooks, no cashier's checks, no third-party check printing (explicitly including ADP and Gusto payroll checks), no international checks. The funds mechanic is unusual and good: money is "set aside immediately after you send the payment" but does not leave your account until Rho is told the check was cashed, and the check is drawn on an account separate from yours, so your account details are not on the paper. Uncashed checks "voided automatically" after 90 calendar days. You can staple a PDF to the envelope: 1 file, up to 6 pages, 15 MB, at no cost. USPS tracking appears in the transaction detail after shipment.

**International, via Wise.** Two distinct products: an international wire in USD (SWIFT, no Rho fee) and a foreign-currency transfer (1% FX conversion charge). The recipient-fee toggle is binary: "Cover all recipient delivery fees" ON costs a flat $15 and the business absorbs correspondent and SWIFT charges, OFF means those are deducted from the amount the recipient gets. Rho publishes 22 supported currencies, with GBP marked "SWIFT payments currently unsupported" and PKR marked "payments to businesses currently unsupported." Eight countries are fully restricted (Cuba, Iran, North Korea, Russia, South Sudan, Sudan, Syria, Venezuela) and owners from them are also ineligible for an account. Four currencies (IDR, PHP, INR, MYR) run on local rails rather than SWIFT, so "once the funds leave Rho, we have limited visibility on the payment and cannot provide tracking information." Three of those four are not on Rho's own supported-currency list, so the two pages do not agree. Every international payment is screened individually for sanctions and anti-money-laundering: "Screening happens per payment," most reviews "clear within a few business days", and Rho's stated ceiling on what support can do is "What we can't do is skip or override a compliance requirement."

**Cancellation.** There is a universal 30-minute window after initiating most payments. After that: domestic wires "typically cannot be reversed or recalled"; printed checks can be canceled until deposited, but "past the 30-minute cancellation window, the recipient may still receive the voided physical check in the mail"; and on international wires "Cancelations are most effective if the request comes within the same business day the funds are initiated."

**Fees, the complete published set.** The pricing page's own summary is seven lines, six of which are $0. The seventh is 1% on foreign currency transfers.

**Verified:** Rho's one-line summary, repeated verbatim in 19 corpus files including the help center, is "The only standard payment fee is 1% on foreign-currency transfers," yet the corpus documents at least eleven other priced charges: a $30 wire recall fee (labeled "international" on /pricing but unqualified in the Terms of Service), an optional flat $15 SWIFT charge, "around $20 - $45" deducted for failed and returned domestic wires, a late fee of "three percent (3%) of the delinquent payment balance for each month" for up to six months, a card foreign-transaction fee of "up to 1% of the transaction amount on foreign transactions," 2.9% + $0.30 on card-paid invoices, the $400 Rho Incorporation fee, "platform access after year one is $1,000 annually and contract services run $100 or $250 per contract," a 0.15% to 0.60% annual Rho Treasury management fee, and an unpublished "current hourly rate" for wire-recovery assistance, all on top of an open-ended reservation that "Fees are not limited to the aforementioned list and we reserve our right to charge additional or other fees." Three of these (the $30 recall, the $15 SWIFT fee and the 3% late fee) appear in the asterisk footnote on the pricing page itself, so they are fine print rather than undisclosed. The genuinely buried ones are the $20-$45 failed-wire fee (one help-center article), the 2.9% + $0.30 invoice card fee (absent from /product/invoicing), the up-to-1% card foreign-transaction fee (Terms of Service only), and the $1,000/year platform access plus $100/$250 per-contract charges (one sentence on one page).

**Verified:** the disclosure gap also runs the other way. Rho's help center names only six nonzero fees, and the pricing page affirmatively discloses three of them, while the pricing page meanwhile discloses two fees the help center never mentions at all (the $30 international wire recall fee and the 3%-per-month late fee). The one fee in genuine tension with an affirmative pricing-page line is the $20-$45 failed-wire charge, which sits against the pricing page's "07 Domestic wire recall fee $0".

**Assessment:** Rho's pricing is genuinely cheap for a company that moves money. A business sending domestic ACH, domestic wires and checks pays literally nothing, which is not true at Chase, at BILL, or on most of Ramp's and Relay's paid tiers. The problem is not the level of the fees, it is that the summary sentence is written as an absolute ("the only standard payment fee") when it is not, and that the exceptions are spread across four documents that never cross-reference each other.

---

### 3.5 Corporate Cards

**What it is.** A charge card, meaning the whole balance is settled every period rather than carried at an interest rate, issued to the company by Webster Bank on Mastercard World Elite Business.

**How it works.** Two repayment programs, and you can only be on one at a time.

| | Daily Terms (default) | Monthly Terms |
|---|---|---|
| Repayment | Settled to zero at the end of each business day, debited automatically from Rho Checking "just after midnight EST" for the prior day's settled charges. The Terms of Service add: "There is no grace period." | "A 30-day billing cycle with a 1-day repayment period", auto-repaid from Rho Checking or an external account |
| Spending capacity | A daily limit derived from "your available checking balance as well as risk factors that vary by client... this limit is not a static limit over time" | An underwritten credit limit "personalized based on the business's financial health" |
| Standard cashback | 1.25% | 1% |
| Platinum cashback | 2% | 1.75% |
| How you qualify | Everyone starts here | $25,000 held at Rho (help center), or $75,000 combined across Rho and linked external accounts excluding personal accounts (product page and FAQ), subject to underwriting |

**Cashback, the dense part.** Cashback is Rho's main pull, so the rules deserve precision. The cap is **$1,000,000 in eligible spend per calendar year** across all tiers, applied to spend, not to the cash earned. Rewards must be redeemed "within twelve months of being earned, or they will be forfeited," and "Rho will not provide notifications regarding the impending expiration." Payment is a hard gate: "If you do not pay the full amount due on time, you will not receive any Cashback Rewards for the billing period." Four merchant categories are excluded outright: Walmart and its subsidiaries, utilities merchants, money transfer and quasi-cash merchants, and "transactions made or authorized outside the U.S." Returns claw back proportionally. Until redeemed, rewards "are not your property and do not belong to you." Rho pays cashback into a dedicated rewards account (visible in the API as `account_type: "rewards"`), and redemption to checking is instant.

**Rho Platinum**, the top rate, has four conditions and all four must hold continuously: payroll is run from Rho, business revenue is deposited via Rho Checking, "50% or more of your company's assets are held at Rho", and you have an open Rho Corporate Card. "It isn't a paid plan" and "there's no subscription fee."

**Assessment:** Platinum is the commercial engine of the entire platform. Rho's revenue is interchange (the fee a merchant's bank pays the card issuer on every swipe, typically a fraction of a percent, which is why card issuers can afford to give some of it back), plus the Treasury advisory fee, plus FX, plus deposit economics. All four scale with how much of your company's money lives at Rho. Platinum prices that explicitly: the extra 75 basis points (a basis point is a hundredth of a percentage point, so this is 0.75%) of cashback is what Rho pays to become the system of record for your payroll, your revenue and the majority of your assets. This is a fair trade if you were going to consolidate anyway, and it is a switching cost if you were not.

**Controls.** Limit types are No Limit, Recurring (daily, weekly, monthly, quarterly, annual), Fixed and Single-use; monthly limits reset on the 1st; fixed-limit cards auto-lock once transactions settle; single-use limits cannot be changed after creation. Up to 20 named merchants can be allowlisted per card, plus category controls by Mastercard merchant category code (the four-digit code that classifies what kind of business a merchant is). International spend is ON by default. Cards expire 3 years from issue. Apple Wallet and Google Wallet are supported, WeChat is not. Card statements issue on the 5th. One constraint is repeated on three separate pages because it confuses people: "Changing a user or card limit does not increase your available balance."

**Fees.** $0 annual, $0 subscription, $0 per card, unlimited cards. Late payments carry the 3%-per-month fee and forfeit that period's rewards.

**The caveat that matters.**

**Verified:** Rho markets corporate cards as "No personal guarantee, no personal credit check, no annual fee" (rho.co/product/corporate-cards), and its Terms of Service (last updated August 27, 2026) do contain an FCRA consumer-report consent, but the two halves of the marketing line are not equally in tension. The no-personal-guarantee half is not contradicted: the ToS contains no personal liability or personal guarantee clause, card "Obligations" are defined as amounts "payable by the Company," and the Section 17 Cross Guaranty is an entity-level Affiliate guaranty of parent and subsidiary entities, not a founder guarantee. The credit-report half is contradicted. There are two consents, one in each card addendum, and they are not identically scoped: both authorize Rho to obtain "a consumer report as defined in the Federal Fair Credit Reporting Act..." but the Daily Terms version obtains it "about the Company and each authorized user," while the Monthly Terms version reads "about you and each authorized user," the individual rather than the entity. Both carry the same standing grant that "we may obtain a consumer report on you" "now, or at any time while in agreement with us." That reserved right cannot both be true, as written, alongside Rho's absolute marketing statements: "no consumer credit report, no personal credit score pull" on the cards comparison table, and "Rho will not conduct a hard or soft check on your credit score when you apply for credit with Rho" in the help center. The checker's own hedge is the important part: "This is a reserved contractual right, not evidence that Rho actually pulls consumer reports," and "A reserved right is not an observed practice... The defensible finding is a documented contradiction between absolute marketing language and a live contractual reservation, not proof that personal credit is being pulled." Rho's separate statement that it does not furnish card activity to personal bureaus is consistent with the ToS, which mentions reporting delinquencies only to "any business credit bureau."

A second contract clause belongs here for completeness and for fairness. Section 1.6 of both card addenda says that "if we issue at least ten (10) Cards to you and your Users, you will be liable for all unauthorized use of all Cards." **Verified:** this is "a restatement of the federal safe harbor at Regulation Z, 12 C.F.R. 1026.12(b)(5), implementing TILA section 135, not a Rho invention" (TILA is the Truth in Lending Act, and the C.F.R., the Code of Federal Regulations, is where federal agency rules are published), it ends the moment Rho receives notice of suspected unauthorized use, and "Brex's card agreement carries the equivalent clause." It is worth knowing; it is not a Rho-specific trap.

One last mismatch: the cards page advertises cashback with "no category restrictions" on the same page as the footnote excluding Walmart, utilities, quasi-cash and every non-US transaction.

---

### 3.6 Vendor Cards

**What it is.** Not a separate product: a card type inside the corporate card program, scoped to a single vendor, with its own tab under Cards.

**How it works.** You generate a card for a named vendor, with logo and name pre-matched. Card details can be shared with the vendor in one click via a secure link that "expires in 72 hours". Limits and merchant rules apply per vendor. A "Subscription Switch" flow replaces payment details during checkout to migrate an existing subscription. Cards default to the creator as cardholder "so they stay working even when team members churn." Vendor cards can be created individually, from the Vendors module, or by bulk CSV upload that auto-creates missing vendors.

There is a second variant, the **single-use AP card**, used as a Bill Pay payment method: nicknamed "[Payee Name] AP Card: [Invoice Number]", pre-set to the payment amount, chargeable exactly once, with a 14-day usage window. After the charge it flips from Active to Canceled and stays visible for audit.

**Eligibility, limits, fees.** Included with every Rho account, unlimited, no fee. Two caveats undercut the pitch. The help center says "Vendor cards are currently a web-only feature, so they won't appear in the mobile app," while the changelog records vendor-card management shipping on mobile in March and again in May 2026; one of the two is stale. And the lifecycle rules contradict the churn-proofing claim directly: "If the user who created a Vendor Card is removed, you will be prompted to delete the card. Similarly, if a Vendor profile is deleted, all linked Vendor Cards will be canceled."

---

### 3.7 Expense Management

**What it is.** The software wrapped around the card program: controls before the spend, receipts and coding after it, approvals in between, and reimbursements for money staff spent out of pocket.

**How it works.** There are two distinct enforcement layers and the distinction is the single most important thing to understand here.

- **Card controls** are pre-spend and real. A limit or a blocked merchant category causes a decline at the terminal.
- **Expense rules** are post-spend. The help center says it flatly: "these are post-spend controls, meaning Expense rules will not cause Rho Cards to get declined." They require information (receipt, note, attendees, client ID, department, label) and can mark a transaction out of policy after the fact.

Rules can key on all expenses, an amount threshold, a department, a merchant category, or a custom combination. Approvals are a separate system keyed on dollar amount, with direct-manager routing available and tiers that are **immutable once created** ("To make changes, you can create a new tier and delete the old one"). Two Rho help pages give conflicting worked examples of the standard ladder, disagreeing on whether the middle tier is $500 or $1,000.

**Receipts** arrive by five routes: web upload, forwarding to receipts@rho.co, SMS to short code 555746 (US and Canada mobile numbers only), a photo in the mobile app, and the Gmail Connector (3.15). Matching was rebuilt in April 2026 with "merchant identity verification... so a receipt from Uber only ever attaches to an Uber transaction."

**Reimbursements** are paid straight out of Rho Checking after direct-manager approval, by ACH, "for domestic bank accounts only." Mileage uses the current IRS rate, pre-populated at $0.70 per mile, overridable with a company rate, with an embedded map computing distance, and calculated at "the rate your business set when the expense occurred."

**Coding and sync.** Departments, Labels, Fields and Custom Attributes all attach to transactions. Mapping rules resolve in a fixed priority order: Label, then Sender, Vendor, Merchant, Card, Department. Native accounting integrations are QuickBooks Online, NetSuite, Sage Intacct and Puzzle; Xero "connects today through a bank feed rather than a native sync," though the same marketing FAQ lists Xero as a direct integration in a different answer.

**Fees.** $0 per user, $0 platform, on every account.

**The caveat that matters.** Uploaded policy documents are storage and distribution only. Nothing in the corpus describes Rho parsing a policy PDF into enforceable rules; you still write each rule by hand.

**Verified:** a related taxonomy problem is real and undisclosed. "Understanding Fields in Rho" states "Your account does not include a Reporting tab. That tab houses the Departments and Labels pages used by longer-tenured accounts," no Departments article acknowledges Fields, and nothing in the corpus carries a migration, deprecation or sunset notice. But the checker's correction matters: "they are not equivalent models: Departments carry budgets, reset cadences and user membership while Fields 'apply to money movement, not to users,' and a third taxonomy, Custom Attributes capped at five, is separately documented." So newer accounts and older accounts are running different spend-tagging models with no published migration path between them.

---

### 3.8 Bill Pay (AP)

**What it is.** Accounts payable automation, meaning the workflow of receiving supplier invoices, approving them and paying them, bundled free into the checking account.

**How it works.** Four steps as marketed. Forward the invoice to a dedicated Rho inbox, "no login required." OCR (optical character recognition, software that reads the invoice image into structured fields) drafts a bill, with a Green/Yellow/Red confidence score on the bills table and automatic duplicate flagging. Route for approval. Pay and sync.

**Scheduling has three hard failure modes**, all documented on one page and all worth memorizing. Scheduled payments release at approximately **4:00am ET** on the payment date. Approvals must clear **before** that release or the payment does not go. A payment scheduled for the same day will not release and will not roll forward: it simply shows as overdue. And a Bill Pay payment dated on a Saturday or Sunday will not send. To pay in real time you use Make A Payment and choose Send Now.

**Approvals** are amount-threshold only: "For X amount or above, X number of approvals are required," with multiple tiers and self-approval counting as the first layer. There is no documented routing by vendor, department, GL account or entity for bill payments. Rho concedes the gap in its own FAQ: "A dedicated AP tool can make sense if your team needs deeper approval-policy customization than a banking-included tool offers."

**Bulk payments** run from a CSV template, one line per payment with no merging, for checks, ACH, domestic wires and single-use cards. Vendors must already exist. Bookkeepers can import a CSV and "make edits to payment drafts", but "By default, Bookkeepers cannot execute payments from the Bulk Payments workflow."

**The caveat that matters: which rails Bill Pay actually supports.**

**Verified:** rho.co/product/bill-pay (re-fetched live 2026-09-11) is written as a check-only product, with step 04 reading "Once approved, pay by check," the comparison row "Domestic per-payment fees $0 on checks," the hero stat "$0 On domestic check payments," and the guide text "it captures invoices automatically, routes them for approval, and pays vendors by check," while Rho's own help center states "You can make Bill Pay payments using the following methods: ACH transfers; Wire transfers (domestic and international); Checks; Single-use cards," so the page understates three of the four documented rails. Two qualifications attach. Bill Pay's international wires are USD-only per the help center: non-USD bills must be paid from the Banking tab and then marked "Paid Externally" in Bill Pay, and bulk payments support domestic wires only. And the help center is not internally consistent either: a vendors article says "Paying a bill through the Bill Pay workflow does not currently support Vendor Cards," which directly contradicts two other help articles describing Single-Use Card as a Bill Pay payment method. Cite the contradiction as marketing-versus-help-center plus a help-center-versus-help-center conflict, not as a clean single source of truth.

**Assessment:** this is a marketing defect, not a product defect, and it cuts against Rho. The product is better than the page says. Someone comparison-shopping AP tools on the product page alone would conclude Rho mails paper checks and nothing else, and would rule it out.

**What Bill Pay genuinely does not do.** No three-way match (the standard AP control that reconciles a purchase order, the vendor invoice and the goods-received record before paying). No purchase order object exists anywhere in the corpus. "It does not include procurement or supply-chain management," stated twice. And no AI auto-approval: "not an AI system that approves payments on its own."

**Fees.** $0 software, $0 per user, $0 per domestic payment on every rail. Vendor management includes W-9 collection (the IRS form that captures a contractor's tax details) and 1099 filing support (the year-end form reporting what you paid them).

---

### 3.9 Invoicing (AR)

**What it is.** Accounts receivable, meaning billing your own customers and collecting from them, built into the checking account at no charge.

**How it works.** Create an invoice with customer, dates, payment terms (Net 30, meaning due 30 days after the invoice date, or Due on receipt), line items and auto-calculated tax and discount. Send it by email from Rho; each carries a branded payment portal with your logo and colors. "Your customer pays by ACH, domestic wire, international wire, or check through a secure payment portal. No Rho account needed on their end." When payment lands, it auto-matches to the invoice. Recurring billing supports weekly, monthly, quarterly and annual cadences. A virtual account number can be activated per the March 2026 changelog "to minimize risk from unauthorized debits."

The API confirms the object model precisely. Invoice statuses are `unpaid`, `pending_payout`, `confirm_payment`, `paid`, `overdue`, `cancelled`; externally-recorded payment methods are `cash`, `check`, `credit_card`, `other`, `received_in_account`; accounting sync states are `not_pushed`, `synced`, `error`, `skip`, `object_changed`. The sandbox carries 7 invoicing customers and 12 invoices.

**Card acceptance is the part with real money attached.** It runs through Stripe, and Rho creates and manages the Stripe account for you: "you can't connect an existing Stripe account," and payout details cannot be changed on the Stripe side. The fee is **2.9% + $0.30 per transaction, paid by your business**, and "surcharging is not currently available," so you cannot pass it to the payer. There is a **$10,000 per day cap across all invoices**; once hit, the card option disappears until it resets. Card payments work only for one-time, full-amount, USD invoices: partials, overpayments, recurring invoices and non-USD invoices must go by bank transfer. The first payout "may take up to two weeks while Stripe completes its initial review."

**Timeline.** Beta March 25, 2026. Payment portal and recurring invoices June 30, 2026. Card acceptance and QuickBooks sync August 31, 2026.

**The caveat that matters: the product page describes an older product than the one that shipped.**

**Verified:** the live page's line "Rho Invoicing does not yet sync with accounting software like QuickBooks or Xero, and there is no mobile app" is stale only on the QuickBooks clause, and the contradicting changelog entry "Rho invoices now sync to QuickBooks" is dated August 31, 2026, eleven days before capture, not months. The Xero exclusion is still accurate because the help center says invoice syncing is "Available for QuickBooks Online only." No changelog entry ships invoicing in the mobile app, so the "there is no mobile app" clause is not contradicted by anything in the corpus; the checker calls this "poorly worded (Rho has a mobile app; invoicing is apparently just not in it), which is an editing problem rather than a factual contradiction." The staleness is broader than one page: Rho's blog post on invoicing tools also still says "No direct accounting-software sync yet."

Two smaller tells. The 2.9% + $0.30 card fee "is not mentioned on the product page at all." And Rho's own competitor table on that page leaves its own cells blank, reading "Not shown" for recurring invoices and for payment matching, the exact two features the body copy of the same page claims to have. The footnote is also unusually defensive: "Rho does not guarantee that any payment will be initiated, authorized, completed, or settled, or that any payment will be automatically matched to a particular invoice."

**Assessment:** invoicing is six months old and reads like it. It is genuinely free and genuinely integrated with the bank account, which is more than Stripe (0.4% to 0.5% per paid invoice) or QuickBooks (free plan capped at 2 invoices per month) offer. But the documentation, the fee disclosure and the marketing page are out of sync with the shipped product in three separate directions at once.

---

### 3.10 Rho Capital

**What it is.** A revolving line of credit against your business's cash flow, drawn and repaid inside the Rho account. Rho frames it against the alternatives: "not a term loan or a venture debt facility" and "not a merchant cash advance: no daily withdrawals and no cut of your revenue."

**How it works.** Apply from inside the Rho account with EIN, formation documents, ownership information and "a look at recent cash flow." Underwriting is described as cash-flow based rather than credit-score based, "built for businesses with lumpy revenue or a thin credit file." On approval the line appears alongside the existing account, with no separate login. Draw, repay, redraw.

**Terms.** Up to $5M ("larger facilities considered case by case"). Funds land "in as little as 24-48 hours after approval." Up to 180 days per draw. $0 origination fee, $0 prepayment penalty.

**Eligibility.** No published revenue floor and no published age-in-business floor. Rho says "Startups that only have an EIN and no trading history yet are a common case, not an edge case." But the lender's disclaimer on the same page says the facility is "Subject to minimum revenue and business requirements," and "Personal Guaranty may be required." Note the asymmetry with the corporate card, where no personal guarantee is required at all.

**The caveat that matters: who lends, and what it costs.** Two pricing words appear below and Rho publishes neither. An **APR** (annual percentage rate) is the all-in yearly cost of borrowing stated as a percentage. A **factor rate** is the flat multiple of the amount borrowed that cash-advance lenders charge instead of interest.

**Verified:** on rho.co/product/capital (verified live 2026-09-11), Rho's FAQ asks "Is Rho a direct lender for its working capital line of credit?" and answers "Yes", while the same page's main pricing copy states that fees "are set when Slope underwrites your line", its disclosure blocks state "Rho is a fintech, not a bank. Financing offered by third parties. Rho Capital is not a broker-dealer. It does not participate in the negotiation or execution of any transactions between customers and third-party financing sources", and its site footer states "Slope is a financial technology company, not a bank. Business-purpose loans made by Lead Bank and subject to credit approval." Only the Lead Bank sentence is footer fine print: the Slope-underwrites sentence sits in the body pricing section and "Financing offered by third parties" appears in the hero and again in the end-of-content disclosure. No interest rate, APR, factor rate, or price range for Rho Capital is published on any Rho page located, including four Capital-related URLs present in the sitemap but absent from the local crawl, which were fetched live and checked; the only Capital prices Rho publishes are $0 origination fee and $0 prepayment penalty. Note also that Rho's own copy is internally inconsistent on who underwrites: the help center says "Cash-flow underwriting: Rho evaluates your real business transaction data", so "not underwritten by Rho" rests on Rho's single explicit naming of Slope rather than on a consistent disclosure. Two fairness notes from the checker: the FAQ's full question is "Is Rho a direct lender for its working capital line of credit?" and the "Yes" is followed by a justification about product experience (the line lives in your Rho account), which is how Rho would likely defend it; and the live /blog/rho-capital announcement says "Draw up to $2M in revolving working capital" in its Highlights while its own FAQ and /product/capital both say up to $5M.

**Assessment:** Capital is the least finished product on the platform and the one where the gap between the marketing voice and the legal voice is widest. There is no help-center category for it (one article, filed under general information), no published rate, APR, factor rate or price range of any kind, the only Capital prices Rho publishes being $0 origination and $0 prepayment, and the personal-guaranty and minimum-revenue conditions appear only in the lender's disclaimer. A buyer cannot compare this to a competing facility without applying. That is normal for underwritten credit and abnormal for a company whose entire brand is "$0 fees, published on the page."

---

### 3.11 Rho Close

**What it is.** A suggestion engine that proposes accounting codes for your card and bank transactions, so month-end coding is a review pass rather than data entry.

**How it works.** It learns from "your chart of accounts, your vendor history, and every coding decision you've made on Rho... not a generic model trained on someone else's books." Your chart of accounts is the list of categories a company books every transaction into, so it is the thing that decides what a suggestion can say. You trigger it from the Accounting Dashboard with a "Suggest coding" button; it fills **empty** accounting attributes only, on card and banking transactions in the current view. It does not create or modify mapping rules, and it does not touch attributes you have already set. You accept or dismiss in bulk, per row, or per individual attribute. It is enabled by default.

**Eligibility.** "Rho Close requires a native accounting integration. If you're currently exporting CSVs, you'll need to connect a supported integration." The two published lists of supported integrations do not match: the marketing FAQ says QuickBooks Online, Oracle NetSuite and Sage Intacct natively plus Xero via bank feed; the help center says QuickBooks, NetSuite, Puzzle or Sage Intacct. Puzzle appears in one, Xero in the other.

**Fees.** Included.

**The caveat that matters.** The marketing line is "Nothing syncs until you approve it. Every time." The help center qualifies it: "If you do sync an individual transaction without actively accepting or dismissing the suggestions, those suggestions will be applied to the sync." So the approval gate is on the sync action, not on each suggestion. Combined with the feature being on by default, the practical default is that unreviewed machine-generated codes reach your general ledger unless you actively dismiss them. Launched May 27, 2026 (announcement published May 06, 2026, updated September 01, 2026). There is no published accuracy figure, no benchmark and no AI-error disclaimer anywhere on the page.

---

### 3.12 Incorporation

**What it is.** Delaware C-corporation formation (the standard US company type that venture investors expect, owned by shareholders and able to issue multiple classes of stock) filed by Rho, reviewed by a licensed attorney, with the Rho bank account application running in the same flow. Launched August 31, 2026.

**How it works.** A questionnaire (company name, share structure, founder details), of which Rho says "Most founders finish the flow in about 5 minutes." Rho files the certificate of incorporation with Delaware first, then prepares and submits your SS-4, the IRS form that requests an EIN. The Rho account application rides along. "Funds move once the IRS issues your EIN."

**Price.** $400 flat, including Delaware state filing fees and year-one registered agent service (a registered agent is the in-state address legally required to receive official mail and legal service for the company). It is credited back if you deposit $10,000 of new money and maintain a daily average balance $10,000 above the pre-deposit balance for 60 days, with the credit posted within 30 days after that window. The offer terms specify "Substituting or reallocating pre-existing funds will not satisfy this account balance requirement." The help center adds a variant absent from marketing: "$1,000 for founders introduced through an accelerator."

The part that is easy to miss: "platform access after year one is $1,000 annually and contract services run $100 or $250 per contract. Delaware franchise taxes apply separately and on an ongoing basis." That $1,000 per year appears in exactly one sentence, on one page, and appears in no pricing page, no help-center article and no llms.txt summary.

**Timing, hedged carefully by Rho itself.** "Filing time measures Delaware state filing only, starting the next business day after you submit your information; it does not measure EIN issuance or account approval. About 80% of filings complete within 24 hours; Delaware processing backlogs can extend this window." The EIN runs on IRS time, "typically within 2 to 4 weeks."

**Eligibility.** At least one owner or officer must be US-based with a physical US operating address. Delaware C-corps only: "Does Rho support LLC formation? Not yet."

**The caveat that matters: what a pre-EIN account actually buys you.**

**Verified:** the pre-EIN figures are quoted correctly and verbatim from rho.co/product/incorporation ("Non-VC-backed founders get a 30-day pre-EIN window before the EIN arrives; VC-backed founders get 60 days. Both require manual review, and neither is guaranteed"), but "pre-EIN account opening" overstates what is unlocked: "Funds cannot move until the IRS issues your EIN and it attaches to your account," and an uploaded SS-4 "lets you start depositing" while "the EIN itself unlocks outgoing transfers." What day one buys is a deposit-only account. The 30/60 split "appears exactly once in the entire corpus," in a FAQ answer on /product/incorporation, "and appears on no help-center page and in no Terms document," so it "is verified live as of 2026-09-11 but is thinly sourced and unilaterally changeable; do not present it as a contractual commitment." Nor is pre-EIN onboarding a Rho differentiator: Rho's own comparison page describes its path as working "through incorporation integrations" (Rho, Stripe Atlas, Clerky), and Mercury offers the same thing through the same Stripe Atlas and Clerky partnerships.

**Assessment:** at $400 including filing fees and year-one agent, credited back on a deposit most funded startups would make anyway, this is the cheapest all-in price in its set once Delaware's filing fee and a year of registered agent service are counted. It is not the cheapest headline: LegalZoom's $149 starting price is lower, but it excludes both, and Rho's own table puts LegalZoom's registered agent at "$249 per year, auto-renews", which by itself carries a first year to $398 before Delaware has charged anything for the filing. Note whose numbers those are. Stripe Atlas at $500, Clerky at $427 to $819 and LegalZoom from $149 plus filing fees billed separately are Rho's own comparison figures, which Rho says it collected from those vendors' websites "as of 2026-09-07, and may change", and which were not independently re-checked against the vendors here. The $1,000 annual platform fee after year one, disclosed once, is what turns that comparison around for a company that stays incorporated for five years, and it is the single sharpest exception to Rho's "every fee on this page is $0" positioning.

---

### 3.13 The Partner Portal for accountants

**What it is.** A separate view of Rho built for accounting firms and fractional CFOs who manage many client companies at once. Rho calls it "A new version of Rho built for world-class accounting partners."

**How it works.** The marketed capabilities are multi-client oversight ("Manage all of your clients in a single platform", "Get an all-up view of each of your clients' finances"), mapping rules that auto-assign accounting attributes, multi-entity management, and per-client customizable permissions with unique logins and two-factor authentication. The concrete evidence in the help center is a role set: Partner Admin, Partner Expense & AP Manager, Partner Accountant, External Admin and External Accountant.

**The partner program**, which is distinct from the portal, lists seven benefits: client referral reciprocity, the oversight dashboard, "custom incentives and preferred rates for your firm and clients," being featured as a preferred accounting partner, "access to in-house CPAs ready to assist our firm partners", cashback eligibility, and co-marketing.

**Eligibility and fees.** Apply or schedule a demo. There is no self-serve signup path documented. No fee is stated; the page's comparison table asserts "Fees / None" against Brex at "$12/mo" and Ramp at "$15/mo" per user (competitor figures stamped 08/02/2026), and claims "Dedicated Support / Yes" against "Enterprise only" for both.

**The caveat that matters.** **Assessment:** across the 253 help-center articles there is no Partner Portal category and no setup article. What is documented is a set of roles inside the normal Rho application, not a distinct product with its own documentation surface. The page itself is a demo-capture page with no pricing block, no FAQ and no footnotes. Treat "a new version of Rho" as marketing language for a permissions model and a client-list view until you have seen it demonstrated.

---

### 3.14 The mobile app

**What it is.** An iOS and Android companion to the web application, free, with a redesigned home screen shipped August 31, 2026 showing "Total cash across all accounts, money in versus out, spend trend."

**What it does.** Balances and transfer review; remote check deposit; create a card; lock, unlock and cancel cards; view card details and share them via the 72-hour secure link; view and edit card controls including all five recurring limit types; upload receipts by camera roll, camera or file; code accounting attributes on transactions; review expenses; approve Bill Pay payments (Approvals tab, AP Payments, with the final approver seeing "Approve & Schedule"); Treasury transfers in and out; reimbursements; switch between businesses; contact support; find your routing and account numbers, including virtual account numbers.

**What it does not do.** No password reset ("The Rho mobile app does not support the password-reset flow"). No accounting sync, mapping rules or accounting settings. No multi-transaction disputes. Vendor cards, per the help center, though the changelog disagrees (see 3.6). And no invoicing, which is what Rho's own invoicing page is clumsily pointing at when it says "there is no mobile app."

**Assessment:** the mobile app is a genuine second surface, not a balance viewer. Approving bills and depositing checks from a phone is the real test and it passes. The gaps are all on the accountant's side of the product, which is a defensible place to put them.

---

### 3.15 The Slack app and the Gmail connector

These are the two places Rho appears inside software you already use. Both are read-only, and understanding that is the whole point.

**Rho for Slack.** Included at no cost. Two layers of authorization: a Rho Admin links one Slack workspace to one Rho business once, then each person separately ties their Slack identity to their Rho login via "Sign in with Rho". If the Slack admin and the Rho admin are different people, "the app generates a hand-off link."

Five slash commands: `/rho-accounts` for balances, `/rho-transactions` for recent activity, `/rho-help`, `/rho-feedback`, and `/rho signin` / `/rho-signout`. "Command replies are visible only to you, even in a channel." A home tab carries balances, alert settings and connection status. Alerts include a daily balance pulse ("Cash balances, yield earned, and a heads-up before payroll leaves") and real-time inflow, outflow and card activity above a configurable dollar threshold, delivered to **one** configured private channel and/or DMs: "Rho won't post alerts to multiple channels."

An **agent chat is in beta for select businesses**: DM the app or mention it in a private channel and it answers questions using live Rho data across balances, transactions, statements and spend by vendor, category or person. "Every answer names its sources." Statement download links work for about 15 minutes. It is explicitly read-only: "it can look things up but never move money."

Three constraints. Private channels only: "If it is invited to [a public channel], it says so and removes itself." No money movement: "Can I approve payments from Slack? Not yet. Today's release is visibility and answers." And a permissions mismatch, where marketing says "Your Rho permissions carry over" while the help center says the app "is available to Account Owners and Admins today, with support for more roles on the way."

**The Gmail connector**, shipped April 30, 2026. Each team member connects their own Gmail or Google Workspace inbox; the connector scans for receipts matching keyword and merchant-sender criteria and auto-attaches them to that person's matching card transactions. The single most important operational fact: "The Gmail Connector captures receipts from the point of connection forward." There is no backfill, so everything before the connection date still has to be uploaded by hand. It may need "Permission from your Gmail admin if your organization restricts third-party app access (Google Workspace customers only)", so the admin gate is scoped to Workspace, not to a personal Gmail account. Rho's privacy claim is narrow and specific: "Receipts, and only receipts. The connector scans subject lines and attachments that look like purchase confirmations", and "nothing else is read, stored, or touched," and "No inbox data is retained after disconnection." Asked when more connectors arrive, Rho says only "In the pipeline. We will share timing when it is confirmed."

**Assessment:** both surfaces are useful and both are honest about their ceiling. The Slack agent is the more interesting of the two because it is the only conversational surface where Rho has shipped anything, and it is deliberately scoped to reading. See the API and MCP section for why that read-only posture is a strategy rather than an accident.

---

### 3.16 The support model

**Rho says:** "When you contact Rho support, you reach a real human", and that human is there "24/7, on every account, at no cost. No phone trees, no paywalled support tiers." The published channels are phone (1-855-743-8746, spelled 1-855-7-GETRHO), email (clientservice@rho.co), and live chat inside the web and mobile apps, with iMessage and WhatsApp added in June 2026. "Every channel is staffed around the clock, every day of the year." On the accountants page the claim escalates: "Dedicated relationship managers are on-call for you and your clients 24/7."

**Verified:** one card help page still contradicts the 24/7 claim, saying live support runs "Monday through Friday from 8am ET to 8pm ET." That is one stale page against a dedicated support article and repeated marketing, so read it as a documentation defect rather than evidence the 24/7 claim is false.

**Assessment: support is not a nicety at Rho, it is load-bearing product infrastructure, and that cuts both ways.** Of 253 help-center articles, 57 (22.5%) route the reader to Client Service. Roughly two dozen actions have no self-serve path at all:

| Action | Why it needs a human |
|---|---|
| Raise any transfer limit | "contact your Rho Specialist at 855-7-GETRHO" |
| Open a Savings account | Request Access, then a DocuSign prepared by Client Service |
| Recall, reverse or dispute a settled bank transfer | Not self-serve at all |
| Get the list of Savings sweep network banks | "available from Rho support on request" |
| Exceed the Treasury Vanguard 50% cap | "unless we have approved a higher limit for your account" |
| Close or liquidate Treasury | "by contacting Rho" |
| Raise the $10,000/day invoice card limit, or refund a card payment | "contact Rho Client Service" |
| Set up a DACA, FedWire drawdown, or micro-deposit linking | Email only |
| Set up a Mastercard Smart Data card feed | Email, 3 to 5 business days |
| Bulk upload vendors | Rho staff do it, 1 to 2 business days |
| Change your phone number (which is your 2FA factor) or business address | Email with a written reason |
| Close your Rho account | Account Owner must call, chat or email |
| Authorize a third-party API integration | Forward to api-partner-request@rho.co |

If the support promise is real, this is a coherent design: a self-serve product for the common path and a human for everything unusual, which for a company whose customers are below $1M of ARR (annual recurring revenue) is cheaper than building the settings screens. If the support promise ever degrades, a quarter of the product becomes inaccessible. Rho also publishes no uptime figure and no SLA anywhere in the corpus. Its status page at status.rho.co (see section 2) has posted no incident since September 2023 and nothing of any kind since September 2024, so it gives a prospective customer no usable availability signal, which for a platform that holds operating cash is a real omission.

---

### 3.17 Capability matrix

"Included free" means no incremental charge beyond having a Rho account. "Maturity" is my own read: **mature** means documented in depth with help-center coverage and no launch date in 2026; **new** means shipped in 2026 with thin or inconsistent documentation; **beta** means Rho labels it so; **announced** means Rho has said it is coming and it is not here.

| Product | Included free? | Gates on | Maturity |
|---|---|---|---|
| Business Checking | Yes | US LLC or corporation; EIN or pending SS-4; US address or US owner with SSN | Mature |
| Business Savings | Yes ($0 fee) | Existing Rho Checking; DocuSign via Client Service; $25,000 avg balance to earn interest | Mature |
| Rho Treasury | No: 0.15% to 0.60% of AUM per year | $50,000 in total deposits (its own tier matrix says $100,000); US business; one US founder | Mature; Apex Ascend migration in progress |
| Corporate Cards (Daily Terms) | Yes | Open Rho account with EIN | Mature |
| Card Monthly Terms | Yes | $25,000 at Rho, or $75,000 combined with linked external accounts, plus underwriting | Mature |
| Rho Platinum cashback tier | Yes | All four: payroll on Rho, revenue into Rho, 50%+ of assets at Rho, open card | Mature |
| Vendor Cards | Yes, unlimited | Corporate card program; web only per help center | Mature |
| Expense Management | Yes | Open Rho account | Mature |
| Gmail connector | Yes | Per-user Gmail/Workspace consent; possibly Gmail admin approval | New (April 30, 2026) |
| Bill Pay (AP) | Yes | Open Rho Checking; not sold standalone | Mature |
| Invoicing (AR) | Yes, except 2.9% + $0.30 on card payments | Open Rho Checking; card acceptance gates on Stripe approval | New (beta March 2026; card + QuickBooks Online sync August 31, 2026) |
| Rho Capital | Price not published; $0 origination, $0 prepayment | Underwriting by Slope; unpublished minimum revenue; personal guaranty may be required | New (2026) |
| Rho Close | Yes | A native accounting integration (CSV export is not enough) | New (May 2026) |
| Incorporation | No: $400 creditable, then $1,000/yr after year one | Delaware C-corp only; one US-based owner or officer | New (August 31, 2026) |
| Partner Portal | Yes | Accounting-firm application or demo; no self-serve path | Mature but thinly documented |
| Mobile app | Yes | A Rho login | Mature |
| Rho for Slack | Yes | Slack workspace admin plus Rho Owner/Admin; Owners and Admins only today | New (2026) |
| Slack agent chat | Yes | Request access; "select Rho businesses" | Beta |
| ACH debit authorizations | Yes | Request access from Client Service | Beta |
| Rho API and MCP server | Yes | Owner or Admin creates a token; read-only, 14 GET operations, 5 scopes | New (changelog 2026-08-03) |
| SAFE note generator (a SAFE, Simple Agreement for Future Equity, is the standard short contract early startups use to take investment before setting a valuation) | Yes, free tool | None stated | Marketing tool, not a banking product |

Announced and not shipped as of 2026-09-11: LLC formation ("Not yet... coming soon"), write access and webhooks on the API ("Read-only is live today. Write access and webhooks are next"), payment approvals from Slack ("Not yet"), invoice sync for non-QuickBooks platforms ("on the roadmap"), syncing unpaid invoices ("currently in development"), Fields-native reporting views ("on the roadmap"), and additional receipt connectors beyond Gmail ("In the pipeline"). Three-way match in Bill Pay is listed by Rho's own blog as "Not yet available" with no roadmap commitment attached.
