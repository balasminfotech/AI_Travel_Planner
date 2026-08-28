from tools.maps_tool import MapsTool


def test_real_geocoding():

    tool = MapsTool()

    result = tool.geocode(
        "Chennai, India"
    )

    print("\n")
    print("=" * 80)
    print("REAL GEOCODING RESULT")
    print("=" * 80)

    print(
        f"Name: {result.name}"
    )

    print(
        f"Latitude: {result.latitude}"
    )

    print(
        f"Longitude: {result.longitude}"
    )

    print("=" * 80)

    assert result is not None

    assert result.latitude

    assert result.longitude


def test_real_route():

    tool = MapsTool()

    result = tool.route(
        origin="Chennai, India",
        destination="Pondicherry, India",
    )

    print("\n")
    print("=" * 80)
    print("REAL ROUTE RESULT")
    print("=" * 80)

    print(
        tool.format_route(result)
    )

    print("=" * 80)

    assert result is not None

    assert result.distance_km > 0

    assert result.duration_minutes > 0

    assert result.distance_text

    assert result.duration_text