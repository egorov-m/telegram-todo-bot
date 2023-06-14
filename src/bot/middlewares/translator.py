from typing import Callable, Dict, Any, Awaitable
from babel.core import Locale

from aiogram import BaseMiddleware
from aiogram.types import Message

from ..structures.data_structure import TransferData
from src.lexicon.translator import locales, Translator as Tr


class TranslatorMiddleware(BaseMiddleware):
    """
    Middlewares to customize translator for handler
    """

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: TransferData
            ) -> Any:
        """

        """
        lang_code: str = event.from_user.language_code
        locale: str = locales[0]
        for lc in locales:
            if lc.split('_')[0] == lang_code:
                locale = lc
                break
        t = Locale.parse(locale)
        data['translator'] = Tr(t)
        return await handler(event, data)
