""" This file represent startup bot logic """

import asyncio
import logging as log

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from db.database import create_async_engine, get_session_maker
from src.config import settings
from src.logconfig import setup_logging
from src.lexicon.translator import Translator
from src.lexicon.translator import load_localizations
from bot.structures.data_structure import TransferData, LoggerType
from bot.dispatcher import get_dispatcher

logger = log.getLogger(LoggerType.BOT_LOGGER)


async def main() -> None:
    """Bot configuration and launch function
    """
    bot: Bot = Bot(token=settings.TELEGRAM_API_BOT_TOKEN, parse_mode='HTML')
    logger.info('Starting bot')

    redis = Redis(host=settings.REDIS_HOST,
                  port=settings.REDIS_PORT,
                  db=settings.REDIS_DB)

    storage: RedisStorage = RedisStorage(redis=redis)
    dp: Dispatcher = get_dispatcher(storage=storage, fsm_strategy=None)

    async_engine = create_async_engine(url=settings.get_postgres_url())
    sessionmaker = get_session_maker(async_engine)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, **TransferData(dispatcher=dp, pool=sessionmaker, translator=Translator()))

    # await set_main_menu(bot, lexicon)


if __name__ == '__main__':
    try:
        setup_logging()

        asyncio.run(load_localizations())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
