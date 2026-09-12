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
