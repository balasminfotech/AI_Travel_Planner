import json

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)

from models.hotel import HotelRecommendations
from models.travel_request import TravelRequest


class HotelAgent:
    """Agent responsible for generating hotel recommendations."""

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE

    def recommend_hotels(
        self,
        travel_request: TravelRequest,
    ) -> HotelRecommendations:
        """Generate structured hotel recommendations."""

        prompt = f"""
        You are an expert travel accommodation advisor.

        Recommend suitable hotels for the following trip.

        Destination:
        {travel_request.destination}

        Budget:
        {travel_request.budget} {travel_request.currency}

        Number of days:
        {travel_request.days}

        Requirements:

        1. Recommend 3 suitable hotels.
        2. Include a mix of budget and mid-range options where possible.
        3. Consider the user's overall travel budget.
        4. Provide estimated price per night.
        5. Calculate estimated total stay cost.
        6. Provide a rating between 0 and 5.
        7. Provide the hotel category.
        8. Provide the location.
        9. Provide a short description.
        10. Prefer practical locations for sightseeing.
        11. Do not claim real-time availability.
        12. Prices are estimates and may change.
        13. Do not invent booking confirmations.

        Return ONLY valid JSON.

        Expected structure:

        {{
            "hotels": [
                {{
                    "name": "Hotel Name",
                    "location": "Location",
                    "price_per_night": 3000,
                    "total_stay_cost": 9000,
                    "rating": 4.2,
                    "category": "Mid-range",
                    "description": "Short description"
                }}
            ]
        }}
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "temperature": self.temperature,
                "response_mime_type": "application/json",
            },
        )

        data = json.loads(response.text)

        return HotelRecommendations.model_validate(data)