import { createSignal } from "solid-js";
import WeatherCard from "./components/week-weather-card";
import "./app.css";

const weeklyForecast = [
    { day: "Monday", temp: "15°C", condition: "Cloudy" },
    { day: "Tuesday", temp: "17°C", condition: "Sunny" },
    { day: "Wednesday", temp: "13°C", condition: "Rainy" },
    { day: "Thursday", temp: "18°C", condition: "Partly Cloudy" },
    { day: "Friday", temp: "20°C", condition: "Sunny" },
    { day: "Saturday", temp: "16°C", condition: "Windy" },
    { day: "Sunday", temp: "19°C", condition: "Sunny" },
];

const App = () => {
    const [showWeekForecast, setShowWeekForecast] = createSignal(false);

    const toggleWeekForecast = () => setShowWeekForecast(!showWeekForecast());

    const [currentLocation, setCurrentLocation] = createSignal("Москва");
    const weatherData = {
        current: {
            temp: 29,
            condition: "Солнечно",
            uvIndex: "Высокий",
            rainChance: 5,
            time: "10:00 AM",
        },
        hourly: [
            { time: "11 AM", temp: 29, icon: "sunny" },
            { time: "12 PM", temp: 31, icon: "sunny" },
            { time: "1 PM", temp: 30, icon: "partly-cloudy" },
            { time: "2 PM", temp: 29, icon: "cloudy" },
            { time: "3 PM", temp: 27, icon: "rain" },
        ],
    };

    return (
        <div class="app-container">
            <div class="weather-card main-card">
                <div class="location-selector">
                    <span>{currentLocation()}</span>
                </div>
                <div class="main-weather-info">
                    <div class="temp">{weatherData.current.temp}°C</div>
                    <div class="condition">{weatherData.current.condition}</div>
                </div>
                <div class="weather-details">
                    <span>Temp: {weatherData.current.temp}°C</span>
                    <span>UV Index: {weatherData.current.uvIndex}</span>
                    <span>Rain Chance: {weatherData.current.rainChance}%</span>
                </div>
                <div class="hourly-forecast">
                    {weatherData.hourly.map((hour) => (
                        <div class="hour-card">
                            <span>{hour.time}</span>
                            <span class={`icon ${hour.icon}`}></span>
                            <span>{hour.temp}°C</span>
                        </div>
                    ))}
                </div>
            </div>
            {showWeekForecast() && (
                <div class="weekly-forecast">
                    {weeklyForecast.map((dayForecast) => (
                        <div class="day-forecast-card">
                            <h3>{dayForecast.day}</h3>
                            <p>Temp: {dayForecast.temp}</p>
                            <p>Condition: {dayForecast.condition}</p>
                        </div>
                    ))}
                </div>
            )}
            <button
                class="weather-button secondary-card"
                onClick={toggleWeekForecast}
            >
                {showWeekForecast()
                    ? "Hide Week Forecast"
                    : "See Week Forecast"}
            </button>
        </div>
    );
};

export default App;
