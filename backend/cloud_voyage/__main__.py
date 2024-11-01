import logging
from cloud_voyage.routes import weather_forecast_blueprint
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with app.app_context():
        app.register_blueprint(weather_forecast_blueprint)

    app.run(host="0.0.0.0", port=5000)
