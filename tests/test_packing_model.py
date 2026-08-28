import pytest

from pydantic import ValidationError

from models.packing import (
    PackingChecklist,
    PackingItem,
)


def test_valid_packing_item():

    item = PackingItem(
        item="T-shirts",
        category="Clothing",
        quantity=4,
        reason="Suitable for warm weather",
    )

    assert item.item == "T-shirts"

    assert item.category == "Clothing"

    assert item.quantity == 4


def test_invalid_quantity():

    with pytest.raises(ValidationError):

        PackingItem(
            item="T-shirts",
            category="Clothing",
            quantity=0,
            reason="Suitable for warm weather",
        )


def test_negative_quantity():

    with pytest.raises(ValidationError):

        PackingItem(
            item="T-shirts",
            category="Clothing",
            quantity=-2,
            reason="Suitable for warm weather",
        )


def test_valid_checklist():

    item = PackingItem(
        item="Passport",
        category="Documents",
        quantity=1,
        reason="Required travel document",
    )

    checklist = PackingChecklist(
        destination="Goa",
        days=3,
        items=[item],
    )

    assert checklist.destination == "Goa"

    assert checklist.days == 3

    assert len(checklist.items) == 1


def test_invalid_days():

    with pytest.raises(ValidationError):

        PackingChecklist(
            destination="Goa",
            days=0,
            items=[],
        )