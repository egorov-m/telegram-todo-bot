from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import lexicon as lx


def create_main_keyboard(lexicon: lx.LEXICON) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=text,
                                         callback_data=data)
                    for text, data in lexicon.main_buttons.items()], width=2)

    return kb_builder.as_markup()
