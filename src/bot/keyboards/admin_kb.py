from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.engine import Row

from src.bot.states.data import SortingStateData
from src.bot.keyboards.callback_factories import (
    BackCallback,
    AdminPanelUsersCallback,
    AdminPanelUserChangeAccessCallback,
    EmptyCallback,
    AdminPanelUsersChangeSortDirectionCallback, AdminPanelUsersResetSearchCallback
)
from src.bot.structures.data_structure import BotBtnTitle, BotItem
from src.bot.utils.message_template import (
    enable_marker,
    get_text_sorting_button,
    get_markers_for_sorting_direction_key
)
from src.lexicon import Translator


async def create_admin_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback().pack()),
                   InlineKeyboardButton(text=await translator.translate(BotBtnTitle.ADMIN_PANEL_USERS),
                                        callback_data=AdminPanelUsersCallback().pack()), width=2)

    return kb_builder.as_markup()


def _get_sorting_buttons(sorting_state_data: SortingStateData):
    directions = get_markers_for_sorting_direction_key()
    sorting_buttons: list[InlineKeyboardButton] = []
    for key, value in directions.items():
        sorting_buttons.append(
            InlineKeyboardButton(
                text=get_text_sorting_button(sorting_state_data,
                                             value,
                                             sorting_state_data["key"] == key),
                callback_data=AdminPanelUsersChangeSortDirectionCallback(key=key,
                                                                         is_ascending=sorting_state_data["is_ascending"]).pack()
            )
        )
    return sorting_buttons


async def create_admin_users_keyboard(translator: Translator,
                                      *,
                                      users: list[Row],
                                      search_text: Optional[str] = None,
                                      sorting_state_data: SortingStateData,
                                      offset: int,
                                      limit: int,
                                      count_pages: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback(where_from=BotItem.ADMIN_PANEL).pack()), width=1)
    if search_text is not None:
        kb_builder.row(InlineKeyboardButton(
            text=await translator.translate(BotBtnTitle.ADMIN_PANEL_USERS_RESET_SEARCH, text=search_text),
            callback_data=AdminPanelUsersResetSearchCallback(offset=offset).pack()), width=1)

    sorting_buttons: list[InlineKeyboardButton] = _get_sorting_buttons(sorting_state_data)
    kb_builder.row(*sorting_buttons, width=3)

    pagination_buttons: list[InlineKeyboardButton] = []
    if offset > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⏪",
                                                       callback_data=AdminPanelUsersCallback(
                                                           offset=offset - limit
                                                       ).pack()))
    page_number = 1 + (offset // limit)
    pagination_buttons.append(InlineKeyboardButton(text=f"{page_number}/{count_pages}",
                                                   callback_data=EmptyCallback().pack()))
    if page_number < count_pages:
        pagination_buttons.append(InlineKeyboardButton(text="⏩",
                                                       callback_data=AdminPanelUsersCallback(
                                                           offset=offset + limit
                                                       ).pack()))
    kb_builder.row(*pagination_buttons, width=3)
    kb_builder.row(*[InlineKeyboardButton(text=f"{enable_marker(user[0])} | "
                                               f"@{user[1]} | "
                                               f"{user[2]} | "
                                               f"{user[3]} | "
                                               f"{user[4]} | "
                                               f"{user[5]} | "
                                               f"{user[6]}",
                                          callback_data=AdminPanelUserChangeAccessCallback(offset=offset,
                                                                                           user_id=user[2],
                                                                                           enabled=user[0]).pack()) for user in users], width=1)

    return kb_builder.as_markup()
