from pydantic import BaseModel, Field


class ExpenseBreakdown(BaseModel):
    hotel_cost: float = Field(
        ...,
        ge=0,
        description="Total hotel expense"
    )

    food_cost: float = Field(
        ...,
        ge=0,
        description="Total food expense"
    )

    transportation_cost: float = Field(
        ...,
        ge=0,
        description="Total transportation expense"
    )

    activities_cost: float = Field(
        ...,
        ge=0,
        description="Total activities expense"
    )

    miscellaneous_cost: float = Field(
        ...,
        ge=0,
        description="Miscellaneous expenses"
    )


class ExpenseEstimate(BaseModel):
    currency: str

    budget: float = Field(
        ...,
        ge=0,
    )

    breakdown: ExpenseBreakdown

    total_cost: float = Field(
        ...,
        ge=0,
    )

    remaining_budget: float

    budget_status: str

    budget_utilization_percentage: float = Field(
        ...,
        ge=0,
    )