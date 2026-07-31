from aiogram.fsm.state import State, StatesGroup


class PaymentState(StatesGroup):

    waiting_target = State()