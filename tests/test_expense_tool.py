import pytest

from tools.expense_tool import ExpenseTool


def test_expense_calculation():

    tool = ExpenseTool()

    result = tool.calculate(
        budget=30000,
        currency="INR",
        hotel_cost=9000,
        food_cost=4500,
        transportation_cost=3000,
        activities_cost=4000,
        miscellaneous_cost=1000,
    )

    assert result.budget == 30000

    assert result.total_cost == 21500

    assert result.remaining_budget == 8500

    assert result.budget_status == "Within Budget"

    assert (
        result.budget_utilization_percentage
        == pytest.approx(71.6666667)
    )


def test_over_budget():

    tool = ExpenseTool()

    result = tool.calculate(
        budget=20000,
        currency="INR",
        hotel_cost=10000,
        food_cost=5000,
        transportation_cost=3000,
        activities_cost=4000,
        miscellaneous_cost=1000,
    )

    assert result.total_cost == 23000

    assert result.remaining_budget == -3000

    assert result.budget_status == "Over Budget"


def test_zero_expenses():

    tool = ExpenseTool()

    result = tool.calculate(
        budget=30000,
        currency="INR",
    )

    assert result.total_cost == 0

    assert result.remaining_budget == 30000

    assert result.budget_status == "Within Budget"


def test_negative_budget():

    tool = ExpenseTool()

    with pytest.raises(ValueError):

        tool.calculate(
            budget=-1000,
            currency="INR",
        )


def test_negative_hotel_cost():

    tool = ExpenseTool()

    with pytest.raises(ValueError):

        tool.calculate(
            budget=30000,
            currency="INR",
            hotel_cost=-500,
        )


def test_negative_food_cost():

    tool = ExpenseTool()

    with pytest.raises(ValueError):

        tool.calculate(
            budget=30000,
            currency="INR",
            food_cost=-100,
        )


def test_format_summary():

    tool = ExpenseTool()

    result = tool.calculate(
        budget=30000,
        currency="INR",
        hotel_cost=9000,
        food_cost=4500,
        transportation_cost=3000,
        activities_cost=4000,
        miscellaneous_cost=1000,
    )

    summary = tool.format_summary(result)

    assert "TRAVEL EXPENSE ESTIMATE" in summary

    assert "30000.00 INR" in summary

    assert "21500.00 INR" in summary

    assert "8500.00 INR" in summary

    assert "Within Budget" in summary