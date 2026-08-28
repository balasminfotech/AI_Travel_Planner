from unittest.mock import MagicMock, patch

from agents.travel_agent import TravelPlannerAgent
from models.travel_request import TravelRequest


def test_travel_agent_initialization():
    with patch("agents.travel_agent.genai.Client") as mock_client:
        agent = TravelPlannerAgent()

        mock_client.assert_called_once()

        assert agent.model_name == "gemini-flash-lite-latest"
        assert agent.temperature == 0.3


def test_generate_plan():
    mock_response = MagicMock()

    mock_response.text = """
    Goa 3-Day Travel Plan

    Day 1:
    Visit Baga Beach and Fort Aguada.

    Day 2:
    Visit Panaji and Old Goa.

    Day 3:
    Explore South Goa.

    Estimated Budget:
    INR 25,000
    """

    with patch("agents.travel_agent.genai.Client") as mock_client:

        mock_client.return_value.models.generate_content.return_value = (
            mock_response
        )

        agent = TravelPlannerAgent()

        request = TravelRequest(
            destination="Goa",
            budget=30000,
            days=3,
        )

        result = agent.generate_plan(request)

        assert result is not None
        assert "Goa" in result
        assert "Travel Plan" in result

        mock_client.return_value.models.generate_content.assert_called_once()