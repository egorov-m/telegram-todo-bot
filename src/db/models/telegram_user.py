""" Telegram_User model file """

from sqlalchemy.dialects.postgresql import (
    UUID,
    BIGINT
)
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Telegram_User(Base):
    """
    Telegram_User model
    """

    id:               Mapped[int] = mapped_column(BIGINT, primary_key=True, nullable=False, autoincrement=True)
    telegram_user_id: Mapped[BIGINT] = mapped_column(BIGINT, nullable=False)
    id_user:          Mapped[UUID] = mapped_column(UUID, nullable=False)

    def __repr__(self) -> str:
        return f"Telegram_User(id={self.id!r}, " \
               f"telegram_user_id={self.telegram_user_id!r}," \
               f"id_user={self.id_user!r})"
