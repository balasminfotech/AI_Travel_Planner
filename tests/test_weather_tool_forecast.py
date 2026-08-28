from unittest.mock import Mock, patch

from tools.weather_tool import WeatherTool


def test_get_forecast():

    geocode_response = Mock()

    geocode_response.json.return_value = {
        "results": [
            {
                "latitude": 15.4909,
                "longitude": 73.8278,
                "name": "Goa",
            }
        ]
    }

    geocode_response.raise_for_status.return_value = (
        None
    )

    weather_response = Mock()

    weather_response.json.return_value = {
        "timezone": "Asia/Kolkata",
        "daily": {
            "time": [
                "2026-08-26",
                "2026-08-27",
                "2026-08-28",
            ],
            "weather_code": [
                3,
                61,
                1,
            ],
            "temperature_2m_max": [
                31.0,
                30.0,
                32.0,
            ],
            "temperature_2m_min": [
                25.0,
                24.0,
                25.0,
            ],
            "precipitation_probability_max": [
                20,
                60,
                10,
            ],
            "precipitation_sum": [
                0.0,
                4.2,
                0.0,
            ],
        },
    }

    weather_response.raise_for_status.return_value = (
        None
    )

    with patch(
        "tools.weather_tool.requests.get",
        side_effect=[
            geocode_response,
            weather_response,
        ],
    ) as mock_get:

        tool = WeatherTool()

        result = tool.get_forecast(
            "Goa",
            forecast_days=3,
        )

        assert result.location == "Goa"

        assert result.latitude == 15.4909

        assert result.longitude == 73.8278

        assert (
            result.timezone
            == "Asia/Kolkata"
        )

        assert len(result.days) == 3

        assert (
            result.days[0].temperature_max
            == 31
        )

        assert (
            result.days[1]
            .precipitation_probability
            == 60
        )

        assert (
            result.days[1]
            .precipitation_sum
            == 4.2
        )

        assert mock_get.call_count == 2