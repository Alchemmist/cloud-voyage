import { WeatherData } from "../services/WeatherService";

type WeatherInfoProps = {
    weather: WeatherData[];
};

const WeatherInfo = (props: WeatherInfoProps) => {
    return (
        <div style={{ padding: "1cm" }}>
            <h2>Weather Info</h2>
            {props.weather.length === 0 ? (
                <p>No weather data available</p>
            ) : (
                <ul>
                    {props.weather.map((w) => (
                        <li
                            key={`${w.location}-${w.date}`}
                            style={{ "margin-bottom": "1rem" }}
                        >
                            <strong>{w.location}</strong> on{" "}
                            <strong>{w.date}</strong>: {w.temperature},{" "}
                            {w.description}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default WeatherInfo;
