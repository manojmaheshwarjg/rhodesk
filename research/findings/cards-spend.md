# Rho: Cards, Spend Controls and Expense Management

Research dossier section. Compiled 2026-09-11 from the local Rho corpus (marketing pages, help center, policy pages, API docs, sandbox JSON). All facts are grounded in the corpus; `[Rho claim]` marks assertions only Rho makes, especially about competitors.

Primary sources used are listed in the final section with exact file paths.

---

## 1. Program architecture: who issues what

| Element | Fact | Source |
|---|---|---|
| Issuer | Webster Bank, a division of Santander Bank, N.A., Member FDIC | product/corporate-cards; ToS Addendum A and B |
| Program manager | Under Technologies, Inc. dba Rho Technologies ("Rho") | ToS Addendum B, cashback terms |
| Network | Mastercard, tier **World Elite Business** (also written "Mastercard World Elite for Business") | product/corporate-cards; product/expense-management footer |
| Legal card products | (a) "Rho Corporate Card with Daily Terms" (ToS Addendum A, internally also called "One-Day Corporate Card"); (b) "Rho Corporate Card with Monthly Terms", formally "**Rho Extended Corporate Credit Card**" (ToS Addendum B, "Monthly Card Agreement") | policies/terms-of-service |
| Credit vehicle | A single "Credit Account" per company, integrated with the Rho Account | ToS 1.2 Credit Account Integration |
| Corporate entity | Under Technologies, Inc. DBA Rho Technologies, 100 Crosby Street, New York, NY 10012 | footers |
| Support | 1 (855) 7-GETRHO / 1 (855) 743-8746, clientservice@rho.co, in-app chat; iMessage and WhatsApp added June 30, 2026 | help pages; changelog |

Note the naming split: ToS Addendum A calls the daily product a "Rho Corporate **Credit** Card with Daily Terms" and simultaneously states "the One-Day Corporate Card **is a charge card**". The API models the backing account as `credit` and describes it as "**Revolving** credit lines backing corporate cards" (docs/docs_v1_accounts.md), which contradicts the marketing framing of a non-revolving charge card. See §16.

---

## 2. Card types

Rho markets **three** card types but the API models only **two** form factors. Vendor cards are virtual cards with a vendor association, not a distinct API type.

| Type | Form | Where created | Distinguishing mechanics |
|---|---|---|---|
| Physical | Plastic, mailed | Cards > All Cards > + Create Card > Physical | Shipped by mail; must be activated; shipping address required; accounting-automation settings configurable |
| Virtual | Instant | Cards > All Cards > + Create Card > Virtual | Usable immediately online and via Apple Pay / Google Pay; full PAN, CVV, expiry visible in dashboard; shareable by secure link |
| Vendor | Virtual, vendor-scoped | Cards > Create Card > Vendor Card, **or** Vendors > Add Vendor > Payment Account = "Single-use vendor card", **or** bulk CSV | Tied to a vendor record (logo + name matched); appears in a dedicated **Vendor Cards** tab; defaults the *creator* as cardholder so the card survives employee churn |

API type enum (`GET /api/v1/cards`): `physical`, `virtual` only. There is no `vendor` type exposed. (api/cards_listcards.md)

Other card-type facts:
- "You may create an **unlimited** number of virtual and physical Rho cards." (help-center/cards/employee-card-faqs)
- Physical and virtual cards **cannot share** numbers, CVV codes, or expiration dates. A virtual card is never a virtual image of a physical card; it is always a separate card. (help-center/cards/how-to-create-a-new-rho-card)
- One card per person by default: "One Rho Corporate Card with Daily Terms may be issued per one person and multiple ... may not be issued to one person, **unless authorized by the Company**." (ToS 1.5)
- Cards pair only to the **Rho Primary Checking account**. "If you have sub-accounts, the spend is tied to the primary account, and this can't be changed." (help-center/cards/how-to-update-your-card-settings; understanding-the-team-cards-page)
- Digital wallet: Apple Wallet and Google Wallet supported for both virtual and physical. **WeChat is explicitly not supported.**
- No PINs. Rho tells cardholders to ask the merchant to run as credit and bypass the PIN prompt.
- **No ATM cash withdrawals, no cash advances, no cash transfers, no push-to-debit.**

### Vendor card specifics
- Single-use vendor cards created from Bill Pay are nicknamed `[Payee Name] AP Card: [Invoice Number]`, are pre-set with the payment amount, and carry a **14-day card usage window** (editable in Card Settings). Once charged successfully the card becomes invalid; status flips Active to Canceled but details stay viewable in Team Cards.
- Vendor card creation from the **Vendors** flow is restricted to single-use only; the Cards flow allows any limit type.
- Deleting the creating user prompts deletion of their vendor cards. Deleting a vendor profile **cancels all linked vendor cards**.
- "Switch subscription" on the confirmation screen auto-matches a subscription carrying the same name as the vendor card.
- Marketing claim: "Unlimited vendor cards with instant setup", "Dedicated Vendor Cards tab under Cards", "Live human support to help migrate spend". [Rho claim]

---

## 3. Charge vs credit mechanics: Daily Terms vs Monthly Terms

Every account **starts on Daily Terms**. Monthly Terms is an application, not a default.

| Dimension | Daily Terms | Monthly Terms |
|---|---|---|
| Formal agreement | ToS Addendum A, "Rho Corporate Card with Daily Terms Agreement" | ToS Addendum B, "Monthly Card Agreement" (Rho Extended Corporate Credit Card) |
| Billing cycle | **Daily Billing Cycle**; balance settled to zero at end of the same day if a business day, otherwise next business day | 30-day billing cycle with a **1-day repayment period** |
| Grace period | "**There is no grace period.**" (ToS 2.1) | Credit period of more than one day; no interest if paid in full and on time |
| Repayment trigger | Auto-debited from Rho Checking **just after midnight EST** for the prior day's settled charges | Automatic balance repayment at end of cycle from Rho Checking **or an external account** |
| Spending power source | Available balance in Rho Checking (plus risk factors) | Overall account credit limit |
| Statement cadence | A Billing Statement is emailed each day there is a transaction or payment, or if the Credit Account balance is positive/negative by more than **$1.00**, or a foreign transaction or fee posted that day. Plus a monthly summary card statement on the **5th of each month**. | Periodic Statement monthly |
| Standard cashback | 1.25% | 1% |
| Platinum cashback | up to 2% | up to 1.75% |
| Qualification | Default for all accounts | $25,000 held at Rho, **or** $75,000 combined across Rho and linked external accounts (personal accounts do not count), subject to underwriting |

Explicit worked example of the daily cycle: "Monday's charge period begins at 12:01 am EST Monday morning and lasts until midnight Monday night. The repayment for Monday's charges follows. Then Tuesday's charge period begins at 12:01 am EST on Tuesday." (help-center/cards/the-rho-card-with-daily-terms)

You can only be on **one program at a time** (product/corporate-cards guide 04).

Marketing framing of charge vs credit: "A corporate card like Rho's is a charge card: the full statement balance is paid on time each period, rather than carried at an interest rate." Rho explicitly tells revolving-credit seekers to look elsewhere: "If your team needs revolving credit you carry over time, a traditional business credit card may fit."

### Credit dashboard fields (Daily Terms)
- **Current Balance**: sum of settled card transactions minus repayments made.
- **Pending Charges**: charges initiated but not yet settled by the merchant, regardless of the day initiated. Pending charges are **subtracted from available credit** and carry over to the next spend period until settled.
- **Available credit**: what the business can spend today; affected by pending charges and the applicable daily credit limit.
- Card Repayments live under Cards > Transactions, with drawers showing credit release ETAs and reasons for delays.

### Threshold contradiction on Monthly Terms minimum
- Marketing (product/corporate-cards, faq): **$25,000 at Rho or $75,000 combined** with linked external accounts.
- Help center (the-rho-card-with-monthly-terms-2): "businesses are required to maintain a **minimum cash balance of $25,000**" with no mention of the $75,000 combined path.
- Rho vs. Mercury comparison table claims Mercury switches to 30-day terms at **$15,000** balances. [Rho claim, competitive data as of 2026-09-08]

---

## 4. Underwriting and limit setting

### What Rho says publicly
- "Underwriting reviews your business financials, not a personal credit report." (product/corporate-cards step 02)
- "The approved credit limit is personalized based on the business's financial health and other relevant factors." (Monthly Terms help)
- Daily Terms: "your company receives a **daily credit limit**. The limit is determined based on a combination of your **available checking balance** as well as **risk factors that vary by client**. As your available checking balance varies over time, this limit is **not a static limit**."
- Monthly Terms application may require **read-only access to the business's primary bank accounts**.
- To apply for credit, Rho needs **bank and accounting statements for all active business accounts**. (applying-to-rho-faqs)

### What the Terms of Service say (both Addendum A and B, near-identical language)
- "All advances or extensions of credit ... are **uncommitted**."
- Limit factors: "the industry the Company is engaged in; spending volume; the nature of the Company's business; the length of time the Company has been in business; and the Company's **revenue and cash**, amongst others."
- "At any given time, the Company shall have **one aggregate dollar spending limit**, regardless of how many Cards can access the Credit Account."
- "**At no time shall we be required to disclose the spending limit to you.**"
- "In our sole and absolute discretion, we may modify or change the spending limit at any time, at a frequency of our own choosing, **with or without providing any notice to you**. We reserve the right to **reduce your spending limit to zero dollars**."
- Ongoing monitoring: "You authorize us to access at this time, and **on a continuing basis**, the Company's accounting platform and bank information for underwriting and credit risk monitoring purposes." If no accessible accounting platform, the company must send Requested Financial Information (P&L, balance sheet, etc.) **monthly, by the 30th day of the following month**.
- "The Company's spending limit with us may, in our sole discretion, be **decreased if we do not have access to the Company's Requested Financial Information on a timely basis**." Failure to provide can expose the company to "consequential, incidental, special, or exemplary damages."
- Monthly Terms only: the limit "applies to all Billing Cycles in the aggregate", is offset by unpaid charges from the current **and prior** Billing Cycle, and "the sum of all Company's Obligations must, at all times, be less than the spending limit."
- Rho may pull funds "without providing notice to you, on any date and at any time ... when the total balance in your Rho Account, linked account(s), and/or Budget Account(s) is **less than the balance minimum required by our underwriting criteria**."

### Limits vs. spending power (repeated warning across three help pages)
"Card limits control how much a card may spend, but they **don't create spending power**. Raising a card or user limit never increases what's actually available."

### Eligibility gates
- US-incorporated entity with an EIN (or SS-4 while the EIN application is pending). LLCs, C-corps and other US-incorporated entities eligible.
- **Virtual addresses from Regus or any other provider are not permitted.**
- Prohibited/high-risk industries (business-and-industry-eligibility): betting/casino gaming chips; adult dating and escort services; drug stores, pharmacies and cannabis; drugs, proprietaries and sundries; stamp and coin stores; quasi-cash, currency, money orders, travelers checks; pawn shops; bearer shares; bail and bond payments; currency exchange businesses; nested MSBs/money transmitters; firework sales; online dating services.
- Application requires SSN of beneficial owners, formation documents, articles of incorporation, EIN; UBO at 25% ownership or, failing that, the person with substantial control. Document upload cap **10 MB**.

---

## 5. Personal-guarantee stance (and the fine print that cuts against it)

### The marketing position, stated repeatedly
- "Apply with your EIN. **No personal guarantee, no personal credit check**, no annual fee."
- "0 personal guarantees or credit checks required to apply."
- "Rho will not conduct a **hard or soft** check on your credit score when you apply for credit with Rho." (employee-card-faqs)
- "Rho does not pull any personal credit reports and does not report business card activity to personal credit reports. **We report to the credit bureaus on the entity (business) side at our discretion.**" (the-rho-card-with-monthly-terms-2)
- Every card type "carrying the same underwriting and terms: no personal guarantee and no personal credit check."

### Countervailing language in the corpus
1. **ToS §1.12 Credit Report Disclosure** (present verbatim in *both* Addendum A and Addendum B): "you and the Company understand and consent to our request for a **consumer report** as defined in the Federal Fair Credit Reporting Act ... being obtained by us from a **consumer or business credit reporting agency about the Company and each authorized user**." The disclosed report contents include "public record information, criminal records, motor vehicle operation history, education records, names and dates of previous employers, reason for termination of employment and work experience, and/or credit worthiness, capacity and standing, character, general reputation, personal characteristics, or **mode of living**." State-specific rights are spelled out for California, Minnesota, Oklahoma and New York residents, i.e. individuals, not entities. This is a signed consent to a consumer report on individuals, sitting under a product marketed as requiring no personal credit check.
2. **ToS §17 Cross Guaranty**: "You absolutely, unconditionally and irrevocably guarantee, **as primary obligor and not merely as surety**" the obligations of any Rho-account affiliate that is a subsidiary or parent entity. This is an **entity-level** cross-guaranty, not a personal one, but it is a guaranty and the daily-card agreement flags it in caps: "YOU AGREE AND UNDERSTAND THAT OBLIGATIONS UNDER THIS AGREEMENT ARE SUBJECT TO A CROSS-GUARANTEE FROM YOUR AFFILIATES."
3. **Rho Capital** (a separate product, not the card): "Application and consent to obtain **personal credit report** is required. ... **Personal Guaranty may be required.**" The same page's body copy says "Applying doesn't involve a hard pull on your personal credit." Internal contradiction on one page.
4. Set-off rights: on default Rho has "the right to set off and apply any and all deposits, against the Company's Obligations, whether such deposit account is held by Rho, **with or without providing notice to you**," and may debit "any linked account" and "Budget Accounts."

### Competitor PG claims [Rho claim, competitive data as of 2026-09-08]
| Provider | Rho's claim about PG |
|---|---|
| Brex | Not required; underwriting on business financials; card does not check or report to personal bureaus |
| Ramp | Not required; eligibility based on business financials |
| Mercury | Not required; no credit check during sign-up |
| Amex | "typically requires a personal guarantee on small-business cards" (site-llms.txt) |

---

## 6. Repayment: cadence, rails, timing, automation

| Mechanism | Detail |
|---|---|
| Daily auto-repayment | Debited from Rho Checking **just after midnight EST**, for the total of settled charges from the prior day |
| Monthly auto-repayment | Automatic debit at end of cycle from Rho Checking or an external account. Rho may debit **before** the due date if the due date falls on a US holiday or weekend |
| Manual one-time repayment | Cards > Transactions > **Pay Credit Balance** (also "Pay Card Balance"), pick Rho Checking or a linked external account |
| ACH cutoff | Repayments initiated **before 2:00 pm ET** process same day; after 2:00 pm ET process next day |
| Settlement | Card repayments "can take up to **4 business days** to settle" |
| Payment not final until | "The Rho Card payment isn't complete until after the payment settlements and the **ACH reversal window** has closed" |
| Prepayment | Allowed any time "without incurring any penalty or fee" (Monthly Card Agreement 2.1) |
| Non-Rho funding | Rho "may, but is not required to, accept payment by ACH or wire from an account that is not held at Rho" |
| If auto-debit fails | Company must remit "promptly, but in any case **within one (1) Business Day**" |
| Late fee | "**three percent (3%) of the delinquent payment balance for each month** that the balance remains unpaid for **up to six (6) months**", unless prohibited by law. Identical language in Addendum A, Addendum B, and the pricing page footnote |
| Collections | Rho may debit Rho Account, any linked account, or Budget Accounts; charges collection costs, attorneys' fees, court costs |
| Revoking ACH authorization | "A failure to maintain such automatic and recurring payment authorization constitutes a **breach**" and can result in termination or credit reduction |

### Automatic Card Payments (interim top-ups)
Configured at Settings > Credit Information > Automatic payments. Only **Account Owners and Administrators** can configure (plus custom roles with "Manage automatic credit repayment settings", which itself requires "Manage Security Settings").

| Parameter | Default | Range | Mechanic |
|---|---|---|---|
| Credit limit threshold | **95%** | 1–99% | When the card balance crosses this % of the credit limit, Rho auto-creates a payment via **ACH Pull** |
| Payment amount | **5%** | 1–99% | Calculated as a % of the **total credit limit**, not of the balance |

Worked example from the help center: credit limit $100,000, threshold 95%, payment 5%. Balance passes $95,000 → Rho pulls **$5,000** by ACH and credits it to the card balance to keep spending uninterrupted. "Automatic payments are credited to your Rho Card account when received to enable uninterrupted card spending **for accounts in good standing**."

Funding sources allowed: Rho checking account, or a linked third-party account.

---

## 7. Spend controls

All controls are **pre-authorization**: they decline transactions at the point of sale. Expense *rules* (§10) are explicitly post-spend and never decline.

### 7.1 Limit types

| UI name | API `spending_limit_type` | Reset behavior |
|---|---|---|
| No Limit | `null` (no `spending_limit`) | n/a. In the UI, entering `0` as the card limit means **no spending cap**; a warning modal appears at creation and in settings |
| Recurring – Daily | `daily` | Resets every day, Eastern Time calendar boundary |
| Recurring – Weekly | `weekly` | Resets every week, ET boundary |
| Recurring – Monthly | `monthly` | Resets **on the 1st of each month**, ET boundary |
| Recurring – Quarterly | `quarterly` | ET calendar boundary (API only; help pages list daily/weekly/monthly/annual) |
| Recurring – Annual | `annual` | Resets on the **anniversary of when the limit took effect**, not on a calendar boundary |
| Fixed | `fixed` | Lifetime ceiling that does not reset. When transactions fully settle, the card **automatically locks** |
| Single-use | `single_use` | Spent after one use. **Limit cannot be changed after creation.** No `spend_period_end` |

Notes:
- Annual, weekly and daily limits shipped **April 30, 2026**. Switching limit types on an existing card without reissuing shipped **May 27, 2026**. Mobile support for the full range (daily/weekly/monthly/quarterly/annual) shipped **June 30, 2026**. (changelog)
- `current_spend` = pending plus settled spend in the current window. `pending_spend` is the pending portion.
- "Card Limit Proactive Notifications" (notify before approaching the limit) shipped **March 25, 2026**.

### 7.2 Merchant and category controls

| Scope | Merchants | Categories | Where |
|---|---|---|---|
| Per card (allow list) | up to **20 distinct merchants** (stated "as of 08/02/2026") | Mastercard-defined merchant categories, e.g. "Advertising Services", "Airlines", "Grocery Stores", "Airlines, Air Carriers and Airports, Flying Fields" | Cards > select card > Configure Card > Spend Controls > Categories / Merchants |
| Company-wide (block list) | up to **20 specific merchants** | **unlimited** number of categories | Settings > Security > Card Restrictions > Change |
| Network/legal (always blocked) | see restricted MCC list below | | Not user-configurable |

API exposes both directions and states the invariant: "Merchant controls use **either** the `blocked_*` fields **or** the `allowed_*` fields, **never both**." Categories carry an **ISO 18245 MCC** plus a human-readable name; merchants are identified by human-readable name only. Sandbox examples: `blocked_categories: [{code:"0742", name:"Veterinary services"}]`, `blocked_merchants: [{name:"Petco"}]`, `allowed_categories: [{code:"5812", name:"Eating places and restaurants"}]`, `allowed_merchants: [{name:"Sweetgreen"}]`.

Always-restricted merchant categories (employee-card-faqs): betting/casino gaming chips; adult dating and/or escort services; cannabis/paraphernalia; stamp and coin stores; quasi-cash, currency, money orders, travelers' checks; pawnshops; jewelry, precious stones, precious metals, diamonds; bail and bond payments. Plus merchants located in Rho's restricted territories/countries.

ToS restricted-country list for card use (Addendum A §1.10): Afghanistan, Albania, Angola, Belarus, Bosnia and Herzegovina, Burundi, Central African Republic, Chad, Congo, DRC, Cuba, Egypt, Equatorial Guinea, Eritrea, Ethiopia, Guinea, Guinea-Bissau, Haiti, Iran, Iraq, DPRK, Kosovo, Laos, Lebanon, Libya, Mali, Mauritania, Montenegro, Myanmar, Nicaragua, Niger, Nigeria, North Macedonia, Pakistan, State of Palestine, Russian Federation, Somalia, South Sudan, Sudan, Syria, Ukraine, Venezuela, Yemen, Zimbabwe, plus anything newly US-sanctioned.

### 7.3 Other controls

| Control | Default | Detail |
|---|---|---|
| International Spend | **ON** for all cards | Toggle under Advanced Controls. Off = every non-US transaction declines. International transactions are **not eligible for cashback**. FAQ: "Rho Cards does not charge foreign transaction fees" (contradicted by ToS, see §16) |
| Card Usage Dates | none | `usage_starts_at` = first day usable; `usage_ends_at` semantics: "The card can be used **up to the day before** the date defined here. Transactions will be declined **starting on the end date**." |
| Billing address | org billing address | Settable **per card**; used to avoid AVS declines when shipping address differs |
| Card expiration | **3 years from issue date** | |
| Lock / Unlock | Active | Three-dot menu on card detail. Locked cards decline all transactions and move to the Inactive Cards section |
| Cancel | n/a | Irreversible: "Once you've canceled your Rho Card, it cannot be reactivated." Cancel modal shows a 30-day Spend Summary and a list of recurring subscriptions, with an opt-in to create a replacement card and transfer subscriptions |
| Accounting automation per card | off | Physical cards can carry accounting-automation settings; every card can carry a **default option for each Field**, which new transactions inherit with an **AUTO** indicator until overridden |
| User Limits | **legacy, off by default** | "Monthly user limits are a legacy feature that's no longer enabled by default ... no longer part of Rho's standard offering." A recurring monthly cap across all of a user's cards |
| 2FA gates | optional | Settings > Security > Two-Factor Authentication > 2FA Policies: require 2FA **for all transactions**, **for issuing cards**, and **for physical card activation**. Changing the 2FA Policy itself now requires 2FA |

### 7.4 Card status lifecycle (API enum)
`printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `active`, `expiring`, `locked`, `canceled`, `suspended`, `expired`. UI surfaces a narrower set: Active / Inactive / Cancelled (plus Locked, Pending).

---

## 8. Card issuance, shipping and activation

### Creation paths
1. Cards > All Cards > **+ Create Card** (black/green button, top right) > for yourself / for someone else / bulk create.
2. Mobile app (own cards and, since March–May 2026, team and virtual vendor cards).
3. **Bulk CSV** upload: Cards > Create New Card > Bulk Create Cards. Downloadable template.
4. During user setup ("Simultaneous card & user provisioning", shipped March 25, 2026).
5. From the Vendors tab (single-use vendor card only).

### Bulk CSV schema
| Input name | Optional? | Examples |
|---|---|---|
| User Email | No | test@rho.co |
| Card Type | No | Virtual, Physical |
| Card Limit Amount | Yes | 1000 |
| Card Limit Type | Yes | `Fixed`, `Monthly`, `Single_use` |
| Department name | Yes | Test |
| Shipping Address | Yes | 100 Crosby Street |

Upload flow: Import & Review > errors flagged inline and editable > bulk-apply settings to checked rows > Submit.

### Physical card shipping
- Delivered by **FedEx, typically 2–3 business days**. Email notification when mailed; tracking number available from Client Service. Since June 30, 2026 shipping status with FedEx tracking links and delivery-state labels appears on the pending card screen.
- **Cannot ship to P.O. Boxes.** Physical addresses only.
- **International shipping is supported**: same creation flow, enter an international shipping address.
- Cards ship **inactive**.
- Expiring-card replacements: the All Cards page has an **Expiring cards tile**; open a card to update its shipping address during the eligibility window, update it multiple times before the replacement ships, and optionally save it as the default for that cardholder's future replacements. The card-expiration help page instead says to "reach out to Customer Service as soon as you receive the email notification" to change the address, which is the older manual path.
- A fee exists for **expedited card shipping** ("no annual fee, subscription fee, or per-card fee, though an optional fee applies if you pay for expedited card shipping"). **The amount is never stated anywhere in the corpus.**

### Activation
- Physical: scan the **unique QR code in the card mailer** ("Physical cards can only be activated by scanning the unique QR code"), or log in to Rho > Cards > select pending card > **Activate card** > confirm. The two statements sit adjacent on the same page and conflict in strictness.
- Virtual: usable instantly, no activation.

### Expiration and renewal
- Both physical and virtual cards stay active through the **entire month** of their expiration date and are canceled on the **1st of the following month**. Example given: expiry August 5 → active until end of August, canceled September 1.
- Expired cards are automatically canceled and a **replacement is auto-issued**; physical replacements ship to the same address, sent out **before** the expiration date.
- The replacement always has a **new card number**; numbers cannot be transferred.
- Recurring subscriptions are automatically transferred to the new card **where the merchant supports it**; otherwise manual re-entry.
- Clients get emails before expiry.

### Sharing card details
- Cards > select card > three dots > **Share card**. Recipient email plus optional note. Recipient gets a secure link.
- The recipient can open the details **once**; if unopened the link **expires after 72 hours**.
- Same mechanic in the mobile app and for Bill Pay single-use vendor cards.
- Permission: "Share Card Details".

---

## 9. Receipt capture and matching

### Channels
| Method | Address / mechanism | Matching |
|---|---|---|
| SMS | Photo to Rho short code **555746** | Automatic; confirmation text back; multiple receipts per message allowed. Requires a **US or Canada** mobile number; standard messaging rates apply |
| Email forward | **receipts@rho.co** | Automatic |
| Reply to transaction alert | Reply to the transaction email / SMS / push with a photo or PDF | Matched to **that** transaction |
| Gmail Connector | OAuth connect at Settings > Integrations > Gmail | Automatic, from the point of connection forward |
| Mobile app | Photo or camera roll upload on a selected transaction | User selects transaction |
| Desktop | Drag/drop or file picker in the transaction details panel | User selects transaction |

Supported file types: **PDF, JPG, PNG**. Transactions with receipts show a **paperclip icon**. Bulk download: Expenses > Export > Receipt Images > date range > Download Receipts > ZIP; filters applied to the table carry into the export.

### Matching engine
Rebuilt April 30, 2026: "Added **merchant identity verification** to every match, so a receipt from Uber only ever attaches to an Uber transaction. Better **normalization, confidence scoring, and date proximity logic** ... Cardholders can now flag a bad match directly in the app." (changelog)

### Gmail Connector (launched April 30, 2026)
- Scans the connected inbox for receipts from merchants the user has transacted with on their Rho card and attaches matches automatically.
- Scope: "only reads emails that look like receipts. It does not access personal messages, drafts, or any other content." Rho "only requests read access to messages that match receipt criteria."
- Keywords: a default set of keywords and common merchant senders; users can **add custom keywords** at Settings > Integrations > Gmail > Manage. Marketing copy says "You set the keywords **before** connecting, can edit them anytime"; the help page describes keyword management only **after** connecting.
- Per-user: each cardholder connects their own inbox; pulled receipts attach only to that cardholder's transactions. Admins can extend the connector across the whole team in one action.
- **Historical email is not backfilled**: "The Gmail Connector captures receipts from the point of connection forward." Older receipts need manual upload or bulk forwarding.
- Disconnect any time at Settings > Integrations > Gmail > Manage > Disconnect. "No inbox data is retained after disconnection." Already-attached receipts stay in Rho.
- Requires Google Workspace admin permission where third-party app access is restricted.
- Gmail is the **only** connector; "When are more connectors coming? In the pipeline. We will share timing when it is confirmed."

### Receipt notifications (beta, May 27, 2026)
Notifications are driven by **expense rules, not per-card settings**:
- If the policy does not require a receipt for a transaction, no prompt is sent.
- Channel matches context: **SMS for in-person transactions, email for online or recurring transactions**.
- A **daily incomplete-expense reminder** sweeps anything still missing required information at end of day.
- Push notifications are "required and remain enabled by default"; SMS/email toggles at User Settings > Notifications.

### Known friction
- Replying to a notification for a transaction that already has a receipt **returns an error**; to replace, upload a new file in the desktop transaction details panel.
- Receipt uploads flow to QuickBooks with the QBO integration, but "this currently does **not** apply to Treasury transactions."
- Cardholders are told to make sure **tip amounts are included** on the receipt before submitting.

---

## 10. Expense policy enforcement

### Rules Builder (Settings > Expense Rules > + Add Rule)
Applies to "all Rho Card transactions, reimbursements, and credits."

Conditions:
| Condition | Meaning |
|---|---|
| All expenses | All company spending regardless of amount, department, merchant (supports **Exceptions**) |
| Amount | Above a specific dollar threshold |
| Department | Spending from a specific department / cost center |
| Merchant category | Specific business types, e.g. restaurants or travel |
| Custom | Combine multiple conditions |

Requirements that can be demanded: **Receipt, Note, Attendees, Client ID, Department, Label**, plus "Mark expense as out of policy" and "other custom rules available."

Key constraint, stated flatly: "these are **post-spend controls**, meaning Expense rules **will not cause Rho Cards to get declined**." Pre-spend enforcement is card controls (§7) only.

More than one rule can apply to a single charge. Separate policies can be configured for **Expenses** vs **Reimbursements** via a Reimbursement widget on the Policies tab.

Worked rule examples from the help center:
- Require receipts on all transactions **over $20**, with exceptions for 2 users and 4 vendor-specific cards.
- Entertainment budget: require **Attendees** field plus a receipt.
- Home Office Stipend budget, transactions **over $250** → marked **Out-of-Policy** and routed for review.
- Construction Materials budget: receipt plus a note containing a **job number**.

Suggested rules ship as a starting point in the Policies tab; the documented default example is "require receipts and reasons for all transactions **over $10**", editable to e.g. $25.

### Policy documents
Expenses > Policies > **Employee Handbook** section > Upload Document. Storage and distribution only; the corpus describes no parsing of the uploaded policy into enforceable rules.

### Approvals (Settings > Expense Settings > Expense Approvals)
Approvals are keyed on **dollar amount**, separate from the Rules Builder which governs required *information*.

Two worked ladders appear in the corpus, and they disagree on the middle tier:
| Page | Auto-approve | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|---|
| how-to-set-up-approvals-for-expenses | under $10 | over $10 | over **$500** | over $10,000 |
| how-to-set-up-direct-manager-approvals | under $10 | over $10 | over **$1,000** | over $10,000 |

Mechanics:
- Multiple approvers in one tier: **any one of them** can approve or reject.
- **Tier amounts are immutable once created**: "Once you create an approval tier, you won't be able to change the amount. To make changes, you can create a new tier and delete the old one."
- **Direct manager approvals**: managers assigned in the Users tab (Assign Managers), manually or imported from an HRIS; errors are flagged for correction and re-upload. A tier can be "direct manager" alone or combined with a static user.
- Payment approvals are a **separate** system: Settings > Payment Security > Payment Approvals, with its own thresholds and its own number-of-approvers setting (example given: 1 approver over $50, 2 approvers over $100).

### Expense statuses
| Status | Meaning |
|---|---|
| Complete | Approved |
| Auto-Complete | Approved automatically per the approval policy |
| Needs My Approval | Requires approval from the viewing user |
| Needs Approval | Requires approval from one or more other users |
| Incomplete | Missing information per the submission policy |
| Out-Of-Policy | Determined out of policy per the submission policy |
| Rejected | Rejected by an approver |

Rejection requires a note; the reason is sent to the submitter and persists in the expense's activity history. Bulk approve/reject is supported from the table header. A **"Needs My Approval" tile** on Company Expenses shipped June 30, 2026, as did a warning when an admin tries to approve an expense with required fields missing.

### Expense views and coding
- Expenses tab splits into **Company**, **Personal** and **Policies**. Account Owners/Admins see all card spend; **Department Owners see only their departments'** spend.
- Default date window is the **last 60 days**.
- Custom saved table views (columns + filters, "Save As a New View").
- Departments, Labels, and **Fields** all attach to card transactions. Fields: up to **7 active Fields**, free text or predefined list; archived Fields do not count and archiving never deletes history. New accounts ship with a suggested **Category** Field pre-filled with 10 options: Software & Subscriptions, AI & Compute, Marketing, Travel, Food & Meals, Office & Supplies, Equipment, Contractors, Legal, Other.
- **Card repayments do not carry Fields** (to avoid double counting); card purchase **refunds do**.
- Split transactions: any card or banking transaction can be split across departments or custom attributes; the splitting user must be assigned to the departments involved. In CSV exports a split shows as **separate rows sharing one transaction ID**.
- Coding hierarchy for mapping rules, highest priority first: **Label > Sender > Vendor > Merchant > Card > Department**. Manual line-level coding wins over mapping rules and is not overwritten by new rules, except when "Apply Mappings" is run from Accounting > Dashboard > three dots, which overrides even manual codings for a chosen timeframe.
- Native accounting integrations named for expense sync: **QuickBooks Online, NetSuite, Sage Intacct, Puzzle**. Xero is described inconsistently: the expense-management FAQ lists Xero among direct integrations in one answer and then says "Xero connects today through a **bank feed** rather than a native sync" in another.

### Third-party T&E card feeds
- **Card feed integration** via **Mastercard Smart Data**. Request through clientservice@rho.co; Rho confirms T&E compatibility, issues a **Delivery ID** the customer passes to their T&E vendor. Setup takes **3 to 5 business days**.
- Data shared: cardholder name, last 4 of card number, purchase date, purchase amount, merchant name, merchant category. Nothing else.
- Sync frequency: **1 time per day, Monday–Saturday, after 5 PM EST**.
- **Navan Expense** partnership: linked via Mastercard Smart Data (Rho provides Navan the **Mastercard Distribution ID**). Navan sees Rho cards and transactions. Critical split of responsibility: **receipts must be submitted in Navan** ("Adding receipts in Rho will not sync them to Navan"), and **spend policies live in Navan**, while card limits and merchant restrictions stay in Rho. Onboarding is entirely Navan-led.
- Emburse and SAP Concur have partner pages but no mechanics beyond "bring your Rho card". The SAP Concur page contains a copy-paste error: "Connect **Emburse** with Rho Corporate Cards" inside the SAP Concur page body.

---

## 11. Employee reimbursements

| Attribute | Detail |
|---|---|
| Enablement | Settings > Expense settings > Reimbursements; separate toggles for **Reimbursements** and **Mileage Reimbursements**; admin/account owner only |
| Submission | Reimbursements > Request Reimbursement; toggle **Expense** or **Mileage** |
| OCR | Uploading a receipt auto-fills **Amount, Merchant, Transaction Date**; manual entry also allowed. Mobile OCR shipped March 25, 2026 |
| Payment rail | **ACH, domestic bank accounts only** |
| Account type | **Checking accounts only. "Savings accounts are not supported at this time."** |
| Non-US accounts | Explicitly unsupported: "Can reimbursements be issued to non-US bank accounts? **No, that is not something we support right now.**" |
| Privacy | Employee bank details "securely stored and **not visible to other team members**" |
| Approval | Same approval ladder as card expenses; statuses include **Awaiting Approval** and **Awaiting Payment Approval**. Anything not auto-approved needs a manual approve/reject |
| Disbursement | Reimbursements tab > Pay (single) or bulk Pay; pending disbursements group **per user** and "Pay Total" sends **one payment per user**; choose the source account |
| Payout timing | Submitted **before 3 p.m. ET** arrive same day; after 3 p.m. ET arrive next business day |
| Paid outside Rho | Three-dot menu > **Mark as Paid** (e.g. via payroll); removes it from the disbursement queue |
| Status trail | Pending Payment → Paid |
| Retry | Canceled or Failed reimbursements can be retried individually or in bulk (shipped May 27, 2026); no need to recreate |
| Edit | Submitted reimbursements can be edited before processing (shipped March 25, 2026) |
| Archive | Expenses > Personal > Reimbursements > three dots > Archive Reimbursement. **Permanent and cannot be undone**; removes it from the approval queue. Admins/Account Owners can archive for any user |
| Permissions | "Can Disburse Reimbursements" is a discrete permission |
| Accounting | Syncs via mapping rules; needs **Rho Accounts Payable** mapped under Integrations > Mapping Rules > Settings > Other Accounts |
| Funding source | "employees are reimbursed directly from the **Rho checking account**" |

Rho's own positioning of the cards-vs-reimbursement split: "On Rho's corporate cards, the company pays first and sets spend limits before a purchase happens. With reimbursement, the employee pays first and waits to be paid back, and any policy is **enforced only after the fact**."

---

## 12. Mileage

| Attribute | Detail |
|---|---|
| Enable | Settings > Expense settings > Reimbursements > Mileage Reimbursements |
| Default rate | Pre-populated at "the current year's Internal Revenue Service (IRS) rate of **$0.70/mile**" |
| Override | Admin or Account Owner can set any company rate |
| Rate versioning | "Your mileage reimbursement will be calculated using the rate your business set **when the expense occurred**" |
| Distance | Enter start and end points; an **embedded map** auto-calculates mileage and the reimbursement amount. Addresses **must be selected from the dropdown** as typed so the distance measures accurately |
| Multi-stop | Product page: employees "submit trip mileage details in the Rho App, which automatically calculates the distance **between stops**" |
| Payment | Same ACH domestic-checking rail as other reimbursements |
| Accounting | Requires an AP chart-of-accounts mapping (Rho Accounts Payable) or a dedicated expense account, otherwise ERP sync fails |

Staleness: Rho's public **mileage reimbursement calculator** tool page (tools/mileage-reimbursement-calculator, article dated June 16, 2025) still presents **2024** as current, with Business $0.67, Medical/Moving $0.21, Charitable $0.14, and a rate table running 2024 back to 2020. The in-product default is $0.70. No 2026 IRS rate appears anywhere in the corpus.

---

## 13. Cashback program: mechanics, rates, exclusions

Governing document: **Cashback Rewards Program Terms and Conditions**, rho.co/policies/cashback-rewards, dated **April 10, 2025**. (The separate page rho.co/policies/rewards-terms-and-conditions, dated September 11, 2025, is **not** the cashback terms; it is the "Escape with Rho Sweepstakes" official rules. Marketing links labelled "Rewards Terms" are ambiguous between the two.)

### 13.1 Rate matrix

| Card program | Standard | Rho Platinum |
|---|---|---|
| Rho Corporate Card with **Daily Terms** | **1.25%** | **2%** (marketed "up to 2%") |
| Rho Corporate Card with **Monthly Terms** | **1%** | **1.75%** (marketed "up to 1.75%") |

- Cap: **$1,000,000 in eligible spend per calendar year, across all tiers**. "The cap applies to eligible spend, **not to the dollar amount of Cashback Rewards**." Above $1M, Rho says "Talk to sales and we'll build your program."
- No minimum spend to accrue on Daily Terms.
- Rewards are earned **only on settled transactions**.

### 13.2 Rho Platinum qualification (all four required)
1. **Payroll is run from Rho** ("Rho is your central account for payroll").
2. **Business revenue is deposited via Rho Checking**.
3. **50% or more of the company's assets are held at Rho**.
4. **An open Rho Corporate Card**.

Platinum is not a paid plan and carries no subscription fee. Status is continuous, not annual: "Platinum status reflects your **current** setup. If your account no longer meets the qualifications, your Cashback rate returns to the standard rate." There is **no stated grace period, no stated measurement window, no stated audit cadence**, and no self-serve status indicator described beyond "contact your account team or reach support."

### 13.3 Payment condition (hard gate)
"You may only receive Cashback Rewards when you **pay the full amount due on your billing statement on time**. ... If you do not pay the full amount due on time, you will **not receive any Cashback Rewards for the billing period**; and you **forfeit your ability to earn any** Cashback Rewards for the billing period."

Also: "You will not receive Cashback Rewards if you **deposit funds in your Rho Account without making an actual payment to Rho**." Late payment forfeits only that statement period; the next on-time statement earns normally.

### 13.4 Exclusions

**Excluded merchants / merchant categories (four, verbatim):**
1. **Walmart Inc., and its affiliates and subsidiaries**;
2. Merchants offering **"Utilities"**, designated by Mastercard MCC;
3. Merchants offering **money transfer services, digital payments, and/or quasi-cash**, designated by Mastercard MCC;
4. **Transactions conducted or authorized in non-U.S. jurisdictions.**

**Excluded from "Qualifying Purchase" (nine categories, verbatim):** fees, fines, or interest charges paid to Rho; cash advances; balance transfers; cash equivalents; **gift cards**; **prepaid cards or reloadable prepaid cards**; purchases made with Cashback Rewards; **person-to-person payments or transfers**; prohibited or restricted transactions such as **online sports betting and internet gambling**; and **loan payments or account funding made with the Card**.

A Qualifying Purchase is "any purchase made with your Card **minus returns and other credits**."

Third-party processing caveat: "You may not receive additional Cashback Rewards when a merchant uses a third-party to sell a product or service or otherwise uses a third-party to **process** your transaction," or where Rho "cannot identify the types of purchases you make."

### 13.5 Accrual, payout and redemption

| Step | Daily Terms | Monthly Terms |
|---|---|---|
| Accrual → Rewards Account | Typically **on the 6th business day of the month**, for the preceding month's card spend, as **one payment** | Typically **6 business days after** the statement balance is paid in full |
| Where it lands | "Rho Rewards checking account" / "Rewards Account", visible under Banking | same |
| Redemption | Banking > Rewards Account > **Redeem Rewards** > transfer a specified amount or the full balance into the **Primary Checking Account** | same |
| Redemption speed | "**instantly**" | same |
| Who may redeem | **Account Owner** or **Administrator** only, plus custom roles with the **Redeem rewards** permission and Banking visibility. Budget Owner, Employee, Bookkeeper and Investor roles cannot | same |

### 13.6 Expiry, clawbacks, ownership, disputes

| Rule | Detail |
|---|---|
| Expiry | Must be redeemed **within twelve (12) months of being earned**, or forfeited. "**Rho will not provide notifications regarding the impending expiration.** It is your responsibility to track and redeem" |
| Ownership | "The Cashback Rewards you may earn and accumulate are **not your property and do not belong to you** until ... redeemed and issued to you in the form of a statement credit by Rho" |
| Transferability | Cannot be transferred to anyone or any other Rho Account; cannot be sold or used in a legal action, assignment of rights, or bankruptcy proceeding |
| Returns / exchanges | No cashback on a purchase later returned or exchanged and credited back. The deduction "will apply as a **debit to your billing statement** and will be an amount owed and due to Rho." Rewards account page: reversals net out against accrued rewards "in the following periods" |
| Cashback errors/disputes | Must be raised **within sixty (60) days** from the date the relevant billing statement was issued |
| Card cancellation | "If we cancel your Card or close any of your Rho Accounts for any reason, you **may immediately lose all** the Cashback Rewards" |
| Suspension | Suspending card or account use may suspend cashback use; restored when accounts return to good standing |
| Misuse | Rho's "sole judgment" of misuse or abuse can suspend earning/use or cancel the card/accounts immediately |
| Program change | Rho must give **at least 45 days' notice** to cancel or modify; members then have **90 days from the notice date** to redeem under current terms. Unredeemed rewards are **forfeited** if the program is canceled, or **subject to new terms** if modified |
| Program termination | Terminates automatically if Rho "permanently ceases to operate"; Rho may make exceptions "at any time, without notice to you" |
| Enrollment | Automatic upon Card activation, at no charge. Eligibility requires an open Rho Account and being a Cardholder |
| Returning cashback | Members may return rewards by emailing clientservice@rho.co; Rho "may, in our sole discretion, accept the return" |
| Pay with Cashback | Rewards may be applied to the card billing statement as a credit. Credit "may appear on the current **or following** billing cycle" (typically when a charge lands near period end, or when a past-statement error is found). Even if rewards would cover a cycle, "**you must pay the amount due on each statement at the time the payment is due**"; overpayment is credited or refunded. Only authorized Administrators or Users may apply rewards. "We may at any time **refuse to accept Cashback Rewards** to cover eligible payments without providing notice to you" |
| Arbitration | Governed by the Arbitration Provision and Class Action Waiver in the Rho Terms of Service, incorporated by reference |
| Tax | "Cashback from Rho is **not considered taxable** and we do not issue 1099s for cash back" (help center), with a "consult your own tax adviser" caveat |

### 13.7 Cashback payout form: unresolved contradiction
Three different descriptions coexist:
- Cashback Terms: rewards become yours only when "redeemed and issued to you in the form of a **statement credit**".
- product/corporate-cards footer: cashback is "**issued as a statement credit**".
- Help center and versus/brex: "All Cashback is credited to your **Rho Rewards checking account**"; redeem by transferring to Primary Checking; "Real cash, not points"; "**Credited as cash**".

The operational product is a rewards deposit account with an instant transfer to checking. The governing terms say statement credit. Both are asserted as current.

### 13.8 Mastercard Easy Savings (stacked on top)
Part of the Mastercard World Elite Business program; automatic, no enrollment described.
- Categories: advertising, technology, travel and entertainment.
- Named participating merchants: **Avis, Budget, Dropbox, Squarespace, Snapchat**.
- **4% back at more than 20,000 restaurants** (examples: Chopt) and hotels (Days Inn, Holiday Inn).
- Rate range: **1% to 25%**.
- **No annual limit** on Easy Savings rebates, "though some limits may apply at individual merchants' discretion."
- Credited by Mastercard **1–5 business days after the purchase settles**, shown as "Mastercard Load". Monthly Terms accounts see it in the credit account; Daily Terms accounts see it credited to the card balance.
- Benefit disclaimer: "**Rho does not provide rental car insurance and other specific benefits directly.** However, they may be available through Mastercard" (check MyCardBenefits.com). This sits against the versus/ramp page, which lists as Rho card benefits: Priority Pass lounge access (stated as complimentary for cardholders, including lounge visits, "just present your Rho card"), **primary car rental insurance**, 24/7 concierge, Easy Savings rebates, and ID theft protection (as of 08/02/2026).

### 13.9 Competitive cashback claims [Rho claim]
| Competitor | Rho's stated claim | As-of date |
|---|---|---|
| Brex | "Category multipliers, not cash back: 7x rideshare, 4x Brex travel, 3x restaurants, 2x software, 1x everything else"; points redeem at **0.6 cents each** for cash (cited to Forbes Advisor, verified 05/06/2026); Essentials free, **Premium $12/user/mo** | 2026-08-17 / 2026-09-08 |
| Ramp | "No published cashback rate"; "the current rate is **variable, 0%–1.5%**, set per business ... you learn your rate after applying"; "Ramp's flat 1.5% ended in **May 2024**" (cited to NerdWallet, updated 06/15/2026); free tier then **Plus at $15/user/mo plus an undisclosed platform fee**; higher limits via a **Reserve Account** locking cash 1:1 | 2026-08-02 / 2026-09-08 |
| Mercury | "**1.5% cashback** on card spend, flat, no higher tier"; "$0 annual fee on IO cards"; switches to 30-day terms at **$15,000** balances | 2026-09-08 |
| Amex | "$895 annual fee" on Business Platinum; points-based | undated on page |

---

## 14. Disputes and fraud handling

### Initiating a dispute
| Path | Cap |
|---|---|
| Transaction drawer > "**I do not recognize this transaction**" | 1 transaction |
| Rho mobile app, from the transaction | 1 transaction |
| **Expenses tab**, multi-select > start dispute | **up to 15 transactions per submission**, bundled into a single dispute |
| Client Service (email / phone / chat), 24/7 | n/a |

Client Service needs: the **last 4 digits of the affected card** and the **Rho Transaction IDs** of the disputed transactions, plus answers to a question set.

**Admins and Account Owners can initiate disputes on behalf of any cardholder** in the organization. Dispute status is trackable in the platform.

### Card cancellation side effect
"If you report a transaction as **fraudulent** and submit a dispute through Rho, the card used for the transaction **will be canceled**." Non-fraud disputes (billing error, duplicate charge, service issue) leave the card active unless the user cancels it. Elsewhere stated as automatic: "the card(s) associated with unrecognized and unauthorized charges will be **automatically canceled**."

### Timelines (three different figures in the corpus)
- "Typically, disputes may take **up to 90 days** to be resolved." (how-to-dispute)
- "A dispute determination can take **45-90 days** and is managed by Mastercard." (same page, later section)
- "our team will begin our investigation, which may take **up to 90 days**." (employee-card-faqs)

### Liability
- Help center: "Rho clients are protected against unauthorized transactions and are **not liable for unauthorized use of Rho Cards once Rho is notified**."
- ToS Addendum A §1.6, the actual allocation, unless the Card Network Liability Waiver Program applies:
  - **10 or more Cards issued** to the company and its users → "you will be liable for **all** unauthorized use of all Cards."
  - **Fewer than 10 Cards issued** → liability limited to the **lesser of $50.00** or the value obtained by the unauthorized use.
  - No liability for unauthorized use occurring **after** Rho receives notice.
  - "unauthorized use" excludes use by a User who is no longer employed, unless and until Rho has been notified and the card canceled.
- ToS §1.8: "The Rho Corporate Card with Daily Terms is a **commercial** credit card and **does not provide consumer protections** for lost or stolen credit cards or unauthorized transactions."
- ToS §1.9: Rho "is **not responsible for tracking or monitoring** the Company's Charges"; the company must review statements and identify suspect charges.
- Disputed charges are still collectible: "Any Charges in connection with a dispute are **subject to collection on the payment date** if the dispute has not yet been resolved." Non-payment during a pending dispute lets Rho suspend/freeze accounts, impose fees, reduce or eliminate the spending limit, accelerate all Obligations, and debit any linked account without notice.
- Chargebacks resolved in the customer's favor are credited "on the following or future statement(s)."
- Process order Rho prescribes: contact the merchant first, then initiate a chargeback.

### Proactive fraud controls
- **SMS fraud alerts** (opt in at User settings > Notifications, cell number required): a flagged transaction is **automatically declined**, the cardholder gets a text; **reply YES** to lift the block and re-attempt, **reply NO** to cancel the card.
- In-dashboard alerts: "Unrecognized card transaction", "Suspicious login or new user alert", "Unrecognized card transaction attempt". Choosing "No, Cancel the Card" auto-cancels and **auto-issues a replacement**.
- Lost/stolen: lock the card immediately from My Cards, then cancel if permanently lost; call 855-743-8746. Rho recommends creating a **new** card after canceling rather than expecting a reissue.
- Disclaimer: "Rho **does not offer fraud prevention as a service** and is unable to guarantee full fraud protection in connection with your account."
- Recommended hardening: 2FA, Rho Card alerts, card-specific controls.
- Merchant-driven holds: Rho may hold or suspend card use where the final amount is unknown at authorization (restaurants, hotels, rental cars), and may hold funds in the Rho Account "less than, equal to, or higher than the actual or final Charge."

### Support-hours contradiction
Most pages: Client Service "available **24/7**" (phone, chat, email; plus iMessage/WhatsApp since June 2026). But employee-card-faqs, under "What should I do if I suspect fraud on my card?": "For live support, our team is available **Monday through Friday from 8am ET to 8pm ET**."

---

## 15. API surface for cards (read-only, v1)

`GET /api/v1/cards` and `GET /api/v1/cards/{id}`. Scope: `cards:read`. Part of the stable, additive-only `v1` contract.

- Filters: `user_id` (repeatable), `type`, `status` (repeatable). Repeats are OR; different filters are AND.
- Pagination: `page_size` default **20**, range **1–100**; cursor `page.next_page_token` passed back as `page_token`. Page tokens are version-scoped, so pagination must restart when migrating v0 → v1.
- Unfiltered lists **include canceled and expired cards** so stable IDs join to historical transactions.
- Money is in **minor units** (cents for USD) with an ISO 4217 currency code.
- **Only `last_4` is exposed. Full PAN, CVC and expiration dates are not available through the API.** Returns 404 for a card belonging to another business.
- Fields: `id`, `name`, `last_4`, `type`, `status`, `cardholder{user_id, first_name, last_name}`, `spending_limit`, `spending_limit_type`, `current_spend`, `pending_spend`, `spend_period_start`, `spend_period_end`, `usage_starts_at`, `usage_ends_at`, `billing_address`, `shipping_address`, `blocked_categories` / `allowed_categories`, `blocked_merchants` / `allowed_merchants`.
- All spend windows computed in **Eastern Time (America/New_York)**.

Card-related transaction types (`GET /api/v1/transactions` enum): `card_debit`, `card_credit`, `card_refund`, `credit_repayment`, `credit_repayment_refund`, `credit_cashback`, `rewards_accrual`, `rewards_cashback_redemption`, `adjustment_credit`, `adjustment_debit`. Account types: `checking`, `credit`, `investment`, `savings`, `rewards`. Statuses: `pending`, `settled`, `failed`, `awaiting_approval`.

Notable API-side gap, in Rho's own words: a refund or credit is "**not by itself a dispute**", and `v1` exposes "**no dispute indicator**". There is also no receipt-required flag, no expense-approval status, no policy or rule object, and no write access (write access and webhooks announced as "next" on 2026-08-03).

Statement objects for the card line expose `repayment_date`, `spending`, `repayments`, `cashback` on `type: "credit"` statements; `account_id` is **null** on credit statements because they are not tied to a deposit account.

Sandbox evidence (sandbox/cards.json, captured against 2026-09 data): limit types seen are `monthly`, `daily`, `fixed`; statuses seen are `active`, `locked`, `suspended`, `canceled`, `expired`; both `physical` and `virtual`; both allow-list and block-list cards; spend windows like `2026-09-01T04:00:00Z` → `2026-10-01T04:00:00Z` (ET midnight boundaries). The `fixed` card has `spend_period_end: null` as documented. Sandbox transaction memo confirms daily repayment naming: `"Daily credit repayment for date 2026/06/24"`.

---

## 16. Contradictions and tensions found in the corpus

| # | Topic | A says | B says |
|---|---|---|---|
| 1 | Charge vs revolving | product/corporate-cards: "it's a **charge card**", full balance paid each period, not carried at an interest rate | docs/docs_v1_accounts.md: `credit` = "**Revolving credit lines** backing corporate cards" |
| 2 | Personal credit | "No personal guarantee, **no personal credit check**"; "Rho will not conduct a hard or soft check on your credit score" | ToS §1.12 (both addenda): consent to obtain a **consumer report** from a "consumer or business credit reporting agency" about the Company **and each authorized user**, with CA/MN/OK/NY individual rights |
| 3 | Foreign transaction fee | employee-card-faqs: "Rho Cards does **not charge foreign transaction fees**"; pricing page lists only a 1% foreign-currency transfer fee | ToS §fees (both addenda): Rho "may charge ... transaction fees (**including up to 1% of the transaction amount on foreign transactions**)". Also "You agree to pay all foreign transaction fees imposed by us" |
| 4 | Cashback form | Terms + product page: "**statement credit**" | Help center + versus/brex: credited to a **Rho Rewards checking account**, redeemed by transfer to checking, "real cash", "Credited as cash" |
| 5 | Monthly Terms threshold | Marketing/FAQ: $25,000 at Rho **or $75,000 combined** with linked external accounts | Help center: "minimum cash balance of **$25,000**", no combined path mentioned |
| 6 | Approval ladder example | how-to-set-up-approvals: tier 2 at **over $500** | direct-manager-approvals: tier 2 at **over $1,000** |
| 7 | Vendor cards on mobile | Help center: "Vendor cards are currently a **web-only** feature, so they won't appear in the mobile app" | Changelog Mar 25 and May 27, 2026: "Team and vendor cards, now on mobile"; "Admins ... can now create virtual vendor cards straight from the Rho app" |
| 8 | Physical card activation | "Physical cards can **only** be activated by scanning the unique QR code" | Same page, next section: "Cards can **also** be activated directly in the Rho platform" |
| 9 | Dispute duration | "Typically ... up to **90 days**" | "A dispute determination can take **45-90 days**" |
| 10 | Support hours | "available **24/7**" (multiple pages) | employee-card-faqs fraud section: "**Monday through Friday from 8am ET to 8pm ET**" |
| 11 | Mastercard benefits | versus/ramp: "**primary car rental insurance**, 24/7 concierge, Priority Pass" as Rho card benefits (as of 08/02/2026) | Easy Savings help page: "**Rho does not provide rental car insurance** and other specific benefits directly" |
| 12 | Xero | expense-management FAQ: Xero listed among "direct accounting integration" options | Same page FAQ: "Xero connects today through a **bank feed** rather than a native sync" |
| 13 | Cashback "on all spending" | site-llms.txt: "up to 2% cashback **on all spending** (as of 08/21/2026)" | Cashback terms: four excluded merchant/category classes plus nine excluded purchase types |
| 14 | Gmail keyword setup | Product FAQ: "You set the keywords **before** connecting" | Help article: keyword management is described only under "Managing keywords and senders" **after** connecting |
| 15 | Expiring-card address change | All Cards page: self-serve address update during the eligibility window, repeatable | card-expiration article: "**reach out to Customer Service**" |
| 16 | Rho Capital personal credit | "Applying doesn't involve a hard pull on your personal credit" | Same page footer: "**consent to obtain personal credit report is required** ... **Personal Guaranty may be required**" |
| 17 | Mileage rate | In-product default **$0.70/mile**, "current year's IRS rate" | tools/mileage-reimbursement-calculator still presents 2024 as current: business **$0.67** |
| 18 | Card limit periods | Help pages list Daily / Weekly / Monthly / Annual | API enum adds **`quarterly`**; mobile changelog also lists quarterly |

---

## 17. Conspicuously absent from the corpus

These are things a reader would expect and that the corpus never states:

1. **Any dollar figure for a card limit.** No starting limit, no typical limit, no maximum, no multiple-of-balance ratio for Daily Terms. The ToS explicitly reserves the right never to disclose the limit.
2. **The expedited card shipping fee amount.** Its existence is acknowledged in two blog comparison pages; the price is never given, and it does not appear on the pricing page.
3. **Monthly Terms credit limit sizing**, approval SLA, or decline reasons. Only "personalized based on the business's financial health."
4. **Daily Terms risk factors**, beyond "risk factors that vary by client."
5. **Whether cashback is measured on posted or settled date for the calendar-year cap**, and what happens to spend that straddles a year boundary.
6. **Platinum measurement mechanics**: how "50% or more of company assets" is measured, over what window, how often it is re-tested, and whether a rate change is retroactive within a statement period.
7. **Any self-serve Platinum status indicator.** The only path given is "contact your account team or reach support."
8. **Cashback on the Mastercard Easy Savings rebate itself** and whether Easy Savings credits count against the $1M cap.
9. **Vendor card limits at the product-page level.** The vendor-cards product page promises "Set controls by vendor ... Apply limits and merchant rules to each vendor" but gives no numbers; the vendor-cards help page mentions only international spend, merchant restrictions and usage dates on the setup screen.
10. **Multi-entity card management.** Enterprise/multi-entity is marketed, but the cards docs say cards can only pair with "the Rho Primary Checking account **for your organization only**" and sub-accounts cannot be used.
11. **Anything about card-level FX rate markups** beyond the network-rate description in the ToS.
12. **A dispute indicator in the API**, receipt-required status, expense-approval status, or any policy object. Cards/expenses are effectively read-only metadata in v1.
13. **Whether expense rules can be applied to vendor cards specifically**; the only signal is a rule-exception example listing "4 vendor-specific cards".
14. **Card benefits documentation owned by Rho.** For World Elite benefits Rho defers to MyCardBenefits.com.
15. **Number of cards or card spend volume.** No scale metrics for the card program anywhere in the corpus.
16. **Receipt OCR accuracy, match-rate, or confidence thresholds**, despite "confidence scoring" being named in the changelog.

---

## 18. Dated facts to carry forward

| Fact | As-of date given by Rho |
|---|---|
| Per-card merchant allow list capped at 20 merchants | **08/02/2026** |
| Competitive comparison data (Brex, Ramp, Mercury) on product/corporate-cards and product/expense-management | **2026-09-08**; "Product claims current as of September 2026. Facts verified as of 2026-09-08" |
| versus/brex figures | **08/17/2026** ("All figures last verified August 17, 2026") |
| versus/ramp figures | **08/02/2026**; cash & yield and Bill Pay rows **08/20/2026**; Mastercard World Elite benefit list **08/02/2026** |
| Brex points cash-redemption value 0.6 cents (Forbes Advisor) | verified **05/06/2026** |
| Ramp variable 0–1.5% cashback (NerdWallet) | updated **06/15/2026** |
| site-llms.txt corporate-cards line ("up to 2% cashback on all spending") | **08/21/2026** |
| Cashback Rewards Program Terms and Conditions | **April 10, 2025** |
| Rewards Terms and Conditions page (sweepstakes, not cashback) | **September 11, 2025** |
| Mileage calculator tool article | **June 16, 2025**, rates current "as of 2024" |
| Vendor cards blog post ("How to use Rho's new vendor card") | published **October 06, 2025**, updated **August 29, 2026** |
| Treasury net-yield footnote on the corporate-cards page (90-day T-Bill basis) | **09/11/2026** |

### Card and expense changelog timeline (rho.co/changelog)
| Date | Card / expense shipment |
|---|---|
| Feb 26, 2026 | Puzzle direct integration (transactions, bills, attachments) |
| Mar 25, 2026 | Team and vendor cards on mobile; mobile reimbursements with OCR; simultaneous card & user provisioning; edit reimbursements; interactive card spending graph; card limit proactive notifications |
| Apr 30, 2026 | Gmail Connector; **annual, weekly, daily card limits**; team and vendor cards on mobile (limits adjustable); **receipt matching rebuilt** with merchant identity verification, normalization, confidence scoring, date proximity, bad-match flagging; QBO bank feed expanded |
| May 27, 2026 | Rho Close; **create virtual vendor cards in mobile**; **receipt notifications follow expense policy [beta]**; **switch limit types on existing cards** without reissue; retry failed/canceled reimbursements |
| Jun 30, 2026 | Mobile card management: full limit-type range incl. quarterly; **physical card shipping status with FedEx tracking**; warning for incomplete expenses at approval; "Needs My Approval" tile; iMessage/WhatsApp support |
| Aug 3, 2026 | **Rho API (read-only)**; **CSV export from the Cards tab** with active filters (card owner, spend limit, last four, department) |
| Aug 31, 2026 | Invoice card payments (2.9% + 30¢ deducted, a card-acceptance fee, not a corporate-card fee) |

---

## 19. Fee summary as it touches cards

| Item | Amount | Source |
|---|---|---|
| Annual fee / subscription fee / per-card fee | **$0** | product/corporate-cards, pricing |
| Per-user fee, platform fee for expense management | **$0** | pricing, expense-management |
| Expedited card shipping | optional fee, **amount never stated** | blog comparisons |
| Late fee | **3% of the delinquent payment balance per month, up to 6 months**, unless prohibited by law | ToS Addendum A and B; pricing footnote |
| Foreign transaction fee on cards | FAQ: none. ToS: **up to 1% of the transaction amount** | conflict, see §16 |
| Foreign currency transfer (banking, not card) | **1%** | pricing |
| Collection costs | all collection costs, reasonable attorneys' fees, court costs | ToS |
| Interest | none if paid in full and on time; Daily Terms ToS: "You will **not** be charged interest on your Credit Account" | ToS 2.1 |

---

## 20. Source files read (all under `.../scratchpad/rho/`)

Core marketing/policy:
`pages/core/product__corporate-cards.txt`, `pages/core/product__vendor-cards.txt`, `pages/core/product__expense-management.txt`, `pages/core/policies__cashback-rewards.txt`, `pages/core/policies__rewards-terms-and-conditions.txt`, `pages/core/policies__terms-of-service.txt`, `pages/core/pricing.txt`, `pages/core/faq.txt`, `pages/core/changelog.txt`, `pages/core/versus__brex.txt`, `pages/core/versus__ramp.txt`, `pages/core/versus__amex.txt`, `pages/core/integrations__emburse.txt`, `pages/core/integrations__sap-concur.txt`, `pages/core/tools__mileage-reimbursement-calculator.txt`, `site-llms.txt`

Help center (cards): `help-center__cards.txt`, `...__the-rho-card-with-daily-terms.txt`, `...__the-rho-card-with-monthly-terms-2.txt`, `...__understanding-rho-card-controls.txt`, `...__how-to-create-a-new-rho-card.txt`, `...__how-to-create-and-manage-vendor-cards-with-rho.txt`, `...__how-to-create-cards-in-bulk.txt`, `...__how-to-edit-the-spending-limit-on-a-rho-card.txt`, `...__how-to-edit-the-permitted-spending-categories-for-a-rho-card.txt`, `...__how-to-set-company-wide-merchant-restrictions.txt`, `...__how-to-update-your-card-settings.txt`, `...__card-expiration-and-renewal.txt`, `...__how-to-dispute-a-transaction-on-a-rho-card.txt`, `...__how-to-pay-your-credit-card-balance.txt`, `...__how-to-pay-your-rho-card-from-an-external-bank-account.txt`, `...__how-to-set-up-automatic-card-payments.txt`, `...__employee-card-faqs.txt`, `...__how-to-share-card-details.txt`, `...__how-to-cancel-a-rho-card.txt`, `...__how-to-lock-and-unlock-a-rho-card.txt`, `...__how-to-add-your-rho-card-to-your-digital-wallet.txt`, `...__how-to-attach-receipts-to-card-transactions.txt`, `...__how-do-i-redeem-my-cash-rewards.txt`, `...__how-to-set-up-a-card-feed-integration.txt`, `...__understanding-the-team-cards-page.txt`, `...__understanding-card-cashback.txt`, `...__understanding-mastercard-easy-savings.txt`, `...__why-was-my-rho-card-declined.txt`, `...__how-to-assign-a-card-to-a-department.txt`, `...__how-to-download-a-csv-for-card-transactions.txt`

Help center (expenses): `...__understanding-the-expenses-tab.txt`, `...__how-to-create-rules-for-expenses.txt`, `...__examples-of-expense-rules.txt`, `...__using-suggested-rules-in-rho-expenses.txt`, `...__how-to-set-up-approvals-for-expenses.txt`, `...__how-to-set-up-direct-manager-approvals.txt`, `...__how-to-review-expenses.txt`, `...__how-to-upload-your-company-policy-document-s.txt`, `...__how-to-enable-reimbursements.txt`, `...__how-to-submit-a-reimbursement.txt`, `...__how-to-approve-and-disburse-a-reimbursement-request.txt`, `...__how-to-archive-a-reimbursement-request.txt`, `...__how-to-use-mileage-reimbursements.txt`, `...__how-to-set-up-the-gmail-connector.txt`, `...__how-to-add-an-invoice-receipt-to-a-transaction.txt`, `...__how-to-download-receipts.txt`, `...__how-to-configure-expense-notifications.txt`, `...__how-to-label-expenses.txt`, `...__how-to-export-a-csv-of-your-expenses.txt`, `...__how-to-filter-and-set-custom-views-in-expenses.txt`, `...__how-to-sync-expenses-to-accounting.txt`

Help center (other): `help-center__admin__how-to-set-monthly-user-limits.txt`, `...__how-to-require-approval-for-specific-transactions.txt`, `...__require-2fa-for-sending-transactions-creating-cards.txt`, `...__how-to-report-suspicious-activity-on-your-account.txt`, `...__user-permissions-glossary.txt`, `...__are-cashback-rewards-taxable.txt`, `help-center__general-rho-information__rho-platinum-what-it-is-and-how-to-qualify.txt`, `...__cashback-rewards-terms-conditions.txt`, `...__how-to-redeem-rewards.txt`, `...__rho-perks-and-rewards-what-s-included.txt`, `...__about-rho-capital.txt`, `...__applying-to-rho-faqs.txt`, `...__business-and-industry-eligibility-at-rho.txt`, `...__pricing-requirements.txt`, `...__understanding-the-integration-between-rho-and-navan-expense.txt`, `help-center__banking__rewards-account-overview.txt`, `...__understanding-transaction-details.txt`, `help-center__bill-pay__paying-bills-with-vendor-cards-single-use.txt`, `help-center__departments__how-to-split-transactions-between-departments-and-more.txt`, `help-center__accounting__how-does-coding-in-rho-work.txt`, `help-center__fields__understanding-fields-in-rho.txt`, `help-center__mobile-app__*` (card creation, controls, details, sharing, receipt upload, expense review, lock/unlock/cancel)

API and sandbox: `docs/docs_v1_cards.md`, `docs/docs_v1_transactions.md`, `docs/docs_v1_accounts.md`, `docs/docs_v1_statements.md`, `api/cards_listcards.md`, `api/transactions_listtransactions.md`, `api/statements_liststatements.md`, `sandbox/cards.json`, `sandbox/transactions.json`

Blog comparison corpus (for card fee/threshold cross-checks): `pages/blogcomp/blog__rho-vs-bank-of-america.txt`, `blog__rho-vs-bluevine.txt`, `blog__rho-vs-chase.txt`, `blog__best-payroll-software-for-startups.txt`
