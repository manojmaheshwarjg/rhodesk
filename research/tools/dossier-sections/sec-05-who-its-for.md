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
