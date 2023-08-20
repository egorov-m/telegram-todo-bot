from datetime import datetime
from hashlib import sha1

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from src.db.models import Task
from src.bot.structures.data_structure import BotMessage, BotItem
from src.db import Database
from src.db.models import User
from src.bot.keyboards.callback_factories import MainCallback, AcceptUserAgreementCallback, UpdateListCallback
from src.lexicon.translator import Translator, translate_list_all
from src.bot.keyboards.main_kb import (
    create_start_keyboard,
    create_main_keyboard,
    create_accept_user_agreement,
    create_back_keyboard
)
from src.bot.utils.message_template import task_list, bold_text, italic_text

start_router = Router(name="start_router")


@start_router.message(Command(*translate_list_all("cmd_start")))
async def cmd_start(message: Message, translator: Translator):
    """
    Start command handler
    """
    title: str = await translator.translate("cmd_start_description")
    kb = await create_start_keyboard(translator=translator)
    await message.answer(text=bold_text(title),
                         reply_markup=kb)


async def user_lockout_message(event: Message | CallbackQuery,
                               *,
                               translator: Translator):
    message: str = f"{bold_text(await translator.translate(BotMessage.USER_LOCKOUT_MESSAGE_TITLE))}\n\n" \
                   f"{italic_text(await translator.translate(BotMessage.USER_LOCKOUT_MESSAGE))}"
    if isinstance(event, Message):
        event: Message
        await event.answer(text=message)
    else:
        event: CallbackQuery
        await event.message.edit_text(text=message)


async def user_agreement_conclusion(event: Message | CallbackQuery,
                                    *,
                                    active_user: User,
                                    translator: Translator):
    message: str = await translator.translate(BotMessage.USER_AGREEMENT)
    if active_user.user_agreement_acceptance_date is None:
        # The user has not yet accepted the agreement, issue a button
        kb = await create_accept_user_agreement(translator=translator)
    else:
        # The agreement is accepted, we issue a note to that effect
        accept: str = await translator.translate(BotMessage.USER_AGREEMENT_ACCEPTED_MESSAGE,
                                                 date=active_user.user_agreement_acceptance_date
                                                 .strftime("%Y-%m-%d %H:%M:%S %Z"))
        message: str = f"{message}\n\n{bold_text(accept)}"
        kb = await create_back_keyboard(translator=translator, where_from=BotItem.SETTINGS)

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text=message, reply_markup=kb)
    else:
        await event.answer(text=message, reply_markup=kb)


@start_router.callback_query(AcceptUserAgreementCallback.filter())
async def btn_accept_user_agreement(callback: CallbackQuery,
                                    state: FSMContext,
                                    *,
                                    database: Database,
                                    active_user: User,
                                    translator: Translator):
    await state.clear()
    await state.set_state(default_state)
    await database.user.update_user(active_user.telegram_user_id,
                                    user_agreement_acceptance_date=datetime.utcnow())
    await start_page(callback,
                     database=database,
                     active_user=active_user,
                     translator=translator)


@start_router.callback_query(MainCallback.filter())
async def btn_start(callback: CallbackQuery,
                    state: FSMContext,
                    *,
                    database: Database,
                    active_user: User,
                    translator: Translator):
    await state.clear()
    await state.set_state(default_state)
    await start_page(callback,
                     database=database,
                     active_user=active_user,
                     translator=translator)


@start_router.callback_query(UpdateListCallback.filter())
async def btn_list_update(callback: CallbackQuery,
                          *,
                          database: Database,
                          active_user: User,
                          translator: Translator):
    new_list_hash: str = callback.data.split(":")[1]
    await start_page(callback,
                     database=database,
                     active_user=active_user,
                     translator=translator,
                     new_list_hash=new_list_hash)


async def start_page(event: Message | CallbackQuery,
                     *,
                     database: Database,
                     active_user: User,
                     translator: Translator,
                     new_list_hash: str = ""):
    callback = None
    if isinstance(event, CallbackQuery):
        message: Message = event.message
        callback: CallbackQuery = event
    else:
        message: Message = event
    tasks = await database.task.get_tasks_for_user(active_user)

    # Checking by hash whether the list needs to be updated
    current_list_hash: str = _get_list_hash(tasks)
    if new_list_hash == current_list_hash:
        if callback is not None:
            await callback.answer()
        return

    title: str = await translator.translate(BotMessage.TASK_LIST_TITLE)
    empty: str = await translator.translate(BotMessage.TASK_LIST_EMPTY_MESSAGE)
    kb = await create_main_keyboard(translator=translator, active_user=active_user, task_list_hash=current_list_hash)
    text = task_list(tasks, title=title, empty_msg=empty)
    await message.edit_text(text=text, reply_markup=kb)


def _get_list_hash(tasks: list[Task]) -> str:
    sha1_hash = sha1()
    sha1_hash.update(str(tasks).encode("utf-8"))
    return sha1_hash.hexdigest()
