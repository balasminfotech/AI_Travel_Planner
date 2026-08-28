from unittest.mock import MagicMock, patch

from agents.hotel_agent import HotelAgent
from models.travel_request import TravelRequest


def test_hotel_agent_initialization():

    with patch(
        "agents.hotel_agent.genai.Client"
    ) as mock_client:

        agent = HotelAgent()

        mock_client.assert_called_once()

        assert agent.model_name == "gemini-flash-lite-latest"
        assert agent.temperature == 0.3


def test_recommend_hotels():

    mock_response = MagicMock()

    mock_response.text = """
    {
        "hotels": [
            {
                "name": "Goa Beach Resort",
                "location": "Calangute",
                "price_per_night": 3000,
                "total_stay_cost": 9000,
                "rating": 4.2,
                "category": "Mid-range",
                "description": "Comfortable resort close to the beach"
            },
            {
                "name": "Budget Stay Goa",
                "location": "Candolim",
                "price_per_night": 1800,
                "total_stay_cost": 5400,
                "rating": 3.9,
                "category": "Budget",
                "description": "Affordable accommodation for budget travelers"
            },
            {
                "name": "Premium Goa Hotel",
                "location": "Panaji",
                "price_per_night": 5000,
                "total_stay_cost": 15000,
                "rating": 4.6,
                "category": "Luxury",
                "description": "Premium hotel with modern facilities"
            }
        ]
    }
    """

    with patch(
        "agents.hotel_agent.genai.Client"
    ) as mock_client:

        (
            mock_client
            .return_value
            .models
            .generate_content
            .return_value
        ) = mock_response

        agent = HotelAgent()

        request = TravelRequest(
            destination="Goa",
            budget=30000,
            days=3,
            start_date="2026-08-26",
        )

        result = agent.recommend_hotels(request)

        assert result is not None

        assert len(result.hotels) == 3

        assert result.hotels[0].name == "Goa Beach Resort"

        assert (
            result.hotels[0].location
            == "Calangute"
        )

        assert (
            result.hotels[0].price_per_night
            == 3000
        )

        assert (
            result.hotels[0].total_stay_cost
            == 9000
        )

        assert result.hotels[0].rating == 4.2

        assert (
            result.hotels[0].category
            == "Mid-range"
        )

        (
            mock_client
            .return_value
            .models
            .generate_content
            .assert_called_once()
        )