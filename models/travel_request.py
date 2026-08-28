from datetime import date

from pydantic import BaseModel, Field


class TravelRequest(BaseModel):
    destination: str = Field(
        ...,
        min_length=2,
        description="Travel destination"
    )

    budget: float = Field(
        ...,
        gt=0,
        description="Total travel budget"
    )

    days: int = Field(
        ...,
        gt=0,
        le=30,
        description="Number of travel days"
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
        description="Budget currency"
    )

    start_date: date = Field(
        default_factory=date.today,
        description="Trip start date"
    )