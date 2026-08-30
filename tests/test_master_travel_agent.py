from unittest.mock import MagicMock, patch

from agents.master_travel_agent import (
    MasterTravelPlannerAgent,
)

from models.travel_request import TravelRequest


def test_master_travel_agent():
    """
    Test the Master Travel Planner Agent orchestration.

    This test verifies that:

    - Planning Agent is called
    - Itinerary Agent is called
    - Hotel Agent is called
    - Restaurant Agent is called
    - Weather Tool is called
    - Expense Tool is called
    - Packing Agent is called
    - MasterTravelPlan is created

    External APIs and specialized agents are mocked.
    """

    # =================================================
    # Create mock dependencies
    # =================================================

    planning_agent = MagicMock()

    itinerary_agent = MagicMock()

    hotel_agent = MagicMock()

    restaurant_agent = MagicMock()

    weather_tool = MagicMock()

    expense_tool = MagicMock()

    packing_agent = MagicMock()

    maps_tool = MagicMock()

    # =================================================
    # Mock intermediate results
    # =================================================

    planning_result = MagicMock(
        name="planning_result"
    )

    activity_1 = MagicMock()
    activity_1.location = "Fort Aguada"

    activity_2 = MagicMock()
    activity_2.location = "Panaji"

    day_plan = MagicMock()
    day_plan.activities = [
        activity_1,
        activity_2,
    ]

    itinerary_result = MagicMock(
        name="itinerary_result"
    )
    itinerary_result.days = [day_plan]

    hotel_result = MagicMock(
        name="hotel_result"
    )

    restaurant_result = MagicMock(
        name="restaurant_result"
    )

    weather_result = MagicMock(
        name="weather_result"
    )

    expense_result = MagicMock(
        name="expense_result"
    )

    packing_result = MagicMock(
        name="packing_result"
    )

    # =================================================
    # Configure return values
    # =================================================

    planning_agent.create_plan.return_value = (
        planning_result
    )

    itinerary_agent.create_itinerary.return_value = (
        itinerary_result
    )

    hotel_agent.recommend_hotels.return_value = (
        hotel_result
    )

    restaurant_agent.recommend_restaurants.return_value = (
        restaurant_result
    )

    weather_tool.get_forecast.return_value = (
        weather_result
    )

    expense_tool.calculate.return_value = (
        expense_result
    )

    packing_agent.create_checklist.return_value = (
        packing_result
    )

    route_result = MagicMock(
        name="route_result"
    )

    maps_tool.route.return_value = route_result

    # =================================================
    # Create Travel Request
    # =================================================

    travel_request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    # =================================================
    # Mock MasterTravelPlan
    #
    # The purpose of this test is orchestration.
    # Actual Pydantic validation is tested separately.
    # =================================================

    mock_master_plan = MagicMock()

    with patch(
        "agents.master_travel_agent.MasterTravelPlan",
        return_value=mock_master_plan,
    ) as master_plan_mock:

        # =============================================
        # Create Master Agent
        # =============================================

        agent = MasterTravelPlannerAgent(
            planning_agent=planning_agent,
            itinerary_agent=itinerary_agent,
            hotel_agent=hotel_agent,
            restaurant_agent=restaurant_agent,
            weather_tool=weather_tool,
            expense_tool=expense_tool,
            packing_agent=packing_agent,
            maps_tool=maps_tool,
        )

        # =============================================
        # Execute Master Workflow
        # =============================================

        result = agent.create_travel_plan(
            travel_request
        )

    # =================================================
    # Verify final result
    # =================================================

    assert result is mock_master_plan

    # =================================================
    # Verify Planning Agent
    # =================================================

    planning_agent.create_plan.assert_called_once_with(
        travel_request
    )

    # =================================================
    # Verify Itinerary Agent
    # =================================================

    itinerary_agent.create_itinerary.assert_called_once_with(
        travel_request=travel_request,
    )

    # =================================================
    # Verify Hotel Agent
    # =================================================

    hotel_agent.recommend_hotels.assert_called_once_with(
        travel_request=travel_request,
    )

    # =================================================
    # Verify Restaurant Agent
    # =================================================

    restaurant_agent.recommend_restaurants.assert_called_once_with(
        travel_request=travel_request,
    )

    # =================================================
    # Verify Weather Tool
    # =================================================

    weather_tool.get_forecast.assert_called_once_with(
        location=travel_request.destination,
        forecast_days=travel_request.days,
        start_date=travel_request.start_date,
    )

    # =================================================
    # Verify Expense Tool
    # =================================================

    expense_tool.calculate.assert_called_once()

    expense_call = (
        expense_tool.calculate.call_args
    )

    expense_kwargs = expense_call.kwargs

    assert (
        expense_kwargs["budget"]
        == travel_request.budget
    )

    assert (
        expense_kwargs["currency"]
        == travel_request.currency
    )

    # =================================================
    # Verify Packing Agent
    # =================================================

    packing_agent.create_checklist.assert_called_once_with(
        travel_request=travel_request,
        weather_summary=str(weather_result),
        activities=str(itinerary_result),
    )

    # =================================================
    # Verify MasterTravelPlan Creation
    # =================================================

    master_plan_mock.assert_called_once()

    master_plan_kwargs = (
        master_plan_mock.call_args.kwargs
    )

    assert (
        master_plan_kwargs["destination"]
        == travel_request.destination
    )

    assert (
        master_plan_kwargs["days"]
        == travel_request.days
    )

    assert (
        master_plan_kwargs["budget"]
        == travel_request.budget
    )

    assert (
        master_plan_kwargs["itinerary"]
        is itinerary_result
    )

    assert (
        master_plan_kwargs["hotels"]
        is hotel_result
    )

    assert (
        master_plan_kwargs["restaurants"]
        is restaurant_result
    )

    assert (
        master_plan_kwargs["weather"]
        is weather_result
    )

    assert (
        master_plan_kwargs["expenses"]
        is expense_result
    )

    assert (
        master_plan_kwargs["packing"]
        is packing_result
    )

    maps_tool.route.assert_called_once_with(
        origin="Fort Aguada",
        destination="Panaji",
    )

    assert master_plan_kwargs["routes"] == [route_result]
