from typing import TypedDict, Callable

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Database
from src.db.models import User
from src.lexicon import Translator


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]  # Function for creating a session
    database: Database
    dispatcher: Dispatcher
    translator: Translator
    active_user: User
