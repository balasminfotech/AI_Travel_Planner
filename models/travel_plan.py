from pydantic import BaseModel

from models.expense import ExpenseEstimate
from models.hotel import HotelRecommendations
from models.itinerary import Itinerary
from models.packing import PackingChecklist
from models.restaurant import RestaurantRecommendations
from models.weather import WeatherForecast


class TravelPlan(BaseModel):
    destination: str
    days: int
    budget: float
    currency: str

    itinerary: Itinerary
    hotels: HotelRecommendations
    restaurants: RestaurantRecommendations
    weather: WeatherForecast
    expenses: ExpenseEstimate
    packing: PackingChecklist

    maps_url: str