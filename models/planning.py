from typing import List

from pydantic import BaseModel, Field


class PlanningTask(BaseModel):
    name: str
    description: str
    priority: int = Field(..., ge=1, le=10)


class TravelPlanStrategy(BaseModel):
    destination: str
    days: int
    budget: float
    currency: str

    tasks: List[PlanningTask]