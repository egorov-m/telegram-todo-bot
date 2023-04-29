from typing import Union

from sqlalchemy.engine import (
    create_async_engine as _create_async_engine,
    URL
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: Union[URL, str], echo: bool = False) -> AsyncEngine:
    return _create_async_engine(url=url, echo=echo, encoding='utf-8', pool_pre_ping=True)


def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    with engine.connect() as connection:
        connection.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
