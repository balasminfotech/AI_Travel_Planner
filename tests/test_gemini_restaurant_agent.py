from agents.restaurant_agent import RestaurantAgent
from models.travel_request import TravelRequest


def test_real_restaurant_agent():

    agent = RestaurantAgent()

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    result = agent.recommend_restaurants(
        request
    )

    print("\n")
    print("=" * 80)
    print("AI RESTAURANT RECOMMENDATIONS")
    print("=" * 80)

    for index, restaurant in enumerate(
        result.restaurants,
        start=1,
    ):

        print(f"\nRestaurant {index}")
        print("-" * 40)

        print(
            f"Name: {restaurant.name}"
        )

        print(
            f"Location: {restaurant.location}"
        )

        print(
            f"Cuisine: {restaurant.cuisine}"
        )

        print(
            f"Price Level: {restaurant.price_level}"
        )

        print(
            f"Average Cost: "
            f"{restaurant.average_cost_per_person} "
            f"{request.currency}"
        )

        print(
            f"Rating: "
            f"{restaurant.rating}/5"
        )

        print(
            f"Best For: "
            f"{restaurant.best_for}"
        )

        print(
            f"Description: "
            f"{restaurant.description}"
        )

    print("\n" + "=" * 80)

    assert result is not None
    assert len(result.restaurants) > 0

    for restaurant in result.restaurants:

        assert restaurant.name
        assert restaurant.location
        assert restaurant.cuisine

        assert (
            restaurant.average_cost_per_person
            >= 0
        )

        assert (
            0 <= restaurant.rating <= 5
        )