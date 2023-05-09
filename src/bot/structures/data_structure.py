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


class BotPages(StrEnum):
    MAIN = 'main'
    ADD_TASK = 'add_task'
    DELETE_TASK = 'delete_task'
    DONE_TASK = 'done_task'
    EDIT_TASK = 'edit_task'
    UPDATE_LIST = 'update_list'
    SETTINGS = 'settings'
    SETTINGS_LANGUAGES = 'settings_languages'


class BotButtons(StrEnum):
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
