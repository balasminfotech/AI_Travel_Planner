import pytest

from pydantic import ValidationError

from models.maps import (
    Location,
    RouteResult,
)


def test_valid_location():

    location = Location(
        name="Chennai",
        latitude=13.0827,
        longitude=80.2707,
    )

    assert location.name == "Chennai"

    assert location.latitude == 13.0827

    assert location.longitude == 80.2707


def test_valid_route_result():

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

    route = RouteResult(
        origin=origin,
        destination=destination,
        distance_km=150.5,
        duration_minutes=180,
        distance_text="150.5 km",
        duration_text="3 hours",
    )

    assert route.origin.name == "Chennai"

    assert route.destination.name == "Pondicherry"

    assert route.distance_km == 150.5

    assert route.duration_minutes == 180


def test_negative_distance():

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

    with pytest.raises(ValidationError):

        RouteResult(
            origin=origin,
            destination=destination,
            distance_km=-10,
            duration_minutes=180,
            distance_text="10 km",
            duration_text="3 hours",
        )


def test_negative_duration():

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

    with pytest.raises(ValidationError):

        RouteResult(
            origin=origin,
            destination=destination,
            distance_km=150,
            duration_minutes=-20,
            distance_text="150 km",
            duration_text="Invalid",
        )