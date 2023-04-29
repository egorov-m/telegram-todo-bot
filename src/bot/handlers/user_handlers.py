from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state

from db.models.task import Task
import lexicon as lx
import bot.keyboards as kb

lexicon: lx.LEXICON = lx.LEXICON_EN()

router: Router = Router()

test_list: List[Task] = [Task(0, 'Test', 'Description', True), Task(
    1, 'Test2', 'Description2', False), Task(2, 'Test3', 'Description3', True)]


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    locale = message.from_user.language_code.title()
    print(locale)
    await message.answer(text=lexicon.start_command(test_list), reply_markup=kb.create_main_keyboard(lx.LEXICON_EN()))
