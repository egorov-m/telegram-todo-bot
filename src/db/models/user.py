""" User model file """

from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field

from .base import Base


class User(Base, table=True):
    """
    User model
    """

    telegram_user_id: int = Field(sa_column=sa.Column(sa.BigInteger, primary_key=True))
    current_language: str = Field(nullable=False, max_length=5)  # format: en_US
    created_date: datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.func.current_timestamp())
    )
    enabled: bool = Field(sa_column=sa.Column(sa.Boolean, nullable=False, server_default=sa.true()))
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
               f"last_activity_date={self.last_activity_date!r}, " \
               f"user_agreement_acceptance_date={self.user_agreement_acceptance_date!r})"
