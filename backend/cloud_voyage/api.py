from datetime import datetime

from redis.typing import ResponseT
from cloud_voyage import cache
import requests
import urllib.parse
import json
import os


def date_alredy_cached(date: datetime, cache: ResponseT) -> bool:
    cached_dates = []
    for i in json.loads(cache)["DailyForecasts"]: # type: ignore
        cached_dates.append(datetime.strptime(i["Date"].split("T")[0], "%Y-%m-%d"))
    return date in cached_dates


def get_forecast(location, date) -> tuple[tuple | None, tuple | None]:
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    cache_key = f"weather:{location}"  # Включите дату в ключ кэша для уникальности
    cached_data = cache.get(cache_key)

    if cached_data and date_alredy_cached(date_obj, cached_data): 
        # Если данные найдены в кэше, возвращаем их
        return parse_cached_response(cached_data, date_obj)

    # Если данных в кэше нет, продолжаем с запросом к AccuWeather
    if "," in location and "." in location:
        url = (
            f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
        )
        response_base_link = requests.get(
            url,
            params={
                "apikey": os.getenv("ACCU_WEATHER_API_KEY"),
                "q": str(location),
                "details": False,
                "offset": 1,
            },
        )
        text_base = dict(json.loads(response_base_link.text))
    else:
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
        text_base = dict(list(json.loads(response_base_link.text))[0])

    if "Key" not in text_base:
        return None, None

    coordinates = (
        text_base["GeoPosition"]["Latitude"],
        text_base["GeoPosition"]["Longitude"],
    )

    url = (
        f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{text_base['Key']}"
    )
    response_data_link = requests.get(
        url, params={"apikey": os.getenv("ACCU_WEATHER_API_KEY"), "details": "true"}
    )

    forecast = dict(json.loads(response_data_link.text))

    # Кэшируем полученные данные перед возвратом
    forecast["GeoPosition"] = {"Latitude": coordinates[0], "Longitude": coordinates[1]}
    cache.set(cache_key, json.dumps(forecast))  # Сериализация в JSON

    return coordinates, parse_accu_response(forecast, date_obj)


def parse_cached_response(cached_data, date):
    # Здесь можно добавить логику для обработки кэшированных данных
    forecast = json.loads(cached_data)  # Десериализация из JSON

    # Получаем координаты из кэшированных данных
    coordinates = (
        forecast["GeoPosition"]["Latitude"],
        forecast["GeoPosition"]["Longitude"],
    )
    main_parse = forecast["DailyForecasts"]
    for weather in main_parse:
        w_date = datetime.strptime(weather["Date"].split("T")[0], "%Y-%m-%d")
        if w_date == date:
            return coordinates, (
                fahrenheit_to_celsius(
                    weather["Day"]["WetBulbTemperature"]["Average"]["Value"]
                ),
                int(weather["Day"]["HasPrecipitation"]) * 100,
                int(weather["Day"]["RelativeHumidity"]["Average"]),
                mih_to_ms(weather["Day"]["Wind"]["Speed"]["Value"]),
                str(weather["Day"]["ShortPhrase"]),
            )
    return coordinates, None


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
                int(weather["Day"]["HasPrecipitation"]) * 100,
                int(weather["Day"]["RelativeHumidity"]["Average"]),
                mih_to_ms(weather["Day"]["Wind"]["Speed"]["Value"]),
                str(weather["Day"]["ShortPhrase"]),
            )
    return None  # Если дата не найдена
