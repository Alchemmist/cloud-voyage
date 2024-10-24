import "./App.css";
import { createSignal } from "solid-js";
import RoutePlanner from "./components/RoutePlanner";
import WeatherInfo from "./components/WeatherInfo";
import { WeatherData, getWeatherData } from "./services/WeatherService";

const WeatherApp = () => {
    const [route, setRoute] = createSignal<
        { location: string; date: string }[]
    >([]);
    const [weather, setWeather] = createSignal<WeatherData[]>([]);

    const addPoint = async (location: string, date: string) => {
        if (
            location &&
            date &&
            !route().some(
                (point) => point.location === location && point.date === date,
            )
        ) {
            setRoute([...route(), { location, date }]);
            const newWeather = await getWeatherData(location, date);
            setWeather([...weather(), newWeather]);
        }
    };

    const removePoint = (location: string, date: string) => {
        setRoute(
            route().filter(
                (point) => point.location !== location || point.date !== date,
            ),
        );
        setWeather(
            weather().filter((w) => w.location !== location || w.date !== date),
        );
    };

    return (
        <div
            style={{
                display: "flex",
                "justify-content": "space-between",
                padding: "2rem",
            }}
        >
            {/* Левая колонка — настройка маршрута */}
            <div style={{ flex: 1, "margin-right": "2rem" }}>
                <RoutePlanner
                    route={route()}
                    onAdd={addPoint}
                    onRemove={removePoint}
                />
            </div>
            {/* Правая колонка — отображение погоды */}
            <div style={{ flex: 1 }}>
                <WeatherInfo weather={weather()} />
            </div>
        </div>
    );
};

export default WeatherApp;
