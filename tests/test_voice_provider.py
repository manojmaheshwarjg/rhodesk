"""The carrier is a URL segment, so the only thing worth pinning is that a
typo cannot quietly build a 404 that reads like an ElevenLabs outage."""
from __future__ import annotations

import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from rhodesk import config, voice  # noqa: E402


def test_default_is_twilio():
    config.ELEVENLABS_TELEPHONY = "twilio"
    assert voice.outbound_provider() == "twilio"


def test_exotel_is_selectable():
    config.ELEVENLABS_TELEPHONY = "exotel"
    assert voice.outbound_provider() == "exotel"


def test_sip_trunk_maps_to_the_hyphenated_path():
    """The env var uses an underscore, the API path uses a hyphen. Passing the
    config value through verbatim built a 404 that looked like a refused call."""
    config.ELEVENLABS_TELEPHONY = "sip_trunk"
    assert voice.outbound_provider() == "sip-trunk"


def test_hyphenated_spelling_also_accepted():
    config.ELEVENLABS_TELEPHONY = "sip-trunk"
    assert voice.outbound_provider() == "sip-trunk"


def test_a_typo_falls_back_rather_than_404s():
    config.ELEVENLABS_TELEPHONY = "exotell"
    assert voice.outbound_provider() == "twilio"
    config.ELEVENLABS_TELEPHONY = "twilio"


# --- spoken reference forms -------------------------------------------------

def test_invoice_prefix_is_not_spelled_out():
    """The agent already says the word "invoice", so I-N-V is three syllables
    of nothing and it is what made the number sound laboured on a real call."""
    assert voice.say_reference("INV-2026-0001") == "twenty twenty six, zero zero zero one"


def test_a_meaningful_prefix_is_still_spelled():
    assert voice.say_reference("FT-2026-0001").startswith("F T,")


def test_a_bare_reference_is_left_alone():
    """A reference that is nothing but the prefix still has to be readable."""
    assert voice.say_reference("INV") == "I N V"


def test_empty_reference_is_empty():
    assert voice.say_reference("") == ""
