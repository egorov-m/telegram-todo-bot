from typing import Optional

from sqlalchemy import desc
from sqlalchemy.engine import Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.sql.functions import func
from sqlmodel import select

from src.bot.structures.types import BotEventType
from src.exceptions import ToDoBotError, ToDoBotErrorCode
from src.db.models import User, Event
from src.bot.structures.role import Role
from src.db.utils import manage_data_protection_method, menage_db_method, CommitMode


class EventRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    @manage_data_protection_method(Role.ADMINISTRATOR)
    async def get_event(self, active_user: User, event_id: int) -> Event:
        event: Event = await self.session.get(Event, event_id)
        if event is None:
            raise ToDoBotError("Event not found", ToDoBotErrorCode.EVENT_NOT_FOUND)

        return event

    @manage_data_protection_method(Role.ADMINISTRATOR)
    async def get_events(self,
                         active_user: User,
                         *,
                         order: UnaryExpression = desc(Event.occurrence_date)) -> list[Event]:
        result: Result = await self.session.execute(
            select(Event).order_by(order, desc(Event.telegram_user_id))
        )
        return result.scalars().all()

    @manage_data_protection_method(Role.ADMINISTRATOR)
    async def get_events_for_timeline(self,
                                      active_user: User,
                                      *,
                                      grouping_field=Event.callback_data_prefix) -> list[Row]:
        date = func.date_trunc("hour", Event.occurrence_date).label("occurrence_date")
        result: Result = await self.session.execute(
            select(date, grouping_field, func.count(Event.id))
            .where(grouping_field.isnot(None)).group_by(Event.occurrence_date, grouping_field)
        )
        return result.all()

    @menage_db_method(CommitMode.FLUSH)
    async def create_event(self,
                           active_user: User,
                           *,
                           event_type: BotEventType,
                           callback_data_prefix: Optional[str] = None,
                           state: Optional[str] = None):
        new_event: Event = Event(type=event_type,
                                 callback_data_prefix=callback_data_prefix,
                                 state=state,
                                 telegram_user_id=active_user.telegram_user_id)

        self.session.add(new_event)
        return new_event
