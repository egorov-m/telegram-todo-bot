from locale import normalize
from typing import Callable, Awaitable
import logging as log

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.bot.routers.start import user_agreement_conclusion, user_lockout_message
from src.bot.structures.data_structure import TransferData, LoggerType, BotItem
from src.db import Database
from src.db.models import User
from src.db.repository import UserRepository
from src.exceptions import ToDoBotError

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
            user = await repo.get_user(telegram_user_id)
        except ToDoBotError:
            user_lang = normalize(event.from_user.language_code.replace('-', '_')).split(".")[0]
            # normalize format en_US.UTF-8, need: en_US
            user = await repo.create_user(telegram_user_id, current_language=user_lang)

        await repo.update_user_last_activity(user.telegram_user_id)
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
            await user_lockout_message(event, translator=data["translator"])
        elif user.user_agreement_acceptance_date is None:
            if isinstance(event, CallbackQuery) and event.data == BotItem.ACCEPTED_USER_AGREEMENT:
                # so that there is no looping when you press the agreement button
                return await handler(event, data)
            else:
                return await user_agreement_conclusion(event, active_user=user, translator=data["translator"])
        else:
            return await handler(event, data)
