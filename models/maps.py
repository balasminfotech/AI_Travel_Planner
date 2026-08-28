from pydantic import BaseModel, Field


class Location(BaseModel):
    name: str

    latitude: float

    longitude: float


class RouteResult(BaseModel):
    origin: Location

    destination: Location

    distance_km: float = Field(
        ...,
        ge=0,
    )

    duration_minutes: float = Field(
        ...,
        ge=0,
    )

    distance_text: str

    duration_text: str