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


class BotItem(StrEnum):
    MAIN = "main"
    USER_AGREEMENT = "user_agreement"
    ACCEPTED_USER_AGREEMENT = "accepted_user_agreement"
    ADD_TASK = "add_task"
    ADD_TASK_SAVE = "add_task_save"
    DELETE_TASK = "delete_task"
    DONE_TASK = "done_task"
    EDIT_TASK = "edit_task"
    UPDATE_LIST = "update_list"
    SETTINGS = 'settings'
    SETTINGS_LANGUAGES = "settings_languages"
    BACK = "back"
    CANCEL = "cancel"
    LANGUAGE = "language"


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
    DONE_TASK = "btn_done_task_title"
    EDIT_TASK = "btn_edit_task_title"
    UPDATE_LIST = "btn_update_list_title"
    SETTINGS = "btn_settings_title"
    DELETE_ALL = "btn_delete_all_title"
    SAVE = "btn_save_title"
    CANCEL = "btn_cancel_title"
    LANGUAGES = "btn_languages_title"
    BACK = "btn_back_title"
    USER_AGREEMENT = "btn_user_agreement"
    ACCEPT_USER_AGREEMENT = "btn_accept_user_agreement"


class BotMessage(StrEnum):
    TASK_LIST_TITLE = "task_list_title"
    TASK_LIST_EMPTY_MESSAGE = "task_list_empty_message"

    ADD_TASK_MESSAGE = "add_task_message"
    ADD_TASK_ENTER_TITLE = "add_task_enter_title"
    ADD_TASK_ENTER_DESCRIPTION = "add_task_enter_description"
    ADD_TASK_CONFIRM = "add_task_confirm"

    INPUT_ERROR_MESSAGE = "input_error_message"

    SETTINGS_TITLE = "settings_title"
    SETTINGS_LANGUAGES_TITLE = "settings_languages_title"
    ERROR_MESSAGE = "error_message"

    USER_AGREEMENT = "user_agreement"
    USER_AGREEMENT_ACCEPTED_MESSAGE = "user_agreement_accepted_message"
