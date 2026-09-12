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
