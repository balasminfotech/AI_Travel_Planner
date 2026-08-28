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
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
)

# =====================================================
# Page Header
# =====================================================

st.title("✈️ AI Travel Planner")
st.write(
    "Plan your trip using AI-powered multi-agent workflow."
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

    All specialized agents and tools are created here and
    injected into the Master Agent.
    """

    planning_agent = PlanningAgent()
    itinerary_agent = ItineraryAgent()
    hotel_agent = HotelAgent()
    restaurant_agent = RestaurantAgent()
    packing_agent = PackingAgent()

    weather_tool = WeatherTool()
    expense_tool = ExpenseTool()
    maps_tool = MapsTool()

    master_agent = MasterTravelPlannerAgent(
        planning_agent=planning_agent,
        itinerary_agent=itinerary_agent,
        hotel_agent=hotel_agent,
        restaurant_agent=restaurant_agent,
        weather_tool=weather_tool,
        expense_tool=expense_tool,
        packing_agent=packing_agent,
        maps_tool=maps_tool,
    )

    return master_agent

# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("✈️ Travel Details")

# =====================================================
# Destination
# =====================================================

destination = st.sidebar.text_input(
    "📍 Destination",
    placeholder="Example: Goa",
)

# =====================================================
# Budget
# =====================================================

budget = st.sidebar.number_input(
    "💰 Budget (₹)",
    min_value=1000.0,
    value=30000.0,
    step=1000.0,
)

# =====================================================
# Number of Days
# =====================================================

days = st.sidebar.number_input(
    "📅 Number of Days",
    min_value=1,
    max_value=30,
    value=3,
    step=1,
)

# =====================================================
# Start Date
# =====================================================

start_date = st.sidebar.date_input(
    "📅 Start Date",
    value=date.today(),
)

# =====================================================
# Generate Button
# =====================================================

generate_plan = st.sidebar.button(
    "🚀 Generate Travel Plan",
    type="primary",
)

# =====================================================
# Input Validation + Plan Generation
# =====================================================

if generate_plan:

    # -------------------------------------------------
    # Validate Destination
    # -------------------------------------------------

    if not destination.strip():
        st.error("Please enter a destination.")
        st.stop()

    # -------------------------------------------------
    # Validate Budget
    # -------------------------------------------------

    if budget <= 0:
        st.error("Budget must be greater than zero.")
        st.stop()

    # -------------------------------------------------
    # Validate Number of Days
    # -------------------------------------------------

    if days <= 0:
        st.error("Number of days must be greater than zero.")
        st.stop()

    # -------------------------------------------------
    # Create Travel Request
    # -------------------------------------------------

    travel_request = TravelRequest(
        destination=destination.strip(),
        budget=budget,
        days=days,
        start_date=start_date,
    )

    # -------------------------------------------------
    # Save Travel Request
    # -------------------------------------------------

    st.session_state.travel_request = travel_request

    # -------------------------------------------------
    # Clear Previous Travel Plan
    # -------------------------------------------------

    st.session_state.travel_plan = None

    # -------------------------------------------------
    # Display Travel Request
    # -------------------------------------------------

    st.success("Travel request created successfully!")

    st.subheader("📋 Travel Request")

    # IMPORTANT:
    # Four columns require st.columns(4), not st.columns(3).
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Destination",
            travel_request.destination,
        )

    with col2:
        st.metric(
            "Budget",
            f"₹{travel_request.budget:,.0f}",
        )

    with col3:
        st.metric(
            "Days",
            travel_request.days,
        )

    with col4:
        st.metric(
            "Date",
            travel_request.start_date.strftime("%d-%m-%Y"),
        )

    # -------------------------------------------------
    # Create Master Agent
    # -------------------------------------------------

    master_agent = create_master_agent()

    # -------------------------------------------------
    # Generate Complete Travel Plan
    # -------------------------------------------------

    try:

        with st.spinner(
            "🤖 AI is creating your complete travel plan..."
        ):

            travel_plan = master_agent.create_travel_plan(
                travel_request
            )

        # ---------------------------------------------
        # Save Generated Plan
        # ---------------------------------------------

        st.session_state.travel_plan = travel_plan

        # ---------------------------------------------
        # Success Message
        # ---------------------------------------------

        st.success(
            "🎉 Travel plan generated successfully!"
        )

    except Exception as exc:

        st.error(
            "❌ Unable to generate the travel plan."
        )

        st.exception(exc)

# =====================================================
# Display Generated Travel Plan
# =====================================================

if st.session_state.travel_plan is not None:

    travel_plan = st.session_state.travel_plan

    # =================================================
    # Travel Plan Header
    # =================================================

    st.divider()
    st.header("🌍 Complete Travel Plan")

    # =================================================
    # Trip Summary
    # =================================================

    st.subheader("📊 Trip Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric(
            "📍 Destination",
            travel_plan.destination,
        )

    with summary_col2:
        st.metric(
            "💰 Budget",
            f"₹{travel_plan.budget:,.0f}",
        )

    with summary_col3:
        st.metric(
            "📅 Days",
            travel_plan.days,
        )

    # =================================================
    # Itinerary
    # =================================================

    if travel_plan.itinerary is not None:

        st.divider()
        st.header("🗓️ Day-by-Day Itinerary")

        itinerary = travel_plan.itinerary

        for day_plan in itinerary.days:

            with st.expander(
                f"📅 Day {day_plan.day} — {day_plan.theme}",
                expanded=True,
            ):

                if hasattr(day_plan, "date"):
                    st.caption(
                        f"Date: {day_plan.date}"
                    )

                # -------------------------------------
                # Activities
                # -------------------------------------

                for activity in day_plan.activities:

                    st.markdown(
                        f"### 🕐 {activity.time} — {activity.title}"
                    )

                    st.write(activity.description)

                    st.markdown(
                        f"📍 **Location:** {activity.location}"
                    )

                    st.markdown(
                        f"💰 **Estimated Cost:** "
                        f"₹{activity.estimated_cost:,.0f}"
                    )

                    st.divider()

                # -------------------------------------
                # Daily Cost
                # -------------------------------------

                st.markdown(
                    f"**💰 Estimated Daily Cost:** "
                    f"₹{day_plan.estimated_daily_cost:,.0f}"
                )

    # =================================================
    # Hotel Recommendations
    # =================================================

    if travel_plan.hotels is not None:

        st.divider()
        st.header("🏨 Hotel Recommendations")

        hotels = travel_plan.hotels

        for index, hotel in enumerate(
            hotels.hotels,
            start=1,
        ):

            with st.expander(
                f"🏨 {index}. {hotel.name}",
                expanded=False,
            ):

                st.markdown(
                    f"📍 **Location:** {hotel.location}"
                )

                st.markdown(
                    f"⭐ **Rating:** {hotel.rating}/5"
                )

                st.markdown(
                    f"🏷️ **Category:** {hotel.category}"
                )

                st.markdown(
                    f"💰 **Price per Night:** "
                    f"₹{hotel.price_per_night:,.0f}"
                )

                st.markdown(
                    f"💰 **Estimated Total Stay:** "
                    f"₹{hotel.total_stay_cost:,.0f}"
                )

                st.write(hotel.description)

    # =================================================
    # Restaurant Recommendations
    # =================================================

    if travel_plan.restaurants is not None:

        st.divider()
        st.header("🍴 Restaurant Recommendations")

        restaurants = travel_plan.restaurants

        for index, restaurant in enumerate(
            restaurants.restaurants,
            start=1,
        ):

            with st.expander(
                f"🍴 {index}. {restaurant.name}",
                expanded=False,
            ):

                st.markdown(
                    f"📍 **Location:** {restaurant.location}"
                )

                st.markdown(
                    f"🍛 **Cuisine:** {restaurant.cuisine}"
                )

                st.markdown(
                    f"💵 **Price Level:** {restaurant.price_level}"
                )

                st.markdown(
                    f"💰 **Average Cost per Person:** "
                    f"₹{restaurant.average_cost_per_person:,.0f}"
                )

                st.markdown(
                    f"⭐ **Rating:** {restaurant.rating}/5"
                )

                st.markdown(
                    f"🎯 **Best For:** {restaurant.best_for}"
                )

                st.write(restaurant.description)

    # =================================================
    # Weather Forecast
    # =================================================

    if travel_plan.weather is not None:

        st.divider()
        st.header("🌤️ Weather Forecast")

        weather = travel_plan.weather

        st.markdown(
            f"📍 **Location:** {weather.location}"
        )

        st.markdown(
            f"🌐 **Timezone:** {weather.timezone}"
        )

        weather_col1, weather_col2 = st.columns(2)

        with weather_col1:
            st.metric(
                "Latitude",
                f"{weather.latitude:.4f}",
            )

        with weather_col2:
            st.metric(
                "Longitude",
                f"{weather.longitude:.4f}",
            )

        st.subheader("📅 Daily Forecast")

        for weather_day in weather.days:

            with st.expander(
                f"🌤️ {weather_day.date}",
                expanded=False,
            ):

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🌡️ Max Temperature",
                        f"{weather_day.temperature_max}°C",
                    )

                with col2:
                    st.metric(
                        "🌡️ Min Temperature",
                        f"{weather_day.temperature_min}°C",
                    )

                with col3:
                    st.metric(
                        "🌧️ Rain Probability",
                        f"{weather_day.precipitation_probability}%",
                    )

                st.markdown(
                    f"🌧️ **Precipitation:** "
                    f"{weather_day.precipitation_sum} mm"
                )

                st.markdown(
                    f"🌤️ **Weather Code:** "
                    f"{weather_day.weather_code}"
                )

    # =================================================
    # Expense Estimate
    # =================================================

    if travel_plan.expenses is not None:

        st.divider()
        st.header("💰 Expense Estimate")

        expenses = travel_plan.expenses
        breakdown = expenses.breakdown

        # ---------------------------------------------
        # Main Expense Metrics
        # ---------------------------------------------

        expense_col1, expense_col2, expense_col3 = (
            st.columns(3)
        )

        with expense_col1:
            st.metric(
                "💰 Total Estimated Cost",
                f"₹{expenses.total_cost:,.0f}",
            )

        with expense_col2:
            st.metric(
                "💵 Remaining Budget",
                f"₹{expenses.remaining_budget:,.0f}",
            )

        with expense_col3:
            st.metric(
                "📊 Budget Utilization",
                f"{expenses.budget_utilization_percentage:.1f}%",
            )

        # ---------------------------------------------
        # Budget Status
        # ---------------------------------------------

        if expenses.budget_status == "Within Budget":
            st.success(
                "✅ Trip is within your budget."
            )
        else:
            st.warning(
                "⚠️ Estimated trip cost exceeds your budget."
            )

        # ---------------------------------------------
        # Expense Breakdown
        # ---------------------------------------------

        st.subheader("📋 Expense Breakdown")

        expense_data = {
            "Category": [
                "Hotel",
                "Food",
                "Transportation",
                "Activities",
                "Miscellaneous",
            ],
            "Estimated Cost": [
                breakdown.hotel_cost,
                breakdown.food_cost,
                breakdown.transportation_cost,
                breakdown.activities_cost,
                breakdown.miscellaneous_cost,
            ],
        }

        st.table(expense_data)

    # =================================================
    # Packing Checklist
    # =================================================

    if travel_plan.packing is not None:

        st.divider()
        st.header("🎒 Packing Checklist")

        packing = travel_plan.packing

        st.markdown(
            f"📍 **Destination:** {packing.destination}"
        )

        st.markdown(
            f"📅 **Trip Duration:** {packing.days} days"
        )

        for index, item in enumerate(
            packing.items,
            start=1,
        ):

            st.markdown(
                f"**{index}. ☐ {item.item}**"
            )

            st.markdown(
                f"&nbsp;&nbsp;&nbsp;🏷️ Category: {item.category}"
            )

            st.markdown(
                f"&nbsp;&nbsp;&nbsp;🔢 Quantity: {item.quantity}"
            )

            st.markdown(
                f"&nbsp;&nbsp;&nbsp;💡 Reason: {item.reason}"
            )

    # =================================================
    # Maps / Routes
    # =================================================

    if travel_plan.routes:

        st.divider()
        st.header("📍 Maps & Routes")

        for index, route in enumerate(
            travel_plan.routes,
            start=1,
        ):

            with st.expander(
                f"🗺️ Route {index}",
                expanded=False,
            ):

                st.markdown(
                    f"📍 **Origin:** {route.origin.name}"
                )

                st.markdown(
                    f"📍 **Destination:** {route.destination.name}"
                )

                st.markdown(
                    f"📏 **Distance:** {route.distance_text}"
                )

                st.markdown(
                    f"⏱️ **Estimated Duration:** "
                    f"{route.duration_text}"
                )

                # -------------------------------------
                # Coordinates
                # -------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.caption("Origin Coordinates")

                    st.write(
                        f"Latitude: {route.origin.latitude}"
                    )

                    st.write(
                        f"Longitude: {route.origin.longitude}"
                    )

                with col2:

                    st.caption("Destination Coordinates")

                    st.write(
                        f"Latitude: {route.destination.latitude}"
                    )

                    st.write(
                        f"Longitude: {route.destination.longitude}"
                    )

    else:

        st.info("📍 No routes were generated.")

    # =================================================
    # Final Summary
    # =================================================

    st.divider()

    st.success(
        "🎉 Your complete AI travel plan is ready!"
    )
