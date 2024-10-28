from datetime import datetime
import requests
import urllib.parse
import json
import os


def get_forecaset(location, date):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"

    response_base_link = requests.get(
        url,
        params={
            "apikey": os.getenv("ACCU_WEATHER_API_KEY"),
            "q": urllib.parse.quote(str(location)),
            "details": False,
            "offset": 1,
        },
    )

    text_base = list(json.loads(response_base_link.text))[0]
    url = (
        f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{text_base['Key']}"
    )
    response_data_link = requests.get(
        url, params={"apikey": os.getenv("ACCU_WEATHER_API_KEY"), "details": "true"}
    )
    forecast = dict(json.loads(response_data_link.text))
    format = "%Y-%m-%d"
    date = datetime.strptime(date, format)
    return parse_accu_response(forecast, date)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


def mih_to_ms(mih: float) -> float:
    return mih / 2.237

def parse_accu_response(
    forecast_5_day: dict, date: datetime
) -> tuple[float, int, int, float, str] | None:
    main_parse = forecast_5_day["DailyForecasts"] 
    for weather in main_parse:
        w_date = datetime.strptime(weather["Date"].split("T")[0], "%Y-%m-%d")
        if w_date == date:
            return (
                fahrenheit_to_celsius(
                    weather["Day"]["WetBulbTemperature"]["Average"]["Value"]
                ),
                int(weather["HasPrecipitation"]) * 100,
                int(weather["RelativeHumidity"]),
                mih_to_ms(weather["Wind"]["Speed"]["Imperial"]["Value"]),
                str(weather["Day"]["ShortPhrase"]),
            )
