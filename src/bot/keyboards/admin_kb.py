from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.callback_factories import (
    BackCallback,
    AdminPanelUsersCallback,
    AdminPanelUserChangeAccessCallback,
    EmptyCallback
)
from src.bot.structures.data_structure import BotBtnTitle, BotItem
from src.bot.utils.message_template import enable_marker
from src.db.models import User
from src.db.repository import TaskRepository
from src.lexicon import Translator


async def create_admin_keyboard(translator: Translator) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback().pack()),
                   InlineKeyboardButton(text=await translator.translate(BotBtnTitle.ADMIN_PANEL_USERS),
                                        callback_data=AdminPanelUsersCallback().pack()), width=2)

    return kb_builder.as_markup()


async def create_admin_users_keyboard(translator: Translator,
                                      *,
                                      users: list[User],
                                      task_repository: TaskRepository,
                                      offset: int,
                                      limit: int,
                                      count_pages: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=await translator.translate(BotBtnTitle.BACK),
                                        callback_data=BackCallback(where_from=BotItem.ADMIN_PANEL).pack()), width=1)
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
    kb_builder.row(*[InlineKeyboardButton(text=f"{enable_marker(user.enabled)} | "
                                               f"{user.telegram_user_id} | "
                                               f"{await task_repository.get_count_tasks_for_user(user, is_existed=False)} | "
                                               f"{await task_repository.get_count_tasks_for_user(user, is_existed=False, is_done=True)}",
                                          callback_data=AdminPanelUserChangeAccessCallback(offset=offset,
                                                                                           user_id=user.telegram_user_id,
                                                                                           enabled=user.enabled).pack()) for user in users], width=1)

    return kb_builder.as_markup()
