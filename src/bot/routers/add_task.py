from aiogram import Router
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.state import default_state, State
from aiogram.fsm.context import FSMContext

from src.config import settings
from src.bot.routers.utils import edit_message, _is_no_valid_input
from src.db.repository import TaskRepository
from src.db import Database
from src.db.models import User
from src.bot.keyboards.task_kb import create_add_task_keyboard
from src.bot.keyboards.main_kb import create_back_keyboard
from src.bot.routers.start import btn_start
from src.bot.states.data import AddTaskStateData
from src.bot.utils.message_template import bold_text, italic_text
from src.bot.keyboards.callback_factories import AddTaskCallback, AddTaskSaveCallback
from src.bot.structures.bot import BotMessage, BotItem
from src.bot.states.groups import AddTaskStates
from src.lexicon.translator import Translator


add_task_router = Router(name="add_task_router")


@add_task_router.callback_query(AddTaskCallback.filter(), default_state)
async def btn_add_task(callback: CallbackQuery,
                       state: FSMContext,
                       *,
                       database: Database,
                       active_user: User,
                       translator: Translator):
    """
    Handler for pressing the add task button
    """
    repo: TaskRepository = database.task
    current_count_tasks = await repo.get_count_tasks_for_user(active_user)
    kb = await create_back_keyboard(translator=translator)
    if current_count_tasks >= settings.COUNT_LIMITS_TASKS_STORAGE_USER:
        msg: str = f"{bold_text(await translator.translate(BotMessage.ADD_TASK_ERROR_TITLE))}\n\n" \
                   f"{italic_text(await translator.translate(BotMessage.ADD_TASK_ERROR_DESCRIPTION, limit=settings.COUNT_LIMITS_TASKS_STORAGE_USER))}"

        await edit_message(callback.message,
                           state,
                           database=database,
                           active_user=active_user,
                           translator=translator,
                           text=msg,
                           kb=kb)
        return

    await state.set_state(state=AddTaskStates.add_task_waiting_title_input)
    data = await state.get_data()
    msg: str = await _get_add_task_full_msg(AddTaskStates.add_task_waiting_title_input,
                                            translator=translator,
                                            data=data)
    message: Message = callback.message
    await state.update_data({AddTaskStateData.ADD_TASK_MESSAGE: message.json()})
    await edit_message(message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)


@add_task_router.callback_query(AddTaskSaveCallback.filter())
async def btn_add_save_new_task(callback: CallbackQuery,
                                state: FSMContext,
                                translator: Translator,
                                database: Database,
                                active_user: User):
    data = await state.get_data()
    repo: TaskRepository = database.task
    await repo.create_task(title=data[AddTaskStateData.TASK_TITLE],
                           description=data[AddTaskStateData.TASK_DESCRIPTION],
                           creator_telegram_user_id=active_user.telegram_user_id)

    await btn_start(callback, state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


async def _get_add_task_msg(translator: Translator,
                            subtitle: str,
                            input_error: bool = False,
                            **kwargs) -> str:
    """
    Getting a message displayed when adding a task
    """
    title: str = await translator.translate(BotMessage.ADD_TASK_MESSAGE, **kwargs)
    error: str = ""
    if input_error:
        error = await translator.translate(BotMessage.INPUT_ERROR_MESSAGE)
    return f'{bold_text(title)}\n\n{italic_text(subtitle)}\n{error}'


async def _get_add_task_full_msg(next_state: State,
                                 *,
                                 translator: Translator,
                                 data: dict[str, any],
                                 input_error: bool = False):
    subtitle: str = await _get_add_task_subtitle(next_state,
                                                 translator=translator)
    task_title = data.get(AddTaskStateData.TASK_TITLE)
    task_description = data.get(AddTaskStateData.TASK_DESCRIPTION)
    msg: str = await _get_add_task_msg(translator,
                                       subtitle,
                                       input_error,
                                       title=task_title,
                                       description=task_description)
    return msg


async def _get_add_task_subtitle(state: State,
                                 *,
                                 translator: Translator) -> str:
    """
    Get a subtitle for messages in the process of adding tasks
    subtitle example: Enter the description of the new task:
    """
    msg: BotMessage | None = None
    match state:
        case AddTaskStates.add_task_waiting_title_input:
            msg = BotMessage.ADD_TASK_ENTER_TITLE
        case AddTaskStates.add_task_waiting_description_input:
            msg = BotMessage.ADD_TASK_ENTER_DESCRIPTION
        case AddTaskStates.add_task_waiting_confirmation:
            msg = BotMessage.ADD_TASK_CONFIRM
    if msg is None:
        raise Exception("The subtitle is not available for the state!")
    else:
        subtitle: str = await translator.translate(msg)
        return subtitle


@add_task_router.message(AddTaskStates.add_task_waiting_title_input)
async def input_title_add_task(message: Message,
                               state: FSMContext,
                               *,
                               database: Database,
                               active_user: User,
                               translator: Translator):
    """
    Task title input handler in the process of adding
    """
    await input_title_add_task_for_str(message.text,
                                       state,
                                       database=database,
                                       active_user=active_user,
                                       translator=translator)


async def input_title_add_task_for_str(text_message: str,
                                       state: FSMContext,
                                       *,
                                       database: Database,
                                       active_user: User,
                                       translator: Translator):
    if _is_no_valid_input(text_message):
        await _invalid_input(state, translator, database, active_user)
    else:
        await state.update_data({AddTaskStateData.TASK_TITLE: text_message})
        data = await state.get_data()
        add_task_message: Message = Message.parse_raw(data[AddTaskStateData.ADD_TASK_MESSAGE])

        msg: str = await _get_add_task_full_msg(AddTaskStates.add_task_waiting_description_input,
                                                translator=translator,
                                                data=data)
        kb = await create_add_task_keyboard(translator=translator, where_from=BotItem.ADD_TASK)
        await state.set_state(AddTaskStates.add_task_waiting_description_input)
        await edit_message(add_task_message,
                           state,
                           database=database,
                           active_user=active_user,
                           translator=translator,
                           text=msg,
                           kb=kb)


@add_task_router.message(AddTaskStates.add_task_waiting_description_input)
async def input_description_aad_task(message: Message,
                                     state: FSMContext,
                                     *,
                                     database: Database,
                                     active_user: User,
                                     translator: Translator):
    """
    Task description input handler in the process of adding
    """
    await input_description_aad_task_for_str(message.text,
                                             state,
                                             database=database,
                                             active_user=active_user,
                                             translator=translator)


async def input_description_aad_task_for_str(text_message: str,
                                             state: FSMContext,
                                             *,
                                             database: Database,
                                             active_user: User,
                                             translator: Translator):
    if _is_no_valid_input(text_message):
        await _invalid_input(state, translator)
    else:
        await state.update_data({AddTaskStateData.TASK_DESCRIPTION: text_message})
        data = await state.get_data()
        add_task_message: Message = Message.parse_raw(data[AddTaskStateData.ADD_TASK_MESSAGE])

        msg: str = await _get_add_task_full_msg(AddTaskStates.add_task_waiting_confirmation,
                                                translator=translator,
                                                data=data)
        kb = await create_add_task_keyboard(translator=translator,
                                            task_data=data,
                                            where_from=BotItem.ADD_TASK,
                                            isSave=True)
        await state.set_state(AddTaskStates.add_task_waiting_confirmation)
        await edit_message(add_task_message,
                           state,
                           database=database,
                           active_user=active_user,
                           translator=translator,
                           text=msg,
                           kb=kb)


async def _invalid_input(state: FSMContext,
                         *,
                         database: Database,
                         active_user: User,
                         translator: Translator) -> bool:
    """
    Editing the message in case of incorrect data entry by the user
    """
    data = await state.get_data()
    add_task_message: Message = Message.parse_raw([AddTaskStateData.ADD_TASK_MESSAGE])
    st = await state.get_state()
    msg: str = _get_add_task_full_msg(st,
                                      translator=translator,
                                      data=data,
                                      input_error=True)
    kb = await create_back_keyboard(translator=translator)
    await edit_message(add_task_message,
                       state,
                       database=database,
                       active_user=active_user,
                       translator=translator,
                       text=msg,
                       kb=kb)
