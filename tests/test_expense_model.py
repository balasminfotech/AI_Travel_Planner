import pytest

from pydantic import ValidationError

from models.expense import (
    ExpenseBreakdown,
    ExpenseEstimate,
)


def test_valid_expense_breakdown():

    breakdown = ExpenseBreakdown(
        hotel_cost=9000,
        food_cost=4500,
        transportation_cost=3000,
        activities_cost=4000,
        miscellaneous_cost=1000,
    )

    assert breakdown.hotel_cost == 9000
    assert breakdown.food_cost == 4500


def test_negative_expense_validation():

    with pytest.raises(ValidationError):

        ExpenseBreakdown(
            hotel_cost=-100,
            food_cost=500,
            transportation_cost=300,
            activities_cost=200,
            miscellaneous_cost=100,
        )


def test_valid_expense_estimate():

    breakdown = ExpenseBreakdown(
        hotel_cost=9000,
        food_cost=4500,
        transportation_cost=3000,
        activities_cost=4000,
        miscellaneous_cost=1000,
    )

    result = ExpenseEstimate(
        currency="INR",
        budget=30000,
        breakdown=breakdown,
        total_cost=21500,
        remaining_budget=8500,
        budget_status="Within Budget",
        budget_utilization_percentage=71.67,
    )

    assert result.currency == "INR"
    assert result.budget == 30000
    assert result.total_cost == 21500
    assert result.remaining_budget == 8500


def test_invalid_budget_utilization():

    breakdown = ExpenseBreakdown(
        hotel_cost=1000,
        food_cost=1000,
        transportation_cost=1000,
        activities_cost=1000,
        miscellaneous_cost=1000,
    )

    with pytest.raises(ValidationError):

        ExpenseEstimate(
            currency="INR",
            budget=5000,
            breakdown=breakdown,
            total_cost=5000,
            remaining_budget=0,
            budget_status="Within Budget",
            budget_utilization_percentage=-10,
        )