from typing import Any

import requests

from config.settings import (
    MAPS_GEOCODING_URL,
    MAPS_REQUEST_TIMEOUT,
    MAPS_ROUTING_URL,
    MAPS_USER_AGENT,
)

from models.maps import (
    Location,
    RouteResult,
)


class MapsTool:
    """
    Tool for geocoding locations and calculating routes.
    
    Uses:
    - OpenStreetMap Nominatim for geocoding
    - OSRM for routing
    """

    NOMINATIM_URL = (
        MAPS_GEOCODING_URL
    )

    OSRM_URL = (
        MAPS_ROUTING_URL
    )

    USER_AGENT = (
        "AI-Travel-Planner/1.0 "
        "(travel-planner-project)"
    )

    def __init__(
        self,
        timeout: int = 10,
    ):
        self.timeout = timeout

    def geocode(
        self,
        place: str,
    ) -> Location:

        if not place or not place.strip():
            raise ValueError(
                "Place cannot be empty."
            )

        params = {
            "q": place,
            "format": "json",
            "limit": 1,
        }

        headers = {
            "User-Agent": self.USER_AGENT,
        }

        response = requests.get(
            self.NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError(
                f"Location not found: {place}"
            )

        result = data[0]

        return Location(
            name=result.get(
                "display_name",
                place,
            ),
            latitude=float(
                result["lat"]
            ),
            longitude=float(
                result["lon"]
            ),
        )

    def route(
        self,
        origin: str,
        destination: str,
    ) -> RouteResult:

        origin_location = self.geocode(
            origin
        )

        destination_location = self.geocode(
            destination
        )

        return self.route_from_coordinates(
            origin=origin_location,
            destination=destination_location,
        )

    def route_from_coordinates(
        self,
        origin: Location,
        destination: Location,
    ) -> RouteResult:

        coordinates = (
            f"{origin.longitude},"
            f"{origin.latitude};"
            f"{destination.longitude},"
            f"{destination.latitude}"
        )

        url = (
            f"{self.OSRM_URL}/{coordinates}"
        )

        params = {
            "overview": "false",
        }

        response = requests.get(
            url,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data: dict[str, Any] = response.json()

        if data.get("code") != "Ok":
            raise ValueError(
                "Unable to calculate route."
            )

        routes = data.get("routes", [])

        if not routes:
            raise ValueError(
                "No route found."
            )

        route = routes[0]

        distance_meters = float(
            route["distance"]
        )

        duration_seconds = float(
            route["duration"]
        )

        distance_km = (
            distance_meters / 1000
        )

        duration_minutes = (
            duration_seconds / 60
        )

        return RouteResult(
            origin=origin,
            destination=destination,
            distance_km=distance_km,
            duration_minutes=duration_minutes,
            distance_text=self._format_distance(
                distance_km
            ),
            duration_text=self._format_duration(
                duration_minutes
            ),
        )

    @staticmethod
    def _format_distance(
        distance_km: float,
    ) -> str:

        return (
            f"{distance_km:.1f} km"
        )

    @staticmethod
    def _format_duration(
        duration_minutes: float,
    ) -> str:

        total_minutes = round(
            duration_minutes
        )

        hours = total_minutes // 60

        minutes = total_minutes % 60

        if hours == 0:
            return f"{minutes} minutes"

        if minutes == 0:
            return (
                f"{hours} hours"
            )

        return (
            f"{hours} hours "
            f"{minutes} minutes"
        )

    @staticmethod
    def format_route(
        result: RouteResult,
    ) -> str:

        return (
            "\n"
            "========================================\n"
            "TRAVEL ROUTE\n"
            "========================================\n"
            f"Origin: "
            f"{result.origin.name}\n"
            f"Destination: "
            f"{result.destination.name}\n"
            f"Distance: "
            f"{result.distance_text}\n"
            f"Duration: "
            f"{result.duration_text}\n"
            "========================================"
        )