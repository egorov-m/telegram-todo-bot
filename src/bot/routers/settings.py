from aiogram import Router
from aiogram.filters.callback_data import CallbackQuery

from src.bot.routers.start import user_agreement_conclusion
from src.db.repository import UserRepository
from src.db import Database
from src.db.models import User
from src.bot.keyboards.callback_factories import SettingsCallback, LanguagesCallback, LanguageCallback, \
    UserAgreementCallback
from src.bot.keyboards.settings_kb import create_settings_keyboard, create_languages_keyboard
from src.bot.utils.html.message_template import bold_text
from src.bot.structures.data_structure import BotBtnTitle, BotMessage
from src.lexicon.translator import Translator


settings_router = Router(name='settings_router')


@settings_router.callback_query(SettingsCallback.filter())
async def btn_settings(callback: CallbackQuery, translator: Translator):
    title: str = await translator.translate(BotBtnTitle.SETTINGS)
    kb = await create_settings_keyboard(translator=translator)
    await callback.message.edit_text(text=bold_text(title),
                                     reply_markup=kb)


@settings_router.callback_query(UserAgreementCallback.filter())
async def btn_settings_user_agreement(callback: CallbackQuery, translator: Translator, active_user: User):
    await user_agreement_conclusion(callback,
                                    active_user=active_user,
                                    translator=translator)


@settings_router.callback_query(LanguagesCallback.filter())
async def btn_settings_languages(callback: CallbackQuery,
                                 *,
                                 translator: Translator):
    title: str = await translator.translate(BotMessage.SETTINGS_LANGUAGES_TITLE)
    kb = await create_languages_keyboard(translator=translator)
    await callback.message.edit_text(text=bold_text(title),
                                     reply_markup=kb)


@settings_router.callback_query(LanguageCallback.filter())
async def btn_language_selection(callback: CallbackQuery,
                                 *,
                                 database: Database,
                                 active_user: User):
    old_lang: str = active_user.current_language
    # callback.data format: language:en_US
    new_lang: str = callback.data.split(":")[1]
    if old_lang != new_lang:
        repo: UserRepository = database.user
        await repo.update_user(active_user.telegram_user_id, current_language=new_lang)
        new_translator: Translator = Translator(locale=new_lang)
        await btn_settings_languages(callback,
                                     translator=new_translator)
    else:
        await callback.answer()
