from aiogram.fsm.state import State, StatesGroup


class AddTaskStates(StatesGroup):
    add_task_waiting_title_input = State()
    add_task_waiting_description_input = State()
    add_task_waiting_confirmation = State()


class BotStates(StatesGroup):
    current_language = State()

    delete_task_waiting_select = State()
    delete_task_waiting_confirmation = State()

    done_task_waiting_select = State()
    done_task_waiting_confirmation = State()

    edit_task_waiting_select = State()
    edit_task_waiting_select_item_for_replacement = State()
    edit_task_waiting_title_input = State()
    edit_task_waiting_description_input = State()
    edit_task_waiting_confirmation = State()

    settings_waiting_select_item = State()
    settings_waiting_select_bot_language = State()
    settings_waiting_confirmation = State()
