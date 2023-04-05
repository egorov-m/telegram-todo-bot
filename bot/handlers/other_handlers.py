from aiogram import Router
from aiogram.types import Message

import lexicon as lx

router: Router = Router()
lexicon: lx.LEXICON = lx.LEXICON_EN()


@router.message()
async def send_error_message(message: Message):
    await message.answer(f'{message.text}\n{lexicon.error_message}')
