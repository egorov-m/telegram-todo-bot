from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field

from src.bot.structures.event import EventType
from src.db.models.base import Base


class Event(Base, table=True):
    """
    Event model
    """
    id: UUID = Field(
        sa_column=sa.Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid4, server_default=sa.text("gen_random_uuid()")
        )
    )
    type: EventType = Field(sa_column=sa.Column(sa.Enum(EventType), nullable=False))
    occurrence_date: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()
        )
    )
    callback_data_prefix: Optional[str] = Field(nullable=True, max_length=64)
    state: Optional[str] = Field(nullable=True, max_length=256)
    telegram_user_id: int = Field(sa_column=sa.Column(sa.BigInteger, nullable=False), foreign_key="user.telegram_user_id")
