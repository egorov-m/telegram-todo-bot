from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.structures.data_structure import TransferData


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
        session = pool()
        data["db_session"] = session
        try:
            return await handler(event, data)
        finally:
            await session.close()
