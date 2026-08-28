from models.travel_request import TravelRequest

from models.itinerary import (
    Activity,
    DailyItinerary,
    Itinerary,
)

from models.hotel import (
    HotelSuggestion,
    HotelRecommendations,
)

from models.restaurant import (
    RestaurantSuggestion,
    RestaurantRecommendations,
)

from models.weather import (
    WeatherDay,
    WeatherForecast,
)

from models.expense import (
    ExpenseEstimate,
    ExpenseBreakdown,
)

from models.packing import (
    PackingItem,
    PackingChecklist,
)


# ============================================================
# Travel Request
# ============================================================

def test_travel_request():

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=4,
        currency="INR",
        start_date="2026-08-26",
    )

    assert request.destination == "Goa"
    assert request.budget == 30000
    assert request.days == 4
    assert request.currency == "INR"
    assert str(request.start_date) == "2026-08-26"


# ============================================================
# Activity
# ============================================================

def test_activity():

    activity = Activity(
        time="10:00 AM",
        title="Visit Beach",
        description="Relax at the beach",
        location="Baga Beach, Goa",
        estimated_cost=500,
    )

    assert activity.title == "Visit Beach"
    assert activity.location == "Baga Beach, Goa"
    assert activity.estimated_cost == 500


# ============================================================
# Itinerary
# ============================================================

def test_itinerary():

    activity = Activity(
        time="10:00 AM",
        title="Visit Beach",
        description="Relax at the beach",
        location="Baga Beach, Goa",
        estimated_cost=500,
    )

    day = DailyItinerary(
        day=1,
        date="2026-08-26",
        theme="Beach Exploration",
        activities=[activity],
        estimated_daily_cost=500,
    )

    itinerary = Itinerary(
        days=[day]
    )

    assert len(itinerary.days) == 1
    assert itinerary.days[0].day == 1
    assert itinerary.days[0].theme == "Beach Exploration"
    assert itinerary.days[0].activities[0].title == "Visit Beach"


# ============================================================
# Hotel
# ============================================================

def test_hotel():

    hotel = HotelSuggestion(
        name="Beach Resort",
        location="North Goa",
        price_per_night=3000,
        total_stay_cost=9000,
        rating=4.2,
        category="Mid-range",
        description="Comfortable beach resort",
    )

    hotels = HotelRecommendations(
        hotels=[hotel]
    )

    assert len(hotels.hotels) == 1
    assert hotels.hotels[0].name == "Beach Resort"
    assert hotels.hotels[0].rating == 4.2
    assert hotels.hotels[0].total_stay_cost == 9000
    assert hotels.hotels[0].category == "Mid-range"


# ============================================================
# Restaurant
# ============================================================

def test_restaurant():

    restaurant = RestaurantSuggestion(
        name="Sea View Restaurant",
        location="Panaji",
        cuisine="Indian",
        price_level="$$",
        average_cost_per_person=600,
        rating=4.3,
        best_for="Local cuisine",
        description="Popular local restaurant",
    )

    restaurants = RestaurantRecommendations(
        restaurants=[restaurant]
    )

    assert len(restaurants.restaurants) == 1
    assert restaurants.restaurants[0].name == (
        "Sea View Restaurant"
    )
    assert restaurants.restaurants[0].rating == 4.3
    assert restaurants.restaurants[0].average_cost_per_person == 600


# ============================================================
# Weather
# ============================================================

def test_weather():

    weather_day = WeatherDay(
        date="2026-08-26",
        weather_code=80,
        temperature_max=30,
        temperature_min=24,
        precipitation_probability=60,
        precipitation_sum=5.0,
    )

    forecast = WeatherForecast(
        location="Goa",
        latitude=15.4909,
        longitude=73.8278,
        timezone="Asia/Kolkata",
        days=[weather_day],
    )

    assert forecast.location == "Goa"
    assert forecast.latitude == 15.4909
    assert forecast.longitude == 73.8278
    assert forecast.timezone == "Asia/Kolkata"
    assert len(forecast.days) == 1
    assert forecast.days[0].weather_code == 80
    assert forecast.days[0].temperature_max == 30


# ============================================================
# Expense
# ============================================================
# ============================================================
# Expense
# ============================================================

def test_expense():

    breakdown = ExpenseBreakdown(
        hotel_cost=10000,
        food_cost=5000,
        transportation_cost=3000,
        activities_cost=4000,
        miscellaneous_cost=1000,
    )

    expense = ExpenseEstimate(
        currency="INR",
        budget=30000,
        breakdown=breakdown,
        total_cost=23000,
        remaining_budget=7000,
        budget_status="Within Budget",
        budget_utilization_percentage=76.67,
    )

    assert expense.currency == "INR"
    assert expense.budget == 30000

    assert expense.breakdown.hotel_cost == 10000
    assert expense.breakdown.food_cost == 5000
    assert expense.breakdown.transportation_cost == 3000
    assert expense.breakdown.activities_cost == 4000
    assert expense.breakdown.miscellaneous_cost == 1000

    assert expense.total_cost == 23000
    assert expense.remaining_budget == 7000
    assert expense.budget_status == "Within Budget"
    assert expense.budget_utilization_percentage == 76.67

# ============================================================
# Packing
# ============================================================

def test_packing():

    item1 = PackingItem(
        item="Passport",
        category="Documents",
        quantity=1,
        reason="Important travel document",
    )

    item2 = PackingItem(
        item="Umbrella",
        category="Weather",
        quantity=1,
        reason="Useful during rain",
    )

    packing = PackingChecklist(
        destination="Goa",
        days=3,
        items=[
            item1,
            item2,
        ],
    )

    assert packing.destination == "Goa"
    assert packing.days == 3
    assert len(packing.items) == 2
    assert packing.items[0].item == "Passport"
    assert packing.items[1].item == "Umbrella"