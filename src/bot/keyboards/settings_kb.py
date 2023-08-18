from typing import List, AsyncGenerator

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.keyboards.callback_factories import (
    LanguagesCallback,
    LanguageCallback,
    BackCallback,
    UserAgreementCallback
)
from src.bot.structures.data_structure import BotItem, BotLanguage, BotBtnLanguageTitle, BotBtnTitle
from src.lexicon.translator import Translator


async def create_settings_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(BotBtnTitle.LANGUAGES),
                                          callback_data=LanguagesCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.USER_AGREEMENT),
                                          callback_data=UserAgreementCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                          callback_data=BackCallback(where_from=BotItem.MAIN).pack())], width=2)
    return kb_builder.as_markup()


async def create_languages_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[item async for item in _create_language_buttons(translator,
                                                                     BotBtnLanguageTitle.__members__.values(),
                                                                     BotLanguage.__members__.values())],
                   InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback(where_from=BotItem.SETTINGS).pack()), width=2)
    return kb_builder.as_markup()


async def _create_language_buttons(translator: Translator,
                                   btn_title_list: List[str],
                                   languages_list: List[str]) -> AsyncGenerator[InlineKeyboardButton, None]:
    for title, lang in zip(btn_title_list, languages_list):
        yield InlineKeyboardButton(text=await translator.translate(title),
                                   callback_data=LanguageCallback(language=lang).pack())
