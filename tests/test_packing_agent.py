from unittest.mock import MagicMock, patch

from agents.packing_agent import PackingAgent
from models.travel_request import TravelRequest


def test_packing_agent_initialization():

    with patch(
        "agents.packing_agent.genai.Client"
    ) as mock_client:

        agent = PackingAgent()

        mock_client.assert_called_once()

        assert (
            agent.model_name
            == "gemini-flash-lite-latest"
        )

        assert agent.temperature == 0.3


def test_create_checklist():

    mock_response = MagicMock()

    mock_response.text = """
    {
        "destination": "Goa",
        "days": 3,
        "items": [
            {
                "item": "T-shirts",
                "category": "Clothing",
                "quantity": 4,
                "reason": "Suitable for warm weather"
            },
            {
                "item": "Shorts",
                "category": "Clothing",
                "quantity": 3,
                "reason": "Useful for warm weather"
            },
            {
                "item": "Sunscreen",
                "category": "Health",
                "quantity": 1,
                "reason": "Protection from strong sunlight"
            },
            {
                "item": "Umbrella",
                "category": "Weather",
                "quantity": 1,
                "reason": "Useful during rain"
            },
            {
                "item": "Phone charger",
                "category": "Electronics",
                "quantity": 1,
                "reason": "Required for charging the phone"
            },
            {
                "item": "Passport",
                "category": "Documents",
                "quantity": 1,
                "reason": "Important travel document"
            }
        ]
    }
    """

    with patch(
        "agents.packing_agent.genai.Client"
    ) as mock_client:

        (
            mock_client
            .return_value
            .models
            .generate_content
            .return_value
        ) = mock_response

        agent = PackingAgent()

        request = TravelRequest(
            destination="Goa",
            budget=30000,
            days=3,
            start_date="2026-08-26",
        )

        result = agent.create_checklist(
            travel_request=request,
            weather_summary=(
                "Warm weather with possible rain"
            ),
            activities=(
                "Beach sightseeing and hiking"
            ),
        )

        assert result is not None

        assert result.destination == "Goa"

        assert result.days == 3

        assert len(result.items) == 6

        first_item = result.items[0]

        assert first_item.item == "T-shirts"

        assert first_item.category == "Clothing"

        assert first_item.quantity == 4

        assert (
            first_item.reason
            == "Suitable for warm weather"
        )

        (
            mock_client
            .return_value
            .models
            .generate_content
            .assert_called_once()
        )


def test_format_checklist():

    with patch(
        "agents.packing_agent.genai.Client"
    ) as mock_client:

        agent = PackingAgent()

        from models.packing import (
            PackingChecklist,
            PackingItem,
        )

        checklist = PackingChecklist(
            destination="Goa",
            days=3,
            items=[
                PackingItem(
                    item="T-shirts",
                    category="Clothing",
                    quantity=4,
                    reason=(
                        "Suitable for warm weather"
                    ),
                ),
                PackingItem(
                    item="Umbrella",
                    category="Weather",
                    quantity=1,
                    reason=(
                        "Useful during rain"
                    ),
                ),
            ],
        )

        summary = agent.format_checklist(
            checklist
        )

        assert (
            "TRAVEL PACKING CHECKLIST"
            in summary
        )

        assert "T-shirts" in summary

        assert "Umbrella" in summary

        assert "Goa" in summary

        assert "4" in summary