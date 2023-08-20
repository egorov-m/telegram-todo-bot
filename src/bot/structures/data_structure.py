from enum import StrEnum
from typing import Callable, TypedDict

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Database
from src.db.models import User
from src.lexicon.translator import Translator


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]  # Function for creating a session
    database: Database
    dispatcher: Dispatcher
    translator: Translator
    active_user: User


class LoggerType(StrEnum):
    BOT_LOGGER = "bot_logger"
    BOT_ERROR_LOGGER = "bot_error_logger"


class BotCmd(StrEnum):
    CMD_START_TITLE = "cmd_start_title"
    CMD_START_DESCRIPTION = "cmd_start_description"

    CMD_HELP_TITLE = "cmd_help_title"
    CMD_HELP_DESCRIPTION = "cmd_help_description"


class BotItem(StrEnum):
    MAIN = "main"
    USER_AGREEMENT = "user_agreement"
    ACCEPTED_USER_AGREEMENT = "accepted_user_agreement"
    ADD_TASK = "add_task"
    ADD_TASK_SAVE = "add_task_save"

    DELETE_TASK = "delete_task"
    DELETE_ALL_TASKS = "delete_all_tasks"
    DELETE_SELECTED_TASKS = "delete_selected_tasks"
    SELECT_DELETE_TASK = "select_delete_task"

    DONE_TASK = "done_task"
    DONE_STATE_ALL_TASKS = "done_state_all_tasks"
    DONE_STATE_NOTHING_TASKS = "done_state_nothing_tasks"
    SAVE_DONE_STATE_TASKS = "save_done_state_tasks"
    CHANGE_DONE_STATE_TASK = "change_done_state_task"

    EDIT_TASK = "edit_task"
    EDIT_TASK_SELECT = "edit_task_select"
    EDIT_TASK_TITLE = "edit_task_title"
    EDIT_TASK_DESCRIPTION = "edit_task_description"
    SAVE_EDIT_TASK = "save_edit_task"

    UPDATE_LIST = "update_list"
    SETTINGS = "settings"

    ADMIN_PANEL = "admin_panel"
    ADMIN_PANEL_USERS = "admin_panel_users"
    ADMIN_PANEL_USERS_CHANGE_SORT_DIRECTION = "admin_panel_users_change_sort_direction"
    ADMIN_PANEL_USER_ACCESS = "admin_panel_user_access"

    SETTINGS_LANGUAGES = "settings_languages"
    EMPTY = "empty"
    BACK = "back"
    CANCEL = "cancel"
    LANGUAGE = "language"
    ABOUT = "about"


class BotLanguage(StrEnum):
    EN_US = "en_US"
    RU_RU = "ru_RU"


class BotBtnLanguageTitle(StrEnum):
    EN_US = "btn_language_en_US_title"
    RU_RU = "btn_language_ru_RU_title"


class BotBtnTitle(StrEnum):
    START = "btn_start_title"
    ADD_TASK = "btn_add_task_title"

    DELETE_TASK = "btn_delete_task_title"
    DELETE_ALL_TASKS = "btn_delete_all_tasks_title"
    DELETE_SELECTED_TASKS = "btn_delete_selected_tasks_title"

    DONE_TASK = "btn_done_task_title"
    ALL_DONE_TASK = "btn_all_done_task_title"
    NOTHING_DONE_TASK = "btn_nothing_done_task"

    EDIT_TASK = "btn_edit_task_title"
    CHANGE_TITLE = "btn_edit_task_change_title"
    CHANGE_DESCRIPTION = "btn_edit_task_change_description"

    UPDATE_LIST = "btn_update_list_title"
    SETTINGS = "btn_settings_title"
    ABOUT = "btn_about_title"
    DELETE_ALL = "btn_delete_all_title"
    SAVE = "btn_save_title"
    APPLY = "btn_apply_title"
    CANCEL = "btn_cancel_title"
    LANGUAGES = "btn_languages_title"
    BACK = "btn_back_title"
    USER_AGREEMENT = "btn_user_agreement_title"
    ACCEPT_USER_AGREEMENT = "btn_accept_user_agreement_title"

    ADMIN_PANEL = "btn_admin_panel"
    ADMIN_PANEL_USERS = "btn_admin_panel_users"


class BotMessage(StrEnum):
    HELP_TITLE = "help_title"
    HELP_MESSAGE = "help_message"

    TASK_LIST_TITLE = "task_list_title"
    TASK_LIST_EMPTY_MESSAGE = "task_list_empty_message"

    ADD_TASK_MESSAGE = "add_task_message"
    ADD_TASK_ENTER_TITLE = "add_task_enter_title"
    ADD_TASK_ENTER_DESCRIPTION = "add_task_enter_description"
    ADD_TASK_CONFIRM = "add_task_confirm"

    ADD_TASK_ERROR_TITLE = "add_task_error_title"
    ADD_TASK_ERROR_DESCRIPTION = "add_task_error_description"

    DELETE_TASK_MESSAGE_TITLE = "delete_task_message_title"
    DELETE_TASK_MESSAGE_SUBTITLE = "delete_task_message_subtitle"
    DELETE_TASK_INFO_MESSAGE = "delete_task_info_message"

    EDIT_TASK_MESSAGE_TITLE = "edit_task_message_title"
    EDIT_TASK_MESSAGE_SUBTITLE = "edit_task_message_subtitle"
    EDIT_TASK_MESSAGE_SUBTITLE_TASK = "edit_task_message_subtitle_task"
    EDIT_TASK_MESSAGE_SUBTITLE_EDIT = "edit_task_message_subtitle_edit"
    EDIT_TASK_MESSAGE_ENTER_TITLE = "edit_task_message_enter_title"
    EDIT_TASK_MESSAGE_ENTER_DESCRIPTION = "edit_task_message_enter_description"

    DONE_TASK_MESSAGE_TITLE = "done_task_message_title"
    DONE_TASK_MESSAGE_SUBTITLE = "done_task_message_subtitle"

    INPUT_ERROR_MESSAGE = "input_error_message"

    SETTINGS_TITLE = "settings_title"
    SETTINGS_LANGUAGES_TITLE = "settings_languages_title"

    ABOUT_TITLE = "about_title"
    ABOUT_DESCRIPTION = "about_description"

    ADMIN_PANEL_MESSAGE_TITLE = "admin_panel_message_title"
    ADMIN_PANEL_MESSAGE_ADMIN_DATA = "admin_panel_message_admin_data"
    ADMIN_PANEL_USERS_MESSAGE_TITLE = "admin_panel_users_message_title"
    ADMIN_PANEL_USERS_MESSAGE_SUBTITLE = "admin_panel_users_message_subtitle"
    ADMIN_PANEL_USERS_MESSAGE_USER = "admin_panel_users_message_user"

    ERROR_MESSAGE = "error_message"
    EXCEPTION_MESSAGE = "exception_message"

    USER_AGREEMENT = "user_agreement"
    USER_AGREEMENT_ACCEPTED_MESSAGE = "user_agreement_accepted_message"

    USER_LOCKOUT_MESSAGE_TITLE = "user_lockout_message_title"
    USER_LOCKOUT_MESSAGE = "user_lockout_message"
