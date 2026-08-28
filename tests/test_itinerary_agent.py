from unittest.mock import MagicMock, patch

from agents.itinerary_agent import ItineraryAgent
from models.travel_request import TravelRequest


def test_itinerary_agent_initialization():

    with patch(
        "agents.itinerary_agent.genai.Client"
    ) as mock_client:

        agent = ItineraryAgent()

        mock_client.assert_called_once()

        assert agent.model_name == "gemini-flash-lite-latest"
        assert agent.temperature == 0.3


def test_create_itinerary():

    mock_response = MagicMock()

    mock_response.text = """
    {
        "days": [
            {
                "day": 1,
                "date": "2026-09-01",
                "theme": "North Goa Exploration",
                "activities": [
                    {
                        "time": "09:00 AM",
                        "title": "Breakfast",
                        "description": "Have breakfast at a local restaurant",
                        "location": "Calangute",
                        "estimated_cost": 300
                    },
                    {
                        "time": "11:00 AM",
                        "title": "Baga Beach",
                        "description": "Relax and explore Baga Beach",
                        "location": "Baga Beach",
                        "estimated_cost": 0
                    },
                    {
                        "time": "04:00 PM",
                        "title": "Fort Aguada",
                        "description": "Explore the historic fort",
                        "location": "Fort Aguada",
                        "estimated_cost": 50
                    }
                ],
                "estimated_daily_cost": 350
            },
            {
                "day": 2,
                "date": "2026-09-02",
                "theme": "Old Goa and Panaji",
                "activities": [
                    {
                        "time": "09:00 AM",
                        "title": "Basilica of Bom Jesus",
                        "description": "Visit the historic basilica",
                        "location": "Old Goa",
                        "estimated_cost": 0
                    }
                ],
                "estimated_daily_cost": 500
            },
            {
                "day": 3,
                "date": "2026-09-03",
                "theme": "South Goa",
                "activities": [
                    {
                        "time": "09:00 AM",
                        "title": "Palolem Beach",
                        "description": "Relax at Palolem Beach",
                        "location": "Palolem",
                        "estimated_cost": 0
                    }
                ],
                "estimated_daily_cost": 800
            }
        ]
    }
    """

    with patch(
        "agents.itinerary_agent.genai.Client"
    ) as mock_client:

        (
            mock_client
            .return_value
            .models
            .generate_content
            .return_value
        ) = mock_response

        agent = ItineraryAgent()

        request = TravelRequest(
            destination="Goa",
            budget=30000,
            days=3,
            start_date="2026-09-01",
        )

        result = agent.create_itinerary(request)

        assert result is not None

        assert len(result.days) == 3

        assert result.days[0].day == 1
        assert result.days[0].theme == "North Goa Exploration"

        assert len(result.days[0].activities) == 3

        assert (
            result.days[0]
            .activities[0]
            .title
            == "Breakfast"
        )

        assert (
            result.days[0]
            .activities[1]
            .location
            == "Baga Beach"
        )

        assert (
            result.days[0]
            .estimated_daily_cost
            == 350
        )

        (
            mock_client
            .return_value
            .models
            .generate_content
            .assert_called_once()
        )