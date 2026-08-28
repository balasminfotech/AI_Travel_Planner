# ✈️ AI Travel Planner

<p align="center">
  <strong>AI-powered multi-agent travel planning application built with Python, Streamlit, Google Gemini, and Pydantic.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Google-Gemini-4285F4?logo=google&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Pydantic-Data%20Validation-E92063?logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</p>

---

## 🌍 Overview

**AI Travel Planner** creates a complete, personalized travel plan from a destination, budget, trip duration, and start date.

The application uses a **multi-agent architecture** in which specialized agents handle different parts of trip planning, while the **Master Travel Planner Agent** coordinates the overall workflow.

### ✨ What It Generates

- 🗓️ Day-by-day itinerary
- 🏨 Hotel recommendations
- 🍴 Restaurant recommendations
- 🌤️ Weather forecast
- 💰 Expense estimation
- 🎒 Packing checklist
- 📍 Maps and route information

---

The application generates a complete travel plan based on the user's destination, budget, number of days, and start date.

It combines multiple specialized AI agents and tools to generate:

- 🗓️ Day-by-day itinerary
- 🏨 Hotel recommendations
- 🍴 Restaurant recommendations
- 🌤️ Weather forecast
- 💰 Expense estimation
- 🎒 Packing checklist
- 📍 Maps and route information

---


## 🚀 Features

##### 1. 📋 Travel Request

Users can provide:

* Destination
* Budget
* Number of days
* Start date

The request is validated using a Pydantic model.

---

##### 2. 🤖 Multi-Agent Travel Planning

The application uses multiple specialized agents.

##### Planning Agent

Creates the overall travel plan structure.

##### Itinerary Agent

Generates a day-by-day itinerary with:

* Time
* Activity
* Description
* Location
* Estimated cost
* Daily estimated cost

##### Hotel Agent

Provides hotel recommendations including:

* Hotel name
* Location
* Price per night
* Total stay cost
* Rating
* Category
* Description

##### Restaurant Agent

Provides restaurant recommendations including:

* Restaurant name
* Location
* Cuisine
* Price level
* Average cost
* Rating
* Best for
* Description

##### Packing Agent

Creates a destination-specific packing checklist.

##### Master Travel Planner Agent

Coordinates all specialized agents and tools to produce the complete travel plan.

---

## 🛠️ Tools

The project contains several supporting tools.

### 🌤️ Weather Tool

Provides weather forecast information including:

* Location
* Latitude
* Longitude
* Timezone
* Weather code
* Maximum temperature
* Minimum temperature
* Precipitation probability
* Precipitation amount

---

### 💰 Expense Tool

Calculates estimated travel expenses.

Expense categories include:

* Hotel
* Food
* Transportation
* Activities
* Miscellaneous

The application also calculates:

* Total estimated cost
* Remaining budget
* Budget utilization percentage
* Budget status

---

### 📍 Maps Tool

Provides location and route information.

It supports:

* Geocoding
* Route calculation
* Distance calculation
* Duration calculation
* Route formatting

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Master Travel Planner Agent
  │
  ├── Planning Agent
  │
  ├── Itinerary Agent
  │
  ├── Hotel Agent
  │
  ├── Restaurant Agent
  │
  ├── Packing Agent
  │
  ├── Weather Tool
  │
  ├── Expense Tool
  │
  └── Maps Tool
  │
  ▼
Complete Travel Plan
```

---

## 📁 Project Structure

```text
AI_Travel_Planner/
│
├── agents/
│   ├── __init__.py
│   ├── hotel_agent.py
│   ├── itinerary_agent.py
│   ├── master_travel_agent.py
│   ├── packing_agent.py
│   ├── planning_agent.py
│   ├── restaurant_agent.py
│   └── travel_agent.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── logs/
│   └── app.log
│
├── models/
│   ├── __init__.py
│   ├── expense.py
│   ├── hotel.py
│   ├── itinerary.py
│   ├── maps.py
│   ├── master_travel_plan.py
│   ├── packing.py
│   ├── planning.py
│   ├── restaurant.py
│   ├── travel_plan.py
│   ├── travel_request.py
│   └── weather.py
│
├── reports/
│
├── screenshots/
│
├── tests/
│   ├── __init__.py
│   ├── test_hotel_agent.py
│   ├── test_hotel_model.py
│   ├── test_expense_demo.py
│   ├── test_expense_model.py
│   ├── test_expense_tool.py
│   ├── test_gemini_hotel_agent.py
│   ├── test_gemini_itinerary_agent.py
│   ├── test_gemini_packing_agent.py
│   ├── test_gemini_planning_agent.py
│   ├── test_gemini_restaurant_agent.py
│   ├── test_gemini_travel_agent.py
│   ├── test_itinerary_agent.py
│   ├── test_itinerary_validation.py
│   ├── test_maps_model.py
│   ├── test_maps_tool.py
│   ├── test_master_agent_initialization.py
│   ├── test_master_travel_agent.py
│   ├── test_master_workflow.py
│   ├── test_models.py
│   ├── test_packing_agent.py
│   ├── test_packing_model.py
│   ├── test_planning_agent.py
│   ├── test_real_maps_tool.py
│   ├── test_real_weather_tool.py
│   ├── test_restaurant_agent.py
│   ├── test_restaurant_model.py
│   ├── test_settings.py
│   ├── test_travel_agent.py
│   ├── test_weather_model.py
│   ├── test_weather_tool.py
│   └── test_weather_tool_forecast.py
│
├── tools/
│   ├── __init__.py
│   ├── expense_tool.py
│   ├── maps_tool.py
│   └── weather_tool.py
│
├── utils/
│   ├── __init__.py
│   └── logger.py
│
├── .env
├── .gitignore
├── app.py
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 💻 Technologies Used

| Technology    | Purpose                               |
| ------------- | ------------------------------------- |
| Python        | Core programming language             |
| Streamlit     | Web application UI                    |
| Google Gemini | Generative AI                         |
| Pydantic      | Data validation and structured models |
| Pytest        | Automated testing                     |
| Requests      | API communication                     |
| Python-dotenv | Environment variable management       |
| Git           | Version control                       |
| GitHub        | Source code repository                |

---

## 🧠 AI Architecture

The project follows a **multi-agent architecture**.

Instead of using one AI component for the entire task, different agents are responsible for different parts of travel planning.

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit App     │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ Master Travel Planner    │
                 │         Agent            │
                 └────────────┬─────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
   Planning Agent     Itinerary Agent       Hotel Agent
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
 Restaurant Agent      Packing Agent        Weather Tool
                              │
                              ▼
                         Expense Tool
                              │
                              ▼
                          Maps Tool
                              │
                              ▼
                  Complete Travel Plan
```

---

## 🔗 Repository

**GitHub:** https://github.com/balasminfotech/AI_Travel_Planner

---

## ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/balasminfotech/AI_Travel_Planner.git
```

Navigate to the project directory:

```bash
cd AI_Travel_Planner
```

---

# 🐍 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

# 📦 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# 🔐 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit your `.env` file to GitHub.

The `.gitignore` file should contain:

```text
.env
venv/
__pycache__/
.pytest_cache/
*.pyc
logs/*.log
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually it will be available at:

```text
http://localhost:8501
```

---

## 🧪 Running Tests

The project includes automated tests for:

* Models
* Agents
* Tools
* Master agent
* Weather
* Maps
* Expense calculation
* Packing
* Settings
* Gemini integrations

Run all tests:

```bash
python -m pytest -v
```

Expected result:

```text
85 passed
```

Run the model tests:

```bash
python -m pytest tests/test_models.py -v
```

Expected result:

```text
8 passed
```

---

## 📊 Example Output

The application generates a complete travel plan containing:

```text
🌍 Complete Travel Plan

📊 Trip Summary

Destination: Goa
Budget: ₹30,000
Days: 3

🗓️ Day-by-Day Itinerary

Day 1
- Visit Aguada Fort
- Lunch at Beachside Shack
- Explore Fontainhas
- Mandovi River Cruise

Day 2
- Basilica of Bom Jesus
- Spice Plantation
- Colva Beach
- Heritage Restaurant

Day 3
- Anjuna Flea Market
- Lunch
- Chapora Fort

🏨 Hotel Recommendations

🍴 Restaurant Recommendations

🌤️ Weather Forecast

💰 Expense Estimate

🎒 Packing Checklist

📍 Maps & Routes
```

---

## 💰 Expense Calculation

The Expense Tool calculates the total estimated travel cost.

Example:

```text
Hotel             ₹30,000
Food               ₹3,000
Transportation     ₹1,500
Activities         ₹7,200
Miscellaneous      ₹1,500
--------------------------------
Total              ₹43,200
```

The application also calculates:

```text
Budget:              ₹30,000
Estimated Cost:      ₹43,200
Remaining Budget:   -₹13,200
Utilization:          144%
Status:              Over Budget
```

---

## 🔒 Security

API keys and sensitive configuration values should be stored in environment variables.

Never commit the following to GitHub:

```text
.env
API keys
Passwords
Access tokens
Secret credentials
```

---

## 🧪 Testing Strategy

The project follows a structured testing approach.

##### Unit Tests

Tests individual:

* Models
* Agents
* Tools
* Utility functions

##### Integration Tests

Tests interaction between:

* Agents
* Tools
* Master Travel Planner
* Gemini API

##### Real API Tests

The project also contains tests for real integrations such as:

* Gemini
* Weather
* Maps

Make sure the required API configuration is available before running tests that access external services.

---

## 📈 Future Improvements

Possible future enhancements include:

* 🗺️ Interactive maps
* ✈️ Flight recommendations
* 🚆 Train and bus recommendations
* 🏨 Real-time hotel availability
* 🍴 Real-time restaurant availability
* 💳 Expense tracking
* 📄 PDF travel report generation
* 📥 Markdown report export
* 💾 Travel history
* 🔐 User authentication
* 🌐 Multi-language support
* 📱 Mobile-friendly interface
* ☁️ Cloud deployment
* 🧠 Long-term travel preferences
* 🔄 Re-planning based on weather conditions

---

## 🎯 Learning Objectives

This project demonstrates practical implementation of:

* Python
* Object-Oriented Programming
* Pydantic
* Generative AI
* Google Gemini
* Prompt Engineering
* Multi-Agent AI Architecture
* Tool Calling
* Streamlit
* API Integration
* Data Validation
* Automated Testing
* Git and GitHub
* Environment Variables
* Software Project Architecture

---

## 👨‍💻 Author

**Balasubramanian V**

Python / Django Developer | Agentic AI Engineer

GitHub: https://github.com/balasminfotech

---

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---
