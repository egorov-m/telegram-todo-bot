from aiogram.fsm.state import State, StatesGroup


class AddTaskStates(StatesGroup):
    add_task_waiting_title_input = State()
    add_task_waiting_description_input = State()
    add_task_waiting_confirmation = State()


class DeleteTaskStates(StatesGroup):
    delete_task_waiting_select = State()
    delete_task_waiting_confirmation = State()


class DoneTaskStates(StatesGroup):
    done_task_waiting_select = State()
    done_task_waiting_confirmation = State()


class EditTaskStates(StatesGroup):
    edit_task_waiting_select_task = State()
    edit_task_waiting_select_edit_item = State()
    edit_task_waiting_title_input = State()
    edit_task_waiting_description_input = State()


class AdminPanelStates(StatesGroup):
    open_admin_panel = State()
    open_users_panel = State()
    open_stats_panel = State()


class BotStates(StatesGroup):
    current_language = State()

    edit_task_waiting_select = State()
    edit_task_waiting_select_item_for_replacement = State()
    edit_task_waiting_title_input = State()
    edit_task_waiting_description_input = State()
    edit_task_waiting_confirmation = State()

    settings_waiting_select_item = State()
    settings_waiting_select_bot_language = State()
    settings_waiting_confirmation = State()
