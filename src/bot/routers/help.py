from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.structures.data_structure import BotMessage
from src.bot.utils.message_template import bold_text, italic_text
from src.lexicon.translator import Translator, translate_list_all

help_router = Router(name="help_router")


@help_router.message(Command(*translate_list_all("cmd_help")))
async def cmd_help(message: Message,
                   *,
                   translator: Translator):
    """
    Help command handler
    """
    msg: str = f"{bold_text(await translator.translate(BotMessage.HELP_TITLE))}\n\n" \
               f"{italic_text(await translator.translate(BotMessage.HELP_MESSAGE))}"
    await message.answer(msg)
