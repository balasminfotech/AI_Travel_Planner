from typing import List

from pydantic import BaseModel, Field


class RestaurantSuggestion(BaseModel):
    name: str = Field(
        ...,
        description="Restaurant name"
    )

    location: str = Field(
        ...,
        description="Restaurant location"
    )

    cuisine: str = Field(
        ...,
        description="Cuisine type"
    )

    price_level: str = Field(
        ...,
        description="Budget category such as $, $$, $$$"
    )

    average_cost_per_person: float = Field(
        ...,
        ge=0,
        description="Estimated average cost per person"
    )

    rating: float = Field(
        ...,
        ge=0,
        le=5,
        description="Restaurant rating"
    )

    best_for: str = Field(
        ...,
        description="What the restaurant is best known for"
    )

    description: str = Field(
        ...,
        description="Short restaurant description"
    )


class RestaurantRecommendations(BaseModel):
    restaurants: List[RestaurantSuggestion]