import pytest

from pydantic import ValidationError

from models.hotel import HotelSuggestion


def test_hotel_rating_validation():

    with pytest.raises(ValidationError):

        HotelSuggestion(
            name="Test Hotel",
            location="Goa",
            price_per_night=3000,
            total_stay_cost=9000,
            rating=6.5,
            category="Luxury",
            description="Test hotel",
        )


def test_hotel_negative_price_validation():

    with pytest.raises(ValidationError):

        HotelSuggestion(
            name="Test Hotel",
            location="Goa",
            price_per_night=-1000,
            total_stay_cost=9000,
            rating=4.0,
            category="Budget",
            description="Test hotel",
        )


def test_valid_hotel():

    hotel = HotelSuggestion(
        name="Test Hotel",
        location="Goa",
        price_per_night=3000,
        total_stay_cost=9000,
        rating=4.2,
        category="Mid-range",
        description="Comfortable hotel",
    )

    assert hotel.name == "Test Hotel"
    assert hotel.rating == 4.2