import axios from "axios";

export type WeatherData = {
    location: string;
    date: string;
    temperature: string;
    description: string;
};

export const getWeatherData = async (location: string, date: string) => {
    try {
        const response = await axios.get("http://localhost:5000/get_weather_forecast", {
            params: { location, date },
        });
        console.log("Response received:", response);
        return {
            location,
            date,
            temperature: response.data.temperature,
            description: response.data.description,
        };
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Axios error:", error.message, error.code, error.config, error.request);
        } else {
            console.error("Unexpected error:", error);
        }
        return {
            location,
            date,
            temperature: "-",
            description: "No data for this date",
        };
    }
};

