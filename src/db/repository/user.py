""" User repository file """

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import DATE, TIMESTAMP

from ..models import User
from .abstract import Repository


class UserRepo(Repository[User]):
    """
    User repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize user repository
        """
        super().__init__(type_model=User, session=session)

    async def new(self,
                  current_language: Optional[str],
                  reg_date: Optional[DATE],
                  reg_time: Optional[TIMESTAMP],
                  upd_date: Optional[DATE],
                  upd_time: Optional[TIMESTAMP],
                  username: Optional[str] = None,
                  email: Optional[str] = None,
                  phone: Optional[str] = None
                  ) -> User:
        """
        Insert a new user into the database
        :param current_language The current language of the bot user interface
        :param reg_date Date of user registration
        :param reg_time Time of user registration
        :param upd_date The date the user was last updated
        :param upd_time The time the user was last updated
        :param username Current username in Telegram
        :param email Email specified by the user
        :param phone Phone specified by the user
        """

        new_user = await self.session.merge(
            User(
                current_language=current_language,
                reg_date=reg_date,
                reg_time=reg_time,
                upd_date=upd_date,
                upd_time=upd_time,
                username=username,
                email=email,
                phone=phone
            )
        )

        return new_user
