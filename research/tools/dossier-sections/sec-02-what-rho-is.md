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
