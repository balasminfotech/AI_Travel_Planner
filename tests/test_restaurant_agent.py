from unittest.mock import MagicMock, patch

from agents.restaurant_agent import RestaurantAgent
from models.travel_request import TravelRequest


def test_restaurant_agent_initialization():

    with patch(
        "agents.restaurant_agent.genai.Client"
    ) as mock_client:

        agent = RestaurantAgent()

        mock_client.assert_called_once()

        assert agent.model_name == "gemini-flash-lite-latest"
        assert agent.temperature == 0.3


def test_recommend_restaurants():

    mock_response = MagicMock()

    mock_response.text = """
    {
        "restaurants": [
            {
                "name": "Goa Spice Kitchen",
                "location": "Panaji",
                "cuisine": "Goan",
                "price_level": "$$",
                "average_cost_per_person": 600,
                "rating": 4.4,
                "best_for": "Goan local cuisine",
                "description": "Popular restaurant serving traditional Goan dishes"
            },
            {
                "name": "Beach View Cafe",
                "location": "Baga",
                "cuisine": "Multi-cuisine",
                "price_level": "$$",
                "average_cost_per_person": 500,
                "rating": 4.2,
                "best_for": "Beachside dining",
                "description": "Casual restaurant near the beach"
            },
            {
                "name": "Budget Bites",
                "location": "Calangute",
                "cuisine": "Indian",
                "price_level": "$",
                "average_cost_per_person": 250,
                "rating": 4.0,
                "best_for": "Budget meals",
                "description": "Affordable local food"
            },
            {
                "name": "Seafood Paradise",
                "location": "Candolim",
                "cuisine": "Seafood",
                "price_level": "$$$",
                "average_cost_per_person": 1000,
                "rating": 4.5,
                "best_for": "Fresh seafood",
                "description": "Specializes in fresh seafood dishes"
            },
            {
                "name": "Sunset Restaurant",
                "location": "Anjuna",
                "cuisine": "Indian",
                "price_level": "$$",
                "average_cost_per_person": 550,
                "rating": 4.1,
                "best_for": "Sunset dinner",
                "description": "Relaxed restaurant with sunset views"
            }
        ]
    }
    """

    with patch(
        "agents.restaurant_agent.genai.Client"
    ) as mock_client:

        (
            mock_client
            .return_value
            .models
            .generate_content
            .return_value
        ) = mock_response

        agent = RestaurantAgent()

        request = TravelRequest(
            destination="Goa",
            budget=30000,
            days=3,
            start_date="2026-08-26",
        )

        result = agent.recommend_restaurants(
            request
        )

        assert result is not None

        assert len(result.restaurants) == 5

        first_restaurant = result.restaurants[0]

        assert (
            first_restaurant.name
            == "Goa Spice Kitchen"
        )

        assert (
            first_restaurant.location
            == "Panaji"
        )

        assert (
            first_restaurant.cuisine
            == "Goan"
        )

        assert (
            first_restaurant.average_cost_per_person
            == 600
        )

        assert (
            first_restaurant.rating
            == 4.4
        )

        assert (
            first_restaurant.best_for
            == "Goan local cuisine"
        )

        (
            mock_client
            .return_value
            .models
            .generate_content
            .assert_called_once()
        )