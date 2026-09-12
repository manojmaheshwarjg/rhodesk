"""ElevenLabs voice agent: place the call, receive the result.

Set ELEVENLABS_API_KEY plus ELEVENLABS_AGENT_ID (and
ELEVENLABS_PHONE_NUMBER_ID for outbound telephony) to place real calls.
Without them, `start_call` runs a scripted simulation so the full flow is
demonstrable with no phone number, which is what you want while building.

VERIFY BEFORE THE DEMO: the outbound-call request shape below follows
ElevenLabs' documented Agents API, but it was written without a key to test
against. Check elevenlabs.io/docs and adjust `start_call` if it has moved.

The dossier reaches the agent as dynamic variables, so one agent
configuration serves every counterparty. In the ElevenLabs dashboard your
agent's prompt should reference them as {{counterparty}}, {{amount}} and so
on, and you should register a `get_invoice_details` server tool pointing at
this app's /api/tools/invoice endpoint.
"""
from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone

import httpx

from . import config, db


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety"]


def say_number(n: int) -> str:
    """Write an integer the way a person reads it aloud."""
    n = int(n)
    if n < 0:
        return "minus " + say_number(-n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return ONES[n // 100] + " hundred" + ("" if rest == 0 else " and " + say_number(rest))
    for size, word in ((1_000_000_000, "billion"), (1_000_000, "million"), (1000, "thousand")):
        if n >= size:
            rest = n % size
            return say_number(n // size) + " " + word + ("" if rest == 0 else " " + say_number(rest))
    return str(n)


def say_money(cents: int) -> str:
    """$59,200.00 becomes 'fifty nine thousand two hundred dollars'.

    TTS reads raw currency strings badly, and amounts are the whole point of
    these calls, so the spoken form is computed here rather than left to the
    model to improvise on every turn.
    """
    whole, part = divmod(abs(int(cents)), 100)
    out = say_number(whole) + (" dollar" if whole == 1 else " dollars")
    if part:
        out += " and " + say_number(part) + (" cent" if part == 1 else " cents")
    return out


# Prefixes that already mean "invoice". The agent says the word "invoice"
# before reading the reference, so spelling out I-N-V adds three syllables of
# nothing and makes the number sound harder than it is.
REDUNDANT_PREFIXES = {"INV", "INVC", "INVOICE", "IN"}


def say_reference(ref: str) -> str:
    """INV-2026-0001 becomes 'twenty twenty six, zero zero zero one', which is
    how a person reads a reference code down a phone line. A leading INV is
    dropped rather than spelled, because the sentence around it already says
    invoice; a meaningful prefix is still spelled out."""
    if not ref:
        return ""
    groups = []
    chunks = [c for c in re.split(r"[^A-Za-z0-9]+", ref) if c]
    for index, chunk in enumerate(chunks):
        if index == 0 and len(chunks) > 1 and chunk.upper() in REDUNDANT_PREFIXES:
            continue
        if chunk.isalpha():
            groups.append(" ".join(chunk.upper()))
        elif chunk.isdigit() and len(chunk) == 4 and chunk[0] in "12":
            # A year reads as a year: 2026 is "twenty twenty six".
            groups.append(f"{say_number(int(chunk[:2]))} {say_number(int(chunk[2:]))}"
                          if chunk[2:] != "00" else say_number(int(chunk)))
        else:
            groups.append(" ".join(ONES[int(d)] if d.isdigit() else d.upper() for d in chunk))
    return ", ".join(groups)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# Last outbound-call failure, surfaced in /api/status. A refused call falls
# back to simulation and otherwise looks identical to a working demo, which is
# how a 404 on the endpoint path went unnoticed once already.
last_error: str = ""

# The URL segment each carrier uses. These are NOT just the config values:
# ElevenLabs spells the SIP trunk path with a hyphen while the env var uses an
# underscore, and passing the env value straight through builds a 404 that
# looks exactly like a refused call.
PROVIDER_PATHS = {
    "twilio": "twilio",
    "exotel": "exotel",
    "sip_trunk": "sip-trunk",
    "sip-trunk": "sip-trunk",
}


def outbound_provider() -> str:
    """The URL segment for the configured carrier. Unknown values fall back to
    twilio rather than building a 404, because a typo in an env var should not
    look like an ElevenLabs outage."""
    return PROVIDER_PATHS.get(config.ELEVENLABS_TELEPHONY, "twilio")


class VoiceClient:
    @property
    def live(self) -> bool:
        return bool(config.ELEVENLABS_API_KEY and config.ELEVENLABS_AGENT_ID)

    def spoken_opening(self, cp: dict, brief: dict) -> str:
        """The opening line with its numbers already written out.

        The UI keeps the readable form ("$59,200.00") because a human is
        reading it off a briefing screen. The agent gets this one, because a
        machine is about to read it out loud.
        """
        line = brief.get("opening_line", "")
        amount = f"${cp.get('outstanding', 0) / 100:,.2f}"
        days = str(cp.get("oldest_days") or 0)
        invoice = brief.get("invoice_number", "")
        if amount in line:
            line = line.replace(amount, say_money(cp.get("outstanding", 0)))
        if invoice:
            line = line.replace(invoice, say_reference(invoice))
        line = re.sub(rf"\b{re.escape(days)} days\b", f"{say_number(int(days))} days", line)
        return line

    def dynamic_variables(self, cp: dict, brief: dict) -> dict[str, str]:
        """Everything the agent needs to sound like it did its homework."""
        return {
            "company": config.COMPANY_NAME,
            "counterparty": cp["display_name"],
            "contact_name": cp.get("contact_name") or "there",
            "posture": cp.get("posture", "collect"),
            "amount": f"${cp.get('outstanding', 0) / 100:,.2f}",
            "amount_spoken": say_money(cp.get("outstanding", 0)),
            "oldest_days": str(cp.get("oldest_days") or 0),
            "oldest_days_spoken": say_number(cp.get("oldest_days") or 0),
            "invoice_number": brief.get("invoice_number", ""),
            "invoice_spoken": say_reference(brief.get("invoice_number", "")),
            "opening_line": self.spoken_opening(cp, brief),
            "opening_line_written": brief.get("opening_line", ""),
            "may_agree": "; ".join(brief.get("may_agree", [])),
            "must_not": "; ".join(brief.get("must_not", [])),
            "context": " ".join(brief.get("context", [])),
        }

    def start_call(self, cp: dict, brief: dict, to_number: str) -> dict:
        """Dial out through whichever carrier is configured, returning
        {provider_ref, simulated}.

        ElevenLabs exposes one endpoint per provider, but they take the same
        body (agent_id, agent_phone_number_id, to_number, plus the client data)
        and return the same fields, so switching carriers is a URL and a
        different phone number id in the dashboard. Nothing else here moves.
        """
        if not self.live:
            return {"provider_ref": f"sim_{uuid.uuid4().hex[:10]}", "simulated": True}

        payload = {
            "agent_id": config.ELEVENLABS_AGENT_ID,
            "agent_phone_number_id": config.ELEVENLABS_PHONE_NUMBER_ID,
            "to_number": to_number,
            "conversation_initiation_client_data": {
                "dynamic_variables": self.dynamic_variables(cp, brief),
            },
        }
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.post(
                    f"{config.ELEVENLABS_BASE_URL}/v1/convai/"
                    f"{outbound_provider()}/outbound-call",
                    headers={"xi-api-key": config.ELEVENLABS_API_KEY,
                             "content-type": "application/json"},
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:  # noqa: BLE001 - fall back rather than fail the demo
            global last_error
            detail = str(exc)[:300]
            resp = getattr(exc, "response", None)
            if resp is not None:
                detail = f"{resp.status_code}: {resp.text[:300]}"
            last_error = f"{outbound_provider()} - {detail}"
            # Printed as well as stored: a silent fallback to simulation is
            # indistinguishable from a working demo until someone picks up.
            print(f"[voice] outbound call refused: {last_error}", flush=True)
            return {"provider_ref": f"sim_{uuid.uuid4().hex[:10]}", "simulated": True,
                    "error": detail}
        return {"provider_ref": data.get("conversation_id") or data.get("callSid") or "",
                "simulated": False, "raw": data}

    def signed_url(self) -> str | None:
        """A short-lived URL the browser can open without ever seeing the API
        key. Required for private agents; public agents can connect with the
        agent id alone.

        VERIFY: endpoint shape follows the documented Agents API but was
        written without a key to test against.
        """
        if not self.live:
            return None
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.get(
                    f"{config.ELEVENLABS_BASE_URL}/v1/convai/conversation/get-signed-url",
                    params={"agent_id": config.ELEVENLABS_AGENT_ID},
                    headers={"xi-api-key": config.ELEVENLABS_API_KEY},
                )
                resp.raise_for_status()
                return resp.json().get("signed_url")
        except Exception:  # noqa: BLE001 - public agents work without one
            return None

    def fetch_conversation(self, conversation_id: str) -> dict | None:
        if not self.live or not conversation_id:
            return None
        try:
            with httpx.Client(timeout=45.0) as client:
                resp = client.get(
                    f"{config.ELEVENLABS_BASE_URL}/v1/convai/conversations/{conversation_id}",
                    headers={"xi-api-key": config.ELEVENLABS_API_KEY},
                )
                resp.raise_for_status()
                return resp.json()
        except Exception:  # noqa: BLE001
            return None


# --- simulation ------------------------------------------------------------
# A scripted call so the whole loop is demonstrable with no telephony. The
# turns are revealed one at a time by the UI polling /api/calls/{id}.
#
# Not every call ends in a tidy commitment, and a demo where all four do looks
# fake. So there is an outcome catalogue: which one a counterparty gets is
# chosen deterministically from its id, biased by posture and by what the
# research found, so the same counterparty always behaves the same way while
# the log as a whole looks like real collections work.


def _pick(cp: dict, options: list[str]) -> str:
    """Stable choice: the same counterparty always gets the same outcome."""
    digest = hashlib.sha1(cp["id"].encode()).digest()
    return options[digest[0] % len(options)]


def _eligible(cp: dict, signals: list[dict] | None = None) -> list[str]:
    severities = {s.get("severity") for s in (signals or [])}
    if cp.get("posture") == "cut":
        return ["cut_agreed", "cut_cancelled", "cut_retention", "cut_escalated", "voicemail"]
    if cp.get("posture") == "cover" or "severe" in severities:
        # A company in trouble rarely pays in full on the first call.
        return ["partial", "deferred", "refused", "partial", "dispute"]
    if "positive" in severities:
        # They just raised, so they can pay.
        return ["commitment", "commitment", "partial", "deferred"]
    return ["commitment", "partial", "voicemail", "dispute", "deferred"]


def simulate(cp: dict, brief: dict, signals: list[dict] | None = None) -> dict:
    """Returns {'kind', 'script', 'outcome'} for one simulated call."""
    kind = _pick(cp, _eligible(cp, signals))
    name = cp["display_name"]
    total = cp.get("outstanding", 0)
    amount = f"${total / 100:,.2f}"
    half = f"${total / 200:,.2f}"
    days = cp.get("oldest_days") or 0
    inv = brief.get("invoice_number") or "the open invoice"
    opening = brief.get("opening_line", "")
    tool = {"role": "tool",
            "text": f"get_invoice_details · {inv if inv else name} · returned in 340ms"}

    if kind == "voicemail":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "You have reached the accounts inbox. Please leave a message after the tone."},
            {"role": "agent", "text": f"This is a message for the accounts team at {name}. "
                                      f"Calling about {inv}, {amount}, now {days} days past due. "
                                      f"Please call {config.COMPANY_NAME} back, or reply to the email we sent this morning."},
        ], "outcome": {
            "result": "voicemail", "answered": False,
            "summary": "No answer. Voicemail left, retry queued.",
            "commitments": [], "sentiment": "n/a"}}

    if kind == "commitment":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "Yes, go ahead. I have the invoice open."},
            tool,
            {"role": "agent", "text": f"It is {amount}, now {days} days out. Could we agree a date this week?"},
            {"role": "human", "text": "We can release it Friday. It was sitting in an approval queue, nobody chased it."},
            {"role": "agent", "text": "Friday works. I will send written confirmation today so it does not stall again."},
            {"role": "human", "text": "Appreciated."},
        ], "outcome": {
            "result": "commitment", "answered": True,
            "summary": "Full payment agreed for Friday.",
            "commitments": [{"label": "Payment in full", "value": f"{amount} on Friday"}],
            "sentiment": "cooperative"}}

    if kind == "partial":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "Sure. Let me pull it up. Can you tell me what it was for?"},
            tool,
            {"role": "agent", "text": f"It is {amount}, now {days} days out. I know things have been busy "
                                      "on your side, so I am not looking to make this difficult. "
                                      "Could we agree a date this week?"},
            {"role": "human", "text": "I can do Thursday. I would need to split it though, half Thursday "
                                      "and half at the end of the month."},
            {"role": "agent", "text": "Two instalments works. So half on Thursday and the balance at "
                                      "month end. I will send written confirmation today."},
            {"role": "human", "text": "That is agreed."},
        ], "outcome": {
            "result": "partial", "answered": True,
            "summary": "Split into two instalments with dates agreed.",
            "commitments": [{"label": "Instalment 1", "value": f"{half} on Thursday"},
                            {"label": "Instalment 2", "value": f"{half} at month end"}],
            "sentiment": "cooperative"}}

    if kind == "dispute":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "I am not sure we owe that. We raised a query on it back in July."},
            tool,
            {"role": "agent", "text": f"I have {inv} at {amount}, issued on net 30 terms. I do not have "
                                      "a query logged against it on my side. Could you tell me what the "
                                      "query was, and I will get it to the right person?"},
            {"role": "human", "text": "Two of the line items were for work we cancelled. I sent an email to "
                                      "your accounts address and never heard back."},
            {"role": "agent", "text": "Understood, and I am sorry that went unanswered. I am not able to "
                                      "adjust an invoice on this call, so I am passing this to a person "
                                      "today with what you have told me. You will hear back within one "
                                      "business day."},
        ], "outcome": {
            "result": "dispute", "answered": True,
            "summary": "Invoice disputed, two line items queried. Escalated to a human.",
            "commitments": [{"label": "Action", "value": "Human follow up within 1 business day"}],
            "sentiment": "frustrated"}}

    if kind == "deferred":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "I am not the right person for that. Payments go through our "
                                      "finance director and she is out until Monday."},
            tool,
            {"role": "agent", "text": f"That is fine. It is {inv}, {amount}, {days} days past due. "
                                      "Could I leave it with you to put in front of her, and call back Monday?"},
            {"role": "human", "text": "Yes, send it across and I will make sure she sees it."},
        ], "outcome": {
            "result": "deferred", "answered": True,
            "summary": "Decision maker unavailable. Callback agreed for Monday.",
            "commitments": [{"label": "Callback", "value": "Monday"}],
            "sentiment": "neutral"}}

    if kind == "refused":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "I will be straight with you, we cannot commit to a date right now."},
            tool,
            {"role": "agent", "text": f"I appreciate you saying so. It is {amount} on {inv}. Rather than "
                                      "a date, is there a smaller amount you could move this month?"},
            {"role": "human", "text": "Maybe part of it. I would have to come back to you, I cannot promise "
                                      "anything on this call."},
            {"role": "agent", "text": "That is honest and it helps. I will note that no date was agreed and "
                                      "flag it to our team rather than keep calling you."},
        ], "outcome": {
            "result": "refused", "answered": True,
            "summary": "No commitment. Counterparty says it cannot pay to a date.",
            "commitments": [], "sentiment": "strained"}}

    if kind == "cut_agreed":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "Let me pull up the account. What is the company name?"},
            tool,
            {"role": "agent", "text": f"{config.COMPANY_NAME}. Your published price for our plan is now "
                                      "lower than what we are being charged. Can we move to the current rate?"},
            {"role": "human", "text": "I can apply the current list price from your next renewal."},
            {"role": "agent", "text": "That works. Could you send written confirmation to finance?"},
            {"role": "human", "text": "Yes, I will send it today."},
        ], "outcome": {
            "result": "agreed", "answered": True,
            "summary": "Vendor agreed to move to current list pricing at renewal.",
            "commitments": [{"label": "New rate applied", "value": "at next renewal"}],
            "sentiment": "cooperative"}}

    if kind == "cut_cancelled":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "Sure, I can see two active subscriptions on this domain."},
            tool,
            {"role": "agent", "text": "That is the problem. We are paying for the same plan twice under two "
                                      "billing contacts. Please cancel the newer one and keep the original."},
            {"role": "human", "text": "Done. Cancellation reference is A-88213, effective at the end of "
                                      "this billing period."},
            {"role": "agent", "text": "Thank you. Could you email that reference to finance?"},
            {"role": "human", "text": "Already sent."},
        ], "outcome": {
            "result": "cancelled", "answered": True,
            "summary": "Duplicate subscription cancelled, reference A-88213.",
            "commitments": [{"label": "Cancelled", "value": "end of billing period"},
                            {"label": "Reference", "value": "A-88213"}],
            "sentiment": "cooperative"}}

    if kind == "cut_retention":
        return {"kind": kind, "script": [
            {"role": "agent", "text": opening},
            {"role": "human", "text": "Before we cancel anything, I can offer you 20% off for twelve months."},
            tool,
            {"role": "agent", "text": "I am not authorised to accept a retention offer on this call. I will "
                                      "put it in front of the account owner with the numbers, and someone "
                                      "will come back to you."},
            {"role": "human", "text": "No problem, the offer stands for thirty days."},
        ], "outcome": {
            "result": "retention_offered", "answered": True,
            "summary": "Vendor offered 20% for 12 months. Needs a human to accept.",
            "commitments": [{"label": "Offer", "value": "20% for 12 months, valid 30 days"}],
            "sentiment": "cooperative"}}

    # cut_escalated
    return {"kind": kind, "script": [
        {"role": "agent", "text": opening},
        {"role": "human", "text": "Pricing changes have to go through your account manager, I cannot do that here."},
        tool,
        {"role": "agent", "text": "Understood. Could you give me the account manager's name and the best "
                                  "way to reach them?"},
        {"role": "human", "text": "I will have them email you. Give me the billing address on the account."},
        {"role": "agent", "text": "It is on file with your billing contact. I will note that this needs the "
                                  "account manager and hand it to a person on our side."},
    ], "outcome": {
        "result": "escalated", "answered": True,
        "summary": "Front line cannot change pricing. Needs the account manager.",
        "commitments": [{"label": "Next step", "value": "Account manager to email"}],
        "sentiment": "neutral"}}


OUTCOME_SYSTEM = """You read the transcript of a call an AI agent made on
behalf of a business, chasing an unpaid invoice or renegotiating a vendor
contract, and extract what was actually agreed.

Return JSON:
{"result": "commitment"|"partial"|"dispute"|"deferred"|"refused"|"agreed"|"cancelled"|"none",
 "answered": true,
 "summary": "one sentence a finance person would want in the log",
 "commitments": [{"label": "...", "value": "..."}],
 "sentiment": "cooperative"|"neutral"|"strained"|"frustrated"}

Record only what the other party actually committed to. If nothing was agreed,
use "none" and an empty commitments list. Never invent a date or an amount."""


def extract_outcome(transcript: list[dict], counterparty: str) -> dict:
    """Turn a real conversation into the same outcome shape the simulation and
    the post-call webhook produce, so the log is uniform however a call ran."""
    from .llm import LLMClient

    spoken = [t for t in transcript if t.get("role") in ("agent", "human")]
    fallback = {
        "result": "none" if not spoken else "answered",
        "answered": bool(spoken),
        "summary": (f"Live conversation with {counterparty}, {len(spoken)} turns. "
                    "No model configured, so nothing was extracted."),
        "commitments": [], "sentiment": "",
    }
    if not spoken:
        return {**fallback, "summary": "No conversation recorded."}

    body = "\n".join(f"{'Agent' if t['role'] == 'agent' else counterparty}: {t['text']}"
                      for t in spoken)
    return LLMClient().json_call(OUTCOME_SYSTEM,
                                 f"Counterparty: {counterparty}\n\n{body}",
                                 fallback, max_tokens=900)


def turns_from(data: dict) -> list[dict]:
    """ElevenLabs writes {role, message}; the rest of the app speaks
    {role, text} with roles agent/human. One shape, wherever it arrived from."""
    turns = []
    for turn in (data.get("transcript") or []):
        role = "agent" if turn.get("role") in ("agent", "assistant") else "human"
        text = turn.get("message") or turn.get("text") or ""
        if text:
            turns.append({"role": role, "text": text})
    return turns


def reconcile(max_calls: int = 10) -> int:
    """Close out phone calls that nobody told us had ended.

    A browser call posts its own transcript back when the page closes it, and
    a webhook would do the same for a phone call. There is no webhook here, so
    a phone call stays "live" forever and never reaches the call log. This
    polls ElevenLabs for the conversation instead, which needs no public URL.

    Returns how many calls were closed.
    """
    client = VoiceClient()
    if not client.live:
        return 0
    closed = 0
    for call in db.query("calls", "state = ?", ("live",), "created_at DESC")[:max_calls]:
        ref = call.get("provider_ref") or ""
        if not ref.startswith("conv_"):
            continue                      # simulated, or never reached a carrier
        data = client.fetch_conversation(ref)
        if not data or data.get("status") not in ("done", "failed", "ended"):
            continue                      # still in progress, leave it alone
        turns = turns_from(data)
        cp = db.one("counterparties", call["counterparty_id"]) or {}
        outcome = extract_outcome(turns, cp.get("display_name", "the counterparty"))
        db.set_fields("calls", call["id"], state="done", ended_at=_now(),
                      transcript=json.dumps(turns), outcome=json.dumps(outcome))
        closed += 1
    return closed


def ingest_webhook(body: dict) -> str | None:
    """Accept an ElevenLabs post-call webhook and fold it into the call row.
    Returns the call id it matched, or None."""
    data = body.get("data") or body
    conv_id = data.get("conversation_id") or body.get("conversation_id")
    if not conv_id:
        return None
    rows = db.query("calls", "provider_ref = ?", (conv_id,))
    if not rows:
        return None
    call = rows[0]

    turns = turns_from(data)
    analysis = data.get("analysis") or {}
    outcome = {
        "result": analysis.get("call_successful", "unknown"),
        "summary": analysis.get("transcript_summary", ""),
        "commitments": analysis.get("data_collection_results", {}),
        "sentiment": "",
    }
    db.set_fields("calls", call["id"], state="done", ended_at=_now(),
                  transcript=json.dumps(turns) if turns else call["transcript"],
                  outcome=json.dumps(outcome))
    return call["id"]
