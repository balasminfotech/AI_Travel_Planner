from models.itinerary import (
    Activity,
    DailyItinerary,
    Itinerary,
)


def test_itinerary_structure():

    activity = Activity(
        time="10:00 AM",
        title="Visit Beach",
        description="Relax at the beach",
        location="Baga Beach",
        estimated_cost=0,
    )

    day = DailyItinerary(
        day=1,
        date="2026-09-01",
        theme="Beach Day",
        activities=[activity],
        estimated_daily_cost=0,
    )

    itinerary = Itinerary(
        days=[day]
    )

    assert len(itinerary.days) == 1
    assert itinerary.days[0].day == 1
    assert itinerary.days[0].theme == "Beach Day"

    assert (
        itinerary.days[0]
        .activities[0]
        .location
        == "Baga Beach"
    )