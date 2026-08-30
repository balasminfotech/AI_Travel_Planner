from config import settings


def test_default_model_name_is_available():
    assert isinstance(settings.MODEL_NAME, str)
    assert settings.MODEL_NAME


def test_temperature_is_float():
    assert isinstance(settings.TEMPERATURE, float)


def test_request_timeouts_are_positive():
    assert settings.WEATHER_REQUEST_TIMEOUT > 0
    assert settings.MAPS_REQUEST_TIMEOUT > 0


def test_logging_configuration_is_positive():
    assert settings.LOG_MAX_BYTES > 0
    assert settings.LOG_BACKUP_COUNT >= 0


def test_validate_required_settings_returns_list():
    result = settings.validate_required_settings()
    assert isinstance(result, list)
