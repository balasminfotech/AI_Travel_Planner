from agents.itinerary_agent import ItineraryAgent
from models.travel_request import TravelRequest


def test_real_itinerary_agent():

    agent = ItineraryAgent()

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    result = agent.create_itinerary(request)

    print("\n")
    print("=" * 80)
    print("AI GENERATED ITINERARY")
    print("=" * 80)

    for day in result.days:

        print(
            f"\nDay {day.day}: "
            f"{day.theme}"
        )

        print(
            f"Date: {day.date}"
        )

        for activity in day.activities:

            print(
                f"  {activity.time} | "
                f"{activity.title}"
            )

            print(
                f"    Location: "
                f"{activity.location}"
            )

            print(
                f"    Description: "
                f"{activity.description}"
            )

            print(
                f"    Cost: "
                f"{activity.estimated_cost}"
            )

        print(
            f"  Daily Cost: "
            f"{day.estimated_daily_cost}"
        )

    print("\n" + "=" * 80)

    assert result is not None
    assert len(result.days) == request.days