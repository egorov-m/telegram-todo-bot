""" Telegram_User model file """

from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlmodel import Field

from .base import Base


class Telegram_User(Base, table=True):
    """
    Telegram_User model

    :param reg_datetime: Time and date of adding a Telegram account for the bot user.
    """

    id: int = Field(
        sa_column=sa.Column(
            sa.BigInteger, primary_key=True, autoincrement=True
        )
    )
    telegram_user_id: int = Field(sa_column=sa.Column(sa.BigInteger, nullable=False))
    id_user: UUID = Field(nullable=False, foreign_key="user.id")
    reg_datetime: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()
        )
    )

    def __repr__(self) -> str:
        return f"Telegram_User(id={self.id!r}, " \
               f"telegram_user_id={self.telegram_user_id!r}," \
               f"id_user={self.id_user!r})"
