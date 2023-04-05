from aiogram import Bot
from aiogram.types import BotCommand

import lexicon as lx


async def set_main_menu(bot: Bot, lexicon: lx.LEXICON):
    main_menu_commands = [BotCommand(command=command,
                                     description=description)
                          for command, description in lexicon.commands.items()]
    await bot.set_my_commands(main_menu_commands)
