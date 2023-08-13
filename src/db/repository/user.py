import re
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.bot.structures.role import Role
from src.db.models import User
from src.db.utils import menage_db_method, CommitMode
from src.exceptions import ToDoBotError, ToDoBotErrorCode


class UserRepository:
    session: AsyncSession
    lang_pattern: str = r"^[a-z]{2}_[A-Z]{2}$"

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, telegram_user_id: int) -> User:
        user: User = await self.session.get(User, telegram_user_id)
        if user is None:
            raise ToDoBotError("User not found", ToDoBotErrorCode.USER_NOT_FOUND)

        return user

    @menage_db_method(CommitMode.FLUSH)
    async def create_user(self,
                          telegram_user_id: int,
                          *,
                          current_language: str = "en_US",
                          enabled: bool = True,
                          role: Role = Role.USER,
                          is_user_agreement_acceptance: bool = False) -> User:
        if not re.match(self.lang_pattern, current_language):
            raise ToDoBotError("The language is not in the correct format", ToDoBotErrorCode.USER_NOT_SPECIFIED)
        user: User = await self.session.get(User, telegram_user_id)
        if user is not None:
            raise ToDoBotError("The user already exists", ToDoBotErrorCode.USER_NOT_SPECIFIED)
        new_user: User = User(telegram_user_id=telegram_user_id,
                              enabled=enabled,
                              role=role,
                              current_language=current_language)
        if is_user_agreement_acceptance:
            new_user.user_agreement_acceptance_date = datetime.utcnow()

        self.session.add(new_user)
        return new_user

    @menage_db_method(CommitMode.FLUSH)
    async def update_user(self,
                          telegram_user_id: int,
                          *,
                          current_language: Optional[str] = None,
                          enabled: Optional[bool] = None,
                          role: Optional[Role] = None,
                          last_activity_date: Optional[datetime] = None,
                          user_agreement_acceptance_date: Optional[datetime] = None) -> User:
        user: User = await self.get_user(telegram_user_id)

        if current_language is not None:
            user.current_language = current_language
        if enabled is not None:
            user.enabled = enabled
        if role is not None:
            user.role = role
        if last_activity_date is not None:
            user.last_activity_date = last_activity_date
        if user_agreement_acceptance_date is not None:
            user.user_agreement_acceptance_date = user_agreement_acceptance_date

        return user

    @menage_db_method(CommitMode.FLUSH)
    async def update_user_last_activity(self, telegram_user_id: int) -> User:
        current_time = datetime.utcnow()
        user = await self.get_user(telegram_user_id)
        user.last_activity_date = current_time
        return user
