""" Telegram User repository file """

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID, BIGINT

from ..models import Telegram_User
from .abstract import Repository


class TelegramUserRepo(Repository[Telegram_User]):
    """
    Telegram user repository for CRUD and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize telegram user repository
        """
        super().__init__(type_model=Telegram_User, session=session)

    async def new(self,
                  telegram_user_id: Optional[BIGINT],
                  id_user: Optional[UUID]
                  ):
        """
        Insert a new telegram user id for user into the database
        :param telegram_user_id Telegram user id
        :param id_user User ID in the database
        """

        new_telegram_user_id = await self.session.merge(
            Telegram_User(
                telegram_user_id=telegram_user_id,
                id_user=id_user
            )
        )

        return new_telegram_user_id
