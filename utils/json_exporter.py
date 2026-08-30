from __future__ import annotations

import json
from typing import Optional

from models.master_travel_plan import MasterTravelPlan
from models.travel_request import TravelRequest


def generate_json_export(
    travel_plan: MasterTravelPlan,
    travel_request: Optional[TravelRequest] = None,
) -> str:
    """
    Serialize the complete travel plan as human-readable JSON.
    """

    payload = {
        "travel_request": (
            travel_request.model_dump(mode="json")
            if travel_request is not None
            else None
        ),
        "travel_plan": travel_plan.model_dump(mode="json"),
    }

    return json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
    )
