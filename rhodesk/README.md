# Rho Desk

Every name on your ledger is a relationship nobody is managing. Rho Desk reads
your Rho account, works out who each counterparty actually is, researches them,
and then calls them.

Three postures fall out of one pipeline:

| Posture | Trigger | Action |
| --- | --- | --- |
| **Collect** | They owe you, and they look healthy | Call and agree a payment date |
| **Cover** | They owe you, and something bad turned up | Escalate before the other creditors do |
| **Cut** | You pay them repeatedly, and it is duplicated or overpriced | Call to renegotiate or cancel |

## Run it

```bash
./run.sh
```

Then open http://127.0.0.1:8787 and press **Run desk**.

That works with no API keys at all. The Rho sandbox needs no account, and every
other service falls back to a deterministic stub so the whole pipeline
completes. The sidebar always shows which services are live and which are
stubbed, so you never have to guess what you are looking at.

## What is real, and what is not

**Real, today, with no setup:** the Rho client. It reads the live sandbox at
`rhoapi-sandbox.rho.co`, pages every endpoint to exhaustion, and the invoice
numbers, amounts and overdue days you see in the UI come straight out of it.

**Stubbed until you add a key:**

| Service | Env var | Without it |
| --- | --- | --- |
| Tavily | `TAVILY_API_KEY` | Search and extract return fixed results |
| LLM | `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` | Entity resolution and call briefs fall back to rules |
| ElevenLabs | `ELEVENLABS_API_KEY`, `ELEVENLABS_AGENT_ID` | Calls run as a scripted simulation |

Copy `.env.example` to `.env` and fill in what you have. Nothing breaks if you
leave a key blank.

**Two request shapes need checking before you demo.** The Tavily and ElevenLabs
clients follow those vendors' documented REST APIs, but they were written
without keys to test against. Verify `tavily.py::_post` and
`voice.py::start_call` against current docs before you rely on them.

## Architecture

```
Rho sandbox ──► extract ──► resolve ──► monitor ──► classify ──► SQLite ──► UI
                (code)      (1 LLM)    (Tavily)    (rules)                   │
                                                                             ▼
                                                          ElevenLabs agent ──► phone
                                                                 │
                                            post-call webhook ◄──┘
```

Deliberately **not** an agent loop. Extraction and classification are
arithmetic and rules, which keeps the demo deterministic. Only two steps get a
model: resolving a messy ledger string to a real company, and writing the call
script. The one genuinely agentic thing in the system is the voice agent on the
phone, and ElevenLabs runs that.

| File | Does |
| --- | --- |
| `rhodesk/rho.py` | Rho API client, pagination, retries, the sandbox quirks |
| `rhodesk/pipeline.py` | extract, resolve, monitor, classify, build_brief |
| `rhodesk/tavily.py` | Search and extract, with stubs |
| `rhodesk/llm.py` | Anthropic or OpenAI, JSON mode, falls back to a caller-supplied default |
| `rhodesk/voice.py` | ElevenLabs outbound calls, plus the simulation |
| `rhodesk/settings.py` | Persisted desk settings that actually drive the agent |
| `rhodesk/api.py` | FastAPI routes and the webhook |
| `rhodesk/static/` | The UI, in Rho's brand tokens |

## Browser voice, the one a judge can use

The briefing screen has two buttons. **Simulate call** runs the scripted
version. **Talk to the agent** opens a real WebRTC conversation in the
browser: you speak into the laptop, the agent answers in an ElevenLabs voice,
and the transcript streams into the call log as it happens.

Setup is two environment variables and nothing else:

```bash
ELEVENLABS_API_KEY=...
ELEVENLABS_AGENT_ID=...
```

No phone number, no Twilio, no ngrok, no public URL. Without the keys the
button explains what is missing and offers the simulation instead.

How it fits together: `POST /api/voice/session` builds the brief, enforces the
approval threshold and the do-not-call list, opens a call record, and returns
the dossier as dynamic variables plus a short-lived signed URL so the browser
never sees your API key. The page streams turns to
`POST /api/calls/{id}/transcript`, and on hang-up
`POST /api/calls/{id}/finish` runs the transcript through the LLM to extract
what was agreed, in the same outcome shape the simulation and the post-call
webhook produce. One log, three ways of calling.

VERIFY BEFORE THE DEMO: the signed-URL endpoint and the `Conversation.startSession`
options follow the documented Agents SDK but were written without a key to
test against.

## Wiring up ElevenLabs for real phone calls

1. Create an agent in the ElevenLabs dashboard.
2. In its system prompt, reference the dynamic variables this app sends:
   `{{company}}`, `{{counterparty}}`, `{{contact_name}}`, `{{amount}}`,
   `{{oldest_days}}`, `{{invoice_number}}`, `{{opening_line}}`,
   `{{may_agree}}`, `{{must_not}}`, `{{context}}`.
3. Add a server tool called `get_invoice_details` pointing at
   `POST {your public url}/api/tools/invoice`, taking `invoice_number`. That is
   what lets the agent look something up mid-conversation, which is the best
   moment in the demo.
4. Set the post-call webhook to `POST {your public url}/api/webhooks/elevenlabs`.
5. Attach a phone number, put its id in `ELEVENLABS_PHONE_NUMBER_ID`, and use
   `ngrok http 8787` to give ElevenLabs a public URL for steps 3 and 4.

**Set `DEMO_OVERRIDE_NUMBER` to your own mobile before any live demo.** It
forces every call to dial you rather than whatever number is on the record.

## Simulated call outcomes

Without ElevenLabs keys a call runs a scripted simulation. There are ten
outcomes, not one: full commitment, instalments, dispute, deferred to a
decision maker, refusal, voicemail, and four vendor-side endings (agreed,
cancelled, retention offer, escalated to an account manager).

Which one a counterparty gets is chosen deterministically from its id and
biased by posture and research, so a distressed customer rarely pays in full
on the first call and one that just raised usually does. The same counterparty
always behaves the same way, so demos are reproducible while the log still
looks like real collections work.

A voicemail does not count as answered, and a dispute does not count toward
value secured.

## Fixtures mode

```bash
RHO_MODE=fixtures   # generated ledger, no network
RHO_MODE=live       # call RHO_BASE_URL (default)
```

`rhodesk/fixtures.py` generates eighteen months of activity for a Series B
company: ten recurring vendors billed under rotating aliases, one genuinely
duplicated subscription, irregular spend, and ten customers with receivables
spread across the age bands. Roughly 270 transactions against the public
sandbox's 72.

Two properties matter. It is seeded, so the same run gives the same ledger and
your demo does not shift under you. And dates are computed backwards from
today, so overdue counts stay correct however long the repo sits.

Shapes match the live API field for field, so `FixtureClient` is a drop-in and
nothing downstream knows the difference.

### Reading the ledger at an earlier moment

`FIXTURE_DAYS_AGO` rewinds the generated ledger: transactions that had not
posted yet are removed, and invoices paid since are put back to unpaid. It is
the same ledger read at an earlier moment, not a different one, and nothing is
invented.

Its only purpose is the history layer. A diff needs two runs that genuinely
differ before it has anything to say, and waiting a day for one is not a demo.

```bash
python seed_history.py 7     # runs the desk as of 7 days ago, then as of today
```

Against a live Rho account the ledger moves on its own and this is unnecessary.

## History

Every run is recorded, snapshotted per counterparty, and diffed against the
previous run. The diff is computed once when the run finishes and stored, so
"What changed" is a read and "what changed last Tuesday" stays answerable.

Two rules shape it:

**Counterparties can appear and disappear, but rarely do.** The resolver
regroups far more often than companies actually leave, so a counterparty
folded into another is reported as a merge, not a departure.

**Signals only ever appear.** News does not un-happen, and a live search
returns a slightly different set every time, so reporting "signal disappeared"
would be reporting search noise. Signals are append-only; only first sightings
count as new.

### Degraded runs

A run that could not resolve entities, or could not research anybody, still
completes. What it must not do is present the resulting absence as news: a
rate-limited resolver made every counterparty look new, and an exhausted
Tavily key made every risk read "high to none".

So a run records which stage degraded, and the diff suppresses whatever that
stage feeds. A resolver outage suppresses appeared, disappeared and merged; a
research outage suppresses signal, risk and posture. The ledger arithmetic
survives both, because it does not depend on the outside world. The comparison
says plainly that it was degraded rather than quietly showing less.

Use it when the network is the risk (a venue, a flaky VPN) or when you want
the product to look like itself: on fixtures, subscription detection fires on
its own and the three synthetic Cut vendors are unnecessary, so set
`DEMO_VENDORS=false`.

### What the keyless fallback can and cannot merge

Without an LLM key, counterparties are grouped by brand token: the first
substantial word that is not a payment-processor prefix, a TLD, a region or a
generic noun. That collapses `ASANA.COM` with `ASANA INC`, `ATLASSIAN*JIRA`
with `ATLASSIAN PTY`, and `MSFT*GITHUB` with `GITHUB.COM`.

A shared token alone is not enough, though, or `SUMMIT ANALYTICS` (a customer)
would fuse with `SUMMIT LEGAL LLP` (a vendor). The distinguishing tokens must
be compatible: one name's significant tokens must contain the other's.

What it deliberately cannot do is merge `AWS EMEA` with `AMAZON WEB SVCS`, or
`DATADOG INC` with `DDOG*MONITORING`. Those need to know what the company is
actually called. Set an LLM key and the resolve step handles them.

## Two things the sandbox cannot do

**Subscription detection never fires.** The sandbox holds 72 transactions and
its busiest real vendor has two charges, so nothing looks recurring. Three
labelled synthetic vendors fill the Cut posture; they are badged `demo` in the
UI and carry `demo=1` in the database. Turn them off with `DEMO_VENDORS=false`.

**Nothing can be written back.** Every Rho v1 endpoint is a `GET`, and every
write method returns `405 Method Not Allowed`. That is why every action this
system takes happens in the world (a phone call) rather than in the ledger.
It is the design, not a workaround.

## API

| Route | Does |
| --- | --- |
| `POST /api/run` | Run the pipeline. `GET /api/run` polls progress |
| `GET /api/counterparties` | The table. `?posture=collect\|cut\|cover\|watch` |
| `GET /api/counterparties/{id}` | Dossier: signals, invoices, calls |
| `POST /api/counterparties/{id}/brief` | Write the call brief |
| `POST /api/calls` | Place a call. Refuses with 412 above the approval threshold unless `approved_by` is set |
| `GET /api/calls/{id}` | Poll a call. Drives the live transcript |
| `POST /api/tools/invoice` | Server tool for the ElevenLabs agent |
| `POST /api/webhooks/elevenlabs` | Post-call webhook |
| `GET /api/queue` | The collect queue, ranked by expected recovery |
| `GET /api/call-stats` | Calls placed, completed, commitments, value secured |
| `GET /api/settings` · `PUT /api/settings` | Read and write desk settings |
| `POST /api/settings/reset` | Back to the `.env` defaults |
| `GET /api/rho/ping` | Check the Rho connection |

## Screens

| Screen | Does |
| --- | --- |
| Counterparties | One row per relationship. Click through to the dossier |
| Collect queue | Who to call and in what order, ranked by expected recovery rather than raw amount |
| Signals | What changed about the companies you deal with, newest first |
| Calls | Every call with its outcome. Click a row for the transcript |
| Agent settings | Identity, limits, guardrails and the do-not-call list |

### The ranking

The collect queue sorts on expected recovery, not size: `outstanding x
recoverability`, where age reduces the score, a severe signal roughly halves
it and a positive signal lifts it. It is a heuristic, not a model, and the UI
shows every term so you can disagree with it. On the sandbox that puts a $450
customer who just raised above a $1,682 one that just had a down round.

### Settings are not decoration

The approval threshold gates dialling (`POST /api/calls` returns 412 without
an approver), the do-not-call list is refused at the API with 403 rather than
hidden in the UI, and the payment window, instalment limit, AI disclosure and
company name all flow into the brief the voice agent receives.
