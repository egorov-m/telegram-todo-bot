from enum import StrEnum
from typing import Callable, TypedDict

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from src.lexicon.translator import Translator


class TransferData(TypedDict):
    bot: Bot
    pool: Callable[[], AsyncSession]  # Function for creating a session
    dp: Dispatcher
    translator: Translator


class BotItem(StrEnum):
    MAIN = 'main'
    ADD_TASK = 'add_task'
    DELETE_TASK = 'delete_task'
    DONE_TASK = 'done_task'
    EDIT_TASK = 'edit_task'
    UPDATE_LIST = 'update_list'
    SETTINGS = 'settings'
    SETTINGS_LANGUAGES = 'settings_languages'
    BACK = 'back'
    LANGUAGE = 'language'


class BotLanguage(StrEnum):
    EN_US = 'en_US'
    RU_RU = 'ru_RU'


class BotBtnLanguageTitle(StrEnum):
    EN_US = 'btn_language_en_US_title'
    RU_RU = 'btn_language_ru_RU_title'


class BotBtnTitle(StrEnum):
    START = 'btn_start_title'
    ADD_TASK = 'btn_add_task_title'
    DELETE_TASK = 'btn_delete_task_title'
    DONE_TASK = 'btn_done_task_title'
    EDIT_TASK = 'btn_edit_task_title'
    UPDATE_LIST = 'btn_update_list_title'
    SETTINGS = 'btn_settings_title'
    DELETE_ALL = 'btn_delete_all_title'
    SAVE = 'btn_save_title'
    CANCEL = 'btn_cancel_title'
    LANGUAGES = 'btn_languages_title'
    BACK = 'btn_back_title'


class BotMessage(StrEnum):
    TASK_LIST_TITLE = 'task_list_title'
    TASK_LIST_EMPTY_MESSAGE = 'task_list_empty_message'

    ADD_TASK_MESSAGE = 'add_task_message'
    ADD_TASK_ENTER_TITLE = 'add_task_enter_title'
    ADD_TASK_ENTER_DESCRIPTION = 'add_task_enter_description'
    ADD_TASK_CONFIRM = 'add_task_confirm'

    INPUT_ERROR_MESSAGE = 'input_error_message'

    SETTINGS_TITLE = 'settings_title'
    SETTINGS_LANGUAGES_TITLE = 'settings_languages_title'
    ERROR_MESSAGE = 'error_message'
