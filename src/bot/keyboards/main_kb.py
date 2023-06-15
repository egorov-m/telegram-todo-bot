from enum import StrEnum
from typing import Dict

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.bot.keyboards.callback_factories import (
    MainCallback,
    AddTaskCallback,
    DeleteTaskCallback,
    DoneTaskCallback,
    EditTaskCallback,
    UpdateListCallback,
    SettingsCallback,
    BackCallback
)
from src.bot.structures.data_structure import BotBtnTitle, BotItem
from src.lexicon.translator import Translator


_buttons_data: Dict[StrEnum, CallbackData] = {
    BotBtnTitle.ADD_TASK: AddTaskCallback(),
    BotBtnTitle.DELETE_TASK: DeleteTaskCallback(),
    BotBtnTitle.DONE_TASK: DoneTaskCallback(),
    BotBtnTitle.EDIT_TASK: EditTaskCallback(),
    BotBtnTitle.UPDATE_LIST: UpdateListCallback(),
    BotBtnTitle.SETTINGS: SettingsCallback()
}


async def create_start_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(BotBtnTitle.START),
                                          callback_data=MainCallback().pack())], width=2)

    return kb_builder.as_markup()


async def create_back_keyboard(translator: Translator, where_from: BotItem = BotItem.MAIN) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback(where_from=where_from).pack()), width=2)

    return kb_builder.as_markup()


async def create_main_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(key),
                                          callback_data=value.pack()) for key, value in _buttons_data.items()], width=2)

    return kb_builder.as_markup()
