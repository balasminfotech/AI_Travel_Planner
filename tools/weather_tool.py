from datetime import date, datetime, timedelta

import requests

from config.settings import (
    WEATHER_FORECAST_URL,
    WEATHER_GEOCODING_URL,
    WEATHER_REQUEST_TIMEOUT,
)

from models.weather import (
    WeatherDay,
    WeatherForecast,
)


KNOWN_INDIAN_LOCATIONS = {
    "goa": {
        "latitude": 15.4909,
        "longitude": 73.8278,
        "name": "Goa",
    },
    "chennai": {
        "latitude": 13.0827,
        "longitude": 80.2707,
        "name": "Chennai",
    },
    "bangalore": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "name": "Bangalore",
    },
    "bengaluru": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "name": "Bangalore",
    },
    "mumbai": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "name": "Mumbai",
    },
    "delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "name": "Delhi",
    },
    "new delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "name": "New Delhi",
    },
    "hyderabad": {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "name": "Hyderabad",
    },
    "kolkata": {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "name": "Kolkata",
    },
    "pune": {
        "latitude": 18.5204,
        "longitude": 73.8567,
        "name": "Pune",
    },
    "jaipur": {
        "latitude": 26.9124,
        "longitude": 75.7873,
        "name": "Jaipur",
    },
    "kochi": {
        "latitude": 9.9312,
        "longitude": 76.2673,
        "name": "Kochi",
    },
    "madurai": {
        "latitude": 9.9252,
        "longitude": 78.1198,
        "name": "Madurai",
    },
    "pondicherry": {
        "latitude": 11.9416,
        "longitude": 79.8083,
        "name": "Puducherry",
    },
    "puducherry": {
        "latitude": 11.9416,
        "longitude": 79.8083,
        "name": "Puducherry",
    },
}


class WeatherTool:
    """Tool for retrieving real weather forecast data."""

    GEOCODING_URL = WEATHER_GEOCODING_URL
    WEATHER_URL = WEATHER_FORECAST_URL

    def __init__(
        self,
        timeout: int | None = None,
    ):
        self.timeout = (
            timeout
            if timeout is not None
            else WEATHER_REQUEST_TIMEOUT
        )

    # =================================================
    # Geocoding
    # =================================================

    def _geocode(
        self,
        location: str,
    ) -> tuple[float, float, str]:

        search_location = location.strip()

        if not search_location:
            raise ValueError(
                "Location cannot be empty."
            )

        normalized_location = search_location.lower()

        # -------------------------------------------------
        # Production optimization:
        #
        # For common Indian destinations, use deterministic
        # coordinates immediately and avoid an unnecessary
        # external geocoding request.
        # -------------------------------------------------

        known_location = KNOWN_INDIAN_LOCATIONS.get(
            normalized_location
        )

        if known_location is not None:
            return (
                known_location["latitude"],
                known_location["longitude"],
                known_location["name"],
            )

        # -------------------------------------------------
        # Generic destination - Open-Meteo geocoding
        # -------------------------------------------------

        params = {
            "name": search_location,
            "count": 10,
            "language": "en",
            "format": "json",
        }

        response = requests.get(
            self.GEOCODING_URL,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "results",
            [],
        )

        if not results:
            raise ValueError(
                f"Location not found: {location}"
            )

        result = results[0]

        return (
            float(result["latitude"]),
            float(result["longitude"]),
            str(
                result.get(
                    "name",
                    location,
                )
            ),
        )

    # =================================================
    # Weather Forecast
    # =================================================

    def get_forecast(
        self,
        location: str,
        forecast_days: int = 7,
        start_date: date | str | None = None,
    ) -> WeatherForecast:

        if not location.strip():
            raise ValueError(
                "Location cannot be empty."
            )

        if not 1 <= forecast_days <= 16:
            raise ValueError(
                "forecast_days must be between "
                "1 and 16."
            )

        (
            latitude,
            longitude,
            resolved_name,
        ) = self._geocode(
            location
        )

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max,"
                "precipitation_sum"
            ),
            "timezone": "auto",
        }

        # -------------------------------------------------
        # Align weather dates with the requested trip.
        # -------------------------------------------------

        if start_date is not None:

            if isinstance(start_date, str):
                trip_start_date = datetime.strptime(
                    start_date,
                    "%Y-%m-%d",
                ).date()

            elif isinstance(start_date, datetime):
                trip_start_date = start_date.date()

            elif isinstance(start_date, date):
                trip_start_date = start_date

            else:
                raise ValueError(
                    "start_date must be a date, datetime, "
                    "YYYY-MM-DD string, or None."
                )

            trip_end_date = (
                trip_start_date
                + timedelta(days=forecast_days - 1)
            )

            params["start_date"] = (
                trip_start_date.isoformat()
            )

            params["end_date"] = (
                trip_end_date.isoformat()
            )

        else:
            params["forecast_days"] = forecast_days

        response = requests.get(
            self.WEATHER_URL,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        daily = data.get(
            "daily"
        )

        if not daily:
            raise ValueError(
                "Weather API returned no daily data."
            )

        dates = daily["time"]
        weather_codes = daily["weather_code"]
        temperature_max = daily[
            "temperature_2m_max"
        ]
        temperature_min = daily[
            "temperature_2m_min"
        ]
        precipitation_probability = daily[
            "precipitation_probability_max"
        ]
        precipitation_sum = daily[
            "precipitation_sum"
        ]

        days = []

        for index, forecast_date in enumerate(
            dates
        ):

            days.append(
                WeatherDay(
                    date=forecast_date,
                    weather_code=(
                        weather_codes[index]
                    ),
                    temperature_max=(
                        temperature_max[index]
                    ),
                    temperature_min=(
                        temperature_min[index]
                    ),
                    precipitation_probability=(
                        precipitation_probability[index]
                        or 0
                    ),
                    precipitation_sum=(
                        precipitation_sum[index]
                        or 0
                    ),
                )
            )

        return WeatherForecast(
            location=resolved_name,
            latitude=latitude,
            longitude=longitude,
            timezone=data.get(
                "timezone",
                "UTC",
            ),
            days=days,
        )
