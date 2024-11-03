import requests
from datetime import datetime, timedelta

def get_weather_data(start_point, end_point, forecast_period):
    if isinstance(end_point, tuple):
        end_point = ",".join(map(str, end_point))

    if isinstance(start_point, tuple):
        start_point = ",".join(map(str, start_point))

    today = datetime.now()
    start_forecast = []
    for day in range(forecast_period):
        weather = requests.get(
            "http://backend:5000/get_weather_forecast",
            params={
                "location": start_point,
                "date": (today + timedelta(days=day)).strftime("%Y-%m-%d"),
            },
        ).json()
        start_forecast.append(weather)

    end_forecast = []
    for day in range(forecast_period):
        weather = requests.get(
            "http://backend:5000/get_weather_forecast",
            params={
                "location": end_point,
                "date": (today + timedelta(days=day)).strftime("%Y-%m-%d"),
            },
        ).json()
        end_forecast.append(weather)

    return (
        f"<strong>{start_point}:</strong>\n{format_forecast(start_forecast)}\n\n"
        f"<strong>{end_point}:</strong>\n{format_forecast(end_forecast)}"
    )

def format_forecast(forecast):
    formatted_weathers = []
    for weather in forecast:
        if weather["status"] == "not_found":
            return "Error. Location not found"
        if weather["status"] == "no_data":
            formatted_weathers.append(
                f"<i>{weather['date']}</i>\nNo data for this date"
            )
            continue

        formatted_weathers.append(
            f"<i>{weather['date']}</i>\n"
            f"{weather['description']}\n"
            f"Temperature: {weather['temperature']}\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Wind speed: {weather['wind_speed']} ms\n"
            f"Rain probability: {weather['rain_percent']}\n"
        )
    return "\n".join(formatted_weathers)

