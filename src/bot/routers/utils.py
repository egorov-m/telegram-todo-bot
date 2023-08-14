from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import InlineKeyboardMarkup, Message

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
