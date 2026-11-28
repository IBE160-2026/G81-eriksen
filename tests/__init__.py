"""Testpakken. Ingen test skal sende ekte KI-kall, selv om `.env` har en nøkkel (NFR-8)."""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.conf import settings  # noqa: E402

# Testene velger selv en nøkkel med `override_settings` og bruker falsk transport eller `FalskKi`.
settings.ANTHROPIC_API_KEY = ""
