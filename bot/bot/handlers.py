from aiogram import types, F
from aiogram.fsm.context import FSMContext
from bot.states import Form
from bot.keyboards import location_keyboard, forecast_keyboard
from bot.weather import get_weather_data

async def cmd_start(message: types.Message):
    await message.reply(
        "Welcome! This bot provides a weather forecast. Use /help to get a list of commands."
    )

async def cmd_help(message: types.Message):
    await message.reply(
        "/start - Greetings\n"
        "/help - Commands list\n"
        "/weather - Get weather forecast"
    )

async def cmd_weather(message: types.Message, state: FSMContext):
    await message.reply(
        "You can send your current location or enter the starting point of the route:",
        reply_markup=location_keyboard(),
    )
    await state.set_state(Form.waiting_for_start_point)

async def handle_location(message: types.Message, state: FSMContext):
    user_location = message.location
    current_state = await state.get_state()

    if current_state == Form.waiting_for_start_point:
        await state.update_data(start_point=(user_location.latitude, user_location.longitude))
        await state.set_state(Form.waiting_for_end_point)
        await message.reply(
            "The location of the starting point has been obtained. Now send the destination of the route or enter its address:",
            reply_markup=location_keyboard(),
        )
    elif current_state == Form.waiting_for_end_point:
        await state.update_data(end_point=(user_location.latitude, user_location.longitude))
        await state.set_state(Form.waiting_for_forecast_period)
        await message.reply("The location of the endpoint has been received. Select the forecast length:", reply_markup=forecast_keyboard())

async def process_forecast_period(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    start_point = user_data["start_point"]
    end_point = user_data["end_point"]
    forecast_period = 3 if message.text == "3 days forecast" else 5

    weather_data = get_weather_data(start_point, end_point, forecast_period)

    if weather_data:
        await message.reply(
            f"<strong>{forecast_period} days forecast:</strong>\n{weather_data}",
            parse_mode="HTML",
        )
    else:
        await message.reply("The weather forecast could not be received. Check the entered data or try again later.")
    await state.clear()

def register_handlers(dp):
    dp.message.register(cmd_start, F.text == "/start")
    dp.message.register(cmd_help, F.text == "/help")
    dp.message.register(cmd_weather, F.text == "/weather")
    dp.message.register(handle_location, F.content_type == types.ContentType.LOCATION)
    dp.message.register(
        process_forecast_period,
        Form.waiting_for_forecast_period,
        F.text.in_({"3 days forecast", "5 days forecast"}),
    )

