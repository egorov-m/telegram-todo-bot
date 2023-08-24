""" User model file """

from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field

from src.bot.structures.role import Role
from src.db.models.base import Base


class User(Base, table=True):
    """
    User model
    """

    telegram_user_id: int = Field(sa_column=sa.Column(sa.BigInteger, primary_key=True))
    username: Optional[str] = Field(nullable=True, max_length=32, min_length=5)
    first_name: Optional[str] = Field(nullable=True, max_length=255)
    last_name: Optional[str] = Field(nullable=True, max_length=255)
    current_language: str = Field(nullable=False, max_length=5)  # format: en_US
    created_date: datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp())
    )
    enabled: bool = Field(sa_column=sa.Column(sa.Boolean, nullable=False, server_default=sa.true()))
    role: Role = Field(sa_column=sa.Column(sa.Enum(Role), nullable=False, default=Role.USER))
    last_activity_date: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True, server_default=sa.func.current_timestamp())
    )
    user_agreement_acceptance_date: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True))

    def __repr__(self) -> str:
        return f"User(telegram_user_id={self.telegram_user_id!r}, " \
               f"current_language={self.current_language!r}" \
               f"created_date={self.created_date!r}, " \
               f"enabled={self.enabled!r}, " \
               f"role={self.role!r}, " \
               f"last_activity_date={self.last_activity_date!r}, " \
               f"user_agreement_acceptance_date={self.user_agreement_acceptance_date!r})"
