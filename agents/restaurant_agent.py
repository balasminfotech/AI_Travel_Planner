import json

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)

from models.restaurant import RestaurantRecommendations
from models.travel_request import TravelRequest


class RestaurantAgent:
    """Agent responsible for generating restaurant recommendations."""

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE

    def recommend_restaurants(
        self,
        travel_request: TravelRequest,
    ) -> RestaurantRecommendations:
        """Generate structured restaurant recommendations."""

        prompt = f"""
You are an expert local food and restaurant advisor.

Recommend restaurants for the following trip.

Destination:
{travel_request.destination}

Budget:
{travel_request.budget} {travel_request.currency}

Number of days:
{travel_request.days}

Requirements:

1. Recommend 5 restaurants.
2. Include different cuisines where practical.
3. Include budget-friendly options.
4. Include at least one popular/local specialty option.
5. Provide the restaurant name.
6. Provide the location.
7. Provide cuisine type.
8. Provide price level using $, $$, or $$$.
9. Provide estimated average cost per person.
10. Provide a rating between 0 and 5.
11. Explain what each restaurant is best for.
12. Provide a short description.
13. Consider the user's overall travel budget.
14. Do not claim real-time availability.
15. Prices and ratings are estimates and may change.
16. Do not claim that a reservation has been made.

Return ONLY valid JSON.

Expected structure:

{{
    "restaurants": [
        {{
            "name": "Restaurant Name",
            "location": "Location",
            "cuisine": "Indian",
            "price_level": "$$",
            "average_cost_per_person": 500,
            "rating": 4.3,
            "best_for": "Local cuisine",
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

        return RestaurantRecommendations.model_validate(data)