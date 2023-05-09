from aiogram import Router
from aiogram.filters.callback_data import CallbackQuery

from src.bot.keyboards.callback_factories import SettingsCallback, BackCallback
from src.bot.keyboards.settings_kb import create_settings_keyboard
from src.bot.utils.html.message_template import bold_title
from src.lexicon.translator import Translator
from .start import btn_start


settings_router = Router(name='settings_router')


@settings_router.callback_query(SettingsCallback.filter())
async def btn_settings(callback: CallbackQuery, translator: Translator):
    title: str = await translator.translate('settings_title')
    kb = await create_settings_keyboard(translator=translator)
    await callback.message.edit_text(text=bold_title(title),
                                     reply_markup=kb)


@settings_router.callback_query(BackCallback.filter())
async def btn_back(callback: CallbackQuery, translator: Translator):
    data = callback.data.split(':')[1]
    match data:
        case _:
            await btn_start(callback, translator)
