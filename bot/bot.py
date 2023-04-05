import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from keyboards import set_main_menu
from handlers import user_handlers, other_handlers
import lexicon as lx

logger = logging.getLogger(__name__)
lexicon: lx.LEXICON = lx.LEXICON_EN()

async def main() -> None:
    """Bot configuration and launch function
    """

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()

    bot: Bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot=bot)

    await set_main_menu(bot, lexicon)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
