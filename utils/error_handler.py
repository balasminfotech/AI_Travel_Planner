from __future__ import annotations


def friendly_error_message(
    component: str,
    exc: Exception,
) -> str:
    """
    Convert common API/LLM/network failures into concise,
    user-friendly messages suitable for the Streamlit UI.

    The original exception is intentionally not exposed to users.
    """

    component_name = component.strip() or "Service"
    raw = str(exc).lower()

    if (
        "429" in raw
        or "resource_exhausted" in raw
        or "quota" in raw
        or "rate limit" in raw
        or "rate_limit" in raw
    ):
        return (
            f"{component_name} is temporarily rate-limited "
            "or its API quota has been reached."
        )

    if (
        "503" in raw
        or "unavailable" in raw
        or "service unavailable" in raw
    ):
        return (
            f"{component_name} is temporarily unavailable."
        )

    if (
        "timeout" in raw
        or "timed out" in raw
        or "readtimeout" in raw
        or "connecttimeout" in raw
    ):
        return (
            f"{component_name} did not respond in time."
        )

    if (
        "validation" in raw
        or "pydantic" in raw
        or "json" in raw
        or "parse" in raw
        or "schema" in raw
    ):
        return (
            f"{component_name} returned an invalid response "
            "that could not be processed."
        )

    if (
        "location not found" in raw
        or "geocod" in raw
    ):
        return (
            f"{component_name} could not resolve one or more "
            "locations."
        )

    return (
        f"{component_name} could not complete this part "
        "of the travel plan."
    )
