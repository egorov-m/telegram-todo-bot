from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field

from src.db.models.base import Base


class Task(Base, table=True):
    """
    Task model
    """
    id: UUID = Field(
        sa_column=sa.Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid4, server_default=sa.text("gen_random_uuid()")
        )
    )
    title: str = Field(nullable=False, max_length=64)
    description: str = Field(nullable=False, max_length=256)
    creator_telegram_user_id: int = Field(sa_column=sa.Column(sa.BigInteger,
                                                              nullable=False), foreign_key="user.telegram_user_id")
    created_date: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()
        )
    )
    is_done: bool = Field(
        sa_column=sa.Column(sa.Boolean, default=False, server_default=sa.false(), nullable=False)
    )
    is_exist: bool = Field(
        sa_column=sa.Column(sa.Boolean, default=True, server_default=sa.true(), nullable=False)
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}," \
               f"title={self.title!r}," \
               f"description={self.description!r}," \
               f"creator_telegram_user_id={self.creator_telegram_user_id!r}," \
               f"created_date={self.created_date!r}," \
               f"is_done={self.is_done!r}," \
               f"is_exist={self.is_exist!r})"
