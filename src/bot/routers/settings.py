from aiogram import Router
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from src.bot.keyboards.callback_factories import SettingsCallback, LanguagesCallback, BackCallback
from src.bot.keyboards.settings_kb import create_settings_keyboard, create_languages_keyboard
from src.bot.utils.html.message_template import bold_text
from src.bot.structures.data_structure import BotItem, BotBtnTitle
from src.lexicon.translator import Translator
from .start import btn_start


settings_router = Router(name='settings_router')


@settings_router.callback_query(SettingsCallback.filter())
async def btn_settings(callback: CallbackQuery, translator: Translator):
    title: str = await translator.translate(BotBtnTitle.SETTINGS)
    kb = await create_settings_keyboard(translator=translator)
    await callback.message.edit_text(text=bold_text(title),
                                     reply_markup=kb)


@settings_router.callback_query(LanguagesCallback().filter())
async def btn_settings_languages(callback: CallbackQuery, translator: Translator):
    title: str = await translator.translate('settings_languages_title')
    kb = await create_languages_keyboard(translator=translator)
    await callback.message.edit_text(text=bold_text(title),
                                     reply_markup=kb)


@settings_router.callback_query(BackCallback.filter())
async def btn_back(callback: CallbackQuery, state: FSMContext, translator: Translator):
    data = callback.data.split(':')[1]
    match data:
        case BotItem.SETTINGS:
            await btn_settings(callback, translator)
        case _:
            await state.clear()
            await state.set_state(default_state)
            await btn_start(callback, translator)
