"""FastAPI app: the desk's HTTP surface and the UI it serves."""
from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import config, db, history, pipeline, settings as desk_settings, voice
from .llm import LLMClient
from . import rho as rho_module
from .rho import RhoError
from .tavily import TavilyClient

app = FastAPI(title="Rho Desk")

_run_lock = threading.Lock()
_run_state: dict = {"running": False, "stage": "idle", "detail": "", "finished": None}

TURN_SECONDS = 3.5


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.on_event("startup")
def _startup() -> None:
    db.init()


# --- status and setup ------------------------------------------------------

@app.get("/api/status")
def status() -> dict:
    from .llm import last_error as llm_error
    counts = {
        "signals": len(db.query("signals")),
        "calls": len(db.query("calls")),
    }
    from .tavily import last_error as tavily_error
    # Rows outlive the run that wrote them now, so a plain COUNT would report
    # every counterparty ever seen rather than the ones on the desk today.
    where, params = _current_scope()
    counts["counterparties"] = len(db.query("counterparties", where, params))
    services = config.status()
    if llm_error:
        services["llm"]["last_error"] = llm_error
    if tavily_error:
        services["tavily"]["last_error"] = tavily_error
        services["tavily"]["note"] = "key set, but " + tavily_error
    current = history.current_run()
    last = history.run(current) if current else None
    return {"services": services, "counts": counts, "run": _run_state,
            "current_run": current,
            "last_run": last,
            "run_count": db.scalar("SELECT COUNT(*) FROM runs WHERE status='done'") or 0}


@app.get("/api/rho/ping")
def rho_ping() -> dict:
    try:
        with rho_module.client() as rho:
            return rho.ping()
    except RhoError as exc:
        raise HTTPException(502, str(exc)) from exc


# --- the run ---------------------------------------------------------------

def _do_run() -> None:
    def progress(stage: str, detail: str) -> None:
        _run_state.update(stage=stage, detail=detail)

    try:
        _run_state.update(running=True, stage="starting", detail="", finished=None)
        result = pipeline.run_desk(progress)
        _run_state.update(finished=result)
    except Exception as exc:  # noqa: BLE001
        _run_state.update(stage="error", detail=str(exc)[:400])
    finally:
        _run_state["running"] = False
        _run_lock.release()


@app.post("/api/run")
def run(background: BackgroundTasks) -> dict:
    if not _run_lock.acquire(blocking=False):
        return {"started": False, "reason": "already running"}
    background.add_task(_do_run)
    return {"started": True}


@app.get("/api/run")
def run_state() -> dict:
    return _run_state


# --- counterparties --------------------------------------------------------

def _enrich(row: dict) -> dict:
    row["signals"] = db.query("signals", "counterparty_id = ?", (row["id"],),
                              "observed_at DESC")
    return row


def _current_scope() -> tuple[str, tuple]:
    """Rows are no longer wiped between runs, so the live view is whatever the
    most recent run touched. Everything else is history."""
    current = history.current_run()
    if current is None:
        return "", ()
    return "last_seen_run = ?", (current,)


@app.get("/api/counterparties")
def counterparties(posture: str | None = None) -> list[dict]:
    where, params = _current_scope()
    if posture and posture != "all":
        where = f"{where} AND posture = ?" if where else "posture = ?"
        params = (*params, posture)
    rows = db.query("counterparties", where, params,
                    "outstanding DESC, money_out DESC")
    by_cp: dict[str, int] = {}
    for s in db.query("signals"):
        by_cp[s["counterparty_id"]] = by_cp.get(s["counterparty_id"], 0) + 1
    # Nothing is "new" on a first run, when everything is.
    comparable = (db.scalar("SELECT COUNT(*) FROM runs WHERE status='done'") or 0) > 1
    for r in rows:
        r["signal_count"] = by_cp.get(r["id"], 0)
        r["is_new"] = bool(comparable and r.get("first_seen_run")
                           and r["first_seen_run"] == r.get("last_seen_run"))
        top = db.query("signals", "counterparty_id = ?", (r["id"],),
                       "CASE severity WHEN 'severe' THEN 0 WHEN 'warn' THEN 1 "
                       "WHEN 'positive' THEN 2 ELSE 3 END")
        r["top_signal"] = top[0] if top else None
    return rows


@app.get("/api/counterparties/{cp_id}")
def counterparty(cp_id: str) -> dict:
    row = db.one("counterparties", cp_id)
    if not row:
        raise HTTPException(404, "unknown counterparty")
    row = _enrich(row)
    row["calls"] = db.query("calls", "counterparty_id = ?", (cp_id,), "created_at DESC")
    return row


@app.get("/api/signals")
def signals() -> list[dict]:
    rows = db.query("signals", order="CASE severity WHEN 'severe' THEN 0 "
                                     "WHEN 'warn' THEN 1 WHEN 'positive' THEN 2 "
                                     "ELSE 3 END, observed_at DESC")
    names = {c["id"]: c for c in db.query("counterparties")}
    for r in rows:
        cp = names.get(r["counterparty_id"]) or {}
        r["counterparty_name"] = cp.get("display_name", r["counterparty_id"])
        r["outstanding"] = cp.get("outstanding", 0)
        r["posture"] = cp.get("posture", "watch")
    return rows


# --- briefing and calling --------------------------------------------------

@app.post("/api/counterparties/{cp_id}/brief")
def brief(cp_id: str) -> dict:
    row = db.one("counterparties", cp_id)
    if not row:
        raise HTTPException(404, "unknown counterparty")
    sigs = db.query("signals", "counterparty_id = ?", (cp_id,))
    return pipeline.build_brief(row, sigs, LLMClient())


@app.post("/api/calls")
async def start_call(request: Request) -> dict:
    body = await request.json()
    cp_id = body.get("counterparty_id")
    row = db.one("counterparties", cp_id or "")
    if not row:
        raise HTTPException(404, "unknown counterparty")

    brief_doc = body.get("brief")
    if not brief_doc:
        sigs = db.query("signals", "counterparty_id = ?", (cp_id,))
        brief_doc = pipeline.build_brief(row, sigs, LLMClient())

    cfg = desk_settings.get()
    if cp_id in (cfg.get("do_not_call") or []):
        raise HTTPException(403, "this counterparty is on the do-not-call list")
    if brief_doc.get("needs_approval") and not body.get("approved_by"):
        raise HTTPException(412, "this call is above the approval threshold "
                                 "and needs approved_by")

    to_number = (cfg.get("demo_override_number") or body.get("to_number")
                 or row.get("contact_phone") or "")
    client = voice.VoiceClient()
    started = client.start_call(row, brief_doc, to_number)

    sim_plan = {}
    if started.get("simulated"):
        sigs = db.query("signals", "counterparty_id = ?", (cp_id,))
        sim_plan = voice.simulate(row, brief_doc, sigs)

    call_id = uuid.uuid4().hex
    db.upsert("calls", [{
        "id": call_id, "counterparty_id": cp_id, "posture": row.get("posture"),
        "state": "live", "to_number": to_number,
        "brief": json.dumps(brief_doc), "transcript": "[]", "outcome": "{}",
        "provider_ref": started.get("provider_ref", ""),
        "simulated": 1 if started.get("simulated") else 0,
        "created_at": _now(), "ended_at": None,
        "sim_plan": json.dumps(sim_plan),
    }])

    return {"call_id": call_id, "simulated": bool(started.get("simulated")),
            "to_number": to_number, "provider_error": started.get("error")}


@app.get("/api/calls/{call_id}")
def call_state(call_id: str) -> dict:
    row = db.one("calls", call_id)
    if not row:
        raise HTTPException(404, "unknown call")

    sim = row.get("sim_plan") or {}
    if sim.get("script") and row["state"] == "live":
        started = datetime.fromisoformat(row["created_at"])
        elapsed = (datetime.now(timezone.utc) - started).total_seconds()
        script = sim["script"]
        reveal = min(int(elapsed / TURN_SECONDS) + 1, len(script))
        row["transcript"] = script[:reveal]
        row["elapsed_seconds"] = int(elapsed)
        if reveal >= len(script) and elapsed > len(script) * TURN_SECONDS:
            db.set_fields("calls", call_id, state="done", ended_at=_now(),
                          transcript=json.dumps(script),
                          outcome=json.dumps(sim["outcome"]))
            row.update(state="done", transcript=script, outcome=sim["outcome"])
    cp = db.one("counterparties", row["counterparty_id"]) or {}
    row["counterparty_name"] = cp.get("display_name", "")
    return row


@app.post("/api/calls/{call_id}/end")
def end_call(call_id: str) -> dict:
    row = db.one("calls", call_id)
    if not row:
        raise HTTPException(404, "unknown call")
    sim = row.get("sim_plan") or {}
    if sim.get("script"):
        db.set_fields("calls", call_id, state="done", ended_at=_now(),
                      transcript=json.dumps(sim["script"]),
                      outcome=json.dumps(sim["outcome"]))
    else:
        db.set_fields("calls", call_id, state="done", ended_at=_now())
    return {"ok": True}


@app.get("/api/calls")
def calls() -> list[dict]:
    rows = db.query("calls", order="created_at DESC")
    names = {c["id"]: c["display_name"] for c in db.query("counterparties")}
    for r in rows:
        r["counterparty_name"] = names.get(r["counterparty_id"], r["counterparty_id"])
    return rows


# --- agent-facing endpoints ------------------------------------------------

@app.post("/api/tools/invoice")
async def tool_invoice(request: Request) -> dict:
    """`get_invoice_details`, the tool the agent calls mid-conversation.

    Scoped deliberately. The lookup is confined to the counterparty on the
    call, so the agent cannot retrieve someone else's invoice by guessing a
    number, and an omitted number returns that counterparty's open invoices
    rather than whatever happened to be first in the table.

    Amounts come back in spoken form as well as written, because whatever this
    returns is about to be read out loud.
    """
    body = await request.json()
    number = (body.get("invoice_number") or "").strip()
    cp_id = (body.get("counterparty_id") or "").strip()

    cp = db.one("counterparties", cp_id) if cp_id else None
    if not cp:
        # Without a counterparty we refuse rather than search every customer.
        return {"found": False,
                "error": "no counterparty on this call, cannot look anything up"}

    invoices = cp.get("invoices") or []
    if number:
        match = next((i for i in invoices
                      if (i.get("number") or "").upper() == number.upper()), None)
        if not match:
            return {"found": False, "counterparty": cp["display_name"],
                    "message": f"No invoice {number} on this account."}
        return _invoice_payload(cp, match)

    open_invs = [i for i in invoices if i.get("open")]
    if not open_invs:
        return {"found": False, "counterparty": cp["display_name"],
                "message": "No open invoices on this account."}
    if len(open_invs) == 1:
        return _invoice_payload(cp, open_invs[0])
    return {
        "found": True, "counterparty": cp["display_name"],
        "count": len(open_invs),
        "total_spoken": voice.say_money(sum(i.get("total", 0) for i in open_invs)),
        "invoices": [_invoice_payload(cp, i) for i in open_invs],
    }


def _invoice_payload(cp: dict, inv: dict) -> dict:
    cents = inv.get("total", 0)
    overdue = inv.get("days_overdue") or 0
    return {
        "found": True,
        "counterparty": cp["display_name"],
        "invoice_number": inv.get("number"),
        "invoice_spoken": voice.say_reference(inv.get("number") or ""),
        "amount": f"${cents / 100:,.2f}",
        "amount_spoken": voice.say_money(cents),
        "due_date": inv.get("due_date"),
        "days_overdue": overdue,
        "days_overdue_spoken": voice.say_number(overdue),
        "status": inv.get("status"),
        "terms": "net 30",
    }


@app.post("/api/webhooks/elevenlabs")
async def elevenlabs_webhook(request: Request) -> JSONResponse:
    body = await request.json()
    call_id = voice.ingest_webhook(body)
    return JSONResponse({"ok": True, "call_id": call_id})


# --- browser voice ---------------------------------------------------------
# A judge talks to the agent through the laptop. No phone number, no Twilio,
# no ngrok. The browser opens a WebRTC session straight to ElevenLabs; this
# app supplies the dossier as dynamic variables and records what happened.

@app.post("/api/voice/session")
async def voice_session(request: Request) -> dict:
    body = await request.json()
    cp_id = body.get("counterparty_id")
    row = db.one("counterparties", cp_id or "")
    if not row:
        raise HTTPException(404, "unknown counterparty")

    cfg = desk_settings.get()
    if cp_id in (cfg.get("do_not_call") or []):
        raise HTTPException(403, "this counterparty is on the do-not-call list")

    brief_doc = body.get("brief")
    if not brief_doc:
        sigs = db.query("signals", "counterparty_id = ?", (cp_id,))
        brief_doc = pipeline.build_brief(row, sigs, LLMClient())
    if brief_doc.get("needs_approval") and not body.get("approved_by"):
        raise HTTPException(412, "this call is above the approval threshold "
                                 "and needs approved_by")

    client = voice.VoiceClient()
    call_id = uuid.uuid4().hex
    db.upsert("calls", [{
        "id": call_id, "counterparty_id": cp_id, "posture": row.get("posture"),
        "state": "live", "to_number": "browser",
        "brief": json.dumps(brief_doc), "transcript": "[]", "outcome": "{}",
        "provider_ref": "", "simulated": 0 if client.live else 1,
        "created_at": _now(), "ended_at": None, "sim_plan": "{}",
    }])

    return {
        "call_id": call_id,
        "available": client.live,
        "agent_id": config.ELEVENLABS_AGENT_ID or None,
        "signed_url": client.signed_url(),
        "dynamic_variables": client.dynamic_variables(row, brief_doc),
        "counterparty_name": row["display_name"],
        "opening_line": brief_doc.get("opening_line", ""),
    }


@app.post("/api/calls/{call_id}/transcript")
async def append_transcript(call_id: str, request: Request) -> dict:
    """The browser streams turns in as they happen, so the log is live."""
    row = db.one("calls", call_id)
    if not row:
        raise HTTPException(404, "unknown call")
    body = await request.json()
    turns = body.get("transcript") or []
    db.set_fields("calls", call_id, transcript=json.dumps(turns),
                  provider_ref=body.get("conversation_id") or row.get("provider_ref") or "")
    return {"ok": True, "turns": len(turns)}


@app.post("/api/calls/{call_id}/finish")
async def finish_call(call_id: str, request: Request) -> dict:
    """Close a browser call and extract what was agreed from the transcript,
    the same shape the simulation and the webhook produce."""
    row = db.one("calls", call_id)
    if not row:
        raise HTTPException(404, "unknown call")
    body = await request.json()
    turns = body.get("transcript") or row.get("transcript") or []
    cp = db.one("counterparties", row["counterparty_id"]) or {}
    outcome = voice.extract_outcome(turns, cp.get("display_name", "the counterparty"))
    db.set_fields("calls", call_id, state="done", ended_at=_now(),
                  transcript=json.dumps(turns), outcome=json.dumps(outcome))
    return {"ok": True, "outcome": outcome}


# --- settings --------------------------------------------------------------

@app.get("/api/settings")
def read_settings() -> dict:
    return desk_settings.get()


@app.put("/api/settings")
async def write_settings(request: Request) -> dict:
    return desk_settings.put(await request.json())


@app.post("/api/settings/reset")
def reset_settings() -> dict:
    return desk_settings.reset()


# --- collect queue ---------------------------------------------------------

def _recoverability(row: dict) -> float:
    """How likely is this money to come back if we call today?

    Age hurts, a severe signal hurts a lot, a positive signal helps. This is a
    heuristic, not a model, and it is deliberately legible: the UI shows every
    term so an operator can disagree with it.
    """
    score = 1.0
    days = row.get("oldest_days") or 0
    score *= max(0.35, 1.0 - days / 365)
    sev = {s["severity"] for s in row.get("signals", [])}
    if "severe" in sev:
        score *= 0.55
    elif "warn" in sev:
        score *= 0.8
    if "positive" in sev:
        score = min(1.0, score * 1.25)
    return round(score, 3)


@app.get("/api/queue")
def queue() -> dict:
    """The Collect queue: who to call, in order, and why."""
    where, params = _current_scope()
    rows = [r for r in db.query("counterparties", where, params)
            if r["posture"] in ("collect", "cover")]
    calls = db.query("calls", order="created_at DESC")
    last_call = {}
    for c in calls:
        last_call.setdefault(c["counterparty_id"], c)

    items = []
    for r in rows:
        r["signals"] = db.query("signals", "counterparty_id = ?", (r["id"],))
        recov = _recoverability(r)
        prev = last_call.get(r["id"])
        items.append({
            "id": r["id"], "display_name": r["display_name"],
            "posture": r["posture"], "outstanding": r["outstanding"],
            "oldest_days": r["oldest_days"], "open_invoices": r["open_invoices"],
            "ar_share": r["ar_share"], "recommendation": r["recommendation"],
            "contact_email": r["contact_email"],
            "recoverability": recov,
            "expected": int(r["outstanding"] * recov),
            "top_signal": (sorted(r["signals"],
                                  key=lambda s: {"severe": 0, "warn": 1,
                                                 "positive": 2}.get(s["severity"], 3))
                           or [None])[0],
            "last_call": {"state": prev["state"],
                          "created_at": prev["created_at"],
                          "summary": (prev.get("outcome") or {}).get("summary", "")}
                         if prev else None,
        })
    items.sort(key=lambda i: i["expected"], reverse=True)

    cfg = desk_settings.get()
    return {
        "items": items,
        "total_outstanding": sum(i["outstanding"] for i in items),
        "total_expected": sum(i["expected"] for i in items),
        "needs_approval_above": cfg["approval_threshold_cents"],
        "calls_per_run": cfg["calls_per_run"],
        "already_called": sum(1 for i in items if i["last_call"]),
    }


# --- history ---------------------------------------------------------------

@app.get("/api/runs")
def run_list(limit: int = 30) -> dict:
    rows = history.runs(limit)
    return {"runs": rows, "current": history.current_run()}


@app.get("/api/changes")
def changes(run_id: int | None = None) -> dict:
    """What moved between a run and the one before it. Computed once when the
    run finished and stored, so this is a read."""
    run_id = run_id or history.current_run()
    if not run_id:
        return {"run": None, "previous": None, "changes": [], "summary": {},
                "comparable": False}

    record = history.run(run_id) or {}
    prev_id = history.previous_run(run_id)
    rows = history.changes_for(run_id)

    summary: dict[str, int] = {}
    for row in rows:
        summary[row["weight"]] = summary.get(row["weight"], 0) + 1

    money = {"recovered": 0, "new_overdue": 0}
    for row in rows:
        if row["kind"] == "cleared":
            money["recovered"] += row["amount"] or 0
        elif row["kind"] in ("appeared", "aging") and (row["amount"] or 0) > 0:
            money["new_overdue"] += row["amount"] or 0

    return {
        "run": record,
        "previous": history.run(prev_id) if prev_id else None,
        "comparable": prev_id is not None,
        "changes": rows,
        "summary": summary,
        "money": money,
    }


@app.get("/api/counterparties/{cp_id}/timeline")
def timeline(cp_id: str) -> dict:
    rows = history.timeline(cp_id)
    if not rows:
        raise HTTPException(404, "no history for this counterparty")
    return {"counterparty_id": cp_id, "points": rows,
            "changes": db.rows(
                "SELECT * FROM changes WHERE counterparty_id = ? "
                "ORDER BY run_id DESC", (cp_id,))}


# --- calls log -------------------------------------------------------------

@app.get("/api/call-stats")
def call_stats() -> dict:
    rows = db.query("calls")
    done = [c for c in rows if c["state"] == "done"]
    answered = [c for c in done if (c.get("outcome") or {}).get("answered")]
    SECURES = {"commitment", "partial", "agreed", "cancelled"}
    committed = [c for c in done
                 if (c.get("outcome") or {}).get("result") in SECURES]
    recovered = 0
    for c in committed:
        cp = db.one("counterparties", c["counterparty_id"]) or {}
        recovered += cp.get("outstanding", 0)
    breakdown: dict[str, int] = {}
    for c in done:
        key = (c.get("outcome") or {}).get("result") or "unknown"
        breakdown[key] = breakdown.get(key, 0) + 1
    return {
        "placed": len(rows), "completed": len(done), "answered": len(answered),
        "commitments": len(committed), "value_secured": recovered,
        "simulated": sum(1 for c in rows if c["simulated"]),
        "breakdown": breakdown,
    }


# --- UI --------------------------------------------------------------------

@app.middleware("http")
async def no_cache_static(request: Request, call_next):
    """The UI is edited live all day. A cached app.js silently serves stale
    code and looks like the change did not work, so never cache it."""
    response = await call_next(request)
    if request.url.path.startswith("/static") or request.url.path == "/":
        response.headers["Cache-Control"] = "no-store, must-revalidate"
    return response


app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(config.STATIC_DIR / "index.html")
