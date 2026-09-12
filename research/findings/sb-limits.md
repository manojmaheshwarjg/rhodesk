# Rho sandbox: observed transport, headers, latency and rate-limit behavior

Empirical characterisation of `https://rhoapi-sandbox.rho.co/api/v1`, bearer token `sandbox`.

| Field | Value |
| --- | --- |
| Probe window | 2026-09-11 23:43:17 UTC to 2026-09-11 23:53:43 UTC (about 10.5 minutes) |
| Client | curl 8.7.1 (x86_64-apple-darwin25.0), libcurl 8.7.1, SecureTransport/LibreSSL 3.3.6, nghttp2 1.68.1 |
| Client location | single residential/office IP, all requests terminated on Cloudflare colo `EWR` (Newark) |
| Total requests issued to the sandbox host | approximately 430 |
| Peak instantaneous rate achieved | 68.9 req/s (60 requests in 0.871 s, concurrency 60) |
| Peak sustained rate achieved | 5.8 req/s for 11.3 s, and 5.6 req/s for 10.7 s |
| HTTP status codes observed on `/api/v1/accounts` with a valid-format bearer | `200` only, 0 non-200 in approximately 350 successful-path requests |
| 429 responses observed | **zero** |
| Raw evidence | `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-limits/` (408 files, 2.9 MB, indexed in `README.md` there) |

Baseline documentation under test: `/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/docs/docs_v1_rate-limits.md`.

---

## 1. Headline findings

1. **Neither documented rate limit is enforced on the sandbox host at any load this probe could ethically generate.** The docs state approximately 60 requests per minute per API Access Token. I issued 150 requests on the token `sandbox` inside a 57-second window (23:47:03 to 23:48:00 UTC) and 65 requests on a brand-new, never-before-used token inside 11.3 seconds. Every one returned `200`. That is 2.5x the documented per-token allowance with zero throttling, and it rules out the possibility that the literal string `sandbox` is simply an allowlisted token, because the unique-token run behaved identically.
2. **Not a single rate-limit-related response header exists.** No `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `X-RateLimit-*`, `Retry-After`, or `RateLimit-Policy` in any of the roughly 430 responses captured. A client has no way to observe its own budget consumption before being cut off.
3. **`429` is unreachable within a responsible probe budget, so the documented `Retry-After` contract is unverifiable.** The rate-limits page specifies branch logic on `Retry-After` including the unusual case of `Retry-After: 0`, but nothing in the live sandbox can be made to emit it. The behavior described in the docs is therefore untested surface from an integrator's point of view.
4. **`429` is absent from the OpenAPI contract entirely.** All 14 operation reference pages document `400, 401, 403, 500, 503` (plus `404` on the 8 single-resource operations). None documents `429`. The prose rate-limits guide and the machine-readable API reference disagree about whether `429` is part of the v1 response set.
5. **There is no server-issued request identifier.** The only per-request correlation handle in any response is Cloudflare's `cf-ray`. There is no `X-Request-Id`, `X-Correlation-Id`, `Traceparent`, `X-Cloud-Trace-Context`, or `X-Amzn-Trace-Id`. For a regulated-money API this is a notable operational gap: a customer reporting a failed call can only cite a CDN ray id.
6. **Conditional requests do not work and cannot work.** No `ETag`, no `Last-Modified`, no `Cache-Control`, no `Vary` is ever emitted. `If-None-Match: *`, `If-None-Match: "abc123"`, and `If-Modified-Since` in both directions all returned a full `200` with the complete body. Bandwidth-efficient polling is impossible.
7. **Compression is gzip-only.** Brotli, zstd and deflate are all declined, and `Vary: Accept-Encoding` is never set. On a 40,768-byte transactions page, gzip cuts the wire payload to about 5.6 to 6.0 KB, a 6.8x to 7.2x reduction, so omitting `Accept-Encoding: gzip` costs an integrator roughly 7x the bytes.
8. **The API is unusable from a browser.** `OPTIONS` returns `405` with no CORS headers at all, and a GET carrying an `Origin` header gets no `Access-Control-Allow-Origin`. This is a deliberate server-to-server posture, but it is never stated in the docs.
9. **`HEAD` is not supported.** `HEAD /api/v1/accounts` returns `405` with `allow: GET`. RFC 9110 treats `HEAD` as mandatory wherever `GET` is implemented, so this is a spec deviation, and it breaks the common "cheap liveness check" pattern.
10. **MCP does not exist on the sandbox host.** `/mcp/v1` on `rhoapi-sandbox.rho.co` returns `404 default backend - 404`, the ingress-nginx default backend, meaning no route is configured. The same path on production `rhoapi.rho.co` returns a proper `401 application/problem+json`. The MCP doc never says the sandbox lacks an MCP surface.

---

## 2. Transport layer

### 2.1 DNS

| Host | A records | AAAA records |
| --- | --- | --- |
| `rhoapi-sandbox.rho.co` | `104.18.26.176`, `104.18.27.176` | `2606:4700::6812:1ab0`, `2606:4700::6812:1bb0` |
| `rhoapi.rho.co` | `104.18.27.176`, `104.18.26.176` | (same Cloudflare anycast range) |

Sandbox and production resolve to the **same Cloudflare anycast IP pair**. No CNAME is exposed. DNS resolution measured at 2.2 to 4.2 ms (p50 3.3 ms) from a warm resolver cache.

Consequence for the documented per-source-IP limit: because both environments share the same edge IPs, a "per source IP" limit as documented must be keyed on the *client's* source IP, not the server IP. Sandbox and production traffic from one integrator would land on the same counter if the counter is client-IP-keyed and environment-agnostic. The docs do not say whether sandbox and production share an IP budget.

### 2.2 TLS

| Property | Observed |
| --- | --- |
| Negotiated protocol (default) | TLSv1.3 |
| Negotiated cipher (TLS 1.3) | `AEAD-CHACHA20-POLY1305-SHA256` |
| TLS 1.2 forced (`--tls-max 1.2`) | accepted, `ECDHE-ECDSA-AES128-GCM-SHA256`, ALPN still `h2` |
| TLS 1.1 forced (`--tls-max 1.1`) | **rejected**, `tlsv1 alert protocol version`, connection closed, curl exit code 000 |
| ALPN offered by client | `h2,http/1.1` |
| ALPN selected by server | `h2` |
| Handshake duration | min 31.9 ms, p50 40.3 ms, p90 55.2 ms, max 290.4 ms (n=20) |
| Session timeout advertised | 7200 s |
| Certificate verification | `Verify return code: 0 (ok)` |

Certificate chain (3 certificates, all captured to `probe-limits/cert_1.pem` through `cert_3.pem`):

| Depth | Subject | Issuer | Serial | Not before | Not after | Key | Sig alg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 (leaf) | `CN=rhoapi-sandbox.rho.co` | `C=US, O=Google Trust Services, CN=WE1` | `E10FCE516085ECC90E0FA59077DBB34B` | 2026-08-28 11:19:11 UTC | **2026-11-26 12:19:05 UTC** | EC P-256 | `ecdsa-with-SHA256` |
| 1 | `C=US, O=Google Trust Services, CN=WE1` | `C=US, O=Google Trust Services LLC, CN=GTS Root R4` | `7FF31977972C224A76155D13B6D685E3` | 2023-12-13 09:00:00 UTC | 2029-02-20 14:00:00 UTC | EC P-256 | `ecdsa-with-SHA384` |
| 2 | `C=US, O=Google Trust Services LLC, CN=GTS Root R4` | `C=BE, O=GlobalSign nv-sa, OU=Root CA, CN=GlobalSign Root CA` | `7FE530BF331343BEDD821610493D8A1B` | 2023-11-15 03:43:21 UTC | 2028-01-28 00:00:42 UTC | EC P-384 | `sha256WithRSAEncryption` |

Notes:
- Leaf SAN is exactly one name, `DNS:rhoapi-sandbox.rho.co`. Production is a separate certificate.
- Leaf validity is a 90-day window issued 2026-08-28. As of 2026-09-11 it has **76 days** remaining.
- Issuance is Google Trust Services WE1 through Cloudflare, i.e. Cloudflare Universal SSL with a GTS-backed leaf, not an origin certificate exposed to the client.
- All-ECDSA leaf and intermediate. An integrator pinning to an RSA chain will fail.

### 2.3 HTTP versions

| Test | Result |
| --- | --- |
| Default request | **HTTP/2** (`HTTP/2 200`), negotiated via ALPN |
| Forced `--http1.1` | works, `HTTP/1.1 200 OK`, adds `Transfer-Encoding: chunked` and `Connection: keep-alive` |
| HTTP/3 | **not advertised**. No `alt-svc` header on any of approximately 430 responses. Notable because Cloudflare zones normally advertise `h3`; HTTP/3 appears disabled for this hostname |
| Connection reuse | confirmed: 20 requests, then 60 requests, then 65 requests each completed with `num_connects=1` |
| Multiplexing | confirmed: 50 concurrent requests completed over a single h2 connection in 1.596 s |
| Port 80 | `301 Moved Permanently` to the identical `https://` URL. Response carries `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` but correctly omits `Strict-Transport-Security` over plaintext |
| IPv4 forced | `200`, remote_ip `104.18.26.176` |
| IPv6 forced | `200`, remote_ip `2606:4700::6812:1ab0` |

On HTTP/2, successful `200` responses carry **no `content-length`**; the body is delivered as a length-unknown h2 data stream. Error responses (`401`, `404`, `400`) **do** carry `content-length`. This asymmetry means a client cannot pre-size a success buffer but can pre-size an error.

---

## 3. Response header inventory

### 3.1 Complete header set on a `200`

Verbatim, from `probe-limits/01-baseline.headers`:

```
HTTP/2 200
date: Fri, 11 Sep 2026 23:43:17 GMT
content-type: application/json
via: 1.1 google
cf-cache-status: DYNAMIC
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=63072000; includeSubDomains; preload
x-content-type-options: nosniff
x-frame-options: DENY
server: cloudflare
cf-ray: a39a88a81db98ae3-EWR
```

Ten headers. Header order was stable across 60 concurrent responses in run D: all 60 carried exactly `x-frame-options, x-content-type-options, via, strict-transport-security, server, referrer-policy, date, content-type, cf-ray, cf-cache-status`, with no extras and no omissions.

### 3.2 Union of every header name seen across all probes

`allow`, `cache-control`, `cf-cache-status`, `cf-ray`, `connection`, `content-encoding`, `content-length`, `content-type`, `date`, `expires`, `referrer-policy`, `server`, `strict-transport-security`, `transfer-encoding`, `via`, `x-content-type-options`, `x-frame-options`.

That is 17 distinct names total, and `cache-control` plus `expires` appear only on the Cloudflare WAF block page, never on an API response.

### 3.3 Header set by status class

| Header | 200 | 400 / 401 / 404 (problem+json) | 405 (origin) | 411 (upstream) | 414 (nginx) | 403 (CF WAF) | 301 (port 80) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `date` | yes | yes | yes | yes | yes | yes | yes |
| `content-type` | `application/json` | `application/problem+json` | absent on HEAD, `content-length: 0` otherwise | `text/html; charset=UTF-8` | `text/html` | `text/html; charset=UTF-8` | `text/html; charset=UTF-8` |
| `content-length` | **absent** | yes | `0` | absent | absent | absent | absent (chunked) |
| `via: 1.1 google` | yes | yes | yes | **absent** | yes | **absent** | **absent** |
| `cf-cache-status` | `DYNAMIC` | `DYNAMIC` | `DYNAMIC` | `DYNAMIC` | `DYNAMIC` | absent | absent |
| `cf-ray` | yes | yes | yes | yes | yes | yes | yes |
| `server: cloudflare` | yes | yes | yes | yes | yes | yes | yes |
| `strict-transport-security` | yes | yes | yes | yes | yes | yes | **absent, correct** |
| `x-content-type-options` | yes | yes | yes | yes | yes | yes | yes |
| `x-frame-options` | yes | yes | yes | yes | yes | yes | yes |
| `referrer-policy` | yes | yes | yes | yes | yes | yes | yes |
| `allow` | no | no | `GET` | no | no | no | no |
| `cache-control` | no | no | no | no | no | `private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0` | no |
| `expires` | no | no | no | no | no | `Thu, 01 Jan 1970 00:00:01 GMT` | no |

The presence or absence of `via: 1.1 google` is a reliable tell for which layer produced the response: with it, the request reached the Google-fronted origin stack; without it, Cloudflare or the Google frontend terminated it early.

### 3.4 Header value census over approximately 250 captured responses

| Header | Distinct values observed | Detail |
| --- | --- | --- |
| `cf-cache-status` | 1 | `DYNAMIC` on 249 of 249 API responses. Nothing is ever cached at the edge, and nothing ever will be while no `Cache-Control` is emitted. |
| `cf-ray` colo suffix | 1 | `EWR` on 251 of 251. No colo flapping, no anycast drift during the probe. |
| `strict-transport-security` | 1 | `max-age=63072000; includeSubDomains; preload`, i.e. 2 years, subdomains included, preload asserted. |
| `server` | 1 | `cloudflare` always; the origin server software is never leaked in this header. |
| `via` | 1 | `1.1 google`. |

### 3.5 Headers conspicuously NOT present

| Missing header | Why it matters |
| --- | --- |
| `RateLimit-Limit` / `RateLimit-Remaining` / `RateLimit-Reset` (RFC 9331 draft) | No budget observability. The docs tell clients to "pace traffic steadily below one request per second" but give them no feedback signal to pace against. |
| `X-RateLimit-*` (the de-facto Stripe/GitHub convention) | Same. Rho's own comparison content positions it against fintech API peers, all of whom emit these. |
| `Retry-After` | Documented as the backoff contract for `429`; never observed on any status, including the `405`, `411`, `414` and `403` paths where it would be harmless. |
| `X-Request-Id` / `Request-Id` / `X-Correlation-Id` | No support-ticket correlation handle other than `cf-ray`. |
| `traceparent` / `tracestate` / `X-Cloud-Trace-Context` | No distributed-trace propagation back to the caller. |
| `ETag` / `Last-Modified` | Conditional GET impossible. |
| `Cache-Control` / `Expires` on API responses | Caching semantics are left entirely undefined; intermediaries must guess. |
| `Vary` | gzip and identity are served from the same URL with no `Vary: Accept-Encoding`. Any shared cache in front of an integrator's fleet can serve a gzip body to a client that did not ask for one. |
| `Access-Control-Allow-Origin` and all `Access-Control-*` | Browser clients are excluded. Never stated in the docs. |
| `WWW-Authenticate` on `401` | RFC 9110 section 11.6.1 makes `WWW-Authenticate` mandatory on `401`. Rho returns `401` without it, on both sandbox and production. |
| `Content-Security-Policy`, `Permissions-Policy` | Present on neither, though `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff` are set. Low impact for a JSON API. |
| `alt-svc` | No HTTP/3 upgrade path. |
| `Deprecation` / `Sunset` (RFC 8594) | The versioning doc promises "at least 15 days' notice" before a v1 deprecation, but there is no machine-readable header channel to deliver that notice on. Integrators must watch the docs by hand. |

---

## 4. Latency distribution

All figures in milliseconds. `server ttfb` is `time_starttransfer - time_pretransfer`, i.e. the interval from the request being fully written to the first response byte, excluding DNS, TCP and TLS.

### 4.1 Run A: 20 sequential requests, new TLS connection each, paced 1.1 s apart

`GET /api/v1/accounts`, 2,558-byte response.

| Phase | n | min | p50 | p90 | p95 | max | mean | sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DNS lookup | 20 | 2.2 | 3.3 | 3.7 | 3.8 | 4.2 | 3.2 | 0.5 |
| TCP connect | 20 | 19.0 | 28.3 | 140.4 | 218.2 | 232.9 | 56.6 | 62.7 |
| TLS handshake | 20 | 31.9 | 40.3 | 55.2 | 82.9 | 290.4 | 54.3 | 54.9 |
| **Server TTFB** | 20 | **98.8** | **123.9** | **142.0** | **143.2** | **145.4** | **124.9** | **13.0** |
| Total wall | 20 | 160.8 | 206.5 | 378.5 | 408.7 | 442.1 | 242.2 | 77.0 |

The server-side component is remarkably tight: standard deviation 13.0 ms, full range 98.8 to 145.4 ms. Essentially all of the wall-clock variance comes from TCP connect and TLS handshake, that is, from the anycast edge, not from Rho's application.

### 4.2 Run B: 20 requests over one reused HTTP/2 connection

| Metric | n | min | p50 | p90 | p95 | max | mean | sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Server TTFB, warm (requests 2 to 20) | 19 | 88.3 | 111.7 | 133.8 | 146.0 | 203.5 | 115.9 | 24.7 |

Connection reuse saves the whole connect plus handshake cost, roughly 70 to 100 ms per request on this path. Warm p50 of 111.7 ms versus cold total p50 of 206.5 ms means keep-alive halves effective latency.

### 4.3 All load-shape runs side by side

| Run | Shape | Endpoint | Payload | n | min | p50 | p90 | max | Wall span | Effective rate | Non-200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | sequential, new conn, 1.1 s pacing | `/accounts` | 2,558 B | 20 | 160.8 | 206.5 | 378.5 | 442.1 | approx 24 s | 0.83 req/s | 0 |
| B | sequential, 1 conn | `/accounts` | 2,558 B | 20 | 88.3* | 111.7* | 133.8* | 203.5* | approx 2.5 s | approx 8 req/s | 0 |
| C | 60 sequential, 1 conn, unpaced | `/accounts` | 2,558 B | 59 | 85.2 | 119.5 | 339.0 | 832.7 | 10.67 s | 5.6 req/s | 0 |
| D | 60 at concurrency 30, separate conns | `/accounts` | 2,558 B | 60 | 197.2 | 474.8 | 765.9 | 798.4 | 1.173 s | 51.2 req/s | 0 |
| E | 60 at concurrency 60, separate conns | `/accounts` | 2,558 B | 60 | 368.6 | 430.7 | 477.6 | 494.8 | 0.871 s | **68.9 req/s** | 0 |
| F | 50 multiplexed on 1 h2 conn | `/accounts` | 2,558 B | 50 | 1005.1 | 1504.1 | 1543.9 | 1551.4 | 1.596 s | 31.3 req/s | 0 |
| G | 30 at concurrency 30 | `/transactions?page_size=100` | 40,768 B | 30 | 259.1 | 366.5 | 542.9 | 570.1 | approx 1.0 s | approx 30 req/s | 0 |
| H | 65 sequential, 1 conn, **unique bearer token** | `/accounts` | 2,558 B | 64 | 85.4 | 118.1 | 371.5 | 630.7 | 11.30 s | 5.8 req/s | 0 |

\* Run B figures are server TTFB, not total wall, because the connection was already established.

### 4.4 Per-endpoint latency, 3 requests each over a warm connection

Times are `time_starttransfer` in seconds; the first value in each row includes connection setup.

| Endpoint | Response size | r1 | r2 | r3 |
| --- | --- | --- | --- | --- |
| `/accounts` | 2,558 B | 0.394 | 0.292 | 0.129 |
| `/transactions?page_size=100` | 40,768 B | 0.213 | 0.148 | 0.122 |
| `/cards` | 6,357 B | 0.195 | 0.119 | 0.114 |
| `/statements` | 28,132 B | 0.197 | 0.109 | 0.086 |
| `/invoicing/customers` | 3,383 B | 0.465 | 0.113 | 0.099 |
| `/invoicing/invoices` | 15,390 B | 0.476 | **1.055** | 0.120 |

Two observations. First, **payload size does not drive latency**: the 40 KB transactions page is not slower than the 2.5 KB accounts page, consistent with fully precomputed, in-memory deterministic fixtures. Second, there is a fat tail: a single `/invoicing/invoices` call took 1.055 s, roughly 9x the warm median, with no accompanying error. Under the 50-way multiplex test (run F) every stream took 1.0 to 1.55 s, so a shared single-connection backlog serialises badly.

### 4.5 Concurrency behavior

| Concurrency | Per-request p50 | Per-request max | Aggregate throughput |
| --- | --- | --- | --- |
| 1 (warm) | 112 ms | 204 ms | approx 8 req/s |
| 30 (separate conns) | 475 ms | 798 ms | 51.2 req/s |
| 60 (separate conns) | 431 ms | 495 ms | 68.9 req/s |
| 50 (one h2 conn, multiplexed) | 1504 ms | 1551 ms | 31.3 req/s |

Latency inflates roughly 4x from concurrency 1 to concurrency 30 to 60, but **no request failed, no request was shed, and no 5xx appeared**. The tightening of the spread at concurrency 60 (sd 29.4 ms versus 254.9 ms at concurrency 30) indicates that the backend saturates into an orderly queue rather than degrading unevenly.

Single-connection multiplexing is the worst-performing shape: 50 streams on one connection produced a 1.5 s p50, roughly 13x the warm single-stream p50, for only 31 req/s aggregate. An integrator that opens one connection and multiplexes heavily will see far worse per-call latency than one that spreads across several connections, which runs directly counter to the usual HTTP/2 advice.

### 4.6 Clock

Server `date` matched the client's UTC clock to the second (`Fri, 11 Sep 2026 23:52:23 GMT` on both). No meaningful skew.

---

## 5. Rate limits: documented versus observed

### 5.1 What the docs say

From `docs/docs_v1_rate-limits.md`, verbatim:

| Limit | Threshold |
| --- | --- |
| Per API Access Token | Approximately 60 requests per minute |
| Per source IP | Approximately 600 requests per minute |

Plus these prose commitments:
- "These limits apply uniformly across all public Rho API endpoints."
- "The source-IP limit covers the combined traffic from every integration sharing that IP address, including integrations using different API Access Tokens."
- "We enforce rate limits across a distributed edge network, so the limits are approximate rather than an exact concurrency allowance. Clients must not assume that exactly 60 simultaneous requests will succeed."
- "Pace traffic steadily below one request per second instead of sending the full minute's allowance in a burst."
- "When a limit is exceeded, we return `429 Too Many Requests`."
- `Retry-After` positive integer: wait at least that many seconds. `Retry-After: 0`: "we have not applied a fixed cooldown... use exponential backoff with jitter instead of retrying in a tight loop."

### 5.2 What was observed

| Test | Documented expectation | Observed | Verdict |
| --- | --- | --- | --- |
| 60 requests on token `sandbox` in 10.67 s (337 req/min pace) | should cross the approximately 60/min token limit after request 60 within the minute | 60 x `200`, single connection, zero throttling | **limit not enforced** |
| Additional 60 requests at concurrency 30 in 1.173 s, same token, same minute | cumulative approximately 120 in the minute, 2x the token limit | 60 x `200` | **limit not enforced** |
| Additional 30 requests at concurrency 30 on a 40 KB endpoint, same minute | cumulative approximately 150 in the minute, 2.5x | 30 x `200` | **limit not enforced** |
| Cumulative window 23:47:03 to 23:48:00 UTC (57 s) | at least 150 requests on one token from one IP | zero `429`, zero `5xx` | **limit not enforced** |
| 60 requests at concurrency 60 in 0.871 s (68.9 req/s = 4,134 req/min instantaneous) | docs explicitly warn "clients must not assume that exactly 60 simultaneous requests will succeed" | all 60 succeeded | **the warned-about failure did not occur** |
| 65 requests on a never-before-seen bearer token `probe-uniq-1789170731-50749` in 11.30 s (345 req/min pace) | fresh token bucket should be exhausted after approximately 60 | 65 x `200` | **limit not enforced, and the `sandbox` token is not specially allowlisted** |
| `Retry-After` on any response | present on `429` | never observed on any status | **unverifiable** |
| `429` body shape | not documented anywhere, including the OpenAPI reference | never observed | **unknown** |
| Rate-limit headers | not promised by the docs, and indeed absent | absent | consistent, but a usability gap |

### 5.3 Divergence table

| # | Documented | Actual on sandbox | Severity for an integrator |
| --- | --- | --- | --- |
| 1 | approximately 60 req/min per API Access Token | at least 150 req/min tolerated on one token; at least 65 req in 11.3 s on a fresh token; no throttle at 68.9 req/s instantaneous | High. An integrator who load-tests against sandbox will build a client that production may reject. Sandbox provides no negative feedback for a client that violates the documented budget. |
| 2 | approximately 600 req/min per source IP | not reached in this probe (approximately 430 requests over 10.5 minutes, peak 150 in one rolling minute). Unrefuted but also unconfirmed. | Medium. Reaching it would require a deliberate flood, which this probe did not run. |
| 3 | `429 Too Many Requests` is returned when a limit is exceeded | `429` was not reachable; zero observed in approximately 430 requests | High. The retry path that every integrator must implement cannot be exercised in the sandbox. There is no way to test backoff code against Rho's own test environment. |
| 4 | `Retry-After` header carries the cooldown, with a specified `0` special case | never emitted on any status code | High. The documented branch logic (`positive integer` versus `0`) is dead code for anyone who cannot produce a `429`. |
| 5 | "These limits apply uniformly across all public Rho API endpoints" | no endpoint-specific throttling observed either; `/transactions?page_size=100` at 40 KB per response, 30 concurrent, was served without shedding | Low as stated, but it means payload-weighted limits, if any exist in production, are also untestable. |
| 6 | "We enforce rate limits across a distributed edge network" | Cloudflare is in the path (`server: cloudflare`, `cf-ray`, all colo `EWR`) but no rate-limiting rule fired at 68.9 req/s from a single IP | High. Either no Cloudflare rate-limit rule is bound to the sandbox hostname, or its threshold is far above the documented figures. |
| 7 | "Pace traffic steadily below one request per second" | 5.6 to 5.8 req/s sustained for over 10 s produced zero errors; 68.9 req/s produced zero errors | Medium. The advice is 5x to 70x more conservative than observed sandbox tolerance, which trains integrators to distrust the guidance. |
| 8 | The rate-limits guide asserts `429` is part of the API's behavior | **no OpenAPI operation page documents a `429` response**. All 14 operations list `200, 400, 401, 403, 500, 503`; 8 single-resource operations add `404` | High. Generated clients will not have a `429` case. A codegen consumer of the OpenAPI document produces a client that treats `429` as an unexpected status. |
| 9 | No mention of rate-limit observability headers | none present | Medium. Without `RateLimit-Remaining` an integrator cannot self-pace; the only strategy left is fixed, conservative pacing. |
| 10 | Rate-limits page does not distinguish sandbox from production | sandbox demonstrably does not enforce; production unprobed for limits (only 3 unauthenticated requests were sent there, to compare error shape) | High. The docs give no warning that sandbox limits differ from production limits. This is the single most load-bearing unstated caveat on the page. |

### 5.4 What was deliberately NOT tested

- No attempt was made to reach the approximately 600 req/min per-source-IP threshold. That would require more than 600 requests inside 60 seconds against a shared multi-tenant sandbox, which is the "sustained flood" the probe brief rules out. The per-IP limit is therefore neither confirmed nor refuted.
- No rate-limit probing was performed against production `rhoapi.rho.co`. Exactly three requests reached production (two unauthenticated `401` comparisons and one `/mcp/v1` probe), all rejected by auth.
- No authenticated production traffic exists, so the possibility that limits are enforced only in production is open and, given the evidence, likely.

---

## 6. Compression

Every test against `GET /api/v1/transactions?page_size=100`, a 40,768-byte uncompressed body.

| `Accept-Encoding` sent | `Content-Encoding` returned | Wire bytes | Ratio | Decoded matches identity? |
| --- | --- | --- | --- | --- |
| `gzip` | `gzip` | 5,645 | 7.22x | yes, md5 `0e3829abca0416ff2e2058ec9cd1f6eb` |
| `gzip, deflate, br, zstd` | `gzip` | 5,962 | 6.84x | yes, same md5 |
| `br` | none | 40,768 | 1.00x | n/a |
| `deflate` | none | 40,768 | 1.00x | n/a |
| `zstd` | none | 40,768 | 1.00x | n/a |
| `identity` | none | 40,768 | 1.00x | n/a |
| `*` | none | 40,768 | 1.00x | n/a |
| header omitted entirely | none | 40,768 | 1.00x | n/a |

Findings:
- **gzip only.** Brotli and zstd are not served, which is unusual behind Cloudflare (Cloudflare normally brotli-encodes `application/json`). This is consistent with compression being applied by the origin stack, not the edge, and with the edge passing the body through untouched because `cf-cache-status: DYNAMIC`.
- `Accept-Encoding: *` does **not** trigger compression. A client relying on the wildcard gets the full 40 KB. Clients must name `gzip` explicitly.
- **No `Vary: Accept-Encoding` is ever emitted**, on either the gzip or the identity response. This is a correctness bug for any intermediary cache: the same URL returns two different representations with nothing telling a cache to key on the request encoding.
- Compressed sizes differ between two identical requests (5,645 versus 5,962 bytes, 5.6 percent apart) for a byte-identical 40,768-byte payload. Same content, same md5 after decode. That implies at least two compressor configurations or levels in the fleet, likely different instances or a compression step that varies with buffering.
- Body content is fully deterministic: all 30 concurrent responses in run G decoded to a single md5, and identity, gzip, br, zstd and no-header variants all produced md5 `0e3829abca0416ff2e2058ec9cd1f6eb`.

---

## 7. Conditional requests and caching

| Request | Response |
| --- | --- |
| `If-None-Match: *` | `200`, full 2,558-byte body, 0.278 s |
| `If-None-Match: "abc123"` | `200`, full 2,558-byte body, 0.220 s |
| `If-Modified-Since: Fri, 11 Sep 2026 00:00:00 GMT` (today) | `200`, full body, 0.196 s |
| `If-Modified-Since: Thu, 01 Jan 2015 00:00:00 GMT` (ancient) | `200`, full body, 0.195 s |

**Conditional requests are entirely unimplemented.** No `304` is reachable. This follows necessarily from the absence of `ETag` and `Last-Modified`, since there is no validator for a client to echo.

Caching posture:
- `cf-cache-status: DYNAMIC` on 249 of 249 API responses. Cloudflare never caches, never will, because no `Cache-Control` is present to make the response cacheable.
- No `Cache-Control`, no `Expires`, no `Age`, no `Vary` on any API response.
- `If-None-Match: *` returning `200` rather than the RFC-correct outcome for a GET with no matching representation is a minor spec deviation on top of the larger gap.

Consequence: an integrator polling `/transactions` every minute for change detection pays full payload cost on every poll, roughly 5.6 KB gzipped or 40 KB raw per page. There is no cheap "has anything changed" primitive, and no webhook surface is documented anywhere in the corpus either.

---

## 8. Method and malformed-request handling

| Method / request | Status | Body / key headers | Produced by |
| --- | --- | --- | --- |
| `GET /api/v1/accounts` | `200` | `application/json`, chunked | Go API service |
| `HEAD /api/v1/accounts` | `405` | `allow: GET`, no body | Go API service (`via: 1.1 google` present) |
| `OPTIONS /api/v1/accounts` | `405` | `allow: GET`, `content-length: 0` | Go API service |
| `OPTIONS` with `Origin` + `Access-Control-Request-Method: GET` | `405` | `allow: GET`, **no `Access-Control-*` headers** | Go API service |
| `GET` with `Origin: https://evil.example` | `200` | **no `Access-Control-Allow-Origin`** | Go API service |
| `POST` with no `Content-Length` | `411` | `<title>411 Length Required</title>`, `<h2>POST requests require a <code>Content-length</code> header.</h2>`, **no `via` header** | Google Frontend, before the origin |
| `PUT` with no `Content-Length` | `411` | identical GFE page, which still says "POST requests require..." | Google Frontend |
| `POST` with `Content-Length: 0` | `405` | `allow: GET`, `content-length: 0` | Go API service |
| `POST` with `Content-Type: application/json` and body `{}` | `405` | `allow: GET` | Go API service |
| `PATCH` | `405` | `allow: GET` | Go API service |
| `DELETE` | `405` | `allow: GET` | Go API service |
| `TRACE` | `405` | `<hr><center>cloudflare</center>` nginx-style page | Cloudflare edge |
| `FOO` (invalid method token) | `403` | `<title>Attention Required! | Cloudflare</title>`, `cache-control: private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0`, `expires: Thu, 01 Jan 1970 00:00:01 GMT` | Cloudflare WAF block page |
| `GET /api/v1/nope-not-a-real-endpoint` | `404` | `404 page not found` (19 bytes), `text/plain; charset=utf-8` | Go `http.NotFound` |
| `GET /` (host root) | `404` | `default backend - 404` (21 bytes), `text/plain; charset=utf-8` | ingress-nginx default backend |
| `GET /api/v1/accounts?x=<8000 chars>` | `200` | normal JSON | accepted |
| `GET /api/v1/accounts?x=<16000 chars>` | `414` | `<title>414 Request-URI Too Large</title>`, `<hr><center>nginx</center>`, `via: 1.1 google` present | ingress-nginx |
| `GET` with a single approximately 12 KB request header | `200` | normal JSON | accepted |

Notes:
- The **URI length ceiling sits between 8 KB and 16 KB** and is enforced by nginx, not by the application. Given that `page_token` cursors are opaque strings, a very long cursor chain is theoretically at risk; observed cursors are far shorter.
- A single approximately 12 KB request header is accepted, so the header-size ceiling is above that.
- The `411` from the Google frontend is a useful fingerprint: `POST` without `Content-Length` never reaches Rho's code. The `PUT` case returns the same page still worded for `POST`, which is Google's bug, not Rho's, but it will confuse an integrator debugging a write attempt.
- Sending a nonstandard method token gets the caller a Cloudflare WAF `403` block page, not a `405`. A client library that probes with an unusual verb risks tripping WAF reputation scoring.

---

## 9. Error catalogue observed (RFC 9457 problem details)

The OpenAPI overview states "Errors follow RFC 9457 problem details" and the per-operation pages describe `type` as "A URI reference that identifies the problem type. Example: about:blank".

| Request | Status | `content-type` | Body verbatim |
| --- | --- | --- | --- |
| `GET /accounts` with no `Authorization` (production) | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| `GET /accounts` with `Bearer rho_not_a_real_token_000` (production) | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| `GET /accounts` with `Authorization: Bearer ` (empty, sandbox) | `401` | `application/problem+json` | `{"type":"2","title":"Unauthenticated","status":401}` |
| `GET /mcp/v1` no auth (production) | `401` | `application/problem+json` | `{"status":401,"title":"Unauthenticated","type":"2"}` |
| `GET /accounts/00000000-0000-4000-8000-000000000000` | `404` | `application/problem+json` | `{"type":"1303","title":"account not found","status":404}` |
| `GET /accounts/not-a-uuid` | `400` | `application/problem+json` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: account_id"}` |
| `GET /transactions?page_size=101` | `400` | `application/problem+json` | `{"type":"1317","title":"page_size must be between 1 and 100","status":400}` |
| `GET /accounts?sort_by=bogus` | `400` | `application/problem+json` | `{"type":"1317","title":"invalid sort_by parameter: \"bogus\"","status":400}` |
| `GET /accounts?bogus=1&page_size=abc` | `400` | `application/problem+json` | `{"type":"about:blank","title":"Bad Request","status":400,"detail":"invalid parameter: page_size"}` |

Observations:
- **`type` is not a URI reference**, contradicting the OpenAPI field description. Observed values: `"2"`, `"1303"`, `"1317"`, and `"about:blank"`. These are bare numeric strings, not URIs. RFC 9457 says a non-URI `type` should be treated as `about:blank`, so any strictly conforming client will collapse `"2"`, `"1303"` and `"1317"` into the same generic type and lose the distinction.
- **Two distinct error producers.** Errors with `type: "about:blank"` and a `detail` field are framework-level parameter validation; errors with a numeric `type` and a descriptive `title` but no `detail` are application-level. They never co-occur in one body, and `detail` is present only on the `about:blank` family.
- **JSON key order differs between services.** `/api/v1` emits `{"type","title","status"}`; `/mcp/v1` on production emits `{"status","title","type"}`. Same struct, different serializer ordering, which points to two separate implementations behind one contract.
- **No `WWW-Authenticate` on any `401`**, on sandbox or production.
- Unknown query parameters are silently ignored (`bogus=1` produced no complaint); only recognised-but-invalid parameters are rejected.
- Error code `1317` covers at least two different validation failures (`page_size` range, `sort_by` value), so `type` is a coarse family, not a precise identifier.

---

## 10. Infrastructure fingerprint

Four layers are distinguishable from error pages alone:

| Layer | Evidence | Notes |
| --- | --- | --- |
| 1. Cloudflare edge | `server: cloudflare`, `cf-ray: <id>-EWR`, `cf-cache-status: DYNAMIC`, the `TRACE` `405` page footed `cloudflare`, the `FOO` `403` "Attention Required! | Cloudflare" page | Proxied, Universal SSL with a Google Trust Services WE1 leaf. No rate-limiting rule observed firing. |
| 2. Google frontend / Cloud load balancer | `via: 1.1 google` on everything that reaches the origin; the `411` page `<h1>Error: Length Required</h1>` with `<h2>POST requests require a <code>Content-length</code> header.</h2>` and **no** `via` header | Classic GFE. Terminates `POST`/`PUT` without `Content-Length` before Rho's code sees them. |
| 3. ingress-nginx (Kubernetes) | `GET /` returns `default backend - 404`, the exact ingress-nginx default-backend string; the `414` page footed `nginx` with `via: 1.1 google` present | Confirms a Kubernetes ingress in front of the service. URI-length ceiling enforced here, between 8 KB and 16 KB. |
| 4. Go HTTP service | `GET /api/v1/<unknown>` returns `404 page not found` with `text/plain; charset=utf-8` and `X-Content-Type-Options: nosniff`, the byte-exact output of Go's `http.NotFound`; `405` responses carry `allow: GET` | The API itself is a Go service. Header order on `200` is stable across concurrent responses, consistent with a single handler chain. |

The origin server software is never leaked via `Server:` (always `cloudflare`), but the error pages of three separate upstream layers leak it anyway.

---

## 11. Sandbox versus production divergences

| Surface | Sandbox `rhoapi-sandbox.rho.co` | Production `rhoapi.rho.co` | Documented? |
| --- | --- | --- | --- |
| Edge IPs | `104.18.26.176`, `104.18.27.176` | same pair | no |
| TLS leaf | `CN=rhoapi-sandbox.rho.co`, GTS WE1, expires 2026-11-26 | separate cert, not enumerated here | no |
| Auth | "accepts any non-empty bearer token" per the getting-started doc; empty bearer returns `401` | real token required; both no-token and bogus-token return the same `401` body | yes, in getting-started |
| `/mcp/v1` | **`404` `default backend - 404`**, i.e. the route does not exist | `401 application/problem+json` `{"status":401,...}`, i.e. the route exists and demands auth | **no** |
| `/mcp` | `404 default backend - 404` | not probed | no |
| `/api/v1/mcp` | `404 page not found` (Go router, so the API service is reached but has no such route) | not probed | no |
| Rate limits | not enforced up to 68.9 req/s and 150 req/min per token | not probed | **no** |
| Error body shape | identical problem+json families | identical | partially |
| Response header set | identical 10-header set | identical 10-header set on `401` | no |

The MCP gap matters: `docs/docs_v1_mcp.md` documents `/mcp/v1` as the MCP surface, states "MCP uses the same API contract, authentication model, scopes, and error behavior as the REST API", and gives a `claude mcp add` example pointing at the **production** URL. It never says the sandbox has no MCP endpoint. An integrator following the sandbox-first advice in getting-started, and substituting the sandbox host into the MCP URL by analogy with the REST host, hits a bare `404` with no explanation.

---

## 12. Contradictions and unstated caveats

| # | Contradiction or gap | Sources |
| --- | --- | --- |
| 1 | Rate-limits page says `429` is returned when a limit is exceeded; **no OpenAPI operation documents a `429` response** | `docs/docs_v1_rate-limits.md` line 23 versus all 14 files in `api/` |
| 2 | Rate-limits page gives concrete thresholds with no environment qualifier; sandbox enforces neither | `docs/docs_v1_rate-limits.md` versus runs C, D, E, G, H |
| 3 | OpenAPI describes problem `type` as "A URI reference... Example: about:blank"; live values are `"2"`, `"1303"`, `"1317"` | `api/accounts_listaccounts.md` versus `probe-limits/80-*.body`, `50-prod-noauth.body` |
| 4 | Docs never mention CORS; the API is unusable from a browser (`OPTIONS` -> `405`, no `Access-Control-*` on any response) | corpus silence versus `probe-limits/08`, `09`, `10` |
| 5 | Docs never mention `HEAD` being unsupported; `HEAD` returns `405 allow: GET` | corpus silence versus `probe-limits/07-head.headers` |
| 6 | Docs never mention compression; only `gzip` works, `Accept-Encoding: *` is ignored, `Vary` is never set | corpus silence versus `probe-limits/02-enc-*` |
| 7 | Docs never mention caching or conditional requests; no `ETag`, no `304` path exists | corpus silence versus `probe-limits/03` to `06` |
| 8 | Versioning page promises "at least 15 days' notice" for deprecation; no `Deprecation` or `Sunset` header channel exists to carry it | `docs/docs_v1_versioning.md` versus the header union in section 3.2 |
| 9 | MCP page documents `/mcp/v1` with no note that the sandbox lacks it | `docs/docs_v1_mcp.md` versus `probe-limits/64-mcp_mcp_v1.body` |
| 10 | `401` responses omit the RFC-mandatory `WWW-Authenticate` header on both environments | RFC 9110 11.6.1 versus `probe-limits/50`, `51`, `52` |
| 11 | Rate-limits page warns "Clients must not assume that exactly 60 simultaneous requests will succeed"; 60 simultaneous requests did all succeed, twice | `docs/docs_v1_rate-limits.md` line 15 versus runs D and E |
| 12 | Two gzip encoders in the fleet produce 5,645 versus 5,962 bytes for byte-identical content | `probe-limits/02-enc-gzip.body` versus `02-enc-gzipdeflatebrzstd.body` |
| 13 | `/mcp/v1` and `/api/v1` serialise the same problem+json struct in different key orders, indicating two implementations behind "the MCP server is 1:1 with the REST API" | `docs/docs_v1_versioning.md` MCP parity section versus `probe-limits/65-prod-mcp.body` |

---

## 13. Practical implications for an integrator

1. **Do not size your client against sandbox.** Sandbox tolerates at least 2.5x the documented per-token rate and 68.9 req/s bursts. Build to the documented approximately 60 req/min per token and approximately 600 req/min per IP, and treat sandbox as a correctness environment only, never a capacity environment.
2. **You cannot test your backoff code.** There is no way to elicit a `429` or a `Retry-After` from Rho. Retry logic must be written blind and unit-tested against synthetic responses. Handle a missing `Retry-After` on a `429` as well, since nothing guarantees it is emitted.
3. **Always send `Accept-Encoding: gzip` explicitly.** Not `*`, not brotli, not zstd. It is a 6.8x to 7.2x wire-bytes saving on list endpoints.
4. **Reuse connections, but do not over-multiplex one of them.** Keep-alive halves latency (206 ms to 112 ms p50). Multiplexing 50 streams onto a single connection made p50 13x worse. Prefer a small pool of connections with modest per-connection concurrency.
5. **Budget approximately 90 to 145 ms of server time per call**, plus 70 to 100 ms of connect and handshake if the connection is cold, from a US East client. Payload size is not a latency driver. Allow for a rare approximately 1 s tail.
6. **Log `cf-ray` on every request.** It is the only identifier Rho's support can correlate against, since no request id is returned.
7. **Handle `429` even though the OpenAPI document does not declare it.** Generated clients will not have the case. Add it by hand.
8. **Poll cost is unavoidable.** No `ETag`, no `304`, no `Last-Modified`, no webhooks anywhere in the corpus. Change detection means full page pulls plus client-side diffing, so choose your polling interval against real byte cost.
9. **Keep URIs under 8 KB.** The nginx ceiling sits between 8 KB and 16 KB and returns an HTML `414` that is not problem+json, so your error parser must tolerate non-JSON error bodies at `411`, `414`, `403` and `405`.
10. **Never call the API from browser JavaScript.** There is no CORS. Proxy through your own backend.
11. **Certificate pinning, if used, must target ECDSA and the GTS WE1 chain, and be renewed often.** The leaf is a 90-day certificate.
12. **For MCP, target production only.** `https://rhoapi.rho.co/mcp/v1` exists; the sandbox equivalent does not.

---

## 14. Method note and probe hygiene

- All bursts were bounded. The largest single burst was 65 requests; the four rate-limit bursts totalled 275 requests, and the whole session issued approximately 430 requests to the sandbox over 10.5 minutes.
- No burst was repeated after a `429`, because no `429` ever occurred.
- No write operations were attempted beyond method-probing `POST`/`PUT`/`PATCH`/`DELETE` against a read-only endpoint, all of which were rejected with `405` or `411` before reaching any state.
- Production received exactly three requests, all unauthenticated, solely to compare error shape and confirm the `/mcp/v1` route exists. No rate-limit probing was performed against production.
- The approximately 600 req/min per-source-IP limit remains untested by design.

## 15. Evidence layout

```
scratchpad/rho/sandbox/probe-limits/
  README.md                       index of every artefact
  01-baseline.{body,headers,verbose}   full TLS + h2 trace
  02-enc-*.{body,headers,gz,dec}       7 Accept-Encoding variants + decoded bodies
  03-inm-star,04-inm-fake,05-ims-future,06-ims-past   conditional requests
  07-head,08-options,09-preflight,10-get-origin       HEAD/OPTIONS/CORS
  11-method-{POST,PUT,PATCH,DELETE,TRACE,FOO}         method matrix
  12-404,13-root,14-post-cl0,15-post-json
  20-latency-coldconn.tsv              run A raw timings (10 columns incl. cf-ray)
  21-latency-keepalive.tsv             run B raw timings
  30-burst1-seq60.txt + burst1/        run C, 60 request/response header captures
  31-burst2-par60.txt + burst2/        run D, per-request start/end epochs
  32-burst3-heavy30.txt + burst3/      run G
  33-burst4-par60conc60.txt + burst4/  run E
  34-h2-multiplex50.txt                run F
  35-burst5-uniqtoken65.txt            run H, token recorded in 35-burst5-token.txt
  40-http11,41-tls12,42-openssl.txt,cert_1..3.pem
  50-prod-noauth,51-prod-badtok,52-sb-emptybearer
  60-longurl,61-longurl16k,62-bighdr,63-unknownparam
  64-mcp_*,65-prod-mcp
  70-h2-settings.txt,71-http80,72-ipv4,73-ipv6
  80-{404-unknown-id,400-bad-id,400-pagesize,400-sortby}.{body,headers}
```
