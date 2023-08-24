from datetime import datetime
from math import ceil

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup
from sqlalchemy.engine import Row

from src.bot.structures.types import StatsType, VisualizeFormat
from src.db.models import Event
from src.db.repository import EventRepository
from src.bot.keyboards.main_kb import create_hide_keyboard
from src.bot.states.groups import AdminPanelStates
from src.config import settings
from src.bot.states.data import SortingStateData, SortDirectionKey, StatsStateData, VisProcessData
from src.db.repository import UserRepository
from src.bot.keyboards.admin_kb import create_admin_keyboard, create_admin_users_keyboard, create_admin_stat_keyboard
from src.bot.routers.utils import edit_message, get_expression_sorting
from src.bot.structures.bot import BotMessage
from src.bot.utils.message_template import bold_text, italic_text, get_selected_stats_markers, task_marker
from src.db.repository import TaskRepository
from src.db import Database
from src.db.models import User
from src.lexicon import Translator
from src.bot.keyboards.callback_factories import (
    AdminPanelCallback,
    AdminPanelUsersCallback,
    AdminPanelUserChangeAccessCallback,
    AdminPanelUsersChangeSortDirectionCallback,
    AdminPanelUsersResetSearchCallback,
    AdminPanelStatsCallback,
    AdminPanelStatsTypeCallback, VisualizeCallback
)
from src.visualizer.base import visualize_timeline

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


@admin_panel_router.callback_query(
    AdminPanelStatsCallback.filter(),
    StateFilter(AdminPanelStates.open_admin_panel,
                AdminPanelStates.open_stats_panel)
)
async def btn_admin_panel_stats(callback: CallbackQuery,
                                state: FSMContext,
                                *,
                                database: Database,
                                active_user: User,
                                translator: Translator):
    data: StatsStateData = await state.get_data()
    if not data:
        await state.set_state(AdminPanelStates.open_stats_panel)
        data = StatsStateData(in_process=[], selected_stats=[StatsType.CALLBACK_EVENT, StatsType.STATE_EVENT])
        await state.update_data(data)
    await get_admin_panel_stats(callback.message,
                                state,
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)


async def get_admin_panel_stats(message: Message,
                                state: FSMContext,
                                *,
                                data: StatsStateData,
                                database: Database,
                                active_user: User,
                                translator: Translator):
    markers = get_selected_stats_markers(data["selected_stats"])
    msg: str = f"{bold_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_TITLE))}\n" \
               f"{italic_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_SUBTITLE))}\n\n" \
               f"{bold_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_OPTIONS))}:\n" \
               f"- {markers[StatsType.CALLBACK_EVENT]} {italic_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_CALLBACK_EVENT))}\n" \
               f"- {markers[StatsType.STATE_EVENT]} {italic_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_STATE_EVENT))}"
    is_visualized: bool = len(data["selected_stats"]) > 0
    if not is_visualized:
        msg += f"\n\n{italic_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_SELECTION_ERROR))}"
    in_process: list[VisProcessData] = data["in_process"]
    if len(in_process) > 0:
        msg += f"\n\n{bold_text(await translator.translate(BotMessage.ADMIN_PANEL_STATS_MESSAGE_FORMATION_PROCESS))}:\n"
        for item in in_process:
            msg += f"- {task_marker()} {bold_text(item['visualize_format'].upper())} - {' | '.join(item['selected_stats'])}\n"

    kb = await create_admin_stat_keyboard(translator=translator, is_visualized=is_visualized)

    await edit_message(message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@admin_panel_router.callback_query(VisualizeCallback.filter(), AdminPanelStates.open_stats_panel)
async def btn_admin_panel_stats_visualize(callback: CallbackQuery,
                                          state: FSMContext,
                                          *,
                                          database: Database,
                                          active_user: User,
                                          translator: Translator):
    vis_format: VisualizeFormat = callback.data.split(":")[1]
    is_photo: bool = callback.data.split(":")[2] == "True"
    data: StatsStateData = await state.get_data()
    in_process: list[VisProcessData] = data["in_process"]
    selected_stats: list[StatsType] = data["selected_stats"]
    new_process = VisProcessData(selected_stats=selected_stats, visualize_format=vis_format)
    in_process.append(new_process)
    data["in_process"] = in_process
    await state.update_data(data)
    await get_admin_panel_stats(callback.message,
                                state,
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)

    kb = await create_hide_keyboard(translator=translator)
    repo: EventRepository = database.event
    for stat in selected_stats:
        match stat:
            case StatsType.CALLBACK_EVENT.value:
                await answer_media(callback.message, repo, Event.callback_data_prefix, active_user,
                                   title=await translator.translate(
                                       BotMessage.ADMIN_PANEL_STATS_MESSAGE_CALLBACK_EVENT),
                                   vis_format=vis_format,
                                   is_photo=is_photo,
                                   kb=kb)
            case StatsType.STATE_EVENT.value:
                await answer_media(callback.message, repo, Event.state, active_user,
                                   title=await translator.translate(
                                       BotMessage.ADMIN_PANEL_STATS_MESSAGE_STATE_EVENT),
                                   vis_format=vis_format,
                                   is_photo=is_photo,
                                   kb=kb)

    in_process: list[VisProcessData] = data["in_process"]
    in_process.remove(new_process)
    data["in_process"] = in_process
    await state.update_data(data)
    await get_admin_panel_stats(callback.message,
                                state,
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)


async def answer_media(message: Message,
                       repo: EventRepository,
                       grouping_field,
                       active_user: User,
                       *,
                       title: str,
                       vis_format: str,
                       is_photo: bool,
                       kb: ReplyKeyboardMarkup):
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    title = f"{title} - {datetime.utcnow().strftime(datetime_format)}"
    data_callback = await repo.get_events_for_timeline(active_user, grouping_field=grouping_field)
    media_callback = visualize_timeline(data_callback,
                                        title=title,
                                        filename_no_ext=title.lower().replace(" ", "_"),
                                        visualize_format=vis_format)
    if is_photo:
        await message.answer_photo(media_callback, caption=title, reply_markup=kb)
    else:
        await message.answer_document(media_callback, caption=title, reply_markup=kb)


@admin_panel_router.callback_query(AdminPanelStatsTypeCallback.filter(), AdminPanelStates.open_stats_panel)
async def btn_admin_panel_stats_type(callback: CallbackQuery,
                                     state: FSMContext,
                                     *,
                                     database: Database,
                                     active_user: User,
                                     translator: Translator):
    stats_type: StatsType = callback.data.split(":")[1]
    data: StatsStateData = await state.get_data()
    selected_stats = data["selected_stats"]
    if stats_type in selected_stats:
        selected_stats.remove(stats_type)
    else:
        selected_stats.append(stats_type)
    data["selected_stats"] = selected_stats
    await state.update_data(data)
    await get_admin_panel_stats(callback.message,
                                state,
                                data=data,
                                database=database,
                                active_user=active_user,
                                translator=translator)


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
