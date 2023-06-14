""" This file represent startup bot logic """

import asyncio
import logging as log

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.context import FSMContext
from redis.asyncio import Redis
from src.config import Config, load_config
from src.logconfig import setup_logging
from src.lexicon.translator import Translator
# from keyboards import set_main_menu
# from handlers import user_handlers, other_handlers, callback
# from db.database import create_async_engine
# from db.database import get_session_maker
from src.lexicon.translator import load_localizations
from .structures.data_structure import TransferData
from .dispatcher import get_dispatcher

logger = log.getLogger('bot_logger')


async def main() -> None:
    """Bot configuration and launch function
    """
    config: Config = load_config()
    bot: Bot = Bot(token=config.bot.token, parse_mode='HTML')
    logger.info('Starting bot')

    # redis = Redis(host=config.dbRedis.db_host,
    #               port=config.dbRedis.db_port,
    #               db=config.dbRedis.db_name,
    #               username=config.dbRedis.db_user,
    #               password=config.dbRedis.db_password)

    # storage: RedisStorage = RedisStorage(redis=redis)
    storage: MemoryStorage = MemoryStorage()
    # strategy: FSMStrategy = FSMStrategy()
    dp: Dispatcher = get_dispatcher(storage=storage, fsm_strategy=None)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, **TransferData(dp=dp, translator=Translator()))

    # async_engine = create_async_engine(url=config.dbPostgres.get_url)
    # sessionmaker = get_session_maker(async_engine)

    # await set_main_menu(bot, lexicon)

    # await bot.delete_webhook(drop_pending_updates=True)
    # await dp.start_polling(bot, sessionmaker=sessionmaker)


if __name__ == '__main__':
    try:
        setup_logging()

        asyncio.run(load_localizations())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
