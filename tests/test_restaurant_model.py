import pytest

from pydantic import ValidationError

from models.restaurant import RestaurantSuggestion


def test_valid_restaurant():

    restaurant = RestaurantSuggestion(
        name="Test Restaurant",
        location="Goa",
        cuisine="Indian",
        price_level="$$",
        average_cost_per_person=500,
        rating=4.2,
        best_for="Local food",
        description="Good restaurant",
    )

    assert restaurant.name == "Test Restaurant"
    assert restaurant.rating == 4.2
    assert (
        restaurant.average_cost_per_person
        == 500
    )


def test_restaurant_rating_validation():

    with pytest.raises(ValidationError):

        RestaurantSuggestion(
            name="Test Restaurant",
            location="Goa",
            cuisine="Indian",
            price_level="$$",
            average_cost_per_person=500,
            rating=6.0,
            best_for="Local food",
            description="Good restaurant",
        )


def test_negative_food_cost_validation():

    with pytest.raises(ValidationError):

        RestaurantSuggestion(
            name="Test Restaurant",
            location="Goa",
            cuisine="Indian",
            price_level="$$",
            average_cost_per_person=-100,
            rating=4.0,
            best_for="Local food",
            description="Good restaurant",
        )