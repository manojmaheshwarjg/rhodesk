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
