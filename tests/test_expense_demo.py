from tools.expense_tool import ExpenseTool


def test_expense_demo():

    tool = ExpenseTool()

    result = tool.calculate(
        budget=50000,
        currency="INR",
        hotel_cost=15000,
        food_cost=7500,
        transportation_cost=5000,
        activities_cost=8000,
        miscellaneous_cost=2500,
    )

    print(
        tool.format_summary(result)
    )

    assert result.total_cost == 38000

    assert result.remaining_budget == 12000

    assert (
        result.budget_status
        == "Within Budget"
    )