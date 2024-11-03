from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    waiting_for_start_point = State()
    waiting_for_end_point = State()
    waiting_for_forecast_period = State()

