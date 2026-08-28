from typing import List

from pydantic import BaseModel, Field


class HotelSuggestion(BaseModel):
    name: str = Field(
        ...,
        description="Hotel name"
    )

    location: str = Field(
        ...,
        description="Hotel location"
    )

    price_per_night: float = Field(
        ...,
        ge=0,
        description="Estimated price per night"
    )

    total_stay_cost: float = Field(
        ...,
        ge=0,
        description="Estimated total cost for the stay"
    )

    rating: float = Field(
        ...,
        ge=0,
        le=5,
        description="Hotel rating"
    )

    category: str = Field(
        ...,
        description="Budget, Mid-range, or Luxury"
    )

    description: str = Field(
        ...,
        description="Short hotel description"
    )


class HotelRecommendations(BaseModel):
    hotels: List[HotelSuggestion]