from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from src.bot.keyboards.callback_factories import (
    DoneTaskCallback,
    DoneStateAllTasksCallback,
    DoneStateNothingTasksCallback,
    SaveDoneStateTaskCallback,
    ChangeDoneStateTaskCallback
)
from src.bot.keyboards.task_kb import create_done_task_keyboard
from src.bot.routers.start import btn_start
from src.bot.routers.utils import edit_message
from src.bot.states.data import DoneTask
from src.bot.states.groups import DoneTaskStates
from src.bot.structures.bot import BotMessage
from src.bot.utils.message_template import bold_text, italic_text
from src.db import Database
from src.db.models import User, Task
from src.db.repository import TaskRepository
from src.lexicon import Translator


done_task_router = Router(name="done_task_router")


@done_task_router.callback_query(DoneTaskCallback.filter(), default_state)
async def btn_done_task(callback: CallbackQuery,
                        state: FSMContext,
                        *,
                        database: Database,
                        active_user: User,
                        translator: Translator):
    """
    Handler for pressing the done task button
    """
    await state.set_state(state=DoneTaskStates.done_task_waiting_select)
    msg: str = await _get_done_task_full_message(translator)
    repo: TaskRepository = database.task
    done_tasks: list[DoneTask] = await _get_done_task_list(await repo.get_tasks_for_user(active_user))
    await state.update_data({"tasks": done_tasks})
    kb = await create_done_task_keyboard(translator=translator,
                                         tasks=done_tasks)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@done_task_router.callback_query(ChangeDoneStateTaskCallback.filter(), DoneTaskStates.done_task_waiting_select)
async def btn_change_done_state_task(callback: CallbackQuery,
                                     state: FSMContext,
                                     *,
                                     database: Database,
                                     active_user: User,
                                     translator: Translator):
    task_id = callback.data.split(":")[1]
    data: list[DoneTask] = (await state.get_data())["tasks"]
    for task in data:
        if task["task_id"] == task_id:
            old = task["is_done"]
            task["is_done"] = not old
    await state.update_data({"tasks": data})
    kb = await create_done_task_keyboard(translator=translator,
                                         tasks=data)
    msg: str = await _get_done_task_full_message(translator)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@done_task_router.callback_query(SaveDoneStateTaskCallback.filter(), DoneTaskStates.done_task_waiting_select)
async def btn_save_done_tasks(callback: CallbackQuery,
                              state: FSMContext,
                              *,
                              database: Database,
                              active_user: User,
                              translator: Translator):
    data: list[DoneTask] = (await state.get_data())["tasks"]
    repo: TaskRepository = database.task
    for task in data:
        await repo.done_task(task_id=task["task_id"],
                             is_done=task["is_done"],
                             active_telegram_user_id=active_user.telegram_user_id)
    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


@done_task_router.callback_query(DoneStateAllTasksCallback.filter(), DoneTaskStates.done_task_waiting_select)
async def btn_done_all_tasks(callback: CallbackQuery,
                             state: FSMContext,
                             *,
                             database: Database,
                             active_user: User,
                             translator: Translator):
    repo: TaskRepository = database.task
    await repo.done_tasks_for_user(active_user)
    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


@done_task_router.callback_query(DoneStateNothingTasksCallback.filter(), DoneTaskStates.done_task_waiting_select)
async def btn_no_done_all_tasks(callback: CallbackQuery,
                                state: FSMContext,
                                *,
                                database: Database,
                                active_user: User,
                                translator: Translator):
    repo: TaskRepository = database.task
    await repo.done_tasks_for_user(active_user, is_done=False)
    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


async def _get_done_task_full_message(translator: Translator):
    return f"{bold_text(await translator.translate(BotMessage.DONE_TASK_MESSAGE_TITLE))}\n" \
           f"{italic_text(await translator.translate(BotMessage.DONE_TASK_MESSAGE_SUBTITLE))}\n\n"


async def _get_done_task_list(tasks: list[Task]) -> list[DoneTask]:
    return [DoneTask(task_id=str(task.id),
                     is_done=task.is_done,
                     title=task.title) for task in tasks]
