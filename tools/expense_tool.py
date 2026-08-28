from models.expense import (
    ExpenseBreakdown,
    ExpenseEstimate,
)


class ExpenseTool:
    """
    Tool responsible for calculating
    travel expenses and budget status.
    """

    def calculate(
        self,
        budget: float,
        currency: str,
        hotel_cost: float = 0,
        food_cost: float = 0,
        transportation_cost: float = 0,
        activities_cost: float = 0,
        miscellaneous_cost: float = 0,
    ) -> ExpenseEstimate:

        self._validate_inputs(
            budget=budget,
            hotel_cost=hotel_cost,
            food_cost=food_cost,
            transportation_cost=transportation_cost,
            activities_cost=activities_cost,
            miscellaneous_cost=miscellaneous_cost,
        )

        breakdown = ExpenseBreakdown(
            hotel_cost=hotel_cost,
            food_cost=food_cost,
            transportation_cost=transportation_cost,
            activities_cost=activities_cost,
            miscellaneous_cost=miscellaneous_cost,
        )

        total_cost = (
            hotel_cost
            + food_cost
            + transportation_cost
            + activities_cost
            + miscellaneous_cost
        )

        remaining_budget = (
            budget - total_cost
        )

        if total_cost <= budget:
            budget_status = "Within Budget"
        else:
            budget_status = "Over Budget"

        if budget == 0:
            budget_utilization_percentage = 0
        else:
            budget_utilization_percentage = (
                total_cost / budget
            ) * 100

        return ExpenseEstimate(
            currency=currency,
            budget=budget,
            breakdown=breakdown,
            total_cost=total_cost,
            remaining_budget=remaining_budget,
            budget_status=budget_status,
            budget_utilization_percentage=(
                budget_utilization_percentage
            ),
        )


    @staticmethod
    def format_summary(
        result: ExpenseEstimate,
    ) -> str:

        breakdown = result.breakdown

        return (
            "\n"
            "========================================\n"
            "TRAVEL EXPENSE ESTIMATE\n"
            "========================================\n"
            f"Budget: {result.budget:.2f} "
            f"{result.currency}\n"
            "\n"
            f"Hotel: {breakdown.hotel_cost:.2f} "
            f"{result.currency}\n"
            f"Food: {breakdown.food_cost:.2f} "
            f"{result.currency}\n"
            f"Transportation: "
            f"{breakdown.transportation_cost:.2f} "
            f"{result.currency}\n"
            f"Activities: "
            f"{breakdown.activities_cost:.2f} "
            f"{result.currency}\n"
            f"Miscellaneous: "
            f"{breakdown.miscellaneous_cost:.2f} "
            f"{result.currency}\n"
            "\n"
            f"Total Cost: {result.total_cost:.2f} "
            f"{result.currency}\n"
            f"Remaining Budget: "
            f"{result.remaining_budget:.2f} "
            f"{result.currency}\n"
            f"Budget Status: "
            f"{result.budget_status}\n"
            f"Budget Utilization: "
            f"{result.budget_utilization_percentage:.2f}%\n"
            "========================================"
        )


    @staticmethod
    def _validate_inputs(
        budget: float,
        hotel_cost: float,
        food_cost: float,
        transportation_cost: float,
        activities_cost: float,
        miscellaneous_cost: float,
    ):

        values = {
            "budget": budget,
            "hotel_cost": hotel_cost,
            "food_cost": food_cost,
            "transportation_cost": transportation_cost,
            "activities_cost": activities_cost,
            "miscellaneous_cost": miscellaneous_cost,
        }

        for name, value in values.items():

            if value < 0:
                raise ValueError(
                    f"{name} cannot be negative."
                )