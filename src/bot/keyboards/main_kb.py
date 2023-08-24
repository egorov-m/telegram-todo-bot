from enum import StrEnum
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.bot.structures.role import Role
from src.db.models import User
from src.bot.keyboards.callback_factories import (
    MainCallback,
    AcceptUserAgreementCallback,
    AddTaskCallback,
    DeleteTaskCallback,
    DoneTaskCallback,
    EditTaskCallback,
    UpdateListCallback,
    SettingsCallback,
    BackCallback,
    AdminPanelCallback,
    HideCallback
)
from src.bot.structures.bot import BotBtnTitle, BotItem
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


async def create_hide_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.HIDE),
                                        callback_data=HideCallback().pack()), width=2)

    return kb_builder.as_markup()


async def create_main_keyboard(translator: Translator,
                               active_user: Optional[User] = None,
                               task_list_hash: Optional[str] = None) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=await translator.translate(key),
                                                                callback_data=value.pack()) for key, value in _buttons_data.items()]
    if task_list_hash is not None:
        # The penultimate button for updating the list
        button: InlineKeyboardButton = buttons[-2]
        button.callback_data = UpdateListCallback(task_list_hash=task_list_hash).pack()
    kb_builder.row(*buttons, width=2)

    if active_user is not None and active_user.role == Role.ADMINISTRATOR:
        kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.ADMIN_PANEL),
                                            callback_data=AdminPanelCallback().pack()), width=1)

    return kb_builder.as_markup()
