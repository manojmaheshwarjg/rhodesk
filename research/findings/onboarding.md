# Rho: Access, Onboarding, Identity and Account Structure

Research dossier section. Corpus date: local crawl 2026-09-11. Today: 2026-09-11.
All facts sourced from the local Rho corpus. Rho's own pages are marketing; claims Rho makes about itself or competitors are marked `[Rho claim]`.

---

## 0. Who the counterparty actually is

| Item | Value | Source |
| --- | --- | --- |
| Legal entity | Under Technologies, Inc. DBA Rho Technologies | Site-wide footer, `/policies/terms-of-service` |
| Trademark holder | Under Technologies, Inc. | Site-wide footer |
| Copyright range | "© 2019 - 2026" | Site-wide footer |
| HQ address | 100 Crosby Street, New York, NY 10012 | Site-wide footer |
| Regulatory status | "Rho is a fintech company, not a bank or an FDIC-insured depository institution" | Repeated on every product page |
| Checking + card issuer | Webster Bank, a division of Santander Bank, N.A., Member FDIC | `/product/business-banking`, ToS |
| Savings provider | American Deposit Management Co. (ADM) and its partner banks | Footer disclosures |
| International/FX payments | Wise US Inc. | Footer disclosures |
| Treasury advisor | RBB Treasury LLC dba Rho Treasury, SEC-registered investment adviser, Rho subsidiary | Footer, `/help-center/treasury/about-rho-treasury` |
| Treasury custodians | Apex Clearing Corp. and Interactive Brokers LLC (FINRA/SIPC) | Footer |
| Capital (credit line) lender | **Lead Bank** (not Webster) | `/help-center/general-rho-information/about-rho-capital` |
| ToS version in corpus | **Version 7.0.0, last updated August 27, 2026** | `/policies/terms-of-service` |
| SOC 2 | "Rho is SOC 2 Type 2 compliant... audited every year by a third-party" | `/help-center/general-rho-information/soc-2-type-2-compliance` |

Note: the ToS body says checking and credit card services are "available from Webster Bank, a division of Santander Bank, N.A." The Webster/Santander description is inconsistently rendered across the corpus: `/help-center/general-rho-information/our-partnership-with-webster-bank-n-a-member-fdic` is titled "…Webster Bank, N.A. Member FDIC" while body copy says "a division of Santander Bank, N.A." Santander's US banking organization is described as $327B in assets "(per Santander, 08/20/2026)" in `site-llms-full.txt`; the Clerky partner page instead says "$70B AUM" for the same partner. **These two figures contradict each other.**

---

## 1. Who can open a Rho account

### 1.1 The binding statement (Terms of Service, §13 "Prohibited Users")

Verbatim:

> "You agree that the Rho Services may not be used for **individual consumer use**. You agree and understand that you must be a **business, charitable organization or not-for-profit organization** to be party to this Agreement and access to the Rho Services."
>
> "**Rho Services are only available to businesses based in the United States of America.**"

Prohibited persons, verbatim enumeration from §13:

| # | Prohibited person |
| --- | --- |
| (i) | Persons on the U.S. Treasury OFAC **Specially Designated Nationals List (SDN)**, or otherwise subject to sanctions enforced by OFAC or any government authority including the **United Nations, the European Union, the State Secretariat for Economic Affairs of Switzerland, the Swiss Directorate of International Law, H.M. Treasury of the United Kingdom, the Hong Kong Monetary Authority, or the Monetary Authority of Singapore** |
| (ii) | Authorized Users who are natural Persons **less than 18 years of age or the age of majority in the state in which your business is located** |
| (iii) | Persons, **or their Affiliates**, who have procured any services from Rho and have been **terminated for cause by Rho** |
| (iv) | Individual consumers |

ToS §18.3 "Business Use Only" restates the representation: "You are a business, charitable organization or not-for-profit organization and shall use the Rho Services for only business purposes and not for individual consumer purposes."

ToS §18.1 "Legal Authority": "You are the **exclusive owner of the Rho Account and are not operating the Rho Account on behalf of any third party**." §13.1 reinforces: "You agree to use the Rho Services only for good faith Transactions and **not for Transactions on behalf of third parties**."

### 1.2 Entity types: eligible vs excluded

| Entity type | Status | Source and exact wording |
| --- | --- | --- |
| Corporation (incl. Delaware C-corp) | Eligible | `/product/business-banking`: "Articles of Incorporation for a corporation" listed as accepted formation doc |
| LLC (single-member) | Eligible | "A single-member LLC can usually open an account with formation documents, an EIN, and an ID" |
| LLC (multi-member) | Eligible, with extra doc | "multi-member LLCs should also have the operating agreement ready, since it shows who can sign for the company" |
| "other US-incorporated entities" | Eligible for cards | `/faq`: "LLCs, C-corps, and other US-incorporated entities can apply for a Rho Corporate Card with an EIN and formation documents" |
| Charitable organization / not-for-profit | Eligible **per ToS**, never mentioned in marketing | ToS §13, §18.3 |
| VC funds / fund entities | Marketed to | `/fund-banking`: "Built for VCs and their portfolio companies… every entity in one login" |
| **Sole proprietorship** | **Explicitly INELIGIBLE** | `/product/business-banking`: "**Sole proprietorships aren't eligible on Rho; the business needs to be a registered LLC or corporation.**" |
| Individual consumers | Explicitly prohibited | ToS §13 |
| Non-US-incorporated entity | Ineligible | "entities must be incorporated in the United States" |

**Key gap: there is no page in the corpus that enumerates accepted entity types positively.** Eligibility for S-corps, partnerships, LPs, LLPs, trusts, PBCs (Delaware Public Benefit Corporations), holding companies, series LLCs, SPVs, and DAOs is never stated. The sole-proprietorship exclusion is the only explicit entity-type exclusion, and it appears once, buried in an SEO "in-depth guide" block on `/product/business-banking`, not in any help-center eligibility article.

### 1.3 Incorporation product: much narrower entity scope

`/product/incorporation` and `/help-center/general-rho-information/incorporating-your-company-with-rho`:

- "**Delaware C-corps only** — other entity types and states aren't supported yet"
- "Rho Incorporation forms Delaware C-corps only"
- "Does Rho support LLC formation? **Not yet.** Rho Incorporation is C-corp only today; **LLC formation is coming soon**."
- Nav promo copy: "New Delaware C-Corp, filed in about 24 hours. **LLC coming soon.**"

So the incorporation funnel is strictly narrower than the banking funnel: Rho will *bank* an LLC but will not *form* one.

---

## 2. Geographic requirements

### 2.1 The eligibility rule (and its contradiction)

`/help-center/banking/can-i-open-a-rho-account-if-i-dont-live-in-the-u-s` (title: "Can I Open a Rho Account if I Don't Live in the U.S.?"):

> "Rho partners with Banks to offer accounts to **business owners worldwide**. However, entities must be **incorporated in the United States**, and **either** hold a **US Operating Address** **or** have **one business owner based in the United States with a valid tax identification number (SSN)**."

`/product/incorporation` states the requirement as a conjunction, not a disjunction:

> "At least one **US-based owner or officer** **and** a **US operating address**"
> "Who can incorporate with Rho? At least one owner or officer must be US-based **with** a US operating address, and your business can't be in a restricted industry or country."

**Contradiction to carry:** banking eligibility is stated as `US-incorporated AND (US operating address OR one US-based owner with SSN)`; incorporation eligibility is stated as `US-incorporated AND US-based owner/officer AND US operating address`. The help-center "either/or" is the more permissive of the two. Which governs a plain banking application is not resolved anywhere in the corpus.

A third framing appears in ToS §13: "Rho Services are only available to businesses **based in** the United States of America" — "based in" is undefined and is stricter-sounding than "incorporated in."

`/help-center/general-rho-information/business-and-industry-eligibility-at-rho` opens with: "Rho offers accounts to business owners **worldwide**."

### 2.2 Virtual addresses

`/help-center/general-rho-information/applying-to-rho-faqs`:

> "Is a Regus address permissible? **Virtual addresses from Regus or any other provider are not permitted.**"

`/product/incorporation` requires "A **physical** U.S. operating address."

Contrast: `/help-center/general-rho-information/can-i-change-my-business-address` exists in the corpus but the corpus provides no rule on PO boxes for the *business* address. (A separate page, `/help-center/payments/can-i-send-a-wire-to-a-vendor-with-a-po-box-address`, covers vendor PO boxes only.)

### 2.3 Ineligible owner locations (account eligibility)

Both `/help-center/banking/can-i-open-a-rho-account-if-i-dont-live-in-the-u-s` and `/help-center/payments/restricted-countries-and-international-payment-types` give the same 8-country list. The payments page states the link explicitly: "**Owners from these countries are also ineligible to apply for an account.**"

| ISO | Country |
| --- | --- |
| CU | Cuba |
| IR | Iran, Islamic Republic of |
| KP | Korea, Democratic People's Republic of |
| RU | Russian Federation |
| SS | South Sudan |
| SD | Sudan |
| SY | Syrian Arab Republic |
| VE | Venezuela, Bolivarian Republic of |

Framing: "As a U.S. company, Rho and its affiliates must comply with U.S. law, including trade sanctions administered and enforced by the Office of Foreign Assets Control (OFAC). **To further reduce risk, fraud and illegal activities, Rho and its partners prohibit additional high-risk locations.**"

### 2.4 Payment-only geographic restrictions (not owner eligibility, but same page)

"International Banking Payment restriction" list (payments blocked; *not* stated to block account opening) — 40 entries:

Afghanistan (AF), Burundi (BI), Belarus (BY), Belize (BZ), Bonaire (BQ), American Samoa (AS), Bouvet Island (BV), Central African Republic (CF), Curaçao (CW), Chad (TD), Crimea, Eritrea (ER), Iraq (IQ), Libya (LY), Congo Republic (CG), Congo DRC (CD), Djibouti (DJ), Donetsk and Luhansk People's Republic, French Southern Territories (TF), Guam (GU), Guinea (GN), Pakistan (PK), Nigeria (NG), Equatorial Guinea (GQ), Madagascar (MG), Swaziland (SZ), Somalia (SO), Saint Barthelemy (BL), Saint Martin French Part (MF), Turkmenistan (TM), Palestine (PS), Jordan (JO), British Indian Ocean Territory (IO), Venezuela (VE), Togo (TG), Tokelau (TK), Syria (SY), South Georgia and the South Sandwich Islands (GS), Mayotte (YT), Myanmar (MM), North Korea (KP), Sint Maarten (SX), Cameroon (CM), Yemen (YE), Zimbabwe (ZW).

Currency exceptions table:

| ISO | Country | Currency / rule |
| --- | --- | --- |
| BD | Bangladesh | BDT (payments to businesses not supported) |
| BR | Brazil | BRL (payments to businesses not supported) |
| CO | Colombia | COP (payments to businesses not supported) |
| EH | Western Sahara | MAD (payments to individuals **and** businesses supported) |
| TZ | Tanzania | TZS (payments to businesses not supported) |
| QA | Qatar | EUR or GBP (USD unsupported at this time) |
| PK | Pakistan | PKR (payments to businesses not supported) |
| UA | Ukraine | UAH (payments to businesses not supported) |

"Card Transaction restriction" list (merchants in these countries blocked): Afghanistan, Burundi, Belarus, Central African Republic, Chad, Congo Republic, Congo DRC, Donetsk and Luhansk People's Republic, Myanmar, Iraq, Eritrea, **Albania, Angola, Bosnia and Herzegovina, Ethiopia** (list continues past corpus capture).

ToS §12 "Prohibited Activities" carries its own wire-payment blocklist that **does not match** the help-center list. ToS §12 verbatim: "At this time, wire payments may not be made to the following countries: Afghanistan, American Samoa, Belarus, Belize, Bonaire, Burundi, Cameroon, Central African Republic, Chad, Colombia, Comoros, Congo, Democratic Republic of Congo, Cuba, Curacao, Djibouti, Equatorial Guinea, Eritrea, Ethiopia, Guam, Jordan, Islamic Republic of Iran, Iraq, People's Democratic Republic of Korea, Republic of Kosovo, Lebanon, Libya, Madagascar, Mali, Myanmar, Nigeria, Russian Federation, Saint Barthelemy, Somalia, South Sudan, Sudan, Syrian Arab Republic, Turkmenistan, Ukraine, Bolivarian Republic of Venezuela, Yemen, Zimbabwe." Plus: "At this time, wire payments may not be made in **Indian Rupees**."

**Contradictions:** the ToS list includes Comoros, Kosovo, Lebanon, Mali and Ethiopia, which the help-center payments page does not; the help-center list includes Guinea, Swaziland, Palestine, Togo, Tokelau, Mayotte, Sint Maarten, French Southern Territories, Bouvet Island, South Georgia, British Indian Ocean Territory, Crimea and Pakistan, which the ToS does not. The ToS blanket-bans INR wires while the help center maintains a separate `/help-center/payments/inr-purpose-code-restrictions` article and a `how-to-transfer-funds-in-pakistani-rupees-pkr` article, implying both currencies are in fact supported in some form.

---

## 3. Prohibited business and industry types

There are **two distinct, non-overlapping prohibited lists** in the corpus. Neither cross-references the other.

### 3.1 Help center list — "certain high risk businesses may also be prohibited"

`/help-center/general-rho-information/business-and-industry-eligibility-at-rho` (page `<title>`: "Rho | Compliance: Who Can Open a Rho Account"). Framing is hedged: "businesses that offer illegal services or products are not eligible… In addition, **certain high risk businesses may also be prohibited, such as the following industries**:"

1. Betting, casino gaming chips, etc.
2. Adult dating and/or escort services
3. Drug stores, pharmacies, and cannabis
4. Drugs, proprietaries and sundries
5. Stamp and coin stores
6. Quasi-cash, currency, money orders, travelers checks
7. Pawn shops
8. Bearer shares
9. Bail and bond payments
10. Currency exchange businesses
11. Nested MSBs / Nested money transmitters
12. Firework sales
13. Online dating services

Note the hedge: "may also be prohibited" and "such as" — this is a non-exhaustive, discretionary list, not a rule.

### 3.2 Terms of Service list — "Prohibited Activity" (the binding glossary definition)

ToS §29 Glossary. Far longer and materially broader. Verbatim enumeration, "the operation of or the direct or indirect facilitation of any of the following":

| # | Prohibited Activity |
| --- | --- |
| 1 | any act that is illegal in the United States or in the jurisdiction where the person carrying out the activity is resident, domiciled or located |
| 2 | bath salts and herbals |
| 3 | **bill payment services** |
| 4 | buyers or discount clubs |
| 5 | cigarettes, tobacco or e-cigarettes |
| 6 | gambling |
| 7 | credit counseling or repair agencies |
| 8 | credit protection or identity theft protection services |
| 9 | **digital goods regulated as securities or derivatives and digital currencies** |
| 10 | direct marketing or subscription offers |
| 11 | inbound or outbound telemarketing businesses including lead generation businesses |
| 12 | infomercial sales |
| 13 | internet, mail or telephone order pharmacies or pharmacy referral services |
| 14 | items that encourage, promote, facilitate or instruct others to engage in illegal activity |
| 15 | items that may be counterfeit (designer handbags, clothing and accessories, consumer electronics) |
| 16 | items that may infringe or violate any copyright, trademark, right of publicity or privacy or any other proprietary right |
| 17 | items that promote hate, violence, racial intolerance, or the financial exploitation of a crime |
| 18 | items that promote, support or glorify acts of violence or harm towards self or others |
| 19 | **legal fees including bankruptcy attorneys** |
| 20 | **live animals** |
| 21 | **medical equipment** |
| 22 | multi-level marketing businesses (MLM) |
| 23 | obscene or pornographic items |
| 24 | **payment aggregators** |
| 25 | prepaid phone cards or phone services |
| 26 | purchase, sale or promotion of **drugs, alcohol, or drug paraphernalia**, or items that may represent these uses |
| 27 | **real estate or motor vehicles** |
| 28 | rebate based businesses |
| 29 | sales of money-orders or foreign currency |
| 30 | up-sell merchants |
| 31 | using the Rho Services as a means to **transfer funds between bank accounts held in the same name** |
| 32 | using the Rho Services for any illegal purpose or in violation of any local, state, national or international law |
| 33 | use Rho or any payment card network reasonably believes to be abuse of the payment card system or violation of network rules |
| 34 | use in any manner that could damage, disable, overburden, or impair Rho, "including without limitation, **using the Rho Services in an automated manner**" |
| 35 | using the Rho Services in violation of the terms of the Agreement, as reasonably determined by Rho |
| 36 | using the Rho Services in any way that assists others in violation of any law, statute or ordinance |
| 37 | collecting payments supporting **pyramid or ponzi schemes, matrix programs, other "business opportunity" schemes or certain multi-level marketing programs** |
| 38 | using the Rho Services to control an account linked to another account that engaged in any of the foregoing |
| 39 | using the Rho Services to defame, harass, abuse, threaten or defraud others, or collect personal information about others without consent |
| 40 | intentionally interfering with another person's enjoyment of it (viruses, adware, spyware, worms, malicious code) |
| 41 | making unsolicited offers, advertisements, proposals, or sending junk mail or spam |
| 42 | sending or receiving what Rho considers funds resulting from fraud or other illegal behavior |
| 43 | impersonating any person or entity or falsely claiming an affiliation |
| 44 | **weapons including replicas and collectible items** |
| 45 | **weight loss programs** |
| 46 | **wire transfer money orders** |

Notable: #27 "real estate or motor vehicles" is an extremely broad exclusion that would, read literally, exclude real-estate brokerages, property managers, car dealerships, and PropTech. #21 "medical equipment" and #19 "legal fees including bankruptcy attorneys" are similarly broad. #3 "bill payment services" and #24 "payment aggregators" would exclude a large class of fintechs — while Rho itself markets "Bill Pay." None of this is reconciled anywhere on the marketing side; Rho's customer case studies include a **freight broker** (Best Bay Logistics), **consumer brands** (Dr. Squatch LLC, Mad Rabbit, MUD\WTR, Munk Pack), a **govtech** firm (Polimorphic), and a **PEO/payroll** firm (Niural).

ToS §12 carve-out for AI: "your access to or use of any application, integration or AI-Assisted Feature that Rho makes available to you, in the manner Rho intends and in accordance with this Agreement, **is not a Prohibited Activity, including where that use involves automated access to, or automated delivery of, Data**" — this narrows #34.

### 3.3 What is conspicuously NOT on the prohibited list

Neither list names: **cryptocurrency exchanges or custodians by name** (only "digital currencies" as a good), **firearms dealers** (only "weapons" as an item category), **defense contractors**, **political campaigns or PACs**, **religious organizations**, **staffing/PEO**, **debt collection**, **telemedicine**, **short-term lending / payday**, **ATM operators**, **precious metals dealers** (only "stamp and coin stores"), or **shell / holding companies with no operations**. No revenue minimum, no funding-stage minimum, no minimum-headcount requirement is stated anywhere for the core checking account.

---

## 4. Ownership, officer and UBO requirements

| Requirement | Exact wording | Source |
| --- | --- | --- |
| Beneficial ownership threshold | "a government-issued photo ID for any owner with **25% or more** of the company"; "Ownership information for anyone who owns **25% or more**" | `/product/business-banking` |
| No 25% owner exists | "In the event that **no individual owns at least 25%** of your business, you can add the person who exercises **substantial control** over the business instead (i.e. typically the **CEO or financial officer**)." | `/help-center/general-rho-information/applying-to-rho-faqs` |
| SSN | "Your social security number is one of several data points required for Rho to fulfill **mandatory customer identification requirements**" | applying-to-rho FAQs |
| US-based owner/officer | At least one, per incorporation page; per banking page, satisfiable by US operating address instead | see §2.1 |
| Age | Users must be 18+ or age of majority in the state where the business is located | ToS §13(ii) |
| UBO collaboration | "You can invite collaborators to help with **adding a UBO (Ultimate Beneficial Owner)**. You can invite them directly from those steps in the application flow." | applying-to-rho FAQs |
| Signatory authority | "The signatory to this Agreement has the legal authority to bind your organization" | ToS §18.1 |
| Owner-location gate | "Owners from these countries are also ineligible to apply for an account" (8-country list, §2.3) | restricted-countries page |

International founders: "**International founders without a U.S. SSN or TIN are supported too** — expect a longer EIN timeline from the IRS" (`/help-center/general-rho-information/incorporating-your-company-with-rho`). This is stated only for the *incorporation* path.

Personal guarantee: repeatedly disclaimed for **cards** — "No personal guarantee, no consumer credit report, no personal credit score pull" (`/product/corporate-cards`); "Applying for a Rho Corporate Card does not require a personal guarantee or a personal credit report, so it does not affect your personal credit score" (`/faq`). **But Rho Capital contradicts this posture**: "Application and consent to obtain **personal credit report** is required… **Personal Guaranty may be required.**" (`/help-center/general-rho-information/about-rho-capital`, disclosure). Capital also says "Applying doesn't involve a **hard** pull on your personal credit" — a soft pull is therefore implied.

---

## 5. Pre-EIN onboarding

The single most differentiated eligibility mechanic in the corpus.

| Claim | Exact wording | Source |
| --- | --- | --- |
| Support exists | "Yes. Rho supports **pre-EIN onboarding**, so you can start banking while your EIN application is in progress." | incorporating-your-company help page |
| Windows | "**Non-VC-backed founders get a 30-day pre-EIN window** before the EIN arrives; **VC-backed founders get 60 days.** **Both require manual review, and neither is guaranteed.**" | `/product/incorporation` FAQ |
| Money movement block | "**Funds cannot move until the IRS issues your EIN and it attaches to your account.**" | `/product/incorporation` FAQ |
| Deposits vs transfers | "an uploaded **SS-4 lets you start depositing**; the **EIN itself unlocks outgoing transfers**" | `/product/business-banking` |
| Partner paths | "whether you form through Rho, **Stripe Atlas, or Clerky**" | `/startups` FAQ |
| Clerky | "Pre-EIN applications supported.†" | `/clerky` |
| Blog restatement | "Rho supports pre-EIN account opening through both integrations — the same-day path still applies." | `blog/best-banks-for-seed-stage-startups` |

The 30-day / 60-day split by VC-backing is stated **exactly once in the entire corpus** (`/product/incorporation` FAQ). No help-center page mentions it. What happens at day 31 / day 61 without an EIN is not stated.

EIN retrieval if lost (`/help-center/general-rho-information/how-do-i-request-my-business-ein`):
- "**You'll need your EIN letter to join Rho.**" (flatly contradicts pre-EIN onboarding)
- Call IRS Business & Specialty Tax Line at **1-800-829-4933**, **7:00 AM to 7:00 PM local time**, request a **147c letter**. "The request is free and typically processed the **same-day**."
- Rho's inbound fax for 147c letters: **+1 646-455-3240**. "Please alert your **business banker** that it's on its way."

---

## 6. The incorporation flow and the $400 refund

### 6.1 What is included

`/product/incorporation` and `/help-center/general-rho-information/incorporating-your-company-with-rho`:

| Included | Detail |
| --- | --- |
| Delaware certificate of incorporation | Filed on your behalf; state filing fees included in the $400 |
| Attorney review | "every formation document **reviewed and approved by a licensed attorney**" / "A licensed attorney reviews and **signs off** on your certificate of incorporation" |
| EIN application | "Your **SS-4** (EIN application) submitted to the IRS" / "prepared and submitted for you" |
| Registered agent | "included for the **first year**" |
| Bank account application | "opens in the same flow, **subject to approval**" |

Four-step flow, verbatim step names: **01 Answer a short questionnaire** (company name, share structure, founder details) → **02 Rho files with Delaware** → **03 Get your formation documents** (attorney sign-off) → **04 Apply for your Rho account and EIN**.

"Most founders finish the flow in about **5 minutes**."

### 6.2 Timing

- "Roughly **80% of filings complete within 24 hours**." (repeated 6+ times)
- Footnote defines the measurement precisely: "Filing time measures **Delaware state filing only, starting the next business day after you submit your information**; it **does not measure EIN issuance or account approval**. About 80% of filings complete within 24 hours; **Delaware processing backlogs can extend this window**."
- Sequencing: "Rho files your Delaware certificate **first**, then submits your EIN application. …the EIN follows on the IRS's timeline."

### 6.3 The $400 fee and the refund conditions

Three materially different versions of the same offer exist in the corpus.

**Version A, `/product/incorporation` body and `/help-center` (the operative one):**
> "$400 fee, credited back once you **deposit $10,000 in new money** into your Rho checking account **and keep your daily average balance at least $10,000 above where it started** for the **60 days after incorporation** (terms apply)."

**Version B, help-center adds an accelerator carve-out:**
> "…**($1,000 for founders introduced through an accelerator)**."
> Ambiguous: it is not stated whether $1,000 replaces the $10,000 deposit, the $10,000 balance delta, or both. This clause appears **only** on the help-center page.

**Version C, `site-llms-full.txt`, Rho's own machine-readable summary:**
> "Rho offers **free** Delaware C-corp incorporation — the $400 **deposit** is **fully refunded** once you open a Rho account and **maintain a $10,000 average checking balance for 60 days** (as of **08/02/2026**)."
> This version (a) calls the product "free," (b) calls the $400 a "deposit" rather than a fee, and (c) **drops the "new money" and "above where it started" conditions entirely**, converting a delta requirement into an absolute balance requirement. `/product/incorporation` FAQ directly rebuts it: "**Does Rho offer free incorporation? Rho Incorporation costs $400**, credited back once…"

**Full legal terms (`/product/incorporation` footnote):**

| Condition | Exact term |
| --- | --- |
| Qualification (1) | Incorporate through Rho Incorporation on the Rho platform |
| Qualification (2) | Deposit **at least $10,000.00** into your Rho checking account **and** maintain a daily average balance **at least $10,000.00 greater than the balance immediately prior to that qualifying deposit** for **sixty (60) days after the incorporation** |
| Stacking | "You may earn **more than one reward**." Each additional concurrent reward requires an **additional $10,000 deposit** and raises the daily-average-balance delta by **$10,000** per reward (2 rewards → $20,000 deposit and $20,000 delta) |
| Stacking decay | "Once a reward's sixty (60)-day qualifying period has ended, the corresponding deposit and daily average balance amounts **no longer count** toward the requirement for any subsequent, non-concurrent reward." |
| Anti-gaming | "**Substituting or reallocating pre-existing funds will not satisfy this account balance requirement.**" |
| Payout mechanic | "reimbursement of the **$400.00 fee**… credited to your Rho checking account **within thirty (30) days following the first sixty (60) days** of the opening of your Rho checking account **if we determine that you have met these offer requirements**" |
| Good standing | "The Rho checking account must remain **open and in good standing** throughout the 60-day period **and at the time we apply any earned reward**" |
| Eligibility | "This offer is available to **both new and existing** Rho customers." "A qualifying business, **including all subsidiaries, affiliates, and related entities**, may earn multiple rewards" |
| Substitution right | "Rho reserves the exclusive right to **substitute or change** the offer rewards for a reward of **equal or higher value**." |
| Clawback | "Rho reserves the right to **rescind or demand repayment**… **including reclaiming the reimbursed incorporation fee**, if it determines, **in its sole discretion**, that the customer has engaged in fraudulent, deceptive, or suspicious activity" |
| Tax | "You are solely responsible for any federal, state, or local tax payments, reporting, or other tax consequences." |
| Combinability | "cannot be combined with any other offer unless stated otherwise by that other offer's terms, and cannot be reproduced, purchased, sold, transferred, or traded. **Void where prohibited.**" |
| Revocation | "This offer may be **changed or discontinued at any time without notice**." |

Note the payout-clock ambiguity: the qualifying period runs "for sixty (60) days **after the incorporation**," but the credit lands 30 days after "the first sixty (60) days of **the opening of your Rho checking account**." If incorporation and account opening are not simultaneous (and per §5 they need not be, since the account can open pre-EIN), the two clocks diverge and the terms do not say which controls.

### 6.4 Ongoing costs after year one

`/product/incorporation`, "How the fee works": "Registered agent service is included for your first year with Rho Incorporation; **platform access after year one is $1,000 annually** and **contract services run $100 or $250 per contract**. **Delaware franchise taxes apply separately** and on an ongoing basis."

This $1,000/year figure is a notable outlier: it sits inside a paragraph on a page whose headline promise is "no subscription fees," and it appears nowhere on `/pricing`, which lists "Subscription Fees $0." What "platform access" and "contract services" mean here is never defined; it appears to describe a legal-document platform (the registered-agent/formation stack) rather than Rho banking, but the page does not say so.

### 6.5 Liability disclaimer

"Rho Incorporation is **not a law firm or accounting firm** and does not provide legal, tax, or accounting advice. Rho is **not responsible or liable for any errors, omissions, or mistakes** made by Rho Incorporation or in any materials, filings, or documents prepared or provided through the service. **You are solely responsible for reviewing all such materials** and should have your own legal counsel… review any materials provided by Rho Incorporation before relying on them."

This sits in tension with the headline promise that "every formation document [is] reviewed and approved by a licensed attorney."

### 6.6 Rho's own competitive table (all `[Rho claim]`)

"Competitive data collected from Stripe Atlas, Clerky, and LegalZoom websites **as of 2026-09-07**, and may change."

| | Rho | Stripe Atlas | Clerky | LegalZoom |
| --- | --- | --- | --- | --- |
| Upfront price | $400, credited back with qualifying deposit | $500 one-time, includes state filing fees + year-1 registered agent | $427 to $819 one-time, includes DE filing fees + year-1 registered agent | Starts at $149 **plus filing fees, billed separately** |
| Filing speed | ~24 hours; ~80% within that window | Within two business days | 2 to 3 business days | 1 to 2 days on fastest ($349) tier; 7 to 10 days standard |
| Registered agent | Covered first year | Included year one; **$100 annually after** | Included year one; renewal price **not published** | **$249/year, auto-renews** |
| EIN handling | SS-4 prepared and submitted; IRS issues on its own timeline | "Gets your company tax ID" | Completes IRS forms and submits them | **Not published** |
| Account at formation | Rho account application in same flow, subject to approval; funds move once IRS issues EIN | Opens a **Stripe Treasury account the moment you incorporate** | Helps you apply to outside banks with pre-filled applications, **no EIN needed**; does not open an account of its own | **Not published** |

Rho's own comparison concedes Stripe Atlas opens a usable account faster (immediately vs. blocked-until-EIN) and that Clerky's pre-filled bank applications need no EIN. The "free incorporation" positioning is weaker than Stripe Atlas's flat $500 only if the $10,000/60-day condition is met.

### 6.7 The Clerky partnership (separate path)

`/clerky`:
- "Incorporate with Clerky and manage your banking with Rho – and get a **$1,600 bonus** to fuel your launch. **Pre-EIN applications supported.†**"
- "Clerky makes it easy to get startup formation done correctly, then lets you **one-click transfer your company data to Rho**"
- "Qualifying founders earn a **$1,600 bonus** after opening their Rho account—and gain access to **$600k+ in exclusive startup perks**." (Same page also says "**$1M+ perks**" — internal contradiction.)
- Clerky entity support `[Rho claim about Clerky]`: "Delaware C corporations… both regular Delaware C corporations as well as **Delaware Public Benefit C corporations**." Notable: Rho itself does not say whether it will *form* or *bank* a PBC.
- Clerky timing `[Rho claim]`: "you automatically receive **expedited processing from Delaware**… incorporation typically takes **1 to 3 business days**."
- Announcement dated "**March 10, 2025**, Updated **August 26, 2026**."
- Perk referenced elsewhere: "Clerky — Company Lifetime Package for **$794**" (`/startups` perks carousel).

The $1,600 Clerky bonus terms are marked with a dagger (†) whose footnote text is not present in the captured page.

---

## 7. KYC / KYB: what Rho actually collects

### 7.1 Documents and data

| Item | Who / when | Source |
| --- | --- | --- |
| **EIN** (or uploaded SS-4 for deposit-only) | Business | `/product/business-banking` |
| **Formation documents** (Articles of Organization (LLC) or Articles of Incorporation (corp)) | Business | `/product/business-banking` |
| **Operating agreement** | Multi-member LLCs | `/product/business-banking` |
| **Articles of incorporation and EIN number** | "Rho will also ask for details about your **company structure**" | applying-to-rho FAQs |
| **Ownership details for anyone ≥25%** | UBOs | `/product/business-banking` |
| **Government-issued photo ID** | Each owner **and signer** | `/product/business-banking` |
| **Social Security number** | Individual applicants | applying-to-rho FAQs |
| **Banking + accounting data** (6 months of statements if aggregation unsupported) | For credit; also for identity/legal obligations | applying-to-rho FAQs |
| **Business license, certificate of good standing, beneficial ownership and authorization forms** | Named for **Treasury** applications | `/help-center/treasury` |
| **SSN / TIN / Passport / EIN** | Named for **Treasury** applications | `/help-center/treasury` |

Credit specifically: "In order to provide credit, Rho needs **bank and accounting statements for all active business accounts**."

### 7.2 Data aggregation vendors

Named: **Plaid**, **Finicity**, **Codat** (applying-to-rho FAQs). Elsewhere for external account linking: "All external accounts are linked using **Plaid, Mastercard Data Connect, and Stripe Financial Connections**" (`/help-center/banking/viewing-account-information`). Rho Switch uses **Plaid** or statement upload and analyzes "the last **120 days** of account activity."

Manual fallback: "If you do not see your provider, you can opt to **upload 6 months of accounting and banking statements for all your accounts** by clicking **Upload Statements Manually**."

ToS §13.2 "Account Aggregation Disclosure" grants Rho, the Sponsor Bank and third-party providers "a **limited power of attorney**… as your **true and lawful attorney-in-fact and agent**, with full power of substitution and resubstitution," to access third-party sites, retrieve information, and "**register for accounts or request loans**." Rho "may access your third-party accounts **any time**… **at any time while you have a Rho Account**." Revocable by emailing clientservice@rho.co.

### 7.3 Application mechanics

| Mechanic | Detail |
| --- | --- |
| Duration | "The application takes **less than 10 minutes**" (repeated on `/product/business-banking`, `/versus/brex`, `/versus/mercury`) |
| Save and resume | "you can **revisit your application later by re-entering the same email address**… You will then receive an email with a new link that will take you to your saved, in-progress application." |
| Collaboration | "**Invite Teammate** button at the top-right of your screen"; separately, "You can invite collaborators to help with adding a UBO… directly from those steps in the application flow." |
| Field policy | "**Most fields in the application are mandatory.** Non-mandatory fields are labeled with **(Optional)**." |
| File upload limits | **10 MB maximum** file size; zipped files must be unzipped first; supported types per section; split large PDF/CSV/DOC/XLS/XLSX |
| In-app support | in-application chat, 1 (855) 7-GETRHO, clientservice@rho.co |
| Existing-customer routing | "If you enter an email that is already used by Rho… you will be taken to the login page. On the **Business Login page**, you will see a list of **all active businesses and applications in progress**… You can also start a new application by clicking **Apply for a new business**." |

### 7.4 Verification and holds

- `/product/business-banking` step 03: "**Get verified** — Our team reviews what you've submitted and **reaches out directly if anything else is needed**."
- ToS §13.3: "Rho reserves the right to **impose limits on Transactions** and other elements of the Rho Services **at its sole discretion**… **without prior notice**. **New accounts may be subject to longer hold or review periods.**"
- Card addendum: "If you do not cooperate with our review process, your deposit or payment may be **delayed or declined**, and we reserve the right to take **any actions necessary with your account, including termination**. New accounts may be subject to longer hold or review periods."

### 7.5 What is conspicuously NOT stated about approval

**No page in the corpus states an approval SLA for the core checking account.** Every published timeline is for something else:

| Product | Stated timeline |
| --- | --- |
| Delaware state filing | ~24 hours, ~80% of filings |
| **Rho checking account approval** | **Never stated** |
| Rho Treasury | "approval typically takes **up to 2 business days**" / "typically takes **2 business days**" (two phrasings, same page family) |
| Rho Capital | "approved funds typically land in your Rho account within about **48 hours** of application" |
| Rho Savings | No timeline; gated on a Client Service DocuSign round trip and partner review |
| Rho Switch (migration) | "Most customers complete the full switch in **under 15 minutes**"; automated updates "about **30 seconds each**" |

Rho markets against slow approvals — "In practice, 'we'll be in touch' often means **5 to 14 business days** before a decision lands" and "a five-business-day account approval that blocks a vendor wire" (both from blog comparison posts about traditional banks) — while publishing no number of its own. The closest is "Open an account in **minutes**" (homepage), which is about *application* duration, not approval. `/product/incorporation` footnote explicitly disclaims: the 24-hour figure "**does not measure EIN issuance or account approval**."

---

## 8. Multi-entity support

| Capability | Exact wording | Source |
| --- | --- | --- |
| Apply for a second entity | "Do you have an existing account with Rho and wish to add a new one under the same login? You can submit another Application by clicking on the **Apply for a new business** button." | applying-to-rho FAQs |
| Switch entities (web) | "To view and **switch between businesses** or open a new business account, click on your business's name **at the top of the navigation bar**; a dropdown will appear." | `/help-center/general-rho-information/navigating-rho` |
| Switch entities (mobile) | Settings icon top-right → **Switch Business** at bottom of Settings menu → select from list | `/help-center/mobile-app/how-to-switch-businesses-in-the-mobile-app` |
| Positioning | "Streamline accounting and expenses **across multiple entities**" | `/solutions/enterprise` |
| Fund banking | "**every entity in one login**" | `/fund-banking` |
| Vs. Mercury `[Rho claim]` | "Multi-entity banking supported on one platform; users can switch between organizations and entities in Rho (rho.co, **as of 08/17/2026**)." | `/versus/mercury` |
| Customer proof | Best Bay Logistics: "**2 Businesses** Managed with Rho's multi-entity support"; Willet + Cumro Innovations: "**10 Brands** Businesses managed with Rho's multi-entity support" | customer pages |

**Cross-entity liability (ToS §17 "Cross Guaranty")** — the most consequential and least-marketed multi-entity fact:

> "You **absolutely, unconditionally and irrevocably guarantee, as primary obligor and not merely as surety**, the full and punctual payment and performance of all present and future obligations… required to be observed and performed or paid or reimbursed by you and/or **any of your Rho Accounts that is a subsidiary or parent entity that, directly or indirectly, owns you** (each an '**Affiliate**')…"

Scope of the Affiliate Guaranty: "all obligations related to your or any Affiliate's use of the Platform and the Rho Services, **any Rho Account, Treasury Management Account or Credit Account**, Transactions initiated by you, a User or any Affiliate and Charges arising therefrom, all indemnity or reimbursement obligations… and all fees, penalties or similar amounts… plus all costs, expenses and fees (including the reasonable and documented fees and expenses of Rho's counsel)."

The guaranty is "**irrevocable, continuing, absolute and unconditional**" and survives (a) illegality or unenforceability of the underlying obligation, (b) changes to payment terms, (c) release or impairment of collateral, (d) default or delay, (e) "**any change, restructuring or termination of the corporate structure, ownership or existence** of you or any Affiliate or **any insolvency, bankruptcy, reorganization** or other similar proceeding," and (f) Rho's failure to disclose information about the Affiliate's financial condition (customer waives Rho's duty to disclose). Customer waives subrogation, contribution, reimbursement and indemnification "until all Guaranteed Obligations shall have been indefeasibly paid and discharged in full."

**Practical effect:** a holdco/opco structure banking multiple entities at Rho cross-collateralizes them. This is never mentioned on `/solutions/enterprise`, `/fund-banking`, or in the multi-entity customer case studies.

The incorporation offer terms use the same lens in the customer's favor: "A qualifying business, **including all subsidiaries, affiliates, and related entities**, may earn multiple rewards."

**Not stated anywhere:** whether one login can hold an unlimited number of entities, whether roles and permissions are per-entity or global, whether consolidated cross-entity reporting exists, whether intercompany transfers between two Rho-held entities are supported (ToS Prohibited Activity #31 bars "transfer funds between bank accounts held in the same name," which cuts the other way), or whether the API can span entities (API Access Tokens are explicitly "**scoped to a single business**").

---

## 9. Account structure

### 9.1 Account types (API enum: the authoritative list)

`/docs/v1/accounts` and `/api/v1/openapi/accounts` (ListAccounts). `account_type` enum: **`checking`, `credit`, `investment`, `savings`, `rewards`**.

| Type | Docs description |
| --- | --- |
| `checking` | "Operating cash accounts used for everyday inflows and outflows." |
| `savings` | "Higher-yield depository accounts segregated from operating cash." |
| `credit` | "Revolving credit lines backing corporate cards." |
| `investment` | "Treasury sleeves invested in money-market funds or short-duration securities." |
| `rewards` | "Cash-back balances earned on card spend." |

"Account `account_type` is **immutable** for the lifetime of an account." Balances are returned in **minor units** (integers) with an ISO 4217 currency code. "The list endpoint has **no server-side type filter**" — filter client-side. Page size max **100**.

Account fields exposed: `id`, `account_type`, `balance.amount`, `balance.currency`, `account_number_last_4`, `routing_number_last_4`, `account_name`.

**Not in the enum:** DACA/clearing accounts (which the permission model does expose as a distinct thing), and virtual account numbers.

### 9.2 Sub-accounts (multiple operating accounts)

`/help-center/banking/how-to-set-up-multiple-operating-accounts`:
- "Rho clients can create **multiple operating accounts for a single business entity** to better organize their operating cash."
- "All businesses get access to a **primary Rho Checking Account**. You can easily create additional **sub-accounts** to organize cash for purposes like **payroll or taxes**."
- Flow: Banking tab → **"Create Account"** top right → name → create.
- **FDIC: "Each Rho customer gets up to $250,000 in FDIC deposit insurance coverage across ALL Rho checking accounts."** Sub-accounts do not multiply coverage.

**No stated cap on the number of sub-accounts.** `/fund-banking` markets "multiple fee-free operating accounts."

### 9.3 Virtual Account Numbers (VANs)

`/help-center/banking/how-to-find-your-routing-or-account-number`:
- "Virtual Account Numbers are now available directly within the **mobile app** (**excluding DACA accounts**). You can find your VANs in the **Account Details drawer**, alongside your standard account and routing numbers."
- "**Credit-only**: VANs can only be used to **receive** funds — they **cannot** be used to initiate payments or withdraw funds"
- "**Fraud protection**: Using VANs helps reduce fraud risk by allowing you to share unique receiving details instead of your primary…"
- Invoicing tie-in (changelog, **March 25, 2026**): "**Activate a virtual account number to minimize risk from unauthorized debits.** When the payment arrives in your Rho account, it maps to the right invoice without manual reconciliation."

**Not stated:** how many VANs per account, whether they can be issued per-customer or per-invoice programmatically, or whether they appear in the API.

### 9.4 DACA (Deposit Account Control Agreement) accounts

`/help-center/banking/does-rho-support-daca-accounts`:
- "Rho, in partnership with Webster Bank, a division of Santander Bank, N.A., is pleased to offer DACA accounts."
- "**Springing DACAs**: Rho currently offers **only** Springing DACAs. This type of DACA activates under certain conditions, allowing the lender to take control of the account."
- "**Fully-Blocked DACAs**: Rho **does not support** fully-blocked DACA at this time."
- Setup is manual: "reach out to our client service team via email."
- Permission model treats DACA as first-class: `View clearing account` = "User can view **DACA accounts**"; `Create DACA account transfers` = "User can create new banking transfers **from the DACA account**."
- VANs are explicitly excluded from DACA accounts.

### 9.5 Savings

`/help-center/banking/understanding-rho-savings-accounts`:
- Opening is **not self-serve**: Savings tab → **Request Access** → "A member of the **Rho Client Service team** will prepare and send you a **DocuSign agreement**" → sign → "your agreement is submitted to **our partner for review** and your account will be opened."
- "Depending on your answers to the **due diligence questions**, our partner may request **additional information** before your account is opened. Our team will handle this on your behalf."
- Funding is one-way-in: "Transfers into your Rho Savings account can **only** be initiated from a Rho Checking account."
- Settlement: Checking → Savings "typically settles the **same business day**, if created **before 1pm ET**"; Savings → Checking "typically settles the **next business day**, if created before 1pm ET."
- **Transfers out are limited to six (6) per month** (restated on the account-closure page with an as-of date: "**as of 08/02/2026**"). No limit on transfers in.
- Interest accrues daily, paid monthly.
- FDIC: "Up to **$75 million** in FDIC insurance coverage" via ADM and "a network of **400+** FDIC- and NCUA-insured institutions, as of **August 2026**… **not a contractual guarantee**."

### 9.6 Treasury

Eligibility (`/help-center/treasury/about-rho-treasury`), four hard gates:
1. Be a **U.S.-registered business**
2. **Operate primarily in the United States**
3. Have **at least one founder based in the United States**
4. Maintain **at least $50,000 in total deposits**

Note gate 3 says "**founder**," not owner or officer — a different and narrower term than the banking eligibility page uses, and one that would be meaningless for an acquired or long-established company.

Application: "**less than 10 minutes**"; "approval typically takes **2 business days**" (elsewhere on the same page family: "**up to** 2 business days"). "If you don't see the Treasury page but believe you're eligible, contact our Client Services team" — implying Treasury visibility is server-gated.

Assets (max **4 held simultaneously**): IJTXX (JPMorgan U.S. Treasury Plus MMF, fixed $1.00 NAV, no minimum, swept daily), **13-week T-Bills** (purchased in **$1,000 increments**), MULSX (Morgan Stanley Ultra-Short Income, not a MMF, variable NAV), VFSUX (Vanguard Short-Term Investment-Grade, highest yield, meaningful NAV variability). Allocations in **5% increments**, must total 100%. **Vanguard capped at 50%** of portfolio (VFSTX + VFSUX combined); existing allocations above 50% grandfathered but must be reduced before any portfolio change "unless we have approved a higher limit for your account."

Presets: Maximum liquidity (100% IJTXX, same-day); Capital preservation (50/50 IJTXX/T-Bills, 3mo); Balanced income (40% IJTXX / 60% MULSX, 4-12mo); Optimized yield (15% IJTXX / 60% MULSX / 25% VFSUX, 12+mo); Custom.

Fee: "annualized management fee of **0.15%–0.60%** based on **AUM**, billed monthly. **AUM includes the combined balance of your Rho Checking and Treasury accounts.**" Elsewhere stated as "0.15% for deposits of $20M or more to 0.6% (the maximum annual fee) for deposits under $2M." Fee is deducted from portfolio cash; "if insufficient cash is available, **Rho will automatically sell a small amount of holdings** to cover it."

Note the AUM definition is unusually customer-adverse: Rho charges an investment-advisory fee on a base that includes **checking** balances not under management.

Custody: "Securities are held **directly in your business's name** and are **not pooled** with other clients' assets."

Movement control: "Funds can only be transferred to and from your Rho Checking account by **individuals you have authorized in your Rho account settings**, or through **auto-transfer rules**."

Accountant access: "You can set your accountant up with **read-only** access to your Treasury account. They will be able to view your **monthly statements, trade confirmations, and tax documents**."

Closure: "Closing requires **liquidating all holdings**, which typically takes **2-3 business days**."

### 9.7 Credit / cards

- Two card programs: **Rho Card with Daily Terms** (spending backed by available Checking balance) and **Rho Card with Monthly Terms** (spending backed by an overall account credit limit).
- Monthly Terms qualification (`/faq`): "**Daily Terms is the default; Monthly Terms requires $25,000 held at Rho, or $75,000 combined across Rho and linked external accounts, subject to underwriting approval.**"
- A conflicting threshold appears on `/product/corporate-cards`: "New or lower-balance customers start on daily repayment; **accounts can switch to 30-day terms once balances reach $15,000**." **$25,000 vs $15,000 — unresolved contradiction.**
- Card eligibility: "A startup needs to be **incorporated in the US with an EIN** to apply." "No personal guarantee and no personal credit check."
- Card expiry: "By default, all Rho cards **expire 3 years from the issue date**."
- Merchant controls: "limit a card's acceptance to a group of **up to 20 distinct merchants**"; MCC-level category controls set by Mastercard.
- Card network: "Mastercard **World Elite Business**" (`/faq`).

### 9.8 Rewards account

`/help-center/banking/rewards-account-overview`: dedicated Rewards Account in the Banking tab, showing available rewards balance, cashback rate, rewards redeemed. Monthly Terms cashback deposits "typically **6 business days following full repayment of the statement balance**"; Daily Terms "typically on the **6th business day of the month**, for card spend during the preceding month." Redemption: transfer from Rewards Account to Primary Operating Account, "deposited **instantly**." "Rewards are earned **only on settled transactions**." "**Late payments do not earn rewards** for transactions during that statement period."

### 9.9 Departments (soft budgets, not accounts)

`/help-center/departments/understanding-the-departments-tab`. Departments are reporting/budget constructs, explicitly **not** funded sub-accounts:
- "Do these departments need to be fully funded? **No.** Creating a department is just like creating a spending budget… **unlike a card limit, you CAN go over a Department budget.** …these are **soft limits**, just for tracking, **not meant to inhibit spending**."
- Attributes per department: color label, name, number of users, budget, period spending, **reset cadence** (e.g. monthly), remaining spend %.
- Cards, vendors, users and transactions can all be assigned to a department; transactions can be **split** across departments.

---

## 10. User roles and the permission model

### 10.1 Default roles

`/help-center/admin/how-to-manage-users-and-roles-in-rho` says "Rho has **six** pre-set user roles… These are **Account Owner, Administrator, Department Owner, Employee, Bookkeeper, and Investor**" — and then the table immediately below lists **nine**. The page was evidently updated without fixing the count. **Flag this: "six" is stale; nine roles ship.**

| Role | Description (verbatim highlights) | Editable? |
| --- | --- | --- |
| **Account Owner** | "the owner of the account at Rho, typically the **CEO or CFO**… full access… creating and using Team Cards, creating wires/ACHs, viewing account balances, creating and viewing Departments, **accepting legal agreements**, and adding new Team Members." | **Not editable** |
| **Administrator** | "individuals who require comprehensive access and control… often assigned to a member of the company's executive or leadership team, such as the **Director of Finance or CFO**." Same powers as Account Owner including accepting legal agreements. | **Not editable** |
| **Department Owner** | "the manager of a team of employees but not an Administrator… view and manage Departments that they are added to, and any team cards that are also added to that Departments. **Department Owners can not create bills.**" | Editable |
| **Employee** | "limited permissions. They are **unable to view account balances or Vendor history**." | Editable |
| **Bookkeeper** | Description is **verbatim identical to Employee** ("limited permissions… unable to view account balances or Vendor history"). | Editable |
| **Investor** | "investors who need to review account finances directly. This role is predominantly '**view only**', however, **investors CAN create transactions in the banking tab**." | Editable |
| **AP & Expense Manager** | "AP Specialist or Finance Operations Manager… view all transactions across the organization, approve or reject spend requests when assigned as an approver, and create and pay bills. **Does NOT have the ability to configure expense policies or set up approval rules.**" | Not stated |
| **External Admin** | "external parties who require full administrative access… such as a **fractional CFO or an outsourced finance team**. **super-user level access**, including the ability to make payments, issue cards, and configure the account's expense policies, approval workflows, accounting rules, and business settings. They can also **invite new users**. Mirrors Administrator but for trusted external collaborators." | Not stated |
| **External Accountant** | "third-party bookkeeper or accounting firm… view transaction and bill data, add attributes to transactions, configure and sync data to connected direct integrations, or generate **bank feed tokens**. **Read-focused with limited action permissions.**" | Not stated |

Two oddities worth flagging: (a) the **Investor** role is billed as "view only" but can **create banking transactions** — an unusual default; (b) **Bookkeeper** and **Employee** carry identical published descriptions, so the distinction is undocumented.

### 10.2 Role management operations

- **Create Role**: Users → Roles → "Create Role" top right. "In the Permissions section, **all permissions will be set to Off status as default**."
- **Duplicate**: three-dot menu → "Duplicate Group." Available for all roles **except Account Owner and Administrator**.
- **Delete**: "once a Group is deleted, **it cannot be restored**."
- **Edit defaults**: "further customizations may be made to the **Department Owner, Employee, Bookkeeper, or Investor** groups. Note that the **Account Owner or Administrator is not editable**." (Silent on the three newer roles.)
- Search for and directly add/remove users from groups in the Roles tab.

### 10.3 User management operations

Add user fields: **First Name, Last Name, Email Address, Phone Number, User Roles, Monthly User Spending Limit**.
- "**Phone number is not required** when adding a new user. However, users must have a phone number on file to **activate cards under their name**, as well as for the **mandatory 2FA**."
- Bulk: "**Add from CSV**" with a Rho-provided template.
- Delete: "deletions are **permanent and irreversible**." "**Removing a user automatically cancels any cards issued to them.** This includes both physical and virtual cards."
- Password reset by admin: Users tab → select member → **Reset Password** → Continue. (The mobile app "**does not support the password-reset flow**"; resets must complete at app.rho.co.)
- Phone number changes must go through **clientservice@rho.co**; users cannot self-serve.

Monthly user limits are deprecated: "**Monthly user limits are a legacy feature that's no longer enabled by default.** Monthly user limits are **no longer part of Rho's standard offering.** If you don't see the Request New User Limit option, your account likely uses **just card limits** instead." Critically: "Card spending is based on the **available balance** in your Rho Checking account [Daily Terms] / your **overall account credit limit** [Monthly Terms]. …**Changing a user or card limit does not increase your available balance**."

### 10.4 The permission catalogue

`/help-center/admin/user-permissions-glossary`. "These permissions can be customized for user groups, **except for Account Owner or Administrator user groups**." Grouped into nine sections. The glossary contains visible duplicate/legacy pairs (e.g. `View team cards` vs `View cards`, `Manage team cards` vs `Manage cards`, `Manage attached files` vs `Manage team attached files`), suggesting a renaming migration mid-flight.

**Credit** (1): `Request credit terms change`.

**Cards, personal** (10): `View own cards`; `View own card transactions`; `Code Accounting Attributes`; `Manage own cards` (view settings only); `Manage own card permissions` (edit Nickname, Department, Limit, Receipt Upload Notifications, Selected Merchants/Categories, Card Usage Dates); `Issue own physical cards`; `Issue own virtual cards`; `Lock own cards`; `Unlock own cards`; `Delete own cards`; `Share Card Details` (share virtual card details to any email address).

**Cards, team** (17): `View team cards` / `View cards`; `Manage team cards` (edit) / `Manage cards` (see but not edit); `Manage team card permissions` / `Manage card permissions`; `Issue team physical cards` / `Issue physical cards`; `Issue team virtual cards` / `Issue virtual cards`; `Lock team cards` / `Lock cards`; `Unlock team card` / `Unlock cards`; `Delete team cards` / `Delete cards`; `View team card transactions` / `View card transactions`; `Manage automatic credit repayment settings` (**requires "Manage Security Settings" on first** — an explicit permission dependency).

**Banking, personal** (3): `View own transactions`; `Manage own attached files`; `Manage own user notes`.

**Banking, team** (5): `View team transactions`; `Manage attached files` / `Manage team attached files`; `Manage user notes` / `Manage team user notes`.

**Transfers and Accounts** (11): `Create transfers`; `Manage recurring transfers` / `Manage team recurring transfers`; `Update transfer` / `Update team transfer` (labels, departments); `Delete transfers` (cancel scheduled); `Redeem rewards`; `Manage multiline transactions` (split transactions); `View accounts`; **`View clearing account` (= DACA accounts)**; `Manage accounts`; **`Create DACA account transfers`**.

**Expense management** (10): `Can view expenses`; `Can view department expenses`; `Can approve department expenses`; `Can approve expenses`; `Can reject expenses`; `Can reject department expenses`; **`Can be approver`** (eligibility to be selected as an approver; the hook the approval engine uses); `Can Edit Expense Policy`; `Can configure expenses`; `Can Disburse Reimbursements`.

**Rho Treasury** (2): `View treasury` (overview, balances, positions, activity, transfers, linked accounts, statements — "**parent permission** to Manage treasury"); `Manage treasury` (transfers, linked accounts).

**Vendors** (6): `Create Vendors` ("does **not** control the user's ability to add a payment type"); `Manage Vendors` (add/edit payment types); `Delete Vendors`; `View Vendors` (addresses and payment types ACH/Wire/Check); **`View Full Vendor Routing and Account Number`** ("account and routing number will be **masked** if this permission is not enabled"); `View Vendor Payment history`.

**Departments** (12): `View own departments`; `View team departments`; `View departments balances`; `Download CSV data`; `Download team CSV data`; `Manage labels`; `Create departments`; `Update departments`; `Delete departments`; `View attributes`; `Manage attributes` (create new types, add/remove to cards); `Manage attribute values` (CRUD on values for any custom attribute type).

**Bill Pay** (5): `View Accounts Payable report` ($ outstanding, open bills, approvals needed, scheduled payments, recently paid); `View bills`; `Manage bills`; `View Bulk Payments`; `Create Bulk Payments`.

**Security** (13): `View department users`; `View organization settings`; `Manage security settings`; `Authorize integrations`; `View integrations`; `Manage users`; `View user groups`; `Update user groups`; `Manage groups and permissions`; `Manage external banking connections`; **`Accept deposit agreement`**; **`Accept check deposit terms of service`**; `Can upload company documents` (bank statements, financials, other documents).

Roughly **95 distinct named permissions** across 9 sections.

### 10.5 Hard-coded role gates (not permission-driven)

Certain capabilities are bound to Account Owner / Admin and are **not** exposed as toggles:

| Capability | Gate | Source |
| --- | --- | --- |
| Enable Google SSO | "Admins and Account Owners" | managing-google-sso |
| Require 2FA on every login | "Admins" (Settings → Security) | set-up-2-factor-authentication |
| Manage ACH debit authorizations | "**Only Account Owners and Admins**… **Other users cannot see or change these settings.**" | manage-your-ach-debit-approvals |
| Create/manage API Access Tokens | "**only Account Owners and Admins**" + 2FA challenge at creation | `/docs/v1/auth` |
| Initiate OAuth consent for partner apps | "**Only Account Owners and Admins** can perform this action" | `/docs/v1/partner-auth`, AI-tools help page |
| Accept legal agreements on behalf of client | Account Owner and Administrator "**default ability**" | how-to-manage-users-and-roles |
| Request account closure | "Closure must be requested by the **Account Owner**." | how-to-close-your-rho-account |
| HRIS integration setup | "must have **administrator permissions both in Rho and in your HRIS system**" | how-to-use-rhos-hris-integrations |
| Assign direct managers | Users tab → "Assign Managers" (admin-level implied) | how-to-set-up-direct-manager-approvals |

ToS §6 puts the burden squarely on the customer: "You acknowledge that **limitations on such access can only be controlled by you and an Admin User, not Rho**." And: "Rho will **not have any responsibility to verify any transaction** in your Rho Account initiated by any User, and **you may be liable for any loss**… including anyone else using credentials to access your Rho Account, **whether authorized or not**."

Also: "**No more than one individual shall gain access to a User account at any given time**" — shared logins are contractually barred.

---

## 11. Approval chains

Three independent approval engines, all threshold-based on dollar amount, all configured under Settings.

### 11.1 Payment approvals (banking transfers)

`Settings → Payment Security → Payment Approvals` (also reachable as Settings → Security → Payment Approvals).

- "designate specific Team Members to authorize payments, define **how many members need to approve** a transaction before it goes out, and specify **transaction amounts that require approval**."
- Set an **Approval Threshold**; "any transaction initiated over the specified amount will require approval. **Approvals are based on dollar amounts.**"
- "select the **number of users** who need to approve a transfer before it's sent, and designate which users are **Approvers**."
- Worked example: "require **one approver for all transactions over $50**, and **two approvers for all transactions over $100**."
- "the Designated Approvers will receive **emails** to approve each transaction prior to the release of funds."
- Settings surface shows "the transfer threshold amount, the number of approvers required for transfers that exceed the threshold, and the designated approvers."

### 11.2 Bill Pay approvals

`Settings → Security → Payment Approvals → Change`.

- Master toggle: "**Require approval for all outgoing bank payments**" → On, then **+ Add Rule**.
- Rule logic verbatim: "**For X amount or above, X number of approvals are required.**"
- Worked example: "if you set your minimum amount as **$50** and your number of approvals at **2**, then any transfer of fifty dollars or more must receive **two approvals from two separate people** designated in the Approver list before the outgoing payment can be sent."
- Constraint: "**only users who are part of your organization can be added as approvers**." Invite via **Invite User**.
- "You can create **multiple rules**."

### 11.3 Expense approvals

`Settings → Expense Settings → Expense Approvals`.

- "While the **Rules Builder** determines **what additional information is required** for a given expense, **approvals are set by dollar amount**."
- Auto-approve band supported ("such as $100 and below").
- **Tiered escalation**, verbatim worked example:
  - "All spending **under $10** will be **auto-approved**"
  - "For transactions **over $10**, a user in the **first tier** of approvers must approve"
  - "For transactions **over $500**, **both** a user in the first tier **and** the second tier must approve" (the direct-manager article gives the same example with **$1,000** instead of $500 — **inconsistent worked examples across two pages**)
  - "All transactions **greater than $10,000** require **three tiers** of approval"
- **Immutability trap:** "**Once you create an approval tier, you won't be able to change the amount.** To make changes, you can create a new tier and delete the old one."

### 11.4 Direct manager approvals

`/help-center/expenses/how-to-set-up-direct-manager-approvals`:
- "automatically route employee expenses **up the direct manager approval chain**, which can be assigned **both in Rho and via your HRIS integration**."
- Assignment: Users tab → **Assign Managers** button; manual or by importing org structure from HRIS. "After importing, any **errors will be flagged**. Correct these errors in the file and re-upload."
- "**Direct managers can be assigned solo to a tier or combined with a static user.** When **multiple approvers are in a tier, any ONE of them can approve or reject.**" (OR-logic within a tier; AND-logic across tiers.)

### 11.5 ACH debit authorization (beta): an inbound approval chain

`/help-center/banking/manage-your-ach-debit-approvals-in-rho-beta-`:
- Status: "**currently in beta**. If you don't see this feature… **contact Rho Client Services to request it**."
- Gate: **Account Owners and Admins only**; "Other users cannot see or change these settings." Found under **Banking → All Accounts → Authorizations** tab.
- "Adding, editing, or removing an authorization, and changing your default rule, is **gated behind multi-factor authentication (MFA)**."
- Matching is by **ACH Company ID**, not name: "It can contain letters and numbers, for example **SHOPIFYPMT**. Rho matches debits by Company ID **rather than counterparty name, because it is the most reliable identifier**."

| Incoming ACH debit | Rho action |
| --- | --- |
| Counterparty authorized for this account **and** amount within limit | Allows the debit |
| Counterparty not on your list | Flags the debit |
| Counterparty on list but not authorized for **this** account | Flags the debit |
| Amount over the counterparty's limit | Flags the debit |

- Hold window: "Rho **holds the debit for 8 hours** and notifies Account Owners and Admins. …If **no one approves or rejects it within 8 hours**, Rho applies your **default action** for flagged debits."
- Surfaces in three places: home page notification, warning banner on All Accounts with "Go to approvals" link, and the Approvals page ("Approvals needed" tile).

### 11.6 Approvals on mobile

The mobile **Approvals tab** has a **Banking** section for transfers ("approve or reject each of these transfers. If you reject a transfer, you can **add a note to the rejection** for the requester"), an expenses flow (filter "**Needs My Approval**"; reject requires "a reason, which will be shared with the expense submitter"), and AP bill review. Changelog (June 30, 2026) added a "'**Needs My Approval**' tile" on the Company Expenses page and scheduled payment dates on the Approvals screen.

---

## 12. Authentication and SSO

### 12.1 2FA

- "Rho uses two-factor authentication **every time you log in**, send a transaction or create a new Rho card!" / "Rho **requires 2FA every time you log in**."
- Methods: **Google Authenticator** (recommended), **Authy** (recommended), **SMS** ("**This is the least secure method**; using an app is highly encouraged").
- Method switching requires verifying with the existing method first.
- Phone number on file is required for 2FA and for card activation; **phone number changes must go through clientservice@rho.co**.
- Admin policy toggles (`Settings → Two-Factor Authentication`, within Security). "2FA Policies" section can require 2FA:
  - **For all transactions**
  - **For issuing cards**
  - **For physical cards activation**
- Org-wide: "**Require two-factor authentication on every login** — even on **trusted devices**. …this **overrides your trusted device settings**."
- Meta-protection: "changing the **2FA Policy settings now requires two-factor authentication**."
- Granularity: "Each setting in the Security panel includes its own toggle."

### 12.2 SSO

- **Google SSO only.** No SAML, no Okta, no Entra/Azure AD, no SCIM anywhere in the corpus.
- "Admins and Account Owners are now able to turn on **Google Single Sign-On (SSO)** for their organization. When Google SSO is enabled, **users within your email domain** can log into Rho using their Google accounts, rather than a password."
- Path: `Settings → Manage Single Sign-On → Enforce single sign-on → **Require Google SSO**` → Continue → Google account picker.
- Post-activation UX: "you **no longer need to input your email upfront** and can immediately select the '**Sign in with Google**' option."
- Failure mode: "If a user selects SSO but the organization hasn't enabled it, a clear warning message will inform that SSO is not available for the organization."
- Settings surface lists "**SSO** - Configure single sign-on settings for your account" under the Security section.

The button is labeled "**Require** Google SSO" / "**Enforce** single sign-on," implying it can be mandatory, but no page states whether password login is disabled for all users once enabled, or whether break-glass accounts are supported.

### 12.3 Other security surface

- **1Password integration**: `/help-center/general-rho-information/1password-integration-overview-setup` exists in the corpus.
- Card detail sharing has an expiry: "The recipient can only access the card details **once**, and the link will **automatically expire after 72 hours** if it hasn't been opened."
- SMS notifications for suspicious transactions available.
- ToS §6: Rho "may interrupt or refuse all access and any orders made using this password **within one (1) business day** following the receipt of the notification" of a compromised credential.

### 12.4 API auth (relevant to programmatic access control)

| Control | Value |
| --- | --- |
| Token type | Opaque long-lived API Access Token, prefix **`rhobat_`** |
| Scoping | "**scoped to a single business**" |
| Who can create | **Account Owners and Admins only**, plus a **2FA challenge at creation** |
| Shown | "The raw token is **shown only once**" |
| Max tokens | "**at most 20 active tokens** at a time" per business |
| Idle expiry | "expire automatically after **45 days of inactivity**" (window starts at creation for never-used tokens) |
| Max expiration | "Required. **Maximum one year.**" |
| IP allowlist | Optional, "**Up to 100 entries per token**" |
| Scopes (all read-only) | `accounts:read`, `transactions:read`, `statements:read` |
| Partner OAuth | Authorization Code + **PKCE (S256)**, authz server `https://auth.rho.co`, audience `https://rhoapi.rho.co`; access token `expires_in: 900` (15 min); `offline_access` for refresh tokens |
| Partner onboarding | Manual email to **`api-partner-request@rho.co`** with app name, legal entity, logo, redirect URIs, scopes, privacy policy URI, ToS URI, support email; "After review, Rho registers your OAuth client" |
| Grant model | "A business can have **at most one active grant per app** — approving again updates the existing connection." |
| Consent gate | "**Only Account Owners and Admins** can perform this action." Declining or having no eligible business returns `error=access_denied` |
| Sandbox | `https://rhoapi-sandbox.rho.co/api/v1`, "**any non-empty bearer token is accepted**" |

AI tool access (`/help-center/the-rho-api/what-connected-al-tools-have-access-to-in-your-rho-account`): connected AI tools are **read-only** and explicitly **cannot** "Move money / Issue, lock, or edit cards / Add or manage users / Make changes to your Rho account." Data available: Accounts (details, types, balances), Transactions (card, ACH, wire, refunds), Statements. "Write access and webhooks are next" (changelog, **August 3, 2026**).

---

## 13. Mobile app

Install: App Store and Google Play, via QR code or direct links (`/help-center/mobile-app/how-to-install-the-rho-mobile-app`). Login at the app or app.rho.co. **14 mobile help articles** in the corpus.

### What the mobile app CAN do

| Capability | Detail |
| --- | --- |
| **Switch businesses** | Settings icon (top right) → Switch Business → pick from list. Business logo/name shown below Home title, Settings title, and Account Settings as "visual cues" for the active entity. |
| **Approvals** | Approvals tab with **Banking** (transfers: approve/reject with rejection note), **Expenses** (filter "Needs My Approval"; reject requires a reason shared with submitter), and **AP Bills pending approval**. |
| **Create cards** | Full card creation; "Mobile now supports the **full range of card limit types — daily, weekly, monthly, quarterly, and annual** — in both card creation and card settings." |
| **Card management** | Lock / unlock / cancel; Overview / Details / Settings tabs; view card number, CVV, expiry, limit type and amount; copy fields for wallet entry; **team and vendor cards** now visible on mobile. |
| **Card controls** | Merchant controls (up to 20 merchants), permitted spending categories, card usage dates (start/end), international spend toggle, Rho Attributes assignment, notification channels (SMS, email, push). |
| **Share card details** | Cards → card → three dots → **Share Card** → email + optional note; recipient link opens **once**, expires after **72 hours**. |
| **Deposit a check** | `/help-center/mobile-app/how-to-deposit-a-check-in-the-mobile-app` |
| **Upload receipts** | Camera roll, live camera, or file; "in addition to desktop, **email, and SMS** uploads." |
| **Accounting attributes** | View/edit accounting details on Banking transfers, Expenses and Reimbursements; view for AP Bills pending approval; per-split Accounting sections. **Only for businesses with Accounting Integrations enabled.** |
| **Reimbursements** | "Snap a receipt, let **OCR** handle the details, and track approval status." |
| **Treasury** | "Treasury is now **fully available** in the mobile app. **Transfer In and Transfer Out** are both live." (changelog, Aug 3 2026) |
| **Routing / account numbers + VANs** | Account Details drawer; VANs available in mobile (excluding DACA accounts). |
| **Home screen** | "Total cash across all accounts, money in versus out, spend trend." |
| **Physical card shipping** | FedEx tracking links and delivery state labels on the pending card screen. |
| **Support** | In-app Help → 24/7 live support chat. |

### What the mobile app CANNOT do (explicitly stated)

| Blocked | Exact wording |
| --- | --- |
| **Password reset** | "The Rho mobile app **does not support the password-reset flow**, so set your new password at app.rho.co." |
| **Accounting sync** | "**Transaction Syncing: Sync status and transaction syncing are NOT available on Mobile.**" |
| **Mapping rules** | "Setting up Mapping Rules is **only available on the Web** via Accounting > Mapping Rules." |
| **Accounting settings** | "**Only accessible via the Web** at Accounting > Settings." |
| **Digital wallet** | "we **don't support** adding Rho cards to **WeChat**" (Apple Wallet and Google Wallet are supported). |

**Not stated anywhere:** whether the mobile app can originate wires or ACH transfers (only *approving* transfers and Treasury transfers are documented), whether user/role administration is possible on mobile (the AI-tools and ACH-authorization pages imply admin config is web-only), or whether the app supports biometric login.

---

## 14. Support model

### 14.1 The published model

`/help-center/general-rho-information/how-do-i-contact-support`, verbatim:

> "When you contact Rho support, you reach a **real human — 24/7, on every account, at no cost. No phone trees, no paywalled support tiers.**
> **Phone: 1 (855) 743-8746** — that's 1-855-7-GETRHO
> **Email: clientservice@rho.co**
> **Live chat**: log in to Rho (web or mobile app), click **Help in the lower left**, and select **24/7 live support**
> **Every channel is staffed around the clock, every day of the year.**"

| Channel | Availability | Notes |
| --- | --- | --- |
| Phone | 24/7/365 | 1 (855) 743-8746 = 1-855-7-GETRHO |
| Email | 24/7/365 | clientservice@rho.co |
| Live chat (web + mobile) | 24/7/365 | Requires login. "Live chat requires being logged in to your account, so **phone and email are the channels to use when you're locked out**." |
| **SMS / text** | Added June 30, 2026 | "**Text Rho for support.** Rho Client Services now supports **iMessage and WhatsApp**. Message us directly from your phone, **no laptop or login required**." |
| In-app help bubble | Question bubble, bottom-left | Also surfaces Help Articles, phone, email, **Leave product feedback**, **Product Guide** |

Note: **iMessage and WhatsApp are not listed on the official "How Do I Contact Support?" help page** — they appear only in the changelog and in `/versus/brex` ("phone, chat, or SMS"). The canonical support page is stale by ~2.5 months.

Response time `[Rho claim]`, repeated on landing pages and `/startups`: "**support response times under a minute**" / "**average response times under one minute**" / "dedicated support and **response times under a minute**." No page defines whether this is first-response on chat, phone pickup, or email.

### 14.2 Who gets an account manager: Rho contradicts itself

| Page | Claim |
| --- | --- |
| `/versus/amex` | "Rho provides a **dedicated human account manager to EVERY client**, while Amex reserves its highest-tier support for large corporate or premium accounts." |
| `/versus/chase` (FAQ prose) | "Rho provides a **dedicated human account manager to EVERY client**, while Chase does not include dedicated account managers." |
| `/versus/hsbc` | "Rho provides a **dedicated account manager to EVERY client at no additional cost**." |
| `/versus/chase` (comparison **table row**) | "Dedicated account manager — **Growth-stage and qualifying clients**; 24/7 human support (phone, chat, SMS) for every account, every tier" |
| `/versus/brex` (prose) | "Every client gets 24/7 human support by phone, chat, or SMS; **dedicated account management is available for growth-stage and QUALIFYING clients**." |
| `/solutions/accountants` | "Known for our unmatched service, **white-glove onboarding, and dedicated relationship managers**… **Dedicated relationship managers are on-call for you and your clients 24/7**." |
| `/lp/affiliate-banking`, `/lp/affiliate-card`, `/lp/nerdwallet-startup-cards` | Promo bullet: "**White glove support, dedicated account manager**" — but conditioned on the promo's own qualifying deposit/spend |
| `/solutions/enterprise` | "**Dedicated support**, fast onboarding, and no hidden contracts" |

**The `/versus/chase` page states both positions on the same page** — "dedicated account manager to every client" in the FAQ and "Growth-stage and qualifying clients" in the comparison table. The narrower phrasing ("growth-stage and qualifying clients") appears in the pages that carry dated competitor citations (as of 08/17/2026) and is the one to treat as operative. **"Qualifying" is never defined.**

Evidence that account managers are real and operationally load-bearing, from help-center (not marketing): "To adjust your credit agreement, please **contact your Account Manager**" (Settings → Business → Credit Information); "Contact Rho support at clientservice@rho.co **or reach out to your account manager**" (payroll setup); "Contact **your account team** or reach support 24/7" (Rho Platinum qualification).

Customer-side corroboration: "Hands down @rhobusiness, **you get your own bank guy**" (`/grow/ig`); "the **white-glove service** Dr. Squatch received in the stressful moments of **SVB's collapse**" (`/customers/dr-squatch`); "From initial onboarding to the development of our treasury strategy, we've loved the **white-glove experience** we get with Rho Prime Treasury" (`/customers/superfiliate`). Note "**Rho Prime Treasury**" is a product name that appears nowhere else in the corpus.

### 14.3 Support-dependent (non-self-serve) operations

These are the operations where Rho's support model is not a nicety but a required path:

| Operation | Why support is required |
| --- | --- |
| Open a **Savings** account | "Request Access" → Client Service prepares a **DocuSign** agreement → partner review |
| Open / close a **DACA** account | "reach out to our client service team via email" |
| Close a **Treasury** account | "Contact Rho to close Treasury" |
| **Close the Rho account** | Must be requested by the Account Owner via phone/chat/email; a "Rho specialist will confirm the request" |
| **Change a phone number** | "please email the Rho team at clientservice@rho.co" |
| **Reset a password** | Email support, or an admin does it (no self-serve reset documented) |
| Access **ACH debit authorizations** beta | "contact Rho Client Services to request it" |
| **Adjust a credit agreement** | "contact your Account Manager" |
| **Treasury tab not visible** | "contact our Client Services team" |
| Add an **international vendor** during a Switch | "contact Rho Client Services for assistance" |
| Move a **VFSTX position to VFSUX** early | "contact the Rho team" |
| Exceed the **50% Vanguard cap** | "unless we have approved a higher limit for your account" |
| Exceed **$1M/yr cashback** | "Talk to sales and we'll build your program" |
| **Historical statements** after closure | "Rho support can provide historical statements on request" |

### 14.4 Account closure

`/help-center/general-rho-information/how-to-close-your-rho-account`:
- Requester: **Account Owner only**.
- Pre-closure checklist: pay off Rho Card balance ("Closure **can't be processed** until any outstanding card balance is settled"); cancel scheduled and recurring payments (Banking → Scheduled Transactions); move Savings balance to Checking (subject to the **six-per-month** withdrawal cap, "as of **08/02/2026**"); liquidate Treasury ("**2–3 business days**"; "Assets are sold at current market prices and **may be worth less than your original investment**"); download statements (Settings → Documents → Account Statements) and export transactions to CSV **before requesting closure** because "**Your dashboard access ends when the account closes**"; save vendor W-9s and tax documents from vendor profiles.
- On closure: "**All Rho Cards on the account — physical and virtual — are canceled.** Any **remaining balance is returned by wire or check** — your Rho specialist will arrange the method."
- Timing: "**no stated SLA**"; "Closure timing can depend on pending transactions clearing — incoming deposits, outgoing payments, and card transactions must settle."

---

## 15. Product-level eligibility gates (summary table)

| Product | Gate |
| --- | --- |
| **Checking** | US-incorporated business (not sole prop), EIN or SS-4, formation docs, ≥25% owner IDs, US operating address or US owner with SSN, non-prohibited industry/country. **No minimum balance, no minimum deposit, no revenue minimum.** |
| **Sub-accounts** | Included with any account; no stated cap |
| **Savings** | Request Access → DocuSign → partner review; additional diligence possible. No minimum stated |
| **Treasury** | US-registered; operates primarily in US; **≥1 founder US-based**; **≥$50,000 total deposits**; ~2 business day approval |
| **Corporate Card (Daily Terms)** | Default. US-incorporated with EIN. No PG, no personal credit check |
| **Corporate Card (Monthly Terms)** | **$25,000 held at Rho, or $75,000 combined across Rho and linked external accounts**, subject to underwriting (`/faq`). Conflicting figure: **$15,000** (`/product/corporate-cards`) |
| **Rho Platinum** (up to 2% cashback) | All **four**: payroll runs from Rho; revenue lands in Rho Checking; **≥50% of company assets held at Rho**; an active Rho Corporate Card. 2% applies to **first $1,000,000 in eligible spend per calendar year**; standard Daily Terms rate 1.25%, Monthly Terms 1.75% Platinum / 1% standard. Requires paying full statement balance on time. Status is dynamic: "If your account no longer meets the qualifications, your Cashback rate **returns to the standard rate**." |
| **Rho Capital** | Loans by **Lead Bank**, "subject to credit approval"; "consent to obtain **personal credit report** is required"; "Subject to **minimum revenue and business requirements**" (unquantified); "**Personal Guaranty MAY be required**"; lines "up to **$5M+**"; repayment terms up to **180 days**; funding ~**48 hours**; no origination fee, no prepayment penalty |
| **Rho Incorporation** | Delaware C-corp only; ≥1 US-based owner or officer; physical US operating address; non-restricted industry/country |
| **API** | Account Owner/Admin only; token scoped to a single business; read-only scopes |
| **ACH debit authorizations** | Beta, request via Client Services; Account Owner/Admin only |
| **Google SSO** | Account Owner/Admin enables; scoped to your email domain |

Pricing floor (`/pricing`, `/help-center/general-rho-information/pricing-requirements`): "Rho has **no subscription fees, no per-user fees, and no platform fees on any account**… The only standard payment fee is **1% on foreign-currency transfers**." Fee table: Same-Day ACH / wires / checks $0; subscription $0; checking minimum $0; AP + Expense + Accounting Automation $0; per-user $0; foreign currency transfer 1%; domestic wire recall $0. Other disclosed fees: **$30 international wire recall**, **optional $15 SWIFT fee**, **1% FX conversion**, late fee "**three percent (3%) of the delinquent payment balance for each month** that the balance remains unpaid for **up to six (6) months**."

---

## 16. Contradictions, gaps and things to verify

### Contradictions inside Rho's own corpus

1. **Geographic eligibility conjunction**: help center says US-incorporated **AND (US address OR US owner with SSN)**; `/product/incorporation` says US-incorporated **AND US owner/officer AND US address**; ToS says "businesses **based in** the United States." Three different rules.
2. **Account managers**: "every client" (`/versus/amex`, `/versus/hsbc`, `/versus/chase` FAQ) vs "growth-stage and qualifying clients" (`/versus/brex`, `/versus/chase` table). The Chase page carries both.
3. **Incorporation is free / is $400**: `site-llms-full.txt` says "free… fully refunded"; `/product/incorporation` FAQ says "**Rho Incorporation costs $400**." site-llms also drops the "new money" and "above where it started" conditions.
4. **Refund threshold for accelerator founders**: "$1,000 for founders introduced through an accelerator" appears only in the help center, with no indication of which number it replaces.
5. **Refund clock**: qualifying period is "60 days **after the incorporation**"; payout is 30 days after "the first 60 days of the **opening of your Rho checking account**." Pre-EIN account opening guarantees these can diverge.
6. **Role count**: "Rho has **six** pre-set user roles" followed immediately by a table of **nine**.
7. **Bookkeeper vs Employee**: identical published descriptions.
8. **Investor role**: described as "predominantly view only" but "investors **can create transactions** in the banking tab."
9. **Monthly Terms threshold**: $25,000 at Rho / $75,000 combined (`/faq`) vs "balances reach **$15,000**" (`/product/corporate-cards`).
10. **Expense approval worked example**: second tier at **$500** on one page, **$1,000** on another, with the same $10 and $10,000 tiers around it.
11. **EIN requirement**: "**You'll need your EIN letter to join Rho**" (EIN help page) vs the entire pre-EIN onboarding proposition.
12. **Restricted-country lists**: ToS §12 wire list and the help-center payments list diverge in both directions (see §2.4). ToS bans INR wires outright while a help-center article explains INR purpose codes.
13. **Partner bank size**: "$327B-asset U.S. banking organization (per Santander, 08/20/2026)" vs "Webster Bank, a division of Santander Bank, N.A. (**$70B AUM**)" on `/clerky`.
14. **Personal guarantee posture**: "no personal guarantee" for cards vs "**Personal Guaranty may be required**" and "consent to obtain personal credit report is required" for Capital.
15. **Perks value**: `/clerky` says "$600k+ in exclusive startup perks" and "more than $1M+ perks" on the same page. `/startups` says "$1M+ in partner rewards."
16. **Subscription-free positioning** vs `/product/incorporation`'s "platform access after year one is **$1,000 annually**."
17. **Support channels**: iMessage/WhatsApp shipped June 30 2026 per changelog, absent from the canonical support page.
18. **Prohibited "real estate or motor vehicles" and "bill payment services"** in the ToS vs Rho marketing a Bill Pay product and publishing customer stories for a freight broker and consumer-goods brands.

### Conspicuously not stated

- **No approval SLA for the checking account.** Every other product has one; the core product does not.
- **No positive list of accepted entity types.** S-corp, LP, LLP, partnership, trust, PBC, holding company, series LLC, SPV, DAO: all unaddressed.
- **No decline reasons, no appeal process, no re-application rule.**
- **No cap on sub-accounts, VANs, users, or entities per login.**
- **No SAML / Okta / Entra / SCIM.** Google SSO is the only identity federation.
- **No documented audit log or access-review export** beyond a per-user "activity" view.
- **No statement of whether roles/permissions are per-entity or global** in a multi-entity login.
- **No disclosure of the Cross Guaranty (ToS §17)** on any multi-entity marketing page.
- **No stated minimum revenue, headcount, funding stage, or time-in-business** for the checking account.
- **No cash deposit support** is ever affirmatively described; `/product/business-banking` concedes online-first platforms have "limited or unavailable cash deposits."
- **No mention of whether the mobile app can originate payments** (only approve them).
- **What "qualifying" means** for a dedicated account manager.
- **What happens at day 31 / day 61** of a pre-EIN window with no EIN.
- **Whether the six-per-month Savings withdrawal cap is a Reg D artifact** or a Rho/ADM policy.

### Dated facts to carry forward

| Fact | As-of date |
| --- | --- |
| Competitive incorporation data (Stripe Atlas, Clerky, LegalZoom) | **2026-09-07** |
| Competitive checking data (Mercury, Bluevine, Chase) | **09/06/2026** |
| Brex comparison data | **08/17/2026** |
| Mercury comparison data | **08/17/2026** |
| Multi-entity capability claim (rho.co) | **08/17/2026** |
| Savings withdrawal limit of six per month | **08/02/2026** |
| $0 same-day ACH, $0 domestic wires | **08/02/2026** |
| Savings up to $75M via 400+ institution sweep | **08/02/2026** / "as of **August 2026**" |
| Incorporation refund terms | **08/02/2026** |
| Rho Capital: lines to $5M, 48-hour funding, no hard pull | **08/02/2026** |
| Treasury $50K minimum vs competitors' $250K+ | **08/04/2026** |
| Santander $327B US banking organization | **08/20/2026** |
| Treasury yield basis (90-day T-Bill) | **09/11/2026** |
| Terms of Service Version 7.0.0 | last updated **August 27, 2026** |
| Clerky partnership announcement | **March 10, 2025**, updated **August 26, 2026** |
| "Product claims current as of" (`/product/incorporation`) | **September 2026** |

---

## 17. Source index for this section

Primary:
- `pages/help/help-center__general-rho-information__business-and-industry-eligibility-at-rho.txt`
- `pages/help/help-center__general-rho-information__applying-to-rho-faqs.txt`
- `pages/help/help-center__banking__can-i-open-a-rho-account-if-i-dont-live-in-the-u-s.txt`
- `pages/help/help-center__general-rho-information__incorporating-your-company-with-rho.txt`
- `pages/help/help-center__general-rho-information__how-do-i-request-my-business-ein.txt`
- `pages/core/product__incorporation.txt`
- `pages/core/product__business-banking.txt`
- `pages/core/clerky.txt`
- `pages/core/policies__terms-of-service.txt` (§6, §12, §13, §17, §18, §29 Glossary)
- `pages/help/help-center__admin__user-permissions-glossary.txt`
- `pages/help/help-center__admin__how-to-manage-users-and-roles-in-rho.txt`
- `pages/help/help-center__admin__managing-google-sso-for-your-organization.txt`
- `pages/help/help-center__admin__set-up-2-factor-authentication.txt`
- `pages/help/help-center__admin__require-2fa-for-sending-transactions-creating-cards.txt`
- `pages/help/help-center__admin__how-to-require-approval-for-specific-transactions.txt`
- `pages/help/help-center__bill-pay__how-to-set-up-approvals-for-bill-pay.txt`
- `pages/help/help-center__expenses__how-to-set-up-approvals-for-expenses.txt`
- `pages/help/help-center__expenses__how-to-set-up-direct-manager-approvals.txt`
- `pages/help/help-center__banking__how-to-set-up-multiple-operating-accounts.txt`
- `pages/help/help-center__banking__manage-your-ach-debit-approvals-in-rho-beta-.txt`
- `pages/help/help-center__banking__does-rho-support-daca-accounts.txt`
- `pages/help/help-center__banking__understanding-rho-savings-accounts.txt`
- `pages/help/help-center__banking__how-to-find-your-routing-or-account-number.txt`
- `pages/help/help-center__banking__switch-your-business-banking-to-rho.txt`
- `pages/help/help-center__banking__viewing-account-information.txt`
- `pages/help/help-center__general-rho-information__how-do-i-contact-support.txt`
- `pages/help/help-center__general-rho-information__how-to-close-your-rho-account.txt`
- `pages/help/help-center__general-rho-information__how-to-log-in-to-rho-and-fix-login-issues.txt`
- `pages/help/help-center__general-rho-information__rho-platinum-what-it-is-and-how-to-qualify.txt`
- `pages/help/help-center__general-rho-information__pricing-requirements.txt`
- `pages/help/help-center__general-rho-information__about-rho-capital.txt`
- `pages/help/help-center__treasury__about-rho-treasury.txt`, `help-center__treasury.txt`
- `pages/help/help-center__payments__restricted-countries-and-international-payment-types.txt`
- `pages/help/help-center__mobile-app*.txt` (14 files)
- `pages/help/help-center__admin__how-to-use-rhos-hris-integrations.txt`
- `pages/help/help-center__the-rho-api__what-connected-al-tools-have-access-to-in-your-rho-account.txt`
- `docs/docs_v1_accounts.md`, `docs/docs_v1_auth.md`, `docs/docs_v1_partner-auth.md`, `api/accounts_listaccounts.md`
- `pages/core/faq.txt`, `pages/core/pricing.txt`, `pages/core/startups.txt`, `pages/core/changelog.txt`
- `pages/core/solutions__enterprise.txt`, `solutions__accountants.txt`, `fund-banking.txt`, `partners.txt`
- `pages/core/versus__brex.txt`, `versus__chase.txt`, `versus__amex.txt`, `versus__hsbc.txt`, `versus__mercury.txt`
- `site-llms-full.txt` (Rho's self-authored machine summary; self-serving, contradicts product pages on the incorporation fee)
