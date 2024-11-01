import logging
from cloud_voyage.routes import weather_forecast_blueprint
from cloud_voyage import app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with app.app_context():
        app.register_blueprint(weather_forecast_blueprint)

    app.run(host="0.0.0.0", port=5000)
