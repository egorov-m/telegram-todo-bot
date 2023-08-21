import re
from datetime import datetime
from typing import Optional

from sqlalchemy import desc, and_, or_, cast, String
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.sql.functions import count, func
from sqlmodel import select

from src.db.models import Task
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

    async def get_users(self,
                        active_user: User,
                        *,
                        offset: int = 0,
                        limit: int = 5,
                        order: UnaryExpression = desc(User.created_date)) -> list[User]:
        if active_user.role != Role.ADMINISTRATOR:
            raise ToDoBotError("Only the administrator can retrieve users", ToDoBotErrorCode.USER_NOT_SPECIFIED)

        result: Result = await self.session.execute(
            select(User).where(User.telegram_user_id != active_user.telegram_user_id)
            .order_by(order, desc(User.telegram_user_id)).offset(offset).fetch(limit)
        )
        return result.scalars().all()

    async def get_users_with_more_info(self,
                                       active_user: User,
                                       *,
                                       search_text: Optional[str] = None,
                                       offset: int = 0,
                                       limit: int = 5,
                                       order: UnaryExpression = desc(User.created_date)) -> list:
        if active_user.role != Role.ADMINISTRATOR:
            raise ToDoBotError("Only the administrator can retrieve users", ToDoBotErrorCode.USER_NOT_SPECIFIED)

        conditions = [User.telegram_user_id != active_user.telegram_user_id]
        if search_text is not None:
            text: str = f"%{search_text}%"
            conditions.append(or_(cast(User.telegram_user_id, String).ilike(text),
                                  User.username.ilike(text),
                                  User.first_name.ilike(text),
                                  User.last_name.ilike(text)))

        result: Result = await self.session.execute(
            select(User.enabled,
                   User.username,
                   User.telegram_user_id,
                   User.first_name,
                   User.last_name,
                   func.count(Task.id),
                   func.count(Task.id).filter(Task.is_done == True))
            .join(Task, Task.creator_telegram_user_id == User.telegram_user_id, full=True)
            .where(and_(*conditions))
            .group_by(User.telegram_user_id,
                      User.enabled,
                      User.username,
                      User.first_name,
                      User.last_name)
            .order_by(order, desc(User.telegram_user_id)).offset(offset).fetch(limit)
        )

        return result.all()

    async def get_count_users(self, active_user: Optional[User] = None, search_text: Optional[str] = None) -> int:
        conditions = []
        if active_user is not None:
            conditions.append(User.telegram_user_id != active_user.telegram_user_id)
            if search_text is not None:
                text: str = f"%{search_text}%"
                conditions.append(or_(cast(User.telegram_user_id, String).ilike(text),
                                      User.username.ilike(text),
                                      User.first_name.ilike(text),
                                      User.last_name.ilike(text)))
        result: Result = await self.session.execute(
            select(count(User.telegram_user_id)).where(and_(*conditions))
        )

        return int(result.scalars().all()[0])

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
                          username: Optional[str] = None,
                          first_name: Optional[str] = None,
                          last_name: Optional[str] = None,
                          current_language: Optional[str] = None,
                          enabled: Optional[bool] = None,
                          role: Optional[Role] = None,
                          last_activity_date: Optional[datetime] = datetime.utcnow(),
                          user_agreement_acceptance_date: Optional[datetime] = None) -> User:
        user: User = await self.get_user(telegram_user_id)

        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
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
