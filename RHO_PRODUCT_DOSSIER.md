# Rho: An End-to-End Product Dossier

**Unofficial.** Compiled 2026-09-11. Rho is a US business banking and finance platform at https://www.rho.co.

This document exists to take someone who knows nothing about business banking and give them a working
command of what Rho is, how it makes money, who it is for, how it compares to its 2026 competitors, and
what to check before trusting it with a company's cash. It is written to be argued with, not believed.

---

## The short version

If you read nothing else, read this. Each line points at the section that argues it.

| | Finding |
| --- | --- |
| **What it is** | A single platform that bundles a business bank account, corporate cards, bill payment, invoicing, expense management and a treasury product, and charges nothing for the software. (§1) |
| **It is not a bank** | Rho is a software company in front of other people's balance sheets. Deposits sit at Webster Bank, a division of Santander Bank, N.A. FDIC insurance covers that bank failing, not Rho failing. (§1.4, §9.1) |
| **It is an orchestration layer** | At least seven regulated or third-party providers sit behind the products: Webster/Santander, American Deposit Management, Apex Clearing and Interactive Brokers, Mastercard, Wise, Stripe, and Slope with Lead Bank. (§2.2) |
| **The software really is $0** | There is no paid tier anywhere. You pay through interchange on card spend, the spread on deposits, 1% on foreign currency, and a 0.15% to 0.60% Treasury advisory fee. Free software funded by balances is a legitimate model, and it is the model. (§4) |
| **The headline yield is not reachable** | The advertised Treasury rate assumes a 100% allocation to a fund the product caps at 50%. Under the standard published rules the achievable blended figure at the best fee tier is materially lower. (§3.3, §8.2) |
| **The API cannot move money** | Fourteen operations, all HTTP GET, shipped 2026-08-03. No writes, no webhooks. Rho says write access is next. (§6) |
| **Where it genuinely wins** | No seat fees at any size, 24/7 human support including phone on a $0 account, a $50,000 Treasury minimum against Mercury's $250,000, AP automation included and settling from the account that holds the cash, and comparison pages that name where competitors beat it. (§8.1) |
| **Where it is behind** | Scale, write-capable APIs and agent surface. Ramp, Brex and Mercury all shipped agent tooling before Rho, and Mercury and Brex can both initiate payments programmatically. (§7, §8.2) |
| **The verdict** | A well-executed bundle built on one structural pricing bet, not a differentiated technology company. That is not a criticism: the bundle is the product. (§8.4) |
| **Before moving cash** | Work the eighteen diligence questions in §9.6. |

---

## How this was researched, and how much to trust it

### The corpus

- **556 pages of rho.co**, crawled in full: all 13 product pages, pricing, all 8 competitor comparison pages, all 269 help-center articles, 125 comparison and review blog posts, every policy and terms page, 14 customer case studies, and the changelog. The sitemap lists 1,042 URLs; the 486 not crawled are almost entirely blog posts and partner landing pages outside the product surface.
- **The complete developer documentation** at docs.rho.co: 13 guides and 14 API operation references.
- **The live API**, measured directly. Roughly 2,500 requests against the public sandbox.
- **Independent sources** for everything about the outside world: SEC EDGAR (the Securities and Exchange Commission's free public filings database) and Form ADV filings (the annual disclosure every SEC-registered investment adviser must file), FDIC BankFind (the FDIC's public register of insured banks), licensing decisions by the OCC (the Office of the Comptroller of the Currency, the federal regulator that grants national bank charters), Capital One's 10-Q (a public company's quarterly financial report to the SEC), competitor documentation and pricing pages, and press coverage.

### The method

Two passes, deliberately adversarial. A first pass extracted findings from the corpus. A second pass took the
sixteen most load-bearing claims and handed each to an independent checker whose instructions were to
**refute** it, defaulting to "unverified" rather than "confirmed" when evidence was thin.

That second pass changed the document materially. Fifteen of the sixteen claims came back
`PARTIALLY_CONFIRMED` rather than `CONFIRMED`, meaning the original was directionally right but wrong in a
number, a date, or a scope. One example worth stating up front, because it shows what the process is for:
the first pass reported that Rho's terms make a customer "liable for all unauthorized use of all cards" once
ten or more cards are issued, which reads alarming. The checker confirmed the clause exists and then
established that it is a near-verbatim restatement of federal law, Regulation Z at 12 C.F.R. 1026.12(b)(5),
that Brex's card agreement carries the same clause, and that it is standard commercial card practice. The
alarming number comes from the CFPB (the Consumer Financial Protection Bureau, the US federal agency that
writes and enforces consumer finance rules), not from Rho. That correction survives into section 9.

### The three labels

| Label | Meaning |
| --- | --- |
| **Rho says** | A claim from Rho's own marketing, help center, docs or contracts, and nothing more |
| **Verified:** | Checked against a primary source outside Rho's control, or a live HTTP response |
| **Assessment:** | A judgment. Reject it freely; the evidence it rests on is cited |

Anything with a rate, a fee, a valuation or a product status carries an as-of date, because all four change.

### What this research could not do

No Rho account was opened. No sales conversation happened. The production API was never called with a real
token, so every measured API statement is sandbox behavior. Pricing and product claims about competitors are
their own published figures unless a primary source is cited. Several important things, notably the actual
cost of Rho Capital and the real distribution of card credit limits, are not published anywhere and remain
open. Section 10 lists every one of them.

---

## Contents

- [1. Rho in plain English](#1-rho-in-plain-english)
    - [The vocabulary you need](#the-vocabulary-you-need)
    - [The problem Rho is solving](#the-problem-rho-is-solving)
    - [What Rho bundles instead](#what-rho-bundles-instead)
    - [The one thing to understand](#the-one-thing-to-understand)
    - [How to read the rest of this document](#how-to-read-the-rest-of-this-document)
- [2. What Rho actually is, structurally](#2-what-rho-actually-is-structurally)
    - [The legal entity](#the-legal-entity)
    - [The orchestration map](#the-orchestration-map)
    - [What this architecture buys, and what it costs](#what-this-architecture-buys-and-what-it-costs)
    - [The corporate record](#the-corporate-record)
    - [Reliability, as far as it can be checked](#reliability-as-far-as-it-can-be-checked)
- [3. The product surface, one piece at a time](#3-the-product-surface-one-piece-at-a-time)
    - [3.0 Who actually provides each service](#30-who-actually-provides-each-service)
    - [3.1 Business Checking](#31-business-checking)
    - [3.2 Business Savings](#32-business-savings)
    - [3.3 Rho Treasury](#33-rho-treasury)
    - [3.4 The rails: timing, cutoffs, limits and checks](#34-the-rails-timing-cutoffs-limits-and-checks)
    - [3.5 Corporate Cards](#35-corporate-cards)
    - [3.6 Vendor Cards](#36-vendor-cards)
    - [3.7 Expense Management](#37-expense-management)
    - [3.8 Bill Pay (AP)](#38-bill-pay-ap)
    - [3.9 Invoicing (AR)](#39-invoicing-ar)
    - [3.10 Rho Capital](#310-rho-capital)
    - [3.11 Rho Close](#311-rho-close)
    - [3.12 Incorporation](#312-incorporation)
    - [3.13 The Partner Portal for accountants](#313-the-partner-portal-for-accountants)
    - [3.14 The mobile app](#314-the-mobile-app)
    - [3.15 The Slack app and the Gmail connector](#315-the-slack-app-and-the-gmail-connector)
    - [3.16 The support model](#316-the-support-model)
    - [3.17 Capability matrix](#317-capability-matrix)
- [4. How Rho makes money](#4-how-rho-makes-money)
    - [4.1 The revenue map](#41-the-revenue-map)
    - [4.2 Interchange: the fee the merchant pays](#42-interchange-the-fee-the-merchant-pays)
    - [4.3 Deposit spread: the largest line, and the one Rho never names](#43-deposit-spread-the-largest-line-and-the-one-rho-never-names)
    - [4.4 The Rho Treasury advisory fee](#44-the-rho-treasury-advisory-fee)
    - [4.5 The 1% foreign exchange fee](#45-the-1-foreign-exchange-fee)
    - [4.6 Card acceptance on invoices: 2.9% + $0.30](#46-card-acceptance-on-invoices-29-030)
    - [4.7 Rho Capital: referral economics, undisclosed](#47-rho-capital-referral-economics-undisclosed)
    - [4.8 Incorporation: a fee that is mostly a deposit test](#48-incorporation-a-fee-that-is-mostly-a-deposit-test)
    - [4.9 The fee reality](#49-the-fee-reality)
    - [4.10 The gating structure](#410-the-gating-structure)
    - [4.11 How this compares](#411-how-this-compares)
- [5. Who Rho is for, and who it is not for](#5-who-rho-is-for-and-who-it-is-not-for)
    - [5.1 The eligibility gate](#51-the-eligibility-gate)
    - [5.2 The ideal customer profile the money describes](#52-the-ideal-customer-profile-the-money-describes)
    - [5.3 Practical fit guide](#53-practical-fit-guide)
    - [5.4 The anti-fit cases](#54-the-anti-fit-cases)
- [6. The API and the agent surface](#6-the-api-and-the-agent-surface)
    - [6.1 What shipped, and when](#61-what-shipped-and-when)
    - [6.2 The whole surface fits in one table](#62-the-whole-surface-fits-in-one-table)
    - [6.3 Two ways to hold a credential](#63-two-ways-to-hold-a-credential)
    - [6.4 MCP, and Rho's MCP server](#64-mcp-and-rhos-mcp-server)
    - [6.5 Rate limits](#65-rate-limits)
    - [6.6 The capability boundary](#66-the-capability-boundary)
    - [6.7 Where Rho sits on the agentic-banking timeline](#67-where-rho-sits-on-the-agentic-banking-timeline)
    - [6.8 Why read-only is a defensible choice](#68-why-read-only-is-a-defensible-choice)
    - [6.9 What it costs](#69-what-it-costs)
- [7. The 2026 competitive landscape](#7-the-2026-competitive-landscape)
    - [7.1 "Business banking" is at least four markets, and most comparisons mix them](#71-business-banking-is-at-least-four-markets-and-most-comparisons-mix-them)
    - [7.2 Rho vs Ramp](#72-rho-vs-ramp)
    - [7.3 Rho vs Brex](#73-rho-vs-brex)
    - [7.4 Rho vs Mercury](#74-rho-vs-mercury)
    - [7.5 Rho vs the spend and AP incumbents](#75-rho-vs-the-spend-and-ap-incumbents)
    - [7.6 Rho vs traditional banks and the chartered digital banks](#76-rho-vs-traditional-banks-and-the-chartered-digital-banks)
    - [7.7 The positioning map](#77-the-positioning-map)
- [8. Where Rho actually differentiates](#8-where-rho-actually-differentiates)
    - [8.1 The genuine differentiators](#81-the-genuine-differentiators)
    - [8.2 Differentiation that is thinner than claimed](#82-differentiation-that-is-thinner-than-claimed)
    - [8.3 What Rho is missing that its cohort has](#83-what-rho-is-missing-that-its-cohort-has)
    - [8.4 A differentiated company, or a well-executed bundle?](#84-a-differentiated-company-or-a-well-executed-bundle)
- [9. Risks, fine print, and what to check before committing](#9-risks-fine-print-and-what-to-check-before-committing)
    - [9.1 Where the money actually sits](#91-where-the-money-actually-sits)
    - [9.2 The savings sweep, read closely](#92-the-savings-sweep-read-closely)
    - [9.3 What happens if Rho fails, versus if the bank fails](#93-what-happens-if-rho-fails-versus-if-the-bank-fails)
    - [9.4 The contract](#94-the-contract)
    - [9.5 Concentration and vendor risk](#95-concentration-and-vendor-risk)
    - [9.6 The diligence checklist](#96-the-diligence-checklist)
- [10. Open questions and how to keep this document current](#10-open-questions-and-how-to-keep-this-document-current)
    - [10.1 What this research could not settle](#101-what-this-research-could-not-settle)
    - [10.2 Facts with the shortest shelf life](#102-facts-with-the-shortest-shelf-life)
    - [10.3 How this document was built](#103-how-this-document-was-built)
    - [10.4 Refresh procedure](#104-refresh-procedure)

A companion document, `RHO_API_REFERENCE.md`, covers the developer surface in full detail:
the endpoint reference, the sandbox, MCP, and the places where Rho's published docs diverge from live behavior.

---

## 1. Rho in plain English

Rho is a web application that a US-registered company logs into to hold its money, spend it, pay its bills, collect what it is owed, and keep its books, all in one place and with no software subscription fee. It does not hold the money itself: the cash sits at Webster Bank (a division of Santander Bank, N.A.) and at a network of partner banks, the cards are issued by Webster under a Mastercard license, the investment product is run by a Rho subsidiary registered with the SEC, and the credit line is originated by Lead Bank, so what Rho actually sells is the software and the coordination between those parties. The legal entity is Under Technologies, Inc., incorporated in Delaware in 2018, operating as Rho Technologies from 100 Crosby Street in New York.

### The vocabulary you need

Every term below is used throughout this document. Where a term does particularly heavy work in a later section, it is restated briefly at that point; otherwise this is the only place it is defined. Where Rho's own product is the clearest example, the example is Rho's.

| Term | What it means | Concrete example |
| --- | --- | --- |
| **Business checking account** | A company's everyday cash account: money comes in, money goes out, and the balance normally earns little or nothing. Legally distinct from a personal account, and it belongs to the company, not to the founder. | A startup's payroll and vendor payments run out of checking. Rho's checking pays no interest and has no monthly fee (rho.co/pricing, captured 2026-09-11). |
| **ACH and wire** | The two ways US businesses move money between banks. **ACH** (Automated Clearing House) is a cheap batch network; it settles in a day or more, can be returned, and carries payroll and most recurring vendor payments. A **wire** is processed individually, arrives the same day, and is effectively irreversible once sent. | Rho's pricing page lists "Same-Day ACH, wires, and checks $0" domestically. A payroll run leaves by ACH; a $2M acquisition payment leaves by wire. |
| **FX and SWIFT** | **FX** is foreign exchange, the business of converting one currency into another; an FX fee is the margin taken on the conversion. **SWIFT** is the international messaging network banks use to instruct each other to move money across borders, and a SWIFT payment can pick up charges from intermediary banks along the way. | Rho charges 1% to convert dollars into another currency, plus an optional flat $15 if you choose to absorb the correspondent and SWIFT charges rather than let them come out of what the recipient receives. |
| **Corporate card** | A payment card issued in the company's name, given out to employees, with the bill going to the company rather than to the employee. | Rho issues Mastercard World Elite Business cards through Webster Bank. An engineer buys AWS credits on one and never files for reimbursement. |
| **Charge card vs credit card** | A **charge card** must be paid off in full at the end of each cycle and carries no revolving balance or interest. A **credit card** lets you carry a balance and charges interest on it. Both are "corporate cards"; the difference is whether the debt can roll. | Rho's two modes are both charge-style. Daily Terms settles the balance to zero at the end of the same business day, with "no grace period" (Terms of Service, Addendum A, section 2.1). Monthly Terms is "a 30-day billing cycle with a 1-day repayment period" (Rho help center). |
| **Personal guarantee** | A promise by a founder, signed personally, to repay the company's debt out of their own pocket if the company cannot. It is the thing that makes a failed startup also a personal bankruptcy. | Rho markets "No personal guarantee, no personal credit check, no annual fee" on its corporate cards page. Sections 3.5 and 9.4 examine what its Terms of Service actually reserve. |
| **Interchange** | The fee a merchant pays every time a card is used, split between the card network and the bank that issued the card. It is invisible to the cardholder and is the main reason a card can be free to the company using it. | A vendor charging $10,000 to a commercial card typically nets a little over $9,700, with the difference shared among the network and the issuer. **Verified:** interchange is never named as a Rho revenue line anywhere in Rho's 522-page corpus; that it is one is an inference, supported outside the corpus by Banking Dive (2022-08-23, quoting Rho's own characterization of interchange-led revenue) rather than by Rho's own disclosure. |
| **FDIC insurance** | A US government guarantee that if a bank fails, each depositor gets back up to $250,000 per insured bank, per ownership category. It protects against the *bank* failing, not against the software company in front of the bank failing. | Rho's own footer states it plainly: "FDIC deposit insurance coverage is available only to protect you against the failure of an FDIC-insured bank that holds your deposits... It does not protect you against the failure of Rho or other third party." |
| **SIPC** | The brokerage equivalent of FDIC, covering up to $500,000 per customer (of which at most $250,000 in cash) if the *broker* fails. It does not protect you if the investments themselves lose value. | Rho's Treasury product is held at Apex Clearing Corp. or Interactive Brokers LLC, both members of FINRA (the Financial Industry Regulatory Authority, the brokerage industry's self-regulator) and of SIPC. The funds inside can still fall in price. |
| **Sweep network** | A service that automatically spreads one large deposit across many banks in $250,000 slices, so that each slice stays inside the FDIC limit. The customer sees one balance; behind it are dozens of banks. | Rho Business Savings runs through American Deposit Management Co., which Rho describes as "a network of 400+ FDIC- and NCUA-insured institutions, as of August 2026" (the NCUA is the credit-union equivalent of the FDIC, with the same $250,000 limit), advertising up to $75,000,000 of coverage per entity. |
| **Treasury / idle cash** | "Idle cash" is money the company will not need for months. "Treasury" is the practice of parking it somewhere that pays more than a checking account, usually short-term government debt or conservative bond funds. | A company that raised $10M and burns $300k a month has roughly $8M idle. Rho Treasury invests it in Treasury Bills and two funds, for an advisory fee of 0.15% to 0.60% of assets per year. |
| **Money market fund** | A mutual fund that holds only very short-term, very safe debt (Treasury bills, government paper, bank paper) and is run so that each share stays worth exactly $1.00. It pays close to the short-term government rate, is bought through a brokerage rather than a bank, and is covered by SIPC rather than the FDIC, which means nothing guarantees the $1.00 share price: in principle it can lose value, even though these funds almost never do. | A company with $8M idle typically parks it in a money market fund at Schwab or Fidelity. Rho Treasury offers one (IJTXX, a JPMorgan US Treasury Plus fund at a fixed $1.00 NAV) alongside T-Bills, an ultra-short income fund and a short-term bond fund. |
| **Yield and APY** | **Yield** is the annualized return on an investment. **APY** (annual percentage yield) is the same idea for a deposit account, including the effect of compounding. A yield is not guaranteed and moves daily; an APY on a bank deposit is set by the bank. | Rho's headline "up to 4.66%" (stamped 09/11/2026) is a fund yield net of fees, not an APY, and it can fall. Section 3.3 shows why the reachable number under Rho's own allocation rules is 4.18%. |
| **Venture debt** | A loan made to a startup that is not yet profitable, sized against the equity it has just raised rather than against its earnings, usually by a specialist bank or fund. It is how a company borrows without selling more shares. | SVB and First Citizens size venture debt at 20% to 40% of a startup's last equity round. Rho does not offer it: Rho Capital is a smaller revolving line drawn against cash flow, and Rho describes it as "not a term loan or a venture debt facility." |
| **Accounts payable (AP)** | Money the company owes to other people, and the process of approving and paying it. | A design agency emails a $12,000 invoice. Somebody has to read it, code it to a budget line, get it approved, and send the money. Rho calls this Bill Pay. |
| **Accounts receivable (AR)** | Money other people owe the company, and the process of billing for it and chasing it. | You finish a project, send a $40,000 invoice, and wait. Rho calls this Invoicing. |
| **Spend management** | Software that controls company spending *before* it happens: who gets a card, what they can buy on it, up to what limit, and who approves the exception. Distinct from accounting, which records spending after the fact. | Give the marketing lead a card capped at $5,000 a month that only works at ad platforms. Ramp and Brex are the category-defining products here. |
| **Expense report** | The old manual ritual: an employee pays with their own money, keeps receipts, fills in a form, and waits weeks for reimbursement. Company cards plus automatic receipt capture are what kill it. | Rho's pitch is "Receipts, approvals, and coding, automatic," which is the category promise, not a Rho invention. |
| **Month-end close** | The few days after each month ends when finance reconciles every account, codes every transaction, and produces the month's financial statements. It is the single most painful recurring task in a small finance team. | Rho Close uses AI to pre-fill the accounting fields on card and bank transactions. **Verified:** it suggests transaction coding only. It has no close checklist, no period lock, and no sign-off, and its own FAQ answers "No" to whether it syncs to accounting software automatically. |
| **ERP and general ledger (GL)** | The **general ledger** is the authoritative book of every financial entry a company makes. An **ERP** is the larger system the ledger lives inside. For a startup this is usually QuickBooks Online; for a larger company, NetSuite or Sage Intacct. | Rho pushes coded transactions into QuickBooks Online, NetSuite, Sage Intacct, Xero, Campfire and Puzzle at no extra charge. |
| **Reconciliation** | Proving that what the bank says happened matches what the ledger says happened, transaction by transaction, and explaining every difference. | 340 card transactions in the bank feed must each find their match in QuickBooks. Anything unmatched is an error or a fraud until proven otherwise. |
| **Bank charter** | The government license that makes an institution a bank: it can hold insured deposits in its own name, and it is examined by a federal or state regulator. Without one you are not a bank, however bank-like your app looks. | Mercury received **preliminary conditional** approval from the OCC on 2026-04-24 to charter Mercury Bank, N.A. Final approval and authorization to open were still outstanding. Rho has no charter and no public application. |
| **Sponsor bank (also "partner bank")** | The chartered bank that actually holds a fintech's customer deposits and issues its cards, while the fintech owns the app, the ledger and the customer relationship. | Rho's sponsor is Webster Bank, a division of Santander Bank, N.A. Brex's checking leg sits at Column N.A.; Mercury's at Choice Financial Group and Column. |
| **Banking-as-a-service (BaaS) middleware** | An extra company that sits between the fintech's app and the sponsor bank, running the ledger and the payment plumbing for many fintechs at once. Every extra layer is another set of records that has to agree with the bank's, and another company that can fail. | Relay reaches its bank (Thread) through middleware called Unit. **Rho says** it connects to Webster directly, which if true removes the layer that failed in the 2024 Synapse collapse. |
| **Fintech vs bank** | A **bank** holds a charter and your deposits. A **fintech** holds neither: it is a software company with a contract with a bank. The distinction is invisible when everything works and decisive when it does not. | Rho states it on every page: "Rho is a fintech company, not a bank or an FDIC-insured depository institution." |
| **API** | Application Programming Interface: a way for your own code, rather than a human in a browser, to ask a system for data or tell it to do something. | Rho's v1 API launched 2026-08-03 with **14 operations, all GET** (read-only), across accounts, cards, transactions, statements and invoicing. Nothing in it can move money. |
| **MCP** | Model Context Protocol: a standard way to hand an AI assistant a set of tools so it can query a system in plain language. An MCP server is that toolset, hosted. | Rho runs an MCP server at rhoapi.rho.co/mcp/v1 so a chat assistant can answer "what did we spend on software last month." It is read-only, and it exists only in production (the sandbox host returns 404). |

### The problem Rho is solving

Take a real shape: a 20 person company, two years old, $12M raised, burning $350,000 a month, with three people who touch finance (a founder, a head of ops, and a part-time controller).

Its money is in more places than anyone finds comfortable. About $400,000 sits in a business checking account so payroll clears. Roughly $8M of the raise sits somewhere earning yield, usually a brokerage money market fund at Schwab or Fidelity, opened separately, funded by wire, and reconciled by hand. Somewhere between those two accounts is a savings account nobody is sure is fully insured, because the FDIC limit is $250,000 per bank and the balance is many multiples of that.

Then the spending. Twenty people need to buy things. Without company cards, they buy on personal cards and file expense reports, which means the controller spends the first week of every month chasing receipts. With company cards, you need software to set limits, route approvals and capture receipts, because a card with no controls is just a faster way to lose money.

Then the bills. Vendors email PDF invoices to an accounting@ address. Someone opens each one, types the amount into a payment tool, routes it for approval, pays it, and then types it again into the ledger. Then the invoices the company sends out, which live in a different tool again, with a different set of reminders nobody sends.

Then, every month, the close: matching several hundred card and bank transactions against the ledger, coding each to a category and a department, and producing a P&L (profit and loss statement, the report showing what the company earned and spent in the month) that the board sees. Each tool exports a CSV, a plain spreadsheet file. The CSVs do not agree.

The old way requires five to seven separate vendors. A representative build, using published 2026 prices, for 20 card holders and three finance seats:

| Job | Typical tool | Published price | Annual, this company |
| --- | --- | --- | --- |
| Checking | Chase Business Complete | $15/month unless a $2,000 daily balance waives it; outgoing wires $25 to $40 | about $180 plus wire fees |
| Corporate card + spend controls | Ramp Plus / Brex Premium | $15 and $12 per user per month (free base tiers exist) | $2,880 at $12 x 20 |
| Expense reports | Expensify Control | $18 per member per month without the Expensify Card, $36 month to month | $4,320 at $18 x 20 |
| AP / bill pay | BILL | $49, $65 or $89 per user per month (Essentials, Team, Corporate) | about $2,340 at $65 x 3 (Team, the cheapest tier with two-way accounting sync) |
| AR / invoicing | Stripe Invoicing or similar | usually free to send, about 2.9% + $0.30 on card payments | volume dependent |
| General ledger | QuickBooks Online | from $38/month | about $456 |
| Treasury | Brokerage money market fund | 0% to 0.60% of assets if advised | $0 to $48,000 on $8M |

**Assessment:** the software bill lands around $10,000 to $11,000 a year before any treasury fee, which is real but not ruinous. The expensive part is not the invoices; it is the three people and the seven logins and the CSVs that disagree. Note also that the two priciest rows are avoidable: Brex Essentials and Ramp's base tier are $0, and Expensify's rate halves if you route card spend through Expensify. Anyone selling you a bundle by adding up list prices is quoting the worst case.

### What Rho bundles instead

Rho's answer is to charge nothing for the software and make its money on the balances and the payments instead. Prices below are from rho.co/pricing and the relevant product pages as captured 2026-09-11.

| Old-way tool | Rho equivalent | What Rho charges |
| --- | --- | --- |
| Business checking at a bank | Rho Checking (at Webster Bank) | $0 monthly, $0 minimum, $0 domestic ACH, wires and checks |
| High-yield savings | Rho Business Savings (ADM sweep, up to $75M FDIC) | $0; Rho does not publish the rate on its pricing page |
| Brokerage money market fund | Rho Treasury (RBB Treasury LLC, an SEC-registered adviser) | 0.15% to 0.60% of assets per year, tiered by size; $50,000 minimum |
| Corporate card program | Rho Corporate Cards (Mastercard World Elite Business) | $0 annual, $0 per card; cashback 1.25% or 2% on Daily Terms, 1% or 1.75% on Monthly, capped at $1,000,000 of eligible spend per calendar year |
| Expense report software | Rho Expense Management | $0, "unlimited users at no extra cost" |
| Bill.com / AP automation | Rho Bill Pay | $0 per payment domestically |
| Invoicing / AR | Rho Invoicing | $0 to send; 2.9% + $0.30 if the customer pays by card |
| Accounting close spreadsheet | Rho Close | included; suggests transaction coding, does not sync automatically |
| Venture debt or a bank line | Rho Capital | $0 origination fee (the up-front charge for setting up a loan), $0 prepayment penalty (the charge for paying it back early); the actual rate is published nowhere |
| Incorporation service (Clerky, Stripe Atlas) | Rho Incorporation | $400, creditable back; "$1,000 annually" for platform access after year one |
| Wise / FX payments | International payments via Wise US Inc. | 1% on foreign-currency (FX) transfers, optional $15 SWIFT fee, $30 international wire recall |
| Payroll (Gusto, Rippling) | **not offered** | Rho does not run payroll, and does not accept cash deposits |

**Rho says:** "Everything your business does with money, in one place" and "the only standard payment fee is 1% on foreign-currency transfers."

**Verified:** that second sentence appears verbatim in 19 files across Rho's own corpus, while the same corpus documents at least eleven other priced charges, including a $30 wire recall fee, an optional $15 SWIFT fee, "around $20 – $45" on failed and returned domestic wires, a 3%-per-month late fee, up to 1% on foreign card transactions, 2.9% + $0.30 on card-paid invoices, the $400 incorporation fee, the 0.15% to 0.60% Treasury fee, and an open-ended reservation in the Terms of Service that "Fees are not limited to the aforementioned list." Three of those are printed in the asterisk footnote on the pricing page itself, so they are fine print rather than concealment. Section 4.9 works through all of them.

**Assessment:** the bundle is genuinely cheap and genuinely broad, and for a company of this size it is a better deal than the seven-vendor stack, mostly because of the integration rather than the price. The honest framing is that you are not getting free software; you are paying for it in interchange on your card spend, in the spread your bank partner earns on your deposits, in 1% on anything you send in a foreign currency, and in an advisory fee if you use Treasury. That is a reasonable trade. It is just not "free."

### The one thing to understand

Rho is not a bank. It is a software company sitting in front of other people's regulated balance sheets, and almost everything else in this document follows from that sentence.

Practically, for a customer, it means four things.

**Your deposits are at Webster, not at Rho.** When you wire money "to Rho," it lands in an account at Webster Bank, a division of Santander Bank, N.A. FDIC insurance covers you if *that bank* fails, up to $250,000. It does not cover you if Rho fails, and Rho's own footer says exactly that. Note one wrinkle the marketing has not fully absorbed: Webster Bank, N.A. (FDIC cert 18221) ceased to exist as a separately insured institution on 2026-08-20, when it was merged into Santander Bank, N.A. (FDIC cert 29950), which kept the Webster name as a division brand (FDIC BankFind records, checked 2026-09-11). Rho's disclosure language is technically accurate. Some of its older blog copy is not.

**Your risk if Rho itself fails is operational, not a loss of principal, but it is not nothing.** The money is at a real bank. What Rho holds is the ledger that says which dollars are yours, the login, the payment rails, and the card program. If the software company were to fail, the deposits would still exist; recovering and reconciling them is a legal and operational exercise, and recent industry history (fintech intermediaries collapsing and stranding customer funds for months) is the reason this sentence is in this document at all. **Rho says** it integrates directly with Webster rather than through a banking-as-a-service middleware layer (the extra ledger-keeping company defined in the glossary above), which would materially reduce that specific failure mode. Nothing in the public record independently confirms it.

**Rho can only ship what its partners allow.** Every product is somebody else's regulated capability wrapped in Rho's interface: savings is American Deposit Management's sweep, treasury is Apex or Interactive Brokers custody under a Rho-owned SEC-registered adviser, credit is Lead Bank origination underwritten by Slope, FX is Wise, invoice card acceptance is Stripe. That is why Rho's feature velocity looks uneven, why some rules read oddly (savings withdrawals limited to six per month, processed Tuesdays and Thursdays), and why the API is read-only. It is also why the competitive question in 2026 is not "whose app is prettier" but "who owns the balance sheet," which is precisely what Mercury's charter application is about.

**The contract you sign is with the software company, and it is drafted accordingly.** Rho's Terms of Service (version 7.0.0, last updated 2026-08-27) cap Rho's own liability at $500, with carve-outs for what law requires and for arbitration. That cap runs to Rho's obligations under its own agreements. It is not a cap on recovering deposits held at Webster under a separate agreement. Section 9.4 reads the contract properly.

None of this makes Rho unusual or dangerous. Mercury, Brex and Ramp all sat in the same position until very recently, and Brex's checking leg still does. It makes Rho *normal*, and the point of saying it out loud in section 1 is that every later claim about safety, yield, coverage and capability has to be read through it.

### How to read the rest of this document

The document runs in ten sections. Each assumes the ones before it.

| # | Section | What it answers |
| --- | --- | --- |
| 1 | Rho in plain English (this one) | What is this, and what do all these words mean? |
| 2 | What Rho actually is, structurally | Who is behind each product, and what has the company itself raised and built? |
| 3 | The product surface, one piece at a time | What does each product actually do, cost and limit? |
| 4 | How Rho makes money | If the software is free, where does the revenue come from? |
| 5 | Who Rho is for, and who it is not for | Can I even open an account, and is this built for a company like mine? |
| 6 | The API and the agent surface | What can a developer or an AI agent do with it today? |
| 7 | The 2026 competitive landscape | How does this compare to Ramp, Brex, Mercury, the legacy tools and real banks? |
| 8 | Where Rho actually differentiates | Which advantages are real, and which are marketing? |
| 9 | Risks, fine print, and what to check | What could go wrong, and what should I ask before moving money? |
| 10 | Open questions and keeping this current | What could not be settled, and what expires first? |

Section 6 is a summary. The full developer reference lives in the companion document, `RHO_API_REFERENCE.md`.

Three labels recur throughout and are worth internalizing now. **"Rho says"** is a claim from Rho's own marketing, help center, documentation or contracts, and nothing more. **"Verified:"** is a claim checked against a primary source outside Rho's control (an SEC filing, an FDIC record, an OCC decision, a live HTTP response, a competitor's own contract) or corroborated inside Rho's corpus by a source with no incentive to say it. **"Assessment:"** is a judgment, which you are free to reject. Anything with a rate, a fee, a valuation or a product status carries an as-of date, because all four change.
## 2. What Rho actually is, structurally

### The legal entity

"Rho" is a brand. The company is **Under Technologies, Inc.**, a Delaware corporation doing business as Rho Technologies, incorporated in 2018, headquartered at 100 Crosby Street, New York, NY 10012 (earlier filings give 203 Lafayette Street, Suite C306, a few blocks away). Its SEC Central Index Key, the identifier the Securities and Exchange Commission assigns to any entity that files with it, is 0001756460. The site footer reads "© 2019 - 2026 Under Technologies, Inc. DBA Rho Technologies."

The first Form D (the short notice a company must file with the SEC after selling shares privately) filed on 2018-10-24 names three executive officers and directors: Peter Damian Kimmelman, Garth Alexander John Wheldon (the "Alex Wheldon" named publicly as co-founder), and Everett Cook. Kimmelman is absent from the next filing on 2019-08-15 and from every filing after it, so he was out as an officer and director within roughly ten months of incorporation. Rho's own 2023 boilerplate says "Founded in 2018 by Everett Cook and Alex Wheldon." Cook is CEO as of 2026-09-11.

One subsidiary matters structurally: **RBB Treasury LLC**, doing business as Rho Treasury (also registered under the name "Rho Prime"), CRD 314581, SEC file number 801-125841. It is a separately registered investment adviser, which is an entity licensed by the SEC to manage money for clients and bound by a fiduciary duty to them. Under Technologies, Inc. has been its sole member since February 2022. This is the only part of the Rho stack that Rho both owns and holds a financial license for.

Everything else is somebody else's license.

### The orchestration map

Rho is a single interface, a single login, a single dashboard, sitting on top of at least nine outside counterparties, each of which holds the regulatory permission that makes one Rho product legal. The product experience is unified. The legal reality underneath is not.

The "prominence" column below counts how many of the 556 rho.co pages captured in the local corpus (130 core pages, 269 help-center pages, 125 comparison posts, 25 partner microsites, plus assorted extras) name that provider at all. The top of the table is boilerplate that appears in the footer of nearly every page. The bottom of the table is named once or twice, in terms-of-service text a customer has to go looking for.

| Product | Who actually provides it | Regulatory wrapper | Named on |
|---|---|---|---|
| Checking deposits, card issuance | **Webster Bank, a division of Santander Bank, N.A.** | National bank charter; FDIC-insured (cert 29950) | 319 pages |
| Savings sweep | **American Deposit Management, LLC** and its subsidiary ADM Consulting, LLC | Deposit placement agent, not a bank; insurance sits at 400+ receiving banks and credit unions | 278 pages |
| Treasury advice | **RBB Treasury LLC** dba Rho Treasury (Rho's own subsidiary) | SEC-registered investment adviser | 211 pages |
| Treasury custody and execution | **Apex Clearing Corporation**, **Interactive Brokers LLC** | Registered broker-dealers, members FINRA/SIPC | 204 / 200 pages |
| Card network | **Mastercard** | Card network rules; Webster issues "pursuant to a license from Mastercard" | 232 pages |
| International and FX payments | **Wise US Inc.** | Wise's own money transmission licenses; customer must separately accept the Wise US Inc. Customer Agreement | 194 pages |
| Rho Capital (credit line) | **Lead Bank** makes the loans; **Slope** underwrites and services them | Bank lending via a fintech underwriter; "Business-purpose loans made by Lead Bank" | Lead Bank 9, Slope 3 |
| Card acceptance on invoices | **Stripe, Inc.** | Payment processor; Rho provisions a Stripe connected account and the customer accepts the Stripe Connected Account Agreement | 1 page |
| External account linking and data | **Plaid**, **Finicity** (Mastercard Data Connect), **Codat**, **Stripe Financial Connections** | Data aggregators / open-banking intermediaries | Plaid 21, Finicity 4, Codat 1 |

A few rows need unpacking.

**Webster is now a brand, not a bank.** Verified: the FDIC's own institution record shows Webster Bank, National Association (cert 18221) with `ACTIVE = 0` and an end-effective date of **08/20/2026**. On that date it was merged into Santander Bank, N.A. (cert 29950), which continues to run the business as a division under the Webster name. So the awkward phrase Rho repeats hundreds of times, "Webster Bank, a division of Santander Bank, N.A., Member FDIC," is technically exact. The bank legally holding Rho checking deposits as of 2026-09-11 is Santander Bank, N.A.

This is the second time Rho's bank partner has changed without Rho choosing it. Rho selected Sterling National Bank in 2020; Webster Financial completed its merger with Sterling Bancorp on 2022-01-31, and Rho's partner became Webster by operation of that deal. Then Santander acquired Webster, closing 2026-08-20. Assessment: Rho's bank relationship is a pass-through of other people's M&A. Rho now markets the result ("unlike most fintechs, the bank behind it is one of the largest in the country") as if it were a strategy.

**The savings sweep is not a bank account.** A sweep network is a service that takes one large deposit and splits it across many banks in sub-$250,000 slices, so that each slice sits inside the FDIC limit. FDIC insurance is the federal guarantee that covers up to $250,000 per depositor per insured bank if that bank fails. Rho says the Rho Business Savings Account offers "up to $75M in FDIC deposit insurance" across "a network of 400+ FDIC- and NCUA-insured institutions, as of August 2026." The entity performing the splitting is American Deposit Management, acting as the customer's agent, and Rho's own footnote concedes the limit is capacity, not contract: "Coverage reflects the partner-bank network's capacity as of August 2026 and is not a contractual guarantee." Verified: the published ADM master services agreement commits only that ADM "will use commercially reasonable efforts to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution," with an explicit carve-out that on a single day "for a limited amount of time (intraday or overnight), the entire amount of the withdrawal or deposit may be held at one Program Institution." Section 9 covers this in detail, including the six-withdrawals-per-month cap and the Exhibit A insurance waiver.

**Treasury is a brokerage account wearing a banking dashboard.** Rho Treasury money is not a deposit. It buys Treasury bills and mutual funds held at Apex Clearing or Interactive Brokers, protected by SIPC (a $500,000-per-customer fund that covers a broker's failure, not a fall in the value of what you bought) rather than by the FDIC. Rho states this plainly and repeatedly.

**Rho Capital is the row where the marketing and the disclosure disagree.** Verified: on rho.co/product/capital (checked live 2026-09-11) the FAQ asks "Is Rho a direct lender for its working capital line of credit?" and answers "Yes." The same page's pricing section says fees "are set when Slope underwrites your line," its hero disclosure says "Financing offered by third parties," and its footer says "Slope is a financial technology company, not a bank. Business-purpose loans made by Lead Bank and subject to credit approval." Two of Rho's own comparison posts put it without ambiguity: "Rho Capital lines are issued by Lead Bank and serviced by Slope; a personal guaranty may be required." Lead Bank held **$2.76B** in assets at the FDIC call report of 06/30/2026 (the financial return every FDIC-insured bank files publicly each quarter). That is the lender, not a deposit partner, so it is not the comparison Rho makes when it argues about the size of the bank holding customer deposits. A buyer sizing a Capital facility against a bank line may still want the number.

**What the map cannot show.** Rho never names a card issuer processor or a payments processor for ACH and wires. Those layers exist in every fintech of this shape, and Rho discloses neither. Assessment: this is a category convention rather than a Rho-specific concealment. No competitor in this set names its own processors either, on the evidence of this research, and the pattern tracks the disclosure duty: the customer can see the regulated edges of the stack because law requires those disclosures, and cannot see the middle at all. The one middle layer Rho does speak to is the core ledger: **Rho says** it built its own rather than renting a banking-as-a-service provider's (see 9.3), which if true removes a layer other programs carry.

### What this architecture buys, and what it costs

**What it buys.** Three things, and they are real.

*Speed.* Rho did not need a bank charter, a broker-dealer license, a money transmitter license in each state (the license a non-bank needs before it can move other people's money, granted state by state), or a lending license. It rented all four. Contrast Mercury, which received OCC **preliminary conditional approval** on 2026-04-24 to charter Mercury Bank, N.A., with final authorization to open, FDIC deposit insurance, and Federal Reserve approvals all still outstanding as of 2026-09-11. That is a multi-year regulatory process. Rho added a lending product, Rho Capital, in a single announcement on 2026-09-09 by wiring in Lead Bank and Slope.

*Bundling.* A company that wanted checking, a corporate card, a $75M-capacity insured sweep, a managed Treasury portfolio, international payments in 22 currencies, invoicing with card acceptance, and a working capital line would otherwise be contracting with a bank, a sweep provider, a broker, a money transmitter, a processor, and a lender separately. Rho presents all of it as one account with one login.

*Price.* Because the regulated counterparties, not Rho, carry the cost structure of the underlying services, Rho can give away the software. Rho's published fee summary as of the captured pricing page reads: Same-Day ACH, wires and checks $0; subscription fees $0; checking account minimum fees $0; AP, expense and accounting automation $0; per-user fees $0. The headline exception is 1% on foreign currency transfers. (Section 4 covers the fees that sit outside that summary.)

**What it costs.** One structural thing, expressed several ways.

Every product is one or two counterparties further from the customer than it looks, and the protections the customer thinks they have attach to the counterparty, not to Rho. Rho's own disclosure says it precisely: "FDIC deposit insurance coverage is available only to protect you against the failure of an FDIC-insured bank that holds your deposits... **It does not protect you against the failure of Rho or other third party.**" That sentence is doing a great deal of work. It means the $250,000 on checking protects against Santander failing, which is remote, and not against Rho failing, which is the risk a customer of a private fintech actually carries.

The practical consequences:

1. **Contracts multiply.** Using Rho's international payments binds the customer to the Wise US Inc. Customer Agreement. Accepting cards on invoices binds them to the Stripe Connected Account Agreement and Stripe's underwriting, "which is not guaranteed." The savings sweep binds them to an ADM master services agreement. None of these are negotiated by or with Rho.
2. **Record-keeping moves off the bank's books.** Sweep ownership is a book entry on records kept by ADM and its custodians, not a deposit account statement from a bank the customer chose. Rho does not publish the list of program institutions: "The current list of network institutions is available from Rho support on request."
3. **Failure modes are somebody else's.** Four of the six incidents Rho ever posted to its status page were third-party failures (Mastercard, an SMS vendor, the card issuing partner, the bank partner), which is what an orchestrated stack looks like when it breaks.
4. **The chain can be re-ordered without the customer.** Rho's bank changed twice by merger. Rho also used **Evolve Bank & Trust** as a partner (Banking Dive, 2022-08-23: "It partners with Evolve Bank & Trust and Webster Bank to deliver its products"), and that relationship ended with no date, no announcement, and no mention anywhere in the 556-page corpus, while Rho's comparison content criticizes Mercury for its own Evolve history.

Assessment: this is not a scandal, it is the standard architecture of US business banking fintech, and Rho's disclosures are unusually complete by the standards of the category. The honest framing is that the customer trades counterparty distance for product breadth, and Rho's marketing is louder about the breadth than about the distance.

### The corporate record

Rho's own funding history is a good test of whether the internet knows anything about this company.

**Verified:** Under Technologies, Inc. has filed exactly **five Form D notices**, from 2018-10-24 through 2022-01-21, reporting **$104,732,452 sold in aggregate** ($2,272,727 + $2,499,998 + $14,959,994 + $9,999,991 + $74,999,742). All five claim the Regulation D exemption, which is what triggers the filing requirement in the first place. The final notice reports a date of first sale of 2021-10-28, and there is **no SEC filing of any type since 2022-01-21**.

| Filed | First sale | Amount sold | Investors | Maps to |
|---|---|---|---|---|
| 2018-10-24 | 2018-09-28 | $2,272,727 | 1 | Pre-seed |
| 2019-08-15 | 2019-08-08 | $2,499,998 | 1 | Seed |
| 2020-11-13 | 2020-10-29 | $14,959,994 | 15 | Series A (announced Jan 2021) |
| 2021-06-08 | 2021-05-24 | $9,999,991 | 13 | Never publicly announced |
| 2022-01-21 | 2021-10-28 | $74,999,742 | 24 | Series B (announced 2021-12-09) |

Three hedges belong with that table, and they are not decoration.

*First, the scope of what Form D proves.* Form D is required only for offerings claiming a Regulation D exemption. Two other routes generate no Form D at all: Section 4(a)(2), the statutory private-placement exemption that Regulation D sits inside as a safe harbor and that carries no filing requirement of its own, and Regulation S, the rule covering sales made outside the United States. The SEC record therefore proves **no Reg D disclosure since 2022-01-21**, which is why "**no disclosed equity since 2021**" is the defensible phrasing. Do not upgrade it to "Rho has raised no equity since 2021."

*Second, equity is not all financing.* Rho did take on money after 2021. Trinity Capital Inc. (NASDAQ: TRIN), a venture debt business development company (a publicly listed fund that lends to private companies and itemizes its positions in its SEC filings), lists Rho Business Banking in its portfolio with "Year Invested: 2024," disclosing neither structure nor amount (trinitycapital.com, fetched 2026-09-11). Any sentence phrased as "Rho has raised nothing since 2021" would be false.

*Third, the date.* 2021-10-28 is the reported date of first sale on the final Form D, not the announcement date. The round was announced 2021-12-09 and the notice filed 2022-01-21. For a general reader, "no equity round announced since December 2021" is the phrasing least likely to be misread.

**The "$150M Series C led by Balderton Capital in 2024" is not supported by any primary source.** It appears only on uncited lead-generation pages whose own figures contradict one another. Balderton's portfolio listing and sitemap do not include Rho. No Form D exists for 2023, 2024, 2025 or 2026. No press release exists on BusinessWire, PRNewswire, or Rho's own newsroom, whose blog index contains exactly two funding posts, the $75M Series B and the $100M CIM financing. Rho's actual Series B (announced 2021-12-09) was led by Dragoneer Investment Group and DFJ Growth, not Balderton. Note the careful wording: "fabricated" asserts intent that cannot be evidenced. The defensible characterisation is that the claim has no primary-source basis and is contradicted by the SEC filing record.

Assessment, and it generalizes well beyond Rho: several of the highest-ranking search results for "Rho funding" are AI-generated lead-generation pages that state a confident number, a confident lead investor, and a confident year, none of which any filing supports. The failure mode is not hallucination in the usual sense. It is a citation-free layer that gets scraped, republished, and eventually treated as consensus, and it is indistinguishable from real data at a glance. When a company has not filed anything in four years, that vacuum is exactly where synthetic facts settle. The counter-move is cheap: EDGAR is free, full-text searchable, and took minutes to check.

**The one hard scale number** in Rho's entire public record comes from the same place. **Verified:** Rho Treasury (RBB Treasury LLC, CRD 314581, SEC 801-125841) reported **$1,892,904,589 of regulatory assets under management across 1,078 accounts, all discretionary**, in its Form ADV annual amendment filed **2026-03-25**. Of those 1,078 accounts, **1,071 are corporations or other businesses** ($1,886,487,962) and **7 are charitable organizations** ($6,416,627); every other client category is zero. Regulatory AUM under Item 5.F is measured within 90 days prior to the filing date, so attribute the figure to the 2026-03-25 filing rather than to a fiscal year end.

Do not conflate this with Rho's marketing scale claims. The $1.89B is the advisory subsidiary's assets under management. It is a different quantity from Rho's "$4B+ in deposits" and from its "$4 billion moving monthly," which are themselves two incompatible readings of the same number (a balance and a flow, differing by roughly twelvefold annualized) and neither of which is independently verifiable. Section 10 takes up the scale claims.

### Reliability, as far as it can be checked

Rho runs a public status page at status.rho.co. Captured 2026-09-11 19:13:30 ET, it reports "All Systems Operational" across five components: **Web Application, Mobile Application, Corporate Cards, Bank Payments, Notifications**. All five carry a start date of 2023-04-30, so the page's own history begins there.

The page has **nine entries in its entire history**: six incidents, all between 2023-06-06 and 2023-09-05, and three planned maintenances, the last on **2024-09-28**. **No incident has been posted since September 2023, and no entry of any kind since that September 2024 maintenance.** The component records corroborate the neglect: Web Application last updated 2024-04-27, Mobile Application 2023-12-05, Corporate Cards and Bank Payments 2024-09-28, Notifications 2023-12-05.

Assessment: three years with no posted incident, and two with no status-page entry of any kind, at a company that shipped an API, a lending product, invoicing, incorporation, and a mobile Treasury flow in 2026 alone is not a plausible operational record. The more likely reading is that the status page has been abandoned. Either way the effect on a prospective customer is the same: there is no working way to verify Rho's current or historical availability. To Rho's credit, it makes no uptime claim anywhere in the corpus, no SLA and no "99.9x%" figure, which is the appropriate posture given the artifact.

One gap matters specifically for the parts of the product this dossier covers later. **The status page has no API component and no MCP component.** Rho shipped a public API in 2026 (changelog 2026-08-03, blog 2026-07-29) and runs an MCP server in production, and neither appears among the five monitored components. An integration or an agent workflow depending on those endpoints has no public health signal at all. Section 6 covers the API and the agent surface.
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
## 5. Who Rho is for, and who it is not for

Two different questions hide inside "who is this for." The first is legal and mechanical: who is Rho allowed to onboard, and what does it demand before it says yes. The second is commercial: of the businesses Rho *can* onboard, which ones does it actually want badly enough to pay for. The two answers are not the same, and the gap between them is the most useful thing in this section.

All page evidence below is from the rho.co corpus crawled 2026-09-11, with live re-fetches noted. Rho's Terms of Service in the corpus is Version 7.0.0, last updated August 27, 2026. Offers, thresholds and rates in this section are point-in-time: every partner page carries the line "This offer may be changed or discontinued at any time without notice."

### 5.1 The eligibility gate

#### Entity type

Rho publishes three different answers to "what kind of business can bank here," at three different levels of authority. In descending order of how binding they are:

| Source | What it says | Status |
| --- | --- | --- |
| Terms of Service §13, §18.3 | "You agree that the Rho Services may not be used for individual consumer use... you must be a business, charitable organization or not-for-profit organization" | The contract. Broadest of the three. |
| Help center, eligibility article | "entities must be incorporated in the United States" | Operational rule. Middle. |
| Product page, /product/business-banking | "Sole proprietorships aren't eligible on Rho; the business needs to be a registered LLC or corporation" | Marketing copy. Narrowest, and the only place the sole-proprietor exclusion appears. |

**Verified:** Rho requires a US-incorporated entity. Sole proprietorships and unincorporated businesses are explicitly excluded, and the Terms of Service bar individual consumers outright, so charities and not-for-profits are in scope even though most of Rho's marketing never mentions them. The controlling language for the entity-type gate is the help center and the ToS, not the product page.

**Verified, and worth flagging rather than resolving:** Rho's own corpus contradicts itself on sole proprietors. /product/business-savings-account says twice that sole proprietors are eligible ("Corporations, LLCs, partnerships, and sole proprietors can all open business savings accounts" and "Rho Business Savings is available to LLCs, corporations, and sole proprietorships that already bank with Rho"), while the business banking page excludes them from the checking account that savings depends on. These are not resolvable from published sources.

**Assessment:** treat the sole-proprietor exclusion as real, because it is stated on the page that governs the account you actually open. The savings-page language is almost certainly SEO copy written against a generic "business savings" query and never reconciled with the product.

What Rho never publishes is a positive list of accepted entity types. S-corps, partnerships, LPs, LLPs, trusts, Delaware public benefit corporations, holding companies, series LLCs, special purpose vehicles and DAOs are all unaddressed in 522 crawled pages. If you are anything other than a plain LLC or C-corp, you will find out by applying.

A narrower gate applies to Rho's own incorporation product, which is a separate thing from banking: "Rho Incorporation forms Delaware C-corps only," with "LLC formation is coming soon." Rho will bank an LLC but will not form one.

#### Geography, and the non-US founder question

This is the question most often asked and most often answered wrongly by third parties, so here is the exact language. The help center article "Can I Open a Rho Account if I Don't Live in the U.S.?" states:

> "Rho partners with Banks to offer accounts to business owners worldwide. However, entities must be incorporated in the United States, and either hold a US Operating Address or have one business owner based in the United States with a valid tax identification number (SSN)."

**Verified:** non-US founders of a US entity are eligible, provided that address-or-US-owner condition is met. Note that it is a disjunction: a US operating address **or** a US-based owner with an SSN, not both.

**Verified caveat:** Rho states this rule three incompatible ways. /product/incorporation makes it a conjunction ("At least one US-based owner or officer **and** a US operating address"). The Terms of Service say something different again and undefined: "Rho Services are only available to businesses **based in** the United States of America." Which governs a plain banking application is not resolved anywhere in the corpus.

Two further hard rules on geography:

- Virtual addresses are refused. "Is a Regus address permissible? Virtual addresses from Regus or any other provider are not permitted." The incorporation product requires "a physical U.S. operating address." This is the rule most likely to trip a genuinely remote-first founder who has a US entity and no US office.
- Owners resident in eight countries are ineligible to apply at all: Cuba, Iran, North Korea, Russia, South Sudan, Sudan, Syria and Venezuela. This is separate from, and shorter than, the roughly 40-country list of places Rho will not send payments to.

#### Ownership and identity

A UBO, or ultimate beneficial owner, is the human being behind a company that banks are legally required to identify. Rho's threshold is the US standard 25%.

| Requirement | Rho's wording |
| --- | --- |
| Beneficial owners | "Ownership information for anyone who owns 25% or more" |
| If nobody owns 25% | "you can add the person who exercises substantial control over the business instead (i.e. typically the CEO or financial officer)" |
| Photo ID | "A government-issued photo ID for each owner and signer" |
| SSN | Required as "one of several data points required for Rho to fulfill mandatory customer identification requirements" |
| Age | 18 or the age of majority in the state where the business is located |

#### Pre-EIN account opening

An EIN is the IRS-issued tax ID a US company needs before a bank can open its account, and waiting for one is the standard delay between incorporating and being able to receive money. Rho markets an escape from that wait.

**Rho says,** on /product/incorporation, re-fetched live 2026-09-11:

> "Can I open a Rho business account before my EIN arrives? Yes. Your Rho business account application can open in the same flow as incorporation, before your EIN arrives, subject to approval. Funds cannot move until the IRS issues your EIN and it attaches to your account. Non-VC-backed founders get a 30-day pre-EIN window before the EIN arrives; VC-backed founders get 60 days. Both require manual review, and neither is guaranteed."

**Verified,** with four qualifications that materially change what is on offer:

1. A pre-EIN account is not a usable account. Per /product/business-banking, an uploaded SS-4 (the EIN application form) "lets you start depositing" while "the EIN itself unlocks outgoing transfers." What day one buys is a deposit-only account.
2. The 30-day / 60-day split by VC backing is stated exactly once across 522 crawled pages, in a FAQ answer on /product/incorporation. It appears on no help-center page and in no Terms document. It is live as of 2026-09-11 but thinly sourced and unilaterally changeable. Do not treat it as a contractual commitment.
3. Rho's own help center contradicts the whole proposition: the EIN retrieval article states flatly "You'll need your EIN letter to join Rho."
4. It is not a differentiator. Rho's own comparison page describes its pre-EIN path as working "through incorporation integrations" (Rho, Stripe Atlas, Clerky), and Mercury offers the same thing through the same Stripe Atlas and Clerky partnerships (clerky.com and mercury.com partnership posts, both accessed 2026-09-11).

What happens at day 31 or day 61 with no EIN issued is not stated anywhere.

#### Documents, and how long any of it takes

KYB, "know your business," is the corporate half of the identity checks a financial institution must run before opening an account; KYC is the same for the individual people involved.

| Collected | From whom |
| --- | --- |
| EIN, or an uploaded SS-4 for a deposit-only account | The business |
| Formation documents (articles of incorporation or organization) | The business |
| Operating agreement | Multi-member LLCs specifically, "since it shows who can sign for the company" |
| Ownership details for anyone at 25%+ | The business |
| Government-issued photo ID | Each owner and each signer |
| Social Security number | Each individual applicant |
| 6 months of bank and accounting statements | Only for credit, or where data aggregation via Plaid, Finicity or Codat is unavailable |
| Business license, certificate of good standing, beneficial ownership forms | Treasury applications specifically |

Application mechanics are genuinely good: "The application takes less than 10 minutes," you can resume by re-entering the same email, and you can invite a teammate or a co-owner to fill in their own UBO section. File uploads cap at 10 MB.

**Assessment, and this is the most striking omission in the onboarding surface:** no page in the corpus states an approval SLA for the core checking account. Every adjacent product has one. Treasury is "up to 2 business days." Capital funds in "about 48 hours." Delaware filings complete within 24 hours for "roughly 80% of filings." The account itself gets only "Our team reviews what you've submitted and reaches out directly if anything else is needed." Rho markets aggressively against slow approvals elsewhere ("In practice, 'we'll be in touch' often means 5 to 14 business days before a decision lands," from its own comparison blog) while publishing no number of its own. The homepage's "Open an account in minutes" measures how long the form takes, not how long the decision takes, and the incorporation footnote says explicitly that the 24-hour figure "does not measure EIN issuance or account approval."

#### Prohibited and restricted businesses

There are two lists, they do not overlap, and neither cross-references the other. Neither is exhaustive.

**List A, the help center** ("certain high risk businesses may also be prohibited, such as the following industries"), 13 entries: betting and casino gaming chips; adult dating and escort services; drug stores, pharmacies and cannabis; drugs, proprietaries and sundries; stamp and coin stores; quasi-cash, currency, money orders and travelers checks; pawn shops; bearer shares; bail and bond payments; currency exchange businesses; nested MSBs and nested money transmitters (a money services business operating through another MSB's bank account); firework sales; online dating services.

**List B, the Terms of Service glossary definition of "Prohibited Activity,"** 46 entries and materially broader. The ones a normal technology or services business would not expect:

| Clause | Why it matters |
| --- | --- |
| "bill payment services" | Would exclude a large class of fintechs, on the same platform that sells a Bill Pay product |
| "payment aggregators" | Same |
| "real estate or motor vehicles" | Read literally, excludes brokerages, property managers, dealerships and proptech |
| "medical equipment" | Excludes a whole medtech category |
| "legal fees including bankruptcy attorneys" | Excludes at least part of legal services |
| "live animals" | Excludes petcare commerce |
| "digital goods regulated as securities or derivatives and digital currencies" | The closest thing to a crypto exclusion; crypto exchanges and custodians are never named |
| "weight loss programs" | Excludes a visible direct-to-consumer (DTC) category |
| "using the Rho Services in an automated manner" | Narrowed by a separate carve-out permitting Rho's own AI features and integrations |

**Assessment:** List B is boilerplate card-network and sponsor-bank language that Rho has clearly not reconciled with its own product or its own customer base. Rho's published case studies include a freight broker, several consumer-goods brands and a govtech firm, and Rho sells a bill payment product. Treat List B as the enforcement option Rho holds in reserve rather than a description of who gets declined. The practical exclusions are the help-center list plus whatever the sponsor bank's underwriting declines that week. Neither published list is the operative policy, and Rho publishes no decline reasons, no appeal process and no re-application rule.

Also conspicuously absent from both lists: firearms dealers by name, defense contractors, political campaigns and PACs, staffing and PEO firms (professional employer organisations, which co-employ a client's staff), debt collection, telemedicine, payday lending, ATM operators and shell or holding companies with no operations. And there is no revenue minimum, no funding-stage minimum, no headcount minimum and no time-in-business minimum stated anywhere for the core checking account.

### 5.2 The ideal customer profile the money describes

Rho's navigation sells four segments by size and industry: Startups, Small Businesses, Enterprises, Accountants, plus Consumer Brands. The product does not vary between them. What varies is the hero line, which three or four products get top billing, the testimonial, and which treasury instruments are named. No segment page discloses segment-specific pricing, limits, onboarding timelines or features.

The real segmentation is visible in two places Rho does not advertise: the partner microsites, where it spends money to acquire customers, and the case studies, where it documents who actually switched.

#### The partner microsites

Rho runs 77 pages at /partner/*, one per accelerator, venture fund, incubator, community or SaaS partner, each carrying a cash-and-goods offer with its own qualification terms. They are absent from Rho's own navigation (rho.co and rho.co/partners contain zero links to them) and absent from site-llms.txt, Rho's machine-readable site index.

**Verified:** they are unlinked, not unindexed. All 77 appear in rho.co/sitemap.xml (1,042 entries total, fetched live 2026-09-11) with self-referencing canonical tags, no noindex tag, and a robots.txt reading "Allow: /".

**Verified,** from a complete census of all 77 pages taken 2026-09-11, banding each page at the highest balance figure in its binding terms footnote:

| Required average daily checking balance | Pages | Share |
| --- | --- | --- |
| $400,000 or $500,000 | 25 | 32.5% |
| $100,000 to $300,000 | 11 | 14.3% |
| $50,000 or less (22 of them at $20,000, one at $10,000) | 25 | 32.5% |
| No balance threshold stated | 16 | 20.8% |

"Average daily checking balance" means what it says: the average of your end-of-day balance over the qualifying window, usually 60 or 90 days. The ladder is continuous, not barbelled. A middle tier exists at $100,000 (Savant Ventures, GoAhead, Profluence, Sweet Spot Capital), $200,000 (Wavefunction), $250,000 (doola's upper tier) and $300,000 (E14, Pillar, Quake Capital, Workhouse, Endurance).

The condition that does not vary is payroll. It appears on 56 of the 77 pages, including all 25 of the $400K-$500K pages, in language like Drive Capital's: qualify by maintaining the balance, "(2) use your Rho account for your company's payroll, (3) complete a payroll transaction, and (4) continue to use your Rho account as your primary business banking account." Deposits alone never qualify.

The 16 pages with no balance threshold are not all offer-free. /partner/ycombinator gates a $10,000 package on a milestone ladder instead: $5,000 for opening and depositing the YC investment, $2,500 for connecting and running payroll, $2,500 at $10,000 of cumulative card spend. The balance test is gone; the payroll test is not.

**Assessment:** the offers price a customer at roughly 0.8% to 1.25% of the qualifying balance over a 60- or 90-day window, paid up front, which annualises to roughly 3% to 5% on the 90-day pages and about 6% on the 60-day ones. The two $10,000 milestone ladders price higher still: Y Combinator's is 2% of a $500,000 check over 90 days, HF0's is 2.5% of $400,000 over 60. That is at or above the entire net interest margin on that money for a year. Rho is not buying float (the interest a platform earns on customer cash simply by holding it), it is buying the primary operating relationship, and it is buying it hardest from venture-backed companies immediately post-round. A separate signal points at the same number: Rho's own /versus/ramp page claims "More than 8,000 businesses with $4B+ in deposits run on Rho," which is exactly $500,000 per business. The partner thresholds are set at Rho's own average account size.

#### What the case studies actually show

Rho publishes 14 customer case studies. Its comparison content is built overwhelmingly against Mercury, Ramp and Brex.

**Verified:** zero of the 14 case studies mention Mercury or Ramp. The systems customers actually named leaving:

| Displaced | Case studies |
| --- | --- |
| SAP Concur (legacy travel and expense software) | InnoMark, Dr. Squatch, Native Strategies, Willet + Cumro (4) |
| A legacy or large bank, unnamed | Anti Agency, Polimorphic, Mad Rabbit, Nexxa (4) |
| Silicon Valley Bank, post-collapse | Superfiliate, MUD\WTR, Dr. Squatch (3) |
| Excel and manual process | Native Strategies, Willet + Cumro (2) |
| Expensify, Bill.com, Brex, Divvy, Capital One, American Express, Tipalti | 1 each |
| Mercury, Ramp | **0** |

Seven of the 14 name no prior vendor at all.

**Verified, with the overstatement corrected:** the claim that Rho's entire comparison library is built around Mercury and Ramp is too strong. Mercury or Ramp appear in the URL of 22 of 125 comparison blog pages (17.6%), 17 of the 57 head-to-head "X vs Y" posts (29.8%), and 2 of the 8 /versus/* pages, the others being Amex, Bill, Brex, Chase, HSBC and SVB.

**Assessment:** Rho's marketing fights the neobank peer set (neobank: a software company that offers a bank-like account through a sponsor bank without holding a charter itself, which is what Mercury, Brex and Rho all are) and its sales wins come from legacy travel-and-expense software, regional and large banks, and companies displaced by the SVB collapse of March 2023. Those are different buyers. The neobank buyer is a founder choosing a first bank account. The Concur buyer is a 25-to-200-person company with a controller, an existing bank it may not want to leave, and a painful expense-report process. Rho's product is genuinely strong for the second, and its own case study evidence says so. Note also that several case studies are visibly dated: only two of the 14 read as recent, and the two paid brand ambassadors among the subjects are disclosed as such.

#### The ideal customer profile, stated plainly

Synthesising the offer census, the payroll condition, the $500K average account size, Rho Platinum's requirement that 50% or more of company assets sit at Rho, and the case-study displacement pattern:

> A US-incorporated, venture-backed or profitably-growing company holding roughly $400,000 to $500,000 or more in operating cash, willing to run payroll and revenue collection through Rho as its primary bank, with 10 to 200 employees, a finance function of zero to three people, and QuickBooks Online or NetSuite as its ledger.

Secondary, in descending order of evidence: multi-entity mid-market operators (5 of 14 case studies are multi-entity or holding companies), direct-to-consumer and consumer packaged goods (CPG) brands (the only vertical with both a segment page and four-plus case studies), accounting firms as a distribution channel rather than a segment, and venture funds as a distribution channel wearing a segment costume (/fund-banking is fully built, has its own FAQ, and appears nowhere in the navigation).

**Assessment:** Rho is not running a segment strategy. It is running a deposit-acquisition strategy with segment-shaped landing pages. The tell is that the product is identical across segments while every incentive in the corpus, without exception, is priced on deposit balance and payroll primacy rather than headcount, revenue, industry or card spend.

### 5.3 Practical fit guide

| Profile | Fit | What they get | What will frustrate them |
| --- | --- | --- | --- |
| Pre-incorporation founder, no entity yet | Good, with conditions | Delaware C-corp filed in about 24 hours for 80% of filings, attorney sign-off, SS-4 submitted, $400 fee credited back on a $10,000 new-money deposit held 60 days; a deposit-only account before the EIN lands | C-corp only, no LLC formation; the $400 refund requires new money and a balance $10,000 above where it started, not just a $10,000 balance; no approval SLA; if you are not incorporating in Delaware, this path does not exist |
| 5-person startup, seed-funded, $500K in the bank | Excellent, and Rho will pay you | Fee-free checking, corporate cards with no personal guarantee, Treasury from a $50,000 minimum, and a partner offer worth $4,000 to $10,000 if you arrived through one of the 77 microsites | Every offer requires payroll primacy and a 60-to-90-day balance lock; Platinum 2% cashback needs 50%+ of company assets at Rho; no cash deposits ever |
| 50-person startup with a controller | Excellent, the sweet spot | Free unlimited seats, approval chains, expense rules, AP, invoicing, NetSuite or QuickBooks sync, and the Concur or Expensify line item disappears | Google sign-in is the only way to connect a company identity system, so there is no support for the enterprise standards (SAML for single sign-on, SCIM for automatically creating and removing user accounts) that Okta and Microsoft Entra use; no documented audit-log export; support availability and response times are claimed three different ways on three pages and measured nowhere |
| 200-person multi-entity company | Good on function, one buried risk | Multi-entity switching in one login, documented in case studies up to 10 brands; the segment where Concur and Amex displacement actually happens | ToS §17 cross-guaranty makes every Rho entity in a parent-subsidiary chain "absolutely, unconditionally and irrevocably" liable for the others' obligations, and it is mentioned on no multi-entity marketing page; whether roles are per-entity or global is never stated; no case study exceeds 1,000 employees |
| Agency or consumer brand | Strong, and best-evidenced | Four consumer-brand case studies, a dedicated segment page, yield on cash between production and payback, and vendor cards for ad-account spend | ToS Prohibited Activity language ("real estate or motor vehicles", "weight loss programs", "live animals") is broad enough to catch adjacent categories; retail-heavy brands with physical cash are excluded outright |
| VC or PE fund | Built, but undocumented | /fund-banking offers per-entity accounts for fund, GP and management company under one login, named integrations with Carta, Juniper Square, NAV and five other fund admins, and up to $75M FDIC capacity per entity on savings | The page is not in the navigation; there is no fund customer, AUM figure or case study anywhere in the corpus; the deal-flow and LP-introduction offer is a barter Rho never prices |
| Accounting or CAS firm | Channel, not customer | Partner Portal for client oversight, in-house CPAs, referral reciprocity, co-marketing, and "custom incentives and preferred rates for your firm and clients" | That last phrase is the only admission in the entire corpus that pricing is negotiable, and it contradicts the sitewide "no platform tiers" line; no revenue share, rebate or portal pricing is published anywhere |

### 5.4 The anti-fit cases

These are structural, not preferences. If you are in one of them, no amount of product improvement inside Rho's current shape fixes it.

**Businesses that take physical cash.** Rho has no branches, no ATM network and no cash deposit path of any kind. Rho concedes this in its own words on its Bank of America comparison page (published 2026-09-02): "Rho doesn't support cash deposits at all," and BoA's free cash allowance is "real, tangible value that a fully digital platform simply can't offer." On its Chase page: "If you take meaningful physical cash, keep a Chase account for it." **Assessment:** this is the cleanest disqualifier in the product, it is honestly disclosed, and it eliminates restaurants, retail, personal services, and most of what "small business" means outside technology.

**Entities incorporated outside the US, and businesses that need to hold foreign currency.** The incorporation requirement is absolute, and it is separate from the founder-residence question answered in 5.1. Beyond eligibility, Rho holds USD only: every account balance in the API sandbox returns `"currency":"USD"`, and foreign currency exists only as a transmission step through Wise US Inc. at a 1% conversion fee plus an optional $15 SWIFT fee. There are no local-currency accounts, no multi-currency balances, and roughly 40 countries where payments are blocked entirely. A company with a UK subsidiary paying UK staff needs another provider for that entity, and Brex is the platform that sells multi-entity international as a product tier.

**Sole proprietors and unincorporated businesses.** Excluded, despite Rho publishing an SEO page ranking itself "#1... for Digitally-Native Sole Proprietors Who Plan to Scale" and despite its own savings page saying twice that sole proprietors are eligible. Incorporate first, or go elsewhere: Rho's own comparison content says "a sole proprietor without employees can open a Novo business checking account using an SSN instead of an EIN" and names Found the "best free back office for sole proprietors."

**Anyone who needs to initiate payments programmatically.** The Rho API, launched 2026-08-03 per the changelog, has 14 operations, all GET, across five resources. Every write method on every path returns 405 Method Not Allowed. Rho states it plainly: "Rho API access tokens are read-only and scoped to account and transaction data. Tokens cannot initiate payments or modify accounts... The Rho API is read-only today." The same applies to the MCP server, which exposes the same read surface to AI agents: the help center's list of what connected AI tools cannot do is "Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account." Rho's own competitive blog concedes the point: "Mercury's API is the most mature overall (read and write)... If you want agents moving money today, those do more." Two further limits matter here. Tokens are scoped to a single business, so a multi-entity company cannot query across its entities with one credential. And Rho's OAuth server (OAuth is the standard that lets you grant one application limited access to your account at another, without handing over your password) at auth.rho.co returns "Dynamic registration is not enabled," so a third-party MCP client cannot self-register; integration happens on Rho's terms or not at all. **Assessment:** if your finance automation requires initiating a payment from code, Rho is a reporting source, not a platform. Section 7 covers the API surface in detail.

**Companies that need real travel and expense management.** Rho has reimbursements, mileage with an embedded map, receipt capture, expense rules and approval chains, and for a US-domestic team that is often enough to retire Concur or Expensify, which is exactly what four of its case studies did. What it does not have is a managed travel program: no booking engine, no negotiated fares, no price-drop rebooking, no group travel rules, no VAT documentation, no global reimbursements in local currency. Rho says so itself on /versus/brex: "No managed travel program comparable to Brex's," and, in the same page's recommendation block, "Large companies running global spend programs: Brex. This one goes to Brex... Travel-heavy teams: Brex." Its published mileage tooling is also visibly stale: the public mileage calculator still presents 2024 IRS rates while the in-product default is $0.70 per mile, and no 2026 rate appears anywhere in the corpus.

**A note on the pattern in these concessions.** Rho concedes loudly and accurately on exactly the axes where it does not sell a product: branches and cash, managed travel, agent write-access, venture debt. Those concessions buy real credibility, and they are the most trustworthy competitive statements in Rho's corpus. They are also, read together, a precise map of the product's boundary. Sections 8 and 9 test how the same competitors hold up when they are the ones describing themselves.
## 6. The API and the agent surface

Everything in this section is as of 2026-09-11. It is the executive view: what Rho shipped, what the pieces mean, and where the wall is. The mechanics (every field of every response, the cursor pagination rules that govern how a client walks a long list one page at a time, the error contract, the sandbox probe logs, the client code) live in the separate Rho API reference document that accompanies this dossier. If you never open that document, this section is designed to leave you with an accurate picture anyway.

### 6.1 What shipped, and when

Rho had an API in private beta before 2026. The public launch has two dates, five days apart, because Rho announced it twice.

| Date | Artifact | What it said |
| --- | --- | --- |
| 2026-07-29 | Blog, "Introducing: The Rho API" (last updated 2026-09-01) | "Today, we're bringing the Rho API out of beta" |
| 2026-08-03 | Product changelog entry | "Read-only is live today. Write access and webhooks are next." |

**Rho says** the API is available to every customer with no waitlist and no approval step, at no additional cost, and that "Most financial APIs predate agents; MCP got bolted on. This one shipped with its MCP server in production. Not a roadmap item, the architecture."

**Verified:** the API exists, the documentation is public at docs.rho.co, the OpenAPI specification is published (the machine-readable file describing every endpoint, which code generators read), the production MCP endpoint responds, and a sandbox with fictional data answers unauthenticated-in-practice requests. I exercised all 14 operations against the sandbox directly.

### 6.2 The whole surface fits in one table

There are 14 operations. All 14 are GET, the HTTP verb that only retrieves data and never changes it. They cover 5 resources.

| Resource | Operations | What you get |
| --- | --- | --- |
| Accounts | 2 (list, get one) | Name, type (checking, credit, investment, savings, rewards), balance, and the last 4 of the account and routing number on 8 of the 14 sandbox accounts (the other 6, all credit and rewards accounts, carry neither) |
| Cards | 2 (list, get one) | Cardholder name, last 4, physical or virtual, status, spending limit and limit period, current and pending spend, billing and shipping address, merchant-category allow and block lists |
| Transactions | 3 (list, get one, get an attached file) | 33 transaction types, signed amounts, status, counterparty name, employee and card attribution, memo and note text. A `tracking_number` field carrying the ACH trace or wire IMAD/OMAD reference is documented in detail but returned on zero of the sandbox's 72 transactions |
| Statements | 2 (list, get one) | Period, opening and closing balance, total credits, debits and fees, and a signed PDF link valid for about 15 minutes |
| Invoicing | 5 (customers list and get, invoices list and get, invoice file) | Customer legal name, email, cc emails, postal address, lifetime revenue; invoice number, status, dates, amounts |

For scale, the public sandbox holds 14 accounts, 8 cards, 72 transactions, 33 statements, 7 invoicing customers and 12 invoices of fictional data. That is the whole test corpus.

A scope is a named permission string attached to a credential, checked before the request reaches the handler. There are five, one per resource, all ending in `:read`: `accounts:read`, `transactions:read`, `statements:read`, `cards:read`, `invoicing:read`.

**Verified:** five scopes, confirmed independently of the docs from Rho's public OAuth metadata document at `https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1`, which lists all five.

**Assessment:** the documentation understates its own product in two places, and both errors point the same way. Rho's Authentication guide at /docs/v1/auth still lists only three scopes in its "scopes available today" table, omitting `cards:read` and `invoicing:read`. Rho's Getting Started page still says the release "covers accounts and transactions" when the reference ships five resources. Anyone sizing the blast radius of a token from the Authentication page alone will underestimate it by the entire Cards and Invoicing surface, which includes employee cardholder names and the postal addresses and emails of the customer's own customers. That is a documentation defect, not a security hole, but it is the kind of defect that matters most: the page a security reviewer reads is the page that is wrong.

There is also no sub-scope granularity. `transactions:read` means the entire ledger for the entire business, for all time. There is no per-account scope, no date-window scope, no amount ceiling, no field redaction.

### 6.3 Two ways to hold a credential

**API Access Tokens (the `rhobat_` model).** A long-lived opaque secret scoped to one business, created in Rho's settings by an Account Owner or Admin behind a two-factor challenge, shown exactly once. It looks like `rhobat_` followed by 62 hex characters. A business may hold at most 20 active tokens. Expiration is mandatory at creation with a one-year maximum, and a token also dies automatically after 45 days of no use. An optional IP allowlist (up to 100 entries) rejects requests from anywhere else. Revocation is immediate and irreversible. No other authentication method is supported: no cookies, no API keys, no signed requests.

**Partner OAuth.** OAuth is the standard "sign in with" mechanism: instead of handing a third-party app your password, you approve it at Rho's own login screen and the app receives a short-lived token limited to what you approved. For a third-party application acting on behalf of Rho customers, Rho runs an OAuth 2.0 authorization server at auth.rho.co using the Authorization Code flow with PKCE (a standard technique that stops an intercepted authorization code from being redeemed by an attacker), method S256. Access tokens expire after 15 minutes, refresh tokens rotate on every use and last 30 days on a rolling basis, and the underlying customer grant lasts one year before re-approval is required. Only Account Owners and Admins can approve a connection, and one business can hold at most one active grant per app.

**Verified:** auth.rho.co's authorization-server metadata document publishes no `registration_endpoint`, and under RFC 8414 the absence of that field is how a server signals it does not offer dynamic client registration. A registration attempt recorded in an earlier probe pass returned "Dynamic registration is not enabled"; that `POST` was not re-sent for this document, because writing to a production authorization server is not a metadata read. Dynamic client registration is the mechanism by which a generic client self-registers with an authorization server it has never met.

**Assessment:** this is the single most consequential undocumented fact about the developer surface. Every OAuth client must be hand-registered by emailing api-partner-request@rho.co with a logo, redirect URIs, a privacy policy and a terms-of-service link. The generic MCP authorization flow that arbitrary clients implement therefore cannot complete against Rho. That is why Rho's own documentation hedges with "Linked-app availability depends on the client" and why every marketing page names Claude as "the natively supported client today." In practice a non-Claude client gets the static token path or nothing. Note that this is a business decision as much as a technical one: gating registration is how Rho keeps a list of who is reading its customers' bank data, which is a defensible posture for a regulated-adjacent company, but it does mean "works anywhere MCP does" is stronger marketing than the auth server supports.

### 6.4 MCP, and Rho's MCP server

If you have not met it: the Model Context Protocol (MCP) is an open convention, introduced by Anthropic in late 2024 and now implemented broadly, for letting an AI assistant call someone else's software. A company runs an "MCP server" that advertises a list of tools, each with a name, a description and a typed input schema. An AI client connects, reads the list, and from then on the model can decide to call `listTransactions` the way a person would click a button, feeding the result back into its own reasoning. The value is that the company writes the integration once instead of once per assistant, and the user connects by authorizing a connector rather than by writing code. The risk is symmetrical: whatever the tools can do, an AI acting on ambiguous instructions can now do too.

Rho's MCP server runs in production at `https://rhoapi.rho.co/mcp/v1` over Streamable HTTP (one HTTP endpoint, JSON-RPC messages in a simple request-and-reply format, optional streamed responses). Rho states parity is one-to-one with REST, the ordinary web API that serves the same endpoints: the same 14 operations, the same five scopes, the same error behavior, with tool names derived from the frozen operation identifiers so that "tool names will never change." Rho is listed in Anthropic's connector directory, so a Claude user connects by searching for Rho, signing in, picking a business and approving scopes.

**Claude Code setup**, the only code snippet on Rho's MCP page, reproduced exactly:

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

**Verified:** the command works. `--scope project` writes the literal token, in plaintext, into `.mcp.json`, the project config file whose entire purpose is to be committed to version control and shared with a team.

**Assessment:** put Rho's two pages side by side. The Authentication guide: "Store tokens in a secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, 1Password, etc.), never in source control, CI logs, or shared documents." The MCP guide's only copy-paste command: writes a bearer token valid for up to a year into the file designed for git. The page with the command is the one people will follow. The fix is trivial (use `--scope user`, or a `${RHO_API_TOKEN}` placeholder in single quotes resolved from the environment) and Rho does not mention it.

Two further gaps are worth stating plainly. First, Rho publishes no tool list, no input schemas and no prompt or resource inventory for the MCP server, telling you instead to introspect it yourself with your client or MCP Inspector. It simultaneously promises the tool names are frozen forever and declines to tell you what they are. Second, **verified by direct probe: the sandbox host has no MCP endpoint. `POST https://rhoapi-sandbox.rho.co/mcp/v1` returns 404.** MCP exists only in production, so the first time you connect an agent to Rho over MCP, it is connected to real money data.

### 6.5 Rate limits

| Limit | Value |
| --- | --- |
| Per API Access Token | Approximately 60 requests per minute |
| Per source IP | Approximately 600 requests per minute, pooled across all tokens on that IP |
| Over-limit response | `429 Too Many Requests` with a `Retry-After` header; if `Retry-After` is 0, use exponential backoff (wait, then wait twice as long, and so on) |
| Guidance | "Pace traffic steadily below one request per second" |
| Page sizes | Default 20 and maximum 100 on all six list endpoints, measured. Rho's own reference pages state only the max for accounts, transactions and statements, and only the default for cards and invoicing |

**Verified:** I issued roughly 430 requests to the sandbox over about ten minutes, including a 150-request burst on one token inside 57 seconds and a 65-request burst on a brand-new token inside 11 seconds. Every response was `200`. No limit was enforced and no `429` was reachable. Separately, none of the 14 operation reference pages documents a `429` response at all; they document 200, 400, 401, 403, 500 and 503, plus 404 on the eight single-object operations.

**Assessment:** two practical consequences. You cannot test your retry code against Rho's own test environment, because the sandbox will not produce the error the docs tell you to handle. And a code generator fed Rho's OpenAPI document produces a client with no `429` case, which you must add by hand. The limits themselves are unremarkable for a read API, but they do shape agent behavior: pulling a year of a busy ledger at 100 rows per page and 60 requests per minute is roughly 300 sequential calls and several minutes of wall clock, with every raw row passing through the model's context, because Rho offers no server-side aggregation, summary or rollup tool.

### 6.6 The capability boundary

This is the part to remember. Every write answer is no, and it is no structurally rather than by policy: there are no non-GET operations in v1 to call.

| Can a connected agent... | Answer | Notes |
| --- | --- | --- |
| Read account balances and types | Yes | All accounts in one call, up to 100 per page |
| Read the full transaction ledger | Yes | 33 transaction types, all history, rich filters |
| Read card metadata and controls | Yes | Last 4 only; the full card number, the CVC security code and the expiry date are never returned |
| Read statements and fetch statement PDFs | Yes | Via short-lived signed links |
| Read invoicing customers and invoices | Yes | Includes third-party customer names, emails and addresses |
| Move money (ACH, wire, check, transfer) | **No** | No endpoint exists |
| Issue, lock, edit or cancel a card | **No** | No endpoint exists |
| Add, remove or manage users | **No** | No endpoint exists |
| Approve a payment or a bill | **No** | No Bill Pay or approvals endpoints at all |
| Receive a webhook (a push notification from Rho when something happens) | **No** | Rho's own comparison table says "Not yet" |
| Read an audit log of its own API activity | **No** | Nothing documented anywhere |

Rho's help center states the boundary in four words per line: connected AI tools cannot "Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account." The product page footnote, as of August 2026: "The Rho API is read-only today."

**Assessment:** the read-only claim is unusually credible because it is verifiable from the published OpenAPI index rather than taken on trust. It is also explicitly temporary. The launch blog: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval, the finance tasks you'd rather delegate. Read ships first because everything else stands on it."

One boundary the read-only design does not cover: read-only protects Rho, not the agent's environment. A finance agent typically also holds email, Slack, a shell or a write-capable MCP server from another vendor, and Rho's transaction `memo`, `note` and `counterparty_name` fields are free text that arrives from outside. Rho's documentation contains no mention of prompt injection (an attacker writing instructions into a field such as a payment memo, in the hope the AI reading it treats them as commands) or untrusted-content handling.

### 6.7 Where Rho sits on the agentic-banking timeline

Rho's framing is that MCP is now table stakes and Rho shipped it as architecture rather than as an afterthought. The dates below are all confirmed against primary sources.

| Date | Who | What |
| --- | --- | --- |
| 2025-03-25 | Ramp | First MCP release (an open-source Python package, not the hosted server buyers connect to today) |
| 2025-05-29 | Griffin | "The Agentic Bank": an agent can "open accounts, make payments, and analyse historic events." UK PRA/FCA-authorised, not US. Sandbox-only at announcement ("For now, agent access is limited to our sandbox environment") and still listed as beta in September 2026 |
| 2025-08-20 | Narmi and Grasshopper | Announced as the first MCP server by a US bank. Read-only, and a controlled beta at launch with general availability planned for Q4 2025 |
| 2025-09 | Coinbase | MCP server, read and write, can make payments |
| 2025-11 | Mercury | MCP server, read-only |
| 2026-04 | Brex | MCP server, roughly 41 tools (~37 read, 4 low-risk write), no money movement |
| 2026-04 | Meow | Agent-initiated payments, behind an initiator-and-approver workflow |
| 2026-04-09 | Nymbus | 19 tools including money movement, sold to US banks and credit unions |
| 2026-07-01 | Navan | MCP server, read-only |
| 2026-07-14 | Grasshopper | First bank listed in Anthropic's connector directory. Read-only, no money movement |
| 2026-07-29 | Rho | "Introducing: The Rho API" |

**Verified:** the openbankingtracker first-party directory, read live on 2026-09-11, lists 10 bank or banking-platform MCP servers worldwide: 5 live and 5 in beta, 5 read-write and 5 read-only, with 4 able to make payments (Griffin, Coinbase, Meow, Slash). That is against roughly 4,000-plus US banks and a similar number of credit unions. Rho does not appear in that directory at all.

**Verified, and the most important line in this section:** no vendor offers ungated autonomous money movement. Every money-moving agent surface in the field is wrapped in a narrower primitive: Ramp's Agent Cards are scoped to a merchant and an amount, Stripe attaches a `human_confirmation` object to its execute and refund tools, and Meow routes agent payments through an initiator-and-approver workflow.

**Assessment:** the "table stakes" framing holds within Rho's own competitive cohort and only there. Against startup banking and spend management (Mercury, Brex, Ramp, Meow, Slash, Navan, Coinbase), every named comparator shipped MCP before Rho and roughly half now support some write, so Rho is late on both date and surface. Against US banking at large, 10 servers against thousands of institutions is not table stakes by any reading, and Rho is not even on the list that counts them. What Rho is genuinely not behind on is agentic payments, because nobody has solved that: the frontier is gated, scoped, human-approved money movement, not autonomy.

One caution for anyone using Rho's own materials: Rho's comparison table on rho.co/product/api, dated "as of 2026-08-20," claims Brex has "No MCP or AI-assistant integration documented on developer.brex.com." Brex's changelog dates its MCP server to April 2026, and Rho's own blog five days later, on 2026-08-25, reverses the claim. Do not cite Rho's competitive table as evidence for anything.

### 6.8 Why read-only is a defensible choice

Taken on its merits, the case is strong.

The blast radius of a leaked credential is bounded by physics rather than by policy. A stolen `rhobat_` token reads everything and moves nothing, and that property survives a bug in Rho's own authorization logic, because the write code path does not exist. Rho's own framing is honest about this: "a leaked token cannot move money."

It also sidesteps the hardest unsolved problem in the category. An agent that can move money needs an approval model, an idempotency model (so a retried instruction does not pay a vendor twice), a limits model, a reversal path and an audit trail that a regulator will accept. Shipping reads first and getting the data model right, then building writes on top, is the order a careful team would choose. Every competitor that does support writes has arrived at the same conclusion in practice by wrapping them in gates.

And it lowers the cost of saying yes. Because nothing can be broken, Rho can give API access to every customer with no waitlist, no approval step and no fee, which is materially more open than banking APIs that gate access behind a partnership review.

### 6.9 What it costs

The bill comes due in four places.

**Automation stops at the read boundary.** The natural next sentence after "our AWS spend is up 40%" is "so freeze that card," and the agent cannot. Every workflow terminates in a human opening the Rho dashboard. That is a real ceiling on the "delegate the finance busywork" promise the launch blog makes.

**No webhooks means no event-driven anything.** Without a push notification when a transaction posts, every integration is a polling loop against a 60-requests-per-minute budget. Alerting, reconciliation triggers and approval routing all become scheduled jobs with latency measured in minutes.

**Coverage of the platform is thin, not just the verbs.** Read access reaches five resources. Bill Pay and accounts payable, expense management, receipts and coding, users and roles, departments, treasury positions, capital draws and disputes have no endpoints at all. Transactions carry a `user_id` and a `user_full_name` with no user directory to resolve them against. So even as a pure read API, this is perhaps a quarter of the product.

**Competitively, read-only is the weaker half of a two-sided pitch.** Rho's differentiation is that it runs banking, cards, payables and receivables on one ledger (covered in the product and business-model sections above). An agent that can read all of that at once is genuinely useful and is Rho's best agentic story. But Mercury's API initiates ACH transfers, Brex's Payments API sends ACH, wires and checks, and Ramp's API creates bills, executes payments and issues cards, all facts Rho itself lists in its own comparison table. Rho turns that gap into a security feature, which is a legitimate move and probably the right one for a company its size. It is still a gap, and the moment Rho ships gated writes, the security argument it is making today becomes an argument against its own roadmap.
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
## 8. Where Rho actually differentiates

The test used throughout this section is not "does Rho have it" but "could a named competitor ship the same thing within a year, and what would it cost them to do so." A feature that is a number in a configuration file is not a differentiator. A feature that requires a competitor to give up a revenue line they have already built a sales motion around is. Everything below is dated, because most of it can change in a quarter.

### 8.1 The genuine differentiators

| Differentiator | Size of edge | Who it beats | Who it does not beat |
|---|---|---|---|
| No software fees, no paid tier at all | Real and structurally costly to copy | Ramp, Brex, Mercury, BILL, SVB, Chase | Nobody in this set matches it |
| 24/7 human support with phone on every account | Real, staffing-driven | Mercury (no phone at any price), Ramp (phone gated to paid tiers) | Brex, which offers 24/7 phone on its free plan |
| $50,000 Rho Treasury minimum | Real but narrow | Mercury ($250,000 minimum) | Brex, whose treasury fund has no minimum |
| AP automation included and settling from the deposit account | Real on price, thinner on capability | BILL, Tipalti, SVB, Chase Cashflow360 | Mercury and Brex, which also include bill pay free |
| Pre-EIN and day-zero onboarding, free incorporation | Narrow and conditional | Most banks | Mercury, which offers pre-EIN through the same partners |
| Comparison pages that name where competitors win | Real, and rare | Almost everyone | Only the five rewritten pages qualify |

#### No software fees anywhere, and no tier to be upgraded into

Rho says: the published fee summary on rho.co/pricing has seven rows, six of them $0 (same-day ACH, wires and checks; subscription fees; checking minimums; "AP, Expense & Accounting Automation"; per-user fees; domestic wire recall) and one nonzero row, "Foreign currency transfer 1%."

Verified: there is no paid tier anywhere in the 522-page corpus. Not a Plus, not a Pro, not an Enterprise SKU with a price. Every competitor in Rho's stated set has one.

| Vendor | Free tier | Paid tiers (as of the dates Rho cites, Aug to Sep 2026) |
|---|---|---|
| Rho | Everything | None exist |
| Ramp | Substantial | Plus $15 per user per month plus an undisclosed platform fee; Enterprise custom; Procurement is an add-on even on top of Plus |
| Brex | Essentials $0 | Premium $12 per user per month; Enterprise custom |
| Mercury | Free | Plus and Pro, published by Rho as both $35/$350 and $29.90/$299 on different pages |
| BILL | None | $45 to $89 per user per month, depending on which Rho page you read |

Assessment: the reason this is harder to match than it looks has nothing to do with engineering. For Ramp, Brex and Mercury, the paid tier is not only revenue, it is the mechanism that partitions the product. Rho's own research on Ramp identifies exactly what forces the upgrade: NetSuite and Sage Intacct connectors, multi-entity, audit log, single sign-on, batch payments, custom roles, approval routing rules, guest travel and procurement. A competitor who matches Rho's posture has to unbundle a feature ladder that sales compensation, packaging and roadmap are all built around. Rho never built one, so it has nothing to give up.

The counterweight is that "free" describes the invoice, not the relationship. Rho Treasury charges an annual advisory fee tiered from 0.60% under $2M down to 0.15% above $20M, computed on assets under management that the help center defines as "the combined balance of your Rho Checking and Treasury accounts." No page in the corpus says plainly whether that means the fee is charged on checking cash or only that checking counts toward the tier that sets the rate. The fee is optional in the sense that the product is: a company that parks $2M in checking and never opens Treasury pays nothing. A company that does open Treasury pays close to $12,000 a year just under the $2M breakpoint at 0.60%, or $9,000 at $2M once the 0.45% tier applies. Either figure exceeds a 25-seat Ramp Plus subscription ($4,500) or a 25-seat Brex Premium subscription ($3,600), though the comparison is not like-for-like: the advisory fee buys discretionary investment management, while the seat fees are mandatory software charges. Foreign-currency transfers cost 1%. And the highest cashback rate, Rho Platinum at 2%, requires four things at once: payroll run from Rho, business revenue deposited via Rho Checking, an open Rho Corporate Card, and 50% or more of company assets held at Rho. The published price is near zero; the actual price is the balance sheet.

#### 24/7 human support, phone included, on a $0 account

Rho says: "24/7 human support (phone, chat, SMS), every account, every tier," at 1-855-7-GETRHO, with iMessage and WhatsApp added in June 2026.

Verified: Mercury advertises no phone support on any plan, including its Pro tier at $350 a month month-to-month ($299 on annual billing), offering only email and in-app messaging. That was confirmed independently against Mercury's own pricing, contact and support pages on 2026-09-11. Ramp publishes a support phone number in its footer but marks 24/7 phone support as a Plus and Enterprise row in its pricing table; the free tier gets 24/7 chat and a 24/7 AI assistant. Brex's own support documentation at brex.com/support/contact-and-support, fetched directly on 2026-09-11, lists 24/7 live support by chat, email, phone, SMS and WhatsApp for all customers with no plan gate; Premium adds dedicated support specialists for admins and bookkeepers within business hours, and Enterprise adds VIP support by email, phone or scheduled Zoom from 5am to 5pm PST. That is Brex's documentation, not Rho's comparison table, which this dossier does not treat as evidence about competitors.

Assessment: this is the cleanest verified win in the set, and it is a staffing decision rather than a technical one, which is why it has survived. It is also narrower than Rho's marketing implies in two ways. First, Brex already matches it, so the correct claim is "Rho and Brex have phone support and Mercury and free-tier Ramp do not," not "nobody else does." Second, Rho's own pages disagree with each other: the help center's contact page says every channel is "staffed around the clock, every day of the year," while an employee-card FAQ on the same help center says live support runs "Monday through Friday from 8am ET to 8pm ET." Separately, four versus pages upgrade the support claim into a named-contact claim. The Amex and Chase pages both state that "Rho provides a dedicated human account manager to every client"; the HSBC page promises "a dedicated account manager to every client at no additional cost"; the BILL page says "Every Rho client has a direct line to a human account manager." Rho's more carefully sourced pages contradict all four by reserving dedicated account management for "growth-stage and qualifying clients," and the Chase page does both on itself, carrying the qualified line in its comparison table and the unqualified one in its FAQ. Chase is one of the five rewritten pages, so this is not confined to the untouched generation.

#### The $50,000 Treasury minimum

Rho says: Rho Treasury opens at a $50,000 minimum, "one-fifth of Mercury's $250,000," and balances between $50K and $250K can earn treasury yield at Rho but not at Mercury.

Verified: Mercury's Treasury minimum is $250,000 with a 0.15% to 0.60% management fee, and Rho's own versus page reports Brex's treasury as "money market fund yield, tiered by total balance, no minimum." Brex's rates-and-fees schedule, effective 09/10/2026, headlines the BNY Dreyfus Government Cash Management fund at "up to 3.70%" with no minimum deposit.

Assessment: the edge is real against Mercury and nonexistent against Brex. Rho's versus/brex page states Brex's "no minimum" and declines to print Brex's rate, which is the one place where the rewritten versus pages behave like the old ones. Rho also misstates its own minimum on the page dedicated to it: /treasury-yield-comparison says "$50,000 minimum" in its hero, body and FAQ, while the Minimum row of that same page's comparison table reads "$100,000" and its bottom yield band reads "$100K to $2M" (as of 2026-09-11). A differentiator the company cannot state consistently on one page is not being pressed hard.

#### AP automation included, settling from the account that holds the cash

AP here means accounts payable, the work of receiving vendor invoices, approving them and paying them.

Rho says: "Rho Bill Pay is automated accounts payable, sometimes called AP automation, included with Rho business banking," with no monthly, per-user or minimum-balance fee, and "$0 on domestic check payments." It is explicitly not sold standalone.

Verified: the comparison set charges for this. By Rho's own sourced figures, BILL runs $45 to $89 per user per month plus $0.59 per ACH transfer and $1.99 per check; Tipalti starts at a $99 monthly platform fee plus transaction pricing; SVB charges $10 a month plus $0.40 per item over 15, with Bill Pay Plus at $50 to $250 a month and a $1,000 ERP implementation fee; Chase sells Cashflow360, a white-labeled BILL, separately with unpublished bundle pricing. Mercury and Brex both include bill pay free on all tiers.

Assessment: the structural point is the one Rho makes least clearly. Because Rho holds the deposit, an approved bill is paid out of the same balance the platform already ledgers, with no funding transfer from an external bank, no intermediary float and no per-payment rail fee to pass through. Standalone AP vendors have to pull funds from your bank before they can push them to your vendor, which is where their per-transaction pricing comes from. That is a genuine architectural advantage, and it is shared with Mercury and Brex rather than unique to Rho.

The capability, as opposed to the price, is thinner than a dedicated AP tool, and Rho says so. Three-way match (reconciling a purchase order against the vendor invoice and the goods receipt) is listed by Rho as "Not yet available," and no purchase-order object appears anywhere in the corpus. Approval routing is documented only by dollar amount, not by vendor, department, GL account or entity. Invoice capture uses unnamed third-party OCR vendors and requires human confirmation. Rho's own FAQ concedes the point: "A dedicated AP tool can make sense if your team needs deeper approval-policy customization than a banking-included tool offers."

#### Pre-EIN and day-zero onboarding, including incorporation

An EIN is the IRS employer identification number, the tax ID a US company needs before a bank can fully open its account.

Rho says: on /product/incorporation, "Non-VC-backed founders get a 30-day pre-EIN window before the EIN arrives; VC-backed founders get 60 days. Both require manual review, and neither is guaranteed." Rho Incorporation forms Delaware C-corps for a $400 fee that is credited back, with attorney review and roughly 80% of filings completing within 24 hours.

Verified: the pre-EIN quote is verbatim and live as of 2026-09-11, but it is stated exactly once in the entire crawled corpus and appears on no help-center page and in no Terms document, so treat it as a marketing statement rather than a commitment. Two caveats are load-bearing. A pre-EIN account is deposit-only: "Funds cannot move until the IRS issues your EIN and it attaches to your account." And the differentiation claim does not survive contact with the competition, because Rho's own versus/brex page describes its pre-EIN path as working "through incorporation integrations" (Rho, Stripe Atlas, Clerky) and Mercury offers pre-EIN account opening through the same Stripe Atlas and Clerky partnerships. Rho's own help center also contradicts the whole proposition in one place: "You'll need your EIN letter to join Rho."

Assessment: what is genuinely less common is that Rho performs the incorporation itself and rebates the fee, against Stripe Atlas at $500 one-time plus $100 a year for a registered agent and Clerky from $427. What that rebate actually costs is in the footnote: $10,000 of new money deposited and a daily average balance kept at least $10,000 above where it started for 60 days. It is a funnel priced in deposits, not a giveaway. Rho also publishes no approval SLA for the core checking account anywhere in the corpus, while marketing against traditional banks that take "5 to 14 business days."

#### Comparison pages that name where competitors win

This one is easy to dismiss as marketing and should not be. How a company writes about competitors is evidence about how it thinks.

Verified: the eight /versus pages split into two clearly dated generations.

| Generation | Pages | Dated claims | Third-party citations | Concedes competitor strengths |
|---|---|---|---|---|
| Rewritten Aug 2026 | ramp, mercury, brex, svb, chase | 11 to 24 each | 2 to 17 each | Yes, in a named section |
| Untouched | amex, bill, hsbc | 1 each (footer only) | 0 | No |

The rewritten pages say things competitors' marketing departments would not sign off on. On Brex: "Large companies running global spend programs: Brex. This one goes to Brex." On SVB: "Venture debt is a genuine SVB strength ... that's the honest headline." On Chase: "Chase's fortress balance sheet is real, and no fintech should pretend otherwise," and Chase's branch network is "a genuine moat for cash-heavy businesses." On Mercury: "its product polish is real." On Ramp, the single most surprising line in the corpus: Ramp's "agent/AI tooling (hosted MCP server with audited write actions, public CLI) is genuinely ahead." And inside its own attack post on the Capital One acquisition of Brex, Rho published a verbatim rebuttal from a Brex employee (a $950M three-year Capital One investment commitment and a 50% increase in Brex's startup team) and left it unanswered.

Assessment: this is a real differentiator, and it has a commercial logic. Rho's most durable competitive line is attacking pricing opacity, and conceding loudly on axes it does not sell (travel programs, venture debt, branches, agent write access) buys credibility for that attack. But the discipline is not uniform, and the exceptions are all in the same direction. The Amex page frames Amex as a "$895 travel card," selecting the Business Platinum, while Rho's own blog lists the $0-annual-fee Amex Blue Business Cash at 2% back. The Chase page never mentions Chase Ink Business Premier, which Rho's own blog describes as "$195 a year, unlimited 2% cash back ... and 2.5% on any single purchase of $5,000 or more," the one widely available card that matches Rho's headline rate with no banking-relationship condition and no $1M cap. The HSBC page is titled for HSBC Innovation Banking and describes a generic HSBC business checking account, contradicting Rho's own blog on the same product. And across every listicle Rho publishes, Rho ranks first in every category where it sells a product; the sole exception is payroll, which it does not sell.

### 8.2 Differentiation that is thinner than claimed

#### The MCP and API story

MCP, the Model Context Protocol, is the interface standard that lets an AI assistant call a vendor's tools directly. A first-party MCP server means the vendor runs it themselves rather than relying on a third-party wrapper.

Rho says, in its launch blog of 2026-07-29: "Most financial APIs predate agents; MCP got bolted on. This one shipped with its MCP server in production. Not a roadmap item, the architecture."

Verified, measured directly this session: the Rho API has 14 operations across 5 resources, all of them HTTP GET. Zero POST, PUT, PATCH or DELETE. Five scopes exist (accounts, transactions, statements, cards and invoicing, each :read), confirmed from the public OAuth metadata at rhoapi.rho.co. The sandbox host has no MCP endpoint at all (HTTP 404), so the only way to exercise the MCP server is to mint a production token against live company money. Rho's OAuth server at auth.rho.co returns "Dynamic registration is not enabled" on client registration, so a third-party MCP client cannot self-register; Mercury documents a registration endpoint for exactly that case.

Verified, on timing: Ramp's changelog dates its first MCP server to 25 March 2025, Griffin published a read-write agent bank in May 2025, Narmi and Grasshopper announced the first MCP server by a US bank on 20 August 2025, Mercury shipped read-only MCP in November 2025, Brex's changelog dates its MCP server to April 2026, and Grasshopper was listed in Anthropic's connector directory on 14 July 2026, two weeks before Rho launched. Within Rho's own competitive cohort, Rho is roughly 12 to 17 months behind the leaders. (Scoped more widely, first-party bank MCP servers are still rare: an aggregator directory listed only 10 worldwide on 2026-09-11, and Rho was not among them, so "table stakes" holds for Rho's cohort and not for US banking generally.)

Verified, on surface area:

| Vendor | API write capability | Webhooks | MCP | Published tool list |
|---|---|---|---|---|
| Rho | None, 14 GET operations | None, "not yet" | Read-only, production | None, Rho says introspect it |
| Mercury | Send money, issue cards, create invoices | Yes | Read-only, 31 tools | Yes, 31 named |
| Brex | Payments API sends ACH, domestic wires, checks | Yes | Yes, since April 2026 | Yes, roughly 41 |
| Ramp | 252 documented operations, 117 write verbs, 40 resource groups | Yes | Three servers, plus an MIT-licensed CLI and Agent Cards in early access | Yes |

Rho is also carrying a false competitor claim on this exact axis. Its /product/api comparison table, with data "as of 2026-08-20," states that Brex has no documented MCP integration. Brex's MCP server had been live since April 2026, and Rho's own blog reversed the claim five days later, on 2026-08-25.

Assessment: what is genuinely good here is the data model, not the reach. Money is returned as an object with integer minor units and an ISO 4217 currency rather than a float, transaction legs are grouped by a money_movement_id, the network identifiers that let you trace a payment are exposed (ACH trace numbers in the format set by NACHA, the body that writes the ACH network's rules, and the IMAD/OMAD input and output message references a bank asks for when a wire goes missing), attributions to user and card are present, and tool names are frozen to v1 operationIds so saved agent workflows do not break. That is a better feed than most aggregators produce. It is still a feed. A read-only transaction feed is close to a commodity: Stripe Financial Connections publishes a price of $0.30 per institution per account holder per month for exactly that, and Plaid or Teller can read a Rho account on the customer's authorization without Rho's participation. Rho's product page argues that read-only is a safety posture ("Read-only by design"), while its own roadmap treats it as stage one: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval." Both cannot be the reason.

#### The yield headline

Rho says: "up to 4.66% net yield" on Rho Treasury (as of 09/11/2026).

Verified: the dagger footnote on /treasury-yield-comparison states that the 4.66% "assumes a 100% allocation to the Vanguard Short-Term Investment-Grade Fund (VFSTX)" at the lowest-fee tier, which requires $20M or more in deposits. The product itself caps that fund: /product/treasury says the short-term bond fund is "capped at 50% of your total allocation," and the help center says "Vanguard allocations are capped at 50% of your portfolio." Under the cap, the highest blended net yield at the best fee tier is 50% VFSTX at 4.66% plus 50% MULSX at 3.70%, which is 4.18%, or 48 basis points (hundredths of a percent) below the headline. The cap is not absolute: pre-existing allocations above 50% are grandfathered and a higher limit can be approved on request. So the headline is not achievable under the product's standard published allocation rules, rather than mathematically impossible.

Two further inconsistencies sit on the same pages. The asterisk footnote on /product/treasury attributes the same 4.66% to "90-day Treasury Bill rates," which is not what that page's own table produces. And on /versus/ramp the figure appears as 4.66% (09/11/2026) in the table and as 4.55% (08/02/2026) in three FAQ answers on the same page.

The adjacent headline numbers are also softer than they read. Savings is quoted as "up to 1.00%" on versus pages without the $25,000 average monthly balance required to earn interest or the six-withdrawals-per-month limit, both of which appear only in Rho's lowest-traffic September 2026 blog cohort. The $75M FDIC savings figure is presented on every versus page without the qualification that it is best-efforts network capacity: the American Deposit Management agreement Rho publishes says only that ADM "will use commercially reasonable efforts to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution," where IntraFi's equivalent agreement commits flatly and adds a reimbursement obligation. Rho's own comparison tables show Grasshopper at $125M, Stifel at $225M and Axos at $265M through the same sweep mechanic, and Rho leads with $75M anyway.

#### "Banking and payments via API"

The global navigation on essentially every page of rho.co carries a "Rho API" item with a "New" badge and the subtitle "Banking and payments via API."

The product page, one click away: "The Rho API gives Rho customers read-only programmatic access to their balances, transactions, and statements." The help center: connected AI tools "cannot: Move money / Issue, lock, or edit cards / Add or manage users / Make changes to your Rho account."

Assessment: there is no payment capability in the API. Not gated, not in beta, not present. The nav label is wrong in the plainest sense a nav label can be wrong.

#### Marketing pages that understate or misstate the product

Unusually, the largest single marketing error in the corpus runs against Rho's own interest.

| Page | What the page says | What Rho's own help center says |
|---|---|---|
| /product/bill-pay | "Once approved, pay by check"; "$0 On domestic check payments"; "it captures invoices automatically, routes them for approval, and pays vendors by check" | "You can make Bill Pay payments using the following methods: ACH transfers; Wire transfers (domestic and international); Checks; Single-use cards" |
| /product/invoicing | "Rho Invoicing does not yet sync with accounting software like QuickBooks or Xero" (live on 2026-09-11) | Changelog, 2026-08-31: "Rho invoices now sync to QuickBooks" |

The Bill Pay page reads as a check-only product when the product supports four rails. Two qualifications keep this honest: Bill Pay's international wires are USD only, and a vendors help article contradicts two other help articles by saying Bill Pay does not currently support vendor cards, so the help center is not internally consistent either. On invoicing, the stale clause is 11 days old as of capture, not months, and the Xero half of the sentence is still accurate because syncing is "Available for QuickBooks Online only."

Elsewhere the pattern reverses. The 2.9% + $0.30 card-acceptance fee on invoices is documented in the invoicing terms, the help center and the changelog, and appears nowhere on /product/invoicing. Three versus pages state that "1% on foreign-currency transfers" is the only standard payment fee, while one September 2026 blog post states that Rho charges "$15 for outbound SWIFT or international wires, and in some corridors that fee is mandatory with no opt-out."

Assessment: this is not a dishonest site so much as an unmaintained one. A 522-page corpus with programmatic SEO cohorts, partial refreshes and two live cashback disclosure texts running simultaneously (40 pages say "1.5% standard," 11 say "1.25% standard") will produce exactly this. It matters here because Rho's strongest competitive frame is other vendors' pricing opacity, and that frame is only as strong as its own house.

### 8.3 What Rho is missing that its cohort has

| Capability | Rho status | Who has it |
|---|---|---|
| Programmatic payment initiation | None. All 14 operations are GET | Mercury (send money, internal transfers), Brex (ACH, domestic wires, checks), Ramp (117 write operations) |
| Webhooks (a push notification from the vendor when something happens, instead of polling) | None. Rho's own blog says "Not yet" | Mercury, Brex, Ramp, Stripe, Plaid, Modern Treasury, Slash |
| Published SDKs (prebuilt client libraries) | None. OpenAPI spec only | Mercury, Brex, Ramp, Stripe, Modern Treasury |
| MCP sandbox | None. The sandbox host returns 404 on /mcp/v1, so first contact is a production token on live money | Ramp publishes a sandbox MCP instance |
| Self-service client registration | Disabled. auth.rho.co returns "Dynamic registration is not enabled"; partner apps are registered manually by email | Mercury documents a registration endpoint |
| Published MCP tool inventory | None. Rho says to introspect the server | Mercury (31), Brex (about 41), Navan (11) |
| Managed travel booking | None. Rho lists it as its own con: "No managed travel program comparable to Brex's" | Brex (free on Essentials), Ramp (free tier, policy tiering on Plus), Navan |
| Procurement | Explicitly excluded: Bill Pay "does not include procurement or supply-chain management" | Ramp (add-on to Plus or Enterprise), Brex Smart Card, Coupa, Zip |
| Three-way match and purchase orders | "Not yet available." No PO object anywhere in the corpus | BILL, Tipalti, Ramp, Coupa |
| Deep multi-entity | Entity switching exists and two case studies cite 2 entities and 10 brands, but no product page explains the model, there is no consolidated cross-entity reporting surface, and API tokens are "scoped to a single business" | Brex publishes an explicit ladder: 2 entities (1 global) on Essentials, US and international multi-entity on Premium, unlimited on Enterprise |
| International entities | None. US-incorporated entities only; sole proprietorships excluded; Bill Pay international wires are USD only | Brex (local card issuance in 50+ countries, acceptance in 210+), HSBC Innovation Banking (UK, EU, Israel, Hong Kong footprint) |
| Published security-certification detail | Thin. See below | Most enterprise-targeting competitors publish a trust center |
| Published approval SLA for the core account | None anywhere in the corpus | n/a, but Rho markets against banks that take "5 to 14 business days" |
| Verifiable satisfaction evidence | Thin. Rho self-publishes a G2 rating of 4.8 on 25 landing and partner pages (G2 and Trustpilot are the public software review sites buyers check), with no review count and no link to the listing. No Trustpilot score and no NPS (net promoter score, the standard customer-satisfaction metric) appears for Rho anywhere | Brex and Ramp, whose G2 scores Rho's own blog cites with the review count attached (Brex 4.8 from 1,611 reviews, Ramp 4.8 from 2,487) |

On multi-entity there is a disclosure gap worth flagging separately. Section 17 of Rho's Terms of Service is an expressly irrevocable cross guaranty under which a customer guarantees the obligations of parent or subsidiary entities in its own ownership chain that also bank at Rho ("absolutely, unconditionally and irrevocably guarantee, as primary obligor and not merely as surety"). A holding-company structure banking multiple entities at Rho is therefore cross-collateralized. That appears in the Terms and in none of the multi-entity marketing or case studies. It is entity-level, not a founder personal guarantee, so it does not contradict Rho's "no personal guarantee" card marketing.

On security: Rho says it is "SOC 2 Type 2 compliant" and "audited every year by a third-party using the SOC 2 framework." SOC 2 Type 2 is an audit of whether a company's stated security controls actually operated over a period of time. Verified: the auditor is not named, the report period is not stated, which trust services criteria are in scope is not stated, and the gating process for obtaining the report is not described beyond a link. The corpus contains zero mentions of penetration testing, no vulnerability disclosure policy or bug bounty, no ISO 27001 (the international information-security certification) and no PCI DSS attestation (the card industry's data security standard, which binds anyone handling card numbers) for Rho itself, in a product that displays full card numbers and CVVs in the browser. Assessment: this is the cheapest gap on the list to close and the one most likely to cost Rho a mid-market deal, because procurement teams ask for exactly these artifacts.

### 8.4 A differentiated company, or a well-executed bundle?

A well-executed bundle with one structural pricing bet and one genuine operating advantage. The argument, rather than the assertion:

**Take the differentiators one at a time and ask what copying costs.** The $50,000 Treasury minimum is a number in a configuration file, and Brex already sits at zero. Free bill pay is already matched by Mercury and Brex. Pre-EIN onboarding has already been copied, through the same two partners. 24/7 phone support costs money and headcount, takes about a quarter to stand up, and Brex has already paid for it. Candid comparison pages cost nothing and are copied by nobody, because most marketing organizations do not want them. Only one item on the list imposes a real cost on the copier: eliminating paid tiers, because for Ramp, Brex and Mercury the tier is simultaneously a revenue line, a packaging mechanism and a sales compensation structure. That is a pricing posture, not a technology, but it is the one thing on the list a competitor cannot decide to match on a Tuesday.

**The bundle shape is a real product idea and it is not unique.** Rho's own framing is the clearest statement of it: "Ramp is a spend-management platform (cards, expenses, bill pay) with a business account attached; Rho is a banking platform (checking, savings, treasury) with cards, AP, and expense management built in." Removing the seam between the account that holds the cash and the software that moves it is genuinely valuable, and it is why Rho's AP economics work. But Mercury is the same shape. Reduced to facts, the Rho-versus-Mercury decision comes down to phone support and Treasury minimum and savings insurance ceiling on one side, against write-capable API, a pending national bank charter, and more published product polish on the other. That is a feature trade inside one category, not a category difference.

**The strategy underneath is deposit gathering, and every mechanism confirms it.** Rho Platinum's 2% requires payroll, revenue and 50% of company assets at Rho. Daily Terms cards settle to zero each day from the linked checking balance, so cash never leaves the platform. The Treasury advisory fee is assessed on checking plus Treasury combined. Every partner microsite offer is priced in average daily balance held for a fixed period, from $20,000 on 22 of the 77 partner pages up to $400,000 or $500,000 on 25 of them. And the one document in the corpus that names the economics, the affiliate agreement, promises partners 30% of the gross profit Rho recognizes on a referred company's deposits, net of interest paid to that company, for twelve months. Free software is the customer-acquisition cost of a deposit business. That is coherent, and it is also what every neobank does.

**The independence claim is the weakest strong claim.** "Independent and focused. We're not for sale" is Rho's sharpest strategic line and rests on no published evidence. SEC records for Under Technologies, Inc. show five Form D filings totaling $104,732,452, the last reporting a first sale on 2021-10-28 and filed 2022-01-21, with no SEC filing of any type since. That proves no disclosed Regulation D equity since 2021, not that no capital was raised: Rho did take debt, and Trinity Capital lists Rho Business Banking in its portfolio with "Year Invested: 2024," disclosing neither structure nor amount. Nothing about funding, ownership, profitability or runway appears anywhere in the 522-page corpus, while Rho uses Brex's change of ownership as a central attack. Meanwhile Ramp closed a $750M round at a $44B valuation on 2026-06-04 and was reported on 2026-09-08 to be in early talks at about $60B; Mercury states more than $650M in annualized revenue and four years of GAAP profitability; Brex sits inside Capital One. Rho is running a capital-intensive deposit strategy against three balance sheets that dwarf its own disclosed equity.

**Verdict.** Rho is a well-executed bundle rather than a differentiated technology company, and in its better writing it is close to admitting that. Its durable edges are two: a zero-software-fee posture that is structurally expensive for tier-monetizing competitors to match, and human phone support on a free account, which competitors keep declining to fund. The agentic and API story is a follower's story, and if write access and webhooks ship as promised, Rho becomes a peer on that axis rather than a leader. The competitor most exposed by this comparison is Mercury, on phone support and treasury minimum. The competitor Rho is least equipped to displace is Ramp, which has a substantial free tier, a far deeper agent surface, travel, procurement and vastly more capital.

For a reader deciding rather than evaluating, the question is not whether Rho is differentiated. It is whether the seam between your bank and your finance software costs you more than the $3,600 to $4,500 a year in seat fees you would pay elsewhere, plus the frustration of not being able to call anyone. For a 25-to-100-person US company with $50K to $20M of idle cash, no dedicated AP tool and no travel program, the answer is often yes. For a company that needs programmatic payments, travel, procurement, international entities or a trust center full of audit artifacts, the answer is no, and Rho's own pages, to their credit, mostly say so.
## 9. Risks, fine print, and what to check before committing

This section is written as diligence, not as a takedown. Most of what follows is structural to the model Rho uses rather than unique to Rho, and in several places Rho's disclosure is better than its competitors'. The job here is to separate three things that get blurred in vendor evaluations: risk that comes from the architecture (a software company in front of someone else's bank), risk that comes from the contract (terms a customer signs and rarely reads), and risk that comes from the counterparties (one sponsor bank, one sweep administrator, one broker-dealer, one lender).

All figures are stamped. Rates, fee schedules, contract versions and bank ownership all changed within the twelve months before this was written, and several will change again.

### 9.1 Where the money actually sits

Rho is not a bank and says so, in the same words, on nearly every page. The practical consequence is that deposit insurance does not attach to Rho. It attaches to whichever chartered institution is holding the cash at that moment.

Two acronyms the rest of this section depends on. **FDIC insurance** is a US federal government guarantee that pays depositors if an insured *bank* fails, up to $250,000 per depositor, per insured bank, per ownership category. It pays nothing if a non-bank technology company fails. **SIPC protection** is a different thing entirely: it covers up to $500,000 per customer (including up to $250,000 in cash) if a *brokerage firm* fails and customer securities go missing. It does not cover the securities losing value. A third acronym appears once below: **NCUA** is the credit-union equivalent of the FDIC, with the same $250,000 limit.

| Product | Protected by | Limit | Protects against the failure of |
|---|---|---|---|
| Rho Checking | FDIC | $250,000 | Webster Bank only |
| Rho Savings | FDIC and NCUA | Up to $75,000,000 | Each program institution, $250,000 at a time |
| Rho Treasury | SIPC, not FDIC | $500,000, of which $250,000 cash | The broker-dealer custodian only |
| Rho Rewards balance | Not stated anywhere | Not stated | Not stated |

Rho says, on its trust page: "checking is FDIC-insured up to $250,000 at Webster Bank, a division of Santander Bank, N.A. The up-to-$75 million coverage applies to Rho savings via the sweep network of 400+ FDIC-insured banks." That is the correct answer to the question most fintechs blur, and Rho volunteers it in an FAQ titled "Does the $75M FDIC coverage include my checking account?"

**Verified:** the $250,000 checking limit is one number covering all of a company's Rho checking accounts combined, not one per sub-account. Opening ten named sub-accounts for budgeting does not create ten insured buckets.

**Assessment:** the checking story has one gap Rho never closes. The Terms of Service say deposits are "held by Webster" but never state whether a customer's checking account is a deposit account titled in the customer's own name at Webster, or a beneficial interest in a pooled account that Webster holds for the benefit of many Rho customers (the industry calls the latter an FBO, "for benefit of," account). That distinction is the entire subject of the FDIC's post-Synapse rulemaking discussed in 9.5, and Rho documents it for Savings but not for Checking. It is question 2 on the checklist.

One more precision problem. Rho states the FDIC limit qualifier six different ways across its own pages: "per depositor, per ownership category" on the security page, "per institution, per account type" in the Terms of Service, "per entity, not per account" in the FAQ, and the actual federal rule ("per depositor, per insured bank, per ownership category") on the startups page. For a single-entity company these converge. For a group running three legal entities through Rho they do not, and the correct rule is the one stated least often.

### 9.2 The savings sweep, read closely

A **sweep network** is a service that takes one large deposit and spreads it across many banks in slices under $250,000 each, so the depositor gets FDIC coverage at each receiving bank instead of being capped at one bank's limit. Rho's is run by American Deposit Management, LLC (ADM), which acts as the customer's agent, not as a bank. Rho publishes ADM's master services agreement as a help-center article, which is more than most competitors do.

**Verified** (all quotations from rho.co/help-center/general-rho-information/rho-savings-account-terms-and-conditions, re-fetched live 2026-09-11):

- ADM "will use commercially reasonable efforts to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution."
- When more than $250,000 moves in or out in one day, "for a limited amount of time (intraday or overnight), the entire amount of the withdrawal or deposit may be held at one Program Institution."
- "Withdrawals are limited to six (6) per month," processed "on Tuesdays and Thursdays (Processing Days) for settlement to your designated account on Wednesdays and Fridays (Settlement Days)," with a 12:00 p.m. Central cutoff and special handling for requests over $3,000,000.
- Section 1 gives the client two elections, extended deposit insurance or not, and states: "By signing Exhibit A, Client expressly waives extended deposit insurance."

Now the fair judgement about which of those is a genuine weakness, because three of the four are not.

**Standard industry language, not a Rho defect.** The commercially-reasonable-efforts standard and the intraday transit exposure appear in essentially every sweep program. Pershing's disclosure says it "will use all commercially reasonable efforts to ensure that no more than $250,000 of your swept funds will be deposited in any single Program Bank." Altruist says "Generally, no more than $250,000." Even IntraFi, the strongest program in the market, concedes in its ICS agreement that a deposit "will not be eligible for FDIC insurance coverage at a Destination Institution before it becomes a deposit ... or after it is withdrawn." Rho itself repeats the effort standard in its marketing footnotes ("reflecting program capacity on a commercially reasonable efforts basis, not a guarantee"). Criticising Rho for this would be criticising the category.

**The Exhibit A waiver is also less alarming than it sounds.** What it waives is collateralization or a surety bond on balances above the insured limit, a feature ADM offers chiefly to public-unit and municipal depositors under state statutes. IntraFi's ICS and CDARS do not offer it at all. A corporate client who waives it is in the same posture as a client of every mainstream competitor. Note also that the published text is internally inconsistent on this point: Section 9 says ADM "will take all steps necessary," "to the extent commercially reasonable," to secure excess balances by repurchase agreement or a perfected first lien when operational cutoffs push funds over the limit, which cuts against a blanket waiver. Exhibit A itself is not published, and the enrollment flow that picks between the two elections is not public, so it cannot be confirmed that every Rho savings customer waives.

**The genuinely non-standard term is the withdrawal cadence.** Six withdrawals a month, processed Tuesday and Thursday, settling Wednesday and Friday, is slower than the benchmark: IntraFi's ICS settles every business day with an optional same-day withdrawal. That is a liquidity constraint, not a coverage constraint, and it collides with Rho's own customer-facing statement that Savings to Checking "typically settles the next business day" and with its payment-settlement page saying two business days. Which schedule actually governs in practice cannot be determined from public sources, so do not assume a Rho customer waits until Friday. Do assume you need to ask.

**The one place ADM is fairly criticised against the benchmark** is the effort standard itself, compared with IntraFi rather than in the abstract. IntraFi commits flatly that placements at a destination institution "will not exceed $250,000" and backs it with a reimbursement obligation if its own non-compliance leaves funds uninsured. ADM promises commercially reasonable efforts and offers no equivalent make-whole. That is a real, specific difference between two named programs.

Four further facts that belong in a diligence file and appear nowhere in Rho's savings marketing:

1. The published agreement is incomplete. It stops at Section 10, omits the Interest, Fees and Termination sections its own body text cross-references, is undated (it reads "entered into as of [Date entered on survey]"), and does not reproduce Exhibit A. The string "$75,000,000" appears on that page only in the site navigation bar, never in the agreement.
2. The list of program institutions is not published. Rho says it is "available from Rho support on request." Because FDIC coverage aggregates per depositor per bank, a company that already banks with a program institution silently loses coverage on the overlap. The ADM agreement says so; Rho's marketing does not.
3. ADM requires every non-public-unit client to represent that it is an "accredited investor" under SEC rules. This never appears in Rho's savings marketing.
4. ADM takes instructions from Rho as if they came from the customer, and the agreement puts the consequences of a misinstruction on the customer: "In the event that Instructions received from Rho, on behalf of Client do not reflect Instructions of Client, Client agrees that such Instructions ... shall be considered Instructions received directly by Client."

**Assessment:** "up to $75M in FDIC insurance" is a real, well-constructed benefit and the honest version of the claim is Rho's own: *up to*. Actual coverage at any moment depends on how many program institutions are accepting funds, which ADM controls at its discretion, and on what other relationships the customer already has inside that unpublished network. The liquidity terms, not the insurance terms, are where a treasurer will feel it.

### 9.3 What happens if Rho fails, versus if the bank fails

These are two different events with two completely different outcomes, and conflating them is the single most common error in fintech risk assessment.

**If Webster Bank fails.** The FDIC takes the bank into receivership. Insured deposits are typically made available within about one business day, either by paying the insurance or by transferring the accounts to an acquiring bank. Checking balances above $250,000 become a receivership claim. This is a well-rehearsed process with a statutory backstop.

**If Rho the company fails.** No bank has failed, so no deposit insurance is triggered. Rho says, on its trust page: "Your deposits are held at Webster Bank ... and the program banks in the sweep network, not on Rho's balance sheet. They remain yours, insured per FDIC rules at the institutions holding them." That is the correct answer as far as it goes, and Rho deserves credit for volunteering the question. What it does not address is access and reconciliation: how a customer identifies and reaches their money at Webster when the software that maintained the ledger is in a bankruptcy proceeding.

**Verified:** that scenario is not hypothetical. The 2024 collapse of Synapse Financial Technologies, a banking-middleware provider, froze funds for more than 100,000 end users across several fintech brands, involving over $265 million. The trustee put the gap between the ledger and the actual cash at $65M to $96M; the CFPB put it at $60M to $90M; a full reconciliation "to the last dollar" may never be possible. The Chapter 11 case ran roughly 19 months and was dismissed in late 2025 without full reconciliation. **Zero dollars of FDIC insurance were paid, because no insured bank failed.** The eventual partial remedy was a CFPB allocation of $46,248,291 from its Civil Penalty Fund on 2025-11-28, against a shortfall two or more times that size. The failure mode was recordkeeping, not theft or bank insolvency.

**Rho says** its architecture avoids this. Its security blog states that it chose direct integration with Webster over Banking-as-a-Service middleware: "While BaaS middleware offers a faster path to market, recent headlines have highlighted its risks. Direct integration requires greater upfront investment and ongoing management, but it ultimately provides more control and stability." A separate post, "Our Partnership with Webster Bank," says Rho "began building out our proprietary core needed to integrate with Webster Bank ... systems."

**Assessment:** if that claim is true, it removes the exact topology that broke in Synapse, where neither the consumer brand nor the bank held the authoritative ledger. Nothing in the public corpus independently verifies it, but it is consistent with the API's framing of a "direct connection to the Rho ledger (no aggregator)." It is worth noting how much shorter Rho's chain is than some competitors': Rho Checking is customer to Rho to Webster, while Relay's is customer to Relay to Unit (middleware) to Thread Bank to program banks. The unanswered question remains the FBO one from 9.1. Who holds the record of who owns each dollar at Webster, and how often is it reconciled? Rho does not say publicly.

### 9.4 The contract

All three provisions below live in the Terms of Service, Version 7.0.0, last updated August 27, 2026 on a page also datelined August 4, 2026. None appears in any marketing, product, pricing or help page. That last fact is close to trivially true, since limitation-of-liability terms are not marketing copy for any issuer, and it should be read as "you will only find these by reading the contract," not as concealment.

#### The $500 liability cap

Section 22 reads, in the original all-caps: "EXCEPT AS REQUIRED BY LAW OR PURSUANT TO THE 'ARBITRATION PROVISION AND CLASS ACTION WAIVER' SECTION BELOW, RHO'S LIABILITY (WHETHER BASED ON AN ACTION OR CLAIM IN CONTRACT, TORT OR OTHERWISE) TO YOU, OR ANY THIRD PARTY, IN ANY WAY CONNECTED WITH OR ARISING OUT OF THIS AGREEMENT (AND ALL OTHER AGREEMENTS BETWEEN RHO AND YOU) WILL AT ALL TIMES BE LIMITED TO A MAXIMUM OF $500.00 (FIVE HUNDRED UNITED STATES DOLLARS)."

Four qualifications are load-bearing and must travel with that number.

1. It is not flat. It carries express carve-outs for what law requires and for the arbitration section.
2. Section 23 concedes it may not apply at all: in states that bar such limits, "LIABILITY IS LIMITED TO THE EXTENT PERMITTED BY LAW."
3. Section 25.4 sets a floor inside arbitration: if the arbitrator awards more than Rho's last written settlement offer, Rho pays the higher of the award or $10,000.
4. **It caps Rho's liability under the Rho-customer agreements. It is not a cap on deposit obligations.** Deposits sit at Webster under a separate Webster Agreement; brokerage assets at Apex or Interactive Brokers; advisory at RBB Treasury. A customer's claim to their own money does not run through Section 22.

Section 22 also limits remedies to termination ("your sole and exclusive remedy shall be termination of this Agreement") and extends the protection to the Sponsor Bank and third-party service providers.

**Assessment:** $500 is unusually low as a drafting choice. Many commercial software contracts cap at fees paid over the preceding twelve months, which for a large Rho customer paying almost nothing in software fees would also be small, so the practical delta is narrower than $500 makes it sound. The operative point for a CFO is not the number but the direction: Rho does not underwrite operational loss, and there is no published cyber, crime or fidelity coverage described that would respond in its place. Ask about it (checklist question 9).

#### Liability for unauthorized card use at ten or more cards

Section 1.6 of both card addenda says: "if we issue at least ten (10) Cards to you and your Users, you will be liable for all unauthorized use of all Cards." Below ten cards, liability is capped at "the lesser of (i) $50.00 or (ii) the amount of money, property, labor or services obtained by the unauthorized use."

This looks alarming out of context and is regularly presented that way. It should not be, and getting this right is the difference between diligence and noise.

**Verified:** the clause is a near-verbatim restatement of federal law, not a Rho invention. Regulation Z, 12 C.F.R. 1026.12(b)(5), implementing TILA section 135 (15 U.S.C. 1645), provides: "If 10 or more credit cards are issued by one card issuer for use by the employees of an organization, this section does not prohibit the card issuer and the organization from agreeing to liability for unauthorized use without regard to this section." The sub-ten fallback tracks 12 C.F.R. 1026.12(b)(1)(ii) almost word for word. Rho cites Regulation Z by name in the same paragraph. Brex's card agreement carries the equivalent clause: "in accordance with Section 135 of the federal Truth in Lending Act, if at any time you have been issued ten (10) or more Cards ... then Company waives any and all limitations on its liability for unauthorized use." This is standard commercial card practice across the industry, and the alarming-sounding threshold comes from the CFPB, not from Rho.

Three limits inside the same paragraph are also usually dropped when the clause is quoted: it is prefaced "Unless prohibited by applicable law, or otherwise provided in accordance with any liability waiver program provided by the Card Network," which preserves the Visa and Mastercard commercial-card waiver programs; and liability ends the moment Rho receives notice of suspected unauthorized use. Rho separately mirrors the federal employee carve-out, agreeing that the company will not push liability onto an individual user beyond what Regulation Z permits.

**The fair criticism is about clarity, not about the term.** Rho's security page says: "Set merchant, limit, and time controls on every card. Mastercard Zero Liability protects against unauthorized card fraud." A customer with 40 cards reading that sentence, and then Section 1.6, has to work out for themselves that the network waiver program is what stands between them and the contract. Rho never explains the interaction. **Assessment:** this is a disclosure-quality issue worth one question in diligence (checklist question 10), not a trap and not a differentiator against competitors, who write the same clause.

#### The entity-level cross guaranty

Section 17 is a real and unusual-to-find-unadvertised provision: each account holder "absolutely, unconditionally and irrevocably guarantee[s], as primary obligor and not merely as surety, the full and punctual payment and performance of all present and future obligations" of affiliated Rho accounts. It is irrevocable and continuing, survives the affiliate's bankruptcy, waives subrogation (the right to step into Rho's shoes and chase the affiliate for what you paid) and notice, and is "a guaranty of payment and performance and not of collection," so Rho need not pursue the affiliate first.

Three corrections keep it accurate:

- "Affiliate" is defined narrowly for Section 17's own purposes as a parent or subsidiary entity in the customer's own ownership chain, not affiliated entities generally.
- The obligation is expressly capped to avoid fraudulent-transfer treatment.
- **It does not contradict Rho's "No personal guarantee" card marketing.** Section 17 is an entity-level guaranty. It creates no personal liability for any founder or officer, and nothing else in the Terms of Service makes an individual liable for company obligations. The guaranty is also flagged in all caps inside the card addenda themselves.

**Assessment:** for a single-entity company this clause is inert. For the multi-entity groups Rho's enterprise page targets, it is the most consequential sentence in the agreement: opening a Rho account for a subsidiary puts the parent behind the subsidiary's card balance. It should be routed to counsel, not to procurement.

A note for completeness: the "no personal guarantee" promise is scoped to the *cards*. Rho Capital, the working-capital line, carries a different disclosure entirely: "Application and consent to obtain personal credit report is required ... Personal Guaranty may be required."

#### Other clauses worth pricing

| Clause | What it says |
|---|---|
| Setoff (Addendum B 2.3) | Rho's right to take money sitting in your accounts to cover what you owe it: on default, Rho may "set off and apply any and all deposits" and debit "any bank accounts for which you have provided routing and account numbers," without notice |
| Card limit discretion (Addendum A 1.3) | Credit is "uncommitted"; the limit is set "in our sole discretion," need never be disclosed, and can be cut "to zero dollars" without notice |
| Termination (20.2) | Rho may terminate or suspend "at any time for no reason or for any reason without prior notice" |
| Limitations period (26.9) | One year from the event, against New York's six-year default for contract claims |
| Dispute resolution (25) | Binding arbitration before the American Arbitration Association in New York County. Class action and jury trial waived, proceedings confidential |
| Indemnity (19) | Customer indemnifies Rho, the Sponsor Bank and third-party providers across thirteen categories. No reciprocal indemnity anywhere |
| Amendment (26.4) | Fees included, by notice; continued use is acceptance |
| Support (26.12) | "We are under no obligation to provide support for the Rho Services" |
| Data on exit (20.3) | No Rho obligation to export or return data. Dashboard access ends at closure |

**Assessment:** individually most of these are common in fintech terms of service. The combination that matters operationally is the last three: fees can change by notice, there is no support obligation in a company whose primary marketing claim is 24/7 human support, and there is no data-return obligation at exit. Export before you close, not after.

### 9.5 Concentration and vendor risk

**One sponsor bank.** All Rho checking deposits and all card issuance sit at Webster Bank, which became a division of Santander Bank, N.A. on 2026-08-20. Rho headlines this as a strength, and on scale it is: Santander's US banking organization is a $327 billion-asset group. **Verified:** that is a parent-group pro forma figure (the combined group counted as if the merger had always been in place), not Webster's. Webster's final standalone bank-level figure was $85.90B at its last FDIC call report (06/30/2026, cert 18221); Rho's trust page still footnotes $85.5B as of 2026-03-31 while using $327B in headlines and navigation. Because Webster Bank, N.A. ceased to exist as a separately insured institution on 2026-08-20, the correct bank-level comparator today is Santander Bank, N.A. (cert 29950) at $103.96B in assets on 06/30/2026. That is still far larger than any competitor's standalone partner bank (Rho's own cited comparator, Cross River Bank, was $8.53B on the same date), and still roughly a third of the $327B group figure Rho headlines.

**Assessment:** a larger, more heavily supervised sponsor genuinely lowers the probability of the bank-side failure modes below. What it introduces is transition risk: Rho's entire trust narrative now rests on an acquisition that closed three weeks before this corpus was captured, and nothing Rho publishes addresses contract continuity, repapering (re-signing the existing agreements under the new owner's name), program-manager agreement renewal, or what Santander's appetite for fintech partnership programs will be. That is checklist question 13.

**What happened to fintech sponsor banks, 2023 to 2025.** The relevant history is not about banks failing. It is about regulators constraining them, and about middleware failing between the fintech and the bank.

| Date | Event |
|---|---|
| 2024-04-22 | Synapse Financial Technologies files Chapter 11 (bankruptcy reorganization) |
| 2024-05-21 | FDIC consent order effective against Thread Bank (IT, AML, third-party due diligence, and procedures to "unwind third-party business lines, including FinTech partners") |
| 2024-06-14 | Federal Reserve consent cease-and-desist against Evolve Bank & Trust for "unsafe and unsound banking practices" in its fintech-partnership risk framework |
| 2024-07-25 | Fed, OCC and FDIC joint statement on bank arrangements with third parties, plus a request for information |
| 2024-09-17 | FDIC proposes Recordkeeping for Custodial Accounts (RIN 3064-AG07), requiring daily reconciliation of beneficial owners |
| ~Nov 2025 | Synapse Chapter 11 dismissed after 19 months without full reconciliation |
| 2025-11-28 | CFPB allocates $46,248,291 from its Civil Penalty Fund to Synapse victims |
| 2026-01-29 | FDIC final rule amending 12 CFR Part 328 published, compliance required by 2027-04-01 |

Blue Ridge Bank, Choice Financial Group, Piermont Bank and Lineage Bank took consent orders across the same window. The pattern to extract: **a fintech's deposit product can be constrained or unwound by an enforcement action against a bank the customer never chose.** And the one rule that would have prevented Synapse directly, the custodial-account recordkeeping proposal, is **still a proposal as of 2026-09-11**. Two years after the collapse, there is no federal daily-reconciliation mandate to rely on, and the signage rule that would police misstatements of insured status does not bite until 2027-04-01.

The chartered-bank failure mode is different and is not the subject here. It is worth noting only that Rho's own published customer stories name SVB as the prior banking relationship for three of fourteen customers, which is a fair reminder that "the big regulated bank" is not a risk-free answer either, just a differently-shaped one.

**Other single points of failure.** A company using the full Rho stack depends on: Under Technologies, Inc. (the contracting party), Webster/Santander (checking and card issuing), ADM plus 400-plus unnamed program institutions (savings), Apex Clearing or Interactive Brokers (treasury custody), RBB Treasury LLC (advisory), Wise US Inc. (international payments, with a separate customer agreement the user must accept), and Slope plus Lead Bank (capital). Rho's marketing presents this as one account. Each is a separate counterparty with separate terms, and only some of those terms are published.

**Rho's own corporate durability.** **Verified** from SEC records: the operating entity, Under Technologies, Inc. (CIK 0001756460), has filed exactly five Form D notices from 2018-10-24 through 2022-01-21, reporting $104,732,452 sold in aggregate, with the last reporting a first-sale date of 2021-10-28. There is no SEC filing of any type since 2022-01-21. The widely repeated "$150M Series C led by Balderton in 2024" has no primary-source basis: it appears only on uncited lead-generation pages whose figures contradict each other, and Balderton's own portfolio listing does not include Rho. Rho's real last round was a $75M Series B announced 2021-12-09, led by Dragoneer and DFJ Growth.

Two caveats that matter. Form D is required only for offerings claiming a Regulation D exemption, so the record proves no *disclosed* equity since January 2022, not that no equity was raised. And Rho did take on financing after 2021: Trinity Capital Inc., a venture-debt fund, lists Rho Business Banking in its portfolio with "Year Invested: 2024," with neither structure nor amount disclosed. Separately, the advisory subsidiary RBB Treasury LLC reported $1,892,904,589 of regulatory assets under management across 1,078 accounts (1,071 corporations or other businesses, 7 charitable organizations) in the Form ADV annual amendment filed 2026-03-25 (Form ADV is the disclosure filing every SEC-registered investment adviser updates yearly). That is a different number from Rho's marketed deposit figures and should not be presented as the same thing.

**Assessment:** no audited financials, no revenue disclosure, no runway statement and no investor update is available to a customer, which is normal for a private company and still leaves a real gap when the counterparty holds your operating cash. The defensible summary is: no disclosed equity round since late 2021, venture debt in 2024, and roughly $1.9B under management in the advisory arm as of March 2026.

### 9.6 The diligence checklist

Eighteen questions to put to Rho in writing before moving a company's operating cash. Each has a reason and a shape a good answer takes. A vendor that answers these cleanly is a good vendor; a vendor that routes them to marketing is telling you something.

**Deposits and insurance**

1. **Is my Rho Checking account a deposit account titled in my company's name at Webster, or a beneficial interest in a pooled FBO account?**
   *Why:* it determines whether FDIC coverage is direct or pass-through, and pass-through coverage depends on the records being right. *Good answer:* a specific structure, named, plus who maintains the ownership records and how often they are reconciled against Webster's books. "Your deposits are held at Webster" is not an answer to this question.

2. **Who reconciles the customer-level ledger to Webster's records, how often, and what happens if they disagree?**
   *Why:* this is exactly what broke in Synapse, and there is still no federal daily-reconciliation rule. *Good answer:* daily, automated, with a named owner and a documented break process.

3. **Send me the current list of every sweep program institution that can hold my savings.**
   *Why:* FDIC coverage aggregates per depositor per bank, so any overlap with your existing banking relationships silently reduces your coverage. *Good answer:* the list, in writing, plus a commitment to notify on changes and a way to exclude named institutions.

4. **What is my actual insured coverage today, not the "up to" number?**
   *Why:* $75M is program capacity on a commercially reasonable efforts basis, not a guarantee, and ADM adds and removes institutions at its discretion. *Good answer:* a current placement report showing balance by institution.

5. **Does ADM or Rho make me whole if a placement error leaves funds uninsured when a program bank fails?**
   *Why:* IntraFi's competing program commits flatly to the $250,000 ceiling and reimburses documented loss from its own non-compliance. ADM promises efforts and no make-whole. *Good answer:* either a written make-whole, or a straight "no," which at least lets you price it.

6. **Am I electing extended deposit insurance or waiving it under Exhibit A, and can I see Exhibit A?**
   *Why:* the published agreement contemplates both elections but does not reproduce the exhibit, and Section 9's collateralization language sits awkwardly with the waiver. *Good answer:* the executed exhibit plus a plain statement of which election applies to you.

7. **What is the real savings withdrawal timeline: the six-per-month, Tuesday/Thursday schedule in the ADM agreement, or "next business day" as the help center says?**
   *Why:* if you keep payroll float in Savings, the difference is whether you can make payroll. *Good answer:* one schedule, in writing, with the cutoff time and the $3,000,000 special-handling threshold spelled out.

8. **Confirm in writing that Rho Treasury is SIPC-protected and not FDIC-insured, and that principal can fall.**
   *Why:* the Vanguard short-term investment-grade fund in the treasury lineup is a bond fund with duration and credit risk, not a cash equivalent, and liquidation runs two to three business days at market prices. *Good answer:* Rho already states this correctly in its footer; you want it attached to your file.

**The contract**

9. **What insurance responds to an operational loss caused by Rho, given the $500 cap?**
   *Why:* the cap means Rho does not underwrite your loss, and no cyber, crime or fidelity coverage is mentioned anywhere in the public corpus. *Good answer:* a certificate of insurance, with limits.

10. **With more than ten cards, how does the Mastercard liability waiver program interact with Section 1.6, and what is the notice procedure that cuts off liability?**
    *Why:* the clause is standard Regulation Z commercial card practice, but the protection that actually stands behind it is the network waiver program, and Rho never explains the interaction. *Good answer:* the waiver program name, its terms, and a documented fraud-notice channel with a response time.

11. **We are a group of entities. Will Section 17 cross guaranty be modified or scoped?**
    *Why:* by default, opening an account for a subsidiary puts the parent behind the subsidiary's card balance. *Good answer:* a negotiated side letter, or a clear "no," which lets you decide which entities to onboard.

12. **Will you commit to a notice period for fee changes and a fee schedule for our term?**
    *Why:* Section 26.4 lets Rho amend fees at any time with continued use as acceptance, and the published fee facts are scattered across pricing footnotes, the Terms of Service and single help articles. *Good answer:* a stated notice period and a fee annex.

**The counterparties**

13. **What changes for us now that Webster is a division of Santander?**
    *Why:* Rho's trust narrative rests on an acquisition that closed 2026-08-20, and nothing published addresses contract continuity or Santander's appetite for partner-bank programs. *Good answer:* a named status for the program agreement, its remaining term, and a transition plan.

14. **Is any partner bank, including sweep program institutions, subject to a public enforcement action?**
    *Why:* between 2023 and 2025 the FDIC, Fed and OCC issued consent orders to Thread, Evolve, Blue Ridge, Choice, Piermont and Lineage, several of which directly constrained fintech programs. These are public and searchable. *Good answer:* a straight answer plus a commitment to notify.

15. **Is there any middleware layer between Rho and Webster, and who holds the authoritative ledger?**
    *Why:* Rho says it integrates directly and built its own core, which if true removes the Synapse topology. It is worth having in writing. *Good answer:* "none, our ledger is authoritative and reconciles daily to Webster," with the reconciliation detail from question 2.

16. **Name every third party that touches our money or data: ADM, Apex or Interactive Brokers, Wise, Slope, Lead Bank, the accounting-data providers, and the AI model providers.**
    *Why:* there is no consolidated sub-processor register anywhere in Rho's public material, and the AI model providers are never named. *Good answer:* a single register with a change-notification commitment.

**Operations and exit**

17. **What are your SOC 2 report period, auditor, Trust Services Criteria in scope, and any exceptions, and what is your incident-notification commitment?**
    *Why:* Rho claims SOC 2 Type 2 but names no auditor, period or scope publicly, and neither the Terms of Service nor the privacy policy commits Rho to telling you about a breach within any timeframe. There is also no published uptime SLA or status page. *Good answer:* the report under NDA, plus a contractual notification window in hours.

18. **Document the exit: what do we export, when does dashboard access end, and who can request closure?**
    *Why:* closure must be requested by the Account Owner only, there is no self-serve close, savings must be drained under the six-per-month limit, treasury liquidation adds two to three business days at market prices, dashboard access ends when the account closes, and Rho has no contractual obligation to return your data. *Good answer:* a written runbook and an agreed export before you sign, not after you leave.

**Assessment on the whole.** Rho's disclosure discipline on the bank-versus-fintech distinction is genuinely above market: it states the FDIC and SIPC scopes correctly, volunteers the "what if Rho shuts down" question, labels the $75M as "up to" and scoped to savings, publishes its sweep administrator's agreement at all, and quotes treasury yields net of fees with an as-of date. The risk in this product is not that Rho hides the model. It is that the model has more moving counterparties than the marketing suggests, that the contract allocates operational risk almost entirely to the customer, and that the parts you most need in writing (the program institution list, the Webster deposit agreement, Exhibit A, the SOC 2 scope, the reconciliation process) are exactly the parts that are available only on request.
## 10. Open questions and how to keep this document current

Everything above was written from public sources, a free sandbox, and SEC filings. That combination has a hard edge. This section says where the edge is, which facts will move first, how the document was actually assembled, and how to re-run it.

### 10.1 What this research could not settle

Four groups. For each question: why it stayed open, and the single cheapest place the answer actually lives.

#### Pricing and economics

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| What Rho Capital (its revolving credit line) actually costs | No rate, APR, factor rate or price range is published on any Rho page. Four Capital-related URLs missing from the local crawl were fetched live on 2026-09-11 and none prices it. Rho's own wording, on /blog/rho-capital, is that rates are "based on your business's cash flow and shown during your application" | A live application from a Rho account, which is the channel /blog/rho-capital names, or the resulting Slope / Lead Bank credit agreement, which /product/capital names as where "your exact pricing is disclosed" |
| Rho's revenue, deposit balance and unit economics | Never disclosed and never estimated by a credible third party. Interchange (the fee a card network routes to the card issuer on every swipe) is an inference about Rho's revenue, not a corpus disclosure: the word never appears in connection with Rho anywhere in 556 captured pages | Nothing public. Rho is private with no filing obligation. The nearest proxy is Trinity Capital's schedule of investments (a business development company must itemize its portfolio positions in its 10-K and 10-Q), which would give the size, rate and maturity of the 2024 debt facility |
| Whether a returned domestic wire costs $0 or $20 to $45 | rho.co/pricing line 07 says "Domestic wire recall fee $0". One help-center article says "a fee of around $20 - $45 will be deducted" for failed and returned domestic wires. Both are live | A support ticket, or a real returned wire on a funded account |
| What "platform access after year one is $1,000 annually" buys at Rho Incorporation | The sentence appears exactly once, on one page, and the corpus never defines what platform access covers or whether it is a registered-agent renewal | A sales call or the incorporation engagement letter |
| The real qualification gate for the Monthly Terms card | Three live Rho numbers: $25,000 minimum cash balance (help center), $75,000 combined across Rho and linked external accounts (product page and FAQ), and "balances reach $15,000" (/product/corporate-cards) | A live card application, or a sales call |
| Whether a 100% Vanguard (VFSTX) Treasury allocation can actually be selected | The 4.66% headline assumes it; the product rules cap the short-term bond fund at 50%; the help center says pre-existing allocations above 50% are grandfathered and a higher limit "can be approved". The allocation UI was never observed | A funded Treasury account (the $50,000 minimum), or RBB Treasury's Form ADV Part 2A wrap-fee brochure, which Rho links but does not host |

#### Product mechanics

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| Rho's MCP tool names, count and schemas | Not published anywhere. The docs promise the names never change but never print one. The sandbox host has no MCP endpoint (404), so MCP exists only in production | Connecting a client with a live production token and listing the tools. This is the largest single gap in this document |
| Whether `cards:read` and `invoicing:read` are actually grantable | The public OAuth metadata enumerates five scopes; the Authentication guide's scope table lists three. Either the docs lag the product or the metadata is ahead of it | The OAuth consent screen on a real account |
| Whether MCP calls share the 60-requests-per-minute token budget | Never stated. No rate-limit response headers exist to measure it against | A production token and a load test, or Rho support |
| Which payment rails Bill Pay really uses | The product page is written as check-only ("pay by check", "$0 On domestic check payments"). The help center lists ACH, domestic and international wires, checks and single-use cards. A separate help-center vendors article says the Bill Pay workflow "does not currently support Vendor Cards". Three Rho sources, three answers | A live Bill Pay draft on a funded account |
| Rho's international AP coverage | Wise US Inc. is named as the provider, but the country, currency and payment-method counts are unpublished. This is the largest unfilled gap against Tipalti and Corpay | A sales call, or the product itself |
| Which savings withdrawal schedule governs | The published American Deposit Management agreement says requests process Tuesdays and Thursdays for Wednesday and Friday settlement, capped at six per month. Rho's help center says savings-to-checking "typically settles the next business day". Rho's settlement-times page says two business days | A funded savings account, or support |
| Which banks are in the $75M sweep network | "The current list of network institutions is available from Rho support on request." It matters because FDIC insurance (the federal government's per-depositor, per-bank deposit guarantee, $250,000) aggregates across accounts at the same bank, so an existing relationship with a network bank silently erodes coverage | A support request for the Program Institution list and ADM Schedule A |
| Whether Departments is being migrated to Fields | Newer accounts get Fields and have no Reporting tab; older accounts have Departments. No migration, deprecation or sunset notice exists anywhere in 269 help pages | A support ticket, or accounts on both cohorts |
| What happens on day 31 or day 61 of a pre-EIN window with no EIN | Stated nowhere in the corpus | A support ticket |
| SOC 2 scope, auditor, report period and exceptions | The auditor is never named, the Trust Services Criteria in scope are never stated, and the Trust Center is not in rho.co's sitemap | Requesting the report through Rho's Trust Center link |

#### Corporate and financial

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| Whether Rho raised equity after 2021 | Form D (the notice a company files with the SEC when it sells securities under the Regulation D private-placement exemption) is required only for Reg D offerings. A round sold under Section 4(a)(2) or offshore under Regulation S generates no filing. Rho's filing entity, Under Technologies, Inc. (CIK 0001756460), has filed five Form Ds totaling $104,732,452 and nothing of any type since 2022-01-21. Forge's $131.01M total implies a roughly $26M gap worth chasing | EDGAR is already exhausted. Secondary-market trackers, a Rho announcement, or a new Form D |
| Rho's current board and executive team | Disclosure stops at the January 2022 Form D. Whether Alex Wheldon has formally left and whether Sebastjan Trepca is still CTO are both unresolved | Company announcement, LinkedIn, or press |
| When and why the Evolve Bank & Trust relationship ended, and whether deposits moved | Nothing found in any source | Rho or Evolve directly |
| Whether Santander will continue the Webster sponsor-bank program | Rho's entire deposit story runs through Webster Bank, now a division of Santander Bank, N.A., following a transaction that closed roughly three weeks before this corpus was captured. No public statement either way on program continuity | Santander investor relations, or the Webster Deposit Account Agreement, which Rho incorporates by reference but does not publish |
| Rho's deposit base | "$4B+ in deposits" and "$4 billion moving monthly" are marketing figures. The only auditable number is Rho Treasury's regulatory assets under management, a different quantity entirely | The next Form ADV annual amendment (the disclosure form a registered investment adviser files with the SEC), CRD 314581, filed each March |
| Terms of the Trinity Capital 2024 facility | Trinity lists "Rho Business Banking" with "Year Invested: 2024" and discloses neither structure nor amount on that page | Trinity Capital's 10-K or 10-Q schedule of investments |
| Whether Mercury's bank charter becomes final | The OCC granted preliminary conditional approval on 2026-04-24. Final authorization to open, FDIC deposit insurance and Federal Reserve approvals were all still outstanding as of 2026-09-11 | The OCC Corporate Applications Search tool, which replaced the OCC Weekly Bulletin on 2025-12-19 |
| Whether Ramp's reported $60B round closed | PYMNTS reported early talks on 2026-09-08. $44B (Series F, closed 2026-06-04) is the last closed mark | Ramp's newsroom or a PR Newswire release |
| Reddit and practitioner sentiment on Rho | Never sampled. It is the most likely place to find unvarnished founder experience, and its absence is a real hole in the customer-evidence picture | r/startups, r/smallbusiness, r/ycombinator |

#### API and agent roadmap

Rho says, in the changelog dated 2026-08-03: "Read-only is live today. Write access and webhooks are next." And in the launch blog dated 2026-07-29: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval." No date accompanies either.

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| When write endpoints ship, and whether they land inside `v1` | Rho's versioning policy makes new operations "additive" and therefore non-breaking, so write tools could appear in `/mcp/v1` with no version bump. The 15-day notice floor covers deprecations, not capability additions | Watch the OAuth protected-resource metadata for a non-`:read` scope. That is the earliest public signal and it needs no account |
| Whether dynamic client registration will be enabled | `POST https://auth.rho.co/oauth2/register` returns "Dynamic registration is not enabled", so third-party MCP clients cannot self-register and every integration is a hand-registered partner | Re-test the endpoint; or ask Rho |
| Whether an MCP sandbox is planned | The sandbox host 404s on `/mcp/v1` and the docs never mention it | Rho support or a changelog entry |
| Whether webhooks, idempotency keys, rate-limit headers, ETags, an audit-log surface or a users endpoint are on the roadmap | None exist. Rho has committed publicly only to write access and webhooks | Changelog and docs diffs |
| Whether an MCP call counts as activity against the 45-day token inactivity clock | Never stated | Rho support |
| What production returns that the sandbox never shows | The sandbox dataset exercises 22 of 33 transaction types, 5 of 11 card statuses and 3 of 7 spending-limit types, including none of the treasury transaction family | A production token |

**Assessment:** the open questions cluster in a revealing pattern. Almost everything unanswered is either behind a sales conversation, behind a funded account, or on a roadmap Rho has announced but not dated. Very little is genuinely unknowable. A reader with a Rho account and one sales call could close roughly two-thirds of this list in a week.

### 10.2 Facts with the shortest shelf life

Every row here was true on the as-of date given. Rows are ordered roughly by how fast they decay.

**Rho**

| Fact | Value | As of | Re-check at |
| --- | --- | --- | --- |
| Treasury headline net yield | "up to 4.66%" ($20M+ tier, 0.15% fee) | 2026-09-11 (the page hero was stamped 09/12/2026 and the footnote 09/11/2026 on the same capture) | rho.co/treasury-yield-comparison. Updates daily and automatically |
| Component fund net yields | VFSTX 4.66%, MULSX 3.70% at the top tier | 2026-09-11 | rho.co/product/treasury tier matrix |
| 13-week T-Bill benchmark on Rho's comparison table | 3.81% | 2026-09-11 | rho.co/treasury-yield-comparison |
| Business Savings rate | "up to 1.00% APY (variable)" on a $25,000 average monthly balance | August 2026 | rho.co/product/business-savings-account |
| Partner microsite offers | 77 pages; 25 gate at $400K to $500K, 11 at $100K to $300K, 25 at $50K or less, 16 with no balance test | 2026-09-11 | rho.co/sitemap.xml plus each page. Every partner page says the offer "may be changed or discontinued at any time without notice" |
| API surface | 14 operations, all GET, across 5 resources; 5 scopes, all `:read` | 2026-09-11 | docs.rho.co/api/v1/openapi.md and rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1 |
| Write endpoints and webhooks | Neither exists | 2026-09-11 | rho.co/changelog. Announced as "next" on 2026-08-03 |
| Terms of Service | Version 7.0.0, last updated 2026-08-27 (page also datelined 2026-08-04) | 2026-09-11 | rho.co/policies/terms-of-service. Rho reserves the right to amend at any time |
| Rho Treasury regulatory AUM | $1,892,904,589 across 1,078 accounts (1,071 businesses, 7 charities) | Form ADV annual amendment filed 2026-03-25 | reports.adviserinfo.sec.gov, CRD 314581. Next amendment due around March 2027 |
| Rho Capital maximum line | $5M on /product/capital, $2M in the /blog/rho-capital Highlights block | 2026-09-11 | Both pages. Rho's own two numbers disagree |
| Invoicing accounting sync | QuickBooks Online only, shipped 2026-08-31. /product/invoicing still says no accounting sync exists | 2026-09-11 | rho.co/changelog and rho.co/product/invoicing |
| Rho's own competitor comparison data | Footnote dates spread from 08/02/2026 to 09/11/2026 by page | varies | Each page's own footnote. Treat every one as its own as-of date |

**Competitors**

| Fact | Value | As of | Re-check at |
| --- | --- | --- | --- |
| Ramp valuation | $44B (Series F, $750M, closed 2026-06-04); reported in early talks at about $60B | Talks reported 2026-09-08 (PYMNTS) | Ramp newsroom, PR Newswire |
| Ramp scale (self-reported, unaudited) | 70,000+ customers, $200B+ annualized purchase volume | 2026-06-01 | Ramp press releases |
| Ramp Developer API size | 252 documented operations across 40 resource groups | 2026-09-11 | docs.ramp.com/llms-api.txt. Drifts as Ramp ships |
| Mercury charter | OCC preliminary conditional approval only. Final authorization, FDIC insurance and Fed approvals outstanding | 2026-04-24 (OCC letter) | OCC Corporate Applications Search |
| Mercury scale (self-reported, unaudited) | 300,000+ businesses and individuals, $650M+ annualized revenue (a run rate, first reported for 2025), four years GAAP profitable | Reported 2026-04-27 | Mercury press releases |
| Mercury MCP | 31 tools, all read-only | 2026-09-11 | docs.mercury.com/docs/supported-tools-on-mercury-mcp |
| Mercury Pro tier | $350/month month-to-month, $299 on annual billing; no phone support on any plan | 2026-09-11 | mercury.com/pricing. The support posture is the single item here most likely to change once the charter lands |
| Brex ownership | Wholly owned subsidiary of Capital One, N.A. since 2026-04-07. Provisional purchase consideration $4,521M, still subject to post-closing adjustment | Q2 2026 10-Q, filed 2026-07-28 | SEC EDGAR, Capital One CIK 0000927628. A revision is likely in the Q3 10-Q or the 2026 10-K |
| Bank MCP server census | 10 first-party bank or banking-platform servers worldwide, 5 read-write, 4 able to make payments. Rho is not listed | 2026-09-11 | openbankingtracker.com/banks-with-mcp-servers. An aggregator that self-reports as incomplete, so treat it as a floor |

### 10.3 How this document was built

**The corpus.** Measured on disk, not estimated:

| Source | Count |
| --- | --- |
| rho.co page captures | 556 (130 core marketing, product and policy pages; 269 help-center articles; 125 comparison blog posts; 25 partner microsites; 7 others) |
| Partner microsites fetched live during verification | 52 more, completing the 77-page census |
| docs.rho.co guide pages | 13 (12 guides plus the docs index page) |
| API operation references | 14, plus the OpenAPI document |
| Sandbox probe artifacts | 2,490 files across auth, pagination, filters, limits and resource probes |
| External primary-source captures | 55 (SEC filings, the Form ADV PDF, the OCC decision, CFPB complaint data, Terms of Service full text) plus 31 Ramp captures |
| Machine-readable site files | sitemap.xml (1,042 URLs), site-llms.txt, site-llms-full.txt, the status page JSON API |
| Research output | 29 findings files, 305,887 words |

A note on one number: earlier files inside this project describe the corpus as "522 pages" and "536 pages". Both are undercounts taken mid-crawl. The count at the end of the crawl is 556. Where this document and its working files disagree, 556 is right.

**The two-pass method.** Pass one: 29 topic agents each read a slice of the corpus and wrote a findings file recording claims with verbatim quotes and absolute file paths. Pass two: 16 load-bearing claims were extracted and handed to independent checkers whose instruction was to refute them, with the corpus plus live web access. Their output is the verified claim register, shipped beside this document as `research/VERIFIED_CLAIMS.md`, and it is the authority wherever it disagrees with a findings file (`research/findings/`).

**What verification changed.** Of 16 claims, one came back CONFIRMED and fifteen came back PARTIALLY_CONFIRMED. None came back clean. Concretely:

- Mercury's charter date moved from 2026-04-27, the press announcement, to 2026-04-24, the date on the OCC letter, and "conditional approval" became "preliminary conditional approval", which is the OCC's own term and materially weaker.
- A widely repeated "$150M Series C led by Balderton Capital in 2024" was deleted outright. Five Form Ds totaling $104,732,452, nothing filed since 2022-01-21, and Balderton's portfolio does not list Rho.
- "1,078 business accounts" in the Form ADV became 1,071 businesses plus 7 charitable organizations.
- The alarming 10-card unauthorized-use clause stopped being a Rho term. It is a near-verbatim restatement of Regulation Z, 12 C.F.R. 1026.12(b)(5), Brex carries the same clause, and the number comes from the CFPB rather than from Rho.
- "Two balance thresholds, no middle tier" on the partner microsites was refuted by a full 77-page census that found a continuous ladder with eleven pages in a $100K to $300K middle band.
- "The 4.66% Treasury headline is mathematically unreachable" softened to "unreachable under the standard published allocation rules", because the help center documents two routes past the 50% Vanguard cap.
- "Months after" on the stale QuickBooks invoicing claim became eleven days.
- "The footnote discloses that Slope underwrites the line" became "the body pricing copy says so", which removes most of the fine-print sting.
- A claim that Rho's affiliate agreement disclosed interchange economics was found false. Interchange appears nowhere in the corpus as a Rho revenue line.
- A claim searching "the 1042-URL corpus" was corrected: 1,042 is the sitemap count, not what was read.

**Assessment:** the adversarial pass changed a number, a date, a scope or a framing in every claim it touched, and it killed one entirely. That is the headline methodological finding. Anything in this dossier not traceable to the verified register should be read as first-pass research that has not been attacked.

**Known limits, stated plainly:**

1. **The production API was never exercised with a real token.** Every statement about production behavior rests on documentation, on the public unauthenticated OAuth metadata, or on a 401 response body. The record counts quoted throughout (14 accounts, 8 cards, 72 transactions, 33 statements, 7 invoicing customers, 12 invoices) are sandbox counts.
2. **No Rho account was opened.** Nothing was observed inside the product: no onboarding flow, no Treasury allocation screen, no Bill Pay draft, no MCP consent dialog, no tool list, no admin audit log.
3. **No sales conversation and no support ticket.** Every question whose answer lives behind "contact Rho" is open, which is most of section 10.1.
4. **Competitor scale figures are self-reported where noted.** Ramp's 70,000 customers and $200B volume, and Mercury's 300,000 businesses, $650M annualized revenue and four years of GAAP profitability, are company boilerplate reproduced by press outlets. They are attributed, not confirmed.
5. **The sandbox is not production.** It has no MCP endpoint, it does not enforce the documented rate limits (150 requests on one token in a 57-second window, and an instantaneous burst of 68.9 requests per second, both with zero 429s), and its dataset never produces roughly a third of the enum values the docs define.
6. **Rho's own comparison tables were not used as evidence about competitors.** Rho's /product/api table claims Brex has no documented MCP integration. Brex's changelog dates its MCP server to April 2026, and Rho's own blog reversed the claim five days later.
7. **Scope was English-language and US-focused.** Non-US regulatory posture, non-US competitors and non-English coverage were not examined.
8. **Practitioner sentiment was never sampled.** No Reddit, no G2, no customer interviews.

### 10.4 Refresh procedure

Re-runnable in about two hours, most of it unattended. Everything this procedure references ships beside this document in `research/`: the crawler (`research/tools/fetch_all.sh` and `fetch_page.py`), the URL lists (`urls-core.txt`, `urls-help.txt`, `urls-blog-comp.txt`), the 556-page corpus (`research/corpus/rho-co-pages/`), the stored sitemap (`research/tools/site-sitemap.xml`), the sandbox probes and their captured output (`research/sandbox/`), the 29 findings files (`research/findings/`) and the verified claim register (`research/VERIFIED_CLAIMS.md`). All paths below are relative to this document. One caveat before you start: `sandbox/census.py` and `sandbox/probe.sh` still carry the absolute output paths of the original run, three lines in total, so repoint them before re-running.

1. **Stamp the run.** Fix today's date at the top. Every number you touch gets that stamp or an older one, never no stamp.
2. **Re-crawl.** Run `research/tools/fetch_all.sh` over `research/tools/urls-core.txt`, `urls-help.txt` and `urls-blog-comp.txt`, writing into a fresh `pages2/` tree, then `diff -rq` it against `research/corpus/rho-co-pages/`. The non-empty diffs are your entire change list. Most files will be byte-identical; the Treasury pages will always differ because the yield date rolls.
3. **Diff the sitemap.** Re-fetch `https://www.rho.co/sitemap.xml` and compare the URL set against the stored 1,042. New `/product/*` and `/partner/*` slugs, and pages that disappeared, are the highest-signal changes on the marketing side.
4. **Re-stamp the rate-bearing pages by hand.** `/product/treasury`, `/treasury-yield-comparison`, `/product/business-savings-account` and `/pricing`. Rewrite the yield rows in 10.2 and note the new footnote dates.
5. **Read the changelog forward.** `rho.co/changelog`, everything newer than the last entry you recorded. As of 2026-09-11 the newest entry was 2026-08-31 and there was no September entry at all.
6. **Re-pull the API contract.** Fetch `https://docs.rho.co/api/v1/openapi.md`, count operations and scopes, and diff against 14 and 5. Then `curl https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` and read `scopes_supported`. **A non-`:read` scope appearing there is the single highest-signal event this document tracks**, because it is the first public sign that Rho's agent surface can move money, and it costs one unauthenticated request to check. Also re-fetch `https://auth.rho.co/.well-known/openid-configuration` and re-test `POST https://auth.rho.co/oauth2/register` for whether dynamic client registration is still disabled.
7. **Re-run the sandbox census.** `research/sandbox/census.py` and `research/sandbox/probe.sh`. You are looking for new operations, new enum values and changed record counts, not for new data.
8. **Check the corporate record.** `https://data.sec.gov/submissions/CIK0001756460.json` for Under Technologies, Inc.; any new filing is a funding event. Then the Form ADV for CRD 314581, whose annual amendment lands each March and carries the AUM and account counts.
9. **Check the competitors.** OCC Corporate Applications Search for Mercury Bank, N.A. final approval; Capital One's next 10-Q for a revised Brex purchase price; Ramp's newsroom for the rumored round; `docs.mercury.com` and `docs.ramp.com` for tool and operation counts; `brex.com/changelog`.
10. **Re-verify anything that moved.** A claim that survived an adversarial check in September is not still verified once its underlying number changes. Re-run the refutation pass on every claim whose evidence you just edited, and re-date the entry in `research/VERIFIED_CLAIMS.md`.

**Suggested cadence:** steps 4 and 6 monthly, because yields and the scope list are the fastest-moving things here. Steps 2, 3, 5 and 7 quarterly. Step 8 on the filings' own calendar, which means Form ADV each March and 10-Qs in the month after each quarter end. Step 9 whenever a competitor makes news, since all four of them announce on their own schedule and this document goes stale from the competitive side first.
