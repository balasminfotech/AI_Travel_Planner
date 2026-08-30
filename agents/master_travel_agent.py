from models.master_travel_plan import MasterTravelPlan
from models.travel_request import TravelRequest
from utils.error_handler import friendly_error_message
from utils.logger import get_logger


logger = get_logger(__name__)


class MasterTravelPlannerAgent:
    """
    Master Travel Planner Agent.

    Orchestrates specialized travel agents and tools while isolating
    partial failures. A failed weather, maps, hotel, restaurant,
    expense, or packing component should not automatically destroy
    the rest of a valid travel plan.
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

        warnings: list[str] = []

        # ============================================
        # 1. Planning
        # ============================================

        try:
            self.planning_agent.create_plan(
                travel_request
            )
        except Exception as exc:
            logger.warning(
                "Planning agent failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Planning agent",
                    exc,
                )
            )

        # ============================================
        # 2. Itinerary
        # ============================================

        itinerary_result = None

        try:
            itinerary_result = (
                self.itinerary_agent.create_itinerary(
                    travel_request=travel_request,
                )
            )
        except Exception as exc:
            logger.warning(
                "Itinerary agent failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Itinerary agent",
                    exc,
                )
            )

        # ============================================
        # 3. Hotels
        # ============================================

        hotel_result = None

        try:
            hotel_result = (
                self.hotel_agent.recommend_hotels(
                    travel_request=travel_request,
                )
            )
        except Exception as exc:
            logger.warning(
                "Hotel agent failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Hotel agent",
                    exc,
                )
            )

        # ============================================
        # 4. Restaurants
        # ============================================

        restaurant_result = None

        try:
            restaurant_result = (
                self.restaurant_agent.recommend_restaurants(
                    travel_request=travel_request,
                )
            )
        except Exception as exc:
            logger.warning(
                "Restaurant agent failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Restaurant agent",
                    exc,
                )
            )

        # ============================================
        # 5. Weather
        # ============================================

        weather_result = None

        try:
            weather_result = (
                self.weather_tool.get_forecast(
                    location=travel_request.destination,
                    forecast_days=travel_request.days,
                    start_date=travel_request.start_date,
                )
            )
        except Exception as exc:
            logger.warning(
                "Weather service failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Weather service",
                    exc,
                )
            )

        # ============================================
        # 6. Expense Calculation
        # ============================================

        expense_result = None

        hotel_cost = 0.0

        if hotel_result is not None:
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

        activities_cost = 0.0

        if itinerary_result is not None:
            activities_cost = sum(
                activity.estimated_cost
                for day in itinerary_result.days
                for activity in day.activities
            )

        miscellaneous_cost = (
            travel_request.budget * 0.05
        )

        try:
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
        except Exception as exc:
            logger.warning(
                "Expense calculator failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Expense calculator",
                    exc,
                )
            )

        # ============================================
        # 7. Packing
        # ============================================

        packing_result = None

        try:
            packing_result = (
                self.packing_agent.create_checklist(
                    travel_request=travel_request,
                    weather_summary=(
                        str(weather_result)
                        if weather_result is not None
                        else "Weather unavailable"
                    ),
                    activities=(
                        str(itinerary_result)
                        if itinerary_result is not None
                        else "Itinerary unavailable"
                    ),
                )
            )
        except Exception as exc:
            logger.warning(
                "Packing agent failed | "
                "error_type=%s | message=%s",
                type(exc).__name__,
                str(exc)[:500],
            )

            warnings.append(
                friendly_error_message(
                    "Packing agent",
                    exc,
                )
            )

        # ============================================
        # 8. Maps / Routes
        # ============================================

        routes = []
        route_failure_count = 0

        if itinerary_result is not None:
            for day_plan in itinerary_result.days:

                activities = day_plan.activities or []
                previous_location = None

                for activity in activities:

                    current_location = (
                        str(activity.location).strip()
                        if activity.location
                        else ""
                    )

                    if not current_location:
                        continue

                    if (
                        previous_location is not None
                        and current_location.lower()
                        != previous_location.lower()
                    ):
                        try:
                            route_result = (
                                self.maps_tool.route(
                                    origin=previous_location,
                                    destination=current_location,
                                )
                            )

                            if route_result is not None:
                                routes.append(route_result)
                            else:
                                route_failure_count += 1

                        except Exception as exc:
                            route_failure_count += 1

                            logger.warning(
                                "Route generation failed | "
                                "origin=%s | destination=%s | "
                                "error_type=%s | message=%s",
                                previous_location,
                                current_location,
                                type(exc).__name__,
                                str(exc)[:500],
                            )

                    previous_location = current_location

        if route_failure_count:
            warnings.append(
                f"Maps service could not generate "
                f"{route_failure_count} itinerary route(s)."
            )

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
            generation_warnings=warnings,
        )
