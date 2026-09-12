# Rho Desk

**Every name on your ledger is a relationship nobody is managing.**

Rho Desk reads a company's Rho account, works out who each counterparty
actually is, researches them on the open web, and then calls them.

Status: working prototype. Built 2026-09-11 to 09-12.

---

## 1. Problem

A finance team's bank account lists transactions. It does not list
*relationships*. So the work that money implies falls through:

- **Money owed to you sits uncollected.** Nobody chases until it is 90 days old,
  and by then the customer may be in trouble.
- **Money leaks out on autopilot.** Duplicate subscriptions, price rises nobody
  noticed, tools nobody uses.
- **Nobody watches the counterparties.** Your biggest customer can have a down
  round and you find out when the invoice goes unpaid.

Each of these is a known job. None of them is anybody's job, because doing them
means cross-referencing a ledger against the outside world, one name at a time,
every day.

## 2. Solution

Turn every name in the ledger into a monitored relationship with a posture and
an action. One pipeline, three outcomes:

| Posture | Trigger | Action |
| --- | --- | --- |
| **Collect** | They owe you, and they look healthy | Call and agree a payment date |
| **Cover** | They owe you, and verified distress turned up | Escalate before the other creditors do |
| **Cut** | You pay them repeatedly, and it is duplicated or the price moved | Call to renegotiate or cancel |

The product surface is **one row per counterparty, not per transaction**. That
inversion is the whole idea. A bank shows you a transaction list; this shows you
who you are in business with.

The agent then acts **in the world** (a phone call), not in the ledger. That is
by design, not a workaround: Rho's v1 API is read-only.

## 3. Architecture

```
  Rho API (or fixtures)
          │  accounts · transactions · cards · invoices · customers
          ▼
  ┌───────────────┐
  │ 1. EXTRACT    │  pure code
  │               │  group by counterparty_name, compute money in/out,
  │               │  open invoices, days overdue, recurrence, duplicates
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 2. RESOLVE    │  1 LLM call (batched)
  │               │  "AWS EMEA" + "AMZN AWS" + "AMAZON WEB SVCS"
  │               │    → Amazon.com, Inc.  (+ domain, sector)
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 3. MONITOR    │  Tavily + 1 LLM call each · 8-way thread pool
  │               │  news, distress, pricing pages → signals with citations
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 4. CLASSIFY   │  rules only, deliberately deterministic
  │               │  → Collect | Cover | Cut | Watch
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 5. CAPTURE    │  pure code
  │               │  snapshot every counterparty against this run id,
  │               │  diff against the previous run, store what moved
  └───────┬───────┘
          ▼
      SQLite  ──────────────►  Web UI (6 screens)
          │                         │
          │                         ▼
          │                 ┌───────────────┐
          └────────────────►│ 6. ACT        │
            brief + guard   │ ElevenLabs    │──► browser voice (WebRTC)
            rails + dossier │ agent "Ellis" │──► phone (needs a number)
                            └───────┬───────┘
                                    │ get_invoice_details (client tool)
                                    ▼
                            back to SQLite: transcript + extracted outcome
```

**Deliberately not an agent loop.** Extraction and classification are arithmetic
and rules, so the demo is deterministic. Only two steps get a model: resolving a
messy ledger string to a real company, and writing the call script. The one
genuinely agentic thing in the system is the voice agent on the phone, and
ElevenLabs runs that.

### Modules

| File | Does |
| --- | --- |
| `rho.py` | Rho API client: pagination, retries, the sandbox quirks |
| `fixtures.py` | Generated 18-month ledger, drop-in for the API client |
| `pipeline.py` | extract → resolve → monitor → classify → build_brief |
| `tavily.py` | Search and extract, with stubs |
| `llm.py` | Anthropic / OpenAI / Groq, JSON mode, records failures |
| `voice.py` | ElevenLabs sessions, spoken number forms, call simulation |
| `history.py` | Run records, per-run snapshots, the run-over-run diff |
| `settings.py` | Persisted settings that actually gate the agent |
| `api.py` | FastAPI routes, webhooks, the agent's tool endpoint |
| `static/` | The UI, in Rho's real brand tokens |
| `tests/` | 29 tests, all on the diff, which is the logic with no model in it |

## 4. Integrations

| Integration | Status | Notes |
| --- | --- | --- |
| **Rho API** | Working | Public sandbox, no account needed. 14 read-only GET operations across 5 resources. Every write returns 405 |
| **Rho fixtures** | Working | 18 months, ~270 transactions, 10 vendors, 10 customers. Seeded, dates anchored to today. `RHO_MODE=fixtures` |
| **Tavily** | Working, key exhausted | Search plus extract. Real citations from Reuters, CRN, PR Newswire. The hackathon key now answers 432, so live runs fall back to stubs until it is topped up |
| **Groq** | Working | `openai/gpt-oss-120b`. Entity resolution in ~1s |
| **Anthropic / OpenAI** | Working | Same interface, swap with `LLM_PROVIDER` |
| **ElevenLabs voice** | Working | Browser WebRTC. Signed URL, 15 dynamic variables, live-streamed transcript |
| **ElevenLabs tool** | Working | `get_invoice_details` as a **client** tool, so no public URL is needed |
| **ElevenLabs phone** | Built, untested | Outbound via Twilio, Exotel or a SIP trunk, set with `ELEVENLABS_TELEPHONY`. All three take the same request, so the carrier is a URL segment. Exotel for Indian numbers. Needs a number |
| **Post-call webhook** | Built, untested | Never received a real webhook |

### Why the tool is a client tool

A server tool would need this app reachable from the public internet (ngrok, a
tunnel, a deploy). A client tool runs in the page, so it calls localhost. It
also means `counterparty_id` comes from the session the page opened rather than
from the model, which is what stops the agent looking up someone else's invoice.

## 5. What works today

- Full pipeline, live, in **~10 to 20 seconds** for 28 counterparties.
  Sequentially it was 279s; the 8-way pool made it 13.5x faster with identical
  output.
- Entity resolution merges 9 alias groups including AWS and Datadog.
- Collect queue ranked by **expected recovery** (`outstanding × recoverability`),
  not raw size, so a healthy $450 customer outranks a distressed $1,682 one.
- Settings that gate real behaviour: approval threshold (API returns 412),
  do-not-call list (403), payment window, instalment cap, AI disclosure.
- Voice agent that looks up a live invoice mid-call and reads amounts in spoken
  form ("forty seven thousand two hundred dollars").
- Call log with outcomes extracted from real transcripts by LLM, in the same
  shape as simulated calls and webhooks. One log, three ways of calling.
- 10 simulated call outcomes, chosen deterministically and biased by posture, so
  a demo without keys still looks like real collections work.
- **History.** Every run is recorded and diffed against the last one. What
  changed reads like a briefing: who crossed 90 days, who paid off, who
  escalated, what news arrived. `python seed_history.py 7` gives two runs a
  week apart to compare.
- **Honest degradation.** A run that could not resolve entities or could not
  research anybody says so, and the diff suppresses whatever that stage feeds
  rather than presenting our own outage as the customer's news.
- 6 screens: Counterparties, What changed, Collect queue, Signals, Calls,
  Agent settings.
- 13-artboard design canvas in Rho's real brand system.

## 6. What is missing

**Blocks a richer demo**

- **Cover is empty on live data.** Fixture customers are fictional, so they have
  no verifiable distress, and unverified signals deliberately cannot escalate
  (a "Cedar & Co" once matched a fraud conviction at an unrelated company). Real
  customer data fixes this; stub mode fakes it.
- **Real Rho environment** (simulated business + OpenVPN) not yet provisioned.
- **Phone calls** need a number and a public URL for the webhook.

**Known gaps**

- No auth. Anyone who can reach the port can read the ledger.
- Single business per token. Multi-entity is not modelled.
- Post-call webhook never exercised.
- Two screens exist in the canvas but not the app: Today (morning briefing) and
  the first-run Connect flow. Today is now unblocked: the diff it needs exists.
- Tests cover the diff only. Nothing covers `extract`, `classify` or the API.
- Nothing is ever written back to a counterparty after a call. A promise to
  pay is captured in the transcript and then nothing watches for it.
- 0 of 28 counterparties have a phone number on live data.

## 7. What to build next

Ordered by value per hour.

1. **Today screen.** The morning briefing: what happened overnight, what needs
   a human. Designed in the canvas, and now buildable, because the diff it
   reads already exists. What changed is the raw feed; Today is the edit of it.
2. **Outbound phone.** Number, webhook URL, voicemail detection. Turns a demo
   into a product. Carrier is already switchable; what is missing is an
   account with a number on it. Exotel needs its Voicebot applet enabled,
   which their support does in 1 to 2 business days.
3. **Auth.** Any real deployment needs it before it touches a real ledger.
4. **Email fallback.** A third of counterparties have no phone number. Drafting
   the chase email is the same brief with a different channel.
5. **Scheduled runs.** The desk should run at 06:00 without being asked.
6. **Close the loop after a call.** A commitment extracted from a transcript
   should become something the next run watches for, and the call should leave
   a mark on the counterparty rather than only on the call log.
7. **Tests** on `extract` and `classify`, which carry the rest of the
   arithmetic.

## 8. Ideas to discuss

- **Write access.** Rho says it is next. When it lands, the desk stops being a
  reporting layer and can settle, schedule and reconcile.
- **Vendor-side leverage.** We only detect duplicates and price moves. Renewal
  dates, seat utilisation and auto-renew traps are bigger money.
- **The counterparty graph.** Shared investors, shared customers, common
  exposure. Concentration risk is currently one number.
- **Inbound.** Ellis answers rather than calls, and handles "when will you pay
  us" from your vendors.
- **Confidence, shown.** Every posture rests on a heuristic. Making the
  reasoning visible and correctable is the difference between a tool people
  trust and one they second-guess.
- **Learning from outcomes.** Recoverability is a hand-written formula. Real
  call outcomes are training data for it.
- **Who else has this problem.** Same pipeline works on any ledger. Rho is the
  first connector, not the product.

## 9. Running it

```bash
./run.sh            # http://localhost:3000
```

Works with no keys at all: fixtures ledger, stubbed search, rule-based
classification, simulated calls. Each key added upgrades one stage
independently, and the sidebar always shows which are live.

```bash
RHO_MODE=fixtures | live          # generated ledger, or the Rho API
TAVILY_API_KEY=                   # real research
LLM_PROVIDER=groq|anthropic|openai
ELEVENLABS_API_KEY=               # browser voice
ELEVENLABS_AGENT_ID=
MONITOR_CONCURRENCY=8             # research pool size
```

See `README.md` for setup detail and the ElevenLabs agent configuration.
