from google import genai

from config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)
from models.travel_request import TravelRequest


class TravelPlannerAgent:
    """AI agent responsible for generating travel plans."""

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE

    def generate_plan(
        self,
        travel_request: TravelRequest,
    ) -> str:
        """Generate a travel plan using Gemini."""

        prompt = f"""
        You are an expert travel planner.

        Create a practical travel plan based on the following request.

        Destination:
        {travel_request.destination}

        Budget:
        {travel_request.budget} {travel_request.currency}

        Number of days:
        {travel_request.days}

        Provide:

        1. Trip overview
        2. Day-by-day itinerary
        3. Recommended places to visit
        4. Food recommendations
        5. Approximate accommodation cost
        6. Approximate food cost
        7. Approximate transportation cost
        8. Approximate activity cost
        9. Packing suggestions
        10. Important travel tips

        Important requirements:

        - Stay within the user's budget.
        - Organize the itinerary clearly by day.
        - Provide realistic estimated costs.
        - Prioritize practical recommendations.
        - Do not claim real-time availability.
        - Clearly state that prices and conditions may change.

        Return a concise but useful travel plan.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "temperature": self.temperature,
            },
        )

        return response.text