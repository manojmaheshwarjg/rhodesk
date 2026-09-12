# Rho: Trust, Regulatory Posture, and Risk

Research dossier section. Compiled 2026-09-11 from a local corpus of rho.co marketing pages, help-center articles, policy pages, docs.rho.co, and two blog posts fetched live (`blog/rho-and-webster-bank`, `blog/security-by-design`).

Labeling convention used throughout:
- **[Rho claim]** = asserted only by Rho, no independent corroboration in corpus. Applied aggressively to anything about a competitor.
- **[ToS]** / **[PP]** = binding contract language from Terms of Service v7.0.0 (last updated 2026-08-27) or Privacy Policy (dated "June 29, 2025" in the contents block, "Last updated August 27, 2026" in the body).
- **[NOT STATED]** = a CFO-relevant fact Rho does not publish anywhere in the corpus.

---

## 1. Headline

Rho is a software company that sits in front of other people's regulated balance sheets. It says so plainly and repeatedly. The customer's deposit risk is with Webster Bank (a division of Santander Bank, N.A.) and, for savings, with 400-plus unnamed sweep-network institutions; the customer's operational and legal risk is with Rho, and **Rho contractually caps its own total liability to the customer at $500.00**. The single most under-advertised fact in the corpus: a company with 10 or more Rho cards is contractually **liable for all unauthorized use of all cards**, which sits awkwardly next to the security page's "Mastercard Zero Liability protects against unauthorized card fraud."

---

## 2. Legal entity structure

| Entity | Role | Regulatory status as stated | Source |
|---|---|---|---|
| **Under Technologies, Inc.**, dba **Rho Technologies** | The contracting party for everything. Trademark owner. "Program manager" for the Sponsor Bank. | Financial technology company. Not a bank, not an FDIC-insured depository institution. | ToS preamble; footer copyright "© 2019 - 2026 Under Technologies, Inc. DBA Rho Technologies" |
| **RBB Treasury LLC** dba **Rho Treasury** (also appears as dba **Rho Prime Treasury**) | Investment management and advisory for Rho Treasury | SEC-registered investment adviser; "a subsidiary of Rho" | ToS Addendum D; universal footer disclaimer; `customers__superfiliate.txt` uses "Rho Prime Treasury" |
| **Webster Bank, a division of Santander Bank, N.A.** | "Sponsor Bank." Holds checking deposits; is the card **Issuer** and "the creditor responsible for funding your Charges" | FDIC-insured national bank, Member FDIC | ToS preamble; Addendum A §1.1 |
| **American Deposit Management, LLC** + wholly owned subsidiary **ADM Consulting, LLC** (collectively "ADM") | Administers the savings sweep as the customer's **agent**; selects Custodians and Program Institutions | Not described as a bank. Deposits sit at Program Institutions. | ADM Master Services Agreement, published as a help-center article |
| **Apex Clearing Corporation** | Treasury custodian for accounts opened **after July 2024** | Registered SEC / FINRA broker-dealer, member SIPC | `product__treasury.txt`; footer |
| **Interactive Brokers LLC** | Treasury custodian for accounts opened **before July 2024** | Registered broker-dealer, member FINRA/SIPC | `product__treasury.txt`; footer |
| **Wise US Inc.** | International and foreign-currency payments | Named only as service provider; customer must separately accept the Wise US Inc. Customer Agreement | ToS preamble; universal footer |
| **Slope** | Underwrites Rho Capital lines | "Slope is a financial technology company, not a bank." | `product__capital.txt` line 171 |
| **Lead Bank** | Makes the Rho Capital loans | "Business-purpose loans made by Lead Bank and subject to credit approval." | `product__capital.txt`; `help-center/.../about-rho-capital` |
| **Mastercard** | Card network; cards issued "pursuant to a license from Mastercard" | Network | Footer |

Registered address: 100 Crosby Street, New York, NY 10012. Governing law: New York (ToS §26.8); card agreements: "federal law, and, to the extent not preempted, the substantive laws of the State of New York."

Note the entity count a CFO actually faces: to use checking + savings + treasury + capital + international payments, the company is in privity with or dependent on **Under Technologies, RBB Treasury, Webster/Santander, ADM (two LLCs), Apex or Interactive Brokers, 400+ unnamed program institutions, Wise US, Slope, and Lead Bank**. Rho's marketing presents this as one account.

---

## 3. "Rho is a fintech company, not a bank" (verbatim disclaimers)

The full universal footer disclaimer, which appears on essentially every marketing page (`about.txt`, `security.txt`, `faq.txt`, product pages):

> "Rho is a fintech company, not a bank or an FDIC-insured depository institution. Checking account and card services provided by Webster Bank, a division of Santander Bank, N.A., member FDIC. Savings account services provided by American Deposit Management Co. and its partner banks. International and foreign currency payments services are provided by Wise US Inc. FDIC deposit insurance coverage is available only to protect you against the failure of an FDIC-insured bank that holds your deposits and subject to FDIC limitations and requirements. **It does not protect you against the failure of Rho or other third party.** Products and services offered through the Rho platform are subject to approval."

Card issuance:

> "The Rho Corporate Cards are issued by Webster Bank, a division of Santander Bank, N.A., member FDIC pursuant to a license from Mastercard, subject to approval."

Treasury (full, verbatim, from the same universal footer):

> "Investment management and advisory services provided by RBB Treasury LLC dba Rho Treasury, an SEC-registered investment adviser and subsidiary of Rho. RBB Treasury LLC facilitates investments in securities: investments are not deposits and are not FDIC-insured. Investments are not bank guaranteed, and may lose value. Investment products involve risk, including the possible loss of the principal invested, and past performance does not indicate future results. Registration with the SEC does not imply a certain level of skill or training. Treasury and custodial services provided through Apex Clearing Corp. ("Apex") and Interactive Brokers LLC ("Interactive"), registered broker dealers and members FINRA/SIPC. Interactive rates may vary from Apex rate shown above."

And:

> "Rho Treasury is not insured by the FDIC. Rho Treasury are not deposits or other obligations of Webster Bank, a division of Santander Bank, N.A., or American Deposit Management Co.'s partner banks, and are not guaranteed by Webster Bank, a division of Santander Bank, N.A., or American Deposit Management Co.'s partner banks. Rho Treasury products are subject to investment risks, including possible loss of the principal invested."

ToS preamble (binding version):

> "Rho is a financial technology company and not a bank. Rho provides you with access to products and services provided by third parties, including FDIC-insured banks and SIPC-insured brokerage accounts that offer Rho-branded banking and brokerage products and services. At this time, the checking account and credit card Rho Services are available from Webster Bank, a division of Santander Bank, N.A., an FDIC-insured national bank ("Webster", also referred to as our "Sponsor Bank"). Deposits are held by Webster and are eligible for deposit insurance by the FDIC through Webster up to the current limit of $250,000 per institution, per account type."

ToS §24, all caps in original:

> "RHO IS FINANCIAL TECHNOLOGY COMPANY AND NOT A BANK, FINANCIAL INSTITUTION OR FINANCIAL ADVISORY SERVICE. NEITHER RHO NOR THE RHO SERVICES ARE INTENDED TO PROVIDE LEGAL, FINANCIAL, INVESTMENT OR TAX ADVICE."

Glossary, ToS §29, closing the loop on scope:

> "For the avoidance of doubt, Rho is a financial technology company and not a bank. Banking products and services are provided by our Sponsor Bank and are not Rho Services."

Help-center footer (Webster article) adds:

> "Rho is not a bank. Rho partners with FDIC-insured banks to offer banking products and services. By using Rho services, you agree to and are bound by the Rho Terms of Service."

**Rho's disclosure discipline on the fintech/bank distinction is genuinely above market.** The trust page volunteers the "What happens to my money if Rho shuts down?" question and answers it correctly: "Your deposits are held at Webster Bank, a division of Santander Bank, N.A. and the program banks in the sweep network, not on Rho's balance sheet."

**Conspicuous exception.** ToS **Addendum C (Rho Savings Account Agreement)** opens: "the terms 'we,' 'our,' 'us,' **'Bank'** and 'Rho' mean Under Technologies, Inc., dba Rho Technologies." Rho defines itself as "Bank" inside its own savings agreement. Sloppy drafting, but it is a defined-term contradiction with every other disclaimer.

---

## 4. The Webster / Santander relationship and its history

Timeline reconstructed from `blog/rho-and-webster-bank` (published 2024-08-01, "Last Updated August 20, 2026") and `blog/security-by-design` (published 2024-12-29, "Last Updated August 20, 2026"):

| Date | Event | Stated figure |
|---|---|---|
| 2018 | Rho launches. "partnering with smaller, tech-native banks became the standard operating procedure for brands like Rho, Chime, Square, PayPal" | - |
| June 2020 | Rho begins search for an institutional bank partner; selects **Sterling National Bank**, "a New York-based, nationally chartered bank" | "approximately $30bn in assets" |
| "Several months after partnering with them" (Sterling/Webster merger closed Jan-Feb 2022 in reality) | Sterling merges with Webster Bank | "approximately $77bn of combined assets at the time" |
| 2021 | Rho launches the **card product** with Webster as issuing sponsor | - |
| 2024 ("earlier this year" in a 2024-08-01 post) | Rho launches **checking and banking products** on Webster | - |
| 2026-03-31 | Webster standalone bank-level assets | **$85.5B** (FDIC call report) |
| **2026-08-20** | Webster becomes **a division of Santander Bank, N.A.**, part of Santander's U.S. banking organization | **$327B**-asset U.S. banking organization "(per Santander's completion announcement)" |

The naming convention Rho now uses everywhere, including retroactively inside 2024 blog posts, is the full string "Webster Bank, a division of Santander Bank, N.A." The find-and-replace was applied mechanically: the 2024 Webster blog post now reads "Sterling merged with Webster Bank, a division of Santander Bank, N.A., with approximately $77bn of combined assets at the time," which is anachronistic on its face.

**The `$327B` number is a pro forma group figure, not Webster's.** Rho discloses this, but only in a small-print footnote on `/trust`:

> "Rho's figure is Santander's pro forma U.S. organization total at the Webster close (per Santander, 8/20/2026); Webster's standalone bank-level figure was $85.5B (FDIC call report, 3/31/2026)."

Every headline and nav-bar use of "$327B" therefore compares a parent-group pro forma total against competitors' standalone bank call-report assets. The apples-to-apples comparison is **$85.5B Webster vs. $8.7B Cross River**, roughly 10x, not the "roughly 37x" Rho headlines.

**Stale text still live.** `blog/security-by-design`, last updated 2026-08-20, still says Webster is "a nationally chartered institution with over $76 billion in assets" and "a publicly traded company with over 200 branch and ATM locations across the United States." After 2026-08-20 Webster is a division of Santander Bank, N.A. and is not itself publicly traded. Three different Webster asset figures ($76B, $77B, $85.5B) plus the $327B group figure appear across pages that were all "updated" the same day.

### Rho's strategic argument on the partnership model [Rho claim]

From `blog/security-by-design`:
- Rho chose **direct integration** with Webster over **Banking-as-a-Service (BaaS) middleware**: "While BaaS middleware offers a faster path to market, recent headlines have highlighted its risks. Direct integration requires greater upfront investment and ongoing management, but it ultimately provides more control and stability."
- "The con is that the direct integration model comes with higher standards, every product and feature you ship must meet your partner bank's rigorous compliance and risk requirements."
- From the Webster blog: "we began building out our **proprietary core** needed to integrate with Webster Bank's systems."

This is the most substantive structural claim Rho makes: no middleware layer (no Synapse/Evolve-style intermediary) between Rho and the bank. Nothing in the corpus independently verifies it, but it is consistent with the ledger-direct framing of the Rho API ("direct connection to the Rho ledger (no aggregator)").

### Competitor deposit-bank table [Rho claim, from `/trust`]

Rho's own table, "Figures verified as of 08/02/2026. Sources: FDIC BankFind call reports (data as of 3/31/2026) and each provider's public disclosures."

| Platform | Deposits held at | Bank assets as Rho states them |
|---|---|---|
| **Rho** | Webster Bank, a division of Santander Bank, N.A. | $327B (per Santander at close, 8/20/2026) [group pro forma, not bank-level] |
| Mercury | Choice Financial Group and Column N.A. | $6.1B / $1.4B |
| Brex (a Capital One company) | Column N.A. | $1.4B |
| Ramp | First Internet Bank of Indiana | $5.7B |
| Bluevine | Coastal Community Bank | $5.7B |

Rho also asserts, unsourced to a specific competitor page: "roughly 37x the next-largest deposit partner bank behind any major US business-banking fintech (Cross River Bank, $8.7B; FDIC, 3/31/2026)." Cross River does not appear in Rho's own table, so the comparison target is not one of the five platforms listed.

Rho footnotes: "Brex was acquired by Capital One (completed April 2026); its deposit partner remains Column N.A. Coverage structures and sweep programs vary by provider, see each provider for current terms." Treat every row as **[Rho claim]**.

---

## 5. FDIC vs SIPC: exact scope, limits, and mechanism

| Product | Protection | Limit | Mechanism | Who fails is covered |
|---|---|---|---|---|
| **Rho Checking** | FDIC | **$250,000** | Direct deposit at Webster Bank, a division of Santander Bank, N.A. | Failure of Webster only |
| **Rho Savings** | FDIC (and NCUA) | **up to $75,000,000** | Sweep administered by ADM across "400+ FDIC- and NCUA-insured institutions"; ADM holds funds in **omnibus deposit accounts** at Program Institutions, ownership evidenced by ADM/Custodian records | Failure of each individual Program Institution, up to $250K each |
| **Rho Treasury** | **SIPC**, not FDIC | **$500,000 per customer, including up to $250,000 for cash** | Securities held in the company's name at Apex Clearing (accounts opened after July 2024) or Interactive Brokers (before that) | Failure of the **broker-dealer custodian only**. Explicitly "not against market loss" |
| **Rho Rewards account** | [NOT STATED] | [NOT STATED] | Cashback accrues into a "Rewards Account" in the Banking tab; redeemed by transfer to the Primary Operating Account | [NOT STATED] |

### The limit qualifier is stated three incompatible ways

| Page | Wording |
|---|---|
| `security.txt` | "insured up to $250K **per depositor, per ownership category**" |
| ToS preamble | "up to the current limit of $250,000 **per institution, per account type**" |
| `faq.txt` (Bill Pay answer) | "FDIC insured up to $250,000 **per entity, not per account**" |
| `product__business-banking.txt` | both "per depositor per ownership category" (line 142) and "per entity" (lines 43, 175) |
| `product__treasury.txt` | savings insurance "**per depositor**" (line 297) |
| `startups.txt` | "$250,000 **per depositor, per insured bank, per ownership category**" |

Only the `startups.txt` and `business-banking.txt` line-142 formulations are the actual FDIC rule. "Per entity" and "per account type" are loose. A CFO running multiple legal entities through Rho needs the real rule, and Rho does not consistently state it.

### Savings sweep mechanics (the precise, load-bearing detail)

From `help-center/banking/how-the-rho-savings-sweep-works` and the ADM Master Services Agreement:

- **Minimum to open: $25,000.** Funding into Savings can **only** come from a Rho Checking account.
- Structure is "an **administered money market deposit account**"; funds sit in deposit accounts at network institutions.
- ADM "will use **commercially reasonable efforts** to ensure that no more than $250,000 of your funds will be deposited in any single Program Institution."
- **Documented insurance gap:** "if funds in excess of $250,000 are deposited into or withdrawn from the Program in a single day, **for a limited amount of time (intraday or overnight), the entire amount of the withdrawal or deposit may be held at one Program Institution**." A $20M inbound wire is, by Rho's own partner's agreement, concentrated at a single bank for up to a day.
- In that event ADM "**may** take steps to secure the amount of your funds by employing the tools available to you by extending deposit insurance." Note "may," not "will."
- **The client waives extended deposit insurance by default.** "By signing Exhibit A, Client expressly waives extended deposit insurance." Waiving it means: "Client funds deposited with a Program Institution in an amount in excess of the applicable limit for FDIC or NCUA insurance coverage, are not guaranteed by the FDIC or NCUA, or through the pledge of identified and agreed upon collateral, or the issuance of a surety bond, or by any government agency and, as a result, in the event of a financial failure of any such Program Institution, Client funds on deposit in a depository account with such Program Institution will be at risk."
- Program Institution selection standard: "**well capitalized** (as such term is defined by applicable FDIC or NCUA regulations) based upon information about such Program Institution published by the FDIC or the NCUA on a **quarterly** basis." ADM then states the obvious limitation itself: "The fact that a Program Institution is well capitalized does not mean that it will not be subject to failure at a later point in time."
- **Recovery is not instant on failure.** "in the event a Program Institution fails, its insured deposits will either be assumed by another insured depository institution, or by the appropriate regulator... **it may take a period of time for ADM to substantiate its claim to and withdraw any funds** previously on deposit at the failed financial institution."
- ADM "may include additional Program Institutions, delete Program Institutions, and determine the order of Program Institutions, **at its discretion**."
- The deposit accounts "constitute a direct obligation of the Program Institution(s) and are **not** directly or indirectly an obligation of ADM or the Custodian."
- **Client must be an "accredited investor."** "All Clients other than public unit depositors, represent and warrant that they are an 'accredited investor' as that term is defined by applicable securities laws and the Securities and Exchange Commission." This is not mentioned anywhere in Rho's savings marketing.
- **ADM takes instructions from Rho as if from the client.** "ADM agrees to honor Client instructions... received from Rho... as if they were delivered to ADM directly by Client. In the event that Instructions received from Rho, on behalf of Client **do not reflect Instructions of Client**, Client agrees that such Instructions, received from Rho, shall be considered Instructions received directly by Client." Rho misinstructing ADM is, contractually, the client's problem, and ADM is not party to the Rho agreement.

### Savings liquidity constraints (buried in the closure article and the ADM agreement)

| Constraint | Value | Source |
|---|---|---|
| Withdrawals from Savings | **6 per month**, hard limit | ADM MSA §4; `how-to-close-your-rho-account` ("as of 08/02/2026"); sweep article |
| Transfers **into** Savings | No limit | sweep article |
| ADM processing days | **Tuesdays and Thursdays** | ADM MSA §4 |
| ADM settlement days | **Wednesdays and Fridays** | ADM MSA §4 |
| Cutoff | **12:00 P.M. Central Time** on a Processing Day | ADM MSA §4 |
| Withdrawals **over $3,000,000** | "special handling... settled at a **mutually acceptable Settlement Day**" regardless of cutoff | ADM MSA §4 |
| Deposit posting | Received by Custodian before 12:00 PM CT posts to Program Institutions **the next business day** | ADM MSA §3 |
| No Fed holidays | ADM cannot process or settle on Federal Reserve Board holidays | ADM MSA §4 |
| No checks / ATM / debit | "The accounts at the Program Institutions do not include check writing privileges, ATM transactions, or debit card transactions." | ADM MSA §4 |
| Interest posting | Accrues daily, paid monthly, posted on the **5th business day** of each month | sweep article |
| Statement delivery | ADM statement no later than the **20th day** of each calendar month | ToS Addendum C |

Rho's marketing describes Savings as offering "next-day liquidity" (`security.txt`). The ADM contract describes a **Tuesday/Thursday processing, Wednesday/Friday settlement, six-per-month, 12:00 CT cutoff** regime with a $3M special-handling threshold. The consumer-facing sweep article says "Savings to Checking typically settles the next business day." These are reconcilable only if Rho is fronting liquidity or the article is describing the happy path; **Rho never explains the reconciliation.**

**Account opening is manual.** "Click Request Access. A member of the Rho Client Service team will prepare and send you a **DocuSign** agreement... Depending on your answers to the **due diligence questions**, our partner may request additional information before your account is opened."

### SIPC scope, stated correctly by Rho

From `how-does-fdic-insurance-coverage-work`:

> "Rho Treasury is different: it holds securities (U.S. Treasury Bills and money market funds), not bank deposits. Treasury assets are protected by SIPC up to $500,000 (including $250,000 for cash) through our custodians, **SIPC protects against custodial failure, not market loss**."

From `/trust` FAQ:

> "Is Rho Treasury FDIC-insured? No. Rho Treasury holds securities (T-Bills and money market funds) and is SIPC-protected through registered broker-dealers. FDIC insurance covers bank deposits, not investments."

Treasury economics for context (`product__treasury.txt`, yields as of 09/11/2026):
- Minimum: **$50,000**.
- Fee tiers, billed monthly on AUM: **0.60%** under $2M; **0.45%** $2-5M; **0.35%** $5-10M; **0.25%** $10-20M; **0.15%** $20M+.
- Instruments: U.S. T-Bills, **MULSX** (Morgan Stanley Ultra-Short Income), **VFSTX** (Vanguard Short-Term Investment-Grade). Allocation in 5% increments; **VFSTX capped at 50%** of total.
- VFSTX is an investment-grade **bond fund** with duration and credit risk, not a cash equivalent. Rho's changelog (2026-04-30) does flag "Each fund carries a different risk and liquidity profile."
- Liquidation to checking: **2 to 3 business days**; "Assets are sold at current market prices and may be worth less than your original investment."
- The headline "up to 4.66%" is the $20M+ tier net of the 0.15% fee. Rho states this explicitly, which is unusually honest for a yield headline.

---

## 6. Rho Capital: a different regulatory stack nobody notices

`product__capital.txt` disclaimer, verbatim:

> "Slope is a financial technology company, not a bank. Business-purpose loans made by Lead Bank and subject to credit approval. Application and consent to obtain personal credit report is required. Subject to minimum revenue and business requirements. Personal Guaranty may be required. Fees vary based on risk assessment and loan term."

And in the body: "Rho is a fintech, not a bank. Financing offered by third parties. Rho Capital is not a broker-dealer. It does not participate in the negotiation or execution of any transactions between customers and third-party financing sources."

**Direct contradiction with Rho's own help center.** `help-center/general-rho-information/about-rho-capital` says: "There are no origination fees and no prepayment penalties. **Applying doesn't involve a hard pull on your personal credit.**" The product page disclaimer says "**Application and consent to obtain personal credit report is required**" and "Personal Guaranty may be required," and line 53 says "Depending on underwriting, approval may also require a **personal guaranty from a business owner**." The help center also names no lender at all beyond "Lead Bank"; it never mentions **Slope**, the party that actually underwrites and prices the line.

This matters because Rho's headline card pitch is "no personal guarantee." That is true of the **cards**. It is not true of **Capital**.

Line sizes: "Lines are available up to $5M+, subject to underwriting" (help center); "credit lines up to $5 million, with larger facilities considered case-by-case (as of 08/02/2026)" (llms.txt). Repayment "terms up to 180 days per draw." Funding "in as little as 24 to 48 hours after approval."

---

## 7. Security certifications and controls

### What Rho actually claims

| Control | Claim | Evidence / source | Gap |
|---|---|---|---|
| **SOC 2 Type 2** | "Rho is SOC 2 Type 2 compliant. Rho is **audited every year** by a third-party using the SOC 2 framework." | `help-center/general-rho-information/soc-2-type-2-compliance` | **Auditor not named. Trust services criteria in scope not named. Report period not stated. Report is behind a link ("clicking on this link") whose gating is not described.** |
| **Trust Center** | Footer link "Rho Trust Center" on every page | Universal footer | **The Trust Center URL does not appear anywhere in the 1042-URL sitemap.** It is off-site (likely a Vanta/Drata/SafeBase-style portal). Contents unverifiable from the corpus. |
| **Encryption** | Rho's own pages: "data encryption, firewalls, and other appropriate technologies" (PP). **No algorithm, no key length, no at-rest/in-transit split.** | Privacy Policy, "Information Security" | AES-256 and TLS are named only in relation to **Plaid**, not Rho: "Plaid keeps your data safe and private with best-in-class encryption protocols like the Advanced Encryption Standard (AES 256) and Transport Layer Security (TLS)" |
| **2FA / MFA** | Mandatory at login: "Rho **requires 2FA every time you log in**." Methods: Google Authenticator (recommended), Authy (recommended), SMS ("the least secure method"). | `set-up-2-factor-authentication`, `how-to-log-in-to-rho` | Phone-number changes require emailing clientservice@rho.co (support-mediated, a social-engineering surface) |
| **Step-up MFA** | Configurable 2FA policies: "For all transactions," "For issuing cards," "for Physical cards activation." Changing the 2FA policy itself **requires 2FA**. | `require-2fa-for-sending-transactions-creating-cards` | |
| **Force MFA on every login** | Admins can "Require two-factor authentication on every login... even on **trusted devices**. This... **overrides your trusted device settings**." Shipped **2026-05-27**. | `set-up-2-factor-authentication`; `changelog.txt` | Implies trusted-device bypass is the default |
| **SSO** | **Google SSO only.** Admins enable it at Settings > Manage Single Sign-On > "Require Google SSO." When enforced, "users within your email domain can log into Rho using their Google accounts, rather than a password." | `managing-google-sso-for-your-organization` | **No SAML. No Okta, Entra/Azure AD, OneLogin, JumpCloud. No SCIM.** Zero hits for SAML, SCIM, Okta across the entire 536-page corpus. |
| **SCIM / automated deprovisioning** | Does not exist. User deletion is manual ("deletions are permanent and irreversible"). Bulk **add** via CSV exists; bulk offboard does not. | `how-to-manage-users-and-roles-in-rho` | Material for any company over ~100 seats |
| **RBAC** | 6 default roles: Account Owner, Administrator, Department Owner, Employee, Bookkeeper, Investor. Custom roles creatable, duplicable, deletable. Permission glossary spans Credit, Cards (own vs team), Banking (own vs team vs Transfers/Accounts), Expense management, Treasury, Vendors, Departments, Bill Pay, Security. | `user-permissions-glossary` | Genuinely granular. Notable specific permissions: "View Full Vendor Routing and Account Number" (masked if off), "Create DACA account transfers," "Accept deposit agreement," "Manage security settings," "Authorize integrations." |
| **Password reset** | Two paths: email clientservice@rho.co, or an Admin/Account Owner resets it from the Users tab. **Reset cannot be completed in the mobile app.** | `how-to-log-in-to-rho` | Support-mediated reset is again a social-engineering surface |
| **1Password integration** | "Save in 1Password" button on card details, Chrome/Brave/Firefox/Safari/Edge | `1password-integration-overview-setup` | Pushes PAN + CVV into a user's personal vault. Convenience, not a control. |
| **Penetration testing** | **[NOT STATED]** | zero hits for "penetration," "pen test" | |
| **Bug bounty / VDP** | **[NOT STATED]** | zero hits | security@rho.co exists but only as a **phishing-forwarding** address |
| **ISO 27001** | **[NOT STATED for Rho.]** Named only for **Codat**: "Codat's Security Compliance program upholds SOC 2 Trust Service Principles and ISO 27001 standards" | `applying-to-rho-faqs` | |
| **PCI DSS** | **[NOT STATED]** for Rho | | Rho displays full PAN/CVV in-app and pushes it to 1Password |
| **GDPR** | **[NOT STATED].** The word never appears in the Privacy Policy or ToS. | | A **DPA** is referenced 7 times in the ToS and governs "Personal Data," but **the DPA is not published anywhere in the sitemap** |
| **Uptime SLA / status page** | **[NOT STATED].** ToS §7 affirmatively disclaims it: "Rho shall not, however, have any liability whatsoever to you in the event of any failure or bugs in the Rho Services, or interruptions of the Rho Services." | | |
| **Data residency** | US-centric but explicitly not guaranteed: PP "International Transfers" says data "may cause your Personal Information to be processed and/or stored **outside of your country of residence**"; ToS §10 says network portions "may be located abroad" | | |

### API and integration security (docs.rho.co, strong and well documented)

| Control | Detail |
|---|---|
| Auth scheme | `Authorization: Bearer`. "No other authentication header (cookie, API key, signed request) is supported." |
| Token prefix | `rhobat_` |
| Who can create | **Account Owners and Admins only** |
| Creation gate | **2FA challenge at the moment of creation** |
| Token display | "shown **only once**... There is no way to recover the secret later" |
| IP allowlist | Optional per token, **up to 100 entries**; off-list source IP gets `403` |
| Expiry | **Required. Maximum one year.** Plus auto-expiry after **45 days of inactivity** |
| Max tokens | **20 active tokens** per business |
| Revocation | "**immediate**... no grace period and no way to un-revoke" |
| Scopes | `accounts:read`, `transactions:read`, `statements:read`. Enforced pre-handler; `403` on mismatch. **Read-only across the board.** |
| Partner OAuth | OAuth 2.0 **Authorization Code + PKCE (S256)** at `https://auth.rho.co`; access token **15 min**; refresh token **30 days rolling**, **single-use and rotating**; grant lifetime **1 year** then re-consent. Only Account Owners and Admins can consent. One active grant per app per business. Discovery at `/.well-known/openid-configuration`. |
| Sandbox | `rhoapi-sandbox.rho.co` accepts **any non-empty bearer token**, "intentionally permissive," fictional data |

**Doc contradiction:** `docs_v1_cards.md` says the card endpoints "require the `cards:read` scope," but the authoritative scope table in `docs_v1_auth.md` lists only `accounts:read`, `transactions:read`, `statements:read`. Invoicing endpoints exist in the API reference with no scope named at all. Also, a token is described as "**long-lived**" in the opening sentence and as capped at one year with 45-day inactivity expiry two paragraphs later.

**No write scopes exist.** The Rho API is read-only (accounts, transactions, cards, statements, invoicing reads). A CFO cannot move money via API, which is simultaneously a control and a limitation.

### Connected Platforms and AI: the newest data-egress surface

ToS §28 (Connected Platforms) is worth quoting because it is the widest disclosure authorization in the agreement:

> "By enabling a Connected Platform, you authorize Rho to disclose your Data, **including Bank Account balances, Transaction detail and output of the AI-Assisted Features**, to that Connected Platform and to make that Data available to the individuals to whom you have granted access to the workspace, channel, conversation or other destination you designate, **whether or not those individuals are Users**."

And: "Rho does not control and is not responsible for the Connected Platform, including its availability, security, access controls, or retention or deletion of Data."

ToS §27 (AI-Assisted Features), verbatim on reliance:

> "Responses generated by the AI-Assisted Features are produced automatically and may be incomplete, inaccurate or out of date. Your Rho Account remains the authoritative record of your balances, Transactions and other Data, and **you agree to verify any response against your Rho Account before relying on it**."

Privacy Policy adds the model-training commitment, which is the right one:

> "Our service providers include providers that host the artificial intelligence models used to power certain features of the Rho Service, and providers that help us monitor the quality of those features. Service providers may use your information only to provide services to us, and **are not permitted to use it for their own purposes, including to train their own models**."

The AI model providers are **not named**. The Gmail connector (changelog 2026-04-30) claims "Rho only scans for receipts, nothing else in your inbox is read or stored."

---

## 8. Fraud controls

| Control | Mechanism | Notes |
|---|---|---|
| **SMS fraud alerts** | Opt-in. Suspicious transaction is **automatically declined**, SMS asks YES/NO. YES lifts the block; **NO cancels the card automatically** and a new card is issued. | Opt-in, not default. Requires a mobile number on file. |
| **In-app suspicious-activity alerts** | Three alert types: "Unrecognized card transaction," "Suspicious login or new user alert," "Unrecognized card transaction attempt." Buttons: "Yes, Unblock the merchant" / "No, Cancel the Card." | "We also proactively monitor your account and send alerts when something looks unusual" |
| **Card controls** | Merchant, category, limit, and time controls per card; limit types daily/weekly/monthly/quarterly/annual, switchable on an existing card without reissue (changelog 2026-05-27) | |
| **ACH debit authorization (positive pay), BETA** | Allowlist by **ACH Company ID** (not name). Unlisted/over-limit/wrong-account debits are **held 8 hours** and notified to Account Owners and Admins. Configurable default if nobody acts. | **Default for new accounts is "Automatically approve."** Adding/editing an authorization or changing the default rule is **gated behind MFA**. Beta, opt-in via Client Services. |
| **ACH allowlist caveats (Rho states these itself)** | "One ACH Company ID can be used by more than one counterparty... If you authorize a counterparty that uses a shared ID, **other counterparties that use the same ID may also be allowed**." And: "Rho cannot confirm the ID belongs to that counterparty until a matching debit arrives." And: "Rho cannot bring back a debit that was already returned." | Honest, and a real limit of the control |
| **Payment approvals** | Settings > Payment Approvals; approval required for team-created transactions | |
| **Bill Pay controls** | `security.txt`: "Rho Bill Pay verifies suppliers, flags anomalies, and restricts payments to approved vendors" | No mechanism detail published; no named vendor-bank-detail-change verification step |
| **Expense review** | `security.txt`: "Transactions that need closer inspection get routed to **human review**" | Unspecified |
| **Invoicing** | "Activate a **virtual account number** to minimize risk from unauthorized debits" (changelog 2026-03-25) | |
| **Phishing guidance** | Forward to **security@rho.co**. "Rho will never contact you unexpectedly to ask for your password, verification code, or banking details." Official domains: `https://www.rho.co` and `https://app.rho.co/login`. | |
| **Mastercard Zero Liability** | Asserted on `security.txt`: "Mastercard Zero Liability protects against unauthorized card fraud." | **Contradicted by the ToS card addenda. See §9.** |

### Onboarding / KYC-KYB controls

- CIP notice in ToS §1: names, addresses, DOB, "copies of driver's licenses or other identifying documentation" for control parties **and potentially for every Admin User and User**.
- SSN required: "Your social security number is one of several data points required for Rho to fulfill mandatory customer identification requirements."
- **Biometric identity verification**: facial recognition matching a selfie to a government ID, performed by Rho and service providers (PP, Biometric Information and Retention Policy).
- Bank/accounting data pulled via **Plaid, Finicity, Codat**, or 6 months of manual statements.
- UBO collection at 25% threshold, with fallback: "In the event that no individual owns at least 25% of your business, you can add the person who exercises substantial control."
- Application upload limit: **10 MB max file size**.
- **Virtual addresses banned**: "Virtual addresses from Regus or any other provider are not permitted."
- Eligibility: US-incorporated entities only; either a US operating address or one US-based owner with a valid SSN. "Rho Services are only available to businesses based in the United States of America." No consumer use.
- **Ineligible geographies** (`can-i-open-a-rho-account-if-i-dont-live-in-the-u-s`): Cuba, Iran, North Korea, Russian Federation, South Sudan, Sudan, Syria, Venezuela.
- **Prohibited industries** (`business-and-industry-eligibility-at-rho`): betting/casino gaming chips, adult dating/escort, drug stores/pharmacies/cannabis, drugs/proprietaries/sundries, stamp and coin stores, quasi-cash/currency/money orders/travelers checks, pawn shops, bearer shares, bail and bond payments, currency exchange, **nested MSBs/nested money transmitters**, firework sales, online dating.
- **ToS §12 wire-blocked countries** (far broader than the account-ineligibility list, 40+ jurisdictions): Afghanistan, American Samoa, Belarus, Belize, Bonaire, Burundi, Cameroon, Central African Republic, Chad, Colombia, Comoros, Congo, DRC, Cuba, Curacao, Djibouti, Equatorial Guinea, Eritrea, Ethiopia, Guam, Jordan, Iran, Iraq, DPRK, Kosovo, Lebanon, Libya, Madagascar, Mali, Myanmar, **Nigeria**, Russian Federation, Saint Barthelemy, Somalia, South Sudan, Sudan, Syria, Turkmenistan, **Ukraine**, Venezuela, Yemen, Zimbabwe. Plus: "wire payments may not be made **in Indian Rupees**."
- **Card-use restricted countries** are a *third*, different and longer list (Addendum A §1.10), adding Albania, Angola, Bosnia and Herzegovina, **Egypt**, Guinea, Guinea-Bissau, Haiti, Laos, Mauritania, Montenegro, Nicaragua, Niger, North Macedonia, **Pakistan**, State of Palestine, and others.

Three overlapping-but-different restriction lists (account eligibility, wire destinations, card use) with no cross-reference is itself a compliance-diligence finding.

---

## 9. What risk the customer actually carries

### 9.1 The $500 liability cap

ToS §22, verbatim, all caps in original:

> "NOTWITHSTANDING ANYTHING TO THE CONTRARY CONTAINED HEREIN, RHO, ITS AFFILIATES, SPONSOR BANK, THIRD-PARTY SERVICE PROVIDERS, AGENTS, SUPPLIERS AND LICENSORS, SHALL NOT, UNDER ANY CIRCUMSTANCES, BE LIABLE, TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, TO YOU OR ANY THIRD PARTY FOR ANY DAMAGES ATTRIBUTABLE TO LOSS OF PROFITS, SALES OR BUSINESS, LOSS OF ANTICIPATED SAVINGS, LOSS OF USE OR BUSINESS INTERRUPTION, WORK STOPPAGE OR ANY CONSEQUENTIAL, INCIDENTAL, SPECIAL OR EXEMPLARY DAMAGES, EVEN IF RHO HAS BEEN APPRISED OF THE LIKELIHOOD OF SUCH DAMAGES OCCURRING. EXCEPT AS REQUIRED BY LAW OR PURSUANT TO THE "ARBITRATION PROVISION AND CLASS ACTION WAIVER" SECTION BELOW, RHO'S LIABILITY (WHETHER BASED ON AN ACTION OR CLAIM IN CONTRACT, TORT OR OTHERWISE) TO YOU, OR ANY THIRD PARTY, IN ANY WAY CONNECTED WITH OR ARISING OUT OF THIS AGREEMENT (AND ALL OTHER AGREEMENTS BETWEEN RHO AND YOU) WILL AT ALL TIMES BE LIMITED TO A MAXIMUM OF **$500.00 (FIVE HUNDRED UNITED STATES DOLLARS**)."

Also §22: "in the event of any failure of the Rho Services, or in the event Rho otherwise defaults under any provision of this Agreement, then **your sole and exclusive remedy shall be termination of this Agreement** and... you hereby waive and relinquish any and all other rights or remedies it may have at law or in equity."

$500 is not a percentage of fees paid or a 12-month-fees cap. It is a flat, absolute number. It extends to the Sponsor Bank and Third-Party Service Providers as well.

### 9.2 Card unauthorized-use liability: the 10-card cliff

ToS Addendum A §1.6 and Addendum B §1.6, identical language in both card agreements:

> "Unless prohibited by applicable law, or otherwise provided in accordance with any liability waiver program provided by the Card Network (the 'Card Network Liability Waiver Program'), you agree as follows:
> - **if we issue at least ten (10) Cards to you and your Users, you will be liable for all unauthorized use of all Cards.**
> - If we issue fewer than ten (10) Cards to you and your Users, your liability for unauthorized use of a Card will be limited to the lesser of (i) $50.00 or (ii) the amount of money, property, labor or services obtained by the unauthorized use."

Plus Addendum A §1.8:

> "The Rho Corporate Card with Daily Terms is a **commercial credit card and does not provide consumer protections for lost or stolen credit cards or unauthorized transactions**... **Until you report a Rho Corporate Card with Daily Terms as lost or stolen or report an unauthorized transaction on a Rho Corporate Card with Daily Terms, Company is fully responsible for all transactions**, even if the Rho Corporate Card with Daily Terms is lost, misplaced, stolen or used for unauthorized transactions."

And the ex-employee trap:

> "Unless we have received notice and canceled the Rho Corporate Card with Daily Terms, **use of a Rho Corporate Card with Daily Terms by a User at any time, even if the User is no longer associated with or employed by you, does not constitute unauthorized use**."

**This is the sharpest edge in the entire corpus.** `security.txt` tells a prospect "Mastercard Zero Liability protects against unauthorized card fraud." The contract says: at 10+ cards you carry all of it, subject only to whatever the Card Network Liability Waiver Program happens to provide. Mastercard Zero Liability is a network program with its own eligibility conditions that the customer must satisfy; the ToS explicitly preserves Rho's position "unless... otherwise provided in accordance with any liability waiver program provided by the Card Network." A 12-person startup with a card each is already past the cliff.

Also §1.9: "**We are not responsible for tracking or monitoring the Company's Charges, expenses or transactions**... You are responsible for seeking and identifying any Charges that are unauthorized." And §2.1 (Addendum B): "Your failure to communicate with us about any errors, inconsistencies, suspicious activities or disputes **constitutes a waiver to exercise your rights**."

### 9.3 Account-level liability

ToS §6:

> "You agree that we can rely on any request or transaction initiated through such codes **without the need for further confirmation**... You agree that Rho will **not have any responsibility to verify any transaction** in your Rho Account initiated by any User, and **you may be liable for any loss, damage or expense arising from access to a Rho Account by any User of your Rho Account, including anyone else using credentials to access your Rho Account, whether authorized or not**."

Credential-compromise notification has a **one business day** response window on Rho's side: "Rho may interrupt or refuse all access and any orders made using this password within **one (1) business day** following the receipt of the notification."

ToS §13.1: "**Rho does not have the ability to undo Transactions**." §13.4: "Some payment transactions, such as wire transfers may be irreversible, so you agree to exercise extreme caution."

ToS §13.3: "Rho reserves the right to **impose limits on Transactions** and other elements of the Rho Services **at its sole discretion** and where in compliance with applicable law, **without prior notice**. New accounts may be subject to longer hold or review periods."

### 9.4 Cross-guaranty across the corporate group

ToS §17 makes every Rho-account entity guarantee every other one:

> "You absolutely, unconditionally and irrevocably guarantee, **as primary obligor and not merely as surety**, the full and punctual payment and performance of all present and future obligations... required to be observed and performed or paid or reimbursed by you and/or **any of your Rho Accounts that is a subsidiary or parent entity that, directly or indirectly, owns you**..."

The guaranty is "irrevocable, continuing, absolute and unconditional," survives the affiliate's bankruptcy or restructuring, waives subrogation/contribution/reimbursement, waives notice, and is a "guaranty of **payment and performance and not of collection**" so "Rho is not obligated to enforce or exhaust our remedies against any Affiliate... before proceeding." Rho "may resort to you for payment... whether or not Rho has resorted to any collateral therefor."

**For a multi-entity group (the exact customer Rho's `/solutions/enterprise` page targets), this means opening a Rho account for a subsidiary puts the parent's assets behind the subsidiary's card balance.** It is the single most consequential clause for an enterprise CFO and it appears nowhere in marketing.

### 9.5 Setoff and sweep-your-other-accounts rights

Addendum B §2.3:

> "In the event of default under this Monthly Card Agreement, we shall have, to the fullest extent permitted by law, the right to **set off and apply any and all deposits**, against the Company's Obligations, whether such deposit account is held by Rho, **with or without providing notice to you**."

> "you grant Rho the right to initiate electronic fund transfers to **debit any bank accounts for which you have provided routing and account numbers**"

> "You also authorize us... to obtain funds from your Rho Account, any linked account, or any Budget Account **without providing notice to you, on any date and at any time, in our sole discretion, when the total balance... is less than the balance minimum required by our underwriting criteria**."

Also: authorization extends "to benefit any other creditors who may be legally entitled to seize the Company's assets."

### 9.6 Credit-account discretion (the runway risk)

Addendum A §1.3:
- "all advances or extensions of credit... are **uncommitted**."
- "Your spending limit shall be established by us in **our sole discretion**."
- "**At no time shall we be required to disclose the spending limit to you.**"
- "we may modify or change the spending limit at any time, at a frequency of our own choosing, **with or without providing any notice to you**. We reserve the right to **reduce your spending limit to zero dollars** at our sole discretion."
- Continuous financial reporting is mandatory: accounting-platform access, or monthly statements "no later than the thirtieth (30th) day of the following month." Failure can reduce the limit, and: "**you may be held liable for consequential, incidental, special, or exemplary damages for your failure to provide Requested Financial Information**." Note that this is the one place the ToS asserts *consequential damages against the customer*, in the same document where it disclaims them against Rho.

Fees on the credit side: late fee "**three percent (3%) of the delinquent payment balance for each month** that the balance remains unpaid for up to six (6) months." Foreign transaction fee "up to 1% of the transaction amount." Daily Terms has "**no grace period**"; the balance settles to zero at the end of each business day.

Representations that a growth-stage company should read carefully (Addendum A §1.11): the Company represents it "is not in or expects to be in default with respect to any lender, creditor, or other third parties" and that it and "any of its affiliates, principals, officers or directors are **not parties to any litigation or government investigation, whether ongoing or otherwise**" nor party to insolvency/bankruptcy proceedings "at any time during the past ten (10) years." Any company with ordinary commercial litigation is technically in breach at signing.

### 9.7 Termination, suspension, and exit

ToS §20.2:

> "**Rho can terminate or suspend performance hereunder and any Rho Service provided hereunder (including any addendum hereto) at any time for no reason or for any reason without prior notice to or consent from you.**"

Plus discretionary suspension where continuing "would expose Rho to excessive risk, whether legal, regulatory, compliance, security, financial, reputational or otherwise." And §20.4: Rho may "suspend or discontinue the Platform or any or all of the Rho Services at any time at its sole discretion **without liability or penalty**."

**Exit mechanics** (`how-to-close-your-rho-account`), which a CFO should treat as the real switching cost:
1. Closure must be requested by the **Account Owner** only, via phone/chat/email; there is no self-serve close.
2. Card balance must be fully settled first.
3. All scheduled and recurring transactions must be canceled manually.
4. Savings must be emptied, subject to the **six-per-month** withdrawal limit (as of 08/02/2026).
5. Treasury liquidation adds **2 to 3 business days** and is at market price, possibly below cost.
6. **"Your dashboard access ends when the account closes"**, so statements and CSV exports must be pulled before requesting closure. Rho "can provide historical statements on request" afterwards, with no stated SLA.
7. W-9s and vendor tax documents must be downloaded from vendor profiles first.
8. All cards, physical and virtual, are canceled. Residual balance returns "by wire or check."

There is **no data-export or data-return obligation on Rho in the ToS**. §20.3 runs the other way: "Upon request by Rho at termination, **you** agree to either destroy or return all Rho Data and documentation."

### 9.8 Dispute resolution

| Provision | Content |
|---|---|
| Arbitration | Binding, **AAA**, Federal Arbitration Act, **single arbitrator who must be a commercial-law attorney practicing in New York**, in English |
| Class action | Waived. "YOU AND RHO AGREE THAT EACH MAY BRING CLAIMS AGAINST THE OTHER ONLY IN YOUR OR ITS INDIVIDUAL CAPACITY." Consolidation prohibited unless both agree |
| Jury trial | Waived |
| Venue | New York County, New York. Claims $10,000 or under may be documents-only, telephonic, or in-person at the customer's billing-address county |
| Pre-arbitration | Written Notice of Arbitration by certified mail or FedEx to 100 Crosby Street; **30-day** good-faith period |
| Beat-the-offer bonus | If the arbitrator awards more than Rho's last written settlement offer, Rho pays the higher of the award or **$10,000** |
| Carve-outs | Small claims court; agency enforcement actions; injunctive relief in aid of arbitration; IP infringement suits |
| Confidentiality | "All arbitration proceedings between the parties will be confidential" |
| Frivolous-claim risk | If the claim or relief sought is found frivolous under FRCP 11(b), "you agree to reimburse Rho for all monies previously disbursed by it" |
| Opt-out of changes | Only for *future amendments* to the arbitration clause: written notice within 30 days, and "**your Rho Account will be immediately terminated**" |
| **Statute of limitations** | **ToS §26.9: "No legal action of any kind arising out of this Agreement may be brought by you against Rho if the event giving rise to said legal action occurred more than one (1) year before the legal action is commenced."** |

A one-year contractual limitations period is aggressive; New York's default for contract claims is six years.

### 9.9 Amendment and consent

ToS §26.4: "Rho may amend or revise this Agreement, **including any fees**, at any time by providing written notice... **Your continued use of the Platform or Rho Services following the Effective Date of any amendment constitutes your acceptance**." Notice can be in-app. §26.5: "**Rho may assign any of its rights or obligations hereunder without prior notice to or consent from you**," while the customer may not assign at all without Rho's consent, "which consent may be withheld for any reason."

§26.10: "Each Sponsor Bank... is a **third party beneficiary** under this Agreement entitled to enforce the rights of Rho against you." (Note the asymmetry: the bank gets enforcement rights against the customer; the customer gets no stated third-party rights.)

§26.11: "**We may publicly reference you as a Rho client** on our website or in other communications. You grant Rho a limited license to use your trademarks or service marks for this purpose." Opt-out is by emailing clientservice@rho.co. In the other direction, "Any publicity... by you concerning or naming Rho are prohibited without the prior written approval of Rho."

§26.13: Feedback is licensed to Rho "unrestricted, perpetual, irrevocable, non-exclusive, fully-paid, royalty-free."

§26.12: "**We are under no obligation to provide support for the Rho Services**," in a company whose primary marketing claim is 24/7 human support.

### 9.10 Indemnification

ToS §19: the customer indemnifies Rho **and the Sponsor Bank and Third-Party Service Providers** across thirteen enumerated categories, including "(vii) you relationship with any Sponsor Bank or any other Third-Party Service Provider," "(xii) responding to requests for Data or your information by third parties including but not limited to **subpoenas or court orders**," and "(xiii) Transactions or financial transactions of you, **Sponsor Bank or other Third-Party Service Providers**." The customer indemnifies Rho for the Sponsor Bank's own transactions. There is **no reciprocal indemnity from Rho** anywhere in the agreement.

---

## 10. Data handling and privacy

Privacy Policy metadata is itself contradictory: the page header reads "Rho Privacy Policy / June 29, 2025" while the body says "Last updated August 27, 2026."

### What is collected

Legal name, **SSN**, home and/or business address, **biometric information**, government identification, transaction data, state of incorporation, organizational documents, company financials "including real-time financial accounting information provided to and by third parties and linked accounts," credit information, and AML/BSA compliance data.

Behavioral collection is broad and explicitly includes session replay:

> "We, our service providers, and our vendors may also use technologies such as cookies, beacons, and scripts to collect information on how you use the Site or Rho Service, such as your browsing behavior, **clicks and cursor movements**, web pages visited, searches, **text entered in forms** and **replays of your visit** to the Site or Rho Service."

Linked-account aggregation: "Any time you link an account, we may receive real-time data and information associated with the linked accounts including account names, transactions (and transaction history), account balances, bank routing numbers, and unique identifiers."

**Credential storage** (ToS §9, the most under-discussed clause):

> "You authorize us to use Account Information that you provide us, **including usernames and passwords, to log into the third-party site(s)** that maintains your Account Information. You hereby authorize and permit us to **use and store such information**..."
> "By submitting information, data, **passwords, usernames, PINs, other login information**, materials and other content through the Sites ('User Content'), you are licensing the User Content to us..."

Plus a **limited power of attorney**: "You grant Rho (or, in connection with the Treasury Services..., RBB Treasury LLC) limited power of attorney, and appoint Rho... as your **attorney-in-fact and agent**, to access third party sites and retrieve and use your information with the full power and authority to do and perform each thing necessary as you could do in person." A partial guardrail follows: "we shall have **no authority to take or have possession of any assets** in the accounts maintained by such third parties or to direct delivery of any securities or payment of any funds held in such account to itself."

### Commitments and non-commitments

| Area | What Rho says |
|---|---|
| Security posture | "We use certain physical, organizational, and technical safeguards... These measures **may** include, among others, physical access security, administrative security measures, data encryption, firewalls, and other appropriate technologies." Note "may." |
| Honest disclaimer | "**Notwithstanding Rho's efforts, no security measure is perfect or impenetrable and no method of transmission over the internet or electronic storage is 100% secure. Therefore, Rho cannot guarantee complete security** of the transmission or storage of your Personal Information." |
| De-identified data | "this Privacy Policy **does not apply** to De-Identified Information, and we may use and disclose De-Identified Information **for any purposes in our discretion**." No re-identification prohibition, no k-anonymity or aggregation standard stated. |
| Model training | Service providers "are not permitted to use it for their own purposes, **including to train their own models**." Silent on whether **Rho itself** trains models on customer data. |
| Business transfers | "customer information (including your email address) would likely be one of the transferred business assets" in a sale or merger. |
| Fraud-data exchange | "This includes **exchanging information with other companies and organizations** for fraud protection, and spam/malware prevention." |
| Do Not Track | "**we do not currently recognize or respond to browser-initiated DNT signals**." Global Privacy Control **is** honored "in accordance with applicable legal obligations." |
| "Sale"/"sharing" under CCPA | Admitted for online identifiers: "Our use of third-party analytics services and online advertising services, may result in the disclosure of online identifiers (e.g., cookie data, IP addresses, device identifiers, and usage information) in a way that **may be considered a 'sale' or 'sharing' under the CCPA**." Contact info, transactional info, internet/device info, demographic info and professional info are all shared with "Online advertising and analytics partners." |
| Never sold/shared | Account authentication information; SSN and government identifiers; identity-verification info including photograph and ID; financial information; customer-service interactions; service usage; **biometric information**. |
| Analytics | Google Analytics named. |
| Biometric retention | Until the earlier of purpose satisfaction **or within three (3) years of your last interaction with us**, then "delete and permanently destroy." |
| General retention | "We keep your information for no longer than necessary for the purposes for which it is processed." **No schedule, no periods, no per-category table.** |
| Privacy policy changes | If a change is not legally required and "you do not close your Rho Service account within **thirty (30) days** of notice... then you shall be deemed to have accepted the amendment." |
| Conflict of terms | "If you're using Rho through your Company pursuant to a Service Agreement... In the event of a conflict between this Privacy Policy and the data processing terms of the Service Agreement, **the Service Agreement governs**." Same for the DPA in the ToS. |
| Rights channel | "please access the consent preferences here" (a cookie-consent widget). No dedicated DSAR email or portal named. |
| Contact | clientservice@rho.co, 1-(855) 7-GETRHO. **No named Data Protection Officer or privacy contact.** |

---

## 11. Contradictions and inconsistencies across pages

| # | Contradiction | Pages |
|---|---|---|
| 1 | **"400+" vs "more than 300" sweep institutions.** Marketing, help center, and llms.txt all say "400+ FDIC- and NCUA-insured institutions." The binding **ToS Addendum C** says "a deposit network of **more than 300** FDIC-insured banks and NCUA-insured credit unions listed on **Schedule A**." | `trust.txt`, sweep article vs ToS Addendum C |
| 2 | **FDIC-only vs FDIC-and-NCUA.** `/trust` says savings sweeps across "a network of **400+ FDIC-insured banks**" and calls it "$75 million in **FDIC** insurance." The help center and ToS say the network includes **NCUA-insured credit unions**, whose deposits are insured by NCUA, not FDIC. | `trust.txt` vs `how-does-fdic-insurance-coverage-work`, ADM MSA |
| 3 | **Mastercard Zero Liability vs 10-card liability rule.** See §9.2. | `security.txt` vs ToS Addenda A and B §1.6 |
| 4 | **Rho Capital hard pull.** Help center: "Applying doesn't involve a hard pull on your personal credit." Product page: "Application and **consent to obtain personal credit report is required**." | `about-rho-capital` vs `product__capital.txt` |
| 5 | **Rho Capital fees.** Help center: "There are **no origination fees**." Product page: "Fees vary based on risk assessment and loan term," with no origination-fee carve-out. | same pair |
| 6 | **Rho Capital lender identity.** Help center names only "Lead Bank." Product page names **Slope** as underwriter and Lead Bank as lender. | same pair |
| 7 | **Webster asset size.** $76B / "over $76 billion" (security-by-design blog, updated 2026-08-20), "approximately $77bn of combined assets at the time" (Webster blog), $85.5B (call report, 3/31/2026), $327B (Santander group pro forma). | three pages, all "updated" 2026-08-20 |
| 8 | **Webster is publicly traded.** security-by-design still says "As a publicly traded company with over 200 branch and ATM locations." After the 2026-08-20 close, Webster is a division of Santander Bank, N.A. `security.txt` handles it correctly: "a nationally chartered bank within Banco Santander's publicly traded group." | `blog/security-by-design` vs `security.txt` |
| 9 | **FDIC limit qualifier.** "per depositor, per ownership category" vs "per institution, per account type" vs "per entity, not per account" vs "per depositor." | §5 table above |
| 10 | **Savings liquidity.** "next-day liquidity" and "typically settles the next business day" vs ADM's Tue/Thu processing, Wed/Fri settlement, 12:00 CT cutoff, $3M special handling. | `security.txt`, sweep article vs ADM MSA §4 |
| 11 | **"Bank" defined as Rho.** ToS Addendum C: "the terms 'we,' 'our,' 'us,' **'Bank'** and 'Rho' mean Under Technologies, Inc." | ToS Addendum C vs every "Rho is not a bank" disclaimer |
| 12 | **Addendum C mixes up its own products.** The Savings Account Agreement repeatedly refers to "the Rho **Treasury Management** Account" and to persons "authorized by the Company to open a Rho **Treasury** Account" while defining a **Savings** Account. Savings and Treasury are entirely different products with different insurance regimes. | ToS Addendum C |
| 13 | **API scopes.** `cards:read` is required by the cards docs but absent from the authoritative scope table; invoicing endpoints have no documented scope. | `docs_v1_cards.md` vs `docs_v1_auth.md` |
| 14 | **API token lifetime.** "long-lived" vs "Maximum one year" vs "expire automatically after 45 days of inactivity." | `docs_v1_auth.md` |
| 15 | **24/7 support promise vs ToS §26.12** "We are under no obligation to provide support for the Rho Services." | `how-do-i-contact-support` vs ToS |
| 16 | **Privacy Policy date.** "June 29, 2025" in the header, "Last updated August 27, 2026" in the body. | `policies__privacy-policy.txt` |
| 17 | **Restricted-country lists.** Account eligibility (8 countries), wire destinations (42), card use (40+), with different memberships and no cross-reference. Egypt and Pakistan are card-restricted but not wire-restricted; Colombia and Jordan are wire-restricted but not card-restricted. | `can-i-open-a-rho-account...`, ToS §12, Addendum A §1.10 |
| 18 | **Consequential damages.** ToS §22 disclaims them entirely, "UNDER ANY CIRCUMSTANCES." Addendum A §1.3 then asserts them against the customer for failing to deliver financial statements. | ToS §22 vs Addendum A §1.3 |

---

## 12. What a careful CFO wants and Rho does not say

**Audit and certification**
1. **The SOC 2 auditor is never named.** Nor the report period, nor which Trust Services Criteria are in scope (Security only, or Availability / Confidentiality / Processing Integrity / Privacy too). Nor whether there were qualifications or exceptions.
2. **No stated NDA or gating process** for obtaining the SOC 2 report; the help article just says "clicking on this link."
3. **The Trust Center is not in the sitemap** and its contents cannot be verified from anything Rho publishes on rho.co.
4. **No penetration test cadence, no summary letter, no bug bounty or vulnerability disclosure policy.** security@rho.co exists only as a phishing inbox.
5. **No ISO 27001, no PCI DSS attestation for Rho itself**, despite the platform displaying full PAN and CVV in-browser and pushing them into 1Password.

**Security architecture**
6. **No encryption specifics for Rho.** No AES-256 at rest, no TLS version floor, no key management or HSM statement. The only concrete crypto in the corpus belongs to **Plaid**.
7. **No SAML SSO and no SCIM.** Google SSO only. For an enterprise-targeting product ("Rho for Enterprises: Streamline accounting and expenses across multiple entities"), the absence of SAML and automated deprovisioning is a hard blocker at many companies.
8. **No customer-visible audit log or admin activity export** is documented anywhere. "Full audit trails" is asserted once on the Bill Pay bullet of `solutions__enterprise.txt` with no article describing it. A permission exists to "View your user profile and activity," which is per-user, not organization-wide.
9. **No IP allowlisting for the web app** (only for API tokens).
10. **No session management controls**: no documented session timeout, concurrent-session limit, or device-revocation screen. The ToS says "No more than one individual shall gain access to a User account at any given time" but no enforcement mechanism is described.
11. **No named sub-processor list.** Plaid, Finicity, Codat, Wise, ADM, Apex, Interactive Brokers, Navan, Slope, Lead Bank are each disclosed somewhere, but there is no single consolidated register, and the **AI model providers are never named**.

**Continuity and operations**
12. **No uptime SLA, no published status page, no historical availability data.** ToS §7 affirmatively disclaims liability for interruptions.
13. **No RTO/RPO, no business continuity or disaster recovery statement.**
14. **No incident notification commitment.** Neither the ToS nor the Privacy Policy commits Rho to notifying the customer of a security incident or data breach within any timeframe. The obligation runs only in the customer's direction: "You shall **immediately notify Rho** of any actual or suspected breaches in the security of your devices or any Data."
15. **No data retention schedule.** "no longer than necessary" is the entire commitment for everything except biometrics (3 years).
16. **No customer data-export or data-return obligation on termination.** Dashboard access ends at closure; statements are available "on request" with no SLA.

**Financial and counterparty**
17. **The sweep network Program Institution list is not published.** "The current list of network institutions is available from Rho support on request." A CFO cannot pre-check for concentration against banks the company already uses, and **an existing relationship with a Program Institution silently erodes coverage**, since FDIC aggregates per depositor per bank. The ADM agreement says so ("subject to the aggregation of any other funds you have on deposit at the same Program Institution in the same legal capacity"); **Rho's marketing never mentions it.** This is the largest substantive omission in the FDIC story.
18. **ADM Schedule A is referenced but never published.**
19. **"Up to $75M" is not "$75M."** Actual coverage depends on how many Program Institutions accept funds at any moment, which ADM controls unilaterally. No minimum guaranteed coverage is stated.
20. **The accredited-investor representation** required by the ADM agreement is never surfaced in Rho's savings marketing.
21. **The intraday/overnight single-bank concentration window** is disclosed only inside the ADM contract, never on `/trust` or `/security`.
22. **Rho's own financial condition is never disclosed**: no funding history, no revenue, no runway, no investor list, no audited financials, no regulatory actions. "Founded in 2018," "New York-based," "thousands of businesses," "more than a dozen publicly traded companies run on Rho" is the sum of it.
23. **The Webster Deposit Account Agreement ("the Webster Agreement") is incorporated by reference and mandatory but is not published on rho.co.** Same for the **DPA**, the **Deposit Account Agency Agreement**, and **Rho Treasury's Form ADV-2A Wrap Fee Brochure** (linked, not hosted).
24. **What happens to the Webster relationship post-Santander is never addressed.** Rho's entire trust narrative now rests on an acquisition that closed three weeks before this corpus was captured. There is no statement about contract continuity, repapering, program-manager agreement renewal, or what happens if Santander exits BaaS-style partnerships.
25. **No cyber/crime insurance or fidelity bond is mentioned**, which is what would actually respond to the $500 liability cap.
26. **No fraud-loss reimbursement policy.** There is no analogue to a "we will make you whole" commitment for ACH or wire fraud; the ToS says the opposite.

**Contractual**
27. **The $500 cap, the 10-card rule, and the cross-guaranty appear in no marketing material whatsoever.** All three are found only by reading a 714-line, ~200KB Terms of Service.
28. **No fee schedule stability commitment.** Fees change "at any time," and the published fee facts in the corpus are thin: "$30 wire recall fee, optional $15 SWIFT fee and 1% foreign currency conversion fee" (ToS §15), plus "up to 1% of the transaction amount on foreign transactions" and a **3% per month late fee** in the card addenda.
29. **No stated dispute-resolution SLA** for chargebacks or ACH errors: "Rho uses commercially reasonable efforts to investigate the error, but **makes no representation as to its ability to correct the error**."

---

## 13. Things Rho does unusually well (for balance)

- The FDIC/SIPC distinction is stated correctly and repeatedly, including the sentence most fintechs bury: "It does not protect you against the failure of Rho or other third party."
- `/trust` volunteers the failure-mode question ("What happens to my money if Rho shuts down?") and answers it accurately.
- The $75M figure is consistently labeled "**up to**" and consistently scoped to Savings, with checking and Treasury explicitly excluded in the same breath.
- Treasury yield headlines are stated **net of fees** with the fee tier disclosed on the same row and a dated as-of ("Yields as of 09/11/2026 and change daily").
- SIPC is described as protecting against "custodial failure, not market loss," which is the correct and commonly-botched framing.
- The ACH debit-approval feature documentation honestly enumerates its own weaknesses (shared Company IDs, unverifiable IDs, irreversible returns).
- API security design is above average for the category: mandatory expiry, 2FA-gated creation, per-token IP allowlists, immediate revocation, read-only scopes, PKCE with rotating single-use refresh tokens.
- The direct-integration (no BaaS middleware) architecture claim, if true, materially reduces the Synapse-class intermediary failure mode that has stranded fintech deposits.

---

## 14. Source index

| Topic | File |
|---|---|
| Security narrative, product-by-product protection | `pages/core/security.txt` |
| Deposit-holder claims, competitor bank table, FDIC FAQ | `pages/core/trust.txt` |
| Privacy Policy (CCPA table, biometrics, retention) | `pages/core/policies__privacy-policy.txt` |
| Terms of Service v7.0.0, 2026-08-27, 714 lines, 5 addenda | `pages/core/policies__terms-of-service.txt` |
| Company positioning, universal footer | `pages/core/about.txt` |
| FDIC scope per product, $25K savings minimum | `pages/help/help-center__general-rho-information__how-does-fdic-insurance-coverage-work.txt` |
| Webster history and partnership benefits | `pages/help/help-center__general-rho-information__our-partnership-with-webster-bank-n-a-member-fdic.txt` |
| SOC 2 Type 2 | `pages/help/help-center__general-rho-information__soc-2-type-2-compliance.txt` |
| ADM Master Services Agreement (full text) | `pages/help/help-center__general-rho-information__rho-savings-account-terms-and-conditions.txt` |
| Sweep mechanics, withdrawal limits | `pages/help/help-center__banking__how-the-rho-savings-sweep-works.txt` |
| Account closure / exit mechanics | `pages/help/help-center__general-rho-information__how-to-close-your-rho-account.txt` |
| 2FA setup and admin enforcement | `pages/help/help-center__admin__set-up-2-factor-authentication.txt` |
| Google SSO | `pages/help/help-center__admin__managing-google-sso-for-your-organization.txt` |
| Step-up 2FA policies | `pages/help/help-center__admin__require-2fa-for-sending-transactions-creating-cards.txt` |
| Fraud alerts and reporting | `pages/help/help-center__admin__how-to-report-suspicious-activity-on-your-account.txt`, `...__how-to-enable-sms-notifications-for-suspicious-transactions.txt` |
| Full RBAC permission glossary | `pages/help/help-center__admin__user-permissions-glossary.txt` |
| ACH positive pay (beta) | `pages/help/help-center__banking__manage-your-ach-debit-approvals-in-rho-beta-.txt` |
| KYC/KYB, Plaid/Finicity/Codat | `pages/help/help-center__general-rho-information__applying-to-rho-faqs.txt` |
| Prohibited industries | `pages/help/help-center__general-rho-information__business-and-industry-eligibility-at-rho.txt` |
| Ineligible countries | `pages/help/help-center__banking__can-i-open-a-rho-account-if-i-dont-live-in-the-u-s.txt` |
| DACA (springing only) | `pages/help/help-center__banking__does-rho-support-daca-accounts.txt` |
| Treasury fees, custodians, SIPC | `pages/core/product__treasury.txt` |
| Rho Capital / Slope / Lead Bank | `pages/core/product__capital.txt`, `pages/help/help-center__general-rho-information__about-rho-capital.txt` |
| API auth, scopes, OAuth | `docs/docs_v1_auth.md`, `docs/docs_v1_partner-auth.md` |
| Security-control changelog dates | `pages/core/changelog.txt` |
| Webster history (fetched 2026-09-11) | `pages/extra/blog__rho-and-webster-bank.txt` |
| BaaS vs direct integration argument (fetched 2026-09-11) | `pages/extra/blog__security-by-design.txt` |
| Rho's self-description for machines | `site-llms.txt`, `site-llms-full.txt` |
