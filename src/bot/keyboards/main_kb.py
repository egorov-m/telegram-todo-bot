from typing import Dict

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.keyboards.callback_factories import (
    MainCallback,
    AddTaskCallback,
    DeleteTaskCallback,
    DoneTaskCallback,
    EditTaskCallback,
    UpdateListCallback,
    SettingsCallback
)
from src.lexicon.translator import Translator


buttons_data: Dict[str, CallbackData] = {
    'btn_add_task_title': AddTaskCallback(),
    'btn_delete_task_title': DeleteTaskCallback(),
    'btn_done_task_title': DoneTaskCallback(),
    'btn_edit_task_title': EditTaskCallback(),
    'btn_update_list_title': UpdateListCallback(),
    'btn_settings_title': SettingsCallback()
}


async def create_start_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate('btn_start_title'),
                                          callback_data=MainCallback().pack())], width=2)

    return kb_builder.as_markup()


async def create_main_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(key),
                                          callback_data=value.pack()) for key, value in buttons_data.items()], width=2)

    return kb_builder.as_markup()
