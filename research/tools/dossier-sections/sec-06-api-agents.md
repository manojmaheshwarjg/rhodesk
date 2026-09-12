## 6. The API and the agent surface

Everything in this section is as of 2026-09-11. It is the executive view: what Rho shipped, what the pieces mean, and where the wall is. The mechanics (every field of every response, the cursor pagination rules that govern how a client walks a long list one page at a time, the error contract, the sandbox probe logs, the client code) live in the separate Rho API reference document that accompanies this dossier. If you never open that document, this section is designed to leave you with an accurate picture anyway.

### 6.1 What shipped, and when

Rho had an API in private beta before 2026. The public launch has two dates, five days apart, because Rho announced it twice.

| Date | Artifact | What it said |
| --- | --- | --- |
| 2026-07-29 | Blog, "Introducing: The Rho API" (last updated 2026-09-01) | "Today, we're bringing the Rho API out of beta" |
| 2026-08-03 | Product changelog entry | "Read-only is live today. Write access and webhooks are next." |

**Rho says** the API is available to every customer with no waitlist and no approval step, at no additional cost, and that "Most financial APIs predate agents; MCP got bolted on. This one shipped with its MCP server in production. Not a roadmap item, the architecture."

**Verified:** the API exists, the documentation is public at docs.rho.co, the OpenAPI specification is published (the machine-readable file describing every endpoint, which code generators read), the production MCP endpoint responds, and a sandbox with fictional data answers unauthenticated-in-practice requests. I exercised all 14 operations against the sandbox directly.

### 6.2 The whole surface fits in one table

There are 14 operations. All 14 are GET, the HTTP verb that only retrieves data and never changes it. They cover 5 resources.

| Resource | Operations | What you get |
| --- | --- | --- |
| Accounts | 2 (list, get one) | Name, type (checking, credit, investment, savings, rewards), balance, and the last 4 of the account and routing number on 8 of the 14 sandbox accounts (the other 6, all credit and rewards accounts, carry neither) |
| Cards | 2 (list, get one) | Cardholder name, last 4, physical or virtual, status, spending limit and limit period, current and pending spend, billing and shipping address, merchant-category allow and block lists |
| Transactions | 3 (list, get one, get an attached file) | 33 transaction types, signed amounts, status, counterparty name, employee and card attribution, memo and note text. A `tracking_number` field carrying the ACH trace or wire IMAD/OMAD reference is documented in detail but returned on zero of the sandbox's 72 transactions |
| Statements | 2 (list, get one) | Period, opening and closing balance, total credits, debits and fees, and a signed PDF link valid for about 15 minutes |
| Invoicing | 5 (customers list and get, invoices list and get, invoice file) | Customer legal name, email, cc emails, postal address, lifetime revenue; invoice number, status, dates, amounts |

For scale, the public sandbox holds 14 accounts, 8 cards, 72 transactions, 33 statements, 7 invoicing customers and 12 invoices of fictional data. That is the whole test corpus.

A scope is a named permission string attached to a credential, checked before the request reaches the handler. There are five, one per resource, all ending in `:read`: `accounts:read`, `transactions:read`, `statements:read`, `cards:read`, `invoicing:read`.

**Verified:** five scopes, confirmed independently of the docs from Rho's public OAuth metadata document at `https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1`, which lists all five.

**Assessment:** the documentation understates its own product in two places, and both errors point the same way. Rho's Authentication guide at /docs/v1/auth still lists only three scopes in its "scopes available today" table, omitting `cards:read` and `invoicing:read`. Rho's Getting Started page still says the release "covers accounts and transactions" when the reference ships five resources. Anyone sizing the blast radius of a token from the Authentication page alone will underestimate it by the entire Cards and Invoicing surface, which includes employee cardholder names and the postal addresses and emails of the customer's own customers. That is a documentation defect, not a security hole, but it is the kind of defect that matters most: the page a security reviewer reads is the page that is wrong.

There is also no sub-scope granularity. `transactions:read` means the entire ledger for the entire business, for all time. There is no per-account scope, no date-window scope, no amount ceiling, no field redaction.

### 6.3 Two ways to hold a credential

**API Access Tokens (the `rhobat_` model).** A long-lived opaque secret scoped to one business, created in Rho's settings by an Account Owner or Admin behind a two-factor challenge, shown exactly once. It looks like `rhobat_` followed by 62 hex characters. A business may hold at most 20 active tokens. Expiration is mandatory at creation with a one-year maximum, and a token also dies automatically after 45 days of no use. An optional IP allowlist (up to 100 entries) rejects requests from anywhere else. Revocation is immediate and irreversible. No other authentication method is supported: no cookies, no API keys, no signed requests.

**Partner OAuth.** OAuth is the standard "sign in with" mechanism: instead of handing a third-party app your password, you approve it at Rho's own login screen and the app receives a short-lived token limited to what you approved. For a third-party application acting on behalf of Rho customers, Rho runs an OAuth 2.0 authorization server at auth.rho.co using the Authorization Code flow with PKCE (a standard technique that stops an intercepted authorization code from being redeemed by an attacker), method S256. Access tokens expire after 15 minutes, refresh tokens rotate on every use and last 30 days on a rolling basis, and the underlying customer grant lasts one year before re-approval is required. Only Account Owners and Admins can approve a connection, and one business can hold at most one active grant per app.

**Verified:** auth.rho.co's authorization-server metadata document publishes no `registration_endpoint`, and under RFC 8414 the absence of that field is how a server signals it does not offer dynamic client registration. A registration attempt recorded in an earlier probe pass returned "Dynamic registration is not enabled"; that `POST` was not re-sent for this document, because writing to a production authorization server is not a metadata read. Dynamic client registration is the mechanism by which a generic client self-registers with an authorization server it has never met.

**Assessment:** this is the single most consequential undocumented fact about the developer surface. Every OAuth client must be hand-registered by emailing api-partner-request@rho.co with a logo, redirect URIs, a privacy policy and a terms-of-service link. The generic MCP authorization flow that arbitrary clients implement therefore cannot complete against Rho. That is why Rho's own documentation hedges with "Linked-app availability depends on the client" and why every marketing page names Claude as "the natively supported client today." In practice a non-Claude client gets the static token path or nothing. Note that this is a business decision as much as a technical one: gating registration is how Rho keeps a list of who is reading its customers' bank data, which is a defensible posture for a regulated-adjacent company, but it does mean "works anywhere MCP does" is stronger marketing than the auth server supports.

### 6.4 MCP, and Rho's MCP server

If you have not met it: the Model Context Protocol (MCP) is an open convention, introduced by Anthropic in late 2024 and now implemented broadly, for letting an AI assistant call someone else's software. A company runs an "MCP server" that advertises a list of tools, each with a name, a description and a typed input schema. An AI client connects, reads the list, and from then on the model can decide to call `listTransactions` the way a person would click a button, feeding the result back into its own reasoning. The value is that the company writes the integration once instead of once per assistant, and the user connects by authorizing a connector rather than by writing code. The risk is symmetrical: whatever the tools can do, an AI acting on ambiguous instructions can now do too.

Rho's MCP server runs in production at `https://rhoapi.rho.co/mcp/v1` over Streamable HTTP (one HTTP endpoint, JSON-RPC messages in a simple request-and-reply format, optional streamed responses). Rho states parity is one-to-one with REST, the ordinary web API that serves the same endpoints: the same 14 operations, the same five scopes, the same error behavior, with tool names derived from the frozen operation identifiers so that "tool names will never change." Rho is listed in Anthropic's connector directory, so a Claude user connects by searching for Rho, signing in, picking a business and approving scopes.

**Claude Code setup**, the only code snippet on Rho's MCP page, reproduced exactly:

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

**Verified:** the command works. `--scope project` writes the literal token, in plaintext, into `.mcp.json`, the project config file whose entire purpose is to be committed to version control and shared with a team.

**Assessment:** put Rho's two pages side by side. The Authentication guide: "Store tokens in a secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, 1Password, etc.), never in source control, CI logs, or shared documents." The MCP guide's only copy-paste command: writes a bearer token valid for up to a year into the file designed for git. The page with the command is the one people will follow. The fix is trivial (use `--scope user`, or a `${RHO_API_TOKEN}` placeholder in single quotes resolved from the environment) and Rho does not mention it.

Two further gaps are worth stating plainly. First, Rho publishes no tool list, no input schemas and no prompt or resource inventory for the MCP server, telling you instead to introspect it yourself with your client or MCP Inspector. It simultaneously promises the tool names are frozen forever and declines to tell you what they are. Second, **verified by direct probe: the sandbox host has no MCP endpoint. `POST https://rhoapi-sandbox.rho.co/mcp/v1` returns 404.** MCP exists only in production, so the first time you connect an agent to Rho over MCP, it is connected to real money data.

### 6.5 Rate limits

| Limit | Value |
| --- | --- |
| Per API Access Token | Approximately 60 requests per minute |
| Per source IP | Approximately 600 requests per minute, pooled across all tokens on that IP |
| Over-limit response | `429 Too Many Requests` with a `Retry-After` header; if `Retry-After` is 0, use exponential backoff (wait, then wait twice as long, and so on) |
| Guidance | "Pace traffic steadily below one request per second" |
| Page sizes | Default 20 and maximum 100 on all six list endpoints, measured. Rho's own reference pages state only the max for accounts, transactions and statements, and only the default for cards and invoicing |

**Verified:** I issued roughly 430 requests to the sandbox over about ten minutes, including a 150-request burst on one token inside 57 seconds and a 65-request burst on a brand-new token inside 11 seconds. Every response was `200`. No limit was enforced and no `429` was reachable. Separately, none of the 14 operation reference pages documents a `429` response at all; they document 200, 400, 401, 403, 500 and 503, plus 404 on the eight single-object operations.

**Assessment:** two practical consequences. You cannot test your retry code against Rho's own test environment, because the sandbox will not produce the error the docs tell you to handle. And a code generator fed Rho's OpenAPI document produces a client with no `429` case, which you must add by hand. The limits themselves are unremarkable for a read API, but they do shape agent behavior: pulling a year of a busy ledger at 100 rows per page and 60 requests per minute is roughly 300 sequential calls and several minutes of wall clock, with every raw row passing through the model's context, because Rho offers no server-side aggregation, summary or rollup tool.

### 6.6 The capability boundary

This is the part to remember. Every write answer is no, and it is no structurally rather than by policy: there are no non-GET operations in v1 to call.

| Can a connected agent... | Answer | Notes |
| --- | --- | --- |
| Read account balances and types | Yes | All accounts in one call, up to 100 per page |
| Read the full transaction ledger | Yes | 33 transaction types, all history, rich filters |
| Read card metadata and controls | Yes | Last 4 only; the full card number, the CVC security code and the expiry date are never returned |
| Read statements and fetch statement PDFs | Yes | Via short-lived signed links |
| Read invoicing customers and invoices | Yes | Includes third-party customer names, emails and addresses |
| Move money (ACH, wire, check, transfer) | **No** | No endpoint exists |
| Issue, lock, edit or cancel a card | **No** | No endpoint exists |
| Add, remove or manage users | **No** | No endpoint exists |
| Approve a payment or a bill | **No** | No Bill Pay or approvals endpoints at all |
| Receive a webhook (a push notification from Rho when something happens) | **No** | Rho's own comparison table says "Not yet" |
| Read an audit log of its own API activity | **No** | Nothing documented anywhere |

Rho's help center states the boundary in four words per line: connected AI tools cannot "Move money. Issue, lock, or edit cards. Add or manage users. Make changes to your Rho account." The product page footnote, as of August 2026: "The Rho API is read-only today."

**Assessment:** the read-only claim is unusually credible because it is verifiable from the published OpenAPI index rather than taken on trust. It is also explicitly temporary. The launch blog: "Today your agent reads Rho. Next, it acts on Rho: workflows, money movement with your approval, the finance tasks you'd rather delegate. Read ships first because everything else stands on it."

One boundary the read-only design does not cover: read-only protects Rho, not the agent's environment. A finance agent typically also holds email, Slack, a shell or a write-capable MCP server from another vendor, and Rho's transaction `memo`, `note` and `counterparty_name` fields are free text that arrives from outside. Rho's documentation contains no mention of prompt injection (an attacker writing instructions into a field such as a payment memo, in the hope the AI reading it treats them as commands) or untrusted-content handling.

### 6.7 Where Rho sits on the agentic-banking timeline

Rho's framing is that MCP is now table stakes and Rho shipped it as architecture rather than as an afterthought. The dates below are all confirmed against primary sources.

| Date | Who | What |
| --- | --- | --- |
| 2025-03-25 | Ramp | First MCP release (an open-source Python package, not the hosted server buyers connect to today) |
| 2025-05-29 | Griffin | "The Agentic Bank": an agent can "open accounts, make payments, and analyse historic events." UK PRA/FCA-authorised, not US. Sandbox-only at announcement ("For now, agent access is limited to our sandbox environment") and still listed as beta in September 2026 |
| 2025-08-20 | Narmi and Grasshopper | Announced as the first MCP server by a US bank. Read-only, and a controlled beta at launch with general availability planned for Q4 2025 |
| 2025-09 | Coinbase | MCP server, read and write, can make payments |
| 2025-11 | Mercury | MCP server, read-only |
| 2026-04 | Brex | MCP server, roughly 41 tools (~37 read, 4 low-risk write), no money movement |
| 2026-04 | Meow | Agent-initiated payments, behind an initiator-and-approver workflow |
| 2026-04-09 | Nymbus | 19 tools including money movement, sold to US banks and credit unions |
| 2026-07-01 | Navan | MCP server, read-only |
| 2026-07-14 | Grasshopper | First bank listed in Anthropic's connector directory. Read-only, no money movement |
| 2026-07-29 | Rho | "Introducing: The Rho API" |

**Verified:** the openbankingtracker first-party directory, read live on 2026-09-11, lists 10 bank or banking-platform MCP servers worldwide: 5 live and 5 in beta, 5 read-write and 5 read-only, with 4 able to make payments (Griffin, Coinbase, Meow, Slash). That is against roughly 4,000-plus US banks and a similar number of credit unions. Rho does not appear in that directory at all.

**Verified, and the most important line in this section:** no vendor offers ungated autonomous money movement. Every money-moving agent surface in the field is wrapped in a narrower primitive: Ramp's Agent Cards are scoped to a merchant and an amount, Stripe attaches a `human_confirmation` object to its execute and refund tools, and Meow routes agent payments through an initiator-and-approver workflow.

**Assessment:** the "table stakes" framing holds within Rho's own competitive cohort and only there. Against startup banking and spend management (Mercury, Brex, Ramp, Meow, Slash, Navan, Coinbase), every named comparator shipped MCP before Rho and roughly half now support some write, so Rho is late on both date and surface. Against US banking at large, 10 servers against thousands of institutions is not table stakes by any reading, and Rho is not even on the list that counts them. What Rho is genuinely not behind on is agentic payments, because nobody has solved that: the frontier is gated, scoped, human-approved money movement, not autonomy.

One caution for anyone using Rho's own materials: Rho's comparison table on rho.co/product/api, dated "as of 2026-08-20," claims Brex has "No MCP or AI-assistant integration documented on developer.brex.com." Brex's changelog dates its MCP server to April 2026, and Rho's own blog five days later, on 2026-08-25, reverses the claim. Do not cite Rho's competitive table as evidence for anything.

### 6.8 Why read-only is a defensible choice

Taken on its merits, the case is strong.

The blast radius of a leaked credential is bounded by physics rather than by policy. A stolen `rhobat_` token reads everything and moves nothing, and that property survives a bug in Rho's own authorization logic, because the write code path does not exist. Rho's own framing is honest about this: "a leaked token cannot move money."

It also sidesteps the hardest unsolved problem in the category. An agent that can move money needs an approval model, an idempotency model (so a retried instruction does not pay a vendor twice), a limits model, a reversal path and an audit trail that a regulator will accept. Shipping reads first and getting the data model right, then building writes on top, is the order a careful team would choose. Every competitor that does support writes has arrived at the same conclusion in practice by wrapping them in gates.

And it lowers the cost of saying yes. Because nothing can be broken, Rho can give API access to every customer with no waitlist, no approval step and no fee, which is materially more open than banking APIs that gate access behind a partnership review.

### 6.9 What it costs

The bill comes due in four places.

**Automation stops at the read boundary.** The natural next sentence after "our AWS spend is up 40%" is "so freeze that card," and the agent cannot. Every workflow terminates in a human opening the Rho dashboard. That is a real ceiling on the "delegate the finance busywork" promise the launch blog makes.

**No webhooks means no event-driven anything.** Without a push notification when a transaction posts, every integration is a polling loop against a 60-requests-per-minute budget. Alerting, reconciliation triggers and approval routing all become scheduled jobs with latency measured in minutes.

**Coverage of the platform is thin, not just the verbs.** Read access reaches five resources. Bill Pay and accounts payable, expense management, receipts and coding, users and roles, departments, treasury positions, capital draws and disputes have no endpoints at all. Transactions carry a `user_id` and a `user_full_name` with no user directory to resolve them against. So even as a pure read API, this is perhaps a quarter of the product.

**Competitively, read-only is the weaker half of a two-sided pitch.** Rho's differentiation is that it runs banking, cards, payables and receivables on one ledger (covered in the product and business-model sections above). An agent that can read all of that at once is genuinely useful and is Rho's best agentic story. But Mercury's API initiates ACH transfers, Brex's Payments API sends ACH, wires and checks, and Ramp's API creates bills, executes payments and issues cards, all facts Rho itself lists in its own comparison table. Rho turns that gap into a security feature, which is a legitimate move and probably the right one for a company its size. It is still a gap, and the moment Rho ships gated writes, the security argument it is making today becomes an argument against its own roadmap.
