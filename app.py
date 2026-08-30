import re
import streamlit as st
from datetime import date

# =====================================================
# Agents
# =====================================================

from agents.planning_agent import PlanningAgent
from agents.itinerary_agent import ItineraryAgent
from agents.hotel_agent import HotelAgent
from agents.restaurant_agent import RestaurantAgent
from agents.packing_agent import PackingAgent
from agents.master_travel_agent import MasterTravelPlannerAgent

# =====================================================
# Tools
# =====================================================

from tools.weather_tool import WeatherTool
from tools.expense_tool import ExpenseTool
from tools.maps_tool import MapsTool

# =====================================================
# Models
# =====================================================

from models.travel_request import TravelRequest

# =====================================================
# Export Utilities
# =====================================================

from utils.pdf_generator import generate_pdf_report
from utils.markdown_generator import generate_markdown_report
from utils.json_exporter import generate_json_export
from utils.error_handler import friendly_error_message
from utils.logger import get_logger
from config.settings import validate_required_settings


# =====================================================
# Logger
# =====================================================

logger = get_logger(__name__)


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# Custom Styling
# =====================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.6rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #6b7280;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }

        .section-title {
            font-size: 1.45rem;
            font-weight: 750;
            margin-top: 0.4rem;
            margin-bottom: 0.8rem;
        }

        .info-card {
            padding: 1rem 1.1rem;
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 0.8rem;
            min-height: 110px;
        }

        .card-label {
            font-size: 0.85rem;
            color: #6b7280;
            margin-bottom: 0.25rem;
        }

        .card-value {
            font-size: 1.35rem;
            font-weight: 700;
        }

        .hotel-card, .restaurant-card {
            padding: 0.9rem 1rem;
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 0.75rem;
            margin-bottom: 0.75rem;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.88rem;
        }

        .status-good {
            padding: 0.7rem 1rem;
            border-radius: 0.65rem;
            border: 1px solid rgba(46, 125, 50, 0.25);
        }

        .status-warning {
            padding: 0.7rem 1rem;
            border-radius: 0.65rem;
            border: 1px solid rgba(245, 158, 11, 0.30);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# Page Header
# =====================================================

st.markdown(
    '<div class="main-title">✈️ AI Travel Planner</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Plan your trip with an AI-powered multi-agent workflow — itinerary, hotels, restaurants, weather, expenses, packing and routes.</div>',
    unsafe_allow_html=True,
)

# =====================================================
# Session State
# =====================================================

if "travel_request" not in st.session_state:
    st.session_state.travel_request = None

if "travel_plan" not in st.session_state:
    st.session_state.travel_plan = None

# =====================================================
# Master Agent Factory
# =====================================================

@st.cache_resource
def create_master_agent():
    """
    Create and cache the complete Master Travel Planner Agent.

    The existing multi-agent workflow is preserved.
    """

    planning_agent = PlanningAgent()
    itinerary_agent = ItineraryAgent()
    hotel_agent = HotelAgent()
    restaurant_agent = RestaurantAgent()
    packing_agent = PackingAgent()

    weather_tool = WeatherTool()
    expense_tool = ExpenseTool()
    maps_tool = MapsTool()

    return MasterTravelPlannerAgent(
        planning_agent=planning_agent,
        itinerary_agent=itinerary_agent,
        hotel_agent=hotel_agent,
        restaurant_agent=restaurant_agent,
        weather_tool=weather_tool,
        expense_tool=expense_tool,
        packing_agent=packing_agent,
        maps_tool=maps_tool,
    )

# =====================================================
# Sidebar — Travel Input
# =====================================================

st.sidebar.header("✈️ Travel Details")

destination = st.sidebar.text_input(
    "📍 Destination",
    placeholder="Example: Goa",
)

budget = st.sidebar.number_input(
    "💰 Budget (₹)",
    min_value=1000.0,
    value=30000.0,
    step=1000.0,
)

days = st.sidebar.number_input(
    "📅 Number of Days",
    min_value=1,
    max_value=30,
    value=3,
    step=1,
)

start_date = st.sidebar.date_input(
    "📅 Start Date",
    value=date.today(),
)

st.sidebar.divider()

generate_plan = st.sidebar.button(
    "🚀 Generate Travel Plan",
    type="primary",
    use_container_width=True,
)

if st.sidebar.button(
    "🗑️ Clear Current Plan",
    use_container_width=True,
):
    st.session_state.travel_request = None
    st.session_state.travel_plan = None
    st.rerun()

# =====================================================
# Input Validation + Plan Generation
# =====================================================

if generate_plan:

    if not destination.strip():
        st.error("Please enter a destination.")
        st.stop()

    if budget <= 0:
        st.error("Budget must be greater than zero.")
        st.stop()

    if days <= 0:
        st.error("Number of days must be greater than zero.")
        st.stop()

    try:
        travel_request = TravelRequest(
            destination=destination.strip(),
            budget=budget,
            days=days,
            start_date=start_date,
        )

        st.session_state.travel_request = travel_request
        st.session_state.travel_plan = None

        master_agent = create_master_agent()

        with st.spinner(
            "🤖 AI is creating your complete travel plan..."
        ):
            travel_plan = master_agent.create_travel_plan(
                travel_request
            )

        st.session_state.travel_plan = travel_plan

        logger.info(
            "Travel plan stored in session | warnings=%s",
            len(travel_plan.generation_warnings),
        )

        if travel_plan.generation_warnings:
            st.warning(
                "⚠️ Travel plan generated with some unavailable "
                "components. Available sections are shown below."
            )
        else:
            st.success(
                "🎉 Travel plan generated successfully!"
            )

    except Exception as exc:
        logger.exception(
            "Travel plan generation failed | error=%s",
            type(exc).__name__,
        )

        st.session_state.travel_plan = None

        st.error(
            "❌ Travel plan could not be generated."
        )

        st.warning(
            friendly_error_message(
                "Travel planner",
                exc,
            )
        )

        st.caption(
            "Please try again. If the problem continues, "
            "check your API configuration and service availability."
        )

# =====================================================
# Display Generated Travel Plan
# =====================================================

if st.session_state.travel_plan is not None:

    travel_plan = st.session_state.travel_plan

    # =================================================
    # Trip Overview
    # =================================================

    st.divider()
    st.markdown(
        '<div class="section-title">🌍 Trip Overview</div>',
        unsafe_allow_html=True,
    )

    overview_col1, overview_col2, overview_col3, overview_col4 = (
        st.columns(4)
    )

    with overview_col1:
        st.metric(
            "📍 Destination",
            travel_plan.destination,
        )

    with overview_col2:
        st.metric(
            "💰 Budget",
            f"₹{travel_plan.budget:,.0f}",
        )

    with overview_col3:
        st.metric(
            "📅 Duration",
            f"{travel_plan.days} days",
        )

    with overview_col4:
        request_date = (
            st.session_state.travel_request.start_date
            if st.session_state.travel_request is not None
            else None
        )
        st.metric(
            "🗓️ Start Date",
            request_date.strftime("%d-%m-%Y")
            if request_date
            else "N/A",
        )

    # =================================================
    # Partial Generation Warnings
    # =================================================

    if travel_plan.generation_warnings:

        st.warning(
            "⚠️ Some parts of this travel plan could not be generated."
        )

        with st.expander(
            "View generation warnings",
            expanded=True,
        ):
            for warning in travel_plan.generation_warnings:
                st.write(f"• {warning}")

        st.caption(
            "The available sections below remain usable."
        )

    # =================================================
    # Travel Plan Export
    # =================================================

    st.markdown(
        '<div class="section-title">📥 Export Travel Plan</div>',
        unsafe_allow_html=True,
    )

    travel_request = st.session_state.travel_request

    safe_destination = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        travel_plan.destination.strip(),
    ).strip("_") or "travel_plan"

    try:
        markdown_report = generate_markdown_report(
            travel_plan,
            travel_request,
        )

        json_report = generate_json_export(
            travel_plan,
            travel_request,
        )

        pdf_report = generate_pdf_report(
            travel_plan,
            travel_request,
        )

        logger.info(
            "Travel export files prepared successfully | destination=%s",
            travel_plan.destination,
        )

        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            st.download_button(
                label="📄 Download PDF",
                data=pdf_report,
                file_name=f"{safe_destination}_travel_plan.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        with export_col2:
            st.download_button(
                label="📝 Download Markdown",
                data=markdown_report,
                file_name=f"{safe_destination}_travel_plan.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with export_col3:
            st.download_button(
                label="📦 Download JSON",
                data=json_report,
                file_name=f"{safe_destination}_travel_plan.json",
                mime="application/json",
                use_container_width=True,
            )

        st.caption(
            "Export the complete generated trip as PDF, Markdown, or JSON."
        )

    except Exception as export_exc:
        logger.warning(
            "Travel export preparation failed | destination=%s | error=%s",
            travel_plan.destination,
            type(export_exc).__name__,
        )

        st.warning(
            "⚠️ The travel plan was generated successfully, "
            "but one or more export files could not be prepared."
        )
        st.caption(str(export_exc))

    # =================================================
    # Quick Expense Summary
    # =================================================

    if travel_plan.expenses is not None:

        expenses = travel_plan.expenses

        st.markdown(
            '<div class="section-title">💰 Expense Summary</div>',
            unsafe_allow_html=True,
        )

        expense_col1, expense_col2, expense_col3, expense_col4 = (
            st.columns(4)
        )

        with expense_col1:
            st.metric(
                "Estimated Cost",
                f"₹{expenses.total_cost:,.0f}",
            )

        with expense_col2:
            st.metric(
                "Budget",
                f"₹{expenses.budget:,.0f}",
            )

        with expense_col3:
            st.metric(
                "Remaining",
                f"₹{expenses.remaining_budget:,.0f}",
            )

        with expense_col4:
            st.metric(
                "Utilization",
                f"{expenses.budget_utilization_percentage:.1f}%",
            )

        if expenses.budget_status == "Within Budget":
            st.success("✅ Estimated trip cost is within your budget.")
        else:
            st.warning(
                "⚠️ Estimated trip cost exceeds your budget."
            )

    # =================================================
    # Itinerary
    # =================================================

    if travel_plan.itinerary is not None:

        st.divider()
        st.markdown(
            '<div class="section-title">🗓️ Day-by-Day Itinerary</div>',
            unsafe_allow_html=True,
        )

        itinerary = travel_plan.itinerary

        for day_plan in itinerary.days:

            with st.expander(
                f"📅 Day {day_plan.day} — {day_plan.theme}",
                expanded=day_plan.day == 1,
            ):

                if hasattr(day_plan, "date"):
                    st.caption(f"🗓️ Date: {day_plan.date}")

                if not day_plan.activities:
                    st.info("No activities were generated for this day.")
                    continue

                for activity in day_plan.activities:

                    activity_col1, activity_col2 = st.columns(
                        [3, 1]
                    )

                    with activity_col1:
                        st.markdown(
                            f"### 🕐 {activity.time} — {activity.title}"
                        )
                        st.write(activity.description)
                        st.markdown(
                            f"📍 **Location:** {activity.location}"
                        )

                    with activity_col2:
                        st.metric(
                            "Estimated Cost",
                            f"₹{activity.estimated_cost:,.0f}",
                        )

                    st.divider()

                st.markdown(
                    f"**💰 Estimated Daily Cost:** "
                    f"₹{day_plan.estimated_daily_cost:,.0f}"
                )

    else:
        st.divider()
        st.markdown(
            '<div class="section-title">🗓️ Day-by-Day Itinerary</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "The itinerary is currently unavailable."
        )

    # =================================================
    # Hotels
    # =================================================

    if travel_plan.hotels is not None:

        st.divider()
        st.markdown(
            '<div class="section-title">🏨 Hotel Recommendations</div>',
            unsafe_allow_html=True,
        )

        hotels = travel_plan.hotels.hotels

        if not hotels:
            st.info("No hotel recommendations were generated.")
        else:
            hotel_columns = st.columns(
                min(3, len(hotels))
            )

            for index, hotel in enumerate(hotels):

                with hotel_columns[index % len(hotel_columns)]:

                    st.markdown(
                        f"""
                        <div class="hotel-card">
                            <h4>🏨 {index + 1}. {hotel.name}</h4>
                            <div class="small-muted">
                                📍 {hotel.location}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.metric(
                        "⭐ Rating",
                        f"{hotel.rating}/5",
                    )

                    st.markdown(
                        f"🏷️ **Category:** {hotel.category}"
                    )

                    st.markdown(
                        f"💰 **Per Night:** "
                        f"₹{hotel.price_per_night:,.0f}"
                    )

                    st.markdown(
                        f"💰 **Total Stay:** "
                        f"₹{hotel.total_stay_cost:,.0f}"
                    )

                    st.write(hotel.description)

    else:
        st.divider()
        st.markdown(
            '<div class="section-title">🏨 Hotel Recommendations</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "Hotel recommendations are currently unavailable."
        )

    # =================================================
    # Restaurants
    # =================================================

    if travel_plan.restaurants is not None:

        st.divider()
        st.markdown(
            '<div class="section-title">🍴 Restaurant Recommendations</div>',
            unsafe_allow_html=True,
        )

        restaurants = travel_plan.restaurants.restaurants

        if not restaurants:
            st.info("No restaurant recommendations were generated.")
        else:
            restaurant_columns = st.columns(
                min(3, len(restaurants))
            )

            for index, restaurant in enumerate(restaurants):

                with restaurant_columns[
                    index % len(restaurant_columns)
                ]:

                    st.markdown(
                        f"""
                        <div class="restaurant-card">
                            <h4>🍴 {index + 1}. {restaurant.name}</h4>
                            <div class="small-muted">
                                📍 {restaurant.location}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"🍛 **Cuisine:** {restaurant.cuisine}"
                    )

                    st.markdown(
                        f"💵 **Price Level:** {restaurant.price_level}"
                    )

                    st.markdown(
                        f"💰 **Average / Person:** "
                        f"₹{restaurant.average_cost_per_person:,.0f}"
                    )

                    st.markdown(
                        f"⭐ **Rating:** {restaurant.rating}/5"
                    )

                    st.markdown(
                        f"🎯 **Best For:** {restaurant.best_for}"
                    )

                    st.write(restaurant.description)

    else:
        st.divider()
        st.markdown(
            '<div class="section-title">🍴 Restaurant Recommendations</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "Restaurant recommendations are currently unavailable."
        )

    # =================================================
    # Weather
    # =================================================

    if travel_plan.weather is not None:

        st.divider()
        st.markdown(
            '<div class="section-title">🌤️ Weather Forecast</div>',
            unsafe_allow_html=True,
        )

        weather = travel_plan.weather

        weather_col1, weather_col2, weather_col3 = st.columns(3)

        with weather_col1:
            st.metric("📍 Location", weather.location)

        with weather_col2:
            st.metric(
                "🌐 Timezone",
                weather.timezone,
            )

        with weather_col3:
            st.metric(
                "📌 Coordinates",
                f"{weather.latitude:.4f}, {weather.longitude:.4f}",
            )

        if weather.days:

            forecast_rows = []

            for weather_day in weather.days:
                forecast_rows.append(
                    {
                        "Date": weather_day.date,
                        "Max °C": weather_day.temperature_max,
                        "Min °C": weather_day.temperature_min,
                        "Rain %": weather_day.precipitation_probability,
                        "Precipitation (mm)": weather_day.precipitation_sum,
                        "Weather Code": weather_day.weather_code,
                    }
                )

            st.dataframe(
                forecast_rows,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No weather forecast data is available.")

    else:
        st.divider()
        st.markdown(
            '<div class="section-title">🌤️ Weather Forecast</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "Weather information is currently unavailable. "
            "The rest of your travel plan can still be used."
        )

    # =================================================
    # Expense Dashboard
    # =================================================

    if travel_plan.expenses is not None:

        st.divider()
        st.markdown(
            '<div class="section-title">💰 Expense Dashboard</div>',
            unsafe_allow_html=True,
        )

        expenses = travel_plan.expenses
        breakdown = expenses.breakdown

        budget = float(expenses.budget)
        total_cost = float(expenses.total_cost)
        remaining = float(expenses.remaining_budget)
        utilization = float(
            expenses.budget_utilization_percentage
        )

        # ---------------------------------------------
        # Expense Summary Cards
        # ---------------------------------------------

        expense_col1, expense_col2, expense_col3, expense_col4 = (
            st.columns(4)
        )

        with expense_col1:
            st.metric(
                "💰 Budget",
                f"₹{budget:,.0f}",
            )

        with expense_col2:
            st.metric(
                "📊 Estimated Cost",
                f"₹{total_cost:,.0f}",
            )

        with expense_col3:
            if remaining >= 0:
                st.metric(
                    "💵 Remaining",
                    f"₹{remaining:,.0f}",
                )
            else:
                st.metric(
                    "⚠️ Over Budget",
                    f"₹{abs(remaining):,.0f}",
                )

        with expense_col4:
            st.metric(
                "📈 Utilization",
                f"{utilization:.1f}%",
            )

        # ---------------------------------------------
        # Budget Status
        # ---------------------------------------------

        if expenses.budget_status == "Within Budget":
            st.success(
                f"✅ Estimated trip cost is within your budget. "
                f"₹{remaining:,.0f} remains available."
            )
        else:
            over_budget = abs(remaining)
            st.warning(
                f"⚠️ Estimated trip cost exceeds your budget "
                f"by ₹{over_budget:,.0f}."
            )

        # ---------------------------------------------
        # Budget Utilization
        # ---------------------------------------------

        st.markdown("#### 📊 Budget Utilization")

        progress_value = min(
            max(utilization / 100, 0.0),
            1.0,
        )

        st.progress(progress_value)

        st.caption(
            f"₹{total_cost:,.0f} estimated out of "
            f"₹{budget:,.0f} budget "
            f"({utilization:.1f}% utilized)"
        )

        # ---------------------------------------------
        # Budget vs Estimated Cost
        # ---------------------------------------------

        st.markdown("#### 🎯 Budget vs Estimated Cost")

        comparison_col1, comparison_col2 = st.columns(2)

        with comparison_col1:
            st.metric(
                "💰 Planned Budget",
                f"₹{budget:,.0f}",
            )

        with comparison_col2:
            difference = total_cost - budget

            if difference > 0:
                delta_text = f"₹{difference:,.0f} over budget"
            elif difference < 0:
                delta_text = f"₹{abs(difference):,.0f} under budget"
            else:
                delta_text = "Within budget"

            st.metric(
                "📊 Estimated Trip Cost",
                f"₹{total_cost:,.0f}",
                delta=delta_text,
                delta_color="inverse",
            )

        # ---------------------------------------------
        # Expense Breakdown Data
        # ---------------------------------------------

        expense_rows = [
            {
                "Category": "Hotel",
                "Estimated Cost": float(
                    breakdown.hotel_cost
                ),
            },
            {
                "Category": "Food",
                "Estimated Cost": float(
                    breakdown.food_cost
                ),
            },
            {
                "Category": "Transportation",
                "Estimated Cost": float(
                    breakdown.transportation_cost
                ),
            },
            {
                "Category": "Activities",
                "Estimated Cost": float(
                    breakdown.activities_cost
                ),
            },
            {
                "Category": "Miscellaneous",
                "Estimated Cost": float(
                    breakdown.miscellaneous_cost
                ),
            },
        ]

        # ---------------------------------------------
        # Chart + Table
        # ---------------------------------------------

        chart_col, table_col = st.columns([1.25, 1])

        with chart_col:
            st.markdown(
                "#### 📊 Expense Breakdown Chart"
            )

            chart_data = {
                row["Category"]: row["Estimated Cost"]
                for row in expense_rows
                if row["Estimated Cost"] > 0
            }

            if chart_data:
                st.bar_chart(
                    chart_data,
                    use_container_width=True,
                )
            else:
                st.info(
                    "No expense breakdown data is available."
                )

        with table_col:
            st.markdown(
                "#### 📋 Expense Breakdown"
            )

            table_rows = []

            for row in expense_rows:
                amount = row["Estimated Cost"]

                percentage = (
                    (amount / total_cost * 100)
                    if total_cost > 0
                    else 0
                )

                table_rows.append(
                    {
                        "Category": row["Category"],
                        "Estimated": f"₹{amount:,.0f}",
                        "Share": f"{percentage:.1f}%",
                    }
                )

            st.dataframe(
                table_rows,
                use_container_width=True,
                hide_index=True,
            )

        # ---------------------------------------------
        # Highest Expense Category
        # ---------------------------------------------

        highest_expense = max(
            expense_rows,
            key=lambda row: row["Estimated Cost"],
        )

        highest_percentage = (
            (
                highest_expense["Estimated Cost"]
                / total_cost
                * 100
            )
            if total_cost > 0
            else 0
        )

        st.info(
            f"💡 **Highest expense category:** "
            f"{highest_expense['Category']} — "
            f"₹{highest_expense['Estimated Cost']:,.0f} "
            f"({highest_percentage:.1f}% of estimated cost)."
        )

        st.caption(
            "ℹ️ These figures are estimated costs generated by "
            "the current travel-planning workflow. "
            "Actual expense tracking will be added separately."
        )

    else:
        st.divider()
        st.markdown(
            '<div class="section-title">💰 Expense Dashboard</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "Expense estimation is currently unavailable."
        )

    # Packing Checklist
    # =================================================

    if travel_plan.packing is not None:

        st.divider()
        st.markdown(
            '<div class="section-title">🎒 Packing Checklist</div>',
            unsafe_allow_html=True,
        )

        packing = travel_plan.packing

        packing_col1, packing_col2 = st.columns(2)

        with packing_col1:
            st.metric(
                "📍 Destination",
                packing.destination,
            )

        with packing_col2:
            st.metric(
                "📅 Trip Duration",
                f"{packing.days} days",
            )

        if packing.items:

            st.caption(
                "Tick each item as you pack. Your checklist is kept "
                "during the current Streamlit session."
            )

            for index, item in enumerate(
                packing.items,
                start=1,
            ):

                checked = st.checkbox(
                    f"{item.item} × {item.quantity}",
                    key=f"packing_{index}_{item.item}",
                )

                if checked:
                    st.caption(
                        f"✅ {item.category} — {item.reason}"
                    )
                else:
                    st.caption(
                        f"🏷️ {item.category} — {item.reason}"
                    )

        else:
            st.info("No packing items were generated.")

    else:
        st.divider()
        st.markdown(
            '<div class="section-title">🎒 Packing Checklist</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "Packing recommendations are currently unavailable."
        )

    # =================================================
    # Maps / Routes
    # =================================================

    st.divider()
    st.markdown(
        '<div class="section-title">🗺️ Maps & Routes</div>',
        unsafe_allow_html=True,
    )

    if travel_plan.routes:

        st.caption(
            f"{len(travel_plan.routes)} route(s) generated "
            "from consecutive itinerary locations."
        )

        for index, route in enumerate(
            travel_plan.routes,
            start=1,
        ):

            origin_name = route.origin.name
            destination_name = route.destination.name

            with st.expander(
                f"🗺️ Route {index}: "
                f"{origin_name} → {destination_name}",
                expanded=index == 1,
            ):

                route_col1, route_col2, route_col3 = st.columns(3)

                with route_col1:
                    st.metric(
                        "📏 Distance",
                        route.distance_text,
                    )

                with route_col2:
                    st.metric(
                        "⏱️ Duration",
                        route.duration_text,
                    )

                with route_col3:
                    st.metric(
                        "🚗 Travel Mode",
                        "Driving",
                    )

                st.markdown("#### 📍 Origin")

                origin_col1, origin_col2 = st.columns(2)

                with origin_col1:
                    st.write(f"**{origin_name}**")

                with origin_col2:
                    st.caption("Coordinates")
                    st.write(
                        f"{route.origin.latitude:.6f}, "
                        f"{route.origin.longitude:.6f}"
                    )

                st.markdown("#### 🎯 Destination")

                destination_col1, destination_col2 = st.columns(2)

                with destination_col1:
                    st.write(f"**{destination_name}**")

                with destination_col2:
                    st.caption("Coordinates")
                    st.write(
                        f"{route.destination.latitude:.6f}, "
                        f"{route.destination.longitude:.6f}"
                    )

                st.markdown("#### 🗺️ Route Map")

                map_data = [
                    {
                        "lat": route.origin.latitude,
                        "lon": route.origin.longitude,
                    },
                    {
                        "lat": route.destination.latitude,
                        "lon": route.destination.longitude,
                    },
                ]

                st.map(
                    map_data,
                    zoom=10,
                )

    else:
        st.info(
            "📍 No routes could be generated from the "
            "itinerary locations. This can happen when "
            "a location cannot be geocoded or the routing "
            "service is temporarily unavailable."
        )

    # =================================================
    # Final Status
    # =================================================

    st.divider()
    st.success(
        "🎉 Your complete AI travel plan is ready!"
    )

else:

    # =================================================
    # Empty State
    # =================================================

    st.info(
        "👈 Enter your destination, budget, trip duration and "
        "start date in the sidebar, then click "
        "**Generate Travel Plan**."
    )

    st.markdown(
        """
        ### ✨ What this planner can generate

        - 🗓️ AI-generated day-by-day itinerary
        - 🏨 Hotel recommendations
        - 🍴 Restaurant recommendations
        - 🌤️ Weather forecast
        - 💰 Expense estimate
        - 🎒 Interactive packing checklist
        - 🗺️ Route information and map visualization
        """
    )
