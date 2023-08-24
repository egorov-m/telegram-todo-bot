from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter
from aiogram.types import CallbackQuery, Message

from src.bot.routers.start import btn_start
from src.bot.states.data import EditTaskStateData, EditTask
from src.db.repository import TaskRepository
from src.bot.keyboards.callback_factories import (
    EditTaskCallback,
    SelectTaskForEditCallback,
    SaveEditTaskCallback,
    EditTaskTitleCallback,
    EditTaskDescriptionCallback
)
from src.bot.keyboards.task_kb import create_edit_task_select_task_keyboard, create_edit_task_select_edit_item_keyboard
from src.bot.routers.utils import edit_message, _is_no_valid_input
from src.bot.states.groups import EditTaskStates
from src.bot.structures.bot import BotMessage
from src.bot.utils.message_template import bold_text, italic_text, done_marker
from src.db import Database
from src.db.models import User, Task
from src.lexicon import Translator


edit_task_router = Router(name="edit_task_router")


@edit_task_router.callback_query(EditTaskCallback.filter(), default_state)
async def btn_edit_task(callback: CallbackQuery,
                        state: FSMContext,
                        *,
                        database: Database,
                        active_user: User,
                        translator: Translator):
    """
    Handler for pressing the edit task button
    """
    await state.set_state(state=EditTaskStates.edit_task_waiting_select_task)
    msg: str = await _get_edit_task_full_msg(translator)
    repo: TaskRepository = database.task
    kb = await create_edit_task_select_task_keyboard(translator=translator,
                                                     tasks=await repo.get_tasks_for_user(active_user))
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@edit_task_router.callback_query(SelectTaskForEditCallback.filter(), EditTaskStates.edit_task_waiting_select_task)
async def btn_edit_selected_task(callback: CallbackQuery,
                                 state: FSMContext,
                                 *,
                                 database: Database,
                                 active_user: User,
                                 translator: Translator):
    await state.set_state(state=EditTaskStates.edit_task_waiting_select_edit_item)
    task_id = callback.data.split(":")[1]
    repo: TaskRepository = database.task
    task: Task = await repo.get_task(task_id=task_id)
    edit_task: EditTask = EditTask(task_id=task_id,
                                   is_done=task.is_done,
                                   title=task.title,
                                   description=task.description)
    await state.set_data(EditTaskStateData(task=edit_task))
    msg: str = await _get_edit_task_full_selected_task_msg(translator, task=edit_task)
    kb = await create_edit_task_select_edit_item_keyboard(translator=translator)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@edit_task_router.callback_query(
    EditTaskTitleCallback.filter(),
    StateFilter(
        EditTaskStates.edit_task_waiting_select_edit_item,
        EditTaskStates.edit_task_waiting_title_input,
        EditTaskStates.edit_task_waiting_description_input
    )
)
async def btn_edit_title_task(callback: CallbackQuery,
                              state: FSMContext,
                              *,
                              database: Database,
                              active_user: User,
                              translator: Translator):
    await state.set_state(state=EditTaskStates.edit_task_waiting_title_input)
    data = await state.get_data()
    task: EditTask = data["task"]
    await state.update_data(EditTaskStateData(task=task, edit_task_message=callback.message.json()))
    msg: str = await _get_edit_task_full_selected_task_msg(translator, task=task, is_enter_title=True)
    kb = await create_edit_task_select_edit_item_keyboard(translator=translator)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@edit_task_router.message(EditTaskStates.edit_task_waiting_title_input)
async def input_title_task(message: Message,
                           state: FSMContext,
                           *,
                           database: Database,
                           active_user: User,
                           translator: Translator):
    await input_item_task(message,
                          state,
                          item_task="title",
                          database=database,
                          active_user=active_user,
                          translator=translator)


@edit_task_router.message(EditTaskStates.edit_task_waiting_description_input)
async def input_description_task(message: Message,
                                 state: FSMContext,
                                 *,
                                 database: Database,
                                 active_user: User,
                                 translator: Translator):
    await input_item_task(message,
                          state,
                          item_task="description",
                          database=database,
                          active_user=active_user,
                          translator=translator)


async def input_item_task(message: Message,
                          state: FSMContext,
                          *,
                          item_task: str = "title",
                          database: Database,
                          active_user: User,
                          translator: Translator):
    data = await state.get_data()
    task: EditTask = data["task"]
    main_message: Message = Message.parse_raw(data["edit_task_message"])
    if not _is_no_valid_input(message.text):
        task[item_task] = message.text
        await state.update_data(data)

    await state.set_state(EditTaskStates.edit_task_waiting_select_edit_item)
    msg: str = await _get_edit_task_full_selected_task_msg(translator, task=task)
    kb = await create_edit_task_select_edit_item_keyboard(translator=translator)
    await edit_message(main_message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@edit_task_router.callback_query(
    EditTaskDescriptionCallback.filter(),
    StateFilter(
        EditTaskStates.edit_task_waiting_select_edit_item,
        EditTaskStates.edit_task_waiting_title_input,
        EditTaskStates.edit_task_waiting_description_input
    )
)
async def btn_edit_description_task(callback: CallbackQuery,
                                    state: FSMContext,
                                    *,
                                    database: Database,
                                    active_user: User,
                                    translator: Translator):
    await state.set_state(state=EditTaskStates.edit_task_waiting_description_input)
    data = await state.get_data()
    task: EditTask = data["task"]
    await state.update_data(EditTaskStateData(task=task, edit_task_message=callback.message.json()))
    msg: str = await _get_edit_task_full_selected_task_msg(translator, task=task, is_enter_title=False)
    kb = await create_edit_task_select_edit_item_keyboard(translator=translator)
    await edit_message(callback.message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@edit_task_router.callback_query(SaveEditTaskCallback.filter(), EditTaskStates.edit_task_waiting_select_edit_item)
async def btn_save_edit_task(callback: CallbackQuery,
                             state: FSMContext,
                             *,
                             database: Database,
                             active_user: User,
                             translator: Translator):
    task = (await state.get_data())["task"]

    repo: TaskRepository = database.task
    await repo.update_task(task["task_id"], title=task["title"], description=task["description"])
    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


async def _get_edit_task_full_msg(translator: Translator):
    return f"{bold_text(await translator.translate(BotMessage.EDIT_TASK_MESSAGE_TITLE))}\n\n" \
           f"{italic_text(await translator.translate(BotMessage.EDIT_TASK_MESSAGE_SUBTITLE))}"


async def _get_edit_task_full_selected_task_msg(translator: Translator, task: EditTask, is_enter_title: bool | None = None):
    subtitle: str = await translator.translate(BotMessage.EDIT_TASK_MESSAGE_SUBTITLE_TASK,
                                               is_done=done_marker(task["is_done"]),
                                               title=bold_text(task["title"]),
                                               description=italic_text(task["description"]))
    subtitle2: str
    if is_enter_title is None:
        subtitle2 = await translator.translate(BotMessage.EDIT_TASK_MESSAGE_SUBTITLE_EDIT)
    else:
        if is_enter_title:
            subtitle2 = await translator.translate(BotMessage.EDIT_TASK_MESSAGE_ENTER_TITLE)
        else:
            subtitle2 = await translator.translate(BotMessage.EDIT_TASK_MESSAGE_ENTER_DESCRIPTION)
    return f"{bold_text(await translator.translate(BotMessage.EDIT_TASK_MESSAGE_TITLE))}\n" \
           f"{subtitle}\n\n" \
           f"{italic_text(subtitle2)}"
