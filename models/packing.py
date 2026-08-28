from typing import List

from pydantic import BaseModel, Field


class PackingItem(BaseModel):
    item: str = Field(
        ...,
        description="Packing item name"
    )

    category: str = Field(
        ...,
        description="Packing category"
    )

    quantity: int = Field(
        ...,
        ge=1,
        description="Recommended quantity"
    )

    reason: str = Field(
        ...,
        description="Why this item is recommended"
    )


class PackingChecklist(BaseModel):
    destination: str

    days: int = Field(
        ...,
        ge=1,
    )

    items: List[PackingItem]