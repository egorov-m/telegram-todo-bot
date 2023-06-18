""" User model file """

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field

from .base import Base


class User(Base, table=True):
    """
    User model
    """

    id: UUID = Field(
        sa_column=sa.Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid4, server_default=sa.text("gen_random_uuid()")
        )
    )
    current_language: str = Field(nullable=False, max_length=5)  # format: en_US
    login: str = Field(nullable=False, unique=True, max_length=50)
    phone: Optional[str] = Field(nullable=True, unique=True, max_length=20)
    reg_datetime: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()
        )
    )
    upd_datetime: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp()
        )
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, " \
               f"current_language={self.current_language!r}" \
               f"login={self.login!r}, " \
               f"phone={self.phone!r}, " \
               f"reg_datetime={self.reg_datetime!r}, " \
               f"upd_datetime={self.upd_datetime!r})"
