# Rho Desk

**Every name on your ledger is a relationship nobody is managing.**

Rho Desk reads a company's Rho account, works out who each counterparty
actually is, researches them on the open web, and then picks up the phone.

A bank account shows you transactions. This shows you who you are in business
with, and does something about it.

---

## 1. What it is

One pipeline over your ledger. One row per counterparty, not per transaction.

| Posture | Trigger | Action |
| --- | --- | --- |
| **Collect** | They owe you, and they look healthy | Call and agree a payment date |
| **Cover** | They owe you, and verified distress turned up | Escalate before the other creditors do |
| **Cut** | You pay them repeatedly, and it is duplicated or the price moved | Call to renegotiate or cancel |

---

## 2. The problem

**43%** of US B2B invoice value runs overdue. **5%** is never collected.

A dollar is **68.9%** collectable at three months past due. At one year it is
**21.4%**.

US companies pay agencies **$13.6 billion a year** to make those calls, and
the commission rises as the dollar shrinks.

Meanwhile **36%** of SaaS licenses go unused, and **81%** of software is
bought outside IT, so one vendor lands on three cards under three names and
nobody sees them side by side.

Nobody is watching either side of the ledger. That is the whole problem.

*(Figures, scope and sources: [Appendix](#appendix-the-numbers).)*

---

## 3. The solution

Rho Desk reads your ledger, works out who each name actually is, checks what
the open web says about them, and calls them.

```
  what the bank shows you          what Rho Desk shows you
  ───────────────────────          ───────────────────────
  ASANA.COM      $49               Asana, Inc.        Cut      on 2 cards
  SQ *ASANA      $49        ──►    Northwind Traders  Cover    94 days, down round
  ASANA INC      $49               Summit Analytics   Collect  $28,400, call today
  NORTHWIND      $59,200
```

**It calls early.** The queue ranks by `outstanding x recoverability`, not by
size, because a dollar at three months is worth three at a year.

**It cites its sources.** Every posture resting on outside information carries
a URL. Unverified signals cannot escalate anything.

**It acts in the world, not in the ledger.** Rho's v1 API is read only, so the
only lever is a conversation with a human. That turns out to be the right
lever anyway.

## 4. Why this extends Rho

**Rho already issues the invoice. Rho does not collect it.**

That gap is a $13.6bn industry, served today by third parties. The data to
close it is already in the account.

| Rho already has | Rho Desk turns it into |
| --- | --- |
| Invoicing and customers | A ranked collections queue that works itself |
| Card and transaction history | Duplicate subscriptions and price rises, found |
| Counterparty names | A monitored relationship with a risk posture |
| Accounts and balances | Concentration risk, visible before it bites |

Three ways it compounds:

- **Action, not record.** Other spend tools report. This one does the thing
  the report implies.
- **The natural home for write access.** When Rho's writes land, the desk
  stops agreeing payment dates and starts settling them. The conversational
  layer is the hard part, and it is built.
- **Not Rho specific.** Rho is the first connector, not the product.

---

## 5. The stack

| Tool | Role | Why this one |
| --- | --- | --- |
| **Rho** | The ledger | Accounts, cards, transactions, invoices, customers. The public sandbox needs no account |
| **Tavily** | Research | Search plus full page extract, built for agents, returns citations |
| **Groq** | Inference | Entity resolution across 32 ledger names in about a second |
| **ElevenLabs** | The voice agent | The only genuinely agentic part of the system. Browser and phone from one agent |
| **Telnyx** | Telephony | SIP trunk to PSTN. Usage priced, no per channel fee |
| **FastAPI + SQLite** | The desk | One process, one file, no infrastructure |

Anthropic and OpenAI are drop in alternatives to Groq via `LLM_PROVIDER`.
Twilio and Exotel are drop in alternatives to Telnyx via `ELEVENLABS_TELEPHONY`.

---

## 6. How each tool is used

### Rho

Fourteen read only GET operations across five resources. The client pages
every endpoint to exhaustion, retries 429s and 5xx, and strips empty params
because the sandbox silently ignores unknown ones.

Every write returns `405 Method Not Allowed`. That single fact shapes the
entire product: the desk cannot settle an invoice, so it calls the person who
can.

`RHO_MODE=fixtures` swaps in a generated 18 month ledger (273 transactions, 10
vendors, 10 customers) that is a field for field drop in replacement. The
sandbox has only 72 transactions, too few for subscription detection to fire.

### Tavily

Two or three searches per counterparty, plus a full page extract on vendor
pricing pages. Results feed one LLM call that turns them into signals with
severity and a source URL.

Tavily is the difference between "they owe you $59,200" and "they owe you
$59,200 and they raised a down round four days ago."

### Groq

Two jobs, both classification, both at `temperature=0` because the desk
compares one run against the next and sampling noise would show up as business
change.

1. **Entity resolution.** 32 ledger descriptors to 28 real companies, batched
   into one call, about one second.
2. **Signal extraction.** Search results to structured findings with severity.

Everything else is arithmetic and rules. Deliberately.

### ElevenLabs

The agent, Rhonica, receives 15 dynamic variables per call: the amount and
invoice in spoken form, what it may agree to, what it must not, and the
research context.

Spoken forms are computed in Python, not left to the model. `$59,200.00`
becomes "fifty nine thousand two hundred dollars". Invoice references are one
letter and three digits, so `R204` becomes "R two zero four": no year, and no
dash for the voice to read out.

`get_invoice_details` is registered as a **client** tool, so it runs in the
page and needs no public URL. It also means `counterparty_id` comes from the
session rather than from the model, which is what stops the agent looking up
somebody else's invoice.

### Telnyx

A SIP trunk from ElevenLabs straight to the phone network. FQDN connection,
TCP transport, digest auth, no media encryption.

No part of this system is in the audio path, which is the point: no tunnel,
no public URL, nothing between ElevenLabs and the phone network. Transcripts
come back by polling the ElevenLabs conversation API rather than by webhook,
so the desk stays reachable only from inside your own network.

---

## 7. Architecture

```
  Rho API (or fixtures)
          │  accounts · transactions · cards · invoices · customers
          ▼
  ┌───────────────┐
  │ 1. EXTRACT    │  pure code
  │               │  group by counterparty, compute money in/out, open
  │               │  invoices, days overdue, recurrence, duplicates
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 2. RESOLVE    │  1 LLM call, batched
  │               │  "AWS EMEA" + "AMZN AWS" → Amazon.com, Inc. (+domain)
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 3. MONITOR    │  Tavily + 1 LLM call each · 8-way thread pool
  │               │  news, distress, pricing → signals with citations
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 4. CLASSIFY   │  rules only, deterministic
  │               │  → Collect | Cover | Cut | Watch
  └───────┬───────┘
          ▼
  ┌───────────────┐
  │ 5. CAPTURE    │  pure code
  │               │  snapshot every counterparty against this run id,
  │               │  diff against the previous run, store what moved
  └───────┬───────┘
          ▼
      SQLite  ──────────────►  Web UI (7 screens)
          │                         │
          │                         ▼
          │                 ┌───────────────┐
          └────────────────►│ 6. ACT        │
            brief + guard   │ ElevenLabs    │──► browser (WebRTC)
            rails + dossier │ agent Rhonica │──► phone (Telnyx SIP → PSTN)
                            └───────┬───────┘
                                    │ get_invoice_details (client tool)
                                    ▼
                            back to SQLite: transcript + extracted outcome
```

### Data flow, stage by stage

| Stage | In | Out | Cost |
| --- | --- | --- | --- |
| Extract | ~273 transactions, 17 invoices | 32 ledger groups | free, ~1s |
| Resolve | 32 groups | 28 companies with domains | 1 LLM call, ~1s |
| Monitor | 28 companies | ~90 signals with citations | ~70 Tavily + 28 LLM, ~20s |
| Classify | companies + signals | 4 postures | free, instant |
| Capture | companies | 1 snapshot row each, plus a diff | free, instant |
| Act | 1 counterparty + brief | a phone call and a transcript | ~$0.005/min |

The monitor stage is entirely network bound, so it runs in an 8 way pool.
Sequentially it took 279 seconds; concurrently it takes 21, with byte
identical output. **13.5x**, and the ordering is preserved because results are
collected into a dict and applied in the original order.

### Modules

| File | Lines | Does |
| --- | --- | --- |
| `pipeline.py` | 863 | extract → resolve → monitor → classify → brief |
| `api.py` | 617 | FastAPI routes, webhooks, the agent's tool endpoint |
| `voice.py` | 564 | ElevenLabs sessions, spoken forms, simulation, reconciliation |
| `history.py` | 460 | Run records, per run snapshots, the diff |
| `fixtures.py` | 378 | Generated 18 month ledger, drop in for the API client |
| `db.py` | 322 | SQLite schema, migrations, JSON columns |
| `today.py` | 239 | The morning briefing, derived from everything above |
| `llm.py` | 173 | Anthropic / OpenAI / Groq, JSON mode, rate limit retries |
| `tavily.py` | 165 | Search and extract, with a deterministic offline mode |
| `rho.py` | 126 | Rho API client: pagination, retries, sandbox quirks |
| `settings.py` | 100 | Persisted settings that actually gate the agent |
| `tests/` | 605 | 47 tests, mostly on the diff and the spoken forms |

**Deliberately not an agent loop.** Extraction and classification are
arithmetic and rules, so the output is reproducible. Only two steps get a
model. The one genuinely agentic thing in the system is the voice agent on the
phone, and ElevenLabs runs that.

---

## 8. Running it

```bash
./run.sh
```

Then open http://localhost:3000 and press **Run desk**.

**Every external dependency degrades rather than fails.** With no API keys
configured the pipeline still completes end to end: generated ledger, offline
search, rule based classification, scripted calls. Each key upgrades one stage
independently, and the sidebar always shows which services are live, so the
output is never ambiguous about what produced it.

```bash
RHO_MODE=fixtures | live          # generated ledger, or the Rho API
TAVILY_API_KEY=                   # real research
LLM_PROVIDER=groq|anthropic|openai
ELEVENLABS_API_KEY=               # browser voice
ELEVENLABS_AGENT_ID=
ELEVENLABS_PHONE_NUMBER_ID=       # phone calls
ELEVENLABS_TELEPHONY=sip_trunk    # twilio | exotel | sip_trunk
DEMO_OVERRIDE_NUMBER=             # safety: pin all outbound calls to one number
MONITOR_CONCURRENCY=8
FIXTURE_DAYS_AGO=0                # read the ledger as it stood N days ago
```

**`DEMO_OVERRIDE_NUMBER` is a safety control.** Set it and every outbound
call goes to that number regardless of which counterparty is selected, which
makes it impossible for the agent to reach a real counterparty. Leave it set
until you have deliberately decided the agent should call real people.

---

## 9. Screens

| Screen | Does |
| --- | --- |
| **Today** | The morning briefing. What needs a person, what the desk handled, what it will work next |
| **Counterparties** | One row per relationship. Click through to the dossier |
| **What changed** | Every movement since the previous run, weighted and grouped |
| **Collect queue** | Who to call and in what order, by expected recovery |
| **Signals** | What changed about the companies you deal with |
| **Calls** | Every call with its outcome. Click for the transcript |
| **Agent settings** | Identity, limits, guardrails, do-not-call list |

---

## 10. Design decisions worth knowing

### History: what counts as news

Every run is recorded, snapshotted per counterparty, and diffed against the
previous run. The diff is computed once and stored, so "what changed last
Tuesday" stays answerable.

Two rules shape it:

**Counterparties appear and disappear, but rarely do.** The resolver regroups
far more often than companies actually leave, so a counterparty folded into
another is reported as a **merge**, not a departure.

**Signals only ever appear.** News does not un-happen, and a live search
returns a slightly different set every time, so reporting "signal disappeared"
would be reporting search noise.

Counterparty ids come from the **ledger keys**, not from the resolved name.
The model is allowed to change its mind between runs; the transaction
descriptors are not.

### Degraded runs

A run that could not resolve entities, or could not research anybody, still
completes. What it must not do is present the resulting absence as news.

A rate limited resolver once made every counterparty look new. An exhausted
Tavily key once made every risk read "high to none", which the briefing would
have shown as good news.

So a run records **which stage** degraded, and the diff suppresses whatever
that stage feeds:

| Degraded stage | Suppressed |
| --- | --- |
| `resolve` | appeared, disappeared, merged |
| `research` | signal, risk, posture |

Ledger arithmetic survives both, because it does not depend on the outside
world. The comparison says plainly that it was degraded rather than quietly
showing less.

### Settings are not decoration

The approval threshold gates dialling (`POST /api/calls` returns **412**
without an approver). The do-not-call list is refused at the API with **403**
rather than hidden in the UI. The payment window, instalment limit, AI
disclosure and company name all flow into the brief the agent receives.

### Reading the ledger at an earlier moment

`FIXTURE_DAYS_AGO` rewinds the generated ledger: transactions that had not
posted yet are removed, invoices paid since are put back to unpaid. Same
ledger, earlier moment, nothing invented.

It exists for the history layer, which needs two runs that genuinely differ
before the diff has anything to say, and for testing that the diff reports the
right things when they do.

```bash
python seed_history.py 7     # runs the desk as of 7 days ago, then as of today
```

Against a live Rho account this is unnecessary: the ledger moves on its own.

---

## 11. API

| Route | Does |
| --- | --- |
| `POST /api/run` | Run the pipeline. `GET /api/run` polls progress |
| `GET /api/today` | The morning briefing. Reconciles unclosed calls first |
| `GET /api/changes` | What moved between a run and the one before it |
| `GET /api/runs` | Run history with counts and degradation flags |
| `GET /api/counterparties` | The table. `?posture=collect\|cut\|cover\|watch` |
| `GET /api/counterparties/{id}` | Dossier: signals, invoices, calls |
| `GET /api/counterparties/{id}/timeline` | Every snapshot of one counterparty |
| `POST /api/counterparties/{id}/brief` | Write the call brief |
| `POST /api/calls` | Place a call. 412 above the approval threshold, 403 on do-not-call |
| `GET /api/calls/{id}` | Poll a call. Drives the live transcript |
| `POST /api/tools/invoice` | The agent's tool endpoint, scoped by counterparty |
| `POST /api/webhooks/elevenlabs` | Post-call webhook |
| `GET /api/queue` | The collect queue, ranked by expected recovery |
| `GET /api/settings` · `PUT /api/settings` | Read and write desk settings |
| `GET /api/status` | What is live, what is degraded, what last failed |

---

## 12. What is missing

Honest list, kept current in [PRD.md](PRD.md).

- **Cover does not fire on generated data.** Generated customers are
  fictional, so they have no verifiable distress, and unverified signals
  deliberately cannot escalate. The posture needs a real customer book to
  exercise it.
- **Contact data is missing.** 0 of 28 counterparties carry a phone number,
  so the product's headline action has no input until contact enrichment is
  built.

- Nothing is written back to a counterparty after a call. A commitment to pay
  Thursday changes nothing about Thursday.
- No auth. Anyone who can reach the port can read the ledger.
- Single business per token. Multi-entity is not modelled.
- Tests cover the diff and the spoken forms. Nothing covers `extract` or
  `classify`, which carry the arithmetic.

---

## Appendix: the numbers

Everything quoted at the top, with scope and source. All figures are US
specific. No global, regional or non US data is used anywhere in this document.

### Receivables

Of the total value of B2B invoices issued by US companies:

| | Share of invoice value |
| --- | --- |
| Paid on time | 52% |
| Overdue | **43%** |
| Written off as bad debt | **5%** |

In electronics and ICT, terms average **50 days** from invoicing, **44%** of
invoices run overdue and **6%** is written off.

Source: [Atradius Payment Practices Barometer, US 2025](https://atradius.us/dam/jcr:5609b617-ac29-4e30-8b01-0663a01d94bd/payment-practices-barometer-us-2025-en.pdf). US only,
surveyed end Q2 to mid Q3 2025.

### Why calling early is the whole game

Probability of ever collecting a commercial dollar, by age past due:

| Age past due | Probability of collection |
| --- | --- |
| 3 months | **68.9%** |
| 6 months | **51.3%** |
| 1 year | **21.4%** |
| 2 years | **8.9%** |

Source: Commercial Collection Agencies of America, *Impact of Bad Debt
Write-Off on Sales*, cited in [AFM](https://www.afmcollects.com/insights/defining-high-performance-in-commercial-collections). US commercial (B2B).

A dollar loses roughly a third of its value in the first quarter and half by
six months. There is no cliff, just a steady bleed from the day it goes past
due. The economics run against the people doing the work: the cheapest moment
to call is the earliest, which is exactly when nobody has time, because
nothing is on fire yet.

### The outsourced alternative

US debt collection agencies are a **$13.6 billion industry** (2025). Agency
commission is lowest on accounts 90 to 270 days past due and highest past 360
days, so the fee rises exactly as the recoverable amount falls.

Source: [IBISWorld, Debt Collection Agencies in the US](https://www.ibisworld.com/united-states/industry/debt-collection-agencies/1474/).

### Software spend

| Finding | Figure |
| --- | --- |
| SaaS licenses left unused | **36%** |
| SaaS spend controlled by business units, not IT | **81%** (IT manages 15%) |
| Growth in expense-based SaaS spend, year over year | **267%** |

Source: [Zylo 2026 SaaS Management Index](https://zylo.com/news/2026-saas-management-index), built on 40 million SaaS
licenses and $75 billion in spend across 218 IT leaders.

The second row is the mechanism. When most software is bought by whoever
needed it that week, and expensed rather than procured, the same vendor ends
up on several cards under several descriptors. The card statement has the
evidence. It just reads as `ASANA.COM`, `SQ *ASANA` and `ASANA INC` on three
separate lines.

### A note on what is not here

Contingency fee percentages for US commercial collections are widely quoted
online at 25% to 35%, but every instance traced back to secondary content
rather than a primary source, and IBISWorld keeps its rate data behind a
paywall. The figure is therefore left out rather than cited weakly.

---

Independent project. Not affiliated with or endorsed by Rho.
