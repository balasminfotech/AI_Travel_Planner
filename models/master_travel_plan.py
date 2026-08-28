from typing import Optional

from pydantic import BaseModel

from models.expense import ExpenseEstimate
from models.hotel import HotelRecommendations
from models.itinerary import Itinerary
from models.maps import RouteResult
from models.packing import PackingChecklist
from models.restaurant import RestaurantRecommendations
from models.weather import WeatherForecast


class MasterTravelPlan(BaseModel):
    destination: str

    days: int

    budget: float

    itinerary: Optional[Itinerary] = None

    hotels: Optional[HotelRecommendations] = None

    restaurants: Optional[RestaurantRecommendations] = None

    weather: Optional[WeatherForecast] = None

    expenses: Optional[ExpenseEstimate] = None

    packing: Optional[PackingChecklist] = None

    routes: list[RouteResult] = []