from agents.packing_agent import PackingAgent
from models.travel_request import TravelRequest


def test_real_packing_agent():

    agent = PackingAgent()

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    weather_summary = """
    Goa weather:
    Day 1: 31°C maximum, 25°C minimum,
    20% rain probability.

    Day 2: 30°C maximum, 24°C minimum,
    60% rain probability.

    Day 3: 32°C maximum, 25°C minimum,
    10% rain probability.
    """

    activities = """
    Beach sightseeing,
    local sightseeing,
    evening outdoor activities.
    """

    result = agent.create_checklist(
        travel_request=request,
        weather_summary=weather_summary,
        activities=activities,
    )

    print("\n")
    print("=" * 80)
    print("AI PACKING CHECKLIST")
    print("=" * 80)

    print(
        f"Destination: "
        f"{result.destination}"
    )

    print(
        f"Days: {result.days}"
    )

    for index, item in enumerate(
        result.items,
        start=1,
    ):

        print(
            f"\n{index}. {item.item}"
        )

        print(
            f"   Category: "
            f"{item.category}"
        )

        print(
            f"   Quantity: "
            f"{item.quantity}"
        )

        print(
            f"   Reason: "
            f"{item.reason}"
        )

    print("\n" + "=" * 80)

    assert result is not None

    assert result.destination == "Goa"

    assert result.days == 3

    assert len(result.items) > 0

    for item in result.items:

        assert item.item

        assert item.category

        assert item.quantity >= 1

        assert item.reason