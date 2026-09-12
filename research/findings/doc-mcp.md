# Rho MCP server: complete reference and assessment

Research date: 2026-09-11. Corpus: local Rho crawl plus five live HTTP probes run 2026-09-11 23:38 to 23:39 UTC (documented in section 10).

Primary sources read in full:

| Source | Local path |
| --- | --- |
| MCP guide (docs.rho.co/docs/v1/mcp) | `scratchpad/rho/docs/docs_v1_mcp.md` (38 lines, the entire public MCP doc) |
| Rho API product page (rho.co/product/api) | `scratchpad/rho/pages/core/product__api.txt` |
| Claude Code landing page (rho.co/claude-code) | `scratchpad/rho/pages/core/claude-code.txt` |
| Auth guide | `scratchpad/rho/docs/docs_v1_auth.md` |
| Partner (OAuth) auth guide | `scratchpad/rho/docs/docs_v1_partner-auth.md` |
| Versioning guide (contains the MCP parity clause) | `scratchpad/rho/docs/docs_v1_versioning.md` |
| Rate limits, pagination, getting started | `scratchpad/rho/docs/docs_v1_{rate-limits,pagination,getting-started}.md` |
| OpenAPI index and 14 operation pages | `scratchpad/rho/docs/api_v1_openapi.md`, `scratchpad/rho/api/*.md` |
| Help center, The Rho API category (4 articles) | `scratchpad/rho/pages/help/help-center__the-rho-api*.txt` |
| Launch blog | `scratchpad/rho/pages/extra/blog__introducing-rho-api.txt` |
| Banking-API ranking blog (74 MCP mentions) | `scratchpad/rho/pages/blogcomp/blog__best-banking-apis-for-business.txt` |
| AI-startups blog | `scratchpad/rho/pages/blogcomp/blog__best-banks-for-ai-startups.txt` |
| Prior live captures | `scratchpad/rho/mcp/{prm.json,prod-401.txt,authsrv.json,init.headers,as.json}` |

Headline: the public MCP documentation is 38 lines. It gives one URL, one transport, three protocol version strings, one Claude Code command, two authentication paths, and then explicitly declines to list the tools, telling you to introspect the server yourself. Everything else in this file is reconstructed from the REST contract that Rho says the MCP surface mirrors 1:1, from the help center, and from live probes.

---

## 1. The entire MCP doc, reproduced verbatim

Source: `https://docs.rho.co/docs/v1/mcp` (local: `docs/docs_v1_mcp.md`). Nav subtitle for this page in the docs app data (`docs-app-data.json`): "Connect MCP clients to the Rho API."

````markdown
# MCP

The service exposes MCP over Streamable HTTP. The MCP endpoint is separate from the REST API routes:

| REST endpoint | MCP endpoint |
|  --- | --- |
| `/api/v1` | `/mcp/v1` |


MCP uses the same API contract, authentication model, scopes, and error behavior as the REST API. The `/mcp/v1` tool schemas follow the same stability policy as the REST contracts - see [Versioning and compatibility](/docs/v1/versioning).

## Protocol Versions

The MCP endpoint advertises and supports protocol versions `2026-07-28`, `2025-11-25`, and `2025-06-18`. Clients can negotiate the current sessionless protocol through `server/discover`. Every non-`initialize` request must include the selected version in the `MCP-Protocol-Version` header. Versions older than `2025-06-18` and JSON-RPC batches are rejected.

## Claude Code

Add the Rho API MCP server:

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

Use `/mcp` inside Claude Code to confirm the server is connected.

## Authentication

Rho supports two MCP authentication paths:

- **Direct connections** require an API Access Token in `Authorization: Bearer <rho_api_access_token>`.
- **Linked apps** use the OAuth connection provided by the MCP client, without requiring users to configure an API Access Token manually. Linked-app availability depends on the client.


## Tools and Prompts

The MCP server exposes Rho API tools, prompts, and resources. You can use your MCP client like Claude Code or
[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) to inspect all available capabilities.
````

That is the complete document. There is exactly one configuration snippet on the page (the `claude mcp add` command above) and it is reproduced here verbatim, including line continuations.

The second MCP passage in the docs, from `docs/docs_v1_versioning.md`, verbatim:

```markdown
## MCP parity

The MCP server is 1:1 with the REST API, so the `/mcp/v1` tool schemas follow the same policy as the
REST contracts above: additive-only, with breaking changes requiring a new version. One policy covers
both surfaces.

Tool *names* derive from the frozen `v1` operationIds, so **tool names will never change**. You can
reference them explicitly in workflows, agent skills, and saved automations without them breaking.

Tool *descriptions* are not part of the contract - they may be improved at any time to help agents use
the tools well, and such changes are never treated as breaking.
```

---

## 2. Endpoint, transport, hosts

| Property | Value | Source |
| --- | --- | --- |
| MCP endpoint (production) | `https://rhoapi.rho.co/mcp/v1` | MCP doc Claude Code snippet; confirmed live as the `resource` in protected-resource metadata |
| REST endpoint (production) | `https://rhoapi.rho.co/api/v1` | openapi.md Servers block |
| REST endpoint (sandbox) | `https://rhoapi-sandbox.rho.co/api/v1` | openapi.md Servers block |
| MCP endpoint (sandbox) | Does not exist. `POST https://rhoapi-sandbox.rho.co/mcp/v1` returns HTTP 404 `default backend - 404` (probe, 2026-09-11 23:38:48 UTC) | Live probe, section 10 |
| Transport | "MCP over Streamable HTTP" (single HTTP endpoint, JSON-RPC POST, optional SSE stream). No stdio, no WebSocket, no SSE-legacy endpoint documented | MCP doc |
| Path strictness | `/mcp` and `/mcp/v1/` (trailing slash) both return 404; only the exact path `/mcp/v1` is served | Live probe |
| Edge | Cloudflare in front of a Google (GCP) origin: `server: cloudflare`, `via: 1.1 google`, `cf-cache-status: DYNAMIC` on every response | Response headers |
| Security headers on the MCP route | `strict-transport-security: max-age=63072000; includeSubDomains; preload`, `x-content-type-options: nosniff`, `x-frame-options: DENY`, `referrer-policy: strict-origin-when-cross-origin` | Live probe |

Not stated anywhere: whether the MCP server keeps sessions (`Mcp-Session-Id`), whether it supports server-to-client notifications, resumability (`Last-Event-ID`), or elicitation/sampling. The phrase "the current sessionless protocol" in the doc implies a sessionless mode exists, but nothing describes how session-mode clients are handled.

---

## 3. Protocol version handling

| Rule | Detail |
| --- | --- |
| Advertised and supported versions | `2026-07-28`, `2025-11-25`, `2025-06-18` |
| Negotiation | "Clients can negotiate the current sessionless protocol through `server/discover`" |
| Header requirement | "Every non-`initialize` request must include the selected version in the `MCP-Protocol-Version` header" |
| Rejected | Any version older than `2025-06-18`; all JSON-RPC batch requests |

Notes and caveats:

- `server/discover` is not a method in the MCP specification revisions I can verify from this corpus, and no example request or response for it appears anywhere in the docs, the help center, or the marketing pages. Rho names it once and never shows it. Treat it as unverified surface.
- `2026-07-28` and `2025-11-25` as protocol revision dates are asserted only by Rho here; the corpus contains no spec reference for them.
- The batch rejection is consistent with MCP 2025-06-18, which removed JSON-RPC batching.
- Nothing states what error is returned for an unsupported version, a missing `MCP-Protocol-Version` header, or a malformed JSON-RPC envelope. The REST side documents a full RFC 9457 problem-details error model; the MCP page says error behavior is "the same as the REST API", which is not obviously well-defined for a JSON-RPC transport (JSON-RPC error objects vs HTTP problem+json).

---

## 4. Authentication model

### 4.1 The two documented paths

| Path | Credential | Who can create it | Client support |
| --- | --- | --- | --- |
| Direct connection | API Access Token, sent as `Authorization: Bearer <rho_api_access_token>` | Account Owners and Admins only, behind a 2FA challenge, from Settings, then Configurations, then Access Tokens (product page) or Settings, then API, then Access Tokens (help center) | Any MCP client that can set a static header |
| Linked app | OAuth connection provided by the MCP client. "without requiring users to configure an API Access Token manually. Linked-app availability depends on the client." | Only Account Owners and Admins can authorize an OAuth grant | Claude is the only client named anywhere in the corpus |

### 4.2 API Access Token lifecycle (from `docs/docs_v1_auth.md`, applies to MCP because the MCP doc says the auth model is identical)

| Property | Value |
| --- | --- |
| Prefix and shape | `rhobat_` plus 62 hex characters. Doc example: `rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f` |
| Scope of the secret | "long-lived, opaque secret scoped to a single business", survives personnel changes |
| Display | Shown only once, immediately after creation. "There is no way to recover the secret later." |
| Max active tokens | 20 per business |
| Expiration | Required at creation, maximum one year |
| Inactivity expiry | Automatic after 45 days of inactivity; a successful authenticated request counts as activity; for never-used tokens the window starts at creation |
| IP allowlist | Optional, up to 100 entries per token; requests from other source IPs are rejected with 403 |
| Revocation | Immediate, no grace period, no un-revoke; next request returns 401 |
| Other auth methods | "No other authentication header (cookie, API key, signed request) is supported." |
| Sandbox auth | Any non-empty bearer token (`Authorization: Bearer sandbox`). Irrelevant to MCP because the sandbox exposes no MCP endpoint |

Error semantics carried over to MCP by the parity claim: `401` for missing, malformed, unknown, revoked, or expired token; `403` for a valid token lacking the endpoint scope or coming from an IP outside the allowlist. Bodies are `application/problem+json` per RFC 7807/9457, documented example:

```json
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Token is revoked or has expired"
}
```

The live MCP 401 does not match that shape (see section 10).

### 4.3 OAuth path (linked apps), from `docs/docs_v1_partner-auth.md` plus live metadata

| Property | Value |
| --- | --- |
| Flow | OAuth 2.0 Authorization Code with PKCE (`code_challenge_method=S256` in the documented example) |
| Authorization server | `https://auth.rho.co` |
| Authorize endpoint | `https://auth.rho.co/oauth2/auth` |
| Token endpoint | `https://auth.rho.co/oauth2/token` |
| Revoke endpoint | `https://auth.rho.co/oauth2/revoke` |
| Audience parameter | `audience=https%3A%2F%2Frhoapi.rho.co` |
| Client registration | Manual only. Email `api-partner-request@rho.co` with app name, company name, logo, redirect URIs, requested scopes, privacy policy URI, ToS URI, support email. Rho then issues `client_id` and `client_secret` |
| Access token TTL | 900 seconds (15 minutes), per the documented token response `"expires_in": 900` |
| Refresh token | Single-use, rotates on every refresh, 30 days rolling |
| Grant lifetime | 1 year, after which the customer must re-approve |
| Grants per app per business | At most one active grant; approving again updates the existing connection |
| Consent | Customer signs in, selects the business, grants scopes. Only Account Owners and Admins can do this |
| Customer revocation | Immediate, invalidates all tokens for the grant including refresh tokens |
| Discovery | `https://auth.rho.co/.well-known/openid-configuration` |

Live authorization-server metadata (fetched 2026-09-11, identical at `/.well-known/oauth-authorization-server` and the previously captured `/.well-known/openid-configuration`):

- `grant_types_supported`: `authorization_code`, `implicit`, `client_credentials`, `refresh_token`, `urn:ietf:params:oauth:grant-type:device_code`. The device-code and client-credentials grants are advertised but documented nowhere on docs.rho.co.
- `code_challenge_methods_supported`: `["plain","S256"]`. The docs mandate S256; the server also advertises `plain`, which is a weaker PKCE mode.
- `token_endpoint_auth_methods_supported`: `client_secret_post`, `client_secret_basic`, `private_key_jwt`, `none`.
- `scopes_supported` at the AS: `["offline_access","offline","openid"]` only. The Rho API scopes are not advertised by the AS, only by the protected-resource metadata.
- **No `registration_endpoint`.** RFC 7591 dynamic client registration is not advertised. Implication below.
- Stack fingerprint: `credentials_endpoint_draft_00`, backchannel and frontchannel logout, `end_session_endpoint` at `/oauth2/sessions/logout`. This is an Ory Hydra style deployment.

**The DCR gap is the single most important undocumented fact about the "linked apps" path.** The MCP authorization flow that generic clients implement (protected-resource metadata, then AS metadata, then dynamic client registration, then authorization code with PKCE) cannot complete against `auth.rho.co`, because there is no registration endpoint to self-register with. Every OAuth client must be hand-registered by Rho's partner process. That is precisely why the doc hedges with "Linked-app availability depends on the client" and why every marketing page says Claude is "the natively supported client today". A third-party MCP client is therefore restricted to the static-token path in practice.

### 4.4 Protected-resource metadata (live, verbatim)

`GET https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` returns HTTP 200, `content-length: 294`:

```json
{"resource":"https://rhoapi.rho.co/mcp/v1","authorization_servers":["https://auth.rho.co"],"bearer_methods_supported":["header"],"scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],"resource_documentation":"https://docs.rho.co/docs/v1/mcp"}
```

A second, resource-wide document exists at `GET https://rhoapi.rho.co/.well-known/oauth-protected-resource` (HTTP 200):

```json
{"resource":"https://rhoapi.rho.co","authorization_servers":["https://auth.rho.co"],"bearer_methods_supported":["header"],"scopes_supported":["accounts:read","transactions:read","statements:read","cards:read","invoicing:read"],"resource_documentation":"https://docs.rho.co"}
```

`GET https://rhoapi.rho.co/.well-known/oauth-authorization-server` returns 404, and `/.well-known/oauth-protected-resource/api/v1` returns 404 `page not found`. So the RFC 9728 discovery chain exists for the MCP route (and the host root) and nowhere else, which is a deliberate MCP-shaped implementation.

---

## 5. How a user connects, per client

| Client | Documented? | Mechanism | Who must do it |
| --- | --- | --- | --- |
| Claude (claude.ai apps, connector directory) | Yes, in the help center and on the product page | Customize, then Connectors directory, select Rho, sign in with Rho credentials, select the business, answer an onboarding question if prompted, review and adjust the requested permissions, click Authorize | Account Owner or Administrator only |
| Claude Code | Yes, the only code snippet in the docs | `claude mcp add --scope project --transport http rho-api ...` with an inline `Authorization: Bearer` header, then `/mcp` to confirm | Anyone holding a token; the token itself requires Owner or Admin to mint |
| Any other MCP client | Generic instructions only | "In your AI tool, add the Rho MCP server and authenticate using your access token. See MCP for the server address and the exact header format." | Owner or Admin to mint the token |
| Claude Desktop | **Not documented.** No `claude_desktop_config.json`, no `mcpServers` JSON block anywhere in the corpus | n/a | n/a |
| Cursor, VS Code, Codex CLI, ChatGPT | **Not documented for Rho.** These names appear in Rho's comparison blog only as descriptions of Mercury, Stripe, Brex, and Modern Treasury support | n/a | n/a |
| MCP Inspector | Named once as a way to introspect capabilities, with no configuration example | n/a | n/a |

Verbatim connection copy, Claude connector directory (help center, `Connect Claude to your Rho account`):

> In Claude, open the Customize, then Connectors directory and select Rho. Sign in with your Rho credentials. Select the business you want to connect. If prompted, answer the onboarding question about how you plan to use the integration. Review the requested permissions and adjust them if needed. Click Authorize.

Multi-entity behavior, verbatim: "Each connection links Claude to one Rho business. If you have multiple businesses, Claude connects to one at a time: to switch, reconnect the Rho connector and choose a different business at the authorization step." That is a real limitation for accounting firms and multi-entity groups, which Rho otherwise markets to via the Partner Portal.

Disconnect paths (help center, `Connecting AI tools to your Rho account`):

- Connected through a connector directory: remove the Rho connection in the AI tool's settings, then revoke the connection in Rho under **Settings, then API, then Linked Apps**.
- Connected with an API access token: revoke the token in **Settings, then API, then Access Tokens**.
- "Once access is revoked, it stops working immediately."

Note the settings-path contradiction: the product page says "Settings, then Configurations, then Access Tokens"; the help center and the OpenAPI `tokenUrl` say Settings, then API, then Access Tokens (`https://app.rho.co/settings/access-tokens`). Minor, but the product page is stale or wrong.

---

## 6. What the MCP server exposes: tools, prompts, resources

### 6.1 What Rho actually says

Two sentences, verbatim: "The MCP server exposes Rho API tools, prompts, and resources. You can use your MCP client like Claude Code or [MCP Inspector] to inspect all available capabilities."

That is the entire treatment. **Rho publishes no tool list, no tool names, no input schemas, no output schemas, no prompt names, no resource URIs, and no annotations (no `readOnlyHint`, no `openWorldHint`).** There is no MCP section in the OpenAPI index, no `tools.json`, and nothing in `docs-llms.txt` beyond the page itself. The doc simultaneously promises that tool names are frozen forever and declines to tell you what they are.

### 6.2 The inferable tool inventory

Two contract statements let the inventory be reconstructed with high confidence:

1. "The MCP server is 1:1 with the REST API" (versioning doc).
2. "Tool names derive from the frozen `v1` operationIds, so tool names will never change" (versioning doc).

The v1 REST surface is exactly 14 operations, all GET, all read. Operation identifiers below are taken from the docs URL slugs at `docs.rho.co/api/v1/openapi/<tag>/<operationid>.md`; the canonical operationId casing (for example `listAccounts` vs `listaccounts`) is not published, and neither is the tool-name transform (prefix, separator, or namespace).

| # | REST operation | Method and path | Docs operationId slug | Required scope | Page size |
| --- | --- | --- | --- | --- | --- |
| 1 | List accounts | GET /accounts | `listaccounts` | `accounts:read` | max 100 |
| 2 | Get account | GET /accounts/{account_id} | `getaccount` | `accounts:read` | n/a |
| 3 | List cards | GET /cards | `listcards` | `cards:read` | default 20, range 1 to 100 |
| 4 | Get card | GET /cards/{id} | `getcard` | `cards:read` | n/a |
| 5 | List transactions | GET /transactions | `listtransactions` | `transactions:read` | max 100 |
| 6 | Get transaction | GET /transactions/{id} | `gettransaction` | `transactions:read` | n/a |
| 7 | Get transaction file | GET /transactions/{transaction_id}/files/{file_id} | `gettransactionfile` | `transactions:read` | n/a |
| 8 | List statements | GET /statements | `liststatements` | `statements:read` | max 100 |
| 9 | Get statement | GET /statements/{id} | `getstatement` | `statements:read` | n/a |
| 10 | List invoicing customers | GET /invoicing/customers | `listinvoicingcustomers` | `invoicing:read` | default 20 |
| 11 | Get invoicing customer | GET /invoicing/customers/{customer_id} | `getinvoicingcustomer` | `invoicing:read` | n/a |
| 12 | List invoicing invoices | GET /invoicing/invoices | `listinvoicinginvoices` | `invoicing:read` | default 20 |
| 13 | Get invoicing invoice | GET /invoicing/invoices/{invoice_id} | `getinvoicinginvoice` | `invoicing:read` | n/a |
| 14 | Get invoicing invoice file | GET /invoicing/invoices/{invoice_id}/files/{file_id} | `getinvoicinginvoicefile` | `invoicing:read` | n/a |

So: **14 tools, 0 write tools, 5 resource families.** If parity is literal, an agent gets 6 list tools with rich filters, 6 single-object getters, and 2 signed-URL file fetchers.

### 6.3 Prompts and resources

The word "prompts" appears once (the heading and one sentence) and "resources" once. No prompt is named. No MCP resource URI scheme is given. Plausible candidates (statement PDFs, invoice PDFs, transaction attachments as MCP resources) are never confirmed. **This is the single largest documentation gap: a client operator cannot know, before connecting a finance account, what the server will inject into the model's context.**

---

## 7. Permission scope: what a connected agent can actually see

### 7.1 Scopes

Scope format is `resource:action`, enforced before the handler, 403 on mismatch.

| Scope | Description | Listed in auth guide? | Listed in OpenAPI security block? | Listed in live PRM? |
| --- | --- | --- | --- | --- |
| `accounts:read` | Read account information for the business | Yes | Yes | Yes |
| `transactions:read` | Read transactions the business has access to | Yes | Yes | Yes |
| `statements:read` | Read statements for the business's accounts | Yes | Yes | Yes |
| `cards:read` | Read access to business cards information | **No** | Yes | Yes |
| `invoicing:read` | Read access to Invoicing information | **No** | Yes | Yes |

The authentication guide's scope table is stale by two scopes. Anyone sizing the blast radius from `docs/v1/auth` alone will underestimate it by the entire Cards and Invoicing surface, including cardholder names and customer PII. The OAuth partner guide's example scope string (`accounts:read transactions:read offline_access`) also omits them.

Scope selection is per connection: "For every connection you create with your AI tools, you can select the scope of data available through that connection." Scopes are set "at token creation" or "at OAuth consent" (help center, with two screenshots referenced as `a) Token Creation` and `b) OAuth Consent`). Claude's authorization screen lets the user "Review the requested permissions and adjust them if needed", so scope reduction at consent is supported.

There is no sub-scope granularity: no per-account scoping, no date-window scoping, no amount ceiling, no field-level redaction, no read-only-to-a-single-card restriction. `transactions:read` means the whole ledger for the whole business, for all time.

### 7.2 Field-level view of what lands in the model's context

Accounts (`accounts:read`): `id`, `account_name`, `account_type` (`checking`, `credit`, `investment`, `savings`, `rewards`), `balance.amount` (signed integer minor units) and `balance.currency`, `account_number_last_4`, `routing_number_last_4`. Sandbox sample: `{"account_name":"Cash (Checking)","account_number_last_4":"9508","account_type":"checking","balance":{"amount":876138,"currency":"USD"},"routing_number_last_4":"0089"}`.

Transactions (`transactions:read`): `id`, `money_movement_id`, `account_id`, `account_name`, `account_type`, `transaction_type` (33 enum values, listed in section 12.3), `status` (`pending`, `settled`, `failed`, `awaiting_approval`), `amount.amount` signed minor units and `amount.currency`, `initiated_at`, `posted_at` (nullable), `attachments[]` with `file_id` and `file_name`, plus:

- Attribution: `user_id`, `user_full_name` (employee names), `card_id`, `card_name`.
- Counterparty: `counterparty_name` ("the merchant, or the other side of the money movement. Always present, though it can be an empty string"), `counterparty_logo_url`.
- Free text: `memo` ("supplied by a bank or payment provider or generated by Rho", not user-editable) and `note` (user or system annotation).
- Payment tracing: `tracking_number`, an "ACH NACHA trace number, or a wire IMAD/OMAD". MT103 references are explicitly not returned.

Cards (`cards:read`): `id`, `name`, `last_4`, `type` (`physical`, `virtual`), `status`, `cardholder.{user_id,first_name,last_name}`, `spending_limit`, `spending_limit_type` (`daily`, `weekly`, `monthly`, `quarterly`, `annual`, `fixed`, `single_use`), `current_spend`, `pending_spend`, `spend_period_start`, `spend_period_end`, `usage_starts_at`, `usage_ends_at`, `billing_address` (street, city, subdivision, postal code, country), `shipping_address`, `blocked_categories[]` (MCC code plus name) or `allowed_*`, `blocked_merchants[]`. Explicit limit, verbatim: "Only the last four PAN digits are returned; full card numbers, CVCs, and expiration dates are not available through these endpoints." That is a materially better posture than Slash, which per Rho's own comparison blog may return plaintext PAN and CVV unless an RSA public key is configured [Rho claim about a competitor].

Statements (`statements:read`): `id`, `period_start`, `period_end`, `available_at`, `pdf_url` (signed, "valid for up to 15 minutes", null when unlinkable), and an `accounts[]` array with `account_id`, `account_type`, `opening_balance`, `closing_balance`, `total_credits`, `total_debits`, `total_fees`, and for credit statements `repayment_date`, `spending`, `repayments`, `cashback`.

Invoicing (`invoicing:read`): customers with `legal_name`, `email`, `cc_emails[]`, full postal `address`, `note`, `total_revenue`, `created_at`, `updated_at`, `deleted_at`, `last_invoice_id`; invoices with number, status, due dates, amounts, and `file_id` for the PDF. Sandbox sample customer record: `{"address":{"address1":"77 Broadway","city":"Boston","country":"USA","state":"MA","zip_code":"02109"},"cc_emails":["billing@orbitmedia.co","cfo@orbitmedia.co"],"email":"accounts@orbitmedia.co","legal_name":"Orbit Media Group",...}`. **This is third-party PII belonging to the customer's customers, reachable by an LLM client under a single scope checkbox, and the help center never mentions it.**

### 7.3 What the agent cannot do

Help center, `What connected AI tools have access to in your Rho account`, verbatim list of prohibitions: "Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account." Plus: "AI connections are read-only and cannot perform actions on your behalf."

Product page footnote, verbatim: "Rho API access tokens are read-only and scoped to account and transaction data. Tokens cannot initiate payments or modify accounts, and can be revoked at any time. The Rho API is read-only today."

The read-only property is structural rather than policy-based: there simply are no non-GET operations in v1. That is the strongest single security statement in this whole surface, and it is verifiable from the OpenAPI index rather than taken on trust.

Launch-blog forward statement [Rho claim], verbatim: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval, the finance tasks you'd rather delegate. Read ships first because everything else stands on it." So write tools are an announced direction, and the current safety story is explicitly temporary. The comparison blog says the same in flatter language: "Write endpoints and webhooks are planned but are not currently available."

---

## 8. Limits

| Limit | Value | Source and caveat |
| --- | --- | --- |
| Per API Access Token | approximately 60 requests per minute | Rate-limits doc. Stated to apply "uniformly across all public Rho API endpoints". Whether one MCP `tools/call` equals one request is never stated |
| Per source IP | approximately 600 requests per minute | Aggregated across all tokens sharing the IP |
| Enforcement character | "distributed edge network, so the limits are approximate rather than an exact concurrency allowance" | Clients "must not assume that exactly 60 simultaneous requests will succeed" |
| Pacing guidance | "Pace traffic steadily below one request per second" | Rate-limits doc |
| Over-limit response | `429 Too Many Requests` with `Retry-After`. If positive integer, wait that many seconds; if `0`, use exponential backoff with jitter | Rate-limits doc |
| Page sizes | accounts 100 max, transactions 100 max, statements 100 max, cards default 20 (1 to 100), invoices default 20, customers default 20 | Per-operation reference pages |
| Cursor rules | `page_token` is bound to the exact endpoint, filters, and sort order. Changing any of them mid-iteration returns `400 Bad Request`. Cursors are not durable bookmarks | Pagination doc |
| Statement PDF URL | signed, valid up to 15 minutes, re-fetch `GET /statements/{id}` for a fresh one | Statements doc |
| Transaction and invoice file URLs | "fresh, short-lived signed download URL", to be followed immediately **without an Authorization header**, never persisted | Transactions and Invoicing reference |
| Active tokens | 20 per business | Auth doc |
| IP allowlist entries | 100 per token | Auth doc |
| Token max lifetime | 1 year; auto-expiry after 45 days of inactivity | Auth doc |
| OAuth access token | 15 minutes; refresh 30 days rolling; grant 1 year | Partner-auth doc |
| Protocol | JSON-RPC batches rejected; protocol versions before 2025-06-18 rejected | MCP doc |
| Webhooks | None. "Not yet" in Rho's own comparison table | Comparison blog |
| Sandbox for MCP | None (404) | Live probe |
| Deprecation notice | "at least 15 days' notice" before any v1 deprecation or sunset | Versioning doc |

Practical consequence of the rate limit for an agent: at 100 transactions per page and roughly 60 requests per minute, a full-year pull of a busy account (say 30,000 transactions) is 300 sequential tool calls, about 5 minutes of wall clock at the cap, and 300 tool results in the model's context. Nothing in the MCP doc addresses aggregation, summarization, or server-side rollups, so every analytical question is answered by dragging raw ledger rows through the model.

---

## 9. Coverage: how much of the API, and how much of Rho, does MCP reach?

### 9.1 MCP versus the REST API

Per the versioning doc, parity is 1:1 and total: 14 of 14 operations, 5 of 5 scopes. **On its own terms, MCP coverage of the v1 API is 100%.** That is an unusually clean claim and it is credible precisely because the API is so small.

What MCP adds beyond REST: nothing functional. No aggregate tools, no `search_all`, no "cash summary" prompt, no server-side analytics. The MCP layer is a protocol adapter, not a product.

What MCP loses relative to REST: no visible schema documentation (the REST side has 14 published reference pages plus an OpenAPI spec; the MCP side publishes nothing), no sandbox to test against, and no published error contract.

### 9.2 The REST API versus the Rho product

This is where the real coverage number lives. Rho's platform spans checking, savings, treasury, corporate cards, expense management, bill pay, invoicing, capital, incorporation, and accounting integrations. The API reaches five read surfaces.

| Rho product area | API/MCP coverage |
| --- | --- |
| Account balances and types | Full read (5 account types) |
| Transaction ledger | Full read, 33 transaction types, rich filters |
| Statements and statement PDFs | Full read |
| Corporate cards (metadata, limits, controls) | Read only, last 4 only |
| Invoicing (AR customers and invoices) | Full read |
| Bill Pay / AP (vendors, bills, approvals) | **No endpoints** |
| Expense management (receipts, policies, coding, reimbursements) | **No endpoints.** Transaction `note` and `attachments` are the only trace |
| Users, roles, departments, labels, custom fields | **No endpoints.** `user_id` and `user_full_name` appear on transactions with no user directory to resolve them |
| Payments of any rail (ACH, wire, check, transfer) | **No endpoints** by design |
| Card issuance, lock, limit changes | **No endpoints** by design |
| Treasury positions, trades, yields | Visible only as `investment` account balances and `treasury_*` transaction types |
| Capital (credit line, draws, repayments) | Visible only as `credit` accounts and `credit_repayment*` transactions |
| Rewards and cashback | `rewards` account balance, `credit_cashback`, `rewards_accrual`, `rewards_cashback_redemption` transaction types, `cashback` on credit statements |
| Disputes | Explicitly absent: "A refund or credit is not by itself a dispute, v1 exposes no dispute indicator" |
| Webhooks and events | Absent, planned |
| Audit log of API or agent activity | **Nothing documented anywhere** |

So: MCP covers 100% of a v1 API that covers perhaps a quarter of the platform, and none of the write surface. An agent connected over MCP is a very well-informed read-only analyst with no hands.

### 9.3 What an agent can actually do with it

Well supported, using only documented fields:

- Balance and cash-position questions across all accounts in one `listaccounts` call (up to 100 accounts per page).
- Burn and runway from `listtransactions` windowed on `posted_after`/`posted_before` with `status=settled`.
- Vendor and merchant spend rollups via `counterparty_name` plus `search` (free text across `counterparty_name`, `memo`, `note`).
- Per-employee and per-card spend via `user_id` and `card_id` filters (both accept repeats).
- Refund and credit analysis via `transaction_type=card_refund` and `card_credit` against `account_type=credit`.
- Month-end reconciliation against statement `closing_balance`, `total_credits`, `total_debits`, `total_fees`.
- AR aging from invoices filtered on `status`, `due_date_after`, `due_date_before`.
- Card hygiene review: unused cards, limits near exhaustion via `current_spend` vs `spending_limit`, merchant-control audits.
- Document retrieval: statement PDFs and transaction attachments through short-lived signed URLs.

Traps an agent will hit, all documented and none mentioned on the MCP page:

- `id` is not unique per row. "the entries of one money movement can share an `id`", so naive dedupe by `id` silently drops a leg. Correct unit is `money_movement_id`, or `id` plus `account_id`.
- Filters must stay constant across pagination, or the cursor 400s. An agent that "refines the query" mid-walk restarts from scratch.
- `posted_at` is nullable regardless of status and `v1` guarantees no status transition order.
- Amounts are signed integers in minor units. A model that treats `amount.amount` as dollars is wrong by 100x.
- `sort_by`/`order` exist on lists but ordering on invoices "is not user-configurable".
- Account list has no server-side `account_type` filter; the client must filter after fetching.
- Statement `account_id` filtering selects whole statement documents, and the returned PDF "may include additional accounts belonging to the authenticated business". An agent asked for one account's statement can surface another account's data.
- `awaiting_approval` means no funds have moved, and a model summarizing "payments made" that counts those rows will overstate outflows.

Third-party build examples, all [Rho claim] from the launch blog:

- Seve Ortale, Wayve Payments: AI finance dashboard in about five hours (auto-categorization, burn and runway, AI CFO chat, weekly board summaries) using a Genspark-powered agent wired to the API.
- Ishan Sheth, Joinergo: spend-tracking built "entirely through Rho's MCP connection to Claude", per-person and go-to-market spend, acquisition cost per demo.
- Justin Hays, Arbor Management: bookkeeping automation joining Rho and QuickBooks through a self-built MCP server, a weekly "bookkeeping skill" replacing 3 to 5 hours a week of work.

---

## 10. Live probe evidence, 2026-09-11

All probes unauthenticated except where noted. Times are from response `date` headers.

| # | Request | Result |
| --- | --- | --- |
| 1 | `GET https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` | 200, JSON reproduced in 4.4, `content-length: 294` |
| 2 | `GET https://rhoapi.rho.co/.well-known/oauth-protected-resource` | 200, host-level variant reproduced in 4.4 |
| 3 | `GET https://rhoapi.rho.co/.well-known/oauth-authorization-server` | 404 |
| 4 | `GET https://rhoapi.rho.co/.well-known/oauth-protected-resource/api/v1` | 404 `page not found` |
| 5 | `POST https://rhoapi.rho.co/mcp/v1` with a valid `initialize` JSON-RPC envelope, protocolVersion `2025-06-18`, no Authorization | 401, `content-type: application/problem+json`, body `{"status":401,"title":"Unauthenticated","type":"2"}` |
| 6 | Same with `Authorization: Bearer rhobat_invalidtoken` | Identical 401 body |
| 7 | `GET https://rhoapi.rho.co/mcp/v1` with `Accept: text/event-stream` | Identical 401 body |
| 8 | `POST https://rhoapi-sandbox.rho.co/mcp/v1` with `Authorization: Bearer sandbox` and a valid `initialize` | 404, `content-type: text/plain`, body `default backend - 404` |
| 9 | `GET https://rhoapi-sandbox.rho.co/.well-known/oauth-protected-resource/mcp/v1` | 404 `default backend - 404` |
| 10 | `GET https://rhoapi.rho.co/mcp` and `GET https://rhoapi.rho.co/mcp/v1/` | 404 each |
| 11 | `GET https://auth.rho.co/.well-known/oauth-authorization-server` | 200, metadata analyzed in 4.3, no `registration_endpoint` |

Earlier capture in the corpus (`mcp/prod-401.txt`, dated 2026-09-11 23:28:52 UTC) shows the full 401 header set, including the discovery pointer:

```
www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"
```

Three findings from the probes that contradict or extend the docs:

1. **The MCP server implements RFC 9728 discovery correctly**, returning `WWW-Authenticate` with a `resource_metadata` pointer on 401. That is real MCP-authorization-spec behavior, not a marketing claim, and it means a spec-compliant client will find `auth.rho.co` on its own. It will then fail at registration (no DCR).
2. **The 401 body is not RFC 9457 conformant.** `{"status":401,"title":"Unauthenticated","type":"2"}` sets `type` to the string `"2"`, not a URI. The auth doc promises `"type": "about:blank"` and a `detail` field. Neither appears. So the "same error behavior as the REST API" claim is already false at the first error an MCP client will hit.
3. **There is no MCP sandbox.** The getting-started doc sells a sandbox that "accepts any non-empty bearer token, so you do not need to create a real API Access Token before testing", but that host serves no `/mcp/v1`. To try the MCP server at all, an Owner or Admin must mint a production token against live company money data. That is a real onboarding-safety gap and it is stated nowhere.

---

## 11. Security implications of connecting a finance account to an LLM client

### 11.1 What is genuinely strong

- **Read-only is architectural, not policy.** Fourteen GET operations, no writes in the spec, five `*:read` scopes and no `*:write` scopes anywhere in the live protected-resource metadata. A leaked token or a hijacked agent cannot move money through this surface. Rho's framing ("a leaked token cannot move money") is accurate today.
- **Admin-gated minting with 2FA**, mandatory expiry with a one-year ceiling, 45-day inactivity expiry, 20-token cap, optional 100-entry IP allowlist, immediate irrevocable revocation. This is a better token regime than most fintech APIs.
- **PAN, CVC, and expiry are never returned.** Card data exposure is capped at last 4 plus cardholder name.
- **File URLs are short-lived and never embedded in list responses**, which limits how much durable secret material sits in a model transcript.
- **OAuth consent is Owner/Admin only, one business per grant, revocable immediately from Settings, then API, then Linked Apps.**

### 11.2 What is genuinely risky, and mostly undiscussed by Rho

1. **Prompt injection through the ledger.** `memo`, `note`, `counterparty_name`, invoice fields, customer `note`, and PDF contents are all attacker-influenceable text that flows straight into a model's context. Anyone who can send the business a $0.01 ACH, issue an invoice, or be paid by the business can plant instructions in a field that a finance agent will read verbatim. Rho's tools cannot act on those instructions, but the agent's *other* tools can: email, Slack, a shell, a write-capable payments MCP from another vendor. Rho's documentation contains zero mentions of prompt injection, content sanitization, provenance marking, or untrusted-content handling. Its own MCP safety checklist for finance teams (in the comparison blog) covers scopes, rotation, IP allowlists, approval gates, idempotency, audit logs, webhook signatures, and output validation, and still never names injection. This is the largest unaddressed risk in the whole surface.
2. **Read-only is not leak-proof.** The data reachable under five checkboxes includes every counterparty the company pays, per-employee spend, cardholder names and billing addresses, masked account and routing numbers, wire IMAD/OMAD and ACH trace numbers, full statement PDFs, and AR customer names, emails, and addresses. That is a complete financial and partial-PII picture of the business and, via Invoicing, of its customers. Uploading it to a third-party LLM client is a data-processing decision, not a convenience toggle, and neither the help center nor the MCP doc frames it that way.
3. **The documented Claude Code command puts a long-lived bearer secret in a project file.** `claude mcp add --scope project` writes to the project-scoped MCP config (`.mcp.json`), which is the file teams check into git. The header value is the raw `rhobat_` token. Rho's own auth guide says: "Store tokens in a secret manager, never in source control, CI logs, or shared documents." The MCP page's only snippet violates Rho's own best-practice page. A safer form would use `--scope user` or an environment-variable reference, and Rho documents neither.
4. **IP allowlisting, the control Rho markets hardest, does not fit the MCP use case.** Laptops roam, and a hosted client such as claude.ai egresses from the vendor's infrastructure, not the customer's. The allowlist is useful for a warehouse sync job and close to useless for an AI client. Marketing copy that pairs "connect Claude" with "optional IP allowlists" invites a false sense of control.
5. **No dynamic client registration means the OAuth path is effectively Claude-only.** Every other MCP client is pushed onto the static-token path, which is the weaker of the two credentials (long-lived, up to one year, no per-session consent, no 15-minute rotation). The architecture nudges non-Claude users toward the higher-risk option.
6. **No audit surface.** Nothing in the corpus describes a log of which tool an agent called, when, from where, or how much data it pulled. There is no audit API, no "last used" field documented on tokens beyond the 45-day inactivity mechanic, and no per-connection activity view. By contrast Rho's own blog notes that Brex's MCP records actions "as being performed by the MCP client on behalf of the authenticated identity" [Rho claim about a competitor]. Rho documents no equivalent. For a regulated finance function, "we cannot show what the agent read" is a material gap.
7. **Signed URLs are unauthenticated bearer links.** The transactions guide says to follow the download URL "straight away, without an Authorization header". Any such URL that lands in a chat transcript, a log, a screenshot, or a shared conversation is a live credential to a statement or receipt for its lifetime (15 minutes for statements, unspecified for transaction and invoice files). No TTL is published for the transaction and invoice file URLs at all.
8. **Rate limits are not a data-exfiltration control.** 60 requests per minute at 100 rows per page is 6,000 transactions per minute. A curious or compromised agent can drain the entire ledger in minutes, and nothing documented detects or alerts on that pattern.
9. **The safety story is explicitly temporary.** Rho's launch blog promises "money movement with your approval" next. Every "read-only by design" assurance in the help center and on the product page is scoped to today. Teams that approve the connector on the strength of "it cannot move money" should expect that property to change, and no versioning or notice policy covers a *capability* addition (the 15-day notice policy covers deprecations, and new operations are explicitly "additive" and therefore non-breaking, meaning write tools could appear in `/mcp/v1` without a version bump).
10. **Weak-PKCE advertisement.** `auth.rho.co` advertises `code_challenge_methods_supported: ["plain","S256"]`. A client that picks `plain` gets no meaningful PKCE protection. The docs mandate S256 but the server does not appear to.
11. **Undocumented grants.** The AS advertises `implicit`, `client_credentials`, and device-code grants that no Rho documentation describes. Undocumented auth paths on a finance authorization server are worth a question to Rho.
12. **No status-page coverage.** `status.rho.co` (captured 2026-09-11 19:13 ET) lists five components: Web Application, Mobile Application, Corporate Cards, Bank Payments, Notifications. There is no API component and no MCP component, so an agent workflow silently depending on `/mcp/v1` has no public health signal.

### 11.3 Practical hardening checklist for a team connecting this

1. Mint a dedicated token per agent client, never reuse the warehouse token (Rho's own advice: "Issue one token per integration").
2. Grant the minimum scopes. In particular, leave `invoicing:read` off unless AR analysis is the point, because it carries third-party PII, and leave `cards:read` off unless card analysis is the point, because it carries employee names and addresses.
3. Prefer the OAuth connector path where the client supports it (15-minute access tokens, per-business consent, revocable from Settings, then API, then Linked Apps) over a one-year static token.
4. If you must use a static token, use a user-scoped or environment-referenced MCP config, not `--scope project`, and set the shortest workable expiry rather than the one-year maximum.
5. Treat every string field that originates outside the company (`memo`, `counterparty_name`, `note`, invoice and customer fields, PDF text) as untrusted input to the model, and do not let the same agent session hold Rho read tools and any money-moving or message-sending tool.
6. Rotate before expiry (create, deploy, then revoke), and rehearse revocation: revoke a test token and confirm the client actually breaks.
7. Re-verify scope and capability after any Rho release, because additive changes, including potentially new tools, ship into v1 without a version bump.

---

## 12. Contradictions, stale statements, and conspicuous omissions

### 12.1 Contradictions found across the corpus

| # | Contradiction | Pages |
| --- | --- | --- |
| 1 | Auth guide lists 3 scopes; OpenAPI security block and live PRM list 5 (`cards:read`, `invoicing:read` missing from the auth guide) | `docs/v1/auth` vs `api/v1/openapi` vs live `/.well-known/oauth-protected-resource/mcp/v1` |
| 2 | Getting started: "Current release is read-only and covers accounts and transactions." The published API also covers statements, cards, and invoicing | `docs/v1/getting-started` vs the 14 reference pages |
| 3 | OpenAPI description: "accounts, cards, **payments**, and the transaction ledger". There are no payment endpoints, and everything else insists the API cannot move money | `api/v1/openapi` vs product page footnote |
| 4 | `site-llms-full.txt` line 35: Rho API is "Programmatic access to accounts, **payments**, and card data". Same overclaim in Rho's own machine-readable summary | `site-llms-full.txt` vs `site-llms.txt`, which correctly says read-only |
| 5 | Site navigation labels the product "Rho API New Banking **and payments** via API" on every page footer nav | all core pages vs the read-only footnote on the same pages |
| 6 | MCP doc promises REST-identical error behavior; the live 401 body is `{"status":401,"title":"Unauthenticated","type":"2"}`, which is neither the documented shape nor RFC 9457 conformant (`type` must be a URI) | `docs/v1/mcp` and `docs/v1/auth` vs live probe |
| 7 | Token settings path: product page says Settings, then Configurations, then Access Tokens; help center and the OpenAPI `tokenUrl` (`https://app.rho.co/settings/access-tokens`) say Settings, then API, then Access Tokens | `product/api` vs help center |
| 8 | MCP page's only snippet stores a long-lived secret in a project-scoped config, contradicting the auth guide's "never in source control" | `docs/v1/mcp` vs `docs/v1/auth` |
| 9 | Getting-started sells a permissive sandbox as the way to test before minting a token; the sandbox has no MCP endpoint | `docs/v1/getting-started` vs live probe |
| 10 | Partner-auth documents Authorization Code with PKCE S256 only; the AS also advertises implicit, client_credentials, device_code, and `plain` PKCE | `docs/v1/partner-auth` vs live AS metadata |
| 11 | Help center says AI tools can access "Account balances, Transactions, Statements"; the live scope list also includes cards and invoicing | help center `Connecting AI tools` vs live PRM |
| 12 | OpenAPI declares the security scheme `Type: oauth2` with `Token URL: https://app.rho.co/settings/access-tokens`, which is a settings page, not a token endpoint. The real token endpoint is `https://auth.rho.co/oauth2/token` | `api/v1/openapi` vs `docs/v1/partner-auth` |

### 12.2 What the MCP doc conspicuously does not say

Precise omissions from `docs/v1/mcp`, each of which a client operator would need:

1. No tool names. Not one.
2. No tool input schemas, output schemas, or examples. No `tools/list` sample response.
3. No prompt names, arguments, or examples, despite a section titled "Tools and Prompts".
4. No resource URIs, MIME types, or subscription semantics, despite claiming resources exist.
5. No tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`), which is exactly the metadata that would let a client enforce the read-only promise mechanically.
6. No statement of how `page_token` cursors and the 100-row page caps surface through tool calls, or whether the server aggregates pages for the agent.
7. No statement of whether MCP calls consume the same 60-requests-per-minute token budget, and no MCP-specific rate limit.
8. No error catalogue for the MCP transport: no JSON-RPC error codes, no mapping from the REST 401/403/429 model onto JSON-RPC responses.
9. No sandbox or test path for MCP, and no acknowledgement that the documented sandbox host does not serve `/mcp/v1`.
10. No mention of the RFC 9728 protected-resource metadata document that the server actually publishes, nor of the `WWW-Authenticate` discovery pointer it returns.
11. No mention of whether dynamic client registration is supported (it is not), which silently blocks the generic OAuth path.
12. No client list beyond Claude Code. No Claude Desktop config, no Cursor, no VS Code, no ChatGPT, no Codex CLI, no generic `mcpServers` JSON block.
13. No session semantics: `Mcp-Session-Id`, resumability, `Last-Event-ID`, SSE stream lifetime, keepalives, timeouts.
14. No `server/discover` request or response example, for a method the doc itself introduces.
15. No security guidance whatsoever: no prompt-injection warning, no advice on scope minimization for agent connections, no guidance on where to store the token, no warning about signed URLs in transcripts.
16. No audit or observability story: no log of tool calls, no per-connection activity view, no alerting.
17. No data-residency, retention, or subprocessor statement for data that flows to an LLM vendor.
18. No versioning of the MCP endpoint independent of the API (`/mcp/v1` tracks `/api/v1`), and no statement about whether new tools (including future write tools) can appear inside `/mcp/v1` without notice. Read against the versioning policy, they can, because additions are non-breaking.
19. No multi-entity guidance for MCP (one business per connection is documented only in the help center, for Claude).
20. No performance characteristics: no timeouts, no maximum response size, no guidance on how large a `listtransactions` result can get in model context.

### 12.3 Reference data carried through for the dossier

Transaction type enum, 33 values, verbatim from `api/transactions_listtransactions.md` and `api/transactions_gettransaction.md`:

`card_credit`, `card_debit`, `card_refund`, `credit_repayment`, `credit_repayment_refund`, `credit_cashback`, `ach_credit`, `ach_debit`, `ach_return`, `wire_in`, `wire_out`, `wire_fee`, `international_wire_in`, `international_wire_out`, `check_deposit`, `check_payment`, `internal_transfer`, `savings_deposit`, `savings_withdrawal`, `savings_interest`, `treasury_deposit`, `treasury_withdrawal`, `treasury_fee`, `treasury_interest`, `treasury_maturity`, `treasury_sale`, `treasury_market_value_adjustment`, `rewards_accrual`, `rewards_cashback_redemption`, `adjustment_credit`, `adjustment_debit`, `international_wire_fee`, `international_wire_fee_refund`

Account type enum: `checking`, `credit`, `investment`, `savings`, `rewards`.
Transaction status enum: `pending`, `settled`, `failed`, `awaiting_approval`.
Card spending-limit types: `daily`, `weekly`, `monthly`, `quarterly`, `annual`, `fixed`, `single_use`. Calendar resets are computed in Eastern Time (America/New_York); `annual` resets on the anniversary of when the limit took effect.

---

## 13. Competitive framing, all [Rho claim]

From `product/api`, with the page's own footnote "Competitive data collected from Mercury, Brex, and Ramp websites as of 2026-08-20, and may change":

| Dimension | Rho | Mercury | Brex | Ramp |
| --- | --- | --- | --- | --- |
| Programmatic access | Read-only accounts and transactions | Balances and transactions via REST | Transactions API: transactions, accounts, statements | Transactions endpoints for spend visibility |
| AI assistant / MCP | Native Claude connection plus an MCP guide in the developer docs | Native MCP server, read-only for AI tools | "No MCP or AI-assistant integration documented on developer.brex.com" | Three documented MCP servers |
| Can API tokens move money? | "No, by design" | "Yes, the API can initiate ACH transfers" | "Yes, the Payments API sends ACH, domestic wires, and checks" | "Yes, write operations include bill creation, payment execution, and card issuance" |
| Token security | Scoped, revocable, optional IP allowlists, Owner/Admin only | Scoped tokens, fine-grained permissions, IP allow-listing | Admin-created, scoped at creation, expire after 90 days unused | OAuth 2.0 with granular permission scopes |
| Public docs | docs.rho.co (REST reference, MCP guide, rate limits) | docs.mercury.com | developer.brex.com (10 REST APIs) | docs.ramp.com (OpenAPI published) |

Note the internal tension: the same page's comparison table says Brex has no documented MCP, while Rho's own ranking blog (`blog/best-banking-apis-for-business`) says Brex ships a "first-party MCP, early access" whose permissions are inherited from the authenticated user or service account. Both are Rho pages. The blog is the more recent and more detailed treatment; the product-page table is the weaker claim.

From the ranking blog, Rho's self-assessment [Rho claim]: "Rho wins the ranking. First-party, read-only MCP access to accounts, transactions, and statements, without giving an AI agent the ability to move money." And the honest counterweight, also Rho's own words: "Mercury's API is the most mature overall (read and write) ... If you want agents moving money today, those do more."

From `blog/best-banks-for-ai-startups`: "Only one platform in this comparison has a banking MCP server for AI agents" (contradicted three lines later in the same article, which describes Mercury's and Ramp's MCP surfaces, and by the ranking blog's nine-platform MCP table). Treat the "only one platform" line as marketing shorthand for "only one read-only first-party banking MCP among the seven compared".

---

## 14. As-of date register

| Fact | As-of date |
| --- | --- |
| Rho API product-page capabilities | "current as of August 2026" (page footnote) |
| Competitive API comparison (Mercury, Brex, Ramp) | 2026-08-20 |
| Rho API entry in `site-llms.txt` | 2026-08-01 |
| Launch blog "Introducing Rho API" | published 2026-07-29, last updated 2026-09-01 |
| Mercury write-capable API verification | 2026-08-02 |
| Ramp hosted MCP with write actions | ramp.com/support, 2026-08-02 |
| Live MCP endpoint probes in this file | 2026-09-11, 23:38 to 23:39 UTC |
| Prior corpus captures of `/mcp` metadata | 2026-09-11, 23:28 to 23:29 UTC |
| Status page component list | 2026-09-11 19:13:30 ET |
| OpenAPI document version | 1.0.0, API version `v1` |

---

## 15. Open questions to resolve with Rho

1. What are the literal MCP tool names, and what is the transform from operationId (prefix? casing? namespace?)? The doc promises they never change but never prints one.
2. What prompts and resources does the server actually expose? Are statement and invoice PDFs exposed as MCP resources, and if so, under what URI scheme?
3. Do MCP tool calls share the 60-requests-per-minute token budget, or is there a separate MCP budget?
4. Does the MCP server paginate on the agent's behalf, or does the agent drive `page_token` cursors itself?
5. What is `server/discover`, and where is it specified?
6. Is there any audit log of MCP tool calls available to the customer, and does the 45-day inactivity clock treat an MCP call as activity?
7. Will write tools appear inside `/mcp/v1` under the additive-only policy, and will customers get notice before an agent connection gains write capability?
8. What is the TTL on transaction and invoice file download URLs (statements are documented at 15 minutes, the others only as "short-lived")?
9. Why is there no MCP sandbox, and is one planned?
10. Is dynamic client registration planned for `auth.rho.co`, or is "linked apps" permanently limited to hand-registered partners?
11. Why does the MCP 401 emit `"type":"2"` instead of an RFC 9457 type URI?
12. Are the advertised `client_credentials`, `implicit`, and device-code grants actually enabled for the Rho API audience, and if so, why are they undocumented?
