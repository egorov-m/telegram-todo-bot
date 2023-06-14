from sqlalchemy.dialects.postgresql import (
    UUID,
    BIGINT,
    VARCHAR,
    BOOLEAN,
    DATE,
    TIMESTAMP
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class Task(Base):
    """
    Task model
    """

    id:                   Mapped[UUID] = mapped_column(UUID, primary_key=True, nullable=False, autoincrement=True)
    title:                Mapped[str] = mapped_column(VARCHAR(64), unique=False, nullable=False)
    description:          Mapped[str] = mapped_column(VARCHAR(256), unique=False, nullable=True)
    reg_telegram_user_id: Mapped[int] = mapped_column(BIGINT, unique=False, nullable=False)
    reg_date:             Mapped[DATE] = mapped_column(DATE, nullable=False)
    reg_time:             Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    isDone:               Mapped[bool] = mapped_column(BOOLEAN, unique=False, nullable=False)
    isExist:              Mapped[bool] = mapped_column(BOOLEAN, unique=False, nullable=False)
    id_user:              Mapped[UUID] = mapped_column(ForeignKey("user.id"), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}," \
               f"title={self.title!r}," \
               f"description={self.description!r}," \
               f"reg_telegram_user_id={self.reg_telegram_user_id!r}," \
               f"reg_date={self.reg_date!r}," \
               f"reg_time={self.reg_time!r}," \
               f"isDone={self.isDone!r}," \
               f"isExist={self.isExist!r}," \
               f"idUser={self.id_user!r})"
