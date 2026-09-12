# Rho: Money-Movement Mechanics (Accounts, Rails, Timing, Limits, Insurance)

Source corpus: local snapshot of rho.co help center, product pages, policies, docs.rho.co and the Rho API reference/sandbox. Every fact below is grounded in that corpus. Rho's own pages are marketing or self-published documentation; facts asserted only by Rho are labelled **[Rho claim]**. Where Rho stamps an as-of date, the date is carried through. Today is 2026-09-11.

Primary sources used (paths relative to `scratchpad/rho/`):
- `pages/help/help-center__payments__*.txt` (32 pages)
- `pages/help/help-center__banking*.txt` (23 pages)
- `pages/help/help-center__treasury__*.txt` (5 pages)
- `pages/help/help-center__general-rho-information__{how-does-fdic-insurance-coverage-work, our-partnership-with-webster-bank-n-a-member-fdic, rho-savings-account-terms-and-conditions, pricing-requirements, how-to-close-your-rho-account}.txt`
- `pages/help/help-center__{bill-pay,cards,vendors,invoicing,admin,mobile-app}__*.txt`
- `pages/core/{pricing, product__business-banking, product__business-savings-account, product__treasury, product__capital, policies__terms-of-service, policies__yield-methodology, faq}.txt`
- `docs/docs_v1_accounts.md`, `docs/docs_v1_transactions.md`, `api/transactions_listtransactions.md`, `api/accounts_listaccounts.md`, `sandbox/accounts.json`

---

## 1. Who actually holds the money (legal stack)

| Layer | Entity | Role | Source |
|---|---|---|---|
| Platform | Under Technologies, Inc. DBA Rho Technologies | Fintech, **not a bank** | ToS; every page footer |
| Checking + cards | **Webster Bank, a division of Santander Bank, N.A., Member FDIC** ("Sponsor Bank") | Holds checking deposits; issues Rho Mastercard cards | ToS §; Webster partnership page |
| Savings sweep | **American Deposit Management, LLC + ADM Consulting, LLC ("ADM")** | Agent that deploys deposits into 400+ Program Institutions | Savings T&C (ADM Master Services Agreement) |
| Treasury custody | **Apex Clearing Corporation** (primary) and **Interactive Brokers LLC** | Registered broker-dealers, members FINRA/SIPC | About Rho Treasury; ToS |
| Treasury advisory | **RBB Treasury LLC dba Rho Treasury**, SEC-registered RIA, Rho subsidiary | Investment management | About Rho Treasury |
| International / FX payments | **Wise US Inc.** | "International and foreign currency payments services are provided by Wise US Inc." | pricing.txt footnote; business-banking footer |
| Capital (credit line) | **Lead Bank** makes the loans; **Slope** underwrites | "Business-purpose loans made by Lead Bank"; "Fees vary based on risk assessment and loan term... set when Slope underwrites your line" | About Rho Capital; product__capital |
| Invoice card acceptance | **Stripe** (Rho creates and manages a separate Stripe account for the business) | Card acquiring on invoices | Accept card payments on invoices |
| External bank linking | **Plaid**, **Mastercard Data Connect** (Finicity), **Stripe Financial Connections** | Account linking / verification | How to connect to an external bank account |

Webster Bank: founded 1935; as of **August 20, 2026** part of Santander's **$327 billion-asset** U.S. banking organization (per Santander's completion announcement, cited by Rho). Rho routing number for checks/ACH: **021913655** (stated in the check-endorsement instructions).

Notable: `sandbox/accounts.json` shows routing_number_last_4 = **"0089"** on checking and savings accounts, which does **not** match the last 4 of 021913655 ("3655"). Sandbox is synthetic, so this is fixture data, not evidence of a second routing number. Conspicuously **not stated** anywhere in the corpus: a separate wire-only routing number for Rho, even though Rho's own comparison text warns that "many banks have different routing numbers reserved for receiving ACHs, separate from the routing number they use to receive wires."

---

## 2. Account types and what each can do

### 2.1 The five account types (from the Rho API, which is the most precise enumeration)

`docs/docs_v1_accounts.md` + `api/accounts_listaccounts.md`: `account_type` enum = **`checking`, `credit`, `investment`, `savings`, `rewards`**. `account_type` is **immutable for the lifetime of an account**. Balances are returned in **minor units** (integer cents) with an ISO 4217 currency code.

| `account_type` | Product name | Can send | Can receive | Interest / yield | Insurance |
|---|---|---|---|---|---|
| `checking` | Rho Checking (primary + unlimited sub-accounts) | ACH, domestic wire, international wire, printed check, internal transfer | ACH, wires, RDC check deposit, linked-account pull, internal transfer | None stated | FDIC to **$250,000 per entity** via Webster |
| `savings` | Rho Business Savings | Only internal transfer → Rho Checking; **6 withdrawals/month max** | Only from Rho Checking; **no limit on transfers in** | Up to **1.00% APY** variable (as of Aug 2026); $25,000 average monthly balance required | FDIC up to **$75,000,000 per entity** via ADM sweep |
| `investment` | Rho Treasury | Only to Rho Checking | Only from Rho Checking | Net yield up to **4.66%** (as of 09/11/2026) | **Not FDIC.** SIPC to **$500,000** incl. **$250,000** cash |
| `credit` | Rho Card credit account (Daily or Monthly Terms) | n/a (card spend) | Repayments via ACH from Rho Checking or a linked external account | n/a | n/a |
| `rewards` | Rewards Account (cashback) | Transfer to Primary Operating Account, **deposited instantly** | Cashback accruals | n/a | n/a |

Sandbox reality check (`sandbox/accounts.json`, 14 accounts): 6 `checking` (named "Reserve Checking", "Cash (Checking)" x2, "Treasury Checking", "Inventory Checking", "Primary Checking"), 4 `credit`, 2 `rewards`, 2 `savings`. **Zero `investment` accounts appear in the sandbox fixture** despite the enum, and the Treasury sleeve appears only as a *checking* account named "Treasury Checking". Only `checking` and `savings` rows carry `account_number_last_4` / `routing_number_last_4`; `credit` and `rewards` rows carry neither, i.e. those account types have no routable account number.

### 2.2 Sub-accounts / multiple operating accounts

- "All businesses get access to a primary Rho Checking Account." Additional sub-accounts are created via Banking → **Create Account**. Webster partnership page advertises **"Unlimited secondary checking accounts."**
- **FDIC is per customer, not per account**: "Each Rho customer gets up to $250,000 in FDIC deposit insurance coverage **across all Rho checking accounts**." The FAQ repeats: "Funds are FDIC insured up to $250,000 **per entity, not per account**."
- Sub-accounts **cannot be individually linked** to an external bank: "you will not be able to directly link a 'sub-account' to an external account. All external accounts are linked to the Rho account as a whole (subs included)." You can still choose the destination sub-account at deposit time.

### 2.3 DACA accounts

Rho offers **Springing DACAs** only (Deposit Account Control Agreements, with Webster). **Fully-Blocked DACAs are not supported.** Virtual Account Numbers are available in the mobile app **excluding DACA accounts**.

### 2.4 Virtual Account Numbers (VANs)

- Available in the mobile app, found in the Account Details drawer alongside the standard account and routing numbers.
- **Credit-only**: "VANs can only be used to receive funds - they cannot be used to initiate payments or withdraw funds."
- Purpose stated: fraud reduction by not exposing the primary account number.

### 2.5 Eligibility gates on the account itself

- Entity must be **incorporated in the United States**, and must either hold a **US operating address** or have **one business owner based in the US with a valid SSN**.
- **Sole proprietorships are not eligible**; must be a registered LLC or corporation.
- Ineligible owner locations (also full payment restriction): Cuba, Iran, North Korea, Russian Federation, South Sudan, Sudan, Syria, Venezuela.
- Treasury adds: US-registered business, operating primarily in the US, at least one US-based founder, and **at least $50,000 in total deposits**; application <10 minutes, approval typically **2 business days** (one page says "up to 2 business days").

---

## 3. Fee schedule (exact, with as-of dates)

From `pages/core/pricing.txt` (the canonical fee summary) plus help-center pages:

| Item | Fee | Source / date |
|---|---|---|
| Same-Day ACH (outgoing) | **$0** | pricing.txt |
| Domestic wires (outgoing and incoming) | **$0** | pricing.txt; "$0 domestic wires" as of 08/02/2026 |
| Printed checks | **$0** | pricing.txt ("Same-Day ACH, wires, and checks $0") |
| Subscription / platform fee | **$0** | pricing.txt |
| Per-user fee | **$0** | pricing.txt |
| Checking account minimum fee | **$0** | pricing.txt |
| AP (Bill Pay), Expense, Accounting automation | **$0** | pricing.txt |
| **Foreign-currency transfer (FX conversion)** | **1%** | pricing.txt; "1% FX rate" repeated on intl-wire page; as of 08/02/2026 |
| **Domestic wire recall fee** | **$0** | pricing.txt |
| **International wire recall fee** | **$30** | pricing.txt footnote |
| **Optional SWIFT / "cover all recipient delivery fees" toggle** | **$15 flat** | pricing.txt footnote; intl-wire page; Bill Pay intl page (as of 08/02/2026) |
| **Failed/returned domestic wire** | **~$20 - $45**, deducted from the Rho account | Fees For Recalls & Failed Wires; restated "as of 08/02/2026" on the failure-troubleshooting page |
| Recalls (ACH and wire) themselves | **Free** | How to Cancel, Reverse or Dispute a Bank Transfer |
| Card payments on Rho Invoices (acquiring) | **2.9% + $0.30 per transaction**, paid by the business; surcharging not available | Accept card payments on invoices |
| Rho Treasury management fee | **0.15% - 0.60%/yr**, billed monthly, tiered by AUM | About/Managing Rho Treasury |
| Card late fee | **3% of the delinquent balance per month, up to 6 months** | ToS §; pricing.txt footnote |

**Contradiction to flag:** pricing.txt lists "Domestic wire recall fee $0" while the help center says a failed/returned domestic wire costs **~$20-$45**. These are arguably different events (a customer-requested recall vs. a bank-returned wire), but Rho never reconciles them on the same page, and the $20-$45 charge is presented as automatic ("will be deducted from your Rho account for any domestic wire payments that fail and are returned").

Also note the pricing footnote's own hedge: "International wires in USD can be subject to additional fees set by recipient, correspondent, or intermediary banks, in addition to the SWIFT network," and "Rho may not have visibility to additional fees incurred by the recipient, intermediary, or correspondent banks' fees while the funds are in transit."

Promotion in the global nav: "**$100 when you deposit (terms apply)**." Incorporation: $400 Delaware deposit refunded once you open a Rho account and maintain a **$10,000 average checking balance for 60 days** (as of 08/02/2026).

---

## 4. Cut-off times (the complete list found in the corpus)

| Cut-off | Applies to | Consequence of missing it | Source |
|---|---|---|---|
| **2:00 pm ET** | Outgoing ACH (push) | Same-day if before 2pm **and** under $1mm; otherwise next day / 1-3 business days | Payment Settlement Times; Transfer FAQs |
| **2:00 pm ET** | Card repayment ACH pulls | "begin processing the same day" before 2pm; next-day processing after | How to Pay Your Credit Card Balance |
| **2:00 PM ET** | **Incoming** deposits generally | "Deposits made after 2PM ET on a business day or on a Saturday, Sunday or bank holiday are considered received on the next business day" | Payment Settlement Times (note) |
| **4:45 pm ET** | Outgoing domestic wires | Same-day arrival before 4:45; next business day after | Payment Settlement Times; Transfer FAQs; Webster partnership page |
| **3 PM ET** | **Incoming** domestic wires | "Domestic Wire payments will reach your account within the same day if sent before 3 PM ET in most cases" | How To Fund Your Account |
| **1 pm ET** | Checking → Savings | Settles same business day if before 1pm ET | Understanding Rho Savings Accounts; Savings Sweep |
| **1 pm ET** | Savings → Checking | Settles next business day if before 1pm ET | Understanding Rho Savings Accounts; How to Close Your Rho Account (as of 08/02/2026) |
| **3:00 PM ET** | Treasury withdrawal funded from IJTXX / uninvested cash | Same business day before 3pm; next business day after | Managing your Rho Treasury account |
| **5:00 PM ET** | Treasury T-Bill sale | Before: next business day allocation / 2 business days; after: 3 business days | Managing Treasury; Payment Settlement Times |
| **4:00 PM ET** | Treasury mutual-fund redemption (MULSX, VFSTX/VFSUX) | Before: 1-2 business days / 2 business days; after: 3 business days | Managing Treasury; Payment Settlement Times |
| **~4:00 am ET** | Release time for **all** scheduled and recurring payments | Payment does not go out; marked overdue; **does not auto-retry the next business day** | What Time Are Scheduled Payments Sent Out; Bill Pay scheduling page |
| **~4:00 am ET** | Deadline for approvals on scheduled payments | Unapproved at 4am ET = not released | Same |
| **8:00 a.m. ET** | Auto-transfer rule evaluation | Rules evaluated daily at 8am ET on applicable business days | Setting up auto-transfer rules |
| **just after midnight EST** | Daily-Terms card auto-repayment debit from Rho Checking | Debits the prior day's settled charges | The Rho Card with Daily Terms |
| **12:00 P.M. Central Time** | ADM savings-sweep deposit cut-off | Deposits received by the Custodian before 12pm CT are deposited with Program Institutions **the next business day** | ADM Master Services Agreement §3 |
| **12:00 P.M. Central Time** on a Processing Day | ADM savings-sweep withdrawal cut-off | Before: settles next Settlement Day; after: settles the Settlement Day **after** that | ADM MSA §4 |

Business day definition Rho publishes: "Business Days means Monday through Friday, excluding bank holidays."

Scheduled-payment hard rules (three separate failure modes, all on the same page):
1. You **cannot schedule a payment for the same day** it must go out. It will not release and will not roll to the next business day; it shows as **overdue**.
2. Payments needing approval must be approved **before 4am ET on the due date**.
3. **Bill Pay bills only**: a payment date on a Saturday or Sunday will not send and shows as overdue.
To pay in real time you must use the **Make A Payment** button and choose **"Send Now"** (vs "Send Later").

Recurring-transfer date arithmetic: the transfer executes on the exact calendar date each period "regardless of whether it's a weekend or not"; for short months, Jan 31 monthly becomes **Feb 29, Mar 31, Apr 30** (Rho's own example, implying a leap year). Execution date is not the settlement date.

---

## 5. Settlement times: the canonical tables

### 5.1 Incoming (money landing in a Rho account)

| Payment type | Settlement time | Notes |
|---|---|---|
| Incoming Linked Account Transfer (runs over ACH) | **Up to 5 business days** | Rho's own example: initiated Monday morning should land Thursday afternoon |
| Incoming ACH | **1-3 business days** | "An ACH pull can take 2-3 business days, and a push can take 1-3 business days" |
| Incoming Domestic Wire | **1-2 business days** | Fund-your-account page says same-day if sent before **3 PM ET** "in most cases" |
| Incoming International Wire | **1-5 business days** | Rho asks to be told in advance if you expect them |
| Remote Check Deposit (RDC) | **2-3 business days**, subject to risk-based monitoring, **generally up to 6-7 business days** | See §8 contradiction |
| Savings → Checking | **2 business days** (settlement-times page) | Savings pages say **next business day** if before 1pm ET |
| Treasury → Checking, T-Bills | **2 business days** if initiated before 5 pm ET; **3 business days** if after 5 pm ET, on a weekend, or a market holiday | |
| Treasury → Checking, mutual funds (MULSX or VFSTX) | **2 business days** if before 4 pm ET; **3 business days** if after 4 pm ET, on a weekend, or a market holiday | |

### 5.2 Outgoing (money leaving a Rho account)

| Payment type | Settlement time |
|---|---|
| Outgoing ACH | **Same-day if created before 2 pm ET AND under $1mm**; next day if after 2 pm ET or over $1mm |
| Outgoing Domestic Wire | **Same-day if created before 4:45 pm ET**; next day if after |
| Outgoing International Wire | **1-3 business days, up to 5 business days**; non-SWIFT 1-3 days (conversion alone can take up to 2 working days); SWIFT "wait 4 to 5 business days" |
| Outgoing Printed Check | **Up to 8 business days** to arrive at the recipient address via USPS; settlement after deposit depends on the recipient bank |
| Internal transfer, same business, checking → checking | **Within 1 hour** |
| Internal transfer, **different businesses** both at Rho, checking → checking | **1 business day** (settlement-times page) / **2-3 hours** (internal-transfer page) |
| Checking → Savings | **2 business days** (settlement-times page) / **same business day if before 1pm ET** (savings pages) |
| Checking → Treasury, T-Bills | 2 business days if before 5 pm ET; 3 business days if after 5 pm ET / weekend / market holiday |
| Checking → Treasury, mutual funds | 2 business days if before 4 pm ET; 3 business days if after 4 pm ET / weekend / market holiday |
| Vendor-initiated ACH pull from a Rho account | **Next day** (subject to external bank policy). Rho adds: "Please employ discretion before allowing this service by your vendors." |
| Card repayment (from Rho Checking or linked external account) | **Up to 4 business days to settle** |

Blanket caveat Rho repeats: "**payments over $1mm could take an extra day to settle**," and "Rho does not have visibility or control over external banks' settlement times/policies."

Factors Rho lists as affecting outgoing international wire timing: payment method, currency type, banking hours/holidays, and compliance/security checks. "We can't speed up SWIFT payments."

---

## 6. Transfer and payment limits (the complete published set)

| Rail | Limit | Notes |
|---|---|---|
| **Outgoing domestic wires** | **$90 million per day** | "Larger wires can be accommodated, as long as they are communicated to us in advance" |
| **Outgoing international wires** | **$2.5mm per day** | |
| **Incoming international wires** | up to **$10 million per day** | |
| **Incoming ACH (pull) to and from a Rho account** | **$20 million per day**, **$10 million per transaction** | |
| **Outgoing ACH (push)** | **$20 million per day in aggregate** | "Larger ACH transfers can be accommodated... communicated to us in advance" |
| **Linked external account transfers (in and out)** | **$5 million per transaction** | larger by arrangement |
| **Remote check deposits** | **No limit**, but deposits **over $15,000.00 in one business day** may get additional screening and settlement delays | |
| **Savings transfers in** | **No limit** | |
| **Savings transfers out** | **6 per month** | Mirrors the ADM MSA: "Withdrawals are limited to six (6) per month" |
| **ADM sweep withdrawal special handling** | requests **> $3,000,000** are "special handling," settled on a mutually acceptable Settlement Day regardless of cut-off | ADM MSA §4 |
| **Card payments on Rho Invoices** | **$10,000 per day across all invoices** | Option disappears from invoices once hit; bank transfer / international wire still available |
| **INR payments to businesses in India** | **1.5 million INR per invoice daily** | Trade transfers exceeding 1.5M INR are an unsupported purpose |
| **PKR transfers** | up to **35,000,000 PKR per transfer** | |
| **PKR Asaan accounts** | transfers rejected if recipient's Asaan account has a **500,000 PKR** limit | |
| **Check attachment (printed check enclosure)** | 1 PDF per check, up to **6 pages**, **15 MB max**, PDF only, one-time payments only, **no added cost** | |
| Approval thresholds | Configurable per dollar amount; Rho's own example: 1 approver over **$50**, 2 approvers over **$100** | Settings → Payment Security → Payment Approvals |

Escalation path for all of these: contact your Rho Specialist at **855-7-GETRHO / +1 (855) 743-8746** or clientservice@rho.co "and they will assist you in amending your controls." Rho frames limits as "placed on transactional activities for the protection of our clients and Rho."

ToS reserves an override: "Rho reserves the right to impose limits on Transactions and other elements of the Rho Services **at its sole discretion**... **without prior notice**. **New accounts may be subject to longer hold or review periods.**"

Conspicuously **not stated** anywhere: any per-transaction minimum, any daily count limit on ACH/wires, any limit on the number of checking sub-accounts (Webster page says "unlimited"), and any published limit on outgoing check amounts.

---

## 7. ACH mechanics

### 7.1 Same-day vs standard ACH

Rho never uses the phrase "Same-Day ACH" in the help center; the pricing page does ("Same-Day ACH... $0"). Operationally, the help center describes one ACH product whose speed is conditional:

- **Same-day** if created **before 2 pm ET** *and* **under $1mm**.
- **Next day** if created after 2 pm ET **or** over $1mm.
- "ACH settlement time varies depending on various factors, such as the policy of the receiving bank or transaction amount. Typically, ACH transfers are received within 1 to 3 business days."
- Transfer FAQs give the cleanest formulation: "ACHs sent before 2 p.m. EST will land the same day. ACHs sent after 2 p.m. EST will land within 1-3 business days." (Note "EST" vs "ET" is used interchangeably across pages.)

ACH network framing Rho publishes: batched, Nacha-governed, **US-only** ("thus not available for vendors outside the United States").

### 7.2 ACH debits pulled by third parties (vendor pulls / payroll pulls)

- Default posture: **open**. "There are currently no restrictions on Rho's end, and vendor numbers do not require whitelisting to complete the pull." You share your Rho account + routing number and the counterparty debits.
- Rho's own risk language: "Please use discretion before providing any banking information to your vendors."
- **FedWire Drawdown** is supported as a funding method **for payroll providers only**, set up manually by emailing clientservice@rho.co with the provider name and reason. Use cases Rho lists: same-day/time-sensitive payroll funding, providers without ACH debit support, provider-automated pulls, guaranteed same-day settlement.

### 7.3 ACH Debit Authorizations (BETA) - the debit-block product

This is the single most mechanically detailed control in the corpus.

- Location: **Banking → All Accounts → Authorizations** tab. **Account Owners and Admins only.** Adding/editing/removing an authorization and changing the default rule are **gated behind MFA**.
- Matching key: the **ACH Company ID** (example given: `SHOPIFYPMT`), **not** counterparty name, "because it is the most reliable identifier." Can contain letters and numbers.
- Decision table Rho publishes:

| Incoming ACH debit condition | Rho action |
|---|---|
| Counterparty authorized for this account **and** amount within the limit | **Allow** |
| Counterparty not on your list | **Flag** |
| Counterparty on the list but not authorized for **this** account | **Flag** |
| Amount over the counterparty's limit | **Flag** |

- **Hold window: 8 hours.** Rho holds the flagged debit and notifies Account Owners and Admins. If nobody approves or rejects within 8 hours, the **default action** fires.
- Default action for new accounts: **Automatically approve**. Can be changed to **Automatically reject** (change requires MFA).
- Approving can optionally (a) authorize the counterparty for future debits and (b) set a transaction limit. Leaving the limit off means "the counterparty can pull any amount from the selected accounts."
- Rejecting **returns the debit to the sender**. Rho emails Owners/Admins with counterparty, ACH Company ID, account, amount, date, and reason. "**Rho cannot bring back a debit that was already returned.**"
- Surfaces in three places: home-page notification, All Accounts warning banner with "Go to approvals", and the Approvals page / "Approvals needed" tile.
- Documented sharp edges: one Company ID can be shared by multiple counterparties via a common processor (authorizing one may authorize others); one counterparty may use multiple Company IDs (you must add each); "Rho cannot confirm the ID belongs to that counterparty until a matching debit arrives."
- Availability: **beta**, request access from Client Services.

### 7.4 ACH reversal / recall

- **Cannot be canceled while Pending.**
- "They can generally be **reversed/recalled once they settle, within 2 business days**." Request via clientservice@rho.co.
- Recalls are **free**; a successful recall "could take **up to 4 weeks** to be returned."
- Recalls depend on the recipient bank's cooperation and "may or may not be honored."
- ACH trace number for investigations: "typically a 15-digit number," obtained from the sender's bank, plus exact sender name, amount, date.

---

## 8. Checks

### 8.1 Inbound: Remote Deposit Capture (RDC) only

- **Mobile or web RDC only.** "Rho does not accept check deposits by mail or in person. Checks sent by mail or delivered to our offices or any of our partner bank's offices or branches will not be processed."
- **US checks only**: "we do not support remote deposit checks issued by non-US banks. Our system processes only U.S. checks with **9-digit ABA numbers**."
- Endorsement requirements (exact):
  - **Printed/live checks**: wet signature on the back **and** must state "for mobile deposit only".
  - **Digital-copy checks** must be typed/written/stamped on the back with: `"Pay to the order of Webster Bank, a division of Santander Bank, N.A. For Mobile Deposit Only"`, your company name, **Rho routing number (021913655)**, last 4 digits of your checking account number, and the current date.
- Image requirements: high resolution, horizontally oriented, against a **dark, contrasting** background, all 4 corners visible. Web upload accepts **.jpg or .png**.
- Capture fields: Amount (USD), Sender, Deposit To (defaults to the org's **Rho Primary Checking**).
- Status flow in-app: **queued → processing → settled** (identical on web and mobile).
- Screening threshold: deposits **in excess of $15,000.00 in one business day** may get additional screening and settlement delays.

**Settlement contradiction (four different numbers across four pages):**

| Page | Stated RDC clearing time |
|---|---|
| Payment Settlement Times | "2-3 business days, subject to risk-based monitoring (generally up to 6-7 business days)" |
| How to Deposit a Check | "Checks settle in **3 business days** after they are uploaded, subject to risk-based monitoring (generally up to 6-7 business days)" |
| How To Fund Your Account | "Check deposits take **2-3 business days** to clear, subject to risk-based monitoring (generally up to 6-7 business days)" |
| Transfer Limits | "check deposits take **6-7 business days** to clear" (stated flatly, no "up to") |
| Mobile app check deposit | "2 to 3 business days to clear... generally up to 6-7 business days" |

### 8.2 Outbound: printed checks

- Rho generates the physical check and mails it to the vendor's configured address. **No checkbooks, no printed checks, no cashier's checks** issued to the customer, "for security and fraud prevention purposes." **No third-party check issuance or printing** (explicitly including checks from ADP, Gusto, etc.).
- **No international checks**: "At this time, we are unable to send checks internationally."
- Payroll checks workaround: create employees as Vendors and issue Rho checks.
- **Funds-hold mechanic (important):** "funds are **set aside immediately** after you send the payment in the banking account... **Funds do not leave your checking account until Rho receives notice that the check has been cashed** by the recipient." Rho compares this to a cashier's check: it can't bounce, and the check is "drawn from an account that is **separate from your Rho account**, reducing the exposure of your account details." Caveat: "Rho checks are only accepted at locations that accept **corporate checks**, not cashier's checks."
- **90-calendar-day expiry**: "Any check that has not been cashed in 90 calendar days will be **voided automatically**."
- Undeliverable checks are "returned back to your business address that we have on file."
- Outstanding checks are visible by filtering the all-activity page to status **Pending**.
- Tracking: an estimated delivery timeline is shown at creation; after shipment a **"Track Your Check"** link opens the **USPS** tracking page. Check number appears in the Bill Pay/Banking transaction window, in the vendor notification email, and in the transaction PDF export.
- Attachment: 1 PDF, ≤6 pages, ≤15 MB, printed and mailed in the same envelope, one-time payments only, no additional cost.
- Cancellation: "Printed checks can be canceled up until a recipient deposits the check and the funds are cleared by the recipient bank." Post-deposit reversal can be attempted but is not guaranteed. **Caveat**: "past the 30-minute cancellation window, the recipient may still receive the voided physical check in the mail."

---

## 9. Wires

### 9.1 Domestic wires

- Cut-off **4:45 p.m. ET** for same-day arrival; after that, "the wire should arrive within 24 hours of being sent."
- "With wire payments, funds are immediately available within 24 hours of arriving in the vendor's bank account."
- **Cannot be canceled once in "Pending" status.** "Domestic wires typically cannot be reversed or recalled."
- Failed/returned domestic wire: **~$20-$45** deducted from the Rho account (as of 08/02/2026).
- **PO Box prohibited**: BSA requires a physical beneficiary address. Workarounds Rho suggests: a different physical address, ACH, or check.
- Trace evidence required from the sender for an incoming-wire investigation: **IMAD and OMAD** federal reference numbers, plus sender name, amount, date.
- New wire payment methods for a vendor can now be added **inside the payment flow** without leaving the transfer.

### 9.2 International wires

- Two distinct products: **international USD wire** (SWIFT, no Rho fee) and **foreign-currency transfer** (1% FX).
- **1% FX rate** for foreign currency conversion and transmission. **[Rho claim]** it is "a market-leading 1% FX rate."
- Fee direction is a toggle: **"Cover all recipient delivery fees"** ON = the business absorbs recipient/correspondent/intermediary + SWIFT charges for a **flat $15**; OFF = those fees are deducted from the wire amount so the recipient bears them. Fee totals shown are **estimates only**.
- **International wire recall fee: $30** (pricing footnote).
- Required data for a foreign vendor: currency + payment option, and possibly **IBAN** and **SWIFT/BIC**.
- **Local rails, not SWIFT**: "Certain currencies including **IDR, PHP, INR, and MYR** are processed via local payments rails, not the SWIFT network. This means that once the funds leave Rho, we have **limited visibility** on the payment and cannot provide tracking information." (Note: IDR, PHP and MYR do not appear on Rho's own supported-currency list - see §10.)
- Transfer-detail fields: **Transfer reference** (e.g. invoice number), **Payment Reason**, **Memo** (recipient-visible), attachment (recipient does **not** receive it).
- **2FA is mandatory on confirm**: "Rho sends a confirmation code using the two-factor authentication method specified in your Account Settings"; alternates are text message, phone call, or email.
- Beneficiary name must match exactly; business vendors must be added **as a business, not an individual**; "Once a wire is sent, the beneficiary name can't be changed."
- FX rate on scheduled payments is **not locked**: "if a payment is scheduled in advance, the currency conversion rate may change from the time it is initiated to the time the payment is sent out."
- Cancellation: "can be attempted... most effective if the request comes within the same business day the funds are initiated. The more time passes, the less likely the cancellation becomes."
- Trace evidence required: **MT103 data or SWIFT confirmation**.
- HSBC Hong Kong quirk (Rho publishes a whole page on it): use zip `000000`, SWIFT `HSBCHKHHXXX`, and strip any leading letters such as "HK" from the beneficiary account number.

### 9.3 Compliance review on international payments

- **Every** international payment is screened (sanctions/OFAC + AML). "Screening happens **per payment**," so a corridor used many times can still be pulled.
- Common triggers Rho lists: first payment to a new country/currency corridor/beneficiary; business-address verification; an expired document on file; corridor-specific checks.
- Typical asks: proof of current operating address, an invoice/contract supporting purpose, confirmation of beneficiary details.
- Duration: "**Most reviews clear within a few business days**, but some take longer - we can't promise a specific timeline."
- Rho's stated ceiling on help: "What we can't do is skip or override a compliance requirement."
- Outcome set: released, returned, or (rarely) declined.

---

## 10. Currencies and countries

### 10.1 Supported currencies (22 rows as published)

AUD, CAD, BGN, CHF, CZK, DKK, EGP, EUR, **GBP (SWIFT payments currently unsupported)**, GEL, HUF, INR, JPY, NOK, PLN, RON, **RSD** (row labelled "Serbia"), SEK, USD, COP, ILS, **PKR (payments to businesses currently unsupported)**.

**Gap to flag:** the international-wire page names **IDR, PHP, INR, MYR** as local-rail currencies, but **IDR, PHP and MYR are absent from the supported-currency table**. The restricted-countries page separately names supported exception currencies **BDT, BRL, MAD, TZS, UAH** that are also absent from the currency table. So the currency list is not a complete or consistent enumeration.

Coverage claim: **[Rho claim]** "transactions worldwide in **over 200 countries and territories**."

### 10.2 Fully restricted countries (all payments in and out unsupported; owners also ineligible)

CU Cuba, IR Iran, KP North Korea, RU Russian Federation, SS South Sudan, SD Sudan, SY Syria, VE Venezuela.

### 10.3 International-banking-payment restricted (44 entries as listed)

AF Afghanistan, BI Burundi, BY Belarus, BZ Belize, BQ Bonaire, AS American Samoa, BV Bouvet Island, CF Central African Republic, CW Curaçao, TD Chad, Crimea, ER Eritrea, IQ Iraq, LY Libya, CG Congo (Republic), CD Congo (DRC), DJ Djibouti, Donetsk and Luhansk People's Republic, TF French Southern Territories, GU Guam, GN Guinea, **PK Pakistan**, NG Nigeria, GQ Equatorial Guinea, MG Madagascar, SZ Swaziland, SO Somalia, BL Saint Barthelemy, MF Saint Martin (French Part), TM Turkmenistan, PS Palestine, **JO Jordan**, IO British Indian Ocean Territory, VE Venezuela, TG Togo, TK Tokelau, SY Syria, GS South Georgia and the South Sandwich Islands, YT Mayotte, MM Myanmar, KP North Korea, SX Sint Maarten, CM Cameroon, YE Yemen, ZW Zimbabwe.

### 10.4 Exceptions (restricted country, but one currency is allowed)

| Code | Country | Currency | Condition |
|---|---|---|---|
| BD | Bangladesh | BDT | payments to businesses **not** supported |
| BR | Brazil | BRL | payments to businesses **not** supported |
| CO | Colombia | COP | payments to businesses **not** supported |
| EH | Western Sahara | MAD | individuals **and** businesses supported |
| TZ | Tanzania | TZS | payments to businesses **not** supported |
| QA | Qatar | EUR or GBP | **USD unsupported** |
| PK | Pakistan | PKR | payments to businesses **not** supported |
| UA | Ukraine | UAH | payments to businesses **not** supported |

### 10.5 Card-transaction restricted countries (separate, longer list)

AF, BI, BY, CF, TD, CG, CD, Donetsk/Luhansk, MM, IQ, ER, AL Albania, AO Angola, BA Bosnia and Herzegovina, ET Ethiopia, HT Haiti, LA Laos, LB Lebanon, LY, SO, YE, ML Mali, Crimea, MR Mauritania, ME Montenegro, NI Nicaragua, NE Niger, NG, GN, GW Guinea-Bissau, GQ, UA, MK North Macedonia, EG Egypt, XK Kosovo, PS, PK, ZW. (Note EG is card-restricted while EGP is a supported transfer currency.)

### 10.6 Industry restrictions for international payments (sender side)

Rho account holders in these industries **may not send international payments**: weapons/military-grade security, pawnbrokers, political organizations, precious metals and stones, adult entertainment, drug paraphernalia, CBD and related products, carbon credits, cryptocurrencies, gambling, Ponzi/pyramid schemes, and firms servicing illegal goods/services (counterfeit goods/trademark infringement, human trafficking, child labor, prostitution). Payments **to** recipients in these industries "may be rejected or subject to additional compliance screenings."

### 10.7 Corridor-specific rules

**India (INR)** - purpose code is mandatory. Allowed: *Travel expenses* (travel agents, hotels, airlines), *Property purchase* (B2C only), *Pay for services* (export of services incl. software), *Pay for goods* (export of goods). Unsupported purposes: payments to charities, trade transfers exceeding 1.5M INR, foreign direct investments, pay to employees. Limit: **1.5 million INR per invoice daily** to businesses in India.

**Pakistan (PKR)** - personal accounts only; **cannot send PKR to business accounts in Pakistan**. Max **35,000,000 PKR per transfer**. Avoid **Meezan Bank Express Accounts** and **Allied Bank Express Accounts** (no Interbank Funds Transfer credits / inward local transfers; transfers are "instantly rejected or held up with the recipient bank until funds are reclaimed"). Rejected if the recipient's **Asaan account has a 500,000 PKR limit**. Sending from a business account is allowed; receiving into a business account is not.

---

## 11. Transfers between accounts

### 11.1 Internal transfers (within one entity)

- Path: Banking → **Move Funds → Transfer**. Must **not** have a specific account selected on the left rail.
- Covers Checking → Checking (sub-accounts), Checking ↔ Savings, Checking ↔ Treasury.
- **Cross-entity internal transfers are not offered**: "We do not offer the option to transfer funds from one company's Rho account to another company's account at Rho, even if both companies are owned by the same user."
- Workaround Rho documents: create the other company as a **Vendor** under Company A, add a **Domestic Wire** payment type using Company B's wire instructions, and send a domestic wire.
- Recurring frequencies: One Time Only (default), Every day, Every week, Every month, Every year. **Recurring is not available for transfers to and from the Savings account.**
- Sending to your own external bank account requires adding it **as a Vendor** with a payment method, even if it is already a Linked Account. "A linked external bank account is used to fund your Rho account and does **not** automatically become an outbound payment recipient."

### 11.2 Linked external accounts

- Providers: **Plaid**, **Mastercard Data Connect**, **Stripe Financial Connections**. Location: Settings → Business → **External Bank Accounts** → Link Account.
- Two link purposes at connect time: **for transfers** or **for credit verification**. **"Rho does not support maintaining two separate connections from the same institution for different use cases"** - only one connection per institution can be active at a time.
- **Pull eligibility rule**: "To pull funds into Rho from a linked external account, the external account must be a **business account** with an **account name that exactly matches** the name on your Rho account. **Personal accounts are not eligible** for linked-account pulls. To fund your Rho account from a personal account, send an inbound wire or ACH credit instead."
- Linked-account transfers are processed as **ACH**.
- Some external banks require debit-block whitelisting: "If your external account requests specific numbers to whitelist when initiating a pull, please contact our Client Services for the exact codes required."
- Micro-deposits: an alternative linking method that must be **enabled by Rho support on request**. Flow: instant or manual connection; manual asks for account/routing number, account name, account type; authorize; **$0.00 deposit** arrives containing a short verification code; **Plaid sends next steps by SMS**. Verification takes **1-2 business days**.
- Documented external-link errors: Incorrect Credentials (incl. the SVB Go vs SVB Online Banking case and "third-party application password" settings), Incorrect Institution (business vs personal sites), Temporary Connection Issue, Authentication/Permission Issue (security-question mismatch, inactive MFA device, institution not sending the OTP, special security configuration, account not fully set up, revoked data-sharing consent, insufficient user permissions).
- **PayPal linking** (Rho documents it explicitly): in PayPal, Pay & Get Paid → Banks & Cards → Link a New Bank → type random letters to surface "Don't see your bank here?" → enter Rho routing + account number. Entity names must match exactly. **Micro-deposits from PayPal appear in the Rho account within 2-3 business days.**
- Third-party connectivity also supported via **Stripe Financial Connections** ("Rho is supported within Stripe Financial Connections, so no workarounds are required").

### 11.3 Auto-transfer rules (Checking ↔ Treasury and Checking ↔ Checking)

- Location: **All Accounts → Auto-transfer rules → Add rule**.
- Two rule families: **Recurring transfers** (fixed amount; Daily / Weekly / Monthly / Custom dates) and **Maintain balance rules** (Minimum balance, Maximum balance, **$0 balance** = sweep the full available balance on each execution date).
- Evaluated at **8:00 a.m. ET**. Treasury rules do **not** run on weekends or market holidays; a scheduled run on such a day runs on the **previous** applicable business day.
- **The date you pick is the settlement date, not the initiation date.** For Treasury → Checking, "Rho initiates the transfer **3 business days before settlement** and adjusts earlier for weekends and market holidays."
- Treasury → Checking minimum-balance rules use **preset cadences** only: Weekly (choose one weekday), **Twice monthly (fixed 11th and 25th)**, or Monthly (choose one date). Custom schedules exist only for Checking ↔ Checking.
- **Rule limits**: max **5 active auto-transfer rules per organization**; **one rule per source/destination account pair**; each account can be the **source of only one rule**; circular flows are blocked (e.g. Operating→Payroll minimum plus Payroll→Operating maximum). **Only one Checking account can be funded by Treasury.**
- Source and destination cannot be changed after creation (delete and recreate); amount and schedule are editable.
- Migration of the legacy Treasury sweep: old rule = "Every day at 8:00 AM ET, if your Checking balance falls below $250,000, transfer at least $25,000 from Treasury." New rule = same $250,000 minimum, but Rho initiates a Treasury sale in advance so funds settle **every Thursday** (weekly schedule with Thursday settlement).
- Behaviour change: auto-transfer rules "now transfer **only the amount needed to restore your account to its minimum balance**" (the old "top-up amount" is gone).
- Failure mode: insufficient Treasury funds → "The transfer won't be completed, and you'll receive a notification."
- Rho's own recommendation, stated twice: **keep about 3 months of operating cash in Rho Checking.**

---

## 12. Holds, cancellation, reversal and disputes

### 12.1 The universal 30-minute window

"You have a **30-minute window to cancel the transfer before it is released**." Cancel via the transfer item → **Cancel Transaction** in Transaction Details. This applies to **all payments** before release.

### 12.2 Per-rail cancellation matrix (Rho's own table, restated)

| Rail | While pending | After settlement |
|---|---|---|
| All payments | 30 minutes after initiation, before release | - |
| **ACH** | **Cannot cancel** while Pending | Recall **generally possible within 2 business days** after settlement |
| **Domestic wire** | **Cannot cancel** once Pending | "typically cannot be reversed" or recalled |
| **International wire** | Cancellation **can be attempted**; most effective same business day | Recall can be attempted, not guaranteed |
| **Check** | Cancelable until the recipient deposits and the recipient bank clears it; voided check may still arrive in the mail | Post-deposit reversal can be attempted, not guaranteed |
| **Treasury deposit** | Cancelable while **pending, scheduled, or under review**; eligibility indicated by a `(...)` menu on the Activity row | Not cancelable |
| **Any "settled" status** | - | **"can no longer be canceled"** |

Recall economics: **free**, but "if successful, could take **up to 4 weeks** to be returned." Everything depends "on the cooperation of the recipient bank and may or may not be honored."

### 12.3 Holds imposed by Rho

- **Check payments**: funds are set aside immediately at send, but only actually leave the account when Rho is notified the check was cashed (§8.2).
- **ACH debit beta**: flagged debits are **held 8 hours** pending approval.
- **New accounts**: ToS - "New accounts may be subject to longer hold or review periods."
- **Compliance holds**: ToS - "we or our Sponsor Bank may **block, freeze, suspend, or place a hold on an account pending an investigation**"; "We may put your payment, deposit, or your payment method on hold for review. If you do not cooperate with our review process, your deposit or payment [may be affected]."
- **Card authorization holds**: "We may hold, freeze, or temporarily suspend your ability to use your Card when the Card is used for a transaction where the final amount... is unknown at the time of authorization" (restaurants, hotels, rental cars).
- **Check-deposit screening**: >$15,000 in one business day.
- **International payment review**: per-payment, indefinite duration.
- **ACAT out of Treasury**: "once an ACAT transfer is initiated, you will be **unable to add or withdraw funds for up to 90 days**." Holdings keep earning during the freeze.

### 12.4 Failure causes Rho enumerates (seven)

1. Wrong recipient bank details (the most common cause).
2. Recipient bank rejection/return (domestic wire return fee ~$20-$45, as of 08/02/2026).
3. Missed scheduled release (same-day scheduling, missing approval before 4am ET, weekend Bill Pay date).
4. Insufficient available funds.
5. International compliance review.
6. Uncashed (90-day void) or undeliverable check.
7. Unsupported destination (PO Box; restricted country/currency).

### 12.5 Transaction statuses

UI statuses in Transaction Details: **Awaiting Approval, Cancelled Transaction, Pending Transaction, Queued Transaction, Settled Transaction**, with a status history showing each status and its date. Transaction tables use single letters: **A** Awaiting Approval, **C** Canceled, **P** Pending, **Q** Queued, **R** Rejected, **S** Settled. Note **R (Rejected)** appears in the table legend but **not** in the Transaction Details list.

API statuses (`api/transactions_listtransactions.md`) are a smaller set: **`pending`, `settled`, `failed`, `awaiting_approval`** - no `queued`, `canceled`, or `rejected`. `posted_at` is "Null while status is pending," but the docs warn: "`v1` does not guarantee that a failed transaction has an empty `posted_at`... Nor does `v1` guarantee a transition order." An `awaiting_approval` transaction is "held pending action on your side - a payment waiting on an approver, or a debit waiting on your authorization - and **no funds have moved** while it sits in that state."

### 12.6 Transaction type codes

UI codes: **ACH-US** (domestic ACH), **CHECK** (Rho-generated physical check), **EXTERNAL** (external, non-RDC transaction to your Rho account), **INTERNAL** (Rho-to-Rho), **RDC** (remote deposit capture), **WIRE-DOM**, **WIRE-INT** (international wire (SWIFT) and foreign exchange). `EXTERNAL` appears in the Transaction Details list but **not** in the transaction-table list.

API `transaction_type` enum (33 values, the most granular money-movement taxonomy Rho publishes):
`card_credit, card_debit, card_refund, credit_repayment, credit_repayment_refund, credit_cashback, ach_credit, ach_debit, ach_return, wire_in, wire_out, wire_fee, international_wire_in, international_wire_out, check_deposit, check_payment, internal_transfer, savings_deposit, savings_withdrawal, savings_interest, treasury_deposit, treasury_withdrawal, treasury_fee, treasury_interest, treasury_maturity, treasury_sale, treasury_market_value_adjustment, rewards_accrual, rewards_cashback_redemption, adjustment_credit, adjustment_debit, international_wire_fee, international_wire_fee_refund`

Notable API gaps: there is **no `ach_reversal` / `wire_recall` / `check_void` type** (returns surface only as `ach_return`), and the docs state explicitly "**`v1` exposes no dispute indicator**" - "A refund or credit is not by itself a dispute." Transactions sharing a `money_movement_id` belong to the same movement (confirmed in sandbox: a credit repayment appears as two rows, `-1750` on the checking account and `+1750` on the credit account, both with `money_movement_id: 40000000-0000-4000-8000-000000000002`).

---

## 13. FDIC / SIPC coverage mechanics, including the sweep

### 13.1 Three different protection regimes, one dashboard

| Account | Protection | Mechanism | Limit |
|---|---|---|---|
| **Rho Checking** | FDIC | Direct deposit at Webster Bank, a division of Santander Bank, N.A., Member FDIC | **$250,000 per entity**, aggregated **across all Rho checking accounts** |
| **Rho Savings** | FDIC **and NCUA** | **Administered sweep** run by American Deposit Management (ADM) across **400+ FDIC- and NCUA-insured institutions** (as of **August 2026**) | **Up to $75,000,000 per entity** |
| **Rho Treasury** | **SIPC, not FDIC** | Securities held in the company's name at Apex Clearing Corp (and Interactive Brokers) | **$500,000 per customer, including $250,000 for cash** |

Rho is explicit that the $75M does not travel: "**No** - coverage depends on where your funds sit in Rho, and **only Savings uses the sweep**."

SIPC scope, stated repeatedly: "SIPC protects against **custodial failure, not market loss**" / "against the loss of assets in the event of a brokerage failure - it does not protect against the decline in value of your securities."

FDIC scope, stated in the ToS: deposits "are eligible for deposit insurance by the FDIC through Webster up to the current limit of **$250,000 per institution, per account type**." And on every relevant page: "FDIC deposit insurance coverage is available only to protect you against the failure of an FDIC-insured bank that holds your deposits... **It does not protect you against the failure of Rho or other third party.**"

### 13.2 How the sweep actually works (mechanics)

1. You fund Rho Savings **from Rho Checking only** ($25,000 minimum to earn the rate).
2. **ADM**, acting as your **agent**, allocates funds "across the network institutions in increments **below the $250,000 per-bank FDIC limit**."
3. Legal structure: an **administered money market deposit account** - the **American Money Market Account (AMMA)** in the ADM Master Services Agreement. Funds sit in **omnibus deposit accounts** at the Program Institutions. (The MSA also offers an **American Term Deposit Account** = CD Accounts; nothing in the Rho-facing pages says CDs are offered to Rho customers.)
4. Program Institution deposit accounts "may be classified as money market accounts, non-interest bearing accounts, interest bearing accounts, savings accounts or NOW accounts."
5. Ownership evidence is a **book entry** on records maintained by ADM and/or the Custodians. You get a monthly statement showing deposits, withdrawals, per-institution balances, net earnings and a "delivered rate."
6. You see **one account and one balance** in the Rho dashboard.

Rho's worked example: "$5 million at one bank: $250,000 is FDIC-insured. The remaining $4,750,000 is not. $5 million in Rho Savings: the program spreads it across **20+ institutions**, each holding less than $250,000."

### 13.3 The caveats Rho does disclose (these matter)

- **Intraday/overnight concentration exception** (ADM MSA §3): "if funds **in excess of $250,000 are deposited into or withdrawn from the Program in a single day**, for a limited amount of time (**intraday or overnight**), **the entire amount of the withdrawal or deposit may be held at one Program Institution**." In that event ADM "may" secure the excess via collateral or a surety bond.
- **Extended deposit insurance is waived by default in the Rho flow**: the MSA gives the client a choice between (1) extended coverage secured by pledged collateral or a surety bond, and (2) waiver. "**By signing Exhibit A, Client expressly waives extended deposit insurance.**" The Rho help-center overview never mentions this waiver.
- **Commercially reasonable efforts, not a guarantee**: "ADM will use **commercially reasonable efforts** to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution." Marketing pages echo: "Coverage reflects the partner-bank network's capacity as of August 2026 and is **not a contractual guarantee**," and "reflecting program capacity on a **commercially reasonable efforts basis**, not a guarantee."
- **Qualification of institutions is point-in-time**: a Program Institution must be "well capitalized" **at the time of a first deposit**. "The fact that a Program Institution is well capitalized does **not** mean that it will not be subject to failure at a later point in time."
- **Recovery is not instant**: on a Program Institution failure, "it may take a period of time for ADM to substantiate its claim to and withdraw any funds previously on deposit at the failed financial institution."
- **ADM can reshuffle unilaterally**: "ADM may include additional Program Institutions, delete Program Institutions, and determine the order of Program Institutions, **at its discretion**." If an institution rejects deposits or exits, you pre-authorize ADM to move your funds; if no alternative exists, ADM transfers your balance to "your account at your primary financial institution."
- **Aggregation risk**: your $250,000 per Program Institution is "subject to the aggregation of any other funds you have on deposit at the same Program Institution in the same legal capacity" - i.e. if you separately bank at a network institution, coverage overlaps.
- **Bank-list opacity**: "The current list of network institutions is **available from Rho support on request**." It is **not published**. This is the single most conspicuous omission in the FDIC story.
- **Eligibility representation**: non-public-unit clients must represent they are an "**accredited investor**" as defined by applicable securities laws. Program is open only to **U.S. Persons**.
- Program Institution accounts have **no check writing, no ATM, no debit card**.
- Funds must enter through the Custodian: "cannot be placed directly with ADM or any of the Program Institutions."

### 13.4 Sweep deposit/withdrawal operational schedule (ADM MSA, stricter than the Rho UI copy)

| Event | Rule |
|---|---|
| Deposits | "Deposits received by the Custodian on any standard banking day **before 12:00 P.M. Central Time** will be deposited with the Program Institutions **on the next business day**." Payments by check/money order/cashier's check are held based on availability of funds. |
| Withdrawal cadence | Processed on **Tuesdays and Thursdays** ("Processing Days"), settled **Wednesdays and Fridays** ("Settlement Days"). |
| ≤ $3,000,000, received by 12:00 PM CT on a Processing Day | Settles on the **next Settlement Day** you specified |
| ≤ $3,000,000, received after 12:00 PM CT | Settles on the **Settlement Day after that** |
| > $3,000,000 | **Special handling**; mutually acceptable Settlement Day regardless of cut-off |
| Federal Reserve holidays | No processing or settlement; requests roll to the next Processing Day, settlements to the next Settlement Day |
| Count limit | **Six (6) withdrawals per month** |
| CD Accounts | Time deposits; early withdrawal penalties/fees are the client's responsibility |

**Contradiction:** the customer-facing Savings page says "Savings → Checking: typically settles the **next business day**, if created before 1pm ET," while the governing ADM agreement says withdrawals only process **Tuesdays and Thursdays** for **Wednesday and Friday** settlement. A Friday 12:00pm ET request under the MSA settles the following Wednesday at the earliest, which is four business days, not one.

### 13.5 Competitor coverage comparisons **[Rho claim]**

From `product__business-savings-account.txt` (competitive data "collected from Mercury, Brex, and Relay websites as of 2026-09-06"): Rho up to **$75M** vs **Mercury $5M**, **Brex $6M**, **Relay $3M**; Mercury Treasury and Brex Treasury are described as **SIPC-only**, not FDIC deposit accounts. From `product__business-banking.txt` (data "as of 09/06/2026"): Mercury "Up to $5M via partner-bank sweep networks," Bluevine "Up to $3M via Coastal Community Bank's program-bank network," Chase "Member FDIC; no dollar figure published." Treat all of these as Rho-sourced.

---

## 14. Savings account mechanics

| Parameter | Value | Source |
|---|---|---|
| APY | **Up to 1.00%**, variable, set monthly, as of **August 2026** | product__business-savings-account |
| Minimum to earn interest | **$25,000 average monthly balance** ("not a single day's snapshot") | Savings pages |
| Effective rate below minimum | **0%** - "below $25,000, the balance earns 0% with Rho" | product page FAQ |
| Interest accrual | **Daily**, paid **monthly** | |
| Interest posting date | **5th business day of each month**; if the 5th falls on a weekend/holiday, the next business day | |
| Interest basis | Average monthly balance, computed from **daily ending balances** | |
| Day-count convention | **30/365** | Understanding Rho Savings Accounts |
| Monthly statements | Available by **6pm ET on the 5th business day** of each month (Settings → Documents) | |
| Transfers in | From **Rho Checking only**; **no limit** | |
| Transfers out | **6 per month** maximum | |
| Checking → Savings | Same business day if before **1pm ET** | |
| Savings → Checking | Next business day if before **1pm ET** | |
| Recurring transfers | **Not available** for transfers to and from Savings | How to Create an Internal Transfer |
| Opening flow | Savings tab → **Request Access** → Rho Client Service sends a **DocuSign** agreement → signed agreement goes to the partner (ADM) for review → account opens; additional due-diligence info may be requested | |
| Monthly fee | **$0** | |
| Dashboard fields | Available balance, Current balance, Pending out, APY | |

**Contradiction on Savings settlement (three values):** "same business day"/"next business day" (Savings pages, gated on 1pm ET) vs "**2 business days**" (Payment Settlement Times, both directions) vs "**1-3 business days**" and "**1-2 business days**" in two places on the same internal-transfer page. The savings product page states "**Within 2 business days** typical time to move money back to checking."

---

## 15. Treasury mechanics (money movement, not investment thesis)

### 15.1 Assets and their liquidity

| Asset | Type | Purchase mechanics | Liquidity | Suitable horizon |
|---|---|---|---|---|
| **IJTXX** (JPMorgan U.S. Treasury Plus Money Market Fund) | Government MMF, **$1.00 stable NAV** | **Cash sweep**: cash sits in the account during the day, Apex sweeps it into the fund **each business day**; **no minimum purchase or redemption** | **Same day** (only Treasury asset with same-day access) | Any time |
| **T-Bills (13-week / 90-day)** | Direct US government securities | Purchased **exclusively 13-week, in $1,000 increments**; bought at a discount, redeemed at face value | Next business day allocation (5:00 PM ET cutoff) | ≥3 months |
| **MULSX** (Morgan Stanley Ultra-Short Income Portfolio) | **Not** a money market fund; variable NAV | Bought at daily NAV | 1-2 business days (4:00 PM ET cutoff) | 4-6 months |
| **VFSUX / VFSTX** (Vanguard Short-Term Investment-Grade, Admiral / Investor) | Short-term corporate bond fund, meaningful NAV variability | Bought at daily NAV; **VFSUX only for new allocations** | 1-2 business days (4:00 PM ET cutoff) | ≥12 months |

T-Bill worked example Rho gives: purchased at **$989.96**, matures at **$1,000.00**, return **$10.04**. T-Bill interest is federally taxable, exempt from state and local income tax. If the proportional T-Bill allocation for a deposit **falls below $1,000**, that portion is held as cash and invested at the next deposit/rebalance, or swept into IJTXX if enrolled.

### 15.2 Allocation and rebalancing

- Allocations are **percentage-based, in 5% increments, must total 100%**. **Vanguard capped at 50%** of the portfolio (VFSTX + VFSUX combined); existing >50% allocations can remain but must be brought to ≤50% before submitting any change, unless Rho approved a higher limit.
- Preset strategies:

| Strategy | Horizon | Allocation |
|---|---|---|
| Maximum liquidity | Same day | 100% IJTXX |
| Capital preservation | 3 months | 50% IJTXX / 50% T-Bills |
| Balanced income | 4-12 months | 40% IJTXX / 60% MULSX |
| Optimized yield | 12+ months | 15% IJTXX / 60% MULSX / 25% VFSUX |
| Custom | your choice | 5% increments |

(One page lists "Three preset strategies"; the table on that same page lists four plus Custom. Minor internal inconsistency.)

- **Funding waterfall**: "New funds top up IJTXX first." If IJTXX is below its target %, incoming funds go to IJTXX until the target is restored; the remainder is spread proportionally across T-Bills, MULSX and Vanguard. Applies to deposits, T-Bill maturity proceeds, fund dividends, and cash interest.
- Investments take **1 to 2 business days to settle**; **IJTXX settles same business day**.
- **Rebalancing triggers**: (a) every new money event invests to target; (b) editing the target triggers an immediate rebalance; (c) **monthly on the 6th**, Rho reviews and rebalances automatically if any holding has **drifted more than 5%** from target.
- An allocation-change rebalance "typically takes **2 to 4 business days** to complete. **You cannot make changes while a rebalance is in progress.** Your funds remain invested during this time."
- Not enrolled in the IJTXX sweep: cash earns "a small amount of interest" and is reinvested across targets **on the 6th of every month**; **cash interest is paid monthly, mid-month**.

### 15.3 Withdrawal algorithm (explicitly documented, unusual detail)

- "Available same day" = **IJTXX balance + uninvested cash**. Submit by **3:00 PM ET** on a business day to use funds the same day.
- **If the withdrawal ≤ available balance**: the **full amount** is pulled from IJTXX and cash. Before 3:00 PM ET → Rho **wires** the funds to Rho Checking the same day. After 3:00 PM ET → next business day.
- **If the withdrawal > available balance**: the **full amount comes from the other assets instead**. Rho sells T-Bills, MULSX and Vanguard **proportionally to current allocation**; **IJTXX is left untouched** so the same-day buffer survives.
- "**We do not split a withdrawal across IJTXX and your other assets, and you cannot select which assets are sold.** Shares are sold **first-in, first-out (FIFO)**."
- Rho's worked example: portfolio = 20% IJTXX ($20,000) + 80% MULSX ($80,000). Withdraw $15,000 before 3pm ET → from IJTXX, same day. Withdraw $30,000 → exceeds the $20,000 IJTXX balance, so the **full $30,000** sells from MULSX, IJTXX stays at $20,000, funds arrive in **1 to 2 business days**.
- VFSTX is sold **before** VFSUX (older lots, FIFO). VFSTX disappears from the portfolio when its balance reaches $0.00; historical VFSTX entries remain in Activity.

### 15.4 Treasury settlement timelines (Rho's table)

| Asset | Cutoff | Allocation after sale |
|---|---|---|
| IJTXX | 3:00 PM ET | Same business day |
| T-Bills | 5:00 PM ET | Next business day |
| MULSX | 4:00 PM ET | 1 to 2 business days |
| VFSUX / VFSTX | 4:00 PM ET | 1 to 2 business days |

Cutoffs apply on business days only; weekend and market-holiday requests process the next business day.

**Contradiction stack on Treasury → Checking timing (four different framings):**
1. Managing Treasury table: T-Bills **next business day**, funds **1-2 business days**.
2. Payment Settlement Times: T-Bills **2 business days** before 5pm / **3** after; mutual funds **2 business days** before 4pm / **3** after.
3. Auto-transfer rules page: "Treasury → Checking transfers can take **up to 3 business days** to settle"; Rho "initiates the transfer **3 business days before settlement**."
4. `product__treasury.txt` headline: "**2 to 3 business days** to move funds back to checking," with a footnote that itself splits: "cash settles in **2 business days**, then reaches checking within **2 more** business days" vs "Proceeds from Treasury sell orders reach your checking **within 2 business days** (as of 08/03/2026)" and the yield-methodology page's "**within two (2) business days of trade execution** (as of 08/03/2026)."

### 15.5 Fees, custody, tax, closing

- Fee tiers (annualized, billed monthly, **calculated daily**):

| Total AUM | Annual fee |
|---|---|
| > $20M | **0.15%** (15 bps) |
| $10M - $20M | **0.25%** (25 bps) |
| $5M - $10M | **0.35%** (35 bps) |
| $2M - $5M | **0.45%** (45 bps) |
| Under $2M | **0.60%** (60 bps) |

- **AUM basis is broader than Treasury**: "AUM includes the combined balance of your **Rho Checking and Treasury** accounts."
- Fee is deducted from portfolio cash; "if insufficient cash is available, Rho will **automatically sell a small amount of holdings** to cover it."
- Dashboard net yield formula Rho publishes: `Σ (target allocation % × current asset yield) - management fees`.
- **Yields as of 09/11/2026, net of fee, by tier** (product__treasury):

| Tier | Fee | Vanguard bond fund (30-day SEC, net) | Morgan Stanley MMF (7-day SEC, net) | 13-week T-Bills (7-day avg, net) |
|---|---|---|---|---|
| $20M+ | 0.15% | **4.66%** | 3.70% | 3.66% |
| $10-20M | 0.25% | 4.56% | 3.60% | 3.56% |
| $5-10M | 0.35% | 4.46% | 3.50% | 3.46% |
| $2-5M | 0.45% | 4.36% | 3.40% | 3.36% |
| $50K-$2M | 0.60% | 4.21% | 3.25% | 3.21% |

  The headline "**up to 4.66%**" is therefore the **$20M+ tier in a 100% Vanguard bond fund** - an allocation the product itself **caps at 50%**. The footnote admits the assumption: "assumes total Rho deposits of $20M+, a **100% allocation to the Vanguard Short-Term Investment-Grade Fund (VFSTX)**." Two internal conflicts: the cap makes 100% impossible under stated rules, and the footnote names VFSTX while the product says only VFSUX takes new allocations.
- **Custody platform migration**: **VFSUX and the IJTXX MMF sweep are only available on "Apex Ascend."** Accounts opened **on or after July 23, 2026** are on Ascend; accounts opened before will migrate "in the coming months." You must **accept the sweep terms** before IJTXX becomes active.
- Assets are **not pooled**: "Securities are held directly in your business's name."
- Movement authority: "Funds can only be transferred to and from your **Rho Checking account** by individuals you have authorized in your Rho account settings, or through auto-transfer rules."
- Statements: generated by **Apex**, posted **within 7 business days of the start of each month**, at Settings → Account Statements → Treasury Account. Monthly statements are produced only for months with **deposits, withdrawals, or trades**; dividends, interest and market-value changes do **not** qualify. Otherwise a combined **quarterly** statement.
- 1099 thresholds Apex applies: **$10** for dividends and interest, **$20** for cash in lieu, **$600** for miscellaneous income. **C corporations are generally exempt** from 1099 broker reporting.
- Apex email domains Rho pre-authenticates: trade confirmations and statements `notifications@investordelivery.com`, tax documents `rho@tax-docs.com`, prospectuses `prospectus_mbox@investordelivery.com`, proxy notices `id@proxyvote.com`.
- **Closing**: contact Rho; requires liquidating all holdings, "typically takes **2-3 business days**"; sold at current market prices and may lose value.
- **ACAT out**: initiated by the receiving brokerage; **no deposits or withdrawals for up to 90 days**; "Rho's ability to support issues related to the transfer may be limited."
- Read-only accountant access to Treasury is supported (statements, trade confirmations, tax documents).

---

## 16. Payroll, card repayment, and other automated debits out of checking

### 16.1 Payroll

- "**Rho does not run payroll natively.**" You keep Gusto, Rippling, Justworks, Deel, Every, or any ACH-based tool, and change one setting: the funding account. "This is a bank account swap, not a platform migration."
- Two connection options: **Plaid** (instant when supported) or **manual routing + account number**, which most providers verify with **two micro-deposits taking 2-3 business days**.
- Rho's timing advice: "start the verification process at least **3-4 business days** before your next payroll run."
- Provider navigation paths Rho publishes: **Gusto** = Settings → Plan & Billing → Payroll Bank Accounts → Add account; **Rippling** = Payroll → Settings → Payroll Bank Accounts → Add additional payroll bank accounts. Justworks/Deel/Every = generic path.
- Failure mode: "A failed payroll run is usually caused by **insufficient funds**."
- The provider debits Rho directly. Alternative for same-day certainty: **FedWire Drawdown** (§7.2).

### 16.2 Card repayment (money leaving checking automatically)

- **Daily Terms** (the default for every account): "Payments are automatically debited from your Rho checking account **just after midnight EST** for that day's activity. Daily auto-repayment amounts are for the total amount of **settled charges from the prior day**." Rho's example: Monday's charge period runs 12:01 am EST Monday to midnight Monday; Monday's repayment follows; Tuesday's period begins 12:01 am EST Tuesday. ToS: "settled so that it has a **zero balance at the end of the same day** if such day is a business day, otherwise the next business day. **There is no grace period.**"
- **Daily credit limit is dynamic**: "determined based on a combination of your available checking balance as well as risk factors that vary by client... this limit is **not a static limit over time**."
- **Monthly Terms**: **30-day billing cycle with a 1-day repayment period**; automatic full-balance repayment at cycle end from Rho Checking or an external account. Qualification: **minimum cash balance of $25,000** (help center). The site FAQ states it differently: "**$25,000 held at Rho, or $75,000 combined across Rho and linked external accounts**, subject to underwriting approval" - a materially different second path that the help center omits.
- **Automatic Card Payments** (interim ACH pulls): threshold default **95%** (settable 1-99%) of the credit limit triggers a payment; payment amount default **5%** of the total credit limit (settable 1-99%). Rho's example: $100,000 limit, balance passes $95,000 → automatic **$5,000** ACH pull. Source account = Rho checking **or** a linked third-party account. Configurable by **Account Owners and Administrators only**.
- Repayment timing: "card repayments abide by **ACH cut-off times**. Repayments initiated prior to **2:00 pm ET** should begin processing the same day. Any repayments initiated after 2:00 pm ET would be subject to next-day processing. **Card repayments can take up to 4 business days to settle.**"
- Important hold nuance: "Automatic payments are **credited to your Rho Card account when received**... The Rho Card payment isn't complete until after the payment settles **and the ACH reversal window has closed**."
- Escalation: ToS requires you to remit any amount Rho cannot auto-debit "**within one (1) Business Day**."
- Late fee: **3% of the delinquent balance per month, up to 6 months**.

### 16.3 Cashback / rewards money movement

- **Monthly Terms**: cashback deposited into the Rewards Account "typically **6 business days** following full repayment of the statement balance."
- **Daily Terms**: cashback deposited "typically on the **6th business day of the month**, for card spend during the preceding month."
- Redemption: transfer any amount or the full balance from Rewards to the Primary Operating Account; "**Redeemed rewards are deposited instantly.**"
- Rewards earned only on **settled** transactions. Late payments forfeit rewards for that statement period. Refunds/returns/disputes/fraud/reversals cause rewards to be **deducted from accrued rewards in following periods**.
- Cashback cap: up to **2% with Rho Platinum** on up to **$1,000,000 in eligible card spend per calendar year**; **1.25% standard** (terms apply).

---

## 17. Approvals, 2FA and controls on outbound money

- **Payment Approvals**: Settings → Payment Security → Payment Approvals. Set an **approval threshold** in dollars; any transaction initiated over it requires approval. Choose how many users must approve and who the approvers are. Multiple tiers by amount are supported (Rho's example: 1 approver over $50, 2 over $100). Approvers receive emails per transaction before funds release.
- **2FA policies** (Settings → Security → Two-Factor Authentication → 2FA Policies): require 2FA **for all transactions**, **for issuing cards**, and **for physical card activation**. Changing the 2FA Policy itself now requires 2FA.
- International wires **always** require 2FA at confirm, independent of policy. Verification methods: text message, phone call, email (and authenticator app for card/wallet flows).
- ACH debit authorization changes are **MFA-gated** (§7.3).
- Bill Pay bulk payments: **Admins and Account Owners can execute**; **Bookkeepers can import and edit drafts but cannot execute by default**.
- Approvals surface in: Banking tab "Approvals Needed" tile → View All → Approvals page (approve or deny per transaction).
- Transactions can also be reviewed and approved in the **mobile app** and via the **Rho Slack app**.

---

## 18. Bulk payments and Bill Pay rails

- **Bulk Payments** is CSV-driven: download the Rho CSV template, one payment per line, import. "Each line-item in the CSV will create one payment, **there is no merging** of multiple payment line items into one payment."
- Supported rails in bulk: **Checks, ACH, Wires (domestic accounts only), single-use virtual Rho cards shared via email**. **International wires cannot be included in a bulk CSV.**
- Single-use card payments: the card is created when the payment is created; details are emailed on the Created/Due date; card nickname format `<Vendor> AP Card: <Invoice Number>`.
- CSV errors Rho names: **Vendor Missing** (vendor name in yellow, no match in Rho) and **Destination Error** (no payment details for that vendor on the chosen method).
- Creation/Due date must be **today or in the future**.
- **Bill Pay supports international wires in USD only.** Non-USD bills must be paid from the Banking tab and then **Mark as Paid** in Bill Pay, which moves the bill to **Paid Externally** and archives it.
- Bill Pay statuses: **Draft → Missing Payment Details → Ready for Payment → Awaiting Approval → Payment Scheduled → Paid** (or **Paid Externally**, or **Failed Payment** with a Retry action).
- Scheduled bill payments release at **~4:00 a.m. ET** on the payment date; must be a **future business day**; same-day or weekend dates will not release and appear overdue. Cancel a scheduled bill payment via **Revoke** (Bill Pay → Bills → filter Payment Scheduled → three dots → Revoke).

---

## 19. Inbound money: instructions, tracing, statements

- Receiving instructions live in two places: Banking → select account → **Account Details → View Receiving Instructions**, and the newer consolidated **Settings → Payment Instructions**. Four documents can be emailed or downloaded: **Domestic Wire Instructions**, **International Wire Instructions**, **ACH Transfer Instructions**, **Void Check Template**.
- A **Bank Letter** (proof of account) is at Settings → Documents → Bank Letter; can be downloaded or emailed directly to a third party ("The letter will be delivered to them immediately").
- Tracing incoming funds requires, from the sender: ACH → **15-digit ACH TRACE number**; domestic wire → **IMAD and OMAD**; international wire → **MT103 data or SWIFT confirmation**. In all cases plus sender name, amount, date.
- Rho's own disclaimer, repeated: "Rho is **unlikely to be able to track incoming payments**. We recommend contacting the sending bank directly."
- Statement availability by account type:

| Account | Statement availability |
|---|---|
| **Checking** | **Second calendar day** of every month |
| **Savings** | By the end of the **fifth business day** of each month (can be the 6th or 7th depending on weekends/holidays); by **6pm ET** on that day |
| **Treasury** | Posted within **7 business days** of the start of each month, by Apex; monthly only if there were deposits/withdrawals/trades, otherwise combined quarterly |
| **Card, Daily Terms** | **5th of every month** |
| **Card, Monthly Terms** | **One business day** following the statement repayment date |

  A same-page note contradicts the checking row: "You can download a statement for the previous month starting on the **5th** of each month. Documents for the current month become available on the **5th of the following month**," and the proof-of-account page says "**Statements are generated on the 5th of every month**." So checking statements are variously the 2nd or the 5th.
- Running balance: CSV export from the Banking tab includes a **Balance** column, but only if you (a) select a single checking account and (b) filter to **SETTLED** status. On All Accounts the balance column is blank.
- Balance vocabulary Rho uses consistently: **Available balance** (usable today, excludes pending transfers), **Current balance** (includes pending transfers), **Pending out** (outgoing funds in flight). All Accounts "Balance" includes the Treasury **portfolio balance** but not pending transfers.

---

## 20. Account closing (final money movement)

Checklist Rho publishes: pay off the card balance first (closure cannot process until settled); cancel scheduled and recurring payments (Banking → Scheduled Transactions); move the Savings balance out (next business day if before 1pm ET, 6 transfers/month cap, as of **08/02/2026**); liquidate Treasury (**2-3 business days**, sold at market and may be worth less); download statements and CSVs before access ends; save vendor W-9s.

On closure: all Rho cards (physical and virtual) are canceled; "Any remaining balance is returned **by wire or check**." Timing depends on pending transactions clearing. Closure must be requested by the **Account Owner**.

---

## 21. Contradictions and inconsistencies found (consolidated)

| # | Topic | Page A | Page B |
|---|---|---|---|
| 1 | Check deposit clearing | "2-3 business days... generally up to 6-7" (Settlement Times, Fund Your Account, Mobile) | "**3 business days**" (How to Deposit a Check); "**6-7 business days**" flatly (Transfer Limits) |
| 2 | Savings ↔ Checking timing | "same business day before 1pm ET" / "next business day" (Savings pages) | "**2 business days**" both directions (Payment Settlement Times); "**1-3 business days**" and "**1-2 business days**" on the same Internal Transfer page |
| 3 | Savings withdrawal cadence | "next business day" (help center) | ADM MSA: processed **Tue/Thu only**, settles **Wed/Fri** |
| 4 | Cross-entity internal transfers | "**We do not offer** the option to transfer funds from one company's Rho account to another company's account at Rho" (Internal Transfer page) | Same page then gives a settlement time for "business-to-business internal transfers... 2-3 hours"; Settlement Times page lists "Internal Transfers Between Different Businesses Holding Accounts at Rho (Checking to Checking): **1 business day**" |
| 5 | Linked-account settlement | "**up to 5 business days**" (Settlement Times, Fund Your Account, Transfer Limits) | "**3-5 business days**" (Transferring Money From a Linked Account) |
| 6 | Domestic wire recall/return fee | "Domestic wire recall fee **$0**" (pricing.txt) | "a fee of around **$20-$45**... for any domestic wire payments that fail and are returned" (Fees for Recalls & Failed Wires; restated as of 08/02/2026) |
| 7 | Incoming domestic wire cutoff | "within the same day if sent **before 3 PM ET** in most cases" (Fund Your Account) | 4:45 pm ET is the number everywhere else (that one is outgoing, but the two are never distinguished on the same page) |
| 8 | Treasury → Checking timing | "1 to 2 business days" (Managing Treasury) | "2 business days / 3 after cutoff" (Settlement Times); "up to 3 business days" (Auto-transfer rules); "2 to 3 business days" (product page) |
| 9 | Treasury headline yield basis | "up to 4.66%" | assumes **100% VFSTX**, but Vanguard is **capped at 50%** and VFSTX is closed to new allocations (VFSUX only) |
| 10 | Treasury presets | "**Three** preset strategies are available" (About Rho Treasury prose) | The table on that same page lists **four** presets plus Custom |
| 11 | Treasury minimum | "**Maintain at least $50,000 in total deposits**" (eligibility) | "$50,000 minimum **to open**" / "$50,000 minimum investment" (product page, yield methodology) |
| 12 | Monthly Terms qualification | "minimum cash balance of **$25,000**" (help center) | "$25,000 held at Rho, **or $75,000 combined** across Rho and linked external accounts" (site FAQ) |
| 13 | Checking statement date | "**second calendar day** of every month" | "starting on the **5th**" (same page note); "generated on the **5th** of every month" (proof-of-account page) |
| 14 | Supported currencies vs local rails | Currency table omits **IDR, PHP, MYR** | Intl wire page says IDR, PHP, INR, MYR run on local rails (implying they are sendable) |
| 15 | Transaction status vocabularies | UI: Awaiting Approval / Cancelled / Pending / Queued / Settled (+ Rejected in tables only) | API: pending / settled / failed / awaiting_approval only |
| 16 | Transaction type vocabularies | UI: ACH-US, CHECK, EXTERNAL, INTERNAL, RDC, WIRE-DOM, WIRE-INT (EXTERNAL missing from the table legend) | API: 33 granular `transaction_type` values |
| 17 | Micro-deposit verification | Rho's own micro-deposit link flow: "**1-2 business days**" | PayPal micro-deposits into Rho: "**2-3 business days**"; payroll provider micro-deposits: "**2-3 business days**" |
| 18 | Capital lender | "Business-purpose loans made by **Lead Bank**" | Same corpus: "Fees... set when **Slope** underwrites your line"; "**Slope** is a financial technology company, not a bank" |

---

## 22. What is conspicuously NOT stated

1. **The sweep bank list.** 400+ institutions is asserted; the list is "available from Rho support on request" and never published. No named Program Institution appears anywhere in the corpus.
2. **The extended-deposit-insurance waiver** in the ADM agreement is never surfaced on any customer-facing Savings page, despite being the mechanism that decides whether above-limit intraday balances are secured.
3. **No wire-specific routing number.** Rho warns customers that receiving banks often have separate ACH and wire routing numbers, but publishes only one Rho routing number (021913655) and never says whether it accepts both.
4. **No stated incoming-check, incoming-ACH, or incoming-wire fee.** Pricing covers outbound only; incoming is implied free but never affirmatively priced.
5. **No overdraft, NSF, returned-item, or stop-payment fee schedule.** The only failure fee published is the $20-$45 returned domestic wire and the $30 international recall.
6. **No published dispute process for bank transfers** (only cards have a dispute article). The API docs say flatly: "`v1` exposes no dispute indicator."
7. **No SLA or maximum duration on international compliance reviews**, and no published appeal path.
8. **No RTP / FedNow / instant-payments support** is mentioned anywhere. Rho's fastest rail is same-day ACH or a same-day domestic wire.
9. **No multi-currency accounts.** Rho holds USD only; every account balance in the API sandbox is `"currency":"USD"`. Foreign currency exists only as a transmission step through Wise US Inc.
10. **No ATM access, cash deposit, or branch deposit** anywhere. Rho's own comparison table concedes online-first providers have "limited or unavailable cash deposits."
11. **No published cut-off for outgoing international wires** (the corpus gives cutoffs for domestic wire, ACH, Savings, Treasury, and scheduled release, but never one for FX/SWIFT origination).
12. **No holds schedule / funds-availability policy** in Regulation CC terms (first $X available next day, etc.). Availability is described narratively per rail only.
13. **No statement of whether checking sub-accounts share the same account number** or each get a distinct one. Sandbox shows distinct `account_number_last_4` per checking account, but no help page says so.
14. **No published limit on the Savings account balance** even though the coverage claim tops out at $75M.
15. **No FBO/omnibus disclosure for checking.** The ToS says deposits are "held by Webster" and FDIC-eligible "per institution, per account type," but never states whether checking is a direct DDA in the customer's name or an FBO structure. (By contrast, the savings omnibus structure is spelled out in the ADM agreement.)

---

## 23. Quick-reference: every number in one place

**Cut-offs (ET unless noted):** 12:00am (daily card repayment debit) · ~4:00am (scheduled payment release and approval deadline) · 8:00am (auto-transfer rule evaluation) · 1:00pm (Savings in/out) · 2:00pm (outgoing ACH; card repayment; incoming deposit posting) · 3:00pm (Treasury IJTXX withdrawal; incoming domestic wire per Fund-Your-Account) · 4:00pm (Treasury mutual funds) · 4:45pm (outgoing domestic wire) · 5:00pm (Treasury T-Bills) · 6:00pm (Savings statement posting) · 12:00pm **Central** (ADM sweep deposit and withdrawal).

**Limits:** $90M/day outgoing domestic wire · $2.5M/day outgoing international wire · $10M/day incoming international wire · $20M/day ACH in and $20M/day ACH out · $10M per ACH transaction · $5M per linked-account transaction · $15,000/business-day check-deposit screening trigger · $1mm same-day ACH ceiling · $3M ADM special-handling threshold · 6 Savings withdrawals/month · 5 auto-transfer rules per org · $10,000/day invoice card payments · 1.5M INR per invoice/day · 35M PKR per transfer · 500K PKR Asaan rejection · $1,000,000/calendar year cashback-eligible spend · 6 pages / 15MB check attachment · 5% allocation increments · 50% Vanguard cap · 5% drift rebalance trigger.

**Windows:** 30 minutes (universal cancel) · 8 hours (flagged ACH debit hold) · 2 business days (ACH recall) · 4 weeks (successful recall return) · 90 calendar days (uncashed check auto-void) · 90 days (ACAT freeze) · 120 days (Rho Switch lookback and data retention) · 180 days (Capital repayment per draw) · 6 months (max late-fee accrual).

**Money:** $250,000 FDIC checking · $75,000,000 FDIC savings · $500,000 SIPC ($250,000 cash) Treasury · $25,000 savings minimum average balance · $25,000 Monthly Terms minimum · $50,000 Treasury minimum · $1,000 T-Bill increment · $15 SWIFT fee · $30 international recall · $20-$45 returned domestic wire · 1% FX · 2.9% + $0.30 card acquiring · 0.15%-0.60% Treasury fee · 3%/month late fee · $400 incorporation deposit refunded at $10,000 average balance for 60 days · $100 deposit promo.

**Contact for exceptions:** clientservice@rho.co · +1 (855) 743-8746 (1-855-7-GETRHO) · live chat in-product · 24/7, every channel, every day, no paid support tier **[Rho claim]**.
