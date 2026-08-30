from unittest.mock import Mock, patch

from tools.weather_tool import WeatherTool


def test_weather_uses_trip_start_and_end_dates():

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
    geocode_response.raise_for_status.return_value = None

    weather_response = Mock()
    weather_response.json.return_value = {
        "timezone": "Asia/Kolkata",
        "daily": {
            "time": [
                "2026-08-31",
                "2026-09-01",
            ],
            "weather_code": [53, 53],
            "temperature_2m_max": [28.6, 29.0],
            "temperature_2m_min": [24.5, 24.2],
            "precipitation_probability_max": [96, 80],
            "precipitation_sum": [9.0, 4.0],
        },
    }
    weather_response.raise_for_status.return_value = None

    with patch(
        "tools.weather_tool.requests.get",
        side_effect=[
            geocode_response,
            weather_response,
        ],
    ) as mock_get:

        result = WeatherTool().get_forecast(
            location="Goa",
            forecast_days=2,
            start_date="2026-08-31",
        )

    weather_call = mock_get.call_args_list[1]
    params = weather_call.kwargs["params"]

    assert params["start_date"] == "2026-08-31"
    assert params["end_date"] == "2026-09-01"
    assert "forecast_days" not in params

    assert result.days[0].date == "2026-08-31"
    assert result.days[1].date == "2026-09-01"
