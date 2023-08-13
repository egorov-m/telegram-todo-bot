from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.bot.keyboards.callback_factories import (
    MainCallback,
    AcceptUserAgreementCallback,
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


_buttons_data: dict[StrEnum, CallbackData] = {
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


async def create_accept_user_agreement(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(text=await translator.translate(BotBtnTitle.ACCEPT_USER_AGREEMENT),
                                          callback_data=AcceptUserAgreementCallback().pack())], width=2)

    return kb_builder.as_markup()


async def create_back_keyboard(translator: Translator, where_from: BotItem = BotItem.MAIN) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback(where_from=where_from).pack()), width=2)

    return kb_builder.as_markup()


async def create_main_keyboard(translator: Translator, task_list_hash: str | None = None) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=await translator.translate(key),
                                                                callback_data=value.pack()) for key, value in _buttons_data.items()]
    if task_list_hash is not None:
        # The penultimate button for updating the list
        button: InlineKeyboardButton = buttons[-2]
        button.callback_data = UpdateListCallback(task_list_hash=task_list_hash).pack()
    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()
