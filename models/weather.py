from typing import List

from pydantic import BaseModel, Field


class WeatherDay(BaseModel):
    date: str

    weather_code: int

    temperature_max: float

    temperature_min: float

    precipitation_probability: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    precipitation_sum: float = Field(
        default=0,
        ge=0,
    )


class WeatherForecast(BaseModel):
    location: str

    latitude: float

    longitude: float

    timezone: str

    days: List[WeatherDay]