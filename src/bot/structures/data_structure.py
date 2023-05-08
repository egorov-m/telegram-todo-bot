from typing import Callable, TypedDict

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from src.lexicon.translator import Translator


class TransferData(TypedDict):
    bot: Bot
    pool: Callable[[], AsyncSession]  # Function for creating a session
    dp: Dispatcher
    translator: Translator
