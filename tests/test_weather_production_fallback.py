from unittest.mock import Mock, patch

from tools.weather_tool import WeatherTool


def test_known_location_case_insensitive():

    with patch(
        "tools.weather_tool.requests.get"
    ) as mock_get:

        latitude, longitude, name = (
            WeatherTool()._geocode(
                "  GOA  "
            )
        )

    mock_get.assert_not_called()

    assert latitude == 15.4909
    assert longitude == 73.8278
    assert name == "Goa"


def test_chennai_bypasses_geocoding():

    with patch(
        "tools.weather_tool.requests.get"
    ) as mock_get:

        latitude, longitude, name = (
            WeatherTool()._geocode(
                "Chennai"
            )
        )

    mock_get.assert_not_called()

    assert latitude == 13.0827
    assert longitude == 80.2707
    assert name == "Chennai"


def test_unknown_destination_uses_geocoder():

    response = Mock()

    response.raise_for_status.return_value = None

    response.json.return_value = {
        "results": [
            {
                "latitude": 48.8566,
                "longitude": 2.3522,
                "name": "Paris",
            }
        ]
    }

    with patch(
        "tools.weather_tool.requests.get",
        return_value=response,
    ) as mock_get:

        latitude, longitude, name = (
            WeatherTool()._geocode(
                "Paris"
            )
        )

    mock_get.assert_called_once()

    assert latitude == 48.8566
    assert longitude == 2.3522
    assert name == "Paris"
