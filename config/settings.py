import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-flash-lite-latest"
)

TEMPERATURE = float(
    os.getenv(
        "TEMPERATURE",
        "0.3"
    )
)


# Application configuration
APP_NAME = "AI Travel Planner"
APP_VERSION = "1.0.0"


# Report configuration
REPORTS_DIR = "reports"


# Logging configuration
LOGS_DIR = "logs"
LOG_FILE = "logs/app.log"


# Validation
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to the .env file."
    )