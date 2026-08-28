from agents.hotel_agent import HotelAgent
from models.travel_request import TravelRequest


def test_real_hotel_agent():

    agent = HotelAgent()

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    result = agent.recommend_hotels(request)

    print("\n")
    print("=" * 80)
    print("AI HOTEL RECOMMENDATIONS")
    print("=" * 80)

    for index, hotel in enumerate(
        result.hotels,
        start=1,
    ):

        print(f"\nHotel {index}")
        print("-" * 40)

        print(
            f"Name: {hotel.name}"
        )

        print(
            f"Location: {hotel.location}"
        )

        print(
            f"Category: {hotel.category}"
        )

        print(
            f"Rating: {hotel.rating}/5"
        )

        print(
            f"Price per night: "
            f"{hotel.price_per_night} "
            f"{request.currency}"
        )

        print(
            f"Total stay cost: "
            f"{hotel.total_stay_cost} "
            f"{request.currency}"
        )

        print(
            f"Description: "
            f"{hotel.description}"
        )

    print("\n" + "=" * 80)

    assert result is not None
    assert len(result.hotels) > 0

    for hotel in result.hotels:
        assert hotel.name
        assert hotel.location
        assert hotel.price_per_night >= 0
        assert hotel.total_stay_cost >= 0
        assert 0 <= hotel.rating <= 5