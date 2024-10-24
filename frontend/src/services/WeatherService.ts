export type WeatherData = {
    location: string;
    date: string;
    temperature: string;
    description: string;
};

// Функция для получения данных о погоде (тестовые данные вместо запроса)
export const getWeatherData = async (
    location: string,
    date: string,
): Promise<WeatherData> => {
    const testWeather = {
        "New York": {
            "2024-10-25": { temperature: "25°C", description: "clear sky" },
            "2024-10-26": { temperature: "23°C", description: "partly cloudy" },
        },
        Paris: {
            "2024-10-25": { temperature: "20°C", description: "rainy" },
            "2024-10-26": {
                temperature: "18°C",
                description: "overcast clouds",
            },
        },
        Tokyo: {
            "2024-10-25": { temperature: "28°C", description: "sunny" },
            "2024-10-26": { temperature: "27°C", description: "clear sky" },
        },
    };

    const weatherForLocation = testWeather[location];
    const weatherForDate = weatherForLocation?.[date];
    return weatherForDate
        ? { location, date, ...weatherForDate }
        : { location, date, temperature: "N/A", description: "unknown" };
};
