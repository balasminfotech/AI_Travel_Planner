from unittest.mock import MagicMock, patch

import pytest

from models.maps import Location
from tools.maps_tool import MapsTool


def test_geocode():

    mock_response = MagicMock()

    mock_response.json.return_value = [
        {
            "display_name": "Chennai, Tamil Nadu, India",
            "lat": "13.0827",
            "lon": "80.2707",
        }
    ]

    mock_response.raise_for_status.return_value = None

    with patch(
        "tools.maps_tool.requests.get",
        return_value=mock_response,
    ) as mock_get:

        tool = MapsTool()

        result = tool.geocode(
            "Chennai"
        )

        assert result.name == (
            "Chennai, Tamil Nadu, India"
        )

        assert result.latitude == 13.0827

        assert result.longitude == 80.2707

        mock_get.assert_called_once()


def test_geocode_empty_place():

    tool = MapsTool()

    with pytest.raises(ValueError):

        tool.geocode("")


def test_geocode_not_found():

    mock_response = MagicMock()

    mock_response.json.return_value = []

    mock_response.raise_for_status.return_value = None

    with patch(
        "tools.maps_tool.requests.get",
        return_value=mock_response,
    ):

        tool = MapsTool()

        with pytest.raises(ValueError):

            tool.geocode(
                "UnknownPlace123456"
            )


def test_route_from_coordinates():

    origin = Location(
        name="Chennai",
        latitude=13.0827,
        longitude=80.2707,
    )

    destination = Location(
        name="Pondicherry",
        latitude=11.9416,
        longitude=79.8083,
    )

    mock_response = MagicMock()

    mock_response.json.return_value = {
        "code": "Ok",
        "routes": [
            {
                "distance": 150500,
                "duration": 10800,
            }
        ],
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "tools.maps_tool.requests.get",
        return_value=mock_response,
    ):

        tool = MapsTool()

        result = tool.route_from_coordinates(
            origin=origin,
            destination=destination,
        )

        assert result.distance_km == 150.5

        assert (
            result.duration_minutes
            == 180
        )

        assert (
            result.distance_text
            == "150.5 km"
        )

        assert (
            result.duration_text
            == "3 hours"
        )


def test_route_failure():

    origin = Location(
        name="Chennai",
        latitude=13.0827,
        longitude=80.2707,
    )

    destination = Location(
        name="Pondicherry",
        latitude=11.9416,
        longitude=79.8083,
    )

    mock_response = MagicMock()

    mock_response.json.return_value = {
        "code": "NoRoute",
        "routes": [],
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "tools.maps_tool.requests.get",
        return_value=mock_response,
    ):

        tool = MapsTool()

        with pytest.raises(ValueError):

            tool.route_from_coordinates(
                origin=origin,
                destination=destination,
            )


def test_format_distance():

    assert (
        MapsTool._format_distance(150.567)
        == "150.6 km"
    )


def test_format_duration_minutes():

    assert (
        MapsTool._format_duration(45)
        == "45 minutes"
    )


def test_format_duration_hours():

    assert (
        MapsTool._format_duration(120)
        == "2 hours"
    )


def test_format_duration_hours_minutes():

    assert (
        MapsTool._format_duration(185)
        == "3 hours 5 minutes"
    )


def test_format_route():

    origin = Location(
        name="Chennai",
        latitude=13.0827,
        longitude=80.2707,
    )

    destination = Location(
        name="Pondicherry",
        latitude=11.9416,
        longitude=79.8083,
    )

    mock_response = MagicMock()

    mock_response.json.return_value = {
        "code": "Ok",
        "routes": [
            {
                "distance": 150500,
                "duration": 10800,
            }
        ],
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "tools.maps_tool.requests.get",
        return_value=mock_response,
    ):

        tool = MapsTool()

        result = tool.route_from_coordinates(
            origin=origin,
            destination=destination,
        )

        summary = tool.format_route(
            result
        )

        assert "TRAVEL ROUTE" in summary

        assert "Chennai" in summary

        assert "Pondicherry" in summary

        assert "150.5 km" in summary

        assert "3 hours" in summary