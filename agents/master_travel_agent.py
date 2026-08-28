from models.master_travel_plan import MasterTravelPlan
from models.travel_request import TravelRequest


class MasterTravelPlannerAgent:
    """
    Master Travel Planner Agent.

    Orchestrates all specialized travel agents
    and tools to create a complete travel plan.
    """

    def __init__(
        self,
        planning_agent,
        itinerary_agent,
        hotel_agent,
        restaurant_agent,
        weather_tool,
        expense_tool,
        packing_agent,
        maps_tool,
    ):
        self.planning_agent = planning_agent
        self.itinerary_agent = itinerary_agent
        self.hotel_agent = hotel_agent
        self.restaurant_agent = restaurant_agent
        self.weather_tool = weather_tool
        self.expense_tool = expense_tool
        self.packing_agent = packing_agent
        self.maps_tool = maps_tool

    def create_travel_plan(
        self,
        travel_request: TravelRequest,
    ) -> MasterTravelPlan:

        # ============================================
        # 1. Planning
        # ============================================

        planning_result = (
            self.planning_agent.create_plan(
                travel_request
            )
        )

        # ============================================
        # 2. Itinerary
        # ============================================

        itinerary_result = (
            self.itinerary_agent.create_itinerary(
                travel_request=travel_request,
            )
        )

        # ============================================
        # 3. Hotels
        # ============================================

        hotel_result = (
            self.hotel_agent.recommend_hotels(
                travel_request=travel_request,
            )
        )

        # ============================================
        # 4. Restaurants
        # ============================================

        restaurant_result = (
            self.restaurant_agent.recommend_restaurants(
                travel_request=travel_request,
            )
        )

        # ============================================
        # 5. Weather
        # ============================================

        weather_result = (
            self.weather_tool.get_forecast(
                location=travel_request.destination,
                forecast_days=travel_request.days,
            )
        )

        # ============================================
        # 6. Expense Calculation
        # ============================================

        hotel_cost = sum(
            hotel.total_stay_cost
            for hotel in hotel_result.hotels
        )

        food_cost = (
            travel_request.days
            * 2
            * 500
        )

        transportation_cost = (
            travel_request.days
            * 500
        )

        activities_cost = sum(
            activity.estimated_cost
            for day in itinerary_result.days
            for activity in day.activities
        )

        miscellaneous_cost = (
            travel_request.budget * 0.05
        )

        expense_result = (
            self.expense_tool.calculate(
                budget=travel_request.budget,
                currency=travel_request.currency,
                hotel_cost=hotel_cost,
                food_cost=food_cost,
                transportation_cost=transportation_cost,
                activities_cost=activities_cost,
                miscellaneous_cost=miscellaneous_cost,
            )
        )

        # ============================================
        # 7. Packing
        # ============================================

        packing_result = (
            self.packing_agent.create_checklist(
                travel_request=travel_request,
                weather_summary=str(
                    weather_result
                ),
                activities=str(
                    itinerary_result
                ),
            )
        )

        # ============================================
        # 8. Maps
        # ============================================
        #
        # Routes will be generated when meaningful
        # locations are available.
        #
        # We do not calculate:
        #
        # Goa -> Goa
        #
        # because that is not useful.
        # ============================================

        routes = []

        # ============================================
        # 9. Final Master Travel Plan
        # ============================================

        return MasterTravelPlan(
            destination=travel_request.destination,
            days=travel_request.days,
            budget=travel_request.budget,
            itinerary=itinerary_result,
            hotels=hotel_result,
            restaurants=restaurant_result,
            weather=weather_result,
            expenses=expense_result,
            packing=packing_result,
            routes=routes,
        )