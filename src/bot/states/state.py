from aiogram.fsm.state import State, StatesGroup


class FSMLanguages(StatesGroup):
    current_language = State()
