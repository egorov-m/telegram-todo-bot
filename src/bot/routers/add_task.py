from enum import StrEnum

from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.state import default_state, State
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_kb import create_back_keyboard
from bot.routers.start import start
from bot.utils.html.message_template import bold_text, italic_text
from src.bot.keyboards.callback_factories import AddTaskCallback
from src.bot.structures.data_structure import BotMessage
from src.bot.states.state import AddTaskStates
from src.lexicon.translator import Translator

add_task_router = Router(name='add_task_router')


@add_task_router.callback_query(AddTaskCallback.filter(), default_state)
async def btn_add_task(callback: CallbackQuery, state: FSMContext, translator: Translator):
    await state.set_state(state=AddTaskStates.add_task_waiting_title_input)
    subtitle: str = await _get_add_task_subtitle(translator, AddTaskStates.add_task_waiting_title_input)
    msg: str = await _get_add_task_msg(translator, subtitle)
    kb = await create_back_keyboard(translator=translator)
    message: Message = callback.message
    await state.set_data({AddTaskStateData.ADD_TASK_MESSAGE: message})
    await _edit_message(message, state, msg, kb, translator)


async def _get_add_task_msg(translator: Translator, subtitle: str, input_error: bool = False, **kwargs) -> str:
    title: str = await translator.translate(BotMessage.ADD_TASK_MESSAGE, kwargs)
    error: str = ""
    if input_error:
        error = await translator.translate(BotMessage.INPUT_ERROR_MESSAGE)
    return f'{bold_text(title)}\n\n{italic_text(subtitle)}\n{error}'


async def _get_add_task_subtitle(translator: Translator, state: State) -> str:
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
    if _is_no_valid_input(message.text):
        await _invalid_input(state, translator)
    else:
        data = await state.get_data()
        add_task_message: Message = data[AddTaskStateData.ADD_TASK_MESSAGE]
        subtitle: str = await _get_add_task_subtitle(translator, AddTaskStates.add_task_waiting_description_input)
        task_title = message.text
        msg: str = await _get_add_task_msg(translator, subtitle, title=task_title)
        kb = await create_back_keyboard(translator=translator)
        await state.update_data({AddTaskStateData.TASK_TITLE: task_title})
        await state.set_state(AddTaskStates.add_task_waiting_description_input)
        await _edit_message(add_task_message, state, msg, kb, translator)


@add_task_router.message(AddTaskStates.add_task_waiting_description_input)
async def input_description_aad_task(message: types.Message, state: FSMContext, translator: Translator):
    if _is_no_valid_input(message.text):
        await _invalid_input(state, translator)
    else:
        data = await state.get_data()
        add_task_message: Message = data[AddTaskStateData.ADD_TASK_MESSAGE]
        subtitle: str = await _get_add_task_subtitle(translator, AddTaskStates.add_task_waiting_confirmation)
        task_data = await state.get_data()
        task_description = message.text
        msg: str = await _get_add_task_msg(translator,
                                           subtitle,
                                           title=task_data[AddTaskStateData.TASK_TITLE],
                                           description=task_description)
        kb = await create_back_keyboard(translator=translator)
        await state.update_data({AddTaskStateData.TASK_DESCRIPTION: task_description})
        await _edit_message(add_task_message, state, msg, kb, translator)


async def _invalid_input(state: FSMContext, translator: Translator) -> bool:
    data = await state.get_data()
    add_task_message: Message = data[AddTaskStateData.ADD_TASK_MESSAGE]
    st = await state.get_state()
    subtitle: str = await _get_add_task_subtitle(translator, st)
    msg: str = await _get_add_task_msg(translator,
                                       subtitle,
                                       True,
                                       title=data.get(AddTaskStateData.TASK_TITLE),
                                       description=data.get(AddTaskStateData.TASK_DESCRIPTION))
    kb = await create_back_keyboard(translator=translator)
    await _edit_message(add_task_message, state, msg, kb, translator)


async def _edit_message(message: types.Message,
                        state: FSMContext,
                        text: str,
                        kb: InlineKeyboardMarkup,
                        translator: Translator):
    try:
        await message.edit_text(text=text,
                                reply_markup=kb)
    except ValueError:
        await state.clear()
        await state.set_state(default_state)
        await start(translator, message)


def _is_no_valid_input(text: str | None):
    return (text is None or
            text.isspace() or
            text == '' or
            text.__contains__("\"") or
            text.__contains__("\'"))


class AddTaskStateData(StrEnum):
    TASK_TITLE = "task_title"
    TASK_DESCRIPTION = "task_description"
    ADD_TASK_MESSAGE = "add_task_message"
