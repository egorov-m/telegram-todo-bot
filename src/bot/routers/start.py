from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from src.lexicon.translator import Translator, translate_list_all

start_router = Router(name='start_router')


@start_router.message(Command(*translate_list_all('cmd_start')), StateFilter(default_state))
async def cmd_start(message: types.Message, translator: Translator):
    """
    Start command handler
    """
    msg: str = await translator.translate('cmd_start_description')
    await message.answer(msg)
