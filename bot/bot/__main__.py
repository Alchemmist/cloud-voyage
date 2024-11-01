import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import requests

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "")  # Замените на свой токен

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
    await message.reply("Добро пожаловать! Этот бот предоставляет прогноз погоды. Используйте /help для получения списка команд.")

# Команда /help
async def cmd_help(message: types.Message):
    await message.reply(
        "/start - Приветствие\n"
        "/help - Список команд\n"
        "/weather - Получить прогноз погоды"
    )

# Команда /weather
async def cmd_weather(message: types.Message, state: FSMContext):
    await message.reply("Вы можете отправить ваше текущее местоположение или ввести начальную точку маршрута:", reply_markup=location_keyboard())
    await state.set_state(Form.waiting_for_start_point)

# Клавиатура для отправки местоположения или ввода адреса
def location_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить местоположение", request_location=True)],
            [KeyboardButton(text="Ввести адрес вручную")]
        ],
        resize_keyboard=True
    )

# Обработка местоположения как начальной или конечной точки
async def handle_location(message: types.Message, state: FSMContext):
    user_location = message.location
    current_state = await state.get_state()
    
    if current_state == Form.waiting_for_start_point:
        await state.update_data(start_point=(user_location.latitude, user_location.longitude))
        await state.set_state(Form.waiting_for_end_point)
        await message.reply("Местоположение начальной точки получено. Теперь отправьте конечную точку маршрута или введите ее адрес:", reply_markup=location_keyboard())
    elif current_state == Form.waiting_for_end_point:
        await state.update_data(end_point=(user_location.latitude, user_location.longitude))
        await state.set_state(Form.waiting_for_forecast_period)
        await message.reply("Местоположение конечной точки получено. Выберите временной интервал прогноза:", reply_markup=forecast_keyboard())

# Обработка нажатия кнопки "Ввести адрес вручную" для начальной или конечной точки
async def handle_manual_address_button(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Form.waiting_for_start_point:
        await message.reply("Введите начальную точку маршрута текстом:")
    elif current_state == Form.waiting_for_end_point:
        await message.reply("Введите конечную точку маршрута текстом:")

# Обработка текстового адреса для начальной точки
async def process_start_point(message: types.Message, state: FSMContext):
    await state.update_data(start_point=message.text)
    await state.set_state(Form.waiting_for_end_point)
    await message.reply("Введите конечную точку маршрута или отправьте ее местоположение:", reply_markup=location_keyboard())

# Обработка текстового адреса для конечной точки
async def process_end_point(message: types.Message, state: FSMContext):
    await state.update_data(end_point=message.text)
    await state.set_state(Form.waiting_for_forecast_period)
    await message.reply("Выберите временной интервал прогноза:", reply_markup=forecast_keyboard())

# Создание клавиатуры для выбора прогноза
def forecast_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Прогноз на 3 дня")],
            [KeyboardButton(text="Прогноз на неделю")]
        ],
        resize_keyboard=True
    )

# Обработка выбора временного интервала
async def process_forecast_period(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    start_point = user_data['start_point']
    end_point = user_data['end_point']
    forecast_period = 3 if message.text == "Прогноз на 3 дня" else 7

    # Получение прогноза погоды
    weather_data = get_weather_data(start_point, end_point, forecast_period)

    if weather_data:
        await message.reply(f"Прогноз погоды:\n{weather_data}")
    else:
        await message.reply("Не удалось получить прогноз погоды. Проверьте введенные данные или попробуйте позже.")

    await state.clear()

# Заглушка для функции прогноза
def get_weather_data(start_point, end_point, forecast_period):
    return f"От {start_point} до {end_point} на {forecast_period} дня(ей)."

# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, F.text == "/start")
    dp.message.register(cmd_help, F.text == "/help")
    dp.message.register(cmd_weather, F.text == "/weather")
    dp.message.register(handle_location, F.content_type == types.ContentType.LOCATION)
    dp.message.register(handle_manual_address_button, Form.waiting_for_start_point, F.text == "Ввести адрес вручную")
    dp.message.register(handle_manual_address_button, Form.waiting_for_end_point, F.text == "Ввести адрес вручную")
    dp.message.register(process_start_point, Form.waiting_for_start_point)
    dp.message.register(process_end_point, Form.waiting_for_end_point)
    dp.message.register(process_forecast_period, Form.waiting_for_forecast_period, F.text.in_({"Прогноз на 3 дня", "Прогноз на неделю"}))

# Основная функция
async def main():
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

