import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
from datetime import date, timedelta
import dash_leaflet as dl
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def fetch_weather_data(location: str, date_str: str):
    response = requests.get(
        "http://backend:5000/get_weather_forecast",
        params={"location": location, "date": date_str},
    ).json()
    if response["status"] == "success":
        return {
            "status": "success",
            "temperature": response["temperature"],
            "humidity": response["humidity"],
            "wind_speed": response["wind_speed"],
            "location": location,
            "rain_percent": response["rain_percent"],
            "description": response["description"],
            "date": date_str,
            "lat": response["lat"],
            "lon": response["lon"],
        }
    elif response["status"] == "no_data":
        return {
            "status": "no_data",
            "temperature": None,
            "description": "Could not fetch weather data",
            "location": location,
            "date": date_str,
            "lat": response.get("lat"),
            "lon": response.get("lon"),
        }
    else:  # статус not_found
        return {"status": "not_found"}

app.layout = dbc.Container(
    [
        dl.Map(
            id="route-map",
            center=[56, 37],
            zoom=5,
            children=[dl.TileLayer()],
            style={
                "width": "100%",
                "height": "300px",
                "margin": "0px",
                "padding": "0px",
                "overflow": "hidden",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Route Planner"),
                        dbc.Form(
                            [
                                dbc.Input(
                                    id="location-input",
                                    placeholder="Enter location",
                                    type="text",
                                    style={"margin-bottom": "10px"},
                                ),
                                dbc.Input(
                                    id="date-input",
                                    placeholder="Select date",
                                    type="date",
                                    value=str(date.today()),
                                    style={"margin-bottom": "10px"},
                                ),
                                dbc.Button(
                                    "Add Point",
                                    id="add-point-btn",
                                    color="primary",
                                    className="mt-2",
                                ),
                            ]
                        ),
                        html.H4("Your Route"),
                        html.Ul(id="route-list", className="list-unstyled mt-3"),
                        dbc.Alert(
                            "City not found. Please check the spelling or try a different location.",
                            id="not-found-alert",
                            color="danger",
                            is_open=False,
                            dismissable=True,
                            duration=4000,
                        ),
                    ],
                    width=4,
                    style={"border-right": "1px solid #ddd", "padding-right": "20px"},
                ),
                dbc.Col(
                    [
                        html.H2("Weather Information"),
                        dcc.Loading(
                            id="loading",
                            type="default",
                            children=html.Ul(
                                id="weather-info", className="list-unstyled mt-3"
                            ),
                        ),
                    ],
                    width=8,
                ),
            ],
            className="mt-5",
            style={'margin-left': '150px', 'margin-right': '150px'},
        ),
        html.Div(id="weather-output"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id="selected-location", className="mt-3"),
                        dcc.Dropdown(
                            id="metric-selector",
                            options=[
                                {"label": "Temperature", "value": "temperature"},
                                {"label": "Humidity", "value": "humidity"},
                                {"label": "Rain probability", "value": "rain_percent"},
                                {"label": "Wind speed", "value": "wind_speed"},
                            ],
                            value="temperature",
                            placeholder="Select a metric",
                        ),
                        dcc.Graph(id="weather-graph"),
                    ],
                    width=12,
                )
            ],
            className="mt-4",
            style={"margin-left": "150px", "margin-right": "150px"}
        ),
    ],
    fluid=True,
    style={'margin': '0', 'padding': '0'},
)

route_data = []

@app.callback(
    Output("route-list", "children"),
    Output("weather-info", "children"),
    Output("route-map", "children"),
    Output("selected-location", "children"),
    Output("weather-graph", "figure"),
    Output("not-found-alert", "is_open"),
    Input("add-point-btn", "n_clicks"),
    Input({"type": "delete-btn", "index": dash.ALL}, "n_clicks"),
    Input("metric-selector", "value"),
    State("location-input", "value"),
    State("date-input", "value"),
    prevent_initial_call=True,
)
def update_route(add_clicks, delete_clicks, selected_metric, location, date_str):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "add-point-btn" and location and date_str:
        weather = fetch_weather_data(location, date_str)
        if weather["status"] == "not_found":
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True

        route_data.append(
            {
                "location": location,
                "date": date_str,
                "weather": weather,
                "lat": weather["lat"],
                "lon": weather["lon"],
            }
        )

    elif "delete-btn" in button_id:
        index = eval(button_id)["index"]
        if index < len(route_data):
            del route_data[index]

    route_items = [
        html.Li(
            [
                f"{point['location']} on {point['date']}",
                dbc.Button(
                    "Delete",
                    id={"type": "delete-btn", "index": idx},
                    color="danger",
                    size="sm",
                    className="ms-2",
                ),
            ],
            className="mb-2",
        )
        for idx, point in enumerate(route_data)
    ]

    weather_items = [
        html.Li(
            [
                html.Strong(
                    f"{point['weather']['location']} on {point['weather']['date']}: "
                ),
                f"{point['weather']['temperature']}°C, {point['weather']['description']}",
            ],
            className="mb-3",
        )
        for point in route_data
    ]

    markers = [
        dl.Marker(
            position=[point["weather"].get("lat", 0), point["weather"].get("lon", 0)],
            children=[
                dl.Tooltip(point["location"]),
                dl.Popup(f"{point['location']} on {point['date']}"),
            ],
        )
        for point in route_data
    ]

    route_coords = [
        [point["weather"].get("lat", 0), point["weather"].get("lon", 0)]
        for point in route_data
    ]
    polyline = dl.Polyline(positions=route_coords, color="blue", weight=4)

    if route_data:
        # Подготавливаем данные для графика
        all_data = {
            "Date": [],
            "Value": [],
            "Location": []
        }

        # Устанавливаем диапазон дат для графика
        start_date = min(pd.to_datetime(point["date"]) for point in route_data)
        end_date = max(pd.to_datetime(point["date"]) for point in route_data)

        # Сбор данных по всем дням
        for point in route_data:
            location = point["location"]
            date_point = pd.to_datetime(point["date"])
            # Добавляем данные на дату точки маршрута
            all_data["Date"].append(date_point)
            all_data["Location"].append(location)
            all_data["Value"].append(point["weather"][selected_metric])

            # Добавляем данные по всем дням между стартовой и конечной датой
            for n in range((end_date - start_date).days + 1):
                current_date = start_date + timedelta(days=n)
                if current_date != date_point:
                    daily_weather = fetch_weather_data(location, current_date.strftime('%Y-%m-%d'))
                    if daily_weather["status"] == "success":
                        all_data["Date"].append(current_date)
                        all_data["Location"].append(location)
                        all_data["Value"].append(daily_weather[selected_metric])

        # Создаем DataFrame и строим график
        df = pd.DataFrame(all_data)
        df.sort_values(by="Date", inplace=True)
        fig = px.line(
            df,
            x="Date",
            y="Value",
            color="Location",
            labels={'Value': selected_metric.capitalize(), 'Date': 'Date'},
            title=f"{selected_metric.capitalize()} over time for each location"
        )
    else:
        fig = {}

    return (
        route_items,
        weather_items,
        [dl.TileLayer(), dl.LayerGroup(markers), polyline],
        f"{route_data[-1]['weather']['location']}" if route_data else "",
        fig,
        False,
    )

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=3000, debug=True)

