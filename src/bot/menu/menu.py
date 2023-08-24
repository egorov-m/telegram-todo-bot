from aiogram import Bot
from aiogram.types import BotCommand

from src.bot.structures.bot import BotCmd
from src.lexicon import Translator


async def set_main_menu(bot: Bot):
    translator: Translator = Translator()
    await bot.set_my_commands(await _add_command(translator))


async def _add_command(translator: Translator) -> list[BotCommand]:
    commands = [
        BotCommand(command=await translator.translate(BotCmd.CMD_START_TITLE),
                   description=await translator.translate(BotCmd.CMD_START_DESCRIPTION)),
        BotCommand(command=await translator.translate(BotCmd.CMD_HELP_TITLE),
                   description=await translator.translate(BotCmd.CMD_HELP_DESCRIPTION)),
    ]
    return commands
