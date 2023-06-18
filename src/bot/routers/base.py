from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.state import default_state, State

from bot.routers.add_task import btn_add_task, input_title_add_task_for_str
from bot.routers.settings import btn_settings
from bot.routers.start import btn_start
from bot.states.data import AddTaskStateData
from bot.states.state import AddTaskStates
from bot.structures.data_structure import BotItem
from src.bot.keyboards.callback_factories import BackCallback, CancelCallback
from src.lexicon.translator import Translator


base_router = Router(name='base_router')


@base_router.callback_query(BackCallback.filter())
async def btn_back(callback: CallbackQuery, state: FSMContext, translator: Translator):
    data = callback.data.split(':')[1]
    match data:
        case BotItem.SETTINGS:
            await btn_settings(callback, translator)
        case BotItem.ADD_TASK:
            st: State = await state.get_state()
            match st:
                case AddTaskStates.add_task_waiting_description_input:
                    await btn_add_task(callback, state, translator)
                case AddTaskStates.add_task_waiting_confirmation:
                    state_data = await state.get_data()
                    # an alternative version of the handler is used, receiving the message as a string
                    await input_title_add_task_for_str(state_data.get(AddTaskStateData.TASK_TITLE),
                                                       state,
                                                       translator)

                case _:
                    await btn_cancel(callback, state, translator)
        case _:
            await btn_cancel(callback, state, translator)


@base_router.callback_query(CancelCallback.filter())
async def btn_cancel(callback: CallbackQuery, state: FSMContext, translator: Translator):
    await state.clear()
    await state.set_state(default_state)
    await btn_start(callback, state, translator)