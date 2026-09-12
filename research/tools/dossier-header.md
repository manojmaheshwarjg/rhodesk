# Rho: An End-to-End Product Dossier

**Unofficial.** Compiled 2026-09-11. Rho is a US business banking and finance platform at https://www.rho.co.

This document exists to take someone who knows nothing about business banking and give them a working
command of what Rho is, how it makes money, who it is for, how it compares to its 2026 competitors, and
what to check before trusting it with a company's cash. It is written to be argued with, not believed.

---

## The short version

If you read nothing else, read this. Each line points at the section that argues it.

| | Finding |
| --- | --- |
| **What it is** | A single platform that bundles a business bank account, corporate cards, bill payment, invoicing, expense management and a treasury product, and charges nothing for the software. (§1) |
| **It is not a bank** | Rho is a software company in front of other people's balance sheets. Deposits sit at Webster Bank, a division of Santander Bank, N.A. FDIC insurance covers that bank failing, not Rho failing. (§1.4, §9.1) |
| **It is an orchestration layer** | At least seven regulated or third-party providers sit behind the products: Webster/Santander, American Deposit Management, Apex Clearing and Interactive Brokers, Mastercard, Wise, Stripe, and Slope with Lead Bank. (§2.2) |
| **The software really is $0** | There is no paid tier anywhere. You pay through interchange on card spend, the spread on deposits, 1% on foreign currency, and a 0.15% to 0.60% Treasury advisory fee. Free software funded by balances is a legitimate model, and it is the model. (§4) |
| **The headline yield is not reachable** | The advertised Treasury rate assumes a 100% allocation to a fund the product caps at 50%. Under the standard published rules the achievable blended figure at the best fee tier is materially lower. (§3.3, §8.2) |
| **The API cannot move money** | Fourteen operations, all HTTP GET, shipped 2026-08-03. No writes, no webhooks. Rho says write access is next. (§6) |
| **Where it genuinely wins** | No seat fees at any size, 24/7 human support including phone on a $0 account, a $50,000 Treasury minimum against Mercury's $250,000, AP automation included and settling from the account that holds the cash, and comparison pages that name where competitors beat it. (§8.1) |
| **Where it is behind** | Scale, write-capable APIs and agent surface. Ramp, Brex and Mercury all shipped agent tooling before Rho, and Mercury and Brex can both initiate payments programmatically. (§7, §8.2) |
| **The verdict** | A well-executed bundle built on one structural pricing bet, not a differentiated technology company. That is not a criticism: the bundle is the product. (§8.4) |
| **Before moving cash** | Work the eighteen diligence questions in §9.6. |

---

## How this was researched, and how much to trust it

### The corpus

- **556 pages of rho.co**, crawled in full: all 13 product pages, pricing, all 8 competitor comparison pages, all 269 help-center articles, 125 comparison and review blog posts, every policy and terms page, 14 customer case studies, and the changelog. The sitemap lists 1,042 URLs; the 486 not crawled are almost entirely blog posts and partner landing pages outside the product surface.
- **The complete developer documentation** at docs.rho.co: 13 guides and 14 API operation references.
- **The live API**, measured directly. Roughly 2,500 requests against the public sandbox.
- **Independent sources** for everything about the outside world: SEC EDGAR (the Securities and Exchange Commission's free public filings database) and Form ADV filings (the annual disclosure every SEC-registered investment adviser must file), FDIC BankFind (the FDIC's public register of insured banks), licensing decisions by the OCC (the Office of the Comptroller of the Currency, the federal regulator that grants national bank charters), Capital One's 10-Q (a public company's quarterly financial report to the SEC), competitor documentation and pricing pages, and press coverage.

### The method

Two passes, deliberately adversarial. A first pass extracted findings from the corpus. A second pass took the
sixteen most load-bearing claims and handed each to an independent checker whose instructions were to
**refute** it, defaulting to "unverified" rather than "confirmed" when evidence was thin.

That second pass changed the document materially. Fifteen of the sixteen claims came back
`PARTIALLY_CONFIRMED` rather than `CONFIRMED`, meaning the original was directionally right but wrong in a
number, a date, or a scope. One example worth stating up front, because it shows what the process is for:
the first pass reported that Rho's terms make a customer "liable for all unauthorized use of all cards" once
ten or more cards are issued, which reads alarming. The checker confirmed the clause exists and then
established that it is a near-verbatim restatement of federal law, Regulation Z at 12 C.F.R. 1026.12(b)(5),
that Brex's card agreement carries the same clause, and that it is standard commercial card practice. The
alarming number comes from the CFPB (the Consumer Financial Protection Bureau, the US federal agency that
writes and enforces consumer finance rules), not from Rho. That correction survives into section 9.

### The three labels

| Label | Meaning |
| --- | --- |
| **Rho says** | A claim from Rho's own marketing, help center, docs or contracts, and nothing more |
| **Verified:** | Checked against a primary source outside Rho's control, or a live HTTP response |
| **Assessment:** | A judgment. Reject it freely; the evidence it rests on is cited |

Anything with a rate, a fee, a valuation or a product status carries an as-of date, because all four change.

### What this research could not do

No Rho account was opened. No sales conversation happened. The production API was never called with a real
token, so every measured API statement is sandbox behavior. Pricing and product claims about competitors are
their own published figures unless a primary source is cited. Several important things, notably the actual
cost of Rho Capital and the real distribution of card credit limits, are not published anywhere and remain
open. Section 10 lists every one of them.

---

## Contents

{{TOC}}

A companion document, `RHO_API_REFERENCE.md`, covers the developer surface in full detail:
the endpoint reference, the sandbox, MCP, and the places where Rho's published docs diverge from live behavior.

---

