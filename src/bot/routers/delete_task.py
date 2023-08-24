from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from src.bot.keyboards.callback_factories import (
    DeleteTaskCallback,
    DeleteAllTasksCallback,
    SelectTaskDeleteCallback,
    DeleteSelectedTasksCallback
)
from src.bot.keyboards.task_kb import create_delete_task_keyboard
from src.bot.routers.utils import edit_message
from src.bot.routers.start import btn_start
from src.bot.states.data import DeletableTask
from src.bot.states.groups import DeleteTaskStates
from src.bot.structures.bot import BotMessage
from src.bot.utils.message_template import bold_text, italic_text
from src.db import Database
from src.db.models import User, Task
from src.db.repository import TaskRepository
from src.lexicon import Translator


delete_task_router = Router(name="delete_task_router")


@delete_task_router.callback_query(DeleteTaskCallback.filter(), default_state)
async def btn_delete_task(callback: CallbackQuery,
                          state: FSMContext,
                          *,
                          database: Database,
                          active_user: User,
                          translator: Translator):
    """
    Handler for pressing the delete task button
    """
    await state.set_state(state=DeleteTaskStates.delete_task_waiting_select)
    msg: str = await _get_delete_task_full_message(translator)
    repo: TaskRepository = database.task
    deletable_tasks: list[DeletableTask] = await _get_deletable_task_list(await repo.get_tasks_for_user(active_user))
    await state.update_data({"tasks": deletable_tasks})
    kb = await create_delete_task_keyboard(translator=translator,
                                           tasks=deletable_tasks)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@delete_task_router.callback_query(SelectTaskDeleteCallback.filter(), DeleteTaskStates.delete_task_waiting_select)
async def btn_select_delete_task(callback: CallbackQuery,
                                 state: FSMContext,
                                 *,
                                 database: Database,
                                 active_user: User,
                                 translator: Translator):
    task_id = callback.data.split(":")[1]
    data: list[DeletableTask] = (await state.get_data())["tasks"]
    count_selected: int = 0
    for task in data:
        if task["task_id"] == task_id:
            old = task["is_delete"]
            task["is_delete"] = not old
        if task["is_delete"]:
            count_selected += 1
    await state.update_data({"tasks": data})
    kb = await create_delete_task_keyboard(translator=translator,
                                           tasks=data)
    msg: str = await _get_delete_task_full_message(translator,
                                                   count_selected=count_selected)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@delete_task_router.callback_query(DeleteSelectedTasksCallback.filter(), DeleteTaskStates.delete_task_waiting_select)
async def btn_delete_selected_tasks(callback: CallbackQuery,
                                    state: FSMContext,
                                    *,
                                    database: Database,
                                    active_user: User,
                                    translator: Translator):
    data: list[DeletableTask] = (await state.get_data())["tasks"]
    repo: TaskRepository = database.task
    for task in data:
        if task["is_delete"]:
            await repo.delete_task(task_id=task["task_id"],
                                   active_telegram_user_id=active_user.telegram_user_id)
    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


@delete_task_router.callback_query(DeleteAllTasksCallback.filter(), DeleteTaskStates.delete_task_waiting_select)
async def btn_delete_all_tasks(callback: CallbackQuery,
                               state: FSMContext,
                               *,
                               database: Database,
                               active_user: User,
                               translator: Translator):
    repo: TaskRepository = database.task
    await repo.delete_tasks_for_user(active_user)
    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


async def _get_delete_task_full_message(translator: Translator, count_selected: int = 0):
    return f"{bold_text(await translator.translate(BotMessage.DELETE_TASK_MESSAGE_TITLE))}\n" \
           f"{italic_text(await translator.translate(BotMessage.DELETE_TASK_MESSAGE_SUBTITLE))}\n\n" \
           f"{bold_text(await translator.translate(BotMessage.DELETE_TASK_INFO_MESSAGE, count=count_selected))}"


async def _get_deletable_task_list(tasks: list[Task]) -> list[DeletableTask]:
    return [DeletableTask(task_id=str(task.id),
                          is_delete=False,
                          is_done=task.is_done,
                          title=task.title) for task in tasks]
