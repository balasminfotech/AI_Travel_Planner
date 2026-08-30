from datetime import date

from models.expense import ExpenseBreakdown, ExpenseEstimate
from models.hotel import HotelRecommendations, HotelSuggestion
from models.itinerary import Activity, DailyItinerary, Itinerary
from models.maps import Location, RouteResult
from models.master_travel_plan import MasterTravelPlan
from models.packing import PackingChecklist, PackingItem
from models.restaurant import (
    RestaurantRecommendations,
    RestaurantSuggestion,
)
from models.travel_request import TravelRequest
from models.weather import WeatherDay, WeatherForecast

from utils.json_exporter import generate_json_export
from utils.markdown_generator import generate_markdown_report
from utils.pdf_generator import generate_pdf_report


def build_sample_plan():
    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=1,
        start_date=date(2026, 8, 30),
    )

    itinerary = Itinerary(
        days=[
            DailyItinerary(
                day=1,
                date="2026-08-30",
                theme="Goa Highlights",
                activities=[
                    Activity(
                        time="09:00 AM",
                        title="Fort Visit",
                        description="Explore a historic fort.",
                        location="Fort Aguada",
                        estimated_cost=100,
                    )
                ],
                estimated_daily_cost=100,
            )
        ]
    )

    hotels = HotelRecommendations(
        hotels=[
            HotelSuggestion(
                name="Sample Hotel",
                location="Goa",
                price_per_night=2500,
                total_stay_cost=2500,
                rating=4.5,
                category="Budget",
                description="A sample hotel.",
            )
        ]
    )

    restaurants = RestaurantRecommendations(
        restaurants=[
            RestaurantSuggestion(
                name="Sample Restaurant",
                location="Goa",
                cuisine="Goan",
                price_level="$$",
                average_cost_per_person=500,
                rating=4.4,
                best_for="Local food",
                description="A sample restaurant.",
            )
        ]
    )

    weather = WeatherForecast(
        location="Goa",
        latitude=15.49,
        longitude=73.82,
        timezone="Asia/Kolkata",
        days=[
            WeatherDay(
                date="2026-08-30",
                weather_code=1,
                temperature_max=31,
                temperature_min=25,
                precipitation_probability=20,
                precipitation_sum=1.0,
            )
        ],
    )

    expenses = ExpenseEstimate(
        currency="INR",
        budget=30000,
        breakdown=ExpenseBreakdown(
            hotel_cost=2500,
            food_cost=1500,
            transportation_cost=1000,
            activities_cost=100,
            miscellaneous_cost=500,
        ),
        total_cost=5600,
        remaining_budget=24400,
        budget_status="Within Budget",
        budget_utilization_percentage=18.67,
    )

    packing = PackingChecklist(
        destination="Goa",
        days=1,
        items=[
            PackingItem(
                item="T-shirt",
                category="Clothing",
                quantity=2,
                reason="Warm weather",
            )
        ],
    )

    route = RouteResult(
        origin=Location(
            name="Fort Aguada",
            latitude=15.492,
            longitude=73.773,
        ),
        destination=Location(
            name="Panaji",
            latitude=15.4909,
            longitude=73.8278,
        ),
        distance_km=11.7,
        duration_minutes=14,
        distance_text="11.7 km",
        duration_text="14 minutes",
    )

    plan = MasterTravelPlan(
        destination="Goa",
        days=1,
        budget=30000,
        itinerary=itinerary,
        hotels=hotels,
        restaurants=restaurants,
        weather=weather,
        expenses=expenses,
        packing=packing,
        routes=[route],
    )

    return request, plan


def test_markdown_export():
    request, plan = build_sample_plan()

    result = generate_markdown_report(plan, request)

    assert "# AI Travel Planner Report" in result
    assert "Goa" in result
    assert "Fort Aguada" in result
    assert "Sample Hotel" in result


def test_json_export():
    request, plan = build_sample_plan()

    result = generate_json_export(plan, request)

    assert '"destination": "Goa"' in result
    assert '"travel_request"' in result
    assert '"travel_plan"' in result


def test_pdf_export():
    request, plan = build_sample_plan()

    result = generate_pdf_report(plan, request)

    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")
    assert len(result) > 1000
