import logging as log

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.state import State, default_state
from aiogram.types import ErrorEvent

from src.bot.structures.types import LoggerType
from src.bot.routers.admin import btn_admin_panel
from src.bot.routers.edit_task import btn_edit_task
from src.db import Database
from src.db.models import User
from src.bot.routers.add_task import btn_add_task, input_title_add_task_for_str
from src.bot.routers.settings import btn_settings
from src.bot.routers.start import btn_start
from src.bot.states.data import AddTaskStateData
from src.bot.states.groups import AddTaskStates
from src.bot.structures.bot import BotItem, BotMessage
from src.bot.keyboards.callback_factories import BackCallback, CancelCallback, EmptyCallback, HideCallback
from src.lexicon.translator import Translator


base_router = Router(name='base_router')
logger = log.getLogger(LoggerType.BOT_ERROR_LOGGER)


@base_router.callback_query(BackCallback.filter())
async def btn_back(callback: CallbackQuery,
                   state: FSMContext,
                   *,
                   database: Database,
                   active_user: User,
                   translator: Translator):
    data = callback.data.split(':')[1]
    match data:
        case BotItem.SETTINGS:
            await btn_settings(callback,
                               state,
                               database=database,
                               active_user=active_user,
                               translator=translator)
        case BotItem.ADD_TASK:
            st: State = await state.get_state()
            match st:
                case AddTaskStates.add_task_waiting_description_input:
                    await btn_add_task(callback, state,
                                       database=database,
                                       active_user=active_user,
                                       translator=translator)
                case AddTaskStates.add_task_waiting_confirmation:
                    state_data: AddTaskStateData = await state.get_data()
                    # an alternative version of the handler is used, receiving the message as a string
                    await input_title_add_task_for_str(state_data["task_title"],
                                                       state,
                                                       database=database,
                                                       active_user=active_user,
                                                       translator=translator)

                case _:
                    await btn_cancel(callback,
                                     state,
                                     database=database,
                                     active_user=active_user,
                                     translator=translator)
        case BotItem.EDIT_TASK:
            await btn_edit_task(callback,
                                state,
                                database=database,
                                active_user=active_user,
                                translator=translator)
        case BotItem.ADMIN_PANEL:
            await state.clear()
            await btn_admin_panel(callback,
                                  state,
                                  database=database,
                                  active_user=active_user,
                                  translator=translator)
        case _:
            await btn_cancel(callback,
                             state,
                             database=database,
                             active_user=active_user,
                             translator=translator)


@base_router.callback_query(CancelCallback.filter())
async def btn_cancel(callback: CallbackQuery,
                     state: FSMContext,
                     *,
                     database: Database,
                     active_user: User,
                     translator: Translator):
    await state.set_state(default_state)
    await btn_start(callback,
                    state,
                    database=database,
                    active_user=active_user,
                    translator=translator)


@base_router.callback_query(HideCallback.filter())
async def btn_hide(callback: CallbackQuery):
    await callback.message.delete()


@base_router.callback_query(EmptyCallback.filter())
async def empty(callback: CallbackQuery):
    await callback.answer()


@base_router.errors()
async def errors_bot_handler(event: ErrorEvent,
                             *,
                             translator: Translator):
    callback: CallbackQuery = event.update.callback_query
    text = await translator.translate(BotMessage.EXCEPTION_MESSAGE)
    exc: Exception = event.exception
    logger.error(exc)

    if callback is not None:
        await callback.answer(text=text)
    else:
        message = event.update.message
        if message is not None:
            await message.answer(text=text)
