"""Configuration. Everything external is optional: if a key is missing the
matching client falls back to a deterministic stub so the whole pipeline
still runs end to end."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _flag(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()


# --- Rho -------------------------------------------------------------------
# The sandbox needs no account and accepts any non-empty bearer token.
# live | fixtures. "fixtures" serves a generated 18-month ledger with no
# network at all, which is both richer than the public sandbox and immune to
# venue wifi. See rhodesk/fixtures.py.
RHO_MODE = _flag("RHO_MODE", "live").lower()
RHO_BASE_URL = _flag("RHO_BASE_URL", "https://rhoapi-sandbox.rho.co/api/v1")
RHO_TOKEN = _flag("RHO_TOKEN", "sandbox")

# --- Tavily ----------------------------------------------------------------
TAVILY_API_KEY = _flag("TAVILY_API_KEY")
TAVILY_BASE_URL = _flag("TAVILY_BASE_URL", "https://api.tavily.com")

# --- LLM -------------------------------------------------------------------
# provider: anthropic | openai | groq | off
# Groq is OpenAI-compatible and very fast, which matters here: a full desk run
# makes one LLM call per counterparty, so latency compounds.
LLM_PROVIDER = _flag("LLM_PROVIDER", "anthropic").lower()
ANTHROPIC_API_KEY = _flag("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = _flag("ANTHROPIC_MODEL", "claude-sonnet-5")
OPENAI_API_KEY = _flag("OPENAI_API_KEY")
OPENAI_MODEL = _flag("OPENAI_MODEL", "gpt-4.1")
GROQ_API_KEY = _flag("GROQ_API_KEY")
GROQ_MODEL = _flag("GROQ_MODEL", "openai/gpt-oss-120b")
GROQ_BASE_URL = _flag("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

# --- ElevenLabs ------------------------------------------------------------
ELEVENLABS_API_KEY = _flag("ELEVENLABS_API_KEY")
ELEVENLABS_AGENT_ID = _flag("ELEVENLABS_AGENT_ID")
ELEVENLABS_PHONE_NUMBER_ID = _flag("ELEVENLABS_PHONE_NUMBER_ID")
ELEVENLABS_BASE_URL = _flag("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io")
# Which carrier ElevenLabs dials through: twilio | exotel | sip_trunk. All
# three take the same request and return the same response, so this only picks
# a URL. Exotel is the one that matters for Indian numbers, where Twilio's
# regulatory position makes outbound awkward.
ELEVENLABS_TELEPHONY = _flag("ELEVENLABS_TELEPHONY", "twilio").lower()
TELEPHONY_PROVIDERS = ("twilio", "exotel", "sip_trunk")

# --- Desk behaviour --------------------------------------------------------
COMPANY_NAME = _flag("COMPANY_NAME", "FusionTech")
# Calls above this amount (in cents) need a human to approve before dialling.
APPROVAL_THRESHOLD_CENTS = int(_flag("APPROVAL_THRESHOLD_CENTS", "2500000"))
# A counterparty is "overdue" once an invoice passes this many days.
OVERDUE_DAYS = int(_flag("OVERDUE_DAYS", "1"))
# Dial this number instead of the counterparty's, for demos. Strongly advised.
DEMO_OVERRIDE_NUMBER = _flag("DEMO_OVERRIDE_NUMBER")
# The sandbox has only 72 transactions, so no vendor is charged often enough
# for subscription detection to fire and the Cut posture never appears. Set
# this to add clearly-labelled synthetic vendors so all three postures are
# demonstrable. Everything they produce is badged "demo" in the UI.
# How many counterparties to research at once. The monitor stage is entirely
# network-bound (Tavily searches plus one LLM call each), so running it
# sequentially costs minutes. Raise if your API rate limits allow.
MONITOR_CONCURRENCY = int(_flag("MONITOR_CONCURRENCY", "8"))
# Give up on one counterparty rather than stalling the whole run.
MONITOR_TIMEOUT_SECONDS = int(_flag("MONITOR_TIMEOUT_SECONDS", "90"))

DEMO_VENDORS = _flag("DEMO_VENDORS", "true").lower() in ("1", "true", "yes")

# Read the generated ledger as it stood this many days ago. Only meaningful
# with RHO_MODE=fixtures. Its purpose is the history layer: a diff needs two
# runs that genuinely differ, and waiting a day for one is not a demo.
FIXTURE_DAYS_AGO = int(_flag("FIXTURE_DAYS_AGO", "0"))


def reading_date():
    """The date the desk is reading the ledger as of. Today, unless a demo has
    asked to look backwards. Every age in the pipeline is measured from here,
    so a rewound ledger also reads as younger."""
    from datetime import date, timedelta
    return date.today() - timedelta(days=FIXTURE_DAYS_AGO)

DB_PATH = Path(_flag("DB_PATH", str(ROOT / "rhodesk.db")))
STATIC_DIR = Path(__file__).resolve().parent / "static"


def status() -> dict:
    """What is actually wired up. The UI shows this so you always know
    whether you are looking at live data or a stub."""
    llm_key = {"anthropic": ANTHROPIC_API_KEY, "openai": OPENAI_API_KEY,
               "groq": GROQ_API_KEY}.get(LLM_PROVIDER, "")
    return {
        "rho": {"live": RHO_MODE != "fixtures",
                "base_url": "fixtures://generated" if RHO_MODE == "fixtures" else RHO_BASE_URL,
                "mode": RHO_MODE,
                "note": ("generated ledger, no network" if RHO_MODE == "fixtures"
                         else "sandbox" if "sandbox" in RHO_BASE_URL else "PRODUCTION")},
        "tavily": {"live": bool(TAVILY_API_KEY),
                   "note": "live search" if TAVILY_API_KEY else "stubbed, set TAVILY_API_KEY"},
        "llm": {"live": bool(llm_key), "provider": LLM_PROVIDER,
                "model": {"anthropic": ANTHROPIC_MODEL, "openai": OPENAI_MODEL,
                          "groq": GROQ_MODEL}.get(LLM_PROVIDER, ""),
                "note": (f"{LLM_PROVIDER} live" if llm_key
                         else f"stubbed, set {LLM_PROVIDER.upper()}_API_KEY")},
        "voice": {"live": bool(ELEVENLABS_API_KEY and ELEVENLABS_AGENT_ID),
                  "telephony": ELEVENLABS_TELEPHONY,
                  "note": "ElevenLabs wired" if ELEVENLABS_API_KEY and ELEVENLABS_AGENT_ID
                          else "simulated calls, set ELEVENLABS_API_KEY and ELEVENLABS_AGENT_ID"},
        "company": COMPANY_NAME,
        "approval_threshold_cents": APPROVAL_THRESHOLD_CENTS,
        "demo_override_number": bool(DEMO_OVERRIDE_NUMBER),
        "demo_vendors": DEMO_VENDORS,
        "monitor_concurrency": MONITOR_CONCURRENCY,
    }
