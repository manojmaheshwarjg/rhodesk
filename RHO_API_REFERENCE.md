# Rho API: A Practical Reference

**Unofficial.** Compiled 2026-09-11 from Rho's published documentation plus direct measurement of the live sandbox.
Rho's official documentation is at https://docs.rho.co. This document is not a replacement for it. It is what the
official docs say, plus what the API actually does when you call it, plus the places where those two disagree.

A companion document, `RHO_PRODUCT_DOSSIER.md`, covers the product, the business model, eligibility, the risk
picture and the 2026 competitive landscape. Its section 6 summarises this document. Read that one first if you
are evaluating Rho, and this one if you are integrating with it.

---

## About this document

### What it covers

The Rho API is the programmatic interface to a Rho business banking account. Version `v1` shipped on
2026-08-03 and is **read-only**: 14 operations, all `GET`, across five resources (accounts, cards,
transactions, statements, invoicing). There is no write path of any kind. Rho's own roadmap statement is
"Read-only is live today. Write access and webhooks are next."

There is also an MCP server, which lets an AI client such as Claude query the same data in the same way.

### How it was built

Two passes. First, every page of `docs.rho.co` was read (13 guides and 14 operation references), alongside
a 522-page crawl of `rho.co`. Second, the live sandbox at `https://rhoapi-sandbox.rho.co/api/v1` was
exercised directly: every endpoint listed and paged to exhaustion, every documented parameter tested with
valid and invalid values, every error class triggered deliberately, and every single-resource GET compared
field by field against its list representation. Roughly 2,500 raw responses were captured.

Claims are labelled throughout:

| Label | Meaning |
| --- | --- |
| (no label) | Stated in Rho's official documentation |
| **Observed** | Measured against the live sandbox, with the request that shows it |
| `> **Divergence:**` | Official documentation and observed behavior disagree |

### What it does not cover

Production was never exercised with a real API Access Token, because no Rho account was opened. Every
"observed" statement is therefore sandbox behavior unless it concerns an unauthenticated production
endpoint, which is called out where it happens. Production may differ, and in at least one known case it
certainly does: rate limits are documented but were never triggered in sandbox at any load this research
was willing to generate.

### The single most useful finding

The sandbox is open. It needs no account, no signup, and no approval. Any non-empty bearer token works:

```bash
curl https://rhoapi-sandbox.rho.co/api/v1/accounts -H "Authorization: Bearer sandbox"
```

That means you can evaluate this API completely, including its data model and its failure modes, before
talking to anyone at Rho. Section 3 is a full guide to doing exactly that.

### The second most useful finding

The official documentation diverges from live behavior in more than 40 specific, reproducible places. Some
are cosmetic. Several will cost an integrator a day each. The five worth knowing before you write a line of
code:

| # | What the docs say | What actually happens |
| --- | --- | --- |
| 1 | The auth guide lists **three** scopes | **Five** exist. `cards:read` and `invoicing:read` are missing from the table. Confirmed from Rho's own public OAuth metadata. |
| 2 | Errors follow RFC 9457 with `type: "about:blank"` and a `detail` field | The media type is right, but `type` is a bare number as a string (`"2"`, `"1303"`, `"1317"`) and `detail` is usually absent |
| 3 | Getting started: "covers accounts and transactions" | Cards, statements and invoicing are also live and fully documented |
| 4 | Cursors are "stable across changes to the underlying data" | Five of six endpoints use offset-based cursors internally, which structurally cannot provide that guarantee |
| 5 | Nothing is said about testing MCP | There is no sandbox MCP endpoint. MCP exists only in production, so it cannot be tried without a real account |

Each is documented in full, with reproduction steps, in the section that owns it.

### Keeping it current

This is a snapshot of a six-week-old API that Rho has said is actively moving. Section 6.4 covers the
versioning contract and section 7.10 lists the open questions. The table below is the watch list: each check
is a single unauthenticated command, and each one is the earliest public signal that something changed.

| Check | Command | What a change means | Cadence |
| --- | --- | --- | --- |
| Scopes | `curl https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` | Diff `scopes_supported` against the five `:read` scopes. **A scope that does not end in `:read` is the first public sign of write access.** | Monthly |
| Operation count | `curl https://docs.rho.co/api/v1/openapi.md` | Diff against 14 operations across 5 resources. New resources appear here before they appear in the guides. | Monthly |
| Dynamic client registration | `curl -X POST https://auth.rho.co/oauth2/register -d '{}'` | Currently returns "Dynamic registration is not enabled". If that changes, third-party MCP clients can self-register (see 7.6). | Monthly |
| Sandbox MCP | `curl -o /dev/null -w "%{http_code}" https://rhoapi-sandbox.rho.co/mcp/v1` | Currently 404. A 401 or 200 means MCP became testable without a production token (see 7.2). | Monthly |
| Webhooks | `curl https://docs.rho.co/llms.txt` | Watch for a webhooks or events guide appearing in the table of contents. Rho has said webhooks are next. | Monthly |
| Deprecation signals | any API response headers | No `Deprecation` or `Sunset` header (RFC 8594) has ever been observed. Their appearance is the only machine-readable notice channel that would exist. | Each run |
| Data model census | re-run the section 3.3 census | New enum values, new fields, changed record counts. The contract permits all three additively without notice. | Quarterly |

---

## Contents

- [1. Orientation and mental model](#1-orientation-and-mental-model)
    - [1.1 What the Rho API is](#11-what-the-rho-api-is)
    - [1.2 What it is not](#12-what-it-is-not)
    - [1.3 When it shipped, and what that implies](#13-when-it-shipped-and-what-that-implies)
    - [1.4 The read-only boundary, and exactly what it forbids](#14-the-read-only-boundary-and-exactly-what-it-forbids)
    - [1.5 The two hosts](#15-the-two-hosts)
    - [1.6 The surface: 14 operations across 5 resources](#16-the-surface-14-operations-across-5-resources)
    - [1.7 The five scopes](#17-the-five-scopes)
    - [1.8 Decision guide: REST, MCP, or neither](#18-decision-guide-rest-mcp-or-neither)
    - [1.9 In five minutes, against the sandbox](#19-in-five-minutes-against-the-sandbox)
- [2. Authentication and authorization](#2-authentication-and-authorization)
    - [2.1 The two models at a glance](#21-the-two-models-at-a-glance)
    - [2.2 API Access Tokens end to end](#22-api-access-tokens-end-to-end)
    - [2.3 Scopes](#23-scopes)
    - [2.4 Partner authentication (OAuth 2.0)](#24-partner-authentication-oauth-20)
    - [2.5 What probing actually shows](#25-what-probing-actually-shows)
    - [2.6 401 versus 403](#26-401-versus-403)
    - [2.7 Token hygiene checklist](#27-token-hygiene-checklist)
- [3. The sandbox](#3-the-sandbox)
    - [3.1 Base URL and authentication](#31-base-url-and-authentication)
    - [3.2 One shared tenant, read-only](#32-one-shared-tenant-read-only)
    - [3.3 Complete inventory of the fixture dataset](#33-complete-inventory-of-the-fixture-dataset)
    - [3.4 Sandbox versus production: the four differences that will bite you](#34-sandbox-versus-production-the-four-differences-that-will-bite-you)
    - [3.5 Worked examples](#35-worked-examples)
    - [3.6 Sandbox gotchas](#36-sandbox-gotchas)
- [4. Endpoint reference: Accounts, Transactions and Cards](#4-endpoint-reference-accounts-transactions-and-cards)
    - [4.0 Conventions and evidence base](#40-conventions-and-evidence-base)
    - [4.1 The seven operations at a glance](#41-the-seven-operations-at-a-glance)
    - [4.2 Parameter semantics shared by the three list operations](#42-parameter-semantics-shared-by-the-three-list-operations)
    - [4.3 Accounts](#43-accounts)
    - [4.4 Transactions](#44-transactions)
    - [4.5 Cards](#45-cards)
    - [4.6 Joining the three resources](#46-joining-the-three-resources)
    - [4.7 Divergence index for this section](#47-divergence-index-for-this-section)
- [5. Endpoint reference: Statements, Invoicing and the file endpoints](#5-endpoint-reference-statements-invoicing-and-the-file-endpoints)
    - [5.1 The seven operations](#51-the-seven-operations)
    - [5.2 Read this first: the invoice file endpoint returns 404 on every documented-correct pairing](#52-read-this-first-the-invoice-file-endpoint-returns-404-on-every-documented-correct-pairing)
    - [5.3 Statements](#53-statements)
    - [5.4 Invoicing: invoices](#54-invoicing-invoices)
    - [5.5 Invoicing: customers](#55-invoicing-customers)
    - [5.6 The file endpoints and signed-URL mechanics](#56-the-file-endpoints-and-signed-url-mechanics)
    - [5.7 Errors specific to these seven operations](#57-errors-specific-to-these-seven-operations)
    - [5.8 Checklist for an integrator](#58-checklist-for-an-integrator)
    - [5.9 Enum inventory for this section](#59-enum-inventory-for-this-section)
- [6. Cross-cutting mechanics](#6-cross-cutting-mechanics)
    - [6.1 Pagination](#61-pagination)
    - [6.2 Rate limits](#62-rate-limits)
    - [6.3 Errors](#63-errors)
    - [6.4 Versioning and compatibility](#64-versioning-and-compatibility)
    - [6.5 The short version](#65-the-short-version)
- [7. MCP and agent access](#7-mcp-and-agent-access)
    - [7.1 Endpoint and transport](#71-endpoint-and-transport)
    - [7.2 There is no sandbox MCP endpoint](#72-there-is-no-sandbox-mcp-endpoint)
    - [7.3 Protocol versions, the header requirement, and what gets rejected](#73-protocol-versions-the-header-requirement-and-what-gets-rejected)
    - [7.4 Authentication: the two paths](#74-authentication-the-two-paths)
    - [7.5 Protected-resource metadata is public, and more accurate than the docs](#75-protected-resource-metadata-is-public-and-more-accurate-than-the-docs)
    - [7.6 Dynamic client registration is disabled, so OAuth is Rho-onboarded clients only](#76-dynamic-client-registration-is-disabled-so-oauth-is-rho-onboarded-clients-only)
    - [7.7 Claude Code setup, and the secret-hygiene problem in the published command](#77-claude-code-setup-and-the-secret-hygiene-problem-in-the-published-command)
    - [7.8 What the server exposes, and what the docs will not tell you](#78-what-the-server-exposes-and-what-the-docs-will-not-tell-you)
    - [7.9 Security: what an agent connected to Rho can and cannot do](#79-security-what-an-agent-connected-to-rho-can-and-cannot-do)
    - [7.10 Open questions for Rho](#710-open-questions-for-rho)
- [8. Building on it](#8-building-on-it)
    - [8.1 The constraints that actually drive the design](#81-the-constraints-that-actually-drive-the-design)
    - [8.2 Incremental sync](#82-incremental-sync)
    - [8.3 Idempotency and reconciliation](#83-idempotency-and-reconciliation)
    - [8.4 Handling money correctly](#84-handling-money-correctly)
    - [8.5 Storing and joining IDs](#85-storing-and-joining-ids)
    - [8.6 Retry, backoff and throttling](#86-retry-backoff-and-throttling)
    - [8.7 Observability](#87-observability)
    - [8.8 What you cannot build](#88-what-you-cannot-build)
    - [8.9 Reference implementation](#89-reference-implementation)

---

## 1. Orientation and mental model

All observations in this section were captured against the live sandbox and against unauthenticated production metadata endpoints on **2026-09-11 and 2026-09-12 (UTC)**. Wherever a claim comes from Rho's published documentation it is attributed to the page it came from. Wherever it comes from a request this document actually made, it is labelled "observed" and the request is shown.

### 1.1 What the Rho API is

Rho is a business banking and spend-management platform. The Rho API is that platform's read interface to a single Rho business's own data: balances, the transaction ledger, corporate cards, period-end statements, and the invoicing records (issued invoices and the customers they bill).

Rho's own framing, from `/product/api`, contrasts it with the two adjacent categories it is not:

> "The Rho API is neither: it is the banking platform's own front door to your own company's data."

Three properties define the shape of everything else in this document:

| Property | Value | Source |
| --- | --- | --- |
| Surface size | 14 operations, 5 resource families, all `GET` | `https://docs.rho.co/api/v1/openapi` index, confirmed by enumeration |
| Access model | Long-lived bearer token per business (`rhobat_` prefix), or OAuth 2.0 for third-party apps | `/docs/v1/auth`, `/docs/v1/partner-auth` |
| Cost and eligibility | $0, no separate API fee, "every Rho business gets API access, no waitlist and no approval step" | `/product/api` |

The API is versioned in the URL path. The current and only version is `v1`, spec version `1.0.0`. Rho's versioning page commits `v1` to being "stable and additive-only": new enum values, new nullable fields, and new optional query parameters can appear without warning, while removals, renames, type changes, and newly-required fields require a new API version. Deprecations carry "at least 15 days' notice."

> **Divergence:** The versioning page promises at least 15 days' notice before a `v1` deprecation, but there is no machine-readable channel to deliver it on. No `Deprecation` or `Sunset` header (RFC 8594) was observed on any response, on either host. Notice arrives by watching the docs by hand.

### 1.2 What it is not

Naming the non-goals early saves a lot of evaluation time.

| It is not | Consequence |
| --- | --- |
| A payments API | No operation initiates, approves, cancels, or reschedules any money movement. See §1.4. |
| An aggregator (Plaid, Teller, MX) | It reads one business's Rho data only. There is no institution-linking concept, no item, no cross-bank coverage. |
| Banking-as-a-service | You cannot open accounts, issue cards, or onboard sub-entities through it. |
| Event-driven | There are no webhooks and no event stream. Every integration polls. Rho's changelog (2026-08-03) states webhooks are "next", with no date. |
| Browser-callable | No CORS headers are emitted on any response and `OPTIONS` returns `405`. Observed, §1.8. Server-to-server only. |
| A full mirror of the Rho product | There is no Payments, Bill Pay, Users, Departments, Vendors, Approvals, Reimbursements, Expenses, or Treasury-trading resource in `v1`. Bill Pay and AP in particular have no representation at all. |
| Multi-entity | A token is scoped to one business. A Claude MCP connection is likewise one business at a time, per Rho's help center. |

### 1.3 When it shipped, and what that implies

The API came out of beta in mid-2026. Rho published two different dates for the same launch:

| Source | Date | Text |
| --- | --- | --- |
| Blog, "Introducing: The Rho API" | 2026-07-29 | API out of beta, MCP server in production, Claude native support live, available to all customers |
| Changelog, "Introducing Rho API" | 2026-08-03 | "Read-only is live today. Write access and webhooks are next." |
| `/product/api` page footer | "current as of August 2026" | capability as-of stamp |

So the public surface is roughly six weeks old as of this writing (2026-09-11): 44 days after the blog date, 39 after the changelog date. Wherever this document dates the API, that is the figure it means. Three practical implications follow, and each one shows up concretely later in this document:

1. **The documentation is behind the implementation in specific, checkable ways.** Cards and Invoicing shipped, their scopes were added to the OpenAPI document and to the per-product guides, but not back-ported to the central pages. Two of the divergences in this section are exactly this failure mode (§1.6, §1.7).
2. **The sandbox is a static fixture set, not a simulator.** It cannot produce a `403`, a `429`, or a rate-limit header, and at least one documented endpoint is outright broken in it (§1.5). Anything an integrator must handle in production but cannot trigger in sandbox is unit-test territory, not integration-test territory.
3. **The read-only boundary is a v1 property, not a permanent one.** Rho has publicly announced write access as the next step. Design the client so that a future write surface is additive to your code, and do not build product assumptions ("a leaked token cannot move money") that would silently become false on a future version.

### 1.4 The read-only boundary, and exactly what it forbids

This is the single most load-bearing fact about the API, and unusually for a security claim it is structurally verifiable rather than a policy assertion: there is no non-`GET` operation in `v1` to call.

**Observed.** Every write method on every path returns `405 Method Not Allowed` with `Allow: GET` and a zero-byte body, and it does so *before authentication runs*:

```bash
curl -sS -o /dev/null -D - -X POST https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H "Content-Length: 0"
```

```http
HTTP/2 405
date: Sat, 12 Sep 2026 00:23:35 GMT
content-length: 0
allow: GET
via: 1.1 google
cf-cache-status: DYNAMIC
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
server: cloudflare
cf-ray: a39ac3acfbcac4d1-EWR
```

Note the absence of any `Authorization` header. The prior probe pass swept `POST`, `PUT`, `PATCH`, and `DELETE` across all six collection paths and the single-resource paths, with a valid token, a garbage token, and no token at all: `405` in every one of those cells, `Allow: GET` on every path. Routing precedes method checking, which precedes auth, so `POST` to a path that does not exist returns `404 page not found` instead.

Two consequences worth internalising:

- There is no hidden write surface reachable by verb probing. No path advertises anything but `GET`.
- A `405` is **not** evidence that your token was accepted. If you are health-checking with a write verb, you are testing the router, not your credential.

What the boundary forbids, drawn from the operation catalogue plus Rho's own help-center enumeration ("Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account."):

| Cannot | Notes |
| --- | --- |
| Initiate any payment | ACH, wire, international wire, check, internal transfer, bill pay |
| Act on the approvals queue | You can *read* `status: "awaiting_approval"` on transactions; you cannot approve, reject, or cancel |
| Create, issue, lock, cancel, or modify a card | Including spending limits and MCC allow/block rules |
| Manage users, roles, or permissions | No Users resource exists |
| Change any account setting | Including 2FA, alerts, and debit controls |
| Create, edit, send, cancel, or mark-paid an invoice | Invoicing is read-only too, despite being a workflow product in the dashboard |
| Write back to a transaction | No note, memo, label, department, or receipt upload |
| Move Treasury positions | No trading surface |
| Receive a push event | No webhooks. Poll only, under the documented ~60 req/min per token |
| See a full PAN, CVC, or expiry | Cards expose `last_4` only, stated explicitly in `/docs/v1/cards` |

Rho describes four independent enforcement layers behind this: the surface has no write op; every scope is `*:read`, so there is no writable scope to request; only Account Owners and Admins can mint a token or authorize an OAuth or Claude connection, behind 2FA; and credentials expire, cap out at 20 per business, support a 100-entry IP allowlist, and revoke instantly. Layers two through four are covered in the Authentication section; layer one is the one you can verify yourself in ten seconds with the command above.

### 1.5 The two hosts

| Environment | Base URL | Auth | MCP surface |
| --- | --- | --- | --- |
| Production | `https://rhoapi.rho.co/api/v1` | Real API Access Token or OAuth access token | `https://rhoapi.rho.co/mcp/v1` |
| Sandbox | `https://rhoapi-sandbox.rho.co/api/v1` | Any non-empty bearer token | none (observed `404`) |

Both hostnames resolve to the same pair of Cloudflare edge IPs (`104.18.26.176`, `104.18.27.176`, observed via `dig +short`) and return byte-identical `401` bodies and header sets. The sandbox serves a deterministic fictional fixture set. Record counts, observed just after 00:20 UTC on 2026-09-12 by walking every list endpoint at `page_size=100`:

| Endpoint | Response array key | Records |
| --- | --- | --- |
| `/accounts` | `accounts` | 14 |
| `/cards` | `cards` | 8 |
| `/transactions` | `transactions` | 72 |
| `/statements` | `statements` | 33 |
| `/invoicing/customers` | **`customers`** | 7 |
| `/invoicing/invoices` | **`invoices`** | 12 |

The array key is the bare resource name, not the path. `/invoicing/customers` returns `customers`, not `invoicing_customers`. This trips up generic client code that derives the key from the path.

Four things the sandbox cannot do for you:

1. **It cannot produce a `403`.** Scopes are not enforced there at all. A single garbage token (`Bearer qqqq-garbage-token-no-scopes-at-all`) read all five scope families successfully. Your scope-denial handling and your IP-allowlist-rejection handling are untestable before production.
2. **It cannot produce a `429`.** 150 requests on one token inside a 57-second window all returned `200`, a pace 2.5 times the documented per-token allowance, with no throttling and no rate-limit header of any kind. Your backoff path is untestable there.
3. **It has no MCP endpoint.** Observed: `GET https://rhoapi-sandbox.rho.co/mcp/v1` returns `404` with the body `default backend - 404` (the ingress-nginx default backend, meaning no route is configured), and `https://rhoapi-sandbox.rho.co/.well-known/oauth-protected-resource/mcp/v1` returns the same. The MCP guide documents `/mcp/v1` and gives a `claude mcp add` example pointing at production, but never says the sandbox lacks the route.
4. **At least one documented endpoint is broken in it.** All 9 sandbox invoices that carry a `file_id` return `404` from the invoice-file endpoint that is supposed to exchange that `file_id` for a download URL:

```bash
curl -sS -w '\nHTTP %{http_code}\n' \
  "https://rhoapi-sandbox.rho.co/api/v1/invoicing/invoices/70000000-0000-4000-8000-000000000010/files/50000000-0000-4000-8000-000000000027" \
  -H "Authorization: Bearer sandbox"
```

```json
{"type":"1303","title":"invoice file not found","status":404}
```

> **Divergence:** `/docs/v1/invoicing` says "When an invoice has a PDF, `file_id` is present ... Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`." In sandbox, every documented-correct `(invoice_id, file_id)` pairing returns `404`. The equivalent transaction-attachment endpoint works (shown in §1.9). Treat invoice PDF retrieval as unverifiable until you have production credentials.

> **Divergence:** There is no way to tell the two environments apart from an error response. Production and sandbox `401` bodies are byte-identical (`{"type":"2","title":"Unauthenticated","status":401}`, same 52 bytes, same md5), the header sets match, and the hostnames share Cloudflare IPs. No environment marker exists in any response. A typo in `RHO_API_BASE_URL` that points a sandbox integration at production produces a `401` that reads exactly like a bad token, and the developer will reasonably debug the credential rather than the hostname.

### 1.6 The surface: 14 operations across 5 resources

All 14 are `GET`. The `operationId` column is the docs URL slug at `docs.rho.co/api/v1/openapi/<tag>/<id>.md`; Rho commits in the versioning page that MCP tool names derive from these frozen `v1` operationIds and "will never change", though it never publishes the exact casing or the tool-name transform.

| # | Resource | Method and path | operationId | Scope | Kind |
| --- | --- | --- | --- | --- | --- |
| 1 | Accounts | `GET /accounts` | `listaccounts` | `accounts:read` | list |
| 2 | Accounts | `GET /accounts/{account_id}` | `getaccount` | `accounts:read` | single |
| 3 | Cards | `GET /cards` | `listcards` | `cards:read` | list |
| 4 | Cards | `GET /cards/{id}` | `getcard` | `cards:read` | single |
| 5 | Transactions | `GET /transactions` | `listtransactions` | `transactions:read` | list |
| 6 | Transactions | `GET /transactions/{id}` | `gettransaction` | `transactions:read` | single |
| 7 | Transactions | `GET /transactions/{transaction_id}/files/{file_id}` | `gettransactionfile` | `transactions:read` | file |
| 8 | Statements | `GET /statements` | `liststatements` | `statements:read` | list |
| 9 | Statements | `GET /statements/{id}` | `getstatement` | `statements:read` | single |
| 10 | Invoicing | `GET /invoicing/customers` | `listinvoicingcustomers` | `invoicing:read` | list |
| 11 | Invoicing | `GET /invoicing/customers/{customer_id}` | `getinvoicingcustomer` | `invoicing:read` | single |
| 12 | Invoicing | `GET /invoicing/invoices` | `listinvoicinginvoices` | `invoicing:read` | list |
| 13 | Invoicing | `GET /invoicing/invoices/{invoice_id}` | `getinvoicinginvoice` | `invoicing:read` | single |
| 14 | Invoicing | `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | `getinvoicinginvoicefile` | `invoicing:read` | file |

Read that table as three tiers, because the tiers behave very differently:

- **Six list endpoints.** These carry the query surface. `/transactions` alone takes 13 filters (`account_id`, `account_type`, `transaction_type`, `status`, `user_id`, `card_id`, `search`, `initiated_after/before`, `posted_after/before`, `min_amount`, `max_amount`) plus `sort_by`, `order`, and the two pagination parameters. `/statements` takes 6 filters. This is where the real work happens. See the Filters and the Pagination sections.
- **Six single-resource getters.** **Observed:** these return exactly the same fields as the corresponding list row, with zero additions. The sweep that establishes this listed each collection, then re-fetched every row individually (`GET /{resource}/{id}` for each id in the list) and compared deep-equal: 146 resources across the six types (14 accounts, 8 cards, 72 transactions, 33 statements, 7 customers, 12 invoices), 146/146 identical, no key present in one form and not the other, no value differences. There is no summary-versus-detail tier. Fetching a list and then looping single `GET`s to "enrich" rows buys nothing and burns your ~60 req/min budget. The one exception is `GET /statements/{id}`, which buys you a re-signed `pdf_url`, not new fields, and even that is subject to a server-side signing cache described in the Files section.
- **Two file endpoints.** These are not file downloads. They return three keys (`download_url`, `file_id`, `file_name`) where `download_url` is a Google Cloud Storage V4 signed URL with `X-Goog-Expires=899` (14 minutes 59 seconds), fetched without your Rho credential. One of them (`gettransactionfile`) works in sandbox; the other (`getinvoicinginvoicefile`) does not, per §1.5.

> **Divergence:** The getting-started page states "Current release is **read-only** and covers accounts and transactions." The read-only half is correct. The coverage half is wrong by three entire resource families: Cards, Statements, and Invoicing are all live, documented on their own guide pages, present in the OpenAPI index, and returning data in sandbox right now. An evaluator who reads only `/docs/v1/getting-started` will conclude the API is 5 operations when it is 14.

### 1.7 The five scopes

Scopes are `resource:action` strings. Per `/docs/v1/auth` they are enforced before the request reaches the handler, and a token missing the required scope is rejected with `403 Forbidden`. There are exactly five, and every one of them is `:read`:

| Scope | Grants | Covers operations |
| --- | --- | --- |
| `accounts:read` | Account information for the business | 1, 2 |
| `cards:read` | Business cards information | 3, 4 |
| `transactions:read` | Transactions the business has access to | 5, 6, 7 |
| `statements:read` | Statements for the business's accounts | 8, 9 |
| `invoicing:read` | Invoicing information | 10 to 14 |

The authoritative live source is the RFC 9728 protected-resource metadata document, which is public and needs no credential:

```bash
curl -sS https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1
```

```json
{"resource":"https://rhoapi.rho.co/mcp/v1","authorization_servers":["https://auth.rho.co"],"bearer_methods_supported":["header"],"scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],"resource_documentation":"https://docs.rho.co/docs/v1/mcp"}
```

> **Divergence:** `/docs/v1/auth` says "The scopes available today are:" and then lists **three**: `accounts:read`, `transactions:read`, `statements:read`. The OpenAPI `AccessToken` security scheme lists **five**. `/docs/v1/cards` says "Both endpoints require the `cards:read` scope" and `/docs/v1/invoicing` says "Every endpoint requires the `invoicing:read` scope." The live metadata above lists **five**. The authoritative answer is five; the central auth page is stale by exactly the two scopes that shipped with Cards and Invoicing. This matters most for partner OAuth: `/docs/v1/partner-auth` tells you to email Rho your "requested scopes" with the example string `accounts:read transactions:read offline_access` and a link to that stale table, so an app built from those two pages will request too few scopes and discover it only when a customer's Cards or Invoicing call 403s.

The per-operation reference pages do not help you here. Fetch one and look at its Security line:

```bash
curl -sS https://docs.rho.co/api/v1/openapi/accounts/listaccounts.md | sed -n '1,8p'
```

```text
# List accounts

Returns a paginated list of accounts for the authenticated business

Endpoint: GET /accounts
Version: 1.0.0
Security: AccessToken
```

> **Divergence:** `/docs/v1/auth` says "The required scope for each endpoint is listed under its **Security** section in the API reference." It is not. Every one of the 14 operation reference pages carries the bare line `Security: AccessToken` with no scope name attached, as the fetch above shows (`.../cards/listcards.md` behaves the same). There is no published per-endpoint scope mapping anywhere in Rho's docs. The mapping in the table above is reconstructed from the per-product guides plus the resource-to-scope naming pattern; Cards and Invoicing are the only two Rho states outright, and Statements is never given a scope on its own guide page at all.

Three further scope facts, from Rho's help center and `/docs/v1/auth`, that shape design:

- Scope selection happens at token creation or at OAuth consent, and Claude's authorization screen lets the user reduce the requested set. Grant the narrowest set per integration.
- There is no sub-scope granularity at all: no per-account scoping, no date window, no amount ceiling, no field-level redaction. `transactions:read` means the entire ledger for the entire business for all time. `invoicing:read` includes your customers' legal names, emails, and postal addresses, which is third-party PII.
- Only Account Owners and Admins can mint a token (behind a 2FA challenge) or authorize an OAuth or Claude connection.

### 1.8 Decision guide: REST, MCP, or neither

The two surfaces are the same contract. Rho's versioning page states the MCP server is "1:1 with the REST API" and the MCP page states it "uses the same API contract, authentication model, scopes, and error behavior." So the choice is not about capability, it is about who is calling and how the result is consumed.

**Reach for the REST API when:**

| Situation | Why REST |
| --- | --- |
| Warehouse or ETL ingestion of the ledger | You need deterministic pagination, retry, and idempotent upsert. Section on Pagination covers the cursor contract. |
| Reconciliation against an accounting system | You need exact, repeatable field access, not a model's summary of it. |
| An internal dashboard or a scheduled cash report | Server-side scheduled job, cached, one token, predictable request count. |
| Anything that must be auditable | A REST call is reproducible from the request line. A tool call mediated by an LLM is not. |
| You need a specific filter combination | The 13 transaction filters and 6 statement filters are only addressable from REST. An MCP client may or may not expose them all. |

**Reach for MCP when:**

| Situation | Why MCP |
| --- | --- |
| A human is asking ad-hoc questions of the data | "What did we spend on software last quarter?" is a conversation, not a job. |
| You are building an agent workflow in Claude or another MCP client | One command connects it, shown below. |
| You want zero integration code | The Claude connector path (Customize → Connectors → Rho → sign in → pick business → authorize) requires no token handling at all, and uses OAuth rather than a pasted secret. |
| You want tool names that are frozen forever | Rho commits that tool names derive from the frozen `v1` operationIds and will never change, so they are safe to hard-code in saved automations. Tool *descriptions* are explicitly not part of the contract. |

The setup command, verbatim from `/docs/v1/mcp`. Note that it points at production: there is no sandbox MCP host to substitute (§1.5).

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

MCP specifics worth knowing before you commit: it is Streamable HTTP at `/mcp/v1`, it advertises protocol versions `2026-07-28`, `2025-11-25`, and `2025-06-18`, every non-`initialize` request must carry `MCP-Protocol-Version`, JSON-RPC batches are rejected, and anything older than `2025-06-18` is rejected. **Observed:** production `/mcp/v1` is the only endpoint in the estate that returns an RFC-compliant `401`, carrying `www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"`; the REST API at `/api/v1` returns `401` with no `WWW-Authenticate` header at all, on both hosts. Rho publishes no tool list, no input or output schemas, no prompt names, and no resource URIs for the MCP server, so what lands in a model's context is only inferable from the 14 REST operations.

**Neither is the right tool when you need any of the following.** Each of these is a hard stop in `v1`, not a workaround:

| You need | Status | What to do instead |
| --- | --- | --- |
| To write anything | Impossible. All 14 ops are `GET`; §1.4. | Use the dashboard, or wait for the announced write surface. Rho has not said whether writes will land as new `v1` operations or as a new version, so do not assume your `v1` client keeps working unchanged when they arrive. |
| Webhooks or any push event | Do not exist. Changelog 2026-08-03: "Write access and webhooks are next." | Poll, inside the documented ~60 req/min per token and ~600 req/min per source IP. Filter on `posted_after` / `initiated_after` to keep pages small. |
| Real-time or sub-minute freshness | Not achievable. Polling one endpoint every second exceeds the documented token budget; no `ETag`, no `Last-Modified`, no `304` path exists, so every poll transfers the full body. | Re-scope to a polling cadence measured in minutes, or drive the workflow from the Rho dashboard. |
| To call it from a browser | Impossible. **Observed:** no `Access-Control-Allow-Origin` on any response with or without an `Origin` header, no `Vary: Origin`, and `OPTIONS /api/v1/accounts` returns `405` with `allow: GET`. | Proxy through your own backend. This also keeps the token off the client. |
| A cheap liveness probe | `HEAD /api/v1/accounts` returns `405` with `allow: GET`, a deviation from RFC 9110, which expects `HEAD` wherever `GET` is implemented. | Probe with `GET /accounts?page_size=1`. |
| Bill Pay, vendors, users, approvals, departments, reimbursements, or treasury trading | No resource exists in `v1`. | Out of scope for the API entirely. |
| A request id for support escalation | **Observed:** no `X-Request-Id`, `traceparent`, or equivalent on any response. The only correlation handle is Cloudflare's `cf-ray`. | Log `cf-ray` on every response. |
| Rate-limit budget observability | **Observed:** no `RateLimit-*`, no `X-RateLimit-*`, and no `Retry-After` on any of roughly 430 captured responses. | Pace conservatively from a fixed budget; you get no feedback signal. |

> **Divergence:** The rate-limits page documents `429 Too Many Requests` with branch logic on `Retry-After` (positive integer means wait that long, `0` means back off exponentially). None of the 14 operation reference pages documents a `429` response at all. All 14 list `200, 400, 401, 403, 500, 503`, and the 8 single-resource operations add `404`. A client generated from the OpenAPI document will therefore have no `429` case, and the sandbox cannot produce one to catch the gap in testing. Add the `429` path by hand.

### 1.9 In five minutes, against the sandbox

Everything below was run end to end against `https://rhoapi-sandbox.rho.co/api/v1` on 2026-09-12 (UTC) and the outputs are the real ones. You need `curl` and `python3`. You do not need a Rho account, a token, or an approval step.

`--compressed` is worth setting from the start: gzip is the only encoding the API honours (brotli, zstd, and deflate are all declined), and on a 40 KB transactions page it cuts the wire payload by roughly 7 times.

#### Step 1: point at the sandbox

```bash
export RHO_BASE=https://rhoapi-sandbox.rho.co/api/v1
export RHO_TOKEN=sandbox   # any non-empty string works in sandbox
```

The literal string `sandbox` is not special. Sandbox auth is a non-empty-string check after a case-sensitive `Bearer ` prefix, nothing more. Details and the exact inferred algorithm are in the Authentication section.

#### Step 2: read every account and its balance

```bash
curl -sS --compressed "$RHO_BASE/accounts?page_size=100" \
  -H "Authorization: Bearer $RHO_TOKEN" \
  -H "Accept: application/json" | python3 -c '
import sys, json
d = json.load(sys.stdin)
for a in d["accounts"]:
    b = a["balance"]
    print("%s  %-9s %13s %s  %s" % (a["id"], a["account_type"], format(b["amount"] / 100, ",.2f"), b["currency"], a["account_name"]))
print("count", len(d["accounts"]), "next", d["page"]["next_page_token"])
'
```

The real output, in full:

```text
30000000-0000-4000-8000-000000000002  checking       8,761.38 USD  Cash (Checking)
30000000-0000-4000-8000-000000000003  checking      87,116.97 USD  Cash (Checking)
30000000-0000-4000-8000-000000000007  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000008  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000009  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000010  credit             0.00 USD  Credit Account
30000000-0000-4000-8000-000000000005  checking           0.00 USD  Inventory Checking
30000000-0000-4000-8000-000000000006  checking       8,119.70 USD  Primary Checking
30000000-0000-4000-8000-000000000001  checking          10.46 USD  Reserve Checking
30000000-0000-4000-8000-000000000011  rewards            0.00 USD  Rewards
30000000-0000-4000-8000-000000000012  rewards            0.00 USD  Rewards
30000000-0000-4000-8000-000000000013  savings            0.00 USD  Savings
30000000-0000-4000-8000-000000000014  savings            0.00 USD  Savings
30000000-0000-4000-8000-000000000004  checking     154,609.29 USD  Treasury Checking
count 14 next None
```

Two conventions land in that one call and hold everywhere: **money is always an object**, `{"amount": <signed integer minor units>, "currency": "<ISO 4217>"}`, never a decimal; and **the last page is signalled by `page.next_page_token` being JSON `null`**, with the key always present.

Two details in the output are worth carrying into the data-model sections. The four `credit` rows omit `account_number_last_4` and `routing_number_last_4` entirely rather than returning them as `null`, so field-absence is meaningful in this API. And the account displayed as "Treasury Checking" has `account_type: "checking"`; `treasury` shows up as an `account_type` only inside statement rows, where it is not a member of the documented account enum at all.

#### Step 3: filter the ledger

```bash
curl -sS --compressed -G "$RHO_BASE/transactions" \
  -H "Authorization: Bearer $RHO_TOKEN" \
  --data-urlencode "status=settled" \
  --data-urlencode "page_size=3"
```

The first of the three rows, complete and unedited:

```json
{
  "account_id": "30000000-0000-4000-8000-000000000009",
  "account_name": "Credit Account",
  "account_type": "credit",
  "amount": { "amount": -6331, "currency": "USD" },
  "attachments": [
    { "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15", "file_name": "parking-receipt.pdf" }
  ],
  "card_id": "20000000-0000-4000-8000-000000000004",
  "card_name": "Lucas Bennett",
  "counterparty_name": "Midtown Parking Services",
  "id": "019f0554-0bf0-7000-8000-00000000000a",
  "initiated_at": "2026-06-26T19:07:02Z",
  "money_movement_id": "40000000-0000-4000-8000-000000000007",
  "posted_at": "2026-06-27T19:13:15Z",
  "status": "settled",
  "transaction_type": "card_debit",
  "user_full_name": "Lucas Bennett",
  "user_id": "10000000-0000-4000-8000-000000000004"
}
```

Note how much is denormalized onto the row: account name and type, card id and name, user id and name. That is deliberate, and it is why the single-resource getters add nothing (§1.6). Reconciliation rarely needs a second call.

#### Step 4: walk every page

Save as `rho_walk.py`. This is the canonical iteration shape for all six list endpoints; only the path and the array key change.

```python
import json, os, urllib.parse, urllib.request

BASE  = os.environ.get("RHO_BASE", "https://rhoapi-sandbox.rho.co/api/v1")
TOKEN = os.environ.get("RHO_TOKEN", "sandbox")

def walk(path, key, **filters):
    params = dict(filters)
    params.setdefault("page_size", 100)
    while True:
        url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
        yield from body[key]
        token = body["page"]["next_page_token"]
        if token is None:
            return
        params["page_token"] = token

if __name__ == "__main__":
    rows = list(walk("/transactions", "transactions", page_size=25))
    net = sum(r["amount"]["amount"] for r in rows)
    print(f"{len(rows)} transactions, net {net/100:,.2f} USD")
```

```bash
python3 rho_walk.py
```

```text
72 transactions, net 1,723,640.44 USD
```

Three rules the cursor imposes, all covered in depth in the Pagination section: the token is opaque and must be passed back verbatim; it is bound to the endpoint *and* its filters and sort order, so changing any filter mid-walk invalidates it with a `400`; and page size is `[1, 100]` inclusive across all six endpoints, defaulting to 20.

#### Step 5: fetch a file

The file endpoint returns metadata plus a signed URL. The download itself goes to Google Cloud Storage and must not carry your Rho token.

```bash
TID=019f0554-0bf0-7000-8000-00000000000a
FID=2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15

URL=$(curl -sS "$RHO_BASE/transactions/$TID/files/$FID" \
  -H "Authorization: Bearer $RHO_TOKEN" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["download_url"])')

curl -sS -o receipt.pdf -w 'HTTP %{http_code}  %{size_download} bytes  %{content_type}\n' "$URL"
```

```text
HTTP 200  769 bytes  application/pdf
```

The metadata response is exactly three keys:

```json
{
  "download_url": "https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&...",
  "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15",
  "file_name": "parking-receipt.pdf"
}
```

The signed URL is valid for 899 seconds from its `X-Goog-Date`, not the "up to 15 minutes" the docs round it to, and statement PDFs behave differently from transaction attachments in a way the docs do not describe. See the Files and signed URLs section before you build an archiver.

#### Step 6: confirm the boundary yourself

```bash
curl -sS -o /dev/null -w 'POST  -> HTTP %{http_code}\n'   -X POST   -H "Content-Length: 0" -H "Authorization: Bearer $RHO_TOKEN" "$RHO_BASE/accounts"
curl -sS -o /dev/null -w 'DELETE-> HTTP %{http_code}\n'   -X DELETE -H "Authorization: Bearer $RHO_TOKEN" "$RHO_BASE/accounts/30000000-0000-4000-8000-000000000002"
curl -sS -o /dev/null -w 'HEAD  -> HTTP %{http_code}\n'   -I       -H "Authorization: Bearer $RHO_TOKEN" "$RHO_BASE/accounts"
```

```text
POST  -> HTTP 405
DELETE-> HTTP 405
HEAD  -> HTTP 405
```

That is the whole mental model: five read-only resources, fourteen `GET`s, one cursor convention, one money representation, signed URLs for binaries, and a `405` for everything else.

#### Before you move to production

| Step | Where |
| --- | --- |
| Create an API Access Token (Owner or Admin, 2FA-gated, shown once, max 1 year, 45-day idle expiry, max 20 per business, optional 100-entry IP allowlist) | Authentication section |
| Handle the error shapes the sandbox will not show you: `403` (scope or IP allowlist), `429` (undocumented in the OpenAPI), and the non-JSON bodies returned for oversized or duplicated `Authorization` headers | Errors section |
| Pace to the documented ~60 req/min per token, not to what the sandbox tolerates (at least 2.5 times that, observed) | Rate limits section |
| Decide your polling cadence and your `posted_after` watermark, since there are no webhooks and no conditional requests | Pagination and Rate limits sections |
## 2. Authentication and authorization

Rho has two credential families and exactly one way to present either of them. Direct customers mint an **API Access Token** (`rhobat_` prefix) from the Rho web console and send it as a bearer credential. Third-party applications acting for Rho customers obtain an **OAuth 2.0 access token** from `https://auth.rho.co` and send that as a bearer credential instead. The resource server does not distinguish the two at the header level, and there is no other supported channel: no cookie, no API key header, no signed request, no query parameter.

Everything in this section that is marked "observed" was reproduced live against `https://rhoapi-sandbox.rho.co/api/v1` and against unauthenticated metadata endpoints on `https://rhoapi.rho.co` and `https://auth.rho.co` on 2026-09-11 and 2026-09-12. Everything else comes from `docs.rho.co` and is cited to the page it came from. Error bodies, problem-details conformance, and the numeric `type` namespace are treated in depth in the section on Errors and status codes; rate limiting is covered in the section on Rate limits; the MCP surface's separate auth middleware is covered in the section on the MCP surface.

### 2.1 The two models at a glance

| Dimension | API Access Token (`/docs/v1/auth`) | OAuth partner token (`/docs/v1/partner-auth`) |
| --- | --- | --- |
| Intended use | Internal integration against your own business | Third-party app acting on behalf of Rho customers |
| Issuance | Self-service, Rho banking settings UI | Rho staff register the client; `auth.rho.co` mints tokens |
| Onboarding | Immediate, in-product | Email `api-partner-request@rho.co`, human review, no stated SLA |
| Credential format | Opaque bearer, `rhobat_` prefix | Opaque bearer, prefix not documented, plus a refresh token |
| Who authorizes | Account Owners and Admins | Account Owners and Admins, via a consent screen |
| Second factor | 2FA challenge at creation | Not documented; consent is login plus approval |
| Scope selection | Chosen per token at creation | Registered set, narrowed per authorization request |
| Binding | One business | One business per grant, chosen at consent |
| Access lifetime | Your chosen expiry, max 1 year | 15 minutes (`expires_in: 900`) |
| Renewal | None. Create a new token by hand | Refresh token, rotating, 30-day rolling window |
| Ceiling | 20 active tokens per business | One active grant per (business, app) |
| IP allowlist | Optional, up to 100 entries | Not documented |
| Revocation by holder | UI only, immediate, irreversible | `POST /oauth2/revoke`, programmatic |
| Failure after revocation | `401` | `401` |
| Sandbox support | Yes, any non-empty bearer | No sandbox authorization server exists (observed) |

The decision rule is Rho's own, verbatim from `/docs/v1/partner-auth`: "If you are building an internal integration for your own account, you don't need OAuth, use an API Access Token instead."

### 2.2 API Access Tokens end to end

#### 2.2.1 Definition and binding

Per `/docs/v1/auth`: "An API Access Token is a long-lived, opaque secret scoped to a single business, the same token continues to work as people on your team come and go."

The structural consequence is the important part. The token is bound to the **business**, not to the user who created it. No user identity travels with the request, and staff turnover does not invalidate the credential. Audit trails on the Rho side can only attribute activity to the token, which is why Rho's own best-practice list says to issue one token per integration.

#### 2.2.2 Who can create one, and the 2FA gate

Two gates, both from `/docs/v1/auth`:

- "The fact that only **Account Owners** and **Admins** can manage API Access Tokens."
- "A **2FA challenge** at the moment of creation."

Note the word "manage", not "create". The same two roles govern the whole lifecycle including revocation. The help center (`Build a custom integration with Rho`) describes the same flow as: "Navigate to Settings → API → Access Tokens" / "Create a new access token" / "Choose the appropriate permissions and complete two-factor authentication."

> **Divergence:** the navigation path to the token screen is described four different ways across Rho's own properties. `/docs/v1/auth` says "your Rho banking settings"; the help center says "Settings → API → Access Tokens"; the product page says "Settings, then Configurations, then Access Tokens"; and the OpenAPI security scheme points at `https://app.rho.co/settings/access-tokens`. Use the URL, it is the only unambiguous one.

#### 2.2.3 What you choose at creation

Verbatim table from `/docs/v1/auth`:

| Field | Notes |
| --- | --- |
| **Name** | A human-readable label that appears in the token list |
| **Scopes** | One or more permissions the token grants |
| **Allowed IPs** | Optional IP allowlist. If set, requests from any other source IP are rejected. Up to 100 entries per token. |
| **Expiration** | Required. Maximum one year. |

Four hard facts fall out of that table:

1. **Scopes are fixed at creation time** in the sense that Rho never documents whether they can be edited afterwards. Neither can name, expiration, nor the allowlist. Plan for immutability and rotate rather than edit.
2. **The IP allowlist caps at 100 entries per token.** Rho does not say whether an entry may be a CIDR block or must be a single address, and says nothing about IPv6. If your egress is a NAT pool larger than 100 addresses and CIDR is not accepted, the allowlist is unusable for you. Confirm the entry format with Rho before designing around it.
3. **Expiration is mandatory.** There is no non-expiring token. The maximum is one year and no minimum is stated.
4. **An allowlist rejection is a 403, not a 401.** See section 2.6.

#### 2.2.4 The show-once secret

Verbatim: "The raw token is **shown only once**, immediately after creation. There is no way to recover the secret later." Rho's advice is to copy it into a secret manager before closing the dialog.

The documented example, verbatim from `/docs/v1/auth`:

```text
rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f
```

That example's hex body is 62 characters, 69 including the `rhobat_` prefix. 62 hex characters is 31 bytes, not a round 32, so the example is almost certainly illustrative rather than a length specification. Rho never states token length as part of the contract, and the versioning guide's "treat IDs as opaque strings" obligation argues against pinning it. **Do not validate token length or charset in your client.** Store the string, send the string.

The phrasing "tokens created in Rho banking settings use the `rhobat_` prefix" implies at least one other token family with a different prefix. No prefix is documented anywhere for OAuth partner access tokens, and there is no published prefix taxonomy.

#### 2.2.5 The 20-active-token cap

Verbatim: "A business can hold at most **20 active tokens** at a time. If you need more, revoke unused ones first."

Whether "active" excludes expired and revoked tokens is not stated, though the word implies it. The practical bite is the interaction with Rho's own rotation guidance, which is overlap-then-revoke: "Create the replacement token, deploy it, and only then revoke the old one to avoid downtime." A business running 20 integrations cannot follow that guidance, because creating token 21 to overlap with token 20 is refused. An operator at the cap must accept a revoke-then-create gap, which means an outage window for that integration. Budget headroom: treat 18 as your real ceiling if you rotate on a schedule.

#### 2.2.6 Mandatory expiry, and the 45-day inactivity clock

| Limit | Value | Exact wording, `/docs/v1/auth` |
| --- | --- | --- |
| Active tokens per business | 20 | "A business can hold at most **20 active tokens** at a time." |
| Maximum expiration | 1 year | "Expiration \| Required. Maximum one year." |
| Inactivity expiry | 45 days | "API Access Tokens also expire automatically after **45 days of inactivity**." |
| What counts as activity | A successful authenticated request | "A successful authenticated API request counts as activity." |
| Clock start for unused tokens | Creation | "For tokens that have never been used, the 45-day window starts at creation." |

**Two independent clocks run concurrently and the token dies at whichever fires first.** The absolute expiry you set at creation (up to one year) and the rolling 45-day inactivity timer are separate mechanisms. A token with an 11-month expiry that is idle for 46 days is dead at day 46.

Read "successful authenticated" carefully. The qualifier excludes failures. A request that returns `401` has not authenticated, and a request that returns `403` authenticated but did not succeed, so on a literal reading neither refreshes the clock. `429` is not addressed at all. Since the phrasing is ambiguous and Rho publishes no warning or notification before a token lapses, the defensive posture is:

- Run a cheap authenticated heartbeat well inside the window, for example `GET /accounts?page_size=1` on a weekly cron, not a 44-day one.
- Make the heartbeat assert a `200`, not merely "no exception", so a `403` from a scope change does not silently look like activity.
- Alert on the heartbeat failing, because there is no other signal that a token is about to die.

Two gaps worth knowing: Rho documents no expiry notification of any kind, and there is **no API to list tokens or read their expiry**, so your own records are the only inventory you will have.

#### 2.2.7 Revocation is immediate and one-way

Verbatim: "Tokens can be revoked at any time from the same settings screen used to create them. Revocation is **immediate**: the next request made with that token will return `401 Unauthorized`. There is no grace period and no way to un-revoke, issue a new token instead."

Three consequences:

1. **No grace period** means a revocation is a hard cutover. In-flight requests are the only thing that survives, and even that is not promised. There is no "revoked but honored for N minutes" window to drain traffic through.
2. **Irreversible.** A mistaken revocation costs you a new token, a new secret-manager write, and a new deploy.
3. **A revoked token is indistinguishable from an expired or unknown one.** Rho's own documented `detail` string merges the two ("Token is revoked or has expired"), and live responses carry no `detail` at all (section 2.6). Your incident runbook cannot ask the API which of the two happened.

Revocation, creation, and listing are **UI-only operations**. There is no documented endpoint to create, list, inspect, or revoke API Access Tokens, which means programmatic key rotation is impossible for direct customers. Rotation always requires a human in the Rho console. If your compliance regime demands automated credential rotation, this is a blocking gap, and the OAuth partner path is the only programmatic alternative (and even there, only revocation is programmatic, not issuance).

If a token leaks, Rho's instruction is to revoke it and notify Customer Support.

#### 2.2.8 Sending the credential

Verbatim from `/docs/v1/auth`:

```http
GET /api/v1/transactions HTTP/1.1
Host: rhoapi.rho.co
Authorization: Bearer rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f
Accept: application/json
```

```bash
curl -s https://rhoapi.rho.co/api/v1/transactions \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

And the exclusivity clause: "No other authentication header (cookie, API key, signed request) is supported." That claim is empirically accurate (section 2.5.2).

### 2.3 Scopes

#### 2.3.1 How many there are

Scopes use a `resource:action` format. Per `/docs/v1/auth`, they "are enforced before your request reaches the handler. A request whose token lacks the required scope is rejected with `403 Forbidden`."

The authoritative inventory is **five**, and it is confirmed by a live, unauthenticated, public metadata document:

```bash
curl -s https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1
```

Observed response (2026-09-12, HTTP 200, `application/json`, no credential required):

```json
{
  "resource": "https://rhoapi.rho.co/mcp/v1",
  "authorization_servers": ["https://auth.rho.co"],
  "bearer_methods_supported": ["header"],
  "scopes_supported": [
    "accounts:read",
    "transactions:read",
    "statements:read",
    "cards:read",
    "invoicing:read"
  ],
  "resource_documentation": "https://docs.rho.co/docs/v1/mcp"
}
```

A second, resource-wide document at `https://rhoapi.rho.co/.well-known/oauth-protected-resource` returns the same five scopes for `"resource": "https://rhoapi.rho.co"` (observed).

| Scope | In `/docs/v1/auth` table | In OpenAPI `AccessToken` | In live RFC 9728 metadata | Gates |
| --- | --- | --- | --- | --- |
| `accounts:read` | Yes | Yes | Yes | `GET /accounts`, `GET /accounts/{id}` |
| `transactions:read` | Yes | Yes | Yes | `GET /transactions`, `GET /transactions/{id}`, transaction files |
| `statements:read` | Yes | Yes | Yes | `GET /statements`, `GET /statements/{id}` |
| `cards:read` | **No** | Yes | Yes | `GET /cards`, `GET /cards/{id}` |
| `invoicing:read` | **No** | Yes | Yes | the five `/invoicing/*` operations |
| `offline_access` | **No** | **No** | **No** | OAuth only: issues a refresh token |

> **Divergence:** `/docs/v1/auth` says "the scopes available today are" and then lists exactly three: `accounts:read`, `transactions:read`, `statements:read`. The OpenAPI `AccessToken` security scheme lists five, `/docs/v1/cards` says "both endpoints require the `cards:read` scope", `/docs/v1/invoicing` says "every endpoint requires the `invoicing:read` scope", and the live RFC 9728 protected-resource metadata lists five (observed above). The auth guide's table is stale: Cards and Invoicing shipped and their scopes were propagated everywhere except the central scopes table. This matters most for partner integrations, because `/docs/v1/partner-auth` tells you to pick your requested scopes from that very table, so following the docs literally gets you a client registered for three scopes when the API has five.

> **Divergence:** `offline_access` is used as a scope throughout `/docs/v1/partner-auth` and appears in neither the auth guide's scope table nor the OpenAPI security scheme. It is an OAuth server scope, not an API scope, which is why it is absent from the protected-resource metadata, but nothing in the docs says so.

> **Divergence:** `/docs/v1/statements` mentions no required scope at all, even though `statements:read` exists in all three inventories. Do not read the absence of a scope note on an endpoint page as "no scope required".

#### 2.3.2 What a read scope does not let you do

Every scope shipped today ends in `:read`, and the API is read-only. The help center page `What connected AI tools have access to in your Rho account` enumerates the ceiling: connected tools can read Accounts (details, types, balances), Transactions (card transactions, ACH and wire transfers, refunds), and Statements; they cannot "Move money", "Issue, lock, or edit cards", "Add or manage users", or "Make changes to your Rho account." The product page repeats it: "Rho API access tokens are read-only and scoped to account and transaction data. Tokens cannot initiate payments or modify accounts."

That is a meaningful security property to carry into a risk review: a leaked Rho token is a data-disclosure incident, not a funds-movement incident, as of the v1 surface.

### 2.4 Partner authentication (OAuth 2.0)

`/docs/v1/partner-auth` covers the third-party path in full. This subsection restates it completely, then section 2.5 reports what the authorization server actually advertises.

#### 2.4.1 Registration is an email, not an endpoint

"OAuth clients are registered by Rho. To onboard as a partner, email the following details to `api-partner-request@rho.co`:"

| Field | Notes, verbatim |
| --- | --- |
| **Client / app name** | Shown to customers on the consent screen. |
| **Company name** | Your legal entity name. |
| **Logo** | Your app's logo image. Shown on the consent screen. |
| **Redirect URI(s)** | All URIs you need, production, development, local. |
| **Requested scopes** | The scopes your app needs, e.g. `accounts:read transactions:read offline_access`. |
| **Privacy policy URI** | Linked from the consent screen. |
| **Terms of Service URI** | Linked from the consent screen. |
| **Support / contact email** | Used for operational and security notices about your integration. |

"After review, Rho registers your OAuth client and sends you your `client_id` and `client_secret`."

There is no stated review SLA and no self-service path. The customer-side route is gated the same way: the help center tells a Rho customer who is asked to authorize a vendor to "forward their request to `api-partner-request@rho.co`", and says "our team will review the request and work directly with the vendor." A Rho customer therefore **cannot** authorize an arbitrary unregistered application, no matter how well-formed its authorization request is. Every partner integration passes through Rho's manual review. Plan onboarding lead time accordingly, and request all five API scopes plus `offline_access` rather than the three in the stale table.

#### 2.4.2 Step 1: the authorization request

Verbatim shape from the docs:

```text
GET https://auth.rho.co/oauth2/auth?
  response_type=code&
  client_id=<your_client_id>&
  redirect_uri=<registered_redirect_uri>&
  scope=accounts:read%20transactions:read%20offline_access&
  state=<opaque_state>&
  code_challenge=<pkce_challenge>&
  code_challenge_method=S256&
  audience=https%3A%2F%2Frhoapi.rho.co
```

| Parameter | Rule, verbatim |
| --- | --- |
| `response_type` | always `code` |
| `client_id` | issued during onboarding |
| `redirect_uri` | must exactly match a registered redirect URI |
| `scope` | space-separated subset of your registered scopes. Include `offline_access` if you need refresh tokens |
| `state` | an opaque value your app verifies on the redirect back |
| `code_challenge`, `code_challenge_method` | required. PKCE with `S256` |
| `audience` | the Rho API your app will call: `https://rhoapi.rho.co` |

Two notes on the contract. PKCE with `S256` is **required**, not optional, and `plain` is not offered by the docs. `audience` is an Ory/Auth0-style extension parameter, not core OAuth 2.0, and its value is the API **origin** `https://rhoapi.rho.co` with no `/api/v1` path.

A runnable builder that generates a correct verifier, challenge and state, and prints the URL:

```bash
RHO_CLIENT_ID=your_client_id \
RHO_REDIRECT_URI=https://yourapp.example.com/callback \
python3 - <<'PY'
import base64, hashlib, os, urllib.parse

verifier  = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b"=").decode()
challenge = base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode()
state     = base64.urlsafe_b64encode(os.urandom(24)).rstrip(b"=").decode()

params = {
    "response_type":        "code",
    "client_id":            os.environ["RHO_CLIENT_ID"],
    "redirect_uri":         os.environ["RHO_REDIRECT_URI"],
    "scope":                "accounts:read transactions:read statements:read "
                            "cards:read invoicing:read offline_access",
    "state":                state,
    "code_challenge":       challenge,
    "code_challenge_method":"S256",
    "audience":             "https://rhoapi.rho.co",
}
print("code_verifier:", verifier)
print("state:        ", state)
print("authorize_url: https://auth.rho.co/oauth2/auth?"
      + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
PY
```

Persist `code_verifier` and `state` server-side, keyed by session, before redirecting the browser.

#### 2.4.3 Step 2: consent

Verbatim: "The customer signs in to Rho, selects the business they want to connect, and grants the requested access on the consent screen. Only Account Owners and Admins can perform this action." And: "A business can have at most one active grant per app, approving again updates the existing connection."

Grant uniqueness is **one per (business, app)**, and re-consent updates rather than duplicates. One human identity can authorize several businesses, one at a time, which mirrors the business-scoped binding of API Access Tokens. Rho's help center confirms the same role gate for the Claude connector: "Only Account Owners and Administrators can authorize an OAuth connection for their business."

#### 2.4.4 Step 3: the redirect back

```text
https://yourapp.example.com/callback?code=<authorization_code>&state=<opaque_state>
```

"Verify that `state` matches the value you sent. Authorization codes are single-use and expire after a few minutes." The exact code TTL is never published.

"If the customer declines, or has no business where they are allowed to approve integrations, the redirect carries `error=access_denied` instead of a code."

Both cases collapse into one error value, so **a partner app cannot distinguish "the user declined" from "the user is not an Owner or Admin anywhere"**. Your error copy has to cover both, for example "access was not granted. If you expected this to work, check that you are an Account Owner or Admin on the business you want to connect."

#### 2.4.5 Step 4: exchange the code

Verbatim:

```http
POST /oauth2/token HTTP/1.1
Host: auth.rho.co
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <base64(client_id:client_secret)>

grant_type=authorization_code&
code=<authorization_code>&
redirect_uri=<registered_redirect_uri>&
code_verifier=<pkce_verifier>
```

Runnable:

```bash
curl -s -X POST https://auth.rho.co/oauth2/token \
  -u "$RHO_CLIENT_ID:$RHO_CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=authorization_code" \
  --data-urlencode "code=$RHO_AUTH_CODE" \
  --data-urlencode "redirect_uri=$RHO_REDIRECT_URI" \
  --data-urlencode "code_verifier=$RHO_CODE_VERIFIER"
```

(`curl -u` base64-encodes `client_id:client_secret` verbatim. RFC 6749 §2.3.1 requires both halves to be form-urlencoded before encoding, so if Rho issues you a secret containing reserved characters, build the header yourself rather than relying on `-u`.)

Documented response:

```json
{
  "access_token": "<access_token>",
  "token_type": "bearer",
  "expires_in": 900,
  "refresh_token": "<refresh_token>",
  "scope": "accounts:read transactions:read offline_access"
}
```

`expires_in: 900` is 15 minutes, consistent with the prose. `token_type` is lowercase `bearer`, while the resource server requires the literal capitalized `Bearer ` prefix in the header (section 2.5.1). Do not echo `token_type` straight into your `Authorization` header.

#### 2.4.6 Step 5: call the API

```bash
curl -s https://rhoapi.rho.co/api/v1/transactions \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Identical transport to a direct API Access Token.

#### 2.4.7 Step 6: refresh

Verbatim:

```http
POST /oauth2/token HTTP/1.1
Host: auth.rho.co
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=<refresh_token>
```

"Refresh tokens are **single-use and rotate on every refresh**: each response includes a new refresh token, and the old one stops working. Persist the new token immediately."

> **Divergence:** the same page shows three different client-authentication styles. The code exchange carries `Authorization: Basic <base64(client_id:client_secret)>` (`client_secret_basic`), the refresh sample carries **no client authentication at all**, and the revoke sample puts `client_id` and `client_secret` in the form body (`client_secret_post`). Rho never says whether refresh is a public-client call or whether the Basic header was simply dropped from the sample. A confidential client should send Basic on refresh too and verify against the sandbox of its own integration tests. The live authorization server advertises `client_secret_post`, `client_secret_basic`, `private_key_jwt` and `none` (section 2.5.3), so all three styles are plausibly accepted and the doc is simply inconsistent rather than describing three different requirements.

Rotation being single-use has a hard operational implication: **a refresh must be atomic with respect to your storage**. If two workers refresh the same token concurrently, one wins and the other has burned a token that is already invalid. Serialize refreshes per grant with a lock, write the new refresh token before returning it to the caller, and treat "refresh returned an error" as "re-consent may be required", not as "retry with the same token".

Runnable:

```bash
curl -s -X POST https://auth.rho.co/oauth2/token \
  -u "$RHO_CLIENT_ID:$RHO_CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$RHO_REFRESH_TOKEN"
```

#### 2.4.8 OAuth lifetimes

| Artifact | Lifetime | Wording, `/docs/v1/partner-auth` |
| --- | --- | --- |
| Authorization code | "a few minutes", single-use | "Authorization codes are single-use and expire after a few minutes." |
| Access token | 15 minutes (`expires_in: 900`) | "Access tokens expire after **15 minutes**." |
| Refresh token | 30 days, rolling, single-use, rotating | "Refresh tokens last **30 days** on a rolling basis, each refresh starts a new 30-day window." |
| Grant | 1 year | "The grant itself lasts **1 year**; after that the customer must re-approve your app." |

A partner that refreshes at least once every 30 days keeps access alive for up to a year with no user interaction, then must re-drive consent. An app idle for more than 30 days loses the grant early and must re-consent. If your product has seasonal users (quarter-end accounting tooling, for example) schedule a keepalive refresh inside the 30-day window rather than discovering the loss at quarter end.

#### 2.4.9 Revocation

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://auth.rho.co/oauth2/revoke \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "token=$RHO_REFRESH_TOKEN" \
  --data-urlencode "client_id=$RHO_CLIENT_ID" \
  --data-urlencode "client_secret=$RHO_CLIENT_SECRET"
```

No `token_type_hint` parameter is documented, though the endpoint accepts "access or refresh token".

Customer-side revocation, verbatim: "Customers can also disconnect your app from their Rho business settings. Customer revocation is **immediate** and invalidates all tokens for the grant, including refresh tokens, your next API request returns `401 Unauthorized`. Handle this gracefully by sending the customer through the authorization flow again."

Customer revocation surfaces to you as a plain `401`, byte-identical to an expired access token, a malformed header, or a wrong host. **Your client cannot tell revocation from expiry from the response**, so the only safe handling is: on `401`, attempt exactly one refresh; if the refresh also fails, mark the connection as needing re-consent and stop calling.

### 2.5 What probing actually shows

#### 2.5.1 Header parsing is stricter than the spec

Observed against `https://rhoapi-sandbox.rho.co/api/v1/accounts` (2026-09-12). Reproduce the whole matrix with:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
p(){ printf '%-34s ' "$1"; shift
     curl -s -o /tmp/rho.body -w '%{http_code} %{content_type}' "$@" --max-time 20
     echo "  $(head -c 60 /tmp/rho.body)"; }
p "no header"            "$B/accounts"
p "Bearer sandbox"       "$B/accounts" -H "Authorization: Bearer sandbox"
p "Bearer x"             "$B/accounts" -H "Authorization: Bearer x"
p "Bearer <empty>"       "$B/accounts" -H "Authorization: Bearer "
p "bearer lowercase"     "$B/accounts" -H "Authorization: bearer sandbox"
p "BEARER uppercase"     "$B/accounts" -H "Authorization: BEARER sandbox"
p "Basic scheme"         "$B/accounts" -H "Authorization: Basic c2FuZGJveDpzYW5kYm94"
p "Token scheme"         "$B/accounts" -H "Authorization: Token sandbox"
p "no scheme"            "$B/accounts" -H "Authorization: rhobat_abcdef"
p "double space"         "$B/accounts" -H "Authorization: Bearer  sandbox"
```

| Case | `Authorization` sent | Status | Body |
| --- | --- | --- | --- |
| No header | *(absent)* | `401` | `{"type":"2","title":"Unauthenticated","status":401}` |
| Documented sandbox token | `Bearer sandbox` | `200` | account fixture |
| One-character token | `Bearer x` | `200` | identical fixture |
| Empty credential | `Bearer ` | `401` | `{"type":"2","title":"Unauthenticated","status":401}` |
| Lowercase scheme | `bearer sandbox` | `401` | same 401 |
| Uppercase scheme | `BEARER sandbox` | `401` | same 401 |
| Wrong scheme | `Basic c2FuZGJveDpzYW5kYm94` | `401` | same 401 |
| Wrong scheme | `Token sandbox` | `401` | same 401 |
| No scheme, bare token | `rhobat_abcdef` | `401` | same 401 |
| Two spaces after scheme | `Bearer  sandbox` | `200` | identical fixture |
| Tab separator | `Bearer\tsandbox` | `401` | same 401 |
| Two `Authorization` headers | `Bearer sandbox` + `Bearer other` | `400` | Cloudflare **HTML**, `cf-ray: -` |
| Token of 8168 chars | `Bearer AAAA…` | `200` | fixture |
| Token of 8169 chars | `Bearer AAAA…` | `400` | nginx **HTML**, `Request Header Or Cookie Too Large` |

The parse is exactly: require a literal, case-sensitive `"Bearer "` (six letters plus one U+0020), take the remainder, trim surrounding whitespace, reject if empty. `Bearer  sandbox` passing and `Bearer ` plus one space failing together prove the trim runs before the emptiness test.

> **Divergence:** RFC 9110 §11.1 makes the authentication scheme token **case-insensitive**. Rho's resource server rejects `bearer` and `BEARER` with `401` (observed). A compliant HTTP client library that normalizes the scheme to lowercase will fail against this API for reasons that look like a credential problem. Always emit the exact string `Authorization: Bearer <token>`.

> **Divergence:** two of the failure modes return **HTML** from an API that documents `application/problem+json` everywhere. A duplicated `Authorization` header is killed at the Cloudflare edge (`cf-ray: -`, so it never reaches Rho) and an `Authorization` header line longer than 8190 bytes is killed by ingress-nginx with `400 Request Header Or Cookie Too Large`. Any client that calls `JSON.parse` on an error body without checking `Content-Type` first will throw on both.

The 8190-byte ceiling is nginx's default `large_client_header_buffers` of 8k, not a Rho rule, and it is reached at 8168 token characters (observed by binary search in the prior probe pass, `sandbox/probe-auth/len-*`). Real `rhobat_` tokens are ~69 characters, so this only matters if you accidentally concatenate tokens or stuff a JWT-shaped credential in.

#### 2.5.2 No other credential channel works

Every alternative returned `401 {"type":"2","title":"Unauthenticated","status":401}` (observed):

| Channel attempted | Result |
| --- | --- |
| `GET /accounts?access_token=sandbox` | `401` |
| `GET /accounts?token=sandbox` | `401` |
| `X-Api-Key: sandbox` | `401` |
| `Cookie: session=sandbox` | `401` |
| `Authorization: Basic <b64>` | `401` |
| `Authorization: Token sandbox` | `401` |

This independently confirms the docs' claim, and it is corroborated by the live protected-resource metadata field `"bearer_methods_supported": ["header"]`. Note that the query-parameter attempts return `401` rather than a `400` for an unknown parameter, because unknown query parameters are silently ignored and the request then fails auth.

#### 2.5.3 The authorization server is an Ory Hydra deployment

`GET https://auth.rho.co/.well-known/openid-configuration` returns `200 application/json` with no credential. The identical document is served at `/.well-known/oauth-authorization-server` (observed 2026-09-12).

```bash
curl -s https://auth.rho.co/.well-known/openid-configuration | python3 -m json.tool
```

| Field | Observed value |
| --- | --- |
| `issuer` | `https://auth.rho.co` |
| `authorization_endpoint` | `https://auth.rho.co/oauth2/auth` |
| `token_endpoint` | `https://auth.rho.co/oauth2/token` |
| `revocation_endpoint` | `https://auth.rho.co/oauth2/revoke` |
| `device_authorization_endpoint` | `https://auth.rho.co/oauth2/device/auth` |
| `userinfo_endpoint` | `https://auth.rho.co/userinfo` |
| `end_session_endpoint` | `https://auth.rho.co/oauth2/sessions/logout` |
| `jwks_uri` | `https://auth.rho.co/.well-known/jwks.json` (returns `200`) |
| `grant_types_supported` | `authorization_code`, `implicit`, `client_credentials`, `refresh_token`, `urn:ietf:params:oauth:grant-type:device_code` |
| `response_types_supported` | `code`, `code id_token`, `id_token`, `token id_token`, `token`, `token id_token code` |
| `response_modes_supported` | `query`, `fragment`, `form_post` |
| `code_challenge_methods_supported` | `plain`, `S256` |
| `token_endpoint_auth_methods_supported` | `client_secret_post`, `client_secret_basic`, `private_key_jwt`, `none` |
| `scopes_supported` | `offline_access`, `offline`, `openid` |
| `id_token_signing_alg_values_supported` | `RS256` |
| `subject_types_supported` | `public` |
| `claims_supported` | `sub` |
| `request_uri_parameter_supported` / `require_request_uri_registration` | `true` / `true` |
| `credentials_endpoint_draft_00` | `https://auth.rho.co/credentials` |
| `credentials_supported_draft_00` | `jwt_vc_json`, types `VerifiableCredential`, `UserInfoCredential` |
| `registration_endpoint` | **absent** |

The combination of `credentials_endpoint_draft_00` and `credentials_supported_draft_00` with `jwt_vc_json`, alongside the bare `offline` scope, backchannel and frontchannel logout, and `/oauth2/sessions/logout`, is the distinctive fingerprint of **Ory Hydra** (in this case an Ory Network hosted deployment, based on its 404 handler, see below). These are Hydra defaults rather than deliberate Rho configuration, which explains most of the divergences that follow.

`GET https://auth.rho.co/userinfo` with no credential returns `401` with a proper `WWW-Authenticate: Bearer error="request_unauthorized"` and body `{"error":"request_unauthorized","error_description":"The request could not be authorized. Check that you provided valid credentials in the right format."}` (observed). That is a different error vocabulary from the REST API's problem documents, another sign that `auth.rho.co` is an off-the-shelf component rather than Rho-authored code.

> **Divergence:** `/docs/v1/partner-auth` mandates `code_challenge_method=S256`, but the server advertises `code_challenge_methods_supported: ["plain", "S256"]`. `plain` PKCE offers no protection against code interception and an OAuth library doing capability negotiation may select it. Pin `S256` in your own code rather than letting a library choose.

> **Divergence:** the server advertises three grants the docs never mention (`implicit`, `client_credentials`, `urn:ietf:params:oauth:grant-type:device_code`) and response types that place tokens in the URL fragment (`token`, `id_token token`). These are deprecated in OAuth 2.1. Whether Rho permits them per client is not observable from outside, but the metadata will mislead any tooling that reads it. `client_credentials` in particular is what an engineer would reach for to build a server-to-server integration, and it is not part of Rho's documented model at all.

> **Divergence:** `token_endpoint_auth_methods_supported` includes `none`, meaning public clients, while `/docs/v1/partner-auth` describes only confidential clients that receive a `client_secret`.

> **Divergence:** the authorization server's `scopes_supported` lists only `offline_access`, `offline` and `openid`. **None of the five Rho API scopes appear there.** An OAuth client library that validates requested scopes against discovery metadata will reject `accounts:read` as unsupported before it ever sends a request. The API scopes are published only in the RFC 9728 protected-resource metadata on `rhoapi.rho.co` (section 2.3.1), which is a different document at a different host. If your library supports strict discovery-driven scope validation, turn it off for Rho.

> **Divergence:** the discovery document is OIDC-shaped (`openid` scope, `id_token`, `userinfo_endpoint`, `jwks_uri`, `RS256`) but `/docs/v1/partner-auth` describes a plain OAuth 2.0 flow with no ID token, no `openid` scope, and no mention of JWKS. Do not assume you can request `openid` and get a usable ID token, and do not assume the access token is a verifiable JWT. Rho documents no token format and publishes no introspection endpoint on the resource server, so **treat the access token as opaque**.

#### 2.5.4 Dynamic client registration is disabled

This is the single most consequential undocumented fact for anyone building a generic client.

Three independent observations:

1. The authorization server's metadata contains **no `registration_endpoint`** (observed above). Under RFC 8414 §2, omitting the field is how a server says it does not support RFC 7591 dynamic client registration.
2. `GET https://auth.rho.co/oauth2/register` returns `404` (observed 2026-09-12). With `Accept: application/json` the body is the Ory Network router error:

   ```json
   {
     "error": {
       "code": 404,
       "message": "Not Found",
       "reason": "The requested route does not exist. Make sure you are using the right path, domain, and port."
     }
   }
   ```

   A registration attempt against the same path on this deployment reports **"Dynamic registration is not enabled"**, which is the standard Hydra response when the feature is switched off. (Recorded in the earlier probe pass; not re-sent here, because a `POST` to a production authorization server is a write-shaped request rather than a metadata read. The `404` above is sufficient on its own.)
3. Rho's own docs are consistent with it: "OAuth clients are registered by Rho", by email, after human review.

The consequence: **an arbitrary third-party client cannot self-register and therefore cannot complete an OAuth flow against Rho on its own.** This is exactly the chain that a generic MCP client implements (protected-resource metadata → authorization-server metadata → dynamic client registration → authorization code with PKCE), and it breaks at step three. It is why Rho's MCP guide hedges with "linked-app availability depends on the client" and why Claude is described as the natively supported client today. Any other MCP or OAuth client is restricted in practice to the static API Access Token path. See the section on the MCP surface for how that plays out for tooling.

For comparison, this is a deliberate posture difference rather than an oversight: competitor documentation captured in the research corpus shows Mercury publishing `"registration_endpoint": "https://mcp.mercury.com/register"` in its own metadata, which allows self-registration.

#### 2.5.5 There is no sandbox authorization server

`auth-sandbox.rho.co`, `auth.sandbox.rho.co` and `sandbox-auth.rho.co` all fail to resolve (observed, `dig +short`, all empty). `https://rhoapi-sandbox.rho.co/.well-known/oauth-protected-resource` returns the ingress default backend `404` (`default backend - 404`, observed). The sandbox host has no `.well-known` route at all.

**The entire OAuth flow is therefore untestable before you have a real, Rho-issued `client_id`.** There is no way to rehearse consent, code exchange, refresh rotation, or revocation against fictional data. Budget for that in a partner integration plan: the first time your OAuth code runs end to end will be against production, with a real customer's consent screen.

### 2.6 401 versus 403

#### 2.6.1 The documented split

From `/docs/v1/auth`:

| Status | When it happens, verbatim |
| --- | --- |
| `401 Unauthorized` | Missing `Authorization` header, malformed token, unknown token, revoked token, or expired token. |
| `403 Forbidden` | Token is valid but does not carry the scope required by the endpoint, or the request came from an IP outside the token's allowlist. |

Decomposed:

| Condition | Status | Category |
| --- | --- | --- |
| No `Authorization` header | `401` | credential absent |
| Malformed token or header | `401` | credential unparseable |
| Unknown token | `401` | credential not recognized |
| Revoked token | `401` | credential killed |
| Expired token (either clock) | `401` | credential lapsed |
| OAuth grant revoked by the customer | `401` | credential killed |
| Valid token, missing required scope | `403` | credential good, permission insufficient |
| Valid token, source IP off the allowlist | `403` | credential good, context disallowed |

The line is "is this credential currently a credential at all" (`401`) versus "this credential is real, but not for this, from here" (`403`). Putting an IP-allowlist violation in `403` is the notable design choice: it tells a caller holding a leaked token that the token itself is live. That is a mild information leak, and simultaneously the thing that makes egress-IP drift debuggable. Treat any unexpected `403` in production as either a scope change or an egress-IP change, in that order.

#### 2.6.2 The real 401 body

Documented example, `/docs/v1/auth`:

```json
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Token is revoked or has expired"
}
```

Observed, on every `401` from both hosts:

```json
{"type":"2","title":"Unauthenticated","status":401}
```

> **Divergence:** the documented `401` body is wrong on three of its four fields. `type` is `"2"`, not `"about:blank"`. `title` is `"Unauthenticated"`, not `"Unauthorized"`. `detail` is absent entirely, so a live `401` carries **zero** diagnostic information. Reproduce with `curl -s https://rhoapi-sandbox.rho.co/api/v1/accounts`. Do not write client code that reads `detail` on a `401`, and do not match on `title == "Unauthorized"`.

> **Divergence:** the sandbox and production `401` bodies are **byte-identical** (52 bytes, md5 `a9b8c917cbc1e5b43579afaee5ccadd5`, observed by fetching both hosts unauthenticated and hashing), the header sets are identical, and both hostnames resolve to the same Cloudflare addresses. No response anywhere carries an environment marker. A misconfigured base URL pointing at production instead of sandbox produces exactly the `401` a bad sandbox token would, and since sandbox accepts any non-empty string, the developer's natural conclusion ("my token is wrong") is the wrong one. Pin the host in configuration, assert on it at startup, and log it on every auth failure.

Verify:

```bash
curl -s https://rhoapi-sandbox.rho.co/api/v1/accounts | openssl md5
curl -s https://rhoapi.rho.co/api/v1/accounts        | openssl md5
# both: a9b8c917cbc1e5b43579afaee5ccadd5
```

#### 2.6.3 No `WWW-Authenticate` on the REST API

> **Divergence:** RFC 9110 §11.6.1 states that "the server generating a 401 response MUST send a WWW-Authenticate header field". No REST `401` from `rhoapi.rho.co` or `rhoapi-sandbox.rho.co` carries one (observed, `curl -sI https://rhoapi-sandbox.rho.co/api/v1/accounts` shows zero matches). The production MCP endpoint **does** send one: `www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"`, which is RFC 9728 compliant and is what the MCP authorization spec requires. Two different auth middlewares are in play, despite `/docs/v1/mcp` asserting that MCP "uses the same API contract, authentication model, scopes, and error behavior as the REST API". The bodies match modulo JSON key ordering (`{"status":401,"title":"Unauthenticated","type":"2"}` on MCP versus `{"type":"2","title":"Unauthenticated","status":401}` on REST, so different serializers); the headers do not.

The practical fallout: a client cannot discover Rho's authorization server from a REST `401`. Discovery works only from the MCP route or from the two `.well-known/oauth-protected-resource` documents on the production host, and those documents themselves return no CORS headers, which blocks browser-based discovery.

#### 2.6.4 A non-401 does not mean you authenticated

Observed ordering: parameter type binding runs **before** authentication. With no credential at all,

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=abc'
```

returns `400` with `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}`, not `401`. Same for `GET /accounts/not-a-uuid` (`"invalid parameter: account_id"`). Range and enum validation, by contrast, runs **after** auth and uses a different shape (`{"type":"1317", ...}`). Method checking also precedes auth: `POST /accounts` with no credential returns `405` with `allow: GET`, not `401`.

Two rules follow. First, **never infer authentication success from a non-401 status**; a `400` or `405` tells you nothing about your credential. Second, an unauthenticated caller can enumerate parameter names and expected types, which is low severity because those names are public in the OpenAPI document, but it is worth knowing when reading logs.

#### 2.6.5 Scopes are not enforced in sandbox

One deliberately garbage token read every scope family successfully (observed):

| Endpoint | Documented required scope | Status |
| --- | --- | --- |
| `GET /accounts` | `accounts:read` | `200` |
| `GET /transactions` | `transactions:read` | `200` |
| `GET /statements` | `statements:read` | `200` |
| `GET /cards` | `cards:read` | `200` |
| `GET /invoicing/customers` | `invoicing:read` | `200` |
| `GET /invoicing/invoices` | `invoicing:read` | `200` |

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://rhoapi-sandbox.rho.co/api/v1/cards \
  -H "Authorization: Bearer qqqq-garbage-token-no-scopes-at-all"
# 200
```

> **Divergence:** `/docs/v1/auth` calls sandbox authentication "intentionally permissive", which a reader will take to mean the token check is relaxed while scope checks still apply. They do not. No scope is ever consulted in sandbox, and **no probe of any kind produced a `403` from either host**. The `403` path that the docs specify, the OpenAPI declares on every operation, and your production error handling depends on, cannot be exercised before you go live. The same is true of IP-allowlist rejection. Different tokens also return byte-identical data, so there is exactly one fixture tenant and no way to test multi-business handling.

Combined with the absence of rate limiting in sandbox (see the section on Rate limits), the untestable surface before production is: `403` scope rejection, `403` allowlist rejection, revoked-token `401`, expired-token `401`, `429`, and the entire OAuth flow. Write those paths defensively and review them by reading, because you cannot test them.

#### 2.6.6 The security scheme in the OpenAPI document is wrong

> **Divergence:** the OpenAPI `AccessToken` security scheme is declared `Type: oauth2` with `Token URL: https://app.rho.co/settings/access-tokens`. That URL is a human-facing browser settings page, not an OAuth 2.0 token endpoint. The real token endpoint, for the OAuth model only, is `https://auth.rho.co/oauth2/token`. The scheme conflates the two credential models, and a code generator run against this spec will emit a client that attempts an OAuth client-credentials or authorization-code flow against an HTML page. **Do not generate the auth layer from the OpenAPI document.** Hand-write the bearer header, and generate only the data models.

> **Divergence:** `/docs/v1/auth` cites RFC 7807 for `application/problem+json` while the OpenAPI overview cites RFC 9457, which obsoletes 7807. The field sets are compatible, so this is a citation inconsistency rather than a behavioral one, but it is a useful signal about how carefully the two documents are maintained relative to each other.

### 2.7 Token hygiene checklist

Storage and handling:

- [ ] Store the token in a secret manager (AWS Secrets Manager, GCP Secret Manager, Vault, 1Password). Never in source control, CI logs, or a shared doc. Rho's own guidance, and the secret is show-once so there is no recovery path.
- [ ] Copy the secret out of the creation dialog **before closing it**. There is no way to read it again.
- [ ] Redact `Authorization` in every logger, HTTP trace, and error reporter you use. A `rhobat_` token is long-lived and read-only across all five scopes if it was created broadly.
- [ ] Never put the token in a browser. The API sends no CORS headers on any status and `OPTIONS` is not in `allow: GET`, so browser use is structurally impossible cross-origin anyway (observed). Server to server only.
- [ ] Never send the token over `http://`. The plaintext endpoint answers `301` to `https://` with the full path preserved, so a client that follows redirects will have already transmitted the credential in cleartext (observed).
- [ ] Treat the token as opaque. Do not validate its length, charset, or prefix.

Issuance:

- [ ] One token per integration, never one shared token. This is what makes single-integration revocation possible and audit logs interpretable.
- [ ] Grant the narrowest scopes the integration actually needs. Do not request all five by reflex for a direct token, because the blast radius of a leak is exactly the scope set.
- [ ] Set an IP allowlist whenever the caller has stable egress. Confirm with Rho whether CIDR notation and IPv6 are accepted before assuming your range fits in 100 entries.
- [ ] Record, in your own inventory, every token's name, scopes, allowlist, expiry date and owning integration. There is no API to list tokens, so if you do not track this yourself it does not exist anywhere you can query.

Lifecycle:

- [ ] Set a calendar reminder well before the chosen expiry. Rho sends no expiry notification.
- [ ] Run an authenticated heartbeat at least weekly per token, asserting `200`, to keep the 45-day inactivity clock from firing and to surface revocation early. `GET /accounts?page_size=1` is the cheapest.
- [ ] Rotate overlap-first: create, deploy, verify, then revoke. Keep at least two slots free under the 20-token cap so you can do it.
- [ ] Have the revocation runbook written down. Revocation is immediate, irreversible, and UI-only, so it needs a named human with Owner or Admin rights, not a script.
- [ ] On suspected leak: revoke, notify Rho Customer Support, then issue a replacement. In that order.

Client behavior:

- [ ] Emit the header as the exact literal `Authorization: Bearer <token>`. One ASCII space, capital B. Lowercase `bearer` is rejected.
- [ ] Check `Content-Type` before parsing any error body. Four observed failure shapes are not JSON.
- [ ] Branch on the HTTP status, never on the problem document's `type` or `title`. See the section on Errors and status codes for why.
- [ ] On `401`: refresh once if you hold an OAuth grant, otherwise fail closed and alert. Do not retry a static token on `401`, it will never start working.
- [ ] On `403`: do not retry. Alert, and check scope configuration and egress IP.
- [ ] Assert the configured base URL at startup and log it with every auth failure. Sandbox and production `401`s are byte-identical.

OAuth partners specifically:

- [ ] Request all five API scopes plus `offline_access` at registration, not the three in the stale scopes table, unless you genuinely need fewer.
- [ ] Pin `code_challenge_method=S256` yourself. The server also advertises `plain`.
- [ ] Disable discovery-driven scope validation in your OAuth library. The authorization server's `scopes_supported` does not contain the API scopes.
- [ ] Serialize refreshes per grant and persist the rotated refresh token before anything else. Refresh tokens are single-use.
- [ ] Keep a grant alive with a refresh inside every 30-day window, and re-drive consent before the 1-year grant expiry.
- [ ] Store `state` and `code_verifier` server-side per session, and verify `state` on the callback.
- [ ] Handle `error=access_denied` as covering both "declined" and "not an Owner or Admin anywhere", because the redirect cannot distinguish them.
## 3. The sandbox

The sandbox is where you will spend your first week with this API, and it is the part of the estate most likely to teach you something false. It is a single, shared, read-only fixture set behind an authentication check that validates presence and nothing else. It does not enforce scopes, it does not enforce rate limits, it has no MCP endpoint, and its failure responses are byte-identical to production's. Everything you can learn from it about *shapes* is trustworthy. Almost everything you might infer from it about *policy* is not.

Everything in this section is either quoted from the official `docs.rho.co` corpus (labelled as such) or observed against the live host. Observed facts carry the request that produced them. The probe runs behind this section were executed on 2026-09-11 between 23:38Z and 2026-09-12 00:30Z, and the spot checks in the worked examples were re-run at the end of that window. Raw captures live under `rho/sandbox/` (`probe-auth/`, `probe-pagination/`, `probe-resources/`, `probe-filters/`, `probe-limits/`, and the full dataset walk in `full/`).

---

### 3.1 Base URL and authentication

#### 3.1.1 The two hosts

| | Sandbox | Production |
|---|---|---|
| Base URL | `https://rhoapi-sandbox.rho.co/api/v1` | `https://rhoapi.rho.co/api/v1` |
| Credential | any non-empty bearer token | a real `rhobat_`-prefixed API Access Token |
| MCP endpoint | **none** (404) | `https://rhoapi.rho.co/mcp/v1` |
| DNS A records | `104.18.26.176`, `104.18.27.176` | **the same pair** |
| TLS leaf | `CN=rhoapi-sandbox.rho.co`, Google Trust Services WE1, ECDSA P-256 | `CN=rhoapi.rho.co`, same issuer |

Official docs (`docs/v1/getting-started`) give exactly one sandbox instruction:

```bash
curl https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H "Authorization: Bearer sandbox"
```

and state that "the sandbox accepts any non-empty bearer token, so you do not need to create a real API Access Token before testing requests there." `docs/v1/auth` repeats it: "Sandbox authentication is intentionally permissive so you can test API shapes against fictional data without creating a production API Access Token."

That claim is accurate, and understated. It is also the only thing the docs say about the sandbox anywhere in the corpus, aside from one line in `docs/v1/transactions` noting that sandbox file downloads contain "non-empty representative fictional documents."

#### 3.1.2 What "permissive" means exactly

The sandbox checks that the `Authorization` header value begins with the literal, case-sensitive string `Bearer ` (with one U+0020) and that what follows, after trimming surrounding whitespace, is non-empty. There is no format check, no length check below the nginx header ceiling, no charset check, and no token registry.

Observed, `GET https://rhoapi-sandbox.rho.co/api/v1/accounts` in every case:

| `Authorization` header sent | Status | Body |
|---|---|---|
| `Bearer sandbox` | `200` | full 2,558-byte account fixture |
| `Bearer rhobat_0000…0000` (production-shaped) | `200` | identical bytes |
| `Bearer zzzzz-not-a-real-token-!!!` | `200` | identical bytes |
| `Bearer x` (one character) | `200` | identical bytes |
| `Bearer two words` | `200` | identical bytes |
| `Bearer tökén-ünïcode` | `200` | identical bytes |
| `Bearer AAAA…` (1,024 chars) | `200` | identical bytes |
| `Bearer  sandbox` (two spaces) | `200` | identical bytes |
| `authorization: Bearer sandbox` (lowercase header name) | `200` | identical bytes |
| *(header absent entirely)* | `401` | `{"type":"2","title":"Unauthenticated","status":401}` |
| `Bearer ` (trailing space, empty token) | `401` | same 52 bytes |
| `Bearer  ` (token is one space) | `401` | same 52 bytes |
| `Bearer` (scheme only, no space) | `401` | same 52 bytes |
| `Authorization:` (header present, value empty) | `401` | same 52 bytes |
| `bearer sandbox` (lowercase scheme) | `401` | same 52 bytes |
| `BEARER sandbox` (uppercase scheme) | `401` | same 52 bytes |
| `Bearer\tsandbox` (tab separator) | `401` | same 52 bytes |
| `rhobat_abcdef0123456789` (no scheme) | `401` | same 52 bytes |
| `Basic c2FuZGJveDpzYW5kYm94` | `401` | same 52 bytes |
| `Token sandbox` | `401` | same 52 bytes |
| two `Authorization` headers | `400` | Cloudflare HTML, `cf-ray: -` (killed at the edge) |
| `Bearer AAAA…` (8,169 chars or more) | `400` | nginx HTML, `400 Request Header Or Cookie Too Large` |

Reproduce the two ends of that table:

```bash
# 200 with a token that is obviously not a credential
curl -s -o /dev/null -w '%{http_code}\n' \
  https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H 'Authorization: Bearer zzzzz-not-a-real-token-!!!'
# -> 200

# 401 with an empty bearer value
curl -s -w '\n%{http_code}\n' \
  https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H 'Authorization: Bearer '
# -> {"type":"2","title":"Unauthenticated","status":401}
#    401
```

Three consequences worth internalising before you write a line of client code.

**The scheme match is case-sensitive and space-sensitive.** `bearer`, `BEARER` and `Bearer<tab>` all fail. RFC 9110 §11.1 makes the auth scheme case-insensitive, so this is a deviation, and it is the single most likely cause of a mysterious 401 from a hand-rolled HTTP client. Send exactly `Authorization: Bearer <token>` with one ASCII space.

**Two error paths return HTML, not JSON.** A duplicated `Authorization` header is rejected by Cloudflare with an HTML body, and an oversized one by nginx with an HTML body. The exact ceiling is 8,190 bytes of header line (`"Authorization: Bearer "` is 22 bytes, so 8,168 token characters pass and 8,169 fail), which is the nginx default `large_client_header_buffers` of 8 KB. A client that unconditionally calls `JSON.parse` on an error body will throw on both.

**The 401 carries no `WWW-Authenticate` header.** RFC 9110 §11.6.1 makes it mandatory. It is absent from every REST 401 on both hosts. Production's `/mcp/v1` is the only endpoint in the estate that sends one.

> **Divergence:** `docs/v1/auth` prints this 401 body:
> ```json
> {"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}
> ```
> The live body, on sandbox and production alike, is:
> ```json
> {"type":"2","title":"Unauthenticated","status":401}
> ```
> `type` differs, `title` differs, and `detail` is absent. Three of four fields in the documented example are wrong. Do not key any logic on `title == "Unauthorized"`.

> **Divergence:** the OpenAPI schema describes the problem `type` member as "A URI reference that identifies the problem type. Example: `about:blank`." Live values on the auth, not-found and validation paths are `"2"`, `"1303"` and `"1317"`, bare numeric strings. A strictly conforming RFC 9457 client treats a non-URI `type` as `about:blank` and collapses all three into one generic type, losing the distinction entirely. Branch on the HTTP status code, not on `type`. See the Errors and Problem Details section for the full catalogue.

#### 3.1.3 Alternate credential channels

All rejected with the standard 401, confirming the docs' claim that "no other authentication header (cookie, API key, signed request) is supported":

| Channel | Result |
|---|---|
| `?access_token=sandbox` | `401` |
| `?token=sandbox` | `401` |
| `X-Api-Key: sandbox` | `401` |
| `Cookie: session=sandbox` | `401` |
| `Authorization: Basic <b64>` | `401` |
| `Authorization: Token sandbox` | `401` |

The query-parameter attempts return 401 rather than "unknown parameter" because unknown query parameters are silently ignored (see §3.6), so the request simply proceeds to the auth check with no credential.

Production's RFC 9728 discovery document independently corroborates this: `bearer_methods_supported: ["header"]`. Fetch it without any credential:

```bash
curl -s https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1
```
```json
{"resource":"https://rhoapi.rho.co/mcp/v1","authorization_servers":["https://auth.rho.co"],"bearer_methods_supported":["header"],"scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],"resource_documentation":"https://docs.rho.co/docs/v1/mcp"}
```

The same path on the sandbox host returns `default backend - 404`. The sandbox has no `.well-known` route at all.

---

### 3.2 One shared tenant, read-only

#### 3.2.1 The dataset is identical regardless of token

The token is not a tenant selector. Four different tokens produce byte-identical responses:

| Token | `/accounts` md5 | bytes |
|---|---|---|
| `sandbox` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |
| `rhobat_0000…0000` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |
| `completely-different-token-xyz` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |
| `1` | `593d7be465d362f7a9ba94fcbebbb927` | 2,558 |

Verify it yourself in two calls:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
curl -s "$B/transactions?page_size=100" -H 'Authorization: Bearer sandbox' | openssl md5
curl -s "$B/transactions?page_size=100" -H 'Authorization: Bearer x'       | openssl md5
# both -> MD5(stdin)= 0e3829abca0416ff2e2058ec9cd1f6eb
```

This confirms the docs' "fictional, deterministic data" claim and establishes something the docs never say: **there is exactly one sandbox business, and anyone who knows the hostname can read all of it.** There is no mechanism, documented or discoverable, for selecting a second tenant, an empty-state business, or an error-state business. No magic tokens, no `?scenario=` parameter, no seeded failure accounts. What you see is what everyone sees.

#### 3.2.2 The dataset is read-only, and 405 precedes authentication

Every write method on every path returns `405 Method Not Allowed` with `allow: GET` and a zero-byte body:

| Method | `/accounts` | `/accounts/{id}` | `/transactions/{id}` | `/invoicing/invoices/{id}` | `/transactions/{id}/files/{fid}` | `/invoicing/customers` |
|---|---|---|---|---|---|---|
| POST | 405 | 405 | 405 | 405 | 405 | 405 |
| PUT | 405 | 405 | 405 | 405 | 405 | n/a |
| PATCH | 405 | 405 | 405 | 405 | 405 | n/a |
| DELETE | 405 | 405 | 405 | 405 | 405 | n/a |

```bash
curl -s -D- -o /dev/null -X POST https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H 'Authorization: Bearer sandbox' -H 'Content-Type: application/json' -d '{}' \
  | grep -Ei '^(HTTP|allow|content-length)'
```
```
HTTP/2 405
content-length: 0
allow: GET
```

No path advertises any write verb, so there is no hidden write surface reachable by verb probing. This is consistent with the whole v1 surface: all 14 documented operations are `GET`, and all five OAuth scopes end in `:read`.

The method check runs **before** the auth check. `DELETE /accounts/{id}` with no `Authorization` header at all returns `405`, not `401` (verified). Two practical consequences: an unauthenticated caller can enumerate which methods each path supports, and a non-401 status is **not** evidence that your token was accepted. The same holds for parameter type-binding errors, which also precede auth: `GET /accounts?page_size=abc` with no credential returns `400 {"type":"about:blank",…,"detail":"invalid parameter: page_size"}`.

The full ordering, derived from requests designed to fail several checks at once:

```
1. Cloudflare edge         duplicate Authorization -> 400 text/html, cf-ray: -
                           nonstandard method token (FOO) -> 403 WAF block page
                           TRACE -> 405 nginx-style HTML
2. Google frontend         POST/PUT without Content-Length -> 411 HTML (no `via` header)
3. ingress-nginx           path outside /api/v1 -> 404 "default backend - 404"
                           header line > 8190 bytes -> 400 "Request Header Or Cookie Too Large"
                           URI between 8 KB and 16 KB -> 414 HTML
4. Go router               unknown path under /api/v1 -> 404 "404 page not found" (text/plain)
5. Method check            -> 405 + "allow: GET", empty body
6. Parameter TYPE BINDING  -> 400 {"type":"about:blank", …, "detail":"invalid parameter: X"}
7. AUTHENTICATION          -> 401 {"type":"2","title":"Unauthenticated","status":401}
8. Handler + semantics     -> 400 {"type":"1317", …} / 404 {"type":"1303", …}
```

Those three distinct 404 surfaces are a useful debugging tool. `default backend - 404` means the request never reached the Rho application. `404 page not found` means the application was reached but no route matched. `{"type":"1303",…}` means the handler ran and the record does not exist.

#### 3.2.3 The fixtures are static, with one live exception

Repeat calls return byte-identical payloads across hours, tokens and connections. The exception is card spend windows, which are computed against the wall clock at request time: the six `monthly` cards report `spend_period_start` = `2026-09-01T04:00:00Z` and `spend_period_end` = `2026-10-01T04:00:00Z`, and the one `daily` card reported `2026-09-09T04:00:00Z` to `2026-09-10T04:00:00Z` on the probe date. The `04:00:00Z` offset is midnight America/New_York under EDT, matching the documented reset rule. Everything else in the dataset is frozen.

The other per-request computation is signed URL generation (§3.5.5), which changes the `X-Goog-Date` and `X-Goog-Signature` query parameters on `statements[].pdf_url` and on transaction file `download_url` without changing anything else.

---

### 3.3 Complete inventory of the fixture dataset

Every list endpoint below was walked to exhaustion at `page_size=100` following `page.next_page_token` until it returned `null`, then re-verified live. Every list fits in a single page at `page_size=100`.

#### 3.3.1 Record counts

| Resource | Endpoint | Records | Pages at `page_size=100` | ID space |
|---|---|---:|---|---|
| accounts | `GET /accounts` | **14** | 1 | `30000000-0000-4000-8000-0000000000NN`, NN = 01..14 |
| cards | `GET /cards` | **8** | 1 | `20000000-0000-4000-8000-0000000000NN`, NN = 01..08 |
| transactions | `GET /transactions` | **72** | 1 | UUIDv7, sequence suffix 0x01..0x48 |
| statements | `GET /statements` | **33** | 1 | 6-digit decimal strings, **not UUIDs** |
| invoicing customers | `GET /invoicing/customers` | **7** (8 with `include_deleted=true`) | 1 | `60000000-0000-4000-8000-0000000000NN`, NN = 01..08 |
| invoicing invoices | `GET /invoicing/invoices` | **12** | 1 | `70000000-0000-4000-8000-0000000000NN`, NN = 01..12 |
| transaction attachments | `GET /transactions/{id}/files/{file_id}` | **16 rows over 15 distinct file ids, on 14 transactions** | n/a | random UUIDv4 |
| invoice files | `GET /invoicing/invoices/{id}/files/{file_id}` | **9 referenced, 0 retrievable** | n/a | `50000000-0000-4000-8000-0000000000NN`, NN = 20..28 |

Reproduce the whole census in one command:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
H='Authorization: Bearer sandbox'
for p in accounts:accounts cards:cards transactions:transactions statements:statements \
         invoicing/customers:customers invoicing/invoices:invoices; do
  path="${p%%:*}"; key="${p##*:}"
  curl -s "$B/$path?page_size=100" -H "$H" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print('$path', len(d['$key']), 'next=', d['page']['next_page_token'])"
done
```
```
accounts 14 next= None
cards 8 next= None
transactions 72 next= None
statements 33 next= None
invoicing/customers 7 next= None
invoicing/invoices 12 next= None
```

Coverage was verified rather than assumed. Refetching `/transactions` filtered by each of the 14 `account_id` values, each of the 4 `status` values and each of the 5 documented `account_type` values yielded zero transaction ids absent from the unfiltered list, and each partition sums to exactly 72: by account 20+12+2+0+15+0+0+6+2+5+2+2+4+2, by status `settled` 61 + `failed` 8 + `pending` 2 + `awaiting_approval` 1, by account type `checking` 42 + `credit` 17 + `savings` 6 + `rewards` 7 + `investment` 0.

Three entity types are referenced by the payloads but have no endpoint of their own: **12 users** (`10000000-…`), **65 money movements** (`40000000-…`), and one unnamed business. `GET /users`, `/payments`, `/counterparties`, `/webhooks` and `/business` all return the bare text `404 page not found`.

#### 3.3.2 Date range

| Series | Earliest | Latest |
|---|---|---|
| `transactions.initiated_at` | `2023-05-31T07:29:00Z` | `2026-06-26T19:07:02Z` |
| `transactions.posted_at` | `2023-05-31T07:30:00Z` | `2026-06-27T19:13:15Z` |
| `statements.period_start` | `2024-07-01` | `2026-05-01` |
| `statements.period_end` | `2024-07-31` | `2026-05-31` |
| `statements.available_at` | `2024-08-01T04:02:00Z` | `2026-06-05T21:16:51Z` |
| `invoicing_customers.created_at` | `2026-01-10T09:00:00Z` | `2026-04-12T13:20:00Z` |
| `invoicing_customers.updated_at` | `2026-04-01T08:00:00Z` | `2026-07-24T16:00:00Z` |
| `invoices.created_at` | `2026-01-15T10:00:00Z` | `2026-07-10T09:00:00Z` |
| `invoices.date` (issue date) | `2026-01-15` | `2026-07-10` |
| `invoices.due_date` | `2026-02-01` | `2026-08-20` |
| `cards.spend_period_start` | `2025-03-01T12:00:00Z` | recomputed per request |
| `cards.usage_starts_at` | `2025-10-01T09:00:00Z` | (single value, 7 of 8 null) |
| `cards.usage_ends_at` | `2026-06-30T23:59:59Z` | `2026-09-01T00:00:00Z` |

The ledger is frozen: nothing in transactions, statements, invoices or customers is dated after 2026-08-20, and the newest transaction is roughly eleven weeks older than the probe date. If you build a dashboard that defaults to "last 30 days," the sandbox will show you an empty screen.

Two temporal formats appear, and they never mix within a field:

| Shape | Fields |
|---|---|
| `YYYY-MM-DDTHH:MM:SSZ` (seconds precision, always `Z`, never fractional) | `transactions.initiated_at`, `transactions.posted_at`, `statements.available_at`, `cards.spend_period_start`, `cards.spend_period_end`, `cards.usage_starts_at`, `cards.usage_ends_at`, `customers.created_at`, `customers.updated_at`, `customers.deleted_at`, `invoices.created_at`, `invoices.updated_at`, `invoices.accounting_synced_at`, `invoices.activities[].created_at` |
| `YYYY-MM-DD` (date only, no zone) | `statements.period_start`, `statements.period_end`, `invoices.date`, `invoices.due_date`, `invoices.payments[].paid_at` |

Not one timestamp in the corpus carries a sub-second component or a non-`Z` offset. A single strict parse format per field is safe against this dataset, though not necessarily against production.

#### 3.3.3 The ID scheme

`docs/v1/versioning` is explicit: "**Treat IDs as opaque strings.** Do not parse structure out of an `id` or assume a fixed format," and "Persist the full string exactly as returned, without assuming a fixed length or layout." Follow that advice. The structure below is documented here so you can reason about the fixtures, not so you can build on it.

| Prefix | Entity | Count | Trailing counter |
|---|---|---:|---|
| `10000000` | user (cardholder or initiator) | 12 | 01..12 |
| `20000000` | card | 8 | 01..08 |
| `30000000` | account | 14 | 01..14 |
| `40000000` | money movement **and** invoice activity actor (a genuine collision, see below) | 65 + 3 | 01..65 |
| `50000000` | invoice file | 9 | 20..28 |
| `60000000` | invoicing customer | 8 | 01..08 |
| `70000000` | invoice | 12 | 01..12 |

All of these parse as UUID version 4, variant RFC 4122, because the fixture generator hard-codes the version nibble `4` and the variant nibble `8`. The entropy is zero and the trailing twelve hex digits are a decimal-looking counter. Note that invoice suffixes are decimal-styled, so `…0009` is followed by `…0010` and `…000a` is a 404, while transaction suffixes are genuinely hex.

Two id families break the scheme entirely, and both matter:

- **`statements.id` is a 6-digit decimal string**, for example `"572981"` and `"152980"`. `uuid.UUID()` rejects all 33. This is the single most important trap in the surface: type it as a string, never as a UUID, and expect `GET /statements/abcdef` to return `404` rather than `400` because the endpoint performs no format validation at all.
- **`transactions.attachments[].file_id` is a genuinely random UUIDv4**, for example `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15`. Invoice `file_id` values use the structured `50000000-` prefix. File ids are not one namespace.

Statement ids come from two disjoint sequence bands, which is also the clearest evidence that the aggregation behaviour documented for statements is not exercised here:

| `statement_type` | n | ID range | Observed ids |
|---|---:|---|---|
| credit | 22 | 152980..200527 | 152980, 153670, 154411, 155137, 155915, 156744, 157603, 158472, 159417, 160431, 161396, 161929, 163022, 164322, 165954, 167766, 169823, 172111, 174810, 179033, 186996, 200527 |
| account | 4 | 428772..439951 | 428772, 433488, 439950, 439951 |
| treasury | 7 | 462701..572981 | 462701, 469372, 475381, 490851, 514051, 539240, 572981 |

Transaction ids are UUIDv7 with the random bits zeroed:

| Segment of `019f0554-0bf0-7000-8000-00000000000a` | Bits | Content | Observed |
|---|---|---|---|
| `019f0554-0bf0` | 48 | Unix epoch milliseconds, big-endian | full three-year spread |
| `7000` | 4 + 12 | version nibble `7`, then `rand_a` | `7000` on all 72, so `rand_a` is always zero |
| `8000` | 2 + 14 | variant bits, then `rand_b` high | `8000` on all 72 |
| `00000000000a` | 48 | `rand_b` low | a dense counter, exactly 1..72 with no gaps |

The embedded millisecond timestamp equals `initiated_at` exactly on 70 of 72 records. The two exceptions are the two highest sequence numbers, appended to the fixture set last with a shared base timestamp. Because the v7 prefix dominates lexicographic order, transaction ids sort by time, which is why the default list order and `sort_by=initiated_at` order coincide. Do not sort by the suffix: of 71 adjacent pairs, 15 are out of chronological order.

**A namespace collision to know about.** `transactions.money_movement_id` uses `40000000-0000-4000-8000-000000000001` through `…000065`. `invoices.activities[].user_id` uses `40000000-0000-4000-8000-000000000001`, `…000002` and `…000003`. Those three ids look like money movements 1, 2 and 3 but semantically are Rho users who acted on an invoice. Everything else in the corpus uses `10000000-` for users. The cross-check is unambiguous: 3 references, 0 resolve, 3 dangling. The invoicing product's actor ids and the banking product's user ids are not in the same namespace, so you cannot join an invoice activity to a cardholder or a transaction initiator.

#### 3.3.4 Money representation

Every `currency` field in the entire corpus, across 393 occurrences in all six resources, is `USD`. There is no non-USD record, no FX rate field, no settlement currency, and no second currency anywhere. All monetary values are **integers in minor units** (cents) inside a `{amount, currency}` object.

The only non-integer numerics in the whole dataset are `invoices.tax_rate`, `invoices.discount_rate`, `line_items[].tax_rate`, `line_items[].discount_rate` and `line_items[].quantity`. Observed values include `2.5`, `6.25` and `8.5`, so all three must be declared as float or decimal in a typed client even though most values serialize without a decimal point.

**Sign convention.** There is no `direction`, `debit_credit` or `type: debit|credit` field on a transaction. The sign of `amount.amount` is the only directional signal, and it is relative to the account named in `account_id`. Debits are negative, credits positive, and zero never occurs.

| `transaction_type` | neg | pos | min | max |
|---|---:|---:|---|---|
| `ach_credit` | 0 | 5 | 12771 | 108403 |
| `ach_debit` | 6 | 0 | -1250000 | -56250 |
| `ach_return` | 2 | 0 | -50582 | -18209 |
| `adjustment_credit` | **1** | 0 | -4500 | -4500 |
| `adjustment_debit` | 0 | **1** | 3000 | 3000 |
| `card_debit` | 8 | 0 | -1622132 | -1750 |
| `card_refund` | 0 | 4 | 1159 | 228073 |
| `check_deposit` | 0 | 3 | 100000 | 329900 |
| `check_payment` | 2 | 0 | -339100 | -339100 |
| `credit_repayment` | 3 | 3 | -1658253 | 1658253 |
| `credit_repayment_refund` | 2 | 2 | -282512 | 282512 |
| `internal_transfer` | 2 | 2 | -123987 | 123987 |
| `international_wire_fee` | 2 | 0 | -1500 | -1500 |
| `international_wire_out` | 2 | 0 | -279000 | -52142 |
| `rewards_accrual` | 0 | 4 | 764 | 108403 |
| `rewards_cashback_redemption` | 3 | 0 | -108403 | -12771 |
| `savings_deposit` | 0 | 2 | 3000000 | 130000000 |
| `savings_interest` | 0 | 2 | 225537 | 257025 |
| `savings_withdrawal` | 2 | 0 | -1000000 | -225537 |
| `wire_fee` | 1 | 0 | -1000 | -1000 |
| `wire_in` | 0 | 4 | 9929125 | 15000000 |
| `wire_out` | 4 | 0 | -5900000 | -50000 |

Totals: 40 negative, 32 positive, 0 zero. Global range `-5900000` (a failed `wire_out`) to `130000000` (a `savings_deposit`).

**`adjustment_credit` is negative and `adjustment_debit` is positive.** That is the one pair where the type name and the sign are inverted relative to every other pair. Nothing in `docs/v1/transactions` or the OpenAPI markdown defines the sign of an adjustment, so it cannot be resolved from the corpus. Read direction from the sign, never from the type name.

**Multi-leg movements are true double entry.** 65 distinct `money_movement_id` values cover 72 transactions. 58 are single-leg and 7 have exactly two legs that sum to zero:

| `money_movement_id` suffix | Type | Accounts | Amounts |
|---|---|---|---|
| `…02` | `credit_repayment` | Cash (Checking) / Credit Account | -1750 / +1750 |
| `…03` | `credit_repayment` | Cash (Checking) / Credit Account | -1658253 / +1658253 |
| `…06` | `credit_repayment` | Cash (Checking) / Credit Account | -144827 / +144827 |
| `…21` | `internal_transfer` | Cash (Checking) / Reserve Checking | -123987 / +123987 |
| `…27` | `internal_transfer` | Cash (Checking) / Reserve Checking | **+40564 / -40564** |
| `…59` | `credit_repayment_refund` | Cash (Checking) / Credit Account | +282512 / -282512 |
| `…60` | `credit_repayment_refund` | Cash (Checking) / Credit Account | +9418 / -9418 |

Movements `…21` and `…27` are both internal transfers between the same two accounts with opposite polarity, so leg order carries no meaning. Group by `money_movement_id` before presenting transfers or you will double-count every one of them. Note there is no `money_movement_id` filter on `/transactions`, so grouping has to happen client-side after a full walk.

**Statements use the opposite polarity from transactions.** On a credit statement, `spending` is positive for money spent and `repayments` is negative for money repaid, which is backwards from `card_debit` (negative) and the credit leg of `credit_repayment` (positive). The credit-statement identity holds on all 22 credit statements with no exceptions:

```
closing_balance = opening_balance + spending + repayments
```

Worked example, statement `200527` (credit, account `…008`, 2026-03-13 to 2026-04-12): `5453868 + 6931038 + (-69221) = 12315685`.

Deposit statements use a different and mutually exclusive identity, which holds on all 4 `account` and all 7 `treasury` statements:

```
closing_balance = opening_balance + total_credits - total_debits - total_fees
```

On credit statements `total_credits`, `total_debits` and `total_fees` are always `0` and carry no information. On account and treasury statements the `spending`, `repayments` and `cashback` keys are **omitted entirely**, not null. Branch on `statement_type`, or on key presence.

Cashback is a deterministic function of spending at two different rates depending on the credit account, truncated toward zero rather than floored: account `…007` runs at 1.25% (11 statements) and account `…008` at 1.50% (11 statements). `-26200` at 1.25% is `-327.5` and yields `-327`, not `-328`. Nothing in the API exposes the rate itself.

**Balances do not reconcile to the transaction list.** Summing settled transactions per account reproduces `accounts.balance.amount` on only 4 of 14 accounts, and those are the four where both sides are zero.

| Account | Name | `balance.amount` | Sum of settled txns | Match |
|---|---|---:|---:|---|
| `…001` | Reserve Checking | 1046 | 83423 | no |
| `…002` | Cash (Checking) | 876138 | 8730522 | no |
| `…003` | Cash (Checking) | 8711697 | 38721683 | no |
| `…004` | Treasury Checking | 15460929 | -4500 | no |
| `…005` | Inventory Checking | 0 | 0 | yes |
| `…006` | Primary Checking | 811970 | -457906 | no |
| `…007` | Credit Account | 0 | 0 | yes |
| `…008` | Credit Account | 0 | 0 | yes |
| `…009` | Credit Account | 0 | 25495 | no |
| `…010` | Credit Account | 0 | 0 | yes |
| `…011` | Rewards | 0 | 58255 | no |
| `…012` | Rewards | 0 | -12007 | no |
| `…013` | Savings | 0 | 2000000 | no |
| `…014` | Savings | 0 | 130257025 | no |

The transaction list is a curated sample, not a complete ledger. Do not write reconciliation tests against the sandbox. Note also that all four credit accounts and both rewards accounts report a zero balance, so the sandbox never shows what a carried credit balance looks like on `/accounts`, even though credit statements carry closing balances up to `12315685`.

#### 3.3.5 Per-resource inventories

**Accounts (14).**

| id tail | `account_type` | `account_name` | `balance.amount` | `account_number_last_4` | `routing_number_last_4` |
|---|---|---|---:|---|---|
| 01 | checking | Reserve Checking | 1046 | 0106 | 0089 |
| 02 | checking | Cash (Checking) | 876138 | 9508 | 0089 |
| 03 | checking | Cash (Checking) | 8711697 | 4609 | 0089 |
| 04 | checking | Treasury Checking | 15460929 | 7301 | 0089 |
| 05 | checking | Inventory Checking | 0 | 3608 | 0089 |
| 06 | checking | Primary Checking | 811970 | 5702 | 0089 |
| 07 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 08 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 09 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 10 | credit | Credit Account | 0 | *(omitted)* | *(omitted)* |
| 11 | rewards | Rewards | 0 | *(omitted)* | *(omitted)* |
| 12 | rewards | Rewards | 0 | *(omitted)* | *(omitted)* |
| 13 | savings | Savings | 0 | 3214 | 0089 |
| 14 | savings | Savings | 0 | 2513 | 0089 |

`account_number_last_4` and `routing_number_last_4` are **omitted, not null**, on the six credit and rewards accounts, so `/accounts` returns a four-key object for those and a six-key object for the eight deposit accounts. `account_name` is not unique. All eight deposit accounts share one routing number. "Treasury Checking" has `account_type: "checking"`, not `treasury`, and `treasury` is not a member of the accounts enum at all. Three accounts have zero transactions, and nine of the 14 appear in no statement. There is no `created_at`, `status`, `available_balance` or `credit_limit` on an account.

**Cards (8).**

| id tail | `name` | `type` | `status` | `last_4` | limit type | limit | `current_spend` | `pending_spend` |
|---|---|---|---|---|---|---:|---:|---:|
| 01 | Ethan Parker | virtual | active | 7291 | monthly | 500000 | 6797 | 1500 |
| 02 | Maya Thompson | physical | active | 1846 | monthly | 100000 | 45000 | 8000 |
| 03 | Daniel Rivera | virtual | active | 3150 | monthly | 250000 | 1750 | 250 |
| 04 | Lucas Bennett | physical | locked | 6603 | **daily** | 75000 | 6331 | 900 |
| 05 | Sofia Martin Physical Card | physical | active | **0042** | monthly | 200000 | 5331 | 400 |
| 06 | Hannah Brooks | virtual | suspended | 9027 | monthly | 2500000 | 1622132 | 50000 |
| 07 | Emma Walsh Virtual Card | virtual | canceled | 1184 | monthly | 150000 | 121827 | 0 |
| 08 | Claire Mitchell | physical | expired | 7732 | **fixed** | 500000 | 0 | 0 |

`last_4` really does carry a leading zero on card 05, and it is a string that must stay one. Merchant and MCC controls are omitted, not null, on 7 of 8 cards: exactly one card carries `allowed_categories` (`[{"code":"5812","name":"Eating places and restaurants"}]`) and `allowed_merchants` (`[{"name":"Sweetgreen"}]`), and a different single card carries `blocked_categories` (`[{"code":"0742","name":"Veterinary services"}]`) and `blocked_merchants` (`[{"name":"Petco"}]`). No card has both. MCC codes are strings with leading zeros. `shipping_address` is explicitly `null` on the four virtual cards while merchant controls are omitted, so both null idioms appear on one object. Canceled, suspended, locked and expired cards still report live, recomputed spend windows.

**Statements (33).**

| `statement_type` | n | Accounts | Period cadence | ID band |
|---|---:|---|---|---|
| `credit` | 22 | `…007` (11), `…008` (11) | `…007`: calendar months 2024-07 to 2025-05. `…008`: 13th-to-12th cycles, 2025-05-13/2025-06-12 through 2026-03-13/2026-04-12 | 152980-200527 |
| `account` | 4 | `…006` Primary Checking (3), `…013` Savings (1) | calendar months 2024-07, 2024-12, 2025-05 | 428772-439951 |
| `treasury` | 7 | `…004` Treasury Checking (7) | calendar months 2025-11 through 2026-05 | 462701-572981 |

The 33 statements resolve to only **three distinct PDF blobs**, one per statement type. Statements carry no `account_name`, no statement number, no `created_at`, and no link back to the transactions they cover.

**Transactions (72).** Presence is the whole story. The list surface returns six distinct object shapes depending on which optional keys are omitted:

| Field | Present | Omitted | Ever null when present |
|---|---:|---:|---|
| `posted_at` | 71 | **1** | no |
| `memo` | 39 | 33 | no |
| `note` | 39 | 33 | no |
| `user_id` | 38 | 34 | no |
| `user_full_name` | 38 | 34 | no |
| `card_id` | 12 | 60 | no |
| `card_name` | 12 | 60 | no |
| `counterparty_logo_url` | **0** | 72 | n/a |
| `tracking_number` | **0** | 72 | n/a |
| everything else | 72 | 0 | no |

**Not one transaction field is ever JSON `null`.** Optionality is expressed purely by key omission. `memo` and `note` are present or absent together and are byte-identical on 37 of the 39 records that have them, so the sandbox effectively models them as one field. `user_id` and `user_full_name` are present on exactly the types a person initiates and absent on exactly the system types, with no type on both sides. `card_id` and `card_name` appear on exactly the 12 `card_debit` and `card_refund` records.

**Invoicing customers (7, or 8 with `include_deleted=true`).**

| id tail | `legal_name` | `email` | `total_revenue` | `last_invoice_id` | `deleted_at` |
|---|---|---|---:|---|---|
| 01 | Acme Supplies | info@acmesupplies.com | 108403 | …02 | null |
| 02 | Brightleaf Design | hello@brightleaf.design | 43400 | …03 | null |
| 03 | Northwind Traders | orders@northwind.example | 0 | …06 | null |
| 04 | Harbor Logistics LLC | billing@harborlogistics.com | 156750 | …08 | null |
| 05 | Summit Analytics | contact@summitanalytics.io | 0 | …10 | null |
| 06 | Cedar & Co | **null** | 0 | **null** | null |
| 07 | Orbit Media Group | accounts@orbitmedia.co | 0 | …11 | null |
| 08 | Deleted Co | gone@deletedco.example | 5000 | …12 | **2026-05-01T12:00:00Z** |

Customers are the mirror image of transactions: **all 19 field paths are present on all 8 records**, and optionality is carried by nullity. `address.address2` is the empty string, not null, on the customers that lack one. `address.country` is `"USA"` (alpha-3) while `cards.billing_address.country_code` is `"US"` (alpha-2), and the two address models share no field names. `total_revenue` sums only that customer's `paid`-status invoices, which is why Northwind Traders holds 10,168,200 minor units of invoices and still reports zero.

**Invoicing invoices (12).**

| id tail | Number | Status | Total | `tax_rate` | `discount_rate` | Customer | `file_id` | `accounting_sync_status` | lines | payments | activities |
|---|---|---|---:|---|---|---|---|---|---:|---:|---:|
| 01 | INV-2026-0002 | paid | 108403 | 10 | 0 | …001 | …0020 | synced | 2 | 1 | 6 |
| 02 | INV-2026-0066 | pending_payout | 158000 | 10 | 0 | …001 | …0021 | synced | 4 | 1 | 7 |
| 03 | INV-2026-0060 | overdue | 45000 | 0 | 0 | …002 | …0022 | not_pushed | 1 | 0 | 3 |
| 04 | INV-2026-0040 | paid | 43400 | 8.5 | 0 | …002 | …0023 | synced | 1 | 1 | 4 |
| 05 | INV-2026-0045 | overdue | 72200 | 0 | 5 | …003 | …0024 | error | 1 | 0 | 3 |
| 06 | INV-2026-0065 | unpaid | 96000 | 0 | 0 | …003 | *(omitted)* | not_pushed | 1 | 0 | 2 |
| 07 | INV-2026-0043 | confirm_payment | 10000000 | 0 | 0 | …003 | …0025 | object_changed | 1 | 1 | 3 |
| 08 | INV-2026-0050 | paid | 156750 | 0 | 0 | …004 | …0026 | synced | 1 | 1 | 4 |
| 09 | INV-2026-0041 | cancelled | 22000 | 0 | 0 | …005 | *(omitted)* | skip | 1 | 0 | 2 |
| 10 | INV-2026-0070 | pending_payout | 98000 | 0 | 0 | …005 | …0027 | synced | 1 | 1 | 5 |
| 11 | INV-2026-0052 | unpaid | 45000 | 6.25 | 0 | …007 | …0028 | not_pushed | 1 | 0 | 2 |
| 12 | INV-2026-0001 | paid | 5000 | 0 | 0 | …008 | *(omitted)* | synced | 1 | 1 | 3 |

The invoice total formula, verified against all 12 records:

```
line.total    = round( unit_price.amount * quantity * (1 - line.discount_rate/100) )
invoice.total = round( SUM over lines of
                         line.total
                         * (1 - invoice.discount_rate/100)
                         * (1 + (line.tax_rate ?? invoice.tax_rate)/100) )
```

Two non-obvious parts. A null `line_items[].tax_rate` **falls back to the invoice-level `tax_rate`**, it does not mean zero: `INV-2026-0066` has four lines, two with `tax_rate: null` and two with `tax_rate: 0`, and the total is 100000×1.10 + 20000×1.10 + 20000×1.00 + 6000×1.00 = 158000. If null meant zero the total would be 146000, and 10 of the 16 line items carry a null rate. Second, discount is applied twice, once per line and once at the invoice level, with no netting. Rounding is to nearest: `INV-2026-0052` computes to 45000.0625 and reports 45000.

`file_id` is the lone omission-style field on this resource; every other optional invoice field is null when unset. `payments[]` has 0 or 1 entries and never more, so partial and multi-payment invoices are untested. `payments[].transaction_id` is populated only for `type: "received_in_account"` (2 of 7 payments), and both ids resolve into the 72-transaction set, which is the only link between Invoicing and the banking ledger.

#### 3.3.6 Relationships between records

Edges actually present in the payloads:

```
users (10000000-…, 12, no endpoint)
  |  cards.cardholder.user_id            8 of 12 users hold a card
  |  transactions.user_id                12 of 12 users initiate transactions
  v
cards (20000000-…, 8)
  |  transactions.card_id                all 8 cards appear on 12 transactions
  v
transactions (UUIDv7, 72)
  |  transactions.account_id  ---------> accounts (30000000-…, 14), 11 of 14 referenced
  |  transactions.money_movement_id ---> money movements (40000000-…, 65, no endpoint)
  |  transactions.attachments[].file_id -> GET /transactions/{id}/files/{file_id}   [works]
  ^
  |  invoices.payments[].transaction_id  2 of 12 invoices reach into the ledger
  |
invoices (70000000-…, 12)
  |  invoices.customer.id -------------> customers (60000000-…, 8)
  |  invoices.file_id -----------------> GET /invoicing/invoices/{id}/files/{fid}   [404, broken]
  |  invoices.activities[].user_id ----> 40000000-… ids that resolve to NOTHING
  ^
  |  customers.last_invoice_id           7 of 8 customers point at their newest invoice
  |
statements (6-digit decimal, 33)
  |  statements.accounts[].account_id --> accounts, 5 of 14 referenced
  (no edge to transactions in either direction)
```

Referential integrity, measured:

| Edge | Distinct refs | Resolve | Dangling |
|---|---:|---:|---:|
| `transactions.account_id` to accounts | 11 | 11 | 0 |
| `transactions.card_id` to cards | 8 | 8 | 0 |
| `statements.accounts[].account_id` to accounts | 5 | 5 | 0 |
| `customers.last_invoice_id` to invoices | 7 | 7 | 0 |
| `invoices.customer.id` to customers | 7 | 7 | 0 |
| `invoices.payments[].transaction_id` to transactions | 2 | 2 | 0 |
| `cards.cardholder.user_id` to transaction user ids | 8 | 8 | 0 |
| **`invoices.activities[].user_id` to transaction user ids** | **3** | **0** | **3** |

One broken edge, and it is the `40000000-` collision described above.

Coverage gaps worth knowing before you write assertions:

| Gap | Detail |
|---|---|
| accounts with no transaction | `…005` Inventory Checking, `…008`, `…010` |
| accounts in no statement | 9 of 14: `…001`, `…002`, `…003`, `…005`, `…009`, `…010`, `…011`, `…012`, `…014` |
| customers with no invoice | `…006` Cedar & Co, which is also the one with a null `email` and a null `last_invoice_id` |
| cards with no transaction | none, all 8 are exercised |
| users with no card | 4 of 12: Olivia Chen, Priya Shah, Grace Morgan, Andrew Collins |
| statement-to-transaction links | none, in either direction |
| invoices reaching the ledger | 2 of 12 |

The 12 users are never listable but are reconstructable from `transactions.user_id` plus `cards.cardholder`, which agree on every overlapping id:

| `user_id` | Name | Holds card |
|---|---|---|
| `10000000-…0000001` | Ethan Parker | card `…001` (virtual, active) |
| `10000000-…0000002` | Maya Thompson | card `…002` (physical, active) |
| `10000000-…0000003` | Daniel Rivera | card `…003` (virtual, active) |
| `10000000-…0000004` | Lucas Bennett | card `…004` (physical, locked) |
| `10000000-…0000005` | Olivia Chen | none |
| `10000000-…0000006` | Sofia Martin | card `…005` (physical, active) |
| `10000000-…0000007` | Hannah Brooks | card `…006` (virtual, suspended) |
| `10000000-…0000008` | Emma Walsh | card `…007` (virtual, canceled) |
| `10000000-…0000009` | Claire Mitchell | card `…008` (physical, expired) |
| `10000000-…0000010` | Priya Shah | none |
| `10000000-…0000011` | Grace Morgan | none |
| `10000000-…0000012` | Andrew Collins | none |

Card ids are not offset-aligned with user ids from card 05 onward. Do not infer the mapping from the counters.

#### 3.3.7 Enums: documented versus observed

The versioning policy warns that a new enum value can ship into `v1` at any time and that clients must have a default branch. The gap between documented and observed is therefore your real test-coverage problem.

`transaction_type`: **33 documented, 22 observed, 11 never produced.**

Observed: `ach_credit`, `ach_debit`, `ach_return`, `adjustment_credit`, `adjustment_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `credit_repayment`, `credit_repayment_refund`, `internal_transfer`, `international_wire_fee`, `international_wire_out`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`, `wire_out`.

Never produced: `card_credit`, `credit_cashback`, `international_wire_in`, `international_wire_fee_refund`, and the entire treasury family (`treasury_deposit`, `treasury_withdrawal`, `treasury_fee`, `treasury_interest`, `treasury_maturity`, `treasury_sale`, `treasury_market_value_adjustment`).

The treasury gap is the notable one. The sandbox has a "Treasury Checking" account and seven `treasury` statements, but that account's only transaction is a single `adjustment_credit` of -4500. Treasury is the product whose transaction shapes an integrator most needs and cannot see.

Every other enum:

| Field | Documented values | Observed (with counts) | Never observed |
|---|---|---|---|
| `transactions.status` | pending, settled, failed, awaiting_approval | **all 4** (2 / 61 / 8 / 1) | none |
| `accounts.account_type` | checking, credit, investment, savings, rewards | checking 6, credit 4, rewards 2, savings 2 | **investment** |
| `cards.type` | physical, virtual | physical 4, virtual 4 | none |
| `cards.status` | printing, shipped, out_for_delivery, activate_card, delivery_canceled, active, expiring, locked, canceled, suspended, expired | active 4, locked 1, canceled 1, suspended 1, expired 1 | **printing, shipped, out_for_delivery, activate_card, delivery_canceled, expiring** (the entire fulfilment pipeline) |
| `cards.spending_limit_type` | fixed, monthly, single_use, annual, daily, weekly, quarterly | monthly 6, daily 1, fixed 1 | **single_use, annual, weekly, quarterly** |
| `statements.statement_type` | account, credit, treasury | credit 22, treasury 7, account 4 | none |
| `statements.accounts[].account_type` | checking, savings, credit, treasury | credit 22, treasury 7, checking 3, savings 1 | none |
| `invoices.status` | paid, unpaid, cancelled, overdue, confirm_payment, pending_payout | paid 4, unpaid 2, overdue 2, pending_payout 2, cancelled 1, confirm_payment 1 | none |
| `invoices.accounting_sync_status` | not_pushed, synced, error, skip, object_changed | synced 6, not_pushed 3, error 1, skip 1, object_changed 1 | none |
| `invoices.activities[].activity_type` | created, sent, downloaded, matched, marked_as_paid, marked_as_unpaid, cancelled, reminder_sent, card_payment_received, accounting_synced, payment_accounting_synced | **all 11** | none |
| `invoices.payments[].type` | received_in_account, external | external 5, received_in_account 2 | none |
| `invoices.payments[].external_method` | cash, check, credit_card, other | credit_card 2, cash 1, check 1, other 1 (plus 2 nulls) | none |

Two cross-cutting traps in that table. **`cards.status` spells `canceled` with one L while `invoices.status` and `activities[].activity_type` spell `cancelled` with two.** Both are correct within their own product and both ship in the same API version, so a shared status mapper will silently miss one. And **the statements `account_type` enum is a different set from the accounts `account_type` enum**: statements use `{checking, savings, credit, treasury}`, accounts use `{checking, credit, investment, savings, rewards}`. `treasury` is a statement-level concept mapped onto a checking account.

Invoicing is by far the best-covered product in the sandbox (11 of 11 activity types across only 12 invoices). Cards fulfilment and treasury are the worst.

`transaction_type` crossed with `status`, which is what you actually need when you are picking a fixture to test a UI state against:

| Type | pending | settled | failed | awaiting_approval |
|---|---:|---:|---:|---:|
| `ach_credit` | | 5 | | |
| `ach_debit` | | 5 | | **1** |
| `ach_return` | | 2 | | |
| `adjustment_credit` | | 1 | | |
| `adjustment_debit` | | 1 | | |
| `card_debit` | **2** | 6 | | |
| `card_refund` | | 4 | | |
| `check_deposit` | | | **3** | |
| `check_payment` | | 1 | **1** | |
| `credit_repayment` | | 6 | | |
| `credit_repayment_refund` | | 4 | | |
| `internal_transfer` | | 4 | | |
| `international_wire_fee` | | 2 | | |
| `international_wire_out` | | 2 | | |
| `rewards_accrual` | | 4 | | |
| `rewards_cashback_redemption` | | 3 | | |
| `savings_deposit` | | 2 | | |
| `savings_interest` | | 2 | | |
| `savings_withdrawal` | | 2 | | |
| `wire_fee` | | 1 | | |
| `wire_in` | | 4 | | |
| `wire_out` | | | **4** | |

All four `wire_out` records and all three `check_deposit` records are `failed`. There is no settled wire out and no settled check deposit anywhere in the sandbox.

And crossed with `account_type`:

| `account_type` | Transaction types seen |
|---|---|
| `checking` | ach_credit 5, ach_debit 6, ach_return 2, adjustment_credit 1, adjustment_debit 1, check_deposit 3, check_payment 2, credit_repayment 3, credit_repayment_refund 2, internal_transfer 4, international_wire_fee 2, international_wire_out 2, wire_fee 1, wire_in 4, wire_out 4 |
| `credit` | card_debit 8, card_refund 4, credit_repayment 3, credit_repayment_refund 2 |
| `rewards` | rewards_accrual 4, rewards_cashback_redemption 3 |
| `savings` | savings_deposit 2, savings_interest 2, savings_withdrawal 2 |
| `investment` | none |

Card transactions land on `credit` accounts only. There is no `card_debit` on a checking account anywhere, so a debit-card-on-checking model is untested.

#### 3.3.8 Field-path census

Produced by walking every record on both the list and detail surfaces. `present` is occurrences of the key divided by occurrences of its containing object, so a ratio below 1.0 means the key is **omitted** on some records, which is a different failure mode from null and the single most important signal when writing a deserializer. The list and detail columns were reported separately so that any divergence would show up. None does.

| Resource | List records | Detail records | Distinct field paths |
|---|---:|---:|---:|
| accounts | 14 | 14 | 8 |
| cards | 8 | 8 | 47 |
| transactions | 72 | 72 | 22 |
| statements | 33 | 33 | 33 |
| invoicing_customers | 8 | 8 | 19 |
| invoicing_invoices | 12 | 12 | 39 |

**`accounts`**

| Field path | JSON types | present | null | n distinct | Observed values |
|---|---|---|---:|---:|---|
| `account_name` | string | 14/14 | 0 | 8 | `Cash (Checking)`, `Credit Account`, `Inventory Checking`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_number_last_4` | string | **8/14** | 0 | 8 | `0106`, `2513`, `3214`, `3608`, `4609`, `5702`, `7301`, `9508` |
| `account_type` | string | 14/14 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `balance` | object | 14/14 | 0 | | |
| `balance.amount` | int | 14/14 | 0 | 6 | `0`, `1046`, `811970`, `876138`, `8711697`, `15460929` |
| `balance.currency` | string | 14/14 | 0 | 1 | `USD` |
| `id` | string | 14/14 | 0 | 14 | `30000000-0000-4000-8000-0000000000NN`, NN = 01..14 |
| `routing_number_last_4` | string | **8/14** | 0 | 1 | `0089` |

**`transactions`**

| Field path | JSON types | present | null | n distinct | Observed values |
|---|---|---|---:|---:|---|
| `account_id` | string | 72/72 | 0 | 11 | account ids 01, 02, 03, 04, 06, 07, 09, 11, 12, 13, 14 |
| `account_name` | string | 72/72 | 0 | 7 | `Cash (Checking)`, `Credit Account`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_type` | string | 72/72 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `amount` | object | 72/72 | 0 | | |
| `amount.amount` | int | 72/72 | 0 | 64 | min `-5900000`, max `130000000` |
| `amount.currency` | string | 72/72 | 0 | 1 | `USD` |
| `attachments` | array | 72/72 | 0 | | lengths: 0 ×58, 1 ×12, 2 ×2 |
| `attachments[].file_id` | string | 16/16 | 0 | 15 | random UUIDv4 |
| `attachments[].file_name` | string | 16/16 | 0 | 15 | 14 `.pdf`, 1 `.csv` (`repayment-details.csv`) |
| `card_id` | string | **12/72** | 0 | 8 | all 8 card ids |
| `card_name` | string | **12/72** | 0 | 8 | all 8 card names |
| `counterparty_name` | string | 72/72 | 0 | 37 | `Aaron Blake` … `Zurich Airport Services`, plus `Rho`, `Rho Rewards`, `Rho Savings` and five internal account names |
| `id` | string | 72/72 | 0 | 72 | `018870b5-c260-7000-8000-000000000045` … `019f0554-0bf0-7000-8000-00000000000a` |
| `initiated_at` | string | 72/72 | 0 | 67 | `2023-05-31T07:29:00Z` … `2026-06-26T19:07:02Z` |
| `memo` | string | **39/72** | 0 | 25 | see below |
| `money_movement_id` | string | 72/72 | 0 | 65 | `40000000-0000-4000-8000-0000000000NN`, NN = 01..65 |
| `note` | string | **39/72** | 0 | 25 | identical to `memo` on 37 of 39 |
| `posted_at` | string | **71/72** | 0 | 65 | `2023-05-31T07:30:00Z` … `2026-06-27T19:13:15Z` |
| `status` | string | 72/72 | 0 | 4 | `awaiting_approval`, `failed`, `pending`, `settled` |
| `transaction_type` | string | 72/72 | 0 | 22 | see §3.3.7 |
| `user_full_name` | string | **38/72** | 0 | 12 | the 12 users |
| `user_id` | string | **38/72** | 0 | 12 | `10000000-0000-4000-8000-0000000000NN`, NN = 01..12 |

The memo corpus is worth reading once, because it tells you what the sandbox was built from: `Contractor hours`, `Correction of encoding error regarding check number 100245`, `Daily credit repayment for date 2026/06/23`, `Inventory restock`, `Invoice 317 - consulting services`, `MONEY TRANSFER`, `Monthly office rent`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00`, `PAY1001984`, `Q3 freight invoice`, `Rewards cashback`, `SC - 2509 - desk mat shipping`, `Severance payment`, `Swift OUR fee`, `Transfer to external account`, `Wire fee`, `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle`, `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`. One of those is a Postgres `timestamptz` with microseconds and an Eastern offset rendered into user-visible prose. These were lifted from a real ledger and anonymized, which is why the formats are inconsistent. Your renderer should assume memo text is arbitrary.

**`statements`**

| Field path | JSON types | present | null | n distinct | Observed values |
|---|---|---|---:|---:|---|
| `accounts` | array | 33/33 | 0 | | length 1 on **all 33** |
| `accounts[].account_id` | string | 33/33 | **0** | 5 | accounts `…004`, `…006`, `…007`, `…008`, `…013` |
| `accounts[].account_type` | string | 33/33 | 0 | 4 | `checking`, `credit`, `savings`, `treasury` |
| `accounts[].cashback` | object | **22/33** | 0 | | credit statements only |
| `accounts[].cashback.amount` | int | 22/22 | 0 | 19 | `-327` … `103965` |
| `accounts[].closing_balance.amount` | int | 33/33 | 0 | 14 | `0` … `12315685` |
| `accounts[].opening_balance.amount` | int | 33/33 | 0 | 13 | `0` … `7550175` |
| `accounts[].repayments` | object | **22/33** | 0 | | credit statements only |
| `accounts[].repayments.amount` | int | 22/22 | 0 | 10 | `-2165638` … `26200` |
| `accounts[].spending` | object | **22/33** | 0 | | credit statements only |
| `accounts[].spending.amount` | int | 22/22 | 0 | 19 | `-26200` … `6931038` |
| `accounts[].total_credits.amount` | int | 33/33 | 0 | 2 | `0`, `26200` |
| `accounts[].total_debits.amount` | int | 33/33 | 0 | 2 | `0`, `6000` |
| `accounts[].total_fees.amount` | int | 33/33 | 0 | 1 | `0` |
| `available_at` | string | 33/33 | 0 | 32 | `2024-08-01T04:02:00Z` … `2026-06-05T21:16:51Z` |
| `id` | string | 33/33 | 0 | 33 | 6-digit decimal, `152980` … `572981` |
| `pdf_url` | string | 33/33 | **0** | 3 blobs | signed GCS URL on `sandbox-statements.files.rho.co` |
| `period_end` | string | 33/33 | 0 | 29 | `2024-07-31` … `2026-05-31` |
| `period_start` | string | 33/33 | 0 | 29 | `2024-07-01` … `2026-05-01` |
| `statement_type` | string | 33/33 | 0 | 3 | `account`, `credit`, `treasury` |

The deposit-statement aggregates are essentially unexercised: `total_fees` is `0` on all 33, `total_credits` takes only `{0, 26200}` and `total_debits` only `{0, 6000}`.

**`cards`** (47 field paths; the presence-sensitive ones)

| Field path | present | null | Observed values |
|---|---|---:|---|
| `allowed_categories` / `allowed_merchants` | **1/8** | 0 | one card only |
| `blocked_categories` / `blocked_merchants` | **1/8** | 0 | a different single card |
| `billing_address` | 8/8 | 0 | always present |
| `billing_address.second_line` | **1/8** | 0 | `Floor 5` |
| `cardholder.{user_id,first_name,last_name}` | 8/8 | 0 | 8 distinct users |
| `current_spend` / `pending_spend` | 8/8 | 0 | `{amount:int, currency:"USD"}` |
| `shipping_address` | 8/8 | **4** | explicitly null on the 4 virtual cards |
| `spend_period_end` | 8/8 | **1** | null on the one `fixed` card |
| `spending_limit` / `spending_limit_type` | 8/8 | **0** | never null, so a no-limit card is untested |
| `usage_starts_at` | 8/8 | **7** | `2025-10-01T09:00:00Z` |
| `usage_ends_at` | 8/8 | **5** | `2026-06-30T23:59:59Z`, `2026-09-01T00:00:00Z` |

**`invoicing_customers`** (all 19 paths present on all 8 records; nullity carries optionality)

| Field path | present | null | Observed values |
|---|---|---:|---|
| `address.address1/city/state/zip_code` | 8/8 | 0 | 8, 8, 7, 8 distinct |
| `address.address2` | 8/8 | 0 | `<empty string>`, `Floor 2`, `Suite 400` |
| `address.country` | 8/8 | 0 | `USA` |
| `cc_emails` | 8/8 | 0 | lengths 0 ×4, 1 ×2, 2 ×2 |
| `deleted_at` | 8/8 | **7** | `2026-05-01T12:00:00Z` |
| `email` | 8/8 | **1** | 7 distinct |
| `last_invoice_id` | 8/8 | **1** | 7 distinct |
| `note` | 8/8 | **4** | 4 distinct |
| `total_revenue.amount` | 8/8 | 0 | `0`, `5000`, `43400`, `108403`, `156750` |

> **Divergence:** `api/invoicing_listinvoicingcustomers.md` marks `email` and `last_invoice_id` as `required`. Both are `null` on customer `…006` (Cedar & Co). The OpenAPI "required" marker here means "the key is always present," not "the value is non-null."

**`invoicing_invoices`** (39 paths; the presence-sensitive ones)

| Field path | present | null | Observed values |
|---|---|---:|---|
| `accounting_synced_at` | 12/12 | **5** | 7 distinct timestamps |
| `activities` | 12/12 | 0 | lengths 2 ×3, 3 ×4, 4 ×2, 5 ×1, 6 ×1, 7 ×1 (44 total) |
| `activities[].user_id` | 44/44 | **12** | `40000000-…0000001/2/3` only |
| `due_date` | 12/12 | **0** | 12 distinct |
| `file_id` | **9/12** | 0 | `50000000-…0000020` … `…0000028` |
| `line_items[].quantity` | 16/16 | 0 | `1`, `2`, `2.5`, `3` (float and int) |
| `line_items[].tax_rate` | 16/16 | **10** | `0`, `6.25`, `8.5`, `10` |
| `note` | 12/12 | **3** | 9 distinct, one containing a literal U+2014 |
| `payments` | 12/12 | 0 | lengths 0 ×5, 1 ×7 |
| `payments[].external_method` | 7/7 | **2** | `cash`, `check`, `credit_card`, `other` |
| `payments[].transaction_id` | 7/7 | **5** | two UUIDv7 ids that resolve into `/transactions` |
| `tax_rate` | 12/12 | 0 | `0`, `6.25`, `8.5`, `10` |

---

### 3.4 Sandbox versus production: the four differences that will bite you

The sandbox is a correctness environment, not a policy environment. Four differences matter more than all the rest combined.

#### 3.4.1 No scope enforcement

`docs/v1/auth` states that scopes "are enforced before your request reaches the handler" and that "a request whose token lacks the required scope is rejected with 403 Forbidden." In sandbox, no scope is ever consulted. One garbage token reads every scope family:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1
T='Authorization: Bearer qqqq-garbage-token-no-scopes-at-all'
for p in accounts cards transactions statements invoicing/customers invoicing/invoices; do
  printf '%-22s ' "$p"
  curl -s -o /dev/null -w '%{http_code} %{size_download} bytes\n' "$B/$p" -H "$T"
done
```
```
accounts               200 2558 bytes
cards                  200 6357 bytes
transactions           200 13126 bytes
statements             200 28132 bytes
invoicing/customers    200 3383 bytes
invoicing/invoices     200 15390 bytes
```

**`403` is not reachable in sandbox by any means found.** Not by scope, not by IP allowlist, not by anything. Your 403 handling, your scope-error UX and your IP-rejection path are all untestable before production.

> **Divergence:** the docs describe sandbox authentication as "intentionally permissive" and say nothing at all about scopes. A reader reasonably assumes scope checks still apply. They do not. This is the largest functional gap in the sandbox.

While you are here, note a second scope problem that the sandbox cannot help you with. `docs/v1/auth` lists exactly three scopes (`accounts:read`, `transactions:read`, `statements:read`). The OpenAPI `AccessToken` scheme, the per-product docs, and the live RFC 9728 metadata at `https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` all list **five**, adding `cards:read` and `invoicing:read`. Five is authoritative. Anyone building a partner OAuth integration from `docs/v1/auth` alone will request too few. See the Authentication and Scopes section.

#### 3.4.2 No rate limiting observed

`docs/v1/rate-limits` states: "Per API Access Token: Approximately 60 requests per minute. Per source IP: Approximately 600 requests per minute," returns `429 Too Many Requests` when exceeded, and describes branch logic on a `Retry-After` header including the unusual `Retry-After: 0` case.

Measured against the sandbox, across five independent runs from one source IP:

| Run | Requests | Concurrency | Elapsed | Effective rate | Result |
|---|---:|---:|---|---|---|
| Sequential, one connection | 60 | 1 | 10.67 s | 337 req/min | 60 × `200` |
| Parallel, separate connections | 60 | 30 | 1.173 s | 51.2 req/s | 60 × `200` |
| Parallel, separate connections | 60 | 60 | 0.871 s | **68.9 req/s (4,134 req/min instantaneous)** | 60 × `200` |
| Cumulative on one token in one 57 s window | 150+ | mixed | 57 s | >150 req/min | zero `429`, zero `5xx` |
| Sequential on a **brand-new, never-used token** | 65 | 1 | 11.30 s | 345 req/min | 65 × `200` |
| Burst to `/transactions` | 300 | 20 | 4 s | ~3,600 req/min | 300 × `200` |
| Unauthenticated burst | 75 | 1 | 17 s | ~265 req/min | 75 × `401` |
| Spot check re-run at the end of the probe window | 30 | 1 | 9 s | 200 req/min | 30 × `200` |

**Zero `429` responses across approximately 430 requests in 10.5 minutes**, including a sustained run at 2.5× the documented per-token allowance and an instantaneous burst at roughly 69× it. The fresh-token run rules out the possibility that the literal string `sandbox` is simply allowlisted.

No rate-limit headers exist on any response, on any status. No `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `X-RateLimit-*`, `RateLimit-Policy` or `Retry-After` was observed in any of roughly 430 captured responses. The complete header set on a `200` is ten headers and nothing else:

```
HTTP/2 200
date: Sat, 12 Sep 2026 00:27:36 GMT
content-type: application/json
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: a39ac991ab8caf79-EWR
```

> **Divergence:** `docs/v1/rate-limits` gives concrete thresholds with no environment qualifier, and reads as if it applies to both environments. It does not apply to the sandbox at any load this probe could responsibly generate. This is the single most load-bearing unstated caveat on that page.

> **Divergence:** the rate-limits page asserts that `429` is part of the API's behaviour, but **no OpenAPI operation page documents a `429` response**. All 14 operations list `200, 400, 401, 403, 500, 503`, and the 6 single-resource getters and the 2 file endpoints add `404`. A client generated from the OpenAPI document will treat `429` as an unexpected status. Add the case by hand.

Two things follow. You cannot test your backoff code against Rho at all: `429` is unreachable in sandbox, and probing production for it with a real token is an obviously bad idea. Write the retry path blind, unit-test it against synthetic responses, and handle a `429` that arrives with **no** `Retry-After` header, because nothing guarantees one. And do not size your client against sandbox capacity: build to the documented ~60 req/min per token, treat sandbox as a correctness environment only, and self-throttle open-loop because there is no feedback signal to pace against.

The per-source-IP limit of ~600 req/min was deliberately not probed. Reaching it would require a sustained flood against a shared multi-tenant sandbox. It is neither confirmed nor refuted.

#### 3.4.3 No MCP endpoint on the sandbox host

`docs/v1/mcp` documents `https://rhoapi.rho.co/mcp/v1` as the MCP surface, asserts that MCP "uses the same API contract, authentication model, scopes, and error behavior as the REST API," and gives a `claude mcp add` example pointing at production. It never says the sandbox lacks an MCP surface.

| Request | Sandbox | Production |
|---|---|---|
| `GET /mcp/v1` | `404` `default backend - 404` (ingress default backend, the route does not exist) | `401 application/problem+json` with `WWW-Authenticate` |
| `POST /mcp/v1` (JSON-RPC `initialize`) | `404` `default backend - 404` | `401` same body |
| `GET /mcp` | `404` `default backend - 404` | not probed |
| `GET /api/v1/mcp` | `404 page not found` (Go router reached, no route) | not probed |
| `GET /.well-known/oauth-protected-resource/mcp/v1` | `404` `default backend - 404` | `200` with the five scopes |

```bash
curl -s -w ' [%{http_code}]\n' https://rhoapi-sandbox.rho.co/mcp/v1 \
  -H 'Authorization: Bearer sandbox'
# -> default backend - 404 [404]

curl -s -D- -o /dev/null https://rhoapi.rho.co/mcp/v1 | grep -Ei '^(HTTP|www-authenticate)'
# -> HTTP/2 401
#    www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"
```

> **Divergence:** MCP cannot be exercised without a production token. There is no sandbox MCP host, no alternate path, and no statement anywhere in the docs that MCP is production-only. An integrator following the docs' sandbox-first advice and substituting the sandbox host into the MCP URL by analogy hits a bare `404` with no explanation.

There is a second, subtler divergence visible from the outside. The production MCP 401 body and the REST 401 body carry identical keys and values but in different serialization orders, and only MCP sends `WWW-Authenticate`:

```
REST /api/v1/accounts : {"type":"2","title":"Unauthenticated","status":401}   md5 a9b8c917cbc1e5b43579afaee5ccadd5
MCP  /mcp/v1          : {"status":401,"title":"Unauthenticated","type":"2"}   md5 bd60dba151c99a7227902eb6dd9a3738
```

Two serializers, therefore two implementations, behind a claim of 1:1 parity. Any client comparing error bodies byte-wise or by hash across the two surfaces will see a difference where none is semantically intended. See the MCP section.

#### 3.4.4 Production and sandbox return byte-identical 401 bodies

This is the one that costs people an afternoon.

```bash
curl -s -o /tmp/sb401.json  https://rhoapi-sandbox.rho.co/api/v1/accounts
curl -s -o /tmp/pr401.json  https://rhoapi.rho.co/api/v1/accounts
cmp /tmp/sb401.json /tmp/pr401.json && echo 'BYTE-IDENTICAL'
openssl md5 /tmp/sb401.json /tmp/pr401.json
```
```
BYTE-IDENTICAL
MD5(/tmp/sb401.json)= a9b8c917cbc1e5b43579afaee5ccadd5
MD5(/tmp/pr401.json)= a9b8c917cbc1e5b43579afaee5ccadd5
```

Same 52 bytes, same md5. The response headers are identical too, modulo `date` and `cf-ray`:

```bash
curl -s -D /tmp/hs.txt -o /dev/null https://rhoapi-sandbox.rho.co/api/v1/accounts
curl -s -D /tmp/hp.txt -o /dev/null https://rhoapi.rho.co/api/v1/accounts
diff <(grep -viE '^(date|cf-ray)' /tmp/hs.txt) <(grep -viE '^(date|cf-ray)' /tmp/hp.txt) \
  && echo 'HEADERS IDENTICAL'
# -> HEADERS IDENTICAL
```

Both hosts resolve to the same Cloudflare anycast pair (`104.18.26.176`, `104.18.27.176`), both sit behind the same Google-fronted origin stack, and both carry the same ten-header set. **There is no environment marker anywhere in any response.** No `X-Rho-Environment`, no sandbox flag in the problem document, no distinct `type` code, no difference in the `server` or `via` headers.

> **Divergence:** the documented sandbox posture is "any non-empty bearer token is accepted." A developer who typoes `RHO_API_BASE_URL` and points at production gets exactly the 401 a bad sandbox token would produce, and will reasonably conclude the *token* is wrong rather than the *host*. The docs never warn about this.

The defence is cheap: assert on the host in your client configuration, and log it on every failure.

```python
import os, urllib.parse

BASE = os.environ["RHO_API_BASE_URL"]
EXPECTED_HOST = os.environ.get("RHO_EXPECTED_HOST", "rhoapi-sandbox.rho.co")

host = urllib.parse.urlparse(BASE).netloc
if host != EXPECTED_HOST:
    raise SystemExit(f"refusing to run: base URL host is {host!r}, expected {EXPECTED_HOST!r}")
```

#### 3.4.5 Everything else that differs or is untestable

| Surface | Sandbox | Production | Documented? |
|---|---|---|---|
| Auth | any non-empty bearer | real `rhobat_` token | yes |
| Scopes | not enforced, `403` unreachable | enforced per the docs | **no** |
| Rate limits | not enforced up to 68.9 req/s, `429` unreachable | unprobed | **no** |
| `/mcp/v1` | route does not exist | exists, demands auth | **no** |
| `401` body and headers | identical to production | identical to sandbox | **no** |
| Edge IPs | `104.18.26.176`, `104.18.27.176` | the same pair | no |
| Error body families | identical | identical (on the paths reachable unauthenticated) | partially |
| IP allowlist rejection | no mechanism | documented | untestable |
| `500` / `503` | never observed | documented per operation | untestable |
| Token revocation and expiry | no token registry | documented (45-day inactivity, 1-year max) | untestable |

Of the five error responses the OpenAPI documents per operation, **three (`403`, `500`, `503`) are unreachable in sandbox**, and `401` is reachable only by deliberately breaking your own header.

---

### 3.5 Worked examples

Everything below runs as written against the live sandbox. Set these once:

```bash
export RHO_BASE=https://rhoapi-sandbox.rho.co/api/v1
export RHO_AUTH='Authorization: Bearer sandbox'
```

Send `Accept-Encoding: gzip` explicitly in anything you build. gzip is the only encoding served (brotli, zstd, deflate and `Accept-Encoding: *` all return identity), and it cuts a 40,768-byte transactions page to roughly 5.6 to 6.0 KB, a 7× saving. `curl --compressed` does this for you.

#### 3.5.1 List every resource

```bash
curl -s --compressed "$RHO_BASE/accounts"            -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/cards"               -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/transactions"        -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/statements"          -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/invoicing/customers" -H "$RHO_AUTH" | python3 -m json.tool | head -20
curl -s --compressed "$RHO_BASE/invoicing/invoices"  -H "$RHO_AUTH" | python3 -m json.tool | head -20
```

The envelope is always `{"<resource_key>": [...], "page": {"next_page_token": string|null}}`. The resource key is **not** the path: `/invoicing/customers` returns the bare key `customers` and `/invoicing/invoices` returns `invoices`.

| Endpoint | Resource key | Rows | Default page size | Default ordering (observed) |
|---|---|---:|---|---|
| `/accounts` | `accounts` | 14 | 20 (unobservable, dataset is smaller) | `account_name` ascending |
| `/cards` | `cards` | 8 | 20 (unobservable) | card id order |
| `/transactions` | `transactions` | 72 | **20, proven** | `initiated_at` descending |
| `/statements` | `statements` | 33 | **20, proven** | `period_end` descending |
| `/invoicing/customers` | `customers` | 7 | 20 (unobservable) | `created_at` descending |
| `/invoicing/invoices` | `invoices` | 12 | 20 (unobservable) | `created_at` descending |

`/accounts` is the only endpoint whose default sort is discoverable from the API itself, because its cursor payload spells it out (§3.5.3). The docs never state it.

#### 3.5.2 Page a resource explicitly

```bash
# page_size is bounded [1, 100] on every endpoint
curl -s "$RHO_BASE/transactions?page_size=1"   -H "$RHO_AUTH" | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]))'   # 1
curl -s "$RHO_BASE/transactions?page_size=100" -H "$RHO_AUTH" | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]))'   # 72
```

Changing `page_size` mid-walk is safe, because `page_size` is deliberately excluded from the cursor's filter fingerprint. Changing a **filter** mid-walk is not, and returns `400`. Neither fact appears in the docs.

#### 3.5.3 Follow a cursor to exhaustion

The canonical loop, which works verbatim on all six endpoints:

```python
#!/usr/bin/env python3
"""Walk any Rho list endpoint to exhaustion. Usage: walk.py transactions transactions"""
import json, os, sys, time, urllib.request, urllib.parse

BASE  = os.environ.get("RHO_BASE", "https://rhoapi-sandbox.rho.co/api/v1")
TOKEN = os.environ.get("RHO_TOKEN", "sandbox")

def get(path, params):
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept-Encoding": "gzip",
    })
    with urllib.request.urlopen(req) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip
            raw = gzip.decompress(raw)
        return json.loads(raw)

def walk(path, key, page_size=100, **filters):
    """Yield every record. Filters must stay byte-identical across pages."""
    token, seen = None, 0
    while True:
        params = dict(filters, page_size=page_size)
        if token:
            params["page_token"] = token
        body = get(path, params)
        rows = body[key]
        seen += len(rows)
        yield from rows
        token = body["page"]["next_page_token"]   # present always, null on the last page
        if token is None:
            return
        time.sleep(1.0)   # self-throttle: ~60 req/min, the documented production budget

if __name__ == "__main__":
    path, key = sys.argv[1], sys.argv[2]
    rows = list(walk(path, key))
    ids  = [r["id"] for r in rows]
    print(f"{path}: {len(rows)} records, {len(set(ids))} distinct ids")
```

```bash
python3 walk.py transactions transactions        # transactions: 72 records, 72 distinct ids
python3 walk.py statements statements            # statements: 33 records, 33 distinct ids
python3 walk.py invoicing/customers customers    # invoicing/customers: 7 records, 7 distinct ids
```

Three properties of the termination condition, all verified by walking every endpoint at `page_size` 1, 3, 7 and 100:

- `page.next_page_token` is **always present** and is either a string or JSON `null`. It is never an empty string and never omitted. The API reference types it as `string, required`, which a strict schema validator will reject on the terminal page.
- The concatenated id sequence is byte-for-byte identical at every page size, with no duplicates and no skips.
- When the row count divides evenly into `page_size`, the last full page still carries a token and the next request returns an empty array with a null token. `/cards?page_size=4` (total 8) returns 4 rows **with** a token on page 1.

The cursor is not opaque in practice, which is worth seeing once so you know what you are carrying:

```bash
T=$(curl -s "$RHO_BASE/transactions?page_size=5" -H "$RHO_AUTH" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["page"]["next_page_token"])')
echo "$T"
python3 - "$T" <<'PY'
import base64, json, sys
d = lambda s: base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
env = json.loads(d(sys.argv[1]))
print(env)
print("inner:", d(env["t"]))
PY
```
```
eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qVSJ9
{'v': 1, 'f': 't0HwRhJ0BSGWYAjAT5bQKg', 't': 'b2Zmc2V0OjU'}
inner: b'offset:5'
```

The same on `/accounts`:

```
{'v': 1, 'f': 'SigraTvwZG8Dd7QLdKJzPA', 't': 'eyJsYXN0X2lkIjoiMzAwMDAwMDAtMDAwMC00MDAwLTgwMDAtMDAwMDAwMDAwMDAzIiwic29ydF9ieSI6ImFjY291bnRfbmFtZSIsIm9yZGVyIjoiYXNjIn0'}
inner: b'{"last_id":"30000000-0000-4000-8000-000000000003","sort_by":"account_name","order":"asc"}'
```

| Endpoint | Inner cursor | Strategy |
|---|---|---|
| `/transactions`, `/statements`, `/cards`, `/invoicing/customers`, `/invoicing/invoices` | `offset:N` | **offset** |
| `/accounts` | `{"last_id":…,"sort_by":"account_name","order":"asc"}` | **keyset** |

> **Divergence:** `docs/v1/pagination` states without qualification that "cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." Five of six endpoints return a plain absolute offset, which cannot deliver that guarantee: an insert or delete before the current offset shifts every subsequent row. Only `/accounts` uses a keyset cursor that structurally can. The sandbox dataset is static so the shift cannot be forced here, but the mechanism is dispositive.

> **Divergence:** the same page describes cursors as "opaque" whose "format and lifetime are not part of the API contract," and prints an example token that decodes to `{"o":100,"d":"2026-05-14"}`. Real tokens decode to `{"v":1,"f":…,"t":…}`. The documented shape matches nothing the API emits.

Cursor binding, probed directly:

| Action | Result |
|---|---|
| pass a `/transactions` token to `/statements` | `400` `page_token must be a valid cursor` |
| pass a token back with a **different `page_size`** | **`200`**, works fine |
| pass a token back with an **added filter** (`status=settled`) | `400` |
| pass a token back with the **explicit default** (`sort_by=initiated_at&order=desc`) | `200`, values are canonicalized before hashing |
| pass a token back with `order=asc` changed to `order=ASC` | **`400`**, identical rows, incompatible cursors |
| pass a token back with a duplicated identical enum value | **`400`** |
| pass a token back with an added unknown parameter | `200` |
| `page_token=` (empty string) | `200`, treated as page one |
| garbage string | `400` `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |

Tokens minted at 19:22Z still resolved at 00:03Z the next day, about 4 h 41 m later, with no expiry observed.

#### 3.5.4 Fetch a single record

```bash
curl -s "$RHO_BASE/accounts/30000000-0000-4000-8000-000000000002"     -H "$RHO_AUTH"
curl -s "$RHO_BASE/cards/20000000-0000-4000-8000-000000000001"        -H "$RHO_AUTH"
curl -s "$RHO_BASE/transactions/019f0554-0bf0-7000-8000-00000000000a" -H "$RHO_AUTH"
curl -s "$RHO_BASE/statements/572981"                                 -H "$RHO_AUTH"
curl -s "$RHO_BASE/invoicing/customers/60000000-0000-4000-8000-000000000001" -H "$RHO_AUTH"
curl -s "$RHO_BASE/invoicing/invoices/70000000-0000-4000-8000-000000000001"  -H "$RHO_AUTH"
```

Detail responses are the **bare resource object with no envelope and no `page` key**, confirmed on all 147 detail fetches.

**The detail surface returns exactly the same field set as the list surface for every one of the six resources.** 14/14 accounts, 8/8 cards, 72/72 transactions, 33/33 statements, 7/7 customers (8/8 with include_deleted=true), 12/12 invoices: identical field paths, identical presence, identical nullity, zero value differences. There is no expanded detail representation.

```bash
# Prove it for one account
A=30000000-0000-4000-8000-000000000002
diff <(curl -s "$RHO_BASE/accounts" -H "$RHO_AUTH" \
        | python3 -c "import sys,json;d=json.load(sys.stdin)['accounts'];print(json.dumps([a for a in d if a['id']=='$A'][0],sort_keys=True,indent=2))") \
     <(curl -s "$RHO_BASE/accounts/$A" -H "$RHO_AUTH" \
        | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin),sort_keys=True,indent=2))") \
  && echo 'IDENTICAL'
```

Looping single GETs to "enrich" list rows is pure waste, and at ~60 req/min per token in production it is the fastest way to burn your budget for no gain. The only reason to call `GET /{id}` is to refresh a signed `pdf_url` on a statement, and even that is subject to a server-side signing cache (§3.5.5).

One trap on the transaction detail route. `GET /transactions/{id}` accepts an optional `account_id` query parameter that the docs describe only as "Account ID for the transaction." It is not a hint, it is an **assertion filter**:

| Request | Status |
|---|---|
| `?account_id=<the transaction's real account>` | `200`, full body |
| `?account_id=<a different real account>` | **`404` `transaction not found`** |
| `?account_id=abc` | `400 invalid parameter: account_id` |

Passing a stale or guessed `account_id` makes an existing transaction vanish. The docs do not say this. Omit the parameter unless you are certain.

#### 3.5.5 Fetch a file and its signed URL

Find a transaction with an attachment, exchange the `file_id` for a signed URL, then download it:

```bash
read TID FID FN < <(
  curl -s "$RHO_BASE/transactions?page_size=100" -H "$RHO_AUTH" | python3 -c '
import sys, json
for t in json.load(sys.stdin)["transactions"]:
    if t["attachments"]:
        a = t["attachments"][0]
        print(t["id"], a["file_id"], a["file_name"]); break
')
echo "$TID $FID $FN"
# 019f0554-0bf0-7000-8000-00000000000a 2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15 parking-receipt.pdf

curl -s "$RHO_BASE/transactions/$TID/files/$FID" -H "$RHO_AUTH" | python3 -m json.tool
```
```json
{
    "download_url": "https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=file-service%40pledge-218909.iam.gserviceaccount.com%2F20260912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260912T002649Z&X-Goog-Expires=899&X-Goog-Signature=092cde4c…&X-Goog-SignedHeaders=host",
    "file_id": "2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15",
    "file_name": "parking-receipt.pdf"
}
```

The response is exactly three keys. There is no size, MIME type, upload timestamp or uploader. Now download it, with **no** `Authorization` header, because the signature is the credential:

```bash
U=$(curl -s "$RHO_BASE/transactions/$TID/files/$FID" -H "$RHO_AUTH" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["download_url"])')
curl -s -o /tmp/attachment.pdf -w 'status=%{http_code} type=%{content_type} bytes=%{size_download}\n' "$U"
head -c 8 /tmp/attachment.pdf; echo
```
```
status=200 type=application/pdf bytes=769
%PDF-1.4
```

Signed URL anatomy, identical on both file classes:

| Component | Value |
|---|---|
| Host, transaction attachments | `rho-api-sandbox.files.rho.co` |
| Host, statement PDFs | `sandbox-statements.files.rho.co` |
| Path | `/{24 hex chars}.{ext}`, content-addressed, no account or transaction identifier |
| `X-Goog-Algorithm` | `GOOG4-RSA-SHA256` |
| `X-Goog-Credential` | `file-service@pledge-218909.iam.gserviceaccount.com/YYYYMMDD/auto/storage/goog4_request` |
| `X-Goog-Date` | signing instant, second granularity |
| `X-Goog-Expires` | **`899`** seconds (14 min 59 s), on every URL observed |
| `X-Goog-SignedHeaders` | `host` |

The expiry rule is exactly `X-Goog-Date + X-Goog-Expires`, enforced by Google Cloud Storage. Both values are readable from the URL with no network call, so parse them to decide whether a URL is still worth attempting rather than discovering expiry from a failed download. Tampering behaves as you would expect: altering the last hex character of the signature gives `403 SignatureDoesNotMatch`, stripping the query string gives `403 AccessDenied`, and forcing `X-Goog-Expires=1` gives `400 ExpiredToken` with the exact deadline in the message. The URLs are not single-use, they honour `HEAD`, and they honour `Range` (a `Range: bytes=0-9` returns `206` with 10 bytes).

Two asymmetries matter:

- **Transaction attachment URLs are minted fresh on every request**, always with a full 899 s window. The docs are accurate here.
- **Statement `pdf_url` values are served from a roughly 300 s server-side signing cache**, keyed on the PDF blob rather than the statement. Repeated `GET /statements/{id}` inside that window returns a byte-identical URL. Because the cache rotates roughly 10 minutes before expiry, residual life is bounded between about 599 s and 899 s, with an observed minimum of 606 s.

> **Divergence:** `api/statements_getstatement.md` says "if the link lapses, re-fetch the statement with `GET /statements/{id}` to obtain a fresh URL." Re-fetching does not mint a URL on demand; it returns whatever the cache holds. Because the cache always rotates well before expiry the remedy usually works in practice, but not by the mechanism described, and **a client cannot force a re-sign**. On a `400 ExpiredToken`, back off past the ~300 s cache TTL rather than retrying tightly.

Also note that a single `/statements` list response can carry URLs signed at three different instants, because the 33 statements resolve to only three distinct PDF blobs and each blob has its own cache entry. And the GCP project name `pledge-218909` leaks in the credential parameter of every signed URL Rho issues.

**Invoice files are broken in the sandbox.** All nine invoices that expose a `file_id` return `404` from the endpoint the docs instruct you to call:

```bash
curl -s -w ' [%{http_code}]\n' \
  "$RHO_BASE/invoicing/invoices/70000000-0000-4000-8000-000000000010/files/50000000-0000-4000-8000-000000000027" \
  -H "$RHO_AUTH"
# -> {"type":"1303","title":"invoice file not found","status":404} [404]
```

> **Divergence:** `docs/v1/invoicing` says "when an invoice has a PDF, `file_id` is present. Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`," and `api/invoicing_getinvoicinginvoicefile.md` adds that `file_id` "must match `invoice.file_id` from list or get when that field is set." Doing exactly that returns 404 on all 9. The route itself is wired up (a malformed `file_id` returns `400`, proving the handler runs), so this is a fixture-data gap. **Invoice PDF retrieval cannot be integration-tested against this sandbox at all.**

#### 3.5.6 Trigger each error class deliberately

Every error class the sandbox can produce, with the exact request that produces it. Run the whole block to populate your test fixtures.

```bash
# 401  missing credential (problem+json, 52 bytes)
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts"

# 400  type-binding failure, "about:blank" family with a `detail` field. PRE-AUTH.
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts?page_size=abc"  -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts/not-a-uuid"     -H "$RHO_AUTH"

# 400  semantic validation, "1317" family with no `detail` field. POST-AUTH.
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/transactions?page_size=101"    -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/transactions?page_token=garbage" -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts?order=ASC"             -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts?sort_by=bogus"         -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/cards?status=bogus"             -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/transactions?min_amount=10000&max_amount=-10000" -H "$RHO_AUTH"

# 404  unknown id, "1303" family
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/accounts/00000000-0000-4000-8000-000000000000" -H "$RHO_AUTH"
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/statements/999999" -H "$RHO_AUTH"

# 404  unknown route, text/plain, NOT problem+json
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/webhooks" -H "$RHO_AUTH"

# 404  outside the mount point, ingress default backend, text/plain
curl -s -w ' [%{http_code}]\n' https://rhoapi-sandbox.rho.co/mcp/v1 -H "$RHO_AUTH"

# 405  write method, EMPTY body, `allow: GET`
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$RHO_BASE/accounts" \
  -H "$RHO_AUTH" -H 'Content-Type: application/json' -d '{}'

# 405  HEAD is not supported even though GET is
curl -s -o /dev/null -w '%{http_code}\n' -I "$RHO_BASE/accounts" -H "$RHO_AUTH"

# 411  POST with no Content-Length, HTML from the Google frontend
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$RHO_BASE/accounts" -H "$RHO_AUTH"
```

Observed output:

```
{"type":"2","title":"Unauthenticated","status":401} [401]
{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"} [400]
{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"} [400]
{"type":"1317","title":"page_size must be between 1 and 100","status":400} [400]
{"type":"1317","title":"page_token must be a valid cursor","status":400} [400]
{"type":"1317","title":"invalid order parameter: \"ASC\"","status":400} [400]
{"type":"1317","title":"invalid sort_by parameter: \"bogus\"","status":400} [400]
{"type":"1317","title":"invalid status parameter: \"bogus\"","status":400} [400]
{"type":"1317","title":"min_amount must be less than or equal to max_amount","status":400} [400]
{"type":"1303","title":"account not found","status":404} [404]
{"type":"1303","title":"statement not found","status":404} [404]
404 page not found [404]
default backend - 404 [404]
405
405
411
```

The complete error taxonomy reachable from the sandbox:

| Class | Status | `Content-Type` | Body | `detail`? |
|---|---|---|---|---|
| Missing or malformed credential | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` | no |
| Unknown id on a detail route | `404` | `application/problem+json` | `{"type":"1303","title":"<resource> not found","status":404}` | no |
| Parameter fails type binding (pre-auth) | `400` | `application/problem+json` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: X"}` | **yes** |
| Parameter fails a rule (post-auth) | `400` | `application/problem+json` | `{"type":"1317","title":"<message>","status":400}` | no |
| Unknown path under `/api/v1` | `404` | `text/plain; charset=utf-8` | `404 page not found` | **not a problem document** |
| Path outside `/api/v1` | `404` | `text/plain; charset=utf-8` | `default backend - 404` | **not a problem document** |
| Wrong method | `405` | *(none)* | *(empty, `content-length: 0`)*, `allow: GET` | **not a problem document** |
| `POST`/`PUT` with no `Content-Length` | `411` | `text/html; charset=UTF-8` | Google frontend page | **not a problem document** |
| URI over ~8 KB | `414` | `text/html` | nginx page | **not a problem document** |
| `Authorization` header over 8,190 bytes | `400` | `text/html` | nginx page | **not a problem document** |
| Duplicate `Authorization` header | `400` | `text/html` | Cloudflare page | **not a problem document** |
| Nonstandard method token (`FOO`) | `403` | `text/html; charset=UTF-8` | Cloudflare WAF block page | **not a problem document** |

**Seven of those twelve are not JSON.** Branch on `Content-Type` before parsing, always.

Two additional points on the `1303` and `1317` codes. `1303` covers at least nine distinct not-found conditions (`account`, `card`, `transaction`, `statement`, `customer`, `invoice`, `transaction file`, `invoice file`), distinguished only by the prose `title`. `1317` covers page size, cursor validity, sort field, order, card type, card status and amount ordering. Neither is precise enough to branch on, and `title` is free prose outside the versioning contract. Branch on the HTTP status code. See the Errors and Problem Details section.

Finally, note what you **cannot** trigger: `403`, `422`, `429`, `500` and `503` are all unreachable in the sandbox.

---

### 3.6 Sandbox gotchas

#### 3.6.1 Unknown query parameters are silently ignored

No endpoint ever returns `400` for an unrecognized parameter name. `limit`, `offset`, `per_page`, `size`, `pageSize`, `PAGE_SIZE`, `q`, `query`, `filter`, `expand`, `fields`, `include`, `id`, `currency`, `money_movement_id`, `timezone`, `account_id[]`, and 300 numbered junk parameters in a single URL all return a full, unfiltered `200`.

```bash
curl -s "$RHO_BASE/transactions?limit=5&offset=10&per_page=2&nonsense=x" -H "$RHO_AUTH" \
  | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]),"rows")'
# -> 20 rows
```

Twenty rows, because `limit` does nothing and the default `page_size` of 20 applied. This is exactly how a careless census concludes that the sandbox holds 20 statements rather than 33: `?limit=100` looks like it worked and quietly returns the first default page. The parameter is `page_size`, and the endpoint will never tell you otherwise.

Parameter names are also **case-sensitive** (`PAGE_SIZE` and `pageSize` are ignored), while percent-encoded names are decoded and honoured (`?page%5Fsize=3` returns 3 rows).

A related and nastier variant: **a raw semicolon makes a whole key/value pair vanish.** `?status=settled;x=1&page_size=3` silently drops the entire `status` filter and returns the default fingerprint. That is Go's `url.ParseQuery` rejecting semicolon-separated pairs, and it is a second silent-filter-loss vector.

#### 3.6.2 An empty date filter value returns 200 with zero rows

This is the most dangerous behaviour in the sandbox, because it fails silently in exactly the direction that looks like real data.

```bash
for q in 'initiated_before=' 'initiated_after=' 'posted_before=' 'status=' 'account_type='; do
  printf '%-20s ' "$q"
  curl -s "$RHO_BASE/transactions?$q" -H "$RHO_AUTH" \
    | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]),"rows")'
done
```
```
initiated_before=    0 rows
initiated_after=     20 rows
posted_before=       0 rows
status=              0 rows
account_type=        0 rows
```

The mechanism: an empty date string is coerced to the zero time `0001-01-01T00:00:00Z`. `field >= zero` is universally true, so every `*_after=` is a no-op. `field < zero` is universally false, so every `*_before=` empties the result set. An empty enum string becomes a literal filter value that matches nothing.

The complete empty-value table, which is worth pinning above your desk:

| Parameter | Empty value result |
|---|---|
| `initiated_after=`, `posted_after=`, `period_end_after=`, `period_start_after=`, `date_after=`, `due_date_after=` | **ignored**, full result set |
| `initiated_before=`, `posted_before=`, `period_end_before=`, `period_start_before=`, `date_before=`, `due_date_before=` | **`200` with 0 rows** |
| `account_type=`, `transaction_type=`, `status=`, `statement_type=` | **`200` with 0 rows** |
| `account_id=`, `user_id=`, `card_id=` | `400` |
| `page_size=`, `min_amount=`, `max_amount=` | `400` |
| `include_deleted=` | `400` |
| `search=`, `search=%20` | ignored, full result set |
| `page_token=` | ignored, page one |
| `sort_by=` | `/accounts` and `/invoicing/customers`: `400`. `/transactions` and `/statements`: accepted, no effect |

A templated URL with an undefined variable produces an empty page, not an error, and your reconciliation job reports "no activity." **Build the query string conditionally.** Never interpolate a possibly-empty value into a `*_before` parameter.

The corollary is that `200 []` is ambiguous between "no matching data" and "your filter was silently dropped or nullified." When a filtered result comes back empty, assert against an unfiltered control query before believing it.

#### 3.6.3 `page_size` is bounded [1, 100] with error type `1317`

Probed exhaustively on `/transactions`, then confirmed identical on all six endpoints.

| `page_size` | Status | Body |
|---|---|---|
| `1` .. `100` | `200` | normal |
| `0`, `-1`, `-5`, `-0`, `101`, `150`, `200`, `1000`, `10000`, `999999`, `99999999999999999999` | `400` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| `abc`, `1.5`, `2.0`, `1e2`, `0x10`, `true`, `null`, `%20`, `3#`, empty, duplicated | `400` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}` |
| `%2B3` (leading `+`) | `200` | parsed as **3** |
| `03` (leading zero) | `200` | parsed as **3** |
| `page_size[]=5` (bracket syntax) | `200` | key ignored, falls back to the default 20 |

Note the split: a value that parses as an integer but falls outside the range gets the `1317` family, and a value that does not parse at all gets the `about:blank` family with a `detail` field. Two different producers, two different shapes, one HTTP status.

> **Divergence:** `docs/v1/pagination` says only that "values outside the allowed range return `400 Bad Request`." It does not distinguish the two error shapes, does not state the minimum, and the API reference pages for `/cards`, `/invoicing/customers` and `/invoicing/invoices` say only "Defaults to 20" without naming a maximum. The enforced range is `[1, 100]` uniformly, discoverable only by probing.

#### 3.6.4 Validation is inconsistent across endpoints

This is the deepest gotcha, because it means you cannot learn one rule and apply it everywhere.

**Enum filter validation.** Three endpoints reject a bad value and three accept it and return zero rows:

| Probe | Result |
|---|---|
| `/cards?status=bogus` | `400` `{"type":"1317","title":"invalid status parameter: \"bogus\"","status":400}` |
| `/cards?type=plastic` | `400` `invalid type parameter: "plastic"` |
| `/transactions?status=bogus` | **`200`, 0 rows** |
| `/transactions?account_type=CHECKING` | **`200`, 0 rows** (case-sensitive) |
| `/transactions?account_type=treasury` | **`200`, 0 rows** (valid for statements, not for transactions) |
| `/statements?statement_type=monthly` | **`200`, 0 rows** |
| `/invoicing/invoices?status=draft` | **`200`, 0 rows** |
| `/invoicing/invoices?status=canceled` | **`200`, 0 rows** (the enum value is `cancelled`) |

`/cards` is the only endpoint that strictly validates its enum filters. Validate enum values client-side before sending, or the API will happily tell you there is no data.

**`sort_by` validation.** Four different behaviours across six endpoints:

| Endpoint | Validates `sort_by`? | Accepted values | Does it actually sort? | Default |
|---|---|---|---|---|
| `/accounts` | **yes, 400 on unknown** | only `balance`, `account_name` | yes | `account_name` asc |
| `/invoicing/customers` | **yes, 400 on unknown** | only `created_at` | yes | `created_at` desc |
| `/transactions` | no, silently ignores | any string returns 200 | yes for `amount`, `initiated_at`, `posted_at`; anything else falls back to the default | `initiated_at` desc |
| `/statements` | no, silently ignores | any string returns 200 | **no, nothing changes the order** | `period_end` desc |
| `/cards` | no, not parsed at all | any string returns 200 | not exercised (8 rows) | id order |
| `/invoicing/invoices` | no, not parsed at all | any string returns 200 | not exercised (12 rows) | `created_at` desc |

A typo in `sort_by` fails loudly on two endpoints and silently on four.

> **Divergence:** `/statements` advertises `sort_by` in its OpenAPI definition and its query-parameter table. No value has any observable effect: `period_end`, `period_start`, `available_at` and `bogus` all return the identical sequence. Only `order` does anything.

> **Divergence:** `/invoicing/customers` documents `sort_by` as "Sort field. Defaults to `created_at` when omitted." `created_at` is the only accepted value, and every other value returns `400`. The parameter can only fail, never do anything useful.

`order` is validated wherever it is parsed, and only lowercase `asc` and `desc` are accepted on `/accounts` and `/invoicing/customers`. On `/transactions` and `/statements`, `order=bogus` is a silent no-op that falls back to `desc`, while `order=ASC` is honoured in effect but hashed case-sensitively into the cursor fingerprint, so it breaks any token you carry across it.

**Date parameter semantics.** Three endpoints, three different contracts:

| Endpoint | Parameters | Accepted formats | `after` | `before` |
|---|---|---|---|---|
| `/transactions` | `initiated_after/before`, `posted_after/before` | `2026-01-01`, `2026-01-01T00:00:00Z`, `2026-01-01T00:00:00+00:00`, `2026-01-01T00:00:00.000Z` | inclusive | **exclusive** |
| `/statements` | `period_end_after/before`, `period_start_after/before` | **`2026-01-01` only**, any timestamp form is a `400` | inclusive | **exclusive** |
| `/invoicing/invoices` | `date_after/before`, `due_date_after/before` | **`2026-01-01` only** | inclusive | **inclusive** |

```bash
curl -s -w ' [%{http_code}]\n' "$RHO_BASE/statements?period_end_after=2026-01-01T00:00:00Z" -H "$RHO_AUTH"
# -> {"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: period_end_after"} [400]

curl -s "$RHO_BASE/transactions?page_size=100&initiated_after=2026-01-01T00:00:00Z" -H "$RHO_AUTH" \
  | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["transactions"]),"rows")'
# -> 47 rows
```

The same ISO-8601 timestamp that works on `/transactions` is a `400` on `/statements`. And the `before` bound is exclusive on two endpoints and inclusive on the third.

**Amount filters.** `min_amount` and `max_amount` compare the **signed** amount, not the absolute value, so `min_amount=0` selects the 32 credits and `max_amount=0` selects the 40 debits. Bounds are inclusive on both ends. The parameter docs say only "minimum amount in minor units" without mentioning sign. This is also the only cross-field validation in the whole API: an inverted amount range is a `400`, while an inverted **date** range is a `200` with zero rows.

**Detail routes.** Malformed ids are a `400` on five resources and a `404` on the sixth:

| Path | Malformed id | Unknown id |
|---|---|---|
| `/accounts/{account_id}` | `400 invalid parameter: account_id` | `404 account not found` |
| `/cards/{id}` | `400 invalid parameter: id` | `404 card not found` |
| `/transactions/{id}` | `400 invalid parameter: id` | `404 transaction not found` |
| `/invoicing/customers/{id}` | `400 invalid parameter: customer_id` | `404 customer not found` |
| `/invoicing/invoices/{id}` | `400 invalid parameter: invoice_id` | `404 invoice not found` |
| **`/statements/{id}`** | **`404 statement not found`** (no format validation at all) | `404 statement not found` |

Note also that the `detail` string leaks the internal path-parameter names, and they are inconsistent: `account_id`, `customer_id`, `invoice_id`, `transaction_id` and `file_id`, but a bare `id` for cards and transactions.

#### 3.6.5 The rest of the list

**UUID parsing is lenient, so one resource has at least five URL spellings.** All of these return `200` with an identical body whose `id` is normalised to canonical lowercase-dashed form: canonical, no dashes (32 hex), brace-wrapped, `urn:uuid:`-prefixed, and uppercase hex. This is the accept-set of Go's `github.com/google/uuid`. Normalise ids yourself, or a URL-keyed cache will store up to five copies of the same record.

**`HEAD` is not supported.** `HEAD /accounts` returns `405` with `allow: GET`. RFC 9110 treats `HEAD` as expected wherever `GET` is implemented. Health checkers and monitoring tools that default to `HEAD` will report the API as broken.

**There is no CORS, at all.** `OPTIONS` returns `405` with no `Access-Control-*` headers, and a `GET` carrying an `Origin` header gets no `Access-Control-Allow-Origin` either, on any status, from any origin including `https://app.rho.co`. A browser preflight can never succeed. Combined with a long-lived opaque credential this is a correct posture, but it is stated nowhere in the docs. Proxy through your own backend.

**Conditional requests are impossible.** No `ETag`, no `Last-Modified`, no `Cache-Control`, no `Vary` is ever emitted. `If-None-Match: *`, `If-None-Match: "abc123"` and `If-Modified-Since` in both directions all return a full `200`. There is no cheap "has anything changed" primitive and no webhook surface anywhere in the corpus, so change detection means full page pulls plus client-side diffing.

**There is no request id.** Cloudflare's `cf-ray` is the only per-request correlator in any response, and it is a CDN identifier, not a Rho one. Log it on every request anyway, because it is all you will have to quote to support.

**There is no pagination metadata beyond the cursor.** No `total`, `total_count`, `has_more`, `count`, `prev_page_token` or `Link` header. You cannot show "1-20 of 347" without draining the list.

**gzip is the only compression served.** Brotli, zstd, deflate and `Accept-Encoding: *` all return identity. Name `gzip` explicitly. Note also that no `Vary: Accept-Encoding` is emitted, which is a correctness hazard for any shared cache in front of your fleet.

**`search` exists on only two endpoints and covers only some fields.** On `/transactions` it is a case-insensitive, unanchored substring over `counterparty_name`, `memo` and `note`. On `/invoicing/customers` it covers `legal_name` and `email` only, so searching for a city returns zero. SQL `LIKE` metacharacters are escaped rather than interpreted. `/cards` and `/invoicing/invoices` have no `search` at all, and `/accounts` has no filtering of any kind, so name lookups on those resources require a full walk and client-side matching.

**`include_deleted` uses Go's `strconv.ParseBool`.** It accepts `1`, `t`, `T`, `TRUE`, `true`, `True`, `0`, `f`, `F`, `FALSE`, `false`, `False`. It rejects `yes`, `on`, an empty value and a bare flag, each with a `400`. The default is `false`, and a soft-deleted customer remains fully retrievable by id regardless of the flag.

**The two "cancelled" spellings will bite a shared status mapper.** `cards.status` is `canceled`. `invoices.status` and `activities[].activity_type` are `cancelled`.

**Two country encodings and two address models coexist.** `customers.address.country` is `"USA"` (alpha-3) with `address1`/`address2`/`city`/`state`/`zip_code`. `cards.billing_address.country_code` is `"US"` (alpha-2) with `street`/`second_line`/`city`/`subdivision`/`postal_code`.

**Documented fields that never materialise.** `transactions.tracking_number` (documented in detail as an ACH NACHA trace or wire IMAD/OMAD) and `transactions.counterparty_logo_url` appear on **zero** of 72 transactions, including 11 ACH and 10 wire records. `statements.accounts[].repayment_date` appears on zero of 22 credit statements. You cannot exercise payment tracing against this sandbox.

> **Divergence:** `api/transactions_listtransactions.md` says `posted_at` is "Null while status is pending." In the sandbox, `posted_at` is present on **both** pending records and on all 61 settled and all 8 failed records, and is absent only on the single `awaiting_approval` record. It is also *absent*, never null. The operative rule is "absent while awaiting approval," and the documented rule is contradicted in both directions. `docs/v1/transactions` restates the same pending rule and then loosens it only for other statuses ("posted_at is nullable, and the contract describes it as null while the status is pending. Beyond that it is not coupled to `status`"), so the guide does not contradict the reference page. Both are contradicted by the data.

> **Divergence:** `api/statements_liststatements.md` says `accounts[].account_id` is "null for credit statements, which are not tied to a deposit account." It is never null: all 22 credit statements carry a real credit account id that resolves on `/accounts`. The same page says `accounts[]` may span multiple checking or savings accounts. Its length is **1 on all 33 records**, and the two same-period statements `439950` (checking) and `439951` (savings) exist as separate records rather than one multi-account statement, which is precisely the case the docs say would be combined.

> **Divergence:** `api/cards_listcards.md` says `spending_limit`, `spending_limit_type` and `current_spend` are null when the card has no limit. All three are non-null on all 8 cards; no limitless card exists in the fixture set. `api/invoicing_listinvoicinginvoices.md` says `due_date` is "null when not set." It is non-null on all 12.

#### 3.6.6 A checklist to work from

1. Assert on the base URL host in your client. Sandbox and production are indistinguishable on the failure path.
2. Send `Authorization: Bearer <token>` with a capital B and exactly one ASCII space.
3. Branch on `Content-Type` before parsing any error body. Seven of twelve error classes are not JSON.
4. Branch on the HTTP status, not on `type`. `1303` and `1317` are coarse families and `title` is unversioned prose.
5. Never infer authentication success from a non-401 status. Type-binding `400`s and `405`s precede auth.
6. Build the query string conditionally. An empty `*_before` value silently empties your result set.
7. Validate enum filter values client-side. Half the endpoints will not tell you.
8. Treat `200 []` as ambiguous and assert against an unfiltered control query.
9. Replay the byte-identical filter query string on every page. `page_size` may change freely; case and duplication may not.
10. Type `statements.id` as a string, never a UUID.
11. Handle key **omission** on transactions and cards, not just null. Handle null on customers and invoices, not just omission.
12. Give every enum switch a default branch. The sandbox exercises 22 of 33 transaction types, 5 of 11 card statuses and 3 of 7 spending-limit types.
13. Read direction from the sign of `amount.amount`, never from the type name.
14. Group by `money_movement_id` before presenting transfers.
15. Never loop single GETs to enrich list rows. The detail surface returns nothing extra.
16. Re-fetch signed URLs rather than caching them, and parse `X-Goog-Date + X-Goog-Expires` to know the deadline.
17. Do not build invoice PDF download against this sandbox. It 404s universally.
18. Do not test backoff, scope errors or IP rejection here. `429` and `403` are unreachable.
19. Do not size your client against sandbox capacity. Self-throttle to the documented ~60 req/min per token.
20. For MCP, target production only.
## 4. Endpoint reference: Accounts, Transactions and Cards

Seven operations make up the core of the Rho `v1` REST surface. All seven are `GET`. There are no write
verbs anywhere in `v1`: every non-`GET` method on every path returns `405 Method Not Allowed` with
`Allow: GET` (observed, `POST https://rhoapi-sandbox.rho.co/api/v1/accounts` → `405`, empty body).

This section is the working reference for those seven. For each one: method, path, required scope, every
parameter with its type, default, constraint and whether the constraint is actually enforced, the full
response field table with types, nullability and observed presence rates, every enum value spelled out, a
real sandbox request with its real response, and the error conditions. Where Rho's documentation and the
live API disagree, the disagreement is called out inline.

Cross-references: the credential model and scope grants are covered in section 2, Authentication and
authorization; the cursor mechanics, the offset-versus-keyset split and the empty-value traps are covered
in full in section 6.1, Pagination; the error envelope taxonomy is covered in section 6.3, Errors.
Statements and Invoicing have their own section, section 5.

### 4.0 Conventions and evidence base

**Base URLs** (official docs, `api_v1_openapi.md`):

| Environment | Base URL |
| --- | --- |
| Production | `https://rhoapi.rho.co/api/v1` |
| Sandbox | `https://rhoapi-sandbox.rho.co/api/v1` |

Every operation path below is relative to that prefix. Paths are case sensitive (observed: `GET /ACCOUNTS`
returns a plain-text `404 page not found`, not JSON).

**Authentication.** `Authorization: Bearer <token>`, nothing else. On sandbox any non-empty token is
accepted, and the scheme keyword is matched case sensitively (observed: `Bearer WRONGTOKEN` → `200`;
`bearer sandbox` → `401 {"type":"2","title":"Unauthenticated","status":401}`).

**Evidence base.** Every "observed" claim in this section comes from live calls to
`https://rhoapi-sandbox.rho.co/api/v1` with `Authorization: Bearer sandbox`, captured 2026-09-12 between
00:20Z and 00:40Z UTC. The full sandbox dataset is small and was paged to exhaustion, so presence rates are
census figures, not samples:

| Resource | Records | Pages at `page_size=100` |
| --- | --- | --- |
| accounts | 14 | 1 |
| transactions | 72 | 1 |
| cards | 8 | 1 |

Sandbox data is fictional and frozen (newest transaction `initiated_at` is `2026-06-26T19:07:02Z`), with one
exception: card spend windows are recomputed against the real wall clock on every request. Response bodies
below are the real bytes, reformatted for reading: the API emits compact JSON with keys in alphabetical
order and escapes the ampersand in URL strings as the six-character sequence backslash-u-0-0-2-6, so a
byte-level diff against these examples will show key order and that escape. No values were changed.
Presence rates below describe the sandbox fixture, not a production guarantee. They are useful because
they show which documented fields Rho's own reference implementation never emits.

> **Divergence:** the markdown operation exports under `docs.rho.co/api/v1/openapi/**.md` are a lossy
> rendering of the same OpenAPI document the HTML reference renders. For every one of the seven
> operations the `.md` export silently drops the **required scope**, the **defaults** for `sort_by`,
> `order` and `page_size`, the numeric range on `page_size`, the `uuid`/`date-time`/`uri` formats, the
> `^[0-9]{4}$` pattern on `last_4`, the **enum values on query parameters**, the `or null` nullability
> marker on response fields, and the **`429 Too Many Requests`** response that the HTML declares on every
> operation. If you generate a client from the markdown export you will produce a client with no scope
> documentation, no defaults and no 429 handling. Use the rendered HTML reference, or the tables below.

**The null-versus-omitted rule.** This is the single most useful deserialization fact in the API and it is
documented nowhere. The wire format uses two different idioms, split by whether the field is `required` in
the schema:

| Schema shape | Wire representation | Where you see it |
| --- | --- | --- |
| `required` and nullable | key always present, value may be `null` | every nullable field on `Card` |
| optional (not `required`) | key **omitted entirely**, value is never `null` | every optional field on `Account` and `Transaction`, and the four merchant-control arrays on `Card` |

Observed: across all 72 transactions and all 14 accounts there is **not a single JSON `null`**; across the
8 cards there are 17 explicit `null`s (`shipping_address` 4, `usage_ends_at` 5, `usage_starts_at` 7,
`spend_period_end` 1) and zero omissions among the 16 required keys. The reference types the optional
transaction and account fields as "string or null", so a client that only checks for `null` will read
`undefined` and take the wrong branch. Treat absent and `null` as the same thing everywhere.

**Money.** Shared object used by `Account.balance`, `Transaction.amount`, `Card.spending_limit`,
`Card.current_spend` and `Card.pending_spend`.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `amount` | integer | yes | Minor units, for example cents for USD. Signed on transactions, where negative is a debit. |
| `currency` | string | yes | ISO 4217 code. |

There is no `amount_decimal`, no scale or exponent field, no FX rate and no original-currency field anywhere
in the core surface. Every one of the 393 `currency` occurrences in the sandbox is `USD`.

**Page.** The envelope on all three list operations.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `next_page_token` | string or null | yes | Pass back as `page_token`. `null` means last page. |

No total count, no `has_more`, no previous cursor, no page number. Sizing a result set requires walking it.

### 4.1 The seven operations at a glance

| Operation | Method and path | Scope | Declared statuses (rendered HTML reference) |
| --- | --- | --- | --- |
| ListAccounts | `GET /accounts` | `accounts:read` | 200, 400, 401, 403, 429, 500, 503 |
| GetAccount | `GET /accounts/{account_id}` | `accounts:read` | 200, 400, 401, 403, 404, 429, 500, 503 |
| ListTransactions | `GET /transactions` | `transactions:read` | 200, 400, 401, 403, 429, 500, 503 |
| GetTransaction | `GET /transactions/{id}` | `transactions:read` | 200, 400, 401, 403, 404, 429, 500, 503 |
| GetTransactionFile | `GET /transactions/{transaction_id}/files/{file_id}` | `transactions:read` | 200, 400, 401, 403, 404, 429, 500, 503 |
| ListCards | `GET /cards` | `cards:read` | 200, 400, 401, 403, 429, 500, 503 |
| GetCard | `GET /cards/{id}` | `cards:read` | 200, 400, 401, 403, 404, 429, 500, 503 |

Scopes come from the HTML reference's Security block, for example `AccessToken ( Required scopes :
accounts:read )` on ListAccounts. List operations declare no `404`; single-resource operations do. The
file operation needs only `transactions:read`; there is no separate document or file scope.

> **Divergence:** `docs/v1/auth` states "The scopes available today are:" and lists exactly three:
> `accounts:read`, `transactions:read`, `statements:read`. The OpenAPI security object lists five, adding
> `cards:read` and `invoicing:read`, and the Cards guide independently says "Both endpoints require the
> `cards:read` scope". The auth guide is stale. If you are provisioning a token for a card integration,
> grant `cards:read` even though the scope table does not list it.

> **Divergence:** the status column above is the rendered HTML reference's, and the `429` in it is the
> status the two renderings of the same OpenAPI document disagree about. Verified 2026-09-11 against
> `docs.rho.co/api/v1/openapi/accounts`, `/transactions` and `/cards`: the rendered response list reads
> `200, 400, 401, 403, 429, 500, 503`. None of the fourteen `.md` exports contains the string `429` at
> all, and no `429` body schema is published anywhere, so take the `.md` sets as this table minus `429`
> and add the rate-limit branch to any generated client by hand. `429` is also not reachable in sandbox:
> 300 requests in 4 seconds (roughly 3,600 per minute, against a documented ceiling of about 60 per minute
> per token) returned 300 × `200` and zero `429`. You cannot exercise your backoff path against sandbox.

### 4.2 Parameter semantics shared by the three list operations

These behaviours are identical or near-identical across `/accounts`, `/transactions` and `/cards`, so they
are stated once here and only the deviations are repeated per operation.

**`page_size`** is documented as `integer, [ 1 .. 100 ]`, default `20`, on all three. The range is enforced
uniformly and identically:

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=101' \
  -H 'Authorization: Bearer sandbox'
```

```json
{"type":"1317","title":"page_size must be between 1 and 100","status":400}
```

`0`, `-1`, `101` and `999999` all produce that body. A value that fails integer parsing (`abc`, `1.5`, empty,
or the parameter repeated) produces the other 400 dialect instead:
`{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}`.

The default of `20` is directly observable only on `/transactions`, because the accounts and cards fixtures
are smaller than a default page (observed: `GET /transactions` with no `page_size` returns 20 items and a
non-null cursor; `GET /accounts` returns all 14 and `GET /cards` returns all 8, both with
`next_page_token: null`).

**`page_token`** is an unsigned base64url JSON object, not an opaque blob. Two families exist. `/accounts`
returns a keyset cursor that names its own sort state; `/transactions` and `/cards` return an offset cursor:

```
/accounts  -> {"v":1,"f":"SigraTvwZG8Dd7QLdKJzPA","t":"..."}  where t decodes to
              {"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}
/transactions -> {"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":"b2Zmc2V0OjI"}  where t decodes to "offset:2"
```

`f` is a 16-byte fingerprint of the endpoint plus the canonicalized filter set. Observed binding rules:
replaying the same query with the token works (`200`); changing only `page_size` works (`200`); adding a
filter fails (`400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`); using a
`/transactions` token on `/cards` fails the same way. See section 6.1, Pagination, for the forging
behaviour and the full binding matrix.

> **Divergence:** `docs/v1/pagination` promises "Cursors are stable across changes to the underlying data:
> new items inserted while you are iterating will not shift existing pages or cause items to be skipped or
> duplicated", and separately that cursors are "opaque". Both `/transactions` and `/cards` return a plain
> `offset:N`, which cannot provide insert stability, and no cursor on any endpoint is signed or encrypted.
> Only `/accounts` uses a keyset cursor that structurally can honour the promise.

**Filter and sort validation is inconsistent between the three endpoints**, and the inconsistency is the
main source of silent wrong answers. Summary of observed behaviour:

| Endpoint | Unknown `sort_by` | Unknown `order` | Unknown enum filter value | Unknown parameter name |
| --- | --- | --- | --- | --- |
| `/accounts` | `400 invalid sort_by parameter: "created_at"` | `400 invalid order parameter: "DESC"` | no enum filters exist | `200`, ignored |
| `/transactions` | `200`, silently falls back to the default | `200`, silently falls back to `desc` | `200` with **0 rows** | `200`, ignored |
| `/cards` | `200`, parameter is not parsed at all | `200`, not parsed | `400 invalid status parameter: "bogus"` | `200`, ignored |

The practical rule: `200 []` from `/transactions` is ambiguous between "no matching data" and "you
misspelled a filter value". Validate enum values client-side before sending, and assert a filtered empty
result against an unfiltered control query.

**The empty-value trap.** Interpolating an undefined variable into a `*_before` parameter silently empties
the result set rather than erroring (observed: `GET /transactions?posted_before=` → `200` with
`"transactions": []`). An empty date coerces to the zero time `0001-01-01T00:00:00Z`, so `field < zero` is
never true. The matching `*_after=` parameters are ignored instead, and an empty enum value
(`status=`, `account_type=`) also yields `200` with zero rows. Build query strings conditionally.

---

### 4.3 Accounts

The Accounts API exposes the bank accounts the business holds on Rho. Per the Accounts guide, `account_type`
"determines what it can hold and how it behaves" and is **immutable for the lifetime of an account**.

`AccountType`, all five values, with Rho's own definitions:

| Value | Rho's definition |
| --- | --- |
| `checking` | Operating cash accounts used for everyday inflows and outflows. |
| `savings` | Higher-yield depository accounts segregated from operating cash. |
| `credit` | Revolving credit lines backing corporate cards. |
| `investment` | Treasury sleeves invested in money-market funds or short-duration securities. |
| `rewards` | Cash-back balances earned on card spend. |

Observed distribution over the 14 sandbox accounts: `checking` 6, `credit` 4, `rewards` 2, `savings` 2,
`investment` **0**. The `investment` shape, in particular whether such an account carries masked numbers, is
unverifiable from the sandbox.

> **Divergence:** the Statements resource uses a different account-type vocabulary for the same concept.
> `statements.accounts[].account_type` emits `treasury`, which is not a member of `AccountType` at all,
> while the Accounts API calls the nearest equivalent `investment`. Compounding it, the sandbox account
> named "Treasury Checking" (`30000000-0000-4000-8000-000000000004`) has `account_type: "checking"`. Do
> not build one shared account-type enum across Accounts and Statements.

#### 4.3.1 `GET /accounts` (ListAccounts)

Returns a paginated list of accounts for the authenticated business. Scope: `accounts:read`.

**Query parameters**

| Param | Type | Default | Constraint | Enforced? |
| --- | --- | --- | --- | --- |
| `sort_by` | string | `"account_name"` | Enum: `account_name`, `balance` | **Yes.** Any other value, including `id`, `created_at`, `account_type`, `account_number_last_4` and the empty string, returns `400 {"type":"1317","title":"invalid sort_by parameter: \"<value>\"","status":400}` |
| `order` | string | `"asc"` | Enum: `asc`, `desc` | **Yes**, and case sensitively. `DESC` returns `400 invalid order parameter: "DESC"` |
| `page_size` | integer | `20` | `[1 .. 100]` | **Yes**, see 4.2 |
| `page_token` | string | none | Opaque cursor | **Yes**, keyset cursor bound to endpoint plus sort state |

There is no `account_id`, `account_type`, `currency`, `status` or `search` filter. The Accounts guide says
so explicitly ("The list endpoint has no server-side type filter") and tells you to filter the returned
array client-side. Observed: `GET /accounts?account_type=checking` returns all **14** accounts, silently
ignored, not rejected.

Note that `order` defaults to `asc` here and to `desc` on `/transactions`. `sort_by=balance` with no
explicit `order` sorts ascending (observed: first three rows are the three zero-balance accounts).

**Response `200`**

| Field | Type | Required | Nullable | Observed presence (n=14) | Notes |
| --- | --- | --- | --- | --- | --- |
| `accounts` | array of Account | yes | no | 14 rows | |
| `accounts[].id` | string (uuid) | yes | no | 14/14 | Only unique key on the object |
| `accounts[].account_type` | string enum | yes | no | 14/14 | 4 of 5 values seen |
| `accounts[].balance` | Money | yes | no | 14/14 | |
| `accounts[].balance.amount` | integer | yes | no | 14/14 | All USD; values `0`, `1046`, `811970`, `876138`, `8711697`, `15460929` |
| `accounts[].balance.currency` | string | yes | no | 14/14 | `USD` on all |
| `accounts[].account_name` | string | no | yes | **14/14** | Never omitted, never null in practice |
| `accounts[].account_number_last_4` | string | no | yes | **8/14** | Key omitted, not null, on all 4 `credit` and both `rewards` accounts |
| `accounts[].routing_number_last_4` | string | no | yes | **8/14** | Same 8 rows; every value is `"0089"` |
| `page.next_page_token` | string | yes | yes | 1/1 | |

The Account object has exactly 6 properties. There is no `created_at`, no `status`, no account-level
`currency`, no bank or partner name, no full account or routing number, no IBAN or SWIFT, and no
available-versus-current balance, credit limit, available credit, APR or yield. An account is 4 to 6 keys
and nothing else.

**Real request and response**

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=3' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "accounts": [
    {
      "account_name": "Cash (Checking)",
      "account_number_last_4": "9508",
      "account_type": "checking",
      "balance": { "amount": 876138, "currency": "USD" },
      "id": "30000000-0000-4000-8000-000000000002",
      "routing_number_last_4": "0089"
    },
    {
      "account_name": "Cash (Checking)",
      "account_number_last_4": "4609",
      "account_type": "checking",
      "balance": { "amount": 8711697, "currency": "USD" },
      "id": "30000000-0000-4000-8000-000000000003",
      "routing_number_last_4": "0089"
    },
    {
      "account_name": "Credit Account",
      "account_type": "credit",
      "balance": { "amount": 0, "currency": "USD" },
      "id": "30000000-0000-4000-8000-000000000007"
    }
  ],
  "page": {
    "next_page_token": "eyJ2IjoxLCJmIjoiU2lncmFUdndaRzhEZDdRTGRLSnpQQSIsInQiOiJleUpzWVhOMFgybGtJam9pTXpBd01EQXdNREF0TURBd01DMDBNREF3TFRnd01EQXRNREF3TURBd01EQXdNREEzSWl3aWMyOXlkRjlpZVNJNkltRmpZMjkxYm5SZmJtRnRaU0lzSW05eVpHVnlJam9pWVhOakluMCJ9"
  }
}
```

Three things are visible in that one response. The first two rows share the display name `Cash (Checking)`,
so `account_name` is not unique. The third row has no `account_number_last_4` and no
`routing_number_last_4` key at all. And the rows are in ascending `account_name` order, which is the
default that the `.md` export never states.

> **Divergence:** the Accounts guide states "Alongside the balance, each account carries its type, a display
> name, and the masked account and routing numbers." Six of the fourteen sandbox accounts, every `credit`
> and every `rewards` account, carry neither masked number. The guide's blanket statement is wrong; the
> schema, which marks both fields optional, is right. Any UI that renders "••••{account_number_last_4}"
> unconditionally will print `••••undefined` on credit and rewards accounts.

> **Divergence:** the schema types the three optional account fields as "string **or null**", but the API
> **omits the keys** instead of emitting `null`. This is the general rule from 4.0, and accounts are where
> it bites first.

> **Divergence:** display names are not unique and are not identifiers. `Cash (Checking)` appears twice,
> `Credit Account` four times, `Rewards` twice, `Savings` twice. Nothing in the docs says `account_name`
> can repeat. Key on `id`.

> **Divergence:** the `/accounts` cursor payload literally contains `{"sort_by":"account_name",
> "order":"asc"}`. The defaults are therefore observable from the wire even though the `.md` export omits
> them. This also means the endpoint's own cursor contradicts the "cursors are opaque" claim in the
> pagination guide.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `page_size` outside `[1..100]` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| 400 | `page_size` unparseable or repeated | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}` |
| 400 | `sort_by` not in the enum | `{"type":"1317","title":"invalid sort_by parameter: \"created_at\"","status":400}` |
| 400 | `order` not `asc`/`desc` | `{"type":"1317","title":"invalid order parameter: \"DESC\"","status":400}` |
| 400 | `page_token` garbage, cross-endpoint, or filters changed | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| 401 | Missing, empty, or non-`Bearer` Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403 | Token lacks `accounts:read`, or source IP outside the token allowlist | Documented only. Not reachable in sandbox, which performs no scope or IP checks |
| 429 | Rate limit exceeded, about 60 req/min per token | Documented only (HTML reference). Not reachable in sandbox |
| 500, 503 | Server side | Not reachable in sandbox |

#### 4.3.2 `GET /accounts/{account_id}` (GetAccount)

Returns a single account. Scope: `accounts:read`.

**Path parameters**

| Param | Type | Format | Required |
| --- | --- | --- | --- |
| `account_id` | string | `uuid` | yes |

There are no query parameters, and any that you pass are silently ignored.

**Response `200`**: the identical Account object, unwrapped, with identical nullability and identical
presence rates. Observed exhaustively: all 14 single-resource fetches are byte-for-byte deep-equal to the
corresponding row in the list response. There is no expanded detail representation and no field you can
only get from the single fetch.

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts/30000000-0000-4000-8000-000000000001' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "account_name": "Reserve Checking",
  "account_number_last_4": "0106",
  "account_type": "checking",
  "balance": { "amount": 1046, "currency": "USD" },
  "id": "30000000-0000-4000-8000-000000000001",
  "routing_number_last_4": "0089"
}
```

And the credit-account shape, which is the four-key variant:

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/accounts/30000000-0000-4000-8000-000000000007' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "account_name": "Credit Account",
  "account_type": "credit",
  "balance": { "amount": 0, "currency": "USD" },
  "id": "30000000-0000-4000-8000-000000000007"
}
```

> **Divergence:** looping single GETs to "enrich" list rows buys nothing. This was verified across all 133
> sandbox resources of all six types: zero extra keys, zero value differences. At roughly 60 requests per
> minute per token, an enrichment loop is the fastest way to hit the rate limit for no benefit. Rho says as
> much for transactions ("most reconciliation needs no extra calls") but never states the general rule.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `account_id` not parseable as a UUID | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| 404 | Well-formed UUID that does not exist, or belongs to another business | `{"type":"1303","title":"account not found","status":404}` |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As for ListAccounts | Not reachable in sandbox |

> **Divergence:** UUID parsing is far more lenient than "string, format uuid" implies. All of these return
> `200` with the same body: canonical form, 32 hex digits with no dashes
> (`/accounts/30000000000040008000000000000001`), brace-wrapped, `urn:uuid:`-prefixed, and uppercase hex.
> The response always normalises `id` to canonical lowercase dashed form. Any cache keyed on request URL
> will store up to five copies of the same account. This is the accept-set of Go's `github.com/google/uuid`.

> **Divergence:** the `detail` string leaks the internal path-parameter name, and the names are
> inconsistent across resources: `account_id` here, but bare `id` for `/cards/{id}` and
> `/transactions/{id}`. That matches the OpenAPI declarations, so error-string matching on `detail` is
> resource-specific.

---

### 4.4 Transactions

A transaction record models one ledger event against one account. Three identity concepts matter, and Rho's
own framing is unusual enough to quote:

| Field | Rho's wording | Consequence |
| --- | --- | --- |
| `id` | "The transaction's identifier. Stable across re-fetches, but not guaranteed unique per row. The entries of one money movement can share an `id`." | `id` alone is not a primary key |
| `money_movement_id` | "Identifier shared by every transaction entry belonging to the same money movement." | The join key for the legs of a transfer |
| `account_id` | "The account the event posted against." | The disambiguator that makes `(id, account_id)` unique |

Rho's stated ingestion rule is to key on `(id, account_id)` or to group on `money_movement_id`, never on
`id` alone.

> **Divergence:** the shared-`id` case the documentation tells you to defend against is **never
> demonstrated**. All 72 sandbox transaction ids are distinct, and all 7 multi-leg money movements have
> distinct ids per leg. Observed, movement `40000000-0000-4000-8000-000000000002`: leg
> `019f0143-3ea0-7000-8000-000000000003` on account `…0007` at `+1750`, and leg
> `019f0143-3ea0-7000-8000-000000000002` on account `…0002` at `-1750`. You cannot reproduce the failure
> mode against sandbox, so write the composite key defensively and test it with synthetic data.

> **Divergence:** the attachments section of the same Transactions guide states "A transaction `id`
> identifies one transaction", contradicting the field definition above in the same document. The file
> endpoint also has no `account_id` disambiguator, so if ids really can collide, file lookup has no way to
> express which leg it means.

**Sign convention.** There is no `direction` or `debit_credit` field. The sign of `amount.amount` is the
only directional signal and it is relative to `account_id`. Observed across 72 rows: 40 negative, 32
positive, 0 zero. Refunds are positive. `credit_repayment` is positive on the `credit` leg and negative on
the `checking` leg of the same movement.

> **Divergence:** `adjustment_credit` is **negative** (observed: a single `-4500` on Treasury Checking) and
> `adjustment_debit` is **positive** (observed: a single `+3000` on Cash (Checking)). Every other type pair
> in the dataset has the sign its name implies. Nothing in the docs defines the sign of an adjustment.
> Read the sign, never the type name.

`TransactionStatus`, all four values:

| Value | Meaning per the guide | Observed (n=72) |
| --- | --- | --- |
| `pending` | Created, funds not yet cleared | 2 |
| `settled` | Cleared the ledger | 61 |
| `failed` | Insufficient funds, returned ACH, declined card. Remains queryable for audit | 8 |
| `awaiting_approval` | "held pending action on your side, and no funds have moved while it sits in that state" | 1 |

`TransactionType`, all 33 documented values, in spec order:

| # | Value | Family | Observed (n=72) |
| --- | --- | --- | --- |
| 1 | `card_credit` | Card | 0 |
| 2 | `card_debit` | Card | 8 |
| 3 | `card_refund` | Card | 4 |
| 4 | `credit_repayment` | Credit line | 6 |
| 5 | `credit_repayment_refund` | Credit line | 4 |
| 6 | `credit_cashback` | Credit line | 0 |
| 7 | `ach_credit` | ACH | 5 |
| 8 | `ach_debit` | ACH | 6 |
| 9 | `ach_return` | ACH | 2 |
| 10 | `wire_in` | Domestic wire | 4 |
| 11 | `wire_out` | Domestic wire | 4 |
| 12 | `wire_fee` | Domestic wire | 1 |
| 13 | `international_wire_in` | International wire | 0 |
| 14 | `international_wire_out` | International wire | 2 |
| 15 | `check_deposit` | Check | 3 |
| 16 | `check_payment` | Check | 2 |
| 17 | `internal_transfer` | Internal | 4 |
| 18 | `savings_deposit` | Savings | 2 |
| 19 | `savings_withdrawal` | Savings | 2 |
| 20 | `savings_interest` | Savings | 2 |
| 21 | `treasury_deposit` | Treasury | 0 |
| 22 | `treasury_withdrawal` | Treasury | 0 |
| 23 | `treasury_fee` | Treasury | 0 |
| 24 | `treasury_interest` | Treasury | 0 |
| 25 | `treasury_maturity` | Treasury | 0 |
| 26 | `treasury_sale` | Treasury | 0 |
| 27 | `treasury_market_value_adjustment` | Treasury | 0 |
| 28 | `rewards_accrual` | Rewards | 4 |
| 29 | `rewards_cashback_redemption` | Rewards | 3 |
| 30 | `adjustment_credit` | Adjustment | 1 |
| 31 | `adjustment_debit` | Adjustment | 1 |
| 32 | `international_wire_fee` | International wire | 2 |
| 33 | `international_wire_fee_refund` | International wire | 0 |

Eleven values are never produced by the sandbox, including the entire treasury family. Values 32 and 33
appear after the adjustment pair rather than next to values 13 and 14, which is the fingerprint of an enum
already extended inside `v1`. Rho's versioning policy permits new enum values at any time, so every switch
on `transaction_type` needs a default branch.

Absent from the enum entirely: any dispute or chargeback value (the guide says "`v1` exposes no dispute
indicator"), any return variant for wires or checks, any bill-pay family, and any invoicing or receivable
family.

#### 4.4.1 `GET /transactions` (ListTransactions)

Returns a paginated list of transactions. Scope: `transactions:read`. Sixteen query parameters, more than
the other six operations combined.

**Query parameters**

| Param | Type | Default | Constraint | Enforced? |
| --- | --- | --- | --- | --- |
| `account_id` | array of string (uuid) | none | Repeatable, OR within | Format **yes** (`account_id=xyz` → `400 invalid parameter: account_id`); existence **no** (unknown well-formed UUID → `200` with 0 rows). Comma-joined values are a `400`; `account_id[]=` bracket syntax is silently ignored |
| `account_type` | array of string | none | Enum: `checking`, `credit`, `investment`, `savings`, `rewards` | **No.** `account_type=bogus`, `CHECKING` and `treasury` all return `200` with 0 rows |
| `transaction_type` | array of string | none | Enum: the 33 values above | **No.** Any string returns `200` with 0 rows |
| `status` | array of string | none | Enum: `pending`, `settled`, `failed`, `awaiting_approval` | **No.** `status=bogus` returns `200` with 0 rows |
| `user_id` | array of string (uuid) | none | Repeatable, OR within | Format yes, existence no |
| `card_id` | array of string (uuid) | none | Repeatable, OR within | Format yes, existence no |
| `search` | string | none | Free text over `counterparty_name`, `memo`, `note` | Case-insensitive unanchored substring; whitespace trimmed; SQL LIKE metacharacters escaped, not interpreted. Repeating it is a `400` |
| `initiated_after` | string (date-time) | none | Inclusive | Accepts `2026-01-01` and full RFC 3339 with a zone. A zoneless timestamp is a `400` |
| `initiated_before` | string (date-time) | none | **Exclusive** | Same formats. Empty value returns 0 rows |
| `posted_after` | string (date-time) | none | Inclusive | Same. Excludes rows with no `posted_at` |
| `posted_before` | string (date-time) | none | **Exclusive** | Same. Empty value returns 0 rows |
| `min_amount` | integer | none | Inclusive lower bound | Compares the **signed** value. `min_amount=0` returns only the 32 credits |
| `max_amount` | integer | none | Inclusive upper bound | Compares the signed value. `max_amount=0` returns only the 40 debits |
| `sort_by` | string | `"initiated_at"` | Enum: `initiated_at`, `posted_at`, `amount` | **No.** Only those three reorder; every other value, including the empty string, returns `200` in default order |
| `order` | string | `"desc"` | Enum: `asc`, `desc` | **No.** `order=sideways` returns `200` in `desc` order. `ASC` works but hashes differently into the cursor |
| `page_size` | integer | `20` | `[1 .. 100]` | **Yes** |
| `page_token` | string | none | Cursor | **Yes**, offset cursor |

Repeating an array parameter ORs its values; different parameters are ANDed. Observed:
`transaction_type=wire_in&transaction_type=wire_out` returns 8 rows (4 + 4);
`user_id` with two values returns 3 rows.

The half-open date convention (`after` inclusive, `before` exclusive) makes
`posted_after=D&posted_before=D+1` a clean accounting day. Observed:
`posted_after=2026-06-23T00:00:00Z&posted_before=2026-06-24T00:00:00Z` returns 8 rows.

Filters that do not exist: `money_movement_id` (so you cannot fetch the other legs of a movement by its
movement id), exact-match counterparty, `currency`, `has_attachments`, `tracking_number`, any
merchant-category filter, and any `updated_after` or delta cursor. There is no change feed of any kind.

> **Divergence:** `min_amount` and `max_amount` compare the signed value, which the parameter description
> ("Minimum amount in minor units") does not say. "All transactions over $100" therefore needs two queries
> or client-side filtering. An inverted amount range is the only cross-field validation in the whole API
> (`min_amount=10000&max_amount=-10000` → `400 {"type":"1317","title":"min_amount must be less than or
> equal to max_amount","status":400}`), while an inverted **date** range returns `200` with zero rows.

> **Divergence:** the three enum filters are not validated. `status=Settled`, `status=posted` and
> `account_type=treasury` are all `200` with an empty array. Contrast `/cards`, which rejects the same
> class of mistake with a `400`. Two endpoints in the same API version, opposite behaviour.

**Response `200`**: the Transaction object has 20 properties.

| # | Field | Type | Format | Required | Nullable | Present (n=72) | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | string | uuid | yes | no | 72/72 | UUIDv7 in sandbox; 72 distinct |
| 2 | `money_movement_id` | string | uuid | yes | no | 72/72 | 65 distinct, 7 of them with 2 legs |
| 3 | `account_id` | string | uuid | yes | no | 72/72 | 11 distinct of 14 accounts |
| 4 | `account_type` | string enum | | yes | no | 72/72 | `checking` 42, `credit` 17, `rewards` 7, `savings` 6 |
| 5 | `initiated_at` | string | date-time | yes | no | 72/72 | Always present, seconds precision, always `Z` |
| 6 | `posted_at` | string | date-time | **no** | yes | **71/72** | Omitted on the one `awaiting_approval` row. Never `null` |
| 7 | `transaction_type` | string enum | | yes | no | 72/72 | 22 of 33 values |
| 8 | `status` | string enum | | yes | no | 72/72 | All 4 values |
| 9 | `amount` | Money | | yes | no | 72/72 | Signed; range `-5900000` to `130000000` |
| 10 | `account_name` | string | | **yes** | **no** | 72/72 | Denormalized copy of `Account.account_name` |
| 11 | `counterparty_name` | string | | yes | no | 72/72 | 37 distinct. Documented as possibly `""`; no empty string observed |
| 12 | `counterparty_logo_url` | string | uri | no | yes | **0/72** | Documented, never emitted |
| 13 | `note` | string | | no | yes | 39/72 | User-editable in Rho |
| 14 | `memo` | string | | no | yes | 39/72 | Bank or provider supplied, read-only |
| 15 | `user_id` | string | uuid | no | yes | 38/72 | 12 distinct users |
| 16 | `user_full_name` | string | | no | yes | 38/72 | Always present or absent together with `user_id` |
| 17 | `card_id` | string | uuid | no | yes | 12/72 | Exactly the `card_debit` and `card_refund` rows |
| 18 | `card_name` | string | | no | yes | 12/72 | Together with `card_id` |
| 19 | `tracking_number` | string | | no | yes | **0/72** | Documented, never emitted |
| 20 | `attachments` | array of TransactionAttachment | | **yes** | no | 72/72 | `[]` on 58 rows, 1 file on 12, 2 files on 2 |

`TransactionAttachment` is `{file_id: string(uuid), file_name: string}`, both required. There is no MIME
type, byte size, upload timestamp, uploader or document classification.

> **Divergence, the most consequential one in the core API.** The reference says `posted_at` is "Null while
> status is pending". Live behaviour contradicts it in both directions. Both `pending` rows carry a
> `posted_at`, and it equals `initiated_at` exactly. All 8 `failed` rows carry one too. The only row
> without one is the single `awaiting_approval` row, and there the key is **omitted**, not null. The
> operative rule in the fixture is "absent while awaiting approval". A client that treats
> `posted_at != null` as "posted" will count a pending authorization and a failed check as cleared. Read
> `status`. The Transactions guide states the same pending rule (`docs/v1/transactions`: "Null while the
> status is pending") and then adds that, beyond pending, `posted_at` is "not coupled to `status`" and
> should be read "as nullable whatever the status". The two Rho pages agree with each other. Both state a
> pending rule that the data contradicts.

> **Divergence:** `tracking_number` and `counterparty_logo_url` are documented in detail and emitted on
> zero of 72 transactions, including the 11 `ach_credit` and `ach_debit` rows and the 10 domestic and
> international wire transfer rows (counting neither the 2 `ach_return` rows nor the 3 wire-fee rows),
> which per the documented semantics should carry a NACHA trace number or an IMAD/OMAD. Payment-tracing
> code cannot be exercised against sandbox at all.

> **Divergence:** `memo` and `note` are documented as different things (`memo` arrives from the bank and is
> read-only, `note` is user-entered and editable). In the fixture they are present or absent strictly
> together, 39/39 and 33/33, and byte-identical on 37 of the 39. The only two that differ are the failed
> ACH rows, where `note` is the memo plus `", Error: Invalid receiving routing number."`. The distinction
> the docs draw is untestable here.

> **Divergence:** `Transaction.account_name` is `required` and non-null, while `Account.account_name` on
> the Accounts resource is optional and nullable. The same attribute has two different contracts in the
> same API version. Practically, the transaction copy is the safer one to read.

> **Divergence:** `user_id` is documented as "Null for system-initiated activity such as interest". The
> split in the fixture is clean per transaction type, but the type assignment is arguable: `wire_in` and
> `savings_deposit` carry no user, while the `ach_credit` leg of a rewards cashback is attributed to a
> named user even though it is plainly system-generated. Do not infer "a human did this" from the presence
> of `user_id`.

**Real request and response**

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions?transaction_type=card_debit&status=pending&page_size=2' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "transactions": [
    {
      "id": "019ef508-2808-7000-8000-000000000006",
      "money_movement_id": "40000000-0000-4000-8000-000000000004",
      "account_id": "30000000-0000-4000-8000-000000000009",
      "account_name": "Credit Account",
      "account_type": "credit",
      "amount": { "amount": -45000, "currency": "USD" },
      "attachments": [
        { "file_id": "af1456af-1428-4845-8b03-9c98e098ec18", "file_name": "car-service-receipt.pdf" },
        { "file_id": "104c1de5-dcd3-429d-933e-d61fd076a55c", "file_name": "car-service-itinerary.pdf" }
      ],
      "card_id": "20000000-0000-4000-8000-000000000002",
      "card_name": "Maya Thompson",
      "counterparty_name": "Graceway Car Service",
      "initiated_at": "2026-06-23T15:10:13Z",
      "posted_at": "2026-06-23T15:10:13Z",
      "status": "pending",
      "transaction_type": "card_debit",
      "user_full_name": "Maya Thompson",
      "user_id": "10000000-0000-4000-8000-000000000002"
    }
  ],
  "page": { "next_page_token": null }
}
```

The second row is elided above. It is `019ef37e-4418-7000-8000-000000000001`, a `-4947` `card_debit` on
card `…0001` with the same key set. Those two are the only `pending` rows in the fixture, which is why the
cursor is already `null` at `page_size=2`.

Note `posted_at` present and equal to `initiated_at` on a `pending` row, and note the absence of `memo`,
`note`, `counterparty_logo_url` and `tracking_number` keys rather than `null` values.

The `awaiting_approval` row is the one record in the fixture with no `posted_at` key:

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions?status=awaiting_approval' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "transactions": [
    {
      "id": "019d3e86-4482-7000-8000-000000000048",
      "money_movement_id": "40000000-0000-4000-8000-000000000065",
      "account_id": "30000000-0000-4000-8000-000000000002",
      "account_name": "Cash (Checking)",
      "account_type": "checking",
      "amount": { "amount": -1250000, "currency": "USD" },
      "attachments": [],
      "counterparty_name": "Harborline Logistics",
      "initiated_at": "2026-03-30T11:36:00Z",
      "memo": "Q3 freight invoice",
      "note": "Q3 freight invoice",
      "status": "awaiting_approval",
      "transaction_type": "ach_debit",
      "user_full_name": "Daniel Rivera",
      "user_id": "10000000-0000-4000-8000-000000000003"
    }
  ],
  "page": { "next_page_token": null }
}
```

**Sorting, observed.** Default order is `initiated_at` descending, verified against all 72 rows (the
sequence is monotonically non-increasing). `sort_by=amount` sorts on the signed value, so `order=asc` puts
the largest debit first (`-5900000`). Under `sort_by=posted_at&order=asc` the row with no `posted_at` sorts
**first**; under `desc` it sorts last. `sort_by=bogus` and `order=sideways` both return `200` in default
order, with no indication that the parameter was discarded.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | Malformed UUID in `account_id`, `user_id` or `card_id` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| 400 | Unparseable or repeated scalar (`page_size`, `min_amount`, `search`, `page_token`) | `about:blank` form naming the parameter in `detail` |
| 400 | Unparseable date, including a zoneless timestamp like `2026-01-01T00:00:00` | `about:blank` form |
| 400 | `page_size` outside `[1..100]` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| 400 | `min_amount > max_amount` | `{"type":"1317","title":"min_amount must be less than or equal to max_amount","status":400}` |
| 400 | `page_token` invalid, from another endpoint, or filters changed mid-iteration | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| 401 | Missing or malformed Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403 | Missing `transactions:read`, or IP outside the allowlist | Documented only |
| 429 | Rate limited | Documented only (HTML reference) |
| **200 with 0 rows** | Misspelled enum filter value, or an empty `*_before` value | Not an error. This is the failure mode to guard against |

#### 4.4.2 `GET /transactions/{id}` (GetTransaction)

Returns a single transaction. Scope: `transactions:read`.

| Param | In | Type | Format | Required | Documented description |
| --- | --- | --- | --- | --- | --- |
| `id` | path | string | uuid | yes | Global transaction identifier |
| `account_id` | query | string | uuid | **no** | "Account ID for the transaction" |

**Response `200`**: the same 20-property Transaction object, unwrapped. Verified deep-equal to the list row
on all 72 transactions.

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "id": "019ef508-2808-7000-8000-000000000006",
  "money_movement_id": "40000000-0000-4000-8000-000000000004",
  "account_id": "30000000-0000-4000-8000-000000000009",
  "account_name": "Credit Account",
  "account_type": "credit",
  "amount": { "amount": -45000, "currency": "USD" },
  "attachments": [
    { "file_id": "af1456af-1428-4845-8b03-9c98e098ec18", "file_name": "car-service-receipt.pdf" },
    { "file_id": "104c1de5-dcd3-429d-933e-d61fd076a55c", "file_name": "car-service-itinerary.pdf" }
  ],
  "card_id": "20000000-0000-4000-8000-000000000002",
  "card_name": "Maya Thompson",
  "counterparty_name": "Graceway Car Service",
  "initiated_at": "2026-06-23T15:10:13Z",
  "posted_at": "2026-06-23T15:10:13Z",
  "status": "pending",
  "transaction_type": "card_debit",
  "user_full_name": "Maya Thompson",
  "user_id": "10000000-0000-4000-8000-000000000002"
}
```

> **Divergence, and a live footgun.** The optional `account_id` query parameter is documented with the five
> words "Account ID for the transaction" and is mentioned in neither guide. It is not a hint, it is an
> **assertion filter**. Observed on the transaction above, whose real account is
> `30000000-0000-4000-8000-000000000009`:
>
> ```bash
> # correct account: 200
> curl -s -o /dev/null -w '%{http_code}\n' \
>   'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006?account_id=30000000-0000-4000-8000-000000000009' \
>   -H 'Authorization: Bearer sandbox'
>
> # a different real account: 404
> curl -s \
>   'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006?account_id=30000000-0000-4000-8000-000000000002' \
>   -H 'Authorization: Bearer sandbox'
> # {"type":"1303","title":"transaction not found","status":404}
> ```
>
> A stale or guessed `account_id` turns an existing transaction into a `404`. Pass it only when you are
> certain, which in practice means only when you took it from the same transaction record.

Also never stated anywhere: what the endpoint returns when an `id` genuinely matches multiple entries and
`account_id` is omitted (first match, arbitrary leg, `400`, a list?), and whether `account_id` becomes
required in that case. The sandbox cannot answer it because no id collision exists there.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `id` not parseable as a UUID | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: id"}` |
| 400 | `account_id` query value not parseable | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| 404 | Unknown id, or `account_id` that does not match the transaction | `{"type":"1303","title":"transaction not found","status":404}` |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As elsewhere | Not reachable in sandbox |

#### 4.4.3 `GET /transactions/{transaction_id}/files/{file_id}` (GetTransactionFile)

"Returns file metadata and a fresh, short-lived signed download URL." Scope: `transactions:read`. This is
the only way to get bytes: transaction responses carry stable attachment descriptors and never URLs.

**Path parameters**

| Param | Type | Format | Required | Source |
| --- | --- | --- | --- | --- |
| `transaction_id` | string | uuid | yes | The transaction's `id` |
| `file_id` | string | uuid | yes | An `attachments[].file_id` value from that transaction |

No query parameters; any passed are ignored.

**Response `200`**: exactly three keys, all required.

| Field | Type | Format | Required | Notes |
| --- | --- | --- | --- | --- |
| `file_id` | string | uuid | yes | Echoes the request |
| `file_name` | string | | yes | Original file name, for example `car-service-receipt.pdf` |
| `download_url` | string | uri | yes | Google Cloud Storage V4 signed URL |

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/transactions/019ef508-2808-7000-8000-000000000006/files/af1456af-1428-4845-8b03-9c98e098ec18' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "download_url": "https://rho-api-sandbox.files.rho.co/8dd93c7776de909c0546477c.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=file-service%40pledge-218909.iam.gserviceaccount.com%2F20260912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260912T002646Z&X-Goog-Expires=899&X-Goog-SignedHeaders=host&X-Goog-Signature=0937465ff53c011a…",
  "file_id": "af1456af-1428-4845-8b03-9c98e098ec18",
  "file_name": "car-service-receipt.pdf"
}
```

Fetch the URL immediately, without an `Authorization` header. Observed: the signed URL returns `200
application/pdf`; it is **not** single-use (three fetches, three `200`s); it honours `HEAD` and `Range`
(`Range: bytes=0-9` → `206`); stripping the query string gives `403 AccessDenied`; altering one signature
character gives `403 SignatureDoesNotMatch`.

> **Divergence:** the TTL is never documented. The Transactions guide says only "short-lived", while the
> Statements guide commits to "up to 15 minutes" for its `pdf_url`. Observed here on every call:
> `X-Goog-Expires=899` seconds, that is 14 minutes 59 seconds, measured from `X-Goog-Date`. Both values are
> readable from the URL itself, so compute the deadline locally instead of discovering expiry from a failed
> download. Unlike statement URLs, transaction file URLs are minted fresh on every request, so there is no
> signing cache to work around.

> **Divergence:** `file_id` is documented as a "stable attachment identifier" and is **not** unique per
> transaction. Observed: `cdc328c1-c3a3-4670-a371-28e34891ee68` (`credit-repayment-receipt.pdf`) is
> attached to two different transactions in two different money movements, and both resolve to the same
> storage blob. 16 attachment rows across 15 distinct file ids. The real key is the
> `(transaction_id, file_id)` pair, exactly as the path implies, but nothing in the docs says a file can be
> shared.

> **Divergence:** there is no way to list a transaction's files independently. `GET
> /transactions/{id}/files` returns the Go router's plain-text `404 page not found`, not problem+json. Your
> only inventory is the `attachments` array on the transaction itself, and a client that parses every error
> body as JSON will throw on this one.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `transaction_id` unparseable | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: transaction_id"}` |
| 400 | `file_id` unparseable | Same form, `"detail":"invalid parameter: file_id"` |
| 404 | Unknown `file_id` | `{"type":"1303","title":"transaction file not found","status":404}` |
| 404 | Real `file_id` under the wrong transaction | Byte-identical to the above |
| 404 | Real `file_id` under a transaction with no attachments | Byte-identical |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As elsewhere | Not reachable in sandbox |

The parent-child relationship is enforced and a mismatched pairing is indistinguishable from an unknown
file. That is correct IDOR-resistant behaviour: the handler never reveals that the file exists elsewhere. It
also means you cannot distinguish "wrong parent" from "no such file" by response alone, so log the pair you
sent.

There is no upload, no delete, and no way to attach a file. The whole surface is read-only.

---

### 4.5 Cards

The Cards API exposes the physical and virtual cards belonging to the business linked to the token. Both
operations require `cards:read`. Security posture, quoted: "Only the last four PAN digits are returned; full
card numbers, CVCs, and expiration dates are not available through these endpoints." There is no
`expires_at` field at all; `usage_ends_at` is a usage-window control, not the PAN expiry.

An unfiltered list includes canceled and expired cards so their stable ids stay joinable to historical
transactions. To exclude them you must pass an explicit `status` filter.

`CardType`: `physical`, `virtual`. Observed 4 and 4.

`CardStatus`, all 11 values in spec order:

| Value | Reading | Observed (n=8) | Accepted as a filter value? |
| --- | --- | --- | --- |
| `printing` | Fulfilment | 0 | Yes, `200` with 0 rows |
| `shipped` | Fulfilment | 0 | Yes |
| `out_for_delivery` | Fulfilment | 0 | Yes |
| `activate_card` | Delivered, awaiting activation | 0 | Yes |
| `delivery_canceled` | Fulfilment | 0 | Yes |
| `active` | Usable | 4 | Yes |
| `expiring` | Usable | 0 | Yes |
| `locked` | Not usable, reversible | 1 | Yes |
| `canceled` | Not usable, terminal | 1 | Yes |
| `suspended` | Not usable | 1 | Yes |
| `expired` | Not usable | 1 | Yes |

All 11 are accepted by the filter (verified one by one), which is the only machine-readable confirmation of
the full enum, since the `.md` export omits query-parameter enums. Rho never documents the difference
between `locked` and `suspended`, which transitions are possible, or which statuses a virtual card can
reach. From the help centre, which is product behaviour rather than API contract: `locked` is the
user-toggled Lock Card state and is reversible; `canceled` is terminal; a fixed-limit card locks itself once
its transactions fully settle.

> **Divergence:** `cards.status` spells it `canceled` with one L, while the Invoicing resource in the same
> API version spells it `cancelled`. The filter enforces the difference: `GET /cards?status=cancelled`
> returns `400 {"type":"1317","title":"invalid status parameter: \"cancelled\"","status":400}`. A shared
> status mapper across products will break on this.

`CardSpendingLimitType`, all 7 values, with Rho's reset semantics:

| Value | Reset behaviour | `spend_period_end` | Observed (n=8) |
| --- | --- | --- | --- |
| `daily` | Eastern Time (America/New_York) calendar boundary | non-null | 1 |
| `weekly` | ET calendar boundary | non-null | 0 |
| `monthly` | ET calendar boundary | non-null | 6 |
| `quarterly` | ET calendar boundary | non-null | 0 |
| `annual` | Anniversary of when the limit took effect, not a calendar boundary | non-null | 0 |
| `fixed` | Lifetime ceiling, does not reset | **null** | 1 |
| `single_use` | Spent after one use | **null** | 0 |

The spec's own enum order is `fixed`, `monthly`, `single_use`, `annual`, `daily`, `weekly`, `quarterly`,
again suggesting the last three were added later.

Merchant controls use either the `blocked_*` fields or the `allowed_*` fields, never both. There is no
explicit `control_mode` discriminator: the mode is expressed purely by which keys are present.

#### 4.5.1 `GET /cards` (ListCards)

Scope: `cards:read`.

**Query parameters**

| Param | Type | Default | Constraint | Enforced? |
| --- | --- | --- | --- | --- |
| `user_id` | array of string (uuid) | none | Cardholder user ids, repeatable, OR within | Format **yes** (`user_id=nope` → `400 invalid parameter: user_id`); existence no (`200` with 0 rows) |
| `type` | array of string | none | Enum: `physical`, `virtual` | **Yes.** `type=plastic`, `type=Virtual` and `type=virtual,physical` all return `400 invalid type parameter: "<value>"` |
| `status` | array of string | none | Enum: the 11 `CardStatus` values | **Yes.** `status=frozen` → `400 invalid status parameter: "frozen"` |
| `page_size` | integer | `20` | `[1 .. 100]` | **Yes** |
| `page_token` | string | none | Cursor | **Yes**, offset cursor |

OR within a parameter, AND across parameters. Observed: `status=active&status=locked` → 5 cards;
`type=virtual&status=active` → 2 cards.

> **Divergence:** ListCards has **no `sort_by` and no `order`**, unlike the other two list operations. The
> parameters are not merely undocumented, they are not parsed: passing `sort_by=bogus` returns `200` with
> all 8 cards and does not even change the cursor fingerprint. Card ordering is undefined by the contract.
> Observed order is ascending by `id`. Do not depend on it.

> **Divergence:** `page_size` is documented on this operation as "Number of cards to return. Defaults to
> 20" with no maximum stated in the `.md` export. The server enforces `[1 .. 100]` here exactly as
> elsewhere, and says so in the error.

**Response `200`**: the Card object has 20 properties, 16 of them `required`.

| # | Field | Type | Required | Nullable | Present (n=8) | Nulls | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | string (uuid) | yes | no | 8/8 | 0 | Joins to `Transaction.card_id` |
| 2 | `name` | string | yes | no | 8/8 | 0 | Free text, user-editable, not unique |
| 3 | `last_4` | string, `^[0-9]{4}$` | yes | no | 8/8 | 0 | String because of leading zeroes; `"0042"` observed |
| 4 | `type` | enum | yes | no | 8/8 | 0 | `physical` \| `virtual` |
| 5 | `status` | enum | yes | no | 8/8 | 0 | 5 of 11 values seen |
| 6 | `cardholder` | Cardholder | yes | no | 8/8 | 0 | `{user_id, first_name, last_name}`, all required |
| 7 | `spending_limit` | Money or null | yes | **yes** | 8/8 | **0** | Documented null when no limit |
| 8 | `spending_limit_type` | enum or null | yes | **yes** | 8/8 | **0** | Documented null when no limit |
| 9 | `current_spend` | Money or null | yes | **yes** | 8/8 | **0** | "Pending plus settled spend in the current limit window" |
| 10 | `pending_spend` | Money or null | yes | **yes** | 8/8 | **0** | "Pending portion of `current_spend`" |
| 11 | `spend_period_start` | string (date-time) or null | yes | **yes** | 8/8 | 0 | Computed in America/New_York |
| 12 | `spend_period_end` | string (date-time) or null | yes | **yes** | 8/8 | **1** | Exclusive end. Null on the `fixed` card |
| 13 | `usage_starts_at` | string (date-time) or null | yes | **yes** | 8/8 | **7** | Null when unrestricted |
| 14 | `usage_ends_at` | string (date-time) or null | yes | **yes** | 8/8 | **5** | Null when unrestricted |
| 15 | `billing_address` | Address or null | yes | **yes** | 8/8 | 0 | |
| 16 | `shipping_address` | Address or null | yes | **yes** | 8/8 | **4** | Null on all 4 virtual cards |
| 17 | `blocked_categories` | array of MerchantCategory | **no** | no | **1/8** | n/a | Key present only for a block list |
| 18 | `allowed_categories` | array of MerchantCategory | **no** | no | **1/8** | n/a | Key present only for an allow list |
| 19 | `blocked_merchants` | array of Merchant | **no** | no | **1/8** | n/a | Block list only |
| 20 | `allowed_merchants` | array of Merchant | **no** | no | **1/8** | n/a | Allow list only |

`Address`: `street` (required), `second_line` (optional, omitted on 7 of 8 billing addresses), `city`,
`subdivision`, `postal_code`, `country_code` (ISO 3166-1 alpha-2), all required except `second_line`.
`MerchantCategory`: `code` (required, fixed-width ISO 18245 MCC, a **string** with leading zeros such as
`"0742"`) and `name` (optional). `Merchant`: `name` only, no id.

**Real request and response**

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/cards?type=virtual&status=active&page_size=1' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "cards": [
    {
      "id": "20000000-0000-4000-8000-000000000001",
      "name": "Ethan Parker",
      "last_4": "0042",
      "type": "virtual",
      "status": "active",
      "cardholder": {
        "user_id": "10000000-0000-4000-8000-000000000001",
        "first_name": "Ethan",
        "last_name": "Parker"
      },
      "spending_limit": { "amount": 500000, "currency": "USD" },
      "spending_limit_type": "monthly",
      "current_spend": { "amount": 6797, "currency": "USD" },
      "pending_spend": { "amount": 1500, "currency": "USD" },
      "spend_period_start": "2026-09-01T04:00:00Z",
      "spend_period_end": "2026-10-01T04:00:00Z",
      "usage_starts_at": "2025-10-01T09:00:00Z",
      "usage_ends_at": "2026-09-01T00:00:00Z",
      "billing_address": {
        "street": "100 Broadway",
        "second_line": "Floor 5",
        "city": "New York",
        "subdivision": "NY",
        "postal_code": "10005",
        "country_code": "US"
      },
      "shipping_address": null,
      "blocked_categories": [ { "code": "0742", "name": "Veterinary services" } ],
      "blocked_merchants": [ { "name": "Petco" } ]
    }
  ],
  "page": { "next_page_token": "eyJ2IjoxLCJmIjoicUJZV2JIU015OWdGNzFVLUE1ck1uUSIsInQiOiJiMlptYzJWME9qRSJ9" }
}
```

That single record shows both null idioms on one object: `shipping_address` is explicitly `null`, while
`allowed_categories` and `allowed_merchants` are absent entirely. It also shows the leading-zero `last_4`
and the `04:00:00Z` window boundary, which is midnight EDT.

> **Divergence:** the `04:00:00Z` boundaries confirm the documented America/New_York computation, but they
> are **EDT** boundaries. An EST window would be `05:00:00Z`, which the sandbox never demonstrates because
> its windows are always recomputed against the current wall clock. A client that hard-codes `-04:00` will
> break after the November DST change. Convert with a real tz database.

> **Divergence:** `spending_limit`, `spending_limit_type`, `current_spend` and `pending_spend` are all
> documented as null when the card has no limit. None of them is ever null in the fixture: 8 of 8 cards
> carry populated objects. The no-limit card is unexercised, so the code path you write for it is untested.

> **Divergence, the largest in the Cards resource.** `current_spend` is defined as "pending plus settled
> spend in the current limit window", and every window in the fixture starts `2026-09-01`. Every card
> transaction in the fixture is dated June 2026, outside every window. Yet `current_spend` reproduces the
> sum of that card's debits exactly. Measured live, per card:
>
> | Card | Status | Limit type | `current_spend` | `pending_spend` | Sum of that card's debits | Card transactions in the fixture |
> | --- | --- | --- | ---: | ---: | ---: | --- |
> | `…0001` | active | monthly | 6797 | 1500 | 6797 | one pending `-4947`, one settled `-1850` |
> | `…0002` | active | monthly | 45000 | 8000 | 45000 | one pending `-45000` |
> | `…0003` | active | monthly | 1750 | 250 | 1750 | one settled `-1750` |
> | `…0004` | locked | daily | 6331 | 900 | 6331 | one settled `-6331` |
> | `…0005` | active | monthly | 5331 | 400 | 5331 | one settled `-5331` |
> | `…0006` | suspended | monthly | 1622132 | 50000 | 1622132 | one settled `-1622132` |
> | `…0007` | canceled | monthly | 121827 | 0 | 121827 | one settled `-121827` |
> | `…0008` | expired | fixed | 0 | 0 | 0 | four settled `card_refund`s totalling `+271816` |
>
> So `current_spend` ignores the stated window, and `pending_spend` is not the pending subset of
> `current_spend` on any card (card `…0002`'s only transaction is pending at 45000, yet `pending_spend` is
> 8000). Card `…0008` shows that refunds do not push `current_spend` negative, but Rho never says whether
> refunds net against it at all. Treat both aggregates as server-computed opaque values and do not
> calibrate an implementation against the sandbox.

> **Divergence:** card `…0001` above is `status: "active"` with `usage_ends_at: "2026-09-01T00:00:00Z"`,
> which was in the past at capture time, and with a spend window running to 2026-10-01. `status` evidently
> does not reflect the usage window. `status == "active"` is therefore **not** sufficient to conclude a
> card is usable: check `usage_starts_at` and `usage_ends_at` against now as well.

> **Divergence:** canceled, suspended, locked and expired cards still report live spend windows recomputed
> per request. Card `…0007` is `canceled` and still returns `spend_period_start: "2026-09-01T04:00:00Z"`.
> Card status does not freeze the window.

> **Divergence:** the `.md` export flattens only one level of `$ref`, so `current_spend`, `pending_spend`,
> `shipping_address`, `allowed_categories` and `allowed_merchants` have **no documented sub-fields** at
> all. Their shapes are recoverable only from the wire: `{amount, currency}` for the two money objects, the
> same six-field Address as `billing_address` for shipping, `{code, name}` for categories, `{name}` for
> merchants.

> **Divergence:** the Cards guide's example prints the MCC name as `"Eating Places and Restaurants"` (title
> case); the API returns `"Eating places and restaurants"` (sentence case). Category and merchant names are
> display strings with unstable casing. Never key on them; key on `code` for categories, and accept that
> merchants have no id at all.

> **Divergence:** a Card carries **no `account_id`**. There is no way to ask which credit line a card draws
> on. The only answer is to look at the `account_id` on that card's transactions. Observed: every card
> transaction in the fixture posts to a `credit` account (`…0007` or `…0009`), never to checking.

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `type` not in `{physical, virtual}` | `{"type":"1317","title":"invalid type parameter: \"Virtual\"","status":400}` |
| 400 | `status` not one of the 11 values | `{"type":"1317","title":"invalid status parameter: \"frozen\"","status":400}` |
| 400 | `user_id` not a UUID or empty | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: user_id"}` |
| 400 | `page_size` outside `[1..100]` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| 400 | Invalid or cross-endpoint `page_token` | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403 | Missing `cards:read`, or IP outside the allowlist | Documented only |
| 429, 500, 503 | As elsewhere | Not reachable in sandbox |

#### 4.5.2 `GET /cards/{id}` (GetCard)

Scope: `cards:read`. Path parameter `id`, string, `uuid`, required. No query parameters. Returns the same
20-property Card object, unwrapped. Verified deep-equal to the list row on all 8 cards.

```bash
curl -s 'https://rhoapi-sandbox.rho.co/api/v1/cards/20000000-0000-4000-8000-000000000008' \
  -H 'Authorization: Bearer sandbox'
```

```json
{
  "id": "20000000-0000-4000-8000-000000000008",
  "name": "Claire Mitchell",
  "last_4": "7732",
  "type": "physical",
  "status": "expired",
  "cardholder": {
    "user_id": "10000000-0000-4000-8000-000000000009",
    "first_name": "Claire",
    "last_name": "Mitchell"
  },
  "spending_limit": { "amount": 500000, "currency": "USD" },
  "spending_limit_type": "fixed",
  "current_spend": { "amount": 0, "currency": "USD" },
  "pending_spend": { "amount": 0, "currency": "USD" },
  "spend_period_start": "2025-03-01T12:00:00Z",
  "spend_period_end": null,
  "usage_starts_at": null,
  "usage_ends_at": "2026-06-30T23:59:59Z",
  "billing_address": {
    "street": "350 Fifth Ave",
    "city": "New York",
    "subdivision": "NY",
    "postal_code": "10118",
    "country_code": "US"
  },
  "shipping_address": {
    "street": "350 Fifth Ave",
    "second_line": "Floor 20",
    "city": "New York",
    "subdivision": "NY",
    "postal_code": "10118",
    "country_code": "US"
  }
}
```

This is the `fixed`-limit case, and it matches the documented rule exactly: `spend_period_end` is `null`
because a lifetime ceiling does not reset, and `spend_period_start` is when the lifetime total began. Note
that its `12:00:00Z` start is not an ET midnight boundary, unlike every other card in the fixture, and that
all four merchant-control keys are absent because this card has no controls.

The Cards guide states the `404` semantics explicitly, and they are the only place in the corpus where Rho
commits to `404` rather than `403` for another business's resource: "The endpoint returns `404` when the
card does not exist or belongs to another business."

**Error conditions**

| Status | Trigger | Observed body |
| --- | --- | --- |
| 400 | `id` not parseable as a UUID | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: id"}` |
| 404 | Unknown card, or a card belonging to another business | `{"type":"1303","title":"card not found","status":404}` |
| 404 | An id of the wrong type, for example an account UUID | Same body. Clean type isolation, no cross-namespace resolution |
| 401 | Missing Authorization header | `{"type":"2","title":"Unauthenticated","status":401}` |
| 403, 429, 500, 503 | As elsewhere | Not reachable in sandbox |

---

### 4.6 Joining the three resources

The edges that actually exist in the payloads:

| From | Field | To | Integrity in the fixture |
| --- | --- | --- | --- |
| Transaction | `account_id` | Account `id` | 11 distinct refs, 11 resolve, 0 dangling |
| Transaction | `card_id` | Card `id` | 8 distinct refs, 8 resolve, 0 dangling |
| Transaction | `user_id` | Cardholder `user_id` | 8 of the 12 transaction users hold a card |
| Transaction | `money_movement_id` | nothing | No `/money-movements` endpoint exists |
| Transaction | `attachments[].file_id` | GetTransactionFile | 16 rows, 15 distinct ids, all resolve |
| Card | `cardholder.user_id` | nothing | No `/users` endpoint exists |

Practical consequences:

1. **A transaction is self-sufficient for reconciliation.** It carries `account_id`, `account_type` and
   `account_name` denormalized, plus `card_id`/`card_name` and `user_id`/`user_full_name` when they apply.
   Fetch `/accounts` once for balances and masked numbers and cache it for the job.
2. **Group on `money_movement_id` before presenting transfers.** 7 of 65 movements have two legs that sum
   to zero. A client that does not group will double count every internal transfer and credit repayment.
   There is no filter on `money_movement_id`, so grouping must happen client-side over a paged window.
3. **Cards to accounts has no direct edge.** Infer it from the `account_id` on that card's transactions.
4. **Users are referenced but never listable.** There is no `/users` endpoint, so a `user_id` can only be
   turned into a name if that user appears as a cardholder or on a transaction you can see. Four of the 12
   fixture users hold no card.
5. **Canceled and expired cards keep resolving.** `Transaction.card_name` still equals `Card.name` for the
   `canceled` and `expired` cards, which is exactly why they stay in unfiltered lists.

### 4.7 Divergence index for this section

| # | Operation | Documentation says | Live behaviour |
| --- | --- | --- | --- |
| 1 | all seven | `.md` export is the reference | `.md` drops scopes, defaults, ranges, formats, query enums, nullability markers and the entire `429` response |
| 2 | all seven | Auth guide lists 3 scopes | OpenAPI lists 5; `cards:read` is required and missing from the guide |
| 3 | all seven | Optional fields are "string or null" | Optional fields are **omitted**; only `required` + nullable fields emit `null` |
| 4 | list ops | Cursors are opaque and insert-stable | Unsigned base64url JSON; `offset:N` on transactions and cards, keyset only on accounts |
| 5 | ListAccounts | Every account carries masked account and routing numbers | 6 of 14 carry neither key |
| 6 | ListAccounts | (silent) | `account_name` is not unique; four accounts share `Credit Account` |
| 7 | ListAccounts | (silent, `.md`) | Defaults are `sort_by=account_name`, `order=asc`, `page_size=20` |
| 8 | ListTransactions | `posted_at` is "Null while status is pending" | Present on both pending and all 8 failed rows; absent on the `awaiting_approval` row |
| 9 | ListTransactions | `tracking_number`, `counterparty_logo_url` documented in detail | Emitted on 0 of 72 rows |
| 10 | ListTransactions | `memo` is bank-supplied, `note` is user-edited | Byte-identical on 37 of 39 rows, present or absent strictly together |
| 11 | ListTransactions | `Transaction.account_name` required non-null | `Account.account_name` optional and nullable for the same attribute |
| 12 | ListTransactions | Enum filters are enums | `status`, `account_type`, `transaction_type` are unvalidated: garbage gives `200 []` |
| 13 | ListTransactions | `sort_by` and `order` are enums | Unvalidated; unknown values silently fall back to the default |
| 14 | ListTransactions | `min_amount`/`max_amount` in minor units | Compare the **signed** value; inverted range is the only cross-field `400` |
| 15 | GetTransaction | `account_id` is "Account ID for the transaction" | An assertion filter: a wrong value turns `200` into `404` |
| 16 | GetTransaction | `id` may be shared across entries | All 72 ids distinct; multi-leg movements have distinct ids per leg |
| 17 | GetTransactionFile | "A transaction `id` identifies one transaction" | Contradicts the `id` definition in the same guide |
| 18 | GetTransactionFile | `download_url` is "short-lived" | `X-Goog-Expires=899` seconds, minted fresh per request, not single-use, honours `Range` |
| 19 | GetTransactionFile | `file_id` is a stable attachment identifier | One `file_id` is attached to two transactions; the real key is the pair |
| 20 | ListCards | `spending_limit`, `spending_limit_type`, `current_spend` null when no limit | Never null across all 8 cards |
| 21 | ListCards | `current_spend` is spend "in the current limit window" | Equals total card debits regardless of the window; `pending_spend` matches nothing |
| 22 | ListCards | (silent) | No `sort_by`/`order`; card order is undefined by contract |
| 23 | ListCards | `status` is a lifecycle field | `active` with an elapsed `usage_ends_at` is possible; status does not imply usability |
| 24 | ListCards | (silent) | `canceled` (cards) versus `cancelled` (invoicing) in one API version; the filter rejects the wrong spelling |
| 25 | GetCard | `id` is "string, format uuid" | Five spellings accepted (no dashes, braces, `urn:uuid:`, uppercase), normalised only in the body |
| 26 | all seven | Errors are RFC 9457 problem details with `type` example `about:blank` | Three dialects in practice: `about:blank` with `detail`, numeric `1317`/`1303`/`2` without `detail`, and a plain-text `404 page not found` for unrouted paths |
## 5. Endpoint reference: Statements, Invoicing and the file endpoints

This section covers the remaining seven operations of the `v1` surface. Accounts, Cards and Transactions are in the section "Endpoint reference: Accounts, Cards and Transactions"; cursor mechanics are in "Pagination"; token format, scopes and the 401 body are in "Authentication and scopes"; the full error-code catalogue is in "Errors and failure modes". Everything below assumes the shared contract described there: integer minor units paired with an ISO 4217 `currency`, ISO 8601 UTC timestamps, RFC 9457 `application/problem+json` errors, and read-only `GET` access (every write verb on every path in this section returns `405` with `Allow: GET` and an empty body).

All observed behavior in this section was reproduced live against `https://rhoapi-sandbox.rho.co/api/v1` on 2026-09-12 between 00:24Z and 00:31Z UTC, with `Authorization: Bearer sandbox`. Sandbox accepts any non-empty bearer token. Every command below is runnable as written after:

```bash
export RHO=https://rhoapi-sandbox.rho.co/api/v1
export RHO_API_TOKEN=sandbox
```

For production substitute `https://rhoapi.rho.co/api/v1` and a real `rhobat_`-prefixed token.

### 5.1 The seven operations

| Operation id | Method and path | Scope | Returns |
| --- | --- | --- | --- |
| `liststatements` | `GET /statements` | `statements:read` | `{ statements: [...], page: {...} }` |
| `getstatement` | `GET /statements/{id}` | `statements:read` | bare `Statement` |
| `listinvoicinginvoices` | `GET /invoicing/invoices` | `invoicing:read` | `{ invoices: [...], page: {...} }` |
| `getinvoicinginvoice` | `GET /invoicing/invoices/{invoice_id}` | `invoicing:read` | bare `Invoice` |
| `getinvoicinginvoicefile` | `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | `invoicing:read` | `{ file_id, file_name, download_url }` |
| `listinvoicingcustomers` | `GET /invoicing/customers` | `invoicing:read` | `{ customers: [...], page: {...} }` |
| `getinvoicingcustomer` | `GET /invoicing/customers/{customer_id}` | `invoicing:read` | bare `Customer` |

The scope column is inferred, not stated per operation. The official per-operation reference pages carry only `Security: AccessToken`; the scope list appears once, on the OpenAPI index page (`docs.rho.co/api/v1/openapi`), which enumerates `accounts:read`, `cards:read`, `invoicing:read`, `statements:read`, `transactions:read`. The Invoicing guide adds that "Every endpoint requires the `invoicing:read` scope."

> **Divergence:** the Authentication guide lists only three scopes (`accounts:read`, `transactions:read`, `statements:read`). It omits both `cards:read` and `invoicing:read`, which the OpenAPI index does list. An integrator who provisions a token from the Authentication page alone will not know `invoicing:read` exists. Related: the Getting Started page still says "Current release is read-only and covers accounts and transactions", which was true of an earlier release and is not true of `v1` as shipped.

A structural point that saves work across all seven: **the single-resource GET returns exactly the same fields as the list element.** A prior exhaustive sweep compared all 146 sandbox resources across six resource types (14 accounts, 8 cards, 72 transactions, 33 statements, 7 customers, 12 invoices) and found 146 of 146 deep-equal, zero keys present only in the single GET, zero value differences. There is no summary-versus-detail tier anywhere in `v1`. Looping single GETs to enrich list rows buys nothing and burns the documented ~60 requests per minute per token. The single exception is `GET /statements/{id}`, which buys a possibly re-signed `pdf_url` and nothing else (see 5.6).

---

### 5.2 Read this first: the invoice file endpoint returns 404 on every documented-correct pairing

> **Divergence:** `GET /invoicing/invoices/{invoice_id}/files/{file_id}` is documented as the way to exchange an invoice's `file_id` for a signed PDF link. In sandbox it returns `404 {"type":"1303","title":"invoice file not found","status":404}` for **every one of the 9 invoices that advertise a `file_id`**, using exactly the `invoice_id` and `file_id` values those invoices return. Invoice PDF retrieval cannot be integration-tested against the Rho sandbox at all.

The Invoicing guide is explicit about the flow that fails:

> "When an invoice has a PDF, `file_id` is present. When no PDF exists, the field is omitted. Use `GET /invoicing/invoices/{invoice_id}/files/{file_id}` to exchange it for a fresh, short-lived `download_url`; do not persist that URL."

Observed, 2026-09-12 00:25Z. Reproduce the whole sweep:

```bash
curl -s "$RHO/invoicing/invoices?page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json
for i in json.load(sys.stdin)["invoices"]:
    if "file_id" in i:
        print(i["invoice_number"], i["id"], i["file_id"])
' \
| while read num iid fid; do
    code=$(curl -s -o /dev/null -w "%{http_code}" \
      "$RHO/invoicing/invoices/$iid/files/$fid" \
      -H "Authorization: Bearer $RHO_API_TOKEN")
    echo "$num $fid -> $code"
  done
```

Result, all nine:

| Invoice | `invoice_id` | `file_id` | HTTP |
| --- | --- | --- | --- |
| INV-2026-0070 | `70000000-0000-4000-8000-000000000010` | `50000000-0000-4000-8000-000000000027` | 404 |
| INV-2026-0066 | `70000000-0000-4000-8000-000000000002` | `50000000-0000-4000-8000-000000000021` | 404 |
| INV-2026-0060 | `70000000-0000-4000-8000-000000000003` | `50000000-0000-4000-8000-000000000022` | 404 |
| INV-2026-0052 | `70000000-0000-4000-8000-000000000011` | `50000000-0000-4000-8000-000000000028` | 404 |
| INV-2026-0050 | `70000000-0000-4000-8000-000000000008` | `50000000-0000-4000-8000-000000000026` | 404 |
| INV-2026-0045 | `70000000-0000-4000-8000-000000000005` | `50000000-0000-4000-8000-000000000024` | 404 |
| INV-2026-0043 | `70000000-0000-4000-8000-000000000007` | `50000000-0000-4000-8000-000000000025` | 404 |
| INV-2026-0040 | `70000000-0000-4000-8000-000000000004` | `50000000-0000-4000-8000-000000000023` | 404 |
| INV-2026-0002 | `70000000-0000-4000-8000-000000000001` | `50000000-0000-4000-8000-000000000020` | 404 |

The remaining 3 invoices (INV-2026-0065, INV-2026-0041, INV-2026-0001) omit `file_id` entirely, so per the documented contract they have no PDF and are not expected to work.

#### Why this is a fixture gap and not a missing route

Four probes localize the failure precisely. Run them and you can stop suspecting your own code.

```bash
INV=70000000-0000-4000-8000-000000000010
FID=50000000-0000-4000-8000-000000000027

# 1. Documented-correct pairing: 404, the handler ran and the invoice resolved.
curl -s "$RHO/invoicing/invoices/$INV/files/$FID" -H "Authorization: Bearer $RHO_API_TOKEN"

# 2. Malformed file_id: 400 from the validation layer, so the route exists and parses.
curl -s "$RHO/invoicing/invoices/$INV/files/abc" -H "Authorization: Bearer $RHO_API_TOKEN"

# 3. Unknown invoice, known file_id: the error names the INVOICE, not the file.
curl -s "$RHO/invoicing/invoices/70000000-0000-4000-8000-999999999999/files/$FID" \
  -H "Authorization: Bearer $RHO_API_TOKEN"

# 4. Control: the equivalent transactions endpoint works in the same sandbox.
curl -s "$RHO/transactions/019f0554-0bf0-7000-8000-00000000000a/files/2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

| Probe | HTTP | Body |
| --- | --- | --- |
| 1. correct pairing | 404 | `{"type":"1303","title":"invoice file not found","status":404}` |
| 2. malformed `file_id` | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: file_id"}` |
| 3. unknown `invoice_id` | 404 | `{"type":"1303","title":"invoice not found","status":404}` |
| 4. transaction file control | 200 | `{"download_url":"https://rho-api-sandbox.files.rho.co/f0b72b6108f6ebfd9818fb0f.pdf?...","file_id":"2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15","file_name":"parking-receipt.pdf"}` |

Reading: probe 2 proves the route is mounted and its parameter validation runs. Probe 3 proves the handler resolves the invoice first and reports `invoice not found` when it cannot, so the `invoice file not found` in probe 1 means the invoice resolved and the **file** did not. Probe 4 proves the signed-URL machinery is alive in this sandbox. The conclusion is that the invoice objects advertise `file_id` values with no blob behind them. It is a fixture-data gap in the invoicing domain, not a sandbox-wide gap and not a routing bug.

Two further observations that matter when you write error handling:

- A real `file_id` under the wrong invoice returns the identical `404 invoice file not found`. Observed: `file_id` `...0027` (belonging to INV-2026-0070) requested under invoice `70000000-0000-4000-8000-000000000002` returns 404, not 403. This is correct IDOR-resistant behavior, but it means a genuine "wrong parent", a genuine "file absent", and this fixture gap are **indistinguishable from the response alone**.
- Requesting any `file_id` on an invoice that omits `file_id` also returns `404 invoice file not found`. Observed against `70000000-0000-4000-8000-000000000006`.

#### What to do about it

1. Build and unit-test invoice PDF retrieval against the **transaction** file endpoint (`GET /transactions/{transaction_id}/files/{file_id}`). The response schema is byte-identical: three fields, `file_id`, `file_name`, `download_url`. The signed-URL semantics in 5.6 apply to both.
2. Do not treat `404` from this endpoint as "this invoice has no PDF". Use the presence of `file_id` on the invoice object for that, and treat the 404 as retryable-or-unavailable.
3. Note that the Transactions guide explicitly promises "Sandbox downloads contain non-empty representative fictional documents". **No equivalent promise or disclaimer appears anywhere for invoicing**, so there is no documented statement that invoice PDFs are or are not present in sandbox.
4. Verify against production before you ship. Nothing in this section establishes that the production endpoint is broken; the finding is specific to the sandbox fixture set, and production could not be probed beyond unauthenticated metadata.

---

### 5.3 Statements

#### 5.3.1 What a statement is

A `statement` record covers **one statement period for one statement type**. Period-level fields sit at the top level; the money lives in an `accounts` array. Per the Statements guide, statements are "the finalized, period-end documents Rho issues for the accounts your business holds", and `GET /statements` "Spans all statement types and all accounts in one aggregated surface."

Full payload, observed via `GET /statements/439950` (signature elided for width):

```json
{
  "id": "439950",
  "statement_type": "account",
  "period_start": "2025-05-01",
  "period_end": "2025-05-31",
  "available_at": "2025-06-02T00:31:23Z",
  "pdf_url": "https://sandbox-statements.files.rho.co/4f7150d8341cae23c6ffa33a.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=file-service%40pledge-218909.iam.gserviceaccount.com%2F20260912%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260912T002403Z&X-Goog-Expires=899&X-Goog-Signature=<512 hex chars>&X-Goog-SignedHeaders=host",
  "accounts": [
    {
      "account_id": "30000000-0000-4000-8000-000000000006",
      "account_type": "checking",
      "opening_balance": { "amount": 946209, "currency": "USD" },
      "closing_balance": { "amount": 972409, "currency": "USD" },
      "total_credits":   { "amount": 26200,  "currency": "USD" },
      "total_debits":    { "amount": 0,      "currency": "USD" },
      "total_fees":      { "amount": 0,      "currency": "USD" }
    }
  ]
}
```

Top-level fields:

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `id` | string | yes | "Global statement identifier". Observed: a **numeric string**, not a UUID. Two disjoint ranges in the sandbox: credit `152980` to `200527`, deposit and treasury `428772` to `572981`. Treat as opaque. |
| `period_start` | string (date) | yes | First day of the period, inclusive. |
| `period_end` | string (date) | yes | Close date of the period, inclusive. |
| `available_at` | string (date-time) | yes | When the finalized statement became retrievable. |
| `pdf_url` | string | **no** | Signed download URL, documented "valid for up to 15 minutes", or `null` "when the document cannot be linked". See 5.6. |
| `statement_type` | string | **no** | Enum `account`, `credit`, `treasury`. Not marked required even though all 33 sandbox records carry it. |
| `accounts` | array | yes | Per-account figures. See below. |

#### 5.3.2 The per-account breakdown

Each entry in `accounts` carries one account's figures for the period. Every monetary value is a `Money` object `{ "amount": <integer minor units>, "currency": "<ISO 4217>" }`. There is no scalar amount anywhere in the statement object.

| Field | Type | Marked required | Applies to | Notes |
| --- | --- | --- | --- | --- |
| `account_id` | string | **no** | all | Documented "Null for credit statements, which are not tied to a deposit account". See the divergence below. |
| `account_type` | string | yes | all | Enum `checking`, `savings`, `credit`, `treasury`. |
| `opening_balance` | Money | yes | all | Balance as of the start of `period_start`. |
| `closing_balance` | Money | yes | all | Balance at the close date. The guide calls this "the reconciliation anchor". |
| `total_credits` | Money | yes | all | Sum of credits posted in the period. |
| `total_debits` | Money | yes | all | Sum of debits posted in the period. |
| `total_fees` | Money | yes | all | Fees charged in the period. |
| `repayment_date` | string (date) | no | credit only | Date repayment is or was due. **Never emitted**, see below. |
| `spending` | Money | no | credit only | Total card spend in the period. |
| `repayments` | Money | no | credit only | Repayments applied in the period. |
| `cashback` | Money | no | credit only | Cashback earned in the period. |

The credit-only fields are **omitted keys** on non-credit entries, not nulls. Observed across all 33 sandbox statements: the key set `{spending, repayments, cashback}` is present on exactly the 22 credit entries and absent on the other 11. `repayment_date` is present on 0 of 33.

```bash
curl -s "$RHO/statements?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json
from collections import Counter
st = json.load(sys.stdin)["statements"]
print("statements:", len(st))
print("types:", Counter(s["statement_type"] for s in st))
print("accounts[] lengths:", Counter(len(s["accounts"]) for s in st))
print("credit entries with null account_id:",
      sum(1 for s in st for a in s["accounts"]
          if a["account_type"] == "credit" and a.get("account_id") is None))
print("entries carrying repayment_date:",
      sum(1 for s in st for a in s["accounts"] if "repayment_date" in a))
print("null pdf_url:", sum(1 for s in st if s.get("pdf_url") is None))
'
```

Observed output:

```
statements: 33
types: Counter({'credit': 22, 'treasury': 7, 'account': 4})
accounts[] lengths: Counter({1: 33})
credit entries with null account_id: 0
entries carrying repayment_date: 0
null pdf_url: 0
```

That single command demonstrates four separate divergences at once.

> **Divergence:** `account_id` is documented as null on credit statements. It is non-null on all 22 sandbox credit statements, which carry `30000000-0000-4000-8000-000000000007` or `...0008`. Both IDs resolve in `GET /accounts` as real `account_type: "credit"` accounts named "Credit Account". Worse, filtering by a credit account works: `GET /statements?account_id=30000000-0000-4000-8000-000000000008&page_size=100` returns 11 credit statements, which the documented model says should be impossible. Code that detects credit statements with `account_id is None` will be wrong on every record. Use `statement_type == "credit"` or `accounts[].account_type == "credit"` instead.

> **Divergence:** `repayment_date` is documented on both statement reference pages and in the guide's per-account table as the credit repayment due date. It is absent from all 33 sandbox statements, via both `GET /statements` and `GET /statements/{id}`. There is no way to learn a credit statement's repayment due date from this API. This matters because it is the only credit-terms field in the entire surface: there is no minimum payment, no amount due, no APR and no credit limit anywhere in `v1`.

> **Divergence:** consolidated multi-account statements do not occur. The guide devotes a section, "Filtering by account", to the fact that account and treasury statements "may span multiple checking/savings accounts" and that "a matched statement's `accounts` array and PDF may include additional accounts belonging to your business". All 33 sandbox statements have exactly one `accounts` entry. The stronger evidence is a matched pair: statements `439950` (checking `...0006`) and `439951` (savings `...0013`) cover the same period 2025-05-01 to 2025-05-31, share the same `available_at` of `2025-06-02T00:31:23Z`, and have consecutive IDs. That is one statement per account, not one consolidated statement. The consolidation caveat is unverifiable here, so write the `accounts` loop defensively but do not design around consolidation you cannot observe.

> **Divergence:** `accounts[].account_type` in a statement disagrees with the same account's type in `GET /accounts`, and the two enums are disjoint in both directions. Statement `572981` reports `account_type: "treasury"` for account `30000000-0000-4000-8000-000000000004`; `GET /accounts` reports that same account as `account_type: "checking"`, `account_name: "Treasury Checking"`. The statements enum is `checking, savings, credit, treasury`; the accounts enum is `checking, credit, investment, savings, rewards`. `treasury` exists only in statements, `investment` and `rewards` only in accounts. Do not join on `account_type` across the two APIs. Join on `account_id`, which is consistent.

Observed cross-check:

```bash
curl -s "$RHO/statements/572981" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); a=d["accounts"][0]; print(d["statement_type"], a["account_id"], a["account_type"])'
# treasury 30000000-0000-4000-8000-000000000004 treasury

curl -s "$RHO/accounts?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; print([(a["account_type"], a["account_name"]) for a in json.load(sys.stdin)["accounts"] if a["id"].endswith("0004")])'
# [('checking', 'Treasury Checking')]
```

Two further statement-data facts that are not divergences but will break naive reconciliation:

- **Credit statements report `total_credits`, `total_debits` and `total_fees` as zero on all 22 records**, even where `spending` is 6,931,038 minor units. The three "required" totals are useless for credit reconciliation. The guide's advice, to anchor on `closing_balance` and use the credit trio for the card line, is the only workable path, and it does not say why the totals are empty.
- **Sign conventions are undocumented and inconsistent.** Statement `200527` has `spending: 6931038`, `repayments: -69221`, `cashback: 103965`. Statement `161396` has `spending: -26200`, `repayments: 26200`, `cashback: -327`. No reference states whether these are signed or absolute, or what a negative means. Take absolute values at your own risk.

#### 5.3.3 `GET /statements`

```bash
curl -s "$RHO/statements?period_end_after=2026-05-01&period_end_before=2026-06-01&page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

| Parameter | Type | Documented | Observed |
| --- | --- | --- | --- |
| `account_id` | array | "Return complete statements that include at least one requested account. Multiple values use OR semantics." | Confirmed. Repeated-key array style. `account_id=...0006&account_id=...0013` returns 4 statements (3 for 0006, 1 for 0013). An account with no statements returns `200` and an empty array, not 404. A malformed value returns `400 {"type":"about:blank",...,"detail":"invalid parameter: account_id"}`. |
| `statement_type` | array | "Filter by statement type". Enum not restated on the parameter. | Multi-value OR confirmed. **Unvalidated**: `statement_type=bogus` returns `200` with `"statements":[]`, not a 400. |
| `period_end_after` | string (date) | "Earliest statement close date, **inclusive**" | Confirmed inclusive. `period_end_after=2026-05-31` returns statement `572981`, whose `period_end` is 2026-05-31. |
| `period_end_before` | string (date) | "Latest statement close date, **exclusive**" | Confirmed exclusive. `period_end_after=2026-05-31&period_end_before=2026-05-31` returns 0 rows; `...&period_end_before=2026-06-01` returns 1. |
| `period_start_after` | string (date) | "Earliest statement open date, inclusive" | Confirmed. |
| `period_start_before` | string (date) | "Latest statement open date, exclusive" | Confirmed. |
| `sort_by` | string | "Sort field". No enum, no default given. | **Inert.** `sort_by=period_start`, `period_end`, `available_at`, `id`, `created_at` and `bogus` all return identical ordering and no error. It is nonetheless hashed into the pagination cursor, so changing it mid-iteration invalidates your cursor for no benefit. |
| `order` | string | "Sort direction". No enum, no default given. | Anything that lowercases to `asc` yields ascending. Every other value, including `BOGUS` and omission, yields descending. No 400 for invalid input. Observed: default first ID `572981`, `order=asc` first ID `428772`, `order=BOGUS` first ID `572981`. |
| `page_size` | integer | "Number of statements per page; max 100". Default not documented. | Default **20**. Bounds 1 to 100 enforced: `page_size=0` and `page_size=101` both return `400 {"type":"1317","title":"page_size must be between 1 and 100","status":400}`. |
| `page_token` | string | Opaque cursor from `page.next_page_token`. | See "Pagination". |

Dates accept `YYYY-MM-DD`. A non-ISO value such as `05/01/2026` returns `400` with `detail: "invalid parameter: period_end_after"`. Unknown query parameters are silently ignored with a `200`.

> **Divergence:** `*_before` means **exclusive** on statements and **inclusive** on invoicing, in the same API version, with the same idiom. Both pages document their own behavior correctly and both were verified live, so this is a deliberate asymmetry rather than a documentation bug. It is still a footgun for any shared date-range helper. See 5.4.1 for the invoicing verification.

> **Divergence:** parameter validation strictness is inconsistent across endpoints. `/statements` silently ignores an unknown `sort_by` or `order`; `/invoicing/customers` hard-rejects both with `400 {"type":"1317",...}`. Same parameter names, same version, opposite contracts. Do not write one shared "these params are safe" assumption.

**Conspicuously absent from the filter set:** there is no `available_at_after` or `available_at_before`. The guide's headline workflow is "List statements **as they become available**", and the API gives you no way to ask "what has been finalized since T". Incremental polling requires rescanning by period window and diffing IDs yourself. There is also no batch fetch by ID list, no currency filter, and no way to project only your requested account's figures out of a statement, which the guide states outright: filtering "does not remove those entries or alter the PDF".

#### 5.3.4 `GET /statements/{id}`

Path parameter `id`, string, no format stated. Response is the bare `Statement` object, identical field set to a list element, with no wrapper and no `page`.

```bash
curl -s "$RHO/statements/200527" -H "Authorization: Bearer $RHO_API_TOKEN"
```

Its documented purpose beyond simple retrieval is as the refresh mechanism for an expired `pdf_url`: "If the link lapses, re-fetch the statement with `GET /statements/{id}` for a fresh URL." That remedy does not work the way it reads. See 5.6.3.

Error behavior differs from every other resource in `v1`, because the statement ID is an opaque string rather than a UUID and therefore gets no format validation:

| Request | HTTP | Body |
| --- | --- | --- |
| `GET /statements/999999999` | 404 | `{"type":"1303","title":"statement not found","status":404}` |
| `GET /statements/abc` | 404 | same |
| `GET /statements/-1` | 404 | same |
| `GET /statements/200527/files/x` | 404 | `404 page not found` (plain text, from the Go router, not problem+json) |

> **Divergence:** for accounts, cards, transactions, invoices and customers a malformed ID is a `400` with `detail: "invalid parameter: <name>"`. For statements it is a `404`. Do not validate statement IDs as UUIDs client-side, and do not treat 400-versus-404 as a uniform contract across the API.

Note the last row: **there is no `GET /statements/{id}/files/{file_id}` analogue.** Statements are the only resource in `v1` that embeds a signed URL directly in its payload, and the only refresh path is a full single-statement re-fetch.

#### 5.3.5 Statement census and timing

The sandbox fixture, observed 2026-09-12, is 33 statements, all USD, `period_start` from 2024-07-01 to 2026-05-01.

| `statement_type` | Count | Accounts involved | ID range |
| --- | --- | --- | --- |
| `credit` | 22 | `...0007` (calendar-month cycle), `...0008` (13th to 12th cycle) | 152980 to 200527 |
| `treasury` | 7 | `...0004` | 462701 to 572981 |
| `account` | 4 | `...0006` checking, `...0013` savings | 428772 to 439951 |

Two backing ID ranges, consistent with a deposit ledger and a card ledger stitched into "one aggregated surface". The Versioning guide already tells you to "Treat IDs as opaque strings"; this is why.

`available_at` lag varies by type and is documented only on the product side, not in the API:

| Type | Observed lag | Help-center rule |
| --- | --- | --- |
| `account` (checking, savings) | available on the 2nd of the following month, 00:20Z to 00:31Z | "Checking Account Statements are available on the second calendar day of every month"; "Savings Account Statements are available by the end of the fifth business day of each month" |
| `credit` | the day after `period_end`, 04:00Z to 05:02Z | Card accounts with Daily Terms "on the fifth of every month"; with Monthly Terms "one business day following the statement repayment date" |
| `treasury` | between the 5th and the 8th, 21:00Z to 22:06Z | not covered by the help-center page |

> **Divergence:** the savings statement `439951` became available at `2025-06-02T00:31:23Z`, that is the 2nd of the month, not "by the end of the fifth business day" as the help center states for savings. Neither the observed treasury lag nor the observed credit cycle for account `...0008` (13th to 12th) corresponds to any documented rule. Nothing in the API exposes the billing cycle or the terms; you have to infer them from `period_start` and `period_end`.

Also undocumented: whether a statement can ever be reissued or restated after `available_at`, and what condition produces a `null` `pdf_url`. Zero of 33 sandbox records exercise the null case.

---

### 5.4 Invoicing: invoices

Two resources plus one file exchange. Customers are "the businesses you bill" and are soft-deletable. Invoices are "issued documents" and reference exactly one customer by ID. An invoice has at most one PDF, addressed by `file_id`.

IDs in this domain are UUIDs, as the guide states: customers `60000000-0000-4000-8000-00000000000X`, invoices `70000000-0000-4000-8000-0000000000XX`, invoice files `50000000-0000-4000-8000-000000000XXX`, users `40000000-0000-4000-8000-00000000000X`. Note that invoice IDs are UUIDs while **statement IDs are not**, inside the same `v1` surface. Transaction IDs, which appear on invoice payments, are UUIDv7-shaped, a third format again.

#### 5.4.1 `GET /invoicing/invoices`

"Results are ordered by creation time, newest first. Ordering is not user-configurable; keep filters unchanged while paginating."

| Parameter | Type | Documented | Observed |
| --- | --- | --- | --- |
| `status` | array | "Filter by one or more invoice statuses" | Multi-value OR confirmed. **Unvalidated**: `status=draft`, `status=sent` and `status=bogus` all return `200` with zero rows rather than a 400. Since `draft` and `sent` are plausible-sounding non-values (see 5.4.4), this silently returns an empty result for a reasonable-looking query. |
| `date_after` | string (date) | "Earliest invoice issue date to include, inclusive" | Confirmed. |
| `date_before` | string (date) | "Latest invoice issue date to include, **inclusive**" | Confirmed inclusive. |
| `due_date_after` | string (date) | "Earliest invoice due date to include, inclusive" | Confirmed. |
| `due_date_before` | string (date) | "Latest invoice due date to include, **inclusive**" | Confirmed inclusive: `due_date_after=2026-07-31&due_date_before=2026-07-31` returns INV-2026-0066, due exactly 2026-07-31. |
| `page_size` | integer | "Defaults to 20." Max not documented. | Default 20 confirmed. Bounds 1 to 100 enforced with the same `1317` body as statements. |
| `page_token` | string | Cursor; "keep all filters unchanged". | See "Pagination". |

`sort_by` and `order` are **not documented parameters here**. Observed: they are accepted and ignored. `GET /invoicing/invoices?sort_by=date&order=asc` returns INV-2026-0070 first, identical to the unparameterized call. That is consistent with "Ordering is not user-configurable".

**Conspicuously absent: there is no `customer_id` filter.** There is no supported way to list one customer's invoices. `?customer_id=60000000-0000-4000-8000-000000000001` is silently ignored and returns all 12 rows. The only customer-to-invoice link the API offers is `customer.last_invoice_id`, a single most-recent pointer. Per-customer AR ageing therefore requires pulling every invoice and grouping client-side. Also missing: `invoice_number` lookup, free-text search, `created_at` or `updated_at` ranges, and an `accounting_sync_status` filter, so you cannot ask "which invoices failed to sync". There is no `include_deleted` for invoices either; passing it is ignored and returns all 12.

#### 5.4.2 The invoice object

Identical in list and get. Full payload, observed via `GET /invoicing/invoices/70000000-0000-4000-8000-000000000001`:

```json
{
  "id": "70000000-0000-4000-8000-000000000001",
  "invoice_number": "INV-2026-0002",
  "total": { "amount": 108403, "currency": "USD" },
  "tax_rate": 10,
  "discount_rate": 0,
  "status": "paid",
  "note": "Net 30 terms apply.",
  "date": "2026-01-16",
  "due_date": "2026-02-15",
  "customer": { "id": "60000000-0000-4000-8000-000000000001" },
  "line_items": [
    { "name": "Consulting Services - January", "quantity": 1, "discount_rate": 0, "tax_rate": 10,
      "unit_price": { "amount": 90000, "currency": "USD" },
      "total":      { "amount": 90000, "currency": "USD" } },
    { "name": "Travel reimbursement", "quantity": 1, "discount_rate": 0, "tax_rate": 0,
      "unit_price": { "amount": 9403, "currency": "USD" },
      "total":      { "amount": 9403, "currency": "USD" } }
  ],
  "payments": [
    { "type": "received_in_account", "external_method": null,
      "paid_at": "2026-06-21", "transaction_id": "019eebb0-0938-7000-8000-00000000000b" }
  ],
  "activities": [
    { "activity_type": "created",           "created_at": "2026-01-16T14:32:07Z", "user_id": "40000000-0000-4000-8000-000000000001", "emails": [] },
    { "activity_type": "sent",              "created_at": "2026-01-16T15:00:00Z", "user_id": "40000000-0000-4000-8000-000000000001", "emails": ["info@acmesupplies.com", "ap@acmesupplies.com"] },
    { "activity_type": "downloaded",        "created_at": "2026-01-17T09:12:00Z", "user_id": "40000000-0000-4000-8000-000000000003", "emails": [] },
    { "activity_type": "matched",           "created_at": "2026-06-21T19:37:23Z", "user_id": null, "emails": [] },
    { "activity_type": "marked_as_paid",    "created_at": "2026-06-21T19:38:00Z", "user_id": "40000000-0000-4000-8000-000000000003", "emails": [] },
    { "activity_type": "accounting_synced", "created_at": "2026-06-21T20:00:00Z", "user_id": null, "emails": [] }
  ],
  "file_id": "50000000-0000-4000-8000-000000000020",
  "accounting_sync_status": "synced",
  "accounting_synced_at": "2026-06-21T20:00:00Z",
  "created_at": "2026-01-16T14:32:07Z",
  "updated_at": "2026-06-21T20:00:00Z"
}
```

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `id` | string (UUID) | yes | Stable invoice identifier. |
| `invoice_number` | string | yes | Human-readable. Observed `INV-2026-0001` through `INV-2026-0070` with gaps. Not monotonic with `created_at` ordering and not contiguous, so never infer a count from it. |
| `total` | Money | yes | Tax-inclusive, discount-applied. Derivation in 5.4.3. |
| `tax_rate` | number | yes | Invoice-level tax **percentage**, not basis points. Observed `0`, `6.25`, `8.5`, `10`; fractional values occur. |
| `discount_rate` | number | yes | Invoice-level discount percentage. Observed `0` on 11 invoices, `5` on one. |
| `status` | string | yes | Six values. See 5.4.4. |
| `note` | string | yes | Free text shown to the customer. Marked required but **null on 3 of 12**. May contain any Unicode; INV-2026-0043's note contains a literal `U+2014` character, so do not assume ASCII. |
| `date` | string (date) | yes | Issue date. |
| `due_date` | string (date) | yes | "null when not set". Never null in sandbox, but documented nullable. |
| `customer` | object | yes | Contains **only** `customer.id`. No embedded name or email, so rendering an invoice always costs a second call to `/invoicing/customers/{id}`. |
| `line_items` | array | yes | See below. |
| `payments` | array | yes | May be empty; 5 of 12 have none. See 5.4.5. |
| `activities` | array | yes | Never empty; always at least `created`. See 5.4.6. |
| `file_id` | string (UUID) | **no** | Present on 9 of 12. **Key omitted entirely** when absent, never null. |
| `accounting_sync_status` | string | yes | Five values. See 5.4.7. |
| `accounting_synced_at` | string (date-time) | yes | Marked required but **null on 5 of 12**. |
| `created_at` | string (date-time) | yes | The list sort key. No description in the reference. |
| `updated_at` | string (date-time) | yes | Always at or after `created_at`. |

`line_items[]`:

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | The only text field on a line. |
| `unit_price` | Money | yes | Before line-level discount and tax. |
| `quantity` | number | yes | **Fractional allowed**. Observed `2.5` on INV-2026-0066. |
| `discount_rate` | number | yes | Line-level discount percentage. |
| `tax_rate` | number | yes | "When null, the invoice-level `tax_rate` applies." Marked required and **null is the common case**, 10 of 16 sandbox lines. |
| `total` | Money | yes | Line total **after discount, before tax**. |

There is no line ID, no description separate from `name`, no unit of measure, no per-line GL code, and no ordering index.

**Conspicuously absent from the invoice object:** no invoice-level currency (only inside each `Money`), no subtotal, no tax amount, no discount amount, no amount paid, no amount due or balance, no payment-terms string (the UI collects Net 30 and Due on receipt), no recurrence or schedule field (the UI offers "Schedule this invoice to repeat"), no public payment-portal URL, no `sent_at`, and no `deleted_at`.

Because the list and get payloads are identical, **the list endpoint already returns the full activity log and every payment for every invoice**. A 100-invoice page carries 100 embedded activity arrays and there is no `expand` or `fields` parameter to trim it.

#### 5.4.3 How `total` is computed

Neither the guide nor the reference pages state the arithmetic, and the API exposes neither a subtotal nor a tax amount. Any consumer rendering an invoice must reimplement it. Derived and verified against all 12 sandbox invoices:

```
line.total.amount    = round( quantity * unit_price.amount * (1 - line.discount_rate/100) )

effective_tax(line)  = line.tax_rate if line.tax_rate is not None else invoice.tax_rate

invoice.total.amount = round( SUM( line.total.amount * (1 + effective_tax(line)/100) )
                              * (1 - invoice.discount_rate/100) )
```

Re-verified live, 12 of 12 exact, on 2026-09-12:

```bash
curl -s "$RHO/invoicing/invoices?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json
for i in json.load(sys.stdin)["invoices"]:
    sub = sum(l["total"]["amount"] * (1 + (l["tax_rate"] if l["tax_rate"] is not None else i["tax_rate"]) / 100)
              for l in i["line_items"])
    computed = round(sub * (1 - i["discount_rate"] / 100))
    print(i["invoice_number"], computed, i["total"]["amount"],
          "OK" if computed == i["total"]["amount"] else "MISMATCH")
'
```

Three non-obvious rules this establishes:

1. **Discounts compound.** INV-2026-0045 applies a 5 percent line discount (80,000 to 76,000) and then a 5 percent invoice discount (76,000 to 72,200). The invoice discount applies to the post-line-discount, post-tax subtotal, not to the gross.
2. **Tax is per line, using the line rate when set and the invoice rate when null, then summed.** It is not one invoice-level rate on a subtotal. INV-2026-0066 proves it: a flat 10 percent on its 146,000 subtotal would give 160,600, but the actual total is 158,000 because two of its four lines carry an explicit `tax_rate: 0` while the other two carry `null` and inherit the invoice's 10 percent.
3. **Rounding is to the nearest minor unit at the invoice level.** INV-2026-0052 computes to 45000.0625 and states 45000. One sample is not enough to distinguish half-up from half-even from truncation.

#### 5.4.4 Status: the complete enum and the lifecycle

`status` is "Lifecycle status of an invoice in Invoicing". Exactly six values, in reference order:

| Value | Meaning | Sandbox count | Example |
| --- | --- | --- | --- |
| `paid` | Payment complete. For the card rail the help center says "Once the payout is initiated, the invoice status changes to Paid." | 4 | INV-2026-0050, 0040, 0002, 0001 |
| `unpaid` | Issued, not yet paid. | 2 | INV-2026-0065, 0052 |
| `cancelled` | Voided by the business. British spelling. | 1 | INV-2026-0041 |
| `overdue` | Past due and unpaid. | 2 | INV-2026-0060, 0045 |
| `confirm_payment` | Funds arrived in the Rho account and were matched, awaiting confirmation or allocation by the business. | 1 | INV-2026-0043 |
| `pending_payout` | Card payment captured by Stripe, payout to the Rho checking account not yet initiated. Help center: "The invoice is marked Pending payout while Stripe prepares the deposit." | 2 | INV-2026-0070, 0066 |

**The enum has no `draft` and no `sent`.** The "sent" concept exists only as an activity, so an API consumer cannot distinguish an invoice created but never emailed from one that was emailed, except by scanning `activities` for `activity_type == "sent"`. Rho's own help copy for creating an invoice ends at "You'll see a confirmation once your invoice is successfully created and ready to send", which implies a pre-send state the API does not model.

Lifecycle reconstructed from the sandbox activity logs. Every edge below is backed by a specific record.

```text
created ──> unpaid ──> (sent) ──> unpaid ──> overdue                     [due date passes]
                           │
                           ├─> matched ──> confirm_payment ──> marked_as_paid ──> paid    [bank rail]
                           ├─> card_payment_received ──> pending_payout ──> paid          [card rail, Stripe]
                           ├─> marked_as_paid ──> paid                                    [manual, external payment]
                           └─> cancelled ──> cancelled                                    [terminal]

marked_as_paid ──> marked_as_unpaid                                      [reversal, observed]
```

| Edge | Evidence |
| --- | --- |
| Bank rail, mid-state | INV-2026-0043: activity `matched` at `2026-05-18T00:07:03Z`, one `received_in_account` payment with `transaction_id: 019e3868-5858-7000-8000-00000000001a`, status `confirm_payment`. |
| Bank rail, completion | INV-2026-0002: `matched` at `2026-06-21T19:37:23Z`, then `marked_as_paid` at `2026-06-21T19:38:00Z`, 37 seconds later, status `paid`. So `confirm_payment` is the state between match and human confirmation. |
| Card rail | INV-2026-0070: `card_payment_received` at `2026-07-18T08:00:00Z`, status `pending_payout`, payment recorded as `external` / `credit_card`. |
| Reversal | INV-2026-0066: `marked_as_paid` at `2026-07-20T09:00:00Z`, then `marked_as_unpaid` at `2026-07-20T09:05:00Z` with `user_id: null`, then `card_payment_received` at `2026-07-24T10:00:00Z`, status `pending_payout`. |
| Cancellation terminal | INV-2026-0041: activities are only `created` and `cancelled`, with no `sent`. |

> **Divergence:** `status` is stored, not derived. INV-2026-0065 is `unpaid` with `due_date` 2026-08-15 and INV-2026-0052 is `unpaid` with `due_date` 2026-08-20. Both were past due as of the probe date, 2026-09-12, and neither is `overdue`. Do not assume `overdue == (status == "unpaid" AND due_date < today)`. Either the transition is a batch job whose cadence is undocumented, or the fixture is frozen; nothing in the docs says when `unpaid` becomes `overdue`. If your product needs a correct ageing bucket, compute it from `due_date` yourself and treat `status` as advisory for that one question.

Nothing documents whether status can move backwards other than by inference from `marked_as_unpaid`, and there is no refund or chargeback status or activity type anywhere. The Invoicing terms are explicit that Rho "has no obligation to collect, enforce, dispute, or resolve any invoice, chargeback, refund, or customer dispute on your behalf", so the absence is a product boundary, not an oversight.

#### 5.4.5 `payments[]`

| Field | Type | Marked required | Documented | Observed across 7 payments |
| --- | --- | --- | --- | --- |
| `type` | string | yes | Enum `received_in_account`, `external` | 5 `external`, 2 `received_in_account` |
| `external_method` | string | yes | "Set when type is external". Enum `cash`, `check`, `credit_card`, `other` | `credit_card` twice, `check` once, `cash` once, `other` once; `null` on both `received_in_account` rows |
| `paid_at` | string (date) | yes | "User-provided payment date; set for external payments" | **Set on all 7**, including both `received_in_account` rows |
| `transaction_id` | string | yes | "Transaction identifier when type is received_in_account" | Set on the 2 `received_in_account` rows, `null` on all 5 `external` rows |

`transaction_id` values are UUIDv7-shaped and match the ID format of `GET /transactions`, so the join to the ledger is direct. See the Transactions section for that resource.

> **Divergence:** `paid_at` is documented as "set for external payments" but is populated on `received_in_account` payments too. Observed: INV-2026-0043 has `type: "received_in_account"` with `paid_at: "2026-05-18"`, INV-2026-0002 has `paid_at: "2026-06-21"`. Harmless, but a code generator or validator built on the doc text will be surprised.

> **Divergence, and the important one:** a Rho-processed **card** payment is recorded as `type: "external"`, not `received_in_account`. INV-2026-0070 and INV-2026-0066 both show `{"type": "external", "external_method": "credit_card", "transaction_id": null}` while their activity logs contain `card_payment_received` and their status is `pending_payout`, which is the Stripe rail running inside Rho. So `external` does **not** mean "paid outside Rho"; it means "no matched Rho transaction yet". Detect the Rho card rail via the `card_payment_received` activity or `status == "pending_payout"`, never via `payments[].type`. Nothing in the docs warns about this.

**The single largest modelling gap in this surface: there is no per-payment amount field at all.** The API therefore cannot represent a partial payment, an overpayment, or a multi-payment invoice. Every sandbox invoice has at most one payment. The schema neither models nor excludes the multi-payment case, so if your AR workflow allows partial payment you cannot reconcile it from this API.

All four payment fields are marked required and all four are nullable in practice. A strict code generator that emits non-optional types from `required` will fail to deserialise real payloads on `external_method` and `transaction_id`.

Finally, none of the card economics are exposed. The Invoicing terms and the help center state a card processing fee of **2.9 percent plus $0.30 per transaction**, paid by the business, and a **$10,000 per day** card limit across all invoices. There is no fee field, no net-of-fee amount, no payout ID and no Stripe connection status in the API. An integration reconciling a card-paid invoice sees `total: 98000` while the bank receives 98000 minus (2.9 percent plus 30) = 94,858 minor units, with no API-visible link between the two.

#### 5.4.6 `activities[]`: the audit log

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `activity_type` | string | yes | Eleven values, below. |
| `created_at` | string (date-time) | yes | No description in the reference. |
| `user_id` | string (UUID) | yes | "User associated with the activity when available". **Null on 12 of 44** sandbox activities, all system-generated. |
| `emails` | array of string | yes | Always present. Empty array on 32 of 44. |

Complete enum with observed frequency across the 12 sandbox invoices (44 activities total):

| `activity_type` | Count | `user_id` | `emails` | Interpretation |
| --- | --- | --- | --- | --- |
| `created` | 12 | always set | empty | Invoice created. Present on every invoice, and its `created_at` equals the invoice's `created_at` on all 12. |
| `sent` | 10 | always set | 1 or 2 recipients | Invoice emailed. Absent on INV-2026-0041 (cancelled) and INV-2026-0001. |
| `downloaded` | 2 | set | empty | PDF downloaded. |
| `matched` | 2 | **always null** | empty | Incoming bank transaction auto-matched to the invoice. |
| `marked_as_paid` | 5 | set | empty | Manual mark-as-paid. |
| `marked_as_unpaid` | 1 | **null** | empty | Reversal of the above. |
| `cancelled` | 1 | set | empty | Invoice cancelled. |
| `reminder_sent` | 2 | set | 1 or 2 recipients | Dunning email. |
| `card_payment_received` | 2 | **always null** | empty | Stripe card capture. |
| `accounting_synced` | 6 | **always null** | empty | Invoice pushed to the accounting integration. Count matches the 6 invoices at `accounting_sync_status: "synced"`. |
| `payment_accounting_synced` | 1 | **null** | empty | Payment record pushed separately from the invoice. Only INV-2026-0070. |

Ordering: activities are returned **ascending by `created_at`** on all 12 invoices. That is the opposite of the list-level ordering, and it is not documented anywhere.

`emails` reflects the actual send list at the time of the event, primary plus CCs. Observed: INV-2026-0002's `sent` carries `["info@acmesupplies.com","ap@acmesupplies.com"]`, where the second address is one of that customer's `cc_emails`. INV-2026-0060's `reminder_sent` carries `["hello@brightleaf.design","finance@brightleaf.design"]`.

**`user_id` is unresolvable.** There is no user endpoint in `v1`. The three user IDs in the fixture (`...0001` creates and sends, `...0002` cancels, `...0003` marks paid, downloads and sends reminders) cannot be turned into a name or email through any API call. If your UI wants to show who did what, you need a separate directory.

**Conspicuously absent activity types:** nothing for customer-side view or open, nothing for edits or amendments, nothing for accounting-sync **failure** (even though `accounting_sync_status: "error"` exists, and INV-2026-0045 sits in that state with no failure activity), nothing for refunds or chargebacks, nothing for deletion, and nothing for recurring-schedule generation.

> **Divergence, by omission:** the Invoicing guide never mentions `activities` at all. The entire audit log is documented only as an enum list on the two operation reference pages, with no prose describing what any value means or when it is emitted. Everything in the table above beyond the bare value names is derived from observation.

#### 5.4.7 Accounting sync

| Value | Guide definition | Sandbox count |
| --- | --- | --- |
| `not_pushed` | "eligible to be pushed after being unskipped" | 3 |
| `synced` | "successfully synced to the integration" | 6 |
| `error` | "the most recent sync attempt failed. `accounting_synced_at`, when present, remains the timestamp of the last successful sync." | 1 |
| `skip` | "explicitly excluded from syncing" | 1 |
| `object_changed` | "previously synced, but changed since the last successful sync" | 1 |

Observed behavior of `accounting_synced_at` against each state:

| Invoice | `accounting_sync_status` | `accounting_synced_at` | Note |
| --- | --- | --- | --- |
| INV-2026-0070 | synced | `2026-07-18T09:00:00Z` | equals `updated_at` |
| INV-2026-0066 | synced | `2026-07-24T11:00:00Z` | `updated_at` is later (`16:00:00Z`) |
| INV-2026-0065, 0060, 0052 | not_pushed | `null` | never pushed; no `accounting_synced` activity |
| INV-2026-0050, 0040, 0002, 0001 | synced | set | consistent |
| INV-2026-0045 | **error** | **null** | permitted by "when present", but the only `error` sample gives you no last-success timestamp |
| INV-2026-0043 | object_changed | `2026-05-18T00:07:03Z` | equals both `updated_at` and the `matched` activity time, so the payment match is what invalidated the sync |
| INV-2026-0041 | skip | `null` | the cancelled invoice |

> **Divergence:** the `not_pushed` definition, "eligible to be pushed after being unskipped", describes a transition out of `skip`, not the ordinary never-yet-pushed state, and it implies a skip/unskip control that has no representation in the API. All three sandbox `not_pushed` invoices have `accounting_synced_at: null` and no `accounting_synced` activity, that is, they have simply never been pushed. Read `not_pushed` as "not currently synced", nothing more.

Product context that explains the two separate sync activity types: the help center states invoice syncing is **QuickBooks Online only**, requires the "Sync invoices and customers to QuickBooks" toggle plus a configured Default Accounts Receivable Ledger, back-fills existing invoices on enablement, and that "you'll have to manually sync the invoice payment or include invoice transactions in your automated syncs". That is why `accounting_synced` and `payment_accounting_synced` are distinct, and why only 1 of the 6 synced invoices has the payment leg synced.

**Conspicuously absent:** no field naming the integration, no external or QuickBooks object ID, no error message or code for the `error` state, no `accounting_sync_attempted_at`, and no sync state on the customer object even though the product syncs customers too.

#### 5.4.8 `GET /invoicing/invoices/{invoice_id}`

Path parameter `invoice_id`, string, required. Response is the bare `Invoice`, field-for-field identical to a list element.

```bash
curl -s "$RHO/invoicing/invoices/70000000-0000-4000-8000-000000000001" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

| Request | HTTP | Body |
| --- | --- | --- |
| unknown but well-formed UUID | 404 | `{"type":"1303","title":"invoice not found","status":404}` |
| malformed ID (`xyz`) | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: invoice_id"}` |
| a customer UUID at this path | 404 | `{"type":"1303","title":"invoice not found","status":404}` |

There is no payload advantage over the list form. Use this endpoint for refresh-by-ID, not for enrichment.

---

### 5.5 Invoicing: customers

#### 5.5.1 The customer object

Identical in list and get. Observed via `GET /invoicing/customers/60000000-0000-4000-8000-000000000008`, which is the soft-deleted fixture record:

```json
{
  "id": "60000000-0000-4000-8000-000000000008",
  "legal_name": "Deleted Co",
  "email": "gone@deletedco.example",
  "address": {
    "address1": "9 Archive Rd",
    "address2": "",
    "city": "Chicago",
    "state": "IL",
    "zip_code": "60601",
    "country": "USA"
  },
  "note": "Soft-deleted fixture customer",
  "cc_emails": [],
  "total_revenue": { "amount": 5000, "currency": "USD" },
  "last_invoice_id": "70000000-0000-4000-8000-000000000012",
  "created_at": "2026-01-10T09:00:00Z",
  "updated_at": "2026-05-01T12:00:00Z",
  "deleted_at": "2026-05-01T12:00:00Z"
}
```

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `id` | string (UUID) | yes | Stable global customer identifier. |
| `legal_name` | string | yes | No description in the reference. Always populated in sandbox. |
| `email` | string | yes | **Null on 1 of 8** ("Cedar & Co"). |
| `address` | object | yes | Always present, always fully keyed. |
| `address.address1` | string | yes | |
| `address.address2` | string | yes | **Empty string, never null**, when absent. Populated on 2 of 8. |
| `address.city` | string | yes | |
| `address.state` | string | yes | Observed: 2-letter US state codes. |
| `address.zip_code` | string | yes | Observed: 5-digit US ZIPs, leading zero preserved as a string (`"02109"`). |
| `address.country` | string | yes | Observed: all `"USA"`, that is **ISO 3166 alpha-3**, not the alpha-2 used elsewhere in fintech APIs. No standard is stated and no validation is documented. |
| `note` | string | yes | **Null on 4 of 8.** Not covered by `search`. |
| `cc_emails` | array of string | yes | Empty array when none (3 of 8), never null. |
| `total_revenue` | Money | yes | "Total amount collected across paid invoices". See 5.5.4. |
| `last_invoice_id` | string (UUID) | yes | "Identifier of the most recent invoice for this customer". **Null on 1 of 8** (a customer with no invoices). |
| `created_at` | string (date-time) | yes | The default sort key. |
| `updated_at` | string (date-time) | yes | Touched by invoice events, see 5.5.4. |
| `deleted_at` | string (date-time) | yes | "Set when the customer is deleted; null otherwise". Null on 7 of 8. |

No phone, no tax ID, no default payment terms, no default currency, no customer-level accounting sync status and no invoice count.

#### 5.5.2 `GET /invoicing/customers`

"Deleted customers are excluded unless `include_deleted` is true."

| Parameter | Type | Documented | Observed |
| --- | --- | --- | --- |
| `search` | string | "Case-insensitive substring match on `legal_name` and `email`" | Confirmed on both fields and case-insensitive: `search=acme` matches "Acme Supplies", `search=ORBITMEDIA.CO` matches the email `accounts@orbitmedia.co`. `search=Preferred`, a substring of a `note`, returns 0, confirming `note` is not searched. |
| `include_deleted` | boolean | "When true, include deleted customers in the results" | Confirmed: 7 customers by default, 8 with `include_deleted=true`. |
| `sort_by` | string | "Sort field. Defaults to `created_at` when omitted." | **`created_at` is the only accepted value.** `legal_name`, `email`, `updated_at`, `total_revenue`, `id` and `bogus` all return `400 {"type":"1317","title":"invalid sort_by parameter: \"<value>\"","status":400}`. The parameter exists but can only be set to its own default. |
| `order` | string | "Sort direction. Defaults to `desc` when omitted." | Only lowercase `asc` and `desc` accepted. `ASC`, `ascending` and `bogus` return `400 {"type":"1317","title":"invalid order parameter: \"<value>\"","status":400}`. Note that `/statements` accepts `ASC` happily. |
| `page_size` | integer | "Defaults to 20." Max not documented. | Default 20 confirmed. Bounds 1 to 100 enforced. |
| `page_token` | string | Cursor. | See "Pagination". |

Observed validation matrix, reproducible:

```bash
for v in created_at legal_name bogus; do
  printf '%s -> ' "$v"
  curl -s -o /dev/null -w '%{http_code}\n' \
    "$RHO/invoicing/customers?sort_by=$v&page_size=1" \
    -H "Authorization: Bearer $RHO_API_TOKEN"
done
# created_at -> 200
# legal_name -> 400
# bogus      -> 400

for v in asc desc ASC bogus; do
  printf '%s -> ' "$v"
  curl -s -o /dev/null -w '%{http_code}\n' \
    "$RHO/invoicing/customers?order=$v&page_size=1" \
    -H "Authorization: Bearer $RHO_API_TOKEN"
done
# asc -> 200, desc -> 200, ASC -> 400, bogus -> 400
```

#### 5.5.3 Soft-delete semantics, complete

| Aspect | Behavior | Source |
| --- | --- | --- |
| Marker | `deleted_at` timestamp on the customer, null when live | both reference pages |
| List default | deleted customers **excluded** | reference; observed 7 versus 8 |
| List opt-in | `include_deleted=true` | reference; observed |
| Get by ID | **always returns** the deleted customer "while the record exists". No flag needed, no 410, no special status | reference; observed |
| `search` plus `include_deleted` | **They compose.** Observed: `search=deleted` alone returns 0 rows; `search=deleted&include_deleted=true` returns 1, "Deleted Co". The deleted row is filtered out before or alongside the search, not instead of it. This was previously unstated in the docs and unverified | observed 2026-09-12 |
| Sort position of deleted rows | not special-cased; the deleted customer appears in its natural `created_at desc` position, oldest in the fixture | observed |
| Data retained after delete | everything: `legal_name`, `email`, `address`, `note`, `cc_emails`, `total_revenue`, `last_invoice_id` | observed |
| `updated_at` on delete | set equal to `deleted_at`, `2026-05-01T12:00:00Z` | observed |
| Effect on that customer's invoices | **none.** INV-2026-0001 is returned by the default invoice list, still `status: "paid"`, still `accounting_sync_status: "synced"`, and its `customer.id` still points at the deleted record | observed |
| Invoice soft-delete | **does not exist.** Invoices have no `deleted_at`, and `/invoicing/invoices` has no `include_deleted`; passing it is ignored | reference and observed |
| Restore or un-delete | **unstated** anywhere |
| Hard delete and retention | **unstated.** The phrase "while the record exists" implies an eventual purge with no retention period given |

Reproduce the whole model in three calls:

```bash
curl -s "$RHO/invoicing/customers?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["customers"]))'
# 7

curl -s "$RHO/invoicing/customers?page_size=100&include_deleted=true" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["customers"]))'
# 8

curl -s "$RHO/invoicing/customers/60000000-0000-4000-8000-000000000008" -H "Authorization: Bearer $RHO_API_TOKEN" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["legal_name"], d["deleted_at"])'
# Deleted Co 2026-05-01T12:00:00Z
```

The practical consequence: an integration that walks `/invoicing/invoices` and joins `customer.id` against a cached list from `/invoicing/customers` will get cache misses, because live invoices can reference deleted customers. The correct pattern is `include_deleted=true` on the list, or a per-ID fetch on miss.

#### 5.5.4 `total_revenue` and `last_invoice_id`, derived

Both fields are documented in one line each and both mean something more specific than the line says. Verified exactly against all 8 sandbox customers.

**`total_revenue.amount` equals the sum of `total.amount` over that customer's invoices whose `status == "paid"`**, and nothing else:

| Customer | `total_revenue` | Sum of `paid` invoice totals | Excluded |
| --- | --- | --- | --- |
| Harbor Logistics LLC | 156750 | 156750 | none |
| Acme Supplies | 108403 | 108403 | INV-2026-0066 `pending_payout` 158000 |
| Brightleaf Design | 43400 | 43400 | INV-2026-0060 `overdue` 45000 |
| Deleted Co | 5000 | 5000 | none |
| Summit Analytics | 0 | 0 | INV-2026-0070 `pending_payout` 98000, INV-2026-0041 `cancelled` 22000 |
| Northwind Traders | 0 | 0 | INV-2026-0065 `unpaid`, INV-2026-0045 `overdue`, INV-2026-0043 `confirm_payment` 10000000 |
| Orbit Media Group | 0 | 0 | INV-2026-0052 `unpaid` 45000 |
| Cedar & Co | 0 | 0 | no invoices |

Therefore **`pending_payout` and `confirm_payment` do not count as collected**, despite the money having been captured or having arrived. The doc string "Total amount collected across paid invoices" is accurate only if you read "paid" as the literal status value, not as English. It is also gross of the 2.9 percent plus $0.30 card fee, so it is not cash received. Do not use it in a cash-basis report. Note also that `Money` carries a single `currency`, so the field cannot represent a mixed-currency customer at all, and nothing documents what happens if one exists.

**`last_invoice_id` points to the customer's invoice with the latest `created_at`**, not the latest `date`, not the latest unpaid one, and it is unaffected by status. Verified on all 8: Summit Analytics points at INV-2026-0070 rather than its cancelled INV-2026-0041; Cedar & Co, with no invoices, is `null`.

One consequence worth knowing before you build change detection: **the customer's `updated_at` tracks invoice activity**. Acme's `updated_at` (`2026-07-24T16:00:00Z`) equals INV-2026-0066's `updated_at`; Summit's equals INV-2026-0070's; Northwind's equals INV-2026-0065's `created_at`. So `updated_at` on a customer is not a reliable "customer details changed" signal.

#### 5.5.5 `GET /invoicing/customers/{customer_id}`

"Returns a single customer from Invoicing by ID, including deleted customers when they still exist (`deleted_at` is set)."

| Request | HTTP | Body |
| --- | --- | --- |
| unknown but well-formed UUID | 404 | `{"type":"1303","title":"customer not found","status":404}` |
| malformed ID (`abc`) | 400 | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: customer_id"}` |
| an invoice UUID at this path | 404 | `{"type":"1303","title":"customer not found","status":404}` |

---

### 5.6 The file endpoints and signed-URL mechanics

Three resources in `v1` carry files, and they deliver the URL three different ways.

| Resource | How the URL arrives | TTL documented | TTL observed | Sandbox bucket | Works in sandbox |
| --- | --- | --- | --- | --- | --- |
| Statements | **embedded** as `pdf_url` in both list and get | "valid for up to 15 minutes" | `X-Goog-Expires=899` | `sandbox-statements.files.rho.co` | yes |
| Transaction attachments | exchange at `GET /transactions/{transaction_id}/files/{file_id}` | "short-lived" | `X-Goog-Expires=899` | `rho-api-sandbox.files.rho.co` | yes |
| Invoice PDF | exchange at `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | "short-lived", no number given | **not observable** | unknown | **no, 404 on every `file_id`** (see 5.2) |

The two exchange endpoints return a byte-identical three-field schema:

| Field | Type | Marked required | Notes |
| --- | --- | --- | --- |
| `file_id` | string | yes | Echoes the requested ID. |
| `file_name` | string | yes | "Original file name". Observed on transactions: `parking-receipt.pdf`, `repayment-details.csv`. Never appears at the invoice or transaction object level, only here. |
| `download_url` | string | yes | "Fresh, short-lived signed download URL". |

> **Divergence:** only statements commit to a number. The invoicing reference says "Fetch again whenever a new signed URL is needed; do not persist the URL" and gives no TTL at all. By analogy with the two observable buckets, 899 seconds is the likely value, but Rho does not commit to it for invoicing and it could not be measured because the endpoint returns 404.

#### 5.6.1 Anatomy of a signed URL

Both working buckets emit Google Cloud Storage **V4 signed URLs**, RSA-signed by the same service account.

| Component | Value |
| --- | --- |
| Host, transaction attachments | `rho-api-sandbox.files.rho.co` |
| Host, statement PDFs | `sandbox-statements.files.rho.co` |
| Path | `/{24 hex chars}.{ext}`, for example `/f0b72b6108f6ebfd9818fb0f.pdf`, `/4f7150d8341cae23c6ffa33a.pdf` |
| `X-Goog-Algorithm` | `GOOG4-RSA-SHA256` |
| `X-Goog-Credential` | `file-service@pledge-218909.iam.gserviceaccount.com/<YYYYMMDD>/auto/storage/goog4_request` |
| `X-Goog-Date` | signing instant, second granularity, for example `20260912T002403Z` |
| `X-Goog-Expires` | **`899`** on every URL observed, in both buckets |
| `X-Goog-Signature` | 512 hex characters (2048-bit RSA) |
| `X-Goog-SignedHeaders` | `host` |

Two facts an integrator can use directly:

- **The exact deadline is readable from the URL with no network call**: `X-Goog-Date + X-Goog-Expires`. Parse it and decide whether a URL is worth attempting, instead of discovering expiry from a failed download.
- **Object names carry no account, business, invoice or transaction identifier** and are not enumerable. They are also deduplicated: the same `file_id` attached to two different transactions resolves to the same object path.

#### 5.6.2 Failure modes, observed

Every row below was reproduced live on 2026-09-12 against a transaction attachment URL.

| Test | Result |
| --- | --- |
| GET the URL as issued, no `Authorization` header | `200`, `content-type: application/pdf`, 769 bytes, body begins `%PDF-1.4` |
| `HEAD` the URL | `200` |
| `Range: bytes=0-9` | `206`, 10 bytes returned |
| Same URL fetched 3 times | `200` each time. **Not single-use** |
| Last hex character of `X-Goog-Signature` altered | `403`, XML `<Code>SignatureDoesNotMatch</Code>` |
| Last character of the whole query string altered (corrupts `X-Goog-SignedHeaders=host`) | `400`, XML `<Code>MalformedSecurityHeader</Code>`, detail "Host header not signed" |
| Query string stripped, bare object path | `403`, XML `<Code>AccessDenied</Code>`. The bucket is private, there is no public read |
| `X-Goog-Expires` rewritten from `899` to `1` | `400`, XML `<Code>ExpiredToken</Code>`, detail "Request signature expired at: 2026-09-12T00:28:09+00:00", exactly `X-Goog-Date` plus 1 second |
| A URL replayed 27 minutes after signing | `400 ExpiredToken`, "Request signature expired at: 2026-09-11T23:37:21+00:00", exactly signing time plus 899 s |

**Every one of these failures is a Google Cloud Storage XML error document, not RFC 9457 problem+json.** A client that parses every non-2xx body as JSON will throw on all of them. Handle the download leg with a completely separate error path from the API leg.

> **Divergence, minor:** the Transactions guide instructs you to follow the link "straight away, **without an Authorization header**". Observed: sending `Authorization: Bearer sandbox` or `Authorization: Bearer NOPE` alongside the signed URL still returns `200` with the full 769-byte body. GCS ignores the header here because only `host` is in `X-Goog-SignedHeaders`. Follow the doc's advice anyway, since the behavior is not contractual, but a stray header in a shared HTTP client is not the cause of a download failure you are debugging.

Confirming the documented sandbox promise, a transaction CSV attachment downloads as real content:

```csv
transaction_id,account_name,counterparty_name,amount,currency
019f0143-3ea0-7000-8000-000000000003,Credit Account,Cash (Checking),1750,USD
```

That matches the Transactions guide: "Sandbox downloads contain non-empty representative fictional documents, but their contents are not guaranteed to reproduce every field of the transaction fixture." No such statement exists for invoicing.

#### 5.6.3 Expiry, and the statement signing cache

The documented TTL is "valid for up to 15 minutes". The observed `X-Goog-Expires` is 899 seconds, one second short of 15 minutes, which is consistent with a signer computing an absolute deadline and converting back to a relative TTL.

The interesting behavior is that **the two working file surfaces behave differently on refresh**.

A 20-second poll of `GET /statements/200527` and `GET /transactions/.../files/...` in lockstep, run 2026-09-12 00:28Z to 00:37Z, recording the `X-Goog-Date` returned by each. Reproduce it with:

```bash
for i in $(seq 1 28); do
  printf '%s ' "$(date -u +%H:%M:%SZ)"
  printf 'stmt=%s ' "$(curl -s "$RHO/statements/200527" -H "Authorization: Bearer $RHO_API_TOKEN" \
    | python3 -c 'import sys,json,urllib.parse as u; d=json.load(sys.stdin); print(u.parse_qs(u.urlparse(d["pdf_url"]).query)["X-Goog-Date"][0])')"
  printf 'txn=%s\n' "$(curl -s "$RHO/transactions/019f0554-0bf0-7000-8000-00000000000a/files/2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15" \
    -H "Authorization: Bearer $RHO_API_TOKEN" \
    | python3 -c 'import sys,json,urllib.parse as u; d=json.load(sys.stdin); print(u.parse_qs(u.urlparse(d["download_url"]).query)["X-Goog-Date"][0])')"
  sleep 20
done
```

Abridged output, with the two re-sign boundaries marked:

```text
00:28:45Z  stmt=00:24:03Z  txn=00:28:46Z
00:29:06Z  stmt=00:29:06Z  txn=00:29:07Z   <- statement re-signed, 303 s after the prior epoch
00:29:27Z  stmt=00:29:06Z  txn=00:29:28Z
00:30:09Z  stmt=00:29:06Z  txn=00:30:10Z
00:31:11Z  stmt=00:29:06Z  txn=00:31:11Z
00:32:33Z  stmt=00:29:06Z  txn=00:32:34Z
00:33:55Z  stmt=00:29:06Z  txn=00:33:56Z
00:34:16Z  stmt=00:34:16Z  txn=00:34:16Z   <- statement re-signed, 310 s after the prior epoch
00:35:17Z  stmt=00:34:16Z  txn=00:35:18Z
00:37:20Z  stmt=00:34:16Z  txn=00:37:20Z
```

Reading:

- **Transaction attachment URLs are minted fresh on every request.** New `X-Goog-Date`, new signature, a full 899-second window every time. The docs are accurate here.
- **Statement `pdf_url` is served from a server-side signing cache of roughly 300 seconds.** Two back-to-back calls to `GET /statements/200527` return a byte-identical URL. Four re-sign intervals have now been measured across two independent polling runs: 302 s, 313 s, 303 s and 310 s. The cache TTL is not the 899-second expiry.
- Crucially, **each URL is replaced roughly 10 minutes before it expires**, not when it dies. Epoch `00:29:06Z` was valid until `00:44:05Z` and was replaced at `00:34:16Z`, almost 10 minutes early.
- Because the cache rotates about 300 seconds into an 899-second lifetime, **a statement URL you receive always has between roughly 599 and 899 seconds of life left**. Observed minimum residual: 606 s in the earlier run, 610 s in the run above. A statement URL never arrives nearly dead, so the documented "up to 15 minutes" is accurate and conservative.

> **Divergence:** the documented remedy for a lapsed statement link, "If the link lapses, re-fetch the statement with `GET /statements/{id}` for a fresh URL", does not work by the mechanism it describes. Re-fetching does not mint a URL on demand; it returns whatever the ~300-second cache holds. A client **cannot force a re-sign**. In practice the remedy usually works, because the cache rotates about 10 minutes before expiry, so a genuinely expired URL will already have been replaced. But a tight retry loop after a `400 ExpiredToken` will keep receiving the same dead URL until the cache turns over. Back off past the cache TTL instead of retrying immediately.

**The cache key is the PDF blob, not the statement.** Observed on a single `GET /statements?page_size=100`: 33 statements resolved to only **3 distinct object paths**, one shared by the 7 treasury statements, one by the 22 credit statements, one by the 4 account statements.

```bash
curl -s "$RHO/statements?page_size=100" -H "Authorization: Bearer $RHO_API_TOKEN" \
| python3 -c '
import sys, json, urllib.parse as u
from collections import Counter, defaultdict
st = json.load(sys.stdin)["statements"]
paths, dates = Counter(), defaultdict(set)
for s in st:
    p = u.urlparse(s["pdf_url"]); q = u.parse_qs(p.query)
    paths[p.path] += 1
    dates[p.path].add(q["X-Goog-Date"][0])
for path, n in paths.items():
    print(path, n, sorted(dates[path]))
'
# /41addf56a3d9ab46a2bfedc6.pdf 7  ['20260912T003658Z']
# /e9c29858933afd7a8d42e1a7.pdf 22 ['20260912T003416Z']
# /4f7150d8341cae23c6ffa33a.pdf 4  ['20260912T003658Z']
```

Two consequences. First, because signing is per blob and each blob has its own cache epoch, **a single list response can return URLs signed at different instants with different residual lifetimes**. In the run above, one page of 33 statements carried URLs signed 162 seconds apart, so the credit statements' links had 162 fewer seconds of life than the others. All were still inside the 599 to 899 second band, but do not assume a uniform deadline across one page. Second, the sandbox backs all 33 statements with only 3 real PDFs, so per-statement PDF content is not statement-specific fixture data. Testing "does this PDF match this statement" against sandbox is not meaningful.

#### 5.6.4 Budgeting an archive job

The Statements guide's archiving workflow is:

```bash
curl -s "$RHO/statements?period_end_after=2026-05-01&period_end_before=2026-06-01&page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

followed by "download each `pdf_url` promptly" and "For a long-running archive job, download each PDF soon after you read it rather than collecting URLs up front."

The arithmetic behind that advice is never given, so here it is. A 100-item page issues up to 100 signatures that share a single window of at most 899 seconds, and in the worst case as little as ~599 seconds because of the signing cache. At one PDF every 10 seconds a full page takes 1,000 seconds and you will lose the tail. There is no bulk refresh endpoint and no per-statement file endpoint; the only recovery is a full single-statement re-fetch, which is subject to the cache described above and costs one of your ~60 requests per minute.

Practical shape for a correct archiver:

1. Page with `period_end_after` and `period_end_before` windows rather than cursor-walking the live head. The cursor is offset-based (see "Pagination"), so a statement finalized mid-iteration shifts every subsequent page.
2. Parse `X-Goog-Date` plus `X-Goog-Expires` out of each `pdf_url` on arrival and record the absolute deadline.
3. Download concurrently, but pace below the documented one request per second guidance for the API leg. The GCS download leg does not count against the Rho API rate limit, since it is a different host with no Rho authentication.
4. On a deadline you have already passed, re-fetch `GET /statements/{id}`, and if the URL comes back identical, wait out the remainder of the ~300 second cache before trying again.
5. Do not persist signed URLs anywhere. All three reference pages say so, in three different wordings.

---

### 5.7 Errors specific to these seven operations

The declared error sets in the official reference are:

| Operation | Declared responses |
| --- | --- |
| `GET /statements` | 400, 401, 403, 500, 503 |
| `GET /statements/{id}` | 400, 401, 403, 404, 500, 503 |
| `GET /invoicing/invoices` | 400, 401, 403, 500, 503 |
| `GET /invoicing/invoices/{invoice_id}` | 400, 401, 403, 404, 500, 503 |
| `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | 400, 401, 403, 404, 500, 503 |
| `GET /invoicing/customers` | 400, 401, 403, 500, 503 |
| `GET /invoicing/customers/{customer_id}` | 400, 401, 403, 404, 500, 503 |

> **Divergence:** none of the seven declares `429`, even though the Rate limits page states that limits apply "uniformly across all public Rho API endpoints" and that exceeding them returns `429 Too Many Requests` with a `Retry-After` header. Generated clients built strictly from these operation schemas will have no 429 branch.

What these endpoints actually return, all reproduced live:

| HTTP | `type` | `title` | `detail` | Trigger |
| --- | --- | --- | --- | --- |
| 401 | `"2"` | `Unauthenticated` | absent | missing `Authorization` header. Note: sandbox accepts any non-empty bearer value |
| 404 | `"1303"` | `statement not found` | absent | unknown, malformed or negative statement ID |
| 404 | `"1303"` | `invoice not found` | absent | unknown well-formed invoice UUID |
| 404 | `"1303"` | `customer not found` | absent | unknown well-formed customer UUID |
| 404 | `"1303"` | `invoice file not found` | absent | **every** invoice file fetch, including documented-correct pairings (5.2) |
| 400 | `"1317"` | `page_size must be between 1 and 100` | absent | `page_size=0` or `page_size=101` on all three list endpoints |
| 400 | `"1317"` | `page_token must be a valid cursor` | absent | garbage token, changed filters, cross-endpoint token |
| 400 | `"1317"` | `invalid sort_by parameter: "<v>"` | absent | `/invoicing/customers?sort_by=` anything but `created_at` |
| 400 | `"1317"` | `invalid order parameter: "<v>"` | absent | `/invoicing/customers?order=` anything but `asc` or `desc` |
| 400 | `"about:blank"` | `Bad Request` | `invalid parameter: <name>` | malformed path IDs (`invoice_id`, `customer_id`, `file_id`) and malformed query values (`account_id`, `period_end_after`, `date_after`) |

> **Divergence:** the schema describes `type` as "A URI reference that identifies the problem type. Example: `about:blank`". In practice these endpoints return bare numeric strings `"2"`, `"1303"` and `"1317"` for most failures. `"1303"` is shared by every not-found across the whole API, with the resource identified only by the prose `title`, so `type` is useless for programmatic discrimination. Key off HTTP status plus, reluctantly, `title`. The schema also lists `detail` on the 404 responses; **no 404 observed anywhere returns a `detail`**. Only the `about:blank` validation family carries one.

Two distinct error layers are in play: a Rho application layer that emits numeric `type` codes with no `detail`, and a request-validation layer that emits `about:blank` plus a `detail`. The documentation describes only the second.

Non-JSON error surfaces you will also hit on these paths:

| Surface | Example | Body |
| --- | --- | --- |
| Go router, route not matched | `GET /statements/200527/files/x`, `GET /invoicing/invoices/` | `404 page not found`, plain text |
| Load balancer, outside `/api/v1` | `GET /api/v2/statements` | `default backend - 404`, plain text |
| Write verb on any path here | `POST /invoicing/invoices/{id}` | `405`, **empty body**, `Allow: GET` |

Also worth knowing on these endpoints: paths are case-sensitive, a trailing slash is a 404 with no redirect, unknown query parameters are silently ignored, `Accept` is not negotiated (XML requests get JSON), and no response carries `ETag`, `Last-Modified`, `Cache-Control`, `X-Request-Id` or any `X-RateLimit-*` header, so there are no conditional requests and no visible rate-limit headroom.

Finally, the cursor. The cursor internals belong to "Pagination", but two behaviors bite specifically here:

- **The filter fingerprint is enforced, and `sort_by` is part of it on `/statements` even though `sort_by` has no effect on results.** Changing an inert parameter mid-iteration invalidates your cursor with `400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`.
- **`page_size` is not part of the fingerprint.** Observed: a token issued by `GET /statements?page_size=5` used against `GET /statements?page_size=10&page_token=...` returns `200` with 10 rows starting at offset 5. Changing page size mid-iteration is silently allowed, and since the cursor is offset-based, it is a route to skipped or duplicated rows.

---

### 5.8 Checklist for an integrator

Statements:

1. Detect credit statements with `statement_type == "credit"` or `accounts[].account_type == "credit"`, never with `account_id is None`.
2. Do not expect `repayment_date`. It is documented and never returned, and it is the only credit-terms field in the API.
3. Do not join `accounts[].account_type` to the Accounts API's `account_type`. The vocabularies differ and disagree on the same account. Join on `account_id`.
4. Treat credit `total_credits`, `total_debits` and `total_fees` as unusable; anchor on `closing_balance` and the `spending` / `repayments` / `cashback` trio, and do not assume their signs.
5. There is no `available_at` filter, so incremental "finalized since T" polling is impossible. Rescan by period window and diff IDs.
6. Statement IDs are opaque numeric strings, not UUIDs. Junk IDs return 404, not 400.

Invoicing:

7. The invoice file endpoint returns 404 on every advertised `file_id` in sandbox. Prototype the signed-URL flow against the transactions file endpoint, and verify invoice PDFs in production before shipping.
8. Reimplement the total formula in 5.4.3 if you need a subtotal or tax amount. The API exposes neither.
9. `status` has no `draft` and no `sent`. To learn whether an invoice was emailed, scan `activities` for `sent`. `status=draft` and `status=sent` return `200` with zero rows rather than an error.
10. Do not derive `overdue` from `status`; compute it from `due_date` yourself. Observed invoices sit at `unpaid` weeks past due.
11. A Rho card payment appears as `payments[].type == "external"` with `external_method == "credit_card"` and a null `transaction_id`. Detect the card rail via the `card_payment_received` activity or `status == "pending_payout"`.
12. There is no per-payment amount, so partial payments cannot be represented. If your AR flow needs them, this API cannot reconcile it.
13. There is no `customer_id` filter on invoices. Per-customer views require pulling everything and grouping client-side.
14. Fetch customers with `include_deleted=true` when building the invoice-to-customer join, or live invoices will miss their customer.
15. `total_revenue` counts only `status == "paid"` and is gross of the 2.9 percent plus $0.30 card fee. It is not cash received.
16. A customer's `updated_at` moves when its invoices move, so it is not a "customer details changed" signal.

Everything in this section:

17. Generate all response models with every field nullable. `required` in these schemas is a presence guarantee, not a non-null guarantee: `invoice.note`, `invoice.accounting_synced_at`, `payments[].external_method`, `payments[].transaction_id`, `activities[].user_id`, `customer.email`, `customer.note`, `customer.last_invoice_id`, `customer.deleted_at` and `page.next_page_token` are all marked required and all observed null.
18. Handle both absence conventions. Optional fields are **omitted keys** (`invoice.file_id`, the credit-only statement figures); "required but empty" fields are **explicit nulls**.
19. Never loop single GETs to enrich list rows. All 133 sandbox resources are deep-equal between list and single GET, and the only thing `GET /statements/{id}` adds is a possibly re-signed URL.
20. Give every `switch` on these enums a default case. The Versioning policy classifies "a new enum value" as a non-breaking change that can ship into `v1` at any time.
21. Parse `X-Goog-Date` plus `X-Goog-Expires` out of every signed URL to know its exact deadline, and never persist the URL.
22. Use a separate error path for the download leg. Signed-URL failures are GCS XML, API failures are problem+json, route failures are plain text, and 405 has an empty body.

### 5.9 Enum inventory for this section

| Enum | Values |
| --- | --- |
| `statement.statement_type` | `account`, `credit`, `treasury` |
| `statement.accounts[].account_type` | `checking`, `savings`, `credit`, `treasury` |
| `invoice.status` | `paid`, `unpaid`, `cancelled`, `overdue`, `confirm_payment`, `pending_payout` |
| `invoice.payments[].type` | `received_in_account`, `external` |
| `invoice.payments[].external_method` | `cash`, `check`, `credit_card`, `other` |
| `invoice.activities[].activity_type` | `created`, `sent`, `downloaded`, `matched`, `marked_as_paid`, `marked_as_unpaid`, `cancelled`, `reminder_sent`, `card_payment_received`, `accounting_synced`, `payment_accounting_synced` |
| `invoice.accounting_sync_status` | `not_pushed`, `synced`, `error`, `skip`, `object_changed` |
| `customers.sort_by` | `created_at` only. Enforced with a 400, not documented as a restriction |
| `customers.order` | `asc`, `desc`, lowercase only. Enforced with a 400 |
| `statements.order` | not validated. Anything lowercasing to `asc` is ascending, everything else is descending |
| `statements.sort_by` | not validated and inert, but hashed into the pagination cursor |
## 6. Cross-cutting mechanics

Four mechanisms apply to every call you will ever make against Rho v1: how lists are paged, how the service throttles you, how it reports failure, and what it promises not to change. None of them is endpoint-specific, all of them are load-bearing, and each of them diverges from the published documentation in at least one way that will cost you a production incident if you take the docs at face value.

Everything marked **observed** in this section was captured against the sandbox host `https://rhoapi-sandbox.rho.co/api/v1` with the bearer token `sandbox` on 2026-09-11 and 2026-09-12 UTC. The sandbox accepts any non-empty bearer token (see the Authentication section), so every probe below is reproducible by anyone. Production was not probed beyond unauthenticated metadata. Where a behavior is documented but was not reachable in the sandbox, it is labelled as unverified rather than confirmed.

---

### 6.1 Pagination

Every list endpoint (`/accounts`, `/cards`, `/transactions`, `/statements`, `/invoicing/customers`, `/invoicing/invoices`) uses the same two query parameters and the same response wrapper. The detail endpoints take neither.

#### 6.1.1 The wrapper

Official docs (`/docs/v1/pagination`) describe a response with the resource array at the top level plus a `page` object. That is exactly what the service returns, and nothing more.

```bash
curl -s "https://rhoapi-sandbox.rho.co/api/v1/transactions?page_size=2" \
  -H "Authorization: Bearer sandbox"
```

```json
{
  "page": { "next_page_token": "eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qSXcifQ" },
  "transactions": [ { "id": "…" }, { "id": "…" } ]
}
```

| Property | Value (observed) |
| --- | --- |
| Top-level keys | The resource array plus `page`, nothing else |
| Resource key | Matches the resource: `accounts`, `cards`, `transactions`, `statements`, `customers`, `invoices` |
| `page` fields | Exactly one: `next_page_token` |
| Absent | `total`, `total_count`, `count`, `has_more`, `has_next`, `prev_page_token`, `offset`, `limit` |
| Last-page signal | `"next_page_token": null`. The key is always present, never omitted, never an empty string |
| Response headers | No `Link`, no `X-Total-Count`, no pagination headers of any kind |

Note the two invoicing resource keys: `/invoicing/customers` returns `customers`, not `invoicing_customers`, and `/invoicing/invoices` returns `invoices`. A generic client that derives the key from the last path segment works; one that derives it from the full path does not.

> **Divergence:** every operation reference page types the field as `page.next_page_token (string, required)` while the prose on the same page says "null on the last page". Observed, the field is `null` on the last page of all six endpoints. A strictly generated client with a non-nullable `string` will fail to deserialize the terminal response of every walk. Type it `string | null`.

#### 6.1.2 `page_size`: default, bounds, and coercion

The pagination guide says "Each endpoint defines its own minimum, maximum, and default". The operation reference pages publish two different halves of that and never all three:

| Endpoint | Reference wording | Documented max | Documented default | Documented min |
| --- | --- | --- | --- | --- |
| `GET /accounts` | "Number of accounts per page; max 100" | 100 | not stated | not stated |
| `GET /transactions` | "Number of transactions per page; max 100" | 100 | not stated | not stated |
| `GET /statements` | "Number of statements per page; max 100" | 100 | not stated | not stated |
| `GET /cards` | "Number of cards to return. Defaults to 20." | not stated | 20 | not stated |
| `GET /invoicing/customers` | "Number of customers per page. Defaults to 20." | not stated | 20 | not stated |
| `GET /invoicing/invoices` | "Number of invoices per page. Defaults to 20." | not stated | 20 | not stated |

Observed, the behavior is uniform across all six endpoints. The bound is inclusive `[1, 100]` everywhere, and the default is 20.

```bash
# default page size, proven on the two endpoints whose corpus exceeds 20 rows
curl -s "https://rhoapi-sandbox.rho.co/api/v1/transactions" -H "Authorization: Bearer sandbox" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["transactions"]))'
# -> 20   (sandbox holds 72 transactions; /statements holds 33 and also returns 20)
```

| `page_size` | HTTP | Result (observed, identical on all six endpoints) |
| --- | --- | --- |
| omitted | 200 | 20 items |
| `0`, `-1`, `-0` | 400 | `type` `1317`, "page_size must be between 1 and 100" |
| `1` | 200 | 1 item, the minimum |
| `100` | 200 | the maximum |
| `101`, `150`, `1000`, `10000`, `99999999999999999999` | 400 | `type` `1317`, same title |
| `%2B3` (a leading `+`) | 200 | parsed as 3 |
| `03` | 200 | parsed as 3 |
| `2.0`, `2.5`, `1e2`, `0x10`, `abc`, `true`, `null` | 400 | `type` `about:blank`, `detail` "invalid parameter: page_size" |
| `` (empty value) | 400 | `type` `about:blank` |
| `page_size=5&page_size=7` (repeated) | 400 | `type` `about:blank`. It does not take first or last |
| `page_size[]=5` | 200 | the bracketed key is unrecognized and silently ignored; falls back to 20 |
| `PAGE_SIZE=5`, `pageSize=5` | 200 | parameter names are case-sensitive; ignored; falls back to 20 |

> **Divergence:** `/cards`, `/invoicing/customers` and `/invoicing/invoices` publish no maximum, but observed all three enforce the same 1..100 bound and say so in the error. Conversely `/accounts`, `/transactions` and `/statements` publish no default, but observed all use 20. No endpoint documents a minimum even though the guide says each one defines it. Treat `[1, 100]` and default 20 as the real contract on all six.

> **Divergence:** the docs say only that "values outside the allowed range return `400 Bad Request`". There are actually two distinct 400 bodies with different `type` values and different fields, split on whether the value parses as an integer at all. `?page_size=101` gives `{"type":"1317","title":"page_size must be between 1 and 100","status":400}`; `?page_size=abc` gives `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}`. See 6.3.

#### 6.1.3 What the token decodes to

The docs call the cursor opaque and warn that "their format and lifetime are not part of the API contract and may change without notice". Take the warning seriously as an engineering rule and read the rest of this subsection as diagnostics, not as an interface.

Observed, the token is base64url without padding and decodes to a three-field JSON envelope:

```bash
python3 - <<'PY'
import base64, json, urllib.request
req = urllib.request.Request(
    "https://rhoapi-sandbox.rho.co/api/v1/transactions?page_size=36",
    headers={"Authorization": "Bearer sandbox"})
tok = json.load(urllib.request.urlopen(req))["page"]["next_page_token"]

def b64(s: str) -> bytes:
    s = s.replace("-", "+").replace("_", "/")
    return base64.b64decode(s + "=" * (-len(s) % 4))

env = json.loads(b64(tok))
print(env)                 # {'v': 1, 'f': 't0HwRhJ0BSGWYAjAT5bQKg', 't': 'b2Zmc2V0OjM2'}
print(b64(env["t"]))       # b'offset:36'
PY
```

| Field | Meaning (inferred from observed behavior) |
| --- | --- |
| `v` | Envelope version, always `1`. A token rewritten with `"v":2` returns 400. |
| `f` | Query fingerprint. 22 base64url characters, so 16 raw bytes, consistent with a 128-bit digest. It binds the token to the endpoint plus the canonicalized filter and sort set. It is deterministic and stable across process and connection boundaries, and it does not include `page_size`. |
| `t` | The cursor itself, separately base64-encoded. Its decoded form differs by endpoint (6.1.4). |

The decoder is lenient about the base64 alphabet and padding (standard alphabet with `=` padding is accepted) and strict about the envelope: `v` must be 1, `f` must match the fingerprint the server recomputes for the current request, and `t` must itself be base64 of a well-formed cursor. Unknown extra keys in the envelope are ignored and the token still works.

#### 6.1.4 Two implementations behind one envelope

This is the single most important fact in this subsection. The same wrapper hides two different pagination algorithms.

| Endpoint | Decoded `t` | Style |
| --- | --- | --- |
| `/accounts` | `{"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}` | keyset |
| `/cards` | `offset:N` | absolute offset |
| `/transactions` | `offset:N` | absolute offset |
| `/statements` | `offset:N` | absolute offset |
| `/invoicing/customers` | `offset:N` | absolute offset |
| `/invoicing/invoices` | `offset:N` | absolute offset |

Observed on `/accounts`:

```bash
curl -s "https://rhoapi-sandbox.rho.co/api/v1/accounts?page_size=3" \
  -H "Authorization: Bearer sandbox" \
  | python3 -c 'import sys,json,base64
d=json.load(sys.stdin)
b=lambda s:base64.b64decode(s.replace("-","+").replace("_","/")+"="*(-len(s)%4))
env=json.loads(b(d["page"]["next_page_token"])); print(b(env["t"]).decode())'
# -> {"last_id":"30000000-0000-4000-8000-000000000007","sort_by":"account_name","order":"asc"}
```

`N` in the offset form is the absolute count of rows already consumed: request `page_size=1` and the token carries `offset:1`, request `page_size=50` and it carries `offset:50`, with the same `f` in both cases.

#### 6.1.5 What invalidates a cursor and what does not

The gate is purely the fingerprint `f`. The server recomputes it from the current request's endpoint, filters and sort, and compares. A mismatch is `400 {"type":"1317","title":"page_token must be a valid cursor","status":400}`.

| Change between page N and page N+1 | Cursor still valid? (observed) |
| --- | --- |
| Change `page_size` (5 then 3, 1 then 100) | **Yes.** `page_size` is not in the fingerprint |
| Add an unknown parameter (`&zzz=1`) | Yes, unknown parameters are ignored and not fingerprinted |
| Add the explicit default (`sort_by=initiated_at&order=desc` on `/transactions`) | Yes, defaults are canonicalized before hashing |
| `initiated_after=2026-01-01` then `initiated_after=2026-01-01T00:00:00Z` | Yes, dates are normalized before hashing |
| Add `include_deleted=false` on `/invoicing/customers` | Yes, canonicalized to the default |
| `order=asc` then `order=ASC` | **No, 400.** Identical rows, incompatible cursors |
| `status=settled` then `status=settled&status=settled` | **No, 400.** Identical rows, incompatible cursors |
| Add, drop or change any filter | No, 400 (as documented) |
| Change `sort_by` or `order` to a different value | No, 400 (as documented) |
| Token from a different endpoint | No, 400 |
| `page_token=` (empty string) | Treated as absent: returns page 1, HTTP 200 |
| `page_token` repeated | 400 `about:blank`, "invalid parameter: page_token" |

Changing `page_size` mid-walk is not merely tolerated, it is correct. Observed: take the `offset:5` token minted by `page_size=5`, continue it with `page_size=3`, and you get exactly reference positions 6, 7 and 8 with no gap and no overlap.

```bash
B=https://rhoapi-sandbox.rho.co/api/v1; H="Authorization: Bearer sandbox"
T=$(curl -s "$B/transactions?page_size=5" -H "$H" \
    | python3 -c 'import sys,json;print(json.load(sys.stdin)["page"]["next_page_token"])')
curl -s "$B/transactions?page_size=3&page_token=$T" -H "$H" \
  | python3 -c 'import sys,json;print([t["id"][-6:] for t in json.load(sys.stdin)["transactions"]])'
# -> ['000005', '00000f', '00000c']   == positions 6,7,8 of the page_size=100 reference order
```

> **Divergence:** the docs list what invalidates a cursor ("same endpoint with the same filters and sort order") but never state the useful converse, that `page_size` may change freely between pages. That is a real capability: you can start a walk with a small page for latency and escalate to 100 once you know the result set is large. Conversely the docs give no warning that the binding is to the *raw spelling* of a filter rather than its meaning. `order=ASC` and `order=asc` return byte-identical rows, and their cursors are mutually invalid.

The practical rule that follows: build the query string once per walk, store it, and replay it byte for byte on every page, varying only `page_token` (and, if you want, `page_size`).

#### 6.1.6 The stability caveat

The pagination guide makes an unqualified promise:

> "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated."

> **Divergence:** this holds structurally only for `/accounts`. Five of six list endpoints use an absolute offset cursor, and an absolute offset cannot deliver that guarantee. If a row is inserted at a position before your current offset while you walk, every later row shifts by one and you skip a record. If a row is deleted before your offset, a record repeats. The sandbox dataset is static, so a live shift cannot be forced there, but the mechanism is dispositive: `offset:N` carries no anchor to any row, so there is nothing for the server to be stable against. `/accounts` is the exception; its `last_id` keyset cursor does provide the promised behavior, and observed it additionally validates that the anchor row still exists (a fabricated `last_id` with a correct fingerprint returns 400).

The engineering consequence is not subtle, because the ordering makes it worse. `/transactions` defaults to `initiated_at` descending, newest first. New transactions arrive at the head of that ordering, which is exactly where an insert does maximum damage to an offset walk: one new transaction between page 1 and page 2 pushes the last row of page 1 into page 2, and you process it twice.

Three mitigations, in order of preference:

1. **De-duplicate on `id` in the client.** Cheap, always correct for duplicates, and the only defense that needs no cooperation from the server. Both loops in 6.1.9 and 6.1.10 do this.
2. **Pin the window with a filter.** For `/transactions`, adding `initiated_before=<the moment you started>` makes the result set closed against new arrivals, because anything inserted after you started falls outside the filter. Note from the Filtering and sorting section that `*_before` is exclusive on `/transactions` and `/statements` but inclusive on `/invoicing/invoices`, and that an empty value on any `*_before` parameter silently returns zero rows.
3. **Accept the skip risk, and re-walk.** If a walk that must be complete cannot be window-pinned, run it twice and union on `id`, or run it against a quiet period.

Skips cannot be detected client-side at all. That asymmetry, duplicates are cheap to fix and skips are invisible, is why a window filter matters for any reconciliation job.

#### 6.1.7 Termination and the last page

Termination is by `null` cursor and nothing else. There is no `has_more`, no count, and no way to know in advance how many pages remain.

Observed, when the row count is an exact multiple of `page_size` there is **no** trailing empty page. The last full page carries the `null` token itself:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1; H="Authorization: Bearer sandbox"   # 72 transactions total
T=$(curl -s "$B/transactions?page_size=36" -H "$H" \
    | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["page"]["next_page_token"])')
curl -s "$B/transactions?page_size=36&page_token=$T" -H "$H" \
  | python3 -c 'import sys,json;d=json.load(sys.stdin);print(len(d["transactions"]), d["page"]["next_page_token"])'
# -> 36 None
```

Page 1 returns 36 rows plus an `offset:36` token; page 2 returns the remaining 36 rows and `null`. Likewise `/invoicing/customers?page_size=7` against a 7-row corpus returns 7 rows and a `null` token on the very first call. An empty page is reachable only by hand-crafting a cursor whose offset equals the total, which the API itself never mints.

Your loop must therefore handle three cases: a full page with a token, a short page with a token (`page_size=100` against 72 rows returns 72 rows and `null`, so a short page normally means the end, but never rely on that), and a page whose token is `null`. Never treat "fewer items than `page_size`" as the terminator. Only `next_page_token === null` terminates.

#### 6.1.8 Cursor lifetime, forging, and what that implies

| Property | Observed |
| --- | --- |
| Lifetime | No expiry observed. Tokens minted at 2026-09-11T19:22Z still resolved at 2026-09-12T00:03Z, about 4h41m later. No TTL is documented and no expiry error exists |
| Signature | None. The envelope is unsigned and unencrypted. `f` is a fingerprint of the query, not an HMAC over the cursor payload |
| Forgeable | Yes. Keeping a legitimate `f` and rewriting the inner offset to any value in `[0, total]` is honored. `offset:70` on the 72-row transactions corpus returns the last 2 rows; `offset:72` returns an empty array with a `null` token; `offset:73` returns 400 |
| Validation | Offset must be a non-negative integer no greater than the total. The `/accounts` keyset additionally requires the anchor row to exist and the inner `sort_by`/`order` to match the request |

Two things follow. First, an undocumented binary search on the `offset:N` 400 boundary will tell you a total result count in a handful of calls. It works, and you should not ship it: it depends on the exact cursor format that the docs explicitly reserve the right to change without notice, and it will break silently the day Rho migrates the remaining five endpoints to keyset cursors. Second, because the cursor is not authenticated, do not treat it as a capability. It is scoped to a query, not to a tenant, and it tells an attacker who already holds it nothing more than the query it came from, but it is also not something to log to a third party or embed in a URL you share.

The docs' own advice, "cursors are designed for live iteration, not for bookmarks", is the right rule even though no expiry was observed. Persist a timestamp filter as your resume point, never a cursor.

#### 6.1.9 A correct iteration loop in Python

The sample in the official pagination guide is close but omits three things: it never de-duplicates, it calls `raise_for_status()` with no `429` handling (which directly contradicts Rho's own rate-limits page), and it re-sends a fixed `page_size` without saying whether that is required. The version below is the one to copy. It runs as written.

```python
import os
from typing import Any, Dict, Iterator, Optional

import requests

BASE = os.environ.get("RHO_BASE_URL", "https://rhoapi.rho.co/api/v1")


def paginate(
    session: requests.Session,
    path: str,
    resource_key: str,
    params: Optional[Dict[str, Any]] = None,
    page_size: int = 100,
) -> Iterator[Dict[str, Any]]:
    """Yield every item from a Rho list endpoint.

    `params` must stay byte-identical across pages: any change to a filter or
    to sort_by/order invalidates the cursor with 400. page_size is the one
    parameter that may change mid-walk.
    """
    base_params = dict(params or {})
    base_params["page_size"] = page_size
    page_token: Optional[str] = None
    seen: set = set()

    while True:
        query = dict(base_params)
        if page_token is not None:
            query["page_token"] = page_token

        resp = session.get(f"{BASE}{path}", params=query, timeout=30)
        resp.raise_for_status()          # replace with request_with_retry, see 6.2.5
        body = resp.json()

        items = body[resource_key]
        for item in items:
            # Offset cursors can repeat a row if the data shifts under the walk.
            # De-duplicate on the opaque id rather than trusting the cursor.
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            yield item

        page_token = body["page"]["next_page_token"]
        if page_token is None:           # the ONLY terminator
            return
        if not items:
            # Defensive: a non-null token on an empty page would loop forever.
            raise RuntimeError(f"{path}: empty page with a non-null cursor")


def make_session(token: str) -> requests.Session:
    s = requests.Session()               # keep-alive roughly halves per-call latency
    s.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept-Encoding": "gzip",       # must name gzip explicitly, see 6.2.8
    })
    return s
```

Verified against the sandbox, with the module above saved as `rho_paginate.py`:

```bash
export RHO_BASE_URL=https://rhoapi-sandbox.rho.co/api/v1 RHO_API_TOKEN=sandbox
python3 -c '
import os, rho_paginate as r
s = r.make_session(os.environ["RHO_API_TOKEN"])
print(sum(1 for _ in r.paginate(s, "/transactions", "transactions", {"account_type": "checking"}, page_size=7)))
print(sum(1 for _ in r.paginate(s, "/accounts", "accounts", page_size=3)))'
# -> 42
# -> 14
```

42 matches the sandbox corpus (42 of 72 transactions are `account_type=checking`) and 14 matches the full accounts set, at page sizes that force 6 and 5 round trips respectively.

Three details worth naming. The `seen` set is unbounded, so for a multi-million-row walk swap it for a bloom filter or drop de-duplication and pin a window filter instead (6.1.6). `resource_key` is passed explicitly because it is not always derivable (`/invoicing/customers` returns `customers`). And `page_size` lives in `base_params` rather than being re-sent as a literal, so a caller can raise it mid-walk without touching the cursor.

#### 6.1.10 A correct iteration loop in TypeScript

Same contract, using the platform `fetch` (Node 18+, Deno, Bun, or a browser proxied through your own backend, since the API sends no CORS headers at all).

```typescript
const BASE = process.env.RHO_BASE_URL ?? "https://rhoapi.rho.co/api/v1";
const TOKEN = process.env.RHO_API_TOKEN ?? "";

interface Page {
  next_page_token: string | null; // present on every response, null on the last page
}
type ListResponse<K extends string, T> = { page: Page } & { [P in K]: T[] };

/** Walk every page of a Rho list endpoint.
 *  `params` must be byte-identical on every page: changing a filter or the
 *  sort invalidates the cursor with 400. page_size may change mid-walk. */
export async function* paginate<K extends string, T extends { id: string }>(
  path: string,
  resourceKey: K,
  params: Record<string, string> = {},
  pageSize = 100,
): AsyncGenerator<T> {
  let pageToken: string | null = null;
  const seen = new Set<string>();

  for (;;) {
    const query = new URLSearchParams({ ...params, page_size: String(pageSize) });
    if (pageToken !== null) query.set("page_token", pageToken);

    const resp = await rhoFetch(`${BASE}${path}?${query.toString()}`); // see 6.2.6
    if (!resp.ok) {
      const problem = await resp.text();
      throw new Error(`GET ${path} -> ${resp.status}: ${problem}`);
    }
    const body = (await resp.json()) as ListResponse<K, T>;

    const items = body[resourceKey] as T[];
    for (const item of items) {
      // Offset cursors can repeat a row if the data shifts under the walk.
      if (seen.has(item.id)) continue;
      seen.add(item.id);
      yield item;
    }

    pageToken = body.page.next_page_token;
    if (pageToken === null) return;                 // the ONLY terminator
    if (items.length === 0) throw new Error(`${path}: empty page with a non-null cursor`);
  }
}
```

Verified against the sandbox with `node rho.ts` on Node 26 (native type stripping), `RHO_BASE_URL` pointed at sandbox: 42 checking transactions at `pageSize` 7, 14 accounts at `pageSize` 3, identical to the Python walk.

The `next_page_token: string | null` type is the point of the `Page` interface. If you generate types from Rho's OpenAPI document you will get `string` and your terminal page will throw, per the divergence in 6.1.1.

#### 6.1.11 What pagination does not give you

| Missing | Consequence |
| --- | --- |
| Any total or count | Result-set size is knowable only by walking it. Progress bars are impossible; so is "show 1 of 40 pages" |
| Backwards paging | Iteration is forward only. Re-walk from the start to go back |
| A durable resume point | No documented cursor TTL and explicit advice against bookmarking. Resume from a timestamp filter plus client-side `id` de-duplication |
| An incremental-sync primitive | There is no `updated_after` on any endpoint. Delta sync must be built from `initiated_after`/`posted_after` (transactions) or `date_after` (invoices) plus client dedup. See the Filtering and sorting section |
| `ETag` / `Last-Modified` / `304` | Observed, none are emitted and no conditional request works. Every poll pays the full payload, about 5.6 KB gzipped per 100-transaction page |
| Webhooks or an event stream | Nothing in the corpus. Every integration is poll-only, under the rate ceiling in 6.2 |

---

### 6.2 Rate limits

#### 6.2.1 What is documented

From `/docs/v1/rate-limits`, verbatim:

| Limit | Threshold |
| --- | --- |
| Per API Access Token | Approximately 60 requests per minute |
| Per source IP | Approximately 600 requests per minute |

Plus five prose commitments on the same page:

- "These limits apply uniformly across all public Rho API endpoints."
- "The source-IP limit covers the combined traffic from every integration sharing that IP address, including integrations using different API Access Tokens."
- "We enforce rate limits across a distributed edge network, so the limits are approximate rather than an exact concurrency allowance. Clients must not assume that exactly 60 simultaneous requests will succeed."
- "Pace traffic steadily below one request per second instead of sending the full minute's allowance in a burst."
- "When a limit is exceeded, we return `429 Too Many Requests`."

Derived budget arithmetic, which is the number you actually plan against:

| Quantity | Value |
| --- | --- |
| Per-token budget | ~60 req/min, ~1 req/s, ~86,400 req/day |
| Per-IP budget | ~600 req/min, ~10 req/s |
| Tokens needed to saturate one IP | 10, at full per-token rate |
| Max rows/min per token at `page_size=100` | 6,000 |
| Max rows/min per IP at `page_size=100` | 60,000 |
| Time to walk 1,000,000 transactions on one token | ~167 minutes at the ceiling, longer at the documented pacing |

The per-IP pool is shared, and that interacts badly with the auth guide's advice to pin a stable egress IP for the token allowlist: concentrating your traffic on one NAT gateway also concentrates your rate-limit risk there, where an unrelated team's runaway job can throttle you.

#### 6.2.2 What was actually observed

Neither documented limit is enforced on the sandbox host at any load a responsible probe can generate.

| Test (observed) | Documented expectation | Result |
| --- | --- | --- |
| 60 requests to `/accounts` on token `sandbox`, one connection, 10.67 s (337 req/min) | throttle after ~60 in the minute | 60 x 200 |
| 60 more at concurrency 30 in 1.173 s, same token, same minute (~120 cumulative) | throttle | 60 x 200 |
| 30 more at concurrency 30 against `/transactions?page_size=100`, same minute (~150 cumulative) | throttle | 30 x 200 |
| 60 at concurrency 60 in 0.871 s (68.9 req/s, 4,134 req/min instantaneous) | docs explicitly warn 60 simultaneous may not succeed | all 60 succeeded, twice |
| 65 requests on a brand-new, never-used bearer token in 11.30 s | a fresh bucket should exhaust at ~60 | 65 x 200 |
| 300 requests to `/transactions` at concurrency 20 in ~4 s (~3,600 req/min) | throttle | 300 x 200 |
| 30 requests at concurrency 30 in ~1 s, re-run 2026-09-12 | throttle | 30 x 200, zero rate-limit headers |

Roughly 430 requests over 10.5 minutes produced zero `429` responses and zero `5xx`. The unique-token run rules out the possibility that the literal string `sandbox` is allowlisted.

```bash
# reproduce the last row: 30 concurrent calls, all 200, no rate-limit headers anywhere
B=https://rhoapi-sandbox.rho.co/api/v1
for i in $(seq 1 30); do
  curl -s -o /dev/null -D "/tmp/h$i" -w "%{http_code} " "$B/accounts?page_size=1" \
    -H "Authorization: Bearer sandbox" &
done; wait; echo
grep -lihE "retry-after|ratelimit" /tmp/h[0-9]* | wc -l   # -> 0
```

> **Divergence:** the rate-limits page states concrete thresholds with no environment qualifier, and the sandbox enforces neither. An integrator who load-tests against the sandbox will conclude their client is correctly paced and ship something production may reject. Treat the sandbox as a correctness environment only, never a capacity environment, and size your client against the documented 60/min per token and 600/min per IP.

> **Divergence:** `429` is documented in the rate-limits guide but appears in **none** of the 14 operation reference pages, which uniformly list `200, 400, 401, 403, 500, 503` (plus `404` on the eight single-resource operations). A client generated from the OpenAPI document will not have a `429` branch. Add it by hand.

> **Divergence:** because `429` is unreachable in the sandbox, the entire documented `Retry-After` contract, including the unusual `0` case, is untestable against Rho's own test environment. Nobody can confirm from outside that a `429` from Rho carries `Retry-After` at all. Write the retry path blind, unit-test it against synthetic responses (as the implementations below are), and make a missing `Retry-After` a first-class case.

#### 6.2.3 The `Retry-After` contract, including the documented zero

Verbatim from the docs:

- "If it is a positive integer, wait at least that many seconds before retrying."
- "If it is `0`, we have not applied a fixed cooldown. This does not guarantee that an immediate retry will succeed, so use exponential backoff with jitter instead of retrying in a tight loop."

| `Retry-After` value | Required client behavior | Documented? |
| --- | --- | --- |
| Positive integer seconds | Wait at least that many seconds | Yes |
| `0` | No cooldown was computed. Do **not** retry immediately. Fall through to exponential backoff with jitter | Yes |
| Absent | Not documented. Handle it: fall through to backoff | No |
| HTTP-date form (RFC 9110 permits it) | Not documented. Parse it defensively rather than crashing | No |
| Negative or unparseable | Not documented. Fall through to backoff | No |

The `0` case is the trap. RFC 9110 defines `Retry-After` as a delay in seconds or an HTTP-date, so a naive implementation reads `0`, sleeps zero seconds, and hammers the endpoint in a tight loop precisely when the service is asking it to stop. Rho has repurposed `0` to mean "no fixed cooldown", which is the opposite of what the literal value says. Any correct implementation must special-case it.

Both implementations below encode the same rule: `Retry-After` produces a delay only when it parses to a strictly positive value; every other case, including `0`, absent, negative and malformed, falls through to full-jitter exponential backoff.

#### 6.2.4 No budget observability

| Missing header | Consequence |
| --- | --- |
| `RateLimit-Limit` / `RateLimit-Remaining` / `RateLimit-Reset` | You cannot see how much budget you have left, so you cannot self-pace. Fixed conservative pacing is the only strategy available |
| `X-RateLimit-*` | Same. The de-facto convention is absent too |
| `Retry-After` | Never observed on any status code in roughly 430 responses |
| `X-Request-Id` / `Request-Id` / `traceparent` | No correlation handle for support. Cloudflare's `cf-ray` is the only per-request identifier that exists. Log it on every call |

The complete observed header set on a 200 is ten headers and contains none of the above:

```
HTTP/2 200
date: Sat, 12 Sep 2026 00:25:31 GMT
content-type: application/json
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: a39ac685feff0f61-EWR
```

#### 6.2.5 A correct backoff in Python

Retries `429`, `500`, `502`, `503`, `504` and transport failures. Honors a positive `Retry-After`, treats `0`, absent, negative and malformed as "use backoff", caps any single sleep, adds jitter even to an honored header so a fleet does not resynchronize, and drains the body so the connection can be reused.

```python
import datetime
import email.utils
import random
import time
from typing import Any, Dict, Optional

import requests

RETRYABLE = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 6
BASE_DELAY = 0.5      # seconds
MAX_DELAY = 60.0      # cap on any single sleep
MAX_HONORED_RETRY_AFTER = 300.0


def parse_retry_after(value: Optional[str], now: Optional[float] = None) -> Optional[float]:
    """Return a delay in seconds, or None if the header gives no usable delay.

    Rho documents only integer seconds and assigns `0` the special meaning
    "no fixed cooldown applied", so `0` must NOT be treated as "retry now".
    RFC 9110 also permits an HTTP-date, which Rho does not document; parse it
    anyway rather than crashing.
    """
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        seconds = int(value)
    except ValueError:
        try:
            parsed = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        if parsed is None:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=datetime.timezone.utc)
        now = time.time() if now is None else now
        delta = parsed.timestamp() - now
        return delta if delta > 0 else None
    if seconds <= 0:
        return None          # the documented `0` case: fall back to backoff
    return float(seconds)


def backoff_delay(attempt: int) -> float:
    """Full-jitter exponential backoff. attempt is 1-based."""
    ceiling = min(MAX_DELAY, BASE_DELAY * (2 ** (attempt - 1)))
    return random.uniform(0.0, ceiling)


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 30.0,
    sleep=time.sleep,
) -> requests.Response:
    last_exc: Optional[Exception] = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = session.request(method, url, params=params, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
            if attempt == MAX_ATTEMPTS:
                raise
            sleep(backoff_delay(attempt))
            continue

        if resp.status_code not in RETRYABLE:
            return resp
        if attempt == MAX_ATTEMPTS:
            return resp

        header_delay = parse_retry_after(resp.headers.get("Retry-After"))
        if header_delay is not None:
            delay = min(header_delay, MAX_HONORED_RETRY_AFTER)
            delay += random.uniform(0.0, 1.0)   # de-synchronise a fleet
        else:
            delay = backoff_delay(attempt)
        resp.close()
        sleep(delay)

    assert last_exc is not None
    raise last_exc
```

Because Rho cannot produce a `429`, the only way to test this is against a synthetic server. Assertions that must pass:

```python
assert parse_retry_after(None) is None
assert parse_retry_after("") is None
assert parse_retry_after("0") is None      # the documented zero, must fall through
assert parse_retry_after("-3") is None
assert parse_retry_after("5") == 5.0
assert parse_retry_after("garbage") is None
# a local server returning 429 (Retry-After: 0), then 429 (Retry-After: 1), then 200
# -> 3 attempts, first sleep < 0.5 s (backoff, not the header), second sleep in [1.0, 2.0]
```

Those assertions were run against a `http.server` stub and pass: attempt count 3, sleeps `[0.37, 1.075]`.

#### 6.2.6 The same in TypeScript

```typescript
const RETRYABLE = new Set([429, 500, 502, 503, 504]);
const MAX_ATTEMPTS = 6;
const BASE_DELAY_MS = 500;
const MAX_DELAY_MS = 60_000;
const MAX_HONORED_RETRY_AFTER_MS = 300_000;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** Milliseconds of delay from a Retry-After header, or null when it gives none.
 *  Rho documents `0` as "no fixed cooldown applied", so 0 must fall through
 *  to exponential backoff rather than becoming an immediate retry. */
export function parseRetryAfter(value: string | null, nowMs = Date.now()): number | null {
  if (value === null) return null;
  const trimmed = value.trim();
  if (trimmed === "") return null;
  if (/^-?\d+$/.test(trimmed)) {
    const seconds = Number(trimmed);
    return seconds > 0 ? seconds * 1000 : null;
  }
  const at = Date.parse(trimmed); // RFC 9110 also allows an HTTP-date
  if (Number.isNaN(at)) return null;
  const delta = at - nowMs;
  return delta > 0 ? delta : null;
}

export function backoffDelayMs(attempt: number): number {
  const ceiling = Math.min(MAX_DELAY_MS, BASE_DELAY_MS * 2 ** (attempt - 1));
  return Math.random() * ceiling; // full jitter
}

export async function rhoFetch(url: string, init: RequestInit = {}): Promise<Response> {
  for (let attempt = 1; ; attempt++) {
    let resp: Response;
    try {
      resp = await fetch(url, {
        ...init,
        headers: {
          Authorization: `Bearer ${process.env.RHO_API_TOKEN ?? ""}`,
          "Accept-Encoding": "gzip",
          ...(init.headers ?? {}),
        },
        signal: AbortSignal.timeout(30_000),
      });
    } catch (err) {
      if (attempt >= MAX_ATTEMPTS) throw err;
      await sleep(backoffDelayMs(attempt));
      continue;
    }
    if (!RETRYABLE.has(resp.status) || attempt >= MAX_ATTEMPTS) return resp;

    const header = parseRetryAfter(resp.headers.get("retry-after"));
    const delay =
      header === null
        ? backoffDelayMs(attempt)
        : Math.min(header, MAX_HONORED_RETRY_AFTER_MS) + Math.random() * 1000;
    await resp.arrayBuffer(); // drain so the connection can be reused
    await sleep(delay);
  }
}
```

Verified the same way against a `node:http` stub returning `429 Retry-After: 0`, then `429 Retry-After: 1`, then `200`: three attempts, total elapsed 2.2 s, which is consistent with backoff on the first and an honored 1 second plus jitter on the second. `parseRetryAfter` returns `null` for `null`, `""`, `"0"`, `"-3"` and `"garbage"`, `5000` for `"5"`, and a positive value for a future HTTP-date.

#### 6.2.7 Pacing rules that follow

1. **Budget one request per second per token.** The docs say "below one request per second", which reads as under 60/min, not at 60/min. At `page_size=100` that is still 6,000 rows a minute.
2. **Do not burst.** Queue and cap concurrency rather than firing a minute's allowance at once, because a distributed counter can trip while your other requests are still in flight.
3. **Use one token per integration and count tokens against the IP pool.** Ten tokens at full rate saturate a single egress IP.
4. **Reuse connections, but do not over-multiplex one of them.** Observed, keep-alive roughly halves per-call latency (p50 206 ms cold, 112 ms warm), but pushing 50 concurrent streams onto a single HTTP/2 connection made p50 about 13x worse (1,504 ms) for only 31 req/s aggregate. Prefer a small pool of connections with modest per-connection concurrency.
5. **Budget 90 to 145 ms of server time per call** from a US East client, plus 70 to 100 ms of connect and TLS on a cold connection, with a rare tail near 1 s. Payload size is not a latency driver.
6. **Send `Accept-Encoding: gzip` explicitly.** Observed, gzip is the only encoding served; brotli, zstd, deflate and the `*` wildcard all get an uncompressed body. On a 40,768-byte transactions page gzip cuts the wire cost to about 5.6 KB, roughly 7x.
7. **Log `cf-ray` on every request.** It is the only identifier Rho support can correlate against.

---

### 6.3 Errors

#### 6.3.1 The RFC 9457 claim versus reality

The API reference overview states: "Errors follow [RFC 9457 problem details]". The auth guide cites the obsolete RFC 7807 for the same objects. Every operation page documents the same four-field schema:

| Field | Type | Required | Documented description |
| --- | --- | --- | --- |
| `type` | string | required | "A URI reference that identifies the problem type. Example: `about:blank`" |
| `title` | string | required | "A short, human-readable summary of the problem type." |
| `status` | integer | required | "The HTTP status code." |
| `detail` | string | optional | "A human-readable explanation specific to this occurrence of the problem." |

> **Divergence:** `type` is not a URI in practice. Observed values are the bare strings `"2"`, `"1303"`, `"1317"` and `"about:blank"`. The first three are numeric family codes. RFC 9457 says a `type` that is not a usable URI should be treated as `about:blank`, so a strictly conforming client collapses all three into one generic type and loses the only machine-readable distinction the API offers.

> **Divergence:** `title` is occurrence-specific, not type-specific. RFC 9457 section 3.1.2 says `title` should not change for a given `type`, but `1303` produces "account not found", "card not found", "statement not found", "customer not found", "invoice not found", "transaction not found", "transaction file not found" and "invoice file not found", and `1317` produces at least seven different strings. The stable part of the document is too coarse to branch on, and the precise part is free prose outside the versioning contract.

> **Divergence:** the auth guide's worked example is `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}`. Observed, the real 401 is `{"type":"2","title":"Unauthenticated","status":401}`: a different `type`, a different `title`, and no `detail` at all. Every 401 and every 404 carries zero diagnostic information beyond the title.

#### 6.3.2 The actual body shapes

Five shapes exist. Only the first four are JSON, and only the first three are problem documents.

| Class | Exact body | Content-Type | Trigger |
| --- | --- | --- | --- |
| Auth | `{"type":"2","title":"Unauthenticated","status":401}` | `application/problem+json` | Missing, empty, or non-`Bearer` Authorization header |
| Parse failure | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: <name>"}` | `application/problem+json` | A value fails type coercion, or a scalar parameter is repeated |
| Semantic validation | `{"type":"1317","title":"<specific message>","status":400}` | `application/problem+json` | The value parses but fails a rule |
| Not found | `{"type":"1303","title":"<resource> not found","status":404}` | `application/problem+json` | Unknown id on a detail route |
| Framework 404 | `404 page not found` | `text/plain; charset=utf-8` | Unknown path under `/api/v1` (Go's `http.NotFound`) |

Beyond those, four non-JSON bodies come from infrastructure in front of the application and your parser must survive all of them:

| Status | Body | Producer |
| --- | --- | --- |
| 405 | **empty**, `content-length: 0`, `allow: GET` | The Go service, on any method other than GET including `HEAD` and `OPTIONS` |
| 411 | HTML, "POST requests require a Content-length header" | Google frontend, before Rho's code. Also returned for `PUT` with the same POST wording |
| 414 | HTML, nginx "Request-URI Too Large" | ingress-nginx, at a URI length ceiling between 8 KB and 16 KB |
| 403 | HTML, Cloudflare "Attention Required!" | Cloudflare WAF, triggered by a nonstandard method token |
| 404 | `default backend - 404`, `text/plain` | ingress-nginx, for paths outside `/api/v1` |

Reproduce the whole set:

```bash
B=https://rhoapi-sandbox.rho.co/api/v1; H="Authorization: Bearer sandbox"
curl -s "$B/accounts?page_size=101"  -H "$H"   # {"type":"1317","title":"page_size must be between 1 and 100","status":400}
curl -s "$B/accounts?page_size=abc"  -H "$H"   # {"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}
curl -s "$B/accounts?page_token=xyz" -H "$H"   # {"type":"1317","title":"page_token must be a valid cursor","status":400}
curl -s "$B/accounts?sort_by=bogus"  -H "$H"   # {"type":"1317","title":"invalid sort_by parameter: \"bogus\"","status":400}
curl -s "$B/accounts/00000000-0000-4000-8000-000000000000" -H "$H"  # {"type":"1303","title":"account not found","status":404}
curl -s "$B/accounts/not-a-uuid"     -H "$H"   # {"type":"about:blank",...,"detail":"invalid parameter: account_id"}
curl -s "$B/accounts"                          # {"type":"2","title":"Unauthenticated","status":401}
curl -s "$B/nope-not-real"           -H "$H"   # 404 page not found      (text/plain)
curl -s -X POST "$B/accounts" -H "$H" -H "Content-Length: 0" -D - -o /dev/null | head -4   # 405, allow: GET, empty body
```

#### 6.3.3 The numeric `type` codes

Four values have been observed across every reachable error path. They are families, not precise identifiers.

| `type` | Status | Meaning | Distinguishing field | Known coverage |
| --- | --- | --- | --- | --- |
| `"2"` | 401 | Unauthenticated. Credential absent, empty, or not presented as `Bearer <value>` | none; `title` is always "Unauthenticated" | Every auth failure, on both `/api/v1` and production `/mcp/v1` |
| `"1303"` | 404 | Resource not found on a detail route | `title` names the resource | account, card, transaction, transaction file, statement, customer, invoice, invoice file |
| `"1317"` | 400 | The value parsed but violated a rule | `title` carries the message and echoes the offending value | `page_size` range, invalid cursor, `sort_by`, `order`, card `type`, card `status`, `min_amount` > `max_amount` |
| `"about:blank"` | 400 | The value failed type binding, or a scalar parameter was repeated | `detail` names the parameter, never echoes the value | any parameter |

Two dialects, and they never mix. A `1317` body carries a descriptive `title` and **no** `detail`. An `about:blank` body carries the generic title "Bad Request" plus a `detail` that names the parameter. So the field you read to find out what went wrong depends on which dialect you got.

Every `1317` title observed:

| Title | Produced by |
| --- | --- |
| `page_size must be between 1 and 100` | all six list endpoints |
| `page_token must be a valid cursor` | garbage token, cross-endpoint token, token plus a changed filter, forged fingerprint, `v:2`, negative offset, offset greater than the total |
| `invalid sort_by parameter: "<value>"` | `/accounts`, `/invoicing/customers` only |
| `invalid order parameter: "<value>"` | `/accounts`, `/invoicing/customers` only |
| `invalid type parameter: "<value>"` | `/cards` only |
| `invalid status parameter: "<value>"` | `/cards` only |
| `min_amount must be less than or equal to max_amount` | `/transactions` only |

#### 6.3.4 Status code to cause

| Status | Reachable in sandbox | Cause | Retry? |
| --- | --- | --- | --- |
| 200 | yes | Success. Note that a `200` with an empty array is ambiguous between "no matching rows" and "your filter was silently dropped": see the Filtering and sorting section on the empty-value trap and the semicolon trap | n/a |
| 301 | yes | `GET /api/v1` with no trailing path, from nginx | Follow it |
| 400 | yes | Two dialects. `about:blank` means an unparseable value or a repeated scalar parameter; `1317` means a rule violation | **No.** Fix the request |
| 401 | yes | Missing, empty, malformed, unknown, revoked, or expired token, or a scheme other than a capital-B `Bearer`. Observed, `bearer sandbox` in lowercase returns 401, which deviates from RFC 7235 case-insensitive scheme matching | No, unless you rotate the credential |
| 403 | **no** | Documented: a valid token missing the required scope, or a source IP outside the token's allowlist. Unreachable in the sandbox, which enforces neither scopes nor allowlists | No |
| 404 | yes | Two shapes: `1303` problem+json for an unknown id on a detail route, `text/plain` for an unknown path | No |
| 405 | yes | Any method other than GET, including `HEAD` and `OPTIONS`. Empty body, `allow: GET`. Observed, this check runs **before** authentication | No |
| 411 | yes | `POST` or `PUT` with no `Content-Length`, from the Google frontend | No |
| 414 | yes | URI longer than the nginx ceiling, between 8 KB and 16 KB | No |
| 422 | **no** | Never observed. Every validation failure is a 400, so status alone cannot separate malformed syntax from invalid content | n/a |
| 429 | **no** | Documented as the rate-limit response. Not reachable in the sandbox at any load; body shape unknown | **Yes**, per 6.2 |
| 500 | not observed | Documented on every operation | Yes, with backoff |
| 503 | not observed | Documented on every operation, with no explanation anywhere of what it means or whether it is retryable | Yes, with backoff |

> **Divergence:** the operation reference documents `403`, `500` and `503` on every endpoint and none of them was reachable in the sandbox, while `405`, `411` and `414` are all readily reachable and documented nowhere. Your error handling has to cover the union, not the documented set.

#### 6.3.5 Parameter validation runs before authentication

This ordering is worth knowing before you debug a credential problem. Observed, with no `Authorization` header at all:

| Request | Status with no credential | Status with a credential |
| --- | --- | --- |
| `GET /accounts?page_size=abc` | **400** `about:blank`, "invalid parameter: page_size" | 400, identical |
| `GET /accounts/not-a-uuid` | **400** `about:blank`, "invalid parameter: account_id" | 400, identical |
| `GET /accounts?page_size=101` | 401 | 400 `1317` |
| `GET /accounts?page_token=garbage` | 401 | 400 `1317` |
| `GET /accounts/<valid-uuid, unknown>` | 401 | 404 `1303` |
| `POST /accounts` | **405** | 405 |

So type binding (the `about:blank` family) and the method check both sit in front of authentication, while semantic validation (the `1317` family) and resource lookup sit behind it. The operational rule: **a non-401 response does not prove your token worked.** If you are smoke-testing credentials, use a request that is unambiguously well-formed, such as `GET /accounts`, and check for `200`.

#### 6.3.6 A correct error parser

Branch on HTTP status. Capture `type` and `title` for logs. Never make control flow depend on either, because `type` is too coarse (one code covers eight resources) and `title` is free prose that the versioning policy does not cover.

```python
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass(frozen=True)
class RhoError(Exception):
    status: int
    kind: str          # branch on this, never on `type` or `title`
    type_code: Optional[str]
    message: str
    cf_ray: Optional[str]

    def __str__(self) -> str:
        return f"{self.status} {self.kind}: {self.message} (cf-ray={self.cf_ray})"


_KIND_BY_STATUS = {
    400: "bad_request",       # your query is wrong, do not retry unchanged
    401: "unauthenticated",   # missing / malformed / unknown / revoked / expired token
    403: "forbidden",         # valid token, missing scope or source IP off the allowlist
    404: "not_found",
    405: "method_not_allowed",
    429: "rate_limited",      # retryable
    500: "server_error",      # retryable
    503: "unavailable",       # retryable
}


def raise_for_rho(resp: requests.Response) -> None:
    if resp.ok:
        return
    kind = _KIND_BY_STATUS.get(resp.status_code, "unexpected")
    type_code: Optional[str] = None
    message = resp.text[:500]

    # Only application-level errors are problem+json. 405 has an empty body,
    # unrouted paths are text/plain, and 403/411/414 from the edge are HTML.
    if resp.headers.get("content-type", "").startswith("application/problem+json"):
        try:
            body = resp.json()
        except ValueError:
            body = {}
        if isinstance(body, dict):
            type_code = body.get("type")
            message = body.get("detail") or body.get("title") or message

    raise RhoError(
        status=resp.status_code,
        kind=kind,
        type_code=type_code,
        message=message,
        cf_ray=resp.headers.get("cf-ray"),
    )
```

Run against the live sandbox it produces, in order, for the nine probes in 6.3.2:

```
400 kind=bad_request          type=1317         msg='page_size must be between 1 and 100'
400 kind=bad_request          type=about:blank  msg='invalid parameter: page_size'
400 kind=bad_request          type=1317         msg='page_token must be a valid cursor'
404 kind=not_found            type=1303         msg='account not found'
400 kind=bad_request          type=about:blank  msg='invalid parameter: account_id'
401 kind=unauthenticated      type=2            msg='Unauthenticated'
404 kind=not_found            type=None         msg='404 page not found\n'
405 kind=method_not_allowed   type=None         msg=''
```

The last two rows are the reason for the content-type guard: a parser that assumes JSON on every non-2xx crashes on the plain-text 404 and on the zero-byte 405.

#### 6.3.7 Rules for an error handler

1. **Branch on status, log `type` and `title`.** There is no stable machine-readable error code, and the free-prose `title` is not covered by the versioning contract.
2. **Never assume the body is JSON.** Four reachable statuses return HTML, plain text, or nothing. Guard on `content-type: application/problem+json` before parsing.
3. **Read `detail` for `about:blank` and `title` for `1317`.** The two dialects put the useful string in different fields and never populate both.
4. **Do not retry a 400.** It means your query is wrong, and it will be wrong again.
5. **Handle 429 even though the OpenAPI document omits it,** and handle a missing `Retry-After` on it.
6. **Log `cf-ray` on every response, success or failure.** There is no request id; `cf-ray` is the only handle Rho support can correlate.
7. **Do not infer authentication success from a non-401.** Type-binding 400s and the 405 method check run ahead of auth (6.3.5).
8. **Treat `200` with an empty array as suspicious after a filtered query.** A silently dropped filter and a genuinely empty result are indistinguishable. Assert against an unfiltered control query.

---

### 6.4 Versioning and compatibility

#### 6.4.1 The model

From `/docs/v1/versioning`, which calls itself "the stability contract for the Rho API":

- "The Rho API is versioned per release; today that's the URL path `/api/v1`. The current version is `v1`."
- "**`v1` is stable and additive-only**. A request that works today keeps working. Changes that would break existing code require a **new API version**; we do not ship them into `/api/v1`."
- "Any `v1` deprecation or sunset comes with **at least 15 days' notice** before the change takes effect."

Versioning is by URL path only. There is no version header, no date-pinned version, no `Accept` media-type versioning, and no per-account pinning. The OpenAPI document additionally carries `Version: 1.0.0`, which is a document version and not something you can request. A future `v2` would be a separate path, so `v1` callers are never migrated implicitly. That is a good property: you will never be moved without changing a URL.

#### 6.4.2 The change classification

Published exhaustively, and short enough to quote in full:

| Change | Classification | Ships into `v1`? |
| --- | --- | --- |
| Add an enum value | Non-breaking | Yes, at any time |
| Add a nullable response field | Non-breaking | Yes, at any time |
| Add an optional query parameter | Non-breaking | Yes, at any time |
| Remove or rename an enum value | Breaking | No, new version |
| Remove a response field | Breaking | No, new version |
| Change a field's type | Breaking | No, new version |
| Make an optional field required | Breaking | No, new version |

Read that first column again as a threat model: Rho reserves the right to send you, without notice and without a version bump, an enum value you have never seen, a response field you have never seen, and to accept a query parameter you do not send. Those three are the ones your code must survive.

#### 6.4.3 What the policy does not classify

The list of breaking changes is short, which makes its silences load-bearing. None of the following is classified anywhere on the page:

| Unclassified change | Why it matters to you |
| --- | --- |
| Adding a **non-nullable** response field | Only nullable additions are blessed. A non-nullable addition is neither permitted nor forbidden |
| Adding a **required** query parameter | Only optional additions are blessed |
| Adding a new endpoint | Presumably additive, never stated |
| Removing an endpoint | Presumably needs a version, never stated |
| Changing pagination defaults or maxima | A `page_size` maximum dropping from 100 to 50 would break any client hard-coding 100, and the page does not say whether that requires a new version |
| Tightening rate limits | Not addressed. The published limits already say "approximately" |
| Changing error `detail` or `title` strings | Not addressed, which is why you must not parse them |
| Changing a sort default | Not addressed. `/transactions` defaulting to `initiated_at` desc is behavior your cursors depend on |
| Changing the **meaning** of an existing enum value without renaming it | The worst case, and the policy is silent |
| MCP protocol version support (`2026-07-28`, `2025-11-25`, `2025-06-18`) | Dropping `2025-06-18` later would be breaking under no stated policy |

#### 6.4.4 The deprecation notice has no delivery channel

A 15-day floor is short by industry norms, and it applies to "any `v1` deprecation or sunset".

> **Divergence:** the versioning page promises at least 15 days' notice but never names the channel that notice arrives on. There is no changelog URL anywhere in the documentation corpus, no status page reference, and observed, no `Deprecation` or `Sunset` response header (RFC 8594) on any of roughly 430 captured responses. The complete header set on a 200 is the ten headers listed in 6.2.4. So the machine-readable channel that would normally carry a deprecation notice does not exist, and the human channel is unspecified. In practice you will learn about a deprecation from an email to whoever created the token, or from your own monitoring.

The operational consequence: build the monitoring that the notice channel does not give you. Alert on a schema drift (an unknown enum value, an unknown field) appearing in production traffic, because that is the earliest signal you will get that something changed.

#### 6.4.5 Client obligations as engineering rules

Rho publishes four obligations. Each is restated below as a concrete rule, with the failure it prevents.

**1. Never switch on an unknown enum without a default.**

Rho's wording: "Give any `switch` on it a default case so a new value shows up as unknown rather than an error." The shipped enums are already large, which tells you how often they grow: `cards.status` has 11 values (`printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `active`, `expiring`, `locked`, `canceled`, `suspended`, `expired`), `transactions.transaction_type` has 22 distinct values in the sandbox corpus alone, `accounts.account_type` has 5, and `invoices.status` has 6. Concretely:

- Model every enum as `string` at the wire boundary, and map to your own closed type in one place with an explicit `unknown` arm.
- In TypeScript, do not type a response field as a union of literals. Type it `string`, then narrow. A union literal type is a lie about the wire, and structural typing will not catch it at runtime.
- In Rust, `#[serde(other)]` on a catch-all variant. In Java, `@JsonEnumDefaultValue`. In Go, a plain `string`. In Kotlin and Swift, a case that carries the raw string.
- An unknown value must degrade, never throw. A new `transaction_type` should render as "other" in a ledger view and must not abort a reconciliation run.
- Do not persist the enum as a database `ENUM` column or a constrained `CHECK`. A new value from Rho becomes an insert failure at 3 a.m.

**2. Ignore unknown response fields.**

- Turn off strict deserialization at the Rho boundary specifically: Jackson `FAIL_ON_UNKNOWN_PROPERTIES = false`, serde without `deny_unknown_fields`, Zod `.passthrough()` rather than `.strict()`, Pydantic `model_config = ConfigDict(extra="ignore")`.
- If you use code generation from Rho's OpenAPI document, check what your generator does with additional properties by default. Several generate strict models.
- Do not checksum or hash a response body to detect change. A new field added upstream changes the hash without changing anything you care about.

**3. Treat IDs as opaque strings.**

- Do not parse structure out of an id. Most ids in the sandbox look like UUIDs, but statement ids are short numeric-looking strings (`572981`, `439951`, `200527`) and are not validated as UUIDs at all, so a garbage statement id returns 404 rather than 400. Any code that assumes "Rho ids are UUIDs" is already wrong.
- Do not use an id's format to route. Do not infer a resource type from an id.
- Store them as `TEXT` or `VARCHAR` with generous headroom, never `UUID`, never `VARCHAR(36)`. The documented obligation is explicit: "without assuming a fixed length or layout".
- Compare ids byte for byte. Do not case-normalize.

**4. Two more rules the policy implies but does not state.**

- **Never switch on `type` in an error body, and never parse `title` or `detail`.** Neither is covered by the versioning contract, `type` is a coarse family code shared across eight resources, and the titles are free prose. Branch on HTTP status (6.3.6).
- **Never persist or parse a `page_token`.** Its "format and lifetime are not part of the API contract and may change without notice", and it demonstrably has two different internal formats already (6.1.4). Everything in 6.1.3 is diagnostics, not interface. If you build the offset-forging total-count trick, you have shipped a dependency on the one thing Rho explicitly disclaimed.

#### 6.4.6 MCP parity

The versioning page extends the same policy to the MCP surface: "The MCP server is 1:1 with the REST API, so the `/mcp/v1` tool schemas follow the same policy as the REST contracts above: additive-only, with breaking changes requiring a new version."

It goes further on tool names: "Tool *names* derive from the frozen `v1` operationIds, so **tool names will never change**." The 14 operationIds are `listaccounts`, `getaccount`, `listcards`, `getcard`, `listtransactions`, `gettransaction`, `gettransactionfile`, `liststatements`, `getstatement`, `listinvoicingcustomers`, `getinvoicingcustomer`, `listinvoicinginvoices`, `getinvoicinginvoice`, `getinvoicinginvoicefile`. Tool descriptions are explicitly not part of the contract and may change at any time.

> **Divergence:** the "1:1 with the REST API" claim is not quite true at the byte level. Observed, the same problem document serializes its keys in different orders on the two surfaces: `/api/v1` returns `{"type":"2","title":"Unauthenticated","status":401}` while production `/mcp/v1` returns `{"status":401,"title":"Unauthenticated","type":"2"}`. Same fields, same values, different serializers, which implies two implementations behind one stated contract. Any client comparing error bodies by hash across the two surfaces will see a difference where none is intended.

> **Divergence:** `/mcp/v1` does not exist on the sandbox host. Observed, `https://rhoapi-sandbox.rho.co/mcp/v1` returns `404 default backend - 404` from the ingress default backend, meaning no route is configured, while the same path on production returns a proper `401 application/problem+json`. The MCP guide documents the production URL and never says the sandbox lacks the surface. See the MCP section.

---

### 6.5 The short version

| Mechanism | The rule |
| --- | --- |
| Pagination | Loop until `page.next_page_token === null`, never on a short page. Replay the filter query byte for byte; only `page_size` may change. De-duplicate on `id`, because five of six endpoints use an offset cursor that cannot honor the documented stability promise. Type the token `string \| null`. Never parse or persist it |
| Rate limits | Size against the documented 60/min per token and 600/min per IP, not against the sandbox, which enforces neither. Pace under 1 req/s per token, cap concurrency, reuse connections without over-multiplexing |
| Retries | Retry 429, 500, 502, 503, 504 and transport errors with full-jitter exponential backoff. Honor `Retry-After` only when it parses to a strictly positive value; `0`, absent, negative and malformed all mean "use backoff". Add `429` to any generated client, since the OpenAPI document omits it |
| Errors | Branch on HTTP status only. Guard on `content-type: application/problem+json` before parsing. `about:blank` puts the detail in `detail`; `1317` puts it in `title`. Log `type`, `title` and `cf-ray`. A non-401 does not prove your token worked |
| Versioning | Assume new enum values, new response fields and new optional parameters arrive without notice. Default case on every enum, lenient deserialization at the boundary, ids as opaque variable-length strings. Deprecation notice is at least 15 days (a floor, not a fixed figure) and arrives on no machine-readable channel, so monitor for schema drift yourself |
## 7. MCP and agent access

Rho ships a first-party MCP server in production at `https://rhoapi.rho.co/mcp/v1`. It is the surface most people will actually use, because it is how Claude, Claude Code, and any other Streamable HTTP MCP client reach Rho data without you writing a line of REST code.

The official documentation for it is 38 lines long (`https://docs.rho.co/docs/v1/mcp`). It gives one URL, one transport, three protocol version strings, one `claude mcp add` command, two authentication paths, and then declines to list the tools, telling you to introspect the server yourself. Everything the doc does say is reproduced and verified below. Everything it does not say is the more interesting half of this section: there is no sandbox MCP endpoint, the protected-resource metadata is public and more informative than the docs, dynamic client registration is disabled, and the single published setup command writes a long-lived bearer token into a file that teams commit to git.

All probes in this section were run on 2026-09-12 between 00:26 and 00:27 UTC against unauthenticated production metadata endpoints and against the sandbox. Every one is runnable as written.

### 7.1 Endpoint and transport

| Property | Value | Source |
| --- | --- | --- |
| MCP endpoint (production) | `https://rhoapi.rho.co/mcp/v1` | Official docs, `docs/v1/mcp` |
| REST endpoint (production) | `https://rhoapi.rho.co/api/v1` | Official docs, OpenAPI servers block. See "Base URLs and environments". |
| MCP endpoint (sandbox) | Does not exist. Returns 404 | Observed, section 7.2 |
| Transport | MCP over Streamable HTTP: one HTTP endpoint, JSON-RPC over POST, optional `text/event-stream` response | Official docs |
| stdio / WebSocket / legacy SSE endpoint | Not offered, not documented | Absence in `docs/v1/mcp` |
| Path strictness | Only the exact path `/mcp/v1` is served | Observed |
| Contract parity | "MCP uses the same API contract, authentication model, scopes, and error behavior as the REST API" | Official docs |
| Tool schema stability | Same additive-only policy as the REST contract. Tool names derive from frozen `v1` operationIds and "will never change". Tool descriptions are explicitly outside the contract | Official docs, `docs/v1/versioning`, "MCP parity" |
| Edge stack | Cloudflare in front of a Google origin (`server: cloudflare`, `via: 1.1 google`, `cf-cache-status: DYNAMIC`) | Observed on every response |
| Security headers on the MCP route | `strict-transport-security: max-age=63072000; includeSubDomains; preload`, `x-content-type-options: nosniff`, `x-frame-options: DENY`, `referrer-policy: strict-origin-when-cross-origin` | Observed |

Path strictness, observed. Only `/mcp/v1` exists. The bare prefix, the trailing-slash form, and a speculative `v2` all 404:

```bash
for p in /mcp /mcp/v1/ /mcp/v2; do
  printf "%s -> " "$p"
  curl -sS -o /dev/null -w "%{http_code}\n" "https://rhoapi.rho.co$p"
done
# /mcp -> 404
# /mcp/v1/ -> 404
# /mcp/v2 -> 404
```

Nothing in the docs states whether the server maintains sessions (`Mcp-Session-Id`), supports resumability (`Last-Event-ID`), emits server-to-client notifications, or implements elicitation or sampling. The doc's phrase "the current sessionless protocol" implies a sessionless mode exists, but session-mode behavior is undescribed. Treat all of it as unknown until you introspect a live connection.

### 7.2 There is no sandbox MCP endpoint

This is the first practical thing you need to know and it appears nowhere in Rho's documentation.

The "Getting started" guide sells the sandbox as the safe way to try the API first, verbatim: "The sandbox accepts any non-empty bearer token, so you do not need to create a real API Access Token before testing requests there." That is true for REST and false for MCP. The sandbox host serves no MCP route at all.

Observed. A well-formed `initialize` against the sandbox, with the sandbox's own documented bearer token:

```bash
curl -sS -X POST "https://rhoapi-sandbox.rho.co/mcp/v1" \
  -H "Authorization: Bearer sandbox" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  -D - -o -
```

```text
HTTP/2 404
content-type: text/plain; charset=utf-8
content-length: 21

default backend - 404
```

The sandbox does not publish MCP discovery metadata either, while the REST route on the same host is healthy, which rules out a transient outage:

```bash
curl -sS -o /dev/null -w "prm:  %{http_code}\n" \
  "https://rhoapi-sandbox.rho.co/.well-known/oauth-protected-resource/mcp/v1"
curl -sS -o /dev/null -w "rest: %{http_code}\n" \
  "https://rhoapi-sandbox.rho.co/api/v1/accounts" -H "Authorization: Bearer sandbox"
# prm:  404
# rest: 200
```

> **Divergence:** The docs present a permissive sandbox as the on-ramp that spares you from minting a production token, and they present MCP as a surface with "the same API contract, authentication model, scopes, and error behavior as the REST API". Both statements are true of REST and neither is reachable for MCP. `POST https://rhoapi-sandbox.rho.co/mcp/v1` returns `404 default backend - 404` (observed). To evaluate the MCP server at all, an Account Owner or Admin must mint a production API Access Token, behind a 2FA challenge, pointed at live company money. The docs never say this. Budget for it in your evaluation plan: your first MCP handshake is against production.

Practical consequence for evaluation: build and test your REST integration against the sandbox (see "Sandbox and test data"), then do a single, tightly scoped, IP-allowlisted, short-lived production token for the MCP smoke test, and revoke it when you are done. Section 7.9 gives the concrete recipe.

### 7.3 Protocol versions, the header requirement, and what gets rejected

Official docs, verbatim: "The MCP endpoint advertises and supports protocol versions `2026-07-28`, `2025-11-25`, and `2025-06-18`. Clients can negotiate the current sessionless protocol through `server/discover`. Every non-`initialize` request must include the selected version in the `MCP-Protocol-Version` header. Versions older than `2025-06-18` and JSON-RPC batches are rejected."

| Rule | Detail | Source |
| --- | --- | --- |
| Advertised versions | `2026-07-28`, `2025-11-25`, `2025-06-18` | Official docs |
| Oldest accepted | `2025-06-18`. Anything older is rejected | Official docs |
| Header requirement | `MCP-Protocol-Version: <selected>` on every request except `initialize` | Official docs |
| Negotiation method | `server/discover`, named once, never exemplified | Official docs |
| JSON-RPC batches | Rejected | Official docs |
| Rejection status and body | Not documented for any of the above | Absence |

Three things to flag about this paragraph.

The batch rejection is consistent with the MCP specification itself, which removed JSON-RPC batching in the 2025-06-18 revision. So this is not a Rho restriction so much as Rho stating the floor. If your client library predates that revision and still packs batches, it will fail here, and Rho does not document the failure mode. Send one JSON-RPC request per HTTP POST.

`server/discover` is not a method in any MCP specification revision verifiable from this research corpus, and no request or response example for it appears anywhere in Rho's docs, help center, or marketing pages. Rho names it once and never shows it. Likewise, `2026-07-28` and `2025-11-25` are asserted as protocol revision dates only by Rho, with no spec reference in the corpus. Do not build against `server/discover` on the strength of the doc alone: negotiate the ordinary way with `initialize` and pin `2025-06-18`, which is the one version in the list with an unambiguous published specification.

The rejection semantics are undefined. Nothing states what an unsupported version, a missing `MCP-Protocol-Version` header, or a malformed envelope returns. The docs say error behavior matches REST, which is not a well-defined statement for a JSON-RPC transport: REST errors are HTTP status codes plus `application/problem+json` documents, and JSON-RPC errors are `error` objects inside a 200 response. Section 7.5 shows that at the one error you can actually observe, the REST error contract is not honored.

A minimal, correct handshake and first call looks like this. The `initialize` request carries `protocolVersion` in the body and no header. Every subsequent request carries the header:

```bash
RHO_API_TOKEN="rhobat_..."   # from a secret manager, never inline

# 1. initialize (no MCP-Protocol-Version header on this one)
curl -sS -X POST "https://rhoapi.rho.co/mcp/v1" \
  -H "Authorization: Bearer $RHO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-06-18",
      "capabilities": {},
      "clientInfo": { "name": "rho-eval", "version": "1.0.0" }
    }
  }'

# 2. every later request MUST carry the negotiated version in the header
curl -sS -X POST "https://rhoapi.rho.co/mcp/v1" \
  -H "Authorization: Bearer $RHO_API_TOKEN" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Note the `Accept` header carrying both `application/json` and `text/event-stream`. That is the Streamable HTTP requirement: the server may answer a POST with either a single JSON body or an SSE stream, and the client has to declare it accepts both.

### 7.4 Authentication: the two paths

Rho documents two ways to authenticate an MCP client.

| Path | Credential | Lifetime | Who can create it | Realistic client support |
| --- | --- | --- | --- | --- |
| Direct connection | API Access Token in `Authorization: Bearer <rho_api_access_token>` | Up to 1 year, required expiry, auto-expires after 45 days of inactivity | Account Owners and Admins only, behind a 2FA challenge | Any MCP client that can set a static header |
| Linked app | OAuth connection provided by the MCP client, no manual token | Access token 900 seconds, refresh token 30 days rolling and single-use, grant 1 year | Account Owners and Admins authorize the grant | Effectively Rho-onboarded clients only. See section 7.6 |

Official docs, verbatim: "Direct connections require an API Access Token in `Authorization: Bearer <rho_api_access_token>`. Linked apps use the OAuth connection provided by the MCP client, without requiring users to configure an API Access Token manually. Linked-app availability depends on the client."

The direct path is the REST token verbatim, so everything in the "Authentication and tokens" section applies unchanged: `rhobat_` prefix, shown once at creation, 20 active tokens per business, optional IP allowlist of up to 100 entries, immediate irreversible revocation, `401` for a missing or bad token and `403` for a valid token lacking the scope or arriving from a disallowed IP.

The linked-app path is the OAuth 2.0 Authorization Code with PKCE flow described in "Partner OAuth", against `https://auth.rho.co`. The consequential detail, undocumented, is in section 7.6.

### 7.5 Protected-resource metadata is public, and more accurate than the docs

The MCP server implements RFC 9728 discovery correctly, and the documentation never mentions it. This is the single most useful undocumented artifact on the whole surface, because it is the only machine-readable, authoritative statement of what the MCP endpoint's scopes actually are, and anyone can read it without a token.

Observed. An unauthenticated `initialize` returns a 401 carrying the discovery pointer:

```bash
curl -sS -X POST "https://rhoapi.rho.co/mcp/v1" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  -D - -o -
```

```text
HTTP/2 401
content-type: application/problem+json
content-length: 52
www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"

{"status":401,"title":"Unauthenticated","type":"2"}
```

Following that pointer, unauthenticated, returns HTTP 200:

```bash
curl -sS "https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"
```

```json
{
  "resource": "https://rhoapi.rho.co/mcp/v1",
  "authorization_servers": ["https://auth.rho.co"],
  "bearer_methods_supported": ["header"],
  "scopes_supported": [
    "accounts:read",
    "transactions:read",
    "statements:read",
    "cards:read",
    "invoicing:read"
  ],
  "resource_documentation": "https://docs.rho.co/docs/v1/mcp"
}
```

A second, host-level document exists at the bare well-known path, with the same authorization server and the same five scopes:

```bash
curl -sS "https://rhoapi.rho.co/.well-known/oauth-protected-resource"
# {"resource":"https://rhoapi.rho.co","authorization_servers":["https://auth.rho.co"],
#  "bearer_methods_supported":["header"],
#  "scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],
#  "resource_documentation":"https://docs.rho.co"}
```

The discovery chain is deliberately MCP-shaped and exists nowhere else on the host. Observed:

| Path on `rhoapi.rho.co` | Status |
| --- | --- |
| `/.well-known/oauth-protected-resource/mcp/v1` | 200 |
| `/.well-known/oauth-protected-resource` | 200 |
| `/.well-known/oauth-protected-resource/api/v1` | 404 `page not found` |
| `/.well-known/oauth-authorization-server` | 404 |

> **Divergence, scopes:** The authentication guide at `docs/v1/auth` lists three scopes (`accounts:read`, `transactions:read`, `statements:read`). The live protected-resource metadata lists five, adding `cards:read` and `invoicing:read` (observed, `GET https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1`). The OpenAPI security blocks also list five. The help center article "What connected AI tools have access to in your Rho account" likewise names only Accounts, Transactions and Statements. Anyone sizing the blast radius of an agent connection from the auth guide or the help center alone will underestimate it by the entire Cards and Invoicing surface, which includes cardholder names, billing and shipping addresses, MCC control lists, and the names, emails and postal addresses of the business's own invoicing customers. The live metadata is authoritative. See "Scopes and permissions" for the full table.

> **Divergence, error shape:** The MCP doc says MCP has "the same ... error behavior as the REST API", and the auth guide documents failures as RFC 7807/9457 problem documents shaped `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"..."}`. The live MCP 401 body is `{"status":401,"title":"Unauthenticated","type":"2"}` (observed, request above). The `type` member is the string `"2"`, which is not a URI and therefore not RFC 9457 conformant, the `title` is `Unauthenticated` rather than the documented `Unauthorized`, and there is no `detail` member at all. The parity claim is already false at the first error an MCP client will ever hit. Do not write client error handling that expects the documented shape on this route.

### 7.6 Dynamic client registration is disabled, so OAuth is Rho-onboarded clients only

The generic MCP authorization flow that spec-compliant clients implement is: hit the resource, get a 401 with a `resource_metadata` pointer, fetch the protected-resource document, fetch the authorization server metadata, self-register via RFC 7591 dynamic client registration, then run Authorization Code with PKCE. Rho's server does the first three steps correctly. The fourth step is a dead end.

Observed. The authorization server metadata, fetched unauthenticated, has no `registration_endpoint`:

```bash
curl -sS "https://auth.rho.co/.well-known/oauth-authorization-server" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
print('registration_endpoint present:', 'registration_endpoint' in d); \
print('grants:', d['grant_types_supported']); \
print('pkce:', d['code_challenge_methods_supported']); \
print('scopes at AS:', d['scopes_supported'])"
```

```text
registration_endpoint present: False
grants: ['authorization_code', 'implicit', 'client_credentials', 'refresh_token', 'urn:ietf:params:oauth:grant-type:device_code']
pkce: ['plain', 'S256']
scopes at AS: ['offline_access', 'offline', 'openid']
```

`https://auth.rho.co/.well-known/openid-configuration` returns a byte-identical document (observed, `diff` of both responses is empty). `GET https://auth.rho.co/oauth2/register` returns 404 (observed).

| Authorization server fact | Value | Documented by Rho? |
| --- | --- | --- |
| Issuer | `https://auth.rho.co` | Yes |
| Authorize / token / revoke | `/oauth2/auth`, `/oauth2/token`, `/oauth2/revoke` | Yes |
| Registration endpoint | Absent | No, and its absence is not stated |
| Grants advertised | `authorization_code`, `implicit`, `client_credentials`, `refresh_token`, device code | Only `authorization_code` is documented |
| PKCE methods | `plain` and `S256` | Docs mandate `S256` only |
| Client auth methods | `client_secret_post`, `client_secret_basic`, `private_key_jwt`, `none` | Not documented |
| Scopes advertised at the AS | `offline_access`, `offline`, `openid` only. The five Rho API scopes appear only in protected-resource metadata | Partially |
| Client onboarding | Manual. Email `api-partner-request@rho.co` with app name, company, logo, redirect URIs, requested scopes, privacy policy URI, ToS URI, support email. Rho issues `client_id` and `client_secret` | Yes, in "Partner OAuth" |

> **Divergence:** The docs say "Linked apps use the OAuth connection provided by the MCP client ... Linked-app availability depends on the client", which reads like a client-side capability question. It is not. `auth.rho.co` advertises no `registration_endpoint` (observed), so RFC 7591 dynamic client registration is unavailable and no MCP client can self-register. Every OAuth client must be hand-registered through Rho's partner process by email. That is why Rho's product page says "Claude is the natively supported client today", and it means the hedge in the MCP doc is architectural, not a temporary client gap. If you are building an internal agent, a third-party MCP client, or anything Rho has not onboarded, your only option is the static token path. That is the weaker of the two credentials: long-lived (up to a year) instead of 15 minutes, no per-session consent screen, and no refresh rotation. The architecture pushes everyone except Rho's named partners onto the higher-risk credential.

Two smaller items worth a question to Rho. First, the server advertises `plain` as an acceptable PKCE method alongside `S256`, while the partner docs mandate `S256`. A client that picks `plain` gets no meaningful PKCE protection. Second, `implicit`, `client_credentials` and device code grants are advertised by a finance authorization server and documented nowhere on `docs.rho.co`. Neither is exploitable on its own, and both are the sort of thing worth confirming before a security review signs off.

### 7.7 Claude Code setup, and the secret-hygiene problem in the published command

This is the only code snippet on the entire MCP documentation page, reproduced verbatim from `docs/v1/mcp`:

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

The docs then say to run `/mcp` inside Claude Code to confirm the server is connected.

The command is correct and it works. The problem is `--scope project`.

Observed, with Claude Code 2.1.252. Running that command in an empty directory with a placeholder token produces exactly one file, at the project root:

```bash
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer rhobat_FAKETOKEN_FOR_TEST"
# Added HTTP MCP server rho-api with URL: https://rhoapi.rho.co/mcp/v1 to project config
# File modified: <cwd>/.mcp.json

cat .mcp.json
```

```json
{
  "mcpServers": {
    "rho-api": {
      "type": "http",
      "url": "https://rhoapi.rho.co/mcp/v1",
      "headers": {
        "Authorization": "Bearer rhobat_FAKETOKEN_FOR_TEST"
      }
    }
  }
}
```

The token is stored in plaintext. `.mcp.json` is Claude Code's project-scoped config, which by design is checked into version control and shared with the team. Claude Code says so itself: `claude mcp get rho-api` reports `Scope: Project config (shared via .mcp.json)` (observed).

> **Divergence:** Rho's own authentication guide says, verbatim, "Store tokens in a secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, 1Password, etc.), never in source control, CI logs, or shared documents." The only snippet on Rho's MCP page writes a long-lived `rhobat_` bearer token, valid for up to a year and carrying every scope it was minted with, into `.mcp.json`, the file whose entire purpose is to be committed and shared (observed, above). Two Rho documentation pages contradict each other, and the one with the copy-paste command is the one that loses. A token that reaches a git history is effectively permanent: it survives `git rm`, it is on every clone and every CI runner, and Rho provides no way to detect that it leaked, only to revoke it once you find out.

The blast radius is worth stating plainly. That token reads every account balance, the entire transaction ledger for all time with employee and cardholder attribution, every statement PDF, every card's limits and controls, and every invoicing customer's name, email and postal address. It is not scoped to a repo, a user, or a session. Anyone with read access to the repository has it.

#### Safer alternatives

Claude Code expands `${VAR}` in MCP config values from the process environment at connect time. Verified empirically: a config header written as `"Authorization": "Bearer ${RHO_TEST_TOKEN}"` arrived at a local capture server as `Authorization: Bearer EXPANDED_OK` when the variable was exported (observed, local HTTP server logging inbound headers during `claude mcp list` health check). So the reference can stay in the shared file while the secret never does.

| Option | Command | Where the secret lives | Use when |
| --- | --- | --- | --- |
| User scope, real token | `claude mcp add --scope user ...` with the literal token | `~/.claude.json`, outside every repo, per machine | Single developer, no sharing needed |
| Local scope, real token | `claude mcp add --scope local ...` (the CLI default) | `~/.claude.json` keyed to the project path, outside the repo | Same, but you want it only in this project |
| Project scope, env reference | `claude mcp add --scope project ...` with `${RHO_API_TOKEN}` | Nothing committed. The secret is in the shell environment, sourced from a secret manager | Team config you intend to commit |
| Linked app OAuth | Claude connector directory, not Claude Code | Nothing on disk. 15-minute access tokens | Rho-onboarded clients only. See section 7.6 |

The project-scope variant that does not leak, safe to commit:

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header 'Authorization: Bearer ${RHO_API_TOKEN}'
```

Note the single quotes: they stop your shell from expanding `${RHO_API_TOKEN}` at add time, so the literal placeholder is what lands in `.mcp.json`. Claude Code resolves it at connect time instead. Then load the value from a secret manager into the environment, for example:

```bash
# 1Password CLI
export RHO_API_TOKEN="$(op read 'op://Engineering/Rho API token/credential')"

# or AWS Secrets Manager
export RHO_API_TOKEN="$(aws secretsmanager get-secret-value \
  --secret-id rho/api-token --query SecretString --output text)"

claude
```

The user-scope variant, for a single developer who does not want the config in the repo at all:

```sh
claude mcp add --scope user --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer $RHO_API_TOKEN"
```

Whichever you choose, add `.mcp.json` to `.gitignore` if you use the literal-token form anywhere, and run a secret scanner on the repository. `rhobat_` is a distinctive, greppable prefix, which makes both leak detection and pre-commit blocking straightforward:

```bash
# pre-commit guard: refuse any staged file containing a Rho token
git diff --cached -U0 | grep -nE 'rhobat_[A-Za-z0-9]{16,}' \
  && { echo "Rho API token in staged changes, aborting"; exit 1; }

# audit an existing history
git log -p --all | grep -nE 'rhobat_[A-Za-z0-9]{16,}' | head
```

If a token has already reached a shared repository, rotating the file is not enough. Revoke it in Rho (Settings, then API, then Access Tokens), mint a replacement, and treat the old one as compromised. Revocation is immediate with no grace period, per the authentication guide.

### 7.8 What the server exposes, and what the docs will not tell you

Official docs, the complete treatment, verbatim: "The MCP server exposes Rho API tools, prompts, and resources. You can use your MCP client like Claude Code or MCP Inspector to inspect all available capabilities."

That is the whole section. Rho publishes no tool names, no input or output schemas, no prompt names, no resource URIs, and no tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`).

> **Divergence:** The versioning guide makes an unusually strong promise, verbatim: "Tool names derive from the frozen `v1` operationIds, so tool names will never change. You can reference them explicitly in workflows, agent skills, and saved automations without them breaking." Rho guarantees the permanence of identifiers it never prints. You cannot hardcode a tool name in an agent skill from the documentation, because the documentation contains no tool names, and the operationId-to-tool-name transform (prefix, separator, casing, namespace) is unpublished. The guarantee is real but unusable until you connect and run `tools/list` yourself. The missing annotations matter more: `readOnlyHint` is exactly the metadata a client would need to enforce Rho's read-only promise mechanically, rather than trusting it.

The inventory is nonetheless reconstructable with high confidence from two contract statements, both official: "The MCP server is 1:1 with the REST API", and tool names derive from the frozen `v1` operationIds. The v1 REST surface is 14 operations, all GET. See "The resource model" and "Endpoint reference" for the full schemas.

| # | REST operation | Method and path | Required scope |
| --- | --- | --- | --- |
| 1 | List accounts | `GET /accounts` | `accounts:read` |
| 2 | Get account | `GET /accounts/{account_id}` | `accounts:read` |
| 3 | List cards | `GET /cards` | `cards:read` |
| 4 | Get card | `GET /cards/{id}` | `cards:read` |
| 5 | List transactions | `GET /transactions` | `transactions:read` |
| 6 | Get transaction | `GET /transactions/{id}` | `transactions:read` |
| 7 | Get transaction file | `GET /transactions/{transaction_id}/files/{file_id}` | `transactions:read` |
| 8 | List statements | `GET /statements` | `statements:read` |
| 9 | Get statement | `GET /statements/{id}` | `statements:read` |
| 10 | List invoicing customers | `GET /invoicing/customers` | `invoicing:read` |
| 11 | Get invoicing customer | `GET /invoicing/customers/{customer_id}` | `invoicing:read` |
| 12 | List invoicing invoices | `GET /invoicing/invoices` | `invoicing:read` |
| 13 | Get invoicing invoice | `GET /invoicing/invoices/{invoice_id}` | `invoicing:read` |
| 14 | Get invoicing invoice file | `GET /invoicing/invoices/{invoice_id}/files/{file_id}` | `invoicing:read` |

So, inferred: 14 tools, zero write tools, six list tools with rich filters, six single-object getters, two signed-URL file fetchers. Prompts and resources are asserted to exist and are entirely undocumented, which means you cannot know, before connecting a finance account, what content the server will inject into the model's context. Enumerate them on first connect and record the result, because it is the only inventory you will have.

Other undocumented MCP mechanics, all absences you should test for rather than assume:

- Whether an MCP `tools/call` consumes the same per-token budget of approximately 60 requests per minute (see "Rate limits"). No MCP-specific limit is published, and no `X-RateLimit-*` response headers appear on any response this research could capture (observed on sandbox REST 200s and on the production MCP 401 and metadata responses), so a client cannot see remaining quota before a 429.
- Whether the server paginates on the agent's behalf or hands `page_token` cursors to the model. Cursors are bound to the exact endpoint, filters and sort order, and changing any of them mid-walk returns `400` (see "Pagination"). An agent that refines its query mid-iteration restarts from scratch.
- The JSON-RPC error code mapping for the REST 401, 403 and 429 model.
- Session semantics, stream lifetime, keepalives and timeouts.
- Any configuration for a client other than Claude Code. There is no `claude_desktop_config.json` block, no Cursor, VS Code, ChatGPT or Codex CLI example anywhere in Rho's documentation.

### 7.9 Security: what an agent connected to Rho can and cannot do

#### The capability boundary

The read-only property is structural, not a policy setting, and that distinction is what makes it worth something. There is no non-GET operation anywhere in the v1 surface to call, and there is no `*:write` scope anywhere in the live protected-resource metadata to request (observed, section 7.5). Rho describes four independent enforcement layers, and all four are verifiable rather than taken on trust:

1. Surface: 14 operations, all GET. Nothing to POST.
2. Scope: all five scopes are `*:read`. No writable scope exists to grant.
3. Role: only Account Owners and Admins can mint a token or authorize an OAuth grant, behind 2FA.
4. Credential: mandatory expiry capped at one year, 45-day inactivity expiry, 20 active tokens per business, optional 100-entry IP allowlist, immediate irreversible revocation.

| An agent connected to Rho CAN | An agent connected to Rho CANNOT |
| --- | --- |
| Read every account: type, display name, balance in minor units, masked account and routing last 4 | Initiate any payment: ACH, wire, international wire, check, internal transfer, bill pay |
| Read the entire transaction ledger across every rail, filtered by account, type (33 values), status, user, card, free-text search, date windows and amount bounds | Approve, reject, reschedule or cancel anything in the approvals queue |
| See per-employee (`user_id`, `user_full_name`) and per-card (`card_id`, `card_name`) attribution on spend | Create, issue, lock, unlock, cancel or modify a card, or change any limit or MCC rule |
| Read ACH NACHA trace numbers and wire IMAD/OMAD via `tracking_number` (MT103 references are explicitly not returned) | Add, remove or modify users, roles or permissions |
| Read `memo` (bank or provider supplied) and `note` (user or system annotation) free text | Change any account setting, including 2FA, alerts or debit controls |
| See which transactions sit in `awaiting_approval` | Create, edit, send, cancel or mark-paid an invoice, or create or edit an invoicing customer |
| Read every card including cancelled and expired: limits, limit type, current and pending spend, spend and usage windows, billing and shipping addresses, MCC allow and block lists | See a full PAN, CVC or expiration date. The cards guide states, verbatim: "Only the last four PAN digits are returned; full card numbers, CVCs, and expiration dates are not available through these endpoints" |
| Read statements with opening and closing balances, total credits, debits and fees, and for credit statements repayment date, spending, repayments and cashback | Write a note, memo, label, department or receipt back to a transaction |
| Read invoices and invoicing customers, including customer legal name, email, cc emails, full postal address and total revenue | Trigger an accounting sync |
| Fetch short-lived signed URLs for statement PDFs, transaction attachments and invoice PDFs | Receive a webhook or push event. There are none, so it must poll |
| Do all of this identically over REST or MCP | Reach more than one Rho business per connection |

The help center states the prohibitions verbatim: connected AI tools cannot "Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account", and "AI connections are read-only and cannot perform actions on your behalf." Rho's product page footnote adds: "The Rho API is read-only today."

Rho's own framing, "a leaked token cannot move money", is accurate as of 2026-09. That is a genuinely strong position and it is unusual among banking APIs: by Rho's own competitive research, Mercury, Brex and Ramp all expose write operations through their APIs.

#### Why read-only materially lowers the risk but does not eliminate it

Read-only removes the catastrophic outcome (an agent wiring money to an attacker) and leaves five real ones.

**1. The data itself is the asset.** Five scope checkboxes hand a third-party LLM client a complete financial picture of the business and a partial PII picture of its counterparties: every vendor and customer the company transacts with, per-employee spend, cardholder names and home-or-office billing addresses, masked account and routing numbers, payment trace identifiers, full statement PDFs, and, through Invoicing, the legal names, email addresses, cc lists and postal addresses of the business's own customers. That last category is third-party PII: data about people who never agreed to have it processed by your AI vendor. A live sandbox record shows the shape (observed, `GET https://rhoapi-sandbox.rho.co/api/v1/invoicing/customers`):

```json
{
  "legal_name": "Orbit Media Group",
  "email": "accounts@orbitmedia.co",
  "cc_emails": ["billing@orbitmedia.co", "cfo@orbitmedia.co"],
  "address": {
    "address1": "77 Broadway", "city": "Boston",
    "state": "MA", "zip_code": "02109", "country": "USA"
  },
  "total_revenue": { "amount": 0, "currency": "USD" }
}
```

Connecting this to an LLM client is a data-processing decision with contractual and, depending on jurisdiction, regulatory consequences. Neither Rho's help center nor its MCP doc frames it that way, and neither `rho.co/security` nor `rho.co/trust` mentions AI, LLMs, MCP, tokens or agents at all.

**2. Prompt injection through the ledger.** `memo`, `note`, `counterparty_name`, invoice fields, customer `note` and the contents of attached PDFs are all text that flows verbatim into a model's context, and much of it is attacker-influenceable. Anyone who can send the business a one-cent ACH, issue it an invoice, or be paid by it can plant instructions in a field a finance agent will read. A live sandbox transaction shows `memo` and `note` arriving as free text alongside the numbers (observed, `GET /api/v1/transactions`):

```json
{
  "transaction_type": "credit_repayment",
  "amount": { "amount": 1750, "currency": "USD" },
  "counterparty_name": "Cash (Checking)",
  "memo": "Daily credit repayment for date 2026/06/24",
  "note": "Daily credit repayment for date 2026/06/24",
  "user_full_name": "...",
  "attachments": [
    { "file_id": "7de7495f-...", "file_name": "repayment-confirmation.pdf" }
  ]
}
```

Rho's tools cannot act on injected instructions, because they are all reads. The agent's *other* tools can. A finance agent typically also has email, Slack, a shell, a filesystem, a GitHub token, or a write-capable MCP server from a different vendor. The read-only boundary protects Rho, not your environment. Rho's documentation contains zero mentions of prompt injection, content sanitisation, provenance marking or untrusted-content handling, and its own published MCP safety checklist for finance teams (covering scopes, rotation, IP allowlists, approval gates, idempotency, audit logs, webhook signatures and output validation) never names injection either. This is the largest unaddressed risk on the surface.

**3. Signed URLs are unauthenticated bearer links.** The transactions guide instructs clients to follow a download URL "straight away, without an Authorization header". Any such URL that lands in a chat transcript, a log line, a screenshot or a shared conversation is a live credential to a statement or receipt for its lifetime. Statement `pdf_url` values are documented as valid up to 15 minutes. No TTL is published at all for transaction and invoice file URLs, only "short-lived". Agent transcripts are exactly the kind of artifact that gets pasted into tickets and shared with colleagues.

**4. Rate limits are not an exfiltration control.** Approximately 60 requests per minute per token, at up to 100 rows per page, is up to 6,000 transaction rows per minute. A curious, misconfigured or compromised agent can drain the full ledger in minutes, and nothing documented detects or alerts on that access pattern.

**5. The safety property is explicitly temporary, and the versioning policy does not protect it.** Rho's launch blog, verbatim: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval, the finance tasks you'd rather delegate." The changelog says "Read-only is live today. Write access and webhooks are next." Read that against the versioning policy in section 6.4: the MCP contract is additive-only, and additions are by definition non-breaking. Write tools could therefore appear inside `/mcp/v1` without a version bump, and the 15-day notice policy covers deprecations and sunsets, not capability additions. Any approval you obtain today on the strength of "it cannot move money" should be written with an expiry and a re-review trigger.

> **Divergence:** Rho markets IP allowlisting as a primary control for AI connections, pairing "connect Claude" with "optional IP allowlists" on the same pages. The control does not fit the use case it is being sold against. A developer laptop roams between office, home and coffee shop, and a hosted client such as claude.ai egresses from the vendor's infrastructure, not yours. The allowlist is genuinely useful for a warehouse sync job on a fixed NAT gateway and close to useless for an interactive AI client. Pairing the two invites a false sense of control. The allowlist still belongs in your design, but on the server-side integration token, not on the one a laptop or a SaaS client uses.

> **Divergence, audit:** Nothing in Rho's documentation, help center or API describes a log of which tool an agent called, when, from where, or how much data it pulled. There is no audit API, no per-connection activity view, and no documented "last used" timestamp on tokens beyond the mechanic that 45 days of inactivity expires them. Rho's own safety checklist tells finance teams to "preserve agent and API logs for every action taken", and Rho provides no surface on which to do so. For a regulated finance function, "we cannot show what the agent read" is a material gap, and it is the one to raise first with Rho. Until it closes, your logs are the only logs, which is why section 7.9's controls put the egress proxy ahead of everything else.

One more operational gap worth knowing: `status.rho.co` lists five components (Web Application, Mobile Application, Corporate Cards, Bank Payments, Notifications). There is no API component and no MCP component, so an agent workflow depending on `/mcp/v1` has no public health signal.

#### Controls

Ordered by how much risk each removes per unit of effort.

| # | Control | Concretely | Removes |
| --- | --- | --- | --- |
| 1 | Scope minimisation | Mint the token with only the scopes the workload needs. `transactions:read` alone for a burn dashboard. Never grant `invoicing:read` or `cards:read` unless the agent's job requires customer PII or cardholder data | The majority of the PII and third-party-data exposure, since Invoicing and Cards carry most of it |
| 2 | Dedicated token per client | One token per agent, per environment, per person if the client is interactive. Never one shared "AI token". Name it after the consumer so the token list is self-documenting | Turns revocation into a surgical action rather than an outage, and makes the 45-day inactivity clock a useful signal of an unused credential |
| 3 | Keep the secret out of the repo | Use `--scope user`, or `--scope project` with `${RHO_API_TOKEN}` sourced from a secret manager. Add a `rhobat_` pre-commit guard and a repository secret scan (section 7.7) | The leak path that Rho's own published command creates |
| 4 | IP allowlist where it actually applies | Set an allowlist (up to 100 entries) on tokens used by server-side jobs on fixed egress. Do not pretend it protects a laptop or a hosted client | Server-token theft. Explicitly not interactive-client risk |
| 5 | Short expiry and scheduled rotation | Expiry is mandatory and capped at one year. Choose 30 to 90 days instead. Rotate overlap-style: mint the replacement, deploy it, verify, then revoke the old one, because revocation is immediate with no grace period | The window during which a leaked token stays useful |
| 6 | Egress monitoring and volume alerting | Route agent traffic through a proxy you control, and alert on request volume, on any `403` (a scope or IP violation, which is the signature of a token being used outside its intended job), and on file-download calls. Rho publishes no audit surface, so this is the only place you will see this | The undetected bulk-read. Without it you have no detection story at all |
| 7 | Treat all Rho text as untrusted input | In agent prompts, fence `memo`, `note`, `counterparty_name`, invoice and customer fields and PDF contents as data, never as instructions. Do not co-mount a write-capable tool (email, Slack, shell, payments) in the same agent as the Rho reader unless every write is human-gated | Prompt injection escalating through the agent's other tools |
| 8 | Prefer the linked-app OAuth path when it is available | If your client is Rho-onboarded, OAuth gives 15-minute access tokens, per-session consent, single-use rotating refresh tokens, and revocation from Settings, then API, then Linked Apps. Section 7.6 explains why this is not available to everyone | Long-lived-credential risk, for the minority of clients that can use it |
| 9 | Never persist signed URLs | Fetch, download, discard. Scrub `download_url` and `pdf_url` from agent transcripts and logs | Statement and receipt links leaking through shared transcripts |
| 10 | Write the approval with an expiry | Record that read-only is Rho's current posture, not a contractual guarantee, and re-review when write tools ship. Set a calendar reminder rather than trusting a changelog | Silent capability expansion inside `/mcp/v1` under the additive-only policy |

A workable evaluation sequence given that there is no MCP sandbox: build and test everything you can against the REST sandbox (see "Sandbox and test data"), then mint one production token with a single scope and a 30-day expiry, IP-allowlisted to your workstation's egress if it is stable, run `initialize` and `tools/list` to capture the real tool, prompt and resource inventory, record it, and revoke the token the same day. Only then decide which scopes the long-lived integration actually needs.

### 7.10 Open questions for Rho

These are the items a security or architecture review will ask about and the documentation cannot answer.

| # | Question |
| --- | --- |
| 1 | What are the literal MCP tool names, and what is the transform from operationId? The contract freezes them and never prints one |
| 2 | What prompts and resources does the server expose, and are statement and invoice PDFs exposed as MCP resources? |
| 3 | Do MCP tool calls consume the same 60-requests-per-minute token budget, or is there a separate MCP budget? |
| 4 | Does the server paginate on the agent's behalf, or does the agent drive `page_token` cursors itself? |
| 5 | What is `server/discover`, and where is it specified? |
| 6 | Is there any audit log of MCP tool calls available to the customer, and does an MCP call reset the 45-day inactivity clock? |
| 7 | Will write tools appear inside `/mcp/v1` under the additive-only policy, and will customers be notified before an existing agent connection gains write capability? |
| 8 | What is the TTL on transaction and invoice file download URLs? Statements are documented at 15 minutes, the others only as "short-lived" |
| 9 | Is an MCP sandbox planned? |
| 10 | Is dynamic client registration planned for `auth.rho.co`, or is the linked-app path permanently limited to hand-registered partners? |
| 11 | Why does the MCP 401 emit `"type":"2"` instead of an RFC 9457 type URI, and when will the MCP error contract match the documented REST one? |
| 12 | Are the advertised `client_credentials`, `implicit` and device-code grants enabled for the Rho API audience, and why is `plain` PKCE advertised when the docs mandate `S256`? |
## 8. Building on it

Everything below assumes the contract established earlier in this document: fourteen `GET` operations, six list endpoints, opaque-in-intent cursors, a documented budget of roughly 60 requests per minute per token, and no push channel of any kind. This section is about the consequences for code you have to run in production.

The shape of the problem, stated once: **you are building a read-only mirror of somebody else's ledger, by polling, with no change feed, no totals, no conditional requests, and no way to be notified that anything happened.** Every design decision here follows from that.

### 8.1 The constraints that actually drive the design

| Constraint | Evidence | What it forces |
| --- | --- | --- |
| No webhooks, no events, no subscriptions | `GET /webhooks`, `/events`, `/subscriptions` all return `404 page not found` (plain text, Go router). No such concept appears anywhere in the docs corpus. | Poll. Your data freshness floor is your poll interval. |
| No `updated_at` on the banking resources | Accounts, cards, transactions and statements carry no `created_at` or `updated_at` at all. Only `invoicing/customers` and `invoicing/invoices` do, and neither is filterable. | You cannot ask "what changed". You must re-read windows and diff client-side. |
| No `updated_after` filter anywhere | Transactions expose `initiated_after/before` and `posted_after/before` only. No guide offers a change-based filter on any resource, and nothing in the docs acknowledges the gap. | Your watermark has to be a business timestamp, which is not monotonic with respect to change. |
| No `ETag`, `Last-Modified`, `Cache-Control` | Observed: `If-None-Match: *` and `If-Modified-Since` in both directions all return a full `200` with the complete body. `cf-cache-status: DYNAMIC` on 249 of 249 API responses. | There is no cheap "has anything changed" probe. Every poll pays full payload cost. |
| `HEAD` returns `405 allow: GET` | Observed: `curl -I https://rhoapi-sandbox.rho.co/api/v1/accounts` returns `405`. | Liveness checks and existence probes must be real `GET`s. |
| No `total_count`, no `has_more`, no `Link` header | The `page` object has exactly one field, `next_page_token`. | You cannot size a result set without draining it, and you cannot show "1-20 of 347". |
| Five of six list endpoints use an offset cursor | Decoded tokens: `{"v":1,"f":"…","t":base64("offset:20")}` on cards, transactions, statements, invoicing customers and invoicing invoices. Only `/accounts` carries a keyset payload (`{"last_id":…,"sort_by":"account_name","order":"asc"}`). | A long walk over live data can skip or duplicate rows. You need a dedupe key and a periodic full sweep. |
| ~60 req/min per token, ~600 req/min per source IP | Documented in `docs/v1/rate-limits`. Not enforced in sandbox (observed: 150 requests on one token in a 57-second window, zero `429`; 68.9 req/s instantaneous, zero `429`). | Build to the documented budget, not the sandbox's tolerance. The per-IP pool is shared across all your tokens. |
| Read-only | All 14 operations are `GET`. Every write method on every path returns `405` with `allow: GET`, and that `405` is emitted **before** authentication (observed: `POST /accounts` with no `Authorization` header returns `405`, not `401`). All five OAuth scopes end in `:read`. | Nothing you build can move money, issue a card, or annotate a record. |

> **Divergence:** The pagination guide states, unqualified: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." Five of the six list endpoints return a bare absolute offset inside the cursor, which cannot deliver that guarantee: an insert positioned before the current offset shifts every subsequent row. Only `/accounts` uses a keyset cursor that structurally can. The sandbox dataset is static so the failure cannot be forced there, but the mechanism is dispositive. Treat the anti-skip and anti-duplicate promise as false for `/transactions`, `/statements`, `/cards`, `/invoicing/customers` and `/invoicing/invoices`. See also the Pagination section.

### 8.2 Incremental sync

#### 8.2.1 Why the obvious design is wrong

The obvious design is: keep a watermark, ask for everything after it, advance the watermark. That design is wrong here for four independent reasons, and each one alone is enough to corrupt your mirror.

**1. Rows mutate in place.** A transaction is created and then changes. `status` moves through `pending`, `settled`, `failed` and `awaiting_approval`. `posted_at` appears later. The docs are explicit that the money can change too: "The amount can shift between an initial card authorization and final clearing." There is no authorized-amount and settled-amount pair in the schema; `amount` is described as "Settled amount in account currency" even while `status` is `pending`. `note` is user-editable in the Rho web app at any time. None of these mutations moves `initiated_at`, so none of them is visible to a watermark on `initiated_at`.

**2. There is no state machine to lean on.** Quoted in full from the Transactions guide, because it is unusually candid: "`v1` does **not** guarantee that a failed transaction has an empty `posted_at`, so read the field as nullable whatever the status. Nor does `v1` guarantee a **transition order**, so reconcile on the `status` and timestamps a response actually carries rather than on an assumed progression." You may not assume `pending → settled` is terminal, and you may not assume `settled` never changes again.

**3. `posted_at` arrives arbitrarily late.** Measured across the 71 sandbox transactions that carry one: median lag is 0 seconds, 47 of 71 are exactly zero, p90 is 1 day, and the maximum is **18.23 days** (a settled `check_payment`). A row initiated on the 1st can post on the 19th. A `posted_after`-based sync window narrower than that silently drops it.

```bash
# The row with the longest observed lag
curl -s -H "Authorization: Bearer sandbox" \
  'https://rhoapi-sandbox.rho.co/api/v1/transactions?transaction_type=check_payment&page_size=100' \
  | python3 -c 'import sys,json,datetime as d
f="%Y-%m-%dT%H:%M:%SZ"
for t in json.load(sys.stdin)["transactions"]:
    if "posted_at" in t:
        lag=(d.datetime.strptime(t["posted_at"],f)-d.datetime.strptime(t["initiated_at"],f))
        print(t["id"], t["status"], t["initiated_at"], t["posted_at"], lag)'
```

**4. You cannot sync on `posted_at` instead.** It is tempting, because `posted_at` is the accounting-relevant timestamp and Rho's own daily-reconciliation recipe uses it. But any `posted_after` or `posted_before` bound excludes every row that has no `posted_at` at all, which is exactly the set of rows you most need to track.

```bash
# 72 transactions exist; a posted_at bound sees 71.
curl -s -H "Authorization: Bearer sandbox" \
  'https://rhoapi-sandbox.rho.co/api/v1/transactions?posted_after=2000-01-01&page_size=100' \
  | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["transactions"]))'
# -> 71
```

> **Divergence:** `api/transactions_listtransactions.md` says `posted_at` is "Null while status is pending". Observed in the sandbox: both `pending` rows carry a non-null `posted_at`, and the only row without one is the single `awaiting_approval` record (`019d3e86-4482-7000-8000-000000000048`). The operative rule is "absent while awaiting approval", not "absent while pending". Worse, the field is **omitted**, never `null`, so a client written to the literal doc wording (`if txn.posted_at is None`) sees a `KeyError` or an `undefined`, not a null. `docs/v1/transactions` hedges in the opposite direction ("not coupled to `status`"), so Rho's two pages disagree with each other and the reference page disagrees with the data. Verify: `GET /transactions?status=pending&page_size=100` returns two rows, both with `posted_at`.

#### 8.2.2 The filters you can actually sync on

Only a subset of the documented query surface is usable as a sync primitive. This is the working set, per endpoint.

| Endpoint | Usable sync filter | Accepted format | Boundary semantics | Notes |
| --- | --- | --- | --- | --- |
| `/transactions` | `initiated_after`, `initiated_before` | `2026-01-01` or `2026-01-01T00:00:00Z` or `…+00:00` or `…000Z` | `after` inclusive, `before` **exclusive** | The only monotonic-ish key. Does not move when a row changes. |
| `/transactions` | `posted_after`, `posted_before` | same | `after` inclusive, `before` **exclusive** | Excludes rows with no `posted_at`. Good for closing a book, useless for change detection. |
| `/statements` | `period_end_after/before`, `period_start_after/before` | **date-only**, `2026-01-01`. A timestamp form returns `400`. | `after` inclusive, `before` **exclusive** | `available_at` lags `period_end` by 1 to 8 days observed, so re-scan a trailing window. |
| `/invoicing/invoices` | `date_after/before`, `due_date_after/before` | **date-only**. Timestamp forms return `400`. | **both inclusive** | These are issue and due dates. Neither moves when an invoice's `status` changes. |
| `/invoicing/customers` | none | n/a | n/a | No date filter at all. `sort_by=created_at` is the only legal sort value; everything else is a `400`. |
| `/accounts` | none | n/a | n/a | No filters of any kind. `account_type=checking` is silently ignored and returns all rows. |
| `/cards` | none | n/a | n/a | `user_id[]`, `type[]`, `status[]` only. No dates. |

Boundary inclusivity is not uniform, and the difference is real:

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
count() { python3 -c 'import sys,json;d=json.load(sys.stdin);print(len(d[sys.argv[1]]))' "$1"; }

# transactions: after is INCLUSIVE, before is EXCLUSIVE.
# The corpus runs from 2023-05-31T07:29:00Z to 2026-06-26T19:07:02Z.
curl -s -H "$H" "$B/transactions?initiated_before=2023-05-31T07:29:00Z&page_size=100" | count transactions  # 0
curl -s -H "$H" "$B/transactions?initiated_after=2026-06-26T19:07:02Z&page_size=100"  | count transactions  # 1

# invoices: BOTH bounds inclusive. Same day on both sides still returns rows.
curl -s -H "$H" "$B/invoicing/invoices?date_after=2026-05-01&date_before=2026-05-01&page_size=100" | count invoices  # 2
```

Two traps will destroy a sync job silently, and neither is documented.

**The empty-value trap.** An empty value on any `*_before` parameter coerces to the zero time `0001-01-01T00:00:00Z`; `field < zero` is universally false, so you get `200` with an empty array. An empty `*_after` is a no-op and returns everything. A templated URL with an undefined variable therefore reports "no activity" rather than failing.

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
curl -s -H "$H" "$B/transactions?posted_before=&page_size=100"
# {"page":{"next_page_token":null},"transactions":[]}
```

Build query strings conditionally and refuse to emit an empty value. The reference client below raises on this rather than sending it.

**The unvalidated-enum trap.** `/cards` validates `type` and `status` and returns `400` on a bad value. `/transactions`, `/statements` and `/invoicing/invoices` do not: they accept any string and return `200` with zero rows. `status=Settled`, `status=posted`, `account_type=treasury` and `status=canceled` (the invoice enum is `cancelled`, two Ls) all look like working queries that found nothing.

> **Divergence:** `docs/v1/pagination` says only that "Values outside the allowed range return `400 Bad Request`", and every filter is documented with an enum. In practice enum validation is present on `/accounts` and `/invoicing/customers` (`sort_by`, `order`), present on `/cards` (`type`, `status`), and entirely absent on `/transactions`, `/statements` and `/invoicing/invoices`. Validate enums client-side; the server will not tell you. See the Filters section for the full per-endpoint matrix.

Corollary for operations: **`200 []` is ambiguous** between "no matching data" and "your filter was silently dropped". Whenever a filtered query returns empty, assert against an unfiltered control query before concluding anything.

#### 8.2.3 The design: three lanes

Because no single query answers "what changed", correct sync is three overlapping passes with different cadences. Each one covers a failure mode the others miss.

| Lane | Query | Catches | Misses | Cost per run |
| --- | --- | --- | --- | --- |
| **A. New rows** | `initiated_after = watermark - skew`, walked to `null` | Anything newly initiated since last poll | Mutations to older rows; backdated inserts | `ceil(new/100)`, normally 1 request |
| **B. Open-row re-read** | `GET /transactions/{id}` for every row you last saw as `pending`, `awaiting_approval`, or missing `posted_at` | `pending → settled`, amount revision, late `posted_at` | Changes to rows you never saw as open | 1 request per open row |
| **C. Trailing window** | `initiated_after = now - 35d`, walked to `null` | Backdated inserts, any mutation inside the window, offset-cursor skips inside the window | Anything older than the window | `ceil(window_rows/100)` |
| **D. Full sweep** | unfiltered walk to `null` | Everything, including a row an offset cursor skipped months ago | Nothing, but it is expensive | `ceil(total/100)` |

Lane C's 35-day width is not arbitrary: it is roughly double the longest `posted_at` lag observed in the corpus (18.23 days), with headroom. Widen it if your own production data shows longer tails, and measure that directly rather than trusting this number.

**Do not pick an `initiated_after` floor for lane D.** The sandbox corpus spans 2023-05-31 to 2026-06-26, three years, and a naive "last 3 years" horizon drops the two oldest rows. Walk `/transactions` with no date filter at all. If that walk is too expensive, partition it by `account_id` (which is a real, honored filter) rather than by date.

**The watermark must be a `initiated_at` value you actually observed, not your wall clock.** There is no server-supplied cursor, no `created_at`, and no guarantee that a row initiated at T becomes visible at T. Advancing to `max(initiated_at)` and re-scanning from `max - skew` on the next run is correct only because lanes B, C and D exist behind it.

**Every page of a walk must send the byte-identical query string.** The cursor is bound to a fingerprint of the literal filter spelling, not its meaning. `order=asc` then `order=ASC` returns the same rows but invalidates the token. `status=settled` then `status=settled&status=settled` likewise. Changing `page_size` mid-walk is safe (`page_size` is deliberately excluded from the fingerprint), but there is no reason to.

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
# The token survives a changed page_size and dies on a changed filter.
T=$(curl -s -H "$H" "$B/transactions?page_size=5" | python3 -c 'import sys,json;print(json.load(sys.stdin)["page"]["next_page_token"])')
curl -s -o /dev/null -w '%{http_code}\n' -H "$H" "$B/transactions?page_size=37&page_token=$T"          # 200
curl -s                              -H "$H" "$B/transactions?page_size=5&page_token=$T&status=settled"
# {"type":"1317","title":"page_token must be a valid cursor","status":400}
```

Handle that `400` mid-walk by restarting the walk from page 1, not by aborting. Your dedupe key makes the repeat harmless.

#### 8.2.4 Cadence against the budget

The documented budget is approximately 60 requests per minute per token and approximately 600 per minute per source IP, with the explicit pacing advice "pace traffic steadily below one request per second". Read literally, your sustained ceiling is under 60/min, so size against **0.9 req/s = 54 req/min = 77,760 req/day**.

Worked example: a business posting 300 transactions per day, with roughly 30 rows open at any moment, and 330,000 rows of history.

| Lane | Cadence | Requests per run | Requests per day | Wall time per run at 0.9 rps |
| --- | --- | --- | --- | --- |
| A | every 5 min | 1 | 288 | 1 s |
| B | every 5 min | 30 | 8,640 | 33 s |
| C | hourly | `ceil(35 x 300/100)` = 105 | 2,520 | 117 s |
| D | weekly | `ceil(330000/100)` = 3,300 | 471 amortised | 61 min |
| **Total** | | | **~11,900** | **15% of budget** |

Backfill arithmetic, at `page_size=100` and 0.9 req/s:

| Rows | Requests | Elapsed |
| --- | --- | --- |
| 10,000 | 100 | 1.9 min |
| 100,000 | 1,000 | 18.5 min |
| 1,000,000 | 10,000 | 3.1 h |

A million-row backfill consumes a token's entire budget for three hours. Run backfills on a **separate API Access Token** so steady-state sync is not starved. Note that separate tokens do not buy you separate IP budgets: the ~600 req/min per-source-IP ceiling is shared across every token behind that egress address, including other teams' integrations.

Two transport facts change these numbers materially, both observed:

- **Always send `Accept-Encoding: gzip` explicitly.** Only gzip is served. Brotli, zstd, deflate and the wildcard `*` are all declined and return the full payload. On a 40,768-byte transactions page, gzip cuts the wire to about 5.6 KB, a 7.2x saving.
- **Reuse connections, but do not over-multiplex one.** Keep-alive halves effective latency (cold total p50 206 ms vs warm server TTFB p50 112 ms). Multiplexing 50 streams onto a single HTTP/2 connection made per-request p50 13x worse (1,504 ms) for only 31 req/s aggregate. A small pool of connections with modest per-connection concurrency beats the usual HTTP/2 advice here.

Budget approximately 90 to 145 ms of server time per call from a US East client, plus 70 to 100 ms of connect and handshake when cold, with a rare ~1 s tail. Payload size is not a latency driver.

#### 8.2.5 Syncing the other resources

| Resource | Strategy | Why |
| --- | --- | --- |
| `/accounts` | Full walk every poll (14 rows in sandbox; small everywhere). No filters exist. | Balances are the only volatile field and there is no way to ask for changed ones. |
| `/cards` | Full walk every poll. | No date filters. Spend windows (`spend_period_start/end`, `current_spend`) are recomputed per request against the real clock, so cards look "changed" constantly. |
| `/statements` | `period_end_after = last_period_end - 60d`, dedupe on `id`. | `available_at` lags `period_end` by 1 to 8 days observed, so a statement appears after its period closes. |
| `/invoicing/invoices` | Full walk every poll. | `date`/`due_date` filters do not move when `status` or `accounting_sync_status` changes, so they are useless for change detection. No `customer_id` filter either. |
| `/invoicing/customers` | Full walk every poll, with `include_deleted=true` if you need soft-deleted records. | No date filter of any kind. |

**Exclude signed URLs from your change fingerprint.** `statements[].pdf_url` is a Google Cloud Storage V4 signed URL that is re-signed roughly every 300 seconds. If `pdf_url` is part of what you diff, every statement will look changed on most polls. The same applies to `download_url` from the file endpoints, although those never appear on a resource record (transaction responses carry only `attachments[].file_id` and `file_name`, never a URL).

> **Divergence:** `api/statements_getstatement.md` says "If the link lapses, re-fetch the statement with `GET /statements/{id}` to obtain a fresh URL." Observed: `pdf_url` is served from a server-side signing cache keyed on the **PDF blob**, not the statement, with a TTL of about 300 s (re-sign intervals of 302 s and 313 s measured across three epochs). Re-fetching inside that window returns a byte-identical URL. You cannot force a re-sign. In practice the cache rotates roughly 10 minutes before the 899-second expiry, so a genuinely dead URL has usually already been replaced, but not by the mechanism the docs describe. The observed residual life band is 599 to 899 seconds. Transaction file `download_url` values, by contrast, are minted fresh on every request with a full 899 s window. Parse `X-Goog-Date + X-Goog-Expires` out of the URL to know its deadline without a network call.

### 8.3 Idempotency and reconciliation

#### 8.3.1 The primary key is `(id, account_id)`, never `id`

This is the single most important storage decision, and Rho states it plainly in the Transactions guide: "Do not assume `id` is unique per row, though: the entries of a single money movement can share an `id`, so a warehouse keyed on `id` alone **silently drops a leg**. Either key on `id` together with the fields that distinguish entries of the same movement, such as `account_id`, or group on `money_movement_id` and treat the movement as your unit."

The existence of an optional `account_id` query parameter on `GET /transactions/{id}` is the corroborating evidence: the endpoint would not need a disambiguator if `id` were unique.

> **Divergence:** The sandbox cannot exercise the collision. All 72 transaction ids are distinct, `(id, account_id)` yields the same 72 distinct keys, and the seven two-leg money movements all carry **different** ids on each leg (for example movement `…000000000002` has legs `019f0143-3ea0-…000002` and `…000003`). So the documented hazard is real per the contract and untestable per the fixtures. Key on `(id, account_id)` anyway. Additionally, the transaction-file reference page states "A transaction `id` identifies one transaction", directly contradicting the same product's `id` definition, and `GET /transactions/{id}/files/{file_id}` has no `account_id` disambiguator at all, so if ids ever do collide the file lookup has no way to say which leg it means.

#### 8.3.2 Money movements, not transactions, are the accounting unit

65 distinct `money_movement_id` values cover the 72 sandbox transactions. Seven movements have exactly two legs, and in every one of them **the two legs sum to zero**: an internal transfer of 123,987 minor units appears as `-123987` on Cash (Checking) and `+123987` on Reserve Checking. A credit repayment of 1,658,253 appears as `-1658253` on checking and `+1658253` on the credit account.

If you post both legs to a general ledger as independent events, you double-count every internal transfer and every credit repayment. Group on `money_movement_id` and decide once, per movement, what the accounting event is.

Leg order within a movement carries no meaning. Movements `…21` and `…27` are both `internal_transfer` between the same two accounts with **opposite polarity** in the leg array. Only the per-leg `account_id` and sign are load-bearing.

There is **no `money_movement_id` filter** on `/transactions`, despite the docs telling you to "group on it to treat the entries of one movement as a unit". You cannot fetch the sibling legs of a movement by its id. You must page a date window wide enough to contain all legs and group client-side. Leg timestamps within a movement were identical to the millisecond in 5 of 7 sandbox cases and differed by 1 ms in the other 2, so a window of seconds is sufficient in practice, but nothing guarantees the legs settle together. There is no sandbox example of a movement whose legs have different statuses, so half-settled transfers are untested surface.

#### 8.3.3 What can change under you, and what cannot

| Field | Changes after first sight? | Handling |
| --- | --- | --- |
| `id`, `money_movement_id`, `account_id`, `account_type`, `initiated_at`, `transaction_type` | No (assumed stable; the docs call `id` "stable across re-fetches") | Safe to key and partition on. |
| `status` | Yes, in any direction; no transition order guaranteed | Store current value plus a history row. Never assume terminality. |
| `posted_at` | Yes, appears late; up to 18.23 days after `initiated_at` observed | Nullable and **omitted, not null**, when unset. |
| `amount.amount` | Yes, documented: "can shift between an initial card authorization and final clearing" | Store the current value plus the prior one. Do not post to a GL until the row is `settled` unless you are prepared to reverse. |
| `note` | Yes, user-editable in the Rho app | Exclude from accounting logic, include in your change fingerprint if you surface it. |
| `memo` | Documented as bank-supplied and read-only | Treat as stable, but see the divergence below. |
| `attachments[]` | Yes, new attachments can appear | `(transaction_id, file_id)` is the key; `file_id` is not unique per transaction. |
| `account_name`, `card_name`, `user_full_name` | Denormalized copies; can drift from the source | Do not join on them. `account_name` is not unique: "Cash (Checking)" appears twice, "Credit Account" four times. |

> **Divergence:** `docs/v1/transactions` distinguishes `memo` ("supplied by a bank or payment provider", not user-editable) from `note` ("a user or system annotation", editable). Observed: `memo` and `note` are present or absent strictly together (39 of 72 have both, 33 have neither) and are **byte-identical on 37 of the 39**. The only two that differ are failed ACH rows, where `note` is `memo` plus `", Error: Invalid receiving routing number."` The sandbox effectively models them as one field, so you cannot use it to test code that depends on the distinction.

**Rows never disappear.** Failed transactions "remain queryable for audit purposes", and canceled and expired cards stay in the unfiltered card list "so their stable IDs can still be joined to historical transactions". So a row vanishing from your sync is a bug in your sync, not a delete, with one exception: an offset cursor can skip a row mid-walk while the underlying data shifts. That is precisely what the periodic full sweep is for. Never implement "row absent from this window, therefore deleted".

#### 8.3.4 Reconciling to an accounting system

The mechanics that make this workable, and the ones that do not.

**What works.** The idempotent-ingestion pattern Rho publishes is sound: "Re-fetching a day's window returns the same `id` values, so ingestion can be made naturally idempotent." A closed accounting day is a clean half-open interval:

```bash
curl -s -H "Authorization: Bearer $RHO_API_TOKEN" \
  'https://rhoapi.rho.co/api/v1/transactions?status=settled&posted_after=2026-05-21T00:00:00Z&posted_before=2026-05-22T00:00:00Z&page_size=100'
```

`posted_after` is inclusive and `posted_before` is exclusive, so consecutive days tile without overlap or gap. Pin the day boundaries in the timezone your books close in, converted to UTC, and record which timezone you used: the API takes and returns `Z` timestamps exclusively, with no sub-second component and no non-`Z` offset anywhere in the corpus.

**What does not work: balance reconciliation.** `accounts[].balance.amount` is a standalone figure that does not reconcile to the transaction list. Summing settled transactions per account reproduces the balance on only 4 of 14 sandbox accounts, and all four are the ones where both sides are zero. The sandbox transaction list is a curated sample, not a complete ledger, and it does not pretend otherwise. **Do not write a balance-equals-sum-of-transactions assertion and test it against the sandbox**; you will either conclude the API is broken or, worse, tune your logic to match a fixture artifact. Test that assertion against production or not at all.

There is also no `available_balance`, `credit_limit`, `posted_balance` or `pending_balance` on an account. An account is four to six fields: `id`, `account_name`, `account_type`, `balance`, plus `account_number_last_4` and `routing_number_last_4` on deposit accounts only. All four sandbox credit accounts and both rewards accounts report `balance.amount = 0`, so you never see what a carried credit balance looks like on `/accounts` even though credit statements clearly carry non-zero closing balances.

**What does not work: statement-to-transaction reconciliation.** There is no link from a statement to the transactions it covers, in either direction. Reconciling a statement means doing the account and date-range filtering yourself, against a `period_start`/`period_end` pair that is inclusive on both ends, and accepting that the arithmetic may not close because the two surfaces use opposite sign conventions (see 8.4.2).

**Invoicing is almost entirely disconnected from the ledger.** The only join between the Invoicing product and the banking ledger is `invoices[].payments[].transaction_id`, and it is populated **only** for payments with `type: "received_in_account"`. In the sandbox that is 2 of 7 payments; the other 5 are `type: "external"` with a null `transaction_id` and a non-null `external_method`. There is no `customer_id` filter on `/invoicing/invoices` and no `accounting_sync_status` filter, so you cannot ask "which invoices failed to sync" and you cannot list one customer's invoices; both require a full walk plus client-side filtering.

> **Divergence:** `invoices[].activities[].user_id` uses the `40000000-` prefix, which everywhere else in the corpus means a **money movement id**. All three such ids fail to resolve against the 12 banking user ids (which use the `10000000-` prefix). Measured: 3 references, 0 resolve, 3 dangling. The Invoicing product's actor identities and the banking product's user identities are not in the same namespace. You cannot join an invoice activity to a cardholder or a transaction initiator. Nothing in the docs mentions this either way.

**Do not enrich list rows with single GETs.** Verified exhaustively across all 133 sandbox resources of all six types: `GET /{resource}/{id}` returns a byte-identical field set to the list row, with zero additional keys and zero value differences. There is no summary-versus-detail tier. Looping single GETs to "enrich" a list is pure waste and, against a ~60 req/min budget, actively harmful. The one exception is `GET /statements/{id}`, and what it buys is a possibly-re-signed `pdf_url`, not new fields.

**Do not pass `account_id` to `GET /transactions/{id}` speculatively.** The reference describes it only as "Account ID for the transaction". It is in fact an assertion filter: a wrong value turns a `200` into a `404`.

```bash
H='Authorization: Bearer sandbox'; B=https://rhoapi-sandbox.rho.co/api/v1
TX=019ef508-2808-7000-8000-000000000006   # this row lives on account ...0009
curl -s -o /dev/null -w '%{http_code}\n' -H "$H" "$B/transactions/$TX?account_id=30000000-0000-4000-8000-000000000009"  # 200
curl -s -o /dev/null -w '%{http_code}\n' -H "$H" "$B/transactions/$TX?account_id=30000000-0000-4000-8000-000000000002"  # 404
```

### 8.4 Handling money correctly

#### 8.4.1 Integer minor units, always

Every monetary value in the API is a `Money` object: `{"amount": <integer minor units>, "currency": "USD"}`. The docs repeat "treat amounts as integers rather than decimals" in three separate places. There is no `amount_decimal`, no `exponent` or `scale` field, no FX rate, and no original-currency field anywhere.

Store minor units as a 64-bit integer. Never round-trip through a float. The sandbox range is `-5900000` to `130000000` minor units (`-$59,000.00` to `$1,300,000.00`), comfortably inside int64, but a `float64` loses exactness above 2^53 minor units and there is no documented ceiling.

The exceptions are on Invoicing, and they are genuine non-integers:

| Field | Observed values | Required client type |
| --- | --- | --- |
| `invoices[].line_items[].quantity` | `1`, `2`, `2.5`, `3` | decimal / float, **not** int |
| `invoices[].tax_rate`, `line_items[].tax_rate` | `0`, `10` (ints), `6.25`, `8.5` (floats) | decimal / float |
| `invoices[].discount_rate`, `line_items[].discount_rate` | `0`, `5` | decimal / float |

A strict typed client must declare all three as decimal even though most values serialize without a decimal point. A Go or Rust client that types `quantity` as an integer will fail to deserialize the invoice with `quantity: 2.5`.

The invoice total formula, verified exact on all 12 sandbox invoices:

```
line.total    = round( unit_price.amount * quantity * (1 - line.discount_rate/100) )
invoice.total = round( SUM over lines of
                         line.total
                         * (1 - invoice.discount_rate/100)
                         * (1 + (line.tax_rate ?? invoice.tax_rate)/100) )
```

Two non-obvious parts. A **null** `line_items[].tax_rate` falls back to the invoice-level `tax_rate`; it does **not** mean zero (10 of 16 sandbox line items are null, and treating null as 0 gives the wrong total on `INV-2026-0066`: 146,000 instead of 158,000). And discount is applied **twice**, once per line and once at the invoice level; they do not net.

#### 8.4.2 Sign conventions, which are not consistent across the API

**On transactions:** the sign of `amount.amount` is the only directional signal. There is no `direction`, `debit_credit` or `type: debit|credit` field. The sign is **relative to the account named in `account_id`**: debits negative, credits positive. Zero never occurs across all 72 sandbox rows.

Do not infer direction from the type name. The one pair where name and sign disagree:

| `transaction_type` | Sandbox amount | Account | Note |
| --- | --- | --- | --- |
| `adjustment_credit` | **-4500** | Treasury Checking | "Correction of encoding error regarding check number 100245", counterparty `Rho` |
| `adjustment_debit` | **+3000** | Cash (Checking) | counterparty `Rho`, no memo |

Both are single instances, and nothing in `docs/v1/transactions` or the OpenAPI defines the sign of an adjustment, so whether this is intentional Rho semantics or a fixture sign bug cannot be resolved from the corpus. Either way: **read the sign, never the name.**

`credit_repayment`, `credit_repayment_refund` and `internal_transfer` appear with both signs because they are the double-entry types. Every other type has a single consistent sign across the sandbox.

**On statements, the polarity is inverted.** On a credit statement, `spending` is **positive** for money spent and `repayments` is **negative** for money repaid, which is exactly backwards from `card_debit` (negative) and the credit leg of `credit_repayment` (positive) in the transaction ledger. A single sign convention across both surfaces is impossible; branch explicitly.

The two statement families use mutually exclusive identities, verified on every sandbox record:

```
credit statements  (22/22):  closing_balance = opening_balance + spending + repayments
deposit statements (11/11):  closing_balance = opening_balance + total_credits - total_debits - total_fees
```

Applying the deposit identity to a credit statement gives the wrong answer on 11 of 22, because `total_credits`, `total_debits` and `total_fees` are always `0` on credit statements and carry no information. On `account` and `treasury` statements the `spending`, `repayments` and `cashback` keys are **omitted entirely**, not null. Branch on `statement_type`, or on key presence:

```python
from rho_client import RhoClient, SANDBOX


def closing_balance(statement: dict, acct: dict) -> int:
    """Minor units. Branch on statement_type: the two families share no arithmetic."""
    if statement["statement_type"] == "credit":
        # spending is POSITIVE for spend, repayments NEGATIVE for repayment.
        return (acct["opening_balance"]["amount"]
                + acct["spending"]["amount"]
                + acct["repayments"]["amount"])
    # account and treasury statements omit spending/repayments/cashback entirely.
    return (acct["opening_balance"]["amount"]
            + acct["total_credits"]["amount"]
            - acct["total_debits"]["amount"]
            - acct["total_fees"]["amount"])


client = RhoClient("sandbox", SANDBOX, rate_per_sec=4.0)
checked = 0
for statement in client.paginate("/statements"):
    for acct in statement["accounts"]:
        assert closing_balance(statement, acct) == acct["closing_balance"]["amount"], statement["id"]
        checked += 1
print(checked, "account lines reconciled")   # 33
```

**Amount filters compare the signed value, not the magnitude.** `min_amount=0` returns the 32 credits; `max_amount=0` returns the 40 debits. "Transactions over $100" therefore needs two queries or client-side filtering. Both bounds are inclusive. An inverted amount range is the only cross-field validation in the entire API and returns `400 {"type":"1317","title":"min_amount must be less than or equal to max_amount"}`, while an inverted **date** range returns a quiet `200` with zero rows.

#### 8.4.3 Currency

Every `currency` field in the entire sandbox corpus, across 393 occurrences in all six resources, is `USD`. There is no non-USD record, no FX rate, no settlement currency, and no second currency field anywhere. The documented `transaction_type` enum contains `international_wire_in`, `international_wire_out`, `international_wire_fee` and `international_wire_fee_refund`, and the sandbox produces the latter two but never a non-USD amount.

Store `currency` anyway, on every Money column, and enforce that a comparison or sum across two different currency codes is a programming error. The versioning contract explicitly allows new enum values into `v1` at any time, and "currency is implicit from the queried account" is the only guidance the reference gives on `min_amount`/`max_amount`. A single-currency assumption baked into your schema is the kind of thing that costs a migration later.

### 8.5 Storing and joining IDs

#### 8.5.1 The id shapes, and the one that will break you

| Resource | Observed shape | Example | Parses as UUID? |
| --- | --- | --- | --- |
| accounts | UUIDv4-shaped, prefix `30000000-0000-4000-8000-` | `…-000000000002` | yes |
| cards | UUIDv4-shaped, prefix `20000000-` | `…-000000000001` | yes |
| transactions | **UUIDv7**, time-ordered | `019f0554-0bf0-7000-8000-00000000000a` | yes |
| **statements** | **6-digit decimal string** | `"572981"`, `"152980"` | **no** |
| invoicing customers | UUIDv4-shaped, prefix `60000000-` | `…-000000000007` | yes |
| invoicing invoices | UUIDv4-shaped, prefix `70000000-` | `…-000000000010` | yes |
| transaction attachment `file_id` | genuinely random UUIDv4 | `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15` | yes |
| invoice `file_id` | UUIDv4-shaped, prefix `50000000-` | `…-000000000027` | yes |

> **Divergence:** `docs/v1/versioning` says "Treat IDs as opaque strings. Do not parse structure out of an `id` or assume a fixed format" and "Persist the full string exactly as returned, without assuming a fixed length or layout." That advice is correct and you should follow it, but the docs never state the one consequence that actually matters: **`statements.id` is not a UUID.** All 33 sandbox statement ids are exactly six decimal digits and `uuid.UUID()` rejects every one. A client that types statement ids as `uuid` will fail against sandbox and, by implication, production. Worse, `/statements/{id}` performs **no** format validation at all, so a garbage statement id returns `404 {"type":"1303","title":"statement not found"}` rather than the `400 invalid parameter` the other five resources give you. Store every id as `TEXT`/`VARCHAR`, never as a native UUID column.

The other prefix structure is real but you must not build on it, both because the docs forbid it and because it is fixture-generator artifact: all the `NNNNNNNN-0000-4000-8000-` ids have zero entropy and a decimal-looking counter in the last group.

#### 8.5.2 Normalize ids before using them as keys

The path parser accepts at least five distinct spellings of the same UUID, all returning `200` with an identical body whose `id` is normalized to canonical lowercase-dashed form:

| Spelling | Path | Result |
| --- | --- | --- |
| canonical | `/accounts/30000000-0000-4000-8000-000000000002` | 200 |
| no dashes (32 hex) | `/accounts/30000000000040008000000000000002` | 200 |
| brace-wrapped | `/accounts/{30000000-0000-4000-8000-000000000002}` | 200 |
| `urn:uuid:` prefix | `/accounts/urn:uuid:30000000-0000-4000-8000-000000000002` | 200 |
| uppercase hex | `/transactions/019F0554-0BF0-7000-8000-00000000000A` | 200 |

This is the exact accept-set of Go's `github.com/google/uuid` `Parse()`. Anything keying a cache on the request URL will store up to five copies of the same resource. Normalize to the canonical lowercase-dashed form yourself before it reaches a cache key, a log line or a database column.

#### 8.5.3 The joins that exist, and the ones that do not

Measured referential integrity across the whole sandbox corpus:

| Edge | Refs | Resolve | Dangling |
| --- | --- | --- | --- |
| `transactions.account_id` → accounts | 11 | 11 | 0 |
| `transactions.card_id` → cards | 8 | 8 | 0 |
| `statements.accounts[].account_id` → accounts | 5 | 5 | 0 |
| `customers.last_invoice_id` → invoices | 7 | 7 | 0 |
| `invoices.customer.id` → customers | 7 | 7 | 0 |
| `invoices.payments[].transaction_id` → transactions | 2 | 2 | 0 |
| `cards.cardholder.user_id` → transaction `user_id`s | 8 | 8 | 0 |
| **`invoices.activities[].user_id`** → transaction `user_id`s | **3** | **0** | **3** |

Three entity types are referenced by id and have **no endpoint at all**: users (`10000000-…`, 12 distinct), money movements (`40000000-…`, 65 distinct), and the business itself. You can reconstruct a partial user directory only by unioning `transactions.user_id` + `user_full_name` with `cards.cardholder.{user_id, first_name, last_name}`, and it will be missing anyone who neither holds a card nor initiated a visible transaction. `counterparty_name` is a bare string with no id, so counterparties cannot be deduplicated or joined.

`file_id` is **not one namespace**: invoice file ids use the structured `50000000-` prefix while transaction attachment file ids are random UUIDv4. And a single attachment `file_id` can be attached to two different transactions (`cdc328c1-c3a3-4670-a371-28e34891ee68` appears on both `019f0143-…-0002` and `019ef6d6-…-0009`, resolving to the same deduplicated blob), so the real key is the pair `(transaction_id, file_id)`.

#### 8.5.4 A schema that survives all of the above

```sql
CREATE TABLE rho_transaction (
    -- (id, account_id) is the primary key: `id` alone can drop a leg of a money movement.
    id                 TEXT        NOT NULL,
    account_id         TEXT        NOT NULL,
    money_movement_id  TEXT        NOT NULL,
    -- Store enums as text with no CHECK constraint. v1 may add values at any time.
    transaction_type   TEXT        NOT NULL,
    status             TEXT        NOT NULL,
    account_type       TEXT        NOT NULL,
    amount_minor       BIGINT      NOT NULL,   -- signed, account-relative. Never a float.
    currency           CHAR(3)     NOT NULL,
    initiated_at       TIMESTAMPTZ NOT NULL,
    posted_at          TIMESTAMPTZ,            -- omitted (not null) in the payload when unset
    counterparty_name  TEXT        NOT NULL,   -- may be the empty string
    account_name       TEXT        NOT NULL,   -- denormalized, NOT unique, do not join on it
    card_id            TEXT,
    user_id            TEXT,                   -- dangling: there is no /users endpoint
    memo               TEXT,
    note               TEXT,                   -- user-editable, changes after first sight
    raw                JSONB       NOT NULL,   -- keep the whole body: v1 adds fields additively
    first_seen_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, account_id)
);
CREATE INDEX ON rho_transaction (money_movement_id);
CREATE INDEX ON rho_transaction (initiated_at DESC);
CREATE INDEX ON rho_transaction (status) WHERE status IN ('pending', 'awaiting_approval');

CREATE TABLE rho_statement (
    id            TEXT NOT NULL PRIMARY KEY,   -- 6-digit decimal string, NOT a uuid
    statement_type TEXT NOT NULL,
    period_start  DATE NOT NULL,               -- date-only, inclusive
    period_end    DATE NOT NULL,               -- date-only, inclusive
    available_at  TIMESTAMPTZ NOT NULL,
    raw           JSONB NOT NULL               -- pdf_url excluded from change detection
);

CREATE TABLE rho_transaction_file (
    transaction_id TEXT NOT NULL,
    file_id        TEXT NOT NULL,              -- not unique across transactions
    file_name      TEXT NOT NULL,
    PRIMARY KEY (transaction_id, file_id)
);
```

Two schema rules worth stating explicitly, both derived from the versioning contract:

- **No `CHECK` constraint on any enum column, and a `default` branch on every switch.** "A new enum value" is classified as non-breaking and may ship into `v1` at any time. `transaction_type` already has 33 documented values, of which the sandbox produces 22; `cards.status` has 11, of which the sandbox produces 5. Your code will meet values it has never seen.
- **Keep the raw body.** "A new nullable response field" is also non-breaking. A strict deserializer (`serde` with `deny_unknown_fields`, Jackson with `FAIL_ON_UNKNOWN_PROPERTIES`, a non-defaulted generated enum) will break on an additive change that Rho is contractually entitled to ship without notice.

One spelling trap for any shared status mapper: `cards.status` spells it `canceled` with one L, while `invoices.status` and `activities[].activity_type` spell it `cancelled` with two. Both are correct within their own product and both ship in the same API version.

### 8.6 Retry, backoff and throttling

#### 8.6.1 What is retryable

| Status | Retry? | Notes |
| --- | --- | --- |
| `200` | n/a | |
| `400` | **No** | Two distinct dialects: `{"type":"about:blank",…,"detail":"invalid parameter: X"}` for a type-parse failure, `{"type":"1317","title":"<message>"}` for a semantic rule. Both are your bug. The exception: `"page_token must be a valid cursor"` mid-walk, which means restart the walk from page 1. |
| `401` | **No** | Fix the credential. Note that `401` is byte-identical between sandbox and production, so a wrong-host misconfiguration is indistinguishable from a wrong token. |
| `403` | **No** | Missing scope or source IP off the allowlist. Unreachable in sandbox: any non-empty bearer token grants all five scope families. |
| `404` | **No** | Except on `/statements/{id}`, where it also covers malformed ids. |
| `405` | **No** | Zero-byte body, `allow: GET`. You sent a write method. |
| `411`, `414` | **No** | HTML bodies from the Google frontend and nginx respectively, not from Rho. `414` means your URI crossed the ~8 KB to 16 KB nginx ceiling. |
| `429` | **Yes** | Honor `Retry-After` if present, otherwise exponential backoff with jitter. |
| `500`, `503` | **Yes** | Documented in the OpenAPI, never observed in sandbox. No guidance published for either. |
| Connection errors, timeouts | **Yes** | Every operation is a `GET`, so retries are free. There are no idempotency keys because there is nothing to make idempotent. |

Because every operation is a read, you have an unusual luxury: **retries are always safe.** Use it. Set an aggressive-but-bounded retry policy and stop worrying about duplicate side effects.

#### 8.6.2 Your error parser must tolerate non-JSON

At least five error-body shapes exist, and only three of them are JSON:

| Producer | Status | Content-Type | Body |
| --- | --- | --- | --- |
| Rho application (semantic) | 400, 404 | `application/problem+json` | `{"type":"1317"\|"1303",…}`, no `detail` |
| Rho application (parse) | 400 | `application/problem+json` | `{"type":"about:blank",…,"detail":"invalid parameter: X"}` |
| Rho auth middleware | 401 | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| Go router | 404 | `text/plain; charset=utf-8` | `404 page not found` |
| Go method check | 405 | *(none)* | **zero bytes**, `allow: GET` |
| ingress-nginx | 400, 414 | `text/html` | `400 Request Header Or Cookie Too Large`, `414 Request-URI Too Large` |
| Google frontend | 411 | `text/html` | `Error: Length Required` |
| Cloudflare WAF | 403 | `text/html` | "Attention Required!" block page |
| GCLB | 404 | `text/plain` | `default backend - 404` |

Branch on `Content-Type` before parsing. A client that unconditionally calls `.json()` on an error body throws on `405`, on route typos, and on an oversized `Authorization` header.

**Branch on the HTTP status, not on `type`.** The `type` member is not a URI despite the OpenAPI describing it as "A URI reference that identifies the problem type. Example: `about:blank`". Live values are `"2"`, `"1303"`, `"1317"` and `"about:blank"`. `1303` covers at least nine distinct not-found conditions across six resources; `1317` covers page size, cursor validity, sort, order, card type, card status and amount ordering alike. The only field that distinguishes them is `title`, which is free prose outside the versioning contract. There is no published registry for the numeric codes, and the gaps in the numbering imply a larger internal catalogue that is not published.

#### 8.6.3 Throttling is open-loop, and you cannot rehearse it

There are **no rate-limit headers of any kind**. No `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, no `X-RateLimit-*`, no `RateLimit-Policy`, across roughly 430 captured responses. You cannot pace adaptively. The only strategy available is a fixed, conservative, client-side token bucket.

> **Divergence:** `docs/v1/rate-limits` specifies approximately 60 req/min per token and approximately 600 req/min per source IP, returns `429 Too Many Requests`, and defines `Retry-After` handling including the unusual `Retry-After: 0` case. None of it is enforced or observable in the sandbox. Measured: 150 requests on one token inside a 57-second window, zero `429`; 65 requests on a brand-new, never-before-used token in 11.3 seconds, zero `429`; 60 concurrent requests completing in 0.871 s (68.9 req/s), zero `429`. The docs' own warning that "clients must not assume that exactly 60 simultaneous requests will succeed" was contradicted twice. `Retry-After` was never emitted on any status, so the documented branch logic is unexercisable. **You cannot test your backoff code against Rho's own test environment.** Write it blind and unit-test it against synthetic responses.

> **Divergence:** `429` is fully specified in the rate-limits guide and **absent from every one of the 14 OpenAPI operation pages**, all of which document `200, 400, 401, 403, 500, 503` (plus `404` on the 8 single-resource operations). A client generated from the OpenAPI document will treat `429` as an unmodeled status. Add the case by hand.

Practical rules that follow:

- Self-throttle at **0.9 req/s sustained** per token, with burst 1. The docs' advice is "below one request per second"; there is no documented burst allowance and no stated window semantics (fixed or sliding).
- Handle a `429` with an **absent** `Retry-After`. Nothing guarantees it is emitted.
- Treat `Retry-After: 0` as "use exponential backoff with jitter", not "retry now". This is a non-standard use of the header and Rho defines it explicitly.
- Do not size your client against sandbox tolerance. Sandbox absorbed 2.5x the documented per-token rate without complaint; production may not.
- Watch the **shared per-IP pool**. At 54 req/min per token, one egress IP supports about 11 tokens before the ~600 req/min ceiling binds, and that ceiling counts every integration behind the same NAT, including other teams'. Pinning a stable egress IP for the token's IP allowlist is good security and concentrates rate-limit risk on the same address.

### 8.7 Observability

#### 8.7.1 There is no request id

The only per-request correlation handle on any response is Cloudflare's `cf-ray` (for example `a39acb002db9f9a9-EWR`). There is no `X-Request-Id`, `Request-Id`, `X-Correlation-Id`, `traceparent`, or `X-Cloud-Trace-Context` on any status, on sandbox or production. **Log `cf-ray` on every request, success and failure.** It is the only thing you can quote to support.

Log alongside it: the full request URL including the query string (cursors and filters are the thing that goes wrong), the HTTP status, the response `Content-Type`, the elapsed time, and for errors the raw body bytes truncated. The `via: 1.1 google` header is a useful tell: with it, the request reached the Google-fronted origin stack; without it, Cloudflare or the Google frontend terminated it early.

#### 8.7.2 The alarms that matter

This API fails quietly far more often than it fails loudly. These are the signals worth alerting on, because every one of them corresponds to a real silent-failure mode documented above.

| Signal | What it detects |
| --- | --- |
| A filtered query returns `200 []` while an unfiltered control query on the same endpoint returns rows | A silently dropped filter: an unvalidated enum value, an empty `*_before` value, or a raw `;` in a filter value (Go's `url.ParseQuery` makes that whole key/value pair vanish) |
| Sync watermark has not advanced in N intervals | A stuck cursor, a silently empty result set, or genuinely no activity. You cannot distinguish these from the API, so alarm and investigate. |
| Row count from a full sweep drops between runs | An offset cursor skipped rows, or a filter changed. Rows never disappear from this API. |
| `400 page_token must be a valid cursor` rate above zero | Your query string is not byte-stable across pages |
| Count of rows stuck in `pending` or `awaiting_approval` beyond N days | Lane B is not re-reading them, or genuinely stuck money |
| Distinct `money_movement_id` count with an odd number of legs where you expect pairs | A half-ingested transfer |
| Any 5xx, any non-JSON error body, any `429` | Unrehearsable paths. Alarm on the first occurrence. |
| Token age approaching 45 days of inactivity, or approaching its expiry date | Tokens expire after 45 days of inactivity (window starts at creation for unused tokens) and carry a mandatory expiry of at most one year. There is no API to manage them and no warning mechanism. |

That last row deserves emphasis. Token lifecycle is entirely a UI operation: creation requires an Account Owner or Admin plus a 2FA challenge, there is no create/list/revoke API, and the maximum is 20 active tokens per business. Programmatic key rotation is impossible. Put the expiry date in a calendar and in your runbook.

#### 8.7.3 Metrics worth keeping

- Requests per minute per token, plotted against the documented 60, since you have no server-side signal.
- Page count and row count per walk, per endpoint, per run. A sudden change in page count at a fixed `page_size` is the cheapest available proxy for "the dataset moved".
- Wall time per full sweep. This is your backfill and disaster-recovery budget.
- Distribution of `posted_at - initiated_at` in your own production data. The sandbox says 18.23 days is the worst case; your lane C window should be sized against your real tail, not this one.
- Upsert outcome mix (inserted / updated / unchanged). A healthy steady state is mostly `unchanged` with a small `updated` tail. An `updated` rate that climbs means fields are churning, most likely a signed URL or a recomputed spend window leaking into your change fingerprint.

### 8.8 What you cannot build

Everything in this table is a hard "no" in `v1`, not a gap you can work around with a clever query.

| You cannot | Evidence | What it forces instead |
| --- | --- | --- |
| **Initiate a payment.** No ACH, no wire, no check, no transfer, no bill pay, no invoice send. | All 14 operations are `GET`. `POST`, `PUT`, `PATCH` and `DELETE` return `405 allow: GET` on every path, emitted before authentication. All five scopes end in `:read`. Rho's own product page: "Tokens cannot initiate payments or modify accounts... The Rho API is read-only today." | Your product is a read-side mirror plus an out-of-band handoff. Any "approve and pay" flow ends in a deep link to the Rho web app and a human. Design the UX around a handoff, not around an API call that you will add later. |
| **Issue, lock, unlock, or reconfigure a card.** No limit changes, no merchant-control edits, no PAN, CVC or expiry. | No write operation exists. `allowed_categories`, `allowed_merchants`, `blocked_categories` and `blocked_merchants` are read-only fields (and present on only 1 of 8 sandbox cards each). "Only the last four PAN digits are returned; full card numbers, CVCs, and expiration dates are not available through these endpoints." | Card administration stays in Rho's UI. You can build spend monitoring against `spending_limit`, `current_spend` and `pending_spend`, and alerting on utilisation, and a "lock this card" workflow whose last step is a link and a person. |
| **Receive a webhook.** No events, no subscriptions, no push of any kind. | `GET /webhooks` returns `404 page not found`. No such concept appears anywhere in the docs corpus. | Poll on the three-lane design in 8.2.3. Your data-freshness SLA is your poll interval, and your worst case is your lane C period. Tell downstream consumers what that interval is; do not let them assume real time. |
| **Bulk export.** No CSV or NDJSON endpoint, no export job, no `total_count`, no `Link` header, no backwards paging. `page_size` caps at 100. | The `page` object has exactly one field. Documented and enforced range is `[1, 100]` on all six endpoints. | Backfills are full cursor walks: `ceil(N/100)` requests paced at under 1 req/s. Budget 3.1 hours per million rows and run them on a dedicated token. Build resumability into the walk, because there is no bookmark: "Cursors are designed for live iteration, not for bookmarks", with no documented TTL. Resume by re-walking with a narrowed `initiated_after`, not by persisting a cursor. |
| **Serve more than one business from one token.** No entity selector, no `business_id` parameter, no business or organization endpoint. | A token is scoped to "the business linked to your API Access Token". Sandbox has one global fixture tenant and the token is demonstrably not a tenant selector: four different tokens return byte-identical data (md5 `593d7be465d362f7a9ba94fcbebbb927` on `/accounts`). | One credential per legal entity, N credentials for N entities, an explicit entity dimension in your schema and in every query path, and N separate rate-limit budgets that nonetheless share one ~600 req/min per-IP pool. At 54 req/min per token, one egress IP supports about 11 entities. Beyond that, spread egress addresses or accept queueing. For a partner serving many customers, note that the docs never say whether an OAuth-issued access token gets its own 60/min bucket or shares the partner's. |

Also absent, and worth knowing before you scope a feature around it:

- **No user or employee directory.** 12 user ids are referenced by two resources and resolvable by neither. You can only name a user who appears on a card or a transaction you can see.
- **No counterparty or vendor entity.** `counterparty_name` is a bare string with no id. Vendor deduplication is entirely your problem.
- **No money-movement endpoint.** `money_movement_id` groups legs but cannot be fetched or filtered on.
- **No dispute, decline or authorization surface.** Stated outright: "A refund or credit is not by itself a dispute, `v1` exposes no dispute indicator." There is no `card_dispute` or `chargeback` transaction type.
- **No payment tracing in practice.** `tracking_number` is documented in detail ("an ACH NACHA trace number, or a wire IMAD/OMAD") and never appears on any of the 72 sandbox transactions, including 11 ACH rows and 10 wire rows. `counterparty_logo_url` likewise never appears.
- **No invoice PDF retrieval, in sandbox.** All 9 invoices carrying a `file_id` return `404 {"type":"1303","title":"invoice file not found"}` from the exact call the docs prescribe. The handler routes (a malformed `file_id` returns `400`), so this is a fixture gap rather than a missing route, but you cannot integration-test invoice PDFs at all.
- **No browser client.** `OPTIONS` returns `405` with no CORS headers, and a `GET` carrying an `Origin` gets no `Access-Control-Allow-Origin`. Proxy through your own backend. This is the correct posture for a long-lived opaque secret, and it is nowhere stated in the docs.
- **No sandbox scenario control.** No way to elicit a `403`, `429`, `500`, `503`, an empty account list, or a second tenant. Three of the five error responses the OpenAPI documents per operation are unreachable in sandbox, and `401` is reachable only by deliberately breaking the header.

### 8.9 Reference implementation

A complete, runnable client. Tested against `https://rhoapi-sandbox.rho.co/api/v1` on 2026-09-11: it walks all six list endpoints to exhaustion, returns 72 transactions with 72 distinct `(id, account_id)` keys, and produces the expected `1303`/`about:blank` error classifications. Requires `requests`.

#### 8.9.1 `rho_client.py`

```python
"""Minimal Rho API v1 client. Read-only, poll-based."""
from __future__ import annotations

import json
import logging
import random
import threading
import time
from typing import Any, Iterable, Iterator, Sequence

import requests

log = logging.getLogger("rho")

SANDBOX = "https://rhoapi-sandbox.rho.co/api/v1"
PRODUCTION = "https://rhoapi.rho.co/api/v1"

# The array key in a list response is NOT derivable from the path:
# /invoicing/customers returns "customers", /invoicing/invoices returns "invoices".
RESOURCE_KEY = {
    "/accounts": "accounts",
    "/cards": "cards",
    "/transactions": "transactions",
    "/statements": "statements",
    "/invoicing/customers": "customers",
    "/invoicing/invoices": "invoices",
}

RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class RhoError(Exception):
    def __init__(self, status: int, body: Any, cf_ray: str | None, url: str):
        self.status = status
        self.body = body
        self.cf_ray = cf_ray          # the only correlation handle Rho gives you
        self.url = url
        detail = body if isinstance(body, str) else json.dumps(body, sort_keys=True)
        super().__init__(f"HTTP {status} on {url} (cf-ray={cf_ray}): {detail[:400]}")

    @property
    def problem_type(self) -> str | None:
        return self.body.get("type") if isinstance(self.body, dict) else None

    @property
    def title(self) -> str | None:
        return self.body.get("title") if isinstance(self.body, dict) else None


class RhoAuthError(RhoError): pass
class RhoNotFound(RhoError): pass
class RhoBadRequest(RhoError): pass
class RhoCursorInvalid(RhoBadRequest): pass
class RhoRateLimited(RhoError): pass


class TokenBucket:
    """Open-loop self-throttle. Rho emits no rate-limit headers, so pacing cannot be adaptive."""

    def __init__(self, rate_per_sec: float = 0.9, burst: int = 1):
        self._rate = rate_per_sec
        self._capacity = float(burst)
        self._tokens = float(burst)
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def take(self) -> None:
        while True:
            with self._lock:
                now = time.monotonic()
                self._tokens = min(self._capacity, self._tokens + (now - self._last) * self._rate)
                self._last = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                wait = (1.0 - self._tokens) / self._rate
            time.sleep(wait)


def clean_params(pairs: Iterable[tuple[str, Any]]) -> list[tuple[str, str]]:
    """Drop None; refuse empty strings.

    An empty value on any *_before filter returns 200 with zero rows instead of an error,
    so a templated query with an undefined variable silently reports "no activity".
    """
    out: list[tuple[str, str]] = []
    for key, value in pairs:
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            for item in value:                      # repeats OR together within one parameter
                if item is None or str(item) == "":
                    raise ValueError(f"empty value in repeated parameter {key!r}")
                out.append((key, str(item)))
            continue
        text = str(value)
        if text == "":
            raise ValueError(f"empty value for parameter {key!r}; omit it instead")
        out.append((key, text))
    return out


class RhoClient:
    def __init__(
        self,
        token: str,
        base_url: str = PRODUCTION,
        *,
        rate_per_sec: float = 0.9,
        max_attempts: int = 6,
        timeout: tuple[float, float] = (5.0, 30.0),
        session: requests.Session | None = None,
    ):
        if not token:
            raise ValueError("token must be non-empty")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.bucket = TokenBucket(rate_per_sec)
        self.session = session or requests.Session()
        self.session.headers.update({
            # One ASCII space, capital B. 'bearer' and a tab both return 401.
            "Authorization": f"Bearer {token}",
            # Only gzip is served. 'Accept-Encoding: *' gets you the full 7x payload.
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "User-Agent": "rho-client/1.0",
        })
        # Several connections, low per-connection concurrency: 50 streams on one h2
        # connection measured 13x worse p50 than a warm single stream.
        adapter = requests.adapters.HTTPAdapter(pool_connections=4, pool_maxsize=4, max_retries=0)
        self.session.mount("https://", adapter)

    # -- transport ---------------------------------------------------------

    def get(self, path: str, params: Sequence[tuple[str, str]] = ()) -> dict:
        url = f"{self.base_url}{path}"
        for attempt in range(1, self.max_attempts + 1):
            self.bucket.take()
            try:
                resp = self.session.get(url, params=list(params), timeout=self.timeout)
            except requests.RequestException:
                if attempt == self.max_attempts:
                    raise
                self._sleep_backoff(attempt, None)
                continue

            cf_ray = resp.headers.get("cf-ray")
            log.debug("GET %s -> %s cf-ray=%s", resp.url, resp.status_code, cf_ray)

            if resp.status_code == 200:
                return resp.json()

            body = self._parse_error_body(resp)
            if resp.status_code in RETRYABLE_STATUS and attempt < self.max_attempts:
                self._sleep_backoff(attempt, resp.headers.get("Retry-After"))
                continue
            raise self._classify(resp.status_code, body, cf_ray, resp.url)
        raise RuntimeError("unreachable")

    @staticmethod
    def _parse_error_body(resp: requests.Response) -> Any:
        """Error bodies are not always JSON.

        405 is zero bytes, unrouted paths are text/plain, oversized headers and edge blocks
        are HTML, and only 400/401/404 from the application are problem+json.
        """
        if "json" in resp.headers.get("content-type", ""):
            try:
                return resp.json()
            except ValueError:
                pass
        return resp.text[:1000]

    @staticmethod
    def _classify(status: int, body: Any, cf_ray: str | None, url: str) -> RhoError:
        # Branch on status. `type` is an overloaded non-URI code with no published registry:
        # 1303 covers nine not-found conditions, 1317 covers seven validation failures.
        if status == 401:
            return RhoAuthError(status, body, cf_ray, url)
        if status == 404:
            return RhoNotFound(status, body, cf_ray, url)
        if status == 429:
            return RhoRateLimited(status, body, cf_ray, url)
        if status == 400:
            title = body.get("title") if isinstance(body, dict) else ""
            if isinstance(title, str) and "cursor" in title:
                return RhoCursorInvalid(status, body, cf_ray, url)
            return RhoBadRequest(status, body, cf_ray, url)
        return RhoError(status, body, cf_ray, url)

    @staticmethod
    def _sleep_backoff(attempt: int, retry_after: str | None) -> None:
        # Retry-After has never been observed on any Rho response, so treat it as optional.
        # The docs define Retry-After: 0 as "no cooldown computed", not "retry now".
        delay = min(2 ** (attempt - 1), 30.0)
        if retry_after:
            try:
                hinted = float(retry_after)
                if hinted > 0:
                    delay = max(delay, hinted)
            except ValueError:
                pass
        time.sleep(delay + random.uniform(0, delay * 0.25))

    # -- pagination --------------------------------------------------------

    def paginate(
        self,
        path: str,
        params: Sequence[tuple[str, str]] = (),
        *,
        page_size: int = 100,
        max_pages: int = 10_000,
    ) -> Iterator[dict]:
        """Walk a list endpoint to exhaustion.

        Filters are sent byte-identically on every page: the cursor is bound to a fingerprint
        of the literal query, so order=asc then order=ASC invalidates the token even though
        both return the same rows.
        """
        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be between 1 and 100")
        key = RESOURCE_KEY.get(path)
        if key is None:
            raise ValueError(f"unknown list endpoint {path!r}")

        base = list(params) + [("page_size", str(page_size))]
        token: str | None = None
        seen_tokens: set[str] = set()
        for _ in range(max_pages):
            page_params = base if token is None else base + [("page_token", token)]
            try:
                body = self.get(path, page_params)
            except RhoCursorInvalid:
                if token is None:
                    raise
                # The dataset moved under an offset cursor. Restart; the caller dedupes.
                log.warning("cursor invalidated on %s, restarting walk", path)
                token, seen_tokens = None, set()
                continue

            yield from body.get(key, [])

            token = body.get("page", {}).get("next_page_token")
            if token is None:                     # the ONLY end-of-pages signal
                return
            if token in seen_tokens:
                raise RuntimeError(f"cursor loop detected on {path}")
            seen_tokens.add(token)
        raise RuntimeError(f"page limit exceeded on {path}")

    # -- typed helpers -----------------------------------------------------

    def list_accounts(self) -> list[dict]:
        return list(self.paginate("/accounts"))

    def list_transactions(
        self,
        *,
        account_id: Sequence[str] | None = None,
        status: Sequence[str] | None = None,
        transaction_type: Sequence[str] | None = None,
        initiated_after: str | None = None,
        initiated_before: str | None = None,
        posted_after: str | None = None,
        posted_before: str | None = None,
        page_size: int = 100,
    ) -> Iterator[dict]:
        valid_status = {"pending", "settled", "failed", "awaiting_approval"}
        for value in status or ():
            # /transactions does not validate enums: status=Settled returns 200 with zero rows.
            if value not in valid_status:
                raise ValueError(f"unknown transaction status {value!r}")
        params = clean_params([
            ("account_id", account_id),
            ("status", status),
            ("transaction_type", transaction_type),
            ("initiated_after", initiated_after),
            ("initiated_before", initiated_before),
            ("posted_after", posted_after),
            ("posted_before", posted_before),
        ])
        return self.paginate("/transactions", params, page_size=page_size)

    def get_transaction(self, transaction_id: str) -> dict:
        # Never pass account_id here: a wrong value turns a 200 into a 404.
        return self.get(f"/transactions/{transaction_id}")

    def get_transaction_file(self, transaction_id: str, file_id: str) -> dict:
        return self.get(f"/transactions/{transaction_id}/files/{file_id}")


# -- domain helpers --------------------------------------------------------


def row_key(txn: dict) -> tuple[str, str]:
    """The real primary key. `id` alone can silently drop a leg of a money movement."""
    return (txn["id"], txn["account_id"])


def is_open(txn: dict) -> bool:
    """Rows that can still change. v1 promises no transition order, so re-read these."""
    return txn.get("status") in ("pending", "awaiting_approval") or "posted_at" not in txn


def change_fingerprint(txn: dict) -> tuple:
    """Fields observed or documented to mutate in place after first sight.

    Note .get(): optionality on transactions is expressed by key OMISSION, never by null.
    """
    return (
        txn.get("status"),
        txn.get("posted_at"),
        txn["amount"]["amount"],
        txn["amount"]["currency"],
        txn.get("memo"),
        txn.get("note"),
    )
```

#### 8.9.2 `sync.py`

```python
"""Incremental transaction sync. No webhooks, no updated_at, so this is a multi-lane poll."""
from __future__ import annotations

import datetime as dt
import logging
from dataclasses import dataclass, field
from typing import Callable, Iterable

from rho_client import RhoClient, change_fingerprint, is_open, row_key

log = logging.getLogger("rho.sync")

# Longest posted_at - initiated_at lag in the sandbox corpus is 18.23 days (a settled
# check_payment). 47 of 71 rows lag zero; p90 is 1 day. Size this against YOUR tail.
LATE_ARRIVAL_DAYS = 35
CLOCK_SKEW = dt.timedelta(minutes=5)


def rfc3339(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class SyncState:
    """Persist this. `watermark` is an observed initiated_at, never a wall clock."""

    watermark: dt.datetime | None = None
    open_keys: set[tuple[str, str]] = field(default_factory=set)
    last_full_sweep: dt.datetime | None = None


@dataclass
class SyncResult:
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0


def sync_transactions(
    client: RhoClient,
    state: SyncState,
    upsert: Callable[[dict], str],
    *,
    now: dt.datetime | None = None,
    full_sweep_every: dt.timedelta = dt.timedelta(days=7),
) -> tuple[SyncState, SyncResult]:
    """`upsert` returns "inserted", "updated" or "unchanged" and must be idempotent."""
    now = now or dt.datetime.now(dt.timezone.utc)
    result = SyncResult()
    seen: dict[tuple[str, str], dict] = {}

    def collect(rows: Iterable[dict]) -> None:
        for row in rows:
            seen.setdefault(row_key(row), row)

    do_full = (
        state.watermark is None
        or state.last_full_sweep is None
        or now - state.last_full_sweep >= full_sweep_every
    )

    if do_full:
        # Unfiltered. Any initiated_after floor you pick can silently cut off the tail:
        # the sandbox corpus starts 2023-05-31, three years before its newest row.
        log.info("full sweep, unfiltered")
        collect(client.list_transactions(page_size=100))
        state.last_full_sweep = now
    else:
        # Lane A: newly initiated rows.
        lane_a_from = state.watermark - CLOCK_SKEW
        log.info("lane A from %s", rfc3339(lane_a_from))
        collect(client.list_transactions(initiated_after=rfc3339(lane_a_from), page_size=100))

        # Lane C: trailing window, catches backdated inserts and in-place mutations.
        lane_c_from = now - dt.timedelta(days=LATE_ARRIVAL_DAYS)
        if lane_c_from < lane_a_from:
            log.info("lane C from %s", rfc3339(lane_c_from))
            collect(client.list_transactions(initiated_after=rfc3339(lane_c_from), page_size=100))

        # Lane B: rows still open from before the trailing window, one by one.
        # There is no money_movement_id filter and no id-set filter, so this is the
        # only way to re-read a specific old row.
        for txn_id, _account_id in [k for k in state.open_keys if k not in seen]:
            try:
                collect([client.get_transaction(txn_id)])
            except Exception as exc:      # a 404 here is a bug worth seeing, not a no-op
                log.warning("open row %s unreadable: %s", txn_id, exc)

    open_keys: set[tuple[str, str]] = set()
    max_initiated: dt.datetime | None = state.watermark
    for key, row in seen.items():
        outcome = upsert(row)
        setattr(result, outcome, getattr(result, outcome) + 1)
        if is_open(row):
            open_keys.add(key)
        initiated = dt.datetime.strptime(
            row["initiated_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=dt.timezone.utc)
        if max_initiated is None or initiated > max_initiated:
            max_initiated = initiated

    state.open_keys = open_keys
    if max_initiated is not None:
        state.watermark = max_initiated
    return state, result


def make_upsert(store: dict[tuple[str, str], dict]) -> Callable[[dict], str]:
    """Replace the dict with your database. The contract is: keyed on (id, account_id),
    idempotent, and reports whether anything in the change fingerprint moved."""

    def upsert(row: dict) -> str:
        key = row_key(row)
        prior = store.get(key)
        store[key] = row
        if prior is None:
            return "inserted"
        return "unchanged" if change_fingerprint(prior) == change_fingerprint(row) else "updated"

    return upsert
```

#### 8.9.3 Running it

```python
import datetime as dt, logging
from rho_client import RhoClient, SANDBOX
from sync import SyncState, sync_transactions, make_upsert

logging.basicConfig(level=logging.INFO)
client = RhoClient("sandbox", SANDBOX, rate_per_sec=4.0)   # production: 0.9, and a real token

store: dict = {}
upsert = make_upsert(store)
state = SyncState()

state, first = sync_transactions(client, state, upsert)
print(first)          # SyncResult(inserted=72, updated=0, unchanged=0)
print(len(state.open_keys))   # 3  (2 pending card_debits + 1 awaiting_approval)

state, second = sync_transactions(client, state, upsert)
print(second)         # SyncResult(inserted=0, updated=0, unchanged=4)
```

The second run costs four requests: one page for lane A, plus one `GET /transactions/{id}` for each of the three open rows. That is the steady state the three-lane design is built to produce.

One deliberate omission: the client does **not** pin sandbox versus production beyond the `base_url` you pass. It cannot help you there. Sandbox and production rejections are byte-identical (same 52-byte body, same header set, same Cloudflare IPs, md5 `a9b8c917cbc1e5b43579afaee5ccadd5`), so a typo in your base URL surfaces as exactly the `401` a bad token would. Assert on `base_url` in your own configuration tests, and never let the environment be inferred.
