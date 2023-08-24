import time
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import InlineKeyboardMarkup, Message, InputMedia
from sqlalchemy import asc, desc, func
from sqlalchemy.sql.elements import UnaryExpression

from src.bot.states.data import SortDirectionKey, SortingStateData
from src.db.models import Task
from src.bot.routers.start import start_page
from src.db import Database
from src.db.models import User
from src.lexicon import Translator


async def edit_message(message: Message,
                       state: FSMContext,
                       *,
                       database: Database,
                       active_user: User,
                       translator: Translator,
                       text: str,
                       kb: InlineKeyboardMarkup):
    """
    Editing a message (an error handler has been added in case of incorrect messages)
    """
    try:
        await message.edit_text(text=text,
                                reply_markup=kb)
    except ValueError:
        await state.clear()
        await state.set_state(default_state)
        await start_page(message,
                         database=database,
                         active_user=active_user,
                         translator=translator)


def _is_no_valid_input(text: str | None):
    """
    Whether text input from a user is invalid
    """
    return (text is None or
            text.isspace() or
            text == '' or
            text.__contains__("\""))


def get_expression_sorting(data: SortingStateData) -> UnaryExpression:
    if data["is_ascending"]:
        direction = asc
    else:
        direction = desc
    match data["key"]:
        case SortDirectionKey.CREATED_DATE:
            key = User.created_date
        case SortDirectionKey.TASKS:
            key = func.count(Task.id)
        case SortDirectionKey.DONE:
            key = func.count(Task.id).filter(Task.is_done == True)

    return direction(key)
