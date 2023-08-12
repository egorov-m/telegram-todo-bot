from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from bot.structures.data_structure import BotMessage
from db import Database
from db.models import User
from src.bot.keyboards.callback_factories import MainCallback, AcceptUserAgreementCallback
from src.lexicon.translator import Translator, translate_list_all
from src.bot.keyboards.main_kb import (
    create_start_keyboard,
    create_main_keyboard,
    create_accept_user_agreement,
    create_back_keyboard
)
from src.bot.utils.html.message_template import task_list, bold_text


start_router = Router(name='start_router')


@start_router.message(Command(*translate_list_all('cmd_start')), StateFilter(default_state))
async def cmd_start(message: Message, translator: Translator):
    """
    Start command handler
    """
    title: str = await translator.translate('cmd_start_description')
    kb = await create_start_keyboard(translator=translator)
    await message.answer(text=bold_text(title),
                         reply_markup=kb)


async def user_agreement_conclusion(event: Message | CallbackQuery,
                                    state: FSMContext,
                                    translator: Translator,
                                    active_user: User):
    user_agreement: str = await translator.translate(BotMessage.USER_AGREEMENT)
    if active_user.user_agreement_acceptance_date is None:
        # The user has not yet accepted the agreement, issue a button
        kb = await create_accept_user_agreement(translator=translator)
        await event.edit_text(text=user_agreement,
                              reply_markup=kb)
    else:
        # The agreement is accepted, we issue a note to that effect
        accept: str = await translator.translate(BotMessage.USER_AGREEMENT_ACCEPTED_MESSAGE)
        message: str = f"{user_agreement}\n\n{bold_text(accept)}"
        kb = await create_back_keyboard(translator=translator)  # back to the main page
        await event.edit_text(text=message,
                              reply_markup=kb)


@start_router.callback_query(AcceptUserAgreementCallback.filter())
async def btn_accept_user_agreement(callback: CallbackQuery,
                                    state: FSMContext,
                                    translator: Translator,
                                    database: Database,
                                    active_user: User):
    await state.clear()
    await state.set_state(default_state)
    await database.user.update_user(active_user.telegram_user_id, user_agreement_acceptance_date=datetime.utcnow())
    await start(translator, database, active_user, callback.message)


@start_router.callback_query(MainCallback.filter())
async def btn_start(callback: CallbackQuery,
                    state: FSMContext,
                    translator: Translator,
                    active_user: User,
                    database: Database):
    await state.clear()
    await state.set_state(default_state)
    await start(translator, database, active_user, callback.message)


async def start(translator: Translator,
                database: Database,
                active_user: User,
                message: Message):
    title: str = await translator.translate(BotMessage.TASK_LIST_TITLE)
    empty: str = await translator.translate(BotMessage.TASK_LIST_EMPTY_MESSAGE)
    tasks = await database.task.get_tasks_for_user(active_user)
    kb = await create_main_keyboard(translator=translator)
    await message.edit_text(text=task_list(tasks, title=title, empty_msg=empty),
                            reply_markup=kb)
