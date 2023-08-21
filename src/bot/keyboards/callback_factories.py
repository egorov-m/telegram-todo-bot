from uuid import UUID

from src.bot.states.data import SortDirectionKey
from src.bot.structures.data_structure import BotItem

from aiogram.filters.callback_data import CallbackData


class MainCallback(CallbackData, prefix=BotItem.MAIN):
    pass


class AddTaskCallback(CallbackData, prefix=BotItem.ADD_TASK):
    pass


class AddTaskSaveCallback(CallbackData, prefix=BotItem.ADD_TASK_SAVE):
    # !!! Important: The field names must match the AddTaskStateData fields
    task_title: str = "title"
    task_description: str = "description"


class DeleteTaskCallback(CallbackData, prefix=BotItem.DELETE_TASK):
    pass


class DeleteAllTasksCallback(CallbackData, prefix=BotItem.DELETE_ALL_TASKS):
    pass


class DeleteSelectedTasksCallback(CallbackData, prefix=BotItem.DELETE_SELECTED_TASKS):
    pass


class SelectTaskDeleteCallback(CallbackData, prefix=BotItem.SELECT_DELETE_TASK):
    task_id: UUID


class DoneTaskCallback(CallbackData, prefix=BotItem.DONE_TASK):
    pass


class DoneStateAllTasksCallback(CallbackData, prefix=BotItem.DONE_STATE_ALL_TASKS):
    pass


class DoneStateNothingTasksCallback(CallbackData, prefix=BotItem.DONE_STATE_NOTHING_TASKS):
    pass


class SaveDoneStateTaskCallback(CallbackData, prefix=BotItem.SAVE_DONE_STATE_TASKS):
    pass


class ChangeDoneStateTaskCallback(CallbackData, prefix=BotItem.CHANGE_DONE_STATE_TASK):
    task_id: UUID


class EditTaskCallback(CallbackData, prefix=BotItem.EDIT_TASK):
    pass


class SelectTaskForEditCallback(CallbackData, prefix=BotItem.EDIT_TASK_SELECT):
    task_id: UUID


class EditTaskTitleCallback(CallbackData, prefix=BotItem.EDIT_TASK_TITLE):
    pass


class EditTaskDescriptionCallback(CallbackData, prefix=BotItem.EDIT_TASK_DESCRIPTION):
    pass


class SaveEditTaskCallback(CallbackData, prefix=BotItem.SAVE_EDIT_TASK):
    pass


class UpdateListCallback(CallbackData, prefix=BotItem.UPDATE_LIST):
    task_list_hash: str = ""


class SettingsCallback(CallbackData, prefix=BotItem.SETTINGS):
    pass


class AdminPanelCallback(CallbackData, prefix=BotItem.ADMIN_PANEL):
    pass


class AdminPanelUsersCallback(CallbackData, prefix=BotItem.ADMIN_PANEL_USERS):
    offset: int = 0


class AdminPanelUsersResetSearchCallback(CallbackData, prefix=BotItem.ADMIN_PANEL_USERS_RESET_SEARCH):
    pass


class AdminPanelUsersChangeSortDirectionCallback(AdminPanelUsersCallback, prefix=BotItem.ADMIN_PANEL_USERS_CHANGE_SORT_DIRECTION):
    key: SortDirectionKey
    is_ascending: bool


class AdminPanelUserChangeAccessCallback(AdminPanelUsersCallback, prefix=BotItem.ADMIN_PANEL_USER_ACCESS):
    user_id: int
    enabled: bool


class BackCallback(CallbackData, prefix=BotItem.BACK):
    where_from: str = BotItem.MAIN


class CancelCallback(CallbackData, prefix=BotItem.CANCEL):
    pass


class LanguagesCallback(CallbackData, prefix=BotItem.SETTINGS_LANGUAGES):
    """
    Callback - Bot language settings section
    """
    pass


class EmptyCallback(CallbackData, prefix=BotItem.EMPTY):
    pass


class LanguageCallback(CallbackData, prefix=BotItem.LANGUAGE):
    """
    Callback - language selected
    """
    language: str


class AboutCallback(CallbackData, prefix=BotItem.ABOUT):
    pass


class UserAgreementCallback(CallbackData, prefix=BotItem.USER_AGREEMENT):
    pass


class AcceptUserAgreementCallback(CallbackData, prefix=BotItem.ACCEPTED_USER_AGREEMENT):
    pass
