from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards.callback_factories import MainCallback
from src.lexicon.translator import Translator, translate_list_all
from src.bot.keyboards.main_kb import create_start_keyboard, create_main_keyboard
from src.bot.utils.html.message_template import task_list, bold_text
from src.bot.services.task import TaskService


start_router = Router(name='start_router')


@start_router.message(Command(*translate_list_all('cmd_start')), StateFilter(default_state))
async def cmd_start(message: types.Message, translator: Translator):
    """
    Start command handler
    """
    title: str = await translator.translate('cmd_start_description')
    kb = await create_start_keyboard(translator=translator)
    await message.answer(text=bold_text(title),
                         reply_markup=kb)


@start_router.callback_query(MainCallback.filter())
async def btn_start(callback: CallbackQuery, state: FSMContext, translator: Translator):
    await state.clear()
    await state.set_state(default_state)
    await start(translator, callback.message)


async def start(translator: Translator, message: Message):
    task_service: TaskService = TaskService()
    title: str = await translator.translate('task_list_title')
    empty: str = await translator.translate('task_list_empty_message')
    tasks = await task_service.get_tasks_for_user(user=None)
    kb = await create_main_keyboard(translator=translator)
    await message.edit_text(text=task_list(tasks, title=title, empty_msg=empty),
                            reply_markup=kb)
