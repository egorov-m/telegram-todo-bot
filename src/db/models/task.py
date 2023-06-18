from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field
from .base import Base


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
    reg_telegram_user_id: int = Field(sa_column=sa.Column(sa.BigInteger, nullable=False))
    reg_datetime: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()
        )
    )
    is_done: bool = Field(
        sa_column=sa.Column(sa.Boolean, default=False, server_default=sa.false(), nullable=False)
    )
    is_exist: bool = Field(
        sa_column=sa.Column(sa.Boolean, default=False, server_default=sa.false(), nullable=False)
    )
    id_user: UUID = Field(nullable=False, foreign_key="user.id")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}," \
               f"title={self.title!r}," \
               f"description={self.description!r}," \
               f"reg_telegram_user_id={self.reg_telegram_user_id!r}," \
               f"reg_datetime={self.reg_datetime!r}," \
               f"isDone={self.is_done!r}," \
               f"isExist={self.is_exist!r}," \
               f"idUser={self.id_user!r})"
