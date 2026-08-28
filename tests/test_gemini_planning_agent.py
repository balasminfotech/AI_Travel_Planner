from agents.planning_agent import PlanningAgent
from models.travel_request import TravelRequest


def test_real_planning_agent():

    agent = PlanningAgent()

    request = TravelRequest(
        destination="Goa",
        budget=30000,
        days=3,
        start_date="2026-08-26",
    )

    result = agent.create_plan(request)

    print("\n")
    print("=" * 70)
    print("TRAVEL PLANNING STRATEGY")
    print("=" * 70)

    print(f"Destination : {result.destination}")
    print(f"Days        : {result.days}")
    print(f"Budget      : {result.budget}")
    print(f"Currency    : {result.currency}")

    print("\nTasks:")

    for task in result.tasks:
        print(
            f"{task.priority}. "
            f"{task.name} - "
            f"{task.description}"
        )

    print("=" * 70)

    assert result.destination == "Goa"
    assert result.days == 3
    assert result.budget == 30000
    assert len(result.tasks) > 0