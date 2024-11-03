import asyncio
import os
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import requests

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")  # Замените на свой токен

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Состояния для FSM
class Form(StatesGroup):
    waiting_for_start_point = State()
    waiting_for_end_point = State()
    waiting_for_forecast_period = State()


# Команда /start
async def cmd_start(message: types.Message):
    await message.reply(
        "Welcome! This bot provides a weather forecast. Use /help to get a list of commands."
    )


# Команда /help
async def cmd_help(message: types.Message):
    await message.reply(
        "/start - Greetigns\n"
        "/help - Commands list\n"
        "/weather - Get weather forecast"
    )


# Команда /weather
async def cmd_weather(message: types.Message, state: FSMContext):
    await message.reply(
        "You can send your current location or enter the starting point of the route:",
        reply_markup=location_keyboard(),
    )
    await state.set_state(Form.waiting_for_start_point)


# Клавиатура для отправки местоположения или ввода адреса
def location_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Send geoposition", request_location=True)],
            # [KeyboardButton(text="Ввести адрес вручную")],
        ],
        resize_keyboard=True,
    )


# Обработка местоположения как начальной или конечной точки
async def handle_location(message: types.Message, state: FSMContext):
    user_location = message.location
    current_state = await state.get_state()

    if current_state == Form.waiting_for_start_point:
        await state.update_data(
            start_point=(user_location.latitude, user_location.longitude)
        )
        await state.set_state(Form.waiting_for_end_point)
        await message.reply(
            "The location of the starting point has been obtained. Now send the destination of the route or enter its address:",
            reply_markup=location_keyboard(),
        )
    elif current_state == Form.waiting_for_end_point:
        await state.update_data(
            end_point=(user_location.latitude, user_location.longitude)
        )
        await state.set_state(Form.waiting_for_forecast_period)
        await message.reply(
            "The location of the endpoint has been received. Select the forecast length:",
            reply_markup=forecast_keyboard(),
        )


# Обработка нажатия кнопки "Ввести адрес вручную" для начальной или конечной точки
async def handle_manual_address_button(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Form.waiting_for_start_point:
        await message.reply("Enter the starting point of the route in text:")
    elif current_state == Form.waiting_for_end_point:
        await message.reply("Enter the ending point of the route in text:")


# Обработка текстового адреса для начальной точки
async def process_start_point(message: types.Message, state: FSMContext):
    await state.update_data(start_point=message.text)
    await state.set_state(Form.waiting_for_end_point)
    await message.reply(
        "Enter the destination of the route or send its location:",
        reply_markup=location_keyboard(),
    )


# Обработка текстового адреса для конечной точки
async def process_end_point(message: types.Message, state: FSMContext):
    await state.update_data(end_point=message.text)
    await state.set_state(Form.waiting_for_forecast_period)
    await message.reply("Select forecast length:", reply_markup=forecast_keyboard())


# Создание клавиатуры для выбора прогноза
def forecast_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="3 days forecast")],
            [KeyboardButton(text="5 days forecast")],
        ],
        resize_keyboard=True,
    )


# Обработка выбора временного интервала
async def process_forecast_period(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    start_point = user_data["start_point"]
    end_point = user_data["end_point"]
    forecast_period = 3 if message.text == "3 days forecast" else 5

    # Получение прогноза погоды
    weather_data = get_weather_data(start_point, end_point, forecast_period)

    if weather_data:
        await message.reply(
            f"<strong>{forecast_period} days forecast:</strong>\n{weather_data}",
            parse_mode="HTML",
        )
    else:
        await message.reply(
            "The weather forecast could not be received. Check the entered data or try again later."
        )

    await state.clear()


# Заглушка для функции прогноза
def get_weather_data(start_point, end_point, forecast_period):
    if isinstance(end_point, tuple):
        end_point = ",".join(map(str, end_point))

    if isinstance(start_point, tuple):
        start_point = ",".join(map(str, start_point))

    today = datetime.now()
    start_forecast = []
    for day in range(forecast_period):
        weather = requests.get(
            "http://backend:5000/get_weather_forecast",
            params={
                "location": start_point,
                "date": (today + timedelta(days=day)).strftime("%Y-%m-%d"),
            },
        ).json()
        start_forecast.append(weather)

    end_forecast = []
    for day in range(forecast_period):
        weather = requests.get(
            "http://backend:5000/get_weather_forecast",
            params={
                "location": end_point,
                "date": (today + timedelta(days=day)).strftime("%Y-%m-%d"),
            },
        ).json()
        end_forecast.append(weather)

    return (
        f"<strong>{start_point}:</strong>\n{formating_forecast(start_forecast)}\n\n"
        f"<strong>{end_point}:</strong>\n{formating_forecast(end_forecast)}"
    )


def formating_forecast(forecast: list[dict]) -> str:
    formating_weathers = []
    for weather in forecast:
        if weather["status"] == "not_found":
            return "Error. Location not found"
        if weather["status"] == "no_data":
            formating_weathers.append(
                f"<i>{weather["date"]}</i>\nNo data for this date"
            )
            continue

        formating_weathers.append(
            f"<i>{weather["date"]}</i>\n"
            f"{weather["description"]}"
            f"Temperature: {weather["temperature"]}\n"
            f"Humidity: {weather["humidity"]}%\n"
            f"Wind speed: {weather["wind_speed"]} ms\n"
            f"Rain probability: {weather["rain_percent"]}\n"
        )
    return "\n".join(formating_weathers)


# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, F.text == "/start")
    dp.message.register(cmd_help, F.text == "/help")
    dp.message.register(cmd_weather, F.text == "/weather")
    dp.message.register(handle_location, F.content_type == types.ContentType.LOCATION)
    dp.message.register(
        handle_manual_address_button,
        Form.waiting_for_start_point,
        F.text == "Enter location",
    )
    dp.message.register(
        handle_manual_address_button,
        Form.waiting_for_end_point,
        F.text == "Enter location",
    )
    dp.message.register(process_start_point, Form.waiting_for_start_point)
    dp.message.register(process_end_point, Form.waiting_for_end_point)
    dp.message.register(
        process_forecast_period,
        Form.waiting_for_forecast_period,
        F.text.in_({"3 days forecast", "5 days forecast"}),
    )


# Основная функция
async def main():
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
