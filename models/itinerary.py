from typing import List

from pydantic import BaseModel, Field


class Activity(BaseModel):
    time: str = Field(
        ...,
        description="Time of the activity"
    )

    title: str = Field(
        ...,
        description="Activity title"
    )

    description: str = Field(
        ...,
        description="Detailed activity description"
    )

    location: str = Field(
        ...,
        description="Activity location"
    )

    estimated_cost: float = Field(
        default=0,
        ge=0,
        description="Estimated cost of the activity"
    )


class DailyItinerary(BaseModel):
    day: int = Field(
        ...,
        gt=0
    )

    date: str

    theme: str = Field(
        ...,
        description="Main theme of the day"
    )

    activities: List[Activity]

    estimated_daily_cost: float = Field(
        default=0,
        ge=0
    )


class Itinerary(BaseModel):
    days: List[DailyItinerary]