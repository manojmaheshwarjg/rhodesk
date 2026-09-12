# Rho API Sandbox: Empirical Auth Probe

Live black-box probing of `https://rhoapi-sandbox.rho.co/api/v1` and (unauthenticated only) `https://rhoapi.rho.co/api/v1`.

- **Probe date:** 2026-09-11, ~23:42 to 23:50 UTC (server `date:` headers read `Fri, 11 Sep 2026`).
- **Client:** curl 8.7.1 (x86_64-apple-darwin25.0), libcurl/8.7.1 (SecureTransport), LibreSSL/3.3.6, nghttp2/1.68.1.
- **Raw artifacts:** 147 files in `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-auth/` (`<case>.headers` + `<case>.body` per case, plus `probe.sh`, `len-*` size ladder, `burst-*.log`, `tenant-*` fixtures).
- **Credentials used:** none real. Every token was a synthetic string (`sandbox`, `zzz-garbage`, `rhobat_000…0`, `AAAA…`). No production credential was ever transmitted. Production was probed **only** with no `Authorization` header at all.
- Edge/CDN in front of both hosts is Cloudflare; all probes ran from a single source IP in the `EWR` (Newark) Cloudflare colo per `cf-ray` suffixes.

---

## 1. Headline findings

| # | Finding | Evidence |
|---|---|---|
| 1 | Sandbox auth is a **non-empty string check only**. Any non-empty token after the literal prefix `Bearer ` returns 200. Confirmed with `sandbox`, `1`, `x`, `zzz-garbage…`, `tökén-ünïcode`, `two words`, and 8168 `A`s. | cases 01, 02, 03, 15, 17, 18 |
| 2 | **Scopes are not enforced in sandbox at all.** One garbage token (`qqqq-garbage-token-no-scopes-at-all`) read all five scope families (accounts, transactions, statements, cards, invoicing). A `403` is therefore **not reachable** in sandbox by any means found. | `scope-*.headers` |
| 3 | The `type` member of the problem document is **not a URI** on the auth and not-found paths. Live values are `"2"` and `"1303"`, contradicting Rho's own OpenAPI description ("A URI reference that identifies the problem type. Example: about:blank") and the `docs/v1/auth` worked example (`"type": "about:blank"`). | cases 04, 30; `docs/api_v1_openapi.md`, `docs/docs_v1_auth.md` |
| 4 | The REST API returns **no `WWW-Authenticate` header on any 401**, violating RFC 9110 §11.6.1 ("The server generating a 401 response MUST send a WWW-Authenticate header field"). The **MCP endpoint does** send one. | cases 04-14, 43, 50, 53 vs case 72 |
| 5 | **No CORS headers anywhere.** No `Access-Control-Allow-Origin`, no `Vary: Origin`, on 200 or 401, with or without an `Origin`. `OPTIONS` returns `405` with `allow: GET`. The API cannot be called from a browser cross-origin. Server-to-server only. | cases 40, 41, 42, 43, 54 |
| 6 | The documented 401 `title` is **`Unauthorized`**; the live 401 `title` is **`Unauthenticated`**. | `docs/docs_v1_auth.md` vs every 401 captured |
| 7 | Production and sandbox rejections are **byte-identical** (`cmp` clean, md5 `a9b8c917cbc1e5b43579afaee5ccadd5`, identical header set), and the two hostnames resolve to the **same Cloudflare IPs** (`104.18.26.176`, `104.18.27.176`). Same code, same middleware; only the token-validation branch differs. | cases 05 vs 50; `dig` |
| 8 | The `Bearer` scheme match is **case-sensitive and space-sensitive**, violating RFC 9110 §11.1 (auth scheme is case-insensitive). `bearer` → 401, `BEARER` → 401, `Bearer\t<tok>` → 401. | cases 10, 11, 13 |
| 9 | **Parameter type-binding runs before authentication.** `GET /accounts?page_size=abc` with **no credential** returns `400 {"type":"about:blank",…,"detail":"invalid parameter: page_size"}`, not 401. Range/enum validation runs *after* auth and uses a different shape (`"type":"1317"`). Two distinct 400 producers. | cases 34 + ordering battery |
| 10 | **The documented rate limits are not enforced in sandbox.** 80 requests on one token in 22s (218/min, ~3.6× the documented "approximately 60 requests per minute" per token) returned 80× `200`, zero `429`. 75 unauthenticated requests in 17s returned 75× `401`, zero `429`. No `X-RateLimit-*` and no `Retry-After` header was returned on any of the ~200 requests made. | `burst-auth.log`, `burst-unauth.log` |
| 11 | **`/mcp/v1` does not exist on the sandbox host.** It returns the Kubernetes ingress-nginx `default backend - 404`. The docs say MCP "uses the same API contract, authentication model, scopes, and error behavior as the REST API" but give no sandbox MCP URL, and none exists. | cases 70, 71 |
| 12 | Production `/mcp/v1` **does** exist, is RFC 9728 compliant, and its unauthenticated 401 leaks a public discovery document listing **five** scopes, settling a contradiction inside Rho's own docs (see §8). | cases 72, 73, 74 |

---

## 2. Case table: sandbox auth

Endpoint `GET https://rhoapi-sandbox.rho.co/api/v1/accounts` unless noted. Body column shows the exact bytes returned.

| # | Case | `Authorization` sent | Status | `Content-Type` | Body |
|---|---|---|---|---|---|
| 01 | Valid-looking prod-format token | `Bearer rhobat_0000…0000` (64 hex-ish chars) | `200` | `application/json` | Full 2558-byte account fixture |
| 02 | Documented sandbox token | `Bearer sandbox` | `200` | `application/json` | Identical 2558 bytes |
| 03 | Nonsense token | `Bearer zzzzz-not-a-real-token-!!!` | `200` | `application/json` | Identical 2558 bytes |
| 04 | Empty bearer value | `Bearer ` (trailing space, empty token) | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 05 | No `Authorization` header | *(absent)* | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 06 | Header present, value empty | `Authorization:` (curl `Authorization;`) | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 07 | No scheme, bare token | `rhobat_abcdef0123456789` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 08 | Wrong scheme: Basic | `Basic c2FuZGJveDpzYW5kYm94` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 09 | Wrong scheme: Token | `Token sandbox` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 10 | Lowercase scheme | `bearer sandbox` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 11 | Uppercase scheme | `BEARER sandbox` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 12 | Double space after scheme | `Bearer  sandbox` | `200` | `application/json` | Identical 2558 bytes |
| 13 | Tab separator | `Bearer\tsandbox` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 14 | Scheme only, no space, no token | `Bearer` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 15 | Token containing a space | `Bearer two words` | `200` | `application/json` | Identical 2558 bytes |
| 16 | Two `Authorization` headers | `Bearer sandbox` + `Bearer other` | `400` | `text/html` | nginx/Cloudflare `400 Bad Request` HTML, **`cf-ray: -`** (rejected at the Cloudflare edge, never reached origin) |
| 17 | 1-character token | `Bearer x` | `200` | `application/json` | Identical 2558 bytes |
| 18 | 1024-char token | `Bearer AAAA…` (1024) | `200` | `application/json` | Identical 2558 bytes |
| 19 | 8192-char token | `Bearer AAAA…` (8192) | `400` | `text/html` | `400 Request Header Or Cookie Too Large` (**nginx**) |
| 20 | 16384-char token | `Bearer AAAA…` (16384) | `400` | `text/html` | Same nginx error |
| 21 | 32768-char token | `Bearer AAAA…` (32768) | `400` | `text/html` | Same nginx error |
| n/a | `Bearer` + two spaces (token = one space) | `Bearer  ` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| n/a | Lowercase header **name** | `authorization: Bearer sandbox` | `200` | `application/json` | Identical (HTTP/2 lowercases header names anyway) |
| n/a | Non-ASCII token | `Bearer tökén-ünïcode` | `200` | `application/json` | Identical 2558 bytes |

### 2.1 Inferred sandbox auth algorithm

Every observation above is explained by exactly this, in order:

1. Take the raw `Authorization` header value.
2. Require a **literal, case-sensitive** prefix `"Bearer "` (`B-e-a-r-e-r` + one U+0020). Anything else → 401.
3. Take the remainder verbatim.
4. Trim surrounding whitespace.
5. If the result is empty → 401. Otherwise → authenticated, all scopes granted.

Supporting discriminators:
- `Bearer  sandbox` (double space) passes → the remainder is trimmed, not rejected, so step 4 exists.
- `Bearer  ` (remainder is a single space) fails → step 4 runs **before** the non-empty test in step 5.
- `Bearer\tsandbox` fails → step 2 matches a literal space, not "any whitespace", so the tab never matches the prefix.
- `Bearer two words` passes → no charset or single-token validation on the credential; the whole remainder is the token.
- `bearer`/`BEARER` fail → step 2 is case-sensitive.

**No token format validation exists in sandbox.** The `rhobat_` prefix documented for production tokens is neither required nor checked: `Bearer x` and `Bearer rhobat_0000…` are treated identically.

### 2.2 Token length ceiling (nginx, not Rho)

Binary search on token length, header line = `"Authorization: Bearer " (22 bytes) + token`:

| Token chars | Header line bytes | Status |
|---|---|---|
| 4096 | 4118 | `200` |
| 7936 | 7958 | `200` |
| 8128 | 8150 | `200` |
| 8160 | 8182 | `200` |
| **8168** | **8190** | **`200`** |
| **8169** | **8191** | **`400`** |
| 8170 | 8192 | `400` |
| 8172 | 8194 | `400` |
| 8192 | 8214 | `400` |

The cutoff is exact and lands at **8190 bytes of header line**, i.e. 8190 + CRLF = 8192 = the nginx default `large_client_header_buffers` of 8k. The failure is **not** a Rho application error: the body is the nginx HTML page `400 Request Header Or Cookie Too Large` with `<hr><center>nginx</center>`, `content-type: text/html`, and it is **not** `application/problem+json`. Critically it still carries `via: 1.1 google`, `cf-cache-status: DYNAMIC` and the full Rho security header set, so it reached Rho's origin ingress and was rejected there, unlike case 16 (duplicate header) which Cloudflare killed at the edge with `cf-ray: -`.

**Client implication:** an oversized or duplicated `Authorization` header produces an **HTML** body from a JSON API. Any client that blindly `JSON.parse`es an error body will throw on these two cases.

---

## 3. Scope enforcement in sandbox: none

One token, `Bearer qqqq-garbage-token-no-scopes-at-all`, against every scope family declared in the OpenAPI security scheme:

| Endpoint | Required scope (per docs) | Status | Bytes | `Content-Type` |
|---|---|---|---|---|
| `GET /accounts` | `accounts:read` | `200` | 2558 | `application/json` |
| `GET /transactions` | `transactions:read` | `200` | 13126 | `application/json` |
| `GET /statements` | `statements:read` | `200` | 28132 | `application/json` |
| `GET /cards` | `cards:read` | `200` | 6357 | `application/json` |
| `GET /invoicing/customers` | `invoicing:read` | `200` | 3383 | `application/json` |
| `GET /invoicing/invoices` | `invoicing:read` | `200` | 15390 | `application/json` |

All six succeed. No scope is ever consulted. The byte counts match the previously captured `sandbox/*.json` fixtures exactly, confirming the sandbox is a static fixture set.

**Consequence for integrators:** the `403 Forbidden` path documented in `docs/v1/auth` ("A request whose token lacks the required scope is rejected with 403 Forbidden") **cannot be exercised in sandbox**. No probe produced a `403` from either host. A client's 403 handling, its IP-allowlist-rejection handling, and its scope-error UX are all untestable before going to production. This is the single largest functional gap in the sandbox.

### 3.1 No tenant separation

Different tokens return byte-identical data, so there is one global fixture tenant:

| Token | `/accounts` md5 | Bytes |
|---|---|---|
| `sandbox` | `593d7be465d362f7a9ba94fcbebbb927` | 2558 |
| `rhobat_0000…0000` | `593d7be465d362f7a9ba94fcbebbb927` | 2558 |
| `completely-different-token-xyz` | `593d7be465d362f7a9ba94fcbebbb927` | 2558 |
| `1` | `593d7be465d362f7a9ba94fcbebbb927` | 2558 |

`/transactions` likewise: `sandbox` and `zzz-garbage` both md5 `f4fb6d8df47eb92dd42ec98d1d4f4634`, 13126 bytes.

This confirms Rho's "fictional, deterministic data" claim ([Rho claim], `docs/v1/getting-started`) and additionally establishes that the token is not used as a tenant selector. There is no way to request a second fictional business, a zero-state business, or an error-state business. **Conspicuously absent:** any documented or discoverable mechanism for sandbox scenario selection (no magic tokens, no `?scenario=`, no seeded failure accounts).

---

## 4. RFC 9457 problem details: partial conformance

Rho's OpenAPI states: "Errors follow [RFC 9457 problem details]". The `docs/v1/auth` page instead cites the obsolete **RFC 7807** for the same media type. Live behavior is a partial match at best.

### 4.1 Every distinct error body observed

| Trigger | Status | `Content-Type` | Exact body | `type` is a URI? | `detail` present? |
|---|---|---|---|---|---|
| Missing / empty / malformed credential | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` | No (`"2"`) | No |
| Unknown resource id, any resource | `404` | `application/problem+json` | `{"type":"1303","title":"account not found","status":404}` | No (`"1303"`) | No |
| Param fails type binding (pre-auth) | `400` | `application/problem+json` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}` | Yes | **Yes** |
| Param fails range/enum check (post-auth) | `400` | `application/problem+json` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` | No (`"1317"`) | No |
| Unrouted path | `404` | `text/plain; charset=utf-8` | `404 page not found` | **Not a problem document at all** | n/a |
| Wrong method | `405` | *(none)* | *(empty, `content-length: 0`)*, `allow: GET` | **Not a problem document at all** | n/a |
| Oversized header | `400` | `text/html` | nginx `400 Request Header Or Cookie Too Large` | **Not a problem document at all** | n/a |
| Duplicate `Authorization` | `400` | `text/html` | Cloudflare `400 Bad Request` | **Not a problem document at all** | n/a |
| Path outside `/api/v1` | `404` | `text/plain; charset=utf-8` | `default backend - 404` | **Not a problem document at all** | n/a |

### 4.2 Conformance verdict

| RFC 9457 requirement | Live behavior | Verdict |
|---|---|---|
| Media type `application/problem+json` | Sent on 400/401/404-by-id | **Pass** for application errors |
| `type` is a URI reference (§3.1.1) | `"2"`, `"1303"`, `"1317"` | **Technically** a relative URI reference, so not strictly invalid, but meaningless, non-dereferenceable, and contradicts Rho's own schema description and worked example. Treat as **fail in spirit** |
| `type` absent defaults to `about:blank` (§3.1.1) | Only the pre-auth binding error actually uses `about:blank` | Inconsistent |
| `status` matches the HTTP status code | Matches in every case observed (401/401, 404/404, 400/400) | **Pass** |
| `title` is a short human-readable summary of the **problem type**, not the occurrence | `"account not found"` / `"page_size must be between 1 and 100"` are occurrence-specific and vary by resource while `type` stays constant at `1303`/`1317`. Per §3.1.2 `title` should not change for a given `type` | **Fail** |
| `detail` explains this occurrence | Present only on the `about:blank` 400s. Absent from every 401 and every 404 | Partial; `detail` is optional so not a violation, but it means 401s carry **zero** diagnostic information |
| Extension members | None observed. No `instance`, no trace id, no error code field beyond the overloaded `type` | Minimal |

### 4.3 The `type` code namespace is overloaded

`1303` is returned for **six different resources**, with only `title` distinguishing them:

| Request | Body |
|---|---|
| `GET /accounts/00000000-0000-4000-8000-000000000000` | `{"type":"1303","title":"account not found","status":404}` |
| `GET /transactions/0000…` | `{"type":"1303","title":"transaction not found","status":404}` |
| `GET /statements/0000…` | `{"type":"1303","title":"statement not found","status":404}` |
| `GET /cards/0000…` | `{"type":"1303","title":"card not found","status":404}` |
| `GET /invoicing/customers/0000…` | `{"type":"1303","title":"customer not found","status":404}` |
| `GET /invoicing/invoices/0000…` | `{"type":"1303","title":"invoice not found","status":404}` |
| `GET /transactions/0000…/files/0000…` | `{"type":"1303","title":"transaction file not found","status":404}` |

`1317` similarly covers at least two unrelated validation failures:

| Request | Body |
|---|---|
| `?page_size=101` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| `?page_token=garbage` | `{"type":"1317","title":"page_token must be a valid cursor","status":400}` |
| `?order=bogus` | `{"type":"1317","title":"invalid order parameter: \"bogus\"","status":400}` |

**Integrator implication:** `type` is too coarse to branch on and `title` is too fine (and is free prose that can change at any time, since it is not covered by the versioning contract). There is no stable machine-readable error code. The OpenAPI's four-field schema (`type`, `title`, `status`, `detail`) is the entire contract, and only three fields are reliably populated.

### 4.4 Key ordering differs between REST and MCP

Both are 52 bytes with identical keys and values, but serialized in different orders, so they are different objects from different serializers:

```
REST /api/v1/accounts : {"type":"2","title":"Unauthenticated","status":401}   md5 a9b8c917cbc1e5b43579afaee5ccadd5
MCP  /mcp/v1          : {"status":401,"title":"Unauthenticated","type":"2"}   md5 bd60dba151c99a7227902eb6dd9a3738
```

Any client doing byte or hash comparison on error bodies across the two surfaces will see a difference where none is semantically intended.

---

## 5. Middleware ordering

Derived by sending requests that would fail several checks at once, with and without a credential.

| Request | No credential | With credential |
|---|---|---|
| `GET /nope` | `404` `text/plain` `404 page not found` | `404` `text/plain` (identical) |
| `POST /accounts` | `405`, `allow: GET`, empty body | `405`, `allow: GET`, empty body |
| `GET /accounts?page_size=abc` | **`400`** `about:blank` + `detail` | `400` `about:blank` + `detail` |
| `GET /accounts/not-a-uuid` | **`400`** `about:blank` `"invalid parameter: account_id"` | `400` identical |
| `GET /accounts/<valid-uuid-unknown>` | `401` | `404` `1303` |
| `GET /accounts?page_size=101` | `401` | `400` `1317` |
| `GET /accounts?page_size=0` | `401` | (range error) |
| `GET /accounts?page_token=garbage` | `401` | `400` `1317` |
| `GET /accounts?order=bogus` | `401` | `400` `1317` |
| `GET /accounts?access_token=sandbox` | `401` | n/a |

**Resulting pipeline:**

```
1. Cloudflare edge            -> malformed HTTP (duplicate Authorization): 400 text/html, cf-ray: -
2. GCLB (via: 1.1 google)
3. ingress-nginx              -> unrouted host path: "default backend - 404"
                              -> header > 8190 bytes: 400 "Request Header Or Cookie Too Large"
4. Go router (net/http mux)   -> unknown path: 404 "404 page not found" (Go's http.NotFound default)
5. Method check              -> 405 + "allow: GET", empty body
6. Parameter TYPE BINDING    -> 400 {"type":"about:blank", ... "detail":"invalid parameter: X"}   <-- PRE-AUTH
7. AUTHENTICATION            -> 401 {"type":"2","title":"Unauthenticated","status":401}
8. Handler + semantic checks -> 400 {"type":"1317", ...} / 404 {"type":"1303", ...}
```

Step 6 running before step 7 is the notable one: **an unauthenticated caller can enumerate parameter names and their expected types**. `?page_size=abc` returns `"invalid parameter: page_size"` and `/accounts/not-a-uuid` returns `"invalid parameter: account_id"` with no credential. This is low-severity (the parameter names are already public in the OpenAPI document) but it is an unauthenticated-reachable code path and it means a 400 does not imply authentication succeeded. A client must not infer "my token worked" from a non-401 status.

Conversely, `405` also precedes auth: `POST /accounts` with no credential returns `405`, not `401`.

Unknown query parameters are **silently ignored** when authenticated: `?bogus_param=1&access_token=x` with a valid bearer returns `200`.

---

## 6. Alternate credential channels: all rejected

The `docs/v1/auth` claim "No other authentication header (cookie, API key, signed request) is supported" is **empirically confirmed**. Each of the following returned `401 {"type":"2","title":"Unauthenticated","status":401}`:

| Channel attempted | Result |
|---|---|
| `GET /accounts?access_token=sandbox` | `401` |
| `GET /accounts?token=sandbox` | `401` |
| `X-Api-Key: sandbox` | `401` |
| `Cookie: session=sandbox` | `401` |
| `Authorization: Basic <b64>` | `401` |
| `Authorization: Token sandbox` | `401` |

Note the query-parameter attempts returned `401`, not a `400` for an unknown parameter, which is consistent with §5: unknown query params are ignored, and the request then fails auth.

---

## 7. Security headers and transport

### 7.1 Header set (identical on 200 and 401, identical on sandbox and production)

| Header | Value | Assessment |
|---|---|---|
| `strict-transport-security` | `max-age=63072000; includeSubDomains; preload` | Strong. 2 years, subdomains, preload |
| `x-content-type-options` | `nosniff` | Present |
| `x-frame-options` | `DENY` | Present (irrelevant for a JSON API, harmless) |
| `referrer-policy` | `strict-origin-when-cross-origin` | Present |
| `cf-cache-status` | `DYNAMIC` | Nothing cached at the edge |
| `via` | `1.1 google` | Google Cloud load balancer in path |
| `server` | `cloudflare` | Origin server software masked |
| `cf-ray` | e.g. `a39a8721ca7e0d00-EWR` | Per-request edge trace id |

### 7.2 Conspicuously absent

| Missing header | Why it matters |
|---|---|
| **`WWW-Authenticate`** | RFC 9110 §11.6.1 makes it **mandatory** on 401. Absent from every REST 401. Clients cannot discover the required scheme or the authorization server from the response. Present on `/mcp/v1` only |
| **`Access-Control-Allow-Origin`** / any `Access-Control-*` | No CORS at all, on any status, with any `Origin`. See §7.3 |
| **`Vary`** | Not sent at all, including `Vary: Origin` and `Vary: Authorization`. With `cf-cache-status: DYNAMIC` nothing is cached today, but the absence of `Vary: Authorization` on an authenticated endpoint is a latent cache-poisoning footgun if edge caching is ever enabled |
| **`Cache-Control`** / `Pragma` | Not sent on authenticated 200 responses. Financial data returned with no `no-store` directive; intermediaries are given no instruction |
| **`X-RateLimit-Limit` / `-Remaining` / `-Reset`** | None, on any of ~200 requests. The documented limits are therefore unobservable; a client cannot pace itself from response feedback and can only react to a `429` after the fact |
| **`Retry-After`** | Never seen, because no `429` was ever produced |
| **`Content-Security-Policy`** | Absent (low relevance for a JSON API) |
| **Any request/trace id** (`X-Request-Id`, `traceparent`) | Absent. `cf-ray` is the only correlator, and it is a Cloudflare id, not a Rho one. Support escalations have no Rho-side handle |
| **`alt-svc`** | No HTTP/3 advertised |

### 7.3 CORS: confirmed absent

| Case | Request | Status | CORS headers |
|---|---|---|---|
| 40 | `OPTIONS /accounts`, `Origin: https://evil.example.com`, `Access-Control-Request-Method: GET` | `405` | **None.** `allow: GET` |
| 41 | `OPTIONS /accounts`, `Origin: https://app.rho.co` (Rho's own app origin) | `405` | **None.** `allow: GET` |
| 42 | `GET /accounts`, valid bearer, `Origin: https://evil.example.com` | `200` | **None** |
| 43 | `GET /accounts`, no bearer, `Origin: https://evil.example.com` | `401` | **None** |
| 54 | `OPTIONS /accounts` on **production**, `Origin: https://evil.example.com` | `405` | **None** |

Preflight fails outright: `OPTIONS` is not in `allow: GET`, so a browser preflight can never succeed, and no `Access-Control-Allow-Origin` is emitted even on the simple-request path. The API is **structurally unusable from browser JavaScript cross-origin**. Combined with the fact that the credential is a long-lived opaque secret, this is a deliberate and correct posture: the token must never reach a browser. It is, however, nowhere stated in the docs. A front-end developer reading the quickstart would discover this only by failing.

The RFC 9728 discovery document at `/.well-known/oauth-protected-resource/mcp/v1` **also** returns no CORS headers, which will block browser-based MCP clients performing discovery.

### 7.4 Transport

| Property | Sandbox | Production |
|---|---|---|
| ALPN | `h2` accepted | `h2` accepted |
| TLS | TLSv1.3, `AEAD-CHACHA20-POLY1305-SHA256` | TLSv1.3, `AEAD-CHACHA20-POLY1305-SHA256` |
| Cert CN | `rhoapi-sandbox.rho.co` | `rhoapi.rho.co` |
| Cert issuer | `C=US; O=Google Trust Services; CN=WE1` | `C=US; O=Google Trust Services; CN=WE1` |
| Cert expiry | `Nov 26 12:19:05 2026 GMT` | `Nov 23 15:40:25 2026 GMT` |
| DNS A records | `104.18.26.176`, `104.18.27.176` | `104.18.26.176`, `104.18.27.176` (**same**) |
| HTTP/1.1 fallback | Works; `401 Unauthorized` reason phrase, same body | n/a |
| Plaintext `http://` | `301 Moved Permanently` → `https://rhoapi-sandbox.rho.co/api/v1/accounts`. Redirect carries `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY` but **no HSTS on the plaintext response** (correct per spec, HSTS over cleartext is ignored) | n/a |

**Redirect risk:** the plaintext `301` preserves the full path. A client that sends `Authorization` over `http://` with redirect-following enabled will have transmitted the token in cleartext before the redirect is honored. No `Upgrade-Insecure-Requests` handling or refusal is in place; the request is simply redirected.

### 7.5 `HEAD` is not supported

```
curl -I https://rhoapi-sandbox.rho.co/api/v1/accounts
-> HTTP/2 405, allow: GET, empty body
```

RFC 9110 §9.3.2: "The HEAD method is identical to GET except that the server MUST NOT send content". A server supporting `GET` is expected to support `HEAD`. `allow: GET` lists neither `HEAD` nor `OPTIONS`. Health checkers and monitoring tools defaulting to `HEAD` will report the API as broken.

### 7.6 No content negotiation

`Accept: text/html` on an unauthenticated request still returns `content-type: application/problem+json` with the same 52-byte body. The server ignores `Accept` entirely. No `406` path exists.

---

## 8. Production host, unauthenticated (no token sent)

Every production request below carried **no `Authorization` header whatsoever**.

| # | Request | Status | `Content-Type` | Body |
|---|---|---|---|---|
| 50 | `GET https://rhoapi.rho.co/api/v1/accounts` | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| 51 | `GET https://rhoapi.rho.co/api/v1/transactions` | `401` | `application/problem+json` | identical |
| 52 | `GET https://rhoapi.rho.co/api/v1/nope` | `404` | `text/plain; charset=utf-8` | `404 page not found` |
| 53 | `GET https://rhoapi.rho.co/api/v1/accounts`, `Authorization: Bearer ` (empty value) | `401` | `application/problem+json` | identical |
| 54 | `OPTIONS https://rhoapi.rho.co/api/v1/accounts`, `Origin:` set | `405` | *(none)* | empty, `allow: GET` |
| 61 | `GET https://rhoapi.rho.co/api/v2/accounts` | `404` | `text/plain; charset=utf-8` | `default backend - 404` |
| 72 | `POST https://rhoapi.rho.co/mcp/v1` (JSON-RPC `initialize`) | `401` | `application/problem+json` | `{"status":401,"title":"Unauthenticated","type":"2"}` + **`WWW-Authenticate`** |
| 73 | `GET https://rhoapi.rho.co/mcp/v1` | `401` | `application/problem+json` | identical to 72 |
| 74 | `GET https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` | `200` | `application/json` | discovery doc, see below |

### 8.1 Production REST is indistinguishable from sandbox on the rejection path

```
$ cmp 05-missing-auth-header.body 50-prod-no-auth-accounts.body
IDENTICAL
$ diff <(grep -v 'date:|cf-ray:' sandbox.headers) <(grep -v 'date:|cf-ray:' prod.headers)
HEADERS IDENTICAL
```

Same md5 (`a9b8c917cbc1e5b43579afaee5ccadd5`), same 52 bytes, same header set in the same order, same Cloudflare IPs, same `Google Trust Services WE1` issuer. **There is no way for a client to tell from an error response which environment it is talking to.** A misconfigured `RHO_API_BASE_URL` pointing at production instead of sandbox surfaces the exact same 401 a bad sandbox token would. No environment marker (`X-Rho-Environment`, a `sandbox` flag in the problem document, a distinct `type`) exists anywhere.

This is a real operational hazard: the documented sandbox posture is "any non-empty bearer token is accepted", so a developer who typoes the hostname gets `401` and will reasonably conclude their *token* is wrong rather than their *host*.

### 8.2 Production `/mcp/v1` is the only RFC-compliant 401 in the estate

```
HTTP/2 401
content-type: application/problem+json
content-length: 52
www-authenticate: Bearer resource_metadata="https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1"
```

This is RFC 9728 (OAuth 2.0 Protected Resource Metadata) as required by the MCP authorization spec. The REST API at `/api/v1` sends no such header. Two different auth middlewares are in play despite `docs/v1/mcp` asserting MCP "uses the same API contract, authentication model, scopes, and error behavior as the REST API" [Rho claim]. The error **body** matches (modulo key order) but the error **headers** do not.

### 8.3 The discovery document resolves Rho's internal scope contradiction

`GET https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1` → `200 application/json`, no credential required:

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

`bearer_methods_supported: ["header"]` independently corroborates §6: no query-parameter or form-body credential.

**The contradiction it settles.** `docs/v1/auth` says: "The scopes available today are:" followed by a table of **exactly three** rows: `accounts:read`, `transactions:read`, `statements:read`. But:

| Source | Scopes listed |
|---|---|
| `docs/v1/auth` Scopes table | 3: `accounts:read`, `transactions:read`, `statements:read` |
| `docs/v1/openapi` `AccessToken` scheme | **5**: adds `cards:read`, `invoicing:read` |
| `docs/v1/cards` | "Both endpoints require the `cards:read` scope" |
| `docs/v1/invoicing` | "Every endpoint requires the `invoicing:read` scope" |
| **Live RFC 9728 metadata (2026-09-11)** | **5**: `accounts:read`, `transactions:read`, `statements:read`, `cards:read`, `invoicing:read` |
| `docs/v1/statements` | Mentions **no** scope at all |

The authoritative answer is **five**. The `docs/v1/auth` page is stale: Cards and Invoicing shipped and their scopes were added to the OpenAPI, the per-product docs, and the live authorization server, but not back-ported to the central Scopes table. Anyone building a partner OAuth integration from `docs/v1/auth` alone (which is exactly what `docs/v1/partner-auth` tells them to do: "Requested scopes: The scopes your app needs, e.g. `accounts:read transactions:read offline_access` (see Scopes)") would request too few scopes.

### 8.4 The authorization server is Ory Hydra

`GET https://auth.rho.co/.well-known/openid-configuration` → `200 application/json; charset=utf-8` (public, no credential). Selected values:

| Field | Value |
|---|---|
| `issuer` | `https://auth.rho.co` |
| `authorization_endpoint` | `https://auth.rho.co/oauth2/auth` |
| `token_endpoint` | `https://auth.rho.co/oauth2/token` |
| `device_authorization_endpoint` | `https://auth.rho.co/oauth2/device/auth` |
| `revocation_endpoint` | `https://auth.rho.co/oauth2/revoke` |
| `end_session_endpoint` | `https://auth.rho.co/oauth2/sessions/logout` |
| `userinfo_endpoint` | `https://auth.rho.co/userinfo` |
| `jwks_uri` | `https://auth.rho.co/.well-known/jwks.json` |
| `grant_types_supported` | `authorization_code`, `implicit`, `client_credentials`, `refresh_token`, `urn:ietf:params:oauth:grant-type:device_code` |
| `response_types_supported` | `code`, `code id_token`, `id_token`, `token id_token`, `token`, `token id_token code` |
| `code_challenge_methods_supported` | **`plain`**, `S256` |
| `token_endpoint_auth_methods_supported` | `client_secret_post`, `client_secret_basic`, `private_key_jwt`, **`none`** |
| `scopes_supported` | `offline_access`, `offline`, `openid` (**not** the API scopes) |
| `id_token_signing_alg_values_supported` | `RS256` |
| `subject_types_supported` | `public` |
| `claims_supported` | `sub` |
| `request_uri_parameter_supported` / `require_request_uri_registration` | `true` / `true` |
| `credentials_endpoint_draft_00` | `https://auth.rho.co/credentials` |
| `credentials_supported_draft_00` | `jwt_vc_json`, types `VerifiableCredential`, `UserInfoCredential` |

**Fingerprint:** `credentials_endpoint_draft_00` + `credentials_supported_draft_00` with `jwt_vc_json`, alongside the `offline` scope and the device-code grant, is the distinctive signature of **Ory Hydra**. These are Hydra defaults, not deliberate Rho configuration.

**Gaps between the advertised AS and Rho's documented flow** (all [inference from live metadata], not Rho claims):
- The AS advertises `code_challenge_methods_supported: ["plain", "S256"]`. `docs/v1/partner-auth` mandates `code_challenge_method=S256`. The server will nonetheless accept the downgrade-prone `plain` method unless it is refused per-client.
- `implicit` and `token`-bearing response types are advertised, which are deprecated in OAuth 2.1 and would place access tokens in the URL fragment.
- `token_endpoint_auth_methods_supported` includes `none` (public clients), while Rho's docs describe only confidential clients receiving a `client_secret`.
- `scopes_supported` lists only `offline_access`, `offline`, `openid` and **omits** all five API scopes, so an OAuth library doing strict discovery-driven scope validation would reject `accounts:read` as unsupported.
- `docs/v1/partner-auth` documents only `authorization_code` and `refresh_token`; the AS advertises three more grants.

**Not discoverable:** `https://rhoapi.rho.co/.well-known/oauth-authorization-server` returns `default backend - 404`, so the resource server does not mirror AS metadata. The sandbox host has **no** `.well-known` route at all (`default backend - 404`).

---

## 9. Rate limiting: documented but not enforced in sandbox

`docs/v1/rate-limits` states: "Per API Access Token: Approximately 60 requests per minute. Per source IP: Approximately 600 requests per minute." and describes `429 Too Many Requests` with a `Retry-After` header whose `0` value means "no fixed cooldown".

| Test | Requests | Elapsed | Effective rate | Result |
|---|---|---|---|---|
| Unauthenticated burst, single IP | 75 | 17 s | ~265/min | **75 × `401`**, zero `429` |
| Authenticated burst, single token, single IP | 80 | 22 s | ~218/min | **80 × `200`**, zero `429` |

The authenticated burst exceeded the documented per-token limit by roughly **3.6×** with no throttling. Neither burst emitted `X-RateLimit-*` or `Retry-After` on any response. Total probe volume was roughly 200 requests from one IP inside ~8 minutes, also without a `429`, though that stays under the 600/min IP ceiling.

**Conclusions:**
- Sandbox does not enforce the per-token limit, so a client's backoff logic **cannot be tested in sandbox**. Alongside the missing `403`, this is the second untestable production behavior.
- The `401` path is not rate limited by token (there is no token to key on) and was not IP-throttled at 265/min. Credential-stuffing throttling, if it exists, sits above the rates tested. Since sandbox accepts any string there is nothing to stuff here, but the same middleware appears to serve production (§8.1), and production's rejection is byte-identical.
- Because the documented limits are "approximate" and "enforced across a distributed edge network" [Rho claim], absence in sandbox is not proof of absence in production. It is proof that **the sandbox does not let you rehearse it**.

---

## 10. Documentation vs reality

| Rho's statement | Source | Live reality | Verdict |
|---|---|---|---|
| "any non-empty bearer token is accepted" | `docs/v1/auth`, `docs/v1/getting-started` | Confirmed exactly, including 1-char and non-ASCII tokens | **Accurate** |
| "Sandbox authentication is intentionally permissive" | `docs/v1/auth` | Confirmed; also permissive on scopes, which is not stated | Accurate but **incomplete** |
| 401 body example `{"type":"about:blank","title":"Unauthorized","status":401,"detail":"Token is revoked or has expired"}` | `docs/v1/auth` | Live: `{"type":"2","title":"Unauthenticated","status":401}`. **`type` differs, `title` differs, `detail` absent** | **Wrong on 3 of 4 fields** |
| "Errors follow RFC 9457 problem details" | `docs/v1/openapi` | Partial. 404-unrouted, 405, and both 400-class infra errors are not problem documents; `type` is not a URI on 3 of 4 problem shapes | **Overstated** |
| Errors are `application/problem+json` per RFC **7807** | `docs/v1/auth` | The OpenAPI cites RFC **9457** for the same thing. RFC 9457 obsoletes 7807 | **Internal inconsistency** |
| `type` is "A URI reference that identifies the problem type. Example: about:blank" | OpenAPI schema, all 14 operation pages | Live values `"2"`, `"1303"`, `"1317"` | **Contradicted** |
| "Scopes ... are enforced before your request reaches the handler. A request whose token lacks the required scope is rejected with 403 Forbidden" | `docs/v1/auth` | True in production presumably; **not enforced at all in sandbox**, 403 unreachable | Untestable |
| "The scopes available today are" (3 listed) | `docs/v1/auth` | Live metadata and OpenAPI list **5** | **Stale / contradicted** |
| "No other authentication header (cookie, API key, signed request) is supported" | `docs/v1/auth` | Confirmed: cookie, `X-Api-Key`, `Basic`, `Token`, and two query-param forms all rejected | **Accurate** |
| "~60 requests per minute" per token | `docs/v1/rate-limits` | 218/min sustained in sandbox with zero `429` | **Not enforced in sandbox** |
| `Retry-After` handling guidance | `docs/v1/rate-limits` | Header never observed | Untestable |
| MCP "uses the same ... authentication model ... and error behavior as the REST API" | `docs/v1/mcp` | Body matches modulo key order; **headers differ** (MCP sends `WWW-Authenticate`, REST does not). Sandbox has no MCP endpoint at all | **Overstated** |
| OpenAPI declares `AccessToken` as `Type: oauth2`, `Token URL: https://app.rho.co/settings/access-tokens` | `docs/v1/openapi` | The primary credential is a static opaque `rhobat_` secret pasted from a settings page, not an OAuth token from a token endpoint. The "Token URL" is a human web page, not an OAuth 2.0 token endpoint | **Mis-modeled security scheme**; codegen from this spec will produce a broken OAuth client |
| "fictional, deterministic data" | `docs/v1/getting-started` | Confirmed: byte-identical across tokens and repeats | **Accurate** |
| Production tokens use the `rhobat_` prefix, max 20 active per business, 45-day inactivity expiry, max 1-year expiration, up to 100 allowlisted IPs | `docs/v1/auth` | **Not verifiable** without a real credential. Sandbox ignores token format entirely | Unverified |

---

## 11. What is conspicuously not stated anywhere

- **No CORS policy statement.** The API is browser-unusable cross-origin and nothing in the docs says so.
- **No mention that sandbox skips scope checks.** "Intentionally permissive" is stated about *authentication* only; the reader is left to assume scopes still apply.
- **No mention that sandbox skips rate limiting.** The rate-limit page reads as if it applies to both environments.
- **No sandbox scenario control.** No documented or discoverable way to get a 403, a 429, a 500, a 503, an empty account list, or a second tenant. Three of the five error responses the OpenAPI documents per operation (`403`, `500`, `503`) are unreachable in sandbox, and `401` is only reachable by deliberately breaking the header.
- **No stable machine-readable error code.** `type` is overloaded (`1303` covers seven distinct not-found conditions) and `title` is free prose outside the versioning contract.
- **No environment discriminator** in any response, making a sandbox-vs-production misconfiguration silently indistinguishable.
- **No request-id.** Only Cloudflare's `cf-ray`. Nothing to quote to Rho support.
- **No `WWW-Authenticate` on REST 401s**, and no documentation of that omission.
- **No sandbox MCP endpoint**, and no statement that MCP is production-only.
- **No published error-code registry** for the numeric `type` values. `2`, `1303`, `1317` appear in no corpus page; they are only observable by probing. The gaps in the numbering (1303, 1317) imply a larger internal catalogue that is not published.
- **No token-introspection endpoint** on the resource server: nothing to call to ask "is this token valid, and what scopes does it carry" without performing a real data read.

---

## 12. Practical guidance for an integrator

1. **Do not test auth behavior in sandbox and assume it holds.** Sandbox validates only "non-empty after `Bearer `". It will never produce `403`, `429`, a revoked-token `401`, or an IP-allowlist rejection.
2. **Parse errors defensively.** Four of the nine observed error shapes are not JSON (`text/plain` ×2, `text/html` ×2). Branch on `Content-Type` before parsing, and treat any body as possibly non-JSON.
3. **Branch on the HTTP status, not on `type`.** `type` is a non-URI overloaded integer string with no published registry; `title` is unversioned prose. Neither is a stable contract surface.
4. **Do not infer authentication success from a non-401 status.** Type-binding 400s and 405s are returned before auth runs.
5. **Send the header exactly as `Authorization: Bearer <token>`** with one ASCII space. Lowercase `bearer`, a tab, or a second `Authorization` header all fail, the last one with an HTML body from Cloudflare.
6. **Never put the token in a browser.** No CORS, and the credential is a long-lived secret.
7. **Build backoff blind.** No rate-limit headers exist; you cannot pace from feedback, only react to a `429` you can never rehearse. Follow the docs' advice to stay below 1 req/s with jitter.
8. **Request all five scopes** if building an OAuth partner integration, not the three in `docs/v1/auth`. Confirm against `https://rhoapi.rho.co/.well-known/oauth-protected-resource/mcp/v1`, which is live and authoritative.
9. **Do not generate a client from the OpenAPI security scheme as written.** `Type: oauth2` with a settings page as `Token URL` will produce a client that tries an OAuth flow against an HTML page. Hand-write the bearer header.
10. **Pin the host explicitly and assert on it.** Sandbox and production are byte-identical on failure, so a wrong-host misconfiguration is invisible in the response.

---

## 13. Raw artifact index

All under `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-auth/` (147 files).

| Prefix | Contents |
|---|---|
| `probe.sh` | The harness. `probe.sh <case-id> <url> [curl args…]`, writes `<case-id>.headers` and `<case-id>.body` |
| `01-` … `21-` | Sandbox auth matrix (valid, nonsense, empty, missing, malformed, wrong scheme, long token) |
| `30-` … `34-` | 404 / 405 / 400 error-shape probes |
| `40-` … `43-` | CORS preflight and simple-request probes |
| `50-` … `54-` | **Production**, unauthenticated only |
| `60-`, `61-` | `/api/v2` ingress default-backend probes, both hosts |
| `70-`, `71-` | Sandbox `/mcp/v1` (does not exist) |
| `72-`, `73-` | Production `/mcp/v1` unauthenticated, with `WWW-Authenticate` |
| `74-oauth-protected-resource.*` | RFC 9728 metadata, 5 scopes |
| `75-oidc-config.*` | `auth.rho.co` OIDC discovery (Ory Hydra) |
| `len-<n>.*` | Header-size ladder, 2048 → 8192 |
| `scope-<resource>.*` | Scope-enforcement matrix, one garbage token × 6 endpoints |
| `tenant-*`, `tenantx-*` | Tenant-isolation fixtures (identical md5 across tokens) |
| `burst-unauth.log`, `burst-auth.log` | Rate-limit bursts, 75 and 80 status codes |
