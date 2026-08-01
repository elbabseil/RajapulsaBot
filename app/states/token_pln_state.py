from aiogram.fsm.state import State, StatesGroup


class TokenPLNState(StatesGroup):

    waiting_nominal = State()

    waiting_meter = State()