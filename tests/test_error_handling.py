from unittest.mock import MagicMock, patch

from agents.master_travel_agent import MasterTravelPlannerAgent
from models.travel_request import TravelRequest
from utils.error_handler import friendly_error_message


def _build_agent():
    return MasterTravelPlannerAgent(
        planning_agent=MagicMock(),
        itinerary_agent=MagicMock(),
        hotel_agent=MagicMock(),
        restaurant_agent=MagicMock(),
        weather_tool=MagicMock(),
        expense_tool=MagicMock(),
        packing_agent=MagicMock(),
        maps_tool=MagicMock(),
    )


def test_friendly_rate_limit_message():
    result = friendly_error_message(
        "Gemini",
        RuntimeError("429 RESOURCE_EXHAUSTED quota"),
    )

    assert "rate-limited" in result
    assert "quota" in result


def test_weather_failure_does_not_break_plan():
    agent = _build_agent()

    itinerary = MagicMock()
    itinerary.days = []

    hotels = MagicMock()
    hotels.hotels = []

    restaurants = MagicMock()

    expense = MagicMock()
    packing = MagicMock()

    agent.itinerary_agent.create_itinerary.return_value = itinerary
    agent.hotel_agent.recommend_hotels.return_value = hotels
    agent.restaurant_agent.recommend_restaurants.return_value = (
        restaurants
    )
    agent.weather_tool.get_forecast.side_effect = RuntimeError(
        "503 service unavailable"
    )
    agent.expense_tool.calculate.return_value = expense
    agent.packing_agent.create_checklist.return_value = packing

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=2,
        start_date="2026-08-31",
    )

    with patch(
        "agents.master_travel_agent.MasterTravelPlan"
    ) as plan_model:
        agent.create_travel_plan(request)

    kwargs = plan_model.call_args.kwargs

    assert kwargs["weather"] is None
    assert kwargs["expenses"] is expense
    assert kwargs["packing"] is packing
    assert kwargs["generation_warnings"]
    assert "Weather service" in kwargs["generation_warnings"][0]


def test_route_failure_is_partial():
    agent = _build_agent()

    activity_1 = MagicMock()
    activity_1.location = "Old Goa"

    activity_2 = MagicMock()
    activity_2.location = "Panaji"

    day = MagicMock()
    day.activities = [activity_1, activity_2]

    itinerary = MagicMock()
    itinerary.days = [day]

    hotels = MagicMock()
    hotels.hotels = []

    agent.itinerary_agent.create_itinerary.return_value = itinerary
    agent.hotel_agent.recommend_hotels.return_value = hotels
    agent.restaurant_agent.recommend_restaurants.return_value = (
        MagicMock()
    )
    agent.weather_tool.get_forecast.return_value = MagicMock()
    agent.expense_tool.calculate.return_value = MagicMock()
    agent.packing_agent.create_checklist.return_value = MagicMock()
    agent.maps_tool.route.side_effect = RuntimeError(
        "location not found"
    )

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=1,
        start_date="2026-08-31",
    )

    with patch(
        "agents.master_travel_agent.MasterTravelPlan"
    ) as plan_model:
        agent.create_travel_plan(request)

    kwargs = plan_model.call_args.kwargs

    assert kwargs["routes"] == []
    assert any(
        "Maps service" in warning
        for warning in kwargs["generation_warnings"]
    )
