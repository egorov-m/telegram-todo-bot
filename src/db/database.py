from typing import Union

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from .repository import (
    UserRepo,
    TaskRepo,
    TelegramUserRepo
)


def create_async_engine(url: Union[URL, str], echo: bool = False) -> AsyncEngine:
    """
    Creating an async database engine
    :param url Address for connection in the database
    :param echo Output SQL queries to the standard output stream
    :return:
    """
    return _create_async_engine(url=url, echo=echo, encoding='utf-8', pool_pre_ping=True)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)


class Database:
    """
    Database class is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions
    """

    user: UserRepo
    task: TaskRepo
    telegram_user: TelegramUserRepo

    session: AsyncSession

    def __init__(self,
                 session: AsyncSession,
                 user: UserRepo = None,
                 task: TaskRepo = None,
                 telegram_user: TelegramUserRepo = None
                 ):

        self.session = session
        self.user = user or UserRepo(session=session)
        self.task = task or TaskRepo(session=session)
        self.telegram_user = telegram_user or TelegramUserRepo(session=session)