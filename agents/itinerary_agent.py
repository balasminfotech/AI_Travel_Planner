import json
from datetime import timedelta
from google import genai

from config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)

from models.itinerary import Itinerary
from models.travel_request import TravelRequest


class ItineraryAgent:
    """Agent responsible for creating a day-by-day itinerary."""

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE

    def create_itinerary(
        self,
        travel_request: TravelRequest,
    ) -> Itinerary:
        """Generate a structured travel itinerary."""

        prompt = f"""
        You are an expert travel itinerary planner.

        Create a practical day-by-day itinerary for the following trip.

        Destination:
        {travel_request.destination}

        Budget:
        {travel_request.budget} {travel_request.currency}

        Number of days:
        {travel_request.days}

        Trip start date:
        {travel_request.start_date}

        IMPORTANT DATE RULES:

        1. Day 1 MUST use the exact trip start date:
        {travel_request.start_date}

        2. Each subsequent day MUST be the next calendar day
        after the previous day.

        3. Continue sequentially for all {travel_request.days} days.

        4. Do NOT invent a different year, month, or starting date.

        5. Create exactly {travel_request.days} days.

        6. Every day's date MUST be in YYYY-MM-DD format.

        7. The supplied trip start date is authoritative.

        8. All estimated costs MUST be expressed in
        {travel_request.currency}.

        Requirements:

        1. Create exactly {travel_request.days} days.
        2. Each day must have a clear theme.
        3. Include multiple activities per day.
        4. Include realistic times.
        5. Include the location for every activity.
        6. Include a short description.
        7. Include an estimated cost for every activity.
        8. Include an estimated total daily cost.
        9. Keep the itinerary practical and geographically sensible.
        10. Avoid scheduling too many activities in a single day.
        11. Consider travel time between locations.
        12. Try to stay within the overall budget.
        13. Do not claim real-time availability.
        14. Clearly use reasonable estimated costs.
        15. Do not use dates from example data.
        16. Do not use historical dates unless they match the supplied
            trip start date.
        17. The supplied trip start date is the only authoritative start date.

        Return ONLY valid JSON.

        Expected structure:

        {{
            "days": [
                {{
                    "day": 1,
                    "date": "{travel_request.start_date}",
                    "theme": "Day theme",
                    "activities": [
                        {{
                            "time": "09:00 AM",
                            "title": "Activity name",
                            "description": "Activity description",
                            "location": "Location",
                            "estimated_cost": 500
                        }}
                    ],
                    "estimated_daily_cost": 2500
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

        data = json.loads(
            response.text
        )

        itinerary = Itinerary.model_validate(
            data
        )

        return self._validate_dates(
            itinerary,
            travel_request,
        )

    @staticmethod
    def _validate_dates(
        itinerary: Itinerary,
        travel_request: TravelRequest,
    ) -> Itinerary:
        """
        Validate and normalize itinerary dates.

        The LLM is not trusted to generate dates.
        Dates are calculated deterministically from
        the travel request.
        """

        expected_days = travel_request.days
        start_date = travel_request.start_date

        if len(itinerary.days) != expected_days:
            raise ValueError(
                f"Itinerary must contain exactly "
                f"{expected_days} days, but received "
                f"{len(itinerary.days)} days."
            )

        for index, day in enumerate(
            itinerary.days,
            start=1,
        ):

            expected_date = (
                start_date
                + timedelta(days=index - 1)
            )

            day.day = index

            day.date = expected_date.isoformat()

        return itinerary