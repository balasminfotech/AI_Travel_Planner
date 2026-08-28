from agents.travel_agent import TravelPlannerAgent
from models.travel_request import TravelRequest


def test_real_gemini_travel_agent():

    agent = TravelPlannerAgent()

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    result = agent.generate_plan(request)

    print("\n" + "=" * 70)
    print("AI TRAVEL PLAN")
    print("=" * 70)
    print(result)
    print("=" * 70)

    assert result is not None
    assert len(result) > 0