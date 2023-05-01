""" This file represent startup bot logic"""

import asyncio
import logging as log

from aiogram import Bot, Dispatcher

from config import Config, load_config
from logconfig import setup_logging
from keyboards import set_main_menu
from handlers import user_handlers, other_handlers, callback
from db.database import create_async_engine
from db.database import get_session_maker
import lexicon as lx

logger = log.getLogger('bot_logger')
lexicon: lx.LEXICON = lx.LEXICON_EN()


async def main() -> None:
    """Bot configuration and launch function
    """
    config: Config = load_config()
    bot: Bot = Bot(token=config.bot.token, parse_mode='HTML')
    logger.info('Starting bot')

    async_engine = create_async_engine(url=config.dbPostgres.get_url)
    sessionmaker = get_session_maker(async_engine)

    dp: Dispatcher = Dispatcher(bot=bot)

    await set_main_menu(bot, lexicon)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(callback.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, sessionmaker=sessionmaker)


if __name__ == '__main__':
    try:
        setup_logging()

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
