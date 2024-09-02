from aiogram.fsm.state import State, StatesGroup

class Main(StatesGroup):
    default = State()
    exchange_rate = State()