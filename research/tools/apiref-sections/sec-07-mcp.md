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
