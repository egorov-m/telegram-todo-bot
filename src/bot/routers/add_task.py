from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.state import default_state, State
from aiogram.fsm.context import FSMContext

from src.bot.keyboards.add_task_kb import create_add_task_keyboard
from src.bot.keyboards.main_kb import create_back_keyboard
from src.bot.routers.start import start, btn_start
from src.bot.states.data import AddTaskStateData
from src.bot.utils.html.message_template import bold_text, italic_text
from src.bot.keyboards.callback_factories import AddTaskCallback, AddTaskSaveCallback
from src.bot.structures.data_structure import BotMessage, BotItem
from src.bot.states.state import AddTaskStates
from src.lexicon.translator import Translator

add_task_router = Router(name='add_task_router')


@add_task_router.callback_query(AddTaskCallback.filter(), default_state)
async def btn_add_task(callback: CallbackQuery, state: FSMContext, translator: Translator):
    """
    Handler for pressing the add task button
    """
    await state.set_state(state=AddTaskStates.add_task_waiting_title_input)
    data = await state.get_data()
    msg: str = await _get_add_task_full_msg(translator, AddTaskStates.add_task_waiting_title_input, data)
    kb = await create_back_keyboard(translator=translator)
    message: Message = callback.message
    await state.update_data({AddTaskStateData.ADD_TASK_MESSAGE: message})
    await _edit_message(message, state, msg, kb, translator)


@add_task_router.callback_query(AddTaskSaveCallback.filter())
async def btn_add_save_new_task(callback: CallbackQuery, state: FSMContext, translator: Translator):

    # Here will be a call to the task service for adding a new task to the database

    await btn_start(callback, state, translator)


async def _get_add_task_msg(translator: Translator, subtitle: str, input_error: bool = False, **kwargs) -> str:
    """
    Getting a message displayed when adding a task
    """
    title: str = await translator.translate(BotMessage.ADD_TASK_MESSAGE, kwargs)
    error: str = ""
    if input_error:
        error = await translator.translate(BotMessage.INPUT_ERROR_MESSAGE)
    return f'{bold_text(title)}\n\n{italic_text(subtitle)}\n{error}'


async def _get_add_task_full_msg(translator: Translator,
                                 next_state: State,
                                 data: dict[str, any],
                                 input_error: bool = False):
    subtitle: str = await _get_add_task_subtitle(translator, next_state)
    task_title = data.get(AddTaskStateData.TASK_TITLE)
    task_description = data.get(AddTaskStateData.TASK_DESCRIPTION)
    msg: str = await _get_add_task_msg(translator,
                                       subtitle,
                                       input_error,
                                       title=task_title,
                                       description=task_description)
    return msg


async def _get_add_task_subtitle(translator: Translator, state: State) -> str:
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
async def input_title_add_task(message: types.Message, state: FSMContext, translator: Translator):
    """
    Task title input handler in the process of adding
    """
    await input_title_add_task_for_str(message.text, state, translator)


async def input_title_add_task_for_str(message: str, state: FSMContext, translator: Translator):
    if _is_no_valid_input(message):
        await _invalid_input(state, translator)
    else:
        await state.update_data({AddTaskStateData.TASK_TITLE: message})
        data = await state.get_data()
        add_task_message: Message = data[AddTaskStateData.ADD_TASK_MESSAGE]

        msg: str = await _get_add_task_full_msg(translator,
                                                AddTaskStates.add_task_waiting_description_input,
                                                data)
        kb = await create_add_task_keyboard(translator=translator, where_from=BotItem.ADD_TASK)
        await state.set_state(AddTaskStates.add_task_waiting_description_input)
        await _edit_message(add_task_message, state, msg, kb, translator)


@add_task_router.message(AddTaskStates.add_task_waiting_description_input)
async def input_description_aad_task(message: types.Message, state: FSMContext, translator: Translator):
    """
    Task description input handler in the process of adding
    """
    await input_description_aad_task_for_str(message.text, state, translator)


async def input_description_aad_task_for_str(message: str, state: FSMContext, translator: Translator):
    if _is_no_valid_input(message):
        await _invalid_input(state, translator)
    else:
        await state.update_data({AddTaskStateData.TASK_DESCRIPTION: message})
        data = await state.get_data()
        add_task_message: Message = data[AddTaskStateData.ADD_TASK_MESSAGE]

        msg: str = await _get_add_task_full_msg(translator,
                                                AddTaskStates.add_task_waiting_confirmation,
                                                data)
        kb = await create_add_task_keyboard(translator=translator,
                                            task_data=data,
                                            where_from=BotItem.ADD_TASK,
                                            isSave=True)
        await state.set_state(AddTaskStates.add_task_waiting_confirmation)
        await _edit_message(add_task_message, state, msg, kb, translator)


async def _invalid_input(state: FSMContext, translator: Translator) -> bool:
    """
    Editing the message in case of incorrect data entry by the user
    """
    data = await state.get_data()
    add_task_message: Message = data[AddTaskStateData.ADD_TASK_MESSAGE]
    st = await state.get_state()
    msg: str = _get_add_task_full_msg(translator, st, data, True)
    kb = await create_back_keyboard(translator=translator)
    await _edit_message(add_task_message, state, msg, kb, translator)


async def _edit_message(message: types.Message,
                        state: FSMContext,
                        text: str,
                        kb: InlineKeyboardMarkup,
                        translator: Translator):
    """
    Editing a message (an error handler has been added in case of incorrect messages)
    """
    try:
        await message.edit_text(text=text,
                                reply_markup=kb)
    except ValueError:
        await state.clear()
        await state.set_state(default_state)
        await start(translator, message)


def _is_no_valid_input(text: str | None):
    """
    Whether text input from a user is invalid
    """
    return (text is None or
            text.isspace() or
            text == '' or
            text.__contains__("\"") or
            text.__contains__("\'"))
