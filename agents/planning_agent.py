import json

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)

from models.planning import TravelPlanStrategy
from models.travel_request import TravelRequest


class PlanningAgent:
    """Agent responsible for creating the execution strategy."""

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE

    def create_plan(
        self,
        travel_request: TravelRequest,
    ) -> TravelPlanStrategy:
        """Create a structured execution plan."""

        prompt = f"""
You are a travel planning orchestrator.

Analyze the following travel request and create an execution strategy.

Destination:
{travel_request.destination}

Budget:
{travel_request.budget} {travel_request.currency}

Number of days:
{travel_request.days}

The strategy must include these tasks:

1. itinerary
2. hotels
3. restaurants
4. weather
5. expenses
6. packing
7. maps

For each task provide:

- name
- description
- priority from 1 to 10

Return ONLY valid JSON.

Expected format:

{{
    "destination": "{travel_request.destination}",
    "days": {travel_request.days},
    "budget": {travel_request.budget},
    "currency": "{travel_request.currency}",
    "tasks": [
        {{
            "name": "itinerary",
            "description": "Create a day-by-day travel itinerary",
            "priority": 10
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

        return TravelPlanStrategy.model_validate(data)