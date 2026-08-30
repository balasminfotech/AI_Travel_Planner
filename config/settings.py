from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]

# Load environment variables from the project .env file.
load_dotenv(BASE_DIR / ".env")


def _get_float(
    name: str,
    default: float,
) -> float:
    raw = os.getenv(name)

    if raw is None or raw.strip() == "":
        return default

    try:
        return float(raw)
    except ValueError:
        return default


def _get_int(
    name: str,
    default: int,
) -> int:
    raw = os.getenv(name)

    if raw is None or raw.strip() == "":
        return default

    try:
        return int(raw)
    except ValueError:
        return default


# =====================================================
# Gemini / LLM Configuration
# =====================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "",
).strip()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-flash-lite-latest",
).strip()

TEMPERATURE = _get_float(
    "TEMPERATURE",
    0.2,
)

# =====================================================
# Weather Configuration
# =====================================================

WEATHER_GEOCODING_URL = os.getenv(
    "WEATHER_GEOCODING_URL",
    "https://geocoding-api.open-meteo.com/v1/search",
).strip()

WEATHER_FORECAST_URL = os.getenv(
    "WEATHER_FORECAST_URL",
    "https://api.open-meteo.com/v1/forecast",
).strip()

WEATHER_REQUEST_TIMEOUT = _get_int(
    "WEATHER_REQUEST_TIMEOUT",
    15,
)

# =====================================================
# Maps / Routing Configuration
# =====================================================

MAPS_GEOCODING_URL = os.getenv(
    "MAPS_GEOCODING_URL",
    "https://nominatim.openstreetmap.org/search",
).strip()

MAPS_ROUTING_URL = os.getenv(
    "MAPS_ROUTING_URL",
    "https://router.project-osrm.org/route/v1/driving",
).strip()

MAPS_USER_AGENT = os.getenv(
    "MAPS_USER_AGENT",
    "AI_Travel_Planner/1.0",
).strip()

MAPS_REQUEST_TIMEOUT = _get_int(
    "MAPS_REQUEST_TIMEOUT",
    15,
)

# =====================================================
# Logging Configuration
# =====================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).strip().upper()

LOG_MAX_BYTES = _get_int(
    "LOG_MAX_BYTES",
    1_000_000,
)

LOG_BACKUP_COUNT = _get_int(
    "LOG_BACKUP_COUNT",
    3,
)


def validate_required_settings() -> list[str]:
    """
    Return missing required settings without exposing secret values.
    """

    missing: list[str] = []

    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")

    return missing
