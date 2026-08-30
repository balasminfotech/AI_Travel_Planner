from __future__ import annotations

from html import escape
from io import BytesIO
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from models.master_travel_plan import MasterTravelPlan
from models.travel_request import TravelRequest


def _money(value: float, currency: str = "INR") -> str:
    """
    Use the currency code rather than the rupee glyph so the generated
    PDF remains portable with ReportLab's built-in fonts.
    """
    return f"{currency} {value:,.0f}"


def _safe(value: object) -> str:
    return escape(str(value))


def _page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(
        A4[0] - 18 * mm,
        10 * mm,
        f"Page {doc.page}",
    )
    canvas.restoreState()


def generate_pdf_report(
    travel_plan: MasterTravelPlan,
    travel_request: Optional[TravelRequest] = None,
) -> bytes:
    """
    Generate the complete travel plan as PDF bytes.

    The result is kept in memory so Streamlit can serve it directly
    through st.download_button without creating temporary report files.
    """

    buffer = BytesIO()

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"AI Travel Planner - {travel_plan.destination}",
        author="AI Travel Planner",
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="normal",
    )

    doc.addPageTemplates(
        [
            PageTemplate(
                id="travel-plan",
                frames=[frame],
                onPage=_page_number,
            )
        ]
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TravelTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        "TravelSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=16,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=8,
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=7,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "TravelBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        spaceAfter=5,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=body_style,
        fontSize=8,
        leading=11,
        textColor=colors.grey,
    )

    story = [
        Paragraph("AI Travel Planner Report", title_style),
        Paragraph(
            f"Complete travel plan for {_safe(travel_plan.destination)}",
            subtitle_style,
        ),
        Paragraph("Trip Overview", heading_style),
    ]

    currency = (
        travel_request.currency
        if travel_request is not None
        else (
            travel_plan.expenses.currency
            if travel_plan.expenses is not None
            else "INR"
        )
    )

    overview_rows = [
        ["Destination", _safe(travel_plan.destination)],
        ["Duration", f"{travel_plan.days} days"],
        ["Budget", _money(travel_plan.budget, currency)],
    ]

    if travel_request is not None:
        overview_rows.append(
            ["Start Date", travel_request.start_date.isoformat()]
        )

    overview_table = Table(
        overview_rows,
        colWidths=[45 * mm, 110 * mm],
        hAlign="LEFT",
    )
    overview_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.lightgrey),
            ]
        )
    )
    story.extend([overview_table, Spacer(1, 7 * mm)])

    if travel_plan.generation_warnings:
        story.append(
            Paragraph(
                "Generation Warnings",
                heading_style,
            )
        )

        for warning in travel_plan.generation_warnings:
            story.append(
                Paragraph(
                    f"- {_safe(warning)}",
                    body_style,
                )
            )

        story.append(Spacer(1, 3 * mm))

    # Itinerary
    story.append(Paragraph("Day-by-Day Itinerary", heading_style))

    if travel_plan.itinerary is not None and travel_plan.itinerary.days:
        for day in travel_plan.itinerary.days:
            story.append(
                Paragraph(
                    f"Day {day.day} - {_safe(day.theme)}",
                    subheading_style,
                )
            )
            story.append(
                Paragraph(
                    f"<b>Date:</b> {_safe(day.date)}",
                    body_style,
                )
            )

            for activity in day.activities:
                activity_block = [
                    Paragraph(
                        (
                            f"<b>{_safe(activity.time)} - "
                            f"{_safe(activity.title)}</b>"
                        ),
                        body_style,
                    ),
                    Paragraph(
                        _safe(activity.description),
                        body_style,
                    ),
                    Paragraph(
                        (
                            f"<b>Location:</b> {_safe(activity.location)}"
                            f"<br/><b>Estimated Cost:</b> "
                            f"{_money(activity.estimated_cost, currency)}"
                        ),
                        small_style,
                    ),
                    Spacer(1, 2 * mm),
                ]
                story.append(KeepTogether(activity_block))

            story.append(
                Paragraph(
                    (
                        f"<b>Estimated Daily Cost:</b> "
                        f"{_money(day.estimated_daily_cost, currency)}"
                    ),
                    body_style,
                )
            )
            story.append(Spacer(1, 3 * mm))
    else:
        story.append(
            Paragraph("No itinerary was generated.", body_style)
        )

    # Hotels
    story.append(Paragraph("Hotel Recommendations", heading_style))

    if travel_plan.hotels is not None and travel_plan.hotels.hotels:
        for index, hotel in enumerate(travel_plan.hotels.hotels, start=1):
            story.append(
                Paragraph(
                    f"{index}. {_safe(hotel.name)}",
                    subheading_style,
                )
            )
            story.append(
                Paragraph(
                    (
                        f"<b>Location:</b> {_safe(hotel.location)}<br/>"
                        f"<b>Category:</b> {_safe(hotel.category)}<br/>"
                        f"<b>Rating:</b> {hotel.rating:.1f}/5<br/>"
                        f"<b>Price Per Night:</b> "
                        f"{_money(hotel.price_per_night, currency)}<br/>"
                        f"<b>Total Stay:</b> "
                        f"{_money(hotel.total_stay_cost, currency)}"
                    ),
                    body_style,
                )
            )
            story.append(
                Paragraph(_safe(hotel.description), body_style)
            )
    else:
        story.append(
            Paragraph(
                "No hotel recommendations were generated.",
                body_style,
            )
        )

    # Restaurants
    story.append(
        Paragraph("Restaurant Recommendations", heading_style)
    )

    if (
        travel_plan.restaurants is not None
        and travel_plan.restaurants.restaurants
    ):
        for index, restaurant in enumerate(
            travel_plan.restaurants.restaurants,
            start=1,
        ):
            story.append(
                Paragraph(
                    f"{index}. {_safe(restaurant.name)}",
                    subheading_style,
                )
            )
            story.append(
                Paragraph(
                    (
                        f"<b>Location:</b> {_safe(restaurant.location)}<br/>"
                        f"<b>Cuisine:</b> {_safe(restaurant.cuisine)}<br/>"
                        f"<b>Price Level:</b> "
                        f"{_safe(restaurant.price_level)}<br/>"
                        f"<b>Rating:</b> {restaurant.rating:.1f}/5<br/>"
                        f"<b>Average / Person:</b> "
                        f"{_money(restaurant.average_cost_per_person, currency)}"
                        f"<br/><b>Best For:</b> "
                        f"{_safe(restaurant.best_for)}"
                    ),
                    body_style,
                )
            )
            story.append(
                Paragraph(_safe(restaurant.description), body_style)
            )
    else:
        story.append(
            Paragraph(
                "No restaurant recommendations were generated.",
                body_style,
            )
        )

    # Weather
    story.append(Paragraph("Weather Forecast", heading_style))

    if travel_plan.weather is not None:
        weather = travel_plan.weather
        story.append(
            Paragraph(
                (
                    f"<b>Location:</b> {_safe(weather.location)} | "
                    f"<b>Timezone:</b> {_safe(weather.timezone)} | "
                    f"<b>Coordinates:</b> "
                    f"{weather.latitude:.4f}, {weather.longitude:.4f}"
                ),
                body_style,
            )
        )

        weather_rows = [
            [
                "Date",
                "Max C",
                "Min C",
                "Rain %",
                "Precip. mm",
            ]
        ]

        for day in weather.days:
            weather_rows.append(
                [
                    _safe(day.date),
                    f"{day.temperature_max:.1f}",
                    f"{day.temperature_min:.1f}",
                    f"{day.precipitation_probability:.0f}",
                    f"{day.precipitation_sum:.1f}",
                ]
            )

        weather_table = Table(
            weather_rows,
            colWidths=[38 * mm, 26 * mm, 26 * mm, 26 * mm, 30 * mm],
            repeatRows=1,
        )
        weather_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(weather_table)
    else:
        story.append(
            Paragraph("No weather forecast was generated.", body_style)
        )

    # Expenses
    story.append(Paragraph("Expense Estimate", heading_style))

    if travel_plan.expenses is not None:
        expenses = travel_plan.expenses
        breakdown = expenses.breakdown

        expense_summary = [
            ["Budget", _money(expenses.budget, expenses.currency)],
            [
                "Estimated Cost",
                _money(expenses.total_cost, expenses.currency),
            ],
            [
                "Remaining Budget",
                _money(expenses.remaining_budget, expenses.currency),
            ],
            ["Status", _safe(expenses.budget_status)],
            [
                "Utilization",
                f"{expenses.budget_utilization_percentage:.1f}%",
            ],
        ]

        expense_table = Table(
            expense_summary,
            colWidths=[55 * mm, 90 * mm],
        )
        expense_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.lightgrey),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.extend([expense_table, Spacer(1, 3 * mm)])

        breakdown_rows = [
            ["Category", "Estimated Cost"],
            ["Hotel", _money(breakdown.hotel_cost, expenses.currency)],
            ["Food", _money(breakdown.food_cost, expenses.currency)],
            [
                "Transportation",
                _money(
                    breakdown.transportation_cost,
                    expenses.currency,
                ),
            ],
            [
                "Activities",
                _money(breakdown.activities_cost, expenses.currency),
            ],
            [
                "Miscellaneous",
                _money(breakdown.miscellaneous_cost, expenses.currency),
            ],
        ]

        breakdown_table = Table(
            breakdown_rows,
            colWidths=[75 * mm, 70 * mm],
            repeatRows=1,
        )
        breakdown_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
                    ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(breakdown_table)
    else:
        story.append(
            Paragraph("No expense estimate was generated.", body_style)
        )

    # Packing
    story.append(Paragraph("Packing Checklist", heading_style))

    if travel_plan.packing is not None and travel_plan.packing.items:
        for item in travel_plan.packing.items:
            story.append(
                Paragraph(
                    (
                        f"[ ] <b>{_safe(item.item)} x {item.quantity}</b> - "
                        f"{_safe(item.category)}: {_safe(item.reason)}"
                    ),
                    body_style,
                )
            )
    else:
        story.append(
            Paragraph("No packing checklist was generated.", body_style)
        )

    # Routes
    story.append(Paragraph("Maps and Routes", heading_style))

    if travel_plan.routes:
        for index, route in enumerate(travel_plan.routes, start=1):
            story.append(
                Paragraph(
                    (
                        f"Route {index}: {_safe(route.origin.name)} -> "
                        f"{_safe(route.destination.name)}"
                    ),
                    subheading_style,
                )
            )
            story.append(
                Paragraph(
                    (
                        f"<b>Distance:</b> {_safe(route.distance_text)}<br/>"
                        f"<b>Duration:</b> {_safe(route.duration_text)}<br/>"
                        f"<b>Travel Mode:</b> Driving<br/>"
                        f"<b>Origin Coordinates:</b> "
                        f"{route.origin.latitude:.6f}, "
                        f"{route.origin.longitude:.6f}<br/>"
                        f"<b>Destination Coordinates:</b> "
                        f"{route.destination.latitude:.6f}, "
                        f"{route.destination.longitude:.6f}"
                    ),
                    body_style,
                )
            )
    else:
        story.append(Paragraph("No routes were generated.", body_style))

    story.extend(
        [
            Spacer(1, 6 * mm),
            Paragraph(
                "Generated by AI Travel Planner.",
                small_style,
            ),
        ]
    )

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
