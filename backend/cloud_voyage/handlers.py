import json
from flask import Blueprint, request
from cloud_voyage import api


weather_forecast_blueprint = Blueprint("weather_forecast", __name__)


@weather_forecast_blueprint.route("/get_weather_forecast")
def five_days_forecast():
    if (location := request.args.get("location")) is None:
        return {"status": "error", "message": "location query param must be provided"}

    if (date := request.args.get("date")) is None:
        return {"status": "error", "message": "date query param must be provided"}

    if not (parse_data := api.get_forecaset(location, date)):
        return {
            "status": "not_found",
            "message": "can't find information to this date or for this location",
        }

    temp, precipitation_probability_percent, humidity_percent, wind_speed_ms, about = parse_data
    
    about = (
        "Good"
        if (
            (-15 <= temp <= 30)
            and (precipitation_probability_percent < 50)
            and (wind_speed_ms < 19)
            and (35 <= humidity_percent <= 55)
        )
        else "Bad"
    )

    return json.dumps({"temperature": temp, "description": about})
