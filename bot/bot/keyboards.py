from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def location_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Send geoposition", request_location=True)],
            # [KeyboardButton(text="Ввести адрес вручную")],
        ],
        resize_keyboard=True,
    )

def forecast_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="3 days forecast")],
            [KeyboardButton(text="5 days forecast")],
        ],
        resize_keyboard=True,
    )

