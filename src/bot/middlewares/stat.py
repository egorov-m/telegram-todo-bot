from typing import Callable, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.structures.event import EventType
from src.db import Database
from src.db.repository import EventRepository
from src.bot.structures.data_structure import TransferData
from src.db.models import User


class StatMiddleware(BaseMiddleware):
    """
    Middleware for stats purposes
    """

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, any]], Awaitable[any]],
            event: Message | CallbackQuery,
            data: TransferData
    ) -> any:

        database: Database = data["database"]
        repo: EventRepository = database.event

        active_user: User = data["active_user"]
        callback_data_prefix: Optional[str] = None
        fsm_context: FSMContext = data["state"]
        state = await fsm_context.get_state()

        if isinstance(event, CallbackQuery):
            event_type: EventType = EventType.CALLBACK_QUERY
            callback_data_prefix = event.data.split(':')[0]
        elif isinstance(event, Message):
            event_type: EventType = EventType.MESSAGE

        await repo.create_event(active_user,
                                event_type=event_type,
                                callback_data_prefix=callback_data_prefix,
                                state=state)
        return await handler(event, data)
