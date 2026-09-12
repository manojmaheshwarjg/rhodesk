# Rho Help Center: Operational Truths

Source corpus: 269 local files in `scratchpad/rho/pages/help/`, filename = URL path with `/` replaced by `__`.
Cross-checked against `all-urls.txt`: the sitemap contains exactly 270 `help-center` URLs (269 articles/indexes plus the `/help-center` root). **Every help-center URL in the sitemap is present locally. Nothing is missing.**

Every article body was extracted (nav chrome and the "Popular help center articles" footer stripped) into `scratchpad/rho/helpbody/` and read. Total extracted body text: ~918,000 characters.

Today is 2026-09-11. Rho stamps some facts "as of 08/02/2026" and Treasury yield footnotes "as of 09/11/2026" (i.e. today). Those as-of dates are carried through below.

Citation convention below: `[cat/slug]` maps to `pages/help/help-center__<cat>__<slug>.txt`.

---

## 1. Category census

269 files = 16 category index pages + 253 articles.

| Category | Total files | Index pages | Articles | Share of articles |
|---|---:|---:|---:|---:|
| payments | 33 | 1 | 32 | 12.6% |
| cards | 32 | 1 | 31 | 12.3% |
| general-rho-information | 30 | 1 | 29 | 11.5% |
| accounting | 28 | 1 | 27 | 10.7% |
| banking | 25 | 1 | 24 | 9.5% |
| expenses | 23 | 1 | 22 | 8.7% |
| bill-pay | 20 | 1 | 19 | 7.5% |
| admin | 16 | 1 | 15 | 5.9% |
| mobile-app | 15 | 1 | 14 | 5.5% |
| vendors | 13 | 1 | 12 | 4.7% |
| departments | 12 | 1 | 11 | 4.3% |
| treasury | 5 | 1 | 4 | 1.6% |
| the-rho-api | 5 | 1 | 4 | 1.6% |
| rho-slack-app | 5 | 1 | 4 | 1.6% |
| fields | 4 | 1 | 3 | 1.2% |
| invoicing | 3 | 1 | 2 | 0.8% |
| **Total** | **269** | **16** | **253** | **100%** |

Census signal, not just counts:

- Payments + cards + banking = 90 files (33%). The core money-movement surface is by far the most documented.
- **Treasury has 4 articles but the densest numeric content in the corpus** (fee tiers, cutoffs, asset behaviour, rebalancing). Low article count, high operational load.
- **Invoicing (2 articles) and fields (3 articles) are the newest surfaces.** Both read as freshly written and both contradict older categories (see §10).
- `the-rho-api` and `rho-slack-app` exist at 4 articles each and are almost entirely about *read-only* access. There is no write API documented anywhere in 269 pages.
- There is **no "Capital" category** despite Capital being a headline nav product. Capital gets exactly one article, filed under general-rho-information.
- There is **no "credit"/"underwriting" category**, no "security" category, and no "statements/documents" category. Those topics are scattered.

---

## 2. Hard limits (numeric caps)

| Limit | Value | Source |
|---|---|---|
| Outgoing domestic wire | $90 million per day | `[payments/transfer-limits]` |
| Outgoing international wire | $2.5mm per day | `[payments/transfer-limits]` |
| Incoming international wire | up to $10 million per day | `[payments/transfer-limits]` |
| Incoming ACH pull | $20 million/day, **$10 million per transaction** | `[payments/transfer-limits]` |
| Outgoing ACH push | $20 million/day aggregate | `[payments/transfer-limits]` |
| Linked external account transfer | $5 million per transaction (in and out) | `[payments/transfer-limits]` |
| Remote check deposit | "No limit", but >$15,000.00 in one business day triggers extra screening | `[payments/transfer-limits]`, `[payments/how-to-deposit-a-check]` |
| INR to businesses in India | 1.5 million INR per invoice daily | `[payments/inr-purpose-code-restrictions]` |
| PKR per transfer | 35,000,000 PKR | `[payments/how-to-transfer-funds-in-pakistani-rupees-pkr]` |
| Savings withdrawals | **six (6) per month**; unlimited transfers in | `[banking/understanding-rho-savings-accounts]` |
| Savings minimum deposit | $25,000 | `[general-rho-information/how-does-fdic-insurance-coverage-work]` |
| Savings minimum avg monthly balance to earn interest | $25,000 | `[banking/understanding-rho-savings-accounts]` |
| Merchant allow-list per card | up to **20 distinct merchants** (as of 08/02/2026) | `[cards/understanding-rho-card-controls]`, `[cards/why-was-my-rho-card-declined]` |
| Company-wide merchant restrictions | unlimited **categories**, up to **20 specific merchants** | `[cards/how-to-set-company-wide-merchant-restrictions]` |
| Multi-transaction dispute | up to **15 transactions** per submission | `[cards/how-to-dispute-a-transaction-on-a-rho-card]` |
| Check attachment | 1 PDF per check, **6 pages max, 15 MB max**, PDF only | `[payments/how-to-send-a-physical-check]` |
| Bill Pay inbox file size | **<50MB per file**, unlimited attachments per email | `[bill-pay/rho-bill-pay-inbox-overview]` |
| W-9 upload | PDF only, **15 MB max** | `[vendors/how-to-collect-w-9s-with-rho]` |
| Application document upload | **10 MB max** | `[general-rho-information/applying-to-rho-faqs]` |
| Invoice card payments | **$10,000 per day across all invoices** | `[invoicing/accept-card-payments-on-invoices]` |
| Custom attributes | up to **5** | `[accounting/how-to-set-up-custom-fields-in-rho]` |
| Fields (newer system) | up to **7 active**; archived ones do not count | `[fields/understanding-fields-in-rho]` |
| Auto-transfer rules | **5 active rules per organization**, one rule per account pair, one rule per source account | `[treasury/setting-up-auto-transfer-rules]` |
| Vanguard allocation | capped at **50% of portfolio** (VFSTX + VFSUX combined) | `[treasury/about-rho-treasury]` |
| T-Bill purchase increment | **$1,000**; sub-$1,000 proportional remainder held as cash | `[treasury/managing-your-rho-treasury-account]` |
| Portfolio allocation granularity | **5% increments, must total 100%** | `[treasury/managing-your-rho-treasury-account]` |
| Standalone Invoice Generator | **5 line items max**, logo 2 MB, file 10 MB, JPEG/JPG/PNG | `[general-rho-information/invoice-generator-technical-guide]` |
| Monthly Terms qualification | **$25,000 minimum cash balance** | `[cards/the-rho-card-with-monthly-terms-2]` |
| Treasury eligibility | **$50,000 minimum in total deposits** | `[treasury/about-rho-treasury]` |
| Rho Platinum 2% cashback | first **$1 million** in eligible spend per calendar year | `[general-rho-information/rho-platinum-what-it-is-and-how-to-qualify]` |
| Rho Capital line size | "up to $5M+, subject to underwriting" | `[general-rho-information/about-rho-capital]` |
| Card virtual/physical count | explicitly **unlimited** | `[cards/employee-card-faqs]` |
| Secondary checking accounts | explicitly **unlimited** | `[general-rho-information/our-partnership-with-webster-bank-n-a-member-fdic]` |

---

## 3. Time windows and cutoffs

| Window | Value | Source |
|---|---|---|
| Cancel any initiated payment | **30 minutes** after initiation, before release | `[payments/how-to-cancel-reverse-or-dispute-a-bank-transfer]` |
| ACH recall after settlement | generally possible within **2 business days** | same |
| Successful recall return of funds | **up to 4 weeks** | same |
| Scheduled payment release | **~4:00 am ET** on the due date | `[payments/what-time-are-scheduled-payments-sent-out]` |
| Approval deadline for a scheduled payment | before **4 am ET** on the due date, or it does not release | same |
| Outgoing ACH same-day | created before **2 pm ET** AND under $1mm | `[payments/payment-settlement-times]` |
| Outgoing domestic wire same-day | created before **4:45 pm ET** | same |
| Card repayment ACH cutoff | **2:00 pm ET** same-day processing; settles up to 4 business days | `[cards/how-to-pay-your-credit-card-balance]` |
| Reimbursement payout same-day | submitted before **3 p.m. ET** | `[expenses/how-to-approve-and-disburse-a-reimbursement-request]` |
| Checking to Savings same business day | created before **1 PM ET** | `[banking/how-the-rho-savings-sweep-works]` |
| Treasury IJTXX withdrawal same day | **3:00 PM ET** | `[treasury/managing-your-rho-treasury-account]` |
| Treasury T-Bill sale cutoff | **5:00 PM ET**, next business day | same |
| Treasury MULSX / VFSUX cutoff | **4:00 PM ET**, 1 to 2 business days | same |
| ADM sweep deposit cutoff | received by Custodian before **12:00 P.M. Central** deposits with Program Institutions the **next** business day | `[general-rho-information/rho-savings-account-terms-and-conditions]` |
| ADM withdrawal processing days | **Tuesdays and Thursdays only**, settling Wednesdays and Fridays | same |
| Auto-transfer rule evaluation | **8:00 a.m. ET** on business days | `[treasury/setting-up-auto-transfer-rules]` |
| Recurring accounting syncs | **3:00 AM ET (8:00 AM UTC)** | `[accounting/setting-up-recurring-syncs-to-automate-your-accounting-integration]` |
| Xero bank feed sync | daily at **3:00 AM EST** | `[accounting/how-to-set-up-rhos-xero-integration]` |
| Bill sync from accounting platform | every **24hrs at ~12AM EST** | `[bill-pay/how-rho-syncs-bill-pay-data-in-your-accounting-system-]` |
| Mastercard Smart Data card feed | **1 time per day, Monday to Saturday after 5 PM EST** | `[cards/how-to-set-up-a-card-feed-integration]` |
| Bill Pay daily digest | **5pm EST** daily, only if 1+ update | `[bill-pay/how-to-configure-bill-pay-notifications]` |
| Bill Pay weekly digest | **10 am EST Friday**, only if 1+ update | same |
| Slack daily balance alert | **9:00 AM ET** default | `[rho-slack-app/how-to-set-up-rho-alerts-in-slack]` |
| Secure card-details link | single view, expires in **72 hours** if unopened | `[cards/how-to-share-card-details]`, `[mobile-app/how-to-securely-share-your-card-details-in-the-mobile-app]` |
| Vendor notification attachments | expire after **7 days** | `[payments/how-to-set-up-vendor-payment-notifications]` |
| Single-use vendor card window | **14 days** (editable in Card Settings) | `[bill-pay/paying-bills-with-vendor-cards-single-use]` |
| Uncashed check auto-void | **90 calendar days** | `[payments/understanding-rho-check-mechanics]` |
| Card expiry behaviour | active through the **entire month** of expiry, canceled on the **1st of the following month** | `[cards/card-expiration-and-renewal]` |
| Card default lifetime | **3 years from issue date** | `[cards/understanding-rho-card-controls]` |
| Flagged ACH debit hold | **8 hours** to approve or reject, then the default action applies | `[banking/manage-your-ach-debit-approvals-in-rho-beta-]` |
| W-9 vendor portal | live for **60 days**, then expires and must be resent | `[vendors/how-to-collect-w-9s-with-rho]` |
| Dispute determination | **45 to 90 days**, managed by Mastercard | `[cards/how-to-dispute-a-transaction-on-a-rho-card]` |
| Slack workspace connection | lapses after **30 days without use** | `[rho-slack-app/how-to-install-and-connect-the-rho-slack-app]` |
| Slack statement download link | works for **about 15 minutes** | `[rho-slack-app/how-to-use-the-rho-slack-app]` |
| Slack sign-in grace | sign in within **15 minutes** and your original question is answered automatically | same |
| Treasury ACAT lockout | no adds or withdrawals for **up to 90 days** once initiated | `[treasury/understanding-rho-treasury]` |
| Rho Switch bank analysis | last **120 days**; switch data deleted ~**120 days** after collection | `[banking/switch-your-business-banking-to-rho]` |
| Incorporation fee clawback window | keep daily average balance $10,000 above starting point for **60 days** | `[general-rho-information/incorporating-your-company-with-rho]` |
| Rho Capital repayment | terms **up to 180 days per draw**; funds land in ~**48 hours** | `[general-rho-information/about-rho-capital]` |
| QuickBooks disconnect | after disconnecting, transactions **older than 90 days may no longer be downloadable** | `[accounting/consolidating-your-quickbooks-integration]` |
| Expenses default view | last **60 days** | `[expenses/how-to-filter-and-set-custom-views-in-expenses]` |

---

## 4. Forty-plus specific operational facts (numbered, with source page)

Facts that a marketing page would never tell you.

1. **Same-day scheduling is silently broken by design.** A payment scheduled on its own due date "will not be released, nor will it default to the next business day automatically. Instead, that payment will be marked as overdue in your Scheduled Payments Tab." `[payments/what-time-are-scheduled-payments-sent-out]`
2. **Bill Pay bills dated Saturday or Sunday never send** and show as overdue. This restriction applies to Bill Pay bills only, not to Banking transfers. Same page.
3. **Recurring transfers cannot be edited at all.** "Unfortunately, you cannot edit a recurring transfer. If you wish to make changes, you will need to cancel the current one and create an entirely new recurring transfer." `[payments/how-to-edit-or-cancel-a-recurring-or-scheduled-payment]`
4. **Recurring frequency is unavailable for Savings transfers.** The frequency dropdown "is not available for transfers to and from the Savings account." `[payments/how-to-create-an-internal-transfer]`
5. **Month-end recurring rollover rule:** a monthly recurring payment set on Jan 31 executes Feb 29, Mar 31, Apr 30 (i.e. clamps to the last day of a short month) and executes on the exact date "regardless of whether it's a weekend or not." `[payments/how-to-send-a-transfer-from-rho]`
6. **You cannot move money between two Rho businesses internally, even if you own both.** The documented workaround is to create Company B as a vendor of Company A and send a domestic wire. `[payments/how-to-create-an-internal-transfer]`
7. **Rho's own routing number is published in the help center: 021913655.** It is required in the digital-check endorsement block. `[payments/how-to-deposit-a-check]`
8. **Digital check deposits require an exact endorsement string**: "Pay to the order of Webster Bank, a division of Santander Bank, N.A. For Mobile Deposit Only" plus company name, Rho routing number, last 4 of the checking account, and the current date. Same page.
9. **Rho will not process checks sent by mail or delivered in person.** "Checks sent by mail or delivered to our offices or any of our partner bank's offices or branches will not be processed." Same page.
10. **Non-US checks cannot be deposited at all.** "Our system processes only U.S. checks with 9-digit ABA numbers." Same page.
11. **Outgoing checks are pre-funded like a cashier's check but are not one.** Funds are set aside immediately and drawn from an account separate from your Rho account, but "Rho checks are only accepted at locations that accept corporate checks, not cashier's checks." `[banking/does-rho-offer-paper-check-books]`
12. **Voiding a check does not stop the mail.** "past the 30-minute cancellation window, the recipient may still receive the voided physical check in the mail." `[payments/how-to-cancel-reverse-or-dispute-a-bank-transfer]`
13. **Failed/returned domestic wires cost the customer $20 to $45**, deducted from the Rho account (as of 08/02/2026). This is the only stated bank-style fee outside FX. `[payments/fees-for-recalls-failed-wires]`, `[payments/why-did-my-payment-fail-stall-or-get-canceled]`
14. **Wires cannot be sent to PO Box addresses**, domestic or international, because of BSA physical-address requirements. `[payments/can-i-send-a-wire-to-a-vendor-with-a-po-box-address]`
15. **Physical Rho cards cannot ship to PO Boxes either**, but they can ship internationally using the same flow. `[cards/how-to-create-a-new-rho-card]`
16. **The "no fees" claim has a $15 exception.** Absorbing recipient/correspondent/intermediary/SWIFT fees on an international USD wire costs "a flat rate of $15." `[payments/how-to-send-an-international-wire]`, restated "as of 08/02/2026" in `[bill-pay/paying-international-bills-in-bill-pay]`
17. **Four currencies leave the tracking grid.** "Certain currencies including IDR, PHP, INR, and MYR are processed via local payments rails, not the SWIFT network... we have limited visibility on the payment and cannot provide tracking information." `[payments/how-to-send-an-international-wire]`
18. **GBP SWIFT payments are unsupported** (listed inline in the currency table as "GBP (SWIFT payments currently unsupported)"). 22 currencies total are supported. `[payments/which-countries-and-currencies-are-supported]`
19. **Qatar can only receive EUR or GBP; USD is unsupported.** `[payments/restricted-countries-and-international-payment-types]`
20. **Seven country/currency corridors are business-blocked but individual-allowed:** BDT, BRL, COP, TZS, PKR, UAH all say "Payments to businesses are currently not supported"; only Western Sahara (MAD) supports both. Same page.
21. **PKR has three stacked constraints:** personal accounts only, 35,000,000 PKR cap per transfer, and named bank products that will reject or trap funds (Meezan Bank Express, Allied Bank Express, and Asaan accounts capped at 500,000 PKR). `[payments/how-to-transfer-funds-in-pakistani-rupees-pkr]`
22. **INR purpose codes are a whitelist of four**: Travel expenses, Property purchase (B2C only), Pay for services, Pay for goods. Charities, trade transfers over 1.5M INR, FDI and employee payments are refused. `[payments/inr-purpose-code-restrictions]`
23. **Eleven industries are barred from international payments entirely** even with a live Rho account, including CBD, carbon credits, cryptocurrencies, precious metals, and political organizations. `[payments/restricted-countries-and-international-payment-types]`
24. **A previously-successful corridor can still be frozen.** "Because screening is per-payment, a transfer that has gone through many times before can still be selected for review. That is normal, even though it can feel arbitrary." Rho support explicitly "can't do... skip or override a compliance requirement." `[payments/why-is-my-international-payment-under-review]`
25. **Vendors can pull from your Rho account with zero controls by default.** "There are currently no restrictions on Rho's end, and vendor numbers do not require whitelisting to complete the pull." `[payments/can-my-vendors-pull-funds-from-my-rho-account-via-ach]`
26. **The fix for #25 is in closed beta and must be requested.** "ACH debit authorizations are currently in beta. If you don't see this feature in your Rho account and would like access, contact Rho Client Services." New accounts default to **Automatically approve** flagged debits. `[banking/manage-your-ach-debit-approvals-in-rho-beta-]`
27. **ACH authorization matches on ACH Company ID, not counterparty name, and that is leaky.** "One ACH Company ID can be used by more than one counterparty... If you authorize a counterparty that uses a shared ID, other counterparties that use the same ID may also be allowed." Same page.
28. **Rejected debits are irreversible:** "Rho cannot bring back a debit that was already returned." Same page.
29. **A card limit of "0" means no limit.** "When you enter '0' as the card limit, it implies that the card has no spending limit." A warning modal appears but the semantics are inverted from intuition. `[cards/how-to-edit-the-spending-limit-on-a-rho-card]`
30. **Card usage end dates are exclusive.** "The card can be used up to the day before the date defined here. Transactions will be declined starting on the end date." `[mobile-app/how-to-view-and-edit-your-card-controls-in-the-mobile-app]`
31. **Fixed-limit cards auto-lock themselves.** "When transactions on a fixed limit card have fully settled, the card will automatically lock to help prevent additional spend." `[cards/understanding-rho-card-controls]`
32. **Every card is hard-wired to the primary checking account.** "By default, your Rho cards are tied to your primary Rho Checking Account. If you have sub-accounts, the spend is tied to the primary account, and this can't be changed." `[cards/how-to-update-your-card-settings]`
33. **Raising a limit never raises spending power.** On Daily Terms spend is capped by available checking balance; on Monthly Terms by the account credit limit. "Changing a user or card limit does not increase your available balance." `[cards/why-was-my-rho-card-declined]`, `[admin/how-to-set-monthly-user-limits]`
34. **Filing a fraud dispute auto-cancels the card.** "The dispute process for fraud triggers an automatic cancellation of the affected Rho Card." Non-fraud disputes (billing error, duplicate charge) leave the card active. `[cards/employee-card-faqs]`, `[cards/how-to-dispute-a-transaction-on-a-rho-card]`
35. **Replying NO to an SMS fraud alert instantly and irreversibly cancels the card.** Replying YES lifts the block and you can retry the purchase. `[general-rho-information/how-to-enable-sms-notifications-for-suspicious-transactions]`
36. **Removing a user silently kills their cards.** "Removing a user automatically cancels any cards issued to them. This includes both physical and virtual cards." `[admin/how-do-i-remove-a-team-member-from-my-rho-account]`
37. **Deleting a vendor profile cancels every vendor card linked to it.** `[cards/how-to-create-and-manage-vendor-cards-with-rho]`
38. **Physical cards can only be activated by the QR code in the mailer or in-platform.** No phone-line activation is documented. `[cards/employee-card-faqs]`
39. **No cash, ever.** No ATM withdrawals, no cash advances, no cash transfers, no push-to-debit. `[cards/employee-card-faqs]`
40. **No PINs on Rho cards**, with a documented workaround script for POS terminals that demand one ("press continue or bypass PIN"). Same page.
41. **International card spend earns zero cashback** even though international spend is on by default and there is no FX fee. Same page.
42. **Four cashback exclusion buckets**: Walmart Inc. and affiliates; utilities MCCs; money transfer/digital payment/quasi-cash MCCs; and anything "made or authorized outside the U.S." `[cards/understanding-card-cashback]`
43. **Late payment forfeits that statement period's rewards entirely**, and refunds/disputes claw rewards back out of later periods. `[banking/rewards-account-overview]`
44. **Savings insurance is an administered sweep run by a third party, American Deposit Management (ADM)**, across "400+ FDIC- and NCUA-insured institutions (as of August 2026)." `[banking/how-the-rho-savings-sweep-works]`
45. **The Savings T&C page is the ADM master services agreement and it contains harsher mechanics than the marketing page.** Withdrawals are processed only on Tuesdays and Thursdays for Wednesday/Friday settlement; requests over **$3,000,000** are "special handling" settled "at a mutually acceptable Settlement Day"; deposits received before 12:00 P.M. Central deposit with Program Institutions only on the *next* business day. `[general-rho-information/rho-savings-account-terms-and-conditions]`
46. **By signing, the client "expressly waives extended deposit insurance."** ADM only uses "commercially reasonable efforts" to keep any one institution under $250,000, and explicitly warns that intraday or overnight, "the entire amount of the withdrawal or deposit may be held at one Program Institution." Same page.
47. **All non-public-unit Savings clients must represent they are an "accredited investor."** Same page.
48. **Sweep accounts have no check writing, ATM, or debit card privileges**, and the network institution list is not published: "The current list of network institutions is available from Rho support on request." Same page and `[banking/how-the-rho-savings-sweep-works]`
49. **Checking FDIC coverage is $250,000 per customer across ALL Rho checking accounts**, not per sub-account, despite "unlimited secondary checking accounts" being a marketed feature. `[banking/how-to-set-up-multiple-operating-accounts]`
50. **DACA support is partial:** "Rho currently offers only Springing DACAs... Rho does not support fully-blocked DACA at this time." `[banking/does-rho-support-daca-accounts]`
51. **Virtual Account Numbers (VANs) exist and are barely marketed.** They are credit-only ("cannot be used to initiate payments or withdraw funds"), live in the Account Details drawer, and are excluded for DACA accounts. `[banking/how-to-find-your-routing-or-account-number]`
52. **Linked-account pulls require an exact name match on a business account.** "Personal accounts cannot be used for linked-account pulls." `[payments/how-to-connect-to-an-external-bank-account]`
53. **You cannot hold two live connections to the same external institution for different use cases** (transfers vs credit verification). Same page.
54. **A linked external account is not a payment destination.** To send money to your own bank you must additionally add it as a vendor. Same page, and `[payments/how-to-send-a-transfer-from-rho]`
55. **Sub-accounts cannot be linked individually** to an external bank; linkage is at the whole-Rho-account level. Same page.
56. **Micro-deposit verification is a support-gated fallback**, not a self-serve option: "please email our support team at clientservice@rho.co with your request, and we will activate it." It uses a $0.00 deposit carrying a verification code, delivered by SMS via Plaid, and takes 1 to 2 business days. `[banking/how-to-set-up-micro-deposits]`
57. **Rho tells you it probably cannot find your missing incoming payment.** "Rho is unlikely to be able to track incoming payments. We recommend contacting the sending bank directly." `[payments/how-to-fund-your-account]`
58. **Treasury management fees are tiered and undisclosed on the pricing page:** 0.60% under $2M, 0.45% $2M-$5M, 0.35% $5M-$10M, 0.25% $10M-$20M, 0.15% $20M+. AUM for tiering "includes the combined balance of your Rho Checking and Treasury accounts." `[treasury/managing-your-rho-treasury-account]`
59. **If your Treasury cash is insufficient to pay the fee, Rho sells your holdings to cover it** without asking. `[treasury/about-rho-treasury]`
60. **Treasury withdrawals are never split across assets and you cannot choose what is sold.** If a withdrawal exceeds your same-day IJTXX balance, "the full amount comes from your other assets instead," sold FIFO. `[treasury/managing-your-rho-treasury-account]`
61. **Automatic monthly rebalancing fires on the 6th if any holding drifts >5% from target**, takes 2 to 4 business days, and **locks you out of portfolio changes while it runs**. Same page.
62. **Treasury is running a live custody migration.** "If you joined Rho Treasury on or after July 23, 2026, your account is on Ascend... If you joined before July 23, your account will migrate to Ascend in the coming months." VFSUX and the IJTXX money-market sweep are unavailable to pre-migration accounts. `[treasury/understanding-rho-treasury]`
63. **Treasury → Checking auto-transfers only run on preset cadences (weekly, twice monthly on the 11th and 25th, or monthly)** because liquidation takes up to 3 business days. Custom schedules exist only for Checking-to-Checking. `[treasury/setting-up-auto-transfer-rules]`
64. **Legacy Treasury sweep rules were silently migrated** from "every day at 8:00 AM ET, if Checking falls below $250,000 transfer at least $25,000" to a weekly Thursday-settlement rule, and the top-up amount changed: rules now "transfer only the amount needed to restore your account to its minimum balance." Same page.
65. **One Treasury account can fund only one Checking account.** Same page.
66. **Treasury holdings do not generate a monthly statement unless there were deposits, withdrawals, or trades.** "Dividends, interest, and changes in market value do not count as qualifying activity." Otherwise you get a combined quarterly statement. `[treasury/understanding-rho-treasury]`
67. **Expense rules are explicitly post-spend and cannot block a card.** "these are post-spend controls, meaning Expense rules will not cause Rho Cards to get declined." `[expenses/how-to-create-rules-for-expenses]`
68. **Expense approval tier amounts are immutable.** "Once you create an approval tier, you won't be able to change the amount. To make changes, you can create a new tier and delete the old one." `[expenses/how-to-set-up-approvals-for-expenses]`
69. **Reimbursements are ACH-only, domestic-only, checking-only.** "Reimbursements can only be sent to checking accounts. Savings accounts are not supported at this time." `[expenses/how-to-submit-a-reimbursement]`
70. **Archiving a reimbursement is permanent.** "archiving is permanent and cannot be undone." `[expenses/how-to-archive-a-reimbursement-request]`
71. **Mileage is prefilled at the IRS rate of $0.70/mile** and is calculated "using the rate your business set when the expense occurred," not the current rate. `[expenses/how-to-use-mileage-reimbursements]`
72. **Receipt uploads by SMS require a US or Canada mobile number** and go to short code **555746**; email receipts go to **receipts@rho.co**. `[cards/how-to-attach-receipts-to-card-transactions]`
73. **Replying with a second receipt to a transaction that already has one returns an error**; replacement is desktop-only. Same page.
74. **The Gmail connector is per-cardholder, not per-company**, and "Receipts pulled from a cardholder's inbox are only attached to that cardholder's transactions." `[expenses/how-to-set-up-the-gmail-connector]`
75. **Bill Pay inbox rejects spreadsheets.** Supported: JPG, JPEG, PNG, HEIC, PDF. "NOT supported: CSV, XLS, etc." W-9s, payment instruction files and statements are also rejected as bills. `[bill-pay/rho-bill-pay-inbox-overview]`
76. **Replying in a thread to the Bill Pay inbox creates duplicate invoices** when image files sit in the email body. They are auto-flagged as duplicates. `[bill-pay/understanding-ocr-technology-at-rho]`
77. **Bills from an unknown sender are invisible until manually approved**, and "rejecting does not mean blocking the sender." `[bill-pay/how-to-manage-your-bill-pay-inbox-and-known-senders]`
78. **Bill sync from QuickBooks has five silent eligibility filters**: open and unpaid, total > $0, at least one line item, **not more than 30 days old**, and vendor active in Rho and mapped. `[bill-pay/how-to-enable-bill-sync-from-your-accounting-software]`
79. **Key bill fields are frozen after the first sync.** "key data points like amount, vendor, due date, invoice # are not mutable after the first sync. Please either edit the details directly in the accounting platform or Void the bill & recreate." `[bill-pay/how-rho-syncs-bill-pay-data-in-your-accounting-system-]`
80. **Bill Pay cannot send a non-USD international wire.** The documented path is to pay from Banking and then "Mark as Paid" in Bill Pay, which archives the bill as "Paid Externally." `[bill-pay/paying-international-bills-in-bill-pay]`
81. **Bulk payments support domestic wires only** and cannot include international wires. Bookkeepers "cannot execute payments from the Bulk Payments workflow" by default. `[bill-pay/understanding-bulk-payments]`
82. **Single-use vendor cards are nicknamed programmatically:** `[Payee Name] AP Card: [Invoice Number]`. They carry a 14-day usage window and go Canceled after one charge, but details stay viewable. `[bill-pay/paying-bills-with-vendor-cards-single-use]`
83. **Vendor cards are web-only.** "Vendor cards are currently a web-only feature, so they won't appear in the mobile app." `[cards/how-to-create-and-manage-vendor-cards-with-rho]`
84. **Bulk vendor upload is not a product, it is a support ticket.** "The Rho Client Service team performs this functionality on your behalf," domestic payments only, one payment method per vendor, 1 to 2 business days turnaround. `[vendors/how-to-bulk-upload-vendors]`
85. **Rho documents "delete and re-create" as the supported fix for a stuck vendor profile.** "If the profile has everything but still won't activate, the reliable fix today is to delete the profile and re-create it... We know this is not elegant, it is the fix that works." `[vendors/troubleshooting-vendor-profiles-incomplete-status-and-duplicates]`
86. **Rho has five vendor-creation paths and warns they collide.** Manual, invite, AP-inbox auto-draft, support bulk upload, and Merchant-to-Vendor auto-creation. "duplicates created inside Rho by dual entry paths must be cleaned up yourself." Same page.
87. **HSBC Hong Kong needs three undocumented-elsewhere hacks**: zip code `000000`, SWIFT `HSBCHKHHXXX` "(instead of the one provided)", and stripping the letters "HK" from the beneficiary account number. `[vendors/how-do-i-set-up-a-vendor-payment-type-for-hsbc-in-hong-kong]`
88. **Rho does not file 1099s.** It exports W-9 data to CSV for "the 1099 filing provider of your choice." Only 2023 1099-MISC/NEC PDFs remain on vendor profiles from a discontinued service. `[vendors/rho-1099-filing-support]`
89. **Invoice card acceptance costs 2.9% + $0.30 per transaction, paid by the business, with no surcharging allowed.** "surcharging is not currently available." `[invoicing/accept-card-payments-on-invoices]`
90. **Invoice card payments are capped at $10,000/day across all invoices**, and once the cap is hit the card option simply disappears from further invoices. Same page.
91. **You cannot bring your own Stripe account.** "you can't connect an existing Stripe account. Rho creates and manages a separate account for your business, so payout details and Payment Portal settings can't be changed directly in Stripe." First card payment deposits "may take up to two weeks." Same page.
92. **Invoice card payments only work for one-time, full-amount USD invoices.** Partial payments, overpayments, recurring invoices and non-USD invoices are bank-transfer only. Same page.
93. **Invoice syncing to accounting is QuickBooks Online only**, and unpaid invoices still do not sync: "syncing unpaid invoices is not yet supported. This feature is currently in development." `[accounting/syncing-invoices-to-your-accounting-software]`, `[accounting/setting-up-recurring-syncs-to-automate-your-accounting-integration]`
94. **Mapping rules resolve in a fixed hierarchy:** Label, Sender, Vendor, Merchant, Card, Department, with "the more complex rule" winning ties. `[accounting/how-does-coding-in-rho-work]`
95. **Mapping rules are forward-only, but "Apply Mappings" is a destructive bulk override.** "this action will override all manual coding." `[accounting/how-to-create-mapping-rules-in-rho]`
96. **Merchant-to-Vendor is off by default, fires after more than three transactions with a merchant, runs on a 6-hour batch, and ignores all history before the toggle.** It is unavailable on the QuickBooks and Xero bank feeds. `[accounting/creating-vendors-from-merchants]`
97. **Deleting the auto-created chart-of-accounts entry breaks the integration.** "You can rename this account, but integration between your Rho account and QuickBooks will not work if the account is deleted." Same rule stated for NetSuite. `[accounting/how-to-set-up-rhos-quickbooks-integration]`, `[accounting/how-to-set-up-rhos-netsuite-integration]`
98. **Running both the QuickBooks bank feed and the direct integration duplicates transactions**, and the bank-feed token "can only be revoked by the user who created it." `[accounting/quickbooks-bank-feed-vs-direct-integration]`, `[accounting/consolidating-your-quickbooks-integration]`
99. **Sage Intacct cannot carry projects or jobs.** "if your transaction requires a 'project' or 'job' to be entered in Sage, we are unable to support it syncing over from Rho at this time." `[accounting/how-to-set-up-rhos-sage-intacct-integration]`
100. **NetSuite setup exposes internal plumbing**: bundle ID **436739**, script `rho_production.js`, callback URL `https://api.rho.co/webhook/netsuite_authorize_callback`, current bundle version **1.01**. `[accounting/how-to-set-up-rhos-netsuite-integration]`, `[accounting/update-your-netsuite-bundle-on-rho]`
101. **Treasury transactions sync only to QBO and NetSuite, and receipts never sync for Treasury.** `[accounting/how-to-sync-rho-transactions-with-your-accounting-software]`, `[accounting/how-to-sync-to-quickbooks]`
102. **Rho publishes a 32-row accounting sync error catalogue**, including closed-period rejections, locked transactions, split-amount mismatches, ERP subscription-tier failures, and "Reimbursements must have a single vendor for all transactions." `[accounting/guide-to-solving-accounting-issues]`
103. **Rho Close (the AI coder) is toggled ON by default**, is limited to direct integrations (QuickBooks, NetSuite, Puzzle, Sage Intacct), will not touch attributes that already have a value, and **applies un-dismissed suggestions if you sync without reviewing them**. `[accounting/what-is-rho-close]`
104. **Zelle, Payoneer, Abacus and Cash App are explicitly unsupported.** Venmo works but "may charge additional fees," and PayPal charges "may be deemed non-disputable." `[accounting/rhos-supported-cash-flow-apps]`
105. **PayPal linking requires a UI hack:** "you will need to type in any mix of letters (eg. abcdefghi) in the search bar in order to prompt the option 'Don't see your bank here?'" `[payments/transfer-faqs]`
106. **2FA is mandatory on every login, and the mobile app cannot reset a password.** "The Rho mobile app does not support the password-reset flow." Phone number changes must go through clientservice@rho.co. `[general-rho-information/how-to-log-in-to-rho-and-fix-login-issues]`, `[admin/how-to-reset-an-employees-passwords]`
107. **Google SSO is the only SSO.** No SAML, Okta, Entra or SCIM appears anywhere in 269 pages. `[admin/managing-google-sso-for-your-organization]`
108. **Monthly user limits are dead.** "Monthly user limits are a legacy feature that's no longer enabled by default. Monthly user limits are no longer part of Rho's standard offering." The article documenting them still exists. `[admin/how-to-set-monthly-user-limits]`
109. **Account Owner and Administrator permissions are neither editable nor duplicable**, and role deletion plus user deletion are both permanent. `[admin/how-to-manage-users-and-roles-in-rho]`
110. **The Investor role, described as "predominantly view only," can create transactions in the banking tab.** Same page.
111. **A user can be added without a phone number but then cannot activate a card or complete mandatory 2FA.** Same page.
112. **HRIS sync is read-only, manual, and one-at-a-time.** Syncs are "triggered in-app," at most every 24 hours; "Rho supports connecting one HR integration at a time"; "Rho never modifies any data or information in your HRIS"; and "Rho does not extract any compensation information." 50+ providers. `[admin/how-to-use-rhos-hris-integrations]`
113. **The Rho API is read-only, period.** Scopes cover accounts, transactions, statements. Connected AI tools "cannot: Move money; Issue, lock, or edit cards; Add or manage users; Make changes to your Rho account." `[the-rho-api/build-a-custom-integration-with-rho]`, `[the-rho-api/what-connected-al-tools-have-access-to-in-your-rho-account]`
114. **API access tokens are shown exactly once** and require 2FA at creation. OAuth partner registration goes through `api-partner-request@rho.co`. `[the-rho-api/connecting-al-tools-to-your-rho-account]`
115. **The Slack app dies of inactivity.** "Connections lapse after 30 days without use." It refuses public channels ("If it is invited to one, it says so and removes itself"), and is available to Account Owners and Admins only today. `[rho-slack-app/how-to-install-and-connect-the-rho-slack-app]`, `[rho-slack-app/understanding-the-rho-slack-app]`
116. **Slack agent chat is in beta for select businesses**, answers channel questions by DM, and is read-only. `[rho-slack-app/how-to-use-the-rho-slack-app]`
117. **Incorporation costs $400, refundable only on deposit behaviour:** credited back after depositing $10,000 of new money and keeping the daily average balance $10,000 above the starting point for 60 days. Accelerator-introduced founders pay $1,000 (the page reads as a different clawback threshold, stated without further explanation). Delaware C-corps only; ~80% of filings complete within 24 hours. `[general-rho-information/incorporating-your-company-with-rho]`
118. **Rho Capital is underwritten and funded by a different bank than Rho's deposits:** "Business-purpose loans made by Lead Bank," with "consent to obtain personal credit report is required" and "Personal Guaranty may be required." `[general-rho-information/about-rho-capital]`
119. **Rho Platinum requires all four of: payroll runs from Rho, revenue lands in Rho, 50%+ of company assets at Rho, and an active Rho Corporate Card.** It is dynamic: "If your account no longer meets the qualifications, your Cashback rate returns to the standard rate." `[general-rho-information/rho-platinum-what-it-is-and-how-to-qualify]`
120. **Rho does not run payroll.** "Rho does not run payroll natively." The setup is a funding-account swap only, verified by Plaid or 2 to 3 business-day micro-deposits. `[payments/how-to-setup-payroll-with-rho]`
121. **Virtual office addresses are refused at application.** "Virtual addresses from Regus or any other provider are not permitted." A registered-agent address still requires a physical operating address. `[general-rho-information/applying-to-rho-faqs]`, `[general-rho-information/can-i-change-my-business-address]`
122. **Business address changes are email-only and require a stated reason.** "Send an email to clientservice@rho.co from your registered email with your previous address, your desired new address, and a brief explanation for why your address is changing." Same page.
123. **Fourteen industries are barred from opening an account at all**, including drug stores/pharmacies and cannabis, online dating services, firework sales, bearer shares, and "Nested MSBs/Nested money transmitters." `[general-rho-information/business-and-industry-eligibility-at-rho]`
124. **Account closure is Account-Owner-only and gated on a zero card balance.** Dashboard access ends at closure, so statements must be exported first; Treasury liquidation adds 2 to 3 business days; the remaining balance comes back by wire or check. `[general-rho-information/how-to-close-your-rho-account]`
125. **Navan receipts do not round-trip.** "Adding receipts in Rho will not sync them to Navan." Policies must live in Navan; only card-level controls stay in Rho; the link is Mastercard Smart Data via a "Mastercard Distribution ID." `[general-rho-information/understanding-the-integration-between-rho-and-navan-expense]`
126. **The Rewards Marketplace is a third-party portal (Built First) with its own login**, and Rho warns: "do not use your Rho password credentials when creating your Built First login." `[general-rho-information/rhos-rewards-marketplace]`
127. **Cashback is asserted non-taxable with no 1099.** "Cashback from Rho is not considered taxable and we do not issue 1099s for cash back." [Rho claim, tax position] `[admin/are-cashback-rewards-taxable]`
128. **The Expenses CSV will never tie to the card statement**, by design: it includes pending charges and excludes merchant refunds and Mastercard credits. `[cards/employee-card-faqs]`
129. **The running-balance CSV only works one account at a time and only when filtered to SETTLED.** Selecting "All Accounts" leaves the Balance column blank. `[banking/how-to-view-your-running-checking-account-balance]`
130. **Transaction type and status enums are published**: types `ACH-US`, `CHECK`, `EXTERNAL`, `INTERNAL`, `RDC`, `WIRE-DOM`, `WIRE-INT`; status codes `A` Awaiting Approval, `C` Canceled, `P` Pending, `Q` Queued, `R` Rejected, `S` Settled. `[banking/understanding-transaction-tables]`, `[banking/understanding-transaction-details]`

---

## 5. Features that exist but are not marketed

| Feature | What it actually is | Source |
|---|---|---|
| ACH debit authorizations | Per-counterparty ACH debit allow-list with limits, MFA-gated, 8-hour hold. **Beta, request-only.** This is the control that makes fact #25 tolerable. | `[banking/manage-your-ach-debit-approvals-in-rho-beta-]` |
| Virtual Account Numbers (VANs) | Credit-only receiving numbers for fraud isolation, in the mobile Account Details drawer | `[banking/how-to-find-your-routing-or-account-number]` |
| Springing DACAs | Lender control agreements over the operating account, for receivables/inventory-backed lines | `[banking/does-rho-support-daca-accounts]` |
| FedWire Drawdown | Payroll providers can pull by wire; set up only by emailing clientservice@rho.co | `[payments/can-i-set-up-reverse-fedwires-from-my-account]` |
| Rho Switch | Plaid/statement-driven bank-switch tool with a **Rho Chrome extension** that updates providers on your behalf | `[banking/switch-your-business-banking-to-rho]` |
| Card feed via Mastercard Smart Data | Push Rho card data into third-party T&E (Navan and others); needs a Delivery ID and 3 to 5 business days | `[cards/how-to-set-up-a-card-feed-integration]` |
| 1Password integration | "Save in 1Password" button on card details | `[general-rho-information/1password-integration-overview-setup]` |
| Bank Letter | Self-serve proof-of-account letter at Settings → Documents → Bank Letter, emailable to a third party | `[banking/how-to-get-a-proof-of-account-document]` |
| Rho Close | Suggestion engine for accounting attributes, **on by default** | `[accounting/what-is-rho-close]` |
| Fields | A newer, simpler replacement for Departments/Labels/Custom Attributes, with a starter "Category" field of 10 options | `[fields/understanding-fields-in-rho]` |
| Puzzle integration | Listed as a native accounting integration in two places, with **no setup article** | `[accounting/how-to-link-rho-to-your-accounting-software]`, `[accounting/what-is-rho-close]` |
| Attach a PDF to a mailed check | Up to 6 pages printed and mailed in the same envelope, free | `[payments/how-to-send-a-physical-check]` |
| USPS check tracking | "Track Your Check" link in transaction details after shipping | same |
| Slack agent chat | Natural-language finance Q&A in Slack, beta | `[rho-slack-app/how-to-use-the-rho-slack-app]` |
| Internal notes on vendors | Free-text notes never shared with the vendor | `[vendors/how-to-manage-vendors-in-rho]` |
| Partner roles | Partner Admin, Partner Expense & AP Manager, Partner Accountant, External Admin, External Accountant | `[accounting/understanding-the-accounting-dashboard]`, `[admin/how-to-manage-users-and-roles-in-rho]` |

## 6. Features that are marketed but turn out to be constrained

| Marketed as | Actual constraint | Source |
|---|---|---|
| "Hundreds of vendors, zero fees" Bill Pay | Cannot send non-USD international wires at all; bulk payments are domestic-wire only | `[bill-pay/paying-international-bills-in-bill-pay]`, `[bill-pay/understanding-bulk-payments]` |
| "Up to $75M in FDIC insurance" | Savings only. Checking is $250K total across all sub-accounts; Treasury is SIPC, not FDIC. $25K minimum, six withdrawals/month | `[general-rho-information/how-does-fdic-insurance-coverage-work]` |
| "No ACH fees", "no subscription fees" | $15 cover-all-fees toggle, $20 to $45 failed-wire fee, 2.9%+$0.30 invoice card fee, 0.15% to 0.60% Treasury AUM fee, $400 incorporation fee | §7 below |
| "Up to 2% Cashback with Rho Platinum" | Requires all four Platinum qualifications; capped at the first $1M of eligible spend per calendar year; excludes Walmart, utilities, quasi-cash and all non-US spend; forfeited on late payment | `[general-rho-information/rho-platinum-what-it-is-and-how-to-qualify]`, `[cards/understanding-card-cashback]` |
| "Banking and payments via API" | Read-only. No write endpoints documented anywhere | `[the-rho-api/build-a-custom-integration-with-rho]` |
| Invoicing with card acceptance | One-time, full-amount, USD only; $10K/day cap; Rho-managed Stripe account you cannot control; first payout up to two weeks | `[invoicing/accept-card-payments-on-invoices]` |
| Expense policy controls | Post-spend only. They never decline a card | `[expenses/how-to-create-rules-for-expenses]` |
| Multiple operating accounts | Cards can only draw on the primary checking account; external links are account-wide, not per sub-account | `[cards/how-to-update-your-card-settings]`, `[payments/how-to-connect-to-an-external-bank-account]` |
| Mobile app | No vendor cards, no password reset, no accounting sync, no mapping rules, no accounting settings, no team-card management, no multi-transaction disputes | `[mobile-app/*]` |
| Rho Switch | US routing/account vendors only; SWIFT/BIC/IBAN vendors must be added manually | `[banking/switch-your-business-banking-to-rho]` |
| Vendor bulk upload | Performed by Rho staff over 1 to 2 business days, domestic only, one payment method per vendor | `[vendors/how-to-bulk-upload-vendors]` |
| "24/7 support" | One card page still says live support is "Monday through Friday from 8am ET to 8pm ET" | `[cards/employee-card-faqs]` vs `[general-rho-information/how-do-i-contact-support]` |
| Treasury liquidity | Only IJTXX is same-day, and only via the Ascend platform which pre-July-23-2026 accounts do not yet have | `[treasury/understanding-rho-treasury]` |

## 7. Every fee named anywhere in the help center

The pricing article says: "Rho has no subscription fees, no per-user fees, and no platform fees on any account... The only standard payment fee is 1% on foreign-currency transfers." `[general-rho-information/pricing-requirements]`

The rest of the corpus names these:

| Fee | Amount | Source |
|---|---|---|
| FX conversion | 1% | `[payments/how-to-send-an-international-wire]` |
| Cover all recipient delivery fees (intl USD wire) | flat $15 (as of 08/02/2026) | same, `[bill-pay/paying-international-bills-in-bill-pay]` |
| Failed/returned domestic wire | ~$20 to $45 | `[payments/fees-for-recalls-failed-wires]` |
| Recalls (ACH and wire) | free | `[payments/how-to-cancel-reverse-or-dispute-a-bank-transfer]` |
| Invoice card acceptance | 2.9% + $0.30 per transaction, paid by the business | `[invoicing/accept-card-payments-on-invoices]` |
| Treasury management | 0.15% to 0.60% annualized, billed monthly | `[treasury/managing-your-rho-treasury-account]` |
| Incorporation | $400 (creditable), $1,000 figure cited for accelerator-introduced founders | `[general-rho-information/incorporating-your-company-with-rho]` |
| Check attachment printing | "no additional cost to you" | `[payments/how-to-send-a-physical-check]` |
| Card foreign transaction fee | none | `[cards/employee-card-faqs]` |
| Rho Capital origination / prepayment | none; "Rates are set during underwriting" | `[general-rho-information/about-rho-capital]` |

---

## 8. Everything that requires contacting support

A useful measure of product maturity: 57 of 253 articles (22.5%) route the reader to Client Service. These are the ones where support is the **only** path:

| Action | Why | Source |
|---|---|---|
| Raise any transfer limit | "contact your Rho Specialist at 855-7-GETRHO" | `[payments/transfer-limits]` |
| Recall / reverse / dispute a settled bank transfer | Not self-serve at all | `[payments/how-to-cancel-reverse-or-dispute-a-bank-transfer]` |
| Set up FedWire Drawdown | Email only | `[payments/can-i-set-up-reverse-fedwires-from-my-account]` |
| Enable micro-deposit account linking | Email only | `[banking/how-to-set-up-micro-deposits]` |
| Get ACH debit authorizations (beta) | Request access | `[banking/manage-your-ach-debit-approvals-in-rho-beta-]` |
| Get whitelisting codes for an external bank's pull | "please contact our Client Services for the exact codes" | `[payments/transferring-money-from-a-linked-account-to-rho]` |
| Open a Savings account | Request Access, then a DocuSign prepared by Client Service | `[banking/understanding-rho-savings-accounts]` |
| Get the list of Savings sweep network banks | "available from Rho support on request" | `[banking/how-the-rho-savings-sweep-works]` |
| Set up a DACA | Email client service | `[banking/does-rho-support-daca-accounts]` |
| Bulk upload vendors | Rho staff do it | `[vendors/how-to-bulk-upload-vendors]` |
| Set up a card feed / Mastercard Smart Data | Email, 3 to 5 business days | `[cards/how-to-set-up-a-card-feed-integration]` |
| Change the shipping address on a reissued card | Contact Customer Service on receiving the reissue email | `[cards/card-expiration-and-renewal]` |
| Change your phone number (2FA) | "Phone number changes go through clientservice@rho.co" | `[general-rho-information/how-to-log-in-to-rho-and-fix-login-issues]` |
| Change your business address | Email with a written reason | `[general-rho-information/can-i-change-my-business-address]` |
| Close your Rho account | Account Owner must call/chat/email | `[general-rho-information/how-to-close-your-rho-account]` |
| Close or liquidate Treasury | "by contacting Rho" | `[treasury/understanding-rho-treasury]` |
| Move a whole VFSTX position to VFSUX | "contact the Rho team" | same |
| Exceed the Vanguard 50% cap | "unless we have approved a higher limit for your account" | `[treasury/about-rho-treasury]` |
| Raise the $10,000/day invoice card limit, or refund a card payment | "contact Rho Client Service" | `[invoicing/accept-card-payments-on-invoices]` |
| Adjust a credit agreement | "please contact your Account Manager" | `[banking/viewing-account-information]` |
| Un-unsubscribe a vendor from payment notifications | "please reach out to Rho client service" | `[payments/how-to-set-up-vendor-payment-notifications]` |
| Authorize a third-party API integration | Forward to api-partner-request@rho.co | `[the-rho-api/build-a-custom-integration-with-rho]` |
| Plan a purchase larger than your daily credit limit | "Contact Rho Client Service for assistance" | `[cards/the-rho-card-with-daily-terms]` |
| Request a blank bank statement or a balance-to-date statement | Phone or email | `[banking/how-to-get-a-proof-of-account-document]` |

---

## 9. Beta, legacy, roadmap and in-development inventory

| Item | Status | Source |
|---|---|---|
| ACH debit authorizations | BETA, request access from Client Services | `[banking/manage-your-ach-debit-approvals-in-rho-beta-]` |
| Slack agent chat | Beta, "select Rho businesses", request access in-app | `[rho-slack-app/how-to-use-the-rho-slack-app]` |
| Slack app roles beyond Owner/Admin | "with support for more roles on the way" | `[rho-slack-app/understanding-the-rho-slack-app]` |
| Monthly user limits | **Legacy**, "no longer part of Rho's standard offering" | `[admin/how-to-set-monthly-user-limits]`, `[cards/how-to-edit-the-spending-limit-on-a-rho-card]` |
| Syncing unpaid invoices | "currently in development" | `[accounting/setting-up-recurring-syncs-to-automate-your-accounting-integration]` |
| Invoice sync for non-QBO platforms | "Support for additional platforms is on the roadmap" | `[accounting/syncing-invoices-to-your-accounting-software]` |
| Fields-native reporting views | "on the roadmap" | `[fields/understanding-fields-in-rho]` |
| Vendor cards in Bill Pay | "does not currently support Vendor Cards" | `[vendors/how-to-manage-vendors-in-rho]` |
| VFSTX | Closed to new allocations; sold FIFO before VFSUX until it hits $0.00 | `[treasury/understanding-rho-treasury]` |
| Apex Ascend migration | Pre-2026-07-23 accounts migrating "in the coming months" | same |
| LLC incorporation | "LLC coming soon" (nav copy carried on every page) | site nav in `pages/help/*` |

---

## 10. Contradictions between pages

1. **Savings/Checking transfer settlement has four different published answers.**
   - `[payments/how-to-create-an-internal-transfer]` says "Settlement times for Savings Account transfers are 1-3 business days" in one paragraph and "Transfers in or out of Savings Accounts typically take 1-2 business days" in another, in the same article.
   - `[payments/payment-settlement-times]` says "Savings to Checking Account Transfers: 2 business days" and "Checking to Savings Account Transfers: 2 business days."
   - `[banking/understanding-rho-savings-accounts]` and `[banking/how-the-rho-savings-sweep-works]` say Checking → Savings settles **same business day** if created before 1pm ET and Savings → Checking **next business day**.
   - The underlying ADM agreement implies Wednesday/Friday settlement only. `[general-rho-information/rho-savings-account-terms-and-conditions]`

2. **Business-to-business internal transfer: 2 to 3 hours vs 1 business day.** `[payments/how-to-create-an-internal-transfer]` says "business-to-business internal transfers may take 2-3 hours to settle"; `[payments/payment-settlement-times]` says "Internal Transfers Between Different Businesses Holding Accounts at Rho (Checking to Checking): 1 business day."

3. **Check deposit clearing: three numbers.** "6-7 business days to clear" `[payments/transfer-limits]`; "Checks settle in 3 business days after they are uploaded... (generally up to 6-7 business days)" `[payments/how-to-deposit-a-check]`; "2-3 business days to clear, subject to risk-based monitoring (generally up to 6-7 business days)" `[payments/how-to-fund-your-account]` and `[payments/payment-settlement-times]`.

4. **Linked-account transfer settlement: "3-5 business days" `[payments/transferring-money-from-a-linked-account-to-rho]` vs "up to 5 business days" everywhere else.**

5. **Support hours.** `[cards/employee-card-faqs]`: "For live support, our team is available Monday through Friday from 8am ET to 8pm ET." `[general-rho-information/how-do-i-contact-support]`: "24/7, on every account... Every channel is staffed around the clock, every day of the year." `[cards/how-to-dispute-a-transaction-on-a-rho-card]` also says 24/7.

6. **"Six pre-set user roles" followed by a nine-row table.** `[admin/how-to-manage-users-and-roles-in-rho]` states "Rho has six pre-set user roles, which are available to use as defaults. These are Account Owner, Administrator, Department Owner, Employee, Bookkeeper, and Investor" and then tabulates nine, adding AP & Expense Manager, External Admin, and External Accountant. `[accounting/understanding-the-accounting-dashboard]` lists a fourth family: Partner Admin, Partner Expense & Accounts Payable Manager, Partner Accountant.

7. **Employee and Bookkeeper have byte-identical role descriptions** ("should be assigned to any employee who should be given limited permissions. They are unable to view account balances or Vendor history"), which cannot both be right given Bookkeeper is elsewhere described as a "view all" role with full transaction visibility. `[admin/how-to-manage-users-and-roles-in-rho]` vs `[accounting/understanding-the-accounting-dashboard]`, `[cards/understanding-the-team-cards-page]`.

8. **Permissions glossary defines the same capability two opposite ways.** "Manage team cards: User can edit team card settings" and "Manage cards: User can see but not edit team card settings" list an identical parenthetical field set; likewise "Manage team card permissions" (edit) vs "Manage card permissions" (see but not edit). `[admin/user-permissions-glossary]`

9. **Departments vs Fields: two live, mutually exclusive data models.** `[fields/understanding-fields-in-rho]` states flatly: "Your account does not include a Reporting tab. That tab houses the Departments and Labels pages used by longer-tenured accounts." All 11 `departments` articles instruct the reader to "navigate to the Reporting tab." Both are presented as current documentation with no cohort banner.

10. **Naming drift: "Departments" vs "Budget Owner" vs "Department Owner."** `[cards/how-to-assign-card-transactions-to-a-department]` and `[departments/how-to-assign-or-tag-a-transaction-to-a-label]` still say "Budget Owner"; `[admin/how-to-manage-users-and-roles-in-rho]` says "Department Owner"; `[banking/understanding-transaction-tables]` still labels the column "Department: The budget assigned to the transaction."

11. **Vendor cards in Bill Pay.** `[bill-pay/paying-bills-with-vendor-cards-single-use]` describes paying bills with single-use vendor cards as a supported method, while `[vendors/how-to-manage-vendors-in-rho]` says "Paying a bill through the Bill Pay workflow does not currently support Vendor Cards. You'll be prompted to add an alternative payment method."

12. **Statement availability.** `[banking/how-to-view-account-and-card-statements]` gives four different dates by account type (Checking on the 2nd calendar day, Savings by the 5th business day, Daily Terms cards on the 5th, Monthly Terms cards 1 business day after repayment) and then adds a blanket note "You can download a statement for the previous month starting on the 5th of each month." `[banking/how-to-get-a-proof-of-account-document]` says simply "Statements are generated on the 5th of every month."

13. **Rho Capital credit pull.** The body says "Applying doesn't involve a hard pull on your personal credit," while the disclosure directly below says "Application and consent to obtain personal credit report is required. ... Personal Guaranty may be required." `[general-rho-information/about-rho-capital]`

14. **Card dispute timeline.** "disputes may take up to 90 days to be resolved" and "our team will begin our investigation, which may take up to 90 days," versus "A dispute determination can take 45-90 days and is managed by Mastercard." `[cards/how-to-dispute-a-transaction-on-a-rho-card]`, `[cards/employee-card-faqs]`

15. **Bulk payments execution rights.** `[bill-pay/understanding-bulk-payments]`: "Admins, Account Owners and Bookkeepers can view bulk payments... By default, Bookkeepers cannot execute payments." `[vendors/how-to-pay-multiple-vendors-at-once]` restates it as "Admins and Account Owners can execute."

16. **Incorporation fee credit threshold.** "$400 fee, which is credited back once you deposit $10,000 of new money... ($1,000 for founders introduced through an accelerator)." The parenthetical is ambiguous about whether $1,000 replaces the fee or the deposit threshold; no other page clarifies. `[general-rho-information/incorporating-your-company-with-rho]`

17. **Unfilled editorial placeholders shipped to production.** `[treasury/managing-your-rho-treasury-account]` and `[treasury/understanding-rho-treasury]` both contain the literal string "[insert Help Center article for IJTXX]". `[payments/how-to-setup-payroll-with-rho]` has a table header typo, "Asnwer."

---

## 11. Conspicuously NOT stated anywhere in 269 help pages

- **Any interest rate or APY number for Savings or Checking.** The only rate anywhere is the Treasury footnote pinned to "90-day Treasury Bill rates as of 09/11/2026", and the nav copy "Earn up to 4.66% on your idle cash." The Savings article says only "Your current APY is shown on the Savings page in your Rho dashboard."
- **The Savings sweep's fee split.** The ADM master agreement page **terminates at Section 10** (Program Institutions). Sections covering ADM's fee, the interest calculation referenced as "Section 9", termination, liability and dispute resolution are absent from the published page, even though Section 8 forward-references "Section 9" for interest.
- **The list of Savings network banks.** Withheld, available "on request."
- **Any credit limit number, underwriting criterion, or APR for the Rho Card with Monthly Terms.** Only "personalized based on the business's financial health."
- **Any Rho Capital rate.** "Rates are set during underwriting based on your business, see your offer for exact terms."
- **Uptime, SLA, or incident/status page.** The mobile article mentions "Rho Support Opening Hours and Status" in the app, but no status URL appears anywhere.
- **Any write API.** No payment initiation, card issuance, or user management endpoint is referenced in the four API articles.
- **SAML, Okta, Entra, SCIM, or any non-Google SSO.** Zero mentions.
- **Data residency beyond "hosted in the United States using SOC 2-audited providers"** (Rho Switch only). No retention schedule for anything other than Switch data (~120 days).
- **Any mention of a Rho savings/checking account for non-US-incorporated entities.** Incorporation in the US is mandatory.
- **Multi-entity/consolidated reporting.** Entity toggling appears only inside accounting mapping rules, never as a reporting surface.
- **International ACH, SEPA direct debit, or local-rail collections.** Money in is wire, ACH, RDC, or linked-account pull only.
- **A Puzzle integration setup guide**, despite Puzzle being listed as a native integration twice.
- **Any article on the Home tab, Integrations tab, or the "Rho Close" monthly close workflow end to end.** Rho Close is documented only as a coding-suggestion engine, not the "close your books faster, every month" product named in the nav.
- **Refunds or chargebacks on Rho invoices** beyond "contact Rho Client Service."
- **What happens to cashback accrued but unredeemed at account closure.** The closure checklist covers card balance, scheduled payments, Savings, Treasury, statements and W-9s, and never mentions the Rewards account.
- **Any fee schedule page.** `[general-rho-information/pricing-requirements]` is 355 bytes and defers to the marketing pricing page.

---

## 12. Dated facts to carry forward

| Fact | As-of date |
|---|---|
| Merchant allow-list cap of 20 distinct merchants per card | 08/02/2026 |
| No Rho fee on international wires sent in USD | 08/02/2026 |
| $15 flat "cover all recipient delivery fees" | 08/02/2026 |
| 1% FX rate | 08/02/2026 |
| Domestic failed-wire fee of $20 to $45 | 08/02/2026 |
| Savings transfers out limited to six per month | 08/02/2026 |
| Savings sweep network of 400+ FDIC/NCUA institutions | August 2026 |
| Webster Bank part of Santander's $327 billion-asset US banking organization | August 20, 2026 |
| Treasury net-yield footnote based on 90-day T-Bill rates | 09/11/2026 (today; appears on all 16 index pages) |
| Apex Ascend platform cutover date for new Treasury accounts | July 23, 2026 |
| Copyright line on every page | 2019 to 2026, Under Technologies, Inc. DBA Rho Technologies |

## 13. Entity and partner map as stated in the help center

| Role | Entity | Source |
|---|---|---|
| Platform operator | Under Technologies, Inc. DBA Rho Technologies. "Rho is not a bank." | footer on all pages, `[general-rho-information/our-partnership-with-webster-bank-n-a-member-fdic]` |
| Deposits and card issuing | Webster Bank, a division of Santander Bank, N.A., Member FDIC (founded 1935) | same |
| Savings sweep administrator | American Deposit Management, LLC + ADM Consulting, LLC | `[general-rho-information/rho-savings-account-terms-and-conditions]` |
| Treasury adviser | RBB Treasury LLC dba Rho Treasury, SEC-registered, a Rho subsidiary | `[treasury/about-rho-treasury]` |
| Treasury custody | Apex Clearing Corporation; Interactive Brokers LLC also named ("Interactive rates may vary from Apex rate shown above") | same |
| Rho Capital lender | **Lead Bank** | `[general-rho-information/about-rho-capital]` |
| Card network | Mastercard (World Elite Business program) | `[cards/understanding-mastercard-easy-savings]` |
| Bank data aggregation | Plaid, Mastercard Data Connect (Finicity), Stripe Financial Connections | `[payments/how-to-connect-to-an-external-bank-account]` |
| Accounting data | Codat (named in the application FAQ) | `[general-rho-information/applying-to-rho-faqs]` |
| Invoice card processing | Stripe (Rho-created and Rho-managed account) | `[invoicing/accept-card-payments-on-invoices]` |
| Rewards marketplace | Built First | `[general-rho-information/rhos-rewards-marketplace]` |
| T&E partner | Navan Expense, linked via Mastercard Smart Data | `[general-rho-information/understanding-the-integration-between-rho-and-navan-expense]` |

## 14. Contact surface (published in the corpus)

| Channel | Value |
|---|---|
| Phone | 1 (855) 743-8746 = 1-855-7-GETRHO |
| Client service email | clientservice@rho.co |
| Security / phishing reports | security@rho.co |
| Partnerships | partnerships@rho.co |
| API partner requests | api-partner-request@rho.co |
| Receipt capture email | receipts@rho.co |
| Receipt capture SMS short code | 555746 |
| Rho inbound fax for IRS 147c letters | +1 646-455-3240 |
| Login | https://app.rho.co |
| NetSuite callback URL | https://api.rho.co/webhook/netsuite_authorize_callback |
| Rho routing number | 021913655 |
