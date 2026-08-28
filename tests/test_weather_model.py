import pytest

from pydantic import ValidationError

from models.weather import (
    WeatherDay,
    WeatherForecast,
)


def test_valid_weather_day():

    day = WeatherDay(
        date="2026-08-26",
        weather_code=3,
        temperature_max=32,
        temperature_min=25,
        precipitation_probability=40,
        precipitation_sum=2.5,
    )

    assert day.date == "2026-08-26"
    assert day.temperature_max == 32
    assert day.temperature_min == 25
    assert (
        day.precipitation_probability
        == 40
    )


def test_invalid_precipitation_probability():

    with pytest.raises(ValidationError):

        WeatherDay(
            date="2026-08-26",
            weather_code=3,
            temperature_max=32,
            temperature_min=25,
            precipitation_probability=120,
            precipitation_sum=2,
        )


def test_weather_forecast():

    day = WeatherDay(
        date="2026-08-26",
        weather_code=1,
        temperature_max=31,
        temperature_min=24,
        precipitation_probability=20,
        precipitation_sum=0,
    )

    forecast = WeatherForecast(
        location="Goa",
        latitude=15.49,
        longitude=73.82,
        timezone="Asia/Kolkata",
        days=[day],
    )

    assert forecast.location == "Goa"
    assert len(forecast.days) == 1