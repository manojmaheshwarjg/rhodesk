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


def test_sip_trunk_is_selectable():
    config.ELEVENLABS_TELEPHONY = "sip_trunk"
    assert voice.outbound_provider() == "sip_trunk"


def test_a_typo_falls_back_rather_than_404s():
    config.ELEVENLABS_TELEPHONY = "exotell"
    assert voice.outbound_provider() == "twilio"
    config.ELEVENLABS_TELEPHONY = "twilio"
