import "./week-weather-card.css";
import { createSignal } from "solid-js";

const weeklyForecast = [
  { day: "Monday", temp: "15°C", condition: "Cloudy" },
  { day: "Tuesday", temp: "17°C", condition: "Sunny" },
  { day: "Wednesday", temp: "13°C", condition: "Rainy" },
  { day: "Thursday", temp: "18°C", condition: "Partly Cloudy" },
  { day: "Friday", temp: "20°C", condition: "Sunny" },
  { day: "Saturday", temp: "16°C", condition: "Windy" },
  { day: "Sunday", temp: "19°C", condition: "Sunny" },
];

function WeatherCard() {
  const [showWeekForecast, setShowWeekForecast] = createSignal(false);

  const toggleWeekForecast = () => setShowWeekForecast(!showWeekForecast());

  return (
    <div class="weather-container">
      <div class="main-weather-card">
        <h2>Today's Weather</h2>
        <p>Temperature: 18°C</p>
        <p>Condition: Sunny</p>
        <button onClick={toggleWeekForecast}>
          {showWeekForecast() ? "Hide Week Forecast" : "See Week Forecast"}
        </button>
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
    </div>
  );
}

export default WeatherCard;

