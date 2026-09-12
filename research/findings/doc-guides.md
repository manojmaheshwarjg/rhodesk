# Rho Developer Platform: Core Guides Digest (docs.rho.co)

Scope: faithful technical digest of the six core guide pages at `docs.rho.co`, read in full from the local corpus.

Primary sources (all local, all Rho-authored, all marketing-adjacent but technically normative):

| Source file | Page |
| --- | --- |
| `rho/docs/docs_v1_getting-started.md` | `/docs/v1/getting-started` |
| `rho/docs/docs_v1_auth.md` | `/docs/v1/auth` |
| `rho/docs/docs_v1_partner-auth.md` | `/docs/v1/partner-auth` |
| `rho/docs/docs_v1_versioning.md` | `/docs/v1/versioning` |
| `rho/docs/docs_v1_pagination.md` | `/docs/v1/pagination` |
| `rho/docs/docs_v1_rate-limits.md` | `/docs/v1/rate-limits` |

Corroborating / cross-checking sources used for contradictions and gaps:
`rho/docs/api_v1_openapi.md`, `rho/docs/docs_v1_mcp.md`, `rho/api/*.md` (14 operation refs), `rho/sandbox/*.json` + `*.headers` (live captures, 2026-09-11 23:22 GMT), `rho/pages/core/product__api.txt`, `rho/pages/help/help-center__the-rho-api__*.txt`, `rho/site-llms.txt`.

Everything below is Rho's own documentation. It is authoritative for Rho's contract but self-asserted. Claims about third parties are flagged `[Rho claim]`.

---

## 1. Environments, base URLs, surfaces

| Surface | Base URL | Notes |
| --- | --- | --- |
| REST production | `https://rhoapi.rho.co/api/v1` | Version in the URL path. Getting started: "The API is published as **`v1`**, served under `/api/v1/`." |
| REST sandbox | `https://rhoapi-sandbox.rho.co/api/v1` | "fictional, deterministic data" |
| MCP production | `https://rhoapi.rho.co/mcp/v1` | From `docs_v1_mcp.md`; Streamable HTTP |
| OAuth authorization server | `https://auth.rho.co` | Partner auth only |
| OAuth discovery | `https://auth.rho.co/.well-known/openid-configuration` | "for OAuth libraries that support discovery" |
| Token management UI | `https://app.rho.co/settings/access-tokens` | From the OpenAPI `AccessToken` security scheme `Token URL` |
| Partner onboarding | `api-partner-request@rho.co` | Email-only, human-reviewed registration |

Release posture, verbatim from getting started: "Current release is **read-only** and covers accounts and transactions."

OpenAPI `Version: 1.0.0`. Servers block lists exactly Production and Sandbox as above.

Cross-surface conventions declared in `api_v1_openapi.md`: "Errors follow [RFC 9457 problem details]"; "timestamps are ISO 8601 UTC"; "monetary amounts are integers in the smallest currency unit."

### First call, verbatim (getting started)

Three steps, verbatim:

1. **Create an API Access Token** from your Rho banking settings. Admins and Account Owners have permission to manage API Access Tokens, and creation is protected by a 2FA challenge - see [Authentication](/docs/v1/auth) for the full lifecycle.
2. **Send the token as a bearer credential** on every request: `Authorization: Bearer <rho_api_access_token>`.
3. **Walk paginated responses** using the cursor returned in each page - see [Pagination](/docs/v1/pagination).

Minimal first call (verbatim):

```bash
curl https://rhoapi.rho.co/api/v1/accounts \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

Sandbox call (verbatim):

```bash
curl https://rhoapi-sandbox.rho.co/api/v1/accounts \
  -H "Authorization: Bearer sandbox"
```

"The sandbox accepts any non-empty bearer token, so you do not need to create a real API Access Token before testing requests there."

---

## 2. Direct customer authentication: API Access Tokens

Definition, verbatim: "An API Access Token is a long-lived, opaque secret scoped to a single business - the same token continues to work as people on your team come and go."

Token binding is to the **business**, not the user. This is the single most important structural fact: no user identity travels with the token, and staff turnover does not invalidate it.

### 2.1 Creation controls

Two gates, verbatim:

- "The fact that only **Account Owners** and **Admins** can manage API Access Tokens."
- "A **2FA challenge** at the moment of creation."

Note the word "manage" (not merely "create"): the same two roles govern the whole token lifecycle including revocation.

### 2.2 Creation-time fields (verbatim table)

| Field | Notes |
| --- | --- |
| **Name** | A human-readable label that appears in the token list |
| **Scopes** | One or more permissions the token grants (see [Scopes](#scopes)). |
| **Allowed IPs** | Optional IP allowlist. If set, requests from any other source IP are rejected. Up to 100 entries per token. |
| **Expiration** | Required. Maximum one year. |

Hard numbers: IP allowlist capped at **100 entries per token**; expiration is **required** with a **maximum of one year**. No minimum expiration is stated. No statement about whether scopes, name, or allowed IPs can be edited after creation.

### 2.3 Secret handling and format

- "The raw token is **shown only once**, immediately after creation. There is no way to recover the secret later."
- Advice: "copy it into your secret manager before closing the dialog, and never commit it to source control."
- Prefix: `rhobat_` ("Tokens created in Rho banking settings use the `rhobat_` prefix").
- Documented example, verbatim:

```
rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f
```

Measured: the example's hex body is **62 characters** (69 including the `rhobat_` prefix). 62 hex characters is 31 bytes, not a round 32. Rho never states the token length as part of the contract, and the versioning guide's "Treat IDs as opaque strings" / "Store IDs as-is" obligations argue against relying on it. Treat the example as illustrative, not as a length spec.

The `rhobat_` phrasing ("Tokens created in Rho banking settings use the `rhobat_` prefix") implies at least one other token family exists with a different prefix. The OAuth guide never states a prefix for partner access tokens. There is no published prefix taxonomy.

### 2.4 Quantity and lifetime limits

| Limit | Value | Exact wording |
| --- | --- | --- |
| Active tokens per business | **20** | "A business can hold at most **20 active tokens** at a time. If you need more, revoke unused ones first." |
| Maximum expiration | **1 year** | "Expiration \| Required. Maximum one year." |
| Inactivity expiry | **45 days** | "API Access Tokens also expire automatically after **45 days of inactivity**." |
| What resets inactivity | A successful authenticated request | "A successful authenticated API request counts as activity." |
| Inactivity clock for unused tokens | Starts at creation | "For tokens that have never been used, the 45-day window starts at creation." |

Two independent expiry clocks run concurrently: the chosen expiration date (max 1 year) and the rolling 45-day inactivity timer. A token dies at whichever comes first. Note "successful authenticated" is the qualifier: a request that 401s or 403s is not documented as refreshing the clock, and a 429 is not addressed at all.

### 2.5 Transport of the credential

Verbatim HTTP example:

```http
GET /api/v1/transactions HTTP/1.1
Host: rhoapi.rho.co
Authorization: Bearer rhobat_4f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f
Accept: application/json
```

Verbatim curl:

```bash
curl https://rhoapi.rho.co/api/v1/transactions \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

Exclusivity clause, verbatim: "No other authentication header (cookie, API key, signed request) is supported."

Sandbox, verbatim:

```bash
curl https://rhoapi-sandbox.rho.co/api/v1/transactions \
  -H "Authorization: Bearer sandbox"
```

"Sandbox authentication is intentionally permissive so you can test API shapes against fictional data without creating a production API Access Token."

Practical consequence: the sandbox cannot be used to test authentication behavior, scope enforcement, IP allowlist rejection, or 401/403 handling. Only shapes.

### 2.6 Scopes

Format and enforcement point, verbatim: "Scopes follow a `resource:action` format and are enforced before your request reaches the handler. A request whose token lacks the required scope is rejected with `403 Forbidden`."

Scopes listed in the **auth guide** (verbatim table):

| Scope | Description |
| --- | --- |
| `accounts:read` | Read account information for the business. |
| `transactions:read` | Read transactions the business has access to. |
| `statements:read` | Read statements for the business's accounts. |

"The required scope for each endpoint is listed under its **Security** section in the [API reference](/api/v1/openapi)."

**Contradiction (documented scope inventory).** `rho/docs/api_v1_openapi.md`, security scheme `AccessToken`, lists **five** scopes, two of which the auth guide omits:

| Scope | In auth guide? | OpenAPI description |
| --- | --- | --- |
| `accounts:read` | Yes | Read access to business accounts information |
| `cards:read` | **No** | Read access to business cards information |
| `invoicing:read` | **No** | Read access to Invoicing information |
| `statements:read` | Yes | Read access to business statements information |
| `transactions:read` | Yes | Read access to business transactions information |

The OpenAPI catalogue also exposes Cards (`GET /cards`, `GET /cards/{id}`) and Invoicing (5 operations) endpoints, and the local sandbox captures include populated `cards.json`, `invoicing_customers.json`, and `invoicing_invoices.json`. So the auth guide's scope table is **stale relative to the shipped API**. Getting started is stale in the same direction: it says the release "covers accounts and transactions" while the reference covers accounts, cards, transactions, statements, and invoicing.

Additional oddity in the OpenAPI security block: the `AccessToken` scheme is declared `Type: oauth2` with `Token URL: https://app.rho.co/settings/access-tokens`, which is a browser settings page, not an OAuth token endpoint. The real OAuth token endpoint is `https://auth.rho.co/oauth2/token` per the partner guide. The scheme conflates the two credential models.

Help-center cross-reference on what scopes gate (`help-center__the-rho-api__what-connected-al-tools-have-access-to-in-your-rho-account.txt`): "Scopes are defined at token creation (see a) or at OAuth consent (see b)"; connected tools can read Accounts (details, types, balances), Transactions (card transactions, ACH and Wire transfers, refunds), Statements; and cannot "Move money", "Issue, lock, or edit cards", "Add or manage users", "Make changes to your Rho account."

### 2.7 The 401 vs 403 distinction

Error media type, verbatim: "Authentication and authorization failures are returned as [`application/problem+json`](https://www.rfc-editor.org/rfc/rfc7807) documents".

Verbatim table:

| Status | When it happens |
| --- | --- |
| `401 Unauthorized` | Missing `Authorization` header, malformed token, unknown token, revoked token, or expired token. |
| `403 Forbidden` | Token is valid but does not carry the scope required by the endpoint, or the request came from an IP outside the token's allowlist. |

Decomposed:

| Condition | Status | Category |
| --- | --- | --- |
| No `Authorization` header | 401 | credential absent |
| Malformed token | 401 | credential unparseable |
| Unknown token | 401 | credential not recognized |
| Revoked token | 401 | credential killed |
| Expired token (either clock) | 401 | credential lapsed |
| Valid token, missing required scope | 403 | credential good, permission insufficient |
| Valid token, source IP not on allowlist | 403 | credential good, context disallowed |

The line is "is this credential currently a credential at all" (401) versus "this credential is real but may not do this, from here" (403). The IP allowlist violation landing in 403 rather than 401 is the notable choice: it tells a caller holding a leaked token that the token itself is live, which is arguably an information leak but is useful for operators debugging egress IP drift.

Verbatim problem-details body:

```json
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Token is revoked or has expired"
}
```

Note the `detail` string deliberately merges revoked and expired into one message, so a client cannot distinguish the two from the response body.

**Contradiction (RFC citation).** The auth guide cites **RFC 7807** for `application/problem+json`. The API reference overview (`api_v1_openapi.md`) cites **RFC 9457**. RFC 9457 obsoletes RFC 7807; the field set is compatible, so this is a citation inconsistency rather than a behavioral one.

Problem-details field shape, from every operation reference (`rho/api/*.md`, identical for 400, 401, 403, 500, 503):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | required | A URI reference that identifies the problem type. Example: `about:blank` |
| `title` | string | required | A short, human-readable summary of the problem type. |
| `status` | integer | required | The HTTP status code. |
| `detail` | string | optional | A human-readable explanation specific to this occurrence of the problem. |

`type` is documented only with the value `about:blank`, meaning there is **no machine-readable error taxonomy**: clients must branch on HTTP status, never on `type`. There are no `instance`, `code`, `errors[]`, or `request_id` fields.

### 2.8 Revocation

Verbatim: "Tokens can be revoked at any time from the same settings screen used to create them. Revocation is **immediate**: the next request made with that token will return `401 Unauthorized`. There is no grace period and no way to un-revoke - issue a new token instead."

"If you believe a token has leaked, revoke it and notify Customer Support."

Revocation is a **UI-only operation**. There is no documented API endpoint to create, list, inspect, or revoke API Access Tokens. Programmatic key rotation is therefore impossible for direct customers; rotation requires a human in the Rho console.

### 2.9 Rotation and best practices (verbatim)

- **Store tokens in a secret manager** (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, 1Password, etc.) - never in source control, CI logs, or shared documents.
- **Issue one token per integration.** Separate tokens make it possible to revoke a single integration without disturbing the others, and make audit logs easier to interpret.
- **Grant the narrowest scopes** that the integration actually needs.
- **Set an IP allowlist** when the calling system has a stable egress range. This blocks the token from being used outside your infrastructure even if the secret leaks.
- **Rotate before expiration.** Create the replacement token, deploy it, and only then revoke the old one to avoid downtime.

The documented rotation pattern is overlap-then-revoke: create, deploy, revoke. Combined with the 20-active-token cap, an operator running 20 integrations cannot rotate without first dropping to 19.

---

## 3. Partner authentication: OAuth 2.0

Purpose, verbatim: "Partner Authentication lets your application access the Rho API on behalf of Rho customers using **OAuth 2.0**."

Flow and server, verbatim: "Rho uses the standard **Authorization Code flow with PKCE**. The authorization server is `https://auth.rho.co`."

Decision rule, verbatim: "If you are building an internal integration for your own account, you don't need OAuth - use an [API Access Token](/docs/v1/auth) instead."

### 3.1 Client registration (manual, email-gated)

"OAuth clients are registered by Rho. To onboard as a partner, email the following details to `api-partner-request@rho.co`:"

Verbatim table:

| Field | Notes |
| --- | --- |
| **Client / app name** | Shown to customers on the consent screen. |
| **Company name** | Your legal entity name. |
| **Logo** | Your app's logo image. Shown on the consent screen. |
| **Redirect URI(s)** | All URIs you need, production, development, local. |
| **Requested scopes** | The scopes your app needs, e.g. `accounts:read transactions:read offline_access` (see [Scopes](/docs/v1/auth#scopes)). |
| **Privacy policy URI** | Linked from the consent screen. |
| **Terms of Service URI** | Linked from the consent screen. |
| **Support / contact email** | Used for operational and security notices about your integration. |

"After review, Rho registers your OAuth client and sends you your `client_id` and `client_secret`. Treat the secret like a password: store it in a secret manager and never share it with anyone."

There is no self-service client registration, no dynamic client registration endpoint, and no stated review SLA. `offline_access` is introduced here as a scope; it does not appear in the auth guide's scope table nor in the OpenAPI security scheme.

### 3.2 Step 1: authorization request (verbatim)

```bash
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

Parameter contract, verbatim:

| Parameter | Rule |
| --- | --- |
| `response_type` | always `code` |
| `client_id` | issued during onboarding |
| `redirect_uri` | must exactly match a registered redirect URI |
| `scope` | space-separated subset of your registered scopes. Include `offline_access` if you need refresh tokens |
| `state` | an opaque value your app verifies on the redirect back |
| `code_challenge`, `code_challenge_method` | required. PKCE with `S256` |
| `audience` | the Rho API your app will call: `https://rhoapi.rho.co` |

PKCE with `S256` is **required**, not optional, and `plain` is not offered. `audience` is an Auth0/Ory-style extension parameter, not core OAuth 2.0; its value is the API origin `https://rhoapi.rho.co` (no `/api/v1` path). The sample is labeled as a `bash` block but is an HTTP request line with whitespace and newlines inside the query string, which are presentational only.

### 3.3 Step 2: consent

Verbatim: "The customer signs in to Rho, selects the business they want to connect, and grants the requested access on the consent screen. Only Account Owners and Admins can perform this action."

"A business can have at most one active grant per app - approving again updates the existing connection."

The business selection step means one customer identity can authorize any of several businesses; the grant is business-scoped, matching the API Access Token model. Grant uniqueness is **one per (business, app)** and re-consent is an update, not a second grant. Corroborated by help center: "Only Account Owners and Administrators can authorize an OAuth connection for their business."

### 3.4 Step 3: redirect back (verbatim)

```text
https://yourapp.example.com/callback?code=<authorization_code>&state=<opaque_state>
```

"Verify that `state` matches the value you sent. Authorization codes are single-use and expire after a few minutes."

"If the customer declines, or has no business where they are allowed to approve integrations, the redirect carries `error=access_denied` instead of a code."

Both the decline case and the not-authorized-for-any-business case collapse to the same `error=access_denied`, so a partner app cannot distinguish "user said no" from "user lacks the Owner/Admin role anywhere". Code lifetime is stated only as "a few minutes", never as an exact number.

### 3.5 Step 4: code exchange (verbatim)

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

Token response (verbatim):

```json
{
  "access_token": "<access_token>",
  "token_type": "bearer",
  "expires_in": 900,
  "refresh_token": "<refresh_token>",
  "scope": "accounts:read transactions:read offline_access"
}
```

`expires_in: 900` seconds = 15 minutes, consistent with the prose. `token_type` is lowercase `bearer`. Client authentication here is HTTP Basic (`client_secret_basic`).

### 3.6 Step 5: calling the API (verbatim)

```bash
curl https://rhoapi.rho.co/api/v1/transactions \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Identical transport to a direct API Access Token. The resource server does not distinguish credential families at the header level.

### 3.7 Step 6: refresh (verbatim)

```http
POST /oauth2/token HTTP/1.1
Host: auth.rho.co
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=<refresh_token>
```

"Refresh tokens are **single-use and rotate on every refresh**: each response includes a new refresh token, and the old one stops working. Persist the new token immediately."

**Inconsistency inside the same page:** the code-exchange sample carries `Authorization: Basic <base64(client_id:client_secret)>`, but the refresh sample has **no** `Authorization` header and no `client_id`/`client_secret` form fields. Rho never says whether refresh is a public-client call or whether the Basic header was simply omitted from the sample. A confidential client should assume Basic auth is still required and test it; the doc as written is ambiguous.

### 3.8 OAuth lifetimes (verbatim numbers)

| Artifact | Lifetime | Wording |
| --- | --- | --- |
| Authorization code | "a few minutes", single-use | "Authorization codes are single-use and expire after a few minutes." |
| Access token | **15 minutes** (`expires_in: 900`) | "Access tokens expire after **15 minutes**." |
| Refresh token | **30 days**, rolling, single-use, rotating | "Refresh tokens last **30 days** on a rolling basis - each refresh starts a new 30-day window." |
| Grant | **1 year** | "The grant itself lasts **1 year**; after that the customer must re-approve your app." |

"All `auth.rho.co` endpoint URLs are also published at `https://auth.rho.co/.well-known/openid-configuration` for OAuth libraries that support discovery."

A partner that refreshes at least once every 30 days keeps access alive for up to one year with no user interaction, then must re-drive consent. An app idle for more than 30 days must re-consent early.

### 3.9 OAuth revocation (verbatim)

```http
POST /oauth2/revoke HTTP/1.1
Host: auth.rho.co
Content-Type: application/x-www-form-urlencoded

token=<access_or_refresh_token>&
client_id=<your_client_id>&
client_secret=<your_client_secret>
```

"Customers can also disconnect your app from their Rho business settings. Customer revocation is **immediate** and invalidates all tokens for the grant, including refresh tokens - your next API request returns `401 Unauthorized`. Handle this gracefully by sending the customer through the [authorization flow](#authorization-flow) again."

Note the third client-auth style on this page: the revoke endpoint puts `client_id` and `client_secret` in the **form body** (`client_secret_post`), while the code exchange uses Basic. No `token_type_hint` parameter is documented.

Customer revocation surfaces to the partner as a plain `401`, indistinguishable from an expired or malformed token. The prescribed remedy is re-consent.

### 3.10 Direct customer auth vs partner auth, side by side

| Dimension | API Access Token (`/docs/v1/auth`) | OAuth partner token (`/docs/v1/partner-auth`) |
| --- | --- | --- |
| Intended user | Internal integration for your own business | Third-party app acting for Rho customers |
| Issuer | Rho banking settings UI, self-service | Rho staff register the client; tokens minted by `auth.rho.co` |
| Onboarding | Immediate, in-product | Email `api-partner-request@rho.co`, human review, no stated SLA |
| Credential | Opaque bearer, `rhobat_` prefix | OAuth access token (prefix not documented) + refresh token |
| Who authorizes | Account Owners and Admins | Account Owners and Admins (consent screen) |
| Second factor | **2FA challenge at creation** | Not stated; consent is a login plus approval |
| Scope selection | Chosen per token at creation | Registered set, narrowed per authorization request; adds `offline_access` |
| Binding | One business | One business per grant, chosen at consent |
| Access lifetime | Up to 1 year, plus 45-day inactivity expiry | 15 minutes |
| Renewal | None; create a new token manually | Refresh token, rotating, 30-day rolling window |
| Ceiling | 20 active tokens per business | One active grant per (business, app); grant lasts 1 year |
| IP allowlist | Yes, optional, up to 100 entries | **Not documented** |
| Revocation by holder | UI only, immediate, irreversible | `POST /oauth2/revoke`, programmatic |
| Revocation by customer | Same UI | Disconnect in business settings; immediate; kills all grant tokens |
| PKCE | N/A | Required, `S256` |
| Failure after revocation | `401 Unauthorized` | `401 Unauthorized` |
| Sandbox support | Yes, any non-empty bearer | **No sandbox authorization server documented** |

MCP maps onto both: "**Direct connections** require an API Access Token in `Authorization: Bearer <rho_api_access_token>`" and "**Linked apps** use the OAuth connection provided by the MCP client, without requiring users to configure an API Access Token manually. Linked-app availability depends on the client." (`docs_v1_mcp.md`)

---

## 4. Versioning and compatibility contract

Framing, verbatim: "This page is the stability contract for the Rho API. It states what may change in a released version, what may not, and the notice you can expect before anything is deprecated."

### 4.1 Model

- "The Rho API is versioned per release; today that's the URL path `/api/v1`. The current version is `v1`."
- "**`v1` is stable and additive-only**. A request that works today keeps working. Changes that would break existing code require a **new API version**; we do not ship them into `/api/v1`."
- "Any `v1` deprecation or sunset comes with **at least 15 days' notice** before the change takes effect."

Versioning is by **URL path only**. There is no version header, no date-pinned version, no `Accept` media-type versioning, and no per-account version pinning. A future `v2` is therefore a separate path; `v1` callers are never migrated implicitly.

15 days is a short deprecation window by industry norms and applies to "any `v1` deprecation or sunset". The channel for that notice is not stated (email, changelog, response header, all unspecified). No changelog URL appears anywhere in the six guides.

### 4.2 Change classification (verbatim, exhaustive as published)

Non-breaking, may ship into `v1` at any time:

- A new enum value.
- A new nullable response field.
- A new optional query parameter.

Breaking, requires a new API version:

- Removing or renaming an enum value.
- Changing a field's type.
- Removing a response field.
- Making an optional field required.

(Listed above in the page's own order: removing/renaming an enum value; removing a response field; changing a field's type; making an optional field required.)

| Change | Classification | Ships into `v1`? |
| --- | --- | --- |
| Add enum value | Non-breaking | Yes |
| Add nullable response field | Non-breaking | Yes |
| Add optional query parameter | Non-breaking | Yes |
| Remove or rename enum value | Breaking | No, new version |
| Remove response field | Breaking | No, new version |
| Change field type | Breaking | No, new version |
| Make optional field required | Breaking | No, new version |

Not classified anywhere on the page: adding a **non-nullable** response field; adding a **required** query parameter; adding a new endpoint (presumably additive); removing an endpoint; changing pagination defaults or maxima; tightening rate limits; changing error `detail` strings; changing sort defaults; changing the meaning of an existing enum value without renaming it. The list of breaking changes is short enough that these silences matter: a caller cannot tell from this page whether a `page_size` maximum drop from 100 to 50 is breaking.

### 4.3 Client obligations (verbatim)

- **Handle unknown enum values gracefully.** A value set grows as Rho adds new products and rails, so a field such as `transaction_type` can return a value your code has not seen before. Give any `switch` on it a default case so a new value shows up as unknown rather than an error.
- **Handle new response fields gracefully.** Ignore fields you do not recognize rather than failing to parse the response, so a field added later never breaks deserialization.
- **Treat IDs as opaque strings.** Do not parse structure out of an `id` or assume a fixed format; use it only as a whole value to look records up and reference them.
- **Store IDs as-is.** Persist the full string exactly as returned, without assuming a fixed length or layout.

Practical reading: strict deserializers (e.g. Rust `serde` with `deny_unknown_fields`, Java Jackson with `FAIL_ON_UNKNOWN_PROPERTIES`, non-defaulted enum mapping in Kotlin/Swift/Go generated clients) will break on additive changes. The enum obligation bites hard given how large the shipped enums already are: `cards.status` alone has 11 values (`printing`, `shipped`, `out_for_delivery`, `activate_card`, `delivery_canceled`, `active`, `expiring`, `locked`, `canceled`, `suspended`, `expired`), `accounts.account_type` has 5 (`checking`, `credit`, `investment`, `savings`, `rewards`), and `invoices.status` has 6 (`paid`, `unpaid`, `cancelled`, `overdue`, `confirm_payment`, `pending_payout`). The ID obligation is enforceable against database schema choices: no fixed `VARCHAR(n)` assumptions.

### 4.4 MCP parity clause (verbatim)

"The MCP server is 1:1 with the REST API, so the `/mcp/v1` tool schemas follow the same policy as the REST contracts above: additive-only, with breaking changes requiring a new version. One policy covers both surfaces."

"Tool *names* derive from the frozen `v1` operationIds, so **tool names will never change**. You can reference them explicitly in workflows, agent skills, and saved automations without them breaking."

"Tool *descriptions* are not part of the contract - they may be improved at any time to help agents use the tools well, and such changes are never treated as breaking."

This is a notably strong commitment: tool names are pinned to frozen operationIds and "will never change". The visible operationIds in the reference index are `listaccounts`, `getaccount`, `listcards`, `getcard`, `listtransactions`, `gettransaction`, `gettransactionfile`, `liststatements`, `getstatement`, `listinvoicingcustomers`, `getinvoicingcustomer`, `listinvoicinginvoices`, `getinvoicinginvoice`, `getinvoicinginvoicefile` (14 operations, per the `.md` filenames of the reference pages). Whether the MCP tool name is exactly the operationId or a derived form ("derive from") is not specified.

MCP protocol versions supported (`docs_v1_mcp.md`): `2026-07-28`, `2025-11-25`, `2025-06-18`. "Versions older than `2025-06-18` and JSON-RPC batches are rejected." "Every non-`initialize` request must include the selected version in the `MCP-Protocol-Version` header." Protocol-version support is not covered by the additive-only clause; dropping `2025-06-18` later would be a breaking change under no stated policy.

---

## 5. Pagination

Model, verbatim: "List endpoints in the Rho API return results in pages using **opaque cursor-based pagination**. You ask for a page size, the response includes the items plus a cursor to the next page, and you follow that cursor to fetch each subsequent page."

Stability claim, verbatim: "Cursors are stable across changes to the underlying data: new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated."

### 5.1 Request parameters (verbatim table)

| Parameter | Type | Notes |
| --- | --- | --- |
| `page_size` | integer | How many items to return. Each endpoint defines its own minimum, maximum, and default - see the [API Reference](/api/v1/openapi). Values outside the allowed range return `400 Bad Request`. |
| `page_token` | string | Opaque cursor returned as `next_page_token` by a previous response. Omit to fetch the first page. |

"Cursors are opaque - pass back exactly the string you received."

"A token returned by one endpoint is only valid for that **same endpoint with the same filters and sort order**. Using a cursor with changed filters or sorting will result in `400 Bad Request`."

### 5.2 What the reference actually publishes for `page_size`

The guide delegates minimum, maximum, and default to the reference. The reference is incomplete and inconsistent across endpoints:

| Endpoint | Documented `page_size` wording | Max | Default | Min |
| --- | --- | --- | --- | --- |
| `GET /accounts` | "Number of accounts per page; max 100" | 100 | not stated | not stated |
| `GET /transactions` | "Number of transactions per page; max 100" | 100 | not stated | not stated |
| `GET /statements` | "Number of statements per page; max 100" | 100 | not stated | not stated |
| `GET /cards` | "Number of cards to return. Defaults to 20." | not stated | 20 | not stated |
| `GET /invoicing/customers` | "Number of customers per page. Defaults to 20." | not stated | 20 | not stated |
| `GET /invoicing/invoices` | "Number of invoices per page. Defaults to 20." | not stated | 20 | not stated |

No endpoint documents all three bounds, and **no endpoint documents a minimum** even though the guide says "Each endpoint defines its own minimum". The older-looking trio (accounts, transactions, statements) publishes a max and no default; the newer-looking trio (cards, invoicing) publishes a default and no max. Since out-of-range values return `400`, a client that guesses `page_size=250` against `/cards` cannot know from the docs whether it will succeed.

Sandbox evidence that the default is 20 on at least the cursor-returning endpoints: the captured `transactions.json` and `statements.json` cursors decode to an inner token `offset:20` (see 5.5) with no `page_size` passed on the request.

Sort parameters exist alongside pagination and are part of the cursor binding: `sort_by` and `order` appear on `/accounts`, `/transactions`, `/statements`, and `/invoicing/customers` (the latter documenting "Sort field. Defaults to created_at when omitted." and "Sort direction. Defaults to desc when omitted."). `/cards` and `/invoicing/invoices` expose no sort parameters; `/invoicing/invoices` states "Results are ordered by creation time, newest first. Ordering is not user-configurable; keep filters unchanged while paginating." `/statements` documents its ordering as "newest close date first".

### 5.3 Response shape (verbatim)

```json
{
  "transactions": [
    { "id": "…", "amount": { "amount": 1299, "currency": "USD" }, "…": "…" },
    { "id": "…", "amount": { "amount": 4500, "currency": "USD" }, "…": "…" }
  ],
  "page": {
    "next_page_token": "eyJvIjoxMDAsImQiOiIyMDI2LTA1LTE0In0"
  }
}
```

"The array key matches the resource being listed (`accounts`, `transactions`, …). The `page.next_page_token` field is either:

- A string - pass it as `page_token` on the next request to fetch the following page.
- `null` - you have reached the last page; there is nothing more to fetch."

Termination is by `null` cursor **only**. There is no `has_more` boolean, no `total_count`, no `prev_page_token`, and no `page.count`. Backwards paging is impossible; total result counts are unavailable without a full walk. Per the operation refs, `page.next_page_token` is marked `(string, required)` with the note "null on the last page", i.e. the key is always present and nullable.

### 5.4 Canonical iteration (verbatim Python)

```python
import os
import requests

def list_all_transactions(account_id: str):
    token = os.environ["RHO_API_TOKEN"]
    page_token = None
    while True:
        params = {"account_id": account_id, "page_size": 100}
        if page_token is not None:
            params["page_token"] = page_token

        resp = requests.get(
            "https://rhoapi.rho.co/api/v1/transactions",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()

        yield from body["transactions"]

        page_token = body["page"]["next_page_token"]
        if page_token is None:
            return
```

Verbatim curl equivalent:

```bash
# First page
curl "https://rhoapi.rho.co/api/v1/transactions?page_size=100" \
  -H "Authorization: Bearer $RHO_API_TOKEN"

# Subsequent page - pass the next_page_token from the previous response
curl "https://rhoapi.rho.co/api/v1/transactions?page_size=100&page_token=eyJvIjoxMDAsImQiOiIyMDI2LTA1LTE0In0" \
  -H "Authorization: Bearer $RHO_API_TOKEN"
```

Observations on Rho's own sample, worth flagging for anyone copying it:
- It sends `page_size=100`, the maximum, on every request. At 60 requests per minute that is a ceiling of 6,000 transactions per minute per token.
- It uses `raise_for_status()`, which throws on `429` with no `Retry-After` handling. The sample directly contradicts the rate-limits guide's retry advice. There is no backoff, no jitter, no sleep, and no pacing anywhere in the example.
- `timeout=30` is the only resilience control present.
- The `account_id` parameter is typed `array` in the reference ("Filter by one or more accounts") but passed as a scalar string here; `requests` will serialize a scalar as a single value, which presumably works, but multi-account filtering syntax is never documented.

### 5.5 Cursor opacity vs observed cursor contents

The docs insist cursors are opaque and that their "format and lifetime are not part of the API contract and may change without notice". They are, however, trivially decodable base64url JSON. From the local live sandbox captures (2026-09-11):

| Source | `next_page_token` | Decodes to |
| --- | --- | --- |
| `rho/sandbox/transactions.json` | `eyJ2IjoxLCJmIjoidDBId1JoSjBCU0dXWUFqQVQ1YlFLZyIsInQiOiJiMlptYzJWME9qSXcifQ` | `{"v":1,"f":"t0HwRhJ0BSGWYAjAT5bQKg","t":"b2Zmc2V0OjIw"}` |
| `rho/sandbox/statements.json` | `eyJ2IjoxLCJmIjoiNl9aQ1ZWOEFrR3M5TjdxSENhaHZwUSIsInQiOiJiMlptYzJWME9qSXcifQ` | `{"v":1,"f":"6_ZCVV8AkGs9N7qHCahvpQ","t":"b2Zmc2V0OjIw"}` |
| Doc sample (pagination guide) | `eyJvIjoxMDAsImQiOiIyMDI2LTA1LTE0In0` | `{"o":100,"d":"2026-05-14"}` |

The inner `t` value `b2Zmc2V0OjIw` base64-decodes to the ASCII string **`offset:20`**.

Three conclusions:

1. The real cursor is an envelope: `v` (envelope version, `1`), `f` (a 22-char base64url value that behaves as a **filter/query fingerprint**, differing per endpoint, which is how Rho detects the "changed filters" case and returns `400`), and `t` (an inner, doubly-base64'd continuation token).
2. On these two endpoints the inner token is a plain **offset**, not a keyset cursor. That is in tension with the guide's stability claim that "new items inserted while you are iterating will not shift existing pages or cause items to be skipped or duplicated." An offset-based continuation over a newest-first ordering does shift under insertion: a row inserted at the head between page 1 and page 2 pushes one row from page 1's tail into page 2, duplicating it. The claim may hold via a snapshot the fingerprint pins, but nothing in the corpus says so, and the observed payload is exactly the shape that classically fails to hold it. Treat the anti-skip/anti-duplicate guarantee as unverified.
3. The documentation's own illustrative cursor (`{"o":100,"d":"2026-05-14"}`, offset 100 plus a date) does not match the live format at all, i.e. it was hand-written.

Sandbox cursors from `accounts.json`, `cards.json`, `invoicing_customers.json`, and `invoicing_invoices.json` are all `null`, meaning those sandbox datasets fit in one page of 20.

### 5.6 Common mistakes (verbatim)

- **Modifying filters between pages.** A `page_token` is bound to the query it was issued for. Change `account_id`, `status`, `sort_by`, etc., and you must start over from the first page.
- **Storing cursors long-term.** Cursors are designed for live iteration, not for bookmarks. Their format and lifetime are not part of the API contract and may change without notice.

Additional pitfalls implied but not spelled out by Rho:
- `page_token` plus a changed `page_size` is not explicitly addressed. `page_size` is not listed among the things that invalidate the cursor ("filters and sort order"), and the curl sample re-sends `page_size=100` on the follow-up request, suggesting it must be re-sent. Whether changing it mid-walk 400s or silently re-pages is undocumented.
- Cursor **lifetime** is never quantified. There is no stated TTL, no documented expiry error, and no guidance on resuming an interrupted walk. "Not for bookmarks" is the only signal.
- There is no incremental-sync primitive. With no `updated_after` filter documented on `/transactions` (only `initiated_after/before` and `posted_after/before`) and no durable cursor, delta sync must be built from timestamp filters plus client-side dedup on `id`.

---

## 6. Rate limits

Preamble, verbatim: "We apply rate limits to keep the Rho API available and responsive for all integrations."

### 6.1 Limits (verbatim table)

| Limit | Threshold |
| --- | --- |
| Per API Access Token | Approximately 60 requests per minute |
| Per source IP | Approximately 600 requests per minute |

"These limits apply uniformly across all public Rho API endpoints. The source-IP limit covers the combined traffic from every integration sharing that IP address, including integrations using different API Access Tokens."

"We enforce rate limits across a distributed edge network, so the limits are approximate rather than an exact concurrency allowance. Clients must not assume that exactly 60 simultaneous requests will succeed."

Derived numbers:

| Quantity | Value |
| --- | --- |
| Per-token budget | ~60 req/min = 1 req/sec = ~86,400 req/day |
| Per-IP budget | ~600 req/min = 10 req/sec |
| Tokens needed to saturate one IP | 10 tokens at full per-token rate |
| Max items/min per token at `page_size=100` | 6,000 |
| Max items/min per IP at `page_size=100` | 60,000 |

The per-IP ceiling is a **shared** pool: co-tenanted integrations behind one NAT gateway or one CI egress IP compete with each other, and an unrelated team's runaway job can 429 yours. This is the strongest argument in the corpus for the auth guide's "Set an IP allowlist" advice cutting both ways: pinning a stable egress IP for security also concentrates rate-limit risk on that IP.

The word "Approximately" appears in both rows, and the distributed-edge caveat means the enforced number can be lower than 60 in practice. There is no documented burst allowance, no token-bucket capacity, and no stated window semantics (fixed vs sliding).

### 6.2 Pacing guidance (verbatim)

"Pace traffic steadily below one request per second instead of sending the full minute's allowance in a burst. Queueing requests and limiting concurrency reduces the chance of crossing a distributed counter while other requests are still in flight."

Read literally, "below one request per second" means the practical sustained rate is **under** 60/min, not 60/min, and concurrency above 1 is discouraged for a single token.

### 6.3 429 handling (verbatim)

"When a limit is exceeded, we return `429 Too Many Requests`. Handle the `Retry-After` header as follows:

- If it is a positive integer, wait at least that many seconds before retrying.
- If it is `0`, we have not applied a fixed cooldown. This does not guarantee that an immediate retry will succeed, so use exponential backoff with jitter instead of retrying in a tight loop."

| `Retry-After` value | Required client behavior |
| --- | --- |
| Positive integer (seconds) | Wait at least that many seconds |
| `0` | No fixed cooldown applied; do **not** retry immediately in a loop; use exponential backoff with jitter |
| Header absent | **Not documented** |
| HTTP-date form | **Not documented** (only integer seconds are described) |

`Retry-After: 0` is a non-standard usage: RFC 9110 defines the header as a delay in seconds or an HTTP-date, and `0` here is repurposed as "no cooldown computed". A client must special-case it rather than sleeping zero and retrying.

### 6.4 What the rate-limit page does not say

- **No rate-limit telemetry headers.** No `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, or RFC 9239 `RateLimit`/`RateLimit-Policy` headers are documented anywhere in the corpus. `Retry-After` on a `429` is the only documented rate-limit signal, so a client cannot see how much budget is left before it is cut off. The live sandbox response headers captured on 2026-09-11 (`rho/sandbox/*.headers`) confirm no rate-limit headers on `200` responses: the full set returned was `date`, `content-type`, `via: 1.1 google`, `cf-cache-status: DYNAMIC`, `referrer-policy`, `strict-transport-security: max-age=63072000; includeSubDomains; preload`, `x-content-type-options: nosniff`, `x-frame-options: DENY`, `server: cloudflare`, `cf-ray`. (`server: cloudflare` plus `via: 1.1 google` corroborates the "distributed edge network" framing: Cloudflare in front of Google Cloud.)
- **`429` is absent from the OpenAPI spec.** Every operation reference in `rho/api/` documents responses `200`, `400`, `401`, `403`, `500`, `503` only. A generated client built from the spec will treat `429` as an unmodeled status.
- **No rate limits stated for OAuth partner access tokens.** The table row says "Per API Access Token". Whether an OAuth-issued access token gets its own 60/min bucket, shares the partner's bucket, or is metered per customer is unstated. For a partner with many customers behind one egress IP, the 600/min IP cap is the binding constraint and it is not addressed.
- **No rate limits stated for the MCP surface** (`/mcp/v1`), nor for the sandbox, nor for `auth.rho.co` token/refresh/revoke endpoints.
- **No `503` guidance.** `503` is in the OpenAPI response list but neither the rate-limits page nor any guide explains it or says whether it is retryable.
- **No request-id / correlation header** documented for support escalation.

---

## 7. Contradictions and inconsistencies found

| # | Contradiction | Sources |
| --- | --- | --- |
| 1 | Scope inventory: auth guide lists 3 scopes (`accounts:read`, `transactions:read`, `statements:read`); OpenAPI lists 5, adding `cards:read` and `invoicing:read`. | `docs_v1_auth.md` vs `api_v1_openapi.md` |
| 2 | Coverage: getting started says the release "covers accounts and transactions"; the reference ships Accounts, Cards, Transactions, Statements, Invoicing (14 operations), and the sandbox returns populated cards and invoicing data. | `docs_v1_getting-started.md` vs `api_v1_openapi.md`, `rho/sandbox/*.json` |
| 3 | `offline_access` is used as a scope in partner auth but appears in neither the auth guide's scope table nor the OpenAPI security scheme. | `docs_v1_partner-auth.md` vs `docs_v1_auth.md`, `api_v1_openapi.md` |
| 4 | Problem-details RFC: auth guide cites RFC 7807; API reference cites RFC 9457 (which obsoletes 7807). | `docs_v1_auth.md` vs `api_v1_openapi.md` |
| 5 | OAuth client authentication style differs across the same page: Basic auth on `/oauth2/token` code exchange, **no** client auth shown on the refresh call, form-body `client_id`+`client_secret` on `/oauth2/revoke`. | `docs_v1_partner-auth.md` |
| 6 | OpenAPI declares the `AccessToken` scheme as `Type: oauth2` with `Token URL: https://app.rho.co/settings/access-tokens`, a human settings page, not the real OAuth token endpoint `https://auth.rho.co/oauth2/token`. | `api_v1_openapi.md` vs `docs_v1_partner-auth.md` |
| 7 | Cursor stability claim ("will not shift existing pages or cause items to be skipped or duplicated") vs observed live cursors whose inner token is literally `offset:20`. | `docs_v1_pagination.md` vs decoded `rho/sandbox/transactions.json`, `statements.json` |
| 8 | The documented example cursor `{"o":100,"d":"2026-05-14"}` does not match the live cursor envelope `{"v":1,"f":...,"t":...}`. | `docs_v1_pagination.md` vs sandbox captures |
| 9 | Pagination guide says each endpoint defines a minimum, maximum, and default `page_size`; no endpoint in the reference documents all three, and none documents a minimum. | `docs_v1_pagination.md` vs `rho/api/*list*.md` |
| 10 | The canonical Python sample calls `raise_for_status()` with no `Retry-After` handling and no pacing, contradicting the rate-limits page's explicit retry guidance. | `docs_v1_pagination.md` vs `docs_v1_rate-limits.md` |
| 11 | Token-creation navigation path differs across Rho's own properties: "Rho banking settings" (auth guide), "Settings → API → Access Tokens" (help center), "Settings, then Configurations, then Access Tokens" (product page), `app.rho.co/settings/access-tokens` (OpenAPI). | `docs_v1_auth.md`, `help-center__the-rho-api__build-a-custom-integration-with-rho.txt`, `pages/core/product__api.txt`, `api_v1_openapi.md` |
| 12 | `429` is fully specified in the rate-limits guide but absent from every operation's response list in the OpenAPI reference. | `docs_v1_rate-limits.md` vs `rho/api/*.md` |

---

## 8. Conspicuously not stated

Credential and lifecycle gaps:
- No API for managing API Access Tokens (create, list, revoke are UI-only). Programmatic key rotation is impossible.
- No statement on whether a token's scopes, name, expiration, or IP allowlist can be edited after creation.
- Whether the 20-active-token cap counts expired or revoked tokens is unstated ("20 active" implies not, but it is not spelled out).
- Whether failed requests (401/403/429) refresh the 45-day inactivity clock. The doc says "A successful authenticated API request counts as activity", implying not.
- No warning or notification mechanism before a token expires or hits the inactivity cutoff.
- No token prefix documented for OAuth access tokens; no documented introspection endpoint.
- No IP allowlisting for OAuth partner clients.
- No 2FA or step-up requirement documented at OAuth consent (only at API Access Token creation).
- No CIDR-vs-single-address guidance for the 100-entry IP allowlist; no IPv6 statement.
- No sandbox equivalent of `auth.rho.co`, so the OAuth flow cannot be exercised against fictional data.
- No `client_credentials` grant, no device flow, no implicit flow; only Authorization Code + PKCE.
- No JWKS, ID token, `openid` scope, or userinfo endpoint mentioned, despite the OIDC-named discovery document at `/.well-known/openid-configuration`.

Contract and operations gaps:
- No changelog URL, status page, or stated channel for the "at least 15 days' notice" deprecation warning.
- No `Sunset` or `Deprecation` response headers documented.
- Non-nullable added fields, added required parameters, endpoint removal, and default/limit changes are unclassified by the versioning policy.
- MCP protocol-version support (`2026-07-28`, `2025-11-25`, `2025-06-18`) is not covered by the additive-only contract.
- No webhooks, no push, no event stream anywhere in the corpus: every integration is poll-only, under a ~60 req/min ceiling.
- No write operations of any kind; "The Rho API is read-only today" (`pages/core/product__api.txt`, footnote, "current as of August 2026").
- No idempotency keys (consistent with read-only).
- No bulk/export endpoint, no `total_count`, no backwards pagination.
- No documented cursor TTL, no incremental-sync cursor, no `updated_after` filter.
- No SDKs or client libraries referenced in any of the six guides.
- No CORS policy, no statement about browser-side calls (bearer tokens in a browser are implicitly discouraged by the secret-manager advice but never explicitly prohibited).
- No uptime SLA, no support SLA for the API, no per-plan API entitlement or pricing (the product page says "available to every Rho customer, with no waitlist and no approval step").

---

## 9. Cross-surface corroboration (non-guide pages)

From `pages/core/product__api.txt` (marketing, with an explicit as-of date):
- "Rho API access tokens are read-only and scoped to account and transaction data. Tokens cannot initiate payments or modify accounts, and can be revoked at any time. The Rho API is read-only today."
- "Only Account Owners and Admins can create Rho API access tokens, so programmatic access stays controlled from the start."
- "Tokens are scoped to account and transaction data, support an optional IP allowlist, and expire on a schedule you set, up to one year."
- "Every token is read-only, created only by an Account Owner or Admin with 2FA, and auto-expires after inactivity."
- "Public developer documentation: Yes, docs.rho.co (REST reference, MCP guide, rate limits)."
- Product capabilities "current as of August 2026"; competitive table data "collected from Mercury, Brex, and Ramp websites as of 2026-08-20".

Competitor assertions on the same page, all `[Rho claim]` and dated 2026-08-20:
- Mercury: "Yes, the API can initiate ACH transfers"; "Scoped tokens with fine-grained permissions and IP allow-listing"; docs at docs.mercury.com.
- Brex: "Yes, the Payments API sends ACH, domestic wires, and checks"; "Admin-created tokens, scoped at creation, **expire after 90 days unused**"; "No MCP or AI-assistant integration documented on developer.brex.com"; docs at developer.brex.com (10 REST APIs).
- Ramp: "Yes, write operations include bill creation, payment execution, and card issuance"; "OAuth 2.0 with granular permission scopes"; "Three documented MCP servers"; docs at docs.ramp.com.
- Direct comparison point worth carrying: Rho's inactivity expiry is **45 days**, Brex's is claimed at **90 days** `[Rho claim]`. Rho's is the stricter of the two.

From `site-llms.txt` line 33: "Rho API: Read-only API for Rho account and transaction data, one access token, direct connection to the Rho ledger (no aggregator), with a production MCP server that connects Rho to Claude and other AI agents. Available to all Rho customers; docs at docs.rho.co (as of 08/01/2026)."

From `help-center__the-rho-api__build-a-custom-integration-with-rho.txt`, the three-path routing table (verbatim structure):

| Intention | Path |
| --- | --- |
| Building an internal tool for your own business | Create an API access token |
| Building a product that connects to your customers' Rho accounts | Register as an OAuth partner |
| Authorizing a third-party vendor's integration | Contact the Rho API team |

Token creation steps per help center: "Navigate to Settings → API → Access Tokens." / "Create a new access token." / "Choose the appropriate permissions and complete two-factor authentication."

Third-party authorization path: "If a vendor has asked you to authorize their application with Rho, forward their request to api-partner-request@rho.co ... Our team will review the request and work directly with the vendor. You don't need to share your Rho credentials or complete any technical setup." This means a customer cannot authorize an arbitrary unregistered app; every partner integration passes through Rho's manual review.

MCP install command (verbatim, `docs_v1_mcp.md`):

```sh
claude mcp add --scope project --transport http rho-api \
  https://rhoapi.rho.co/mcp/v1 \
  --header "Authorization: Bearer <rho_api_access_token>"
```

---

## 10. Quick reference card

| Fact | Value |
| --- | --- |
| Production base | `https://rhoapi.rho.co/api/v1` |
| Sandbox base | `https://rhoapi-sandbox.rho.co/api/v1` |
| MCP endpoint | `https://rhoapi.rho.co/mcp/v1` |
| OAuth server | `https://auth.rho.co` (`/oauth2/auth`, `/oauth2/token`, `/oauth2/revoke`) |
| Auth header | `Authorization: Bearer <token>` only |
| Sandbox auth | any non-empty bearer token |
| Token prefix | `rhobat_` |
| Who can create tokens | Account Owners and Admins, with a 2FA challenge |
| Max active tokens | 20 per business |
| Max token expiration | 1 year (expiration required) |
| Inactivity expiry | 45 days (window starts at creation for unused tokens) |
| IP allowlist | optional, up to 100 entries per token |
| Scopes (auth guide) | `accounts:read`, `transactions:read`, `statements:read` |
| Scopes (OpenAPI) | above + `cards:read`, `invoicing:read` |
| OAuth extra scope | `offline_access` (for refresh tokens) |
| 401 | missing header, malformed, unknown, revoked, expired token |
| 403 | valid token, missing scope OR source IP off the allowlist |
| Error media type | `application/problem+json`, fields `type`/`title`/`status`/`detail`, `type` always `about:blank` |
| Revocation | immediate, no grace period, irreversible |
| OAuth flow | Authorization Code + PKCE `S256`, `audience=https://rhoapi.rho.co` |
| OAuth grant uniqueness | one active grant per (business, app) |
| Access token TTL | 15 minutes (`expires_in: 900`) |
| Refresh token TTL | 30 days rolling, single-use, rotating |
| Grant TTL | 1 year, then re-consent |
| Auth code TTL | "a few minutes", single-use |
| Partner onboarding | email `api-partner-request@rho.co`, 8 required fields |
| Version | `v1` in URL path, additive-only, `Version: 1.0.0` |
| Deprecation notice | at least 15 days |
| Non-breaking | new enum value, new nullable response field, new optional query param |
| Breaking | remove/rename enum value, remove response field, change field type, make optional field required |
| Pagination params | `page_size` (int), `page_token` (opaque string) |
| `page_size` max | 100 on accounts/transactions/statements; unstated on cards/invoicing |
| `page_size` default | 20 on cards/invoicing; unstated on accounts/transactions/statements |
| Out-of-range `page_size` | `400 Bad Request` |
| Cursor bound to | same endpoint + same filters + same sort order; otherwise `400` |
| End of pages | `page.next_page_token` is `null` |
| Rate limit per token | ~60 req/min |
| Rate limit per source IP | ~600 req/min (shared across all tokens on that IP) |
| Rate-limit error | `429 Too Many Requests` with `Retry-After` |
| `Retry-After: 0` | no fixed cooldown; use exponential backoff with jitter |
| Rate-limit headers on 2xx | none observed (verified against live sandbox headers, 2026-09-11) |
