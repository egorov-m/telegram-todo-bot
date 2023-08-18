from math import ceil

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from src.db.repository import UserRepository
from src.bot.keyboards.admin_kb import create_admin_keyboard, create_admin_users_keyboard
from src.bot.routers.utils import edit_message
from src.bot.structures.data_structure import BotMessage
from src.bot.utils.message_template import bold_text, italic_text
from src.db.repository import TaskRepository
from src.db import Database
from src.db.models import User
from src.lexicon import Translator
from src.bot.keyboards.callback_factories import (
    AdminPanelCallback,
    AdminPanelUsersCallback,
    AdminPanelUserChangeAccessCallback
)

admin_panel_router = Router(name="admin_panel_router")

LIMIT_USERS_ON_PAGE: int = 5


@admin_panel_router.callback_query(AdminPanelCallback.filter(), default_state)
async def btn_admin_panel(callback: CallbackQuery,
                          state: FSMContext,
                          *,
                          database: Database,
                          active_user: User,
                          translator: Translator):
    repo: TaskRepository = database.task
    username = active_user.username
    last_name = active_user.last_name
    admin_data: str = await translator.translate(BotMessage.ADMIN_PANEL_MESSAGE_ADMIN_DATA,
                                                 id=active_user.telegram_user_id,
                                                 username=username if username is not None else "None",
                                                 first_name=active_user.first_name,
                                                 last_name=last_name if last_name is not None else "None",
                                                 created_date=active_user.created_date,
                                                 task_now=await repo.get_count_tasks_for_user(active_user),
                                                 task_all_time=await repo.get_count_tasks_for_user(active_user, is_existed=False),
                                                 you_done=await repo.get_count_tasks_for_user(active_user, is_existed=False, is_done=True))
    msg: str = f"{bold_text(await translator.translate(BotMessage.ADMIN_PANEL_MESSAGE_TITLE))}\n\n" \
               f"{admin_data}"
    kb = await create_admin_keyboard(translator=translator)

    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@admin_panel_router.callback_query(AdminPanelUsersCallback.filter(), default_state)
async def btn_admin_panel_users(callback: CallbackQuery,
                                state: FSMContext,
                                *,
                                database: Database,
                                active_user: User,
                                translator: Translator):
    repo: UserRepository = database.user
    count_users: int = await repo.get_count_users(active_user)
    count_pages: int = ceil(count_users / LIMIT_USERS_ON_PAGE)
    offset: int = int(callback.data.split(":")[1])
    users: list[User] = await repo.get_users(active_user,
                                             offset=offset,
                                             limit=LIMIT_USERS_ON_PAGE)

    msg: str = f"{bold_text(await translator.translate(BotMessage.ADMIN_PANEL_USERS_MESSAGE_TITLE))}\n" \
               f"{italic_text(await translator.translate(BotMessage.ADMIN_PANEL_USERS_MESSAGE_SUBTITLE))}\n\n" \
               f"{await translator.translate(BotMessage.ADMIN_PANEL_USERS_MESSAGE_USER)}"
    kb = await create_admin_users_keyboard(translator,
                                           users=users,
                                           task_repository=database.task,
                                           offset=offset,
                                           limit=LIMIT_USERS_ON_PAGE,
                                           count_pages=count_pages)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@admin_panel_router.callback_query(AdminPanelUserChangeAccessCallback.filter(), default_state)
async def btn_admin_panel_user_change_access(callback: CallbackQuery,
                                             state: FSMContext,
                                             *,
                                             database: Database,
                                             active_user: User,
                                             translator: Translator):
    t = callback.data.split(":")
    user_id = int(t[2])
    enabled = t[3] == "True"
    repo: UserRepository = database.user
    await repo.update_user(user_id, enabled=not enabled)
    await btn_admin_panel_users(callback,
                                state,
                                database=database,
                                active_user=active_user,
                                translator=translator)
