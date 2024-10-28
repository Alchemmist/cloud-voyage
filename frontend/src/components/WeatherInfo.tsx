import { WeatherData } from "../services/WeatherService";

type WeatherInfoProps = {
    weather: WeatherData[]; // Принимает массив
};

const WeatherInfo = (props: WeatherInfoProps) => {
    return (
        <div style={{ padding: "1cm", display: "flex", "flex-direction": "column", "align-items": "flex-start" }}>
            <h2>Weather</h2>
            {props.weather.length === 0 ? (
                <p>No information about weather</p>
            ) : (
                <ul>
                    {props.weather.map((w) => (
                        <li
                            style={{ "margin-bottom": "1rem" }}
                        >
                            <strong>{`${w.location}  ${w.date}:`}</strong> {` ${w.temperature}°C  ${w.description}`}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default WeatherInfo;
