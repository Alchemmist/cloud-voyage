import "./App.css";
import { createSignal } from "solid-js";
import { getWeatherData, WeatherData } from "./services/WeatherService";
import RoutePlanner from "./components/RoutePlanner";
import WeatherInfo from "./components/WeatherInfo";

type RoutePoint = {
    location: string;
    date: string;
    weather: WeatherData | null;
};

const WeatherApp = () => {
    const [route, setRoute] = createSignal<RoutePoint[]>([]);
    const [loading, setLoading] = createSignal(false);

    const addPoint = async (location: string, date: string) => {
        setLoading(true);
        const weatherData = await getWeatherData(location, date);
        setRoute((prevRoute) => [...prevRoute, { location, date, weather: weatherData }]);
        setLoading(false);
    };

    const removePoint = (index: number) => {
        setRoute((prevRoute) => prevRoute.filter((_, i) => i !== index));
    };

    return (
        <div class="container">
            <div style={{ padding: "1rem", "margin-right": "0" }}>
                <RoutePlanner
                    route={route()}
                    onAdd={addPoint}
                    onRemove={removePoint}
                    loading={loading()}
                />
            </div>
            <div style={{ width: "13cm", "margin-top": "0.7cm"}}>
                <WeatherInfo
                    weather={route().map((point) => point.weather).filter(Boolean)}
                />
            </div>
        </div>
    );
};

export default WeatherApp;
