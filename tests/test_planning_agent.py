from unittest.mock import MagicMock, patch

from agents.planning_agent import PlanningAgent
from models.travel_request import TravelRequest


def test_planning_agent_initialization():

    with patch(
        "agents.planning_agent.genai.Client"
    ) as mock_client:

        agent = PlanningAgent()

        mock_client.assert_called_once()

        assert agent.model_name == "gemini-flash-lite-latest"
        assert agent.temperature == 0.3


def test_create_plan():

    mock_response = MagicMock()

    mock_response.text = """
    {
        "destination": "Goa",
        "days": 3,
        "budget": 30000,
        "currency": "INR",
        "tasks": [
            {
                "name": "itinerary",
                "description": "Create a day-by-day itinerary",
                "priority": 10
            },
            {
                "name": "hotels",
                "description": "Find suitable hotels",
                "priority": 9
            },
            {
                "name": "restaurants",
                "description": "Find restaurants",
                "priority": 8
            },
            {
                "name": "weather",
                "description": "Check weather forecast",
                "priority": 7
            },
            {
                "name": "expenses",
                "description": "Estimate trip expenses",
                "priority": 8
            },
            {
                "name": "packing",
                "description": "Create packing checklist",
                "priority": 6
            },
            {
                "name": "maps",
                "description": "Prepare useful map locations",
                "priority": 5
            }
        ]
    }
    """

    with patch(
        "agents.planning_agent.genai.Client"
    ) as mock_client:

        (
            mock_client
            .return_value
            .models
            .generate_content
            .return_value
        ) = mock_response

        agent = PlanningAgent()

        request = TravelRequest(
            destination="Goa",
            budget=30000,
            days=3,
            start_date="2026-08-26",
        )

        result = agent.create_plan(request)

        assert result.destination == "Goa"
        assert result.days == 3
        assert result.budget == 30000

        assert len(result.tasks) == 7

        assert result.tasks[0].name == "itinerary"
        assert result.tasks[0].priority == 10

        (
            mock_client
            .return_value
            .models
            .generate_content
            .assert_called_once()
        )