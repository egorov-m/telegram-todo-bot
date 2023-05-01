""" User model file """

from sqlalchemy.dialects.postgresql import (
    UUID,
    VARCHAR,
    DATE,
    TIMESTAMP
)
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    """
    User model
    """

    id:               Mapped[int] = mapped_column(UUID, primary_key=True, nullable=False, autoincrement=True)
    current_language: Mapped[str] = mapped_column(VARCHAR(4), unique=False, nullable=False)
    username:         Mapped[str] = mapped_column(VARCHAR(64), unique=False, nullable=True)
    email:            Mapped[str] = mapped_column(VARCHAR(64), unique=True, nullable=True)
    phone:            Mapped[str] = mapped_column(VARCHAR(20), unique=False, nullable=True)
    reg_date:         Mapped[DATE] = mapped_column(DATE, nullable=False)
    reg_time:         Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    upd_date:         Mapped[DATE] = mapped_column(DATE, nullable=False)
    upd_time:         Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, " \
               f"current_language={self.current_language!r}" \
               f"username={self.username!r}, " \
               f"email={self.email!r}, " \
               f"phone={self.phone!r}, " \
               f"reg_date={self.reg_date!r}, " \
               f"reg_time={self.reg_time!r}, " \
               f"upd_date={self.upd_date!r}, " \
               f"upd_time={self.upd_time!r})"
