from typing import Callable, Dict, Any, Awaitable
from babel.core import Locale

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.structures.data import TransferData
from src.lexicon.translator import locales, Translator as Tr


class TranslatorMiddleware(BaseMiddleware):
    """
    Middlewares to customize translator for handler
    """

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData
            ) -> Any:

        user_lang: str = data["active_user"].current_language
        locale: str = locales[0]
        for lc in locales:
            if lc == user_lang:
                locale = lc
                break
        t = Locale.parse(locale)
        data['translator'] = Tr(t)
        return await handler(event, data)
