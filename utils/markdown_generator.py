from __future__ import annotations

from datetime import date
from typing import Optional

from models.master_travel_plan import MasterTravelPlan
from models.travel_request import TravelRequest


def _money(value: float, currency: str = "INR") -> str:
    """Format a monetary value for text-based exports."""
    return f"{currency} {value:,.0f}"


def generate_markdown_report(
    travel_plan: MasterTravelPlan,
    travel_request: Optional[TravelRequest] = None,
) -> str:
    """
    Build a complete Markdown travel-plan report.

    The function returns Markdown text rather than writing a file so it
    can be used directly with Streamlit's download_button.
    """

    currency = (
        travel_request.currency
        if travel_request is not None
        else (
            travel_plan.expenses.currency
            if travel_plan.expenses is not None
            else "INR"
        )
    )

    lines: list[str] = [
        "# AI Travel Planner Report",
        "",
        "## Trip Overview",
        "",
        f"- **Destination:** {travel_plan.destination}",
        f"- **Duration:** {travel_plan.days} days",
        f"- **Budget:** {_money(travel_plan.budget, currency)}",
    ]

    if travel_request is not None:
        lines.append(
            f"- **Start Date:** {travel_request.start_date.isoformat()}"
        )

    if travel_plan.generation_warnings:
        lines.extend(
            [
                "",
                "## Generation Warnings",
                "",
            ]
        )

        for warning in travel_plan.generation_warnings:
            lines.append(f"- {warning}")

    # Itinerary
    lines.extend(["", "## Day-by-Day Itinerary", ""])

    if travel_plan.itinerary is not None and travel_plan.itinerary.days:
        for day in travel_plan.itinerary.days:
            lines.extend(
                [
                    f"### Day {day.day} - {day.theme}",
                    "",
                    f"**Date:** {day.date}",
                    "",
                ]
            )

            for activity in day.activities:
                lines.extend(
                    [
                        f"#### {activity.time} - {activity.title}",
                        "",
                        activity.description,
                        "",
                        f"- **Location:** {activity.location}",
                        (
                            "- **Estimated Cost:** "
                            f"{_money(activity.estimated_cost, currency)}"
                        ),
                        "",
                    ]
                )

            lines.extend(
                [
                    (
                        f"**Estimated Daily Cost:** "
                        f"{_money(day.estimated_daily_cost, currency)}"
                    ),
                    "",
                ]
            )
    else:
        lines.append("No itinerary was generated.")

    # Hotels
    lines.extend(["", "## Hotel Recommendations", ""])

    if travel_plan.hotels is not None and travel_plan.hotels.hotels:
        for index, hotel in enumerate(travel_plan.hotels.hotels, start=1):
            lines.extend(
                [
                    f"### {index}. {hotel.name}",
                    "",
                    f"- **Location:** {hotel.location}",
                    f"- **Category:** {hotel.category}",
                    f"- **Rating:** {hotel.rating:.1f}/5",
                    (
                        "- **Price Per Night:** "
                        f"{_money(hotel.price_per_night, currency)}"
                    ),
                    (
                        "- **Total Stay Cost:** "
                        f"{_money(hotel.total_stay_cost, currency)}"
                    ),
                    "",
                    hotel.description,
                    "",
                ]
            )
    else:
        lines.append("No hotel recommendations were generated.")

    # Restaurants
    lines.extend(["", "## Restaurant Recommendations", ""])

    if (
        travel_plan.restaurants is not None
        and travel_plan.restaurants.restaurants
    ):
        for index, restaurant in enumerate(
            travel_plan.restaurants.restaurants,
            start=1,
        ):
            lines.extend(
                [
                    f"### {index}. {restaurant.name}",
                    "",
                    f"- **Location:** {restaurant.location}",
                    f"- **Cuisine:** {restaurant.cuisine}",
                    f"- **Price Level:** {restaurant.price_level}",
                    f"- **Rating:** {restaurant.rating:.1f}/5",
                    (
                        "- **Average Cost Per Person:** "
                        f"{_money(restaurant.average_cost_per_person, currency)}"
                    ),
                    f"- **Best For:** {restaurant.best_for}",
                    "",
                    restaurant.description,
                    "",
                ]
            )
    else:
        lines.append("No restaurant recommendations were generated.")

    # Weather
    lines.extend(["", "## Weather Forecast", ""])

    if travel_plan.weather is not None:
        weather = travel_plan.weather
        lines.extend(
            [
                f"- **Location:** {weather.location}",
                f"- **Timezone:** {weather.timezone}",
                (
                    "- **Coordinates:** "
                    f"{weather.latitude:.4f}, {weather.longitude:.4f}"
                ),
                "",
                "| Date | Max C | Min C | Rain % | Precipitation (mm) |",
                "|---|---:|---:|---:|---:|",
            ]
        )

        for day in weather.days:
            lines.append(
                f"| {day.date} | "
                f"{day.temperature_max:.1f} | "
                f"{day.temperature_min:.1f} | "
                f"{day.precipitation_probability:.0f} | "
                f"{day.precipitation_sum:.1f} |"
            )
    else:
        lines.append("No weather forecast was generated.")

    # Expenses
    lines.extend(["", "## Expense Estimate", ""])

    if travel_plan.expenses is not None:
        expenses = travel_plan.expenses
        breakdown = expenses.breakdown

        lines.extend(
            [
                f"- **Budget:** {_money(expenses.budget, expenses.currency)}",
                (
                    "- **Estimated Total Cost:** "
                    f"{_money(expenses.total_cost, expenses.currency)}"
                ),
                (
                    "- **Remaining Budget:** "
                    f"{_money(expenses.remaining_budget, expenses.currency)}"
                ),
                f"- **Budget Status:** {expenses.budget_status}",
                (
                    "- **Budget Utilization:** "
                    f"{expenses.budget_utilization_percentage:.1f}%"
                ),
                "",
                "### Expense Breakdown",
                "",
                "| Category | Estimated Cost |",
                "|---|---:|",
                (
                    f"| Hotel | "
                    f"{_money(breakdown.hotel_cost, expenses.currency)} |"
                ),
                (
                    f"| Food | "
                    f"{_money(breakdown.food_cost, expenses.currency)} |"
                ),
                (
                    f"| Transportation | "
                    f"{_money(breakdown.transportation_cost, expenses.currency)} |"
                ),
                (
                    f"| Activities | "
                    f"{_money(breakdown.activities_cost, expenses.currency)} |"
                ),
                (
                    f"| Miscellaneous | "
                    f"{_money(breakdown.miscellaneous_cost, expenses.currency)} |"
                ),
            ]
        )
    else:
        lines.append("No expense estimate was generated.")

    # Packing
    lines.extend(["", "## Packing Checklist", ""])

    if travel_plan.packing is not None and travel_plan.packing.items:
        for item in travel_plan.packing.items:
            lines.append(
                f"- [ ] **{item.item} x {item.quantity}** - "
                f"{item.category}: {item.reason}"
            )
    else:
        lines.append("No packing checklist was generated.")

    # Routes
    lines.extend(["", "## Maps and Routes", ""])

    if travel_plan.routes:
        for index, route in enumerate(travel_plan.routes, start=1):
            lines.extend(
                [
                    (
                        f"### Route {index}: "
                        f"{route.origin.name} -> {route.destination.name}"
                    ),
                    "",
                    f"- **Distance:** {route.distance_text}",
                    f"- **Duration:** {route.duration_text}",
                    "- **Travel Mode:** Driving",
                    (
                        "- **Origin Coordinates:** "
                        f"{route.origin.latitude:.6f}, "
                        f"{route.origin.longitude:.6f}"
                    ),
                    (
                        "- **Destination Coordinates:** "
                        f"{route.destination.latitude:.6f}, "
                        f"{route.destination.longitude:.6f}"
                    ),
                    "",
                ]
            )
    else:
        lines.append("No routes were generated.")

    lines.extend(
        [
            "",
            "---",
            "",
            "*Generated by AI Travel Planner.*",
            "",
        ]
    )

    return "\n".join(lines)
