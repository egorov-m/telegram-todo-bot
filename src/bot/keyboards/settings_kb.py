from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.keyboards.callback_factories import LanguagesCallback, BackCallback
from src.bot.structures.data_structure import BotPages
from src.lexicon.translator import Translator


async def create_settings_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate('btn_languages_title'),
                                          callback_data=LanguagesCallback().pack()),
                     InlineKeyboardButton(text=await translator.translate('btn_back_title'),
                                          callback_data=BackCallback(where_from=BotPages.MAIN).pack())], width=2)
    return kb_builder.as_markup()
