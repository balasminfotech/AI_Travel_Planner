from tools.weather_tool import WeatherTool


def test_real_weather_tool():

    tool = WeatherTool()

    result = tool.get_forecast(
        "Goa",
        forecast_days=3,
    )

    print("\n")
    print("=" * 80)
    print("REAL WEATHER FORECAST")
    print("=" * 80)

    print(
        f"Location : {result.location}"
    )

    print(
        f"Latitude : {result.latitude}"
    )

    print(
        f"Longitude: {result.longitude}"
    )

    print(
        f"Timezone : {result.timezone}"
    )

    for day in result.days:

        print("\n" + "-" * 60)

        print(
            f"Date: {day.date}"
        )

        print(
            f"Weather Code: "
            f"{day.weather_code}"
        )

        print(
            f"Maximum Temperature: "
            f"{day.temperature_max} °C"
        )

        print(
            f"Minimum Temperature: "
            f"{day.temperature_min} °C"
        )

        print(
            f"Rain Probability: "
            f"{day.precipitation_probability}%"
        )

        print(
            f"Rain Amount: "
            f"{day.precipitation_sum} mm"
        )

    print("\n" + "=" * 80)

    assert result is not None

    assert result.location

    assert len(result.days) == 3