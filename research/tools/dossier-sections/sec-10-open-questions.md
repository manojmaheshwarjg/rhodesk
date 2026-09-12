## 10. Open questions and how to keep this document current

Everything above was written from public sources, a free sandbox, and SEC filings. That combination has a hard edge. This section says where the edge is, which facts will move first, how the document was actually assembled, and how to re-run it.

### 10.1 What this research could not settle

Four groups. For each question: why it stayed open, and the single cheapest place the answer actually lives.

#### Pricing and economics

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| What Rho Capital (its revolving credit line) actually costs | No rate, APR, factor rate or price range is published on any Rho page. Four Capital-related URLs missing from the local crawl were fetched live on 2026-09-11 and none prices it. Rho's own wording, on /blog/rho-capital, is that rates are "based on your business's cash flow and shown during your application" | A live application from a Rho account, which is the channel /blog/rho-capital names, or the resulting Slope / Lead Bank credit agreement, which /product/capital names as where "your exact pricing is disclosed" |
| Rho's revenue, deposit balance and unit economics | Never disclosed and never estimated by a credible third party. Interchange (the fee a card network routes to the card issuer on every swipe) is an inference about Rho's revenue, not a corpus disclosure: the word never appears in connection with Rho anywhere in 556 captured pages | Nothing public. Rho is private with no filing obligation. The nearest proxy is Trinity Capital's schedule of investments (a business development company must itemize its portfolio positions in its 10-K and 10-Q), which would give the size, rate and maturity of the 2024 debt facility |
| Whether a returned domestic wire costs $0 or $20 to $45 | rho.co/pricing line 07 says "Domestic wire recall fee $0". One help-center article says "a fee of around $20 - $45 will be deducted" for failed and returned domestic wires. Both are live | A support ticket, or a real returned wire on a funded account |
| What "platform access after year one is $1,000 annually" buys at Rho Incorporation | The sentence appears exactly once, on one page, and the corpus never defines what platform access covers or whether it is a registered-agent renewal | A sales call or the incorporation engagement letter |
| The real qualification gate for the Monthly Terms card | Three live Rho numbers: $25,000 minimum cash balance (help center), $75,000 combined across Rho and linked external accounts (product page and FAQ), and "balances reach $15,000" (/product/corporate-cards) | A live card application, or a sales call |
| Whether a 100% Vanguard (VFSTX) Treasury allocation can actually be selected | The 4.66% headline assumes it; the product rules cap the short-term bond fund at 50%; the help center says pre-existing allocations above 50% are grandfathered and a higher limit "can be approved". The allocation UI was never observed | A funded Treasury account (the $50,000 minimum), or RBB Treasury's Form ADV Part 2A wrap-fee brochure, which Rho links but does not host |

#### Product mechanics

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| Rho's MCP tool names, count and schemas | Not published anywhere. The docs promise the names never change but never print one. The sandbox host has no MCP endpoint (404), so MCP exists only in production | Connecting a client with a live production token and listing the tools. This is the largest single gap in this document |
| Whether `cards:read` and `invoicing:read` are actually grantable | The public OAuth metadata enumerates five scopes; the Authentication guide's scope table lists three. Either the docs lag the product or the metadata is ahead of it | The OAuth consent screen on a real account |
| Whether MCP calls share the 60-requests-per-minute token budget | Never stated. No rate-limit response headers exist to measure it against | A production token and a load test, or Rho support |
| Which payment rails Bill Pay really uses | The product page is written as check-only ("pay by check", "$0 On domestic check payments"). The help center lists ACH, domestic and international wires, checks and single-use cards. A separate help-center vendors article says the Bill Pay workflow "does not currently support Vendor Cards". Three Rho sources, three answers | A live Bill Pay draft on a funded account |
| Rho's international AP coverage | Wise US Inc. is named as the provider, but the country, currency and payment-method counts are unpublished. This is the largest unfilled gap against Tipalti and Corpay | A sales call, or the product itself |
| Which savings withdrawal schedule governs | The published American Deposit Management agreement says requests process Tuesdays and Thursdays for Wednesday and Friday settlement, capped at six per month. Rho's help center says savings-to-checking "typically settles the next business day". Rho's settlement-times page says two business days | A funded savings account, or support |
| Which banks are in the $75M sweep network | "The current list of network institutions is available from Rho support on request." It matters because FDIC insurance (the federal government's per-depositor, per-bank deposit guarantee, $250,000) aggregates across accounts at the same bank, so an existing relationship with a network bank silently erodes coverage | A support request for the Program Institution list and ADM Schedule A |
| Whether Departments is being migrated to Fields | Newer accounts get Fields and have no Reporting tab; older accounts have Departments. No migration, deprecation or sunset notice exists anywhere in 269 help pages | A support ticket, or accounts on both cohorts |
| What happens on day 31 or day 61 of a pre-EIN window with no EIN | Stated nowhere in the corpus | A support ticket |
| SOC 2 scope, auditor, report period and exceptions | The auditor is never named, the Trust Services Criteria in scope are never stated, and the Trust Center is not in rho.co's sitemap | Requesting the report through Rho's Trust Center link |

#### Corporate and financial

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| Whether Rho raised equity after 2021 | Form D (the notice a company files with the SEC when it sells securities under the Regulation D private-placement exemption) is required only for Reg D offerings. A round sold under Section 4(a)(2) or offshore under Regulation S generates no filing. Rho's filing entity, Under Technologies, Inc. (CIK 0001756460), has filed five Form Ds totaling $104,732,452 and nothing of any type since 2022-01-21. Forge's $131.01M total implies a roughly $26M gap worth chasing | EDGAR is already exhausted. Secondary-market trackers, a Rho announcement, or a new Form D |
| Rho's current board and executive team | Disclosure stops at the January 2022 Form D. Whether Alex Wheldon has formally left and whether Sebastjan Trepca is still CTO are both unresolved | Company announcement, LinkedIn, or press |
| When and why the Evolve Bank & Trust relationship ended, and whether deposits moved | Nothing found in any source | Rho or Evolve directly |
| Whether Santander will continue the Webster sponsor-bank program | Rho's entire deposit story runs through Webster Bank, now a division of Santander Bank, N.A., following a transaction that closed roughly three weeks before this corpus was captured. No public statement either way on program continuity | Santander investor relations, or the Webster Deposit Account Agreement, which Rho incorporates by reference but does not publish |
| Rho's deposit base | "$4B+ in deposits" and "$4 billion moving monthly" are marketing figures. The only auditable number is Rho Treasury's regulatory assets under management, a different quantity entirely | The next Form ADV annual amendment (the disclosure form a registered investment adviser files with the SEC), CRD 314581, filed each March |
| Terms of the Trinity Capital 2024 facility | Trinity lists "Rho Business Banking" with "Year Invested: 2024" and discloses neither structure nor amount on that page | Trinity Capital's 10-K or 10-Q schedule of investments |
| Whether Mercury's bank charter becomes final | The OCC granted preliminary conditional approval on 2026-04-24. Final authorization to open, FDIC deposit insurance and Federal Reserve approvals were all still outstanding as of 2026-09-11 | The OCC Corporate Applications Search tool, which replaced the OCC Weekly Bulletin on 2025-12-19 |
| Whether Ramp's reported $60B round closed | PYMNTS reported early talks on 2026-09-08. $44B (Series F, closed 2026-06-04) is the last closed mark | Ramp's newsroom or a PR Newswire release |
| Reddit and practitioner sentiment on Rho | Never sampled. It is the most likely place to find unvarnished founder experience, and its absence is a real hole in the customer-evidence picture | r/startups, r/smallbusiness, r/ycombinator |

#### API and agent roadmap

Rho says, in the changelog dated 2026-08-03: "Read-only is live today. Write access and webhooks are next." And in the launch blog dated 2026-07-29: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval." No date accompanies either.

| Question | Why it could not be settled | Where the answer comes from |
| --- | --- | --- |
| When write endpoints ship, and whether they land inside `v1` | Rho's versioning policy makes new operations "additive" and therefore non-breaking, so write tools could appear in `/mcp/v1` with no version bump. The 15-day notice floor covers deprecations, not capability additions | Watch the OAuth protected-resource metadata for a non-`:read` scope. That is the earliest public signal and it needs no account |
| Whether dynamic client registration will be enabled | `POST https://auth.rho.co/oauth2/register` returns "Dynamic registration is not enabled", so third-party MCP clients cannot self-register and every integration is a hand-registered partner | Re-test the endpoint; or ask Rho |
| Whether an MCP sandbox is planned | The sandbox host 404s on `/mcp/v1` and the docs never mention it | Rho support or a changelog entry |
| Whether webhooks, idempotency keys, rate-limit headers, ETags, an audit-log surface or a users endpoint are on the roadmap | None exist. Rho has committed publicly only to write access and webhooks | Changelog and docs diffs |
| Whether an MCP call counts as activity against the 45-day token inactivity clock | Never stated | Rho support |
| What production returns that the sandbox never shows | The sandbox dataset exercises 22 of 33 transaction types, 5 of 11 card statuses and 3 of 7 spending-limit types, including none of the treasury transaction family | A production token |

**Assessment:** the open questions cluster in a revealing pattern. Almost everything unanswered is either behind a sales conversation, behind a funded account, or on a roadmap Rho has announced but not dated. Very little is genuinely unknowable. A reader with a Rho account and one sales call could close roughly two-thirds of this list in a week.

### 10.2 Facts with the shortest shelf life

Every row here was true on the as-of date given. Rows are ordered roughly by how fast they decay.

**Rho**

| Fact | Value | As of | Re-check at |
| --- | --- | --- | --- |
| Treasury headline net yield | "up to 4.66%" ($20M+ tier, 0.15% fee) | 2026-09-11 (the page hero was stamped 09/12/2026 and the footnote 09/11/2026 on the same capture) | rho.co/treasury-yield-comparison. Updates daily and automatically |
| Component fund net yields | VFSTX 4.66%, MULSX 3.70% at the top tier | 2026-09-11 | rho.co/product/treasury tier matrix |
| 13-week T-Bill benchmark on Rho's comparison table | 3.81% | 2026-09-11 | rho.co/treasury-yield-comparison |
| Business Savings rate | "up to 1.00% APY (variable)" on a $25,000 average monthly balance | August 2026 | rho.co/product/business-savings-account |
| Partner microsite offers | 77 pages; 25 gate at $400K to $500K, 11 at $100K to $300K, 25 at $50K or less, 16 with no balance test | 2026-09-11 | rho.co/sitemap.xml plus each page. Every partner page says the offer "may be changed or discontinued at any time without notice" |
| API surface | 14 operations, all GET, across 5 resources; 5 scopes, all `:read` | 2026-09-11 | docs.rho.co/api/v1/openapi.md and rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1 |
| Write endpoints and webhooks | Neither exists | 2026-09-11 | rho.co/changelog. Announced as "next" on 2026-08-03 |
| Terms of Service | Version 7.0.0, last updated 2026-08-27 (page also datelined 2026-08-04) | 2026-09-11 | rho.co/policies/terms-of-service. Rho reserves the right to amend at any time |
| Rho Treasury regulatory AUM | $1,892,904,589 across 1,078 accounts (1,071 businesses, 7 charities) | Form ADV annual amendment filed 2026-03-25 | reports.adviserinfo.sec.gov, CRD 314581. Next amendment due around March 2027 |
| Rho Capital maximum line | $5M on /product/capital, $2M in the /blog/rho-capital Highlights block | 2026-09-11 | Both pages. Rho's own two numbers disagree |
| Invoicing accounting sync | QuickBooks Online only, shipped 2026-08-31. /product/invoicing still says no accounting sync exists | 2026-09-11 | rho.co/changelog and rho.co/product/invoicing |
| Rho's own competitor comparison data | Footnote dates spread from 08/02/2026 to 09/11/2026 by page | varies | Each page's own footnote. Treat every one as its own as-of date |

**Competitors**

| Fact | Value | As of | Re-check at |
| --- | --- | --- | --- |
| Ramp valuation | $44B (Series F, $750M, closed 2026-06-04); reported in early talks at about $60B | Talks reported 2026-09-08 (PYMNTS) | Ramp newsroom, PR Newswire |
| Ramp scale (self-reported, unaudited) | 70,000+ customers, $200B+ annualized purchase volume | 2026-06-01 | Ramp press releases |
| Ramp Developer API size | 252 documented operations across 40 resource groups | 2026-09-11 | docs.ramp.com/llms-api.txt. Drifts as Ramp ships |
| Mercury charter | OCC preliminary conditional approval only. Final authorization, FDIC insurance and Fed approvals outstanding | 2026-04-24 (OCC letter) | OCC Corporate Applications Search |
| Mercury scale (self-reported, unaudited) | 300,000+ businesses and individuals, $650M+ annualized revenue (a run rate, first reported for 2025), four years GAAP profitable | Reported 2026-04-27 | Mercury press releases |
| Mercury MCP | 31 tools, all read-only | 2026-09-11 | docs.mercury.com/docs/supported-tools-on-mercury-mcp |
| Mercury Pro tier | $350/month month-to-month, $299 on annual billing; no phone support on any plan | 2026-09-11 | mercury.com/pricing. The support posture is the single item here most likely to change once the charter lands |
| Brex ownership | Wholly owned subsidiary of Capital One, N.A. since 2026-04-07. Provisional purchase consideration $4,521M, still subject to post-closing adjustment | Q2 2026 10-Q, filed 2026-07-28 | SEC EDGAR, Capital One CIK 0000927628. A revision is likely in the Q3 10-Q or the 2026 10-K |
| Bank MCP server census | 10 first-party bank or banking-platform servers worldwide, 5 read-write, 4 able to make payments. Rho is not listed | 2026-09-11 | openbankingtracker.com/banks-with-mcp-servers. An aggregator that self-reports as incomplete, so treat it as a floor |

### 10.3 How this document was built

**The corpus.** Measured on disk, not estimated:

| Source | Count |
| --- | --- |
| rho.co page captures | 556 (130 core marketing, product and policy pages; 269 help-center articles; 125 comparison blog posts; 25 partner microsites; 7 others) |
| Partner microsites fetched live during verification | 52 more, completing the 77-page census |
| docs.rho.co guide pages | 13 (12 guides plus the docs index page) |
| API operation references | 14, plus the OpenAPI document |
| Sandbox probe artifacts | 2,490 files across auth, pagination, filters, limits and resource probes |
| External primary-source captures | 55 (SEC filings, the Form ADV PDF, the OCC decision, CFPB complaint data, Terms of Service full text) plus 31 Ramp captures |
| Machine-readable site files | sitemap.xml (1,042 URLs), site-llms.txt, site-llms-full.txt, the status page JSON API |
| Research output | 29 findings files, 305,887 words |

A note on one number: earlier files inside this project describe the corpus as "522 pages" and "536 pages". Both are undercounts taken mid-crawl. The count at the end of the crawl is 556. Where this document and its working files disagree, 556 is right.

**The two-pass method.** Pass one: 29 topic agents each read a slice of the corpus and wrote a findings file recording claims with verbatim quotes and absolute file paths. Pass two: 16 load-bearing claims were extracted and handed to independent checkers whose instruction was to refute them, with the corpus plus live web access. Their output is the verified claim register, shipped beside this document as `research/VERIFIED_CLAIMS.md`, and it is the authority wherever it disagrees with a findings file (`research/findings/`).

**What verification changed.** Of 16 claims, one came back CONFIRMED and fifteen came back PARTIALLY_CONFIRMED. None came back clean. Concretely:

- Mercury's charter date moved from 2026-04-27, the press announcement, to 2026-04-24, the date on the OCC letter, and "conditional approval" became "preliminary conditional approval", which is the OCC's own term and materially weaker.
- A widely repeated "$150M Series C led by Balderton Capital in 2024" was deleted outright. Five Form Ds totaling $104,732,452, nothing filed since 2022-01-21, and Balderton's portfolio does not list Rho.
- "1,078 business accounts" in the Form ADV became 1,071 businesses plus 7 charitable organizations.
- The alarming 10-card unauthorized-use clause stopped being a Rho term. It is a near-verbatim restatement of Regulation Z, 12 C.F.R. 1026.12(b)(5), Brex carries the same clause, and the number comes from the CFPB rather than from Rho.
- "Two balance thresholds, no middle tier" on the partner microsites was refuted by a full 77-page census that found a continuous ladder with eleven pages in a $100K to $300K middle band.
- "The 4.66% Treasury headline is mathematically unreachable" softened to "unreachable under the standard published allocation rules", because the help center documents two routes past the 50% Vanguard cap.
- "Months after" on the stale QuickBooks invoicing claim became eleven days.
- "The footnote discloses that Slope underwrites the line" became "the body pricing copy says so", which removes most of the fine-print sting.
- A claim that Rho's affiliate agreement disclosed interchange economics was found false. Interchange appears nowhere in the corpus as a Rho revenue line.
- A claim searching "the 1042-URL corpus" was corrected: 1,042 is the sitemap count, not what was read.

**Assessment:** the adversarial pass changed a number, a date, a scope or a framing in every claim it touched, and it killed one entirely. That is the headline methodological finding. Anything in this dossier not traceable to the verified register should be read as first-pass research that has not been attacked.

**Known limits, stated plainly:**

1. **The production API was never exercised with a real token.** Every statement about production behavior rests on documentation, on the public unauthenticated OAuth metadata, or on a 401 response body. The record counts quoted throughout (14 accounts, 8 cards, 72 transactions, 33 statements, 7 invoicing customers, 12 invoices) are sandbox counts.
2. **No Rho account was opened.** Nothing was observed inside the product: no onboarding flow, no Treasury allocation screen, no Bill Pay draft, no MCP consent dialog, no tool list, no admin audit log.
3. **No sales conversation and no support ticket.** Every question whose answer lives behind "contact Rho" is open, which is most of section 10.1.
4. **Competitor scale figures are self-reported where noted.** Ramp's 70,000 customers and $200B volume, and Mercury's 300,000 businesses, $650M annualized revenue and four years of GAAP profitability, are company boilerplate reproduced by press outlets. They are attributed, not confirmed.
5. **The sandbox is not production.** It has no MCP endpoint, it does not enforce the documented rate limits (150 requests on one token in a 57-second window, and an instantaneous burst of 68.9 requests per second, both with zero 429s), and its dataset never produces roughly a third of the enum values the docs define.
6. **Rho's own comparison tables were not used as evidence about competitors.** Rho's /product/api table claims Brex has no documented MCP integration. Brex's changelog dates its MCP server to April 2026, and Rho's own blog reversed the claim five days later.
7. **Scope was English-language and US-focused.** Non-US regulatory posture, non-US competitors and non-English coverage were not examined.
8. **Practitioner sentiment was never sampled.** No Reddit, no G2, no customer interviews.

### 10.4 Refresh procedure

Re-runnable in about two hours, most of it unattended. Everything this procedure references ships beside this document in `research/`: the crawler (`research/tools/fetch_all.sh` and `fetch_page.py`), the URL lists (`urls-core.txt`, `urls-help.txt`, `urls-blog-comp.txt`), the 556-page corpus (`research/corpus/rho-co-pages/`), the stored sitemap (`research/tools/site-sitemap.xml`), the sandbox probes and their captured output (`research/sandbox/`), the 29 findings files (`research/findings/`) and the verified claim register (`research/VERIFIED_CLAIMS.md`). All paths below are relative to this document. One caveat before you start: `sandbox/census.py` and `sandbox/probe.sh` still carry the absolute output paths of the original run, three lines in total, so repoint them before re-running.

1. **Stamp the run.** Fix today's date at the top. Every number you touch gets that stamp or an older one, never no stamp.
2. **Re-crawl.** Run `research/tools/fetch_all.sh` over `research/tools/urls-core.txt`, `urls-help.txt` and `urls-blog-comp.txt`, writing into a fresh `pages2/` tree, then `diff -rq` it against `research/corpus/rho-co-pages/`. The non-empty diffs are your entire change list. Most files will be byte-identical; the Treasury pages will always differ because the yield date rolls.
3. **Diff the sitemap.** Re-fetch `https://www.rho.co/sitemap.xml` and compare the URL set against the stored 1,042. New `/product/*` and `/partner/*` slugs, and pages that disappeared, are the highest-signal changes on the marketing side.
4. **Re-stamp the rate-bearing pages by hand.** `/product/treasury`, `/treasury-yield-comparison`, `/product/business-savings-account` and `/pricing`. Rewrite the yield rows in 10.2 and note the new footnote dates.
5. **Read the changelog forward.** `rho.co/changelog`, everything newer than the last entry you recorded. As of 2026-09-11 the newest entry was 2026-08-31 and there was no September entry at all.
6. **Re-pull the API contract.** Fetch `https://docs.rho.co/api/v1/openapi.md`, count operations and scopes, and diff against 14 and 5. Then `curl https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` and read `scopes_supported`. **A non-`:read` scope appearing there is the single highest-signal event this document tracks**, because it is the first public sign that Rho's agent surface can move money, and it costs one unauthenticated request to check. Also re-fetch `https://auth.rho.co/.well-known/openid-configuration` and re-test `POST https://auth.rho.co/oauth2/register` for whether dynamic client registration is still disabled.
7. **Re-run the sandbox census.** `research/sandbox/census.py` and `research/sandbox/probe.sh`. You are looking for new operations, new enum values and changed record counts, not for new data.
8. **Check the corporate record.** `https://data.sec.gov/submissions/CIK0001756460.json` for Under Technologies, Inc.; any new filing is a funding event. Then the Form ADV for CRD 314581, whose annual amendment lands each March and carries the AUM and account counts.
9. **Check the competitors.** OCC Corporate Applications Search for Mercury Bank, N.A. final approval; Capital One's next 10-Q for a revised Brex purchase price; Ramp's newsroom for the rumored round; `docs.mercury.com` and `docs.ramp.com` for tool and operation counts; `brex.com/changelog`.
10. **Re-verify anything that moved.** A claim that survived an adversarial check in September is not still verified once its underlying number changes. Re-run the refutation pass on every claim whose evidence you just edited, and re-date the entry in `research/VERIFIED_CLAIMS.md`.

**Suggested cadence:** steps 4 and 6 monthly, because yields and the scope list are the fastest-moving things here. Steps 2, 3, 5 and 7 quarterly. Step 8 on the filings' own calendar, which means Form ADV each March and 10-Qs in the month after each quarter end. Step 9 whenever a competitor makes news, since all four of them announce on their own schedule and this document goes stale from the competitive side first.
