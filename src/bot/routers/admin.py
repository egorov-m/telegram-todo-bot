from math import ceil

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.engine import Row

from src.bot.states.state import AdminPanelStates
from src.config import settings
from src.bot.states.data import SortingStateData, SortDirectionKey
from src.db.repository import UserRepository
from src.bot.keyboards.admin_kb import create_admin_keyboard, create_admin_users_keyboard
from src.bot.routers.utils import edit_message, get_expression_sorting
from src.bot.structures.data_structure import BotMessage
from src.bot.utils.message_template import bold_text, italic_text
from src.db.repository import TaskRepository
from src.db import Database
from src.db.models import User
from src.lexicon import Translator
from src.bot.keyboards.callback_factories import (
    AdminPanelCallback,
    AdminPanelUsersCallback,
    AdminPanelUserChangeAccessCallback,
    AdminPanelUsersChangeSortDirectionCallback,
    AdminPanelUsersResetSearchCallback
)

admin_panel_router = Router(name="admin_panel_router")


@admin_panel_router.callback_query(AdminPanelCallback.filter(), default_state)
async def btn_admin_panel(callback: CallbackQuery,
                          state: FSMContext,
                          *,
                          database: Database,
                          active_user: User,
                          translator: Translator):
    await state.set_state(AdminPanelStates.open_admin_panel)
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


@admin_panel_router.callback_query(AdminPanelUsersChangeSortDirectionCallback.filter(), AdminPanelStates.open_users_panel)
async def btn_admin_panel_users_change_sort_direction(callback: CallbackQuery,
                                                      state: FSMContext,
                                                      *,
                                                      database: Database,
                                                      active_user: User,
                                                      translator: Translator):
    t = callback.data.split(":")
    key = t[2]
    is_ascending = t[3] == "True"
    data = await state.get_data()
    if data["key"] == key:
        data["is_ascending"] = not is_ascending
    else:
        data["key"] = key
    await state.update_data(data)
    await btn_admin_panel_users(callback,
                                state,
                                database=database,
                                active_user=active_user,
                                translator=translator)


@admin_panel_router.message(AdminPanelStates.open_users_panel)
async def input_search_text(message: Message,
                            state: FSMContext,
                            *,
                            database: Database,
                            active_user: User,
                            translator: Translator):
    search_text = message.text
    data: SortingStateData = await state.get_data()
    data["search_text"] = search_text
    await state.update_data(data)
    await get_admin_panel_users(Message.parse_raw(data["message"]),
                                state,
                                offset=data["offset"],
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)


@admin_panel_router.callback_query(
    AdminPanelUsersCallback.filter(),
    StateFilter(AdminPanelStates.open_admin_panel,
                AdminPanelStates.open_users_panel)
)
async def btn_admin_panel_users(callback: CallbackQuery,
                                state: FSMContext,
                                *,
                                database: Database,
                                active_user: User,
                                translator: Translator):
    offset: int = int(callback.data.split(":")[1])
    message: Message = callback.message
    await state.set_state(AdminPanelStates.open_users_panel)
    data = await state.get_data()
    if not data:
        data: SortingStateData = SortingStateData(key=SortDirectionKey.CREATED_DATE,
                                                  is_ascending=False,
                                                  search_text=None,
                                                  message=message.json(),
                                                  offset=offset)
        await state.update_data(data)
    else:
        data["offset"] = offset
        await state.update_data(data)

    await get_admin_panel_users(message,
                                state,
                                offset=offset,
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)


@admin_panel_router.callback_query(
    AdminPanelUsersResetSearchCallback.filter(),
    StateFilter(AdminPanelStates.open_admin_panel,
                AdminPanelStates.open_users_panel)
)
async def reset_search(callback: CallbackQuery,
                       state: FSMContext,
                       *,
                       database: Database,
                       active_user: User,
                       translator: Translator):
    data: SortingStateData = await state.get_data()
    data["search_text"] = None
    await state.update_data(data)
    await get_admin_panel_users(callback.message,
                                state,
                                offset=data["offset"],
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)


async def get_admin_panel_users(message: Message,
                                state: FSMContext,
                                *,
                                offset: int,
                                data: SortingStateData,
                                database: Database,
                                active_user: User,
                                translator: Translator):
    repo: UserRepository = database.user
    count_users: int = await repo.get_count_users(active_user, search_text=data["search_text"])
    count_pages: int = ceil(count_users / settings.LIMIT_USERS_ON_PAGE)

    users: list[Row] = await repo.get_users_with_more_info(active_user,
                                                           search_text=data["search_text"],
                                                           offset=offset,
                                                           limit=settings.LIMIT_USERS_ON_PAGE,
                                                           order=get_expression_sorting(data))
    msg: str = f"{bold_text(await translator.translate(BotMessage.ADMIN_PANEL_USERS_MESSAGE_TITLE))}\n" \
               f"{italic_text(await translator.translate(BotMessage.ADMIN_PANEL_USERS_MESSAGE_SUBTITLE))}\n\n" \
               f"{await translator.translate(BotMessage.ADMIN_PANEL_USERS_MESSAGE_USER)}"
    kb = await create_admin_users_keyboard(translator,
                                           users=users,
                                           search_text=data["search_text"],
                                           sorting_state_data=data,
                                           offset=offset,
                                           limit=settings.LIMIT_USERS_ON_PAGE,
                                           count_pages=count_pages)
    await edit_message(message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@admin_panel_router.callback_query(AdminPanelUserChangeAccessCallback.filter(), AdminPanelStates.open_users_panel)
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
