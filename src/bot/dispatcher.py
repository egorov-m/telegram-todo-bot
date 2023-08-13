from aiogram import Dispatcher
from aiogram.fsm.storage.redis import BaseStorage, RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from src.bot.routers import routers
from src.bot.middlewares import middlewares


def get_dispatcher(storage: BaseStorage, fsm_strategy: FSMStrategy, name: str = 'BotDispatcher') -> Dispatcher:
    """

    """

    # Router Registrations
    dp = Dispatcher(storage=storage, fsm_strategy=fsm_strategy, name=name)
    dp.include_routers(*routers)

    # Register middlewares
    for middleware in middlewares:
        dp.message.middleware(middleware)
        dp.callback_query.middleware(middleware)

    return dp
