from unittest.mock import MagicMock

from agents.master_travel_agent import (
    MasterTravelPlannerAgent,
)


def test_master_agent_initialization():

    planning_agent = MagicMock()

    itinerary_agent = MagicMock()

    hotel_agent = MagicMock()

    restaurant_agent = MagicMock()

    weather_tool = MagicMock()

    expense_tool = MagicMock()

    packing_agent = MagicMock()

    maps_tool = MagicMock()

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

    assert (
        agent.planning_agent
        is planning_agent
    )

    assert (
        agent.itinerary_agent
        is itinerary_agent
    )

    assert (
        agent.hotel_agent
        is hotel_agent
    )

    assert (
        agent.restaurant_agent
        is restaurant_agent
    )

    assert (
        agent.weather_tool
        is weather_tool
    )

    assert (
        agent.expense_tool
        is expense_tool
    )

    assert (
        agent.packing_agent
        is packing_agent
    )

    assert (
        agent.maps_tool
        is maps_tool
    )