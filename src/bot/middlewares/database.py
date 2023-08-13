from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.data_structure import TransferData
from src.db import Database


class DatabaseMiddleware(BaseMiddleware):
    """
    Middlewares to customize database session for handler
    """

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData
            ) -> Any:

        pool: Callable[[], AsyncSession] = data["pool"]
        try:
            session: AsyncSession = pool()
            async with session.begin() as transaction:
                data["database"] = Database(session)
                return await handler(event, data)
        finally:
            await session.close()
