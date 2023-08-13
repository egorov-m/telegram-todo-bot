from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from bot.states.state import BotStates
from src.lexicon.translator import Translator, translate_list_all

help_router = Router(name='help_router')


@help_router.message(Command(*translate_list_all('cmd_help')), StateFilter(default_state, BotStates.bot_default_state))
async def cmd_help(message: types.Message, translator: Translator):
    """
    Help command handler
    """
    msg: str = await translator.translate('cmd_help_description')
    await message.answer(msg)
