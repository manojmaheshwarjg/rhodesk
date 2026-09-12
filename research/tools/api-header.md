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

{{TOC}}

---

