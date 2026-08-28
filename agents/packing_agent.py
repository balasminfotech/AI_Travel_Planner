import json

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)

from models.packing import PackingChecklist
from models.travel_request import TravelRequest


class PackingAgent:
    """Agent responsible for generating a travel packing checklist."""

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model_name = MODEL_NAME
        self.temperature = TEMPERATURE

    def create_checklist(
        self,
        travel_request: TravelRequest,
        weather_summary: str = "",
        activities: str = "",
    ) -> PackingChecklist:
        """
        Generate a personalized packing checklist.
        """

        prompt = f"""
        You are an expert travel packing assistant.

        Create a practical packing checklist for this trip.

        Destination:
        {travel_request.destination}

        Number of days:
        {travel_request.days}

        Budget:
        {travel_request.budget} {travel_request.currency}

        Weather information:
        {weather_summary or "No specific weather information provided."}

        Planned activities:
        {activities or "General sightseeing and travel."}

        Requirements:

        1. Create a practical packing checklist.
        2. Consider the destination.
        3. Consider the number of travel days.
        4. Consider the weather information.
        5. Consider the planned activities.
        6. Include clothing.
        7. Include toiletries.
        8. Include electronics.
        9. Include travel documents.
        10. Include medicines/basic personal items where appropriate.
        11. Include weather-specific items.
        12. Avoid unnecessary duplicate items.
        13. Recommend realistic quantities.
        14. Every item must have a category.
        15. Every item must have a reason.
        16. Quantity must be a positive integer.
        17. Do not make medical claims.
        18. Do not include dangerous or prohibited items.

        Recommended categories:

        - Clothing
        - Toiletries
        - Electronics
        - Documents
        - Health
        - Weather
        - Accessories
        - Other

        Return ONLY valid JSON.

        Expected structure:

        {{
            "destination": "{travel_request.destination}",
            "days": {travel_request.days},
            "items": [
                {{
                    "item": "T-shirts",
                    "category": "Clothing",
                    "quantity": 4,
                    "reason": "Suitable for warm weather and daily use"
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

        return PackingChecklist.model_validate(data)


    @staticmethod
    def format_checklist(
        checklist: PackingChecklist,
    ) -> str:

        lines = [
            "",
            "========================================",
            "TRAVEL PACKING CHECKLIST",
            "========================================",
            f"Destination: {checklist.destination}",
            f"Days: {checklist.days}",
            "",
        ]

        for index, item in enumerate(
            checklist.items,
            start=1,
        ):

            lines.append(
                f"{index}. {item.item}"
            )

            lines.append(
                f"   Category: {item.category}"
            )

            lines.append(
                f"   Quantity: {item.quantity}"
            )

            lines.append(
                f"   Reason: {item.reason}"
            )

            lines.append("")

        lines.append(
            "========================================"
        )

        return "\n".join(lines)