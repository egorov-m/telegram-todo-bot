from locale import normalize
from typing import Callable, Awaitable
import logging as log

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.routers.start import user_agreement_conclusion
from bot.structures.data_structure import TransferData, LoggerType
from db import Database
from db.models import User
from db.repository import UserRepository
from exceptions import ToDoBotError

logger = log.getLogger(LoggerType.BOT_LOGGER)


class ActiveUserMiddleware(BaseMiddleware):
    """
    Middleware to retrieve a user from the database
    """

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, any]], Awaitable[any]],
            event: Message | CallbackQuery,
            data: TransferData
            ) -> any:

        database: Database = data["database"]
        repo: UserRepository = database.user
        telegram_user_id = event.from_user.id
        user: User
        try:
            user = repo.get_user(telegram_user_id)
        except ToDoBotError:
            user_lang = normalize(event.from_user.language_code.replace('-', '_'))
            user = await repo.create_user(telegram_user_id, user_lang)

        data["active_user"] = user
        return await handler(event, data)


class ProtectionUserMiddleware(BaseMiddleware):
    """
    Middleware for user protection
    """

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, any]], Awaitable[any]],
            event: Message | CallbackQuery,
            data: TransferData
    ) -> any:

        user: User = data["active_user"]
        if not user.enabled:
            pass
        elif user.user_agreement_acceptance_date is None:
            return await user_agreement_conclusion(event, *data)
        else:
            return await handler(event, data)
