
## 1. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1439: "| Plans | $0 / $35 / $299 per month (Pro, as of 2026-09-11; the page defaults to annual billing) | $0, no tiers |"

**Problem:** $35 and $299 come from two different Mercury price schedules and never coexist. I fetched mercury.com/pricing live: its schema.org Product JSON-LD carries price "0.00", "35.00" and "350.00" (the month-to-month list), and the page's default toggle renders the 15%-off annual equivalents $0 / $29.90 / $299. So Mercury Pro month-to-month is $350, not $299, and the annual Plus rate is $29.90, not $35. The row understates Mercury's month-to-month top tier by $51/month (17%) and contradicts the dossier's own line 1610 ("published by Rho as both $35/$350 and $29.90/$299 on different pages"). Lines 1432, 1621 and 2090 repeat "$299/month Pro tier" without the annual-billing condition. This is the flagship competitor-pricing row in a document whose central argument is "Rho is free and the competitors charge."

**Fix:** Replace the Plans cell with: "$0 / $35 / $350 month-to-month, or $0 / $29.90 / $299 with annual billing (the pricing page defaults to the annual toggle), as of 2026-09-11". At lines 1432, 1621 and 2090 change "the $299/month Pro tier" to "the $350/month Pro tier ($299 on annual billing)".

## 2. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1482: "| **Tipalti** | From $99/month, "unlimited users" | A floor, not a price. Add $0.20 to $36 per payment, 1.9% to 3.5% FX markup, $500 to $600/month per extra legal entity, $4K to $5K setup. Transaction and FX are 50% to 70% of what customers actually pay | No |"

**Problem:** Only "$99/month" is Tipalti's own published figure. The research file this row is built from (findings/mk-spend-legacy.md lines 363-376) heads the entire block "[Third-party] estimated real cost structure" and traces the per-payment range, the FX markup, the per-entity fee and the 50-70% share to a single page, https://multientityaccounting.com/tipalti-pricing-multi-entity/, which I fetched on 2026-09-11: the domain resolves (46.202.182.181) but the server returns nothing over HTTPS (curl exit code 000). The same file records that Tipalti's own pricing page "explicitly declines to give amounts." Four unverifiable SEO-aggregator estimates are printed under a column header reading "What the price really is" - the exact citation-free-layer failure mode the dossier itself warns about at line 283.

**Fix:** Replace the second cell with: "A floor, not a price: Tipalti's own page declines to state transaction, FX, module and implementation amounts. Third-party cost-benchmark sites, not Tipalti and not independently confirmable (the primary source for these ranges was unreachable on 2026-09-11), put the real cost at $0.20 to $36 per payment, a 1.9% to 3.5% FX markup, $500 to $600/month per additional legal entity and $4K to $5K setup, with transaction and FX said to be 50% to 70% of the annual bill." Alternatively delete the four unsourced figures and keep only "$99/month is a floor; Tipalti declines to publish transaction, FX and implementation pricing."

## 3. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1615: "Rho Treasury charges an annual advisory fee tiered from 0.60% under $2M down to 0.15% above $20M, assessed on checking plus Treasury balances combined. At the 0.60% tier a $2M balance pays roughly $12,000 a year, more than a 25-seat Ramp Plus subscription ($4,500) or a 25-seat Brex Premium subscription ($3,600)."

**Problem:** This is the counterweight attached to Rho's single strongest and best-evidenced differentiator (no software fees), and it rests on the document contradicting itself. Sections 3.3 (line 389) and 4.4 (line 859) both read the same help-center sentence the opposite way: 3.3 says the fee is "tiered on assets under management... so your checking balance helps you into a cheaper tier" and 4.4 says "moving operating cash into Rho Checking, which pays nothing, lowers the percentage fee charged on the invested cash." Under the document's own reading, checking sets the tier and the fee is charged on the invested portfolio (the help center says the fee "is deducted from your portfolio cash balance"). Section 8.1 flips to the punitive reading and then computes $12,000 on a "$2M balance" that a reader will take to include pure checking. A Rho customer who never opens Treasury pays $0. The comparison is also not like-for-like: an optional 0.60% advisory fee buys discretionary investment management, while Ramp Plus and Brex Premium seat fees are mandatory software charges. (Source: pages/help/help-center__treasury__about-rho-treasury.txt line 115.)

**Fix:** Replace with: "The counterweight is that 'free' describes the invoice, not the relationship. Rho Treasury charges an annual advisory fee of 0.60% under $2M sliding to 0.15% above $20M, deducted from the Treasury portfolio; the checking balance counts toward the AUM figure that sets the tier, which works in the customer's favour. A company that invests $2M through Treasury pays roughly $12,000 a year for discretionary management it would otherwise buy elsewhere; a company that holds $2M in checking and never opens Treasury pays nothing. Foreign-currency transfers cost 1%. And the highest cashback rate..."

## 4. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 78: "Every term below is used later in this document without re-explanation."

**Problem:** This sentence is false about its own document and it is the promise the whole layman on-ramp rests on. At least seven glossary terms are re-explained later, several of them three times: FDIC insurance (L88, re-explained L322 "FDIC insurance, for readers new to US banking, is a federal government guarantee..." and again L1776), SIPC (L88, re-explained L401 and L1778), sweep network (L89, re-explained L228 and L350), EIN (L332, re-explained L1037 and L1647), MCP (L103, re-explained L1233, L1363 and L1674), accounts payable (L92, re-explained L1635), charge card (L84, re-explained L797). Meanwhile the terms absent from the glossary are never explained anywhere. The document spends its definitional budget on terms it already defined and none on the ones it did not.

**Fix:** Replace with: "Every term below is used throughout this document. A few of the most consequential (FDIC, SIPC, the savings sweep, MCP) are restated briefly at the point they carry the most weight; the rest are not repeated." Then, separately, delete the duplicate definitions at L228, L322, L401, L1363 and L1674, and spend that space on the terms listed in the findings below.

## 5. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 137: "$0 monthly, $0 minimum, $0 domestic ACH, wires and checks" (first use of ACH); line 109: "funded by wire" (first use of wire). Both defined only at line 419.

**Problem:** ACH (41 uses) and wire (66 uses) are the two most-used payment terms in the document and the only two payment rails Rho charges nothing for, which is the central price claim. Both appear inside Section 1's own "What Rho bundles instead" table, and neither has a glossary row. The reader must reach section 3.4, 282 lines and roughly 9,000 words later, for the "Vocabulary" paragraph at line 419. Everything between (the $0 fee claim at 137, the fee summary at 244, the checking fees at 340) is unreadable to a newcomer.

**Fix:** Add a glossary row to Section 1 immediately after "Business checking account": | **ACH and wire** | The two ways US businesses move money between banks. **ACH** (Automated Clearing House) is a cheap batch network that settles in a day or more and can be reversed; it moves payroll and most recurring vendor payments. A **wire** is individually processed, arrives the same day, and is effectively irreversible once sent. | Rho charges $0 for both domestically. A payroll run leaves by ACH; a $2M acquisition payment leaves by wire. | Then shorten the line 419 paragraph to the push/pull distinction only.

## 6. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 109: "usually a brokerage money market fund at Schwab or Fidelity"; also lines 127, 139, 378, 409, 1407, 1629

**Problem:** "Money market fund" is never defined anywhere in the 54,000 words, despite appearing three separate times inside Section 1 and being the exact incumbent product Rho Treasury is positioned against. It is the load-bearing noun of the entire Treasury argument in sections 3.3, 4.4 and 7.3, and the reader is expected to already know what it is, how it differs from a bank deposit, and why it is not FDIC insured. Section 1's "Treasury / idle cash" row at line 90 gestures at "conservative bond funds" but never names or explains the instrument.

**Fix:** Add a glossary row after "Treasury / idle cash": | **Money market fund** | A mutual fund that holds only very short-term, very safe debt (Treasury bills, bank paper) and is designed so each share is always worth exactly $1.00. It pays close to the short-term government rate, is bought through a brokerage rather than a bank, and is protected by SIPC rather than FDIC, so it can in principle lose value even though it almost never does. | A company with $8M idle typically parks it in a money market fund at Schwab or Fidelity. Rho Treasury offers one (IJTXX) alongside T-Bills and two bond funds. |

## 7. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 147: "| Wise / FX payments | International payments via Wise US Inc. | 1% on foreign-currency transfers, optional $15 SWIFT fee, $30 international wire recall |"

**Problem:** Two undefined terms in Section 1's own table, both load-bearing. "FX" is used 22 times and is never expanded at first use; the words "foreign exchange" appear only at line 865, as a section heading 718 lines later, and are never linked back to the abbreviation. "SWIFT" is used 10 times and is never expanded or explained anywhere in the document. A reader who does not already know these two cannot parse Rho's single named non-zero fee, which the document calls "the headline fee."

**Fix:** In the line 147 table cell write "1% on foreign-currency (FX, short for foreign exchange) transfers, optional $15 SWIFT fee" and add a glossary row: | **FX and SWIFT** | **FX** is foreign exchange, the business of converting one currency into another; the fee is the margin taken on the conversion. **SWIFT** is the international messaging network banks use to instruct each other to move money across borders; a SWIFT payment can pick up fees from intermediary banks along the way. | Rho charges 1% to convert dollars into another currency, and an optional flat $15 if you want to absorb the SWIFT intermediaries' charges instead of the recipient. |

## 8. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 145: "| Venture debt or a bank line | Rho Capital | $0 origination, $0 prepayment; the actual rate is published nowhere |"

**Problem:** "Venture debt" first appears in Section 1's own bundle table and is never defined anywhere in the document, despite 6 uses including the Rho Capital positioning at line 619 ("not a term loan or a venture debt facility") and the SVB comparison at line 1509, where it is named as a capability Rho structurally cannot offer. "Origination" (line 145) and "prepayment" penalty are also undefined at first use.

**Fix:** Add a glossary row: | **Venture debt** | A loan made to a startup that is not yet profitable, sized against the equity it has just raised rather than against its earnings, usually by a specialist bank or fund. It is how a company borrows without selling more shares. | SVB sizes venture debt at 20% to 40% of a startup's last equity round. Rho does not offer it; Rho Capital is a smaller revolving line against cash flow. | And in the same table cell write "$0 origination fee (the up-front charge for setting up a loan), $0 prepayment penalty (the charge for paying it back early)".

## 9. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 164: "it integrates directly with Webster rather than through a banking-as-a-service middleware layer"; line 1531: "| Fintech program, BaaS middleware, partner bank, sweep network |"

**Problem:** This is the single most important risk concept in the document and it is never explained. Section 1 uses "banking-as-a-service middleware layer" at line 164 in the passage that tells the reader what happens if Rho fails, with no definition. The abbreviation "BaaS" then appears cold at line 1531 in a counterparty-hops table, 1,367 lines before the only expansion of it (line 1835, inside a quotation from Rho's own blog). The Synapse case study at 1533 and diligence question 15 at line 1975 both depend on the reader understanding what a middleware layer is and why an extra hop matters.

**Fix:** Add a glossary row after "Sponsor bank": | **Banking-as-a-service (BaaS) middleware** | A fourth company that sits between the fintech app and the sponsor bank, running the ledger and the plumbing for many fintechs at once. Every extra layer is another set of records that has to agree with the bank's, and another company that can fail. | Relay reaches its bank through middleware called Unit; Rho says it connects to Webster directly, which if true removes the layer that failed in the Synapse collapse. | Then at line 164 write "...rather than through a banking-as-a-service middleware layer (see the glossary: a fourth company running the ledger in between)."

## 10. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 115: "producing a P&L that the board sees. Each tool exports a CSV. The CSVs do not agree."

**Problem:** "P&L" is used in Section 1's core problem narrative and is never expanded anywhere in the document (1 use, zero expansions). It is the payoff noun of the month-end close paragraph, the thing the whole close problem exists to produce. "CSV" (4 uses) is likewise never expanded, and it carries real weight later at line 641 where Rho Close eligibility turns on "If you're currently exporting CSVs."

**Fix:** Rewrite line 115 as: "...and producing a P&L (profit and loss statement, the report showing what the company earned and spent in the month) that the board sees. Each tool exports a CSV (a plain spreadsheet file). The CSVs do not agree."

## 11. [CRITICAL] RHO_PRODUCT_DOSSIER.md
**Locator:** line 2141: "Re-runnable in about two hours, most of it unattended. All scripts referenced live in the project scratchpad alongside this document."

**Problem:** False as delivered, and it disables the entire refresh procedure. /Users/manojmaheshwarjagadeesan/Desktop/project/ contains exactly two files, the two .md documents. Every asset that section 10.4 instructs the reader to run or diff against exists only under /private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/ (56 MB), a session-scoped temp tree that is purged. I confirmed each named asset exists there and nowhere else: fetch_all.sh, urls-core.txt, urls-help.txt, urls-blog-comp.txt, pages/ (556 files), sandbox/census.py, sandbox/probe.sh. Step 2 ("Run fetch_all.sh over urls-core.txt ... then diff -rq it against pages/") and step 7 ("Re-run the sandbox census. sandbox/census.py and sandbox/probe.sh") are unexecutable on the delivered package. The reader explicitly said they would maintain these documents, so this is the one defect that defeats the stated purpose of the deliverable.

**Fix:** Copy the research tree next to the documents and reference it by relative path. Run: cp -R "/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho" "/Users/manojmaheshwarjagadeesan/Desktop/project/rho-research"  then replace line 2141 with: "Re-runnable in about two hours, most of it unattended. Everything this procedure references ships beside this file in `./rho-research/`: the crawler (`rho-research/fetch_all.sh`), the URL lists (`rho-research/urls-core.txt`, `urls-help.txt`, `urls-blog-comp.txt`), the 556-page corpus (`rho-research/pages/`), the sandbox probes (`rho-research/sandbox/census.py`, `rho-research/sandbox/probe.sh`), the 29 findings files (`rho-research/findings/`), and the verified claim register (`rho-research/VERIFIED.md`). All paths below are relative to this document." Then prefix the filenames in steps 2 and 7 with `rho-research/`.

## 12. [CRITICAL] RHO_API_REFERENCE.md
**Locator:** lines 73-74: "This is a snapshot of a five-week-old API that Rho has said is actively moving. Section 8 lists what will change first. To refresh, re-run the probes in section 3 and diff against the tables here."

**Problem:** The pointer is false and the content it promises does not exist. Section 8 is "Building on it" (8.1 constraints, 8.2 incremental sync, 8.3 idempotency, 8.4 handling money, 8.5 storing IDs, 8.6 retry, 8.7 observability, 8.8 what you cannot build, 8.9 reference implementation) and lists nothing about what will change first. Grepping the whole 80,000-word file for "change first", "will change" and "shortest shelf" returns only this sentence itself. So the document the reader is most likely to need to refresh, by its own account a five-week-old moving target, has three sentences of maintenance guidance, one of which points nowhere, while the companion dossier carries a full 10.2 "Facts with the shortest shelf life" plus a ten-step 10.4 refresh procedure. The asymmetry is backwards.

**Fix:** Replace the "Keeping it current" block with a real one: (a) change line 73-74 to "Section 6.4 covers the versioning contract; the watch list below is what actually moves."; (b) add a dated watch table immediately under it with the highest-signal, zero-cost checks already proven elsewhere in the document: `curl https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` and diff `scopes_supported` against the five `:read` scopes (a non-`:read` scope is the first public sign of write access); re-fetch `https://docs.rho.co/api/v1/openapi.md` and diff the operation count against 14; re-test `POST https://auth.rho.co/oauth2/register` for dynamic client registration; `curl -sS -o /dev/null -w "%{http_code}" https://rhoapi-sandbox.rho.co/mcp/v1` for a sandbox MCP endpoint appearing; re-run the section 3.3 census for new enum values and record counts; re-check for `Deprecation`/`Sunset` headers and for a webhooks/events route. Give each a cadence (monthly for the metadata and OpenAPI diff, quarterly for the census).

## 13. [CRITICAL] RHO_API_REFERENCE.md
**Locator:** Line 6503, table row: "No `updated_after` filter anywhere | Transactions expose `initiated_after/before` and `posted_after/before` only. The docs guide concedes this: \"There is no incremental-sync primitive.\""

**Problem:** Fabricated quotation. The string "There is no incremental-sync primitive" appears nowhere in Rho's published material. A case-insensitive search for "incremental-sync", "incremental sync" and "primitive" across all 13 guides (scratchpad/rho/docs/), all 14 operation references (scratchpad/rho/api/), all 556 captured pages (scratchpad/rho/pages/) and both llms.txt summaries returns zero hits in any Rho-authored text. The only occurrences of the sentence anywhere on disk are in the document being audited and in its own draft (scratchpad/rho/draft/). It is presented as Rho conceding a limitation in its own documentation, which is the most damaging class of misquote: an invented admission. The neighbouring row in the same table correctly says of webhooks "No such concept appears anywhere in the docs corpus", which is the honest formulation.

**Fix:** Delete the quotation and the concession framing. Replace the Evidence cell with: "Transactions expose `initiated_after/before` and `posted_after/before` only. No guide offers a change-based filter on any resource, and nothing in the docs acknowledges the gap."

## 14. [CRITICAL] RHO_API_REFERENCE.md
**Locator:** Line 2737: "`docs/v1/transactions` hedges the opposite way (\"not coupled to status\"), so the two Rho pages also disagree with each other." Repeated at lines 3349-3350: "The Transactions guide actually hedges correctly (\"it is not coupled to `status` … read the field as nullable whatever the status\"), so the guide and the reference page disagree with each other"

**Problem:** Manufactured contradiction, built by stripping the clause that reverses the quoted fragment's meaning. `docs/docs_v1_transactions.md` line 23 states "When the event cleared the ledger. Null while the status is pending" - word for word the same rule as `api/transactions_listtransactions.md` line 80 ("Null while status is pending"). Line 79 of the same guide then reads: "`posted_at` is nullable, and the contract describes it as null while the status is pending. Beyond that it is not coupled to `status`". The document quotes only "it is not coupled to status", dropping the leading "Beyond that" and the preceding sentence in which the guide affirms the pending rule. The guide and the reference page agree; the guide is elaborating on itself about statuses other than pending. This defect anchors what the document itself calls "the most consequential [divergence] in the core API" (line 3343), so it will be read closely.

**Fix:** In both places, delete the guide-versus-reference clause. At line 2737 end the divergence at "...the documented rule is contradicted in both directions." At lines 3349-3350 replace the final clause with: "The Transactions guide states the same pending rule (`docs/v1/transactions`: \"Null while the status is pending\") and then adds that, beyond pending, `posted_at` is \"not coupled to `status`\". Both Rho pages therefore agree with each other and both disagree with the data."

## 15. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1259: "| Page sizes | 100 max for accounts, transactions and statements; 20 default for cards and invoicing |"

**Problem:** This row reproduces the two halves of Rho's own per-endpoint doc wording as if they described the API's actual behaviour, and it contradicts the companion reference and the live API. RHO_API_REFERENCE.md section 6.1.2 (lines 5046-5075) prints exactly this doc split and then states: "Observed, the behavior is uniform across all six endpoints. The bound is inclusive [1, 100] everywhere, and the default is 20." API reference section 8.8 repeats "Documented and enforced range is [1, 100] on all six endpoints", and line 3965 records the /accounts defaults as "page_size=20". I re-verified live against the sandbox during this audit: page_size=101 returns 400 {"type":"1317","title":"page_size must be between 1 and 100"} on all six endpoints including /cards, /invoicing/customers and /invoicing/invoices, and /transactions and /statements both return 20 rows with page_size omitted. So the dossier is wrong in both directions: cards and invoicing do accept 100, and accounts, transactions and statements do default to 20. A reader building against the dossier alone will page cards and invoicing five times slower than necessary and will assume list calls return everything.

**Fix:** Replace the row with: "| Page sizes | Default 20 and maximum 100 on all six list endpoints, observed. Rho's own reference pages state only the max for accounts, transactions and statements and only the default for cards and invoicing |"

## 16. [MAJOR] RHO_API_REFERENCE.md
**Locator:** Lines 2864-2870, section 4.1 "The seven operations at a glance", Declared statuses column, e.g. "| ListAccounts | `GET /accounts` | `accounts:read` | 200, 400, 401, 403, 429, 500, 503 |"

**Problem:** Section 4.1 lists 429 as a declared status on all seven Accounts, Transactions and Cards operations. Three other places say the opposite. Section 3.4.2 (line 2109) states flatly: "no OpenAPI operation page documents a `429` response. All 14 operations list `200, 400, 401, 403, 500, 503`". Section 5.7 (lines 4905-4915) prints the parallel table for the other seven operations with no 429 and adds "Divergence: none of the seven declares `429`". RHO_PRODUCT_DOSSIER.md line 1261 says "none of the 14 operation reference pages documents a `429` response at all; they document 200, 400, 401, 403, 500 and 503". I checked all 14 captured operation exports in scratchpad/rho/api/*.md: not one declares 429. The 4.1 divergence note at line 2882 tries to rescue this with "the `429` row above is from the HTML reference only", but that is precisely what section 3.4.2 denies, and the two endpoint-reference sections still present the same column under the same heading with different contents. A reader comparing sections 4.1 and 5.7 concludes that half the surface declares 429 and half does not.

**Fix:** Remove 429 from all seven rows of the 4.1 Declared statuses column so it matches 5.7 and 3.4.2, and rewrite the note at line 2882 as: "Divergence: none of the fourteen `.md` operation exports declares `429`, although the rate-limits page asserts the API returns one. Add the case by hand to any generated client."

## 17. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 297: "Sections 8 and 9 cover the API and the agent surface." (plus nine more, listed below)

**Problem:** Ten internal cross-references point at the wrong section. The document has 10 sections as listed in its own Contents at lines 55-66. Confirmed wrong: line 85 "Section 5 examines what its Terms of Service actually reserve" (the card ToS reservations are in 3.5 and 9.4; section 5 is "Who Rho is for"); line 91 "Section 4 shows why the reachable number ... is 4.18%" (the 4.18% derivation is 3.3 at lines 403-409, and 4.4 at line 863 explicitly defers to it: "That is treated fully in the products section"); line 152 "Section 6 works through all of them" about fees (fees are 4.9; section 6 is the API); line 168 "Section 5 reads the contract properly" (the contract is 9.4); line 228 "Section 5 covers this in detail, including the six-withdrawals-per-month cap and the Exhibit A insurance waiver" (that is 9.2, and 3.2 at line 360); line 244 "(Section 7 covers the fees that sit outside that summary.)" (fees are 4.9; section 7 is the competitive landscape); line 287 "Section 3 takes up the scale claims" (the $4B+ deposits and $4B moving monthly claims are taken up at 10.1 line 2038 and 5.1 line 1122, not in section 3); line 297 "Sections 8 and 9 cover the API and the agent surface" (that is section 6); line 1177 "Section 7 covers the API surface in detail" (that is section 6); line 1181 "Sections 8 and 9 test how the same competitors hold up" (that is sections 7 and 8). The three API pointers are the most damaging: a reader sent to sections 7, 8 and 9 for the API lands in the competitive landscape, the differentiation chapter and the risk chapter.

**Fix:** Line 85: "Section 5" to "Section 9". Line 91: "Section 4" to "Section 3". Line 152: "Section 6" to "Section 4". Line 168: "Section 5" to "Section 9". Line 228: "Section 5" to "Section 9". Line 244: "Section 7" to "Section 4". Line 287: "Section 3" to "Section 10". Line 297: "Sections 8 and 9" to "Section 6". Line 1177: "Section 7" to "Section 6". Line 1181: "Sections 8 and 9" to "Sections 7 and 8".

## 18. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1207: "| Transactions | 3 (list, get one, get an attached file) | 33 transaction types, ... memo and note text, ACH trace or wire IMAD/OMAD reference numbers |" and line 1205: "| Accounts | 2 (list, get one) | Name, type ..., balance, last 4 of account and routing number |"

**Problem:** The section 6.2 "what you get" table advertises two fields the companion reference proves are not delivered, with no caveat. RHO_API_REFERENCE.md line 2735: "`transactions.tracking_number` (documented in detail as an ACH NACHA trace or wire IMAD/OMAD) and `transactions.counterparty_logo_url` appear on **zero** of 72 transactions", and line 7046 calls it "No payment tracing in practice." RHO_API_REFERENCE.md line 3963 records the Accounts divergence: "Every account carries masked account and routing numbers | 6 of 14 carry neither key". I re-verified both live: no transaction object carries a `tracking_number` key at all, and 6 of the 14 sandbox accounts carry neither `account_number_last_4` nor `routing_number_last_4`. The dossier compounds this at line 1691, where it cites "ACH NACHA traces and wire IMAD/OMAD identifiers are exposed" as evidence that "what is genuinely good here is the data model". An evaluator scoping a reconciliation or payment-tracing feature off the dossier will budget for a field that never arrives.

**Fix:** Line 1207: change the Transactions cell to end "... memo and note text. A `tracking_number` field for ACH trace or wire IMAD/OMAD is documented but returned on zero of 72 sandbox transactions." Line 1205: change the Accounts cell to end "... balance, and masked account and routing numbers on 8 of the 14 sandbox accounts (6 carry neither)." Line 1691: strike "ACH NACHA traces and wire IMAD/OMAD identifiers are exposed" or qualify it as schema-only.

## 19. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1300: "| 2026-04 | Brex | MCP server, 44 tools, limited writes, no money movement |"

**Problem:** The dossier gives Brex's MCP server three different tool counts in three different chapters. Line 1300 (section 6.7 timeline) says 44 tools. Lines 1409 and 1555 (sections 7.3 and 7.7) say "~37 read tools and 4 low-risk write tools" and "~37 reads and 4 low-risk writes", which totals 41. Line 1688 (section 8.1) says "Yes, roughly 41". The underlying research file scratchpad/rho/findings/mk-agentic.md says "~41 tools" at line 51 and enumerates "~37 read tools" plus "4 write tools" at line 75; VERIFIED.md says 44. The two sources were never reconciled and both numbers were carried into the document. This sits in the one comparison the dossier uses to argue Rho is behind its cohort on agent surface area.

**Fix:** Pick one figure and use it in all four places. The enumerated evidence supports 41 (37 read plus 4 write), so change line 1300 to "| 2026-04 | Brex | MCP server, roughly 41 tools (~37 read, 4 low-risk write), no money movement |" and re-check VERIFIED.md's 44 against developer.brex.com/docs/mcp before publishing.

## 20. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1900: "Webster's standalone bank-level assets were $85.5B per the FDIC call report of 2026-03-31 ... The honest comparison against a competitor's standalone partner bank is $85.5B"

**Problem:** Two problems, both under a **Verified:** label. (a) $85.5B is Rho's own trust-page footnote figure for a stale quarter. I queried the FDIC directly (api.fdic.gov/banks/institutions?filters=CERT:18221, 2026-09-11): Webster Bank, N.A.'s final call report is dated 06/30/2026 with ASSET 85,895,199 thousand, i.e. $85.90B, not $85.5B. (b) The dossier's own line 224 establishes that Webster Bank, N.A. (cert 18221) went ACTIVE=0 with end-effective date 08/20/2026 and that Rho's deposits now sit at Santander Bank, N.A. (cert 29950). Offering a defunct entity's March number as "the honest comparison against a competitor's standalone partner bank" is wrong: the bank-level comparator for the institution that actually holds Rho deposits today is Santander Bank, N.A. at ASSET 103,964,782 thousand ($103.96B) as of 06/30/2026, which I pulled from the same FDIC endpoint.

**Fix:** Replace with: "Webster's final standalone bank-level figure was $85.90B at its last FDIC call report (06/30/2026, cert 18221); Rho's trust-page footnote still cites $85.5B as of 03/31/2026 while using $327B in headlines and navigation. Because Webster N.A. ceased to exist on 2026-08-20, the correct bank-level comparator today is Santander Bank, N.A. (cert 29950), $103.96B in assets at 06/30/2026 - still far larger than any competitor's standalone partner bank, and still roughly a third of the $327B group figure Rho headlines."

## 21. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1512, First Citizens / SVB row: "Startup Money Market (rate sheet dated 2025-12-10): **0.10% APY under $50K**, 2.38% $50K to $1M, 3.30% above $1M"

**Problem:** Presented as a competitor's published price in a table of competitor economics. It is not. findings/mk-banks.md line 206 records these three rates as "[Rho claim]" taken from Rho's versus/svb page, notes that Rho itself says SVB "does not publish current startup money-market rates online," and states "I could not independently locate a newer public SVB startup rate sheet." The figure appears exactly once in the dossier, with no attribution and no hedge, in a row a treasurer could act on (0.10% under $50K is the number the surrounding argument leans on). This violates the dossier's own stated method at line 51: "Pricing and product claims about competitors are their own published figures unless a primary source is cited."

**Fix:** Change the cell to: "Startup Money Market, per Rho's versus/svb page citing an SVB rate sheet dated 2025-12-10 and not independently verifiable because SVB publishes no startup money-market rates online: 0.10% APY under $50K, 2.38% $50K to $1M, 3.30% above $1M (Rho's figures, unconfirmed)."

## 22. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 667: "(Stripe Atlas $500, Clerky $427 to $819, LegalZoom from $149 plus filing fees billed separately)"

**Problem:** All three competitor prices are lifted verbatim from Rho's own marketing page, pages/core/product__incorporation.txt lines 128, 131 and 150, which carries its own disclaimer: "(Competitive data collected from Stripe Atlas, Clerky, and LegalZoom websites as of 2026-09-07, and may change.)" The dossier states them as neutral fact with no attribution and no as-of date. They are Rho's comparison of its competitors, not the competitors' published figures, and the dossier's whole thesis is that Rho's competitor content is stale and self-serving. (LegalZoom's "from $149 plus state fees" does check out independently; Atlas and Clerky were not re-verified against the vendors.)

**Fix:** Replace with: "(Rho's own comparison figures, collected by Rho from the vendors' sites as of 2026-09-07 and not independently re-checked: Stripe Atlas $500, Clerky $427 to $819, LegalZoom from $149 plus filing fees billed separately.)"

## 23. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 667: "this is the cheapest headline price in its set (Stripe Atlas $500, Clerky $427 to $819, LegalZoom from $149 plus filing fees billed separately)"

**Problem:** The sentence is refuted by its own parenthetical. LegalZoom's headline price is $149, which is below Rho's $400, so $400 is not "the cheapest headline price in its set." The claim is true only all-in: LegalZoom bills Delaware's filing fee separately (roughly $109 minimum for a corporation) and sells registered agent service separately at $249/year, so a comparable first-year bundle is roughly $507. That is the comparison Rho's own page actually draws, and the dossier collapses it into the wrong word.

**Fix:** Replace "this is the cheapest headline price in its set" with "this is the cheapest all-in price in its set once Delaware filing fees and a year of registered agent service are counted; LegalZoom's $149 headline is lower but excludes both, which is how its bundle reaches roughly $500 in year one".

## 24. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 631: "There is no help-center category for it (one article, filed under general information), no published price of any kind, and the personal-guaranty and minimum-revenue conditions appear only in the lender's disclaimer."

**Problem:** "No published price of any kind" is contradicted three times inside the same document: line 148 ("Rho Capital | $0 origination, $0 prepayment; the actual rate is published nowhere"), line 623 ("$0 origination fee, $0 prepayment penalty") four paragraphs above, and line 881 ("Rho publishes exactly two prices for it: $0 origination fee and $0 prepayment penalty"). The adversarial checker flagged this exact wording in VERIFIED.md under rho-capital: "'No fee range' is true for rates, but Rho does publish two Capital price points ($0 origination, $0 prepayment penalty). Say 'no rate, APR, factor rate or price range' rather than 'no fee'." The correction was applied in section 4 and missed here.

**Fix:** Replace "no published price of any kind" with "no published rate, APR, factor rate or price range of any kind, the only Capital prices Rho publishes being $0 origination and $0 prepayment".

## 25. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1831: "The trustee put the gap between the ledger and the actual cash at $65M to $95M; the CFPB put it at $60M to $90M"

**Problem:** Line 1533 states the same quantity as "$65M to $96M by the Chapter 11 trustee (former FDIC Chair Jelena McWilliams)." The two passages disagree on the same number. The trustee's figure, as reported by American Banker (which I fetched on 2026-09-11), is "$65 million to $96 million of its fintechs' end users' money is missing." Line 1831's $95M is the wrong one, and it sits inside a paragraph explicitly labelled **Verified:**.

**Fix:** At line 1831 change "$65M to $95M" to "$65M to $96M".

## 26. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 293: "six incidents, all between 2023-06-06 and 2023-09-05, and three planned maintenances, the last on **2024-09-28**. **No incident has been posted since September 2024.**"; line 295: "two years of zero posted incidents"

**Problem:** Both sentences contradict the list in the same sentence that precedes them. By the dossier's own data the last incident is 2023-09-05; the 2024-09-28 entry is a planned maintenance, not an incident. So no incident has been posted since September 2023, which is three years to the 2026-09-11 capture, not two. findings/mk-rho-company.md line 16 states it correctly: "the last incident was 09/05/2023; the last entry of any kind was a planned database maintenance on 09/28/2024." The error understates the dossier's own argument by a full year and is visible to any reader who reads two sentences in a row.

**Fix:** Line 293: "...and three planned maintenances, the last on 2024-09-28. No incident has been posted since September 2023, and no entry of any kind since September 2024." Line 295: "Assessment: three years with no posted incident, and two with no status-page entry of any kind, at a company that shipped an API..."

## 27. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1745: "| Any public satisfaction score for Rho | None. No G2, Trustpilot or NPS figure appears anywhere | Rho cites G2 scores against at least eleven competitors |"

**Problem:** Factually false and insinuating. Rho publishes its own G2 rating of 4.8 on 25 pages of the captured corpus, on the same comparison tables where it cites competitors' scores. pages/partner/dfj.txt line 121 reads "G2 Rating 4.8 4.5 4.7 4.8 N/A" under column headers "Rho Mercury Brex Ramp Amex" (so Rho 4.8, Mercury 4.5, Brex 4.7, Ramp 4.8); the same block appears at pages/core/lp__affiliate-banking.txt lines 125-126, pages/core/lp__affiliate-card.txt, pages/core/lp__nerdwallet-checking.txt, pages/core/lp__nerdwallet-startup-cards.txt and pages/core/setupclaw.txt. `grep -rl "G2 Rating" pages/` returns 25 files. The row as written implies Rho selectively hides its own score while citing others', which the corpus contradicts.

**Fix:** Replace the row with: "| Published satisfaction detail | Thin. Rho publishes a self-reported G2 rating of 4.8 on 25 landing and partner pages, with no review count, no date and no link; no Trustpilot score or NPS figure appears anywhere | Competitors' G2 listings carry review counts and dates |" Or delete the row: a self-published G2 score is not a capability gap.

## 28. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 739: "There is also no status page, uptime figure or SLA anywhere in the crawled corpus, which for a platform that holds operating cash is a real omission." And line 1990: "There is also no published uptime SLA or status page."

**Problem:** Both statements are contradicted by the document's own section 2, which devotes a subsection (lines 291-297) to "Rho runs a public status page at status.rho.co," reproduces its five components and its nine-entry history, and captures it at 2026-09-11 19:13:30 ET. A reader of 3.16 or of diligence question 17 will conclude Rho publishes no status page at all and will put a question to Rho that the evidence already answers. The narrow defence, that status.rho.co sits outside the 556-page rho.co crawl, is not available at line 1990, which drops the "in the crawled corpus" qualifier entirely.

**Fix:** Line 739: "Rho publishes no uptime figure and no SLA anywhere in the corpus. Its status page at status.rho.co (section 2) has posted no incident since September 2023 and nothing of any kind since September 2024, so it gives a prospective customer no usable availability signal." Line 1990: "...no contractual breach-notification window. The status page at status.rho.co has been dormant since September 2024 and there is no published uptime SLA."

## 29. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 232: "Note also that Lead Bank held **$2.76B** in assets at the 06/30/2026 FDIC call report, which is smaller than three of the four partner banks Rho names when it argues that its competitors are built on small banks."

**Problem:** An insinuation of hypocrisy built on two non-comparable facts. Rho's size argument is specifically about deposit-holding partner banks: trust.txt line 30 reads "unlike most fintechs, the bank behind it is one of the largest in the country," and pages/blogcomp/blog__best-business-bank-accounts.txt line 216 compares "the next-largest deposit partner bank" (Choice $6.13B, Column $1.39B, Coastal $5.66B, Thread $1.04B, Middlesex $642M). Lead Bank is Rho's lender, not a deposit partner; no customer deposit sits there and its balance sheet bears on lending capacity, not on FDIC exposure. The count is also loose: against the five comparator banks Rho actually names (Cross River $8.53B, Choice $6.38B, First Internet $5.53B, Coastal $5.45B, Column $1.77B per findings/mk-rho-company.md), Lead at $2.76B is smaller than four and larger than one, and the sentence compares a 06/30/2026 figure against Rho's published 3/31/2026 figures.

**Fix:** Replace with: "Lead Bank, which makes the Capital loans, held $2.76B in assets at the 06/30/2026 FDIC call report. That is a lender, not a deposit partner, so it is not the comparison Rho makes when it argues about the size of the bank holding customer deposits; a buyer sizing a Capital facility against a bank line may still want the number."

## 30. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1385: "Two Rho claims in this matchup do not survive contact with the evidence. First, Rho's treasury pages headline 4.66% while never mentioning that Ramp's investment-account minimum is $5,000 against Rho's $50,000, a 10x gap that runs the wrong way for Rho."

**Problem:** The first item is not a claim and nothing about it failed verification. It is a competitor advantage that Rho's marketing does not volunteer, which is what every vendor's marketing does, including Ramp's and Brex's. Filing it under "claims that do not survive contact with the evidence" converts a normal marketing omission into an accusation of falsity, and it sits directly above the one item on the list that genuinely is a claim that failed (the 4.66% headline). This is also the only place in the document where Rho is charged with a failed claim for something it did not say.

**Fix:** Replace the lead-in with: "One Rho claim in this matchup does not survive contact with the evidence, and one competitive omission is worth naming. The omission: Rho's versus/ramp page argues its $50,000 Treasury minimum as a win against Mercury's $250,000 and never mentions that Ramp's investment account opens at $5,000, ten times lower than Rho's. The claim: the 4.66% is the top fee tier's rate and..."

## 31. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1621: "Brex, by Rho's own account on its /versus/brex page (figures verified 08/17/2026), offers \"24/7 live support (chat, email, phone, SMS, WhatsApp) for all users.\""

**Problem:** Two problems in one sentence, on the fact that most undercuts what the same paragraph calls "the cleanest verified win in the set." First, the document's own stated methodology limit 6 (line 2135) reads "Rho's own comparison tables were not used as evidence about competitors," and 6.7 line 1313 instructs "Do not cite Rho's competitive table as evidence for anything." This sentence does exactly that. Second, "figures verified 08/17/2026" misrepresents Rho's own as-of stamp as a verification: the page text at pages/core/versus__brex.txt line 136 reads "(brex.com support docs, as of 08/17/2026)." An independent primary source exists and the research already found it: findings/mk-brex.md lines 517-525, marked `[VERIFIED-PRIMARY - brex.com/support/contact-and-support]`, tabulates "Live support 24/7 (chat, email, phone, SMS, WhatsApp)" as available on both Essentials and Premium. Because this fact is then reused twice more (line 1593 table row "Brex, which offers 24/7 phone on its free plan" and line 1755 "Brex has already paid for it"), the weak sourcing propagates through the whole differentiation verdict.

**Fix:** Replace with: "Brex's own support documentation (brex.com/support/contact-and-support, checked 2026-09-11) lists 24/7 live support by chat, email, phone, SMS and WhatsApp on every plan including the free Essentials tier; Premium adds dedicated specialists for admins and bookkeepers during business hours and Enterprise adds a named account manager with VIP support limited to 5am-5pm PST."

## 32. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 293: "**No incident has been posted since September 2024.**" and line 295: "Assessment: two years of zero posted incidents..."

**Problem:** Both figures are contradicted by the evidence quoted in the same paragraph and by the captured artifact. status-history.rss lists six incidents dated 2023-06-06, 2023-07-27, 2023-08-01, 2023-08-02, 2023-09-01 and 2023-09-05, then three planned maintenances dated 2023-12-05, 2024-04-27 and 2024-09-28. The last incident is September 2023, not September 2024; September 2024 is the last planned maintenance. The gap is therefore three years, not two. The error is in a bolded finding and in the sentence that carries the section's assessment, and it is repeated in the fix at line 739.

**Fix:** Line 293: "**No incident has been posted since September 2023, and nothing of any kind since the planned maintenance of 2024-09-28.**" Line 295: "Assessment: three years of zero posted incidents at a company that shipped an API, a lending product, invoicing, incorporation and a mobile Treasury flow in 2026 alone is not a plausible operational record."

## 33. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 518: "the extra 75 basis points of cashback is what Rho pays to become the system of record"; defined only at line 851

**Problem:** "Basis points" is used at line 518 in the Assessment that explains Rho's entire commercial engine, and is defined 333 lines later at line 851 ("'bps' is basis points, hundredths of a percentage point"). It is used again at 1381 ("48 basis points below the headline") and 1683. A newcomer at line 518 cannot tell whether 75 basis points is large or trivial, which is exactly the judgment that sentence asks them to make.

**Fix:** At line 518 write "the extra 75 basis points (hundredths of a percentage point, so 0.75%) of cashback is what Rho pays..." and either delete the redundant definition at line 851 or add "basis point" as a Section 1 glossary row alongside Yield and APY.

## 34. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1177: "Rho's OAuth server at auth.rho.co returns 'Dynamic registration is not enabled'"; line 1225: "Rho runs an OAuth 2.0 authorization server"

**Problem:** OAuth is used 10 times and is never explained, even though section 6 explains almost every other technical term it uses (scope at 1213, PKCE at 1225, dynamic client registration at 1227, webhook at 1281, idempotency at 1321, GET at 1202). The reader is told what PKCE protects without being told what OAuth is. This matters because 6.3 asks the reader to choose between "two ways to hold a credential" and one of them is only describable in OAuth terms.

**Fix:** At line 1225 open with: "**Partner OAuth.** OAuth is the standard 'sign in with' mechanism: instead of handing a third-party app your password, you approve it at Rho's own login screen and the app receives a short-lived token limited to what you approved. For a third-party application acting on behalf of Rho customers, Rho runs an OAuth 2.0 authorization server at auth.rho.co..." and gloss the earlier line 1177 use as "Rho's OAuth server (the 'sign in with Rho' service at auth.rho.co)".

## 35. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1143: "Rho's marketing fights the neobank peer set"

**Problem:** "Neobank" is never defined in the document, and it is the category noun for Rho's entire competitive set. It is used again at line 1765 ("it is also what every neobank does") in the concluding judgment of section 8.4. Section 1 defines "fintech vs bank" but never gives the reader the word the document actually uses for Rho's peer group.

**Fix:** At line 1143 write: "Rho's marketing fights the neobank peer set (neobank: a software company that offers a bank-like account through a partner bank without holding a charter itself, which is what Mercury, Brex and Rho all are)..." Better, add it to the Section 1 "Fintech vs bank" glossary row as the name for that category.

## 36. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1122: "Rho is not buying float, it is buying the primary operating relationship"; float is defined only at line 1345

**Problem:** "Float" appears at line 1122 as the pivot of the partner-microsite economics assessment, undefined, and is explained 223 lines later in a table cell at line 1345 ("interest on money in transit ('float')"). It then carries a whole sub-argument at line 1491 ("The double dip on float"). Two different senses are in play (interest earned on money in transit, and the general benefit of holding someone's cash) and neither is distinguished.

**Fix:** At line 1122 write: "Rho is not buying float (the interest a company earns simply from holding your cash while it sits there), it is buying the primary operating relationship..." and cut the parenthetical at line 1345 to avoid the duplicate.

## 37. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Lines 378 to 381, the Rho Treasury menu table: "offered as a cash sweep, fixed $1.00 NAV" / "Morgan Stanley Ultra-Short Income Portfolio (commercial paper, corporate debt, asset-backed)" / "investment-grade corporate bonds"

**Problem:** Four undefined instrument terms land in one four-row table that the reader is expected to use to allocate their company's cash: "cash sweep" (distinct from the Section 1 "sweep network" row, which is about FDIC insurance, not funds), "commercial paper", "asset-backed", and "investment-grade". NAV is handled well at line 383, immediately below the table, which proves the author knew this table needed glossing and stopped after one term. The whole point of the table is that these instruments carry different risk, and the reader cannot see the risk without the words.

**Fix:** Extend the line 383 paragraph: "NAV means net asset value, the per-share price of a fund. A fixed $1.00 NAV means the price does not move; a variable NAV means it can. Three other terms in that table matter. **Commercial paper** is short-term IOUs issued by large companies, and **asset-backed** debt is backed by a pool of loans, so both carry a small risk the borrower does not pay, unlike a Treasury Bill. **Investment-grade** means rated safe by the ratings agencies, which is safer than most corporate debt and still not risk-free. A **cash sweep** here means the fund your uninvested cash sits in by default, which is a different thing from the savings sweep network in Section 1."

## 38. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 409: "T-Bills on a trailing 7-day average, money market funds on 7-day SEC yield, bond funds on 30-day SEC yield"

**Problem:** "7-day SEC yield" and "30-day SEC yield" appear once each, undefined, inside the Assessment that tells the reader Rho's yield methodology is honest. The reader is being asked to accept a judgment about a methodology whose terms have not been explained. These are also the basis of the 4.66% versus 4.18% argument that runs through sections 3.3, 4.4, 7.2 and 8.2.

**Fix:** At line 409 write: "...the methodology page is dated and specific (T-Bills on a trailing 7-day average, money market funds on 7-day SEC yield and bond funds on 30-day SEC yield, both of which are the SEC's standard formulas for stating a fund's recent income as an annual rate, net of fees, so that two funds can be compared on the same basis), and..."

## 39. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 352: "a representation that all non-public-unit clients 'are an accredited investor'"; repeated at line 1818

**Problem:** "Accredited investor" is a specific SEC-defined status with numerical thresholds, presented here as something the reader is silently signing up to, and it is never defined. It appears again at line 1818 as diligence-relevant ("This never appears in Rho's savings marketing"), so the document treats it as important while leaving the reader unable to tell whether they qualify. "Non-public-unit" is also undefined.

**Fix:** At line 352 write: "...contains a representation that all clients other than government bodies (\"non-public-unit\" clients) \"are an 'accredited investor'\", which is an SEC status that for a company generally means holding more than $5 million in assets, a condition Rho never mentions in marketing."

## 40. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 198: "The first Form D filed with the SEC on 2018-10-24 names three executive officers"; defined only at line 263

**Problem:** Form D carries the entire corporate-record argument in section 2 and is used 12 times. It is first used at line 198, used again in the funding table at 271, and only defined at line 263 ("A Form D is the short notice a company files with the SEC after selling securities privately under the Regulation D exemption"). The definition arrives after the reader has already been asked to draw conclusions from Form D filings twice. The related "Regulation D exemption", "Section 4(a)(2)", "Regulation S" and "safe harbor" at line 275 are also undefined.

**Fix:** Move the definition from line 263 to line 198: "The first Form D (the short notice a company must file with the SEC after selling shares privately) filed on 2018-10-24 names three executive officers..." and at line 275 write "Equity sold under Section 4(a)(2) without that safe harbor (a different, narrower private-placement rule that carries no filing requirement), or offshore under Regulation S (the rule for sales to non-US buyers), would generate no Form D at all."

## 41. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1095: "### 5.2 The ICP the money describes"

**Problem:** ICP appears cold as a section heading, which is the worst possible place for an undefined acronym because it is also in the table of contents-level structure of the document. It is used again at line 1153 ("#### The ICP, stated plainly"). It is never expanded anywhere.

**Fix:** Retitle to "### 5.2 The ideal customer profile the money describes" and at line 1153 "#### The ideal customer profile, stated plainly". If the abbreviation is wanted, first use should read "the ideal customer profile (ICP), meaning the specific kind of company a vendor's pricing and incentives are actually built to attract".

## 42. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 18: "SEC EDGAR and Form ADV filings, FDIC BankFind, OCC licensing decisions, Capital One's 10-Q"

**Problem:** Four undefined items in the opening credibility statement, the paragraph whose job is to make the reader trust the document. OCC (15 uses) is never expanded anywhere in 54,000 words, despite being decisive to the Mercury charter argument in 7.4. EDGAR (4 uses), Form ADV (11 uses) and 10-Q (7 uses) are likewise unexpanded here; Form ADV finally gets a parenthetical at line 1923 and 10-Q never does. Form ADV supplies the only hard scale number in the document ($1.89B AUM).

**Fix:** Rewrite line 18 as: "- **Independent sources** for everything about the outside world: SEC EDGAR (the Securities and Exchange Commission's free public filings database) and Form ADV filings (the annual disclosure every SEC-registered investment adviser must file), FDIC BankFind (the FDIC's public register of insured banks), licensing decisions by the OCC (Office of the Comptroller of the Currency, the federal regulator that grants national bank charters), Capital One's 10-Q (a public company's quarterly financial report to the SEC), competitor documentation and pricing pages, and press coverage."

## 43. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 33: "The alarming number comes from the CFPB, not from Rho."

**Problem:** CFPB is used 7 times across the document, including as the source of a $46,248,291 victim payment in the Synapse case at line 1533 and as the origin of the ten-card liability rule at line 1863, and it is never expanded anywhere. At line 33 it is the punchline of the paragraph explaining the document's own method.

**Fix:** At line 33 write: "The alarming number comes from the CFPB (the Consumer Financial Protection Bureau, the US federal agency that writes and enforces consumer finance rules), not from Rho."

## 44. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 88 (SIPC glossary row): "both FINRA/SIPC members"; line 89: "400+ FDIC- and NCUA-insured institutions"

**Problem:** Two regulator acronyms are introduced inside Section 1's glossary itself, in the example column, without being defined. FINRA (2 uses) is never expanded anywhere in the document. NCUA (8 uses) is used five times before it is finally defined at line 1776, and the definition there says "A third acronym appears once below", which understates its own frequency. This is the glossary breaking its own contract inside its own rows.

**Fix:** In the line 88 example cell write "both members of FINRA (the brokerage industry's self-regulator) and SIPC." In the line 89 example cell write "a network of 400+ institutions insured by the FDIC or, for credit unions, the NCUA (the credit-union equivalent of the FDIC, same $250,000 limit)." Then delete the NCUA sentence at line 1776.

## 45. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1207: "ACH trace or wire IMAD/OMAD reference numbers"; line 1693: "ACH NACHA traces and wire IMAD/OMAD identifiers are exposed"

**Problem:** IMAD, OMAD and NACHA are used with no explanation in the two places that make the case that Rho's data model is "better than most aggregators produce". The reader is asked to accept a quality judgment resting entirely on three terms they cannot decode. NACHA is used exactly once, at line 1693, as evidence.

**Fix:** At line 1207 write "...ACH trace numbers or the IMAD/OMAD reference numbers that uniquely identify a wire on the Federal Reserve's network (input and output message accountability data), which is what a bank asks for when a wire goes missing." At line 1693 write "ACH trace numbers in the NACHA format (NACHA is the body that writes the ACH network's rules)..."

## 46. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1161: "Google SSO is the only identity federation, no SAML, Okta, Entra or SCIM; no documented audit-log export"

**Problem:** Four undefined technical terms in one table cell, in the row describing the document's stated sweet-spot customer ("50-person startup with a controller"). SSO, SAML and SCIM are each used exactly once, here, and none is expanded; "single sign-on" appears at line 1613 but is never connected to the abbreviation SSO. The cell is the "what will frustrate them" column, so it is precisely the part a buyer reads closely, and it is unreadable without these four terms.

**Fix:** Rewrite the cell as: "Google sign-in is the only way to connect a company identity system, so there is no support for the enterprise standards (SAML for single sign-on, SCIM for automatically creating and removing user accounts) that Okta and Microsoft Entra use; no documented audit-log export; support response times are claimed three different ways on three pages and measured nowhere".

## 47. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1273: "full card number, CVC and expiry are never returned"; line 1446: "lets an agent self-retrieve PAN/expiry/CVC"; line 1749: "displays full card numbers and CVVs in the browser"

**Problem:** Three abbreviations for two concepts, none defined, and the document uses CVC and CVV interchangeably without saying they are the same thing. PAN is used once at line 1446 with no expansion. These appear in security arguments (what a leaked token can reach, what a Mercury agent can self-retrieve, what Rho displays without a PCI attestation) where the whole point is the sensitivity of the data.

**Fix:** At line 1273 write "full card number, the CVC security code on the back, and the expiry date are never returned." At line 1446 write "self-retrieve the full card number (PAN), expiry and security code". At line 1749 use "security codes" rather than introducing a third spelling, CVVs.

## 48. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 354: "Interest accrues daily on a 30/365 convention"; explained only at line 829

**Problem:** The 30/365 convention is presented at line 354 as a plain mechanical fact in the Business Savings section, where the reader is deciding whether 1.00% is worth it, and is explained 475 lines later at line 829 ("A 30/365 convention counts 360 interest days in a 365-day year, so a nominal 1.00% pays closer to 0.986%"). The effect it has on the rate is the reason it is in the document at all, so withholding it at first use inverts the purpose.

**Fix:** At line 354 write: "Interest accrues daily on a 30/365 convention, meaning every month counts as 30 days, so a year pays 360 days of interest rather than 365 and a nominal 1.00% is closer to 0.986% in practice (worked through in 4.3)."

## 49. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** lines 85, 91, 152, 168, 228, 244, 287, 1177, 1349

**Problem:** Nine cross-references point at the wrong section or at a section title that does not exist, which will compound every time the reader edits the file. Verified individually: line 152 "Section 6 works through all of them" (about the eleven undisclosed fees) points at section 6 "The API and the agent surface"; the fees are worked through in 4.9 "The fee reality" (line 902). Line 244 "(Section 7 covers the fees that sit outside that summary.)" points at the competitive landscape; same target, 4.9. Line 168 "Section 5 reads the contract properly" points at "Who Rho is for"; the contract is read in 9.4 "The contract" (line 1837). Line 228 "Section 5 covers this in detail, including the six-withdrawals-per-month cap and the Exhibit A insurance waiver" points at "Who Rho is for"; that material is in 9.2 "The savings sweep, read closely" (lines 1793-1823). Line 85 "Section 5 examines what its Terms of Service actually reserve" (personal guarantee) points at "Who Rho is for"; the examination is at line 526 in 3.5 and at lines 1876-1880 in 9.4. Line 287 "Section 3 takes up the scale claims" points at the product surface; the $4B/8,000 claims are taken up at line 1122 (5.2) and line 2038 (10.2). Line 1177 "Section 7 covers the API surface in detail" points at the competitive landscape; the API is section 6 and the companion document. Line 91 "Section 4 shows why the reachable number ... is 4.18%" points at a section whose own text (line 863) defers back to section 3 ("That is treated fully in the products section"), where the derivation actually lives (line 405, 3.3). Line 1349 "See **The Rho API and MCP surface**" names a heading that does not exist anywhere in the file.

**Fix:** Line 85: "Section 5 examines" -> "Section 9.4 examines". Line 91: "Section 4 shows" -> "Section 3.3 shows". Line 152: "Section 6 works through all of them." -> "Section 4.9 works through all of them." Line 168: "Section 5 reads the contract properly." -> "Section 9.4 reads the contract properly." Line 228: "Section 5 covers this in detail" -> "Section 9.2 covers this in detail". Line 244: "(Section 7 covers the fees that sit outside that summary.)" -> "(Section 4.9 covers the fees that sit outside that summary.)" Line 287: "Section 3 takes up the scale claims." -> "Section 5.2 takes up the scale claims." Line 1177: "Section 7 covers the API surface in detail." -> "The companion document `RHO_API_REFERENCE.md` covers the API surface in detail." Line 1349: "See **The Rho API and MCP surface**" -> "See section 6, The API and the agent surface,".

## 50. [MAJOR] RHO_API_REFERENCE.md
**Locator:** line 2925 "See **Pagination and cursors** for the forging"; line 5999 "See \"Base URLs and environments\"."; line 6195 "See \"Scopes and permissions\" for the full table."; line 6345 "See \"The resource model\" and \"Endpoint reference\" for the full schemas."

**Problem:** Four cross-references name section titles that do not exist in the delivered document; they are leftovers from an earlier outline. Confirmed by grep over all headings: "Pagination and cursors" 0 matches (the heading is 6.1 "Pagination"), "Base URLs and environments" 0 matches (the heading is 1.5 "The two hosts"), "Scopes and permissions" 0 matches (the headings are 1.7 "The five scopes" and 2.3 "Scopes"), "The resource model" 0 matches (no such section). A reader following any of them, in a 7,400-line file with no anchor links, searches and finds nothing.

**Fix:** Line 2925: "See **Pagination and cursors**" -> "See section 6.1, Pagination,". Line 5999: "See \"Base URLs and environments\"." -> "See section 1.5, The two hosts." Line 6195: "See \"Scopes and permissions\" for the full table." -> "See section 2.3, Scopes, for the full table." Line 6345: "See \"The resource model\" and \"Endpoint reference\" for the full schemas." -> "See sections 4 and 5, the endpoint references, for the full schemas."

## 51. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** lines 55-68, the "## Contents" block (same defect at RHO_API_REFERENCE.md lines 78-87)

**Problem:** Neither document is navigable. Both contents blocks are plain unlinked text listing only the top-level sections: 10 entries for a 2,183-line document containing 94 subsections, and 8 entries for a 7,400-line document containing 56 subsections. `grep -c '](#'` returns 0 for both files, so there is not one working anchor link in either. The reader who asked for depth and said they will maintain these has no way to jump to 4.9, 7.4, 9.6, 3.3 or 6.2 except by scrolling or searching, and no way to see from the front matter that those subsections exist at all. This is the direct cause of "buried": section 9.6 "The diligence checklist", eighteen questions to put to Rho in writing before moving operating cash, is arguably the most actionable page in the dossier and is discoverable only by reading to line 1929.

**Fix:** Replace both plain lists with two-level anchor-linked tables of contents. For the dossier, e.g.: "1. [Rho in plain English](#1-rho-in-plain-english)" with nested "   - [1.1 The vocabulary you need](#the-vocabulary-you-need)" style entries for every `###` heading, generated from the existing headings (GitHub-style slugs: lowercase, spaces to hyphens, punctuation stripped). Do the same for the API reference across its 56 `###` headings. At minimum, list every subsection number and title even if the links are omitted.

## 52. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** lines 1-9, everything between the title "# Rho: An End-to-End Product Dossier" and "## How this was researched, and how much to trust it"

**Problem:** The dossier's conclusions are buried and nothing surfaces them up front. A newcomer opening a 54,000-word file gets three lines of purpose and then 44 lines of methodology before any finding. The verdict ("Rho is a well-executed bundle rather than a differentiated technology company", 8.4) is at line 1751 of 2183; the fee reality is at 902; the diligence checklist at 1929; the eligibility gate at 986. The companion API reference solves exactly this problem for itself with "### The single most useful finding" and "### The second most useful finding" inside its first 60 lines, so the pattern already exists in the deliverable and was simply not applied to the document aimed at the reader who "doesn't know anything about the product". This is the most likely thing the reader comes back and asks for: a page they can read in three minutes and a pointer into the rest.

**Fix:** Insert a "## The short version" block immediately after line 7, before "How this was researched", with six to eight one-line findings each ending in a section pointer, drawn verbatim from conclusions already in the text: what Rho is in one sentence (from line 74); "Rho is not a bank; deposits sit at Webster Bank, a division of Santander Bank, N.A., and FDIC insurance covers that bank failing, not Rho failing (1.4, 9.1)"; "The software is genuinely $0; you pay in interchange, deposit spread, 1% FX and the 0.15%-0.60% Treasury fee (4.1-4.9)"; "The headline 4.66% Treasury yield is unreachable under Rho's own 50% allocation cap; 4.18% is the realistic ceiling at the top tier (3.3)"; "The API is 14 read-only GET operations; nothing can move money (6.2)"; "Against Ramp, Brex and Mercury, Rho wins on no seat fees, 24/7 phone support and the $75M savings ceiling, and loses on scale, write APIs and agent surface (7.2-7.4)"; "Verdict: a well-executed bundle with one structural pricing bet, not a differentiated technology company (8.4)"; "Before moving cash, work section 9.6's eighteen questions."

## 53. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 2111: "Their output is the verified claim register, and it is the authority wherever it disagrees with a findings file." Cited as evidence at lines 1361, 1385, 1395, 1428, 1541.

**Problem:** The document names a claim register as its top authority and cites it five times in the competitive section as the basis for load-bearing numbers (Ramp's $44B and 70,000 customers, Capital One's $4,521M purchase consideration, Mercury's 2026-04-24 OCC date, the ADM sweep terms, the 4.18% Treasury ceiling), but never gives the register a filename or a path, and does not deliver it. The file exists as VERIFIED.md in the same undelivered scratchpad tree as the scripts. A reader who wants to check any "Verified (claim register)" citation, or who wants to follow step 10 of the refresh procedure ("Re-run the refutation pass on every claim whose evidence you just edited, and re-date the verified register"), has nothing to open. The same applies to the "29 findings files, 305,887 words" in the 10.3 table.

**Fix:** Ship the register with the documents (it comes along with the cp -R in the first defect's fix) and name it. Change line 2111 to: "Their output is the verified claim register, shipped beside this document as `rho-research/VERIFIED.md`, and it is the authority wherever it disagrees with a findings file (`rho-research/findings/`)." Then change the five in-text citations from "(claim register)" to "(claim register, `rho-research/VERIFIED.md`)" on first use in section 7, at line 1361.

## 54. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 904: "Rho repeats one sentence across 19 files in its own corpus, including its help center and its machine-readable site summary". Same figure at line 152 ("appears verbatim in 19 files across Rho's own corpus") and line 492 ("repeated verbatim in 19 corpus files including the help center")

**Problem:** The count is wrong and its provenance is the research scratchpad, not Rho. The sentence "The only standard payment fee is 1% on foreign-currency transfers" appears verbatim in exactly four Rho-authored documents: the help-center article general-rho-information/pricing-requirements, /versus/chase, site-llms.txt and site-llms-full.txt. Three further Rho pages carry reworded variants (/versus/ramp and /versus/svb both read "1% on foreign-currency transfers as the only standard payment fee"; /blog/best-business-bank-accounts reads "the only standard payment fee is a 1% foreign-currency conversion fee"). A recursive grep over the whole scratchpad returns exactly 19 files, but 11 of them are the research team's own output (VERIFIED.md, four dossier/ section drafts, six findings/ files) and one is a duplicate capture of the help article. The figure was computed over the working directory rather than the corpus. As written the claim overstates Rho's repetition of the line roughly fivefold, in a passage whose whole point is how insistently Rho repeats it.

**Fix:** At line 904 replace "across 19 files in its own corpus" with "in four of its own documents, including its help center and both machine-readable site summaries, with reworded variants on three more pages". At line 152 replace "appears verbatim in 19 files across Rho's own corpus" with "appears verbatim in four of Rho's own documents". At line 492 replace "repeated verbatim in 19 corpus files including the help center" with "repeated verbatim in four corpus files including the help center".

## 55. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1623: "Separately, four versus pages (Amex, BILL, HSBC, SVB) upgrade the claim to \"a dedicated human account manager to every client,\""

**Problem:** The quoted string appears verbatim on exactly two versus pages, and one of the four named pages carries no such claim at all. /versus/amex line 180 and /versus/chase line 186 both read "Rho provides a dedicated human account manager to every client" - and /versus/chase is not in the document's list. /versus/bill line 195 reads "Every Rho client has a direct line to a human account manager", different wording. /versus/hsbc line 174 reads "a dedicated account manager to every client at no additional cost", without "human". /versus/svb line 201 reads "Rho provides dedicated support for every client" and contains no account-manager claim anywhere. The sentence attributes a verbatim quotation to a page that does not make the claim, inside an accusation that Rho overstates its support model.

**Fix:** Replace with: "Separately, /versus/amex and /versus/chase upgrade the claim to \"a dedicated human account manager to every client,\" while /versus/bill offers \"a direct line to a human account manager\" and /versus/hsbc \"a dedicated account manager to every client at no additional cost\" - which Rho's more carefully sourced pages contradict by reserving named account managers for growth-stage and qualifying clients."

## 56. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 581: "Vendors must already exist. \"Bookkeepers can draft but by default cannot execute payments.\""

**Problem:** Paraphrase presented as a verbatim Rho quotation, and the paraphrase broadens the restriction. The source, help-center/bill-pay/understanding-bulk-payments line 53, reads across two sentences: "Admins, Account Owners and Bookkeepers can view bulk payments, meaning they can import a CSV and make edits to payment drafts. By default, Bookkeepers cannot execute payments from the Bulk Payments workflow." No sentence in the corpus matches the quoted words. The compression also silently drops "from the Bulk Payments workflow", turning a workflow-scoped limit into a blanket statement about what bookkeepers can do at Rho.

**Fix:** Replace the quoted sentence with the source wording and keep the scope: "Bookkeepers can import a CSV and \"make edits to payment drafts\", but \"by default, Bookkeepers cannot execute payments from the Bulk Payments workflow.\""

## 57. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 526: "There are two consents, one in each card addendum, authorizing Rho to obtain \"a consumer report as defined in the Federal Fair Credit Reporting Act... about the Company and each authorized user,\""

**Problem:** One quotation is attributed to both addenda; the two addenda use materially different words, and the difference is the load-bearing one for this accusation. Terms of Service line 391 (Rho Corporate Card with Daily Terms Agreement, Section 1.12) reads "...about the Company and each authorized user". Line 504 (Monthly Card Agreement, Section 1.12) reads "...about you and each authorized user" - the individual, not the entity. The dossier's own authority file records this exact distinction ("(Daily Terms; the Monthly Terms version reads 'about you and each authorized user')"), and the parenthetical was lost in compression. Since the paragraph's whole argument is whether Rho reserves a right to pull a report on a person rather than on a company, quoting only the entity-scoped version understates the reserved right while misattributing it to both documents.

**Fix:** Restore the distinction: "...authorizing Rho to obtain \"a consumer report as defined in the Federal Fair Credit Reporting Act... about the Company and each authorized user\" in the Daily Terms addendum, and \"about you and each authorized user\" in the Monthly Terms addendum,"

## 58. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1175: "Rho's own comparison content names Novo as serving \"sole proprietors with an SSN, no EIN needed\""

**Problem:** Paraphrase presented as Rho's own words, sourced from the research notes rather than from Rho. The quoted string appears nowhere in the 556-page crawl. Its only occurrence on disk is scratchpad/rho/findings/mk-banks.md line 298, a researcher-written market note ("Novo serves sole proprietors with an SSN and no EIN"). What Rho actually publishes, on /blog/rho-vs-novo line 136, is: "A sole proprietor without employees can open a Novo business checking account using an SSN instead of an EIN, according to novo.co's own account requirements page." The companion quote in the same sentence ("best free back office for sole proprietors", /blog/best-business-bank-accounts line 320) is verbatim and correct, which makes the fabricated neighbour easy to miss.

**Fix:** Replace with Rho's wording: "Rho's own comparison content says \"a sole proprietor without employees can open a Novo business checking account using an SSN instead of an EIN\" and names Found the \"best free back office for sole proprietors.\""

## 59. [MAJOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 932: "**Genuinely buried:** the $20 to $45 failed-wire fee (one help-center article, and it directly contradicts the pricing page's own \"07 Domestic wire recall fee $0\")"

**Problem:** Both halves of this contradiction pair exist verbatim, but they address different events, so they do not genuinely conflict. /pricing line 43 prices a *recall* - the customer asking for a sent wire to be pulled back - at $0. The help article help-center/payments/fees-for-recalls-failed-wires prices a different event: "a fee of around $20 – $45 will be deducted from your Rho account for any domestic wire payments that fail and are returned to your Rho account." Neither page says a returned wire is free and neither says a recall costs $20-$45. The document's own section 10 (line 2010) gets this right, listing it as an open question with "Both are live" rather than as a contradiction, so the two passages disagree with each other as well.

**Fix:** Replace the parenthetical with: "(one help-center article; note it prices a different event from the pricing page's \"07 Domestic wire recall fee $0\", which covers customer-requested recalls rather than bank-returned wires, so the two are unreconciled rather than contradictory - see section 10)". Apply the same softening to "in genuine tension with an affirmative `$0` line" at line 940.

## 60. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 3354: "zero of 72 transactions, including all 13 ACH rows and all 13 domestic and international wire rows," versus line 2735 and line 7046: "including 11 ACH and 10 wire records"

**Problem:** The same document states the same fixture fact with two different pairs of numbers and never defines either. Verified live against the sandbox: ach_debit 6 + ach_credit 5 + ach_return 2 gives 13 ACH rows, or 11 if ach_return is excluded; wire_in 4 + wire_out 4 + international_wire_out 2 + wire_fee 1 + international_wire_fee 2 gives 13, or 10 if the two fee types are excluded. So 13/13 counts returns and fee rows as ACH and wire records, while 11/10 does not. The 13-wire figure is the weaker of the two, because it counts `wire_fee` and `international_wire_fee` rows as "domestic and international wire rows".

**Fix:** Standardise on the narrower, defensible pair and say what is counted. Change line 3354 to: "zero of 72 transactions, including the 11 `ach_debit` and `ach_credit` rows and the 10 domestic and international wire rows (excluding fee and return types)," so it matches lines 2735 and 7046.

## 61. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 2134: "it does not enforce the documented rate limits (68.9 requests per second sustained with no 429)"

**Problem:** "Sustained" misstates the measurement and contradicts the companion reference. RHO_API_REFERENCE.md line 2082 records 68.9 req/s as 60 requests over 0.871 seconds on 60 parallel connections and labels it "4,134 req/min instantaneous"; line 2089 explicitly separates the two axes: "a sustained run at 2.5x the documented per-token allowance and an instantaneous burst at roughly 69x it". The sustained figure is roughly 150 requests per minute, about 2.5 req/s, not 68.9 req/s. The dossier overstates the sustained throughput by roughly 28x.

**Fix:** Change to: "it does not enforce the documented rate limits (150 requests on one token in 57 seconds, and an instantaneous burst of 68.9 requests per second, both with no 429)".

## 62. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 2109: "A note on one number: earlier files inside this project describe the corpus as \"556 pages\" and \"536 pages\". Both are undercounts taken mid-crawl. The count at the end of the crawl is 556."

**Problem:** The sentence contradicts itself and misquotes the working files. It calls "556 pages" an undercount and then names 556 as the correct final count in the next sentence. It is also wrong about what the working files say: grepping the 29 findings files for page counts returns "536-page", "536 page" and "522-page" and no occurrence of a 556-page corpus claim. The final count of 556 is itself correct (I counted the pages tree on disk: 130 core + 269 help + 125 blogcomp + 25 partner + 7 others = 556, against 1,042 sitemap <loc> entries), so only this note is wrong.

**Fix:** Replace with: "A note on one number: earlier files inside this project describe the corpus as \"536 pages\" and \"522 pages\". Both are undercounts taken mid-crawl. The count at the end of the crawl is 556. Where this document and its working files disagree, 556 is right."

## 63. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 73: "This is a snapshot of a five-week-old API that Rho has said is actively moving. Section 8 lists what will change first."

**Problem:** Two problems in one sentence. First, the cross-reference is wrong: section 8 is "Building on it: integration patterns and a reference client" and nothing in 8.1 through 8.9 lists what will change first. The change-classification table and the additive-only policy are in 6.4; the forward-looking open items are in 7.10. Second, a related wrong pointer sits at line 6446: "Read that against the versioning policy in section 7.1", but section 7.1 is "Endpoint and transport"; the versioning policy and the 15-day notice floor quoted in that same sentence are in 6.4.1.

**Fix:** Line 73: "Section 8 lists what will change first" to "Sections 6.4 and 7.10 list what will change first". Line 6446: "the versioning policy in section 7.1" to "the versioning policy in section 6.4".

## 64. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 73: "a five-week-old API" versus line 139: "So the public surface is roughly six weeks old as of this writing (2026-09-11)."

**Problem:** The document gives the API two different ages 66 lines apart. Both are arithmetically derivable but from the two different launch dates the document itself flags at lines 133-135: 2026-08-03 to 2026-09-11 is 39 days (5.6 weeks), 2026-07-29 to 2026-09-11 is 44 days (6.3 weeks). Section 1.3 exists precisely to explain that there are two dates, so the front matter should not silently pick the other one.

**Fix:** Change line 73 to "a six-week-old API" to match line 139, or to "an API roughly six weeks old (see 1.3 on the two published launch dates)".

## 65. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 22: "every page of `docs.rho.co` was read (13 guides and 14 operation references)" versus RHO_PRODUCT_DOSSIER.md line 2102: "| docs.rho.co guide pages | 14 |"

**Problem:** The two documents disagree on the size of the docs corpus they both claim to have read in full. The captured directory scratchpad/rho/docs holds 14 files, of which 12 are `docs_v1_*` guide pages, one is the docs index and one is the OpenAPI index (`api_v1_openapi.md`). Neither 13 nor 14 is defined, and the dossier's next row already counts the OpenAPI document separately ("API operation references | 14, plus the OpenAPI document"), so the 14 in line 2102 double-counts it.

**Fix:** Standardise on the composition rather than a bare number. API reference line 22: "(12 guides, the docs index, and 14 operation references)". Dossier line 2102: "| docs.rho.co guide pages | 12, plus the docs index |".

## 66. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 2109: "All 14 operations list `200, 400, 401, 403, 500, 503`, and the 8 single-resource operations add `404`." and RHO_PRODUCT_DOSSIER.md line 1261: "plus 404 on the eight single-object operations"

**Problem:** Both documents call the 404-declaring operations "the 8 single-resource operations" or "the eight single-object operations", but the API reference's own taxonomy at lines 258-262 splits the 14 into "Six list endpoints", "Six single-resource getters" and "Two file endpoints". There are six single-resource operations, not eight; the eight that declare 404 are the six getters plus the two file endpoints. Verified against the captured exports: 404 appears in accounts_getaccount, cards_getcard, transactions_gettransaction, statements_getstatement, invoicing_getinvoicingcustomer, invoicing_getinvoicinginvoice, transactions_gettransactionfile and invoicing_getinvoicinginvoicefile.

**Fix:** API reference line 2109: "the 8 single-resource operations add `404`" to "the 6 single-resource getters and the 2 file endpoints add `404`". Dossier line 1261: "the eight single-object operations" to "the six single-object operations and the two file endpoints".

## 67. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 124: "| AP / bill pay | BILL | $49 to $89 per user per month | about $2,844 at $79 x 3 |"

**Problem:** $79 per user per month is not a BILL price. BILL's published AP/AR tiers are Essentials $49, Team $65 and Corporate $89, as the dossier's own line 1476 states and findings/mk-spend-legacy.md lines 47-49 and 513 confirm from BILL's own pricing page. $79 x 3 x 12 = $2,844 computes an annual cost at a rate no customer can buy, and it is the input to the "$10,000 to $11,000 a year" total at line 129.

**Fix:** Use a real tier: "about $2,340 at $65 x 3 (Team)" or "about $3,204 at $89 x 3 (Corporate)". Either keeps line 129's "$10,000 to $11,000 a year" band intact ($10,176 and $11,040 respectively), so only the row needs changing.

## 68. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1481, SAP Concur row: "Real mid-market economics: $9 to $24 per active user/month, $3.50 per invoice document with a $30K minimum, implementation $15K to $350K, 5% to 8% annual escalators"

**Problem:** SAP publishes only the $7/$11-per-report list rates given in the adjacent cell. The "real mid-market economics" numbers come from third-party cost-benchmark sites (costbench.com, atonementlicensing.com, vendorbenchmark.com per findings/mk-spend-legacy.md lines 309-313), not from SAP and not from any primary source, yet they are stated as fact under a column headed "What the price really is." Separately, "$15K to $350K" silently merges two different products: Concur Standard implementation is $15K to $40K and Concur Professional is $80K to $350K.

**Fix:** Replace with: "Third-party cost-benchmark estimates, not SAP figures: $9 to $24 per active user/month, $3.50 per invoice document with a $30K minimum, implementation $15K to $40K (Standard) or $80K to $350K (Professional), 5% to 8% annual escalators."

## 69. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 721: "Of 253 help-center articles, 57 (22.5%) route the reader to Client Service."

**Problem:** 253 is the right denominator for articles, but the dossier says "all 269 help-center articles" at line 15 and "across 269 help-center articles" at line 681, and "269 help pages" at line 2026. The corpus is 269 help-center pages, which findings/helpcenter-ops.md line 16 decomposes as "16 category index pages + 253 articles" (I confirmed 269 files in pages/help/). A reader sees 269 in three places and 253 in one, with no explanation.

**Fix:** Leave line 721 at 253 articles and change the other three. Line 15: "all 269 help-center pages (253 articles plus 16 category indexes)". Line 681: "across the 253 help-center articles". Line 2026: "anywhere in the 269 help-center pages".

## 70. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1615: "At the 0.60% tier a $2M balance pays roughly $12,000 a year, more than a 25-seat Ramp Plus subscription ($4,500) or a 25-seat Brex Premium subscription ($3,600)."

**Problem:** The dossier's own fee tables (lines 395-397 and 853-855) put 0.60% at "Under $2M" and 0.45% at "$2M to $5M", and the same sentence notes the fee is "assessed on checking plus Treasury balances combined." A customer with $2M combined is therefore in the 0.45% band and pays $9,000, not $12,000. $12,000 is only the limit as combined AUM approaches $2M from below. The overstatement is 33%, though the argument survives either way since $9,000 still exceeds $4,500 and $3,600.

**Fix:** Replace with: "A combined balance just under $2M pays close to $12,000 a year at 0.60%, and a $2M balance pays $9,000 at 0.45% - either way more than a 25-seat Ramp Plus subscription ($4,500) or a 25-seat Brex Premium subscription ($3,600)."

## 71. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 1122: "the offers price a customer at roughly 1.0% to 1.25% of a quarter's deposits, paid up front, which annualises to 4% to 6% of the balance"

**Problem:** The arithmetic does not close as written. 1.0% to 1.25% of a quarter annualises to 4% to 5%, not 4% to 6%. The 6% figure only appears on the partner pages whose qualifying window is 60 days rather than 90 (Cowboy Ventures, Unusual Ventures, Eniac, Flybridge, all $4,000 on $400,000 = 1.0% per 60 days = about 6% annualised), which the sentence does not say. The low end is also understated: the Y Combinator alumni and Thiel Fellowship offers are $4,000 on a $500,000 balance, i.e. 0.8% per quarter (findings/segments.md lines 231, 234).

**Fix:** Replace with: "the offers price a customer at roughly 0.8% to 1.25% of the qualifying balance over a 60- or 90-day window, paid up front, which annualises to roughly 3% to 5% on the 90-day pages and about 6% on the 60-day ones".

## 72. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 900: "**Assessment:** the $400 is a conditional charge whose real function is to enforce a 60-day deposit hold, and Rho books revenue on every customer who fails either half of the test"

**Problem:** Two loaded moves where neutral phrasing carries the same fact. "Whose real function is" asserts an intent no cited evidence establishes. "Deposit hold" is wrong as a description of the mechanism: nothing is held, restricted or escrowed; the customer keeps full access and must simply maintain a daily average balance $10,000 above the starting balance. The same document treats the same fee fairly at line 667, where 3.12 calls $400 including filing fees and year-one agent "the cheapest headline price in its set" against Stripe Atlas $500 and Clerky $427 to $819.

**Fix:** Replace with: "**Assessment:** the $400 is a conditional charge. It is credited back only if the customer deposits $10,000 of genuinely new money and keeps the daily average $10,000 above the starting balance for 60 days, so customers who miss either half pay it. The rebate condition is a deposit test, not a price."

## 73. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1623: "Separately, four versus pages (Amex, BILL, HSBC, SVB) upgrade the claim to \"a dedicated human account manager to every client\""

**Problem:** The page list is wrong in both directions. pages/core/versus__svb.txt contains zero occurrences of the string "account manager." pages/core/versus__chase.txt contains three, including the quoted phrase verbatim at line 186 ("Rho provides a dedicated human account manager to every client"). pages/core/versus__bill.txt does not use the quoted phrase; it says "Every Rho client has a direct line to a human account manager" (line 195). The correction matters beyond bookkeeping: Chase is one of the five pages the document holds up at line 1663 as the "Rewritten Aug 2026" candid generation, so the overstatement is not confined to the untouched pages.

**Fix:** Replace with: "Separately, the Amex, Chase and HSBC versus pages upgrade the claim to 'a dedicated human account manager to every client' and the BILL page to 'a direct line to a human account manager', which Rho's more carefully sourced pages contradict by reserving named account managers for growth-stage and qualifying clients. Note that Chase is one of the five rewritten pages, so the overstatement is not limited to the untouched generation."

## 74. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 234: "**What is conspicuously absent from the map.** Rho never names a card issuer processor, a core ledger provider, or a payments processor for ACH and wires. Those layers exist in every fintech of this shape, and Rho discloses none of them."

**Problem:** A universal industry practice framed as a Rho-specific concealment. "Conspicuously absent" implies something is being withheld that peers disclose, but no vendor in the comparison set (Mercury, Brex, Ramp, Bluevine, Relay, Novo) publicly names its issuer processor or ACH processor either, and the document cites no competitor that does. The "core ledger provider" row may not even exist: the document itself reports at line 1833 that Rho states it built a "proprietary core" and integrates directly with Webster rather than through middleware, which it then treats as a credible and favourable structural fact at line 1835.

**Fix:** Replace with: "**What the map cannot show.** Rho names no card issuer processor and no payments processor for ACH and wires. Neither does any competitor in this set: the regulated edges of the stack are disclosed because law requires it, and the middle is disclosed nowhere in the category. Rho separately claims it built its own core ledger rather than renting one (see 9.3), which if true removes one layer other programs carry."

## 75. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Section 6 in full (lines 1182 to 1335); the only credit for the API data model appears at line 1693, inside section 8.2 "Differentiation that is thinner than claimed"

**Problem:** The brief's "good API data model" is the one named strength that is genuinely buried. Section 6, the executive view of the developer surface that the document says is designed "to leave you with an accurate picture" for readers who never open the companion reference, never mentions it: 6.2 lists the surface, 6.3 covers credentials, 6.4 flags the plaintext-token snippet, 6.5 the unenforced rate limits, 6.6 the capability boundary, 6.9 the costs, and only 6.8 is positive and it is about read-only rather than the data model. The credit finally lands at 8.2, inside a section whose title tells the reader the item is overclaimed, and it is closed out four words later with "It is still a feed." A reader who stops at section 6 will not learn that the money object uses integer minor units and ISO 4217, that legs are grouped by money_movement_id, that NACHA traces and IMAD/OMAD identifiers are exposed, or that tool names are pinned to frozen v1 operationIds, a commitment the document itself notes at line 1581 that "almost nobody else makes."

**Fix:** Add a short paragraph at the end of 6.2 or as a new 6.6 lead-in: "What the surface does well. Money is returned as an object with integer minor units and an ISO 4217 currency rather than a float, transaction legs are grouped under a money_movement_id, ACH NACHA traces and wire IMAD/OMAD identifiers are exposed, user and card attributions are present on every transaction, and MCP tool names are pinned to the frozen v1 operation identifiers so saved agent workflows do not break on a release. That is a better-modelled feed than most bank aggregators produce, and it is the part of this surface a reader should not discount for the verbs it lacks."

## 76. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 31: "Regulation Z at 12 C.F.R. 1026.12(b)(5)"; line 528: "implementing TILA section 135"

**Problem:** C.F.R. (7 uses) is never expanded. TILA is used at line 528 and only expanded at line 1862, 1,334 lines later, and even then only inside a quotation from Brex's card agreement rather than in the document's own voice. Both appear in the front-matter example at line 31 that the document uses to demonstrate its own method.

**Fix:** At line 31 write "Regulation Z at 12 C.F.R. 1026.12(b)(5) (the Code of Federal Regulations, where federal agency rules are published)". At line 528 write "implementing TILA (the Truth in Lending Act) section 135".

## 77. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 629: "No interest rate, APR, factor rate, or price range for Rho Capital is published"; line 1377: "Up to 4.44% YTM as of 09/03/2026"

**Problem:** Three pricing terms undefined. APR (3 uses) is never expanded. "Factor rate" is a specific merchant-cash-advance pricing form the reader will not know. YTM appears exactly once, at line 1377, in the head-to-head yield row against Ramp, where the reader is being asked to compare 4.44% YTM against 4.66% net on a different basis.

**Fix:** At line 629 write "No interest rate, APR (annual percentage rate, the all-in yearly cost of borrowing), factor rate (a flat multiple of the amount borrowed, used by cash-advance lenders instead of an interest rate), or price range..." At line 1377 write "Up to 4.44% YTM (yield to maturity, the return if the holdings are kept to the end of their term)".

## 78. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 739: "for a company with sub-$1M-ARR customers"; line 769: "| SAFE note generator | Yes, free tool |"; line 759: "card + QBO sync August 31, 2026"

**Problem:** Three startup-world abbreviations used once each and never expanded: ARR, SAFE and QBO. QBO is especially avoidable, since the document writes "QuickBooks Online" in full at least a dozen times and then abbreviates once, at line 759, with no link between the two.

**Fix:** Line 739: "for a company whose customers are below $1M of ARR (annual recurring revenue)". Line 769: "| SAFE note generator (a SAFE is the standard one-page contract early startups use to take investment before setting a valuation) |". Line 759: replace "QBO" with "QuickBooks Online".

## 79. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 360: "which IntraFi's ICS and CDARS do not offer at all"; repeated at lines 1539 and 1808

**Problem:** ICS (5 uses) and CDARS (2 uses) are the named benchmark programs against which Rho's savings sweep is judged in section 3.2, section 7.6 and section 9.2, and neither is ever expanded or explained. The reader is asked to accept "ADM is weaker than IntraFi" without being told what IntraFi's products are.

**Fix:** At line 360 write "which IntraFi's ICS and CDARS (the two dominant bank-run deposit sweep programs, Insured Cash Sweep for checking-style balances and CDARS for certificates of deposit) do not offer at all".

## 80. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1088: "Excludes a visible DTC category"; line 1151: "DTC and CPG consumer brands"; line 1093: "staffing and PEO firms"; line 1483: "quoted inside a Paylocity HCM deal"; line 1560: "| **Navan** | T&E |"

**Problem:** Five business-category abbreviations used without expansion: DTC (2 uses), CPG (1), PEO (1), HCM (2), T&E (2). DTC and CPG together describe the one vertical the document identifies as Rho's best-evidenced customer segment, so they are not incidental.

**Fix:** Line 1088: "Excludes a visible direct-to-consumer (DTC) category". Line 1151: "DTC and consumer packaged goods (CPG) brands". Line 1093: "staffing and PEO firms (professional employer organizations, which employ staff on a client's behalf)". Line 1483: "inside a Paylocity HCM (human capital management, meaning payroll and HR software) deal". Line 1560: "| **Navan** | Travel and expense (T&E) |".

## 81. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1745: "No G2, Trustpilot or NPS figure appears anywhere"; line 1749: "no ISO 27001 and no PCI DSS attestation"

**Problem:** Four undefined items in the table and paragraph assessing what Rho is missing versus its cohort. G2 (2 uses), NPS (1), ISO 27001 (1) and PCI DSS (1) are each presented as a gap without the reader being told what the thing is, so the gap cannot be weighed.

**Fix:** Line 1745: "No score on G2 or Trustpilot (the two public software review sites buyers check) and no NPS (net promoter score, the standard customer-satisfaction metric)". Line 1749: "no ISO 27001 (the international information-security certification) and no PCI DSS attestation (the card industry's security standard for anyone handling card numbers)".

## 82. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 232: "$2.76B in assets at the 06/30/2026 FDIC call report"; line 240: "a money transmitter license in each state"; line 277: "a venture debt business development company"

**Problem:** Three regulatory-structure terms used as evidence in section 2 with no explanation. "Call report" (3 uses) is the source of the bank-size comparison at 232 and again at 1900. "Money transmitter license" (4 uses) is one of the four licenses the document says Rho rented. "Business development company" (2 uses) is what makes the Trinity Capital disclosure discoverable at all, and is cited again at line 2009 as a research route.

**Fix:** Line 232: "at the FDIC call report of 06/30/2026 (the quarterly financial return every US bank must file publicly)". Line 240: "a money transmitter license in each state (the licence a non-bank needs to move other people's money, granted state by state)". Line 277: "a business development company (a publicly listed fund that lends to private companies and must itemise every position in its SEC filings)".

## 83. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1184: "the pagination cursor rules, the error contract"; line 1197: "the OpenAPI specification is published"; line 1235: "JSON-RPC messages... parity is one-to-one with REST"; line 1257: "use exponential backoff"; line 1287: "no mention of prompt injection"; line 2053: "rate-limit headers, ETags"

**Problem:** Section 6 defines GET, scope, PKCE, webhook, idempotency, dynamic client registration and Streamable HTTP, then leaves six sibling terms cold: cursor pagination, OpenAPI, JSON-RPC, REST, exponential backoff, prompt injection and ETags. Prompt injection matters most: line 1287 is the document's only security warning about agent use, and it names the attack without describing it.

**Fix:** Line 1184: "the cursor pagination rules (how you page through a long list without missing or repeating rows)". Line 1197: "the OpenAPI specification (the machine-readable file describing every endpoint, which code generators read)". Line 1235: "JSON-RPC messages (a simple request-and-reply message format)... parity is one-to-one with REST (the ordinary web API the same endpoints serve)". Line 1257: "use exponential backoff (wait, then wait twice as long, and so on)". Line 1287: "...contains no mention of prompt injection (an attacker writing instructions into a field such as a payment memo, in the hope the AI reading it treats them as commands) or untrusted-content handling."

## 84. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1453: "goes into FDIC receivership" and "behind a trustee, an automatic stay, and professional fees"; line 1870: "waives subrogation and notice"; line 1886: "| Setoff (Addendum B 2.3) |"; line 1900: "a parent-group pro forma figure"; line 1902: "contract continuity, repapering, program-manager agreement renewal"; line 2013: "Form ADV Part 2A wrap-fee brochure"

**Problem:** Six legal and finance terms used without explanation in the risk and diligence sections, which is where a newcomer is most dependent on the text: receivership, automatic stay, subrogation, setoff, pro forma and repapering. "Repapering" in particular is industry slang with no plain-English equivalent given, in the sentence explaining what the Santander acquisition might do to Rho customers.

**Fix:** Line 1453: "goes into FDIC receivership (the FDIC takes the bank over and pays the insured depositors)... behind a trustee, an automatic stay (a court order freezing all claims while the bankruptcy runs), and professional fees". Line 1870: "waives subrogation (the right to step into Rho's shoes and chase the affiliate for what you paid) and notice". Line 1886: "Setoff (Rho's right to seize money in your accounts to cover what you owe it)". Line 1900: "a parent-group pro forma figure (the combined group as if the merger had always been in place), not Webster's". Line 1902: "contract continuity, repapering (re-signing the existing agreements under the new owner's name), program-manager agreement renewal". Line 2013: "Form ADV Part 2A wrap-fee brochure (the plain-English disclosure document an adviser must give clients)".

## 85. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 799: "prices World Elite at 2.60% + $0.10 on the standard Merit I retail program. Commercial rates vary materially by merchant category, data level and ticket size... the network takes assessments, and in a sponsor-bank arrangement the bank... takes a share before anything reaches the program manager."

**Problem:** One sentence carries five undefined card-industry terms: Merit I, data level, ticket size, assessments and program manager. This is the Verified paragraph underpinning the entire interchange revenue estimate in section 4.2, which the document itself calls one of the two lines that carry the business. "Program manager" is especially load-bearing because it is the role Rho actually occupies and the term is never connected to Rho by name.

**Fix:** Rewrite as: "...prices World Elite at 2.60% + $0.10 on Merit I, the baseline retail category. Commercial rates vary materially by the type of merchant, by how much purchase detail the merchant transmits, and by the size of the individual purchase, so 2.60% is a ceiling reference rather than a blended average. The issuer does not keep all of it: the network takes its own cut (called assessments), and in a sponsor-bank arrangement the bank (Webster, now inside Santander) takes a share before anything reaches the program manager, which is the role Rho itself plays."

## 86. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 336: "quasi-cash and money services"; line 599: "payment terms (Net 30, Due on receipt)"; line 639: "It learns from your chart of accounts"; line 651: "Delaware C-corporation formation"; line 655: "year-one registered agent service"; line 810: "are all breakage mechanisms"; line 869: "the mid-market rate Wise itself quotes"

**Problem:** Seven product-level terms a newcomer will not know, each used at a point where it changes the reader's understanding. "Breakage" is the key word in the assessment of whether Rho's 2% cashback is real. "Mid-market rate" is the entire basis of the claim that Rho's total FX take is not computable. "Chart of accounts" is the input to Rho Close. "Registered agent" and "C-corporation" are what the $400 incorporation fee buys.

**Fix:** Line 336: "quasi-cash (anything that converts straight back into cash, such as money orders or casino chips) and money services". Line 599: "payment terms (Net 30, meaning due 30 days after the invoice date; or Due on receipt)". Line 639: "your chart of accounts (the list of categories a company books every transaction into)". Line 651: "Delaware C-corporation formation (the standard US company type that venture investors expect)". Line 655: "year-one registered agent service (the in-state address legally required to receive official mail for the company)". Line 810: "are all breakage mechanisms, breakage being the industry word for rewards that are earned but never actually claimed". Line 869: "the mid-market rate (the true interbank exchange rate, before anyone's margin) that Wise itself quotes".

## 87. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 200: "CRD 314581, SEC file number 801-125841"; line 482: "US checks only, with 9-digit ABA routing numbers"; line 88: "Interactive Brokers LLC" and line 336 "A registered LLC or corporation"; line 291: "Captured 2026-09-11 19:13:30 ET"; line 435: "just after midnight EST"; line 1478: "per its S-1"; line 2034: "Forge's $131.01M total"

**Problem:** A tail of one-off identifiers and abbreviations that are never expanded: CRD (5 uses, the number the reader is told to look up each March at line 2040), ABA (1 use), LLC (25 uses, never once expanded as limited liability company despite being an eligibility criterion), ET and EST (25 and 2 uses, never expanded and used inconsistently in the same cutoff tables), S-1 (1 use), and Forge (1 use, cited as a source contradicting the SEC record by $26M with no indication of what Forge is).

**Fix:** Line 200: "CRD 314581 (the Central Registration Depository number, the public identifier for a registered adviser)". Line 482: "9-digit ABA routing numbers (the bank identifier printed on every US check)". Line 336: "A registered LLC (limited liability company) or corporation". Standardise ET and EST to "ET (US Eastern time)" on first use at line 291 and use ET throughout, since line 435's EST contradicts the ET used elsewhere in the same tables. Line 1478: "per its S-1 (the registration document a company files with the SEC before going public)". Line 2034: "Forge (a marketplace for shares in private companies, whose figures are not filings)".

## 88. [MINOR] RHO_API_REFERENCE.md
**Locator:** line 5985 (section 6.5, The short version): "Deprecation notice is 15 days with no machine-readable channel, so monitor for schema drift yourself"

**Problem:** The one-line summary table drops the qualifier that the document itself uses correctly everywhere else and that the claim register explicitly flags. Lines 111, 113, 5888 and 5929 all say "at least 15 days' notice", which is Rho's actual wording and is a floor. VERIFIED.md's api-contract entry calls this out by name: "Precision error: the versioning guide says 'at least 15 days' notice', a floor. 'Only 15 days of deprecation notice' is defensible as a criticism of the floor but misquotes the policy as a fixed figure." Section 6.5 is the row an integrator is most likely to skim and copy into a design doc, so the misquote is the version that will travel.

**Fix:** Change to: "Deprecation notice is at least 15 days, a floor with no stated ceiling and no machine-readable channel, so monitor for schema drift yourself".

## 89. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** line 16: "**The complete developer documentation** at docs.rho.co: 13 guides and 14 API operation references." versus line 2102: "| docs.rho.co guide pages | 14 |"

**Problem:** The document contradicts itself on the size of its own corpus, in the two places that exist specifically to let the reader audit the corpus. The docs/ capture on disk holds 14 files: 12 docs_v1_*.md guides plus index.html.md plus api_v1_openapi.md. So the guide count is 13 (12 guides plus the index) and the OpenAPI document is separate, which is exactly how the next table row already states it ("API operation references | 14, plus the OpenAPI document"). The table row therefore double-counts the OpenAPI document. RHO_API_REFERENCE.md line 21 uses the correct "13 guides and 14 operation references".

**Fix:** Change line 2102 from "| docs.rho.co guide pages | 14 |" to "| docs.rho.co guide pages | 13 (12 guides plus the docs index) |".

## 90. [MINOR] RHO_API_REFERENCE.md
**Locator:** lines 1-7, the header block ending "It is what the official docs say, plus what the API actually does when you call it, plus the places where those two disagree."

**Problem:** The linkage between the two delivered documents is one-way. The dossier points forward to the API reference twice (lines 68 and 189, "A companion document, `RHO_API_REFERENCE.md`, covers the developer surface in full detail"), but grepping RHO_API_REFERENCE.md for "RHO_PRODUCT_DOSSIER" or "companion" returns zero hits. A reader who opens the API reference first, or who is handed only that file, gets no pointer to the product, business-model, eligibility and risk context that the API reference repeatedly assumes (it references Rho's read-only posture, the roadmap blog, scope policy and competitor agent surfaces without ever saying where the fuller treatment lives).

**Fix:** Add after line 7: "A companion document, `RHO_PRODUCT_DOSSIER.md`, covers the product, the business model, eligibility, the risk picture and the 2026 competitive landscape. Its section 6 is a summary of this document; read it first if you are evaluating Rho rather than integrating with it."

## 91. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Nine quotations where an em or en dash in Rho's copy was replaced inside the quotation marks. Line 717: "When you contact Rho support, you reach a real human, 24/7, on every account, at no cost." Line 774: "...$0 domestic wires, the only standard payment fee is 1%..." Line 709: "...purchase confirmations, nothing else is read, stored, or touched" Line 95: "Receipts, approvals, and coding, automatic" Line 516: "It isn't a paid plan, there's no subscription fee." Line 1619: "24/7 human support (phone, chat, SMS), every account, every tier"

**Problem:** Each of these is presented as verbatim Rho copy but has had a dash silently converted to a comma. Sources: /help-center "you reach a real human — 24/7, on every account, at no cost"; site-llms.txt "$0 domestic wires — the only standard payment fee"; /connectors/gmail "purchase confirmations — nothing else is read, stored, or touched"; /integrations/netsuite "Receipts, approvals, and coding — automatic"; /help-center rho-platinum "It isn't a paid plan — there's no subscription fee"; /versus/svb "24/7 human support (phone, chat, SMS) — every account, every tier". The same substitution hits two API-reference quotes that are explicitly labelled verbatim: line 575 renders /docs/v1/partner-auth's "you don't need OAuth - use an API Access Token instead" as "you don't need OAuth, use an API Access Token instead", and line 581 renders /docs/v1/auth's "scoped to a single business - the same token continues to work" as "scoped to a single business, the same token continues". Individually trivial; collectively they mean no quotation in either document can be pasted into a search box and found, which is the first thing a sceptical reader will try.

**Fix:** Restore the source punctuation inside every pair of quotation marks. The house style rule against dashes governs the documents' own prose, not material reproduced between quotation marks; where a dash is genuinely unwanted, paraphrase outside the quotes instead of editing inside them.

## 92. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 152: "around $20 to $45" versus line 492, line 914 and line 2010: "around $20 - $45"

**Problem:** The same quotation is rendered three different ways in one document, and none matches the source. help-center/payments/fees-for-recalls-failed-wires reads "a fee of around $20 – $45" with an en dash. Line 152 replaces the dash with the word "to" inside the quotation marks, which is an inserted word rather than a punctuation change; lines 492, 914 and 2010 use a hyphen. A reader comparing the fee table at line 914 with the summary at line 152 will see two different quoted figures for one fee.

**Fix:** Use "around $20 – $45" at all four locations, matching the help-center article exactly.

## 93. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 7034, table cell: "Rho's own product page: \"Tokens cannot initiate payments or modify accounts. The Rho API is read-only today.\""

**Problem:** Two non-adjacent fragments spliced into one quotation with no ellipsis. /product/api line 43 reads: "Rho API access tokens are read-only and scoped to account and transaction data. Tokens cannot initiate payments or modify accounts, and can be revoked at any time. The Rho API is read-only today." The document deletes ", and can be revoked at any time" from the middle of a sentence and closes it with a period, so the two quoted sentences read as consecutive when they are not. The dossier quotes the same passage correctly at line 1177, with an ellipsis, which makes the API reference version look like an error rather than a convention.

**Fix:** Match the dossier's rendering: "Tokens cannot initiate payments or modify accounts... The Rho API is read-only today."

## 94. [MINOR] RHO_API_REFERENCE.md
**Locator:** Line 592: "The help center (`Build a custom integration with Rho`) describes the same flow as: \"Navigate to Settings, then API, then Access Tokens\" / \"Create a new access token\" / \"Choose the appropriate permissions and complete two-factor authentication.\""

**Problem:** The first of the three quoted steps is altered. help-center/the-rho-api/build-a-custom-integration-with-rho line 60 reads "Navigate to Settings → API → Access Tokens ." - the arrows were replaced with the word "then" inside the quotation marks. The second and third steps are verbatim and correct. Two lines later, at line 594, the same document quotes the same sentence correctly as "Settings → API → Access Tokens", so the page now presents two different verbatim renderings of one sentence, in a passage whose entire point is that Rho describes this path four different ways.

**Fix:** Restore the arrows in the line 592 quotation: "Navigate to Settings → API → Access Tokens".

## 95. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1833: "Its security blog states that it chose direct integration with Webster over Banking-as-a-Service middleware: \"While BaaS middleware offers a faster path to market...\" and that it built a \"proprietary core\" to integrate with Webster's systems."

**Problem:** The second quotation is attributed to the wrong page. The BaaS sentence is verbatim on /blog/security-by-design (captured as pages/extra/blog__security-by-design.txt line 79) and correctly attributed. "proprietary core" appears nowhere on that page; its only occurrence in the corpus is /blog/rho-and-webster-bank (pages/extra/blog__rho-and-webster-bank.txt line 51: "we began building out our proprietary core needed to integrate with Webster Bank... systems"). The sentence structure attaches both quotes to "Its security blog states".

**Fix:** Split the attribution: "...and a separate post, Why we partnered with Webster Bank, says Rho \"began building out our proprietary core needed to integrate with Webster Bank... systems.\""

## 96. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 709: "It may need \"Permission from your Gmail admin if your organization restricts third-party app access.\""

**Problem:** The quotation is truncated at a point that drops a scoping qualifier, and is closed with a period as though complete. help-center/expenses/how-to-set-up-the-gmail-connector line 56 reads in full: "Permission from your Gmail admin if your organization restricts third-party app access (Google Workspace customers only)". As quoted, the admin-permission requirement reads as applying to anyone connecting a personal Gmail account; Rho scopes it to Google Workspace customers.

**Fix:** Quote the full bullet: "Permission from your Gmail admin if your organization restricts third-party app access (Google Workspace customers only)."

## 97. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 232: "Two of Rho's own comparison posts put it without ambiguity: \"Rho Capital lines are issued by Lead Bank and serviced by Slope.\""

**Problem:** The quotation is cut at a semicolon and closed with a period, dropping a clause that the dossier itself treats as material elsewhere. Both source pages (/blog/brex-vs-mercury line 233 and /blog/ramp-vs-mercury line 239) read: "Rho Capital lines are issued by Lead Bank and serviced by Slope; a personal guaranty may be required." Section 3 at line 625 separately flags "Personal Guaranty may be required" as appearing only in the lender's disclaimer, and the dropped clause is direct evidence that Rho states it in its own body copy too.

**Fix:** Quote the full sentence: "Rho Capital lines are issued by Lead Bank and serviced by Slope; a personal guaranty may be required."

## 98. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 2008, table row: "Rho's own wording is that rates \"are shown during your application\" | A live application at rho.co/product/capital, which is the only disclosure channel Rho names"

**Problem:** Two small errors in one cell. The quoted words are not verbatim: /blog/rho-capital line 108 reads "Rates are based on your business's cash flow and shown during your application — no warrants, no dilution", so "are shown" is an inserted word where the source has "and shown". And the row names /product/capital as "the only disclosure channel Rho names" while the sentence it quotes is on /blog/rho-capital; /product/capital contains no equivalent statement about when rates are shown.

**Fix:** Replace with: "Rho's own wording, on /blog/rho-capital, is that rates are \"based on your business's cash flow and shown during your application\"" and change the remedy column to name /blog/rho-capital as the page that makes the promise.

## 99. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 1227: "**Verified:** Rho's OAuth server returns \"Dynamic registration is not enabled\" on `POST /oauth2/register`". Same present-tense assertion at line 1736 and line 2051

**Problem:** The two delivered documents disagree about the provenance of this quoted string. The dossier presents it three times as a present-tense live response under the "Verified" label, which the document defines at line 41 as "Checked against a primary source outside Rho's control, or a live HTTP response". The companion API reference, at line 1078, discloses the opposite: "(Recorded in the earlier probe pass; not re-sent here, because a `POST` to a production authorization server is a write-shaped request rather than a metadata read.)" The re-verified evidence is the absence of a `registration_endpoint` from auth.rho.co's metadata, not the error string. A reader who reads both documents will catch this.

**Fix:** At line 1227 replace with: "**Verified:** auth.rho.co's authorization-server metadata publishes no `registration_endpoint`, which under RFC 8414 is how a server declares that dynamic client registration is unsupported; a registration attempt recorded in an earlier probe pass returned \"Dynamic registration is not enabled\"." Add the same hedge at lines 1736 and 2051, or drop the quoted string there and cite the missing endpoint only.

## 100. [MINOR] RHO_PRODUCT_DOSSIER.md
**Locator:** Line 653: "A questionnaire ... that \"most founders finish in about 5 minutes\""; line 387: "Approval \"typically up to 2 business days.\""; line 488: international wire cancellation \"is most effective if the request comes within the same business day.\"

**Problem:** Three quotations drop words from the middle or end of a source sentence without marking the elision. help-center/general-rho-information/incorporating-your-company-with-rho line 44 reads "Most founders finish the flow in about 5 minutes" (the words "the flow" are deleted). help-center/treasury/understanding-rho-treasury line 91 reads "approval typically takes up to 2 business days" ("takes" is deleted, leaving an ungrammatical quotation). help-center/payments/how-to-cancel-reverse-or-dispute-a-bank-transfer line 42 reads "Cancelations are most effective if the request comes within the same business day the funds are initiated" (the sentence is cut mid-clause and closed with a period). None changes the meaning, but all three fail a verbatim check.

**Fix:** Line 653: "most founders finish the flow in about 5 minutes". Line 387: Approval "typically takes up to 2 business days". Line 488: "most effective if the request comes within the same business day the funds are initiated".
