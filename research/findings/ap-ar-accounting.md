# Rho: AP (Bill Pay), AR (Invoicing), Accounting Automation and Month-End Close

Research dossier section. Corpus-grounded. Compiled 2026-09-11 from the local Rho crawl.
Convention: **[Rho claim]** marks an assertion only Rho makes (especially about competitors). Dated facts carry Rho's own as-of date.

Primary sources used (local paths relative to `.../scratchpad/rho/`):

| Area | Files |
|---|---|
| Product marketing | `pages/core/product__bill-pay.txt`, `product__invoicing.txt`, `product__close.txt`, `product__expense-management.txt`, `pricing.txt`, `faq.txt`, `changelog.txt` |
| Integrations marketing | `pages/core/integrations.txt` + 11 `integrations__*.txt` |
| Legal | `pages/core/policies__invoicing-terms-and-conditions.txt` |
| Help center | 19 `pages/help/help-center__bill-pay__*`, 27 `help-center__accounting__*`, 12 `help-center__vendors__*`, 3 `help-center__invoicing__*`, plus expenses/payments/admin/fields/mobile pages |
| API | `docs/docs_v1_invoicing.md`, `api/invoicing_*.md`, `sandbox/invoicing_invoices.json`, `sandbox/invoicing_customers.json` |
| Comparison blog | `pages/blogcomp/blog__best-ap-automation-software.txt`, `blog__best-ap-automation-tools-for-startups.txt`, `blog__best-invoicing-tools-for-startups.txt` |
| Self-description | `site-llms-full.txt` (last updated 08/21/2026) |

---

## 1. Headline pricing and fee schedule (AP + AR)

From `pricing.txt` ("Rho fee summary"), `product__bill-pay.txt`, `product__invoicing.txt`, `policies__invoicing-terms-and-conditions.txt`:

| Item | Fee | Source / as-of |
|---|---|---|
| Bill Pay software / platform | $0, included with Rho business banking | bill-pay page; "No monthly, per-user, or minimum-balance fee across Rho banking, cards, expense management, and Bill Pay" |
| Bill Pay per-user / per-seat | $0 | bill-pay page: "does not charge per user or per seat" |
| Domestic check payment (outgoing) | $0 | bill-pay page hero stat "$0 On domestic check payments" |
| Same-day ACH, domestic wires, checks | $0 | pricing.txt item 01; site-llms 08/02/2026 |
| Subscription fees | $0 | pricing.txt item 02 |
| Checking minimum-balance fee | $0 | pricing.txt item 03 |
| "AP, Expense & Accounting Automation" | $0 | pricing.txt item 04 |
| Per-user fees | $0 | pricing.txt item 05 |
| Foreign currency transfer | 1% FX rate | pricing.txt item 06; also "1% FX rate (as of 08/02/2026)" on `paying-international-bills-in-bill-pay` |
| Domestic wire recall | $0 | pricing.txt item 07 |
| International wire recall | $30 | pricing.txt footnote |
| Optional SWIFT fee ("Cover all recipient delivery fees") | $15 flat, optional toggle | pricing footnote; bill-pay intl article states "flat $15 (as of 08/02/2026)" |
| International wire in USD sent from Bill Pay | $0 Rho fee (as of 08/02/2026); recipient/correspondent/intermediary + SWIFT may charge | `paying-international-bills-in-bill-pay` |
| Failed/returned domestic wire | "around $20 – $45" deducted from the Rho account | `help-center/payments/fees-for-recalls-failed-wires` (note: contradicts pricing.txt's "$0 domestic wire recall fee") |
| Late fee on delinquent balance | 3% of delinquent balance per month, up to 6 months | pricing.txt footnote |
| Rho Invoicing subscription / per-invoice | $0 | invoicing page; Invoicing T&C §6 |
| Inbound domestic ACH, wire, check into Rho on an invoice | $0 | invoicing page; T&C §6 |
| Invoice card payment (credit/debit/Google Pay via Stripe) | **2.9% + $0.30 per transaction, paid by the business, not the payer** | `help-center/invoicing/accept-card-payments-on-invoices`; T&C §4; changelog 08/31/2026 |
| Surcharging the payer for the card fee | Not available | card-payments help article |

Marketing headline stats on `product/bill-pay`: "$0", "$0 On domestic check payments", "<10 min¹ To apply", "4 steps From forwarded invoice to a synced, paid bill". Competitive data on that page collected **as of 2026-09-08**; "Product claims current as of September 2026."

---

## 2. Accounts payable: Rho Bill Pay

### 2.1 Positioning and explicit scope exclusions

- `product/bill-pay`: "Rho Bill Pay is automated accounts payable, sometimes called AP automation, included with Rho business banking." Not sold standalone: "Rho Bill Pay is not sold as standalone software. It ships with a Rho business banking account."
- Explicit exclusion, stated twice: "it does not include procurement or supply-chain management."
- "Bill Pay activates once your Rho business banking account is open."
- **Three-way match is explicitly not available.** `blog__best-ap-automation-software.txt` Rho cons: "3-way match: Not yet available." The Willet + Cumro customer story frames it as forward-looking: "As Rho adds new features like international payments and three-way match (matching purchase orders, vendor invoices, and receipts)…". No purchase-order object appears anywhere in the corpus.
- No AI auto-approval: "Rho Bill Pay uses automated invoice capture (optical character recognition) to turn a forwarded invoice into a draft bill for your team to review, not an AI system that approves payments on its own."

### 2.2 Invoice ingestion: the Bill Pay Inbox

Source: `rho-bill-pay-inbox-overview`, `how-to-manage-your-bill-pay-inbox-and-known-senders`, `how-rho-syncs-bill-pay-data-in-your-accounting-system-`.

- Every organization is assigned a dedicated email address, **auto-created once the business is verified**. Editable at **Settings → Configuration → BillPay Setup** (one article) / **Bill Pay → Settings** (another article; the two pages give different navigation paths).
- Ingestion paths: (1) forward email to the inbox, (2) direct upload to the platform (`+ Add Bill`), (3) pull from the accounting platform (see §5.3).

**Known-sender model:**

| Sender class | Behavior |
|---|---|
| Any address on the business's own email domain (e.g. all `@smithcompany.com`) | Allowed by default |
| Any address tied to an active Rho user | Allowed by default |
| Externally added addresses (Bill Pay → Settings → Known senders → Add senders) | Allowed |
| Unknown sender | Email notification to the org; **bills are not visible on the platform until the sender is reviewed**. Review flow: "Review X unknown senders" → Accept (invoices added, sender added to known list) or Reject (invoice not added, sender not added). "Rejecting does not mean blocking the sender." |

**File support for the Bill Pay inbox:**

| Constraint | Value |
|---|---|
| Supported file types | JPG, JPEG, PNG, HEIC, PDF |
| Not supported | CSV, XLS, etc. |
| Max file size | <50MB per file |
| Attachments per email | No limit |
| Multi-page invoices | Allowed, but "OCR processing results for multi-page invoices can be less accurate" |
| Content types not supported | W-9 documents, payment-instruction files, statements. Supported = "files with an amount, invoice or reference # and dates for payment" |

### 2.3 OCR

Source: `understanding-ocr-technology-at-rho`, `how-rho-syncs-bill-pay-data-in-your-accounting-system-`.

- "Rho uses **OCR vendors**" (third-party, unnamed) to parse invoices received in the Bill Pay inbox.
- Fields extracted, per the sync article: **Vendor (and payment details), Invoice Number, Amount, Due Date, Invoice Date, Payment Terms**. The inbox overview lists a shorter set: "the amount, vendor, invoice number, and due dates." The marketing page lists only three: "extracts the vendor, amount, and due date."
- **Confidence score** is surfaced on the bills table as a **Green / Yellow / Red** accuracy indicator:
 - Green = high confidence, no action needed
 - Yellow = review suggested, double-check the flagged fields
 - Red = low confidence, verify details before paying
 - A yellow inline warning is clickable and shows which fields need checking; a call-to-action banner may guide next steps.
- OCR also **creates draft vendors** in the dashboard when the vendor on the invoice is unrecognized, pre-populating vendor and payment information from the invoice.
- **Duplicate detection**: "potential duplicates are flagged before anything is paid" (marketing). The OCR article names a specific duplicate-generating failure mode: "If a user replies in a thread to the original email sent to the Bill Pay inbox and image files invoices are in the email body, duplicate invoices can be created. These invoices will be auto-flagged as duplicates in the platform."
- Human confirmation is mandatory: "key data points will need to be confirmed by a user before the bill is Sent to Payments."

### 2.4 Bill splitting

- Manual split, or **automatic line-level splitting** toggled at **Bill Pay → Settings → Automated Bill Splitting**.
- "These split lines will be represented on the bill record in the accounting platform."
- Split amounts must sum to the transaction total; a mismatch produces a sync error ("Split transactions do not add up to total transaction amount").
- Separate generic split feature for banking/card transactions: Transaction Details → **Split Transaction** → Add Split, allocate amount + department/custom attribute per split. The splitting user "needs to be assigned to the department they are splitting the transaction between."
- Fields-based splitting example: "a $5,600 bill can go $5,100 to Sales, $200 to Marketing, and $300 to Engineering under one Field."

### 2.5 Bill / payment status machine

Source: `status-changes-in-bill-pay`. Statuses and permitted actions:

| Status | Meaning | Actions |
|---|---|---|
| **Draft** | Submitted via Bill Pay Inbox or platform upload, needs info/review | View; Add Payment Details (moves to Missing Payment Details); Archive; Mark as Paid |
| **Missing Payment Details** | Bill complete, payment details missing/incomplete | View; Archive |
| **Ready for Payment** | Bill + payment details complete | Pay; Send to Approvals; Archive |
| **Awaiting Approval** | Requires approval before processing | Approve & Pay; Approve; Reject |
| **Payment Scheduled** | Payment scheduled | View; Revoke |
| **Paid** | Processed and settled | View |
| **Paid Externally** | Paid outside Rho Bill Pay | View |
| **Failed Payment** | Payment failed to process | Retry; Archive |

Bulk actions by status:
- Draft or Missing Payment Details → Archive, Mark as paid
- Ready for Payment → Schedule, Update payment date
- Awaiting Approval (from the Bills table) → bulk Approve / bulk Reject

Archiving: available while Draft or Missing Payment Details; "Archiving a bill removes it from your active workflow but keeps a record"; a reason can be specified. Rejecting from the mobile app also archives the bill with a rejection reason.

Note: a separate sync-error string references a **"Processed"** state not listed in the status table ("You can sync this bill when it moves to Processed state"), and the article says syncing happens after "Send to Payments." So the internal state naming is inconsistent across help pages.

### 2.6 Approval workflows

Sources: `how-to-set-up-approvals-for-bill-pay`, `how-to-send-payments-to-approvals`, `how-to-require-approval-for-specific-transactions`, `how-to-review-bill-pay-payments-in-the-mobile-app`.

Configuration path: **Settings → Security → Payment Approvals → Change** (bill-pay article) / **Settings → Payment Security → Payment Approvals** (admin article). Two different nav strings for the same feature.

Mechanics:
- Master toggle: **"Require approval for all outgoing bank payments"** → On.
- Then **+ Add Rule**. Rule logic is strictly amount-threshold based: *"For X amount or above, X number of approvals are required."*
- Worked example from the docs: "if you set your minimum amount as $50 and your number of approvals at 2, then any transfer of fifty dollars or more must receive two approvals from two separate people designated in the Approver list."
- Approvers must be users in the organization; an **Invite User** button is available inline.
- **Multiple rules** can be created (multi-tier thresholds). Admin article example: "one approver for all transactions over $50, and two approvers for all transactions over $100."
- **Self-approval counts**: "If the user drafting the payment is an approver, the Send for Approval action will count as the first layer of approval."
- Submission paths: from the bill detail screen (**Send for Approval**, top-left), from the table row three-dot menu, or by multi-select checkbox + **Send for Approval** button.
- Approvers receive email notifications. Approvals are also possible in the mobile app: **Approvals tab → AP Payments**; final approver sees **Approve & Schedule** and must confirm all bill details; 2FA may be required if the org enables it.
- **Hard timing constraint**: "any scheduled payments that need approval must be approved prior to 4am EST on their due date, or the payment will not be released."

What is *not* documented anywhere: approval routing by vendor, department, GL account, entity, or category for **bill payments**. Only dollar amount. (Expense approvals, by contrast, support direct-manager routing - see §7.) Rho's own blog acknowledges the richer model exists in the market: "Rules are usually based on amount, vendor, or department" but describes Rho's as "amount-based approval guardrails."

Rho's competitive framing of its own approvals is deliberately modest: *"A dedicated AP tool can make sense if your team needs deeper approval-policy customization than a banking-included tool offers."* (bill-pay FAQ)

Bill Pay permissions (from `user-permissions-glossary`): **View Accounts Payable report** (bills outstanding $, number of open bills, approvals needed, scheduled payments, recently paid), **View bills**, **Manage bills**, **View Bulk Payments**, **Create Bulk Payments**. Vendor permissions are separate: Create Vendors, Manage Vendors (add/edit payment types), Delete Vendors, View Vendors, **View Full Vendor Routing and Account Number** (masked otherwise), View Vendor Payment history.

### 2.7 Payment methods and rails for vendors

Authoritative list (`paying-bills-with-vendor-cards-single-use`): **ACH transfers, wire transfers (domestic and international), checks, single-use cards.**

| Rail | Fee | Settlement | Notes |
|---|---|---|---|
| ACH (outgoing) | $0 | Same-day if created before 2 pm ET and under $1mm; next day if after 2 pm ET or over $1mm | Daily limit $20M aggregate out; $10M/txn on pulls in |
| Domestic wire (outgoing) | $0 | Same-day if created before 4:45 pm ET, else next day | $90M/day limit; larger with advance notice |
| International wire (outgoing) | $0 Rho fee in USD; optional $15 flat "cover all recipient delivery fees"; 1% FX | 1-3 business days, up to 5 | $2.5M/day out; $10M/day in |
| Printed check | $0 | Up to 8 business days to arrive via USPS | Rho prints and mails; USPS tracking in-platform |
| Single-use virtual Rho card | (not stated) | Card auth | 14-day usage window, one authorization |

Check mechanics (`understanding-rho-check-mechanics`, `how-to-send-a-physical-check`):
- Funds are **set aside immediately** when the payment is sent but do not leave the checking account until Rho is notified the check was cashed.
- **Checks auto-void after 90 calendar days** uncashed.
- Undeliverable checks return to the business address on file.
- Check number appears in Bill Pay and Banking transaction windows, in the vendor notification email, and in PDF transaction exports.
- **Attach a PDF to a mailed check**: 1 PDF per check, up to 6 pages, 15 MB max, PDF only, **one-time check payments only** (no recurring). No additional cost. Shipped in the same envelope.
- Not supported: third-party check issuance/printing (including checks from ADP, Gusto), checkbooks, printed check stock, cashier's checks, international checks. Payroll checks workaround: "creating them as Vendors and issuing checks through Rho."

Single-use vendor card mechanics (`paying-bills-with-vendor-cards-single-use`, `understanding-bulk-payments`):
- Card is created when the payment is created; the email with card details is sent based on the Created/Due date on the payment line.
- Card nickname: `<Vendor> AP Card: <Invoice Number>` (also written `[Payee Name] AP Card: [Invoice Number]`).
- **Single authorization**, pre-set to the payment amount, **14-day card usage window** (editable in Card Settings).
- Once successfully charged, the card becomes invalid; status flips Active → Canceled but remains viewable in Team Cards.
- The **secure link to card details expires in 72 hours**.
- Vendor sees: payment creator, sending organization, invoice number, and the card details.
- Viewable under **Cards → Vendor Cards**.

### 2.8 Scheduling and timing

Source: `how-to-schedule-a-bill-payment-in-rho`, `what-time-are-scheduled-payments-sent-out`.

- Scheduled payments are released at **approximately 4:00 a.m. ET** on the payment date ("4am EST" in the payments article). Released early so scheduled domestic wires and ACHs make the same-day cutoff.
- Payments requiring approval **must be approved before that 4 a.m. release**.
- **Same-day scheduling does not work**: a payment scheduled for today will not release and will not roll to the next business day; it is marked **overdue**. Real-time sending requires **Make A Payment → Send Now**.
- Bill Pay payments must be dated on a **business day (Mon-Fri)**; weekend dates will not send and show as overdue.
- Revoke path: **Bill Pay → Bills → filter Payment Scheduled → three dots → Revoke**.
- Bulk date change: **Bill Pay → Payments → Draft table → select → Update Payment Date** → calendar → confirm. Available for checks, ACH, wires, and single-use virtual cards.
- 2FA may be required depending on account security settings.

### 2.9 Bulk payments

Source: `understanding-bulk-payments`, `how-to-pay-multiple-vendors-at-once`, `how-to-add-bulk-payment-date-from-payment-draft-table`.

- CSV-template-driven workflow: import a Rho CSV template to "bulk draft, review, schedule, and send payments."
- Supported payment types in bulk: **Checks, ACH, Wires (domestic accounts only), Single-use virtual Rho cards** delivered by email.
- **One CSV line = one payment. No merging of line items into a single payment.**
- Prerequisite: vendors must already exist in Rho.
- Creation/Due date must be **today or a future date**; past dates error.
- Role gate: "Admins, Account Owners and Bookkeepers can view bulk payments, meaning they can import a CSV and make edits to payment drafts. **By default, Bookkeepers cannot execute payments** from the Bulk Payments workflow."
- Draft-table error states:
 - **Vendor Missing** (vendor name shown in yellow) - CSV vendor could not be matched; resolve via dropdown search or add the vendor first.
 - **Destination Error** - Rho has no payment details for that vendor + method; add the account on the vendor profile.
- International wires **cannot** be included in a bulk payment CSV.
- Alternative bulk path: select bills in the Bills table and Pay / Approve together; bulk approve and bulk reject use the Awaiting Approval filter.
- Approval policies still apply to bulk payments.

### 2.10 International bills

Source: `paying-international-bills-in-bill-pay`.

- **Bill Pay supports international wires in USD only.**
- Non-USD (FX) payments are **not supported in Bill Pay**. The documented workaround is a 5-step split flow:
 1. Add the vendor's international payment method (Vendors → vendor → Add Account → International → International Wire or Bank Transfer; choose currency; IBAN and SWIFT/BIC may be required).
 2. Banking tab → Move Funds → Pay → select vendor → Continue.
 3. Enter amount in "You Pay" or "Vendor Gets"; Rho converts including fees; expand "Total Fees" for the breakdown.
 4. Attach the invoice on Transfer Details (recipient does not receive it); use "Transfer reference" for the invoice number.
 5. Confirm & Pay + 2FA, then back in Bill Pay → **Mark as Paid** → the bill moves to **Paid Externally** and is archived.
- Accounting consequence: "the Banking transfer is the actual payment record - code the Banking transaction to the right category."
- Currency rails caveat: "Certain currencies - **IDR, PHP, INR, and MYR** - are processed on local payment rails rather than SWIFT, so tracking is limited once funds leave Rho."
- Fees as of 08/02/2026: $0 Rho fee on USD international wires; optional $15 flat to absorb recipient/correspondent/SWIFT fees; 1% FX rate. "Fee totals shown are estimates."

### 2.11 Bill Pay notifications and export

- **Notification config**: user dropdown → User Settings → Notifications tab → **Accounts Payable** section (checkboxes).
- **Daily Digest**: sends **5 pm EST every day** if there is ≥1 bill update.
- **Weekly Digest**: sends **10 am EST Friday** if there is ≥1 bill update.
- No email when there is no AP activity. Digests summarize activity across Bills and Payments.
- **CSV export**: Bill Pay tab → Export → choose date range + attributes → Download CSV. "The CSV file will include both bills and payments, which will help you understand your Bill Pay aging after export."

### 2.12 Non-admin attribute coding

`how-to-use-non-admin-attribute-coding`: Admins/Owners enable at **Users → Groups → [group] → Permissions → Change Permissions → Personal Card Management → Code Accounting Attributes → On**. Enabled employees go to the **Accounting** tab and edit coding for **Budget, Accounts, and Vendors** on the summary page or in the transaction slide-out. Changes auto-save. Explicit purpose: "helping finance teams eliminate month-end close delays." Caveat: "your exact view may vary based on specific ERPs."

---

## 3. Vendor management, W-9 and 1099

### 3.1 Vendor creation paths

Five documented paths (`how-to-manage-vendors-in-rho`, `how-to-add-a-vendor-in-rho`, `troubleshooting-vendor-profiles-incomplete-status-and-duplicates`):

| Path | Mechanics |
|---|---|
| Manual | Vendors → **+ Create Vendor**; can save as **Draft vendor** |
| Invite vendor | + Create Vendor → profile name → **Invite Vendor to Complete Profile**; vendor gets email, receives **auto reminders**, can be manually reminded from **Vendors → Drafts** |
| From a bill | When OCR does not recognize the invoice vendor, create the vendor from the Bill Pay screen; Rho pre-populates vendor and payment info from the invoice |
| Bulk upload (CSV) | **Performed by the Rho Client Service team on your behalf**. Template from your success associate; email the completed CSV back; vendors appear under **Vendors → Active** within **1-2 business days**. Supports domestic payments only and **one payment method per vendor per upload** |
| Merchant-to-Vendor auto-creation | See §5.6 |

- An **active vendor profile is required** before paying anyone through Banking or Bill Pay.
- Permission gate: **Manage Vendors**.
- **Incomplete / Draft** = missing required fields, most often a payment account. Documented fix when a vendor completed the invite but the profile will not activate: "the reliable fix today is to **delete the profile and re-create it**. … We know this is not elegant - it is the fix that works." (An unusually candid admission of a product defect.)
- Duplicate avoidance guidance: "Pick one creation path per vendor and stick with it." Most common duplicate cause: inviting a vendor and also entering them manually while waiting. Merchant-to-Vendor uses smart matching to avoid ERP duplicates, but "duplicates created inside Rho by dual entry paths must be cleaned up yourself."
- **Internal notes** field on vendor records: Vendors → select → Edit → Internal notes. "Notes are only visible within Rho and aren't shared with vendors or included in payment workflows."

### 3.2 Default payment account

- Set at the **account** level, not just the method type: vendor profile → ellipsis (⋯) next to the account → **Set as Default**; the account shows a **Default** badge.
- Rho auto-selects the default when creating a payment; the user can still pick another account per payment.
- Changelog 05/27/2026: "Per-account payment defaults for vendors. Default payment methods are now set at the specific account level, not just the method type. Switch which ACH account is the default without deleting and re-adding it."

### 3.3 Vendor notifications and messaging

`how-to-set-up-vendor-payment-notifications`, `how-to-customize-vendor-email-messaging`:
- Vendor Payment Notification emails contain: **ETA, payment amount, method and memo, attachments (links expire after 7 days for security), and for AP bill payments specific invoice numbers and terms.**
- Enabled per vendor profile, with an email address and a preview.
- Vendors receive an onboarding email; they can **unsubscribe** via a link in the notification; the profile shows enabled/unsubscribed state. Re-subscribe requires contacting Rho client service.
- **Notifications are sent only after a transaction is pending**; for check payments Rho sends an additional email once the check is deposited.
- Org-level customization: **Settings → Configuration → Vendor Messaging → Change** → select a Rho contact person (name, phone, email appear in the footer of all vendor notifications) + a custom message.

### 3.4 W-9 collection

`how-to-collect-w-9s-with-rho`:
- Requires an **active vendor profile**. Path: Vendor profile → **Tax Files → New W-9 Form**.
- Two modes:
 - **Upload & Verify** - upload a W-9 already on file. **PDF only, maximum 15 MB.** User must read and accept an attestation. After upload, all parsed fields must be verified, read and attested.
 - **Send Form to Vendor** - confirm/enter the vendor's email, read + attest + confirm, then send.
- Statuses: **Pending from the Vendor** → **On file** (when received through the portal) → or **Completed** if the vendor chose "send externally," in which case "the form will not be available for download, unless uploaded by a user to the Vendor's profile."
- **The vendor portal is live for 60 days.** Uncompleted requests expire and can be resent by the Rho user.
- Vendor portal flow: upload W-9, review, attest to accuracy, submit.
- W-9 documents are **explicitly not supported** as Bill Pay inbox attachments.

### 3.5 1099 filing

`rho-1099-filing-support` - short and limited:
- "Rho allows you to **export** vendor details collected to support annual 1099 filing."
- "If you collect W-9s with Rho, W-9 details are available in the **Vendor CSV export** for you to use for 1099 filing **directly to the IRS or with your vendor of choice**."
- "For those who filed **2023** 1099-MISC or 1099-NEC **with Rho**, PDF copies of 1099s will be available on the Vendor Profile for export."

**Reading: Rho filed 1099s for customers in tax year 2023 and no longer does. Today it is export-only.** Rho's own competitive blog notes Mercury has "W-9 collection plus 1099 filing assistance … built in" - a capability Rho itself describes only as a CSV export. **[Rho claim about Mercury]**

---

## 4. Accounts receivable: Rho Invoicing

### 4.1 Timeline (from `changelog.txt`)

| Date | Event |
|---|---|
| March 25, 2026 | "Invoicing is now in Rho [Beta]". Branded invoices; **virtual account numbers** to "minimize risk from unauthorized debits"; automatic payment-to-invoice mapping |
| April 30, 2026 | Recurring invoices live for all beta customers; **invoices auto-marked as paid** when an incoming payment matches |
| June 30, 2026 | Branded **payment portal** per invoice (logo, colors); recurring invoices weekly/monthly/quarterly/annual; "Free for all Rho customers" |
| August 3, 2026 | **Downloadable invoice aging report** (export dropdown: standard export + industry-standard aging report); option to show operating address instead of registered legal address on invoices |
| August 31, 2026 | **Pay Rho Invoices by Card** (credit, debit, Google Pay) at 2.9% + 30¢; **Rho invoices now sync to QuickBooks** "as accounts receivable invoices, not generic bank deposits" |

### 4.2 Invoice creation

`help-center/invoicing/create-an-invoice`:
1. **Invoices → Create Invoice**
2. **Customer**: choose existing or type a new name to create one automatically
3. **Invoice details**: invoice date, due date, payment terms (examples: Net 30, Due on receipt)
4. **Line items**: product/service name, quantity, rate; totals calculate automatically
5. Optional personal note added to the recipient's email
6. Review: subtotal, taxes, discounts, final amount due → **Create Invoice**
7. **Recurring**: "Schedule this invoice to repeat" with a selectable cadence (weekly / monthly / quarterly / annual per the changelog)

Blog-sourced detail (`blog__best-invoicing-tools-for-startups.txt`): "recurring invoices, white-labeled templates, and **up to 100 line items with per-line sales tax**." The API confirms per-line `tax_rate` and `discount_rate` alongside invoice-level `tax_rate` and `discount_rate`.

Distinct product: the **free public Invoice Generator** at `/tools/free-invoice-generator` is a separate, non-account tool with very different limits (`invoice-generator-technical-guide`): invoice name required, invoice number optional, currency select, tax rate, optional shipping, logo upload **max 2MB** (PNG/JPG, recommended 200x200), **max 5 line items** ("limited to prevent abuse"), max file size 10MB, A4 PDF, direct email delivery with PDF attachment, rate limiting, "allow up to 30 seconds for PDF generation". The live page also advertises **"Autofill with AI - Paste an email or describe the invoice"** and brand-color themes (Ink, Blue, Violet, Emerald, Amber, Rose, Custom); country limited to United States / Canada.

### 4.3 Payment acceptance methods

Sources disagree. Recorded verbatim:

| Source | Stated methods |
|---|---|
| `product/invoicing` "How it works" step 03 | "ACH, domestic wire, **international wire**, or check through a secure payment portal" |
| `product/invoicing` Key features ("Pay without an account") | "credit card, debit card, **Google Pay**, ACH, domestic wire, or check" (no international wire) |
| `product/invoicing` Pricing block | "Get paid by ACH, domestic wire, international wire, or check" |
| `help-center/invoicing/accept-card-payments-on-invoices` - what the customer sees | "Credit or debit card / Bank transfer / International wire" (+ Google Pay on supported devices/browsers) |
| Invoicing T&C §3 | "ACH transfer, wire transfer, check, and card, depending on your configuration and eligibility" |
| `blog__best-invoicing-tools-for-startups` (stale) | "pay by ACH, domestic wire, or check" and lists "**No card payments on invoices yet**" as a con |

Payer never needs a Rho account: "0 Rho accounts required for the person paying your invoice." T&C §1: "Your invoice payers do not need a Rho Account to pay an invoice."

### 4.4 Card acceptance via Stripe (the only processing fee in Rho's AR stack)

`accept-card-payments-on-invoices` + T&C §4:

| Parameter | Value |
|---|---|
| Processor | **Stripe, Inc.** |
| Fee | **2.9% + $0.30 per transaction**, paid by the business |
| Payer pays | Invoice amount only; **surcharging not available** |
| Daily limit | **$10,000 per day across all invoices** (T&C: "default processing limit of $10,000 USD per day") |
| Currency | **USD invoices only** |
| Invoice types supported | **One-time, full-amount USD invoices only**. Partial payments, overpayments, recurring invoices and non-USD invoices must be paid by bank transfer or international wire |
| Who can connect | **Account Owner or Admin only** |
| Existing Stripe account | **Cannot be connected.** "Rho creates and manages a separate account for your business, so payout details and Payment Portal settings can't be changed directly in Stripe" |
| Verification | Stripe's form (business + beneficial owner info); "may take a few business days"; documents go directly to Stripe and are **never stored by Rho** |
| Statuses | **Pending** / **Action required** / **Connected** / **Failed** (can resubmit immediately) |
| Settlement | Funds deposited to **Primary Checking**. Invoice marked **Pending payout** while Stripe prepares the deposit, then **Paid** once the payout is initiated. **First card payment may take up to two weeks** while Stripe completes initial review |
| Other limits | Card payments count toward the daily card payment limit; higher limits and refunds require contacting Rho Client Service; Rho contacts the business if a dispute needs documentation |
| Card data | Collected and stored by Stripe, "never stored by Rho" |

Connect paths: **Administration → Integrations → Payment integrations → Stripe → Connect → Set up account**, or inline from the invoice's **Payment collection → Accept credit cards → Setup Stripe integration**.

Legal framing (T&C §4): Rho "acts solely as a technology provider enabling the integration and is not a payment processor or bank"; the business is bound by the **Stripe Connected Account Agreement** and **Stripe Privacy Policy**, plus card network and PCI rules; Rho disclaims responsibility for verification outcomes, declines, chargebacks, reserves, holds.

### 4.5 Cash application / payment matching

- Marketing: "The moment cash lands in your Rho checking account, it auto-matches to the right invoice. No manual reconciliation."
- Changelog 04/30/2026: "Invoices auto-marked as paid. When an incoming payment matches the invoice, Rho marks it paid automatically."
- **Virtual account numbers** appear on invoices "to minimize risk from unauthorized debits" (changelog 03/25/2026) and to keep real bank details off the invoice (blog).
- Explicit legal disclaimer, repeated on both the product page and T&C §3: **"Rho does not guarantee that any payment will be initiated, authorized, completed, or settled, or that any payment will be automatically matched to a particular invoice."** T&C also puts the burden on the customer: "You are responsible for reviewing and confirming the accuracy of payment matching, reconciliation, and reporting output generated by the Service before relying on it."
- The API models a `confirm_payment` status and a `matched` activity, implying matched-but-unconfirmed payments require human allocation (sandbox example note: "Wire received - confirm allocation.").

### 4.6 Dunning and reminders

**This is the weakest-documented area of the AR product.**

- No help-center article, product page, or T&C clause describes automated payment reminders, dunning schedules, late fees, or escalation for Rho Invoicing.
- The only evidence reminders exist at all is the API: `invoices.activities.activity_type` includes **`reminder_sent`**, with an `emails` array. In the sandbox data, every `reminder_sent` event carries a non-null `user_id` (`40000000-0000-4000-8000-000000000003`), whereas system-generated events (`matched`, `card_payment_received`, `accounting_synced`, `payment_accounting_synced`, `marked_as_unpaid`) carry `user_id: null`. **Inference: reminders are user-triggered, not automated dunning.**
- `overdue` is a first-class invoice status, and an **invoice aging report** shipped 08/03/2026, so the data exists for a dunning workflow that is not described.
- Rho's own advice in its invoicing FAQ is manual: "Send a polite reminder the day after the due date, then follow up weekly until the invoice is paid. Stating a late fee policy on the invoice up front makes enforcement expected rather than adversarial."
- Rho's comparison table credits **Stripe** with "Smart Retries and automated reminders" and lists Rho's own recurring-invoice and payment-matching cells as **"Not shown."** **[Rho claim about Stripe]**

### 4.7 Invoicing API surface and enums (strongest source of hard product truth)

`docs/docs_v1_invoicing.md`, `api/invoicing_*.md`, sandbox JSON. Scope required: **`invoicing:read`**. Stable `v1` contract, additive-only. Amounts are **integer minor units** (USD `124500` = $1,245.00). Ordering: creation time, newest first, not configurable.

**Invoice status enum (6 values):**
`paid` · `unpaid` · `cancelled` · `overdue` · `confirm_payment` · `pending_payout`

**Payment type enum:** `received_in_account` · `external`
**External method enum:** `cash` · `check` · `credit_card` · `other`
(Note: card payments in the sandbox are recorded as `type: "external"` with `external_method: "credit_card"` and a null `transaction_id`, while ACH/wire receipts are `received_in_account` with a `transaction_id`. So Stripe card settlements are modeled outside the bank-transaction ledger at the invoice level.)

**Activity type enum (11 values):**
`created` · `sent` · `downloaded` · `matched` · `marked_as_paid` · `marked_as_unpaid` · `cancelled` · `reminder_sent` · `card_payment_received` · `accounting_synced` · `payment_accounting_synced`

**Accounting sync status enum (5 values)** - the clearest statement of AR sync semantics anywhere in the corpus:

| Value | Meaning (verbatim from docs) |
|---|---|
| `not_pushed` | "eligible to be pushed after being unskipped" |
| `synced` | "successfully synced to the integration" |
| `error` | "the most recent sync attempt failed. `accounting_synced_at`, when present, remains the timestamp of the last successful sync" |
| `skip` | "explicitly excluded from syncing" |
| `object_changed` | "previously synced, but changed since the last successful sync" |

Note the two distinct sync activities: **`accounting_synced`** (the invoice) and **`payment_accounting_synced`** (the payment) - matching the help-center statement that invoice and payment sync are separate steps.

**Invoice object fields:** `id`, `invoice_number`, `total{amount,currency}`, `tax_rate` (invoice-level %), `discount_rate` (invoice-level %), `status`, `note`, `due_date` (nullable), `date`, `customer{id}`, `line_items[]`, `payments[]`, `activities[]`, `file_id` (present only when a PDF exists), `accounting_sync_status`, `accounting_synced_at`, `created_at`, `updated_at`.
**Line item fields:** `name`, `unit_price{amount,currency}`, `quantity` (fractional allowed - sandbox has `2.5`), `discount_rate`, `tax_rate` (null → invoice-level rate applies), `total{amount,currency}` ("Line total after discount, before tax").
**Customer fields:** `id`, `legal_name`, `email` (nullable), `address{address1,address2,city,country,zip_code,state}`, `note`, **`cc_emails[]`**, **`total_revenue{amount,currency}`** ("Total amount collected across paid invoices"), `last_invoice_id`, `created_at`, `updated_at`, `deleted_at`. Soft delete: deleted customers excluded from list unless `include_deleted=true`; get-by-id still returns them while the record exists.
**List filters:** `status[]`, `due_date_after/before`, `date_after/before` (all inclusive), `page_size` (default 20), `page_token`. Customers list adds `search` (case-insensitive substring on legal_name and email), `include_deleted`, `sort_by` (default `created_at`), `order` (default `desc`).
**PDFs:** `GET /invoicing/invoices/{invoice_id}/files/{file_id}` returns `file_id`, `file_name`, and a "fresh, short-lived signed `download_url`"; "do not persist that URL."

Sandbox data points worth carrying: invoice numbers run `INV-2026-0001` … `INV-2026-0070`; observed tax rates 0, 6.25, 8.5, 10; observed discount rates 0 and 5; largest invoice $100,000.00 (`10000000` minor units, "ERP connector", status `confirm_payment`, sync status `object_changed`). Customer `cc_emails` supports multiple AP contacts (e.g. `ap@acmesupplies.com`, `billing@acmesupplies.com`).

**Conspicuously absent from the API:** no write endpoints (read-only; changelog 08/03/2026: "Read-only is live today. Write access and webhooks are next."), no Bill Pay / AP endpoints at all, no vendor endpoints, no accounting-sync endpoints. The API covers accounts, cards, statements, transactions and invoicing only.

### 4.8 Invoicing Terms and Conditions (`/policies/invoicing-terms-and-conditions`)

Header date **August 25, 2026**; body says **"Last amended August 26, 2026."** (internal inconsistency). Entity: Under Technologies, Inc. dba Rho Technologies. These Terms **control** over other Rho Agreements in a conflict.

Notable clauses beyond fees and card processing:
- §1: requires "an active Rho Account that is in good standing"; Rho "may condition, limit, suspend, or terminate access … including where required by law, by a partner bank or processor, or by applicable risk, compliance, or underwriting requirements. Approval is not guaranteed, and eligibility for one feature does not confer eligibility for another."
- §2: customer is solely responsible for invoice content, accuracy, legality, amounts, payment terms, **tax treatment**, branding, payer contact info. "Rho is not a party to any transaction between you and your invoice payers, does not verify the validity of any invoice, and has **no obligation to collect, enforce, dispute, or resolve any invoice, chargeback, refund, or customer dispute** on your behalf." (This is the formal statement that Rho does not do collections/dunning on your behalf.)
- §3: "Payments are settled to the Rho checking account you designate."
- §5: third-party integrations governed by the third party's terms; approval "is not guaranteed and may be revoked at any time."
- §8: "as is"/"as available"; no warranty "that any data, calculation, matching, or report produced by the Service will be accurate or complete." Explicitly not tax/accounting advice; "You are solely responsible for determining the tax treatment of your invoices and payments, for issuing any required tax documentation."

---

## 5. Accounting automation and sync mechanics

### 5.1 Integration inventory and connection type

Sources: `how-to-link-rho-to-your-accounting-software`, `faq.txt`, `product__close.txt`, `what-is-rho-close`, `integrations.txt`, `site-llms-full.txt`.

| Platform | Connection type | Evidence | Marketing page | Help-center setup guide |
|---|---|---|---|---|
| **QuickBooks Online** | Native direct (OAuth) **and** Bank Feed (token) | `how-to-set-up-rhos-quickbooks-integration` | Yes | Yes |
| **Oracle NetSuite** | Native direct (SuiteBundle 436739 + TBA REST/SOAP) | `how-to-set-up-rhos-netsuite-integration` | Yes | Yes |
| **Sage Intacct** | Native direct (Web Services user + sender ID `rho.co`) | `how-to-set-up-rhos-sage-intacct-integration` | Yes | Yes |
| **Xero** | **Bank feed only** | `how-to-set-up-rhos-xero-integration` | Yes | Yes |
| **Puzzle** | Native direct (replaces a Plaid connection) | `how-to-link-rho-to-your-accounting-software`, `what-is-rho-close` | Yes (waitlist page) | **No dedicated setup guide** |
| **Campfire** | Claimed as an accounting/ERP integration on the integrations hub | `integrations__campfire.txt` only | Yes | **Zero help-center coverage** |
| **Microsoft Dynamics 365 Business Central** | Referenced in sync-error strings and self-description; **no marketing page, no help guide, not in the sitemap** | `guide-to-solving-accounting-issues` (3 Business Central-specific errors), `site-llms-full.txt` line 17 and 43, 9 blog posts | **No** | **No** |
| QuickBooks Desktop | Not integrated. CSV download + batch import / convert to a QB-compatible file | `how-to-set-up-rhos-quickbooks-integration`, `how-to-export-csvs-for-reconciliation` | - | - |

Notes:
- `faq.txt` and `product__expense-management.txt` consistently list natives as **QuickBooks Online, NetSuite, Sage Intacct, Puzzle** and put **Xero on a bank feed**: "Xero connects today through a bank feed rather than a native sync."
- Contradiction inside `product__expense-management.txt`: one FAQ answer says "businesses using a direct accounting integration - QuickBooks Online, NetSuite, Sage Intacct, **Xero**, or Puzzle"; another says Xero is bank-feed-only.
- The Xero marketing page claims "Rho's native Xero Integration" and "Configure and sync transactions across all your **Xero subsidiaries**" - both contradicted by the help-center Xero article, which describes a pure bank feed with account mapping.
- Sage (non-Intacct) is listed under `rhos-supported-cash-flow-apps` as **supported only through Plaid**, with "We don't have custom fields explicitly for Sage. However, you can repurpose labels and budgets for the flat file upload."

### 5.2 Sync cadence table (every documented timing in the corpus)

| Mechanism | Cadence / time | Source |
|---|---|---|
| Transaction sync (direct integration) | **Manual by default.** "Syncing with your QuickBooks account is a manual process. Each time you want to reconcile … you must click the Sync button." | `how-to-set-up-rhos-quickbooks-integration`, `how-to-sync-to-quickbooks` |
| **Recurring Syncs** (direct integration) | Run automatically at **3:00 AM ET (8:00 AM UTC)** on the scheduled sync date; include everything available before that time | `setting-up-recurring-syncs-...` |
| **Bill pull** from accounting platform → Rho | **Every 24 hrs at ~12:00 AM EST**; manual "Sync Bills" button at the top of the Bill Pay tables | `how-rho-syncs-bill-pay-data-in-your-accounting-system-` |
| **QuickBooks Bank Feed** | "automatically pushes all transactions … **daily**" | `quickbooks-bank-feed-vs-direct-integration` |
| **Xero bank feed** | "every 24 hours. The daily bank feed sync occurs each day at **3:00 AM EST**" | `how-to-set-up-rhos-xero-integration` |
| **Merchant → Vendor auto-creation** | "This process occurs **every 6 hours**" after 3+ transactions with a merchant | `creating-vendors-from-merchants` |
| **Mastercard Smart Data card feed** to T&E software | **1 time per day, Monday-Saturday, after 5 PM EST** | `how-to-set-up-a-card-feed-integration` |
| **HRIS sync** | "You can sync HR changes to Rho **every 24 hours**… Currently, **syncs are triggered in-app**" (manual) | `how-to-use-rhos-hris-integrations` |
| AP invoice sync (Rho → QBO, AR side) | "happens automatically in the background" when the invoice is sent; the **payment** must be synced manually or included in automated syncs | `syncing-invoices-to-your-accounting-software` |
| Bill Pay daily digest | 5 pm EST | `how-to-configure-bill-pay-notifications` |
| Bill Pay weekly digest | 10 am EST Friday | same |
| Scheduled payment release | ~4:00 a.m. ET | `how-to-schedule-a-bill-payment-in-rho` |

Recurring sync setup: **Accounting → Settings → Recurring Syncs → Add Sync** → choose transaction types + rules.

### 5.3 What syncs: object model per direction

**Transaction types syncable** (`how-to-sync-rho-transactions-with-your-accounting-software`): tabs are **Banking, Card, Accounts Payable, Reimbursement**, plus **Treasury** which is "currently supported only for QBO and NetSuite."

Per-transaction and bulk sync, plus an explicit **Skip sync** action (and a corresponding error if you try to sync a skipped transaction).

**QuickBooks object mapping** (`quickbooks-dashboard-views`, 12 views):
Credit Card Purchase · Credit Card Refund · Credit Card Payment · Bank Transaction (outgoing) · Bank Transaction (incoming) · Bank Transaction (transfer) · AP (bill) · AP (bill payment) · Reimbursement (bill) · Disbursement (bill payment) · Treasury (deposit) · Treasury (withdrawal)

**NetSuite module mapping** (`netsuite-integration-faqs`):

| Rho transaction | NetSuite module |
|---|---|
| Corporate Card - Monthly Card | Credit Card module |
| Rho Card with Daily Terms | Check module |
| Bank transactions (incoming/outgoing ACH, wires, transfers between accounts) | Check, Deposit, and Journal Entry modules |
| AP (bill) | Bill module |
| AP (payments) | Bill Payment module |

NetSuite field placement: **Transaction level** - Subsidiary, Vendor, Account. **Expense/line level** - Account, Department, Class, Customer, Location, Vendor. **Memo** - `[Cardholder] to [merchant]` e.g. "John to Uber". **Receipt** - synced as a file attachment, viewable at Transaction View → line item section → communication files.

**Puzzle** (`integrations__puzzle.txt`, direct integration, replaces Plaid): "ACH, wires, internal and external transfers, card expenses, bill payments, reimbursements, treasury activity (interest, dividends, unrealized gains/losses, fees), and refunds and reversals." Posting semantics: **"Accrual events like reimbursement creation post as journal entries. Cash events like disbursements post as transactions."** Metadata carried: vendor names, memos, classes, projects, COA mappings. Rho's auto-categorization and sync rules "work natively." Availability: "Early access is available now through the waitlist. **Full availability rolls out in April 2026**" - but the changelog says Puzzle shipped **February 26, 2026** ("Rho now integrates directly with Puzzle … Setup takes 30 seconds"), so the Puzzle page is stale relative to the changelog. Multi-entity: "Puzzle doesn't currently support multi-entity natively … Puzzle recommends using their 'Join' feature."

**Campfire** (`integrations__campfire.txt`): "Sync all transactions directly to Campfire - from corporate cards to banking to AP"; "Easily split a single AP or banking transaction into many - across your Campfire Chart of Accounts & Vendors"; multi-subsidiary claimed.

**Receipts**: sync to QuickBooks if stored in Rho; **not supported when syncing Treasury transactions**. Attachment size limits are enforced by the ERP ("Attachment size too large" error).

### 5.4 Bill sync directionality (the two-way AP model)

`how-rho-syncs-bill-pay-data-in-your-accounting-system-` and `how-to-reconcile-rho-bill-pay-with-quickbooks`.

Supported for **QuickBooks Online, NetSuite, Sage Intacct** only (Puzzle, Xero and Campfire are not listed for bill sync).

Two record types: **Bills** (push or pull) and **Bill Payments** (push only).

**Direction 1 - Rho → ERP (bills created in Rho):**
- When the bill is **sent to payments**, the full bill record syncs as an **Open / unpaid bill**, including all accounting attributes and any splits.
- Re-sync of **accounting attributes** is allowed "all the way up until the related bill payment is in a settled state."
- **Key data points (amount, vendor, due date, invoice #) are immutable after the first sync.** Correction path: edit directly in the accounting platform, or **void the bill and recreate it**.

**Direction 2 - ERP → Rho (bills created in the ERP):**
Setup: **Bill Pay → Settings → "Enable Bills from [accounting software]" / "Enable Account Payable from QuickBooks" / "Use Accounts Payable from [Accounting Software]"** → toggle On → select a start date (pulls bills with an Invoice date from that day forward) → Enable/Save. (Three different label strings across three articles for the same toggle.)

Eligibility criteria for a bill to sync into Rho (`how-to-enable-bill-sync-from-your-accounting-software`):
1. Bill must be **open and not marked as paid** in QuickBooks Online
2. Total must be **greater than $0**
3. Must include **at least one line item**
4. Must be **no more than 30 days old** to appear automatically
5. **Vendor must be active in Rho and mapped** to the corresponding ERP vendor

Bills meeting criteria sync **every 24 hours at ~12 AM EST**; a manual "Sync bill from QuickBooks" button plus "Refresh" are available. Resulting payment drafts land in **Bill Pay → Payments → Drafts** with payment details pre-populated.
**Pulled bill details are read-only in Rho** ("not editable from Rho, but can be edited from your accounting platform").

**Bill payments (always Rho → ERP):** once a payment is **scheduled and paid (settled)**, it (1) automatically inherits attributes from the related Bill record and (2) appears as ready to sync in **Accounting → Dashboard → Bill Pay**. When the bill payment syncs, the related bill's status in the ERP is **automatically updated to Paid**, "regardless of whether it was pushed or pulled to Rho."

**Ledger mapping prerequisite:** **Accounting → Mapping Rules → Ledgers** - select the AP account that represents Bill Pay, **per entity/subsidiary** (toggle entities in the left nav). "Make sure to do this for all entities that will use the Bill Pay solution."

### 5.5 AR invoice sync (QuickBooks Online only)

`syncing-invoices-to-your-accounting-software` + changelog 08/31/2026.

- **"Available for QuickBooks Online only. … It is not yet available for other accounting integrations. Support for additional platforms is on the roadmap."**
- Setup: Accounting (or Settings → Integrations) → confirm QBO connected → enable **"Sync invoices and customers to QuickBooks"** → set the **Default Accounts Receivable Ledger** ("Without this, we won't know where to sync your invoices").
- What syncs: the **invoice when it is sent** (customer details, line items, amounts, due date); the **payment when received**, applied against the matching invoice; **status updates across the lifecycle** so open and paid balances stay current.
- Matching: "Customers, invoices, and payments are matched to the correct records in QuickBooks, so you avoid duplicates."
- Backfill: "any invoices you send from Rho will sync on a go-forward basis. **We'll also sync all of your existing invoices** … Though you'll have to **manually sync the invoice payment** or include invoice transactions in your automated syncs."
- Updates/deletes: "If an Invoice is updated or deleted, there is nothing needed from you. Rho syncs after each step."
- Changelog framing: invoices land "as accounts receivable invoices, not generic bank deposits."

Manual reconciliation note when not using the sync (`how-to-reconcile-invoices-in-your-quickbooks-account`): "use the **Receive Payment** option instead of recording it as a **Bank Deposit**" so the invoice can be marked paid; then Chart of Accounts → account → view register → Edit → set customer in "Received From" and select **Accounts Receivable** in the Accounts column → Save and close.

### 5.6 GL coding: mapping rules, hierarchy and attributes

`how-does-coding-in-rho-work`, `how-to-create-mapping-rules-in-rho`.

Three coding mechanisms, in order of the article: **Mapping rules**, **Line-level (manual) coding**, **Default settings** (Default Income, Default Expense, Default Bill Pay accounts).

**Mapping hierarchy - rules are checked in this exact order:**
1. **Label**
2. **Sender**
3. **Vendor**
4. **Merchant**
5. **Card**
6. **Department**

Worked example from the docs: with rules `Vendor = Cindy's Cookies → GL = Meals and Entertainment` and `Card = *1234 → GL = Miscellaneous`, a transaction on Card *1234 at Cindy's Cookies gets **Meals and Entertainment** (vendor beats card).

**Advanced (complex) rules**: one rule can set many attributes at once. Documented example: "if the vendor is Starbucks, then the location is New York, the department is Marketing, the class is Social, and the customer is Jack." Created from a rule's three-dot menu ("Create Advanced Rule") or the **Advanced Rules** tab.
**Conflict resolution: "Rho prioritizes the more complex rule."**

**Account Mapping**: connects any Rho account (**Card, Checking, Treasury, or Accounts Payable**) to an existing or newly created Chart of Accounts entry.

**Ledger defaults**: the Ledger tab holds default rules directing "all unmapped transactions to a specific Income and Expense ledger."

**Temporality - important:**
- "Mapping rules apply **forward-only** from the time they are created."
- "Any rules already applied to past transactions are unaffected, unless you navigate to the **Accounting tab → three dots → Apply Mappings → select the timeframe → Apply**."
- **"Please note that this action will override all manual coding."** / "using the Apply Mappings option … will override existing codings, including those set manually."
- Otherwise "Rho respects user-selected codings and does not update them with new mapping rules."

**Attribute vocabulary that can drive rules** (`how-to-create-mapping-rules-in-rho`): Custom Attributes (= any ERP dimension), Departments (cost centers), Labels (= classes in the accounting system), Cards, Merchants, Merchant Categories, Vendor.

**ERP attributes imported into Rho** - NetSuite list is the only explicit one: **Chart of Accounts, Classifications, Customers, Departments, Locations, Vendors**. General statement from the dashboard article: "common attributes are Chart of Accounts, Vendors, Classes, Projects, and Departments."

**Refresh requirement**: after creating accounts/vendors/attributes in the ERP, click **Refresh Attributes** (Accounting → Dashboard → three dots → Refresh attributes, or the top-right button). "It's important to refresh attributes whenever changes are made in your mapping rules or accounting software." NetSuite-specific: "each time a new Vendor is created in NetSuite, you must click on the Refresh Attributes button."

**Two parallel custom-dimension models coexist in the corpus:**

| | Custom Attributes (legacy) | Fields (newer accounts) |
|---|---|---|
| Limit | **Up to 5** discrete categorizations | **Up to 7** active Fields (archived do not count) |
| Types | Free Text or Multiple Choice | Predefined list or Free text |
| Setup | Settings → Configuration → Custom Attributes | Settings → Fields |
| Default on cards | Card Settings → Advanced Controls → "Assign Rho Attributes" (Off by default); **multi-select attributes only**; one value per card | Any card can carry a default option per Field; transactions show an **AUTO** indicator until overridden |
| Bulk value import | Yes, for multi-select | Yes, paste comma-separated values; duplicates skipped |
| Expense-rule enforcement | Yes, via Expense Rules action section | Yes, e.g. "require Category on every card transaction over $50" |
| CSV export | One column per attribute | One column per active Field; **split transactions export one row per split line** |
| Scope | Card and banking transactions | "every transaction type: card transactions, banking transactions, payments, **bills**, reimbursements, and **invoices**", plus cards |
| Starter set | - | Field named **Category** pre-filled with 10 options: Software & Subscriptions, AI & Compute, Marketing, Travel, Food & Meals, Office & Supplies, Equipment, Contractors, Legal, Other |
| Reporting | Departments/Labels pages under a Reporting tab | **"Your account does not include a Reporting tab"**; spend views live on transaction tables; "Fields-native reporting views are on the roadmap" |
| Notable exclusions | - | Fields do **not** apply to users/people; **card repayments do not carry Fields** (to avoid double counting); card purchase refunds do |
| Permissions | Manage attributes / Manage attribute values | View fields / Edit field values / Manage field configuration |

Renaming a Field option "updates it everywhere it has been applied, including past transactions." Archiving never deletes history but silently breaks any expense policy rule that required the archived Field.

Changelog 08/31/2026 adds: "**Map account attributes by your own Rho attributes.** Use custom attributes as an input in mapping rules."

### 5.7 Merchant → Vendor auto-creation

`creating-vendors-from-merchants`:
- Automatically creates vendor profiles **in the GL software** when you spend with a merchant **more than three times**.
- Runs **every 6 hours** ("Vendors will not be populated immediately").
- **Off by default**; toggled on from the settings page.
- **Not retroactive**: "only considers merchants after the toggle is turned on."
- "We perform **smart matching** to ensure there will not be duplicate Vendors created in your GL software."
- **Direct integrations only** - "users on our bank feed connections for QuickBooks and Xero will not be able to utilize this feature."

### 5.8 The Accounting Dashboard

`understanding-the-accounting-dashboard`:
- "Command center for your accounting workflows": integration status, sync status per transaction, accounting attributes per transaction.
- **Filters**: transaction status, transaction type, **missing accounting attributes**, and **transactions whose attributes changed since they were synced** to the GL.
- **Custom views**: choose which attributes to show and in what order; sortable across most attributes/datapoints.
- Sync status visibility, sync/skip toggles, sync error surfacing with remediation.
- "Request a referral to an outsourced accounting partner who is an expert in Accounting and the Rho platform."
- "You can take advantage of our **AI co-pilot tool**" (named nowhere else; presumably Rho Close).
- Changelog 02/26/2026: "Smarter Accounting dashboard. Transaction details are now enriched with more context directly in your Accounting dashboard."
- Changelog 03/25/2026: "Redesigned accounting mapping rules. The mapping rules tab is now organized into collapsible sections."

**Roles with accounting-dashboard access** (six, including three partner roles for external accountants):

| Role | Access |
|---|---|
| Account Owner | Full access: balances, departments, financial operations |
| Administrator | Comprehensive access: balances, departments, financial operations |
| Bookkeeper | "View all" with limited action permissions; can view all balances and transactions but **requires approvals to send them** |
| Partner Admin | Manage accounting integrations, configure account settings, perform money-movement activities |
| Partner Expense & Accounts Payable Manager | Manage accounting integrations, **create and pay bills**, approve/reject expenses |
| Partner Accountant | **Read-only** on transaction and bill data; can configure and sync transactions to integrations; can **generate bank feed tokens** |

Mobile app coverage (`how-to-code-accounting-attributes-in-the-mobile-app`): Accounting section appears in the transaction drawer only if Accounting Integrations are enabled. Can view/modify accounting details for **Banking transfers, Expenses, Reimbursements**; can **view** (not edit) accounting details for **AP Bills pending approval** in the Approvals tab; supports per-split Accounting sections. **Not on mobile**: sync status and transaction syncing, mapping rules, accounting settings.

---

## 6. Rho Close (month-end close)

Sources: `product/close`, `help-center/accounting/what-is-rho-close`, changelog 05/27/2026, blog announcement "Introducing Rho Close: Intelligent Transaction Coding for Startups" by Esther Nguyen, **published May 06, 2026, updated September 01, 2026, 5 minutes**.

**What it is:** suggested accounting attributes for transactions, learned from your own history. "It learns how your business has coded transactions and delivers suggestions upon request."

**Inputs to the model:** "your chart of accounts, your vendor history, and every coding decision you've made on Rho. It builds a suggested first pass based on how your business actually codes, **not a generic model trained on someone else's books**."

**Coverage and limits (help center, the most precise source):**
- Generates suggestions for **card and banking transactions** only.
- **"It does not currently create or modify mapping rules."**
- **"It does not deliver suggestions for accounting attributes where an accounting attribute has already been selected"** (empty attributes only).

**Enablement:** **Accounting → Settings → General**; **toggled on by default**.

**Invocation:** Accounting Dashboard → **"Suggest coding"** button above the transaction table. "Rho Close will generate suggestions for empty accounting attributes across the card and banking transactions **in your current view**" (so filters scope the run).

**Review model - three levels:**
1. **Bulk** - accept all suggestions across the transactions view in one click (bulk accept/dismiss buttons appear at the top of the table).
2. **Per transaction row** - accept or dismiss for a single transaction.
3. **Per attribute** - hover the cell and click the checkmark to accept; or dismiss/override by selecting a different attribute from the dropdown.

**Default-on-sync behavior (a real gotcha):** "If you do attempt to sync your transactions in bulk **without accepting or dismissing** the suggestions, you can decide whether to accept the suggestions or not as part of the sync." And for a single transaction: **"If you do sync an individual transaction without actively accepting or dismissing the suggestions, those suggestions will be applied to the sync."**
This conflicts with the product page's emphatic "Nothing syncs until you approve it. Every time." and FAQ "Does Rho Close automatically sync to my accounting software? **No.** Nothing syncs until you review and approve it. … Every step requires your sign-off."

**Learning loop:** "Every time you accept or override a suggestion, Rho learns from that decision. Over time the suggestions match your coding patterns more closely."

**Integration prerequisite - two conflicting lists:**
- Help center: "available for businesses with a direct accounting integration (**QuickBooks, NetSuite, Puzzle, or Sage Intacct**)."
- Product page FAQ: "**QuickBooks Online, Oracle NetSuite, and Sage Intacct** via native direct integration. **Xero is also supported via bank feed, with coding handled on the Xero side**." (Puzzle omitted; Xero added.)
- Both agree a direct integration is required: "If you're currently exporting CSVs, you'll need to connect a supported integration."

**Access:** "Anyone with access to the accounting view on Rho … the founder, a first finance hire, or an outsourced accountant. Permissions follow your existing Rho account settings."

**Pricing:** "Rho Close is included with your Rho account."

**What Rho Close is NOT (conspicuously absent):** there is no close **checklist**, no task list, no period lock, no close calendar, no reconciliation sign-off, no flux/variance analysis, no accrual or journal-entry builder, no close status dashboard, and no multi-entity close consolidation anywhere in the corpus. Despite the marketing frame "Your path to a seamless month-end close," Rho Close is scoped to **transaction coding suggestions** only. The only close-period control mentioned is the ERP's own: the sync error "**Accounting period closed**: Rho is unable to sync a transaction to a closed period. Please skip syncing this transaction and manually record the transaction in your GL software. … This is a manual setting in your accounting software."

---

## 7. Sync error catalog (`guide-to-solving-accounting-issues`)

The single most informative page about how the sync actually behaves. 32 distinct error strings. Grouped:

**Connection / configuration**
- "Accounting Connection is not valid" → reconnect with valid credentials
- "We need to know the default ledgers you want to use for all transactions" → Accounting → Mapping Rules → Ledgers
- "Missing mapping rule for Node _0000" → "A primary Cash (Checking) account does not have a mapping rule"
- "This feature is not included in your subscription plan for accounting software" → upgrade the ERP plan

**Period / lock**
- "Accounting period closed" → skip sync and record manually
- "This transaction has been locked in your accounting software" → manual adjustments only
- "This transaction has already been recorded in your accounting software … The transaction has been paid and is no longer editable"

**Deleted / voided upstream**
- "This transaction was already synced from Rho but has since been deleted in your accounting software" (two variants, one for deleted, one for voided) → skip and record manually
- "This Bill has been deleted. Please skip the transaction from syncing or unarchive the Bill"

**Bill readiness**
- "This Bill is not yet ready to sync. You can sync this bill after it has settled" → "Click on **Send to Payments** to process the bill"
- "This Bill is not yet ready to sync. You can sync this bill when it moves to **Processed** state"
- "Transaction has not settled" → wait or skip
- "Transaction has no amount" → skip
- "We need you to fill in the missing field" → named examples: **Invoice Number, Invoice Date, Due Date, Vendor**

**Attribute validity**
- "Accounting attribute is invalid, missing, or cannot be applied to this transaction"
- "Invalid accounting attribute reference" (e.g. wrong account type for a bill)
- "Selected value does not exist in ERP"
- "Unable to push transaction, no **Account** found" / "no **Location** found" / "no **Vendor** found"
- QuickBooks-specific: "**You can't use an Accounts Payable account on the detail portion of a Bill**" - "bills are meant to increase liabilities (AP), not directly expense them"

**Ordering dependencies (matters for close sequencing)**
- "**Associated bill must be pushed before payment record.** Please sync associated bill and then resync the payment."
- "**Associated reimbursement must be pushed before the payment record.** … Ensure that the payment has settled. Sync the reimbursement first. Then sync the disbursement."
- "**Reimbursements must have a single vendor for all transactions.**"

**Splits and lines**
- "Split transactions do not add up to total transaction amount"
- "**Transaction line count does not equal to ERP**" - "The number of splits in Rho does not match the number in **Business Central**"
- "You must enter at least one line item for this transaction"
- "Journal does not exist, please create it in your ERP" - "in your **Business Central** account"

**Attachments**
- "Attachment size too large: please upload a smaller attachment or compress the file"

**Operational**
- "You've selected to skip this transaction when syncing"
- Generic internal error → contact Client Service

Troubleshooting checklists on the same page:
- Values not pulling from the accounting software → Accounting → Dashboard → three dots → **Refresh attributes**
- Bills not appearing in Rho → check amount is not $0; check bill creation date (bills older than 30 days may not pull unless a different initial pull date was set); confirm the "Use Accounts Payable from [Accounting Software]" toggle is On; confirm the vendor exists, is active, and has a mapping rule or a default vendor; check Bills vs Payments tabs; remove filters; run a manual **"Sync bill from [Accounting Software]"** then **Refresh**.

---

## 8. Reimbursements in the accounting chain

`how-rho-syncs-reimbursements-in-your-accounting-system`, `how-to-approve-and-disburse-a-reimbursement-request`, `how-to-use-mileage-reimbursements`:

- Two-object model mirroring AP: **the reimbursement syncs as a Bill in QBO**, then **the disbursement syncs as a Bill Payment**, which marks the bill paid.
- **Sync order matters**: reimbursements first, then disbursements. All transactions must be **settled** before syncing.
- Approval: reimbursements not auto-approved by documentation rules require manual approval; filters include **Awaiting Approval** and **Awaiting Payment Approval**; single, row-level, and bulk approve all supported.
- Disbursement: **one payment per user** aggregating pending disbursements ("Pay Total"); ACH only, **domestic bank accounts only**.
- Cutoff: "Payouts submitted **before 3 p.m. ET** should arrive in your employees' accounts the same day. If submitted after 3 p.m. ET, funds will arrive the next business day."
- "Mark as Paid" for reimbursements paid outside Rho (e.g. via payroll) removes them from the disbursement queue.
- Statuses: Awaiting Approval → Pending Payment → Paid.
- **Mileage**: Rho pre-populates the current year's **IRS rate of $0.70/mile**; admins/owners can override. Rate applied is "the rate your business set **when the expense occurred**." Embedded map auto-calculates mileage from start/end points. Requires an AP Chart of Accounts mapping rule to sync to the ERP.
- Changelog 05/27/2026: "Retry failed or canceled reimbursements … individually or in bulk."
- Changelog 03/25/2026: "Edit reimbursements" before processing.

**Expense approvals (distinct from bill approvals, and richer):** `how-to-set-up-approvals-for-expenses`, `how-to-set-up-direct-manager-approvals`.
- Path: **Settings → Expense Settings → Expense Approvals**.
- Dollar-threshold tiers with auto-approve floors. Documented example: under $10 auto-approve; over $10 tier-1 approver; over $500 (one article) / over $1,000 (the other article) tier-1 + tier-2; over $10,000 three tiers.
- **Direct manager approvals**: routes up the manager chain; managers assignable manually (Users → Assign Managers) or imported from an **HRIS integration**. "Direct managers can be assigned solo to a tier or combined with a static user. When multiple approvers are in a tier, **any one of them can approve or reject**."
- **Immutable thresholds**: "Once you create an approval tier, you won't be able to change the amount. To make changes, you can create a new tier and delete the old one."
- Expense rules are **post-spend controls**: "Expense rules will not cause Rho Cards to get declined."
- Rule conditions: All expenses (with Exceptions), Amount, Department, Merchant category, Custom (combined conditions). Requirements that can be demanded: **Receipt, Note, Attendees, Client ID, Department, Label**, plus "Mark expense as out of policy."

---

## 9. Integrations inventory (every integration page in the corpus)

### 9.1 Accounting / ERP (6 marketing pages)

| Page | Pitch line | Distinctive claims |
|---|---|---|
| `/integrations/quickbooks` | "Connect QuickBooks Online and make accounting frictionless" | "Reconcile corporate card **and invoice** transactions in real-time"; "Sync all transactions … from corporate cards to banking to **AP**"; custom rules to map "merchants, categories, budgets, labels, and cardholders"; **multiple subsidiaries**. Testimonial: Tyler Majors, CFO at Native Strategies - "turned an hours-long reconciliation process for the CFO into a **15-minute exercise**" |
| `/integrations/netsuite` | "Connect NetSuite…" | Same three pillars; "Reconcile corporate card **and invoice** transactions in real-time". Testimonial: Sarah Green, Senior Accountant at Dr. Squatch |
| `/integrations/sage-intacct` | "Connect Sage Intacct…" | Corporate card only in the headline ("Reconcile corporate card transactions"); body still says "from corporate cards to banking to AP". **Testimonial is a copy-paste of the NetSuite one** ("The NetSuite integration saves us so much time…") on a Sage Intacct page |
| `/integrations/xero` | "Connect Xero and make accounting frictionless" | Claims a "**native** Xero Integration" and "sync transactions across all your **Xero subsidiaries**" - both contradicted by the help center (bank feed only). Body omits AP: "Sync all transactions directly to Xero" (no "from corporate cards to banking to AP"). Stray heading "Put your idle cash to work" left on the page. Testimonial: Trey Fulmer, Founder & CEO at Luca |
| `/integrations/puzzle` | "Your money moves. Your books are already done." | Full anti-Plaid argument (see §5.3). "**Join the waitlist**" CTA; "Full availability rolls out in April 2026" |
| `/integrations/campfire` | "Connect Campfire…" | "Split transactions with ease. Easily split a single AP or banking transaction into many - across your Campfire Chart of Accounts & Vendors"; multi-subsidiary. Testimonial genericized to "Rho's accounting integration…" |

Common ERP-page boilerplate: "Eliminate manual data entry," "Categorize expenses automatically. Control exactly how transactions appear in your [X] ledger. **Create custom rules to map merchants, categories, budgets, labels, and cardholders**," "Manage multiple subsidiaries."

Integrations hub copy: Accounting & ERP - "**Sync every Rho transaction to your general ledger in real-time**"; HR - "**Book business travel with ease using your Rho Card**" (wrong description, copied from the Travel section); Travel - Navan, Emburse, SAP Concur.

### 9.2 HR integrations (3 marketing pages + the HRIS help article)

| Page | Mechanism |
|---|---|
| `/integrations/bamboo-hr` | "**Merge** integration onboards employees faster to Rho" - names **Merge.dev** as the aggregator |
| `/integrations/workday` | Identical copy, "Merge integration…" |
| `/integrations/gusto` | Identical copy, "Merge integration…" |

All three pages are byte-for-byte identical except the product name. Claims: sync employee directory, assign roles and permissions, "Automatically update employee records, manage team changes, and streamline user access," "Access up-to-date org charts, track departmental changes, and proactively manage permissions."

**Reality per `how-to-use-rhos-hris-integrations`:**
- "We support **over fifty HR system providers**", named: **BambooHR, Freshteam, Hibob, HR Cloud, HR Partner, Humaans, Lano, Namely, Nmbrs, Paychex Flex, Paylocity, Personio, Proliant, Sage HR, SAP Success Factors, Sapling, Square Payroll, TriNet, UKG Pro, UKG Ready** "and more."
- Hub page says "Connect to over **50+** HR platforms."
- Fields pulled per employee: **Name, Email, Phone Number, Role, Direct Manager** (only if the manager is already on Rho or invited in the same bulk invite), **Department, Location, Employment status, Start Date - Termination date, Employee ID, Company Name**.
- **"Rho does not extract any compensation information."** "Rho never modifies any data or information in your HRIS."
- Sync changes: user profile details, manager assignment (direct approvers), new hires, terminations.
- **Sync is manual/in-app, at most every 24 hours.** "Users with incomplete information will not be imported."
- Auth: OAuth or API key; a modal shows exactly which fields will be read before connecting.
- Admin permissions required in **both** Rho and the HRIS.
- **"Rho supports connecting one HR integration at a time."** Disconnect before switching.
- Entry points: Integrations tab, or Users tab → "Connect HR System."
- Compliance note: "We are fully SOC Type 2 compliant and are audited every year."

Separate payroll article: `how-to-connect-gusto-with-rho` (banking category) covers Gusto as a payroll funding source, distinct from the HRIS directory sync.

### 9.3 Travel and T&E integrations (3 pages + Navan)

| Integration | Marketing page | Mechanism |
|---|---|---|
| **Emburse** | `/integrations/emburse` | "Connect Emburse with Rho Corporate Cards"; "Once you swipe your connected Rho Corporate Card, Emburse goes to work. Expenses are automatically categorized, checked against company policy, reconciled, and submitted" |
| **SAP Concur** | `/integrations/sap-concur` | Identical copy; **contains a copy-paste defect**: "Two platforms, one solution - Connect **Emburse** with Rho Corporate Cards…" on the SAP Concur page |
| **Navan** | Listed on the integrations hub and in `site-llms-full.txt` as `https://www.rho.co/integrations/navan` - **that URL does not exist in the 1042-URL sitemap and no page was crawled.** Only coverage is the help article | See below |

**Navan (`understanding-the-integration-between-rho-and-navan-expense`):**
- Linked through **Mastercard Smart Data**; Navan receives Rho transaction logs; Rho-issued cards and their transactions appear in Navan.
- "Navan Expense is a comprehensive expense management tool … not just travel-related."
- Onboarding is **entirely managed by Navan**; joint onboarding call with a Rho representative to set up **Navan Connect**. Rho provides Navan with your **Mastercard Distribution ID**.
- **Receipts must be submitted in Navan. "Adding receipts in Rho will not sync them to Navan."**
- **Spending policies are managed in Navan**; card-level controls (limits, merchant restrictions) stay in Rho and "work alongside Navan's expense policies."
- Support for Navan Connect goes to Navan, not Rho.
- Testimonial reused on the integrations hub: Christian Hailey, Senior Accountant/Financial Analyst, Palladin Technologies - "Rho and Navan together helps eliminate hours I spent previously managing employee expenses."

**Generic card feed mechanics (`how-to-set-up-a-card-feed-integration`)** - the common substrate for Emburse / Concur / Navan:
- Rho Cards run on **Mastercard**, so they connect to T&E software via **Mastercard Smart Data**.
- Setup is concierge: email `clientservice@rho.co`; Rho confirms Smart Data compatibility; the customer notifies their T&E vendor; **Rho provides a Delivery ID** to configure the feed. **Takes 3 to 5 business days** to set up.
- **Data shared:** cardholder name, last 4 of the card number, purchase date, purchase amount, merchant name, merchant category.
- **Data not shared:** "Only transaction data is sent via Mastercard at the time of purchase. We do not send any other data that you share with Rho." (So no receipts, no Rho coding, no departments/labels.)
- **Frequency: 1 time per day, Monday-Saturday, after 5 PM EST.** (No Sunday feed.)

### 9.4 Other connectors relevant to AP/AR/close

| Connector | Notes |
|---|---|
| **Gmail Connector** (`how-to-set-up-the-gmail-connector`, shipped 04/30/2026) | Settings → Integrations → Gmail → Connect (OAuth). Scans the inbox for receipts matching recent Rho card transactions and auto-attaches them. "Rho only requests read access to messages that match receipt criteria." Per-cardholder connection; receipts attach only to that cardholder's transactions. Custom keywords manageable at Settings → Integrations → Gmail → Manage. Requires ≥1 active card and a Gmail/Workspace address; Workspace admin approval may be needed. Disconnecting stops scanning immediately; already-attached receipts remain. Changelog: "Admins can extend the connector across the whole team in one action." |
| **Receipt capture** (`how-to-attach-receipts-to-card-transactions`) | SMS to short code **555746** (US/Canada mobile required) - auto-matched; email to **receipts@rho.co** - auto-matched; reply to a transaction alert - matched to that transaction; mobile app and desktop - user selects the transaction. Multiple receipts per message supported. Changelog 04/30/2026: "Receipt matching, rebuilt. Added **merchant identity verification** to every match, so a receipt from Uber only ever attaches to an Uber transaction. Better normalization, confidence scoring, and date proximity logic." Receipts sync to QuickBooks if stored in Rho (not for Treasury). Accepted upload types: PDF, JPG, PNG |
| **Rho Slack App** | **Read-only.** Commands `/rho-accounts`, `/rho-transactions`, `/rho-help`, `/rho-feedback`, `/rho signin`, `/rho-signout`. Alerts: daily balance (default 9:00 AM ET), transaction notifications (default $1,000 threshold), card activity (default $1,000). Private channels and DMs only; removes itself from public channels. Available to **Account Owners and Admins today**. Beta agent chat answers questions with live data; statement download links work ~15 minutes. **No approval actions - you cannot approve a bill from Slack.** (Rho's own blog credits Mercury with "sign-off from Slack or the mobile app." **[Rho claim about Mercury]**) |
| **Plaid / aggregators** (`rhos-supported-cash-flow-apps`) | Wave and **Sage** are supported "through Rho's integration with Plaid" (search "Rho Business Banking"). Not supported: **Zelle, Payoneer, Abacus, Cash App**. PayPal supported via bank link; PayPal micro deposits "sometimes take 2-3 days." Changelog 08/03/2026: "Open Banking API – FDX v6.4 support." |
| **1Password** | `1password-integration-overview-setup` (not AP/AR relevant) |

---

## 10. Changelog: AP / AR / accounting items with dates

| Date | Item |
|---|---|
| 2026-02-26 | **Puzzle direct integration** ships: "your transactions, bills, and attachments will now sync automatically … Free for all Rho customers. Setup takes 30 seconds" |
| 2026-02-26 | Bookkeepers can set up Plaid connections by default |
| 2026-02-26 | Smarter Accounting dashboard (enriched transaction detail inline) |
| 2026-02-26 | **"Negative bill line items now sync. Credits and adjustments from QuickBooks pull through cleanly."** |
| 2026-03-25 | **Invoicing launches in Beta** - branded invoices, virtual account numbers, auto payment mapping |
| 2026-03-25 | "Bill Pay UX improvements. … You can now know whether you need to add vendor payment details or move straight to approval" |
| 2026-03-25 | Attach documents to printed checks |
| 2026-03-25 | Redesigned accounting mapping rules (collapsible sections) |
| 2026-03-25 | Mobile reimbursements with OCR |
| 2026-04-30 | Gmail Connector |
| 2026-04-30 | **Recurring invoices** live for all beta customers |
| 2026-04-30 | **Invoices auto-marked as paid** on matched incoming payment |
| 2026-04-30 | **QBO Bank Feed expanded** - Treasury and Savings accounts now sync; consistent card feed descriptions |
| 2026-04-30 | Receipt matching rebuilt with merchant identity verification |
| 2026-05-06 | Blog: "Introducing Rho Close: Intelligent Transaction Coding for Startups" (updated 2026-09-01) |
| 2026-05-27 | **Rho Close** announced in the changelog |
| 2026-05-27 | Per-account payment defaults for vendors |
| 2026-05-27 | Retry failed/canceled reimbursements, individually or in bulk |
| 2026-06-30 | **Invoicing: branded payment portal + recurring invoices** (weekly/monthly/quarterly/annual) |
| 2026-06-30 | Scheduled payment dates shown on the Approvals screen; "Needs My Approval" tile; users can cancel their own scheduled payments; warning for incomplete expenses on approval |
| 2026-08-03 | **Rho API** (read-only; "Write access and webhooks are next") |
| 2026-08-03 | **Downloadable invoice aging report** |
| 2026-08-03 | ACH trace IDs and wire IMAD/OMAD codes in the transaction drawer |
| 2026-08-03 | Show operating address instead of registered legal address on invoices |
| 2026-08-03 | Rho Debit Controls (ACH debit authorization) |
| 2026-08-31 | **Pay Rho Invoices by Card** (2.9% + 30¢) |
| 2026-08-31 | **Rho invoices sync to QuickBooks** as AR invoices |
| 2026-08-31 | **Map account attributes by your own Rho attributes** (custom attributes as a mapping-rule input) |

---

## 11. Contradictions inside Rho's own corpus

1. **Bill Pay payment methods.** `product/bill-pay` says checks and only checks, four times: "Once approved, pay by check"; "pays by check with no per-payment fee"; "it captures invoices automatically, routes them for approval, and **pays vendors by check**"; "Check payment methods next. Rho Bill Pay supports check payments." The hero stat is "$0 On domestic check payments," not "$0 on payments." The help center and the company's own blog say ACH, wires (domestic and international), checks, and single-use cards. The nav sub-label on every page says "Bill Pay - Hundreds of vendors, **zero fees**." The marketing page appears to have been narrowed to a check-only claim that understates the product.
2. **Vendor cards in Bill Pay.** `how-to-manage-vendors-in-rho`: "**Paying a bill through the Bill Pay workflow does not currently support Vendor Cards.** You'll be prompted to add an alternative payment method." Contradicted by an entire dedicated article, `paying-bills-with-vendor-cards-single-use`, and by the bulk-payments article, both of which describe selecting Single-Use Card as a Bill Pay payment method.
3. **Invoice accounting sync.** `product/invoicing` (IN-DEPTH GUIDE 04): "**Rho Invoicing does not yet sync with accounting software like QuickBooks or Xero**, and there is no mobile app." Directly contradicted by `syncing-invoices-to-your-accounting-software`, by the changelog of 2026-08-31, and by the API's `accounting_sync_status` field. `blog__best-invoicing-tools-for-startups` carries the same stale con ("No direct accounting-software sync yet" and "No card payments on invoices yet").
4. **Unpaid invoice sync.** `setting-up-recurring-syncs...`: "invoice payments will sync to your accounting system, but **syncing unpaid invoices is not yet supported**. This feature is currently in development." Contradicted by the invoice-sync article: Rho "creates the corresponding invoice in QuickBooks Online" when you send it, regardless of payment.
5. **Recurring invoices.** The `product/invoicing` comparison table lists Rho's "Recurring invoices" cell as "**Not shown**" and "Payment matching and reconciliation" as "**Not shown**", while the same page's guide sections describe both as working features, and the changelog shipped recurring invoices on 2026-04-30 and 2026-06-30.
6. **Rho Close ERP list.** Help center: QuickBooks, NetSuite, **Puzzle**, Sage Intacct. Product page: QuickBooks Online, NetSuite, Sage Intacct **+ Xero via bank feed**. Neither list matches the other.
7. **Rho Close auto-apply.** Product page: "Nothing syncs until you approve it. **Every time.**" Help center: "If you do sync an individual transaction without actively accepting or dismissing the suggestions, **those suggestions will be applied to the sync**."
8. **Xero: native vs bank feed.** `/integrations/xero` markets a "native Xero Integration" with subsidiary support; `how-to-set-up-rhos-xero-integration` describes a bank feed; `faq.txt` and `product/close` say bank feed; `product/expense-management` says both things in two adjacent FAQ answers.
9. **Domestic wire recall fee.** `pricing.txt` item 07: "Domestic wire recall fee **$0**." `fees-for-recalls-failed-wires`: "a fee of around **$20 – $45** will be deducted from your Rho account for any domestic wire payments that fail and are returned."
10. **Bill Pay settings navigation.** Inbox address editing is "Settings tab > Configuration > BillPay Setup" in one article and "Bill Pay > Settings" in another. Approvals are "Settings → Security → Payment Approvals" in one and "Settings → Payment Security → Payment Approvals" in another. Bill-sync toggle has three distinct labels across three articles.
11. **Expense approval example thresholds** differ between two articles that present the same worked example: "over $500" vs "over $1,000" for the second tier.
12. **Bill status naming.** The status article lists 8 statuses with no "Processed"; the error catalog references a "Processed state."
13. **BILL's pricing, per Rho.** `/versus/bill`: "**$45–$89** per user per month for AP/AR." `/product/bill-pay`: "**$49 to $89** per user per month; Enterprise custom." `blog__best-ap-automation-software`: "No, from **$49**/user/mo." **[Rho claims about BILL]**
14. **Invoicing T&C dates.** Header "August 25, 2026"; body "Last amended August 26, 2026."
15. **Puzzle availability.** `/integrations/puzzle`: "Early access is available now through the waitlist. Full availability rolls out in **April 2026**." Changelog: Puzzle shipped **February 26, 2026**. The page still shows a waitlist CTA as of the crawl.
16. **SAP Concur page** says "Connect **Emburse** with Rho Corporate Cards." **Sage Intacct page** uses a testimonial that says "The **NetSuite** integration saves us so much time."
17. **Post-sync editability.** `customers/dr-squatch` celebrates "the ability to make changes in Rho **post-NetSuite sync**." The bill-sync article says key bill fields are locked after the first sync. (Reconcilable - the customer quote is about card transactions - but the marketing claim reads broader than the documented behavior.)
18. **site-llms link rot.** `site-llms-full.txt` points to `https://www.rho.co/help-center/**accounts-payable**/bill-pay-at-rho-overview`, but the live path is `/help-center/**bill-pay**/...`; it also links `https://www.rho.co/integrations/navan` and `https://www.rho.co/product/partner-portal`, neither of which appears in the 1042-URL sitemap.

---

## 12. Conspicuously NOT stated anywhere in the corpus

**AP**
- **Purchase orders / procurement**: explicitly excluded. No PO object, no requisition, no receiving.
- **Three-way match**: stated as "not yet available."
- **Two-way match** (invoice vs PO) is not mentioned either; only duplicate detection.
- **Approval routing by vendor, GL account, department, entity, or category** for bills. Amount only.
- **Conditional / parallel / delegated approval paths**, out-of-office delegation, or approval SLAs/escalation.
- **Early-payment discount capture or dynamic discounting.** "Early-payment discounts" is mentioned once as a reason to schedule a payment, but no discount-term field, calculation or capture exists.
- **Payment terms enforcement**: OCR extracts "Payment Terms" but nothing in the corpus uses them (no auto-scheduling from terms).
- **Vendor self-service portal** beyond the one-time profile-completion invite and the 60-day W-9 portal. No invoice-status portal for vendors.
- **Vendor bank-detail change verification / micro-deposit validation of vendor accounts / positive pay.**
- **Supplier fraud controls** on vendor payment detail changes (Rho documents ACH *debit* controls for inbound pulls, not outbound vendor detail-change controls).
- **International Bill Pay in non-USD**; no FX forward, no multi-currency bill.
- **Credit memos / vendor credits** in Bill Pay (QuickBooks negative bill line items pull through, but there is no Rho-side credit object).
- **Partial payments against a single bill.**
- **Accruals, prepaid amortization, or recurring bills/accruals** generated in Rho.
- **Bill Pay API.** The public API has no AP, vendor, or payment-creation endpoints.
- **1099 filing** (export only since tax year 2023). No W-8BEN/W-8BEN-E for foreign vendors despite supporting international wires. No TIN matching.

**AR**
- **Automated dunning schedules / reminder cadences / late fees / customer statements.** The `reminder_sent` activity exists but no configuration surface is documented.
- **Credit memos, partial payments applied to an invoice, write-offs, or customer credit limits.**
- **Multi-currency invoicing** (card is USD-only; nothing states non-USD invoices can be created at all, though the T&C references "non-USD invoices").
- **Sales tax calculation** beyond a manual per-line or invoice-level rate. No tax engine, no nexus, no Avalara-style integration.
- **AR aging by customer beyond the single exported "aging report"** (no in-product AR aging dashboard is described).
- **Customer portal** beyond the per-invoice payment link.
- **ACH debit / auto-pay pull from the customer** (Rho invoices are pay-by-push or card only; no "authorize us to debit you"). Contrast: Rho's own comparison notes Stripe's "ACH Direct Debit" and Mercury's "ACH debit collection."
- **AR sync to anything other than QuickBooks Online.**
- **Invoicing on mobile** ("there is no mobile app" per the product page).
- **Invoice approval workflow** (AR invoices have no approval step documented).

**Accounting / close**
- **A close checklist, task list, period lock, close calendar, or sign-off** - despite "Rho Close" branding and "Your path to a seamless month-end close."
- **Journal entry creation, accruals, amortization schedules, or adjusting entries.**
- **Flux/variance analysis, trial balance, or financial statements.**
- **Multi-entity consolidated close** (entity toggling exists for mapping rules; consolidation does not).
- **Audit trail export** for approvals (approvals are described as leaving an audit trail in blog copy, but no audit-log feature is documented).
- **Bidirectional attribute sync** (Rho pulls ERP attributes; it does not write dimensions back except vendors via Merchant-to-Vendor).
- **Campfire** has zero help-center documentation despite a marketing page and hub placement.
- **Microsoft Dynamics 365 Business Central** has no marketing page, no help article, and no sitemap URL, yet appears in three sync error strings and in Rho's own machine-readable integration list.
- **Sync failure alerting** (errors are visible in the dashboard; no notification is documented).
- **Rate limits, SLAs, or throughput numbers** for any sync.

---

## 13. Rho's competitive claims in this surface (all [Rho claim])

### AP comparison, `product/bill-pay`, competitive data collected **2026-09-08**

| | Rho | BILL | Ramp | Relay |
|---|---|---|---|---|
| Software cost | Included with Rho Banking, no extra subscription | $49 to $89 per user per month; Enterprise custom | Free plan available; Ramp Plus $15 per user per month | Plans from $0 to $120 per month |
| Domestic per-payment fees | $0 on checks | ACH $0.59; mailed check $1.99 | "No software or transaction fees" on its free plan, per Ramp | "Additional transaction fees apply," per Relay's pricing page |
| Automated invoice capture | Dedicated Rho inbox, no logins required | Yes | Yes | Yes |
| Approval workflows | Rho routes bills to the right approvers and flags potential duplicates | Automated approvals on all tiers; custom approval policies on higher tiers | Approval workflows | Multi-step bill approval rules |
| Accounting sync | Included with Rho Bill Pay | Tiered: CSV import/export on entry tier; two-way QuickBooks and Xero sync on Team and up | Syncs with 10 ERPs including NetSuite, Sage Intacct, and QuickBooks | QuickBooks Online and Xero |

Rho's stated market baseline: "Dedicated AP software commonly charges **$15 to $89 per user per month**."

### AR comparison, `product/invoicing`, competitive data collected **2026-09-08**

| | Rho | Stripe | Mercury | QuickBooks |
|---|---|---|---|---|
| Invoicing cost | Included, no extra cost | 0.4% per paid invoice (Starter); 0.5% (Plus) | Unlimited invoices free on every tier; recurring requires Plus ($29.90/mo, billed annually) | Free plan capped at 2 invoices/month; unlimited from $20/mo (Lite) |
| ACH / bank transfer fee | $0 on domestic ACH, wires, and checks | 0.8% ACH Direct Debit, $5.00 cap (plus per-invoice fee) | $1/transaction on Plus, $0 on Pro, unavailable on free tier | 1% per ACH bank payment |
| Recurring invoices | **"Not shown"** | Via Stripe Billing: 0.7% of billing volume | Plus and Pro only (from $29.90/mo billed annually) | From Simple Start ($38/mo) |
| Payment matching and reconciliation | **"Not shown"** | Automatic reconciliation; Smart Retries and automated reminders | Auto-imports invoice payments to QuickBooks, NetSuite, or Xero | Books update automatically with every payment taken through QuickBooks |

Rho's own FAQ concedes card acceptance "typically costs **around 3%** in processing fees" - consistent with its own 2.9% + $0.30.

### Blog head-to-head, `blog__best-ap-automation-software` (prices "verified August 2026")

| Platform | Free tier | Payment types | Approvals | Accounting |
|---|---|---|---|---|
| **Rho** | Yes, included with every Rho account | ACH with zero fees, wires including international, single-use vendor cards | Amount-based approval guardrails, included | Auto-sync with QuickBooks and ERP systems |
| BILL | No, from $49/user/mo | ACH $0.59, checks from $1.99, intl USD wire $19.99 | Multi-user approval workflows | QuickBooks, Xero, others |
| Ramp | Yes, $0 plan includes bill pay | ACH, card, check, wire | Tied to spend controls | QuickBooks, NetSuite, others |
| Brex | Yes, $0 Essentials includes bill pay | Pay bills from the Brex business account | Yes, with automatic invoice entry | QuickBooks, NetSuite, others |
| Tipalti | No, from $99/mo plus transaction pricing | Global payment methods across many currencies | Enterprise-grade controls | NetSuite and major ERPs |
| Melio | Yes, 5 free ACH transfers/mo | ACH $0.50 after free allotment, checks $1.50, cards 2.9% | Varies by plan | QuickBooks, Xero |
| Mercury | Yes, unlimited free bill pay | ACH, domestic and international wire, check | Multi-layered approval rules, free | QuickBooks, Xero; NetSuite on paid plans |
| Relay | Yes, bill management on $0 Starter | ACH and wires, fees vary by plan; 10 free same-day ACH/mo on Scale | Multi-step bill approval rules on all plans | QuickBooks, Xero |

Rho-acknowledged competitor strengths in this surface: Mercury's free bill pay includes "AI-assisted data extraction, duplicate invoice detection, and multi-layered approval rules with **sign-off from Slack or the mobile app**," plus "**W-9 collection plus 1099 filing assistance** … built in." Relay includes "multi-step bill approval rules on all plans" including the $0 tier. Ramp includes procurement as a paid add-on ("procurement costs extra even on Plus", as of 08/02/2026). BILL's strength per `/versus` hub copy: "a mature standalone AP/AR product with a large accountant network."

### Puzzle page competitive claims [Rho claim]
- "**Mercury's integration is read-only.**"
- "**Brex covers cards and reimbursements but doesn't manage the full bill lifecycle.**"
- "**Ramp is a spend platform, not a bank**, so you still need a separate banking integration for complete books."
- Against Plaid: "Plaid **strips out transaction metadata, limits which transaction types sync, and disables Rho's accounting automations**."

### Customer-outcome numbers cited in this surface
- **Spark Advisors**: "reduced AP processing time from one week to minutes"; "**90% reduction in invoice approval time**"; "bulk approval process for invoices that once took nearly a week now takes just **10 minutes**"; "**2+ FTEs** saved"; 1-week onboarding.
- **Native Strategies** (via the QuickBooks integration page): reconciliation went from "hours-long" to "a **15-minute** exercise."
- **Dr. Squatch**: "**20+ hours** saved monthly, automating expense and accounting reconciliation," attributed to the NetSuite integration.
- **Innomark Communications**: "**10 hours**" of operational time and "**over $1000** of fees they would have paid on SAP Concur every month."
- **Polimorphic** (site-llms): "saved **40+ hours/month**."
- **Willet + Cumro Innovations**: "about **8 hours a week**" saved for the narrator, plus CFO and EA hours; **10 entities**.

---

## 14. Quick-reference: every hard number in this surface

| Number | What it governs |
|---|---|
| 2.9% + $0.30 | Invoice card processing fee (Stripe), paid by the business |
| $10,000/day | Invoice card payment limit across all invoices |
| $0.70/mile | Pre-populated IRS mileage reimbursement rate |
| 50 MB | Max file size per Bill Pay inbox attachment |
| 15 MB | Max W-9 PDF upload; max check-attachment PDF |
| 10 MB / 2 MB / 5 items | Free invoice generator: max file, max logo, max line items |
| 100 line items | Rho Invoicing max line items (blog-sourced) |
| 6 pages | Max pages on a PDF attached to a mailed check |
| 90 calendar days | Uncashed checks auto-void |
| 60 days | W-9 vendor portal lifetime |
| 14 days | Single-use vendor card usage window (editable) |
| 72 hours | Single-use card secure-details link expiry |
| 7 days | Vendor notification attachment link expiry |
| 30 days | Max age of an ERP bill to auto-pull into Rho |
| 8 hours | Flagged ACH debit hold window before the default rule applies |
| 3 transactions | Merchant spend threshold before Merchant-to-Vendor creates a vendor |
| 6 hours | Merchant-to-Vendor run interval |
| 24 hours | ERP bill pull interval; Xero bank feed; HRIS sync minimum interval |
| ~12:00 AM EST | ERP bill pull time |
| 3:00 AM ET / 8:00 AM UTC | Recurring accounting sync time |
| 3:00 AM EST | Xero daily bank feed time |
| ~4:00 AM ET | Scheduled payment release; approval deadline |
| 5:00 PM EST | Bill Pay daily digest; also the T&E card feed cutoff (Mon-Sat) |
| 10:00 AM EST Friday | Bill Pay weekly digest |
| 2:00 PM ET / $1mm | Outgoing ACH same-day cutoff and amount ceiling |
| 4:45 PM ET | Outgoing domestic wire same-day cutoff |
| 3:00 PM ET | Reimbursement disbursement same-day cutoff |
| 9:00 AM ET | Slack daily balance alert default |
| $1,000 | Slack transaction and card alert default thresholds |
| Up to 8 business days | Printed check USPS delivery |
| 1-2 business days | Bulk vendor CSV upload turnaround by Rho Client Service |
| 3-5 business days | Mastercard Smart Data card feed setup |
| Up to 2 weeks | First card payment payout while Stripe completes initial review |
| 5 / 7 | Max legacy Custom Attributes / max active Fields |
| 6 | Mapping-rule hierarchy levels (Label, Sender, Vendor, Merchant, Card, Department) |
| 12 | QuickBooks dashboard view types |
| 32 | Distinct sync error strings documented |
| 436739 / v1.01 | Rho NetSuite SuiteBundle ID and current bundle version |
| 50+ | HRIS providers supported via Merge |
