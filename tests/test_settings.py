from config.settings import (
    APP_NAME,
    APP_VERSION,
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)


def test_app_name():
    assert APP_NAME == "AI Travel Planner"


def test_app_version():
    assert APP_VERSION == "1.0.0"


def test_gemini_api_key():
    assert GEMINI_API_KEY is not None
    assert len(GEMINI_API_KEY) > 0


def test_model_name():
    assert MODEL_NAME == "gemini-flash-lite-latest"


def test_temperature():
    assert 0.0 <= TEMPERATURE <= 1.0