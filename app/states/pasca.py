from aiogram.fsm.state import State, StatesGroup


class PascaState(StatesGroup):

    waiting_customer_no = State()