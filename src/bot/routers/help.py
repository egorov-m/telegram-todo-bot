from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import default_state
from aiogram.types import Message

from src.lexicon.translator import Translator, translate_list_all

help_router = Router(name="help_router")


@help_router.message(Command(*translate_list_all("cmd_help")), default_state)
async def cmd_help(message: Message,
                   *,
                   translator: Translator):
    """
    Help command handler
    """
    msg: str = await translator.translate("cmd_help_description")
    await message.answer(msg)
