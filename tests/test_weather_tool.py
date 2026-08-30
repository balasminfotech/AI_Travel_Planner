from unittest.mock import Mock, patch

import pytest

from tools.weather_tool import WeatherTool


def test_weather_tool_initialization():

    tool = WeatherTool(
        timeout=5
    )

    assert tool.timeout == 5


def test_empty_location():

    tool = WeatherTool()

    with pytest.raises(ValueError):
        tool.get_forecast("")


def test_invalid_forecast_days():

    tool = WeatherTool()

    with pytest.raises(ValueError):

        tool.get_forecast(
            "Goa",
            forecast_days=0,
        )


def test_known_location_bypasses_geocoder():

    with patch(
        "tools.weather_tool.requests.get"
    ) as mock_get:

        tool = WeatherTool()

        latitude, longitude, name = (
            tool._geocode("Goa")
        )

    assert latitude == 15.4909
    assert longitude == 73.8278
    assert name == "Goa"

    mock_get.assert_not_called()


def test_generic_geocode():

    mock_response = Mock()

    mock_response.json.return_value = {
        "results": [
            {
                "latitude": 35.6762,
                "longitude": 139.6503,
                "name": "Tokyo",
            }
        ]
    }

    mock_response.raise_for_status.return_value = (
        None
    )

    with patch(
        "tools.weather_tool.requests.get",
        return_value=mock_response,
    ) as mock_get:

        tool = WeatherTool()

        latitude, longitude, name = (
            tool._geocode("Tokyo")
        )

    assert latitude == 35.6762
    assert longitude == 139.6503
    assert name == "Tokyo"

    mock_get.assert_called_once()


def test_location_not_found():

    mock_response = Mock()

    mock_response.json.return_value = {
        "results": []
    }

    mock_response.raise_for_status.return_value = (
        None
    )

    with patch(
        "tools.weather_tool.requests.get",
        return_value=mock_response,
    ):

        tool = WeatherTool()

        with pytest.raises(ValueError):

            tool._geocode(
                "UnknownPlaceXYZ"
            )
