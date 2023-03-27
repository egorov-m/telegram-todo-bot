from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon_en import LEXICON_EN

lexicon_en: LEXICON_EN = LEXICON_EN()
router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=lexicon_en.start_command)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=lexicon_en.help_command)
