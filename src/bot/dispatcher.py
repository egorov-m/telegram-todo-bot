from aiogram import Dispatcher
from aiogram.fsm.storage.redis import BaseStorage, RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from src.config import DbRedisConfig
from redis import Redis

from src.bot.routers import routers
from src.bot.middlewares.translator import TranslatorMiddleware


def get_redis_storage(config: DbRedisConfig) -> RedisStorage:
    """
    Creating a Redis storage
    """
    return RedisStorage(redis=Redis(host=config.db_host,
                                    port=config.db_port,
                                    db=config.db_name,
                                    username=config.db_user,
                                    password=config.db_password))


def get_dispatcher(storage: BaseStorage, fsm_strategy: FSMStrategy, name: str = 'BotDispatcher') -> Dispatcher:
    """

    """

    # Router Registrations
    dp = Dispatcher(storage=storage, fsm_strategy=fsm_strategy, name=name)
    dp.include_routers(*routers)

    # Register middlewares
    dp.message.middleware(TranslatorMiddleware())
    dp.callback_query.middleware(TranslatorMiddleware())

    return dp
